import os
from jtalks.DB import DB
from jtalks.DeployToTomcatFacade import DeployToTomcatFacade
from jtalks.Nexus import Nexus
from jtalks.SSH import SSH
from jtalks.Tomcat import Tomcat
from jtalks.backup.Backuper import Backuper
from jtalks.db.DbOperations import DbOperations
from jtalks.db.DbSettings import DbSettings
from jtalks.db.LoadDbFromBackup import LoadDbFromBackup
from jtalks.parser.TomcatServerXml import TomcatServerXml
from jtalks.sanity.SanityTest import SanityTest
from jtalks.settings.ScriptSettings import ScriptSettings
from jtalks.util.EnvList import EnvList
from jtalks.util.EnvironmentConfigGrabber import EnvironmentConfigGrabber

__author__ = 'stanislav bashkirtsev'


class ApplicationContext:
  """
    Carries similar ideas to Spring's AppContext - it builds all the objects. This IoC is manual though, the objects
    are all constructed manually in Python code.
  """

  def __init__(self, environment, project, build, grab_envs, work_dir=None, sanity_test_timeout_sec=120, version=None):
    """
    @param work_dir - needed if you'd like to override a default work dir where all files reside, see ScriptSettings
                      for more details
    """
    self.script_settings = ScriptSettings(build=build, project=project, env=environment, grab_envs=grab_envs,
                                          work_dir=work_dir, sanity_test_timeout_sec=sanity_test_timeout_sec,
                                          package_version=version)
    self.script_settings.create_work_dir_if_absent()
    self.script_settings.log_settings()

  def nexus(self):
    return Nexus(build_number=self.script_settings.build)

  def tomcat(self):
    return Tomcat(backuper=self.backuper(), script_settings=self.script_settings)

  def backuper(self):
    return Backuper(self.script_settings.get_backup_folder(), self.script_settings, self.db_operations())

  def db_operations(self):
    return DbOperations(self.script_settings.env, self.db_settings())

  def db_settings(self):
    config_file_location = self.__project_config_file_location__(self.script_settings.env,
                                                                 self.script_settings.project)
    db_settings = DbSettings(project=self.script_settings.project, config_file_location=config_file_location)
    return db_settings

  def deploy_to_tomcat_facade(self):
    return DeployToTomcatFacade(self)

  def environment_config_grabber(self):
    return EnvironmentConfigGrabber(self.script_settings.get_env_configs_dir(), self.script_settings.get_temp_dir())

  def sanity_test(self):
    http_port = self.tomcat_server_xml().http_port()
    return SanityTest(tomcat_port=http_port, app_name=self.script_settings.get_app_final_name(),
                      sanity_test_timeout_sec=self.script_settings.get_sanity_test_timeout_sec())

  def tomcat_server_xml(self):
    return TomcatServerXml.fromfile(self.script_settings.get_tomcat_location() + "/conf/server.xml")

  def load_db_from_backup(self):
    return LoadDbFromBackup(self.db(), self.ssh())

  def ssh(self):
    return SSH(self.script_settings)

  def db(self):
    return DB(self.script_settings)

  def script_settings(self):
    return self.script_settings

  def env_list(self):
    return EnvList(script_settings=self.script_settings)

  def __project_config_file_location__(self, env, project):
    return os.path.join(self.script_settings.get_env_configs_dir(), env, project + ".xml")