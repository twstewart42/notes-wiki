#!/bin/sh
#execute from /var/www/svn/
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
echo "All done with SVN backup!"

