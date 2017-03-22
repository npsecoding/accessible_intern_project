"""Serve HTML Test Files"""

import os
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer
from threading import Thread


class FileServer(object):
    def __init__(self, port):
        directory = '/www'
        path = os.path.dirname(__file__)
        os.chdir(path)

        handler = SimpleHTTPRequestHandler
        self.server = TCPServer(("", port), handler)
        self.thread = None

    def start(self):
        self.thread = Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
