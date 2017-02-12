JTalks Continuous Integration & Continuous Delivery scripts

----

Scripts to deploy JTalks projects like JCommune, Antarcticle, Poulpe.

The best way to try it out is to use [Docker](https://www.docker.com/) that installs java, mysql, tomcat. 
You'll need to install Docker, then run:
* `docker build -t jtalks/base docker/jtalksbase` to build a docker image with soft like java/mysql/tomcat 
* `docker build -t jtalks/cicd docs` to build a docker image with jtalks-cicd scripts on board
* `docker run -i -p 8080:8080 -t jtalks/cicd /bin/bash` to create a container and log in there. It also exposes 8080 port where apps are going to listen
* `sudo service mysql start` - start MySQL Server, you can log in there with user `root` and empty password
* `jtalks deploy --environment dev --project jcommune|poulpe|antarcticle --build [one of http://ci.jtalks.org/job/JC-UnitTests/]`

On Macs and Windows additionally you'd need to install [boot2docker|http://boot2docker.io/] and it might be required to 
forward ports: `ssh -L 127.0.0.1:8080:127.0.0.1:8080 -N docker@[ip you get when run boot2docker ip]`

### Installation Guide
This project contains JTalks Environment configuration like DEV, UAT, PROD. To use it you'll need python to be installed (was checked on 2.6.6) and:
* `apt-get install python-dev libmysqlclient-dev`
* `apt-get install python-pip; pip install -U pip` - python package manager to install other python-related packages
* `pip install https://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-2.0.3.zip` - this is a hack, 
  but it became impossible to specify the connector via distutils require_installs because it moved to an external 
  site and pip throws error because it doesn't trust to it. Note, that this freaking lib may be absent, so you may need 
  to figure out where to find the newer version.
* `pip install jtalks-cicd`

### User Guide:
* `jtalks --help` to get an idea of the parameters
* `jtalks deploy --build 2600 --environment local --project jcommune` where:
 * 2600 - is the build number, should be taken from [build job](http://ci.jtalks.org/job/JC-UnitTests/) depending on 
   what version of the build you want to deploy
 * local - env name which means connection details, Tomcat location, etc. For each environment you'll need a folder 
   in `~/.jtalks/environments`. You can have several environments that are using e.g. different databases on single machine.
 * jcommune - is a project you want to deploy. It can be also - poulpe

Examples of configuration files that are required for these scripts can be found in [Config Examples](docs/config_examples) dir along with docs.

### Project State
* Currently backup of tomcat & DB is ready, but recover is not implemented
* Backups are not cleaned automatically after critical mass is is gathered
* Package can be installed only from sudo, but the idea is to install them into home directory
* Ability to interactively create environment to be added

-------------------------------
Each subdirectory in 'configs' directory is a set of configuration files for tomcat instance. For internal JTalks usage
we have several envs configured but they are kept in a separate git repo and pulled each time we're running scripts.
For local usage users should create a 'configs/local' (or any other name) directory and place project configuration
there.
