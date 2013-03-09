import pkg_resources
import sys
from jtalks.util.Logger import Logger

__author__ = 'stanislav bashkirtsev'


class LibVersion:
  logger = Logger("LibVersions")

  def log_lib_versions(self):
    self.logger.info("python={0}", sys.version_info)
    self.__log_lib_version("requests")
    self.__log_lib_version("GitPython")
    self.__log_lib_version("mock")


  def __log_lib_version(self, libname):
    self.logger.info("{0}={1}", libname, pkg_resources.get_distribution(libname).version)