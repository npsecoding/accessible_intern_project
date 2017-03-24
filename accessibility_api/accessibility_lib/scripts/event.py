'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from platform import system
from accessibility_api.accessibility_lib.events.WinEventHandler import (
    WinEventHandler
)


def event(interface_t, event_t, _identifiers):
    """Instantiate EventHandler object"""
    protocol = {
        'Windows': WinEventHandler
    }
    return protocol[system()](interface_t, event_t, _identifiers)
