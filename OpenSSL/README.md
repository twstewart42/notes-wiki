<!-- start content -->
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote>OpenSSL is a cryptography toolkit implementing the Secure Sockets Layer ( SSL v2/v3) and Transport Layer Security ( TLS v1) network protocols and related cryptography standards required by them.</blockquote>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ol>
	<li><a class="external text" href="http://linux.die.net/man/1/openssl" rel="nofollow">Man Pages</a></li>
	<li><a class="external text" href="https://securityblog.redhat.com/2013/12/11/tlsv1-1-and-tlsv1-2-now-available-in-rhel/" rel="nofollow">TLSv1</a></li>
	<li><a class="external text" href="https://www.ssllabs.com/ssltest/" rel="nofollow">Qualys SSL Test</a></li>
	<li><a class="extiw" title="wikipedia:Transport Layer Security" href="http://en.wikipedia.org/wiki/Transport_Layer_Security">Wikipedia:Transport Layer Security</a></li>
</ol>
<h1><span id="Overview" class="mw-headline">Overview</span></h1>
Security and encryption is a huge requirement for any company, as of 1/1/2015 we are able to achieve an A- rating for HTTPS security using proper encryption and options in our vhost files.

I try to setup every new service with SSL/TLS enabled.
<h1><span id="https" class="mw-headline">https</span></h1>
We have configured all of our <a title="LAPP Stack" href="https://twstewart84.wordpress.com/systems-administration/lapp-stack/">web servers</a> to support <a title="Hypertext Transfer Protocol" href="http://bfesysapp001.zedxinc.com/wiki/index.php/Hypertext_Transfer_Protocol"> https://:443</a>
<h2><span id="CentOS_7.2FApache_2.4" class="mw-headline">CentOS 7/Apache 2.4</span></h2>
We are capped at an A rating right now.
<pre>#add the following to each vhost's 443 config
SSLProtocol All -SSLv2 -SSLv3   #disable SSLv2 and SSlv3 as those are no longer secure protocols
SSLHonorCipherOrder on
SSLCipherSuite HIGH:RC4-SHA:!MEDIUM:!ADH:!eNULL:!aNULL:!3DES:!DES:!LOW:!MD5  #use highest level cipher suite first
SSLCertificateFile /etc/httpd/excert/example.com.crt   #sha256 level certificates
SSLCertificateKeyFile /etc/httpd/excert/example.com.key
SSLCACertificateFile /etc/httpd/excert/example.com.ca-bundle
</pre>
<h2><span id="CentOS_6.2FApache_2.2" class="mw-headline">CentOS 6/Apache 2.2</span></h2>
We are capped at an A- rating for <a title="LAPP Stack" href="https://twstewart84.wordpress.com/systems-administration/lapp-stack/">web servers</a> on CentOS 6 using Apache 2.2
<pre>SSLProtocol All -SSLv2 -SSLv3
SSLHonorCipherOrder on
SSLCipherSuite HIGH:RC4-SHA:!MEDIUM:!ADH:!eNULL:!aNULL:!3DES:!DES:!LOW:!MD5
SSLCertificateFile /etc/httpd/excert/example.com.crt
SSLCertificateKeyFile /etc/httpd/excert/example.com.key
SSLCACertificateFile /etc/httpd/excert/example.com.ca-bundle
</pre>
<h2><span id="CentOS_5.2FApache_2.2" class="mw-headline">CentOS 5/Apache 2.2</span></h2>
We are capped at a B since it can't use tlsv1.1/tlsv1.2
<pre>SSLProtocol All -SSLv2 -SSLv3 +TLSv1
SSLHonorCipherOrder on
SSLCipherSuite ALL:HIGH:!ADH:!eNULL:!aNULL:!3DES:!DES:!LOW:!MD5
SSLCertificateFile /etc/httpd/excert/example.com.crt
SSLCertificateKeyFile /etc/httpd/excert/example.com.key
SSLCACertificateFile /etc/httpd/excert/example.com.ca-bundle
</pre>
<h1><span id="M.2FMonit" class="mw-headline">M/Monit</span></h1>
The following describes how we use our star.example.com certificate to create a mmonit.pem files which could be used to secure communication for our <a title="Monit" href="https://twstewart84.wordpress.com/systems-administration/monit/">monitoring services</a>.
<pre>#]openssl pkcs12 -export -out mmonit.pfx -inkey example.com.key -in example.com.crt -certfile zedxinc.com.ca-bundle
#]openssl pkcs12 -in mmonit.pfx -out mmonit.pem -nodes
</pre>
One could make a specific certificate for any service or communication within ZedX, Inc.
<pre>mmonit server#]vim /opt/mmonit/etc/servcer.conf
I had to create a whole new section in the server.conf file to support ssl connections from 10.0.20.0 machines
https://mmonit.example.com:8443
</pre>
Then on each machine I configured monitrc with the following
<pre>set mmonit https://monit:monit@mmonit.example.com:8443/collector
set httpd port 2812 and
   ssl enable
   pemfile /etc/certmonger/mmonit.pem
#] chmod 0700 /etc/certmonger/mmonit.pem
</pre>
<h1><span id="PostgreSQL" class="mw-headline">PostgreSQL</span></h1>
We have configured a few of our newest <a title="Postgresql" href="https://twstewart84.wordpress.com/systems-administration/postgresql/">PGSQL</a> servers to use SSL for communication.

copy over the example.com certs and key files to /var/lib/pgsql/9.3/data/excert. then cp example.crt to ../server.crt and so on, postgres is hardwired to look for those names of the certs and will fail if they do not match. then make these changes to /var/lib/pgsql/9.3/data/postgres.conf.
<pre> ssl = true                              # (change requires restart)
 ssl_ciphers = 'HIGH:RC4-SHA:!LOW:!EXP:!MD5:!ADH:!3DES:!DES:@STRENGTH'   # allowed SSL ciphers
 #ssl_renegotiation_limit = 512MB        # amount of data between renegotiations
 ssl_cert_file = 'server.crt'            # (cp zedxinc.crt to ../server.crt)
 ssl_key_file = 'server.key'             # (cp zedxinc.key to ../server.key)
 ssl_ca_file = 'root.crt'                # (cp zedxinc.ca_bundle to ../root.crt)
</pre>
edit the pg_hba.sql to allow for example web001
<pre> hostssl all             postgres                10.0.0.[web001]/32           trust
 OR for most secure
 hostssl projectdb             project_db_user               10.0.0.[web001]/32           md5
 hostssl projectdb       projectdc_db_user       10.0.0.[dba001]/32   md5
</pre>
restart the service and make sure it is running
<pre> 
]# psql agfleetio -h sql001 -U project_db_user -W
 Password for user project_db_user:
 psql (9.3.5)
 SSL connection (cipher: DHE-RSA-AES256-SHA, bits: 256)
 Type "help" for help.
 agfleetio=# \q
</pre>
&nbsp;
<h2></h2>
<h2>cURL, NSS and CentOS 7</h2>
In CentOS, curl is built with NSS security libraries by default, not OpenSSL. This was causing it not trust http's openssl certificates, for our own internal APIs. In short curl would not trust our root CA.

Similar php error: <a href="http://www.sebdangerfield.me.uk/2012/10/nss-error-8023-using-aws-sdk-for-php/">http://www.sebdangerfield.me.uk/2012/10/nss-error-8023-using-aws-sdk-for-php/</a>

Instead of basically rebuilding php, httpd, and curl all to get it on either NSS or OpenSSL, I created a very simple cheat. Only do this if you have <span style="color: #ff0000;"><strong>full</strong></span> trust in the certificates you are downloading.
<pre>&gt; echo | openssl s_client -showcerts -connect devapi.example:443 2&gt;&amp;1 | \ 
  sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | \ 
  awk '{if ( $0 ~ /-----BEGIN CERTIFICATE-----/) a++}{print &gt; "/tmp/excerts"a}'
&gt; ]# ls /tmp/excerts*
    /tmp/excerts /tmp/excerts1 /tmp/excerts2
    /tmp/excerts = example.com.crt
    /tmp/excerts1 = example.com.key
    /tmp/excerts2 = example.com.ca-bundle
&gt; curl -L https://devapi.example.com --cacert /tmp/excerts2</pre>
Do this if you have multiple domains with different certificates to allow anything using the curl library to communicate with a secure connection.

</div>