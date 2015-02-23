import os

from jtalks.ScriptSettings import ScriptSettings
from jtalks.util.Logger import Logger


class EnvList:
    """ Can list all the envs and apps. """
    logger = Logger("EnvList")

    def __init__(self, global_configs_dir):
        """ :param str global_configs_dir: the environments/ dir """
        self.global_configs_dir = global_configs_dir

    def list_envs(self):
        self.logger.info('[%s]' % ', '.join(map(str, self.get_list_of_envs())))

    def get_list_of_envs(self):
        envs = os.listdir(self.global_configs_dir)  # dir contains folders with envs configuration
        global_configuration_file = 'global-configuration.cfg'
        if global_configuration_file in envs:
            envs.remove(global_configuration_file)
        return envs

    def list_projects(self, env):
        projects = os.listdir(os.path.join(self.global_configs_dir, env))
        if ScriptSettings.ENV_CONFIG_FILE_NAME in projects:
            projects.remove(ScriptSettings.ENV_CONFIG_FILE_NAME)
        return [project.replace(".cfg", "") for project in projects if project.endswith(".cfg")]

    def print_envs_with_projects(self):
        for env in self.get_list_of_envs():
            print env
            for project in self.list_projects(env):
                print "  |_" + project
