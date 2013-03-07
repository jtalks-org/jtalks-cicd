#clone/update environments folder with scripts
#this cript should not be called from the environments folder itself, but rather from directory above
#because it will clone a repository into the environments directory
if [ -d "environments" ]; then
  cd environments
  git pull
  cd ..
else
  git clone git@jtalks.org:environments
fi
