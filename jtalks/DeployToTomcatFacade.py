from jtalks.util.Logger import Logger

__author__ = 'stanislav bashkirtsev'


class DeployToTomcatFacade:
  NEXUS_URL = "http://repo.jtalks.org/content/repositories/deployment-pipeline/deployment-pipeline/"
  logger = Logger("DeployToTomcatFacade")

  def __init__(self, application_context):
    self.app_context = application_context

  def deploy(self):
    script_settings = self.app_context.script_settings
    self.__raise_if_settings_not_specified__(script_settings)

    if script_settings.grab_envs == "true":
      self.app_context.environment_config_grabber().grab_jtalks_configs()
    self.app_context.nexus().download_war(project=self.app_context.script_settings.project)
    self.app_context.tomcat().deploy_war()
    self.app_context.sanity_test().check_app_started_correctly()

  def __raise_if_settings_not_specified__(self, script_settings):
    if script_settings.build is None:
      self.logger.error("Build number was not specified, see [{0}] to get list of builds", self.NEXUS_URL)
      raise RuntimeError
    if script_settings.project not in ["jcommune", "poulpe", "antarcticle"]:
      self.logger.error("A correct project should be specified: [poulpe, jcommune, antarcticle]")
      raise RuntimeError
