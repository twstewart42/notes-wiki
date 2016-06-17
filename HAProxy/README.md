<div id="content" role="main">

				
					
<article id="post-274" class="post-274 page type-page status-publish hentry">
	<header class="entry-header">
		<h1 class="entry-title">HAProxy</h1>
	</header><!-- .entry-header -->

	<div class="entry-content">
		<p><!-- start content --></p>
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote><p>The Reliable, High Performance TCP/HTTP Load Balancer</p></blockquote>
<dl>
<dt></dt>
</dl>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ul>
<li><a class="external text" href="http://www.haproxy.org/" rel="nofollow">HAProxy</a></li>
<li><a class="external text" href="https://www.digitalocean.com/community/tutorials/how-to-implement-ssl-termination-with-haproxy-on-ubuntu-14-04" rel="nofollow">HAProxy and SSL</a></li>
</ul>
<h1></h1>
<h1><span id="Install" class="mw-headline">Install</span></h1>
<p>For CentOS 7</p>
<pre> $ yum install haproxy
</pre>
<h1><span id="Configuration" class="mw-headline">Configuration</span></h1>
<h2><span id="SSL_Termination" class="mw-headline">SSL Termination</span></h2>
<p>below is the config that worked for me. /etc/haproxy/haproxy.cfg</p>
<pre>global
        daemon
        #debug
        maxconn 2048
        log         127.0.0.1 local2
        chroot      /var/lib/haproxy
        pidfile     /var/run/haproxy.pid
        user        haproxy
        group       haproxy
        tune.ssl.default-dh-param 2048
        log         127.0.0.1 local2
defaults
        mode http
        log                     global
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms
        option httplog

frontend http-in

        bind 10.0.0.X:80
        bind 10.0.0.X:443 ssl crt /etc/ssl/private/www.example.com.pem
        mode http
        reqadd X-Forwarded-Proto:\ http
        acl host_example2 hdr_beg(host) -i example1
        use_backend example1 if host_example2

        default_backend example1

backend example1
        option forwardfor
        balance roundrobin
        http-send-name-header Host
        option httpchk HEAD / HTTP/1.1\r\nHost:\ www.example.com # this was the trickiest part see link below
        server www-002.example.com www-002.example.com:80 check port 80
        server www-001.example.com www-001.example.com:80 check port 80

</pre>
<pre> <a class="external text" href="http://serverfault.com/questions/594669/haproxy-health-checking-multiple-servers-with-different-host-names" rel="nofollow">link</a>
</pre>
<h2><span id="TCP_passthrough" class="mw-headline">TCP passthrough</span></h2>
<p>This forward https connections to the web services without ssl termination and I prefer this method as it leaves https at the webserver and acts as more of a router than a proxy.</p>
<pre>global
        daemon
        #debug
        maxconn 2048
        log         127.0.0.1 local2
        chroot      /var/lib/haproxy
        pidfile     /var/run/haproxy.pid
        user        haproxy
        group       haproxy
        tune.ssl.default-dh-param 2048

defaults
        log                     global
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms
        option tcplog

frontend https-in

        bind :80
        bind :443
        mode tcp
        
        default_backend example3

backend example3
        balance roundrobin
        mode tcp
        option ssl-hello-chk
        server example105 10.0.0.X:443 check inter 2000 rise 2 fall 5
        server example005 10.0.0.X:443 check inter 2000 rise 2 fall 5
</pre>
<pre><span id="Example" class="mw-headline"></span>
 save file
 systemctl reload haproxy ##you do not have to restart the service if change is not in the global or default sections
 tail -f /var/log/messages ## all logs are sent to rsyslog service
</pre>
</div>