
<h1>One Liners and Snippets</h1>
<p>Run a task, but be alerted if it fails</p>
<pre>#!/bin/sh
yell() { echo "$0: $*" &gt;&amp;2; echo "$@ failed with exit code $?"| \
 mail -s "TEST FAIL" me@mail.com ;}
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }
try ping -c 1 10.0.0.1 #should pass
try ping -c 1 10.0.0.2578 #should fail and alert
try ping -c 1 www.google.com # should pass</pre>
<p>Say a developer has some script/loop that is spawning hundreds of pids or a tone of PostgreSQL connections from a bad query. This is how you can quickly kill those without Copy/Pasting a hundred or so PIDs and not hurting the parent process if it is PostgreSQL or PHP or something else.</p>
<pre>root]# ps fax
...
 7651 ? S 0:58 php script.php 538
 7656 ? S 0:57 php script.php 538
 7686 ? S 0:57 php script.php 538
 7690 ? S 0:57 php script.php 538
 7696 ? S 0:57 php script.php 538
 7700 ? S 0:57 php script.php 538
 7706 ? S 0:57 php script.php 538
 root]# /bin/ps fax | /bin/grep "script.php" | /bin/grep -v grep | \
        /bin/awk '{ print $1 }' | wc -l
127
 root]# /bin/kill -9 `<code>/bin/ps fax | /bin/grep "script.php" | /bin/grep -v grep | \
         /bin/awk '{ print $1 }'`
#Those are back ticks `</code></pre>
<p>&nbsp;</p>
<p>Find number of connections from IP addresses</p>
<pre>root]# netstat -tapn | awk '{print $5}' | sed 's/::ffff://' | sed 's/:.*//' | \
       sort | uniq -c | sort</pre>
<p>Similar, but different but let&#8217;s say you start up an Apache or httpd server and one gets an error that port 80 is already in use</p>
<pre style="margin:0;font-family:Calibri;font-size:11pt;">]# lsof -i :80
OR
]#  netstat -antu | grep 80</pre>
<p>Sometimes a directory can have so many files that rm -f does not work as it trying to find all the files to delete first instead of removing as it finds them, the find command can work when rm fails.</p>
<pre style="margin:0;font-family:Calibri;font-size:11pt;">root]# find . -type f -mmin +720 -print
root]# find . -type f -mmin +720 -delete  # find and delete anything over 12 hours old</pre>
<h2>RSYNC</h2>
<p>see the <a href="https://twstewart84.wordpress.com/systems-administration/python-snippets/">python version here</a>, which runs much better and lighter on resources</p>
<pre>#!/bin/bash
# rsync from random CentOS repos, in order to host a mirror of CentOS repos
# can be done the same with epel, just change mirror_list and output
# array of geologicaly close CentOS mirrors to pull from
mirror_list=(rsync://mirror.us.oneandone.net/centos/ rsync://mirror.cs.pitt.edu/centos/ rsync://mirrors-pa.sioru.com/CentOS/ rsync://mirror.itc.virginia.edu/centos/ rsync://mirror.clarkson.edu/centos rsync://mirror.vcu.edu/centos/ rsync://mirror.umd.edu/centos/ )

#Generate and select a RANDOM Mirror from the list
RANDOM=$$$(date +%s)
ranMirror=${mirror_list[$RANDOM % ${#mirror_list[@]} ] }

echo "selected $ranMirror"

#do rsync of Delta from Mirrors
if [ -d /var/www/repo/html/CentOS/ ] ; then
     rsync -avSHP --delete --exclude "local*" --exclude "isos" --exclude "i386" \
         --exclude "i686" $ranMirror /var/www/repo/html/CentOS/
else
     echo "Target directory /var/www/repo/html/CentOS/ not present."
fi
#This will take a very long time, for the inital rsync but after that it just
# rsyncs the day to day changes or weekly, however you schedule it</pre>
<h2> Disk Check</h2>
<p>Check the local disk on a vm or bare metal and if less than 95 % free alert someone.</p>
<pre>#!/bin/sh
*/15 * * * * timeout 10 /opt/disk_check.sh
df -H | grep 'sd' | grep -v '/boot' | awk '{ print $5 " " $6 }' | while read output;
do
   echo $output
   usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1 )
   partition=$(echo $output | awk '{ print $2 }' )

   if [ $usep -ge 95 ]; then
      echo "Running out of space \"$partition ($usep%)\" on $(hostname) as on $(date) `df -h`" |
      mail -s "Alert: Almost out of disk space $usep% $all" systems@example.com
   fi
   if [ $usep -ge 98 ]; then
      echo "Running out of space \"$partition ($usep%)\" on $(hostname) as on $(date)" |
      mail -s "Alert: Almost out of disk space $usep% $all" pagers@example.com
   fi
done</pre>
<h2>MediaWiki</h2>
<p>Backup A <a href="https://www.mediawiki.org/wiki/MediaWiki">MediaWIKI</a> database</p>
<pre>#!/bin/sh
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
fi</pre>
<h2>SVN</h2>
<p>I used these two scripts to move our svn server from a CentOS 5 host to a CentOS 7 host.</p>
<p>Backup <a href="https://subversion.apache.org/">SVN</a></p>
<pre>#!/bin/sh
# execute from /var/www/svn/
#This backs up the entire SVN repository using 'svnadmin dump'
num=`ls -l | wc -l` 
n=2

while [ $n -le $num ]
do
   echo "$n"
   d=`m=$n ;find -path './*' -prune -type d | awk '{ print $1}' |uniq | head -$num \
     | sed -n $m\p`
   echo "$d "
   name=`echo "$d" | sed -r 's/^.{2}//'`
   echo "$name"
   svnadmin dump $d &gt; /nfs/svnbkup/bkup/$d.svn_dump
   echo "svnadmin dump $d &gt; /nfs/svnbkup/bkup/$name.svn_dump" #I like to be verbose
   n=$((n+1))
done
echo "All done with SVN backup!"</pre>
<p>Restore <a href="https://subversion.apache.org/">SVN</a></p>
<pre>#!/bin/bash

num=`ls -l /nfs/svnbkup/bkup/ | wc -l`
n=1

while [ $n -le $num ]
do
   echo "$n"
   re=`m=$n; ls *.svn_dump | awk ' { print $1} ' | uniq | head -$num | sed -n $m\p`
   echo "$re"
   name=`echo "$re" | sed -e 's/.svn_dump.*$//' `
   echo "$name"
   svnadmin create /var/www/svn/$name
   svnadmin load /var/www/svn/$name &lt; /nfs/subversion/bkup/$re
   n=$((n+1))
done

echo "All finished restoring SVN"</pre>
<p>Create an SVN repository, we give a few senior level devlopers a very specific sudoers permissions that allows them to execute a script to create SVN repositories</p>
<pre>#!/bin/bash
#execute: sudo /var/www/svn/create $reponame
#script to create repo and add basic {trunk, branches, releases} directory trees
repo=$1
echo "creating $repo on http://svn.example.com/svn"
echo "svnadmin create /var/www/svn/$repo"
svnadmin create /var/www/svn/$repo
chown -R apache:apache /var/www/svn/$repo
echo "importing svn-template for $repo"
svnadmin dump /var/www/svn/svn-template &gt; /tmp/svn-template.dump
svnadmin load /var/www/svn/$repo &lt; /tmp/svn-template.dump
chown -R apache:apache /var/www/svn/$repo
echo "Done!"
echo "repo created at http://svn.example.com/svn/$repo/"</pre>
<p>Delete an SVN repository; we gave one senior level devloper a very specific sudoer permission that allows him to execute a script to remove SVN repositories</p>
<pre>#!/bin/bash
#execute: sudo /var/www/svn/delete $reponame
#Script for removing repositories in svn

repo=$1
read -p "You are about to delete /var/www/svn/$repo "
read -p 'Are you sure? yes/no: ' answer
    if [ "$answer" == "yes" ]
    then
        echo "Backing up $repo - just in case"
        svnadmin dump /var/www/svn/$repo &gt; /nfs/subversion/bkup/.deleted/dump_$repo
        echo "removing $repo from http://svn.example.com/svn/"
        rm -r /var/www/svn/$repo/
        echo "$repo has been removed"
    else
        echo "Nothing was deleted."
fi</pre>
