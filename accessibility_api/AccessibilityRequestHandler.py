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
from accessibility_api.accessibility_lib.scripts.commands import command


class AccessibilityRequestHandler(BaseHTTPRequestHandler):
    """
    Service requests for accessible objects
    """

    def response(self, value):
        """
        Send JSON to client
        """

        is_error = value.get('error')
        if is_error:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(dumps({
                'error': is_error,
                'message': value.get('message')
            }))
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(dumps({
                'result': value.get('result')
            }))

    def do_GET(self):
        """
        Proccess get requests
        """

        handlers = {
            '/accessible': accessible,
            '/event': event,
            '/cmd': command
        }
        url = urlparse(self.path)
        handler = handlers.get(url.path)

        if handler:
            params = dict(parse_qsl(url.query))
            params['param'] = parse_qs(url.query).get('param')
            self.response(handler(params))
        else:
            self.send_response(403, 'Invalid Request')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

        return


class WindowsAccessibilityRequestHandler(AccessibilityRequestHandler, object):
    """
    Windows Accessibility Handler
    """

    def __init__(self, request, client_address, server):
        super(WindowsAccessibilityRequestHandler, self)\
              .__init__(request, client_address, server)
        CoInitialize()


def platform_accessibility_request_handler_factory(platform):
    """
    Return platform accessbility handler
    """

    if platform is None:
        platform = sys.platform

    handlers = {
        'win32': WindowsAccessibilityRequestHandler
    }

    return handlers.get(platform)
