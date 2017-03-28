'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from ctypes import byref, wintypes, windll, oledll, POINTER, WINFUNCTYPE
from comtypes.client import PumpEvents
from comtypes.automation import VARIANT
from accessibility_api.accessibility_lib.scripts.accessible import accessible
from accessibility_api.accessibility_lib.events.IEventHandler import (
    IEventHandler
)
from accessibility_api.accessibility_lib.scripts.constants import (
    IAccessible_t, S_OK, CHILDID_SELF,
    TIMEOUT, WIN_EVENT_NAMES, WINEVENT_OUTOFCONTEXT
)
from accessibility_api.accessibility_lib.scripts.debug import DEBUG_ENABLED
from accessibility_api.accessibility_lib.scripts.constants import (
    SUCCESS, ERROR
)


INVALID_EVENT = -1


class WinEventHandler(IEventHandler):
    """
    Handle Windows Events
    """

    # Store information about event used between callback and handler
    info = {}
    found = None

    # Helper function to find matching accessible
    @staticmethod
    def _match_criteria(acc_ptr, child_id=CHILDID_SELF):
        search_criteria = WinEventHandler.filtered_identifiers

        for criteria in search_criteria:
            prefix = 'acc'
            prop_value = getattr(acc_ptr, prefix + criteria)(child_id)
            search_value = search_criteria[criteria]

            # If value is a number convert from unicode to int
            if isinstance(prop_value, int):
                search_value = int(search_value)

            if prop_value != search_value:
                return False

        return True

    # Callback function
    @staticmethod
    def accessible_from_event(hWinEventHook, event, hwnd, idObject,
                              idChild, dwEventThread, dwmsEventTime):
        """
        Get accessible object from event
        """

        acc_ptr = POINTER(IAccessible_t)()
        var_child = VARIANT()
        result = oledll.oleacc.AccessibleObjectFromEvent(
            hwnd, idObject, idChild, byref(acc_ptr), byref(var_child))
        if S_OK != result:
            return

        if DEBUG_ENABLED:
            print acc_ptr.accName(idChild)

        if WinEventHandler._match_criteria(acc_ptr, idChild):
            WinEventHandler.found = {
                'Child_Id': idChild,
                WinEventHandler.interface_t:
                    accessible(WinEventHandler.params).get('result')
            }

    # Callback type
    WINPROC_TYPE = WINFUNCTYPE(
        None,
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.HWND,
        wintypes.LONG,
        wintypes.LONG,
        wintypes.DWORD,
        wintypes.DWORD
    )

    # Declare callback function
    WINEVENT_PROC = WINPROC_TYPE(accessible_from_event.__func__)

    def register_event(self, event_start, event_end):
        """
        Set hook for event
        """

        hook_result = windll.user32.SetWinEventHook(
            event_start,
            event_end,
            None,
            self.WINEVENT_PROC,
            0,
            0,
            WINEVENT_OUTOFCONTEXT
        )
        return hook_result

    def __init__(self, event_t, params):
        super(WinEventHandler, self).__init__(params)
        WinEventHandler.params = self.params
        WinEventHandler.interface_t = self.interface_t
        WinEventHandler.type_t = event_t
        WinEventHandler.filtered_identifiers = self.filtered_identifiers
        WinEventHandler.found = None

        self.hook = self.register_event_hook(event_t)
        print 'Registered ' + event_t + ' hook'
        if self.hook != INVALID_EVENT:
            self.listen_events()

    def serialize_result(self):
        """
        Return event object
        """
        if WinEventHandler.found is None:
            return {
                'error': ERROR,
                'result': None
            }
        else:
            interface_t = WinEventHandler.interface_t
            return {
                'error': SUCCESS,
                'result': {WinEventHandler.type_t:
                           WinEventHandler.found[interface_t]}
            }

    def register_event_hook(self, event):
        """
        Register callback for event type
        """

        if event in WIN_EVENT_NAMES.values():
            event_index = WIN_EVENT_NAMES.values().index(event)
            event_type = WIN_EVENT_NAMES.keys()[event_index]
            return self.register_event(event_type, event_type)
        else:
            return INVALID_EVENT

    def unregesiter_event_hook(self):
        """
        Unregister callback for event type
        """

        result = windll.user32.UnhookWinEvent(self.hook)
        return result

    def listen_events(self):
        """
        Get registered events and trigger callback
        """

        PumpEvents(TIMEOUT)
        self.unregesiter_event_hook()
