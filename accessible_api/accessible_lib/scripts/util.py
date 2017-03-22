"""Create platform utility object"""

import sys
from ..utils.WinUtil import WinUtil


def util():
    """Instantiate the platform utility"""
    platform = sys.platform
    os_t = {
        'win32': WinUtil
    }
    return os_t[platform]()
