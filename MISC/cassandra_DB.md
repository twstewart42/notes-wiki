# CassandraDB  
http://mesosphere.com/2014/02/12/cassandra-on-mesos-scalable-enterprise-storage/
http://www.datastax.com/documentation/cql/3.1/cql/cql_intro_c.html

## On master 

wget http://downloads.mesosphere.io/cassandra/cassandra-mesos-2.0.5-1.tgz
tar xvzf cassandra-mesos*tgz && cd cassandra-mesos*
Change the Mesos master URL and Zookeeper server list in conf/mesos.yaml to match your cluster: 
mesos.master.url: 'zk://localhost:2181/mesos' state.zk: 'localhost:2181'

Note: If you run a local cluster you can leave all defaults.

Change the number of hardware nodes you want Cassandra to be deployed:
cassandra.noOfHwNodes: 1


Note: If you want to try out the scaling feature don't deploy it to all your Mesos nodes initially.

Vim cassandra.yaml
cluster_name: 'TEST'
authenticator: PasswordAuthenticator
seeds: "10.0.0.X,10.0.0.Y" # "master" nosql nodes

 vim cassandra-topology.properties
10.0.5.66=DC1:RAC1
10.0.5.67=DC1:RAC1

default=DC1:RAC1

Start Cassandra on Mesos 
bin/cassandra-mesos

cqlsh -u cassandra -p cassandra slave001
 CREATE USER test WITH PASSWORD fafsdfafa;






create table TEST_DATA (usaf varchar , wban VARCHAR, date timestamp, tmpa float, tmpa_cnt int, dwpa float, dwpa_cnt int, psla float, psla_cnt int, prsa float, prsa_cnt int, visa_m float, visa_cnt int, wspa_m float, wspa_cnt int, wssx_m float, wgsx float, tmpx_m float, tmpx_flag int, tmpn_m float, tmpn_flag int, pcpt_m float, pcpt_flag varchar, swdt float, fog_flag int, rain_flag int, snow_flag int, hail_flag int, thunder_flag int, tornado_flag int, PRIMARY KEY (usaf, wban, date) );

INSERT INTO TEST_DATA (usaf, wban, date, tmpa, tmpa_cnt, dwpa, dwpa_cnt, psla, psla_cnt, prsa, prsa_cnt, visa_m, visa_cnt, wspa_m, wspa_cnt, wssx_m, wgsx, tmpx_m, tmpx_flag, tmpn_m, tmpn_flag, pcpt_m, pcpt_flag, swdt, fog_flag, rain_flag, snow_flag, hail_flag, thunder_flag, tornado_flag) VALUES('007026','99999','2014-07-13 00:00:00',13.4,7,6.7,7,NULL,0,0,0,0.5,7,2.5,7,7,NULL,14,1,12,1,0,'I',NULL,1,0,0,0,0,0);
