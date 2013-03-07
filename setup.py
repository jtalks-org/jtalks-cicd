from distutils.core import setup

__author__ = 'stanislav bashkirtsev'

setup(name='jtalks-cicd',
      version='1.0',
      description='Installs JTalks apps like jcommune and poulpe configuring them. Usually used by CI to implement CD (continuous delivery)',
      author='Stanislav Bashkirtsev',
      author_email='stanislav.bashkirtsev@gmail.com',
      url='http://github.com/jtalks-org/jtalks-cicd',
      requires=['requests', 'mock', 'GitPython','MySQLdb'],
)