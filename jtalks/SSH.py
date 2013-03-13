import os
import ConfigParser

import paramiko
from jtalks.util.Logger import Logger


class SSH:
  env = None
  config = None
  sftpTransport = None
  sftpClient = None
  sftpHost = None
  sftpPort = None
  sftpUser = None
  sftpPass = None
  sftpBackupArchive = None
  sftpBackupFileName = None
  logger = Logger("SSH")

  def __init__(self, script_settings):
    self.env = script_settings.env
    self.config = ConfigParser.ConfigParser()
    self.config.read(script_settings.get_env_configs_dir() + self.env + "/ssh.cfg")
    self.sftpHost = self.config.get('sftp', 'sftp_host')
    self.sftpPort = self.config.get('sftp', 'sftp_port')
    self.sftpUser = self.config.get('sftp', 'sftp_user')
    self.sftpPass = self.config.get('sftp', 'sftp_pass')
    self.sftpBackupArchive = self.config.get('sftp', 'sftp_backup_archive')
    self.sftpBackupFileName = self.config.get('sftp', 'sftp_backup_filename')

  def download_backup_prod_db(self):
    self.sftp_connection()
    attrList = self.sftpClient.listdir_attr('.')
    attrTimeTmp = 0
    dirWithLastUpdate = None
    for attr in attrList:
      if attrTimeTmp < attr.st_mtime:
        attrTimeTmp = attr.st_mtime
        dirWithLastUpdate = attr.filename
    self.sftpClient.get(dirWithLastUpdate + '/' + self.sftpBackupArchive, './' + self.sftpBackupArchive)
    os.popen('bunzip2 -d ' + self.sftpBackupArchive)
    self.sftp_connection_close()

  def sftp_connection_close(self):
    self.sftpClient.close()
    self.sftpTransport.close()

  def sftp_connection(self):
    self.logger.info("Getting a DB backup from {0}", self.sftpHost)
    self.sftpTransport = paramiko.Transport((self.sftpHost, int(self.sftpPort)))
    self.sftpTransport.connect(username=self.sftpUser, password=self.sftpPass)
    self.sftpClient = paramiko.SFTPClient.from_transport(self.sftpTransport)

  def remove_backup_prod_db_file(self):
    os.popen('rm -rf ' + self.sftpBackupFileName)  

  
