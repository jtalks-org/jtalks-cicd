import os
from optparse import OptionParser

from jtalks.DB import DB
from jtalks.SSH import SSH
from jtalks.util.Logger import Logger

logger = Logger("prod_db_to_preprod")


def main():
  """
   For PREPROD env we need a PROD database grabbed from backups and applied.
  """
  env = get_project_and_build_from_arguments()
  logger.info("Starting to upload PROD database to {0}", env)
  ssh = SSH(env)
  db = DB(env)
  ssh.download_backup_prod_db()
  db.connect_to_database()
  db.restore_database_from_file(ssh.sftpBackupFileName)
  db.update_properties_to_preprod()
  db.connection.close()
  ssh.remove_backup_prod_db_file()


def get_project_and_build_from_arguments():
  parser = OptionParser()
  parser.add_option("-e", "--environment", dest="env",
                    help="Environment")

  (options, args) = parser.parse_args()
  return options.env


main()
