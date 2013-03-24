from jtalks.ApplicationContext import ApplicationContext
from jtalks.util.Logger import Logger

__author__ = 'stanislav bashkirtsev'


class DeployToTomcatFacade:
  NEXUS_URL = "http://repo.jtalks.org/content/repositories/deployment-pipeline/deployment-pipeline/"
  logger = Logger("DeployToTomcatFacade")


  def deploy(self, build_number, project, env):
    if build_number is None:
      self.logger.error("Build number was not specified, see [{0}] to get list of builds", self.NEXUS_URL)
      raise RuntimeError
    if project not in ["jcommune", "poulpe"]:
      self.logger.error("A correct project should be specified: [poulpe, jcommune]")
      raise RuntimeError

    app_context = ApplicationContext(environment=env, project=project, build=build_number)
    app_context.environment_config_grabber().grab_jtalks_configs()
    app_context.nexus().download_war(project=app_context.script_settings.project)
    app_context.tomcat().deploy_war()
    app_context.sanity_test().check_app_started_correctly()
