import os
import unittest
import shutil

from jtalks.Tomcat import Tomcat, TomcatNotFoundException


class TomcatTest(unittest.TestCase):
    def setUp(self):
        os.mkdir('test_tomcat')

    def tearDown(self):
        shutil.rmtree('test_tomcat')

    def test_move_war_to_webapps_should_actually_moves_it(self):
        # given
        tmpfile = file('test_tomcat/tomcat-test-project.tmp', 'w')
        os.mkdir('test_tomcat/webapps')
        # when
        dst_filename = Tomcat('test_tomcat').move_to_webapps(tmpfile.name, 'tomcat-test-project')
        # then
        self.assertEqual('test_tomcat/webapps/tomcat-test-project.war', dst_filename)
        self.assertTrue(os.path.exists(dst_filename))

    def test_move_war_deletes_prev_app_dir(self):
        # given
        tmpdir = os.path.join('test_tomcat', 'webapps', 'tomcat-test-project', 'tmpdir')
        os.makedirs(tmpdir)
        tmpfile = file('test_tomcat/tomcat-test-project', 'w')
        # when
        Tomcat('test_tomcat').move_to_webapps(tmpfile.name, 'tomcat-test-project')
        # then:
        self.assertFalse(os.path.exists(tmpdir), 'Tomcat did not remove previous app folder from webapps')

    def test_move_war_to_webapps_raises_if_tomcat_location_is_wrong(self):
        tomcat = Tomcat('./')
        self.assertRaises(TomcatNotFoundException, tomcat.move_to_webapps, 'src_filepath', 'appname')

    def test_start(self):
        os.makedirs('test_tomcat/bin')
        file('test_tomcat/bin/startup.sh', 'w').write('echo test > test_tomcat/test; sleep 5 &')
        Tomcat('test_tomcat').start()
        self.assertEqual('test\n', file('test_tomcat/test').readline())
