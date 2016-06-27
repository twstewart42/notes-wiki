Vim /etc/mail/sendmail.mc


MASQUERADE_AS(example.com)dnl
FEATURE(masquerade_envelope)dnl
FEATURE(masquerade_entire_domain)dnl
FEATURE(allmasquerade)dnl


m4 /etc/mail/sendmail.mc > /etc/mail/sendmail.cf

Systemctl restart sendmail

wget http://rpm.zedxinc.com/CentOS/5/os/x86_64/CentOS/sendmail-cf-8.13.8-8.1.el5_7.x86_64.rpm
 rpm -Uvh sendmail-cf-8.13.8-8.1.el5_7.x86_64.rpm
 vi /etc/mail/mailertable
  + zedxinc.com     esmtp:[10.0.5.110]
 makemap hash /etc/mail/mailertable.db < /etc/mail/mailertable
 vim /etc/mail/sendmail.mc
  #edit like above section
 m4 /etc/mail/sendmail.mc > /etc/mail/sendmail.cf
 make -C /etc/mail
 service sendmail restart