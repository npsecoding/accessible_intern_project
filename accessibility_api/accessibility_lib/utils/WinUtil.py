'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from ctypes import windll, oledll, byref, POINTER
from ctypes.wintypes import c_char_p, c_long
from comtypes.automation import VARIANT
from accessibility_api.accessibility_lib.scripts.constants import *
from accessibility_api.accessibility_lib.scripts.debug import *


class WinUtil(object):
    """
    Utility definition for Windows Platform
    """
    simple_elements = None
    target = None

    @staticmethod
    def _accessible_object_from_window(hwnd):
        """
        Get the accessible object for window
        """
        acc_ptr = POINTER(IAccessible_t)()
        res = oledll.oleacc.AccessibleObjectFromWindow(
            hwnd, OBJID_WINDOW, byref(IID_IAccessible), byref(acc_ptr))

        if res == S_OK:
            acc_ptr.children = WinUtil._accessible_children(acc_ptr)
            return acc_ptr
        else:
            raise ValueError("Can't get accessible from window")

    @staticmethod
    def _accessible_children(accptr):
        """
        Get the children of an accessible object
        """
        ichild_start = 0
        cc_children = accptr.accChildCount
        pc_obtained = c_long()
        variant_array_type = VARIANT * cc_children
        rgvar_children = variant_array_type()
        res = oledll.oleacc.AccessibleChildren(accptr, ichild_start,
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
                    WinUtil._wrap_simple_element(accptr, child.value)
            return acc_objs
        else:
            raise ValueError("Can't get accessible children")

    @staticmethod
    def _wrap_simple_element(accptr, childid):
        """
        Associate simple element and parent accessible object
        """
        if accptr not in WinUtil.simple_elements:
            WinUtil.simple_elements[accptr] = [childid]
        else:
            WinUtil.simple_elements[accptr].append(childid)

    @staticmethod
    def _match_criteria(node, search_criteria, child_id=CHILDID_SELF):
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
    def _traverse(node, visited, search_criteria):
        """
        Traverse through accessible tree looking for node with the given ID
        """

        if WinUtil._match_criteria(node, search_criteria):
            WinUtil.target = node
            WinUtil.target.isSimpleElement = False
            return

        if DEBUG_ENABLED:
            print_accessible(node)

        # Retrieve simple children or accessible children from node
        acc_children = WinUtil._accessible_children(node)

        # Traverse through simple elements of node
        if node in WinUtil.simple_elements:
            for childid in WinUtil.simple_elements[node]:
                if DEBUG_ENABLED:
                    print_simple(node, childid)

                if WinUtil._match_criteria(node, search_criteria, childid):
                    WinUtil.target = node
                    WinUtil.target.isSimpleElement = True
                    WinUtil.target.childId = childid
                    return

        # Traverse through accessible objects of node
        for child in acc_children:
            if child not in visited:
                visited.add(node)
                WinUtil._traverse(child, visited, search_criteria)

    @staticmethod
    def _get_test_window():
        # Get the window for browser
        test_class = c_char_p("MozillaWindowClass")
        current_hwnd = windll.user32.FindWindowA(test_class, None)
        name = (
            WinUtil._accessible_object_from_window(current_hwnd)
            .accName(CHILDID_SELF)
        )
        # Iterate through windows
        while name is None or 'Marionette Accessible' not in name:
            current_hwnd = (
                windll.user32
                .FindWindowExA(None, current_hwnd, test_class, None)
            )
            name = (
                WinUtil._accessible_object_from_window(current_hwnd)
                .accName(CHILDID_SELF)
            )
        return current_hwnd

    @staticmethod
    def get_root_accessible():
        """
        Set root accessible object to test window
        """
        test_window = WinUtil._get_test_window()
        print 'Test Window: %d' % test_window
        root = WinUtil._accessible_object_from_window(test_window)
        return root

    @staticmethod
    def get_target_accessible(search_criteria):
        """
        Retrieve the accessible object for the given ID
        """
        WinUtil.simple_elements = dict()
        root = WinUtil.get_root_accessible()
        visited = set()
        visited.add(root)
        WinUtil.target = None
        WinUtil._traverse(root, visited, search_criteria)
        return WinUtil.target
