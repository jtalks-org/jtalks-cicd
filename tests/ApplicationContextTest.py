from optparse import Values
import unittest

from jtalks.ApplicationContext import ApplicationContext
from jtalks.Tomcat import Tomcat
from jtalks.ScriptSettings import ScriptSettings


class ApplicationContextTest(unittest.TestCase):
    sut = ApplicationContext(ScriptSettings(Values({'project': 'project', 'env': 'system-test', 'build': 510,
                                                    'grab_envs': 'false', 'sanity_test_timeout_sec': 120}),
                                            workdir='.jtalks'))

    def test_nexus_is_created(self):
        nexus = self.sut.old_nexus()
        self.assertEquals(nexus.build_number, 510)

    def test_tomcat_is_created(self):
        tomcat = self.sut.tomcat()
        # can't use assertIsInstance() because on CentOS we use old mock lib
        self.assertTrue(isinstance(tomcat, Tomcat))
