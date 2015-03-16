import os
import re
import urllib
import sgmllib
import shutil

from jtalks.util.Logger import Logger


class JtalksArtifacts:
    logger = Logger('JtalksArtifacts')

    def __init__(self, repo='builds'):
        self.repo = repo

    def download_war(self, project, build):
        gav = Gav(project + '-web-view', 'org.jtalks.' + project, version='', extension='')
        nexus = Nexus()
        version_page_url = gav.to_url(nexus.nexus_url, self.repo)
        version = NexusPageWithVersions().parse(version_page_url).version(build)
        gav.version = version
        gav.extension = 'war'
        nexus.download(self.repo, gav, project + '.war')
        return gav, project + '.war'

    def download_plugins(self, project, version, artifact_ids=()):
        """ -> [str] """
        files = []
        for plugin in artifact_ids:
            gav, filename = self.download_plugin(project, version, plugin)
            files.append(filename)
        return files

    def download_plugin(self, project, version, artifact_id):
        gav = Gav(artifact_id, 'org.jtalks.' + project, version)
        tofile_path = artifact_id + '.' + gav.extension
        Nexus().download(self.repo, gav, tofile_path)
        return gav, tofile_path

    def deploy_plugins(self, to_dir, plugin_files=[]):
        """
        Puts plugins to the config to the specified folder on the FS. Cleans previous plugins of there are any.
        :param str to_dir: directory to put the plugins to. Will be created if it's absent.
        :param [str] plugin_files: file names to put to the target dir
        """
        if to_dir:
            if not os.path.exists(to_dir):
                self.logger.info('Plugin dir did not exist, creating: [{0}]', to_dir)
                os.makedirs(to_dir)
            for filename in os.listdir(to_dir):  # rm previous plugins
                if filename.endswith('.jar'):
                    plugin_path = os.path.join(to_dir, filename)
                    self.logger.info('Removing previous plugins: [{0}]', plugin_path)
                    os.remove(plugin_path)
            for plugin in plugin_files:
                self.logger.info('Adding plugin [{0}] to [{1}]', plugin, to_dir)
                shutil.move(plugin, to_dir)
        elif len(plugin_files) != 0:
            self.logger.warn('Plugin dir was not specified in env configs while there are plugins specified '
                             'to be deployed: [{0}]. Skipping plugin deployment', ','.join(plugin_files))
            return


class Nexus:
    """
    A class to work with Nexus (upload, download, search). Note, that for all the operations we need a build number
    to be passed into the constructor. Other properties may or may not be required (some of them can be determined,
    like project name and version by pom.xml).
    """
    logger = Logger("Nexus")

    def __init__(self, nexus='http://repo.jtalks.org/content/repositories/'):
        self.nexus_url = nexus

    def download(self, repo, gav, tofile_path):
        """
        :param repo - str
        :param gav - Gav
        :param tofile_path str
        """
        url = self.nexus_url + repo + '/' + gav.to_repo_path()
        self.logger.info('Downloading artifact: [{0}]', url)
        urllib.urlretrieve(url, tofile_path)


class Gav:
    def __init__(self, artifact_id, group_id, version, classifier='', extension='jar'):
        self.artifact_id = artifact_id
        self.group_id = group_id
        self.version = version
        self.classifier = classifier
        self.extension = extension

    def to_str(self):
        return '{0}:{1}:{2}:{3}:{4}' \
            .format(self.group_id, self.artifact_id, self.version, self.classifier, self.extension)

    def to_repo_path(self):
        path_pattern = '{0}/{1}'
        if self.version:
            path_pattern += '/{2}/{1}-{2}'
        if self.version and self.classifier:
            path_pattern += '-{3}'
        if self.version and self.extension:
            path_pattern += '.{4}'
        return path_pattern \
            .format(self.group_id.replace('.', '/'), self.artifact_id, self.version, self.classifier, self.extension)

    def to_url(self, nexus_url, repo):
        if not nexus_url.endswith('/'):
            nexus_url += '/'
        return nexus_url + repo + '/' + self.to_repo_path()


class NexusPageWithVersions(sgmllib.SGMLParser):
    """ Can parse full versions of the artifacts by build number. """
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
            match = re.search('(http://.*/)([0-9]+\.[0-9]+\.[0-9]+\.\w+)(.*)', link)
            if match:
                version = match.group(2)
                if '.{0}.'.format(build_number) in version:
                    return version
        raise BuildNotFoundException(
            "Couldn't find a build number {0}. Here are all the links: {1}".format(build_number, self.hyperlinks))


class BuildNotFoundException(Exception):
    pass
