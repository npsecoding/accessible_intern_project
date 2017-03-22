"""Test out accessible service features"""

import sys
import os
from json import load
from urllib import urlencode, urlopen
from pprint import pprint
from marionette_driver import By
from marionette_driver.marionette import Marionette
from www.fileserver import FileServer

# Start services
SERVICE_PORT = 5000
FILE_PORT = 8000
FILE_SERVER = FileServer(FILE_PORT).start()

HOST = "http://localhost:"
ENDPOINT_PREFIX = HOST + str(SERVICE_PORT)
TEST_HTML = HOST + str(FILE_PORT) + "/" + 'test_IAccessible.html'

CLIENT = Marionette(host='localhost', port=2828)
CLIENT.start_session()
CLIENT.navigate(TEST_HTML)

EVENT_PARAMS = urlencode({
    'interface': 'IAccessible',
    'name': 'MSAA Checkbox',
    'type': 'EVENT_OBJECT_STATECHANGE'
    })
EVENT_ENDPOINT = ENDPOINT_PREFIX + "/event?%s"

CMD_PARAMS = urlencode({
    'interface': 'IAccessible',
    'name': 'MSAA Checkbox',
    'function': 'DefaultAction'
    })
CMD_ENPOINT = ENDPOINT_PREFIX + "/cmd?%s"

ACCESSSIBLE_PARAMS = urlencode({
    'interface': 'IAccessible',
    'name': 'MSAA Checkbox',
    'depth': -1
    })
ACCESSIBLE_ENDPOINT = ENDPOINT_PREFIX + "/accessible?%s"

print "-----------------ACCESSIBLE------------------"
RESPONSE = load(urlopen(ACCESSIBLE_ENDPOINT % ACCESSSIBLE_PARAMS))
CHECKBOX = 0x2C
assert RESPONSE['IAccessible']['Role'] == CHECKBOX

print "-----------------EVENT-----------------------"
RESPONSE = load(urlopen(EVENT_ENDPOINT % EVENT_PARAMS))
STATE_CHECKED = 0x10
assert RESPONSE['IAccessible']['Role'] == CHECKBOX
assert RESPONSE['IAccessible']['State'] & STATE_CHECKED == STATE_CHECKED

print "-----------------CMD-----------------------"
RESPONSE = load(urlopen(CMD_ENPOINT % CMD_PARAMS))
defaultaction = 'uncheck'
assert RESPONSE == defaultaction
