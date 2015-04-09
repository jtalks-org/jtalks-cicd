from jtalks.DeployCommand import DeployCommand
from jtalks.OldNexus import Nexus as OldNexus
import jtalks.Nexus as NewNexus
from jtalks.DB import DB
from jtalks.Tomcat import Tomcat
from jtalks.backup.Backuper import Backuper
from jtalks.db.DbOperations import DbOperations
from jtalks.sanity.SanityTest import SanityTest
from jtalks.util.EnvList import EnvList
from jtalks.util.EnvironmentConfigGrabber import EnvironmentConfigGrabber


class ApplicationContext:
    """
      Carries similar ideas to Spring's AppContext - it builds all the objects. This IoC is manual though, the objects
      are all constructed manually in Python code.
    """

    def __init__(self, script_settings):
        """ :param jtalks.ScriptSettings.ScriptSettings script_settings: settings """
        self.script_settings = script_settings
        self.script_settings.create_work_dir_if_absent()
        self.script_settings.log_settings()

    def old_nexus(self):
        return OldNexus(build_number=self.script_settings.build)

    def jtalks_artifacts(self):
        return NewNexus.JtalksArtifacts()

    def tomcat(self):
        return Tomcat(self.script_settings.get_tomcat_location())

    def backuper(self):
        return Backuper(self.script_settings.backups_dir, self.db_operations())

    def db_operations(self):
        return DbOperations(self.script_settings.get_db_settings())

    def db_settings(self):
        return self.script_settings.get_db_settings()

    def deploy_command(self):
        return DeployCommand(
            self.jtalks_artifacts(), self.old_nexus(), self.tomcat(), self.sanity_test(),
            self.backuper(), self.script_settings)

    def environment_config_grabber(self):
        return EnvironmentConfigGrabber(self.script_settings.global_configs_dir, self.script_settings.temp_dir)

    def sanity_test(self):
        http_port = self.script_settings.get_tomcat_port()
        return SanityTest(tomcat_port=http_port, app_name=self.script_settings.get_app_final_name(),
                          sanity_test_timeout_sec=self.script_settings.sanity_test_timeout_sec)

    def db(self):
        return DB(self.script_settings.get_db_settings(), self.script_settings)

    def script_settings(self):
        return self.script_settings

    def env_list(self):
        return EnvList(self.script_settings.global_configs_dir)
