import os
from jtalks.util.Logger import Logger

__author__ = 'ctapobep'


class EnvList:
  """
    Can list all the envs and apps.
  """
  logger = Logger("EnvList")

  def __init__(self, script_settings):
    self.script_settings = script_settings

  def list_envs(self):
    self.logger.info('[%s]' % ', '.join(map(str, self.get_list_of_envs())))

  def get_list_of_envs(self):
    envs = os.listdir(self.script_settings.get_env_configs_dir())
    envs.remove("global-configuration.cfg")
    return envs

  def list_projects(self, env):
    projects = os.listdir(os.path.join(self.script_settings.get_env_configs_dir(), env))
    return [project.replace(".cfg", "") for project in projects if project.endswith(".cfg")]

  def print_envs_with_projects(self):
    for env in self.list_envs():
      print env
      for project in self.list_projects(env):
        print "  |_" + project