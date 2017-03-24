'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from accessibility_api.accessibility_lib.wrappers.BaseIAccessible import (
    BaseIAccessible
)


class IAccessible2(BaseIAccessible):
    """IA2 windows protocol"""
    def __init__(self, identifiers):
        super(IAccessible2, self).__init__()
        # Find accessible object associated with ID
        self._target = self._util.get_target_accessible(identifiers)
        ia2 = self._util.IAccessible_to_IAccessible2(self._target)
        print ia2

    def serialize(self, child_depth=-1):
        """Convert pointer to object for serialization"""
        # TODO
