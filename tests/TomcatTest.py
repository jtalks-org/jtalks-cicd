import os
import unittest
import shutil

from jtalks.Tomcat import Tomcat, TomcatNotFoundException, FileNotFoundException


class TomcatTest(unittest.TestCase):
    def test_move_war_to_webapps_should_actually_moves_it(self):
        # given
        tmpfile = file('tomcat-test-project.tmp', 'w')
        os.mkdir('webapps')
        # when
        dst_filename = Tomcat('.').move_to_webapps(tmpfile.name, 'tomcat-test-project')
        # then
        self.assertEqual('./webapps/tomcat-test-project.war', dst_filename)
        self.assertTrue(os.path.exists(dst_filename))
        # cleanup
        shutil.rmtree('webapps')

    def test_move_war_deletes_prev_app_dir(self):
        # given
        tmpdir = os.path.join('webapps', 'tomcat-test-project', 'tmpdir')
        os.makedirs(tmpdir)
        tmpfile = file('tomcat-test-project', 'w')
        # when
        Tomcat('.').move_to_webapps(tmpfile.name, 'tomcat-test-project')
        # then:
        self.assertFalse(os.path.exists(tmpdir), 'Tomcat did not remove previous app folder from webapps')
        # cleanup
        shutil.rmtree('webapps')

    def test_move_war_to_webapps_raises_if_tomcat_location_is_wrong(self):
        tomcat = Tomcat('./')
        self.assertRaises(TomcatNotFoundException, tomcat.move_to_webapps, 'src_filepath', 'appname')

    def test_cp_app_descriptor_raises_if_src_config_does_not_exist(self):
        self.assertRaises(FileNotFoundException, Tomcat('').cp_app_descriptor_to_conf, 'does-not-exist.xml', 'appname')

    def test_cp_app_descriptor_must_result_in_new_file(self):
        tmpfile = file('tomcat-test.xml', 'w')
        Tomcat('').cp_app_descriptor_to_conf(tmpfile.name, 'appname')
        self.assertTrue(os.path.exists('conf/Catalina/localhost/appname.xml'))
        os.remove(tmpfile.name)
        shutil.rmtree('conf')

    def test_cp_configs_to_conf_should_raise_if_dst_conf_does_not_exist(self):
        tmpfiles = (file('tomcat-config.xml', 'w'), file('tomcat-config2.xml', 'w'))
        os.mkdir('conf')
        Tomcat('').cp_configs_to_conf((tmpfiles[0].name, tmpfiles[1].name))
        self.assertTrue(os.path.exists('conf/' + tmpfiles[0].name))
        self.assertTrue(os.path.exists('conf/' + tmpfiles[1].name))
        shutil.rmtree('conf')
        os.remove(tmpfiles[0].name)
        os.remove(tmpfiles[1].name)

