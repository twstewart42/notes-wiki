find date range

find . -type f -newer translate_list_fctmos.pl ! -newer shd-gz/  -delete

find / -iname "*.mp3" -exec mv {} /mnt/mp3 \; -- it made everything a sticky bit after the move i had to chmod 664 for all teh data in both directories

(1:09:38 PM) Eric Tomeo: http://www.cyberciti.biz/tips/howto-linux-unix-find-move-all-mp3-file.html

find . -type f -newer translate_list_fctmos.pl ! -newer shd-gz/  -exec mv "{}" brokenfiles/ \;


find . -type f -newer translate_list_fctmos.pl ! -newer shd-gz/ -exec ls -l {} \; -print > output.txt to make sure I got the correct range of data | greped for earliest date and latest date


find . -type f -mmin +720 -delete  -- find and delete anyting over 12 hours old
find . ! -name '*Epoch' -type f -mmin +720 -delete -- find but ignore anything with the word Epoch

List number of files in directory
ls -R | wc -l 

From <http://www.unix.com/unix-for-dummies-questions-and-answers/19164-count-number-files-subdirectories.html> 


Example
Ls 
??????  ?2??:  201412  201501  201502  ?6????  ?GA???  Pw?  ???q??  ?rw???

#get inode number
[root@ppa03 CFSRR]# ls -li
total 44
205760 drwxrwxr-x  3 magej128 magej128 4096 Feb  3 08:43 ??????
 39396 drwxrwxr-x  4 magej128 magej128 4096 Feb  3 08:38 ?2??:
170122 drwxrwsr-x 63 ldm      ldm      8192 Feb  5 03:23 201412
454370 drwxrwsr-x 14 ldm      ldm      4096 Feb  5 05:45 201501
454375 drwxrwsr-x  3 ldm      ldm      4096 Feb  3 06:28 201502
452461 drwxrwxr-x  3 magej128 magej128 4096 Feb  3 08:43 ?6????
454356 drwxrwxr-x  9 ldm      ldm      4096 Feb  2 06:44 ?GA???
 91892 drwxrwxr-x  3 magej128 magej128 4096 Feb  3 08:49 Pw?
205777 drwxrwxr-x  3 magej128 magej128 4096 Feb  3 08:46 ???q??
  8818 drwxrwxr-x  3 magej128 magej128 4096 Feb  3 08:57 ?rw???

find . -inum 205760 -exec rm -rf {} \;
Find .inum #### -delete


[root@yslog001 sssd]# lsof -i :514
COMMAND   PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
rsyslogd 4835 root    1u  IPv4 3354631      0t0  TCP *:shell (LISTEN)
rsyslogd 4835 root    2u  IPv6 3354632      0t0  TCP *:shell (LISTEN)
rsyslogd 4835 root    3u  IPv4 3354623      0t0  UDP *:syslog
rsyslogd 4835 root    4u  IPv6 3354624      0t0  UDP *:syslog



Just change the port number and you can find if the dameon is listening on the correct port




 netstat -antu | grep 514 ; will show all tcp and udp listening on the specific interface

netstat -anetu | grep 514; adding the e ads established connections
tcp        0      0 0.0.0.0:514                 0.0.0.0:*                   LISTEN
tcp        0      0 :::514                      :::*                        LISTEN
tcp        0      0 :::5514                     :::*                        LISTEN
tcp        0      0 ::ffff:127.0.0.1:44946      ::ffff:127.0.0.1:9300       ESTABLISHED 497        3320514
udp        0      0 0.0.0.0:514                 0.0.0.0:*                       
udp        0      0 :::514                      :::*                            
udp        0      0 :::5514                     :::*       
