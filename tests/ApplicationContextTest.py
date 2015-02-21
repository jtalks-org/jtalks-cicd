import os
import unittest

from jtalks.ApplicationContext import ApplicationContext
from jtalks.Tomcat import Tomcat
from jtalks.backup.Backuper import Backuper
from jtalks.settings.ScriptSettings import ScriptSettings


class ApplicationContextTest(unittest.TestCase):
    env_config_dir = "" + os.path.expanduser('~/.jtalks/environments/system-test')
    sut = ApplicationContext("system-test", "project1", 510, False, env_config_dir)

    def test_nexus_is_created(self):
        nexus = self.sut.old_nexus()
        self.assertEquals(nexus.build_number, 510)

    def test_tomcat_is_created(self):
        tomcat = self.sut.tomcat()
        # can't use assertIsInstance() because on CentOS we use old mock lib
        self.assertTrue(isinstance(tomcat, Tomcat))
