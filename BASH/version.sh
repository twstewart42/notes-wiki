#!/bin/sh
#Simply sshes to every machine in a subnet and gatheres basic information on versions of software running on it.
#There are many ways to have made this much better, one of the very first bash scripts I ever made, humble beginnings


read -p 'Enter username : ' u_name
read -s -p 'Enter password : ' p_name

echo "	"

#checks all ip's on a subnet
for sub in 0 100
	do
	for ip in {1..254}
		do
		echo "----------------------------------------------------"
		echo "10.0.$sub.$ip"
		nslookup 10.0.$sub.$ip
		#ping -c 1 10.0.$sub.$ip # it would be smarter to only ssh to a machine on a successful ping, but I never bothered setting that up fully
		 
		set yourhost=$(nslookup 10.0.$sub.$ip | grep name | awk -F = '{print $NF}') ## get hostname and set it equal to value
		echo "hostname =" $yourhost
		
		sshpass -p $p_name ssh $u_name@10.0.$sub.$ip -o StrictHostKeyChecking=no -o ConnectTimeout=5 <<ENDSSH

		date
		uname -a
		cat /etc/redhat-release
		echo "Perl:"
		rpm -qa perl
		echo "Python:"
		rpm -qa python
		echo "php:"
                rpm -qa php
		echo "	"
		echo "The Following mysql databases run on" && uname -n
                rpm -qa mysql
		ls /var/lib/mysql/ | grep .sql
		echo "	"
		echo "The Following postgres databases run on" && uname -n
                rpm -qa postgresql
		ls /var/lib/pgsql/ | grep .sql
		echo "	"
		echo "Apache/httpd:"
		rpm -qa apache
		rpm -qa httpd
		echo "	"
		echo "The Following web pages run on" &&  uname -n
		/usr/sbin/httpd -S 2>&1
		echo "	"
		echo "	"
		echo "The Following local groups are on" && uname -n
		cat /etc/group
		echo "	"
		echo "The Following local users are on" && uname -n
		cat /etc/passwd
		echo "	"
		echo "Memory usage report"
		free
		echo "	"
		echo "disk usage report"
		df -h
		echo "	"
		exit

ENDSSH
		
		



#fi
done
done

