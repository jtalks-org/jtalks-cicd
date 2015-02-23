from optparse import Values
from os import path
import os
import unittest

from jtalks.Tomcat import Tomcat
from jtalks.OldNexus import Nexus
from jtalks.Nexus import JtalksArtifacts
from jtalks.DeployCommand import DeployCommand
from jtalks.backup.Backuper import Backuper
from jtalks.db.DbOperations import DbOperations
from jtalks.sanity.SanityTest import SanityTest
from jtalks.ScriptSettings import ScriptSettings


class DeployCommandTest(unittest.TestCase):
    def test_deployment_succeeds(self):
        scriptsettings = ScriptSettings(Values({'env': 'system-test', 'project': 'jcommune', 'build': 6,
                                                'grab_envs': 'false', 'sanity_test_timeout_sec': 120}))
        try:
            DeployCommand(
                JtalksArtifacts(), Nexus(6), Tomcat(path.expanduser('~/tomcat')),
                SanityTest(8080, 'jcommune'),
                Backuper('/home/jtalks', DbOperations(scriptsettings.get_db_settings())), scriptsettings
            ).deploy(scriptsettings.project, scriptsettings.build,
                     scriptsettings.get_app_final_name(), scriptsettings.get_plugins())
        except:
            self._read_log_if_available('/home/jtalks/tomcat/logs/jcommune.log')
            self._read_log_if_available('/home/jtalks/tomcat/logs/catalina.out')
            raise

    def _read_log_if_available(self, log_file):
        if os.path.exists(log_file):
            print('Reading log file [{0}]'.format(log_file))
            f = file(log_file, 'r')
            for line in f.readlines():
                print(line)
        else:
            print('Log file {0} was not created, not logs to show'.format(log_file))

    def test_deployment_results_in_configured_appname_instead_of_artifact_name(self):
        pass
