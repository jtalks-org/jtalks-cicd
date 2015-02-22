import os
from os import path
import unittest
from datetime import datetime
import shutil

from jtalks.backup.Backuper import Backuper


class BackuperTest(unittest.TestCase):
    def setUp(self):
        os.mkdir('backup')
        os.mkdir('to_backup')

    def tearDown(self):
        shutil.rmtree('backup')
        shutil.rmtree('to_backup')

    def test_backup_creates_folder_to_keep_backups(self):
        Backuper('./backup/', None)
        self.assertTrue(path.exists('backup/' + self.get_now_formatted_as_backup()))

    def test_backup_folder_actually_backs_up(self):
        os.mkdir('to_backup/test')
        backuper = Backuper('./backup/', None)
        Backuper('./backup/', None).back_up_dir('./to_backup')
        self.assertTrue(path.exists(path.join(backuper.backup_folder, 'to_backup/test')))

    def get_now_formatted_as_backup(self):
        return datetime.now().strftime("%Y_%m_%dT%H_%M_%S")
