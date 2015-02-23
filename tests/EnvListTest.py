import os
import unittest
import shutil

from jtalks.util.EnvList import EnvList


class EnvListTest(unittest.TestCase):
    tmp_dir = 'EnvListTestResources'
    global_config_dir = 'EnvListTestResources/environments'
    env_dir = os.path.join(global_config_dir, 'env')

    def setUp(self):
        os.makedirs(self.env_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_all_envs_are_listed(self):
        self.assertEqual(len(EnvList(self.global_config_dir).get_list_of_envs()), 1)
        self.assertEqual(['env'], EnvList(self.global_config_dir).get_list_of_envs())

    def test_list_projects_for_env(self):
        file(os.path.join(self.env_dir, 'project.cfg'), 'w')
        projects = EnvList(self.global_config_dir).list_projects('env')
        self.assertEqual(['project'], projects)
