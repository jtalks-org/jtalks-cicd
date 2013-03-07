import unittest
from classes.util.EnvironmentConfigGrabber import EnvironmentConfigGrabber

__author__ = 'stanislav bashkirtsev'

class EnvironmentConfigGrabberTest(unittest.TestCase):
  def test(self):
    EnvironmentConfigGrabber().grab_jtalks_configs()
