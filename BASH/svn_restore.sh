#!/bin/bash

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

echo "All finished restoring SVN"
