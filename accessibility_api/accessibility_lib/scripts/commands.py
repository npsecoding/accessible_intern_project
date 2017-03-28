'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from accessibility_api.accessibility_lib.scripts.accessible import (
    accessible, interface_ptr_types
)
from accessibility_api.accessibility_lib.scripts.constants import (
    SUCCESS, ERROR
)
from comtypes import COMError


def command(params):
    """
    Execute command on accessible object and returns value
    """

    cmd = params.get('function')
    if cmd is None:
        return {
            'error': ERROR,
            'result': None
        }

    acc_obj = accessible(params)
    if acc_obj.get('error'):
        return {
            'error': ERROR,
            'result': None
        }

    value = None
    _json = acc_obj.get('result')[params.get('interface')]

    # Get accessible field from JSON
    if cmd in _json:
        value = _json[cmd]
    # Call accessible method
    else:
        # Localize paramaters
        function_params = params.get('param')
        localized_params = []
        for param in function_params:
            lparam = param.encode('UTF8')
            if lparam.isdigit():
                localized_params.append(int(lparam))
            else:
                localized_params.append(lparam)
        function_params = []
        function_params = localized_params

        try:
            prefix = 'acc'
            value = getattr(acc_obj.get('target'), prefix + cmd)(*function_params)
        except COMError:
            return {
                'error': ERROR,
                'result': None
            }

    # Handles case when value is pointer by wrapping for serialization
    if value in interface_ptr_types():
        return {
            'error': SUCCESS,
            'result': {cmd: acc_obj.get('semantic_wrap')(value)}
        }
    else:
        return {
            'error': SUCCESS,
            'result': {cmd: value}
        }
