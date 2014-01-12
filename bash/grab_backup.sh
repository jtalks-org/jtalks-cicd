#!/bin/sh

PASS=$1
FILE=$2
HOST=u55050.your-backup.de
USER=u55050
DATE=`date +"%d_%m_%Y"`
echo "Starting to sftp..."

lftp -u ${USER},${PASS} sftp://${HOST} <<EOF
cd ${DATE}
get ${FILE}
bye
EOF

echo "done"
