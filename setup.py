"""
verkkomaksut
============

Python wrapper for the JSON API of Suomen Verkkomaksut.

Links
-----

* `documentation <http://packages.python.org/verkkomaksut>`_
* `development version
  <http://github.com/fastmonkeys/python-verkkomaksut/zipball/master#egg=verkkomaksut-dev>`_

"""
import os
import re

from setuptools import setup


HERE = os.path.dirname(os.path.abspath(__file__))


def get_version():
    filename = os.path.join(HERE, 'verkkomaksut', '__init__.py')
    contents = open(filename).read()
    pattern = r"^__version__ = '(.*?)'$"
    return re.search(pattern, contents, re.MULTILINE).group(1)


setup(
    name='verkkomaksut',
    version=get_version(),
    description='Python wrapper for the JSON API of Suomen Verkkomaksut.',
    long_description=(
        open('README.rst').read() + '\n' +
        open('CHANGES.rst').read()
    ),
    author='Janne Vanhala',
    author_email='janne@fastmonkeys.com',
    url='http://github.com/fastmonkeys/python-verkkomaksut',
    packages=['verkkomaksut'],
    include_package_data=True,
    license='BSD',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
