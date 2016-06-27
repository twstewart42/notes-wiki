 yum install system-config-firewall-tui |installed by default in centos 5/yum6 but not centos 7

Setup -> firewall is the easiest way if you don't remember iptable rules easily

Or 
iptables -nL --line-numbers

iptables -I INPUT {LINE_NUMBER} -i eth1 -p tcp --dport 21 -s 123.123.123.123 -j ACCEPT -m comment --comment "This rule is here for this reason"

From <https://snipt.net/johan_adriaans/insert-an-iptables-rule-on-a-specific-line-number-with-a-comment-and-restore-all-rules-after-reboot/> 

Example below for postgres add one for each service that needs access; 80, 443, 22, 3306, 389, 636, 5432, and others that may be necessary in a case by case basis

iptables -I INPUT 5 -i eth0 -p tcp --dport 5432 -j ACCEPT

All rules should be saved by centOS in /etc/sysconfig/iptables
]# cat /etc/sysconfig/iptables
#iptables-save v1.4.7 on Tue May  5 09:36:53 2015
*filter
:INPUT ACCEPT [1:32]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [251:38758]
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT -m comment --comment "Allow all for loopback"
-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT -m comment --comment "SSH Access"
-A INPUT -p udp -m state --state NEW -m udp --dport 22 -j ACCEPT
-A INPUT -p tcp -m multiport --dports 20,21,23,24,25,53,137,138,139 -m state --state NEW,ESTABLISHED -j ACCEPT -m comment --comment "Basic Services"
-A INPUT -p udp -m multiport --dports 20,21,23,24,25,53,137,138,139 -m state --state NEW,ESTABLISHED -j ACCEPT
-A INPUT -p tcp -m multiport --dports 80,443,111,2049,4045,5309,5432,3306,873,388,5308,514,8443,2812,445 -m state --state NEW,ESTABLISHED -j ACCEPT -m comment --comment "General Communication"
-A INPUT -p udp -m multiport --dports 80,443,111,2049,4045,5309,5432,3306,873,388,5308,514,445 -m state --state NEW,ESTABLISHED -j ACCEPT -m comment --comment "Authentication"
-A INPUT -p tcp -m multiport --dports 389,636,88,464,138,139,4456,749,7389,9443 -m state --state NEW,ESTABLISHED -j ACCEPT
-A INPUT -p udp -m multiport --dports 88,464,53,123,138,139,389,445 -m state --state NEW,ESTABLISHED -j ACCEPT
-A INPUT -p tcp -m multiport --dports 11211,2181,5050,5051,8080,8081,8082 -m state --state NEW,ESTABLISHED -j ACCEPT -m comment --comment "Memcache and Mesos"
-A INPUT -p tcp -m multiport --dports 901,902,903,993 -m state --state NEW,ESTABLISHED -j ACCEPT
-A INPUT -p tcp -m multiport --dports 9261,9262,9263,9264,9265,9266,9267,9268 -m state --state NEW,ESTABLISHED -j ACCEPT
-A INPUT -p udp -j REJECT --reject-with icmp-port-unreachable
-A INPUT -p tcp -j REJECT --reject-with icmp-port-unreachable
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
COMMIT
# Completed on Tue May  5 09:36:53 2015

-A OUTPUT -p tcp --dport 22 -j DROP # drops ssh FROM the server


