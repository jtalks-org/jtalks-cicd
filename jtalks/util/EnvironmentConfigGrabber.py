import os
import shutil
from git import GitCommandError
import git.repo as repo
from jtalks.util.Logger import Logger

__author__ = 'stanislav bashkirtsev'


class EnvironmentConfigGrabber:
  CLONE_REPO_TO = '/tmp/jtalks-cicd/environments'
  GRABBED_CONFIGS_LOCATION = CLONE_REPO_TO + "/configs"
  logger = Logger("EnvironmentConfigGrabber")

  def __init__(self, env_configs_root):
    self.env_configs_root = env_configs_root

  def grab_jtalks_configs(self):
    try:
      self.__remove_previous_git_folder__()
      repo.Repo.clone_from('git@jtalks.org:environments', self.CLONE_REPO_TO)
      self.__copy_grabbed_configs_into_work_dir__()
    except GitCommandError:
      self.logger.warn("You don't have access to JTalks repo with environment configs. You may want to use your own "
                       + "local environment. Create a folder with env name in configs directory. If you think you "
                       + "need access to JTalks internal envs (including UAT, DEV, PREPROD, PROD envs), "
                       + "you should write a request to project@jtalks.org.")

  def __remove_previous_git_folder__(self):
    try:
      if os.path.exists(self.CLONE_REPO_TO):
        self.logger.info("Removing {0} directory if it was there", self.CLONE_REPO_TO)
        shutil.rmtree(self.CLONE_REPO_TO)
    except OSError as e:
      if e.errno is not 2:#No such file or directory
        self.logger.warn(e.message)

  def __copy_grabbed_configs_into_work_dir__(self):
    grabbed_dirs_and_files = os.listdir(self.GRABBED_CONFIGS_LOCATION)
    for next_grabbed_file_or_dir in grabbed_dirs_and_files:
      destination_file = self.env_configs_root + next_grabbed_file_or_dir
      if os.path.exists(destination_file):
        self.logger.info("{0} will be overwritten by newer version from git repo", destination_file)
        self.__delete_file_or_dir__(destination_file)
      shutil.move(self.GRABBED_CONFIGS_LOCATION + "/" + next_grabbed_file_or_dir, destination_file)

  def __delete_file_or_dir__(self, destination_file):
    if os.path.isfile(destination_file):
      os.remove(destination_file)
    else:
      shutil.rmtree(destination_file)
