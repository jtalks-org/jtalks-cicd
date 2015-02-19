from Nexus import BuildNotFoundException
from jtalks.util.Logger import Logger


class DeployCommand:
    NEXUS_URL = 'http://repo.jtalks.org/content/repositories/deployment-pipeline/deployment-pipeline/'
    logger = Logger('DeployCommand')

    def __init__(self, jtalks_artifacts, old_nexus, tomcat, sanity_test):
        """
        Args:
            jtalks_artifacts (jtalks.Nexus.JtalksArtifacts):
            old_nexus (jtalks.OldNexus.Nexus):
            tomcat (jtalks.Tomcat.Tomcat):
            sanity_test (jtalks.sanity.SanityTest.SanityTest):
        """
        self.tomcat = tomcat
        self.jtalks_artifacts = jtalks_artifacts
        self.sanity_test = sanity_test
        self.old_nexus = old_nexus

    def deploy(self, project, build, plugins=()):
        self.__validate_params_and_raise__(project, build)
        try:
            self.old_nexus.download_war(project)
        except BuildNotFoundException:
            gav, filename = self.jtalks_artifacts.download_war(project, build)
            self.jtalks_artifacts.download_plugins(project, gav.version, plugins)
        self.tomcat.deploy_war()
        self.sanity_test.check_app_started_correctly()

    def __validate_params_and_raise__(self, project, build):
        if build is None:
            self.logger.error('Build number was not specified, see [{0}] to get list of builds', self.NEXUS_URL)
            raise RuntimeError
        if project not in ['jcommune', 'poulpe', 'antarcticle']:
            self.logger.error('A correct project should be specified: [poulpe, jcommune, antarcticle]. Actual: [{0}]',
                              project)
            raise RuntimeError
