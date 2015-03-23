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
    def test_deployment_from_old_nexus_repo(self):
        scriptsettings = self._scriptsettings(build=2789)
        try:
            self._deploy(scriptsettings)
        except:
            self._read_log_if_available('/home/jtalks/tomcat/logs/jcommune.log')
            self._read_log_if_available('/home/jtalks/tomcat/logs/catalina.out')
            raise

    def test_deployment_from_new_nexus_repo(self):
        scriptsettings = self._scriptsettings(build=6)
        try:
            self._deploy(scriptsettings)
        except:
            self._read_log_if_available('/home/jtalks/tomcat/logs/jcommune.log')
            self._read_log_if_available('/home/jtalks/tomcat/logs/catalina.out')
            raise

    def test_deploy_poulpe_from_old_nexus_repo(self):
        scriptsettings = self._scriptsettings(build=344, project='poulpe')
        try:
            self._deploy(scriptsettings)
        except:
            self._read_log_if_available('/home/jtalks/tomcat/logs/poulpe.log')
            self._read_log_if_available('/home/jtalks/tomcat/logs/catalina.out')
            raise

    def test_deploy_plugins_must_not_clean_prev_plugins_if_not_jc_is_deployed(self):
        jcsettings = self._scriptsettings(build=2789)
        antsettings = self._scriptsettings(build=574, project='antarcticle')
        try:
            self._deploy(jcsettings)
            self._deploy(antsettings)
        except:
            self._read_log_if_available('/home/jtalks/tomcat/logs/catalina.out')
            self._read_log_if_available('/home/jtalks/tomcat/logs/jcommune.log')
            raise
        plugins = os.listdir('/home/jtalks/.jtalks/plugins/system-test')
        self.assertNotEqual(0, len(plugins), 'Actual plugins: ' + ', '.join(plugins))
        self.assertEqual(['questions-n-answers-plugin'], plugins)

    def _deploy(self, scriptsettings):
        DeployCommand(
            JtalksArtifacts(), Nexus(scriptsettings.build), Tomcat(path.expanduser('~/tomcat')),
            SanityTest(scriptsettings.get_tomcat_port(), scriptsettings.project),
            Backuper('/home/jtalks', DbOperations(scriptsettings.get_db_settings())), scriptsettings
        ).deploy(scriptsettings.project, scriptsettings.build,
                 scriptsettings.get_app_final_name(), scriptsettings.get_plugins())

    def _scriptsettings(self, build, project='jcommune'):
        return ScriptSettings(Values({'env': 'system-test', 'project': project, 'build': build,
                                      'grab_envs': 'false', 'sanity_test_timeout_sec': 120}),
                              workdir='tests/.jtalks')

    def _read_log_if_available(self, log_file):
        if os.path.exists(log_file):
            print('Reading log file [{0}]'.format(log_file))
            f = file(log_file, 'r')
            for line in f.readlines():
                print(line)
        else:
            print('Log file {0} was not created, not logs to show'.format(log_file))
