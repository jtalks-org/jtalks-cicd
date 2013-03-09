import unittest
from ApplicationContextTest import ApplicationContextTest
from DbSettingsTest import DbSettingsTest
from EnvListTest import EnvListTest
from TomcatTest import TomcatTest
from backup.BackuperTest import BackuperTest
from jtalks.util.LibVersion import LibVersion
from parser.TomcatServerXmlTest import TomcatServerXmlTest
from settings.ScriptSettingsTest import ScriptSettingsTest

if __name__ == '__main__':
  LibVersion().log_lib_versions()
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(ApplicationContextTest))
  suite.addTest(unittest.makeSuite(DbSettingsTest))
  suite.addTest(unittest.makeSuite(EnvListTest))
  suite.addTest(unittest.makeSuite(TomcatTest))
  suite.addTest(unittest.makeSuite(BackuperTest))
  suite.addTest(unittest.makeSuite(TomcatServerXmlTest))
  suite.addTest(unittest.makeSuite(ScriptSettingsTest))
  result = unittest.TextTestRunner(verbosity=2).run(suite)

  if result.wasSuccessful():
    exit(0)
  else:
    exit(1)