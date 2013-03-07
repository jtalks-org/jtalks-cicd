import shutil
import git.repo as repo
from classes.util.Logger import Logger

__author__ = 'stanislav bashkirtsev'


class EnvironmentConfigGrabber:
  CLONE_REPO_TO = '/tmp/jtalks-cicd/environments'
  logger = Logger("EnvironmentConfigGrabber")

  def grab_jtalks_configs(self):
    self.__remove_previous_configs__()
    repo.Repo.clone_from('git@jtalks.org:environments', self.CLONE_REPO_TO)
    shutil.copytree(self.CLONE_REPO_TO + "/configs", "./configs")

  def __remove_previous_configs__(self):
    try:
      self.logger.info("Removing {0} directory if it was there", self.CLONE_REPO_TO)
      shutil.rmtree(self.CLONE_REPO_TO)
    except OSError as e:
      if e.errno is not 2:#No such file or directory
        self.logger.warn(e.message)
