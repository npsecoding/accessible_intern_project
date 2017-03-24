'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

import sys
from accessibility_api.accessibility_lib.utils.WinUtil import WinUtil


def util():
    """Instantiate the platform utility"""
    platform = sys.platform
    os_t = {
        'win32': WinUtil
    }
    return os_t[platform]()
