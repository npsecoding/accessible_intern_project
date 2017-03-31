'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from SocketServer import TCPServer
from argparse import ArgumentParser
from accessibility_api.AccessibilityRequestHandler import (
    platform_accessibility_request_handler_factory
)


class AccessibilityAPIServer(object):
    """
    API service for Accessible Requests
    """

    def __init__(self, port, app, platform=None, verbose=False, ip=""):
        self.verbose = verbose
        if self.verbose:
            print '.............SETTING UP SERVICE............'
        handler = platform_accessibility_request_handler_factory(platform, app)
        if handler is None:
            raise Exception('Invalid/Not supported platform')

        self.server = TCPServer((ip, port), handler)

    def shutdown(self):
        """
        Stop accessibility server
        """

        if self.verbose:
            print '.............SERVICE STOPPED...........'
        self.server.shutdown()
        self.server.server_close()

    def start(self):
        """
        Start accessibility server
        """

        if self.verbose:
            print '.............SERVICE RUNNING...............'
        self.server.serve_forever()

if __name__ == '__main__':
    PARSER = ArgumentParser()
    PARSER.add_argument('port', help='Port Number', type=int)
    PARSER.add_argument('app', help='Application', type=str)
    PARSER.add_argument('--platform', help='Platform Type', type=str)
    PARSER.add_argument('--verbose', help='Print debug statments', type=bool)
    ARGS = PARSER.parse_args()

    SERVER = AccessibilityAPIServer(ARGS.port, ARGS.app,
                                    ARGS.platform, ARGS.verbose)
    SERVER.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        SERVER.shutdown()
