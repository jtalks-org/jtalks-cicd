from optparse import Values
import os
from os.path import join
import unittest
import shutil

from jtalks.ScriptSettings import ScriptSettings, RequiredPropertyNotFoundException


class ScriptSettingsTest(unittest.TestCase):
    tmp_dir = 'ScripSettingsTest-TmpDir'

    def setUp(self):
        os.mkdir(self.tmp_dir)
        os.makedirs(join(self.tmp_dir, ScriptSettings.ENVS_DIR_NAME, 'env'))
        os.mkdir(join(self.tmp_dir, ScriptSettings.TEMP_DIR_NAME))
        os.mkdir(join(self.tmp_dir, ScriptSettings.BACKUPS_DIR_NAME))

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_global_prop_is_overriden_by_env_prop_which_is_overriden_by_project_prop(self):
        self.write_global_config('[section]\nglobal=global\nenv=global\nproject=global')
        self.write_env_config('[section]\nenv=env\nproject=env')
        self.write_project_config('[section]\nproject=project')
        self.assertEquals('global', self.sut().props['section_global'])
        self.assertEquals('env', self.sut().props['section_env'])
        self.assertEquals('project', self.sut().props['section_project'])

    def test_props_with_special_symbols(self):
        self.write_global_config('[sec-dash.dot]\nopt-dash.dot=val-dash.dot')
        self.assertEqual('val-dash.dot', self.sut().props['sec-dash.dot_opt-dash.dot'])

    def test_placeholder_replaced(self):
        self.write_global_config('[sec]\nopt1=${sec_opt2}\nopt2=${sec_opt3}\nopt3=value')
        self.write_env_config('[sec1]\nproj=${project}\nenv=${env}\nopt3=value')
        self.assertEqual('value', self.sut().props['sec_opt1'])
        self.assertEqual('project', self.sut().props['sec1_proj'])
        self.assertEqual('env', self.sut().props['sec1_env'])

    def test_plugins_section_is_split_into_separate_plugins(self):
        self.write_global_config('[app]\nplugins=plugin1,plugin-2,plugin 3')
        self.assertEqual(['plugin1', 'plugin-2', 'plugin 3'], self.sut().get_plugins())
        self.assertNotEqual(('plugin1', 'plugin-2', 'plugin 3'), self.sut().get_plugins())

        self.write_global_config('[app]\nplugins=plugin1')
        self.assertEqual(['plugin1'], self.sut().get_plugins())
        self.assertNotEqual('plugin1', self.sut().get_plugins())

        self.write_global_config('[app]\nplugins=')
        self.assertEqual(0, len(self.sut().get_plugins()))

        self.write_global_config('[app]\n')
        self.assertEqual(0, len(self.sut().get_plugins()))

    def test_settings_file_mapping(self):
        self.write_global_config('[app-files]\nfile1=/file1\nfile-2=/file2\nfile 3=${project}.xml')
        mapping = self.sut().get_app_file_mapping()
        self.assertEqual('/file1', mapping['file1'])
        self.assertEqual('/file2', mapping['file-2'])
        self.assertEqual('project.xml', mapping['file 3'])

    def test_files_are_deployed(self):
        sut = self.sut()
        file(join(sut.global_configs_dir, 'global-file.xml'), 'w').write('Hello, ${project}')
        file(join(sut.global_configs_dir, 'env-file.properties'), 'w').write('This must be overriden by env file')
        file(join(sut.env_configs_dir, 'env-file.properties'), 'w').write('Hello, ${env}')
        self.write_global_config('[tmp]\ndir=' + self.tmp_dir +
                                 '\n[app-files]'
                                 '\nglobal-file.xml=${tmp_dir}/file.xml'
                                 '\nenv-file.properties=${tmp_dir}/creates_folder/file.properties')
        self.sut().deploy_configs()
        self.assertEqual('Hello, project', file(join(self.tmp_dir, 'file.xml')).readline())
        self.assertEqual('Hello, env', file(join(self.tmp_dir, 'creates_folder', 'file.properties')).readline())

    def test_get_db_settings(self):
        self.write_env_config('[app]\ndb_user=u\ndb_password=pass\ndb_name=name\ndb_host=local\ndb_port=22')
        db_settings = self.sut().get_db_settings()
        self.assertEqual('u', db_settings.user)
        self.assertEqual('pass', db_settings.password)
        self.assertEqual('name', db_settings.name)
        self.assertEqual('local', db_settings.host)
        self.assertEqual(22, db_settings.port)

    def test_get_db_settings_for_optional_fields(self):
        self.write_env_config('[app]\ndb_user=u\ndb_name=name\ndb_host=local')
        db_settings = self.sut().get_db_settings()
        self.assertEqual('', db_settings.password)
        self.assertEqual(3306, db_settings.port)

    def test_get_db_settings_if_required_fields_not_found(self):
        self.write_env_config('[app]\ndb_user=u\ndb_name=name')
        self.assertRaises(RequiredPropertyNotFoundException, self.sut().get_db_settings)

        self.write_env_config('[app]\ndb_user=u\ndb_host=local')
        self.assertRaises(RequiredPropertyNotFoundException, self.sut().get_db_settings)

        self.write_env_config('[app]\ndb_name=name\ndb_host=local')
        self.assertRaises(RequiredPropertyNotFoundException, self.sut().get_db_settings)

    def write_global_config(self, text):
        file(join(self.tmp_dir, ScriptSettings.ENVS_DIR_NAME, ScriptSettings.GLOBAL_ENV_CONFIG_FILE_NAME), 'w')\
            .write(text)

    def write_env_config(self, text, env='env'):
        env_dir = join(self.tmp_dir, ScriptSettings.ENVS_DIR_NAME, env)
        if not os.path.exists(env_dir):
            os.makedirs(env_dir)
        file(join(env_dir, ScriptSettings.ENV_CONFIG_FILE_NAME), 'w').write(text)

    def write_project_config(self, text, env='env', project='project'):
        env_dir = join(self.tmp_dir, ScriptSettings.ENVS_DIR_NAME, env)
        if not os.path.exists(env_dir):
            os.makedirs(env_dir)
        file(join(env_dir, project + '.cfg'), 'w').write(text)

    def sut(self, options_as_dict={}):
        """
        :param dict options_as_dict: options to pass to script settings
        :return: ScriptSettings
        """
        merged = dict(options_as_dict.items() + {'project': 'project', 'env': 'env', 'build': '0', 'grab_envs': 'false',
                                                 'sanity_test_timeout_sec': 120}.items())
        return ScriptSettings(Values(merged), workdir=self.tmp_dir)
