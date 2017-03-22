"""Create EventHandler object"""

from platform import system
from ..events.WinEventHandler import WinEventHandler


def event(interface_t, event_t, _identifiers):
    """Instantiate EventHandler object"""
    protocol = {
        'Windows': WinEventHandler
    }
    return protocol[system()](interface_t, event_t, _identifiers)
