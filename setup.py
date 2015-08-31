#!/usr/bin/python

# Copyright (c) 2011 Jason Hancock <jsnbyh@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name             = 'CloudStackClient',
    version          = '0.1.1',
    description      = "CloudStack API Client",
    long_description = (read('README.md') + '\r\n' +
                        read('HISTORY.rst') + '\r\n' +
                        read('AUTHORS')
                       ),
    author           = "Jason Hancock",
    author_email     = "terbolous@gmail.com",
    url              = "https://github.com/terbolous/cloudstack-python-client",
    packages         = [ 'CloudStackClient' ],
    license          = 'MIT',
    platforms        = 'Posix; MacOS X; Windows',
)
