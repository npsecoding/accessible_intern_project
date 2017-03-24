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

    def _parse_identifiers(self, params):
        name = params.get('name')
        role = params.get('role')

        identifiers = {}
        if name is not None:
            identifiers["Name"] = name
        if role is not None:
            identifiers["Role"] = role

        return identifiers

    def do_GET(self):
        url = urlparse(self.path)
        handler = getattr(self, "get_" + url.path[1:], None)
        if handler:
            handler(url.query)

        else:
            self.send_response(403, 'Invalid Request')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        return

    def get_accessible(self, urlquery):
        '''Retrieve accessible object'''

        params = dict(parse_qsl(urlquery))
        identifiers = self._parse_identifiers(params)
        acc_obj = accessible(params.get('interface'), identifiers)

        if params.get('interface') is None:
            self._bad_request('Bad Request: No interface specified')
            return

        if acc_obj.found:
            json = acc_obj.serialize(params.get('depth'))
            self._successful_response(dumps({params.get('interface'): json}))
        else:
            self._bad_request('Bad Request: Accessible does not exist')

    def get_event(self, urlquery):
        '''Listen for accessible event'''

        params = dict(parse_qsl(urlquery))
        identifiers = self._parse_identifiers(params)

        if params.get('type') is None:
            self._bad_request('Bad Request: No event type specified')
            return

        event_handler = event(params.get('interface'),
                              params.get('type'), identifiers)

        if event_handler.found is not None:
            self._successful_response(dumps(event_handler.found))
        else:
            self._bad_request('Bad Request: No event occurred')

    def get_cmd(self, urlquery):
        '''Perform command on accessible'''
        
        params = dict(parse_qsl(urlquery))
        params['param'] = parse_qs(urlquery).get('param')
        identifiers = self._parse_identifiers(params)

        if params.get('function') is None:
            self._bad_request('Bad Request: No command specified')
            return

        value = execute_command(params.get('interface'), identifiers,
                                params.get('function'), params.get('param'))

        if value is not "ERROR":
            self._successful_response(dumps(value))
        else:
            self._bad_request('Bad Request:'
                              'Command can not be executed on accessible')


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
