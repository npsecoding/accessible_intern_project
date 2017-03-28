'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''


class IEventHandler(object):
    """
    EventHandler Object Interface Definition
    """

    def __init__(self, params):
        self.params = params
        self.interface_t = params.get('interface')
        identifiers = {
            'Name': params.get('name'),
            'Role': params.get('role')
        }
        self.filtered_identifiers = {k: v for k, v in identifiers.items() if v}

    def serialize_result(self):
        """
        Event serialized to JSON
        """
        raise NotImplementedError

    def register_event_hook(self, event):
        """
        Track specific event
        """
        raise NotImplementedError

    def unregesiter_event_hook(self):
        """
        Untrack specific event
        """
        raise NotImplementedError

    def listen_events(self):
        """
        Listen for tracked events
        """
        raise NotImplementedError

