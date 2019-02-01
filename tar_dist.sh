pyinstaller -F --windowed -y backup.spec
cd dist

ls -al huaban_backup.tar.gz
rm -rf huaban_backup/backup.app
rm -rf huaban_backup/*
ls -al huaban_backup/*
rm -rf huaban_backup.tar.gz
cp ../bin/chrome ../bin/chromedriver backup.app/Contents/MacOS
ls backup.app/Contents/MacOS/
cp -r backup.app huaban_backup

type=""
if [ -n "$1" ]; then
    type=".${1}"
fi

tar zcvf "huaban_backup${type}.tar.gz" huaban_backup
ls -al "huaban_backup${type}.tar.gz"
