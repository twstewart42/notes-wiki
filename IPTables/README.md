<div id="content" role="main">

				
					
<article id="post-298" class="post-298 page type-page status-publish hentry">
	<header class="entry-header">
		<h1 class="entry-title">IPTables</h1>
	</header><!-- .entry-header -->

	<div class="entry-content">
		<p><!-- start content --></p>
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote><p>IPTables is used to set up, maintain, and inspect the tables of IP packet filter rules in the Linux kernel. Several different tables may be defined. Each table contains a number of built-in chains and may also contain user-defined chains.</p></blockquote>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ul>
<li><a class="external text" href="http://linux.die.net/man/8/iptables" rel="nofollow">Man Pages</a></li>
<li><a class="external text" href="http://www.cyberciti.biz/faq/fedora-redhat-centos-5-6-disable-firewall/" rel="nofollow">iptables service tutorial</a></li>
<li><a class="extiw" title="wikipedia:List of TCP and UDP port numbers" href="http://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers">Wikipedia:List_of_TCP_and_UDP_port_numbers</a></li>
</ul>
<h1><span id="Basic" class="mw-headline">Basic</span></h1>
<p>The easiest way to setup iptables is using the firewall-tui</p>
<pre> yum install system-config-firewall-tui; --installed by default in CentOS 5/6 but not CentOS 7
 setup; -&gt;firewall; allows specific ports for necessary communication
</pre>
<pre> iptables -nL --line-numbers; --will list out the order of rules and what they apply to
 Chain INPUT (policy ACCEPT)
 num  target     prot opt source               destination
 1    ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0           ctstate RELATED,ESTABLISHED
 2    ACCEPT     icmp --  0.0.0.0/0            0.0.0.0/0
 3    ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0           /* Allow all for loopback */
 4    ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0           state NEW tcp dpt:22 /* SSH Access */
 5    REJECT     udp  --  0.0.0.0/0            0.0.0.0/0           reject-with ic      mp-port-unreachable
 6    REJECT     tcp  --  0.0.0.0/0            0.0.0.0/0           reject-with ic      mp-port-unreachable
 #policy above only accepts ssh(port 22) and rejects all other communication.
</pre>
<pre> iptables -F; flushes out rules and leaves everything open
</pre>
<pre> service iptables save; saves iptables config to /etc/sysconfig/iptables
</pre>
<pre> iptables -I INPUT {LINE_NUMBER} -i eth1 -p tcp --dport 21 -s 123.123.123.123 -j ACCEPT -m comment --comment "This rule is here for this reason"; 
 # adds the rule at a specific line number, important as order does matter. Only allows tcp ftp(port 21) from source 123.123.123.123 on eth1.
</pre>
<pre> iptables -I INPUT 5 -i eth0 -p tcp --dport 5432 -j ACCEPT; ## This would add pgsql(port 5432) communication to the example above and knock the reject rules down to lines 6 and 7
</pre>
<h1><span id="Advanced" class="mw-headline">Advanced</span></h1>
<p>At my work I have a globally deployed a set of IPTables that allows all regular communication, while disallowing anything non-standard. this allows us to truthfully claim that we do have IPTables on on all of our servers, and keeps things secure, while not becoming a nuisance to developers or our customers. Then for more public facing servers we can tighten things as needed but we have a baseline of security instead of &#8220;Allow all.&#8221;</p>
<p>Distribution of IPTables was handled through <a href="https://twstewart84.wordpress.com/systems-administration/cfengine/">CFEngine</a></p>
<pre> #] cat /etc/sysconfig/iptables
 
 #iptables-save v1.4.7 on Tue May  5 09:36:53 2015
 *filter
 :INPUT ACCEPT [1:32]
 :FORWARD ACCEPT [0:0]
 :OUTPUT ACCEPT [251:38758]
 -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
 -A INPUT -p icmp -j ACCEPT
 -A INPUT -i lo -j ACCEPT -m comment --comment "Allow all for loopback"
 -A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT -m comment --comment "SSH Access"
 -A INPUT -p udp -m state --state NEW -m udp --dport 22 -j ACCEPT
 -A INPUT -p tcp -m multiport --dports 20,21,23,24,25 -m state --state NEW,ESTABLISHED -j ACCEPT -m comment --comment "Basic Services"
 -A INPUT -p udp -m multiport --dports 20,21,23,24,25 -m state --state NEW,ESTABLISHED -j ACCEPT
 -A INPUT -p tcp -m multiport --dports 80,443,111,2049,4045,5309,5432,3306,873,388,5308,514,8443,2812,445 -m state --state NEW,ESTABLISHED -j ACCEPT -m comment --comment "General Communication"
 -A INPUT -p udp -m multiport --dports 80,443,111,2049,4045,5309,5432,3306,873,388,5308,514 -m state --state NEW,ESTABLISHED -j ACCEPT 
 -A INPUT -p tcp -m multiport --dports 389,636,88,464,138,139,4456,749,7389,9443 -m state --state NEW,ESTABLISHED -j ACCEPT -m comment --comment "Authentication"
 -A INPUT -p udp -m multiport --dports 88,464,53,123,138,139,389,445 -m state --state NEW,ESTABLISHED -j ACCEPT
 -A INPUT -p tcp -m multiport --dports 11211,2181,5050,5051,8080,8081,8082 -m state --state NEW,ESTABLISHED -j ACCEPT -m comment --comment "Memcache and Mesos"
 -A INPUT -p tcp -m multiport --dports 901,902,903,993 -m state --state NEW,ESTABLISHED -j ACCEPT
 -A INPUT -p tcp -m multiport --dports 9261,9262,9263,9264,9265,9266,9267,9268 -m state --state NEW,ESTABLISHED -j ACCEPT
 -A INPUT -p udp -j REJECT --reject-with icmp-port-unreachable
 -A INPUT -p tcp -j REJECT --reject-with icmp-port-unreachable
 -A FORWARD -j REJECT --reject-with icmp-host-prohibited
 COMMIT
 # Completed on Tue May  5 09:36:53 2015
</pre>
</div>