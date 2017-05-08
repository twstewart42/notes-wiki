
<h1 class="entry-title">Kickstart</h1>

<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote><p>Kickstart installations offer a means to automate the installation process, either partially or fully. Kickstart files contain answers to all questions normally asked by the installation program, such as what time zone you want the system to use, how the drives should be partitioned, or which packages should be installed. Providing a prepared Kickstart file when the installation begins therefore allows the you to perform the installation automatically, without need for any intervention from the user.</p></blockquote>
<dl>
<dt></dt>
</dl>
<p>With this technology I have brought a  CentOS with HTTPD/PHP and <a href="http://mapserver.org/introduction.html">MapServer </a>install down from a day and a half of guess work to 20-40 minute automated install</p>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ol>
<li><a class="external text" href="https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Installation_Guide/chap-kickstart-installations.html" rel="nofollow">Redhat Kickstart Guide</a></li>
<li><a class="external text" href="https://sig-io.nl/?p=372" rel="nofollow">CentOS 7 Kickstart example</a></li>
</ol>
<h1><span id="How_to_Use" class="mw-headline">How to Use</span></h1>
<ol>
<li>Deploy new, blank VM or even bare metal</li>
<li>Start Machine</li>
<li>Enable Network/PXE boot in machine bios and/or very quickly press f12 at boot time</li>
<li>On reboot, the machine should ask our DHCP server for instructions</li>
<li>The PXE boot menu should appear</li>
<li>Select the option which best fits the installation you need</li>
<li>Sit back and relax as it take ~40 minutes for the prd_web ones to install.</li>
</ol>
<h1><span id="Yum" class="mw-headline">Yum</span></h1>
<pre>yum install vsftp xinetd tftp-server syslinux</pre>
<h1><span id="DHCP" class="mw-headline">DHCP</span></h1>
<p>One must have a fully functioning dhcp server with a range of open IP addresses that are available for new machines to grab a dhcp IP address from so that they can load the PXE/kickstart file</p>
<p>edit /etc/dhcp/dhcpd.conf</p>
<pre>#testing kickstart
allow unknown-clients;
allow booting;
allow bootp;
option option-128 code 128 = string;
option option-129 code 129 = text;
next-server 10.0.0.[DH]; #if you have another dhcp server or the same address as 
                        the current one
filename "pxelinux.0";
</pre>
<p>&nbsp;</p>
<h1><span id="TFTP" class="mw-headline">TFTP</span></h1>
<p>edit /etc/xinetd.d/tftp</p>
<pre>{
socket_type = dgram
protocol = udp
wait = yes
user = root
server = /usr/sbin/in.tftpd
server_args = -s /tftpboot
disable = no
per_source = 11
cps = 100 2
flags = IPv4
}

Add a kickstart system user for semi-secure communication.
&lt;pre&gt;
adduser kickstart -s /sbin/nologin
passwd kickstart

</pre>

<p>make directories and copy pxe boot files</p>
<pre>mkdir /tftpboot
cp /usr/share/syslinux/pxelinux.0 /tftpboot/
cp /usr/share/syslinux/menu.c32 /tftpboot/
cp /usr/share/syslinux/mboot.c32 /tftpboot
cp/usr/share/syslinux/chain.c32 /tftpboot/
cp /usr/share/syslinux/ldlinux.c32 /tftpboot/
cp /usr/share/syslinux/libutil.c32 /tftpboot/
</pre>
<p>copy an ISO to /home/kickstart</p>
<pre>mkdir -p /tftpboot/images/centOS-6.4
mount -t iso9660 /home/kickstart/centos.ISO /tftpboot/images/centOS-6.4 -o loop,ro
ln -s /tftpboot/images/centOS-6.4 /home/kickstart/CentOS-6.4 # for the kickstart file to find the iso
</pre>
<h2><span id="PXEBoot_Menu" class="mw-headline">PXEBoot Menu</span></h2>
<p>The next step is to create the tui menu that one will see when booting into the PXE server. Theoretically you can make a PXEboot for any linux distribution as long as you can find the Kernel, initrd, and it can be understood by menu.c32. One of my goals with this was to create a &#8220;SYSTOOLS&#8221; menu that would have special live ISO versions of things like clonezilla, KNOPPIX, but I have not been able to achieve this.</p>
<p>vim /tftpboot/pxelinux.cfg/default</p>
<pre>default menu.c32
prompt 0
timeout 300
ONTIMEOUT local

MENU TITLE PXE Menu

LABEL CentOS 6.4 x64
        MENU Label CentOS 6.4 x64 Base
        KERNEL images/CentOS-6.4/isolinux/vmlinuz
        append initrd=images/CentOS-6.4/isolinux/initrd.img ramdisk_size=10000 ks=ftp://kickstart:kickstart@10.0.0.K/kickstart/CentOS6.4x64.ks

LABEL CentOS 6.4 x64 prd web
        MENU Label CentOS 6.4 x64 prd web
        KERNEL images/CentOS-6.4/isolinux/vmlinuz
        append initrd=images/CentOS-6.4/isolinux/initrd.img ramdisk_size=10000 ks=ftp://kickstart:kickstart@10.0.0.k/kickstart/CentOS6_prdweb.ks


LABEL CentOS 6.4 x64 prd sql
        MENU Label CentOS 6.4 x64 prd sql
        KERNEL images/CentOS-6.4/isolinux/vmlinuz
        append initrd=images/CentOS-6.4/isolinux/initrd.img ramdisk_size=10000 ks=ftp://kickstart:kickstart@10.0.0.K/kickstart/CentOS6_prdsql.ks

LABEL CentOS 7 base
        MENU Label CentOS 7.0 x64 Base
        #menu images/Centos-7/isolinux/vesamenu.c32
        KERNEL images/Centos-7/isolinux/vmlinuz
        append initrd=images/Centos-7/isolinux/initrd.img  ramdisk_size=10000 ks=ftp://kickstart:kickstart@10.0.0.K/kickstart/cent7.ks


LABEL CentOS 7 prd web
        MENU Label CentOS 7.0 x64 prd web
        #menu images/Centos-7/isolinux/vesamenu.c32
        KERNEL images/Centos-7/isolinux/vmlinuz
        append initrd=images/Centos-7/isolinux/initrd.img  ramdisk_size=10000 ks=ftp://kickstart:kickstart@10.0.0.K/kickstart/cent7_prdweb.ks

LABEL CentOS 7 prd sql
        MENU Label CentOS 7.0 x64 prd sql
        #menu images/Centos-7/isolinux/vesamenu.c32
        KERNEL images/Centos-7/isolinux/vmlinuz
        append initrd=images/Centos-7/isolinux/initrd.img  ramdisk_size=10000 ks=ftp://kickstart:kickstart@10.0.0.K/kickstart/cent7_prdsql.ks


LABEL local
        MENU LABEL Boot local hard drive
        menu default
        localboot -1

</pre>
<h1><span id="Kickstart_config_file" class="mw-headline">Kickstart config file</span></h1>
<p>Below is an example of a kickstart file for the CentOS6.4 ISO. Kickstart files must be named .ks or it will fail to be recognized by the PXEBoot.</p>
<pre># Kickstart file CentOS6.4x64.ks

#version=DEVEL
install
url --url ftp://kickstart:hunter2@10.0.0.[K]/CentOS-6.4
#cdrom
#initial Setup
lang en_US.UTF-8
keyboard us
timezone --utc America/New_York

#Network Setup
network --onboot yes --device eth0 --bootproto dhcp --netmask 255.255.255.0 --gateway 10.0.0.254 --nameserver 10.0.0.NS1
#network --onboot no --device eth0 --bootproto dhcp --noipv6

#Security Section
rootpw  password # please change after initial boot
firewall --disable
selinux --disabled

auth --enableshadow --enableldap --enableldapauth --ldapserver=ldp01.example.com, ldp02.example.com --ldapbasedb="dc=example,dc=com" --enablecache

bootloader --location=mbr --driveorder=sda --append="crashkernel=auto rhgb quiet"


#Disk Partitioning

zerombr yes
        ### Tell it to do a dumb move and blow away all partitions
clearpart --all
part /boot      --size 500 --fstype=ext4
part swap --size 2048
part / --size=10240 --grow --fstype=ext4

repo --name="Epel" --baseurl=http://download.fedoraproject.org/pub/epel/6/x86_64

# Install Packages
%packages
@base
@console-internet
@core
@debugging
@directory-client
@hardware-monitoring
@java-platform
@large-systems
@network-file-system-client
@performance
@perl-runtime
@server-platform
@server-policy
pax
oddjob
sgpio
device-mapper-persistent-data
samba-winbind
certmonger
pam_krb5
krb5-workstation
perl-DBD-SQLite
sssd
ftp

%post

</pre>
<h1><span id="Post_Install" class="mw-headline">Post Install</span></h1>
<p>You can automate things even further by creating bash like commands in the %post section of the kickstart script</p>
<h2><span id="Prd_Web_Post_Install" class="mw-headline">Prd Web Post Install</span></h2>
<p>The CentOS basic install pretty much stays the same for each server. Below is the post installation script which has been massively altered to set things up with <a title="Mapserver" href="http://mapserver.org/introduction.html">MapServer</a> and all of our required dependencies. I will add comments to help explain why I have set this up the way they are.</p>
<pre> 

%post

# add another nameserver
echo "nameserver 10.0.0.D1" &gt;&gt; /etc/resolv.conf
echo "nameserver 10.0.0.D2" &gt;&gt; /etc/resolv.conf

##Begin setup of mapserver
```
rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
cd /opt; wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -Uvh /opt/epel-*.rpm
cd /opt; wget http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-centos93-9.3-1.noarch.rpm
rpm -Uvh /opt/pgdg-*.rpm
rpm -Uvh http://elgis.argeo.org/repos/6/elgis-release-6-6_0.noarch.rpm

#this config is spefic to mapserver 6.4 I tried to make it generic but that was impossible for me to figure out the logistics

cd /opt; wget http://download.osgeo.org/mapserver/mapserver-6.4.1.tar.gz

yum clean all

yum -y install perl perl-XML-Simple perl-GD, perl-libs perl-ExtUtils-MakeMaker perl-File-Fetch, perl-Term-UI perl-IO-Compress-Bzip2 perl-SOAP-Lite perl-CPANPLUS perl-OLE-Storage_Lite perl-XML-Grove perl-Module-Load  perl-IO-Compress-Zlib perl-CPAN perl-Newt perl-Module-Loaded perl-HTML-Parser perl-Bit-Vector perl-MailTools perl-Unicode-Map perl-parent perl-Spreadsheet-XLSX perl-DBD-Pg perl-GDGraph perl-version perl-Params-Check perl-IO-Compress-Base perl-ExtUtils-ParseXS perl-Package-Constants perl-ExtUtils-CBuilder perl-Archive-Tar perl-DBI perl-DBD-SQLite perl-Module-CoreList perl-HTML-Tagset perl-BSD-Resource perl-libxml-perl perl-Date-Calc perl-MIME-Types perl-Date-Manip perl-Parse-RecDescent perl-Time-HiRes perl-Jcode perl-Net-SSLeay perl-Crypt-SSLeay perl-GDTextUtil perl-Pod-Escapes perl-Module-Pluggable perl-Locale-Maketext-Simple perl-GDTextUtil perl-Pod-Escapes perl-Module-Pluggable perl-Locale-Maketext-Simple perl-Log-Messag perl-Compress-Raw-Zlib perl-Test-Harness perl-IPC-Cmd perl-Test-Simple perl-IO-Zlib perl-URI perl-DBIx-Simple perl-Digest-SHA perl-XML-Parser perl-ExtUtils-Embed perl-DBD-MySQL perl-Email-Date-Format perl-MIME-Lite perl-Archive-Zip perl-CGI  perl-IO-stringy perl-Digest-Perl-MD5 perl-YAML perl-XML-Twig perl-Module-Load-Conditional perl-Compress-Zlib perl-Object-Accessor perl-Compress-Raw-Bzip2 perl-libwww-perl perl-Module-Build perl-Carp-Clan perl-TimeDate perl-Crypt-RC4 perl-Time-Piece perl-Spreadsheet-ParseExcel perl-XML-Dumper perl-Pod-Simple perl-devel perl-Archive-Extract perl-Log-Message-Simple perl-YAML-Syck perl-Parse-CPAN-Meta perl-Spreadsheet-WriteExcel

yum -y install php php-devel php-mysql php-pgsql php-pdo php-gd php-cli php-soap php-xml glibc gcc gcc-c++ cmake swig ftp subversion git

yum -y install postgresql9*-devel postgis2* postgis2*-devel* geos geos-devel proj proj-epsg proj-devel gdal gdal-java gd gd-devel gdbm gdal-devel gd libcurl-devel libxml2-devel libtool libtiff libgeotiff libjpeg libdng-devl libpng freetype zlib-devel giflib-devel

#mkdir -p /opt/mapserver
cd /opt/; tar -xzvf /opt/mapserver*.tar.gz -C /opt


touch /opt/ftp.sh
chmod 775 /opt/ftp.sh

# make ftp connection to get cmake file for mapserver ##it took me a long time to figure out how to get a config file on the fly.
#You have to create shell scripts that ftp can use to download the pre-config file. 
#Check file persmission on the ftp server if you add a file to download, you can change them once they have been downloaded locally.

echo "
#!/bin/bash
cd /opt
HOST=10.0.0.K
USER=kickstart
PASSWD=********

ftp -i -n -v 10.0.0.R &lt;&lt; EOT
binary
user kickstart kickstart
cd mapserver
mget CMakeLists.txt
bye
EOT
" &gt;&gt; /opt/ftp.sh

#run ftp.sh shell script
/opt/ftp.sh



cd /opt/mapserver-6.4.1;
cp -rf /opt/CMakeLists.txt /opt/mapserver-6.4.1/CMakeLists.txt
mkdir -p /opt/mapserver-6.4.1/build
cd  /opt/mapserver-6.4.1/build; cmake -DCMAKE_PREFIX_PATH="/usr/pgsql-9.3/bin;/usr/bin" ..
make
make install
cd /opt/mapserver-6.4.1/build/mapscript/perl
make
make install
cd /opt/mapserver-6.4.1/build/mapscript/php
make
make install


touch /etc/ld.so.conf.d/mapserver.conf
echo "/usr/local/lib" &gt;&gt; /etc/ld.so.conf.d/mapserver.conf

ldconfig

ln -s /usr/local/lib/libmapserver-6.4.1.so /usr/lib64/libmapserver-6.4.1.so
ln -s /lib64/libreadline.so.6.0 /usr/lib64/libreadline.so.6


# this used to be /usr/local/share/proj/epsg but has since changed
echo "
# Google Projection
 &lt;900913&gt; +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +no_defs &lt;&gt; " &gt;&gt; /usr/share/proj/epsg


##END SETUP for mapserver

mkdir -p /nfs
#mkdir /nfs/carp

yum -y update

#Set up other systems related configs.
yum -y install net-snmp net-snmp-devel ntpdate

authconfig --enablesssd --enablesssdauth --enablelocauthorize --update

# we may get more creative with cfengine and move some of this system level configs to that service instead

touch /opt/ftp_get_sys_configs.sh
chmod 775 /opt/ftp_get_sys_configs.sh

echo "
#!/bin/bash
cd /opt
HOST=10.0.0.K
USER=kickstart
PASSWD=***********

ftp -i -n -v 10.0.0.R &lt;&lt; EOT
binary
user kickstart kickstart
cd systems
mget sssd.conf
mget sshd-banner
mget snmpd.conf
mget nsswitch.conf
bye
EOT
" &gt;&gt; /opt/ftp_get_sys_configs.sh
/opt/ftp_get_sys_configs.sh

cp /etc/sssd/sssd.conf /etc/sssd/sssd.conf.orig
cp -rf /opt/sssd.conf /etc/sssd/sssd.conf
cp -rf /opt/sshd-banner /etc/ssh/sshd-banner
echo "Banner /etc/ssh/sshd-banner" &gt;&gt; /etc/ssh/sshd_config
mv /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.orig
cp -rf /opt/snmpd.conf /etc/snmp/snmpd.conf
cp /etc/nsswitch.conf /etc/nsswitch.conf.orig
cp -rf /opt/nsswitch.conf /etc/nsswitch.conf

/etc/init.d/sssd restart
chkconfig sssd on
/etc/init.d/sshd restart
/etc/init.d/snmpd restart
chkconfig snmpd on
/etc/init.d/ntpd start
chkconfig ntpd on

#Set up cfengine
cd /opt/; wget -O- https://s3.amazonaws.com/cfengine.packages/quick-install-cfengine-community.sh | sudo bash
/var/cfengine/bin/cf-agent --bootstrap 10.0.0.CF

%end
reboot
```
</pre>
<h2><span id="Prd_SQL_Post_Install" class="mw-headline">Prd SQL Post Install</span></h2>
<p>Installes a <a href="https://www.postgresql.org/">PostgreSQL</a> server with <a href="http://postgis.net/">PostGIS</a></p>
<p>kickstart.example.com/kickstart/CentOS6_prdsql.ks</p>
<pre>
```
%post

# add another nameserver
echo "nameserver 10.0.0.D1" &gt;&gt; /etc/resolv.conf
echo "nameserver 10.0.0.D2" &gt;&gt; /etc/resolv.conf


##Begin setup of mapserver

rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
cd /opt; wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -Uvh /opt/epel-*.rpm
cd /opt; wget http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-centos93-9.3-1.noarch.rpm
rpm -Uvh /opt/pgdg-*.rpm
rpm -Uvh http://elgis.argeo.org/repos/6/elgis-release-6-6_0.noarch.rpm

#cd /opt; wget http://download.osgeo.org/mapserver/mapserver-6.4.1.tar.gz
#cd /opt; wget http://ftp.postgresql.org/pub/source/v9.2.4/postgresql-9.2.4.tar.gz
#cd /opt; wget http://download.osgeo.org/postgis/source/postgis-2.0.3.tar.gz

yum clean all


yum -y install postgresql9*-server postgresql9*-devel postgis2* postgis2*-devel* geos geos-devel proj proj-epsg proj-devel gdal gdal-java gd gd-devel gdbm gdal-devel gd libcurl-devel libxml2-devel libtool libtiff libgeotiff libjpeg libdng-devl libpng freetype zlib-devel giflib-devel pgtune

useradd postgres
su - postgres -c "/usr/pgsql-9.3/bin/initdb /var/lib/pgsql/data"
echo "listen_addresses = '*' "&gt;&gt; /var/lib/pgsql/data/postgresql.conf
echo "max_connections = 500 " &gt;&gt; /var/lib/pgsql/data/postgresql.conf

su - postgres -c "pgtune -i /var/lib/pgsql/data/postgresql.conf -o /var/lib/pgsql/data/postgresql.conf.pgt -c 500"
cp /var/lib/pgsql/data/postgresql.conf /var/lib/pgsql/data/postgresql.conf.old
su - postgres -c "cp /var/lib/pgsql/data/postgresql.conf.pgt /var/lib/pgsql/data/postgresql.conf"

su - postgres -c "/usr/pgsql-9.3/bin/pg_ctl -D /var/lib/pgsql/data -l /var/lib/pgsql/pg_startup.log start"

yum -y update

#Set up other systems related configs.
yum -y install net-snmp net-snmp-devel ntpdate

authconfig --enablesssd --enablesssdauth --enablelocauthorize --update

touch /opt/ftp_get_sys_configs.sh
chmod 775 /opt/ftp_get_sys_configs.sh

#this works but is messy, cfengine should do the trick once I figure that all out
echo "
#!/bin/bash
cd /opt
HOST=10.0.0.K
USER=kickstart
PASSWD=*************

ftp -i -n -v 10.0.0.R &lt;&lt; EOT
binary
user kickstart *********
cd systems
mget sssd.conf
mget sshd-banner
mget snmpd.conf
mget pg_hba.conf
mget postgresqld
mget nsswitch.conf
bye
EOT
" &gt;&gt; /opt/ftp_get_sys_configs.sh

/opt/ftp_get_sys_configs.sh

cp /etc/sssd/sssd.conf /etc/sssd/sssd.conf.orig
cp -rf /opt/sssd.conf /etc/sssd/sssd.conf
chmod 600 /etc/sssd/sssd.conf
chown root:root /etc/sssd/sssd.conf
cp -rf /opt/sshd-banner /etc/ssh/sshd-banner
echo "Banner /etc/ssh/sshd-banner" &gt;&gt; /etc/ssh/sshd_config
mv /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.orig
cp -rf /opt/snmpd.conf /etc/snmp/snmpd.conf
chmod 600 /etc/snmp/snmpd.conf
chown root:root /etc/snmp/snmpd.conf
mv /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.orig
cp -rf /opt/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf
chmod 600 /var/lib/pgsql/data/pg_hba.conf
chown postgres:postgres /var/lib/pgsql/data/pg_hba.conf
cp -rf /opt/postgresqld /etc/init.d/postgresql
chmod 750 /etc/init.d/postgresql
cp -rf /etc/nsswitch.conf /etc/nsswitch.conf.orig
cp -rf /opt/nsswitch.conf /etc/nsswitch.conf

/etc/init.d/sssd restart
chkconfig sssd on
/etc/init.d/sshd restart
/etc/init.d/snmpd restart
chkconfig snmpd on
/etc/init.d/ntpd start
chkconfig ntpd on
chkconfig postgresql on


su - postgres -c "/usr/pgsql-9.3/bin/pg_ctl -d /var/lib/pgsql/data -l /var/lib/pgsql/pg_startup.log reload"


#Set up cfengine
cd /opt/; wget -O- https://s3.amazonaws.com/cfengine.packages/quick-install-cfengine-community.sh | sudo bash
/var/cfengine/bin/cf-agent --bootstrap 10.0.0.CF

%end
reboot
```
</pre>
</div>
