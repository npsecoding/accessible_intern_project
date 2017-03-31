'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from .constants import CHILDID_SELF

DEBUG_ENABLED = False


def simple_element_atrribute(json, child_id):
    """
    Add simple element attribute to JSON
    """

    if not DEBUG_ENABLED:
        return

    if child_id != CHILDID_SELF:
        json['SimpleElement'] = True
    else:
        json['SimpleElement'] = False


def print_test_window(window):
    """
    Print test window
    """

    if not DEBUG_ENABLED:
        return

    print 'Test Window: %d' % window


def print_name(acc_ptr, child_id):
    """
    Print accessible name
    """

    if not DEBUG_ENABLED:
        return

    print acc_ptr.accName(child_id)


def print_event(event):
    """
    Print event hook
    """

    if not DEBUG_ENABLED:
        return

    print 'Registered ' + event + ' hook'


def print_accessible(node):
    """
    Print the accessible name and role
    """

    if not DEBUG_ENABLED:
        return

    name = _unicode(node.accName(CHILDID_SELF))
    print '--------------------------'
    print 'Accessible Object'
    print node
    print 'Name: %s' % name
    print 'Role: %s' % node.accRole(CHILDID_SELF)
    print '--------------------------'


def print_simple(node, childid):
    """
    Print the simple element owner, name and role
    """

    if not DEBUG_ENABLED:
        return

    name = _unicode(node.accName(childid))
    print '--------------------------'
    print 'Simple Element'
    print 'Owner:%s' % node
    print 'Name: %s' % name
    print 'Role: %s' % node.accRole(childid)
    print '--------------------------'


def _unicode(name):
    if name:
        return name.encode('utf8')
