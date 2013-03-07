import os

__author__ = 'ctapobep'


class EnvList:
  """
    Can list all the envs and apps.
  """

  def list_envs(self):
    return os.listdir("configs")

  def list_projects(self, env):
    projects = os.listdir("configs/" + env)
    return [project.replace(".cfg", "") for project in projects if project.endswith(".cfg")]

  def print_envs_with_projects(self):
    for env in self.list_envs():
      print env
      for project in self.list_projects(env):
        print "  |_" + project