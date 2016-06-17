I wrote this wiki for my interns and junior admins as a quick overview of simple things to check and use when they encountered an issue.

&nbsp;
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<h1><span id="Bash.2FShell_Scripting" class="mw-headline"><a href="https://twstewart84.wordpress.com/systems-administration/bash/">Bash</a>/Shell Scripting</span></h1>
<a class="external text" href="http://linux.die.net/man/1/bash" rel="nofollow">Bash</a> scripting is the bread and butter of systems administration. Too often we have to repeat a set of commands across many machines, and the goal of everyone should be to complete that goal with as much automation as possible. Any command that you can type on the CMD line is valid in bash scripting along with basic <a class="external text" href="http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-6.html" rel="nofollow">if</a>/elif/<a class="external text" href="http://tldp.org/LDP/Bash-Beginners-Guide/html/sect_07_01.html" rel="nofollow">else</a> logic, <a class="external text" href="http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-7.html" rel="nofollow">for loops</a>, variable substitution, and <a class="external text" href="http://tldp.org/LDP/abs/html/arithexp.html" rel="nofollow">mathematical expressions</a>.
<pre> #!/bin/sh
</pre>
<a class="extiw" title="wikipedia:Bash (Unix shell)" href="http://en.wikipedia.org/wiki/Bash_(Unix_shell)">Wikipedia:Bash (Unix shell)</a>
<h1><span id="Man_Pages" class="mw-headline">Man Pages</span></h1>
If you are ever unsure of what a command does man pages are the way to locally read and understand how to use any command in Linux. It is literally the command's <a class="external text" href="http://linux.die.net/man/" rel="nofollow">manual</a> in text format.
<pre>  ~]# man ifconfig
 IFCONFIG(8)                Linux Programmer’s Manual               IFCONFIG(8)
 
 NAME
        ifconfig - configure a network interface
 
 SYNOPSIS
        ifconfig [interface]
        ifconfig interface [aftype] options | address ...
 
 DESCRIPTION
        Ifconfig  is  used to configure the kernel-resident network interfaces.
        It is used at boot time to set up interfaces as necessary.  After that,
        it  is  usually  only  needed  when  debugging or when system tuning is
        needed.
 
        If no arguments are given, ifconfig displays the  status  of  the  cur-
        rently  active interfaces.  If a single interface argument is given, it
        displays the status of the given interface only; if a single  -a  argu- 
        ment  is  given,  it  displays the status of all interfaces, even those
        that are down.  Otherwise, it configures an interface.
  <b>there is much more to this document in full</b>
</pre>
<h1><span id=".2Fvar.2Flog.2Fmessages" class="mw-headline">/var/log/messages</span></h1>
/var/log/messages is the default catch-all for any system errors that may be occurring. There are sometimes logs setup for specific services. Always try to see if a specific service has its own log file or directory (httpd,cron,secure,php-fpm,mysql,postgresql) and if it does not exist or is empty, check /var/log/messages it will probably have the errors, warning, INFO, emergencies, kernel panics, and any other frightening logs that you need to resolve any issues that may occur.

If you have checked both the service log and /var/log/messages and still cannot find any information about the service you are trying to fix, you may have to enable debugging mode(s) or level(s) on the service itself. This is different for all services and can usually be found in the products documentation.
<h1><span id="Basic_Machine_Info" class="mw-headline">Basic Machine Info</span></h1>
The following is a collection of commands and their result to gather basic information about the machine.
<pre> #] uname -a; -- shows name, kernel # and date of build
 Linux devsql005.example.com 3.10.0-123.8.1.el7.x86_64 #1 SMP Mon Sep 22 19:06:58 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux
 #] cat /etc/hostname; -- edit this file to change host name
devsql005.example.com
 #] env | grep HOSTNAME
 HOSTNAME=devsql005.example.com
 #] export HOSTNAME=devsql005.example.com; -- to set new host name for machine
</pre>
<pre> #] cat /etc/redhat-release; -- shows official CentOS/Redhat version number
  CentOS Linux release 7.0.1406 (Core)
</pre>
<pre> #] ip addr; -- alternative to ifconfig, ifconfig is becoming depreciated in CentOS 7, but this can be used as far back as CentOS 5
 1: lo: &lt;LOOPBACK,UP,LOWER_UP&gt; mtu 65536 qdisc noqueue state UNKNOWN
     link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
     inet 127.0.0.1/8 scope host lo
        valid_lft forever preferred_lft forever
     inet6 ::1/128 scope host
        valid_lft forever preferred_lft forever
 2: ens160: &lt;BROADCAST,MULTICAST,UP,LOWER_UP&gt; mtu 1500 qdisc mq state UP qlen 1000
     link/ether 00:50:56:84:59:79 brd ff:ff:ff:ff:ff:ff
     inet 10.0.0.[?]/24 brd 10.0.0.255 scope global ens160
        valid_lft forever preferred_lft forever
     inet6 fe80::250:56ff:fe84:5979/64 scope link
        valid_lft forever preferred_lft forever
</pre>
<pre> #] ifconfig;
 ens160: flags=4163&lt;UP,BROADCAST,RUNNING,MULTICAST&gt;  mtu 1500
         inet 10.0.0.[?]  netmask 255.255.255.0  broadcast 10.0.50.255
         inet6 fe80::250:56ff:fe84:5979  prefixlen 64  scopeid 0x20&lt;link&gt;
         ether 00:50:56:84:59:79  txqueuelen 1000  (Ethernet)
         RX packets 1675151509  bytes 296413707167 (276.0 GiB)
         RX errors 0  dropped 235945  overruns 0  frame 0
         TX packets 1428044385  bytes 471991954342 (439.5 GiB)
         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
 
 lo: flags=73&lt;UP,LOOPBACK,RUNNING&gt;  mtu 65536
         inet 127.0.0.1  netmask 255.0.0.0
         inet6 ::1  prefixlen 128  scopeid 0x10&lt;host&gt;
         loop  txqueuelen 0  (Local Loopback)
         RX packets 409040766  bytes 330694444196 (307.9 GiB)
         RX errors 0  dropped 0  overruns 0  frame 0
         TX packets 409040766  bytes 330694444196 (307.9 GiB)
         TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
</pre>
<pre> #]pwd;  -- shows the directory you are in
  /var/lib/pgsql/9.3/data
</pre>
<pre> #]cat /etc/passwd;  -- shows local users
 root:x:0:0:root:/root:/bin/bash
 bin:x:1:1:bin:/bin:/sbin/nologin
 daemon:x:2:2:daemon:/sbin:/sbin/nologin
 adm:x:3:4:adm:/var/adm:/sbin/nologin
 lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
 sync:x:5:0:sync:/sbin:/bin/sync
 shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
 halt:x:7:0:halt:/sbin:/sbin/halt
 mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
 ....
</pre>
<pre> #] cat /etc/group;  -- shows local groups
 root:x:0:
 bin:x:1:
 daemon:x:2:
 sys:x:3:
 adm:x:4:
 tty:x:5:
 disk:x:6:
 ....
</pre>
<pre> #] groups apache;  -- shows which groups the user 'apache' is in
 apache : apache cfdev agproduction service_accounts ravendev agdev agdevelopment zxdev zxprod
</pre>
<pre> #] chkconfig --list;  -- shows the boot rc.# level and order CentOS 5 &amp; 6.
 abrt-ccpp       0:off   1:off   2:off   3:on    4:off   5:on    6:off
 abrt-oops       0:off   1:off   2:off   3:on    4:off   5:on    6:off
 abrtd           0:off   1:off   2:off   3:on    4:off   5:on    6:off
 acpid           0:off   1:off   2:on    3:on    4:on    5:on    6:off
 atd             0:off   1:off   2:off   3:on    4:on    5:on    6:off
 auditd          0:off   1:off   2:on    3:on    4:on    5:on    6:off
 autofs          0:off   1:off   2:off   3:on    4:on    5:on    6:off
 blk-availability        0:off   1:on    2:on    3:on    4:on    5:on    6:off
 certmonger      0:off   1:off   2:on    3:on    4:on    5:on    6:off
 cfengine3       0:off   1:off   2:on    3:on    4:on    5:on    6:off
</pre>
&nbsp;
<pre> #] systemctl is-enabled sshd; --In CentOS 7 services must be enabled to start at bootup, is-enabled checks if the service is enabled
 enabled
</pre>
<h1><span id="grep.2Fawk.2Fsed" class="mw-headline">grep/awk/sed</span><span class="mw-editsection"><span class="mw-editsection-bracket">=</span></span></h1>
Learn these three tools, they are the swiss army knife to the system's administrator's war chest. They can be used to do most anything and you will see many example combinations and use cases in the sections below.

You can be like captain planet and when you combine the power of all three of these tools you can create very powerful and flexible scripts that do all the heavy lifting for you.
<h2><span id="grep" class="mw-headline">grep</span><span class="mw-editsection"><span class="mw-editsection-bracket">=</span></span></h2>
<a class="external text" href="http://linux.die.net/man/1/grep" rel="nofollow">grep</a> is a tool mainly used for searching or weeding out information.
<pre> #] grep mysql ;-- will search the entire directory tree and every file in those directories for lines containing the word mysql
 #] cat /var/log/maillog | grep username@mail.com; -- will search the 100,000 line long log file for any line that matches username@mail.com
 #] grep username@mail.com /var/log/maillog; -- alternate way to search maillog for usernam@mail.com
</pre>
<a class="extiw" title="wikipedia:Grep" href="http://en.wikipedia.org/wiki/Grep">Wikipedia:Grep</a>
<h2><span id="awk" class="mw-headline">awk</span></h2>
I generally use <a class="external text" href="http://linux.die.net/man/1/awk" rel="nofollow">awk</a> piped at the end of a command to only print specific parts of the returned information. But awk is it's own programming language and can be just as powerful as perl or any other scripting language.
<pre>#]df -h -t nfs -P | grep /vol/ |  awk '{ print $5 " " $6}'; --df -h 
   gives me a listing of the mounts, I search for /vol/ to get mounted drives, 
   then I awk for result $5 and $6 of each returned line which is always used percentage and the partition that is in question.
#]grep "request ID" history | awk 'match($0,"is"){print substr($0,RSTART+3,50)}'`; 
  this searches for "request ID" in a file called history and 
  awk looks for the word "is" then prints 50 characters, 3 characters after "is", which is always the request ID in this example. I made this to get
  the singularity request ID for processes so that I could remove them from the queue. Below we use the result of the Request ID grep and awk 
  statement and apply some logic checking to see if it succeeded or not.
</pre>
<a class="extiw" title="wikipedia:AWK" href="http://en.wikipedia.org/wiki/AWK">Wikipedia:AWK</a>
<h2><span id="sed" class="mw-headline">sed</span></h2>
<a class="external text" href="http://linux.die.net/man/1/sed" rel="nofollow">sed</a> is used for inline text editing and <a class="external text" href="http://sed.sourceforge.net/sed1line.txt" rel="nofollow">manipulation</a>.
<pre>#]sed -n 51,61p sbr/index.html | sed -i '50r /dev/stdin' testsed; --this takes lines 51-61 of index.html and appends them after line 50 in testsed
 
#]IP=`nslookup $HOSTNAME | grep Address | grep -v "#53"| awk '{ print $2}'`; -looks up hostname using DNS and greps for address, ignores anything with #53, 
   prints second value on returned line
   echo "$IP"
   cat /etc/monitrc | grep 0.0.0.0 | sed -i 's/0.0.0.0/'$IP'/g' /etc/monitrc; - reads file, greps for 0.0.0.0, then replaces 0.0.0.0 with result of $IP in script.
</pre>
<h3><span id="CPU_TEMPS_for_physical_servers" class="mw-headline">CPU TEMPS for physical servers</span></h3>
<pre>#]  __=`sensors | grep Core` &amp;&amp; echo \(`echo $__ | sed 's/.*+\(.*\).C\(\s\)\+(.*/\1/g' | tr "\n" "+" | head -c-1`\)\/`echo $__ | wc -l` | bc &amp;&amp; unset __
</pre>
<h3><span id="CBSG" class="mw-headline"><a class="external text" href="http://www.bashoneliners.com/oneliners/oneliner/popular/" rel="nofollow">CBSG</a></span></h3>
<pre>#]curl -s http://cbsg.sourceforge.net/cgi-bin/live | grep -Eo '^&lt;li&gt;.*&lt;/li&gt;' | sed s,\&lt;/\\?li\&gt;,,g | shuf -n 1
</pre>
<a class="extiw" title="wikipedia:Sed" href="http://en.wikipedia.org/wiki/Sed">Wikipedia:Sed</a>
<h1><span id="Disk_is_full" class="mw-headline">Disk is full</span></h1>
The following are commands and explanation of the many things you can do to find and remove large log/temporary files, unusual file names, and similar scenarios.

Below is a list of the most likely to be filled areas and should be the first place(s) one looks for space that can be reclaimed
<ol>
	<li>/var/log</li>
	<li>/var/spool/{clientmqueue,mqueue,mail}</li>
	<li>/var/cfengine/cf.hostname.logfile</li>
	<li>/tmp</li>
	<li>/var/tmp</li>
	<li>/var/lib/pgsql - look for old .sql exports and pg-startuplog</li>
	<li>Sometimes long-running endless loops in our scripts will fill up "virtual" file space and will appear invisible to the file system (bfeprdapp004); ps fax; -- look for time signatures above 1000 cpu seconds, not always the case, use proper judgment</li>
	<li>large snapshot (Netapp) -- this will be hidden from users and will only be effecting mounts that mysteriously fill up.</li>
</ol>
<h2><span id="df" class="mw-headline">df</span></h2>
<a class="external text" href="http://linux.die.net/man/1/df" rel="nofollow">df</a> -h; shows one the local and mounted filesystems and the amount of space, used vs available.
<pre> ~]#df -h
 Filesystem                              Size  Used Avail Use% Mounted on
 /dev/sda3                                12G  4.9G  6.7G  43% /
 /dev/sda1                               497M  115M  383M  24% /boot
 10.10.0.248:/vol/carp/home              1.9T  1.2T  628G  66% /nfs/carp/home
 vortex:/var/lib/wx/sat                  9.6T  8.4T  1.2T  88% /nfs/vortex/wx/sat
 blizzard:/var/lib/data/qtrdeg/          4.4T  3.2T  1.3T  72% /nfs/blizzard/qtrdeg
 pandora:/var/lib/data/projects/CFSR      13T  8.6T  4.2T  68% /nfs/pandora/CFSR
 10.10.0.247:/vol/wxsan2/data            6.0T  5.4T  713G  89% /wxsan2/data
 10.10.0.245:/vol/wxgrid/data/cimis      8.5T  4.9T  3.7T  58% /wxgrid/data/cimis
 tornado:/var/lib/wx/rtma                 14T   13T  988G  93% /nfs/tornado/rtma
 10.10.0.237:/vol/wxrequestapi/dev       9.5G   61M  9.5G   1% /var/www/wxrequestapi
</pre>
<h2><span id="du" class="mw-headline">du</span></h2>
<a class="external text" href="http://linux.die.net/man/1/du" rel="nofollow">du</a> -sh /var/log/; will count the size of each file within a directory and total it.
<pre> ]# du -sh /var/log
 113M    /var/log
</pre>
<h2><span id="ncdu" class="mw-headline">ncdu</span></h2>
<a class="external text" href="http://dev.yorhel.nl/ncdu/man" rel="nofollow">ncdu</a> is a non-standard tool, but can be installed via yum and available via the CentOS repos, and is like a visual du -sh and it allows you to navigate through directories and remove files directly.
<pre> #] ncdu /var/log;
</pre>
<h2><span id="Clearing_large_Log_files" class="mw-headline">Clearing large Log files</span></h2>
Do not just rm -rf logfile; if a process, say apache, is still writing to the logfile and you remove the file from existence the process will crash. Remember we wish to have an uptime of 24/7/365. Instead you can clear out the file to size 0 and allows the process to continue writing to it.
<pre> ]# cat /dev/null &gt; /var/log/messages
</pre>
<h2><span id="No_Space_to_Delete" class="mw-headline">No Space to Delete</span></h2>
Rarely but it does happen a volume will fill up and be so full that rm will not work as it creates temporary records while it deletes files. There is another way to delete the file by finding it's inode number and using find to delete the file
<pre>#let's assume you did all steps above and found the large offending file.
]# rm /var/tmp/3a8066e5-a90c-4ae5-bdc6-47e117acf354.error
 rm: remove regular file ‘/var/tmp/3a8066e5-a90c-4ae5-bdc6-47e117acf354.error’? y
 rm: cannot remove ‘/var/tmp/3a8066e5-a90c-4ae5-bdc6-47e117acf354.error’: No space left on device
]# ls -li /var/tmp/3a8066e5-a90c-4ae5-bdc6-47e117acf354.error
 56436168 -rw-r--r-- 1 gerbn308 zxdev 0 May 13 11:17 /var/tmp/3a8066e5-a90c-4ae5-bdc6-47e117acf354.error
]# find . -inum 56436168 -delete
</pre>
<h2><span id="find" class="mw-headline">find</span></h2>
<a class="external text" href="http://man7.org/linux/man-pages/man1/find.1.html" rel="nofollow">Find</a> is really really useful and below are some of the ways find has solved strange issues for me
<h3><span id="find_date_range" class="mw-headline">find date range</span></h3>
This use case happened once with jay's shd-chd data. We download data from mesos, which then gets processed and spits out files which are named for the station reporting. They can have any amount of numbers and letters to identify them. but we needed to go back, download missed files and reprocess everything. to do this we had to clear our "bad" processed data and start over. You can clear out data using the <a class="external text" href="http://www.binarytides.com/linux-find-command-examples/" rel="nofollow">find command</a> and a time/date range between two files.
<pre> #] ll -tr;   - will list out files in time/date order newest -&gt; oldest (remove the r if you would like oldest -&gt; newest)
 #] find . -type f -newer translate_list.pl ! -newer shd-gz/ -exec ls -l {} \; -print &gt; output.txt; -- to make sure I got the correct range of data 
    | greped for earliest date and latest date
 #] find . type -newer translate_list.pl ! -newer shd-gz/ delete; -- this will find and delete files with date stamps between translate_list_fctmos 
    and the direcoty shd-gz/
 #] find . -type f -newer translate_list.pl ! -newer shd-gz/  -exec mv "{}" brokenfiles/ \; -- if you want to be extra safe you can move them to a 
    temporary directory and then delete the entire content of that directory once you have verified that you found the correct range of files.
</pre>
<h3><span id="find_a_specific_file_type" class="mw-headline">find a specific file type</span></h3>
In this example we are finding all <a class="external text" href="http://www.cyberciti.biz/tips/howto-linux-unix-find-move-all-mp3-file.html" rel="nofollow">.mp3</a> files and moving them to a mounted usb drive on /mnt/mp3
<pre> #]grep *.mp3 - lets assume there is a mix of file types with no standard naming convention and there are thousands of them
 #]find / -iname "*.mp3" -exec mv {} /mnt/mp3 ; - you can have any command in the -exec section
</pre>
<h3><span id="find_anything_older_than_12_hours" class="mw-headline">find anything older than 12 hours</span></h3>
Sometimes you have to alleviate some pressure so the file system does not fill up and you do not want to clear out files that may be actively being worked on.
<pre> #]ls -R | wc -l; -- will list number of files in directory
 #]find . -type f -mmin +720 -delete;  -- find and delete anything over 12 hours old
</pre>
<h3><span id="find_like_grep" class="mw-headline">find like grep</span></h3>
find can be used much in the same way as grep to search for the name of files in a directory.
<pre> #] cd /usr/local/lib;
 #] find ./ -name "*gdal*" -print; --prints out all files containing the word gdal in their name
 #] find ./ -name "*gdal*" -delete; -- deletes all the files containing the word gdal in their name
</pre>
<h1><span id="Server_seems_slow" class="mw-headline">Server seems slow</span></h1>
This is the holy grail of complaints as there are literally millions of things that could cause a server to be slow.
<h2><span id="top" class="mw-headline">top</span></h2>
<a class="external text" href="http://linux.die.net/man/1/top" rel="nofollow">top</a> gives one a task explorer like peak into the activity of the server. When one is using top you can press "u" key and sort by specific username. "c" allows one to get more detail on the processes running. top by default tries to list everything in order by highest use of %CPU.
<pre> #]top -u apache
  top - 08:37:14 up 41 days, 20:30,  3 users,  load average: 0.00, 0.04, 0.08
  Tasks: 140 total,   3 running, 136 sleeping,   0 stopped,   1 zombie
  %Cpu(s):  1.7 us,  2.0 sy,  0.0 ni, 95.9 id,  0.0 wa,  0.0 hi,  0.3 si,  0.0 st
  KiB Mem:   1885520 total,  1339856 used,   545664 free,        0 buffers
  KiB Swap:  4095996 total,    52368 used,  4043628 free.   462444 cached Mem
  
  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
  11462 apache    20   0 1005776  12212   4072 S  0.0  0.6   1:13.79 httpd
  11492 apache    20   0 1005640  12688   4208 S  0.0  0.7   1:13.22 httpd
  11493 apache    20   0 1005636  12124   4104 S  0.0  0.6   1:13.60 httpd
  12802 apache    20   0  254124   1636    836 S  0.0  0.1   0:00.00 httpd
  12803 apache    20   0  255300   1532    672 S  0.0  0.1   0:14.62 httpd
  12804 apache    20   0  255300   1508    652 S  0.0  0.1   0:00.18 httpd
  12806 apache    20   0 1005940  12892   3548 S  0.0  0.7   4:35.21 httpd
  19201 apache    20   0  656156  13036   1832 S  0.0  0.7   0:00.03 php-fpm
  19202 apache    20   0  656156  13036   1832 S  0.0  0.7   0:00.03 php-fpm
</pre>
<h2><span id="free" class="mw-headline">free</span></h2>
The <a class="external text" href="http://linux.die.net/man/1/free" rel="nofollow">free</a> command will give one a snapshot of the current memory and swap usage. Remember to subtract buffered and cached memory from used to get an actual representation of the amount of RAM in use.
<pre> #]free
              total       used       free     shared    buffers     cached
 Mem:       3924876    3663056     261820          0     298528    1755512
 -/+ buffers/cache:    1609016    2315860
 Swap:      4194296     235456    3958840
</pre>
<h2><span id="ps" class="mw-headline">ps</span></h2>
The <a class="external text" href="http://linux.die.net/man/1/ps" rel="nofollow">ps</a> or process command can be used to get a very detailed account of every single process running at the exact moment you enter the command, it does not refresh like top, but can clue you into process trees and zombie/dead/defunct processes that might not show up in top. I will truncate the output below as it can be quite lengthy.
<pre> #]ps fax
</pre>
<pre>  PID TTY      STAT   TIME COMMAND
    1 ?        Ss     0:18 /sbin/init
  480 ?        S&lt;s    0:00 /sbin/udevd -d
 5799 ?        S&lt;     0:00  \_ /sbin/udevd -d
 1057 ?        S      1:29 /opt/chef-server/embedded/service/bookshelf/erts-5.9.3.1/bin/epmd -daemon
 1349 ?        Sl   174:03 /usr/sbin/vmtoolsd
 1836 ?        S&lt;sl   0:47 auditd
 1854 ?        Ss     0:00 /sbin/portreserve
 1861 ?        Sl     1:12 /sbin/rsyslogd -i /var/run/syslogd.pid -c 5
 1892 ?        Ss    81:11 irqbalance
 1906 ?        Ss     0:16 rpcbind
 1982 ?        Ss     0:00 rpc.statd
 2029 ?        Ss    13:34 rpc.gssd
 2126 ?        Ss     0:04 dbus-daemon --system
 2142 ?        Ss     0:00 cupsd -C /etc/cups/cupsd.conf
 2185 ?        Ss     0:00 /usr/sbin/acpid
 2194 ?        Ssl    1:07 hald
 2195 ?        S      0:00  \_ hald-runner
 2224 ?        S      0:00      \_ hald-addon-input: Listening on /dev/input/event2 /dev/input/event0
 2235 ?        S      0:00      \_ hald-addon-acpi: listening on acpid socket /var/run/acpid.socket
 2255 ?        Ssl    1:44 automount --pid-file /var/run/autofs.pid
 2307 ?        Ss     0:00 rpc.rquotad
 2311 ?        Ss     0:00 rpc.mountd
 2347 ?        Ss     0:00 rpc.idmapd
 2355 ?        Ss     0:00 /usr/sbin/mcelog --daemon
 2365 ?        S     44:47 /usr/sbin/snmpd -LS0-6d -Lf /dev/null -p /var/run/snmpd.pid
 2377 ?        Ss     0:59 /usr/sbin/sshd
21008 ?        Ss     0:02  \_ sshd: me [priv]
 2393 ?        Ss    12:49 ntpd -x -u ntp:ntp -p /var/run/ntpd.pid
 2502 ?        Ss     0:31 /usr/sbin/vsftpd /etc/vsftpd/vsftpd.conf
 2626 ?        Ss     5:14 sendmail: accepting connections
 2699 ?        Ssl   47:09 /usr/sbin/hsflowd -u 564D4180-E560-251E-88F8-8285B49A7839
 2702 ?        Ss     0:02 sendmail: Queue runner@01:00:00 for /var/spool/clientmqueue
 2809 ?        Ss     0:00 /usr/sbin/abrtd
 2817 ?        Ss     0:09 abrt-dump-oops -d /var/spool/abrt -rwx /var/log/messages
 2856 ?        Ssl   15:23 /usr/sbin/qpidd --data-dir /var/lib/qpidd --daemon
 2937 ?        Sl   138:43 thin server (127.0.0.1:5220)
 2951 ?        Ss     1:35 crond
 3007 ?        Ss     0:00 /usr/sbin/atd
 3040 ?        Ss     0:00 /usr/bin/rhsmcertd
 3058 ?        Ss     0:11 /usr/sbin/certmonger -S -p /var/run/certmonger.pid
 3078 tty2     Ss+    0:00 /sbin/mingetty /dev/tty2
 3081 tty3     Ss+    0:00 /sbin/mingetty /dev/tty3
 3083 tty4     Ss+    0:00 /sbin/mingetty /dev/tty4
 3092 tty5     Ss+    0:00 /sbin/mingetty /dev/tty5
 3095 tty6     Ss+    0:00 /sbin/mingetty /dev/tty6
 4846 tty1     Ss+    0:00 /sbin/mingetty /dev/tty1
21685 ?        Ss     3:27 /usr/sbin/httpd
 7578 ?        S      0:18  \_ /usr/sbin/httpd
 7579 ?        S      0:00  \_ /usr/sbin/httpd
 7580 ?        S      0:00  \_ /usr/sbin/httpd
 7581 ?        S      0:00  \_ /usr/sbin/httpd
 7582 ?        S      0:00  \_ /usr/sbin/httpd
 7583 ?        S      0:00  \_ /usr/sbin/httpd
 7584 ?        S      0:00  \_ /usr/sbin/httpd
 7585 ?        S      0:00  \_ /usr/sbin/httpd
 7586 ?        S      0:00  \_ /usr/sbin/httpd
 6584 ?        Sl    24:30 /usr/bin/monit
 5454 ?        Ssl  700:00 /etc/alternatives/java -Djava.awt.headless=true -DJENKINS_HOME=/var/lib/jenkins -jar
28121 ?        Ss     0:09 /var/cfengine/bin/cf-execd
28130 ?        Ss    24:13 /var/cfengine/bin/cf-serverd
28141 ?        Ss     0:59 /var/cfengine/bin/cf-monitord
17905 ?        Ss     0:00 xinetd -stayalive -pidfile /var/run/xinetd.pid
18334 ?        Ss     0:02 /usr/sbin/dhcpd -user dhcpd -group dhcpd
 6133 ?        Ss     0:07 /usr/sbin/sssd -f -D
 6135 ?        S      0:02  \_ /usr/libexec/sssd/sssd_nss --debug-to-files
 6136 ?        S      0:02  \_ /usr/libexec/sssd/sssd_pam --debug-to-files
 6137 ?        S      0:01  \_ /usr/libexec/sssd/sssd_ssh --debug-to-files
 6166 ?        S      0:05  \_ /usr/libexec/sssd/sssd_be --domain default --debug-to-files
</pre>
<pre> #]ps faux - the <b>u</b> will give one system <b>u</b>sage along with the process tree
</pre>
<pre>USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root      2951  0.0  0.0 117296  1256 ?        Ss    2014   1:35 crond
root      3007  0.0  0.0  21540   480 ?        Ss    2014   0:00 /usr/sbin/atd
root      3040  0.0  0.0 104020   544 ?        Ss    2014   0:00 /usr/bin/rhsmcertd
root      3058  0.0  0.0  62300   932 ?        Ss    2014   0:11 /usr/sbin/certmonger -S -p /var/run/certmonger.
root      3078  0.0  0.0   4064   524 tty2     Ss+   2014   0:00 /sbin/mingetty /dev/tty2
root      3081  0.0  0.0   4064   520 tty3     Ss+   2014   0:00 /sbin/mingetty /dev/tty3
root      3083  0.0  0.0   4064   524 tty4     Ss+   2014   0:00 /sbin/mingetty /dev/tty4
root      3092  0.0  0.0   4064   524 tty5     Ss+   2014   0:00 /sbin/mingetty /dev/tty5
root      3095  0.0  0.0   4064   524 tty6     Ss+   2014   0:00 /sbin/mingetty /dev/tty6
root      4846  0.0  0.0   4064   520 tty1     Ss+   2014   0:00 /sbin/mingetty /dev/tty1
root     21685  0.0  0.2 237412  8600 ?        Ss   Mar13   3:27 /usr/sbin/httpd
root      7578  0.0  0.1 236908  4656 ?        S    May10   0:18  \_ /usr/sbin/httpd
apache    7579  0.0  0.1 237680  5748 ?        S    May10   0:00  \_ /usr/sbin/httpd
apache    7580  0.0  0.1 237688  5748 ?        S    May10   0:00  \_ /usr/sbin/httpd
apache    7581  0.0  0.1 237688  6176 ?        S    May10   0:00  \_ /usr/sbin/httpd
apache    7582  0.0  0.1 237688  5748 ?        S    May10   0:00  \_ /usr/sbin/httpd
apache    7583  0.0  0.1 237688  5748 ?        S    May10   0:00  \_ /usr/sbin/httpd
apache    7584  0.0  0.1 237688  5748 ?        S    May10   0:00  \_ /usr/sbin/httpd
apache    7585  0.0  0.1 237688  5748 ?        S    May10   0:00  \_ /usr/sbin/httpd
apache    7586  0.0  0.1 237688  5748 ?        S    May10   0:00  \_ /usr/sbin/httpd
root      6584  0.0  0.0 179628  2872 ?        Sl   Mar17  24:30 /usr/bin/monit
jenkins   5454  1.4 14.7 2503936 577244 ?      Ssl  Apr09 700:00 /etc/alternatives/java -Djava.awt.headless=true
root     28121  0.0  0.0 101428  3364 ?        Ss   May11   0:09 /var/cfengine/bin/cf-execd
root     28130  0.6  0.1 366888  4236 ?        Ss   May11  24:15 /var/cfengine/bin/cf-serverd
root     28141  0.0  0.1  35624  5284 ?        Ss   May11   0:59 /var/cfengine/bin/cf-monitord
root     17905  0.0  0.0  22180   988 ?        Ss   May12   0:00 xinetd -stayalive -pidfile /var/run/xinetd.pid
dhcpd    18334  0.0  0.1  49000  4376 ?        Ss   May12   0:02 /usr/sbin/dhcpd -user dhcpd -group dhcpd
root      6133  0.0  0.0 199608  2372 ?        Ss   May12   0:07 /usr/sbin/sssd -f -D
root      6135  0.0  0.3 201872 14588 ?        S    May12   0:02  \_ /usr/libexec/sssd/sssd_nss --debug-to-files
root      6136  0.0  0.0 192212  2808 ?        S    May12   0:02  \_ /usr/libexec/sssd/sssd_pam --debug-to-files
root      6137  0.0  0.0 189892  2688 ?        S    May12   0:01  \_ /usr/libexec/sssd/sssd_ssh --debug-to-files
root      6166  0.0  0.1 229764  6916 ?        S    May12   0:05  \_ /usr/libexec/sssd/sssd_be --domain default
</pre>
<h2><span id="kill" class="mw-headline">kill</span></h2>
Now is the time to learn how to stop runaway processes. Always first try to do a service reset as it will exit "correctly" and start again and if there are more problems you should be able to see them in a logfile, instead if you just kill it. The process will not have time to show you errors.
<pre> #]kill PID PID2 PID3; -- you can kill any number of specific processes as long as you get their PID number from either top or ps fax.
 #]kill -9 PID PID2 PID3; this <b>REALY</b> kills it if the above does not work, sometime you have to resort to the most drastic measure to get a zombie process out of there. Use sparingly as regular kill alows the process to stop and let go of files before exiting. adding -9 kills it immediately and may leave behind file locks.
 #]killall httpd; -- will kill all processes with the word httpd in the name
 #]killall -u datagorilla; -- will kill all processes running as the datagorilla user
</pre>
In scripted form:
<pre> #!/bin/sh
 k=`/bin/ps fax | /bin/grep "/usr/sbin/mesos-master" | /bin/grep -v grep |  /bin/awk '{ print $1 }'`
 kill $k
 echo "Killed mesos-master with PID $k"
</pre>
<h1><span id="Networking" class="mw-headline">Networking</span></h1>
Often times you will have to determine if a service is working correctly by whether or not it is listening on the <a class="external text" href="http://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers" rel="nofollow">correct port</a> or if it is responding at all.
<h2><span id="ping" class="mw-headline">ping</span></h2>
The most common network debugging tool. It is good for a quick up/down test of the machine, but NOTE if the machine is super busy it will not respond to ping right away and you could be seeing slow ping times and it could have nothing to do with the network or the NIC.
<pre> #]<a class="external text" href="http://linux.die.net/man/8/ping" rel="nofollow">ping</a> 10.0.0.1  --ping the gateway
</pre>
<h2><span id="telnet" class="mw-headline">telnet</span></h2>
<a class="external text" href="http://linux.die.net/man/1/telnet" rel="nofollow">Telnet</a> is a good way to query a specific remote listening port to see if a service is responding as it should
<pre> #] telnet web004 80
  Trying 10.0.0.[web004]...
  Connected to web004.
  Escape character is '^]'.
  ^]
  exit
</pre>
<h2><span id="netstat" class="mw-headline">netstat</span></h2>
<a class="external text" href="http://linux.die.net/man/8/netstat" rel="nofollow">netstat</a> produces a list of listening interfaces, ports, and connections to and from the machine.
<pre>]# netstat -an
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:5308            0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:46341           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:9000          0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:40968           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:9001          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:9002          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:9003          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:9004          0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:34284           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:9005          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:9006          0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:111             0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
...
tcp6       0      0 :::443                  :::*                    LISTEN
tcp6       0      0 :::34459                :::*                    LISTEN
tcp6       0      0 :::51869                :::*                    LISTEN
tcp6       0      0 :::111                  :::*                    LISTEN
tcp6       0      0 :::80                   :::*                    LISTEN
tcp6       0      0 :::48432                :::*                    LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
udp        0      0 0.0.0.0:53348           0.0.0.0:*
udp        0      0 0.0.0.0:111             0.0.0.0:*
udp        0      0 0.0.0.0:123             0.0.0.0:*
udp        0      0 0.0.0.0:58552           0.0.0.0:*
udp        0      0 0.0.0.0:5353            0.0.0.0:*
udp        0      0 127.0.0.1:323           0.0.0.0:*
udp        0      0 0.0.0.0:58715           0.0.0.0:*
udp        0      0 0.0.0.0:54872           0.0.0.0:*
udp        0      0 0.0.0.0:745             0.0.0.0:*
udp        0      0 0.0.0.0:37643           0.0.0.0:*
udp        0      0 127.0.0.1:834           0.0.0.0:*
udp        0      0 127.0.0.1:854           0.0.0.0:*
udp        0      0 0.0.0.0:36748           0.0.0.0:*
udp6       0      0 :::111                  :::*
udp6       0      0 :::55414                :::*
udp6       0      0 :::123                  :::*
udp6       0      0 ::1:323                 :::*
udp6       0      0 :::41442                :::*
udp6       0      0 :::745                  :::*
udp6       0      0 :::48913                :::*
raw6       0      0 :::58                   :::*                    7
</pre>
<pre>netstat -anetu | grep 514; 
tcp        0      0 0.0.0.0:514                 0.0.0.0:*                   LISTEN
tcp        0      0 :::514                      :::*                        LISTEN
tcp        0      0 :::5514                     :::*                        LISTEN
tcp        0      0 ::ffff:127.0.0.1:44946      ::ffff:127.0.0.1:9300       ESTABLISHED 497        3320514
udp        0      0 0.0.0.0:514                 0.0.0.0:*                       
udp        0      0 :::514                      :::*                            
udp        0      0 :::5514                     :::*       
</pre>
<h2><span id="ss" class="mw-headline">ss</span></h2>
the ss command can do the same and more as netstat and should be used in the future. <a class="external text" href="http://linux.die.net/man/8/netstat%7C" rel="nofollow">netstat</a> has become deprecated/obsolete to <a class="external text" href="http://linux.die.net/man/8/ss%7C" rel="nofollow">ss</a> since CentOS 6.4
<pre> #] ss -apnetu | grep 443;
 tcp    LISTEN     0      128                   :::443                  :::*      ino:202599741 sk:ffff88013beba100
 tcp    ESTAB      0      0      ::ffff:10.0.20.63:443    ::ffff:70.198.42.193:2400   timer:(keepalive,119min,0) uid:48 ino:228626831 sk:ffff880011629880
 tcp    TIME-WAIT  0      0      ::ffff:10.0.20.63:443    ::ffff:70.198.42.193:2426   timer:(timewait,48sec,0) ino:0 sk:ffff88013cb3c940
 tcp    ESTAB      0      0      ::ffff:10.0.20.63:443    ::ffff:70.198.42.193:2421   timer:(keepalive,119min,0) uid:48 ino:228626830 sk:ffff8800027380c0
 tcp    TIME-WAIT  0      0      ::ffff:10.0.20.63:443    ::ffff:70.198.42.193:2410   timer:(timewait,47sec,0) ino:0 sk:ffff88013cb3ca80
 tcp    ESTAB      0      0      ::ffff:10.0.20.63:443    ::ffff:70.198.42.193:2414   timer:(keepalive,119min,0) uid:48 ino:228626829 sk:ffff88006031c100
 tcp    TIME-WAIT  0      0      ::ffff:10.0.20.63:443    ::ffff:70.198.42.193:2401   timer:(timewait,48sec,0) ino:0 sk:ffff880017550e80
</pre>
<h3><span id="Find_all_incoming_connections_from_unique_IP_Addresses" class="mw-headline">Find all incoming connections from unique IP Addresses</span></h3>
<pre> #] netstat -tapn | awk '{print $5}' | sed 's/::ffff://' | sed 's/:.*//' | sort | uniq -c | sort;
     1 10.0.20.63
     1 10.0.50.232
     1 10.0.50.234
     1 10.0.50.244
     1 10.0.5.54
     1 10.10.1.231
     2 10.0.5.154
     2 129.82.224.115
    22 129.82.224.137
     3 10.0.20.201
    39 10.0.20.52
     4 10.0.20.30
     9 0.0.0.0
</pre>
<h3><span id="Find_all_outgoing_connections_to_unique_IP_Addresses" class="mw-headline">Find all outgoing connections to unique IP Addresses</span></h3>
<pre> #]  ss -tapw | awk '{print $5}' | sed 's/::ffff://' | sed 's/:.*//' | sort | uniq -c | sort;
  1 10.10.1.63
  12 10.0.20.63
  1 Local
  3 10.0.50.63
</pre>
<h2><span id="lsof" class="mw-headline">lsof</span></h2>
<a class="external text" href="http://linux.die.net/man/8/lsof" rel="nofollow">lsof</a> can also be used to determine which process is using a specific port. We once had an issue with a process running on a sendmail port which would not allow sendmail to start on one of our production web servers. This was key in tracking that down and has become a quicker way to check specific ports than netstat.
<pre>]# lsof -i :514
COMMAND   PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
rsyslogd 4835 root    1u  IPv4 3354631      0t0  TCP *:shell (LISTEN)
rsyslogd 4835 root    2u  IPv6 3354632      0t0  TCP *:shell (LISTEN)
rsyslogd 4835 root    3u  IPv4 3354623      0t0  UDP *:syslog
rsyslogd 4835 root    4u  IPv6 3354624      0t0  UDP *:syslog
</pre>
<h2><span id="CentOS_6_eth0_not_appearing" class="mw-headline">CentOS 6 eth0 not appearing</span></h2>
Often times when we clone a machine in VMWare the MAC address of the NIC will stay with the clone and cause conflicts, this is the way to remove the old MAC address and configure eth0 to accept the new one.
<pre>vi /etc/sysconfig/network-scripts/ifcg-eth0 - make sure mac address matches one in the VM's hardware profile in vcenter

vi /etc/udev/rules.d/70-persistent-net.rules - delete entire line with original MAC address, change in second line eth1 to eth0

ip link set eth1 name eth0
ifup eth0
#should be fixed now to confirm.
ping www.google.com

route -vm
cat /etc/resolv.conf
cat/etc/hosts/
cat /etc/hostname
</pre>
<h1><span id="Copying_large_number_of_files" class="mw-headline">Copying large number of files</span></h1>
Due to having over a Petabyte of data we very often have to move large sums of data around.
<h2><span id="rsync" class="mw-headline">rsync</span></h2>
<a class="external text" href="http://linux.die.net/man/1/rsync" rel="nofollow">rsync</a> is the method to use when copying a large number of files big or small. The / in the from where to where are very important and is the diference between copying the directory or just everything within the directory to a new location.
<pre> #] rsync -avr /nfs/data othermachine:/new/dataarea/ --progress; - copies local directory and all of it's content data to othermachine:/new/dataarea/data
 #] rsync -avr othermachine:/new/dataarea/ /nfs/data --progress; - copies all data FROM the othermachine under dataarea/ to /nfs/data/
</pre>
<h2><span id="screen" class="mw-headline">screen</span></h2>
You should do any long running operations in a <a class="external text" href="http://aperiodic.net/screen/quick_reference" rel="nofollow">screen</a> session so that if your connection to the machine timesout, the operation does not end. This is also a way to do things privetly on a server no one can see within a screen session, unless you allow it
<pre> #] screen -S copyfiles; -- start a new session, named copyfiles
 #] rsync -avr /nfs/data othermachine:/new/dataarea/ --progress; ## example command
 Ctrl-a d - while the rsync is running, Control-a d will detach but leave running the operation and you can continue doing what ever you want
 #] screen -r copyfiles; -- will reattach to the the rsync screen session
 #] screen -d R session_share; -- allows you to <a class="external text" href="http://technonstop.com/screen-commands-for-terminal-sharing" rel="nofollow">share your session</a> with someone else, useful for training.
 #] screen -x session_share; allows a your fried to connect to your session
 Ctrl-d - while inside the screen will detach and terminate the session
</pre>
<h1><span id="I_need_my_script_to_run_at_startup" class="mw-headline">I need my script to run at startup</span></h1>
On many of our servers we need NFS mounts to other servers/NAS devices to be present at start up so that users/services/websites can get to their data.
<pre> #] vim /usr/local/bin/nfs_mounts.sh - insert nfs mount command to new file nfs_mounts.sh
 #] chmod 700 /usr/local/bin/nfs_mounts.sh - changes permissions so only root user can execute.
 #] vim /etc/rc.local
  add the line at the end
  /usr/local/bin/nfs_mounts.sh &amp;   -- make sure their is an &amp; symbol after the command
 #] chmod =X /etc/rc.local --make the rc.local file executable at startup
</pre>
<pre> sidenote: Do not use fstab/mtab to auto-mount NFS volumes if they are not present at boot time then the system will hang indefinetly until it is available. our nfs_mounts shell script is the way to get around that.
</pre>
<h1><span id="PATH" class="mw-headline">PATH</span></h1>
Sometimes a problem occurs when one build a project via source and the executable are not located in /usr/bin or /usr/local/bin, the filesystem does not automatically know where to find them via name so one has to type out the full path to interact with those files.
<h2><span id="env" class="mw-headline">env</span></h2>
<pre> #]env
 MANPATH=:/var/cfengine/share/man
 XDG_SESSION_ID=2
 HOSTNAME=web005.example.com
 SHELL=/bin/bash
 TERM=xterm
 HISTSIZE=1000
 QT_GRAPHICSSYSTEM_CHECKED=1
 USER=root
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.axa=01;36:*.oga=01;36:*.spx=01;36:*.xspf=01;36:
 MAIL=/var/spool/mail/root
 PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/var/cfengine/bin:/root/bin
 PWD=/tmp
 LANG=en_US.UTF-8
 HISTCONTROL=ignoredups
 SHLVL=1
 HOME=/root
 LOGNAME=root
 LESSOPEN=||/usr/bin/lesspipe.sh %s
 _=/bin/env
 OLDPWD=/nfs
</pre>
&nbsp;
<h2><span id="Add_new_location_to_PATH" class="mw-headline">Add new location to PATH</span></h2>
To temporarily add a new location to path type the following:
<pre> #] export PATH=/var/cfengine/bin:$PATH;  --adding $PATH will keep the old PATH along with the new one, order matters, IF you forget $PATH nothing will work, reboot
</pre>
To permanently add a new location to path there are 2 options:

<b>User Specific:</b>
If the user always logs onto the same machine and needs certain files.
<pre> #] vim /nethome/username/.bashrc
 add export command to the file, examples of some below
 # .bashrc
 export SVN_EDITOR=vim
 export PATH=/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin:/opt/grads-  2.0.1.oga.1/Contents:/opt/grib2/wgrib2:/home/gempak/NAWIPS/os/linux64/bin:/home/ldm/bin:
 export GAVERSION=2.0.1.oga.1
 source /home/gempak/NAWIPS/Gemenviron.profile
 export LAPS_DATA_ROOT=/wxrnd/lapsdata
 export LAPS_SRC_ROOT=/opt/laps-0-50-19
 export LAPSINSTALLROOT=/opt/laps-0-50-19
</pre>
<b>Machine Specific:</b>
This is probably the "best practices" way and I would recommend doing this from now instead of .bashrc. As it allows anyone who logs into the machine to have the same PATH settings.
<pre> #]vim /etc/profile.d/postgresql.sh;  -- make sure file ends with .sh or it will not be read by filesystem
 export PATH=/usr/pgsql-9.3/bin:$PATH
 export MANPATH=$MANPATH:/usr/pgsql-9.3/share/man
 save, log out and log back in
 #]env | grep PATH; -- and you should now see the new PATH settings
</pre>
Repeat this for any/all source built files that have non-standard paths or settings.
<h1><span id="Forgot.2Flost_root_password" class="mw-headline">Forgot/lost root password</span></h1>
It happens to the best of us, either one mistypes or cant remember the root password to a machine there is a way to reset the root password. To do that you must boot into single user mode, reset the password, and then a second reboot to restore it to normal
<ol>
	<li>Reset the machine</li>
	<li>wait for the grub boot menu and press 'e'</li>
	<li>Edit the first kernel loader by adding the word 'single' to the end of the line</li>
	<li>Save and press 'b' to boot with the new grub option</li>
	<li>change root password once machine boots; passwd root</li>
	<li>reboot</li>
</ol>
<h1><span id="Change_Hostname" class="mw-headline">Change Hostname</span></h1>
The following files are what you need to edit to change the hostname of a machine
<pre>#]vim /etc/hostname; --edit to newhostname.example.com
#]vim /etc/hosts; --add/edit "newhostname.example.com newhostname" to beginning of both lines in file
#]vim /etc/sysconfig/network-scripts/ifcfg-eth0; -- make sure hostname variable is not set on any NICs or change it
#]export HOSTNAME=newhostname.example.com; change global environmental variable, this way you do not have to reboot
#]ipa-client-install uninstall;  --remove old authentication settings for old host
#]ipa-client-install; -- re-add server to idm
</pre>
<h1><span id="CentOS_Live_CD_Disk_Check" class="mw-headline">CentOS Live CD Disk Check</span></h1>
We sometimes have to evaluate older drives to see if they can be put back into old hardware. Directions below are how to check for bad blocks anr/or uncorrectable errors.
<pre>Boot up with a centos dvd in rescue mode and enter the shell
smartctl -a /dev/sda  - will report ALL the health of the drive in question.
smartctl -t short /dev/sda
</pre>
<h1><span id="CentOS_7_UID_error" class="mw-headline">CentOS 7 UID error</span></h1>
In CentOS 7 by defualt pam is set to not allow log in access by UID lower than 1000. past system administrators made certain user(gerhb308) lower UID than 1000. Here is how you fix that but also keep the server somewhat secure.
<pre>Error: /var/log/secure
pam_succeed_if(sshd:auth): requirement "uid &gt;= 1000" not met by user "gerbn308"
cd /etc/pam.d
vim system-auth - edit line to allow &gt; 500 uid
vim password-auth - edit the same
</pre>
<h1><span id="Sendmail" class="mw-headline">Sendmail</span></h1>
A good thing to add to scripts is alerts when things do not go as planned. Below is a snippet of code that sends an email if a disk's usage is more than 95% full.
<pre> #] mail -s "Alert: Netapp volume out of disk space $usep% $all" systems@example.com
</pre>
<pre>#!/bin/sh
df -h -t nfs -P | grep /vol/ |  awk '{ print $5 " " $6}' | while read output;
do
  echo $output
  usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1  )
  partition=$(echo $output | awk '{ print $2 }' )
  if [ $usep -ge 95 ]; then
    echo "Running out of space \"$partition ($usep%)\" on $(hostname) as on $(date) `df -h -P`" |
     mail -s "Alert: Netapp volume out of disk space $usep% $all" systems@example.com
  elif [ $usep -ge 98 ]; then
    echo "Running out of space \"$partition ($usep%)\" on $(hostname) as on $(date)" |
     mail -s "Alert: Netapp volume out of disk space $usep% $all" pagers@example.com
 else
        echo "Volume has room to grow!"
  fi
done
</pre>
<h2><span id="Sendmail_Masquerade" class="mw-headline">Sendmail Masquerade</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a title="Edit section: Sendmail Masquerade" href="/wiki/index.php?title=Standard_Linux_Tools&amp;action=edit&amp;section=48">edit</a><span class="mw-editsection-bracket">]</span></span></h2>
For some of our production services we send email's to our clients, but lately a few email providers will reject those messages because they did not originate from the MX record in our DNS. You have to masquerade all outgoing mail from the server as coming from @example.com not @web004.example.com.
<pre>#] vim /etc/mail/sendmail.mc
MASQUERADE_AS(example.com)dnl
FEATURE(masquerade_envelope)dnl
FEATURE(masquerade_entire_domain)dnl
FEATURE(allmasquerade)dnl
:wq
#] m4 /etc/mail/sendmail.mc &gt; /etc/mail/sendmail.cf
#] systemctl restart sendmail
</pre>
<h2></h2>
<h1><span id="VMware_and_Kernel_2.6_.28CentOS_6.29" class="mw-headline">VMware and Kernel 2.6 (CentOS 6)</span></h1>
<a class="external text" href="http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&amp;cmd=displayKC&amp;externalId=2011861" rel="nofollow">Testing</a> has shown that NOOP or Deadline perform better for virtualized Linux guests. ESX uses an asynchronous intelligent I/O scheduler, and for this reason virtual guests should see improved performance by allowing ESX to handle I/O scheduling.

To implement this change, please refer to the documentation for your Linux distribution.

Note: All scheduler tuning should be tested under normal operating conditions as synthetic benchmarks typically do not accurately compare performance of systems using shared resources in virtual environments.

For example, this change can be implemented by:
The scheduler can be set for each hard disk unit. To check which scheduler is being used for particular drive, run this command:
<pre> cat /sys/block/disk/queue/scheduler
</pre>
For example, to check the current I/O scheduler for sda:
<pre> # cat /sys/block/sda/queue/scheduler
 [noop] anticipatory deadline cfq
</pre>
In this example, the sda drive scheduler is set to NOOP.

To change the scheduler on a running system, run this command:
<pre> # echo scheduler &gt; /sys/block/disk/queue/scheduler
</pre>
For example, to set the sda I/O scheduler to NOOP:
<pre> # echo noop &gt; /sys/block/sda/queue/scheduler
</pre>
Note: This command will not change the scheduler permanently. The scheduler will be reset to the default on reboot. To make the system use a specific scheduler by default, add an elevator parameter to the default kernel entry in the GRUB boot loader menu.lst file.

For example, to make NOOP the default scheduler for the system, the /boot/grub/menu.lst kernel entry would look like this:
<pre> title CentOS (2.6.18-128.4.1.el5)
 root (hd0,0)
 kernel /vmlinuz-2.6.18-128.4.1.el5 ro root=/dev/VolGroup00/LogVol00 elevator=noop
 initrd /initrd-2.6.18-128.4.1.el5.img
</pre>
With the elevator parameter in place, the system will set the I/O scheduler to the one specified on every boot.
<h1><span id="Summary" class="mw-headline">Summary</span></h1>
There are basically an infinite amount of tools and ways to resolve an issue. 10 times out of 10, if you have a problem someone else has already encountered it and documented how to resolve the issue somewhere out there via google.com.
<ol>
	<li><a class="external text" href="http://www.linux.org/threads/in-linux-everything-is-a-file.4245/" rel="nofollow">EVERYTHING on Linux is a file</a>, understanding this fact is key to understanding linux, permissions, access, drivers, kernels, and debugging</li>
	<li>Follow through! Do not just hit enter and walk away, understand the consequences (good and bad) of what you are doing before you change something.</li>
	<li>Start small, the first thing every aspiring Linux Admin should build is a LAMP or <a title="LAPP Stack" href="/wiki/index.php/LAPP_Stack">LAPP Stack</a> and then move on to more complicated services/setups</li>
	<li>Take notes, so that you remember where you got stuck and what you did so it can be a repeatable process that should be able to be duplicated many times over(this is what the wiki is for)</li>
	<li><a class="external text" href="http://en.wikipedia.org/wiki/Phrases_from_The_Hitchhiker%27s_Guide_to_the_Galaxy#Don.27t_Panic" rel="nofollow">Don't Panic!</a> when you mess up, learn how to fix it this will make you a better admin, trial by fire is the way of life for all of us.</li>
	<li>Take snapshots, backups, SVN/GIT, copy files before any major changes, always start at Testing/DEV and work your way up to BTA/PROD deployments.</li>
	<li>Ask questions, discuss what you are doing before/after you change something(even if it is just research), measure twice/cut once: This allows everyone to know where you are and what you are doing, that way if something bad happens we can quickly triage the situation.</li>
</ol>

<hr />

</div>