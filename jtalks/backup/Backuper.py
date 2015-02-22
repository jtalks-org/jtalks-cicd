from datetime import datetime
import os
import shutil

from jtalks.util.Logger import Logger


class Backuper:
    """
      Responsible for backing up artifacts like war files, config files, as well as DB backups.
      Stores backups in the folder and allows to restore those backups from it.
    """
    logger = Logger("Backuper")
    BACKUP_FOLDER_DATE_FORMAT = "%Y_%m_%dT%H_%M_%S"

    def __init__(self, root_backup_folder, db_operations):
        """
        :param str root_backup_folder: a directory to put backups to, it may contain backups from different envs,
            thus a folder for each env will be created
        :param jtalks.db.DbOperations.DbOperations db_operations: instance of DbOperations
        """
        self.backup_folder = self.create_folder_to_backup(root_backup_folder)
        self.db_operations = db_operations

    def create_folder_to_backup(self, backup_folder):
        """
          We don't just put backups into a backup folder, we're creating a new folder there
          with current date so that our previous backups are kept there. E.g.:
          '/var/backups/prod/20130302T195924'
          :param str backup_folder: the root folder to create folders with datetime names for each backup
        """
        now = datetime.now().strftime(self.BACKUP_FOLDER_DATE_FORMAT)
        final_backup_folder = os.path.join(backup_folder, now)
        if not os.path.exists(final_backup_folder):
            self.logger.info("Creating a folder to store back ups: [{0}]", final_backup_folder)
            os.makedirs(final_backup_folder)
        return final_backup_folder

    def back_up_dir(self, folder_path):
        if os.path.exists(folder_path):
            head, folder_name = os.path.split(folder_path)
            backup_dst = os.path.join(self.backup_folder, folder_name)
            self.logger.info('Backing up [{0}] to [{1}]', folder_path, backup_dst)
            shutil.copytree(folder_path, backup_dst)
        else:
            backup_dst = None
            self.logger.info("There was no previous folder [{0}], so nothing to backup", folder_path)
        return backup_dst

    def back_up_db(self):
        self.db_operations.backup_database(self.backup_folder)
