import os
import shutil
from git import GitCommandError
import git.repo as repo
from jtalks.util.Logger import Logger


class EnvironmentConfigGrabber:
    logger = Logger('EnvironmentConfigGrabber')

    def __init__(self, env_configs_root, temp_dir):
        self.env_configs_root = env_configs_root
        self.temp_dir = temp_dir
        self.clone_repo_to = os.path.join(temp_dir, 'environments')
        self.grabbed_configs_location = os.path.join(self.clone_repo_to, 'configs')

    def grab_jtalks_configs(self):
        try:
            self.__remove_previous_git_folder__()
            self.__create_jtalks_temp_dir__()
            self.logger.info('Cloning environments to {0}', self.clone_repo_to)
            repo.Repo.clone_from('git@jtalks.org:environments', self.clone_repo_to)
            self.__copy_grabbed_configs_into_work_dir__()
        except GitCommandError as e:
            self.logger.warn(
                "You don't have access to JTalks repo with environment configs. You may want to use your own "
                + "local environment. Create a folder with env name in configs directory. If you think you "
                + "need access to JTalks internal envs (including UAT, DEV, PREPROD, PROD envs), "
                + "you should write a request to project@jtalks.org.")
            raise e

    def __remove_previous_git_folder__(self):
        try:
            if os.path.exists(self.clone_repo_to):
                self.logger.info("Removing {0} directory if it was there", self.clone_repo_to)
                shutil.rmtree(self.clone_repo_to)
        except OSError as e:
            if e.errno is not 2:  # No such file or directory
                self.logger.warn(e.message)

    def __copy_grabbed_configs_into_work_dir__(self):
        grabbed_dirs_and_files = os.listdir(self.grabbed_configs_location)
        for next_grabbed_file_or_dir in grabbed_dirs_and_files:
            destination_file = os.path.join(self.env_configs_root, next_grabbed_file_or_dir)
            self.logger.info('Creating [{0}]', os.path.abspath(destination_file))
            if os.path.exists(destination_file):
                self.__delete_file_or_dir__(destination_file)
            shutil.move(os.path.join(self.grabbed_configs_location, next_grabbed_file_or_dir), destination_file)

    def __delete_file_or_dir__(self, destination_file):
        if os.path.isfile(destination_file):
            os.remove(destination_file)
        else:
            shutil.rmtree(destination_file)

    def __create_jtalks_temp_dir__(self):
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)
