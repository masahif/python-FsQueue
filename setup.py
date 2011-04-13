"""
FsQueue
"""

from setuptools import setup, find_packages
import sys

import FsQueue

sys.path.append('./test')

setup(
    name = 'FsQueue',
    py_modules=['FsQueue'],
    version = FsQueue.__version__,
    author=FsQueue.__author__,
    url = 'https://github.com/masahif/python-FsQueue',
    license= FsQueue.__license__,
    description="Elastic queue based on filesystem.",
    long_description = FsQueue.__doc__,
    test_suite='test_fsqueue.suite',

)

