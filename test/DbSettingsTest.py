import unittest
from jtalks.db.DbSettings import DbSettings


class DbSettingsTest(unittest.TestCase):
  def testConfigWithoutPort(self):
    settings = DbSettings("project1", config_file_location="configs/unit-test/project1.xml")
    self.failUnlessEqual(settings.dbUser, 'pr1user')
    self.failUnlessEqual(settings.dbPass, 'pr1pass!#$')
    self.failUnlessEqual(settings.dbHost, 'localhost')
    self.failUnlessEqual(settings.dbName, 'pr1db')
    self.failUnless(settings.dbPort is None or len(settings.dbPort) == 0)

  def testConfigWitPort(self):
    settings = DbSettings("project2", config_file_location="configs/unit-test/project2.xml")
    self.failUnlessEqual(settings.dbUser, 'xxxx')
    self.failUnlessEqual(settings.dbPass, '(((!#$')
    self.failUnlessEqual(settings.dbHost, '192.168.1.1')
    self.failUnlessEqual(settings.dbName, 'pr2_db')
    self.failUnlessEqual(settings.dbPort, '1111')


if __name__ == '__main__':
  unittest.main()
