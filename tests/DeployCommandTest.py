import unittest
from ApplicationContext import ApplicationContext
from DeployCommand import DeployCommand
from Nexus import JtalksArtifacts
from OldNexus import Nexus
from Tomcat import Tomcat
from sanity.SanityTest import SanityTest


class DeployCommandTest(unittest.TestCase):
    def test_deployment(self):
        #DeployCommand(JtalksArtifacts(), Nexus(6), Tomcat(), SanityTest(8080, 'jcommune')).deploy('jcommune', 6)
        pass
