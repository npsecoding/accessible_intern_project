'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from exceptions import WindowsError
from ctypes import windll, oledll, byref, POINTER
from ctypes.wintypes import c_char_p, c_long
from comtypes.automation import VARIANT
from accessibility_api.accessibility_lib.scripts.constants import (
    CHILDID_SELF, S_OK, OBJID_WINDOW,
    IAccessible_t, IID_IAccessible,
    VT_DISPATCH, VT_I4
)
from accessibility_api.accessibility_lib.scripts.debug import (
    print_accessible, print_simple, print_test_window
)


class WinUtil(object):
    """
    Utility definition for Windows Platform
    """

    @staticmethod
    def _accessible_object_from_window(hwnd, simple_elements):
        """
        Get the accessible object for window
        """

        acc_ptr = POINTER(IAccessible_t)()
        try:
            res = oledll.oleacc.AccessibleObjectFromWindow(
                hwnd, OBJID_WINDOW, byref(IID_IAccessible), byref(acc_ptr))
        except WindowsError:
            raise Exception('Specified application not open')

        if res == S_OK:
            acc_ptr.children = WinUtil.accessible_children(acc_ptr,
                                                           simple_elements)
            return acc_ptr
        else:
            raise ValueError('Failed to get accessible from window')

    @staticmethod
    def accessible_children(acc_ptr, simple_elements):
        """
        Get the children of an accessible object
        """

        ichild_start = 0
        cc_children = acc_ptr.accChildCount
        pc_obtained = c_long()
        variant_array_type = VARIANT * cc_children
        rgvar_children = variant_array_type()
        res = oledll.oleacc.AccessibleChildren(acc_ptr, ichild_start,
                                               cc_children,
                                               byref(rgvar_children),
                                               byref(pc_obtained))

        if res == S_OK:
            acc_objs = []
            for child in rgvar_children:
                # Child is IAccessible
                if child.vt == VT_DISPATCH:
                    acc = child.value.QueryInterface(IAccessible_t)
                    acc_objs.append(acc)
                # Child is Simple Element
                elif child.vt == VT_I4:
                    WinUtil._wrap_simple_element(acc_ptr, child.value,
                                                 simple_elements)
                else:
                    acc_objs.append(None)
            return acc_objs
        else:
            raise ValueError('Failed to get accessible children')

    @staticmethod
    def _wrap_simple_element(acc_ptr, childid, simple_elements):
        """
        Associate simple element and parent accessible object
        """

        if acc_ptr not in simple_elements:
            simple_elements[acc_ptr] = [childid]
        else:
            simple_elements[acc_ptr].append(childid)

    @staticmethod
    def _traverse(node, visited, search_criteria, state):
        """
        Traverse through accessible tree looking for node with the given ID
        """

        if WinUtil.match_criteria(node, search_criteria):
            state['target'] = node
            state['target'].isSimpleElement = False
            return

        print_accessible(node)

        # Retrieve simple children or accessible children from node
        acc_children = \
            WinUtil.accessible_children(node, state.get('simple_elements'))

        # Traverse through simple elements of node
        if node in state.get('simple_elements'):
            for childid in state.get('simple_elements')[node]:
                print_simple(node, childid)

                if WinUtil.match_criteria(node, search_criteria, childid):
                    state['target'] = node
                    state['target'].isSimpleElement = True
                    state['target'].childId = childid
                    return

        # Traverse through accessible objects of node
        for child in acc_children:
            if child not in visited:
                visited.add(node)
                WinUtil._traverse(child, visited, search_criteria, state)

    @staticmethod
    def get_indentifiers(params):
        """
        Get accessibility indentifiers
        """

        identifiers = {
            'Name': params.get('name'),
            'Role': params.get('role')
        }
        filtered_identifiers = {k: v for k, v in identifiers.items() if v}

        return filtered_identifiers

    @staticmethod
    def match_criteria(node, params, child_id=CHILDID_SELF):
        """
        Find matching accessible with given criteria
        """

        search_criteria = WinUtil.get_indentifiers(params)
        for criteria in search_criteria:
            prefix = 'acc'
            prop_value = getattr(node, prefix + criteria)(child_id)
            search_value = search_criteria[criteria]

            # If value is a number convert from unicode to int
            if isinstance(prop_value, int):
                search_value = int(search_value)

            if prop_value != search_value:
                return False

        return True

    @staticmethod
    def _get_test_window(test_window_name, simple_elements):
        """
        Get test window handle
        """

        # Get the window for browser
        test_class = c_char_p('MozillaWindowClass')
        current_hwnd = windll.user32.FindWindowA(test_class, None)
        name = (
            WinUtil._accessible_object_from_window(current_hwnd,
                                                   simple_elements)
            .accName(CHILDID_SELF)
        )

        # Iterate through windows
        while name is None or test_window_name not in name:
            current_hwnd = (
                windll.user32
                .FindWindowExA(None, current_hwnd, test_class, None)
            )
            name = (
                WinUtil._accessible_object_from_window(current_hwnd,
                                                       simple_elements)
                .accName(CHILDID_SELF)
            )
        return current_hwnd

    @staticmethod
    def get_root_accessible(app_window, simple_elements):
        """
        Set root accessible object to test window
        """

        test_window = WinUtil._get_test_window(app_window, simple_elements)
        print_test_window(test_window)
        root = WinUtil._accessible_object_from_window(test_window,
                                                      simple_elements)
        return root

    @staticmethod
    def get_target_accessible(params, state):
        """
        Retrieve the accessible object for the given ID
        """

        root = WinUtil.get_root_accessible(params.get('window'),
                                           state.get('simple_elements'))
        state.get('visited').add(root)
        WinUtil._traverse(root, state.get('visited'),
                          params, state)

