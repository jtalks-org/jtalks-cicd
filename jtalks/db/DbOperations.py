import os

import MySQLdb

from jtalks.util.Logger import Logger


class DbOperations:
    """ Base class for working with database """
    logger = Logger("DbBase")

    def __init__(self, dbsettings):
        """ :param jtalks.ScripSettings.DbSettings dbsettings: settings """
        self.dbsettings = dbsettings

    def connect_to_database(self):
        """ Connects to the specified database """
        self.logger.info("Connecting to [{0}] with user [{1}]", self.dbsettings.host, self.dbsettings.user)
        self.connection = MySQLdb.connect(host=self.dbsettings.host, user=self.dbsettings.user,
                                          passwd=self.dbsettings.password)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """ Closes open connection to the database """
        self.connection.close()

    def recreate_database(self):
        """ Deletes the specified database and create it again """
        self.logger.info("Dropping and creating database from scratch: [{0}]", self.dbsettings.name)
        self.cursor.execute('DROP DATABASE IF EXISTS ' + self.dbsettings.name)
        self.cursor.execute('CREATE DATABASE ' + self.dbsettings.name)

    def backup_database(self, backup_path):
        """ Backups database to given backupPath """
        self.logger.info("Backing up database [{0}] to [{1}] using user [{2}]",
                         self.dbsettings.name, backup_path, self.dbsettings.user)
        dump_command = "mysqldump -u'{0}'".format(self.dbsettings.user)
        if self.dbsettings.password:
            dump_command += " -p'{0}'".format(self.dbsettings.password)
        dump_command += " '{0}' > '{1}/{0}.sql'".format(self.dbsettings.name, backup_path)
        self.logger.info("Dumping DB: [{0}]", dump_command.replace(self.dbsettings.password, "***"))
        os.popen(dump_command.format(self.dbsettings.user, self.dbsettings.password,
                                     self.dbsettings.name, backup_path)).read()
        self.logger.info("Database backed up [{0}]".format(self.dbsettings.name))

    def restore_database_from_file(self, backupPath):
        """ Restores database from file specified in backupPath """
        self.logger.info("Loading a db dump from [{0}/{1}.sql]", backupPath, self.dbsettings.name)
        self.recreate_database()
        os.popen("mysql -u'{0}' -p'{1}' '{2}' < '{3}/{2}.sql'"
                 .format(self.dbsettings.user, self.dbsettings.password, self.dbsettings.name, backupPath)).read()
        self.logger.info("Database restored [{0}]".format(self.dbsettings.name))



