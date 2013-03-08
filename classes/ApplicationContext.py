import os
from classes.Nexus import Nexus
from classes.Tomcat import Tomcat
from classes.backup.Backuper import Backuper
from classes.db.DbOperations import DbOperations
from classes.db.DbSettings import DbSettings
from classes.parser.TomcatServerXml import TomcatServerXml
from classes.sanity.SanityTest import SanityTest
from classes.util.EnvironmentConfigGrabber import EnvironmentConfigGrabber

__author__ = 'stanislav bashkirtsev'


class ApplicationContext:
  """
    Carries similar ideas to Spring's AppContext - it builds all the objects. This IoC is manual though, the objects
    are all constructed manually in Python code.
  """
  script_settings = None


  def __init__(self, script_settings):
    self.script_settings = script_settings

  def nexus(self):
    return Nexus(build_number=self.script_settings.build)

  def tomcat(self):
    return Tomcat(backuper=self.backuper(), script_settings=self.script_settings)

  def backuper(self):
    return Backuper("backups", self.script_settings, self.db_operations())

  def db_operations(self):
    return DbOperations(self.script_settings.env, self.db_settings())

  def db_settings(self):
    config_file_location = self.__project_config_file_location__(self.script_settings.env,
                                                                 self.script_settings.project)
    db_settings = DbSettings(project=self.script_settings.project, config_file_location=config_file_location)
    return db_settings

  def environment_config_grabber(self):
    return EnvironmentConfigGrabber()

  def sanity_test(self):
    http_port = self.tomcat_server_xml().http_port()
    return SanityTest(tomcat_port=http_port, app_name=self.script_settings.get_app_final_name())

  def tomcat_server_xml(self):
    return TomcatServerXml.fromfile(self.script_settings.get_tomcat_location() + "/conf/server.xml")

  def __project_config_file_location__(self, env, project):
    return os.path.join("configs", env, project + ".xml")