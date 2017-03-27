'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

import sys
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import urlparse, parse_qs, parse_qsl
from json import dumps
from comtypes import CoInitialize
from accessibility_api.accessibility_lib.scripts.constants import (
    SUCCESSFUL_RESPONSE, ERROR_RESPONSE
)
from accessibility_api.accessibility_lib.scripts.accessible import accessible
from accessibility_api.accessibility_lib.scripts.event import event
from accessibility_api.accessibility_lib.scripts.commands import (
    execute_command
)


class AccessibilityRequestHandler(BaseHTTPRequestHandler):
    """ Service requests for accessible objects """
    def _successful_response(self, json):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json)

    def _bad_request(self, message):
        self.send_response(500, message)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        '''Proccess get requests'''
        url = urlparse(self.path)
        handler = getattr(self, "get_" + url.path[1:], None)
        if handler:
            handler(url.query)
        else:
            self.send_response(403, 'Invalid Request')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

        return

    def response(self, message, key, value, status):
        """Returns appropriate response"""
        response_args = {
            ERROR_RESPONSE: message,
            SUCCESSFUL_RESPONSE: dumps({key: value})
        }[status]

        return {
            ERROR_RESPONSE: self._bad_request,
            SUCCESSFUL_RESPONSE: self._successful_response
        }[status](response_args)

    def get_accessible(self, urlquery):
        '''Retrieve accessible object'''

        params = dict(parse_qsl(urlquery))
        if params.get('interface') is None:
            self._bad_request('Bad Request: No interface specified')
            return

        acc_obj = accessible(params).serialize_result(params.get('depth'))
        self.response(
            'Bad Request: No accessible exists',
            params.get('interface'),
            acc_obj.get('json'),
            acc_obj.get('status')
        )

    def get_event(self, urlquery):
        '''Listen for accessible event'''

        params = dict(parse_qsl(urlquery))
        if params.get('type') is None:
            self._bad_request('Bad Request: No event type specified')
            return

        event_obj = event(params).serialize_result()
        self.response(
            'Bad Request: No event occurred',
            params.get('type'),
            event_obj.get('json'),
            event_obj.get('status')
        )

    def get_cmd(self, urlquery):
        '''Perform command on accessible'''

        params = dict(parse_qsl(urlquery))
        params['param'] = parse_qs(urlquery).get('param')
        if params.get('function') is None:
            self._bad_request('Bad Request: No command specified')
            return

        command_obj = execute_command(params)
        self.response(
            'Bad Request: No command exists',
            params.get('function'),
            command_obj.get('json'),
            command_obj.get('status')
        )


class WindowsAccessibilityRequestHandler(AccessibilityRequestHandler, object):
    '''Windows Accessibility Handler'''
    def __init__(self, request, client_address, server):
        super(WindowsAccessibilityRequestHandler, self)\
              .__init__(request, client_address, server)
        CoInitialize()


def platform_accessibility_request_handler_factory(platform):
    '''Return platform accessbility handler'''
    if platform is None:
        platform = sys.platform

    handlers = {
        'win32': WindowsAccessibilityRequestHandler
    }

    return handlers.get(platform)
