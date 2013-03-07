import sys
import pkg_resources
from optparse import OptionParser
import os
from classes.ApplicationContext import ApplicationContext
from classes.settings.ScriptSettings import ScriptSettings
from classes.util.LibVersion import LibVersion
from classes.util.Logger import Logger

__author__ = 'stanislav bashkirtsev'

"""
  This script downloads the artifact from Nexus (only project name and build number is enough because it's unique)
  and deploys the artifact to the Tomcat. 
  
  Run: python [scriptname].py -h to get list of options.
"""
logger = Logger("deploy_to_tomcat.py")


def main():
  LibVersion().log_lib_versions()
  settings = get_project_and_build_from_arguments()
  settings.log_settings()
  app_context = ApplicationContext(settings)
  app_context.nexus().download_war(project=settings.project)
  app_context.tomcat().deploy_war()
  app_context.sanity_test().check_app_started_correctly()


def get_project_and_build_from_arguments():
  """
  Gets the build number from parameters passed to the script (the -b or --build options). 
  If nothing was specified, None is returned.
  """
  available_envs = os.listdir("configs")
  parser = OptionParser()
  parser.add_option("-b", "--build", dest="build_number",
                    help="The build number of the Deployment Pipline to deploy a unique artifact to Nexus.")
  parser.add_option("-p", "--project", dest="project",
                    help="Project name to be deployed to tomcat (e.g. jcommune, poulpe)")
  parser.add_option("-e", "--environment", dest="env",
                    help="Environment to be deployed. Environment MUST exist on current server. Possible values: {0}".format(
                      available_envs))

  (options, args) = parser.parse_args()
  return ScriptSettings(options.build_number, options.project, options.env)


"""Starting the script by invoking main() method """
if __name__ == "__main__":
  main()
