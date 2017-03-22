""" API for Accessible Requests """

from SocketServer import TCPServer
from argparse import ArgumentParser
from AccessibilityRequestHandler import PlatformAccessibilityRequestHandler


VERBOSE = False


class AccessibilityAPIServer:
    def __init__(self, port, platform=None, ip=""):
        if VERBOSE:
            print '.............SETTING UP SERVICE............'
        handler = PlatformAccessibilityRequestHandler(platform)
        self.server = TCPServer((ip, port), handler)

    def shutdown(self):
        if VERBOSE:
            print '.............SERVICE STOPPED...........'
        self.server.shutdown()
        self.server.server_close()

    def start(self):
        if VERBOSE:
            print '.............SERVICE RUNNING...............'
        self.server.serve_forever()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("port", help="Port Number", type=int)
    parser.add_argument("--platform", help="Platform Type", type=str)
    args = parser.parse_args()

    SERVER = AccessibilityAPIServer(args.port, args.platform)
    SERVER.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        SERVER.shutdown()
