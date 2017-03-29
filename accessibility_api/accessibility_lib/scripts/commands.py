'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from accessibility_api.accessibility_lib.scripts.accessible import (
    accessible, interface_ptr_types
)
from comtypes import COMError


def command(params):
    """
    Execute command on accessible object and returns value
    """

    cmd = params.get('function')
    if cmd is None:
        return {
            'error': True,
            'message': 'No command given'
        }

    acc_obj = accessible(params)
    if acc_obj.get('error'):
        return {
            'error': True,
            'message': 'No accessible found'
        }

    value = None
    json = acc_obj.get('result')[params.get('interface')]

    # Get accessible field from JSON
    if cmd in json:
        value = json[cmd]
    # Call accessible method
    else:
        # Localize paramaters
        function_params = []
        for param in params.get('param'):
            lparam = param.encode('UTF8')
            if lparam.isdigit():
                function_params.append(int(lparam))
            else:
                function_params.append(lparam)
        try:
            prefix = 'acc'
            value = getattr(acc_obj.get('target'),
                            prefix + cmd)(*function_params)
        except COMError:
            return {
                'error': True,
                'message': 'Function failed to execute with paramaters'
            }

    # Handles case when value is pointer by wrapping for serialization
    if isinstance(value, interface_ptr_types()):
        return {
            'result': acc_obj.get('semantic_wrap')(value)
        }
    else:
        return {
            'result': value
        }
