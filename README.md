JTalks Continuous Integration & Continuous Delivery scripts

The best way to try it out is to use [JTalks VM](https://github.com/jtalks-org/jtalks-vm) project which allows to
start up a virtual environment with JTalks CICD on board automatically.

###Installation Guide
This project contains JTalks Environment configuration like DEV, UAT, PROD. To use it you'll need python to be installed (was checked on 2.6.6) and:
* `apt-get install python-dev libmysqlclient-dev`
* `apt-get install python-pip; pip install -U pip` - python package manager to install other python-related packages
* `pip install jtalks-cicd`

###User Guide:
* `jtalks --help` to get an idea of the parameters
* `jtalks deploy --build 601 --environment local --project jcommune` where:
 * 601 - is the build number, should be taken from (deployment pipeline repo)[http://repo.jtalks.org/content/repositories/deployment-pipeline/deployment-pipeline/] depending on what version of the build you want to deploy
 * local - env name which means connection details, Tomcat location, etc. For each environment you'll need a folder in `~/.jtalks/environments`. You can have several environments that are using e.g. different databases on single machine.
 * jcommune - is a project you want to deploy. It can be also - poulpe

###Project State
* Currently backup of tomcat & DB is ready, but recover is not implemented
* SSH information to log in to the env should be also kept in configuration
* Package can be installed only from sudo, but the idea is to install them into home directory
* Ability to interactively create environment to be added

-------------------------------
Each subdirectory in 'configs' directory is a set of configuration files for tomcat instance. For internal JTalks usage
we have several envs configured but they are kept in a separate git repo and pulled each time we're running scripts.
For local usage users should create a 'configs/local' (or any other name) directory and place project configuration
there.

###TBD:
* Sample env configuration should be created to give users a hint on how configs should be created and what should be
 there

