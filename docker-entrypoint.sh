#!/bin/sh
sudo service mysql start
cd ~/jtalks-cicd
python setup.py install

echo '=============================================='
echo '========Running Unit & Component Tests========'
echo '=============================================='
python setup.py test
component_tests_result=$?
echo '=============================================='
echo '=============Running System Tests============='
echo '=============================================='
pip install -e . --user
export PATH="$PATH:/home/jtalks/.local/bin"
rm -rf ~/.jtalks
cp -rv ~/jtalks-cicd/docs/configs_example ~/.jtalks

jtalks deploy -e envname -p jcommune -b 6
jc_system_test_result=$?

jtalks deploy -e envname -p poulpe -b 344
poulpe_system_test_result=$?

if [ "$component_tests_result" != 0 ]; then
  echo '===Component/unit tests failed!==='
  exit 1000
elif [ "$jc_system_test_result" != 0 ]; then
  echo '===JCommune Deployment failed in scope of System Testing==='
  exit 1000
elif [ "$poulpe_system_test_result" != 0 ]; then
  echo '===Poulpe Deployment failed in scope of System Testing==='
  exit 1000
fi
