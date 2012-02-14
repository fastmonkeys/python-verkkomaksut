"""
verkkomaksut
============

Python wrapper for the JSON API of Suomen Verkkomaksut.

Links
-----

* `documentation <http://packages.python.org/verkkomaksut>`_
* `development version
  <http://github.com/jpvanhal/verkkomaksut/zipball/master#egg=verkkomaksut-dev>`_

"""
import sys
import subprocess
from setuptools import Command, setup


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='verkkomaksut',
    version='0.1',
    url='http://github.com/jpvanhal/verkkomaksut',
    license='BSD',
    author='Janne Vanhala',
    author_email='janne.vanhala@gmail.com',
    description='Python wrapper for the JSON API of Suomen Verkkomaksut.',
    long_description=__doc__,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'setuptools',
        'requests',
    ],
    cmdclass={
        'test': PyTest
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
