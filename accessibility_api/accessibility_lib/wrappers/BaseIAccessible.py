'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''


class BaseIAccessible(object):
    """Accessible Object Interface Definition"""
    def __init__(self, params):
        identifiers = {
            'Name': params.get('name'),
            'Role': params.get('role')
        }
        self.filtered_identifiers = {k: v for k, v in identifiers.items() if v}

    def serialize_result(self, depth=-1):
        """Accessible Object to JSON"""
        raise NotImplementedError

