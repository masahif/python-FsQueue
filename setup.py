from distutils.core import setup
import os, sys, FsQueue


sys.path.append('./test')

setup(
    name='FsQueue',
    version=FsQueue.__version__,
    author=FsQueue.__author__,
    author_email=FsQueue.__author_email__,
    py_modules=['FsQueue'],
    scripts=[],
    url='http://pypi.python.org/pypi/FsQueue/',
    description="Elastic queue based on filesystem.",
    long_description=open('README').read(),

    classifiers = [
        'Environment :: Console',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',],
)
