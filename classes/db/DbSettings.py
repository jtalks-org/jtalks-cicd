from xml.dom.minidom import parse
import re


class DbSettings:
  """
  Class keeping connection settings to the database
  """

  def __init__(self, project, config_file_location):
    """
    Creates connection settings object with given project name
    """
    self.dbHost = None
    self.dbUser = None
    self.dbPass = None
    self.dbName = None
    self.dbPort = None
    self.project = project.upper()
    self.parse_config(config_file_location)

  def parse_config(self, config_file_path):
    """
    Parses given config file and gets information about connection settings.
    """
    configs_doc = parse(config_file_path)
    env_elements = configs_doc.getElementsByTagName('Environment')

    for element in env_elements:
      name = element.getAttribute("name")
      value = element.getAttribute("value")

      if name == (self.project + "_DB_USER"):
        self.dbUser = value
      elif name == (self.project + "_DB_PASSWORD"):
        self.dbPass = value
      elif name == (self.project + "_DB_URL"):
        jdbc_pattern = 'mysql://(.*?):?(\d*)/(.*?)\?'
        (host, port, database) = re.compile(jdbc_pattern).findall(value)[0]
        self.dbHost = host
        self.dbName = database
        self.dbPort = port
