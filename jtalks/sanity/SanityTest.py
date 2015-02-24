from time import sleep
import datetime

import requests
from requests.exceptions import ConnectionError

from jtalks.sanity.SanityCheckFailedException import SanityCheckFailedException
from jtalks.util.Logger import Logger


class SanityTest:
    """
      Tests that application was deployed correctly without errors. For these purposes it opens some pages and determines
      whether they return HTML. If let's say they return HTTP 500, then the test failed. It has to break CI builds.
    """
    HOST = "127.0.0.1"
    logger = Logger("SanityTest")
    port = None
    app_name = None

    def __init__(self, tomcat_port, app_name, sanity_test_timeout_sec=120, sleep_sec=30):
        """
         @param tomcat_port - an HTTP port to access the web server where application is
         @param sleep_sec - the amount of time tests ignore error responses as deployment failure. This is needed because
          first tomcat may not start quickly and therefore the response Connection Refused will be immediate. Thus when we
          send requests, first we should treat error messages as possible responses. After this sleep time error responses
          are considered as failed deployment.
        """
        self.port = int(tomcat_port)
        self.app_name = app_name
        self.sanity_test_timeout_sec = sanity_test_timeout_sec
        self.sleep_sec = sleep_sec
        if app_name == "ROOT":
            self.app_name = ""

    def check_app_started_correctly(self):
        request_address = "http://{0}:{1}/{2}".format(self.HOST, self.port, self.app_name)
        tests_sleep_end = datetime.datetime.now() + datetime.timedelta(seconds=self.sleep_sec)
        response = None
        attempt_counter = 0
        while tests_sleep_end > datetime.datetime.now():
            attempt_counter += 1
            self.logger.info(
                "[Attempt #{0}] Running sanity tests to check whether application started correctly and responds back..",
                attempt_counter)
            self.logger.info("[Attempt #{0}] Connecting to {1}", attempt_counter, request_address)
            try:
                response = requests.get(request_address, timeout=self.sanity_test_timeout_sec)
            except ConnectionError:
                self.logger.info("Sleeping for 5 sec..")
                sleep(5)  # so that we don't connect too often
                continue
            if response.status_code in [200, 201]:
                break
            else:
                self.logger.info("Error response, got {0} HTTP status. App server might still be booting.",
                                 response.status_code)
        if not response or response.status_code not in [200, 201]:
            self.logger.error('After {0} no successful response was received from the app. Finishing by timeout {1}',
                              attempt_counter, self.sanity_test_timeout_sec)
            if response:
                self.logger.error("Last time while accessing main page, app answered with error: [{0} {1} {2}]",
                                  response.status_code, response.reason, response.text)
            else:
                self.logger.error("App Server did not even get up!")
            raise SanityCheckFailedException("Sanity check failed")
        self.logger.info("Sanity check passed: [{0} {1}]", response.status_code, response.reason)
