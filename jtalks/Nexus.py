import urllib
import sgmllib

from jtalks.util.Logger import Logger


class Nexus:
    """
    A class to work with Nexus (upload, download, search). Note, that for all the operations we need a build number
    to be passed into the constructor. Other properties may or may not be required (some of them can be determined,
    like project name and version by pom.xml).
    """
    nexus_url = 'http://repo.jtalks.org/content/repositories/'
    repo = 'builds'
    common_group_id = 'org/jtalks'
    logger = Logger("Nexus")

    def __init__(self, build_number):
        self.build_number = build_number

    def download_war(self, project):
        self.logger.info('Looking up build #{0} for {1} project', self.build_number, project)
        war_url = self.get_war_url(project, self.build_number)
        self.logger.info('Downloading artifact: [{0}]', war_url)
        urllib.urlretrieve(war_url, project + ".war")

    def get_war_url(self, project, build_number):
        group_id = "deployment-pipeline/"
        artifact_version_url = NexusPageWithVersions().parse(self.base_url + group_id + project).version(build_number)
        # get version by URL (last part is something like /jcommune/12.3.123/)
        artifact_version = artifact_version_url.rpartition(project + "/")[2].replace("/", "")
        return (artifact_version_url + "{0}-{1}.war".format(project, artifact_version))


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
            # project-x.y.BUILD_NUMBER - old format, project-x.y.BUILD_NUMBER.git_hash - new format
            if ".{0}/".format(build_number) in link or \
                            ".{0}.".format(build_number) in link: return link
        raise Exception(
            "Couldn't find a build number {0}. Here are all the links: {1}".format(build_number, self.hyperlinks))
