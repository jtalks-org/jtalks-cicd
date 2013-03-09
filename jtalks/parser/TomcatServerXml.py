import xml.etree.ElementTree as ElementTree
from jtalks.parser.WrongConfigException import WrongConfigException
from jtalks.util.Logger import Logger

__author__ = 'stanislav bashkirtsev'


class TomcatServerXml:
  """
    Parses $TOMCAT_HOME/conf/server.xml file and returns attributes and tag values.
  """
  logger = Logger("TomcatServerXml")
  HTTP_PROTOCOL = "HTTP/1.1"
  tree = None

  def __init__(self, xml_element):
    """
      Creates a file from xml element object
      @param xml_element server.xml already parsed into xml.etree.Element
    """
    self.tree = xml_element

  @staticmethod
  def fromfile(filename):
    """
      Parses the specified server.xml
    """
    Logger("TomcatServerXml").info("Parsing [{0}] to obtain information about Tomcat", filename)
    return TomcatServerXml(ElementTree.parse(filename))

  @staticmethod
  def fromstring(file_content):
    """
      Creates object from string instead of from file
    """
    return TomcatServerXml(ElementTree.fromstring(file_content))

  def http_port(self):
    """
      Parses server.xml and obtains a Connector with protocol="HTTP/1.1". Returns its port.
    """
    http_connectors = self.tree.findall("./Service/Connector")
    http_connector = None
    for connector in http_connectors:
      if connector.get("protocol") == self.HTTP_PROTOCOL:
        http_connector = connector
        break
    if http_connector is None:
      error_message = "$TOMCAT_HOME/conf/server.xml didn't contain Connector with HTTP/1.1 protocol"
      self.logger.error(error_message)
      raise WrongConfigException(error_message)
    return http_connector.get("port")