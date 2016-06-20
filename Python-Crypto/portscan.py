#!/usr/bin/python
import argparse
from socket import *

def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        print '[+]%d/tcp open'% tgtPort
        connSkt.close()
    except:
        print '[-]%d/tcp closed'% tgtPort
 
def portScan(tgtHost, tgtPorts):
   try:
       tgtIP = gethostbyname(tgtHost)
   except:
       print "[-] Cannot resolve '%s': Unknown host" %tgtHost
       return
   try:
       tgtName = gethostbyaddr(tgtIP)
       print '\n[+] Scan Results for: ' + tgtName[0]
   except:
       print '\n[+] Scan Results for: ' + tgtIP  
   setdefaulttimeout(1)
   print 'debug: tgtPorts - '+ str(tgtPorts)
   for tgtPort in tgtPorts:
       print 'Scanning port ' + tgtPort
       connScan(tgtHost, int(tgtPort))
 
def main():
    parser = argparse.ArgumentParser(description='-H &lt;target host&gt; -p &lt;target port&gt;')
    parser.add_argument('-H', dest='tgtHost', type=str, help='specify target host')
    parser.add_argument('-p', dest='tgtPort', nargs='+', type=str, help='specify target port[s] separated by comma')
    options = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts=options.tgtPort
    print str(tgtPorts)
    if (tgtHost == None) | (tgtPorts[0] == None):
       print '[-] You must specify a target host and port[s].'
       exit(0)
    for port in tgtPorts:
       portScan(tgtHost, tgtPorts)
 
if __name__ == '__main__':
    main()

