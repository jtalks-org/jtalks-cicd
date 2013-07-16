from ConfigParser import ConfigParser, NoSectionError
import os
from jtalks.util.Logger import Logger

__author__ = 'stanislav bashkirtsev'


class ScriptSettings:
  SCRIPT_TEMD_DIR = '/tmp/jtalks-cicd/'
  script_work_dir = "" + os.path.expanduser("~/.jtalks/")
  backups_dir = script_work_dir + "backups/"
  ENV_CONFIGS_DIR = script_work_dir + "environments/"
  GLOBAL_CONFIG_LOCATION = ENV_CONFIGS_DIR + "global-configuration.cfg"
  logger = Logger("ScriptSettings")

  def __init__(self, build, project=None, env=None, grab_envs=None, work_dir=None, sanity_test_timeout_sec=120,
               package_version=None):
    """
     @param grab_envs - whether or not we should clone JTalks predefined environment configuration from private git
     repo
     @param work_dir - standard is ~/.jtalks, but it may be useful to override this value, e.g. during tests
     @param sanity_test_timeout_sec - how much time do sanity tests wait for the application to respond until they
            consider deployment as failed
    """
    self.env = env
    self.build = build
    self.project = project
    self.grab_envs = grab_envs
    self.script_work_dir = work_dir
    self.sanity_test_timeout_sec = sanity_test_timeout_sec
    self.package_version = package_version

  def log_settings(self):
    self.logger.info(
      "Script Settings: project=[{0}], env=[{1}], build number=[{2}], sanity test timeout=[{3}], package version=[{4}]",
      self.project, self.env, self.build, self.sanity_test_timeout_sec, self.package_version)
    self.logger.info("Environment configuration: [{0}]", self.ENV_CONFIGS_DIR)

  def create_work_dir_if_absent(self):
    self.__create_dir_if_absent__(self.script_work_dir)
    self.__create_dir_if_absent__(self.get_env_configs_dir())
    self.__create_dir_if_absent__(self.get_backup_folder())

  def __create_dir_if_absent__(self, directory):
    if not os.path.exists(directory):
      self.logger.info("Creating directory [{0}]", directory)
      os.mkdir(directory)

  def get_tomcat_location(self):
    """
      Gets value of the tomcat home from [project].cfg file related to particular env and project
    """
    return self.__get_property('tomcat', 'location')

  def get_app_final_name(self):
    """
      Gets the name of the application to be deployed (even if it's Poulpe, it can be deployed as ROOT.war).
    """
    return self.__get_property('app', 'final_name')

  def get_temp_dir(self):
    """
     Script can save there some temp files.
    """
    return self.SCRIPT_TEMD_DIR

  def get_tomcat_port(self):
    """
      This is not actually a pre-configured parameter, it parses $TOMCAT_HOME/conf/server.xml to find out the HTTP
      port it's going to be listening. This is needed e.g. for sanity tests to.
    """
    server_xml = os.path.join(self.get_tomcat_location(), "conf", "server.xml")
    raise RuntimeError("tomcat port parsing is not implemented yet")

  def get_backup_folder(self):
    return self.backups_dir

  def get_env_configs_dir(self):
    return self.ENV_CONFIGS_DIR

  def get_global_config_location(self):
    return self.GLOBAL_CONFIG_LOCATION

  def __get_property(self, section, prop_name):
    """
      Finds property first in project configuration, then environment configuration and if there is no such property
      there, then it looks is it up in global configuration.
      @param section - a section joins several properties under it
      @param prop_name - a particular property name from specified section
      @returns None if there is no such property found in any config
    """
    value = self.__get_project_property(section, prop_name)
    if value == None:
      value = self.__get_env_property(section, prop_name)
    if value == None:
      value = self.__get_global_prop(section, prop_name)
    if value == None:
      self.logger.error("Property [{0}] was not found in any configs", prop_name)
      raise ValueError
    return self.__replace_placeholders(value)

  def __get_project_property(self, section, prop_name):
    """
      Finds property value in project configuration. This overrides env and global configuration.
    """
    config = ConfigParser()
    config.read(os.path.join(self.ENV_CONFIGS_DIR, self.env, self.project + ".cfg"))
    return self.__get_value_from_config(config, section, prop_name)

  def __get_env_property(self, section, prop_name):
    """
      Finds property value in configs/${env}/${env}.cfg configuration file. This overrides global configuration, but
      still can be overriden by project configs. These configs are shared between apps of the same environment. E.g.
      if we have Poulpe and JCommune on UAT env, and there is a file configs/uat/uat.cfg, then these properties are
      shared between those Poulpe and JCommune.
    """
    config = ConfigParser()
    config.read(os.path.join(self.ENV_CONFIGS_DIR, self.env, "environment-configuration.cfg"))
    return self.__get_value_from_config(config, section, prop_name)

  def __get_global_prop(self, section, prop_name):
    """
      Finds a property value in configs/global-configuration.cfg.
    """
    config = ConfigParser()
    config.read(self.GLOBAL_CONFIG_LOCATION)
    return self.__get_value_from_config(config, section, prop_name)

  def __get_value_from_config(self, config, section, prop_name):
    try:
      return config.get(section, prop_name)
    except NoSectionError:
      return None

  def __replace_placeholders(self, prop_value):
    """
      Replaces placeholder for env and project that were possibly set in config files.
    """
    return prop_value.replace("${env}", self.env).replace("${project}", self.project)

  def get_sanity_test_timeout_sec(self):
    """
      How much time do sanity tests wait for the application response until they consider that the app didn't start
    """
    self.sanity_test_timeout_sec