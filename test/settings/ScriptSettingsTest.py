import unittest
from jtalks.settings.ScriptSettings import ScriptSettings


__author__ = 'ctapobep'


class ScriptSettingsTest(unittest.TestCase):
  sut = ScriptSettings(100500, "project1", "unit-test")

  def test_prop_is_overriden_by_project_configs(self):
    self.assertEquals('location overriden by project config', self.sut.get_tomcat_location())

  def test_prop_is_overriden_by_env_configs(self):
    self.assertEquals('final_name overriden by env config', self.sut.get_app_final_name())

  def test_tomcat_port_is_taken_from_server_xml(self):
    self.assertRaises(RuntimeError, self.sut.get_tomcat_port)