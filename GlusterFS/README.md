<h1> GlusterFS </h1>

My experience attempting to use commodity hardware across mixed disc types (HDD &amp; SSD) to attempt creating a very fast and also very deep storage solution. I was able to get everything setup correctly, I just wish I had a faster network(10 GiB) for data replication and spanning. In Practice I have ran into issues where if many machines are attempting to write to the same volume things slow down really badly, this could be the very old hardware I setup this demo on, or an issue with <a href="https://gluster.readthedocs.io/en/latest/Quick-Start-Guide/Quickstart/">GlusterFS</a> but I do not have the resources to further test this setup. I&#8217;ll show what I setup and some of the issues that occurred on my journey in understanding <a href="http://www.gluster.org/community/documentation/index.php/HowTo">GlusterFS</a>. Understand that there are many, many (like 10) different ways to setup GlusterFS with different replication, striping, spanning, arbiters, etc settings, and I may have built it in a way that made sense for this project but not necessary what might be the way for everyone out there.

<h1><span id="Distributed-Replicate" class="mw-headline">Distributed-Replicate</span></h1>
<p>Originally I had the idea of creating 2 machines with HDD and 2 machines with SSD, but it turns out that it is wise to have arbiters for each sub grouping of disks so that one can avoid split brain issues should one of the nodes in the group go down. An <a href="https://gluster.readthedocs.io/en/latest/Administrator%20Guide/arbiter-volumes-and-quorum/">Arbiter</a> only stores meta data and file structure not the actual data so they can be sized much smaller. As in <strong>ANY CLUSTER</strong> there must be an <strong>odd</strong> number of nodes to correctly handle failures.</p>
<pre>-glusterFS cluster physical layout
gluster1.example.com - 960GB SSD
gluster2.example.com - 4 TB HDD
arbiter1.example.com - 50 GB HDD VM
gluster3.example.com - 960GB SSD
gluster4.example.com - 4 TB HDD
arbiter2.example.com - 50 GB HDD VM</pre>
<p>The above physical layout is how I thought the replication and striping would go, basically gluster1 and gluster2 would be an extended pool and would replicate data to gluster3 and gluster4(being there own separate pool, with the arbiters for each group make sure nothing went haywire. I ended up being a little mistaken with how the replication worked and you will see later when I set up the volume the cluster is structured a little bit differently than my initial understanding.</p>
<h3>1 Machine</h3>
<p>Here is the setup of 1 machine in the cluster, all machines had the same number of NICs, OS, etc, the only different was physical disk speed and size.</p>
<pre>Hostname: gluster1.example.com
eth0: 10.0.0.[eth0] - gluster1-mgmt.example.com
eth1: 10.0.40.[eth1] - gluster1-data.example.com
/boot 512MB
SWAP 4GB
/ 20GB XFS Volume
/data/brick# - the rest - XFS Volume, change brick number to match number of machine
#the glusterfs volume must be a separate volume than /</pre>
<h2>Install</h2>
<p>I installed everything on CentOS 7, but I have also setup GlusterFS on CentOS 6 which I will show later on in the page.</p>
<pre>#I would recommend checking with gluster.org for newer versions
wget -P /etc/yum.repos.d/ http://download.gluster.org/pub/gluster/glusterfs/3.7/3.7.5/CentOS/glusterfs-epel.repo
yum install glusterfs-server
systemctl start glusterd
systemctl enable glusterd
#repeat on each machine in cluster</pre>
<h3>Network</h3>
<p>The mgmt network is setup for clients to mount and access the data.</p>
<pre>eth0: 10.0.0.[eth0] - gluster1-mgmt.example.com</pre>
<p>The data network is for replication and spanning of data.</p>
<pre>eth1: 10.0.60.[eth1] - gluster1-data.example.com</pre>
<p>It is highly recommend that these functions be separated to distinct networks as GlusterFS has no way of prioritizing a mix of traffic, so if you put all of this on one network one may have issues with replication not keeping up and things will be missing, etc.</p>
<h2>Create</h2>
<p>The Correct volume create command:</p>
<p>I made fake CNAMEs for each host in /etc/hosts so as to not rely on DNS for host discovery. This configuration <b>MUST</b> be the same on each host.</p>
<pre>10.0.60.[g1]1 gluster1ssd-data
10.0.60.[g2]2 gluster2hdd-data
10.0.60.[a1]3 arbiter1-data
10.0.60.[g3]4 gluster3ssd-data
10.0.60.[g4]5 gluster4hdd-data
10.0.60.[a2]6 arbiter2-data

</pre>
<pre>]# gluster peer status
]# gluster peer probe 10.0.60.[gluster2]
#repeat for all nodes in cluster, cannot probe yourself
]# gluster peer status
Number of Peers: 5

Hostname: arbiter1-data
Uuid: 9a36b50b-4c21-443b-b978-8c28b8d0df59
State: Peer in Cluster (Connected)
Other names:
10.0.60.[arbiter1-data]

Hostname: gluster2hdd-data
Uuid: c690a0a6-e752-4f80-833a-a9e6a780323b
State: Peer in Cluster (Connected)
Other names:
10.0.60.[gluster2hdd-data]

Hostname: gluster3ssd-data
Uuid: 99d146cd-35af-4243-a19f-f6464d5da607
State: Peer in Cluster (Connected)
Other names:
10.0.60.[gluster3ssd-data]

Hostname: gluster4hdd-data
Uuid: ac2c0466-8f6b-4ee7-af00-54e629eb749f
State: Peer in Cluster (Connected)
Other names:
10.0.60.[gluster3ssd-data]

Hostname: arbiter2-data
Uuid: f4e66485-5d0e-44bf-9a7d-c0475d8b5a05
State: Peer in Cluster (Connected)
Other names:
10.0.60.[arbiter2-data]

]# mkdir /data/brick#/examplevol # repeat this on each host
]# gluster volume create examplevol replica 3 arbiter 1 \ 
<span style="color:#339966;">gluster1ssd-data:/data/brick1/examplevol gluster3ssd-data:/data/brick4/examplevol \</span>
<span style="color:#339966;">arbiter1-data:/data/brick3/examplevol</span> <span style="color:#ff0000;">gluster2hdd-data:/data/brick2/examplevol \ </span>
<span style="color:#ff0000;">gluster4hdd-data:/data/brick5/examplevol arbiter2-data:/data/brick6/examplevol</span> 
<strong>#order matters! 
</strong>-Correct glusterFS cluster physical layout
<span style="color:#339966;"> gluster1.example.com - 960GB SSD    --|
 gluster3.example.com - 960GB SSD      | Group 1
 arbiter1.example.com - 50 GB HDD VM --|</span>
 <span style="color:#ff0000;">gluster2.example.com - 4 TB HDD     --|
 gluster4.example.com - 4 TB HDD       | Group 2
 arbiter2.example.com - 50 GB HDD VM --|</span> 

]# gluster volume info examplevol
Volume Name: examplevol
Type: Distributed-Replicate
Volume ID: 33ed9c61-348c-41c2-a80f-43443ef6ce99
Status: Started
Number of Bricks: 2 x (2 + 1) = 6
Transport-type: tcp
Bricks:
Brick1: gluster1ssd-data:/data/brick1/examplevol
Brick2: gluster3ssd-data:/data/brick4/examplevol
Brick3: arbiter1-data:/data/brick3/examplevol (arbiter)
Brick4: gluster2hdd-data:/data/brick2/examplevol
Brick5: gluster4hdd-data:/data/brick5/examplevol
Brick6: arbiter2-data:/data/brick6/examplevol (arbiter)
Options Reconfigured:
transport.address-family: inet
performance.readdir-ahead: on

#mount  via mgmt network on client machine
]# mount.glusterfs 10.0.0.[gluster1]:/examplevol /examplevol
]# df -h | grep examplevol
10.0.0.[gluster1]:/examplevol 4.5T 137G 4.4T 3% /nfs/examplevol</pre>
<h3>Bad create</h3>
<pre>gluster volume create examplevol replica 3 arbiter 1 \ 
<span style="color:#008000;">gluster1ssd-data:/data/brick1/examplevol gluster2hdd-data:/data/brick2/examplevol \</span>
<span style="color:#008000;">arbiter1-data:/data/brick3/examplevol</span> <span style="color:#ff0000;">gluster3ssd-data:/data/brick4/examplevol \</span>
<span style="color:#ff0000;">gluster4hdd-data:/data/brick5/examplevol arbiter2-data:/data/brick6/examplevol</span></pre>
<p>This would create just fine but I was ending up with a volume that had a max of ~1.5TB and I couldn&#8217;t at first understand what I was doing wrong. In my misunderstanding of how glusterfs should be setup, I figured the distributed set should be setup before the replication set, so the 4Tb HDD should span with the 960GB SSD, then replicate to the other set. That was wrong. Basically discs of similar size should be setup to replicate files then those sets span to the other set. If all discs were the same size this would not matter, but with varying sizes I lost 2/3 of available space by not configuring it correctly. The sets are highlighted in green vs red to better show the difference.</p>
<pre>-Incorrect glusterFS cluster physical layout
 <span style="color:#339966;">gluster1.example.com - 960GB SSD    --|
 gluster2.example.com - 4 TB HDD       | Group 1
 arbiter1.example.com - 50 GB HDD VM --|</span>
 <span style="color:#ff0000;">gluster3.example.com - 960GB SSD    --|
 gluster4.example.com - 4 TB HDD       | Group 2
 arbiter2.example.com - 50 GB HDD VM --| </span></pre>
<p>If you mess up there are a few things one must do to remove the old volume information, before one can setup a new volume.</p>
<pre>on each node:
setfattr -x trusted.glusterfs.volume-id /data/brick1/examplevol
setfattr -x trusted.gfid /data/brick1/examplevol
rm -rf /data/brick1/examplevol/.g*
rm -rf /data/brick1/examplevol/.t*
systemctl restart glusterd

</pre>
<h2>Client Install/Setup</h2>
<pre>wget -P /etc/yum.repos.d/ http://download.gluster.org/pub/gluster/glusterfs/3.7/3.7.5/CentOS/glusterfs-epel.repo
yum install gluster-client
mkdir -p /nfs/examplevol
mount.glusterfs 10.0.0.[gluster#]:/examplevol /nfs/examplevol

</pre>
<p>&nbsp;</p>
<h2>Mirror Example</h2>
<p>This was my first experimentation with GlusterFS, basically I wanted files on n-number of machines to mirror each other. Example starts with 2 Virtual machines but could be easily expanded.</p>
<pre>node1]# wget -P /etc/yum.repos.d/ http://download.gluster.org/pub/gluster/gluste fs/3.7/3.7.5/CentOS/glusterfs-epel.repo
node1]# yum install glusterfs-server
#make sure there is a second non "/" partition for the brick to be setup on
node1]# vgcreate vg_gluster /dev/sdb
node1]# lvcreate -L 29G -n brick vg_gluster
node1]# mkfs.xfs /dev/vg_gluster/brick
node1]# mount /dev/vg_gluster/brick /brick
node1]# mkdir /brick/brick# 
node1]# systemctl start glusterd
node1]# gluster peer probe node2
node1]# gluster volume create mirrorvol replica 2 node1:/brick/brick1 node2:/brick/brick2
node1]# gluster volume info
Volume Name: mirrorvol
Type: Replicate
Volume ID: 16e069b1-7226-483f-a6fb-8e90509a9870
Status: Started
Number of Bricks: 1 x 2 = 2
Transport-type: tcp
Bricks:
Brick1: node1:/brick/brick1
Brick2: node2:/brick/brick2
Options Reconfigured:
performance.readdir-ahead: on

node1]# mount.glusterfs node1:/mirrorvol /mirrorvol
node2]# mount.glusterfs node2:/mirrorvol /mirrorvol
# mount the glusterFS volumes to the same servers as they are acting as clients 
# as well as hosts
node2]# df -h
...[Redacted]
/dev/mapper/vg_gluster-brick 29G 100M 29G 1% /brick
node2:/mirrorvol 29G 100M 29G 1% /mirrorvol</pre>
<p>And this way mirroring worked just fine, touch a file on one server in /mirrorvol/test and it would pretty quickly be available on the other node. I then ramped this up with checking out an SVN project and watched as the same files were replicated to the 2nd node.</p>
