#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

__author__ = 'stanislav bashkirtsev'

setup(name='jtalks-cicd',
      version='1.0',
      description='Installs JTalks apps like jcommune and poulpe configuring them. Usually used by CI to implement CD (continuous delivery)',
      author='Stanislav Bashkirtsev',
      author_email='stanislav.bashkirtsev@gmail.com',
      url='http://github.com/jtalks-org/jtalks-cicd',
      requires=['requests', 'mock', 'GitPython'],
      scripts=['bin/jtalks', 'bin/prod_db_to_preprod', 'bin/upload_to_nexus'],
      packages=find_packages(),
      # after package installation we'll have a nice directory instead of zipped artifact which is
      # easier to work with
      zip_safe=False
      #include_package_data=True should add MANIFEST.in first to include non-py files if needed
)
