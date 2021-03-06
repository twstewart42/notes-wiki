<h1>MySQL Master/Master Replication and Proxy</h1>


<h2>Links</h2>

<a href=http://dev.mysql.com/doc/refman/5.6/en/mysql-proxy-configuration.html#option_mysql-proxy_proxy-backend-addresses>Mysql Proxy Documentation</a>

<h2>Installation</h2>
One can see this all in play on ldb001, which masquerades the address for sqla00 to connect to either sqla01 or sqla02

 Download and extract mysql-proxy-0.8.4-linux-el6-x86-64bit.tar.gz in /opt.

<h2>Proxy Config and Setup</h2>

 vim /etc/myproxy.cnf
 <pre>
 [mysql-proxy]
  admin-address = ldb001.example.com:3336
  proxy-address = 10.0.X.Y:3306
  proxy-backend-addresses = 10.0.X.A:3306, 10.0.X.B:3306
  #proxy-read-only-backend-addresses = 10.0.X.C:3306
  log-file=/var/log/mysql-proxy.log
  log-level=message
  plugins=proxy
  daemon=true
</pre>
  /opt/mysql-proxy-0.8.4/bin/mysql-proxy --defaults-file=/etc/myproxy.cnf

finally, add the line to /etc/rc.d/rc.local so that mysql-proxy starts on boot 
  /opt/mysql-proxy-0.8.4-linux-el6-x86-64bit/bin/mysql-proxy --defaults-file=/etc/myproxy.cnf &
  
At the time of me setting this up, I did not know about <a href=https://github.com/twstewart42/notes-wiki/tree/master/HAProxy>HAProxy</a>, and if I would do it over again I would probably use that to proxy TCP *:3306 to either backend addresses

<h2>sqla01</h2>
I will show you the master-master replication settings, both servers have to replicate bin-logs to each other acting as a slave for the other.

<h3>my.cnf</h3>
I recommend using something like <a href=http://mysqltuner.com/>mysql-tuner</a> to set cache sizes and other settings appropriately based on the resources available to the server and database.
<pre>
cat /etc/my.cnf
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
user=mysql
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
query_cache_limit = 2G
query_cache_size = 2G
tmp_table_size = 32M
max_heap_table_size = 32M
thread_cache_size = 8
table_cache = 64
max_connections=450
max_connect_errors=10000


#Replication
server-id                               = 10
log-bin                                 = mysql-bin
log-slave-updates                       = 0
replicate-same-server-id                = 0
max_binlog_size                         = 512M
relay-log                               = row
relay-log                               = mysqld-relay-bin
auto_increment_increment                = 10
auto_increment_offset                   = 1
expire_logs_days                        = 2
replicate-ignore-db                     = mysql
master-host                             = sqla02.example.com
master-user                             = sql1user
master-password                         = sql1pass
report-host                             = sqla01.example.com
relay-log-purge                         = 1
relay_log_space_limit                   = 4G
slave_exec_mode                         = idempotent
#default_storage_engine                 = InnoDB

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
</pre>

<h3>loopback:0</h3>
 #] cat /etc/sysconfig/network-scripts/ifcfg-lo:0
 <pre>
 DEVICE=lo:0
 IPADDR=10.0.X.Y
 NETMASK=255.255.255.255
 NETWORK=10.0.X.0
 BROADCAST=10.0.X.255
 ONBOOT=yes
 NAME=loopback
</pre>

<h3>arptables</h3>
 #] cat /etc/sysconfig/arptables
 <pre>
 # Generated by arptables-save v0.0.8 on Tue Feb  4 11:09:12 2014
 *filter
 :IN ACCEPT [19:532]
 :OUT ACCEPT [0:0]
 :FORWARD ACCEPT [0:0]
 [29:812] -A IN -d 10.0.X.Y -j DROP
 [0:0] -A OUT -d 10.0.X.Y -j mangle --mangle-ip-s 10.0.X.A
 [0:0] -A OUT -d 10.0.X.Y -j mangle --mangle-ip-s 10.0.X.B
 COMMIT
 # Completed on Tue Feb  4 11:09:12 2014
</pre>
<h2>bfewxdsqla02</h2>
The /etc/my.cnf file on sqla02

<h3>my.cnf</h3>
<pre>
#]cat /etc/my.cnf
[mysqld]
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
user=mysql
# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
#log = /tmp/mysql.log
query_cache_limit = 2G
query_cache_size = 2G
tmp_table_size = 32M
max_heap_table_size = 32M
thread_cache_size = 8
table_cache = 64
#max_threads = 100
max_connections=450
max_connect_errors=10000

#Replication
server-id                               = 20
log-bin                                 = mysql-bin
log_slave_updates                       = 0
replicate-same-server-id                = 0
max_binlog_size                         = 512M
binlog-format                           = row
relay-log                               = mysqld-relay-bin
auto_increment_increment                = 10
auto_increment_offset                   = 1
expire_logs_days                        = 2
replicate-ignore-db                     = mysql
master-host                             = sqla01.example.com
master-user                             = sql2user
master-password                         = sql2pass
report-host                             = sqla02.example.com
relay-log-purge                         = 1
relay_log_space_limit                   = 4G
default_storage_engine                  = InnoDB
slave_exec_mode                         = idempotent

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
</pre>

<h3>loopback:0</h3>
 #] cat /etc/sysconfig/network-scripts/ifcfg-lo:0
 <pre>
 DEVICE=lo:0
 IPADDR=10.0.X.Y
 NETMASK=255.255.255.255
 NETWORK=10.0.X.Y
 BROADCAST=10.0.X.Y
 NAME=loopback
 TYPE=Ethernet
 BOOTPROTO=none
 IPV6INIT=no
 USERCTL=no
</pre>
<h3>Arptables</h3>
 #] cat /etc/sysconfig/arptables
 <pre>
 # Generated by arptables-save v0.0.8 on Tue Feb  4 11:09:50 2014
 *filter
 :IN ACCEPT [646:18088]
 :OUT ACCEPT [4:112]
 :FORWARD ACCEPT [0:0]
 [14:392] -A IN -d 10.0.X.Y -j DROP
 [0:0] -A OUT -d 10.0.X.Y -j mangle --mangle-ip-s 10.0.X.A
 [0:0] -A OUT -d 10.0.X.Y -j mangle --mangle-ip-s 10.0.X.B
 COMMIT
 # Completed on Tue Feb  4 11:09:50 2014
</pre>
----

