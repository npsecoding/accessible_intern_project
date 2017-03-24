'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''


class IEventHandler(object):
    """EventHandler Object Interface Definition"""
    def __init__(self, interface_t, identifiers):
        self.info = {
            'INTERFACE': interface_t,
            'IDENTIFIERS': identifiers
        }

    def register_event_hook(self, event):
        """Track specific event"""
        raise NotImplementedError

    def unregesiter_event_hook(self):
        """Untrack specific event"""
        raise NotImplementedError

    def listen_events(self):
        """Listen for tracked events"""
        raise NotImplementedError

