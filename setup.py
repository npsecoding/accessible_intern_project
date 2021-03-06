'''
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at http://mozilla.org/MPL/2.0/.
'''

from setuptools import setup, find_packages

setup(
    name='Accessibility_API',
    version='1.0.0',
    description='Platform independent accessibility API',
    author='Nancy Pang',
    author_email='npang@mozila.com',
    install_requires=[
        # dependencies
        'comtypes'
    ],
    packages=find_packages('../accessibility_api')
)
