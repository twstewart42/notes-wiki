#!/bin/sh
#*/15 * * * * timeout 10 /opt/disk_check.sh
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
done
