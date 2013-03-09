import unittest
from datetime import datetime

from mock import patch, MagicMock

from jtalks.backup.Backuper import Backuper
from jtalks.settings.ScriptSettings import ScriptSettings


class BackuperTest(unittest.TestCase):
  @patch('os.makedirs')
  def test_backup_creates_folder_to_keep_backups(self, makedirs_method):
    sut.backup()
    now = datetime.now().strftime("%Y_%m_%dT%H_%M_%S")
    folder_to_create = "/tmp/unit-test/project1/{0}".format(now) #Couldn't find a way to mock date
    makedirs_method.assert_called_with(folder_to_create)


db_operations = MagicMock()
sut = Backuper("/tmp", ScriptSettings(None, "project1", "unit-test"), db_operations)

if __name__ == '__main__':
  unittest.main()
