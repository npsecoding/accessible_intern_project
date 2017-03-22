"""Create Accessible object"""

from ctypes import POINTER
from ..scripts.constants import IAccessible_t, IAccessible2_t
from ..wrappers.IAccessible2 import IAccessible2
from ..wrappers.IAccessible import IAccessible


def interface_ptr_types():
    """Return supported interface pointer types"""
    return [POINTER(IAccessible_t), POINTER(IAccessible2_t)]


def accessible(interface_t, identifiers):
    """Instantiate the accessible object"""
    protocol = {
        'IAccessible': IAccessible,
        'IAccessible2': IAccessible2
    }
    return protocol[interface_t](identifiers)
