__author__ = 'stanislav bashkirtsev'


class LoadDbFromBackup:
  def __init__(self, db, ssh):
    self.db = db
    self.ssh = ssh

  def load(self):
    self.ssh.download_backup_prod_db()
    self.db.connect_to_database()
    self.db.restore_database_from_file(self.ssh.sftpBackupFileName)
    self.db.update_properties_to_preprod()
    self.db.connection.close()
    self.ssh.remove_backup_prod_db_file()
