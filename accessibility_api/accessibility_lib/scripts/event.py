'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from platform import system
from accessibility_api.accessibility_lib.events.WinEventHandler import (
    WinEventHandler
)


def event(params):
    """Instantiate EventHandler object"""

    event_t = params.get('type')
    protocol = {
        'Windows': WinEventHandler
    }

    return protocol[system()](event_t, params)
