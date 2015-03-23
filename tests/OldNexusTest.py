import os
from unittest import TestCase

from jtalks import OldNexus


class OldNexusTest(TestCase):
    NEXUS_BASE_URL = 'http://repo.jtalks.org/content/repositories/deployment-pipeline/deployment-pipeline'

    def test_get_war_url(self):
        nexus = OldNexus.Nexus(build_number=2600)
        self.assertEqual(nexus.get_war_url('jcommune', 2600), self.url('2.12.2600.e148537'))

    def test_download_war(self):
        nexus = OldNexus.Nexus(build_number=344)
        nexus.download_war('poulpe')
        self.assertTrue(os.path.exists('poulpe.war'))
        self.assertEqual(os.stat('poulpe.war').st_size, 29115524)
        os.remove('poulpe.war')

    def url(self, version):
        return self.NEXUS_BASE_URL + '/jcommune/' + version + '/jcommune-' + version + '.war'
