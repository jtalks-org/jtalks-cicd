import os
from unittest import TestCase

from jtalks.Nexus import Gav, Nexus


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

    def test_download(self):
        Nexus().download('thirdparty', Gav('kaptcha', 'com.google.code', '2.3.2'), 'tmpfile.jar')
        self.assertTrue(os.path.exists('tmpfile.jar'))
        self.assertEqual(431542, os.stat('tmpfile.jar').st_size)
        os.remove('tmpfile.jar')
