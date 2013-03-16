import unittest
from jtalks.Nexus import Nexus

__author__ = 'stanislav bashkirtsev'


class NexusTest(unittest.TestCase):
  def test_adds_build_number_if_it_is_not_there(self):
    self.assertEquals("1.123", sut.__final_version__("1"))

  def test_does_not_add_build_if_it_is_there(self):
    self.assertEqual("1.123", sut.__final_version__("1.123"))

  def test_adds_build_number_if_separator_is_not_there(self):
    self.assertEqual("1123.123", sut.__final_version__("1123"))


sut = Nexus(build_number="123")