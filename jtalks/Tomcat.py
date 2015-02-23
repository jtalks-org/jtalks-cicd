import shutil
import subprocess
from subprocess import PIPE
import os

from jtalks.util.Logger import Logger


class Tomcat:
    """ Class for deploying and backing up Tomcat applications """

    logger = Logger("Tomcat")

    def __init__(self, tomcat_location):
        """ :param str tomcat_location: location of the tomcat root dir """
        self.tomcat_location = tomcat_location
        if self.tomcat_location and os.path.exists(tomcat_location):
            self.logger.info('Tomcat location: [{0}]', tomcat_location)
        else:
            self.logger.warn('Tomcat location was not set or it does not exist: [{0}]', tomcat_location)

    def stop(self):
        """ Stops the Tomcat server if it is running """
        if not os.path.exists(self.tomcat_location):
            raise TomcatNotFoundException('Could not found tomcat: [{0}]'.format(self.tomcat_location))
        stop_command = 'pkill -9 -f {0}'.format(os.path.abspath(self.tomcat_location))
        self.logger.info('Killing tomcat [{0}]', stop_command)
        # dunno why but return code always equals to SIGNAL (-9 in this case), didn't figure out how to
        # distinguish errors from this
        subprocess.call([stop_command], shell=True, stdout=PIPE, stderr=PIPE)

    def start(self):
        """ Starts the Tomcat server """
        if not os.path.exists(self.tomcat_location):
            raise TomcatNotFoundException('Could not found tomcat: [{0}]'.format(self.tomcat_location))
        startup_file = self.tomcat_location + "/bin/startup.sh"
        self.logger.info("Starting Tomcat [{0}]", startup_file)
        pipe = subprocess.Popen(['/bin/bash', startup_file], shell=False, stdout=PIPE, stderr=PIPE)
        out, err = pipe.communicate()
        if pipe.returncode != 0:
            error = 'Could not start Tomcat, return code: {0}'.format(pipe.returncode)
            self.logger.error(error)
            self.logger.error(out)
            self.logger.error(err)
            raise CouldNotStartTomcatException(error)

    def move_to_webapps(self, src_filepath, appname):
        """
        Moves application war-file to 'webapps' Tomcat sub-folder
        :param str src_filepath: to get artifact from
        :param str appname: the name of the webapp to be deployed
        """
        webapps_location = os.path.join(self.tomcat_location, 'webapps')
        final_app_location = os.path.join(webapps_location, appname)
        self.logger.info('Putting new war file to Tomcat: [{0}]', final_app_location)
        if not os.path.exists(webapps_location):
            error = 'Tomcat webapps folder was not found in [{0}], configuration must have been wrong. ' \
                    'Please configure correct Tomcat location. Current location contains: {1}' \
                .format(self.tomcat_location, os.listdir(self.tomcat_location))
            self.logger.error(error)
            raise TomcatNotFoundException(error)
        self._remove_previous_app(final_app_location)
        shutil.move(src_filepath, final_app_location + '.war')
        return final_app_location + '.war'

    def _remove_previous_app(self, app_location):
        if os.path.exists(app_location):
            self.logger.info("Removing previous app: [{0}]", app_location)
            shutil.rmtree(app_location)
        else:
            self.logger.info("Previous application was not found in [{0}], thus nothing to remove", app_location)

        war_location = app_location + ".war"
        if os.path.exists(war_location):
            self.logger.info("Removing previous war file: [{0}]", war_location)
            os.remove(war_location)


class TomcatNotFoundException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


class CouldNotStartTomcatException(Exception):
    pass
