import urllib
import sgmllib
import os
from jtalks.parser.PomFile import PomFile
from jtalks.util.Logger import Logger


class Nexus:
  """
  A class to work with Nexus (upload, download, search). Note, that for all the operations we need a build number
  to be passed into the constructor. Other properties may or may not be required (some of them can be determined,
  like project name and version by pom.xml).
  """
  base_url = "http://repo.jtalks.org/content/repositories/deployment-pipeline/"
  logger = Logger("Nexus")

  def __init__(self, build_number):
    self.build_number = build_number

  def upload_war(self, pom_file_location):
    """
      Uploads a war to the Nexus. The path to pom.xml is acceptaced as an argument, by this path
      we also determean where war file is placed.
    """
    pom = PomFile(pom_file_location)
    artifact_version = pom.version()
    artifact_id = pom.artifact_id()
    final_version = self.__final_version__(artifact_version)

    maven_deploy_command = ("mvn deploy:deploy-file -Durl={3} " +
                            "-DrepositoryId=deployment-pipeline -DgroupId=deployment-pipeline -DartifactId={0} -Dpackaging=war " +
                            "-Dfile={0}-view/{0}-web-view/target/{0}.war -Dversion={4}"
    ).format(artifact_id, artifact_version, self.build_number, self.base_url, final_version)
    print maven_deploy_command

    return_code = os.system(maven_deploy_command)
    if (return_code != 0):
      self.logger.error("Maven returned error code: " + str(return_code))
      raise Exception("Maven returned error code: " + str(return_code))

  def download_war(self, project):
    self.logger.info("Looking up build #{0} for {1} project", self.build_number, project)
    war_url = self.get_war_url(project, self.build_number)
    self.logger.info("Downloading artifact: [{0}]", war_url)
    urllib.urlretrieve(war_url, project + ".war")


  def get_war_url(self, project, build_number):
    group_id = "deployment-pipeline/"
    artifact_version_url = NexusPageWithVersions().parse(self.base_url + group_id + project).version(build_number)
    #get version by URL (last part is something like /jcommune/12.3.123/)
    artifact_version = artifact_version_url.rpartition(project + "/")[2].replace("/", "")
    return (artifact_version_url + "{0}-{1}.war".format(project, artifact_version))

  def __final_version__(self, artifact_version):
    """
     If build number is already in the version, then we should do nothing with it
    """
    if artifact_version.endswith("." + self.build_number):
      return artifact_version
    else:
      return artifact_version + "." + self.build_number


class NexusPageWithVersions(sgmllib.SGMLParser):
  hyperlinks = []

  def parse(self, url_with_versions):
    feed = urllib.urlopen(url_with_versions)
    page_content = feed.read()
    feed.close()

    self.feed(page_content)
    self.close()
    return self

  def start_a(self, attributes):
    for name, link in attributes:
      if name == "href":
        self.hyperlinks.append(link)

  def version(self, build_number):
    for link in self.hyperlinks:
      if link.endswith(".{0}".format(build_number + "/")): return link
    raise Exception(
      "Couldn't find a build number {0}. Here are all the links: {1}".format(build_number, self.hyperlinks))
