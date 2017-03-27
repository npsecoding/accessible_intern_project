'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from accessibility_api.accessibility_lib.scripts.accessible import (
    accessible, interface_ptr_types
)
from accessibility_api.accessibility_lib.scripts.constants import (
    SUCCESSFUL_RESPONSE, ERROR_RESPONSE
)


def execute_command(params):
    """Execute command on accessible object and returns value"""

    cmd = params.get('function')
    function_params = params.get('params')
    value = None

    acc_obj = accessible(params).serialize_result(0)
    if acc_obj.get('status') == ERROR_RESPONSE:
        return {
            'status': ERROR_RESPONSE,
            'json': None
        }
    _json = acc_obj.get('json')

    # Get accessible field from JSON
    if cmd in _json:
        value = _json[cmd]
    # Call accessible method
    else:
        # Localize paramaters
        localized_params = []
        for param in params:
            lparam = param.encode('UTF8')
            if lparam.isdigit():
                localized_params.append(int(lparam))
            else:
                localized_params.append(lparam)
        params = []
        params = localized_params

        try:
            prefix = 'acc'
            value = getattr(acc_obj._target, prefix + cmd)(*function_params)
        except:
            return {
                'status': ERROR_RESPONSE,
                'json': None
            }

    # Handles case when value is pointer by wrapping for serialization
    if type(value) in interface_ptr_types():
        return {
            'json': acc_obj.semantic_wrap(value),
            'status': SUCCESSFUL_RESPONSE
        }
    else:
        return {
            'json': value,
            'status': SUCCESSFUL_RESPONSE
        }
