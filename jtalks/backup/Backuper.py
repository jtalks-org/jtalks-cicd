from datetime import datetime
import os
import shutil

from jtalks.util.Logger import Logger


class Backuper:
  """
    Responsible for backing up artifacts like war files, config files, as well as DB backups.
    Stores backups in the folder and allows to restore those backups from it.
    @author stanislav bashkirtsev
  """
  logger = Logger("Backuper")

  def __init__(self, backup_folder, script_settings, db_operations):
    """
      @param backup_folder a directory to put backups to, it may contain backups from different envs,
        thus a folder for each env will be created
      @param script_settings is instance of ScriptSettings class
      @param db_operations instance of DbOperations
    """
    if not backup_folder.endswith("/"):
      raise ValueError("Folder name should finish with '/'")
    self.backup_folder = backup_folder
    self.script_settings = script_settings
    self.db_operations = db_operations

  def backup(self):
    """
    Does all operations for project backup:
     - delete old backup data
     - backup the application database
     - backup application war-file
     - backup tomcat and ehcache configuration files
    """
    folder_to_put_backups = self.create_folder_to_backup(self.backup_folder, self.script_settings)
    self.backup_tomcat(folder_to_put_backups)
    self.backup_db(folder_to_put_backups)


  def create_folder_to_backup(self, backup_folder, script_settings):
    """
      We don't just put backups into a backup folder, we're creating a new folder there
      with current date so that our previous backups are kept there. E.g.:
      '/var/backups/prod/20130302T195924'

      @param backups_folder - basic folder to put backups there, it will be concatenated with env and current time
      @param script_settings to figure out what's the env and what's the project we're going to backup
    """
    now = datetime.now().strftime("%Y_%m_%dT%H_%M_%S")

    final_backup_folder = "{0}{1}/{2}/{3}".format(backup_folder, script_settings.env, script_settings.project, now)
    os.makedirs(final_backup_folder)
    self.logger.info("Backing up old resources to [{0}]", final_backup_folder)
    return final_backup_folder

  def backup_tomcat(self, backup_folder):
    """
      To be safe that we didn't forget anything, we're doing a backup for the whole tomcat directory.
      @param backup_folder a directory to put Tomcat to, should be created by the time this method is invoked
    """
    tomcat_location = self.script_settings.get_tomcat_location()
    if os.path.exists(tomcat_location):
      shutil.copytree(tomcat_location, backup_folder + "/tomcat")
    else:
      self.logger.info("There was no previous tomcat folder [{0}], so nothing to backup", tomcat_location)

  def backup_db(self, backup_folder):
    self.db_operations.backup_database(backup_folder)