import time

import requests

from jtalks.sanity.SanityCheckFailedException import SanityCheckFailedException
from jtalks.util.Logger import Logger


__author__ = 'stanislav bashkirtsev'


class SanityTest:
  """
    Tests that application was deployed correctly without errors. For these purposes it opens some pages and determines
    whether they return HTML. If let's say they return HTTP 500, then the test failed. It has to break CI builds.
  """
  HOST = "127.0.0.1"
  SLEEP_TIME = 10
  logger = Logger("SanityTest")
  port = None
  app_name = None

  def __init__(self, tomcat_port, app_name, sanity_test_timeout_sec=120):
    """
     @param tomcat_port - an HTTP port to access the web server where application is
    """
    self.port = int(tomcat_port)
    self.app_name = app_name
    self.sanity_test_timeout_sec = sanity_test_timeout_sec
    if app_name == "ROOT":
      self.app_name = ""

  def check_app_started_correctly(self):
    self.logger.info("Sleeping for {0} seconds to give Tomcat time to start", self.SLEEP_TIME)
    time.sleep(self.SLEEP_TIME)
    request_address = "http://{0}:{1}/{2}".format(self.HOST, self.port, self.app_name)
    self.logger.info("Running sanity tests to check whether application started correctly and responds back..")
    self.logger.info("Connecting to {0}", request_address)
    response = requests.get(request_address, timeout=self.sanity_test_timeout_sec)
    if response.status_code not in [200, 201]:
      self.logger.error("While accessing main page, app answered with error: [{0} {1} {2}]",
                        response.status_code, response.reason, response.text)
      raise SanityCheckFailedException("Sanity check failed")
    self.logger.info("Sanity check passed: [{0} {1}]", response.status_code, response.reason)
