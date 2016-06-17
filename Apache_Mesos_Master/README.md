<p><!-- start content --></p>
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote><p>The mesos_master daemon is responsible for delivering tasks to each mesos-slave, resource pooling, and framework integration and communication.</p></blockquote>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<dl>
<dd>
<ul>
<li><a class="external text" href="http://timothysc.github.io/blog/2014/09/08/mesos-breeze/" rel="nofollow">CentOS 7 Install Guide</a></li>
<li><a class="external text" href="http://repos.mesosphere.io/el/7/noarch/RPMS/mesosphere-el-repo-7-1.noarch.rpm" rel="nofollow">Mesosphere CentOS 7 rpm</a></li>
<li><a class="external text" href="http://repos.mesosphere.io/el/6/noarch/RPMS/mesosphere-el-repo-6-2.noarch.rpm" rel="nofollow">Mesosphere CentOS 6 rpm</a></li>
<li><a class="external text" href="http://archive.cloudera.com/cdh4/one-click-install/redhat/6/x86_64/cloudera-cdh-4-0.x86_64.rpm" rel="nofollow">Cloudera Repo for Apache Zookeeper</a></li>
</ul>
</dd>
</dl>
<h1><span id="Prereq" class="mw-headline">Prereq</span></h1>
<p>You must first install Zookeeper on all masters before you have any chance of maintaining a fault resistant cluster.</p>
<dl>
<dd>
<ul>
<li><a class="external text" href="http://mesos.apache.org/documentation/latest/high-availability" rel="nofollow">Mesos High Availability</a></li>
<li><a class="external text" href="http://zookeeper.apache.org/doc/trunk/zookeeperAdmin.html#sc_zkMulitServerSetup" rel="nofollow">Zookeeper Multi-Master</a></li>
</ul>
</dd>
</dl>
<pre>yum install java-1.7.0-openjdk zookeeper rpm python-setuptools
echo 1 | sudo tee -a /var/lib/zookeeper/myid &gt;/dev/null #ensure each master has 
   a unique id
zookeeper-server-initialize myid=1 --force

vim /etc/zookeeper/conf/zoo.cfg #All master servers should have the exact same zoo.cfg
maxClientCnxns=50
tickTime=2000
initLimit=10
syncLimit=5
dataDir=/var/lib/zookeeper
clientPort=2181
server.1=10.0.0.[Z1]:2888:3888
server.2=10.0.0.[Z2]:2888:3888
server.3=10.0.0.[Z3]:2888:3888


vim /usr/local/bin/start_zookeeper

#!/bin/bash
##Start Zookeeper
/usr/bin/zookeeper-server start

#Also add the same to /usr/local/bin/start_services.sh
</pre>
<h1><span id="Install" class="mw-headline">Install</span></h1>
<pre>cd /opt
rpm -Uvh http://repos.mesosphere.io/el/7/noarch/RPMS/mesosphere-el-repo-7-1.noarch.rpm 
OR rpm -Uvh http://repos.mesosphere.io/el/6/noarch/RPMS/mesosphere-el-repo-6-2.noarch.rpm -- used these in the wxdappa environment
</pre>
<pre>#On Master
yum install docker jpackage-utils
yum install mesos chronos marathon
</pre>
<pre>#On Slave
yum install mesos
</pre>
<h1><span id="Running_Mesos_Master" class="mw-headline">Running Mesos Master</span></h1>
<ol>
<li>You must try and start all masters at the same time, so that they can elect a master through zookeeper.</li>
</ol>
<p>Click here for all <a class="external text" href="http://mesos.apache.org/documentation/latest/configuration/" rel="nofollow">configuration</a> options</p>
<p>vim /usr/local/bin/start_mesos # change ip and hostname to match local machine.</p>
<pre>#!/bin/sh

##Start Mesos
/usr/sbin/mesos-master --work_dir=/var/run/mesos --ip=10.0.0.[Z1] 
   --hostname=mesos01 --zk=zk://10.0.0.[Z1]:2181,10.0.0.[Z2]:2181,10.0.0.[Z3]:2181/mesos 
   --cluster=Modeling --quorum=2 &gt;/dev/null 2&amp;&gt;1 &amp;
</pre>
<p>vim /usr/local/bin/start_services.sh ##add the same line here so you can start all services at once on startup</p>
<pre>chmod 744 /usr/local/bin/start_services.sh
vim /etc/rc.local
+ /usr/local/bin/start_services.sh &amp;
</pre>
<h1><span id="Running_Mesos_Slave" class="mw-headline">Running Mesos Slave</span></h1>
<p>on wxdappa01-a04 I have installed mesos through the rpm</p>
<p>vim /usr/local/bin/start_services.sh</p>
<pre>#!/bin/sh

#Start Mesos-slave
/usr/sbin/mesos-slave --master=zk://10.0.0.[Z1]:2181,10.0.0.[Z2]:2181,10.0.0.[Z3]:2181/mesos 
&gt;/dev/null 2&gt;&amp;1 &amp;
</pre>
<p>add to the rc.local</p>
<pre>chmod 744 /usr/local/bin/start_services.sh
vim /etc/rc.local
+ /usr/local/bin/start_services.sh &amp;
</pre>
<h1><span id="Start_Services" class="mw-headline">Start Services</span></h1>
<p>For each piece of mesos that I install I created a /usr/local/bin/start_servicename and append it to /usr/local/bin/start_services.sh. I do this because of the nature that one must invoke these programs to run. If you run them direct from the cmd then they will be running under your shell session and not as a service under the root process tree. Should your session close so to would the service end. To avoid this problem I have created these start scripts that &#8220;bounce&#8221; the service out to run under the root process tree.</p>
<dl>
<dd>
<ul>
<li>/usr/local/bin/start_services.sh # start all the services installed on the machine under the mesos frameworks, is not used by cfengine, only at startup(/etc/rc.local).</li>
<li>/usr/local/bin/start_zookeeper #starts only the zookeeper service on the masters and is used by CFengine should the process stop to start it again automatically</li>
<li>/usr/local/bin/start_mesos #starts only the mesos master/slave service and is used by CFengine should the process stop to start it again automatically</li>
<li>/usr/local/bin/start_marathon #starts only the marathon service on the masters and is used by CFengine should the process stop to start it again automatically</li>
<li>/usr/local/bin/start_chronos #starts only the chronos service on the masters and is used by CFengine should the process stop to start it again automatically</li>
<li>/usr/local/bin/start_singularity #starts only the marathon service on the masters and is used by CFengine should the process stop to start it again automatically</li>
</ul>
</dd>
</dl>
<p>This is no longer necessary as know when I use the mesosphere packages they install systemd start scripts which allow much easier administration of the services.</p>
<h1><span id="CFEngine_and_Monit" class="mw-headline"><a title="CFEngine" href="https://twstewart84.wordpress.com/systems-administration/cfengine/">CFEngine</a> and <a title="Monit" href="https://twstewart84.wordpress.com/systems-administration/monit/">Monit</a></span></h1>
<p>For the Mesos Masters group CFEngine has a policy to ensure that the mesos-master, and zookeeper-server daemons are always running and if they are not running to start them.<br />
I decided that CFEngine while great at what it does, was too slow at restarting processes (especially as we move to a more HA environment) so I needed to find something that would catch failures and respond faster than 5 minutes. Monit appears to be the answer. Step 2 of this roll out is to have CFEngine monitor Monit so we can answer the &#8220;<a class="external text" href="http://en.wikipedia.org/wiki/Quis_custodiet_ipsos_custodes%3F" rel="nofollow">Who watches the watchmen</a>?&#8221; concern.</p>
<h1><span id="API" class="mw-headline">API</span></h1>
<p>&nbsp;</p>
<p>See My Page On the seperate <a href="https://twstewart84.wordpress.com/systems-administration/apache-mesos-apis/">Frameworks and API</a>s that I use as part of Apache MEsos</p>
<h1><span id="Zookeeper_Maintenance" class="mw-headline">Zookeeper <a class="external text" href="http://zookeeper.apache.org/doc/r3.4.3/zookeeperAdmin.html#sc_maintenance" rel="nofollow">Maintenance</a></span></h1>
<p>zookeeper takes many snapshots and logs as time goes on and this takes up a lot of space very quickly, I have set crontab to run once a day to keep that down to 3 logs and 3 snapshots. This should be done on every mesos-master machine.</p>
<pre> 01 01 * * *  /bin/java -Dlog4j.configuration=file:///etc/zookeeper/conf.dist/log4j.properties -cp /usr/lib/zookeeper/zookeeper.jar:/usr/lib/zookeeper/lib/slf4j-api-1.6.1.jar:/usr/lib/zookeeper/lib/slf4j-log4j12-1.6.1.jar:/usr/lib/zookeeper/lib/log4j-1.2.15.jar:conf org.apache.zookeeper.server.PurgeTxnLog /var/lib/zookeeper/ /var/lib/zookeeper/ -n 3
</pre>
<hr />
</div>