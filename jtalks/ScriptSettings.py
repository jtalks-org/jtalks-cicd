from ConfigParser import ConfigParser
import os

from jtalks import __version__
from jtalks.util.Logger import Logger


class ScriptSettings:
    logger = Logger("ScriptSettings")
    TEMP_DIR_NAME = 'temp'
    BACKUPS_DIR_NAME = 'backups'
    ENVS_DIR_NAME = 'environments'
    GLOBAL_ENV_CONFIG_FILE_NAME = 'global-configuration.cfg'
    ENV_CONFIG_FILE_NAME = 'environment-configuration.cfg'

    def __init__(self, options_passed_to_script, workdir=os.path.expanduser('~/.jtalks')):
        """ :param optparse.Values options_passed_to_script: thins that are passed with -f or --flags """
        self.env = options_passed_to_script.env
        self.build = options_passed_to_script.build
        self.project = options_passed_to_script.project
        self.grab_envs = options_passed_to_script.grab_envs
        self.sanity_test_timeout_sec = int(options_passed_to_script.sanity_test_timeout_sec)
        self.package_version = __version__

        self.work_dir = workdir
        self.temp_dir = os.path.join(self.work_dir, self.TEMP_DIR_NAME)
        self.backups_dir = os.path.join(self.work_dir, self.BACKUPS_DIR_NAME)
        self.global_configs_dir = os.path.join(self.work_dir, self.ENVS_DIR_NAME)
        self.env_configs_dir = os.path.join(self.global_configs_dir, self.env)

        self.global_config_path = os.path.join(self.global_configs_dir, self.GLOBAL_ENV_CONFIG_FILE_NAME)
        self.env_config_path = os.path.join(self.env_configs_dir, self.ENV_CONFIG_FILE_NAME)
        self.project_config_path = os.path.join(self.env_configs_dir, self.project + '.cfg')

        self.props = self._read_properties()

    def log_settings(self):
        self.logger.info('Script Settings: project=[{0}], env=[{1}], build number=[{2}], sanity test timeout=[{3}], '
                         'package version=[{4}]',
                         self.project, self.env, self.build, self.sanity_test_timeout_sec, self.package_version)
        self.logger.info("Environment configuration: [{0}]", self.env_configs_dir)

    def create_work_dir_if_absent(self):
        self._create_dir_if_absent(self.work_dir)
        self._create_dir_if_absent(self.env_configs_dir)
        self._create_dir_if_absent(self.backups_dir)

    def _create_dir_if_absent(self, directory):
        if not os.path.exists(directory):
            self.logger.info("Creating directory [{0}]", directory)
            os.makedirs(directory)

    def get_tomcat_port(self):
        return int(self.props.get('tomcat_http_port', 0))

    def get_tomcat_location(self):
        """ Gets value of the tomcat home from [project].cfg file related to particular env and project """
        return self.props.get('tomcat_location', None)

    def get_app_final_name(self):
        """ Gets the name of the application to be deployed (even if it's Poulpe, it can be deployed as ROOT.war). """
        return self.props.get('app_final_name', self.project)

    def get_plugins(self):
        if 'app_plugins' in self.props and self.props['app_plugins']:
            return self.props['app_plugins'].split(',')
        else:
            return []

    def get_plugins_dir(self):
        if 'app_plugins_dir' in self.props and self.props['app_plugins_dir']:
            return self.props['app_plugins_dir']
        return None

    def get_app_file_mapping(self):
        """
        :return dict: mapping of the src file name (located either in environments/ or in environments/env folder)
            without folder part and the destination file path (where to put those files on the server)
        """
        file_mapping = {}
        app_files_section = 'app-files_'
        for key in self.props.keys():
            if key.startswith(app_files_section):
                src_filename = key.replace(app_files_section, '')
                dst_filepath = self.props[key]
                file_mapping[src_filename] = dst_filepath
        return file_mapping

    def get_db_settings(self):
        """ :return DbSettings: db settings """
        return DbSettings.build(self.props)

    def deploy_configs(self):
        mapping = self.get_app_file_mapping()
        for key in mapping:
            src_filepath = os.path.join(self.env_configs_dir, key)
            if not os.path.exists(src_filepath):
                src_filepath = os.path.join(self.global_configs_dir, key)
            if not os.path.exists(src_filepath):
                self.logger.info('File {0} did not exist, skipping its deployment', key)
                continue
            dst_filepath = mapping[key]
            self.logger.info('Putting file [{0}]', dst_filepath)
            if not os.path.exists(os.path.dirname(dst_filepath)):
                self.logger.info('Creating dir [{0}] to place the file', os.path.dirname(dst_filepath))
                os.makedirs(os.path.dirname(dst_filepath))
            dst_file = file(dst_filepath, 'w')
            for line in open(src_filepath).readlines():
                dst_file.write(self._resolve_placeholder(self.props, line))
            dst_file.close()

    def _read_properties(self):
        """
        Reads props from global, env and project configs, then returns them as map with `section_option=value`.
        Values may contain placeholders referencing other options and special options like `${project}` & `${env}`
        """
        configs = [os.path.abspath(self.global_config_path), os.path.abspath(self.env_config_path),
                   os.path.abspath(self.project_config_path)]
        props = {}
        config = ConfigParser()
        for config_file in configs:
            abs_path = os.path.abspath(config_file)
            if os.path.exists(abs_path):
                self.logger.info('Reading config file [{0}]', abs_path)
                config.read(abs_path)
            else:
                self.logger.info('Could not read config file as it does not exist: [{0}]', abs_path)
        for section in config.sections():
            for option in config.options(section):
                props[section + '_' + option] = config.get(section, option)
        with_replaced_placeholders = {}
        for key in props.keys():
            with_replaced_placeholders[key] = self._resolve_placeholder(props, props[key])
        return with_replaced_placeholders

    def _resolve_placeholder(self, props, value, n_of_trial=0):
        if n_of_trial > 10:
            self.logger.warn('Could not resolve all placeholders in property value: {0}. Leaving it as is.', value)
            return value
        value = value.replace("${env}", self.env).replace("${project}", self.project)
        if value.find('${') != -1:
            for key in props.keys():
                value = value.replace('${' + key + '}', props[key])
        if value.find('${') != -1:
            value = self._resolve_placeholder(props, value, n_of_trial+1)
        return value


class DbSettings:
    REQUIRED_PROPS = ['app_db_name', 'app_db_user', 'app_db_host']

    def __init__(self, host, name, user, password, port=3306):
        self.password = password
        self.user = user
        self.port = port
        self.name = name
        self.host = host

    @staticmethod
    def build(props):
        """ :return DbSettings: db settings """
        for propname in DbSettings.REQUIRED_PROPS:
            if propname not in props.keys():
                raise RequiredPropertyNotFoundException(
                    'Property {0} was not found. All these properties are required: {1}'.format(
                        propname, ', '.join(DbSettings.REQUIRED_PROPS)))
        port = 3306
        password = ''
        if 'app_db_port' in props:
            port = int(props['app_db_port'])
        if 'app_db_password' in props:
            password = props['app_db_password']
        return DbSettings(props['app_db_host'], props['app_db_name'], props['app_db_user'], password, port)


class RequiredPropertyNotFoundException(Exception):
    pass
