import shutil
import subprocess
from subprocess import PIPE
import os

from jtalks.util.Logger import Logger


class Tomcat:
  """
  Class for deploying and backing up Tomcat applications
  """

  logger = Logger("Tomcat")

  def __init__(self, backuper, script_settings):
    self.backuper = backuper
    self.script_settings = script_settings

  def deploy_war(self):
    """
    Stops the Tomcat server, backups all necessary application data, copies
    new application data to Tomcat directories
    """
    self.logger.info("Deploying {0} to {1}", self.script_settings.project, self.script_settings.get_tomcat_location())
    self.stop()
    self.backuper.backup()
    self.move_war_to_webapps()
    self.put_configs_to_conf()
    self.start()

  def stop(self):
    """
    Stops the Tomcat server if it is running
    """
    stop_command = "pkill -9 -f {0}".format(self.script_settings.get_tomcat_location())
    self.logger.info("Killing tomcat [{0}]", stop_command)
    #dunno why but retcode always equals to SIGNAL (-9 in this case), didn't figure out how to 
    #distinguish errors from this
    retcode = subprocess.call([stop_command], shell=True, stdout=PIPE, stderr=PIPE)

  def move_war_to_webapps(self):
    """
    Moves application war-file to 'webapps' Tomcat subfolder
    """
    final_app_location = self.get_web_apps_location() + "/" + self.script_settings.get_app_final_name()
    self.remove_previous_app(final_app_location)
    self.logger.info("Putting new war file to Tomcat: [{0}]", final_app_location)
    shutil.move(self.script_settings.project + ".war", final_app_location + ".war")

  def remove_previous_app(self, app_location):
    if os.path.exists(app_location):
      self.logger.info("Removing previous app: [{0}]", app_location)
      shutil.rmtree(app_location)
    else:
      self.logger.info("Previous application was not found in [{0}], thus nothing to remove", app_location)

    war_location = app_location + ".war"
    if os.path.exists(war_location):
      self.logger.info("Removing previous war file: [{0}]", war_location)
      os.remove(war_location)

  def get_config_file_location(self):
    return os.path.join(self.script_settings.get_env_configs_dir(), self.script_settings.env, self.get_config_name())

  def put_configs_to_conf(self):
    """
    Copies configuration files for application and ehcache to Tomcat directories
    """
    final_conf_location = self.get_config_folder_location() + "/" + self.script_settings.get_app_final_name() + ".xml"
    conf_file_location = self.get_config_file_location()
    ehcache_config_file_location = os.path.join(self.script_settings.get_env_configs_dir(), self.script_settings.env,
                                                self.get_ehcache_config_name())

    self.logger.info("Putting [{0}] into [{1}]", conf_file_location, final_conf_location)
    shutil.copyfile(conf_file_location, final_conf_location)
    if os.path.exists(ehcache_config_file_location):
      shutil.copy(ehcache_config_file_location, self.script_settings.get_tomcat_location() + "/conf")

  def start(self):
    """
    Starts the Tomcat server
    """
    startup_file = self.script_settings.get_tomcat_location() + "/bin/startup.sh"
    self.logger.info("Starting Tomcat [{0}]", startup_file)
    subprocess.call(startup_file, shell=True, stdout=PIPE, stderr=PIPE)

  def get_ehcache_config_name(self):
    """
    Returns name of the Ehcache configuration file
    """
    return self.script_settings.project + ".ehcache.xml"

  def get_config_name(self):
    """
    Returns name of the Tomcat configuration file
    """
    return self.script_settings.project + ".xml"

  def get_config_folder_location(self):
    """
    Returns configuration folder for Tomcat
    """
    return os.path.join(self.script_settings.get_tomcat_location(), "conf", "Catalina", "localhost")

  def get_web_apps_location(self):
    """
    Returns path to web applications directory of Tomcat
    """
    return self.script_settings.get_tomcat_location() + "/webapps"