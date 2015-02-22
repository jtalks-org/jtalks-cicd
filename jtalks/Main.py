import os
import sys
import traceback

from ApplicationContext import ApplicationContext
from jtalks import __version__
from jtalks.util.Logger import Logger
from util.LibVersion import LibVersion


class Main:
    def __init__(self):
        self.logger = Logger('Main')

    def main(self, args, options):
        command = args[0]
        if command == 'version':
            print __version__
            exit(0)
        app_context = ApplicationContext(options.env, options.project, options.build, options.grab_envs,
                                         os.path.expanduser("~/.jtalks"), options.sanity_test_timeout_sec,
                                         version=__version__)
        script_settings = app_context.script_settings
        if script_settings.grab_envs == "true":
            app_context.environment_config_grabber().grab_jtalks_configs()
        try:
            if command == 'deploy':
                LibVersion().log_lib_versions()
                app_context.deploy_command().deploy(options.project, options.build,
                                                    script_settings.get_app_final_name(), options.plugins)
            elif command == "upload-to-nexus":
                LibVersion().log_lib_versions()
                app_context.old_nexus().upload_war('pom.xml')
            elif command == "list-envs":
                app_context.env_list().list_envs()
            elif command == 'load-db-from-backup':
                LibVersion().log_lib_versions()
                app_context.load_db_from_backup().load()
            else:
                error = 'Command was not recognized, you can use: deploy, list-envs, load-db-from-backup. ' \
                        'Also see jtalks -h'
                self.logger.error(error)
                raise RuntimeError(error)
        except Exception:
            self.logger.error("Program finished with errors")
            if options.debug:
                print("Root cause: %s" % traceback.format_exc())
                sys.exit(1)
