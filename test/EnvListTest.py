import unittest
from jtalks.settings.ScriptSettings import ScriptSettings
from jtalks.util.EnvList import EnvList

__author__ = 'ctapobep'


class EnvListTest(unittest.TestCase):

  def test_all_envs_are_listed(self):
    #can't use assertIn() because in CentOS we have old mock lib
    self.assertTrue("dev" in self.sut.get_list_of_envs())
    self.assertTrue("uat" in self.sut.get_list_of_envs())
    self.assertTrue("prod" in self.sut.get_list_of_envs())
    self.assertTrue("preprod" in self.sut.get_list_of_envs())
    self.assertTrue("unit-test" in self.sut.get_list_of_envs())

  def test_list_projects_for_env(self):
    projects = self.sut.list_projects("unit-test")
    self.assertEqual(len(projects), 2)
    self.assertTrue("project1" in projects, "Actually contained:" + repr(projects))

  sut = EnvList(ScriptSettings(None, None, None))