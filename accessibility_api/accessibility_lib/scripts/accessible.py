'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from ctypes import POINTER
from accessibility_api.accessibility_lib.scripts.constants import (
    IAccessible_t, IAccessible2_t
)
from accessibility_api.accessibility_lib.wrappers.IAccessible import (
    IAccessible
)


def interface_ptr_types():
    """Return supported interface pointer types"""
    return [POINTER(IAccessible_t), POINTER(IAccessible2_t)]


def accessible(params):
    """Instantiate the accessible object"""

    interface_t = params.get('interface')
    protocol = {
        'IAccessible': IAccessible,
    }

    return protocol[interface_t](params)
