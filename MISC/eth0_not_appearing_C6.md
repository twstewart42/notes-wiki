when eth0 not on because of  vm clone or change of vnic

vi /etc/sysconfig/network-scripts/ifcg-eth0 - make sure mac address is correct

vi /etc/udev/rules.d/70-persistent-net.rules - delete origirnal change second eth1 to eth0

ip link set eth1 name eth0
ifup eth0

ping googl.com

route -vm
cat /etc/resolv.conf
cat/etc/hosts/
cat /etc/hostname

http://microdevsys.com/wp/device-eth0-does-not-seem-to-be-present-delaying-initialization-linux-networking/

http://microdevsys.com/wp/linux-networking-persistent-naming-rules-based-on-mac-for-eth0-and-wlan0/
