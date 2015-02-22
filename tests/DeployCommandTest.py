from os import path
import unittest

from jtalks.Tomcat import Tomcat
from jtalks.OldNexus import Nexus
from jtalks.Nexus import JtalksArtifacts
from jtalks.DeployCommand import DeployCommand
from jtalks.backup.Backuper import Backuper
from jtalks.db.DbOperations import DbOperations
from jtalks.sanity.SanityTest import SanityTest
from jtalks.settings.ScriptSettings import AppConfigs


class DeployCommandTest(unittest.TestCase):
    def test_deployment_succeeds(self):
        try:
            DeployCommand(
                JtalksArtifacts(), Nexus(6), Tomcat(path.expanduser('~/tomcat')), SanityTest(8080, 'jcommune'),
                Backuper('/home/jtalks', DbOperations('localhost', 'root', '', 'mysql')),
                AppConfigs(path.expanduser('~/.jtalks/environments/system-test/'))).deploy('jcommune', 6, 'jcommune')
        except:
            print('Reading jcommune.log...')
            f = file('/home/jtalks/tomcat/logs/jcommune.log', 'r')
            for line in f.readlines():
                print(line)
            raise

    def test_deployment_results_in_configured_appname_instead_of_artifact_name(self):
        pass
