import os

import MySQLdb

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
    cursor = None
    connection = None
    jcName = None
    jcDescription = None
    jcUrl = None
    jcNotify = None
    poulpeAdminPass = None
    logger = Logger("DB")

    def __init__(self, dbsettings, scriptsettings):
        self.dbHost = dbsettings.host
        self.dbUser = dbsettings.user
        self.dbPass = dbsettings.password
        self.dbName = dbsettings.name
        self.jcName = scriptsettings.props('forum_name')
        self.jcDescription = scriptsettings.props('forum_description')
        self.jcUrl = scriptsettings.props('forum_url')
        self.jcNotify = scriptsettings.props('forum_notify')
        self.poulpeAdminPass = scriptsettings.props('forum_poulpe_admin_pass')

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
        os.popen(
            'mysql -u ' + self.dbUser + ' --password=' + self.dbPass + ' ' + self.dbName + ' < ' + backupPath).read()
        self.logger.info("Database restored: environment=[{0}]".format(self.env))


    def fix_definer_in_backup(self, backupPath):
        """
         For MySQL.
         If database contains VIEWS then created backup of database (by mysqldump) file contains lines with permissions
         (to user from original database). When we restoring database on another server (the server that doesn't have
         that user) we get an ERROR. To fix this problem, before restore we need remove all entries
         (with DEFINER='{username}') and the view will be created and will be invoked by the user that created the DB.
        """
        os.popen("sed -i 's/DEFINER=[^*]*\*/\*/g' " + backupPath).read()
        self.logger.info("Database definer fixed: environment=[{0}]".format(self.env))

    def update_properties_to_preprod(self):
        """
         This method update application properties in database. Need to call after restore.
        """
        self.cursor.execute('USE ' + self.dbName)
        self.logger.info("Changing forum name to [{0}]", self.jcName)
        self.cursor.execute('UPDATE COMPONENTS SET NAME="' + self.jcName + '", DESCRIPTION="' + self.jcDescription
                            + '" where COMPONENT_TYPE="FORUM"')
        self.logger.info("Switching off mail notifications")
        self.cursor.execute('UPDATE PROPERTIES SET VALUE="' + self.jcUrl + '" where NAME="jcommune.url_address"')
        self.cursor.execute('UPDATE USERS SET PASSWORD=MD5(' + self.poulpeAdminPass + ') WHERE USERNAME="admin"')
        self.connection.commit()
    
   
  
