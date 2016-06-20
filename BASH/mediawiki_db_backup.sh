#!/bin/sh
# 0 1 2 * * /var/www/aggateway/bkup/wikidb_backup.sh
#This runs in a cron on the 2nd day of each month, at 1 A:M
now=$(date)
echo $now
lastmonth=$(date -d "$now - 1 month" +"%Y%m")
echo $lastmonth
sixmonths=$(date -d "$now - 6 month" +"%Y%m")

cp -p -f /var/tmp/wikidb.sql /nfs/keep_longtime/wikidb_$lastmonth.sql
mysqldump wikidb -u wikiuser -pfakepass &gt; /var/tmp/wikidb.sql
echo "wikidb has been backed up for $lastmonth"

#cleanup old out of date dumps
echo $sixmonths;
if [ -a wikidb_$sixmonths ];then
   rm -f /nfs/keep_longtime/wikidb_$sixmonths;
   echo "Removed wikidb_$sixmonths"
else
   echo "Nothing to Remove"
fi

