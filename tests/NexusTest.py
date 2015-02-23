import os
from unittest import TestCase

from jtalks.Nexus import Gav, Nexus, JtalksArtifacts, NexusPageWithVersions


class NexusTest(TestCase):
    def test_gav_to_str(self):
        self.assertEqual('g:a:v::jar', Gav('a', 'g', 'v').to_str())
        self.assertEqual('g:a:v:c:jar', Gav('a', 'g', 'v', 'c').to_str())
        self.assertEqual('g:a:v:c:war', Gav('a', 'g', 'v', 'c', 'war').to_str())

    def test_gav_to_repo_path(self):
        self.assertEqual('g/a/v/a-v.jar', Gav('a', 'g', 'v').to_repo_path())
        self.assertEqual('g/a/v/a-v-c.jar', Gav('a', 'g', 'v', 'c').to_repo_path())
        self.assertEqual('g/a/v/a-v-c.war', Gav('a', 'g', 'v', 'c', 'war').to_repo_path())
        self.assertEqual('g/g/a/v/a-v-c.war', Gav('a', 'g.g', 'v', 'c', 'war').to_repo_path())
        self.assertEqual('g/g/a/v/a-v-c', Gav('a', 'g.g', 'v', 'c', '').to_repo_path())
        self.assertEqual('g/g/a/v/a-v', Gav('a', 'g.g', 'v', '', '').to_repo_path())
        self.assertEqual('g/g/a', Gav('a', 'g.g', '', '', '').to_repo_path())
        self.assertEqual('g/g/a', Gav('a', 'g.g', '', 'c', '').to_repo_path())
        self.assertEqual('g/g/a', Gav('a', 'g.g', '', '', 'war').to_repo_path())

    def test_gav_to_url(self):
        self.assertEqual('http://nexus/repo/g/a/v/a-v.jar', Gav('a', 'g', 'v').to_url('http://nexus', 'repo'))
        self.assertEqual('http://nexus/repo/g/a/v/a-v.jar', Gav('a', 'g', 'v').to_url('http://nexus/', 'repo'))

    def test_parse_version_from_url(self):
        versions_links = NexusPageWithVersions()
        versions_links.hyperlinks = ['http://n/a/b/c/3.0.5.0f5b2cf/', 'http://n/a/b/c/30.-0.6.0f5b2cf/',
                                     'http://n/a/b/c/30.0.7.0f5b2cf/', 'http://n/a/b/c/3.0.8/',
                                     'http://n/a/b/c/3.0.10.0f5b2cf/']
        self.assertEqual('3.0.5.0f5b2cf', versions_links.version(5))
        self.assertRaises(Exception, versions_links.version, 6)
        self.assertEqual('30.0.7.0f5b2cf', versions_links.version(7))
        self.assertRaises(Exception, versions_links.version, 8)
        self.assertEqual('3.0.10.0f5b2cf', versions_links.version(10))

    def test_download(self):
        Nexus().download('thirdparty', Gav('kaptcha', 'com.google.code', '2.3.2'), 'tmpfile.jar')
        self.assertTrue(os.path.exists('tmpfile.jar'))
        self.assertEqual(431542, os.stat('tmpfile.jar').st_size)
        os.remove('tmpfile.jar')

    def test_download_jcommune(self):
        gav, filename = JtalksArtifacts().download_war('jcommune', 2)
        self.assertTrue(os.path.exists(filename))
        self.assertEqual(38996276, os.stat(filename).st_size)
        os.remove(filename)

    def test_download_jc_plugin(self):
        gavs = JtalksArtifacts().download_plugins('jcommune', '3.0.6.8629f39', ['questions-n-answers-plugin'])
        self.assertTrue(os.path.exists(gavs.values()[0]))
        self.assertEqual(861914, os.stat(gavs.values()[0]).st_size)
        for filename in gavs.values():
            os.remove(filename)
