'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from comtypes import COMError
from accessibility_api.accessibility_lib.wrappers.BaseAccessible import (
    BaseAccessible
)
from accessibility_api.accessibility_lib.utils.WinUtil import WinUtil
from ..scripts.constants import (
    CHILDID_SELF, NO_CHILD_TREE
)
from ..scripts.debug import simple_element_atrribute

FLAT_PROPERTIES = [
    'accChildCount', 'accDefaultAction',
    'accDescription', 'accHelp', 'accHelpTopic',
    'accKeyboardShortcut', 'accLocation', 'accName',
    'accRole', 'accState', 'accValue'
]
TREE_PROPERTIES = ['accChildren', 'accParent', 'accFocus', 'accSelection']


class IAccessible(BaseAccessible):
    """
    IAccessible windows interface
    """

    def __init__(self, params):
        super(IAccessible, self).__init__(params)
        # Find accessible object associated with ID
        self.simple_elements = dict()
        self._target = WinUtil.get_target_accessible(params,
                                                     self.simple_elements)
        self.depth = None

    def serialize_result(self, depth):
        """
        Return accessible object
        """

        self.depth = depth

        if self._target is None:
            return {
                'error': True,
                'message': 'No accessible found'
            }
        else:
            return {
                'result': {'IAccessible': self._serialize()},
                'target': self._target,
                'semantic_wrap': self.semantic_wrap
            }

    def _serialize(self):
        """
        Serialize accessible into json
        """

        attributes = FLAT_PROPERTIES[:]
        attributes.extend(TREE_PROPERTIES)
        childid = CHILDID_SELF

        # If object is simple element remove irrelevant children fields
        if self.is_simple_element(self._target):
            attributes.remove('accChildren')
            childid = self._target.childId

        return self.to_json(self._target, attributes, childid)

    def semantic_wrap(self, acc_ptr, child_id=CHILDID_SELF):
        """
        Wrap children and parent pointers exposing semantics
        """

        # Handle cases when accessible object doesn't have:
        # keyboard focus
        # parent accessible
        if acc_ptr is None:
            return None

        attributes = FLAT_PROPERTIES[:]
        return self.to_json(acc_ptr, attributes, child_id)

    def to_json(self, acc_ptr, attributes, child_id=CHILDID_SELF):
        """
        Does parsing of fields and determines call type for value
        """

        json = {}
        prefix = 'acc'

        # For debugging add field to show child is simple element
        simple_element_atrribute(json, child_id)

        for attribute in attributes:
            field = attribute[len(prefix):]

            if attribute in TREE_PROPERTIES:
                if field == 'Children':
                    if acc_ptr.accChildCount == 0:
                        continue
                    json[field] = getattr(self, 'get_' + field.lower())()\
                        .get('Children')
                else:
                    json[field] = getattr(self, 'get_' + field.lower())()
            else:
                if callable(getattr(acc_ptr, attribute)):
                    try:
                        json[field] = getattr(acc_ptr, attribute)(child_id)
                    except AttributeError:
                        json[field] = 'Attribute Not Supported'
                    except COMError:
                        json[field] = 'Member Not Found'
                else:
                    json[field] = getattr(acc_ptr, attribute)

        return json

    def get_focus(self):
        """
        Get focused object
        """

        focus_val = getattr(self._target, 'accFocus')
        return self.process_return(self._target, focus_val)

    def get_selection(self):
        """
        Get selected object
        """

        select_val = getattr(self._target, 'accSelection')
        return self.process_return(self._target, select_val)

    def process_return(self, acc_ptr, value):
        """
        Handle multiple return types
        """

        if value is None:
            return None
        elif isinstance(value, int):
            if self.is_simple_element(acc_ptr):
                return self.semantic_wrap(acc_ptr, value)
            else:
                return self.semantic_wrap(acc_ptr.accChild(value))
        else:
            return self.semantic_wrap(value)

    def get_parent(self):
        """
        Get parent object
        """

        parent = getattr(self._target, 'accParent')
        return self.semantic_wrap(parent)

    def get_children(self):
        """
        Get children of accessible
        """

        tree = {}
        return self.get_children_impl(self._target, self.depth, tree)

    def get_children_impl(self, acc_ptr, child_depth, tree):
        """
        Get child accessible
        """

        # Check if there are children
        if acc_ptr.accChildCount is 0:
            return

        # Determine depth of children
        if child_depth is NO_CHILD_TREE:
            return

        # Decrease child depth on each traversal
        child_depth -= 1

        # First is used to determine if a children field should wrap list
        children_ptrs = WinUtil.accessible_children(acc_ptr,
                                                    self.simple_elements)

        # Check if children are simple elements
        if self.is_simple_element(acc_ptr):
            tree['Children'] = [self.semantic_wrap(acc_ptr, i)
                                for i in range(1, acc_ptr.accChildCount + 1)]
            return

        tree['Children'] = map(self.semantic_wrap, children_ptrs)

        for index, child_ptr in enumerate(children_ptrs):
            self.get_children_impl(child_ptr, child_depth,
                                   tree['Children'][index])

        return tree

    def is_simple_element(self, acc_ptr):
        """
        Determine if object is simple element
        """

        try:
            if acc_ptr.is_simple_element:
                return True
        except AttributeError:
            if acc_ptr in self.simple_elements:
                return True
            else:
                return False
