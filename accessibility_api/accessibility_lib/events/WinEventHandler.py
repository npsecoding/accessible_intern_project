'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from ctypes import byref, wintypes, windll, oledll, POINTER, WINFUNCTYPE
from comtypes.client import PumpEvents
from comtypes.automation import VARIANT
from accessibility_api.accessibility_lib.scripts.accessible import accessible
from accessibility_api.accessibility_lib.utils.WinUtil import WinUtil
from accessibility_api.accessibility_lib.events.BaseEventHandler import (
    BaseEventHandler
)
from accessibility_api.accessibility_lib.scripts.constants import (
    IAccessible_t, S_OK, INVALID_EVENT,
    TIMEOUT, WIN_EVENT_NAMES, WINEVENT_OUTOFCONTEXT
)
from accessibility_api.accessibility_lib.scripts.debug import (
    print_event, print_name
)


class WinEventHandler(BaseEventHandler):
    """
    Handle Windows Events
    """

    # Store information about event used between callback and handler
    info = {}
    found = None

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

        print_name(acc_ptr, idChild)

        if WinUtil.match_criteria(acc_ptr, WinEventHandler.params, idChild):
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
        WinEventHandler.found = None

        self.hook = self.register_event_hook(event_t)
        print_event(event_t)
        if self.hook != INVALID_EVENT:
            self.listen_to_events()

    def serialize_result(self):
        """
        Return event object
        """
        if WinEventHandler.found is None:
            return {
                'error': True,
                'message': WinEventHandler.type_t + ' not found'
            }
        else:
            interface_t = WinEventHandler.interface_t
            return {
                'result': {WinEventHandler.type_t:
                           WinEventHandler.found[interface_t]}
            }

    def register_event_hook(self, event):
        """
        Register callback for event type
        """

        event_type = WIN_EVENT_NAMES.get(event)
        if event_type:
            return self.register_event(event_type, event_type)
        else:
            return INVALID_EVENT

    def unregesiter_event_hook(self):
        """
        Unregister callback for event type
        """

        result = windll.user32.UnhookWinEvent(self.hook)
        return result

    def listen_to_events(self):
        """
        Get registered events and trigger callback
        """

        PumpEvents(TIMEOUT)
        self.unregesiter_event_hook()
