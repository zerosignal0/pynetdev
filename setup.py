# Copyright (C) 2014  Gary Wright <gwright@secureneo.com>
#
# This file is part of pynetdev
#
# Pynetdev is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Pynetdev is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pynetdev; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Suite 500, Boston, MA  02110-1335  USA.


longdesc = '''
Pynetdev is a library made to wrap common network automation into easy to
use, reusable templates.  Also exposed is a CLI like interface for interaction
with multiple network devices, provided a common authentication (or provided ssh
key).

Required packages:
    setuptools, paramiko, rainbow_logging_handler

'''

kw = {
    'install_requires': [
        'rainbow_logging_handler >= 2.1.2',
        'fabric >= 1.8',
        'readline >= 6.2.4.1',
        'pyyaml >= 3.11',

    ],
    'scripts':  ['bin/netautomaton.py',
                 'pynetdev.config.banner1',
                 'pynetdev.config.banner2',
                 'pynetdev.config.banner3',
                 'pynetdev.config.banner4',
                 'pynetdev.config.banner5',
                 'pynetdev.config.banner6',
                 'pynetdev.config.default_conf_template.yaml', ],
    'packages': [ 'pynetdev',
                  'pynetdev.config'],
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = "pynetdev",
    version = "1.0.0",
    description = "Network devices automation library based on paramiko.",
    long_description = longdesc,
    author = "Gary Wright",
    author_email = "gwright@secureneo.com",
    url = "https://github.com/zerosignal0/pynetdev",
    license = 'LGPL',
    platforms = 'Posix; MacOS X', #Windows is currently unsupported due to pycrypto instability
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers, Network Engineers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Networking',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    **kw
)
