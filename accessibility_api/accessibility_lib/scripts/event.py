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
    """
    Instantiate EventHandler object
    """

    event_t = params.get('type')
    if event_t is None:
        return {
            'error': True,
            'message': 'No event type given'
        }

    protocol = {
        'Windows': WinEventHandler
    }

    return protocol[system()](event_t, params).serialize_result()
