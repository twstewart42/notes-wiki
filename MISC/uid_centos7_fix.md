If users say they are getting access denied errors from centos7 machine you need to do the following

Error: /var/log/secure
pam_succeed_if(sshd:auth): requirement "uid >= 1000" not met by user "user123"


Cd /etc/pam.d
Vim system-auth | edit line to allow > 500 uid

Vim password-auth with the same


