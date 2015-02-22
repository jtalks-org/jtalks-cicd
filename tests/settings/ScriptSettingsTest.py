import os
import unittest
import shutil

from jtalks.settings.ScriptSettings import ScriptSettings, AppConfigs


class ScriptSettingsTest(unittest.TestCase):
    sut = ScriptSettings(100500, "project1", "system-test")
    tmp_dir = 'ScripSettingsTest-TmpDir'

    def setUp(self):
        os.mkdir(self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_prop_is_overriden_by_project_configs(self):
        self.assertEquals('location overriden by project config', self.sut.get_tomcat_location())

    def test_prop_is_overriden_by_env_configs(self):
        self.assertEquals('final_name overriden by env config', self.sut.get_app_final_name())

    def test_tomcat_port_is_taken_from_server_xml(self):
        self.assertRaises(RuntimeError, self.sut.get_tomcat_port)

    def test_app_config_deployment_descriptor(self):
        project_file = os.path.join(self.tmp_dir, 'project.xml')
        file(project_file, 'w')
        self.assertEqual(project_file, AppConfigs(self.tmp_dir).get_app_descriptor_path('project'))

    def test_app_config_does_not_include_app_descriptor_in_configs(self):
        project_file = os.path.join(self.tmp_dir, 'project.xml')
        file(project_file, 'w')
        self.assertEqual(0, len(AppConfigs(self.tmp_dir).get_app_config_paths('project')))

    def test_app_config_includes_project_configs_in_config_paths(self):
        project_files = (os.path.join(self.tmp_dir, 'project.xml'), os.path.join(self.tmp_dir, 'project-conf.xml'))
        file(project_files[0], 'w'), file(project_files[1], 'w')
        self.assertEqual(1, len(AppConfigs(self.tmp_dir).get_app_config_paths('project')))
        self.assertEqual(project_files[1], AppConfigs(self.tmp_dir).get_app_config_paths('project')[0])
