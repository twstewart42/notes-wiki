<!-- start content -->
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote>A LAPP Stack stands for <b>L</b>inux, <b>A</b>pache, <b>P</b>ostgreSQL, and <b>P</b>HP/Python/Perl. It is the basis for nearly every web service, and can come in varying sizes and configurations.</blockquote>
<blockquote>We do occasionally build LAMP Stacks which more people are familiar with. The only difference is using MySQL instead of PostgreSQL.</blockquote>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ul>
	<li><dl><dd><a class="external text" href="https://www.centos.org/" rel="nofollow"><b>L</b>inux - CentOS</a></dd></dl></li>
</ul>
<ul>
	<li><dl><dd><a class="external text" href="http://httpd.apache.org/" rel="nofollow"><b>A</b>pache HTTPD</a></dd></dl></li>
</ul>
<ul>
	<li><dl><dd><a class="external text" href="http://www.postgresql.org/" rel="nofollow"><b>P</b>ostgreSQL</a></dd></dl></li>
</ul>
<ul>
	<li><dl><dd><a class="external text" href="http://php.net/" rel="nofollow"><b>P</b>HP</a></dd></dl></li>
</ul>
<ul>
	<li><dl><dd><a class="external text" href="http://wiki.apache.org/httpd/PHP-FPM" rel="nofollow">PHP-FPM</a></dd></dl></li>
</ul>
<ul>
	<li><dl><dd><a class="external text" href="http://www.tldp.org/HOWTO/Apache-Compile-HOWTO/php.html" rel="nofollow">mod_php</a> - for historical reference</dd></dl></li>
</ul>
<h1><span id="All_In_One" class="mw-headline">All In One</span></h1>
The LAPP Stack can be configured all on one single machine.

Steps for Creating a LAPP Stack:
<ol>
	<li>Install CentOS 5.X/6.X/7.X Linux,  create a Virtual Machine</li>
	<li>CentOS 5/6 - yum install <a title="Hypertext Transfer Protocol" href="http://bfesysapp001.zedxinc.com/wiki/index.php/Hypertext_Transfer_Protocol">httpd</a> php mod_php mod_fcgid postgresql postgresql-server</li>
	<li>CentOS 7 - yum install <a title="Hypertext Transfer Protocol" href="http://bfesysapp001.zedxinc.com/wiki/index.php/Hypertext_Transfer_Protocol">httpd</a> php php-fpm mod_proxy_fcgid postgresql postgresql-server</li>
	<li>create <a class="external text" href="http://php.net/manual/en/function.phpinfo.php" rel="nofollow">sample/test</a> webpages in /var/www/html</li>
	<li>service httpd start; service postgresql start;</li>
	<li>test that services can communicate with one another</li>
</ol>
It really can be that simple, and should be done by anyone wanting to learn the basics, but at my work we run some very heavy websites, APIs, databases, and processing services which must all be able to handle large work loads at speed so that our customers are able to receive their data in a timely fashion. This has led to us breaking out the pieces of the LAPP stack into their own individual machines so that we can dedicate the maximum amount of resources for the tool, as each service has it's own specific set of dependencies and resource requirements when running in a production environment.
<h1><span id="Broken_Out" class="mw-headline">Broken Out</span></h1>
At my work I generally separate each part of the stack into it's own machine with dedicated resources. Traditionally this means we have 3 distinct machines; a web server, a database server, and an app server. That does not mean that a single web server only runs 1 website, just that web machines will only handle web traffic and not also have a database on it locally.
<h2><span id="CentOS_5.2F6" class="mw-headline">CentOS 5/6</span></h2>
CentOS 5 and 6 only have httpd 2.2 available which means you have to use the old and clunky but tried and true, mod_php to interact with php on the machines. The latest version of PostgreSQL can be built from source on CentOS 5 and 6, if you follow the same steps via the <a href="https://twstewart84.wordpress.com/systems-administration/kickstart/">kickstart</a> prd_sql example.

<span id="Webserver" class="mw-headline">Webserver</span>

<b>Apache HTTPD</b>
<pre>yum install httpd mod_php php php-devel php-mysql php-pgsql php-pdo php-gd php-cli php-soap php-xml glibc gcc gcc-c++
service start httpd
chkconfig httpd on
</pre>
Most of the time you will have to compile php_mapserver on the web server, which has it's own list of <a title="Kickstart" href="https://twstewart84.wordpress.com/systems-administration/kickstart/">dependencies</a>.

<b>Sample VHost</b>
We can run many websites on a single webserver with the use of VHosts that match FQDNs in DNS
<pre>vim /etc/httpd/conf.d/website_name.conf
&lt;VirtualHost *:80&gt;
        
        ServerName web001.example.com
        ServerAlias web001 

        ServerAdmin webmaster@example.com
        DocumentRoot /var/www/web001/html
        
        ScriptAlias /cgi-bin /var/www/web001/cgi-bin
        ErrorLog /var/www/web001/logs/httpd_error_log
        CustomLog /var/www/web001/logs/httpd_access_log common
        &lt;Directory /var/www/web001/html&gt;
                Options FollowSymLinks
                AllowOverride AuthConfig
                Order allow,deny
                Allow from all
        &lt;/Directory&gt;
        &lt;Directory /var/www/web001/cgi-bin&gt;
                Options FollowSymLinks
                AllowOverride AuthConfig
                Order allow,deny
                Allow from all
        &lt;/Directory&gt;
&lt;/VirtualHost&gt;

&lt;VirtualHost *:443&gt;
       
        ServerName web001.example.com
        ServerAlias  web001

        ServerAdmin webmaster@example.com
        DocumentRoot /var/www/web001/html
       
        ScriptAlias /cgi-bin /var/www/web001/cgi-bin
        ErrorLog /var/www/web001/logs/httpd_error_log
        CustomLog /var/www/web001/logs/httpd_access_log common
        &lt;Directory /var/www/web001/html&gt;
                Options FollowSymLinks
                AllowOverride AuthConfig
                Order allow,deny
                Allow from all
        &lt;/Directory&gt;
        &lt;Directory /var/www/web001/cgi-bin&gt;
                Options FollowSymLinks
                AllowOverride AuthConfig
                Order allow,deny
                Allow from all
        &lt;/Directory&gt;

SSLEngine on
SSLProtocol All -SSLv2 -SSLv3 +TLSv1
SSLHonorCipherOrder on
SSLCipherSuite ALL:HIGH:!ADH:!eNULL:!aNULL:!3DES:!DES:!LOW:!MD5
SSLCertificateFile /etc/httpd/example-cert-sha2/star_example.com.crt
SSLCertificateKeyFile /etc/httpd/example-cert-sha2/star_example.com.key
SSLCACertificateFile /etc/httpd/example-cert-sha2/example_CA_bundle.crt

&lt;/VirtualHost&gt;

</pre>
log files must be created manually as httpd cannot create the files on it's own and will fail to start if they are not already created.
<pre>mkdir -p /var/www/web001/logs/
touch /var/www/web001/logs/httpd_error_log
touch /var/www/web001/logs/httpd_access_log
httpd -t #check for syntax errors in config files
service httpd reload
</pre>
<h4><span id="httpd.conf" class="mw-headline">httpd.conf</span></h4>
The big thing to set for httpd 2.2.X in /etc/httpd/conf/httpd.conf is NameVirtualHost to enable Name-based Virtual hosting
<pre>NameVirtualHost *:80
NameVirtualHost *:443
</pre>
Also note that httpd2.2.1 (CentOS 5.X) does not support <a class="external text" href="https://wiki.apache.org/httpd/NameBasedSSLVHostsWithSNI" rel="nofollow">SNI</a>, which means only 1 domain certificate can be served via a single listening address. To get around that either manually compile a newer version or add a second NIC and dedicate a specific vhost to that IP (Change *:80 to 10.0.0.[2nd NIC]:80) Address and it will be able to support multiple domain names.
<h4><span id="SELinux" class="mw-headline">SELinux</span></h4>
If you decide to setup <a class="external text" href="http://docs.fedoraproject.org/en-US/Fedora/11/html/Security-Enhanced_Linux/sect-Security-Enhanced_Linux-SELinux_Contexts_Labeling_Files-Persistent_Changes_semanage_fcontext.html" rel="nofollow">SELinux</a> on the webserver be sure to do the following.

More info on <a class="external text" href="http://wiki.centos.org/TipsAndTricks/SelinuxBooleans" rel="nofollow">SELinux Booleans</a>
<pre>yum install policycoreutils-python
setsebool -P selinuxuser_mysql_connect_enabled on
setsebool -P selinuxuser_postgresql_connect_enabled on
setsebool -P httpd_can_network_connect_db on
setsebool -P httpd_can_network_connect on
setsebool -P httpd_use_nfs on

/usr/sbin/semanage fcontext -a -t httpd_log_t "/var/log/agscouter(/.*)?"
/sbin/restorecon -R -v /var/log/agscouter
</pre>
We generally have to turn SELinux off as we like to abuse /tmp with reading, writing and executing the same file(s) which is generally a no-no and is pretty common way to create a virus, but some of our apps work that way, so buyer beware.

<a class="extiw" title="wikipedia:SELinux" href="http://en.wikipedia.org/wiki/SELinux">Wikipedia:SELinux</a>
<h3><span id="Database_Server" class="mw-headline">Database Server</span></h3>
I have written a separate page on compiling and installing <a title="Postgresql" href="https://twstewart84.wordpress.com/systems-administration/postgresql/">PostgreSQL</a> with PostGIS support which is necessary for almost all of our projects. See also the <a class="external text" href="https://twstewart84.wordpress.com/systems-administration/kickstart/" rel="nofollow">Kickstart</a> wiki page for exact details.

The big thing to make sure is that once you have <a title="Postgresql" href="https://twstewart84.wordpress.com/systems-administration/postgresql/">PostgreSQL</a> installed, make sure the Webserver and the App Server have access to the database which is controlled via /var/lib/pgsql/9.3/data/pg_hba.conf.

Test from webserver, say the webserver is named web001 and the database server is named sql001.
<pre>web001#] psql -h sql001 -U db_user_name -W
Password for user db-user_name:
psql (9.3.5)
SSL connection (cipher: DHE-RSA-AES256-SHA, bits: 256)
Type "help" for help.

sql001=&gt;

</pre>
If you have setup the user and the hba file correctly, then you should be granted access.
<h3><span id="App_Server" class="mw-headline">App Server</span></h3>
More often than not this will need to be setup exactly like the webserver, and ideally should just be a clone of that machine.
<h2><span id="CentOS_7" class="mw-headline">CentOS 7</span></h2>
With the inclusion of httpd2.4, php5.4, and php-fpm there are small but significant changes that have to be made to get all the pieces working together, but we see a large uptick in speed when it is configured correctly. This portion of the wiki assumes that you already understand how to create and deploy a virtual machine.
<pre>yum install httpd php php-fpm mod_proxy_fcgi php-devel php-mysql php-pgsql php-pdo php-gd php-cli php-soap php-xml glibc gcc gcc-c++
systemctl start httpd
systemctl enable httpd
systemctl start php-fpm
systemctl enable php-fpm
</pre>
The next section concerns CentOS 7, HTTPD 2.4, mod_proxy_fcgi, PHP-FPM and the new way of configuring the services.
(Originally an email to Nate)

<b>Past:</b>

/var/log/web001/httpd_error_log

httpd and php would send all logs to one error log as mod_php was configured to run in each process of Apache. This was inefficient and also a slight security hazard.

<b>Now:</b>

The PHP-FPM module was created to handle the execution of php/cgi scripts based per request not per running thread.

vhost files:
in each separate vhost file we have to proxy all php scripts to the php-fpm service which will handle task execution.  note the port number 9000 I had every vhost sending php execution to this port.
<pre>&lt;VirtualHost *:80&gt;
        ServerName web001.example.com
        ServerAlias web001
   
        ErrorLog /var/log/web001/httpd_error_log
        CustomLog /var/log/web001/httpd_access_log "%h %l %u %{%F %T}t.%{msec_frac}t \"%r\" %&gt;s %b "

        DocumentRoot /var/www/web001/html
        &lt;Directory /var/www/web001/html&gt;
                Options FollowSymLinks ExecCGI
                AllowOverride AuthConfig
                require all granted
        &lt;/Directory&gt;

        ScriptAlias /cgi-bin /var/www/web001/cgi-bin
        &lt;Directory /var/www/web001/cgi-bin&gt;
                Options FollowSymLinks ExecCGI
                AllowOverride AuthConfig
                Require all granted
        &lt;/Directory&gt;


        ProxyPassMatch ^/(.*\.php(/.*)?)$ fcgi://127.0.0.1:9000/var/www/web001/html/$1 connectiontimeout=300 timeout=300

&lt;/VirtualHost&gt;
&lt;VirtualHost *:443&gt;
 
        ServerName web001.example.com
        ServerAlias web001

        ErrorLog /var/log/web001/httpd_error_log
        CustomLog /var/log/web001/httpd_access_log "%h %l %u %{%F %T}t.%{msec_frac}t \"%r\" %&gt;s %b "

        ServerAdmin webmaster@example.com

        DocumentRoot /var/www/web001/html
        &lt;Directory /var/www/web001/html&gt;
                SetHandler fcgid-script
                Options FollowSymLinks ExecCGI
                AllowOverride AuthConfig
                Require all granted
 
        &lt;/Directory&gt;

        ScriptAlias /cgi-bin /var/www/web001/cgi-bin
        &lt;Directory /var/www/web001/cgi-bin&gt;
                SetHandler fcgid-script
                Options FollowSymLinks ExecCGI
                AllowOverride AuthConfig
                Require all granted
        &lt;/Directory&gt;

       ProxyPassMatch ^/(.*\.php(/.*)?)$ fcgi://127.0.0.1:9000/var/www/web001/html/$1 connectiontimeout=300 timeout=300


SSLEngine on
SSLProtocol All -SSLv2 -SSLv3
SSLHonorCipherOrder on
SSLCipherSuite HIGH:RC4-SHA:!MEDIUM:!ADH:!eNULL:!aNULL:!3DES:!DES:!LOW:!MD5
SSLCertificateFile /etc/httpd/excert/star_example.com.crt
SSLCertificateKeyFile /etc/httpd/excert/star_example.com.key
SSLCACertificateFile /etc/httpd/excert/example_CA.com.ca-bundle


&lt;/VirtualHost&gt;


</pre>
This works without any additional edits, but what happened was PHP-FPM and fcgi would hold onto all the output and at the completion of the executed task would output all the stderr and stdout as one blob into the httpd_error_log. See the next seciton on PHP-FPM to see how I resolved this issue.

log files must be created manually as httpd cannot create the files on it's own and will fail to start if they are not already created.
<pre>mkdir -p /var/log/web001
touch /var/log/web001/httpd_error_log
touch /var/log/web001/httpd_access_log
httpd -t
service httpd reload
</pre>
After days of searching for answers, I found this guide which was the first one to clue me into the idea of connection pools for PHP-FPM <a class="external free" href="http://notes.benv.junerules.com/apache-2-4-and-php/" rel="nofollow">http://notes.benv.junerules.com/apache-2-4-and-php/</a> "Every pool you define in the PHP-FPM configuration should get a different port number that matches the port number you specify in your apache vhost configuration."
<h4><span id="PHP-FPM" class="mw-headline">PHP-FPM</span></h4>
<b>summary:</b> Each vhost should have its own and unique PHP-FPM connection pool. Leave 9000 as default and for each vhost you create on the machine increase the port number by 1 (I am experimenting with ondemand vs dynamic modes of PHP-FPM). I also decrease the minimum default www pool to 2 servers since that will not be used as much in the future.
<pre>vim /etc/php-fpm.d/www.conf
[web001pool]
#new connection pool for web001
listen=127.0.0.1:9001
listen.allowed_clients = 127.0.0.1
security.limit_extensions = .php
user=apache
group=apache
pm = ondemand
pm.max_children = 50
pm.start_servers = 1
pm.min_spare_servers = 1
pm.max_spare_servers = 3
pm.max_requests = 200
request_terminate_timeout = 300s
php_admin_flag[log_errors] = on
catch_workers_output = yes
php_value[session.save_handler] = files
php_value[session.save_path] = /var/lib/php/web001-session
php_admin_value[error_log] = /var/log/web001/php-fpm_error_log
</pre>
save and then in the vhost make sure that the ProxyPassMatch is sending to the correct connection pool.

make sure you also create the log files and save_path
<pre>touch /var/log/web001/php-fpm_error_log
chown apache /var/log/web001/php-fpm_error_log
mkdir /var/lib/php/web001-session
chown apache /var/lib/php/web001-session
systemctl restart php-fpm
</pre>
&nbsp;
<pre>vim /etc/httpd/conf.d/website.conf
#change port number for ProxyPassMatch
ProxyPassMatch ^/(.*\.php(/.*)?)$ fcgi://127.0.0.1:9001/var/www/web001/html/$1 connectiontimeout=300 timeout=300

systemctl reload httpd
tail -f /var/log/web001/php-fpm_error_log
</pre>
another blog which helped: <a class="external free" href="http://blog.andrewletson.com/installing-apache-2-4-php-5-4-centos-6-5/" rel="nofollow">http://blog.andrewletson.com/installing-apache-2-4-php-5-4-centos-6-5/</a>

There are a lot of "neat" things that we can do with PHP-FPM as it is now project based instead of a global catch-all. (such as sending session data to memcache, or executing PHP as different users depending on the project, etc).
<h4><span id="httpd.conf_2" class="mw-headline">httpd.conf</span></h4>
the following should be setup in /etc/httpd/conf/httpd.conf as global rules
<pre>ErrorLogFormat "[%{cu}t] [%l] %7F: %E: [client\ %a] %M% ,\ referer\ %{Referer}i"
#Format like old httpd2.2 logs or as close to it as possible
ErrorLog "logs/error_log"

&lt;IfModule log_config_module&gt;
    LogFormat "%h %l %u [%{cu}t] \"%r\" %&gt;s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
    LogFormat "%h %l %u [%{cu}t] \"%r\" %&gt;s %b \"%{Referer}i\" \"%{User-Agent}i\"" common
    &lt;IfModule logio_module&gt;
      # You need to enable mod_logio.c to use %I and %O
      LogFormat "%h %l %u [%{cu}t] \"%r\" %&gt;s %b \"%{Referer}i\" \"%{User-Agent}i\"" combinedio
    &lt;/IfModule&gt;
&lt;/IfModule&gt;

HostnameLookups off

&lt;IfModule mpm_worker_module&gt;
ServerLimit         20
StartServers         3
MaxClients          500
MaxRequestsPerChild 0
MinSpareThreads     75
MaxSpareThreads     250
ThreadsPerChild     25
Timeout             200
KeepAlive           On
&lt;/IfModule&gt;

&lt;IfModule mod_rewrite.c&gt;
  RewriteEngine on
  # Pass all requests not referring directly to files in the filesystem to index.php
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_URI} !=/favicon.ico
  RewriteRule ^ index.php [L]
  # Pass Authorization headers to an environment variable
  RewriteRule .* - [E=HTTP_Authorization:%{HTTP:Authorization}]
&lt;/IfModule&gt;

ProxyTimeout 300
Timeout 300

&lt;IfModule mod_proxy.c&gt;
        ProxyTimeout 300
        Timeout 300
&lt;/IfModule&gt;
&lt;IfModule mod_fcgid.c&gt;
        FcgidConnectTimeout 300
        FcgidMinProcessesPerClass 0
        FcgidMaxProcessesPerClass 700
        FcgidMaxRequestLen 268435456
        FcgidBusyTimeout 300
        FcgidIOTimeout 300
&lt;/IfModule&gt;

</pre>
<h4><span id="TMP_Area_not_working" class="mw-headline">TMP Area not working</span></h4>
In CentOS 7 by defualt PHP-FPM is set to create a "virtual" Temp area for each request. This is normally a good thing as it keeps the webserver more secure, but some developers like to do some funky things with dumping files in /tmp and then processing them, so we need to be able to have httpd/php-fpm read and write to the non-virtual /tmp.
<pre>locate php-fpm.service
vim /usr/lib/systemd/system/php-fpm.service
  - PrivateTmp=true
  + PrivateTmp=false
systemctl daemon-reload
systemctl restart php-fpm
</pre>
<h4><span id="SELinux_2" class="mw-headline">SELinux</span></h4>
If you decide to setup <a class="external text" href="http://docs.fedoraproject.org/en-US/Fedora/11/html/Security-Enhanced_Linux/sect-Security-Enhanced_Linux-SELinux_Contexts_Labeling_Files-Persistent_Changes_semanage_fcontext.html" rel="nofollow">SELinux</a> on the webserver be sure to do the following.

More info on <a class="external text" href="http://wiki.centos.org/TipsAndTricks/SelinuxBooleans" rel="nofollow">SELinux Booleans</a>
<pre>yum install policycoreutils-python
setsebool -P selinuxuser_mysql_connect_enabled on
setsebool -P selinuxuser_postgresql_connect_enabled on
setsebool -P httpd_can_network_connect_db on
setsebool -P httpd_can_network_connect on
setsebool -P httpd_use_nfs on

/usr/sbin/semanage fcontext -a -t httpd_log_t "/var/log/zxrequestapi(/.*)?"
/sbin/restorecon -R -v /var/log/zxrequestapi
</pre>
We generally have to turn SELinux off much for the same reason as the /tmp area not working, we like to abuse /tmp with reading, writing and executing the same file(s) which is generally a no-no and is pretty common way to create a virus, but some of our apps work that way, so buyer beware.

<a class="extiw" title="wikipedia:SELinux" href="http://en.wikipedia.org/wiki/SELinux">Wikipedia:SELinux</a>
<h3><span id="Database_Server_2" class="mw-headline">Database Server</span></h3>
I have written a separate wiki on compiling and installing <a title="Postgresql" href="https://twstewart84.wordpress.com/systems-administration/postgresql/">PostgreSQL</a> with PostGIS support which is necessary for almost all of our projects. See also the <a class="external text" href="https://twstewart84.wordpress.com/systems-administration/kickstart/" rel="nofollow">Kickstart</a> wiki page for exact details.

The big thing to make sure is that once you have <a title="Postgresql" href="https://twstewart84.wordpress.com/systems-administration/postgresql/">PostgreSQL</a> installed, make sure the Webserver and the App Server have access to the database which is controlled via /var/lib/pgsql/9.3/data/pg_hba.conf.

Test from webserver, say the webserver is named web001 and the database server is named sql001.
<pre>web001#] psql -h sql001 -U db_user_name -W
Password for user db-user_name:
psql (9.3.5)
SSL connection (cipher: DHE-RSA-AES256-SHA, bits: 256)
Type "help" for help.

sql001=&gt;

</pre>
If you have setup the user and the hba file correctly, then you should be granted access.
<h3><span id="App_Server_2" class="mw-headline">App Server</span></h3>
More often than not this will need to be setup exactly like the webserver, and ideally should just be a clone of the web machine.

&nbsp;

<hr />

</div>