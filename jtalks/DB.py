import os
import MySQLdb
import ConfigParser
from jtalks.util.Logger import Logger


class DB:
  """
    A class to work with DB (upload, download, search). Note, that for all the operations we need a connection to
   database which created by connect_to_database method. To connection need name of environments, which contained config file with properties to database.
  """
  env = None
  config = None
  dbHost = None
  dbUser = None
  dbPass = None
  dbName = None
  dbDefiner = None
  cursor = None
  connection = None
  jcName = None
  jcDescription = None
  jcUrl = None
  jcNotify = None
  poulpeAdminPass = None
  logger = Logger("DB")

  def __init__(self, script_settings):
    self.env = script_settings.env
    self.config = ConfigParser.ConfigParser()
    self.config.read(script_settings.get_env_configs_dir() + self.env + "/db.cfg")
    self.dbHost = self.config.get('db', 'host')
    self.dbUser = self.config.get('db', 'user')
    self.dbPass = self.config.get('db', 'pass')
    self.dbName = self.config.get('db', 'name')
    self.dbDefiner = self.config.get('db', 'definer')
    self.jcName = self.config.get('properties', 'jc_name')
    self.jcDescription = self.config.get('properties', 'jc_description')
    self.jcUrl = self.config.get('properties', 'jc_url')
    self.jcNotify = self.config.get('properties', 'jc_notify')
    self.poulpeAdminPass = self.config.get('properties', 'poulpe_admin_pass')

  def connect_to_database(self):
    """
      Create connection to database.
    """
    self.connection = MySQLdb.connect(host=self.dbHost, user=self.dbUser, passwd=self.dbPass)
    self.cursor = self.connection.cursor()

  def close_connection(self):
    """
      Close connection to database.
    """
    self.connection.close()

  def recreate_database(self):
    """
      Method removed database (whith name, which contains in dbName), and create new(empty)
      database whita same name.
    """
    self.logger.info("Recreating database {0}", self.dbName)
    self.cursor.execute('DROP DATABASE IF EXISTS ' + self.dbName)
    self.cursor.execute('CREATE DATABASE ' + self.dbName)


  def restore_database_from_file(self, backupPath):
    """
      This method get path to filename (.sql) with backup of database. And restoring backup to database whith name,
      which contains in dbName.
    """
    self.logger.info("Loading a db dump from [{0}]", backupPath)
    self.recreate_database()
    self.fix_definer_in_backup(backupPath)
    os.popen('mysql -u ' + self.dbUser + ' --password=' + self.dbPass + ' ' + self.dbName + ' < ' + backupPath).read()
    self.logger.info("Database restored: environment=[{0}]".format(self.env))


  def fix_definer_in_backup(self, backupPath):
    """
     For MySQL.
     If database contains VIEWS then created backup of database (by mysqldump) file contains lines with permissions (to
    user from origin database). When we restoring database to another server(it server don't have it user) we get a ERROR. To fix this problem, before restore we need replace all entries  (with DEFINER='{username}') to MySQL constant CURRENT_USER. This constant indicates that the law should give to the user on whose behalf is restored.
    """
    os.popen('sed -i \'s/DEFINER=' + self.dbDefiner + '/DEFINER=CURRENT_USER/g\' ' + backupPath).read()
    self.logger.info("Database definer fixed: environment=[{0}]".format(self.env))

  def update_properties_to_preprod(self):
    """
     This method update application properties in database. Need to call after restore.
    """
    self.cursor.execute('USE ' + self.dbName)
    self.logger.info("Changing forum name to [{0}]", self.jcName)
    self.cursor.execute(
      'UPDATE COMPONENTS SET NAME="' + self.jcName + '", DESCRIPTION="' + self.jcDescription + '" where COMPONENT_TYPE="FORUM"')
    self.logger.info("Switching off mail notifications")
    self.cursor.execute(
      'UPDATE PROPERTIES SET VALUE="' + self.jcNotify + '" where NAME="jcommune.sending_notifications_enabled"')
    self.cursor.execute('UPDATE PROPERTIES SET VALUE="' + self.jcUrl + '" where NAME="jcommune.url_address"')
    self.cursor.execute('UPDATE USERS SET PASSWORD=MD5(' + self.poulpeAdminPass + ') WHERE USERNAME="admin"')
    self.connection.commit()
    
   
  
