<!-- start content -->
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote>PostgreSQL is an open-source relational database used in support for many of our web and application based projects that need support of geographically aware inputs, i.e. PostGIS and mapserver.</blockquote>
<h1><span id="Overview" class="mw-headline">Overview</span></h1>
The following steps must be installed and compiled in order to ensure a proper configuration of the software packages.
<ol>
	<li>centos-6.x/7.x</li>
	<li><a class="external text" href="http://www.postgresql.org/" rel="nofollow">postgresql-9.x</a></li>
	<li><a class="external text" href="http://trac.osgeo.org/proj/" rel="nofollow">proj-4.8.0</a></li>
	<li><a class="external text" href="http://trac.osgeo.org/geos/" rel="nofollow">geos-3.3.6</a></li>
	<li><a class="external text" href="http://postgis.refractions.net/" rel="nofollow">postgis-2.x</a></li>
</ol>
Further reading

<dl><dd>
<ul>
	<li><a class="extiw" title="wikipedia:PostgreSQL" href="http://en.wikipedia.org/wiki/PostgreSQL">Wikipedia:PostgreSQL</a></li>
	<li><a class="extiw" title="wikipedia:PostGIS" href="http://en.wikipedia.org/wiki/PostGIS">Wikipedia:PostGIS</a></li>
	<li><a class="extiw" title="wikipedia:Open Geospatial Consortium" href="http://en.wikipedia.org/wiki/Open_Geospatial_Consortium">Wikipedia:Open Geospatial Consortium</a></li>
</ul>
</dd></dl>
<h1><span id="Installation" class="mw-headline">Installation</span></h1>
<h2><span id="CentOS_6_with_PostgreSQL_9.3" class="mw-headline">CentOS 6 with PostgreSQL 9.3</span></h2>
I have distilled down the steps for installation of the PostgreSQL server along with Proj, Geos, and Postgis. This is how I install it on our VM's through an automated <a title="Kickstart" href="https://twstewart84.wordpress.com/systems-administration/kickstart/">kickstart</a> script. I will add #comments to explain things in the script.
<pre>#download required repos, versions and links may change, update them as new versions are tested and released. The old way of downloading source files and 
compiling is not truly necessary anymore since these are repos directly from the software creators so they are just as up to date as can be.
rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
cd /opt; wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -Uvh /opt/epel-*.rpm
cd /opt; wget http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-centos93-9.3-1.noarch.rpm
rpm -Uvh /opt/pgdg-*.rpm
rpm -Uvh http://elgis.argeo.org/repos/6/elgis-release-6-6_0.noarch.rpm

yum clean all

# install with yum, will catch and missing libraries or dependencies.
yum -y install postgresql9*-server postgresql9*-devel postgis2* postgis2*-devel* geos geos-devel proj proj-epsg proj-devel gdal gdal-java gd gd-devel gdbm
 gdal-devel gd libcurl-devel libxml2-devel libtool libtiff libgeotiff libjpeg libdng-devl libpng freetype zlib-devel giflib-devel pgtune

#setup user and edit postgresql.conf
useradd postgres
su - postgres -c "/usr/pgsql-9.3/bin/initdb /var/lib/pgsql/data"
echo "listen_addresses = '*' "&gt;&gt; /var/lib/pgsql/data/postgresql.conf
echo "max_connections = 500 " &gt;&gt; /var/lib/pgsql/data/postgresql.conf

#using pgtune, tune it so we can optimize for individual system hardware limits and settings.
su - postgres -c "pgtune -i /var/lib/pgsql/data/postgresql.conf -o /var/lib/pgsql/data/postgresql.conf.pgt -c 500"
cp /var/lib/pgsql/data/postgresql.conf /var/lib/pgsql/data/postgresql.conf.old
su - postgres -c "cp /var/lib/pgsql/data/postgresql.conf.pgt /var/lib/pgsql/data/postgresql.conf"

su - postgres -c "/usr/pgsql-9.3/bin/pg_ctl -D /var/lib/pgsql/data -l /var/lib/pgsql/pg_startup.log start"



</pre>
The next step is to load the PostGIS tables into the template1 database so all projects created on that server have those tables. This is not automated.
<pre>#log into template1 db
/usr/pgsql-9.3/bin/psql template1 -U postgres

template1=# \i /usr/pgsql-9.3/share/contrib/postgis-2.1/postgis.sql
template1=# \i /usr/pgsql-9.3/share/contrib/postgis-2.1/legacy.sql
# there are also spation_ref_sys.sql and rtpostgis.sql to be loaded and unisntall.sql files if you should need to remove anything
</pre>
<h2><span id="CentOS_7_with_PostgreSQL_9.4" class="mw-headline">CentOS 7 with PostgreSQL 9.4</span></h2>
Follow these directions to install <a class="external text" href="http://yum.postgresql.org/repopackages.php" rel="nofollow">PostgreSQL</a> 9.4 on CentOS 7
<pre>rpm -Uvh http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm
rpm -Uvh http://yum.postgresql.org/9.4/redhat/rhel-7-x86_64/pgdg-centos94-9.4-1.noarch.rpm

yum clean all

yum -y install postgresql94-server postgresql94-devel postgis2* postgis2*-devel* geos geos-devel proj proj-epsg proj-devel gdal gdal-java gd gd-devel gdbm gdal-devel gd libcurl-devel
 libxml2-devel libtool libtiff libgeotiff libjpeg libdng-devl libpng freetype zlib-devel giflib-devel

#useradd postgres
su - postgres -c "/usr/pgsql-9.4/bin/initdb /var/lib/pgsql/9.4/data"
echo "listen_addresses = '*' "&gt;&gt; /var/lib/pgsql/9.4/data/postgresql.conf
echo "max_connections = 500 " &gt;&gt; /var/lib/pgsql/9.4/data/postgresql.conf

#pgtune is not yet available for C7

su - postgres -c "/usr/pgsql-9.4/bin/pg_ctl -D /var/lib/pgsql/9.4/data -l /var/lib/pgsql/pg_startup.log start"

#grimm fix for static libraries
chmod 744 /usr/pgsql-9.4/share/postgresql-9.4-libs.conf

</pre>
The next step is to load the PostGIS tables into the template1 database so all projects created on that server have those tables. This is not automated.
<pre>#log into template1 db
/usr/pgsql-9.4/bin/psql template1 -U postgres

template1=# \i /usr/pgsql-9.4/share/contrib/postgis-2.1/postgis.sql
template1=# \i /usr/pgsql-9.4/share/contrib/postgis-2.1/spatial_ref_sys.sql
template1=# \i /usr/pgsql-9.4/share/contrib/postgis-2.1/legacy.sql

# there are also spation_ref_sys.sql and rtpostgis.sql to be loaded and unisntall.sql files if you should need to remove anything
</pre>
<h1><span id="Authentication_and_Access" class="mw-headline">Authentication and Access</span></h1>
Traditionally all access is controlled via the <a class="external text" href="http://www.postgresql.org/docs/9.3/static/auth-pg-hba-conf.html" rel="nofollow">/var/lib/pgsql/data/pg_hba.conf</a> file with explicit IP/32 access for the postgres database user. One has to keep in mind that there is a LINUX user postgres and a DATABASE user named postgres. Two separate levels of access. if one is using the postgres database user and has the IP/32 trust designation in the pg_hba.conf file then that user is given full access no questions, passwords, check points, etc, asked. We are trying to move away from that approach as I believe it leaves some of our most important databases open to anything from that IP address.

Below is a better way to setup access and users based on the project.
<ol>
	<li>Create project specific user</li>
	<li>Set up SSL on new Postgres Servers (Only relevant for new builds)</li>
	<li>edit pg_hba to only allow that project_db_user to acces that specific databse on that machine, no others, over SSL.</li>
	<li>reload service</li>
</ol>
Create a user for the project, example using agfleetio_db_user, and then <a class="external text" href="http://www.postgresql.org/docs/9.3/static/sql-grant.html" rel="nofollow">grant</a> user permissions.
<pre>#log into postgres server
create user project_db_user WITH PASSWORD '*********';
\c projectdb
ALTER USER project_db_user SET SEARCH_PATH TO public;
GRANT USAGE ON SCHEMA public TO project_db_user;
GRANT ALL ON SCHEMA public TO project_db_user;
GRANT ALL ON database projectdb TO project_db_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO project_db_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO project_db_user;
ALTER USER project_db_user SET SEARCH_PATH TO api, core, data, irrigation, profiles, public, records;
GRANT USAGE ON SCHEMA api, core, data, public, records TO project_db_user;
GRANT ALL ON SCHEMA api, core, data, public, records TO project_db_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA api, core, data, public, records TO project_db_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA api, core, data, public, records TO project_db_user;
</pre>
Setup SSL (can be done way before this on initial setup of server)
<b>Certificates must be named server.crt, server.key, root.crt or server will crash on restart</b>
<pre> #copy your example.com.cert, keyfile and the ca-chain file to /var/lib/pgsql/9.3/data and rename them to server.crt, server.key and root.crt
 chown postgres:postgres /var/lib/pgsql/9.3/data/server.crt
 chown postgres:postgres /var/lib/pgsql/9.3/data/server.key
 chown postgres:postgres /var/lib/pgsql/9.3/data/root.crt
 chmod 600 /var/lib/pgsql/9.3/data/server.crt
 chmod 600 /var/lib/pgsql/9.3/data/server.key
 chmod 600 /var/lib/pgsql/9.3/data/root.crt
</pre>
<pre>vim /var/lib/pgsql/9.3/data/postgres.conf

#add the following lines at the very bottom
ssl = true                              # (change requires restart)
ssl_ciphers = 'HIGH:RC4-SHA:!LOW:!EXP:!MD5:!ADH:!3DES:!DES:@STRENGTH'   # allowed SSL ciphers
                                        # (change requires restart)
#ssl_renegotiation_limit = 512MB        # amount of data between renegotiations
ssl_cert_file = 'server.crt'            # (cp zedxinc.crt to ../server.crt)
ssl_key_file = 'server.key'             # (cp zedxinc.key to ../server.key)
ssl_ca_file = 'root.crt'                # (cp zedxinc.ca_bundle to ../root.crt)

</pre>
Setup pg_hba.conf the proper way
<pre>hostssl projectdb       project_db_user       10.0.1.[web001]/32   md5
#or if hostssl will not work(old source built pgsql)
host  projectdv         project_db_user       10.0.1.[web001]/32  md5
</pre>
Old bad way for example, not to be used anymore
<pre>host all all 10.0.1.[web001]/32 trust
</pre>
Reload service so pg_hba is reread by the poostgres service.
<pre> /usr/pgsql-9.3/bin/pg_ctl -D /var/lib/pgsql/9.3/data -l /var/lib/pgsql/pg_startup.log reload
</pre>
<h1><span id="Dump_and_Restore" class="mw-headline">Dump and Restore</span></h1>
A lot of times we will have to move databases around from dev -&gt; beta -&gt; production. This requires a dump and restore procedure

You can do this one of two way, enable pg_hba so that one can dump a file to the server or you can dump localy and scp/rsync the file over, without enabling pg_hba.
<ol>
	<li>pg_dump with hba enabled</li>
</ol>
<pre># example given is if you were logged into sql00X and needed the database from agcon2
/usr/local/pgsql/bin/pg_dump -h db02.example.com projectdb -i -Fc -f /var/lib/pgsql/project.sql
</pre>
<ol>
	<li>local pg_dump without hba enabled</li>
</ol>
<pre>/usr/local/pgsql/bin/pg_dump projectdb -i -Fc -f /var/lib/pgsql/projectdb.sql
#then copy file to new location
</pre>
<ol>
	<li>Restore database</li>
</ol>
<pre>/usr/local/pgsql/bin/pg_restore -d projectdb -i -Fc /var/lib/pgsql/projectdb.sql
</pre>
<h2><span id="Postgis_Upgrade" class="mw-headline"><a class="external text" href="http://postgis.net/docs/manual-2.2/postgis_installation.html#hard_upgrade" rel="nofollow">Postgis</a> Upgrade</span></h2>
A lot of times when moving SQL databases from an older server to a newer one there can be conflicts with different versions of the postgis plug to postgres. Follow these upgrade steps to ensure no data is lost and the database is uptodate with the version of <a class="external text" href="http://postgis.net/docs/manual-2.2/postgis_installation.html#hard_upgrade%7C" rel="nofollow">postgis</a> on the server.

<b>Check postgis version</b>
<pre>       
projectdb=#  SELECT postgis_full_version();
                                           postgis_full_version

--------------------------------------------------------------------------------
---------------------
 POSTGIS="2.1.4 r12966" GEOS="3.4.2-CAPI-1.8.2 r3921" PROJ="Rel. 4.8.0, 6 March
2012" LIBXML="2.9.1"

                 
</pre>
<pre> postgres@oldserver #]pg_dump -h localhost -p 5432 -U postgres -Fc -b -v -f /var/lib/pgsql/projectdb.sql projectdb
 scp /var/lib/pgsql/projectdb.sql newserver:/var/lib/pgsql
 postgres@newserver #] /usr/pgsql-9.5/share/contrib/postgis-2.2/postgis_restore.pl /var/lib/pgsql/projectdb.sql | psql projectdb 2&gt; error.txt
</pre>
<pre>                                            postgis_full_version

------------------------------------------------------------------------------------------------------------------------------------
-------------------------------
 POSTGIS="2.2.1 r14555" GEOS="3.5.0-CAPI-1.9.0 r4084" PROJ="Rel. 4.8.0, 6 March 2012" GDAL="GDAL 1.11.2, released 2015/02/10" LIBXML
="2.9.1" LIBJSON="0.11" RASTER
(1 row)
</pre>
<h1><span id="Make_PostgreSQL_a_daemon_service" class="mw-headline">Make PostgreSQL a daemon service</span></h1>
If PostgreSQL is built from source like on most all machines we have trouble with it acting like a service and have to do EXTRA work to restart postgres and that is unacceptable, also without this step it will not start at boot time and that's a pain during restarts.
<h2><span id="CentOS_5.2F6" class="mw-headline">CentOS 5/6</span></h2>
<pre>cp /usr/local/src/postgresql-9.2.4/contrib/start-scripts/linux /etc/rc.d/init.d/postgresql
chmod a+x /etc/rc.d/init.d/postgresql
vim /etc/rc.d/init.d/postgresql -- change PGDATA and prefix if necessary
chkconfig --add postgresql

service postgresql status
pg_ctl: server is running (PID: 8705)
/usr/local/pgsql/bin/postgres "-D" "/var/lib/pgsql/data"
</pre>
<h2><span id="CentOS_7" class="mw-headline">CentOS 7</span></h2>
<pre>systemctl enable postgresl-9.4
vim /usr/lib/systemd/system/postgresql-9.4.service
#Edit pg_ctl commands to match how the system is configure, usually change /usr/bin/pg_ctl to /usr/pgsql9-4/bin/pg_ctl, things like that
systemctl daemon-reload
#stop manually started postgis (su - postgres; /usr/pgsql-9.4/bin/pg-ctl -d /var/lib/pgsql/9.4/data stop -m fast;)
systemctl start postgresql-9.4
systemctl enable postgresql-9.4
systemctl status postgresql-9.4
postgresql-9.4.service - PostgreSQL 9.4 database server
   Loaded: loaded (/usr/lib/systemd/system/postgresql-9.4.service; enabled)
   Active: active (running) since Wed 2014-12-03 16:00:40 EST; 37min ago
 Main PID: 7068 (postgres)
   CGroup: /system.slice/postgresql-9.4.service
           ├─7068 /usr/pgsql-9.4/bin/postgres -D /var/lib/pgsql/9.4/data
           ├─7069 postgres: logger process
           ├─7071 postgres: checkpointer process
           ├─7072 postgres: writer process
           ├─7073 postgres: wal writer process
           ├─7074 postgres: autovacuum launcher process
           ├─7075 postgres: stats collector process
           ├─7215 postgres: bucardo bucardo [local] idle
           ├─7217 postgres: projectdb_db_user projectdb 10.0.0.[web001](43044) idle
           ├─7219 postgres: bucardo bucardo [local] idle
           └─7220 postgres: projectdb_db_user agfleetio 10.0.0.[web001](43045) idle

Dec 03 16:00:40 sql001.example.com pg_ctl[7064]: server starting
Dec 03 16:00:40 sql001.example.com systemd[1]: Started PostgreSQL 9.4 database server.
</pre>
<h1><span id="Legacy_Install" class="mw-headline">Legacy Install</span></h1>
This shows each manual step to compile PostgreSQL with PostGIS
<h2><span id="CentOS" class="mw-headline">CentOS</span></h2>
<pre>1.	install a base centos configuration on the server that will host the database by choosing the defaults through the setup wizard.
dependencies for postgresql and everything
1.	yum install zlib-devel readline-devel readline-static gcc gcc-c++ libxml2-devel
for geos
2.	yum install gcc gcc-c++
for postgis
3.	yum install libxml2-devel
</pre>
<h2><span id="PostgreSQL" class="mw-headline"><a class="external text" href="http://www.postgresql.org/" rel="nofollow">PostgreSQL</a></span></h2>
<pre>1.      Download source from www.postgresql.org
2.	postgresql will be downloaded in a tar.gz file.  run the command tar-xzvf on the tar.gz to extract the source code.
3.	cd into the directory created for postgres.
4.	run the command ./configure. note: some dependency requirements for postgresql may not be installed.  these packages can be found in the yum rpm repository for easy installation.
5.	once postgresql is configured without errors, run the command “make” and "make install".
6.	postgresql is now successfully installed.
</pre>
<h2><span id="Proj" class="mw-headline"><a class="external text" href="http://trac.osgeo.org/proj/" rel="nofollow">Proj</a></span></h2>
<pre>1.      Download latest source from trac.osgeo.org/proj
2.	proj will be downloaded in the same tar.gz format as postgresql.  it can be successfully configured by following steps 2-6 of the postgresql installation.
</pre>
<h2><span id="Geos" class="mw-headline"><a class="external text" href="http://trac.osgeo.org/geos/" rel="nofollow">Geos</a></span></h2>
<pre>1.      Download latest source from trac.osgeo.org/geos
2.	geos will be downloaded in tar.bz2 format.  to extract the source code, first run the command “bunzip2” on the tar.bz2 file for geos.  you will notice the bz2 extension has disappeared.  next run the command “tar –xvf” on the newly created tar file for geos.
3.	the installation can be completed by following steps 3-6 of the postgresql installation.
</pre>
<h2><span id="PostGIS" class="mw-headline"><a class="external text" href="http://postgis.refractions.net/" rel="nofollow">PostGIS</a></span></h2>
<pre> 1. Download latest source from postgis.refractions.net
 2. follow steps 2-6 of the postgresql installation to configure postgis.
 3. on occasion, postgis cannot locate the config files for both postgresql and geos.  in this instance you will need to add the following commands when running ./configure.  –with-pgconfig=/usr/local/pgsql/bin/pg_config and –with-geosconfig=/usr/local/bin/geos-config –without-raster.   these commands will ensure that postgis is compiled with the proper support for both postgresql and geos.
 4. Load postgis tables
    /usr/loval/pgsql/bin/psql template1
    template1=#\i /usr/pgsql-9.3/share/contrib/postgis-2.1/postgis.sql
    template1=#\i /usr/pgsql-9.3/share/contrib/postgis-2.1/legacy.sql
</pre>
At this point PostgreSQL should be all installed and you can begin setting up user, databases, and access to the service.

<hr />

</div>