import unittest
from classes.parser.TomcatServerXml import TomcatServerXml
from classes.parser.WrongConfigException import WrongConfigException

__author__ = 'stanislav bashkirtsev'


class TomcatServerXmlTest(unittest.TestCase):
  def test_http_port_is_returned(self):
    server_xml = TomcatServerXml.fromstring(self.get_valid_tomcat_file_content())
    self.assertEquals("8080", server_xml.http_port())

  def test_raises_if_http_port_not_found(self):
    server_xml = TomcatServerXml.fromstring(self.get_file_without_http_port())
    self.assertRaises(WrongConfigException, server_xml.http_port)

  def get_valid_tomcat_file_content(self):
    return """<?xml version='1.0' encoding='utf-8'?>
<Server port="8005" shutdown="SHUTDOWN">
  <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" />
  <Listener className="org.apache.catalina.core.JasperListener" />
  <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener" />
  <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener" />
  <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener" />

  <GlobalNamingResources>
    <Resource name="UserDatabase" auth="Container"
              type="org.apache.catalina.UserDatabase"
              description="User database `that can be updated and saved"
              factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
              pathname="conf/tomcat-users.xml" />
  </GlobalNamingResources>
  <Service name="Catalina">
    <Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8443" />
    <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />
    <Engine name="Catalina" defaultHost="localhost">
      <Realm className="org.apache.catalina.realm.LockOutRealm">
        <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
               resourceName="UserDatabase"/>
      </Realm>
      <Host name="localhost"  appBase="webapps"
            unpackWARs="true" autoDeploy="true">
        <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="localhost_access_log." suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" />

      </Host>
    </Engine>
  </Service>
</Server>"""

  def get_file_without_http_port(self):
    return """<?xml version='1.0' encoding='utf-8'?> <Server port="8005" shutdown="SHUTDOWN">
  <Service name="Catalina">
    <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" />
  </Service>
</Server>"""

