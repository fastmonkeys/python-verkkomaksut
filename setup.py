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
from setuptools import setup


setup(
    name='verkkomaksut',
    version='0.1.1',
    description='Python wrapper for the JSON API of Suomen Verkkomaksut.',
    long_description=__doc__,
    author='Janne Vanhala',
    author_email='janne.vanhala@gmail.com',
    url='http://github.com/LiiquOy/python-verkkomaksut',
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
