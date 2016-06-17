<div id="content" role="main">

				
					
<article id="post-603" class="post-603 page type-page status-publish hentry">
	<header class="entry-header">
		<h1 class="entry-title">FreeIPA</h1>
	</header><!-- .entry-header -->

	<div class="entry-content">
		<p><!-- start content --></p>
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote><p>FreeIPA is an integrated security information management solution combining Linux (Fedora/CentOS), 389 Directory Server, MIT Kerberos, NTP, DNS, Dogtag (Certificate System). It consists of a web interface and command-line administration tools.</p></blockquote>
<dl>
<dt>I&#8217;ll admit this document is pretty rough as it is a very large project with many seperate pieces, no matter how many times (twice now) I set this up there is a lot of googling involved.</dt>
</dl>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ul>
<li><a class="external text" href="http://www.freeipa.org/page/Main_Page" rel="nofollow">FreeIPA</a></li>
<li><a class="external text" href="http://directory.fedoraproject.org/docs/389ds/howto/howto-windowssync.html" rel="nofollow">WinSync Tool</a></li>
<li><a class="external text" href="https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Linux_Domain_Identity_Authentication_and_Policy_Guide/index.html" rel="nofollow">Redhat Docs</a></li>
</ul>
<h1><span id="Layout" class="mw-headline">Layout</span></h1>
<p>Two Internal (10.0.0.0) IPA Masters: ldp01, ldp02</p>
<p>Two AD Controllers: ad01, ad01 (passsync)</p>
<p>In addition to the authentication services, I setup each IPA server to act as an internal <a href="https://en.wikipedia.org/wiki/Domain_Name_System">DNS</a> slave and a <a class="external text" href="http://www.tecmint.com/install-ntp-server-in-centos/" rel="nofollow">NTP</a> Server for their respective zones (internal and commercial/private).</p>
<h1><span id="Client_Installation" class="mw-headline">Client Installation</span></h1>
<p>During the <a class="external text" href="http://linux.die.net/man/1/ipa-client-install" rel="nofollow">ipa-client-install</a> it should configure <a class="external text" href="https://fedorahosted.org/sssd/" rel="nofollow">sssd</a>, <a class="external text" href="http://web.mit.edu/kerberos/" rel="nofollow">kerberos</a>, and <a class="external text" href="http://www.ntp.org/" rel="nofollow">ntp</a>. One must have ntpd already running or it will fail to configure the time service to sync with one of the IPA masters, in addition if the ntpd service was not running and the clock skew is too great the client install will fail. You will have to manually reset the date/time &#8216;]# date -s &#8216;YYYY-MM-DD HH:MM:SS&#8217; &#8216; to then get the install to complete and sync up the clock with the master time servers.</p>
<h2><span id="CentOS_7" class="mw-headline">CentOS 7</span></h2>
<pre> vi /etc/resolv.conf ## has to be pointed at correct DNS machines to 'discover'  
    the IPA machines. 10.0.0.[ldp01], 10.0.0[ldp02] OR if in 10.0.100.0 point to  
    10.0.100.[plp01], 10.0.100.[plp02]
 vi /etc/sysconfig/network-scripts/ifcfg-ens160  #check for DNS settings in 
    interface file
 yum install ipa-client
 ipa-client-install 
 vi /etc/pam.d/system-auth  #check that uid &gt; 500
 vi /etc/pam.d/password-auth # check that uid &gt; 500
# some of our oldest users have uid's less than 1000 which is the standard lowest
  id that pam-sssd will allow to use the sssd.so
 service sssd restart
</pre>
<p>if you are upgrading/changing IPA masters, you will need to do an extra step after ipa-client-install &#8211;uninstall<br />
OR if unable to ssh to server after reinstall: ERROR: Decrypt integrity check failed while handling ap-request armor</p>
<pre> systemctl stop sssd
 rm -f /var/lib/sss/db/* # clears any cache that might be left over.
 ipa-client-install
 systemctl start sssd
</pre>
<h2><span id="CentOS_6" class="mw-headline">CentOS 6</span></h2>
<pre> vi /etc/resolv.conf # add correct freeIPA DNS servers
 ip addr; # check for name of interface usually eth0
 vi /etc/sysconfig/network-scripts/ifcfg-eth0  #check for DNS settings in 
    interface file
 yum install ipa-client
 ipa-client-install --uninstall ##only need to do this if previos IPA install exists
 rm /etc/ipa/ca.crt ###removes old certificate
 ipa-client-install  ## make sure that it has IPA Server: new ipa server.example.com
</pre>
<h3><span id=".28Alt.29_sssd-ldap" class="mw-headline">(Alt) sssd-ldap</span></h3>
<p>In some systems, mostly CentOS 6.4 we had to change from using ipa-client(sssd-ipa) to using sssd-ldap to interact with out IPA servers, this was mostly due to high traffic and the ipa-client struggling with caching. One should not have to set many machines up like this.</p>
<p>/etc/sssd/sssd.conf</p>
<pre>[domain/default]

ldap_id_use_start_tls = False
ldap_tls_reqcert = never
cache_credentials = True
ldap_search_base = cn=accounts,dc=example,dc=com
krb5_realm = EXAMPLE.COM
krb5_server = ldp01.example.com:88
id_provider = ldap
auth_provider = ldap
chpass_provider = ldap
ldap_schema = rfc2307bis
ldap_group_member = member
ldap_uri = ldaps://ldp02.example.com,ldaps://ldp01.example.com
ldap_tls_cacertdir = /etc/openldap/cacerts
entry_cache_timeout = 600
ldap_network_timeout = 3
ldap_access_filter = (&amp;(object)(object))
</pre>
<h2><span id="CentOS_5" class="mw-headline">CentOS 5</span></h2>
<pre>  cat /etc/redhat-release # find version of CentOS
  vi /etc/resolv.conf # change DNS to 10.0.0.[ldp01] and 10.0.0.[ldp02]
  ip addr; #check for name of interface usually eth0
  vi /etc/sysconfig/network-scripts/ifcfg-eth0  #check for DNS settings in interface file
  ps fax ; #check for either sssd or nscd
</pre>
<h3><span id="If_nscd" class="mw-headline">If nscd</span></h3>
<pre>  ps fax | grep nscd;
  vi /etc/ldap.conf #make sure settings match below
</pre>
<pre>base cn=compat,dc=example,dc=com
ldap_version 3
nss_base_passwd cn=users,cn=accounts,dc=example,dc=com?sub
nss_base_group cn=groups,cn=compat,dc=example,dc=com?sub
nss_map_attribute uniqueMember member
nss_schema rfc2307bis
nss_srv_domain example.com

uri ldap://ldp01.example.com

ssl no
tls_cacertdir /etc/openldap/cacerts
pam_password md5

</pre>
<pre> service nscd restart
 #attempt login
 nscd --invalidate=group #clears group <a class="external text" href="https://stijn.tintel.eu/blog/2012/05/10/how-to-really-flush-the-various-nscd-caches" rel="nofollow">cache</a>
 # if you have trouble logging in check /etc/nsswitch.conf and make sure it is 
   formatted to check 'passwd: files ldap' for gorups, sudoers, netgroups, 
   services and others.
</pre>
<h3><span id="if_sssd" class="mw-headline">if sssd</span></h3>
<pre> ###change DNS
 ps fax | grep sssd; 
 ipa-client-install --uninstall
 rm /etc/ipa/ca.crt ###removes old certificate
 ipa-client-install  ## make sure that it has IPA Server: new ipa server.example.com
</pre>
<h1><span id="Server_Installation" class="mw-headline">Server Installation</span></h1>
<p>CentOS 7, IPAv4</p>
<p>On First Master(ldp01):</p>
<pre> yum install ipa-server bind bind-dyndb-ldap
 ipa-server-install --forwarder=8.8.8.8 --forwarder=216.97.160.5 --setup-dns 
    --no-ntp -a admin_password -n example.com -p DM_password -r EXAMPLE.COM -P 
    DM_password
</pre>
<pre>Global DNS configuration in LDAP server is empty
You can use 'dnsconfig-mod' command to set global DNS options that
would override settings in local named.conf files
...
Restarting the web server
==============================================================================
Setup complete

Next steps:
        1. You must make sure these network ports are open:
                TCP Ports:
                  * 80, 443: HTTP/HTTPS
                  * 389, 636: LDAP/LDAPS
                  * 88, 464: kerberos
                  * 53: bind
                UDP Ports:
                  * 88, 464: kerberos
                  * 53: bind

        2. You can now obtain a kerberos ticket using the command: 'kinit admin'
           This ticket will allow you to use the IPA tools (e.g., ipa user-add)
           and the web user interface.
        3. Kerberos requires time synchronization between clients
           and servers for correct operation. You should consider enabling ntpd.

Be sure to back up the CA certificate stored in /root/cacert.p12
This file is required to create replicas. The password for this
file is the Directory Manager password
</pre>
<p>Setup IP Tables:</p>
<pre> iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
 iptables -A INPUT -p icmp -j ACCEPT
 iptables -A INPUT -i lo -j ACCEPT
 iptables -A INPUT -m conntrack --ctstate NEW -m tcp -p tcp --dport 22 -j ACCEPT
 iptables -A INPUT -p tcp -m multiport --dports 80,443,389,636,88,464,53,138,139,445,7389 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
 iptables -A INPUT -p udp -m multiport --dports 88,464,53,123,138,139,389,445,7389 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
 iptables -A INPUT -p udp -j REJECT
 iptables -A INPUT -p tcp -j REJECT
 iptables -A FORWARD -j REJECT --reject-with icmp-host-prohibited
</pre>
<h3>Setup DNS:</h3>
<pre>  /usr/sbin/rndc-confgen -a
  /sbin/restorecon /etc/rndc.key
  chown root:named /etc/rndc.key
  chmod 0640 /etc/rndc.key
  vim /etc/named.conf
  vim /etc/rndc.key  # copy this info into top of the /etc/named.conf
  vim /etc/named.conf
     scp slaves.conf and named.ad.zones from other DNS server, add IP ADDR to master named.conf
  see the official /etc/named.conf at the bottom of the page
  named-checkconf /etc/named.conf
  systemctl restart named
  Test:
     dig SRV _kerberos._tcp.example.com  # should return authoritative answer 
     from ldp01 and ldp02
</pre>
<h3>Setup Replication with other IPA master(ldp02):</h3>
<pre> On ldp01:
   ipa config-mod --enable-migration=True
   ipa-replica-prepare ldp02.example.com --ip-address 10.0.0.[ldp02]
   scp /var/lib/ipa/replica-info-ldp02.example.com.gpg ldp02:/var/lib/ipa
   ssh ldp02
</pre>
<pre> On ldp02:
   yum install ipa-server bind bind-dyndb-ldap
   #configure iptables with same settings as above
   ipa-replica-install --setup-dns --forwarder=8.8.8.8 --forwarder=216.97.160.5 
       /var/lib/ipa/replica-info-ldp02.example.com.gpg
   ipa-replica-manage list
     ldp01.example.com: master
     ldp02.example.com: master
</pre>
<p>Migrate from old LDAP/IPA</p>
<pre> On Master:
   kinit admin
   ipa config-mod --enable-migration=True
   echo DM_password | ipa migrate-ds --bind-dn="cn=Directory Manager" --user-container=cn=users,cn=accounts  --group-container="cn=groups,cn=accounts" --base-dn="dc=example,dc=com" --schema=RFC2307bis --group-objectclass=posixgroup  --user-ignore-attribute={krbPrincipalName,krbextradata,krblastfailedauth,krblastpwdchange,krblastsuccessfulauth,krbloginfailedcount,krbpasswordexpiration,krbticketflags,krbpwdpolicyreference} --with-compat ldap://10.0.0.[oldldp]
  # this removes the old kerberos stuff so the passwords will migrate,
  # you can then send people to https://ldp01.example.com/ipa/migration/ to 
    re-enter their credentials to complete the migration
</pre>
<h3>Setup Sync with Active Directory</h3>
<pre> On AD Server:
  Follow these <a class="external text" href="https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Windows_Integration_Guide/managing-sync-agmt.html" rel="nofollow">Directions</a>
  Download and import ca.crt to certificate server(ad01 and ad02): http://ldp01.example.com/ipa/config/ca.crt
  export Example-CA.crt and copy it to ldp01:/root/Example-ca.crt
  
 On ldp01:
  mkdir /etc/openldap/cacerts
  vim /etc/openldap/ldap.conf
    - TLS_CACERTDIR /etc/openldap/certs/
    + TLS_CACERTDIR /etc/openldap/cacerts/
    + TLS_REQCERT allow
  cp /root/ZX-ca.crt /etc/openldap/cacerts/
  cp /etc/ipa/ca..crt /etc/openldap/cacerts/
  cacertdir_rehash /etc/openldap/cacerts/
  kdestroy
 ipa-replica-manage connect --winsync --binddn 
    "cn=IPA Synchronization,OU=Systems,dc=example,dc=com" --bindpw ipaSync_passwd
    --passsync Passsync_password --cacert /root/Example-ca.cer --win-subtree 
    "ou=Systems,dc=example,dc=com" ad01.example.com -v
 # it will ask for the credentials of the Directory Manager
    Added CA certificate /etc/openldap/cacerts/Example-ca.crt to certificate database for ldp01.example.com
    ipa: INFO: AD Suffix is: DC=example,DC=com
    The user for the Windows PassSync service is uid=passsync,cn=sysaccounts,cn=etc,dc=example,dc=com
    Windows PassSync system account exists, not resetting password
    ipa: INFO: Added new sync agreement, waiting for it to become ready . . .
    ipa: INFO: Replication Update in progress: FALSE: status: -11  - LDAP error: Connect error: start: 0: end: 0
    ipa: INFO: Agreement is ready, starting replication . . .
    Starting replication, please wait until this has completed.
  ipa-replica-manage list
    ldp01.example.com: master
    ldp02.example.com: master
    ad01.example.com: winsync
   #repeat for the other AD Server
   ipa-replica-manage connect --winsync --binddn "cn=IPA Synchronization,OU=Systems,dc=example,dc=com" 
       --bindpw ipaSync_passwd --passsync Passsync_password --cacert 
       /root/Example-ca.cer --win-subtree "ou=Systems,dc=example,dc=com" 
       ad02.example.com -v
  scp /root/Example-ca.crt ad02:/root
  ssh ad02:
</pre>
<pre> On ldp02:
   mkdir /etc/openldap/cacerts
   vim /etc/openldap/ldap.conf
    - TLS_CACERTDIR /etc/openldap/certs/
    + TLS_CACERTDIR /etc/openldap/cacerts/
    + TLS_REQCERT allow
   cp /root/Example-ca.crt /etc/openldap/cacerts/
   cp /etc/ipa/ca..crt /etc/openldap/cacerts/
   cacertdir_rehash /etc/openldap/cacerts/
   ipa-replica-manage list
     ad02.example.com: winsync
     ldp02.example.com: master
     ldp01.example.com: master
     as01.example.com: winsync
</pre>
<h3>Setup Passsync on BOTH AD Servers:</h3>
<p>Be sure to enable &#8220;Protected object&#8221; on each AD user you test on. I once completely erased my profile from existence with passsync.</p>
<pre>  Download Latest version of <a class="external text" href="http://directory.fedoraproject.org/docs/389ds/download.html" rel="nofollow">389-PassSync</a>
  Install msi
  use these parameters:
     Host Name: ldp01.example.com
     port: 636
     User Name: uid=passsync,cn=sysaccounts,cn=etc,dc=example,dc=com
     password: Passsync_password
     Search Base: cn=users,cn=accounts,dc=example,dc=com
  copy IPA ca.crt to "C:\Program Files\389 Directory Password Synchronization"
  Open CMD as Administrator
  cd "C:\Program Files\389 Directory Password Synchronization"
  certutil.exe -d . -A -n "ldp01.exa,[;e.com IPA CA" -t "CT,," -a -i ca.crt
  open services.msc and force start Passsync Service
  check C:\Program Files\389 Directory Password Synchronization\passsync.log for 
    any errors
  <b>TEST!</b> Try changing a password in AD and seeing if that change is reflected by 
      signing in as the user to the IPA web service.
</pre>
<h1><span id="DEBUG" class="mw-headline">DEBUG</span></h1>
<p>The following are ways to test that communication is working if one gets stuck.</p>
<pre> ldp02 ~]# LDAPTLS_CACERTDIR=/etc/openldap/cacerts ldapsearch -xLLL -ZZ -h 
     ad01.example.com -D "cn=IPA Synchronization,OU=Systems,dc=example,dc=com" 
     -w Admin_PW -b cn=Systems,dc=example,dc=com
 #repeat the same action from ldp01, this is how I discovered that ldp02 did not 
  have the ZX-ca.crt that was needed to verify connections to the AD servers.
</pre>
<pre> as01: Turn on debug for Passync 
 Open regedit, HKEY_LOCAL_MACHINE\SOFTWARE\PasswordSync and change debug from 
    0 - 1
 use ldp.exe to verify that connections over SSL/636 to IPA servers work.
</pre>
<p>&nbsp;</p>
<h1><span id="named.conf" class="mw-headline">named.conf</span></h1>
<p>This config should be the same on ldp01 and ldp02, if you want them to also host DNS. One must allow them to transfer DNS updates to each other. Sample ldp01 named.conf  below</p>
<pre>key "rndc-key" {
        algorithm hmac-md5;
        secret "************************";
};


controls {
        inet 127.0.0.1 allow { localhost; }
        keys { rndc-key; };
};



options {
        // turns on IPv6 for port 53, IPv4 is on by default for all ifaces
        listen-on-v6 {any;};

        // Put files that named is allowed to write in the data/ directory:
        directory "/var/named"; // the default
        dump-file               "data/cache_dump.db";
        statistics-file         "data/named_stats.txt";
        memstatistics-file      "data/named_mem_stats.txt";

        forward first;
        forwarders {
                8.8.8.8;
                216.97.160.5;
                166.102.165.13;
                166.102.165.11;
        };

        // Any host is permitted to issue recursive queries
        allow-recursion { any; };

        tkey-gssapi-keytab "/etc/named.keytab";
        pid-file "/run/named/named.pid";

        dnssec-enable yes;
        dnssec-validation no;

        /* Path to ISC DLV key */
        bindkeys-file "/etc/named.iscdlv.key";

        managed-keys-directory "/var/named/dynamic";

        tkey-gssapi-credential "DNS/ldp01.example.com";
        tkey-domain "EXAMPLE.COM";

};

/* If you want to enable debugging, eg. using the 'rndc trace' command,
 * By default, SELinux policy does not allow named to modify the /var/named directory,
 * so put the default debug log file in data/ :
 */
logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
                print-time yes;
        };
};

zone "." IN {
        type hint;
        file "named.ca";
};

zone "_tcp.example.com" {
        type master;
        file "zones/_tcp.example.com";
        allow-transfer { 10.0.0.[ldp02]; };
};

zone "_udp.example.com" {
        type master;
        file "zones/_udp.example.com";
        allow-transfer { 10.0.0.[ldp02]; };
};

zone "_kerberos.example.com" {
        type master;
        file "zones/_kerberos.example.com";
        allow-transfer { 10.0.0.[ldp02]; };
};


include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
include "slaves.conf";
include "named.ad.zones";

dynamic-db "ipa" {
        library "ldap.so";
        arg "uri ldapi://%2fvar%2frun%2fslapd-EXAMPLE-COM.socket";
        arg "base cn=dns, dc=example,dc=com";
        arg "fake_mname ldp01.example.com.";
        arg "auth_method sasl";
        arg "sasl_mech GSSAPI";
        arg "sasl_user DNS/ldp01.example.com";
        arg "serial_autoincrement yes";
};
</pre>
<p>&nbsp;</p>
<hr />
</div>