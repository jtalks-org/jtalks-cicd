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
        self.logger.info('Tomcat location: [{0}]', tomcat_location)

    def stop(self):
        """ Stops the Tomcat server if it is running """
        stop_command = 'pkill -9 -f {0}'.format(os.path.abspath(self.tomcat_location))
        self.logger.info('Killing tomcat [{0}]', stop_command)
        # dunno why but return code always equals to SIGNAL (-9 in this case), didn't figure out how to
        # distinguish errors from this
        subprocess.call([stop_command], shell=True, stdout=PIPE, stderr=PIPE)

    def start(self):
        """ Starts the Tomcat server """
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

    def cp_app_descriptor_to_conf(self, descriptor_filepath, appname):
        """
        Copies app descriptor to Tomcat dir, by default it's located in `tomcat/conf/Catalina/localhost`
        :param str descriptor_filepath: location of the app deployment descriptor (with JNDI vars, names, etc).
        """
        if not os.path.exists(descriptor_filepath):
            self.logger.error('Could not find app descriptor file [{0}] to put to tomcat conf', descriptor_filepath)
            raise FileNotFoundException
        dst_conf_dir = os.path.join(self.tomcat_location, 'conf', 'Catalina', 'localhost')
        if not os.path.exists(dst_conf_dir):
            self.logger.info('Conf dir [{0}] did not exist, creating..', dst_conf_dir)
            os.makedirs(dst_conf_dir)
        dst_conf_location = os.path.join(dst_conf_dir, appname + '.xml')
        self.logger.info("Putting [{0}] into [{1}]", descriptor_filepath, dst_conf_location)
        shutil.copyfile(descriptor_filepath, dst_conf_location)

    def cp_configs_to_conf(self, src_filepaths):
        """
        Copies configuration files (usually for application and ehcache) to Tomcat directories
        :param list of [str] src_filepaths: location of the app deployment descriptor (with JNDI vars, names, etc).
                By default it's located in `tomcat/conf/Catalina/localhost`
        """
        for src_filepath in src_filepaths:
            if not os.path.exists(src_filepath):
                self.logger.error('Could not find app config file [{0}] to put to tomcat conf', src_filepath)
                raise FileNotFoundException
        dst_conf_dir = os.path.join(self.tomcat_location, 'conf')
        if not os.path.exists(dst_conf_dir):
            self.logger.info('Conf dir [{0}] did not exist, seems like an correct tomcat location was set. Quitting.',
                             dst_conf_dir)
            raise FileNotFoundException
        for src_filepath in src_filepaths:
            self.logger.info("Putting [{0}] into [{1}]", src_filepath, dst_conf_dir)
            shutil.copy(src_filepath, dst_conf_dir)


class TomcatNotFoundException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


class CouldNotStartTomcatException(Exception):
    pass
