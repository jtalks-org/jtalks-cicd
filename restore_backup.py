from optparse import OptionParser
import os

__author__ = 'stanislav bashkirtsev'


def main():
  print get_project_env_and_backupname_from_arguments()


def get_project_env_and_backupname_from_arguments():
  available_envs = os.listdir('configs')
  parser = OptionParser()
  parser.add_option('-p', '--project', dest='project',
                    help='Project name to be deployed to tomcat (e.g. jcommune, poulpe)')
  parser.add_option('-e', '--environment', dest='env',
                    help='Environment to be deployed. Environment MUST exist on current server. Possible values: {0}'.format(
                      available_envs))
  parser.add_option('-n', '--backup-name', dest='backup_name',
                    help='Name of the backup in form of dates like 2013_03_04T21_08_40')
  return parser.parse_args()


main()
