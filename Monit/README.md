<!-- start content -->
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote>Monit is a monitoring daemon process that will check every 60 seconds on configured services, pids, ports, host information, or pretty much anything you want and also take a course of action on failure/change detected.</blockquote>
<dl><dt>I decided that <a title="CFEngine" href="http://bfesysapp001.zedxinc.com/wiki/index.php/CFEngine"> CFEngine</a> while great at what it does, was too slow at restarting processes (especially as we move to a more HA environment) so I needed to find something that would catch failures and respond faster than 5 minutes. Monit appears to be the answer. Step 2 of this roll out is to have <a href="https://twstewart84.wordpress.com/systems-administration/cfengine/">CFEngine</a> monitor Monit so we can answer the "<a class="external text" href="http://en.wikipedia.org/wiki/Quis_custodiet_ipsos_custodes%3F" rel="nofollow">who watches the watchmen?</a>" concern.</dt></dl>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<dl><dd>
<ul>
	<li><a class="external text" href="http://mmonit.com/monit/documentation" rel="nofollow">Monit Documentation</a></li>
	<li><a class="external text" href="http://mmonit.com/" rel="nofollow">Official Website</a></li>
	<li><a class="external text" href="https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-monit" rel="nofollow">Quick Monit Install Guide</a></li>
	<li><a class="extiw" title="wikipedia:Monit" href="http://en.wikipedia.org/wiki/Monit">Wikipedia:Monit</a></li>
</ul>
</dd></dl>
<h1><span id="ZedX_Configuration" class="mw-headline">Configuration</span></h1>
Every machine monit is installed on you can go to <a class="external free" href="https://machinename.zedxinc.com:2812/" rel="nofollow">https://machinename.example.com:2812</a> to view status information for that individual machine. I have setup a very restricrtive LDAP group that only allows admin to access this page.

I have setup <a class="external text" href="https://bfesysmon001.zedxinc.com:8443/" rel="nofollow">M/Monit</a> which is the centralized version on monit.
Each machine is configured to send all communication over SSL to M/Monit(and from M/Monit back to machine).
<h1><span id="Install" class="mw-headline">Install</span></h1>
I like to do a yum install to setup the services correctly and then download/install the latest binary from their website as the latest version has a lot more options and flexibility than what is available in the regular CentOS repos. Monit-5.12.1 has been tested with and runs successfully on Centos 5, 6 and 7.

<b>Quick install</b>

I created a script to do most of the heavy lifting for me and grab it from our internal RPM site.
<pre>cd /opt;
wget http://rpm.example.com/kickstart/mapserver/monit-install
chmod 0700 monit-install
./monit-install
</pre>
<b>more explanation</b>
<pre>yum install monit ftp
cd /opt; wget http://mmonit.com/monit/dist/binary/5.12.1/monit-5.12.1-linux-x64.tar.gz; 
Or wget http://rpm.zedxinc.com/ZedX/monit-5.12.1-linux-x64.tar.gz (for private 10.0.25.X machines)
</pre>
I have a standard monitrc, pam authentication module, and certificate for ssl traffic that I download from a local ftp site.
<pre>echo "
#!/bin/bash
cd /opt
HOST=10.0.0.K
USER=kickstart
PASSWD=kickstart
ftp -i -n -v 10.0.0.K &lt;&lt; EOT 
binary
user kickstart kickstart
cd monit
mget monitrc
#mget pam-monit 
mget pam-monit-centos6
mget mmonit.pem
bye
EOT  "&gt;&gt; /opt/ftp.sh

chmod 755 /opt/ftp.sh
/opt/ftp.sh;
cp -rf /opt/monitrc /etc/ ;
chmod 0700 /etc/monitrc ;
cp -rf /opt/pam-moni* /etc/pam.d/monit;
mv /opt/mmonit.pem /etc/certmonger/;
chmod 0700 /etc/certmonger/mmonit.pem;

</pre>
<h2><span id="Configs" class="mw-headline">Configs</span></h2>
Most everything is set up properly in /etc/monitrc. If the machine is in our public network then we must manually change the m/monit collector IP address so that data is not going across separate networks. Monit is setup to have a 240 second start delay so that when a machine boots up there are not service start conflicts, this is very important.

after any changes to the config file or adding a new file in /etc/monit.d/, you must check syntax and then reload for the new config to be read.
<pre>monit.d]# monit -t
Control file syntax OK
monit.d]# monit reload
Reinitializing monit daemon
</pre>
<h2><span id="SSL" class="mw-headline">SSL</span></h2>
See the <a href="https://twstewart84.wordpress.com/systems-administration/openssl/">OpenSSL</a> page to understand how we configured the monit.pem to work with M/Monit with SSL
<h1><span id="Monitrc" class="mw-headline">Monitrc</span></h1>
I will paste below the important bits of the monitrc file, make sure these are set on each server
<pre>set daemon 60
with start delay 240
set mmonit https://monit:monit@10.0.1.[public IP]:8443/collector
#set mmonit https://monit:monit@10.0.0.[[Private IP]:8443/collector
# change mmonit collecter depending on network

set httpd port 2812 and
    ssl enable
    pemfile /etc/certmonger/mmonit.pem
    use address 10.0.0.[localhost]  # use primary interface host specific
    allow 10.0.1.[m/monit server]                
    allow @monitadmins
    allow @monitrc readonly

</pre>
Permissions on this file and the mmonit.pem must be 0700 or process will fail to start and also bad people could read our information.
<h1><span id="Monit.d" class="mw-headline">Monit.d</span></h1>
I place individual config files in /etc/monit.d/ for separate services and monitoring configs. Syntax does change between CentOS 6 and CentOS 7 (blame initd vs systemd).
Always run "monit -t" to check syntax is correct before "monit reload" and adding new configs into the mix. Once these launch if they are not properly configured you could end up with unintended consequences (killing production httpd, for example, not that that ever happened or anything).
<h2><span id="Network" class="mw-headline">Network</span></h2>
/etc/monit.d/network
<pre>check network eth0 with interface eth0
        if saturation &gt; 95% then alert
check network eth2 with interface eth2
        if saturation &gt; 95% then alert
#OR if CentOS 7
check network ens160 with interface ens160
        if saturation &gt; 95% then alert
check network ens192 with interface ens192
        if saturation &gt; 95% then alert
</pre>
<h2><span id="Filesystem" class="mw-headline">Filesystem</span></h2>
/etc/monit.d/filesystem
<pre>check filesystem rootfs with path /
if space usage &gt; 95% then alert
</pre>
<h2><span id="Sshd" class="mw-headline">Sshd</span></h2>
/etc/monit.d/sshd
<pre>check process sshd with pidfile /var/run/sshd.pid
start program  "/usr/bin/systemctl start sshd"
stop program  "/usr/bin/systemctl start sshd"
restart program  "/usr/bin/systemctl restart sshd"
if failed port 22 protocol ssh then restart

check process sshd with pidfile /var/run/sshd.pid
start program  "/sbin/service sshd start"
stop program  "/sbin/service sshd stop"
if failed port 22 protocol ssh then restart
</pre>
/etc/monit.d/sssd
<h2><span id="Sssd" class="mw-headline">Sssd</span></h2>
<pre>check process sssd with pidfile /var/run/sssd.pid
start program  "/sbin/service sssd start"
stop program  "/sbin/service sssd stop"
if changed pid then restart
</pre>
<h2><span id="Postgresql" class="mw-headline"><a href="https://twstewart84.wordpress.com/systems-administration/postgresql/">Postgresql</a></span></h2>
/etc/monit.d/postgresql
<pre>check process postgresql with pidfile /var/lib/pgsql/data/postmaster.pid
start program "/etc/init.d/postgresql start"
stop program "/etc/init.d/postgresql stop"
if changed pid then restart
</pre>
<h2><span id="Httpd" class="mw-headline">Httpd</span></h2>
/etc/monit.d/httpd
<pre>check process httpd with pidfile /var/run/httpd/httpd.pid
start program  "/sbin/service httpd start"
stop program  "/sbin/service https stop"
restart program  "/sbin/service httpd restart"
if failed host "IP" port 80 then restart

check process httpd with pidfile /var/run/httpd/httpd.pid
start program  "/usr/bin/systemctl start httpd"
stop program  "/usr/bin/systemctl stop httpd"
restart program  "/usr/bin/systemctl restart httpd"
if failed port 80 protocol ssh then restart
</pre>
<h2><span id="Mysqld" class="mw-headline">Mysqld</span></h2>
/etc/monit.d/mysqld
<pre>check process mysql with pidfile /var/run/mysqld/mysqld.pid
start program  "/sbin/service mysqld start"
stop program  "/sbin/service mysqld stop"
restart program "/sbin/service mysqld restart"
if failed unix /var/lib/mysql/mysql.sock then restart
</pre>
Remember in centos 7 mysql is now mariadb
<h2><span id="Mesos-master" class="mw-headline">Mesos-master</span></h2>
/etc/monit.d/mesos-master
<pre>check process mesos-master matching "/usr/sbin/mesos-master --work_dir=/var/run/mesos --ip=10.0.20.43 --hostname=bfeprdmes001 --zk=zk://10.0.20.43:2181/mesos --cluster=PROD --quorum=1 2 "
start program  "/usr/local/bin/start_mesos"  # I had to create custom start/stop scripts for mesos as monit would not launch it successfully via the standard command you see in the matching portion. 
stop program "/usr/local/bin/kill_mesos"
if failed host localhost port 5050 then restart
if changed pid then restart
alert monitalert@mail.example.com
</pre>
<h2><span id="Singularity" class="mw-headline">Singularity</span></h2>
/etc/monit.d/singularity
<pre>check process singularity matching "java -jar /opt/Singularity/SingularityService/target/SingularityService-0.4.1-shaded.jar server /opt/Singularity/singularity.yaml"
start program  "/usr/local/bin/start_singularity"
stop program "/usr/local/bin/kill_singularity"   
if failed host localhost port 8082 then restart
if changed pid then restart
alert monitalert@mail.zedxinc.com
</pre>
you can adapt these to match pretty much any situation/pid/process/or even exit status of individual tasks.
<h1><span id="M.2FMonit" class="mw-headline">M/Monit</span></h1>
M/Monit is the centralized management website for monit. It makes our job very easy and is a great asset to the systems department.
<h1><span id="Monit_ID" class="mw-headline">Monit ID</span></h1>
If the ID file is duplicated on multiple machines (this can happen if you clone the system including the Monit ID file) then several Monit instances will update the same host entry in M/Monit

1. Change the Monit ID. If you use Monit 5.8 or newer, use monit -r to reset the ID. For older Monit versions just remove the ID file. For example: rm -f ~/.monit.id (the location can have been changed with the "set idfile" statement in .monitrc),

Source <a class="external text" href="http://mmonit.com/wiki/MMonit/FAQ" rel="nofollow">Monit FAQ</a>

&nbsp;

<hr />

</div>