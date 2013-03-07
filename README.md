This project contains JTalks Environment configuration like DEV, UAT, PROD. To use it you'll need python to be installed (was checked on 2.6.6) and additionally might be required to install python-mysqldb module: 'sudo apt-get install python-mysqldb'.
Additional software you'll need to install:
 - `apt-get install python-pip` - python package manager to install other python-related packages
 - `pip install mock` - a mocking library for unit tests
-------------------------------
Project State
* Currently backup of tomcat & DB is ready, but recover is not implemented
* Sanity tests are to be implemented
* SSH information to log in to the env should be also kept in configuration
* Configuration should be kept separately from scripts


-------------------------------
Both scripts in root directory (upload_to_nexus.py and deploy_to_tomcat.py) has help. Invoke them with --help key to get help message.

deploy_to_tomcat.py is used to deploy application to tomcat instanse. Typical usage is
python deploy_to_tomcat.py preprod jcommune $PIPELINE_NUMBER

preprod - name of tomcat instanse where deploy to
jcommune - name of application to deploy
$PIPELINE_NUMBER - actually number of build (in pipeline)

-------------------------------
Each subdirectory in 'configs' directory is a set of configuration files for tomcat instance.
E.g. preprod directory contains ehcache settings for jcommune and poulpe, admin passwords, db URL etc.
They are used by deploy_to_tomcat.py script when application being deployed.

------------------------------
Another script is `prod_db_to_preprod.py` which is needed only for preprod environment where we need to have the same DB as the on on PROD. That script gets the DB from daily backups on FTP server, inserts all the data to the PREPROD database and changes some critical information like admin password, JCommune URL/name, etc.
