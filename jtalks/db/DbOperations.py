import os

import MySQLdb

from jtalks.util.Logger import Logger


class DbOperations:
    """ Base class for working with database """
    logger = Logger("DbBase")

    def __init__(self, host, user, password, name, port=3306):
        self.port = port
        self.name = name
        self.password = password
        self.user = user
        self.host = host

    def connect_to_database(self):
        """ Connects to the specified database """
        self.logger.info("Connecting to [{0}] with user [{1}]", self.host, self.user)
        self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """ Closes open connection to the database """
        self.connection.close()

    def recreate_database(self):
        """ Deletes the specified database and create it again """
        self.logger.info("Dropping and creating database from scratch: [{0}]", self.name)
        self.cursor.execute('DROP DATABASE IF EXISTS ' + self.name)
        self.cursor.execute('CREATE DATABASE ' + self.name)

    def backup_database(self, backup_path):
        """ Backups database to given backupPath """
        self.logger.info("Backing up database [{0}] to [{1}] using user [{2}]",
                         self.name, backup_path, self.user)
        dump_command = "mysqldump -u'{0}'".format(self.user)
        if self.password:
            dump_command += "-p'{0}'".format(self.password)
        dump_command += "'{0}' > '{1}/{0}.sql'".format(self.name, backup_path)
        os.popen(dump_command.format(self.user, self.password, self.name, backup_path)).read()
        self.logger.info("Database backed up [{0}]".format(self.name))

    def restore_database_from_file(self, backupPath):
        """ Restores database from file specified in backupPath """
        self.logger.info("Loading a db dump from [{0}/{1}.sql]", backupPath, self.name)
        self.recreate_database()
        os.popen("mysql -u'{0}' -p'{1}' '{2}' < '{3}/{2}.sql'"
                 .format(self.user, self.password, self.name, backupPath)).read()
        self.logger.info("Database restored [{0}]".format(self.name))



