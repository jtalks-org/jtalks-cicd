from jtalks.DB import DB
from jtalks.SSH import SSH

__author__ = 'stanislav bashkirtsev'

class LoadDbFromBackup:
  def __init__(self, env):
    self.env = env

  def load(self):
    ssh = SSH(self.env)
    db = DB(self.env)
    ssh.download_backup_prod_db()
    db.connect_to_database()
    db.restore_database_from_file(ssh.sftpBackupFileName)
    db.update_properties_to_preprod()
    db.connection.close()
    ssh.remove_backup_prod_db_file()
