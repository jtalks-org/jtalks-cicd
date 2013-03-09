import unittest
from jtalks.ApplicationContext import ApplicationContext
from jtalks.Tomcat import Tomcat
from jtalks.backup.Backuper import Backuper
from jtalks.settings.ScriptSettings import ScriptSettings

__author__ = 'stanislav bashkirtsev'


class ApplicationContextTest(unittest.TestCase):
  sut = ApplicationContext(ScriptSettings(510, "project1", "unit-test"))

  def test_nexus_is_created(self):
    nexus = self.sut.nexus()
    self.assertEquals(nexus.build_number, 510)

  def test_tomcat_is_created(self):
    tomcat = self.sut.tomcat()
    #can't use assertIsInstance() because on CentOS we use old mock lib
    self.assertTrue(isinstance(tomcat, Tomcat))
    self.assertTrue(isinstance(tomcat.script_settings, ScriptSettings))
    self.assertTrue(isinstance(tomcat.backuper, Backuper))


if __name__ == '__main__':
  unittest.main()

