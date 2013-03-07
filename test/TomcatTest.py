import unittest
from classes.Tomcat import Tomcat
from classes.backup.Backuper import Backuper
from classes.settings.ScriptSettings import ScriptSettings


class TomcatTest(unittest.TestCase):
  def test_paths(self):
    tomcat = Tomcat(Backuper(None, None, None), ScriptSettings(build=None, project='project1', env='unit-test'))

    self.assertEquals('project1.xml', tomcat.get_config_name())
    self.assertEquals('project1.ehcache.xml', tomcat.get_ehcache_config_name())
    self.assertEquals('location overriden by project config/conf/Catalina/localhost',
                      tomcat.get_config_folder_location())
    self.assertEquals('location overriden by project config/webapps', tomcat.get_web_apps_location())
    self.assertEquals('configs/unit-test/project1.xml', tomcat.get_config_file_location())


if __name__ == '__main__':
  unittest.main()