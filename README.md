This project contains JTalks Environment configuration like DEV, UAT, PROD. To use it you'll need python to be installed (was checked on 2.6.6) and additionally might be required to install python-mysqldb module: 'sudo apt-get install python-mysqldb'.
Additional software you'll need to install:
 * `apt-get install python-pip` - python package manager to install other python-related packages
 * `pip install mock` - a mocking library for unit tests
 * `apt-get install GitPython`

-------------------------------
Project State
* Currently backup of tomcat & DB is ready, but recover is not implemented
* SSH information to log in to the env should be also kept in configuration

-------------------------------
Both scripts in root directory (upload_to_nexus.py and deploy_to_tomcat.py) has help. Invoke them with --help key to get help message.

`deploy_to_tomcat.py` is used to deploy application to tomcat instance. Typical usage is
python deploy_to_tomcat.py --project jcommune --environment local --build 583

Builds are war files taken from [Nexus](http://repo.jtalks
.org/content/repositories/deployment-pipeline/deployment-pipeline/)

Each subdirectory in 'configs' directory is a set of configuration files for tomcat instance. For internal JTalks usage
we have several envs configured but they are kept in a separate git repo and pulled each time we're running scripts.
For local usage users should create a 'configs/local' (or any other name) directory and place project configuration
there.

###TBD:
* Sample env configuration should be created to give users a hint on how configs should be created and what should be
 there

------------------------------
Another script is `prod_db_to_preprod.py` which is needed only for preprod environment where we need to have the same DB as the on on PROD. That script gets the DB from daily backups on FTP server, inserts all the data to the PREPROD database and changes some critical information like admin password, JCommune URL/name, etc.
