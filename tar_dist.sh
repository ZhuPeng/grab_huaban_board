pyinstaller -F --windowed -y backup.spec
cd dist

ls -al huaban_backup.tar.gz
rm -rf huaban_backup/backup.app
rm -rf huaban_backup/*
ls -al huaban_backup/*
rm -rf huaban_backup.tar.gz
cp -r backup.app huaban_backup

tar zcvf huaban_backup.tar.gz huaban_backup
ls -al huaban_backup.tar.gz
