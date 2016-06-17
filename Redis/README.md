<!-- start content -->
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote>"Redis is an open source (BSD licensed), in-memory data structure store, used as database, cache and message broker. It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs and geospatial indexes with radius queries. Redis has built-in replication, Lua scripting, LRU eviction, transactions and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster."</blockquote>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ul>
	<li><a class="external text" href="http://redis.io/" rel="nofollow">Redis.io</a></li>
	<li><a class="external text" href="http://redis.io/clients" rel="nofollow">Clients</a></li>
	<li><a class="external text" href="http://try.redis.io/" rel="nofollow">Tutorial</a></li>
	<li><a class="external text" href="https://www.javacodegeeks.com/2015/09/redis-clustering.html" rel="nofollow">Clustering</a></li>
</ul>
<h1><span id="Install" class="mw-headline">Install</span></h1>
I have installed redis on CentOS 7 and CentOS 6 without any issues, they specifically make it without any external dependencies so it is very lightweight.
<pre> cd /opt
 wget <a class="external free" href="http://download.redis.io/releases/redis-3.0.7.tar.gz" rel="nofollow">http://download.redis.io/releases/redis-3.0.7.tar.gz</a>
 tar -xzvf redis-3.0.7.tar.gz
 cd redis-3.0.7/
 make
 make test
 make install
</pre>
Best practices state that there should be a <b>Minimum 3 masters</b>, but recommend a slave for each master for a complete HA environement.
<h1><span id="Configuration" class="mw-headline">Configuration</span></h1>
I configured each node as a cluster node, this is somewhat of a new feature for Redis 3.0+, where before one could only setup master to slave replication, and then implement client side sharding to deal with fail-over and partitioning of data.
<pre> $ vim /opt/redis-3.0.7/redis.conf
 port 6379
 bind 10.0.0.[R1] 127.0.0.1
 cluster-enabled yes
 cluster-config-file nodes-6379.conf
 cluster-node-timeout 5000
 appendonly yes
</pre>
setup for clustering <a class="external free" href="http://redis.io/topics/cluster-tutorial" rel="nofollow">http://redis.io/topics/cluster-tutorial</a>

Start Server
<pre> $ redis-server /opt/redis-3.0.7/redix.conf 
 $ ps fax | grep redis -&gt; redis-server 10.0.0.[R1]:6379 [cluster]
</pre>
Should do this on every master, but only really needed on 1 machine to execute redis-trib.rb to properly setup clusters
<pre> $ yum install ruby
 $ gem install redis
 $ /opt/redis-3.0.7/src/redis-trib.rb create 10.0.0.[R1]:6379 10.0.0.[R2]:6379 
     10.0.0.[R3]:6379
</pre>
to create cluster nodes, no data can already be on the nodes and all nodes must up and be running
redis-trib.rb will not start if less than 3 masters, in production should also configure a number of slaves for failover
<h2><span id="Troubleshooting" class="mw-headline">Troubleshooting</span></h2>
If there is already data
<pre> redis-cli -c -h 10.0.0.[R1] -p 6379
 FLUSHALL
 CLUSTER RESET
 Quit
 rm /opt/redis-3.0.7/nodes-6379.conf
</pre>
<h2><span id="Testing" class="mw-headline">Testing</span></h2>
<pre> $ redis-cli -c -h 10.0.0.[R3] -p 6379
 set foo bar
 get foo
 "bar"
</pre>
<pre> $ redis-cli -c -h 10.0.0.[R2] -p 6379
 get foo
 "bar"
</pre>
<h1><span id="Admin_tasks" class="mw-headline">Admin tasks</span></h1>
Add additional master, the example below is with multiple masters running on the same host, but just by changing IP/port you can connect a new master to any existing master in the redis cluster
<pre> ./redis-trib.rb add-node 10.0.0.[R1]:6379 10.0.0.[R4]:6379
</pre>
Add slave node example
<pre> ./redis-trib.rb add-node --slave 10.0.0.[R2]:6379 [10.0.0.[Rs2]:6379
</pre>
Remove node
<pre> ./redis-trib del-node 127.0.0.1:6379 `&lt;node-id&gt;`
</pre>

<hr />

</div>