#!/usr/bin/env python
from distutils.core import setup

from setuptools import find_packages

from jtalks import __version__

setup(name='jtalks-cicd',
      version=__version__,
      description='Installs JTalks apps like jcommune and poulpe configuring them. Usually used by CI to implement CD '
                  '(continuous delivery)',
      author='Stanislav Bashkyrtsev',
      author_email='stanislav.bashkirtsev@gmail.com',
      url='http://github.com/jtalks-org/jtalks-cicd',
      install_requires=['distribute==0.7.3', 'requests', 'GitPython', 'paramiko', 'mock', 'ConfigParser',
                        'MySQL-Python', 'mysql-connector-python'],
      tests_require=['mock'],
      scripts=['bin/jtalks'],
      packages=find_packages(),
      test_suite='tests',
      # after package installation we'll have a nice directory instead of zipped artifact which is
      # easier to work with
      zip_safe=False
      #include_package_data=True should add MANIFEST.in first to include non-py files if needed
)
