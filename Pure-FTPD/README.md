<!-- start content -->
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote>Pure-FTPd is a free (BSD), secure, production-quality and standard-conformant FTP server.</blockquote>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ul>
	<li><dl><dd><a class="external text" href="http://www.pureftpd.org/project/pure-ftpd" rel="nofollow">pure-ftpd</a></dd></dl></li>
</ul>
<ul>
	<li><dl><dd><a class="external text" href="https://www.howtoforge.com/how-to-compile-pure-ftpd-on-centos-7" rel="nofollow">Install guide for CentOS 7</a></dd></dl></li>
</ul>
<h1><span id="Setup" class="mw-headline">Setup</span></h1>
We originally tried to just go with <a class="external text" href="http://prithak.blogspot.com/2013/07/installation-and-configuration-of.html" rel="nofollow">vsftpd</a> on CentOS 7 but I was unhappy that you could either run it secure with <a title="OpenSSL" href="https://twstewart84.wordpress.com/systems-administration/openssl/">SSL</a> but then limit the number of clients that were able to connect(linux ftp client and via web browser were all out) or run it unsecured without SSL.

Pure-FTPD has a way to enable TLS/SSL while also allowing standard less secure ftp transactions to happen. I feel this was the best compromise, we can sell security to the clients who might want or need that but also not hinder our existing customer base from using our services in the same way they have for many years.
<pre> Linux ftp001.example.com 3.10.0-229.4.2.el7.x86_64 #1 SMP Wed May 13 10:06:09 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
 CentOS Linux release 7.1.1503
 pure-ftpd-1.0.36-6.el7.x86_64
</pre>
All configuration is done with /etc/pure-ftpd/pure-ftpd.conf.
<pre>ChrootEveryone              yes
BrokenClientsCompatibility  no
MaxClientsNumber            50 #this can be increased if it becomes a problem
Daemonize                   yes
MaxClientsPerIP             8
VerboseLog                  no
DisplayDotFiles             no
AnonymousOnly               no
NoAnonymous                 yes
SyslogFacility              ftp
FortunesFile                /usr/share/fortune/banner
DontResolve                 yes
MaxIdleTime                 15
UnixAuthentication          yes
LimitRecursion              10000 8
AnonymousCanCreateDirs      no
MaxLoad                     10
PassivePortRange            9261 9268
ForcePassiveIP              216.169.181.156
AntiWarez                   yes
Bind                        10.0.20.40,21
UserBandwidth               512000
Umask                       133:022
MinUID                      1000
UseFtpUsers                 no
AllowUserFXP                no
AllowAnonymousFXP           no
ProhibitDotFilesWrite       yes
ProhibitDotFilesRead        yes
AutoRename                  no
AnonymousCantUpload         yes
AltLog                      clf:/var/log/pureftpd.log
NoChmod                     yes
CreateHomeDir               no
PIDFile                     /var/run/pure-ftpd.pid
MaxDiskUsage                95
NoRename                    yes
CustomerProof               yes
TLS                         1 # 1 : accept both traditional and encrypted sessions.
TLSCipherSuite              HIGH:+TLSv1:!SSLv2:!SSLv3
IPV4Only                    yes #currently have IPv6 disabled
</pre>
All other values, of which there are many should be commented out, or used with caution.
<h1><span id="SSL.2FTLS" class="mw-headline">SSL/TLS</span></h1>
All of the directions tell one to put the pure-ftpd.pem file in /etc/ssl/private, this is wrong for CentOS 7.
<ul>
	<li><dl><dd>Generate pem file from our star_zedxinc.com certificates</dd></dl></li>
</ul>
<pre> openssl pkcs12 -export -out pure-ftpd.pfx -inkey example.com.key -in example.com.crt
 openssl pkcs12 -in pure-ftpd.pfx -out pure-ftpd.pem -nodes
</pre>
<ul>
	<li><dl><dd>Place pem file at /etc/pki/pure-ftpd/</dd></dl></li>
</ul>
<pre> scp pure-ftpd.pem ftp001:/etc/pki/pure-ftpd/
 chmod 0600 /etc/pki/pure-ftpd/pure-ftpd.pem
</pre>
<ul>
	<li><dl><dd>Restart service</dd></dl></li>
</ul>
<pre> systemctl restart pure-ftpd
</pre>
<ul>
	<li><dl><dd>test SSL connection</dd></dl></li>
</ul>
<pre> In Windows use Filezilla and "require" an SSL certificate to connect
</pre>
<h1><span id="IPTables.2FSELinux" class="mw-headline">IPTables/SELinux</span></h1>
We made a special <a title="IPTables" href="http://bfesysapp001.zedxinc.com/wiki/index.php/IPTables"> IPTable</a> rule for this server so that it could not be used to ssh FROM.
<pre> iptables -A OUTPUT -p tcp --dport 22 -j DROP
</pre>
SELinux Booleans
<pre> setenforce 1
 setsebool -P allow_ftpd_full_access 1
 setsebool -P ftp_home_dir 1
</pre>
<h1><span id="Banner" class="mw-headline">Banner</span></h1>
/usr/share/fortune/banner
<pre> ##################################################
 #                                                #
 #     Welcome to Example.com's FTP Service       #
 #                                                #
 #     Have a good day.                           #
 #                                                #
 ##################################################
</pre>
<h1><span id="Creating_Accounts" class="mw-headline">Creating Accounts</span></h1>
The following steps are how to create a new FTP account.
<pre>  #] useradd -s /sbin/nologin -m -d /var/ftp/example example; -- the -p switch is supposed to set a password but the last time I tried that it did not encypt the  
    password just plain text in /etc/shadow.
  #] passwd example; -- sets a password for username 'example'
</pre>
&nbsp;

<hr />

</div>