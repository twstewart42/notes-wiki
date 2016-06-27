#SELinux 

http://wiki.centos.org/TipsAndTricks/SelinuxBooleans
http://docs.fedoraproject.org/en-US/Fedora/11/html/Security-Enhanced_Linux/sect-Security-Enhanced_Linux-SELinux_Contexts_Labeling_Files-Persistent_Changes_semanage_fcontext.html


  $ setsebool -P httpd_use_nfs on

  $ ls -Z -rw-r-----. named named system_u:object_r:named_zone_t:s0 example.com httpd_log_t

  $ yum install policycoreutils-python

  $ /usr/sbin/semanage fcontext -a -t httpd_log_t "/var/log/gis(/.*)?"
  $ /sbin/restorecon -R -v /var/log/gis

  $ setsebool -P selinuxuser_mysql_connect_enabled on
  $ setsebool -P selinuxuser_postgresql_connect_enabled on
  $ setsebool -P httpd_can_network_connect_db on
  $ setsebool -P httpd_can_network_connect on

  $ httpd_sys_script_exec_t



usr/sbin/semanage fcontext -a -t httpd_sys_content_t /web

From <http://docs.fedoraproject.org/en-US/Fedora/11/html/Security-Enhanced_Linux/sect-Security-Enhanced_Linux-SELinux_Contexts_Labeling_Files-Persistent_Changes_semanage_fcontext.html> 


