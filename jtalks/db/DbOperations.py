import os
import MySQLdb

from jtalks.util.Logger import Logger


class DbOperations:
  """
    Base class for working with database
  """
  logger = Logger("DbBase")
  env = None
  db_settings = None

  def __init__(self, env, db_settings):
    """
    Args:
    env: environment name e.g. dev, uat
    db_settings: database connection settings of type DbSettings, which will be used for all
                 database related operations
    """
    self.env = env
    self.db_settings = db_settings


  def connect_to_database(self):
    """
    Connects to the specified database
    """
    self.logger.info("Connecting to [{0}] with user [{1}]", self.db_settings.dbHost, self.db_settings.dbUser)
    self.connection = MySQLdb.connect(host=self.db_settings.dbHost, user=self.db_settings.dbUser,
                                      passwd=self.db_settings.dbPass)
    self.cursor = self.connection.cursor()

  def close_connection(self):
    """
    Closes open connection to the database
    """
    self.connection.close()

  def recreate_database(self):
    """
    Deletes the specified database and create it again
    """
    self.logger.info("Dropping and creating database from scratch: [{0}]", self.db_settings.dbName)
    self.cursor.execute('DROP DATABASE IF EXISTS ' + self.db_settings.dbName)
    self.cursor.execute('CREATE DATABASE ' + self.db_settings.dbName)

  def backup_database(self, backupPath):
    """
    Backups database to given backupPath
    """
    self.logger.info("Backing up database [{0}] to [{1}] using user [{2}]",
                     self.db_settings.dbName, backupPath, self.db_settings.dbUser)
    os.popen("mysqldump -u{0} -p{1} {2} > {3}/{2}.sql"
      .format(self.db_settings.dbUser, self.db_settings.dbPass, self.db_settings.dbName, backupPath)) \
      .read()
    self.logger.info("Database backed up: environment=[{0}]".format(self.env))

  def restore_database_from_file(self, backupPath):
    """
    Restores database from file specified in backupPath
    """
    self.logger.info("Loading a db dump from [{0}/{1}.sql]", backupPath, self.db_settings.dbName)
    self.recreate_database()
    os.popen('mysql -u{0} -p{1} {2} < {3}/{2}.sql'
      .format(self.db_settings.dbUser,self.db_settings.dbPass, self.db_settings.dbName, backupPath))\
      .read()
    self.logger.info("Database restored: environment=[{0}]".format(self.env))



