from Nexus import BuildNotFoundException
from jtalks.util.Logger import Logger


class DeployCommand:
    NEXUS_URL = 'http://repo.jtalks.org/content/repositories/deployment-pipeline/deployment-pipeline/'
    logger = Logger('DeployCommand')

    def __init__(self, jtalks_artifacts, old_nexus, tomcat, sanity_test, backuper, scriptsettings):
        """
        :param jtalks.ScriptSettings.ScriptSettings scriptsettings: config files to be deployed along with the app
        :param jtalks.Nexus.JtalksArtifacts jtalks_artifacts: downloads JTalks artifacts from Nexus
        :param jtalks.OldNexus.Nexus old_nexus: used to download artifacts if it's old and is kept in old repo
        :param jtalks.Tomcat.Tomcat tomcat: manages tomcat
        :param jtalks.sanity.SanityTest.SanityTest sanity_test: runs the tests after an app is deployed
        :param jtalks.backup.Backuper.Backuper backuper: backs up DB, tomcat
        """
        self.scriptsettings = scriptsettings
        self.tomcat = tomcat
        self.jtalks_artifacts = jtalks_artifacts
        self.sanity_test = sanity_test
        self.old_nexus = old_nexus
        self.backuper = backuper

    def deploy(self, project, build, app_final_name, plugins=[]):
        self.__validate_params_and_raise__(project, build)
        plugin_files = []
        try:
            gav, filename = self.jtalks_artifacts.download_war(project, build)
            plugin_files = self.jtalks_artifacts.download_plugins(project, gav.version, plugins)
        except BuildNotFoundException:
            filename = self.old_nexus.download_war(project)
        self.tomcat.stop()
        self.backuper.back_up_dir(self.tomcat.tomcat_location)
        self.backuper.back_up_db()
        self.tomcat.move_to_webapps(filename, app_final_name)
        self.jtalks_artifacts.deploy_plugins(self.scriptsettings.get_plugins_dir(), plugin_files)
        self.scriptsettings.deploy_configs()
        self.tomcat.start()
        self.sanity_test.check_app_started_correctly()

    def __validate_params_and_raise__(self, project, build):
        if build is None:
            self.logger.error('Build number was not specified, see [{0}] to get list of builds', self.NEXUS_URL)
            raise RuntimeError
        if project not in ['jcommune', 'poulpe', 'antarcticle']:
            self.logger.error('A correct project should be specified: [poulpe, jcommune, antarcticle]. Actual: [{0}]',
                              project)
            raise RuntimeError
