from optparse import OptionParser
from classes.ApplicationContext import ApplicationContext
from classes.settings.ScriptSettings import ScriptSettings


def main():
  build_number = get_build_from_arguments()
  # as for now the convention is scripts are inside of jcommune or poulpe project
  ApplicationContext(ScriptSettings(build_number)).nexus().upload_war("../pom.xml")


def get_build_from_arguments():
  """
    Gets the build number from parameters passed to the script (the -b or --build options).
    If nothing was specified, None is returned.
  """
  parser = OptionParser()
  parser.add_option("-b", "--build", dest="build_number",
                    help="The build number of the Deployment Pipline to deploy a unique artifact to Nexus.")
  (options, args) = parser.parse_args()
  return options.build_number


"""Starting the script by invoking main() method """
if __name__ == "__main__":
  main()
