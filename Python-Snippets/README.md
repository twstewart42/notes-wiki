Snippets of Python Code that I wrote and would like to keep in memory. I apologize for the poor formatting wordpress does not parse tabs very well.
<h2>RSync</h2>
rsync CentOS or Epel Repos to create local ones
<pre>#!/usr/bin/python
import os
import random
import argparse
import RSyncBackup 
#http://www.owlfish.com/software/utils/RSyncBackup/ --not a standard pip install

def _rsync(Choice):
   rchoice = Choice
   if rchoice == 'C':
      print "Choice was CentOS"
      mirror_list = ['rsync://mirror.us.oneandone.net/centos/', 'rsync://mirror.cs.pitt.edu/centos/', 'rsync://mirrors-pa.sioru.com/CentOS/', 'rsync://mirror.itc.virginia.edu/centos/', 'rsync://mirror.clarkson.edu/centos', 'rsync://mirror.vcu.edu/centos/', 'rsync://mirror.umd.edu/centos/' ]
      local_dir = '/var/www/repo/html/CentOS/'
      ranMirror = random.choice(mirror_list)
      print 'selected %s' % ranMirror
      exclude = ['local*', 'isos', 'i386', 'i686']
   elif rchoice =='E':
      print "Choice was Epel"
      mirror_list = ['rsync://mirror.unl.edu/fedora-epel', 'rsync://mirror.cs.pitt.edu/fedora-epel', 'rsync://mirrors.mit.edu/fedora-epel']
      local_dir = '/var/www/repo/html/EPEL/'
      ranMirror = random.choice(mirror_list)
      print 'selected %s' % ranMirror
      exclude = ['local*', 'isos', 'i386', 'i686', '4', 'ppc64', 'debug']
   else:
      print "No choice was made"
      sys.exit()

   if os.path.exists(local_dir) == True:
      print 'true'
      backup = RSyncBackup.RSyncBackup(lastRunFile = '/tmp/centos-rsync', rsync="/usr/bin/rsync")
      backup.backup(source=ranMirror, destination=local_dir, excludeList=exclude)
      print 'false'


def main():
   parser = argparse.ArgumentParser(description="Python: rsyncs either CentOS or Epel repos to a local repository")
   parser.add_argument('choice', metavar='c', type=str, help='values: C, E')
   args = parser.parse_args()
   Choice = args.choice
   _rsync(Choice)

if __name__ == '__main__':
   main()</pre>
<pre>/opt/repo-rsync.py -h
usage: repo-rsync.py [-h] c

Python: rsyncs either CentOS or Epel repos to a local repository

positional arguments:
 c values: C, E

optional arguments:
 -h, --help show this help message and exit</pre>
<pre>#syncs centos
5 1 * * * python /opt/repo-rsync.py C
#syncs Epel
25 20 * * 6 python /opt/repo-rsync.py E</pre>
&nbsp;
<h2>Singularity_backup.py</h2>
I once crashed <a href="https://twstewart84.wordpress.com/systems-administration/apache-mesos-apis/">Singularity API</a> so hard that it lost all of it's scheduled requests and it was not correctly backing up to it's pre-configured MySQL database. So I created a better backup.
<pre>#!/usr/bin/env python
##########################################################
# Makes a backup of the singularity/mesos cluster request and deploy configs
# - T. Stewart
##############################################################
import subprocess
import os
import sys
import shutil
import pycurl
import cStringIO
import datetime
import MySQLdb
import argparse


def exportCSV():
  #exports full backup table to csv
  YMd = datetime.datetime.now().strftime('%Y-%m-%d')
  db2=MySQLdb.connect(host="mysql001.example.com", user="user1", passwd="fakepass", db="singularity")
  da=db2.cursor()
  fileb='/tmp/sing_back_%s.csv' % YMd

  if os.path.isfile(fileb) == True:
    #mysql cannot export if file already exists
    print "%s already exists" % fileb
    print "Making backup anyway"
    newname = '%s.bkup' % fileb
    shutil.move(fileb, newname)


  cmd3='SELECT * INTO OUTFILE \'%s\' FIELDS TERMINATED BY \',\' OPTIONALLY ENCLOSED BY \'\"\' LINES TERMINATED BY \'\\n\' FROM singularity_backup ;' % fileb
  print cmd3
  da.execute(cmd3)
  da.close()

  filec = fileb[5:]
  print filec
  finaldest = '/nfs/sing_backup/%s' % filec
  shutil.copyfile(fileb,finaldest)

def backup(r, fullurl, outputJ):
  #Puts everything in mysql table
  #print "%s\n%s\n%s" % (r, fullurl, output)
  YMd = datetime.datetime.now().strftime('%Y-%m-%d')
  print YMd
  #request_name VARCHAR(25) PRIMARY KEY, URL VARCHAR(100), json_config TEXT, last_update DATE
  db=MySQLdb.connect(host="mysql001.example.com", user="user1", passwd="fakepass", db="singularity")
  d=db.cursor()
  try:
    cmd1="INSERT INTO singularity_backup (request_name, URL, json_config, last_update) VALUES('%s', '%s', '%s', '%s');" % ( r, fullurl, outputJ, YMd)
    print cmd1
    d.execute(cmd1)
  except:
    cmd2="update singularity_backup set URL='%s', json_config='%s', last_update='%s' where request_name='%s'" % ( fullurl, outputJ, YMd, r)
    print cmd2
    d.execute(cmd2)
 
  db.close()

def get_JSON(r, url):
  #gets JSON from singularity API
  api = "/api/requests/request/%s" %r
  fullurl = "%s%s" % ( url, api)
  print fullurl

  c = pycurl.Curl()
  response = cStringIO.StringIO()
  c.setopt(pycurl.URL, fullurl)
  c.setopt(pycurl.WRITEFUNCTION, response.write)
  c.perform()
  c.close()
  output = response.getvalue()
  #print output
  return fullurl, output

def get_requests():
  #gets list of requests from zookeeper
  request = "/usr/lib/zookeeper/bin/zkCli.sh -server 127.0.0.1:2181 ls /singularity/requests/all | tail -n1 | tr -d \"[]\" | tr -d \",\"| sed \'s/ /&amp;\\n/g\'"
  print request
  requests_run = subprocess.Popen([request], shell=True, stdout=subprocess.PIPE)
  requests_out, requests_err = requests_run.communicate()
  request_clean = requests_out.splitlines()
  return request_clean


def main():
  parser = argparse.ArgumentParser(description="Makes MySQL and CSV backup of singularity")
  args = parser.parse_args()

  requests = get_requests()
  url = "http://10.0.0.[z01]:8082/singularity"
  for r in requests:
    print r
    fullurl, outputJ = get_JSON(r, url)
    #print outputJ
    #print "%s\n%s\n%s" % (r, fullurl, outputJ)
    backup(r, fullurl, outputJ)
    exportCSV()


if __name__ == '__main__':
 main()

</pre>
&nbsp;
<h2>Singularity Restore</h2>
Of course there is no good use of a backup if you can't restore from it so I created restore-singularity.py. The key to this one was understanding that what came from MySQL was a string and not a <a href="https://twstewart84.wordpress.com/systems-administration/apache-mesos-apis/">JSON</a> object the string would have to be loaded into a python dictionary in order to be segregated into it's separate request and deploy.
<pre>#!/usr/bin/env python
##################
## Makes a file that contains each request and deploy that
## would be needed to restore wxd singularity should it
## loose it's data
##
## - T. Stewart
#################
import json
import sys
from jsonmerge import merge
import MySQLdb
import argparse

def parsejson(blob, fileo):
  #converts string of blob to Python dictionary and reassembles them to individual curl requests
  #print "blob is %s " % blob
  parse = json.loads(blob)
  requestall = parse['request']
  rId = requestall['id']
  if requestall["requestType"] == "ON_DEMAND":
     #ON_DEMAND vs SCHEDULED
     rSchedule = "None"
     rQuartz = "None"
  else:
     rSchedule = requestall['schedule']
     rQuartz = requestall['quartzSchedule']

  rType = requestall["requestType"]
  try:
     #Sometimes they do not have owners assigned to tasks
     rOwners = requestall['owners']
  except:
     rOwners = "None"

  print rId, rType, rOwners, rSchedule, rQuartz

  #build new request JSON
  joinreq = {}
  joinreq['id'] = rId
  joinreq['owners'] = rOwners
  joinreq['schedule'] = rSchedule
  joinreq['quartzSchedule'] = rQuartz

  req_data = json.dumps(joinreq)
  print req_data
  curlrequest = 'curl -i -X POST -H \'Content-Type: application/json\' -d \'%s\' /
     endpoint001:8082/singularity/api/requests' % req_data
  print curlrequest

  try:
     #some do not have deploys, and that is okay
     deployall = parse['activeDeploy']
     dId = deployall['id']
     dCommand = deployall['command']
     print dId, dCommand
 
     resourcesall = deployall['resources']
     cpus = resourcesall["cpus"]
     mem = resourcesall['memoryMb']
     ports = resourcesall['numPorts']
     print cpus, mem, ports
 
     #build new deploy JSON
     joindep = {}
     joindep['requestId'] = rId
     joindep['id'] = dId
     joindep['command'] = dCommand
     dep_data = json.dumps(joindep)
     print dep_data
  
     #Build new resources JSON
     joinreso = {}
     joinreso['cpus'] = cpus
     joinreso['memoryMb'] = mem
     joinreso["numPorts"] = ports
     reso_data = json.dumps(joinreso)
     print reso_data
  
     merged = { 'deploy': joindep, 'resources': joinreso }
     string_merged = json.dumps(merged)
     try:
        string_merged
     except NameError:
        string_merged_exists = False
     else:
        string_merged_exists = True

     print string_merged

     curldeploy = 'curl -i -X POST -H \'Content-Type: application/json\' -d \'%s\' /
          endpoint001:8082/singularity/api/deploys' % string_merged
     print curldeploy
   except:
     print "no deploy"
     curldeploy = ""

   #append output to a file
   print fileo
   with open(fileo, "a") as text_file:
   text_file.write(curlrequest)
   text_file.write("\n")
   text_file.write(curldeploy)
   text_file.write("\n")
   text_file.close


def getcount():
   #Retrieve num of backups with count of rows in singularity_backup table
   db=MySQLdb.connect(host="mysql001.example.com", user="user001", passwd="fakepass", db="singularity")
   q=db.cursor()
   cmd='select count(*) FROM singularity_backup;'
   q.execute(cmd)
   num_a=q.fetchone()
   print num_a
   num = str(num_a).translate(None, "'(L),'")
   q.close()
   return int(num)
  
def getjson(num):
   #Retrieve all json blobs from MySQL table singularity_backup
   db=MySQLdb.connect(host="mysql001.example.com", user="user001", passwd="fakepass", db="singularity")
   q=db.cursor()
   sql='SELECT json_config FROM singularity_backup LIMIT %s,1;' % num
   print sql
   q.execute(sql)
   get=q.fetchall()
   #print get
   q.close()
   for g in get:
     print g
     cleang = str(g).translate(None, "'()'")
     print cleang
     return cleang[:-1]



def main():
  parser = argparse.ArgumentParser(description="Restores singularity request and deploys")
  parser.add_argument('-f', dest='File', type=str, help='Path to output contents of backup')
  args = parser.parse_args()
  if args.File is None:
    fileo = '/tmp/restore_singularity.txt'
  else:
    fileo = args.File


 #blob = '{"request":{"id":"TEST","requestType":"SCHEDULED","owners":["me@example.com"],
  "schedule":"54 * * * *","quartzSchedule":"0 54 * * * ?"},"state":"ACTIVE",
  "requestDeployState":{"requestId":"TEST","activeDeploy":{"requestId":"TEST",
  "deployId":"new_TEST","timestamp":1463933957851}},"activeDeploy":{
  "requestId":"TEST","id":"new_TEST","command":"su - user -c "do_something.sh"",
  "resources":{"cpus":1.0,"memoryMb":512.0,"numPorts":0}}}'
  num = getcount()

  for c in range(0, num):
  blob = getjson(c)

  while True:
    try:
      parsejson(blob, fileo)
    except ValueError as er:
      #This craziness is because some of the JSON have extra double quotes that 
       need to be a part of the JSON file but python does not like that so we have 
       to manually add escapes for them in
       #Use number in the error to use as a location to insert the missing escape
      print er
      ster = str(er)
      word = ster.strip().split()
      print word[6]
      addchar = int(word[6]) - 2
      print addchar
      blob = blob[:addchar] + '\\' + blob[addchar:]
      print blob
      continue
   break


if __name__ == "__main__":
 main()</pre>
&nbsp;
<h1>MultiProcessing Example</h1>
with thread locks for safe execution
<pre>#!/usr/bin/python
from multiprocessing import Process, Lock, Pool
import multiprocessing
from functools import partial
import argparse

ID_array = [1, 2, 3, 4]
zvars = [ a, b, c, d]
def manager(l):
  global lock
  lock = 1

def run_gfsqtr_proc(lock, ID, var):
   for v in var:
      lock.acquire()
      print v
      print id
      lock.release()
   
def main():
   parser = argparse.ArgumentParser(description="Demonstrate Threading")
   parser.add_argument('-t', dest='threads', type=int, help='Number of threads to run')
   args = parser.parse_args()

   if args.threads is None:
      numthreads=multiprocessing.cpu_count()
   else:
     numthreads=args.threads
    
   print numthreads
   m = multiprocessing.Manager()
   l = m.Lock()

   for ID in ID_array:
      p = Pool(processes=numthreads)
      func = partial(run_proc, l, ID)
      p.map(func, zvars)
      p.close()
      p.join()
  



</pre>
&nbsp;
<h2>Threading Example</h2>
This is a more realistic example using the threading Python library
<pre>#!/usr/bin/python
## Checks data_sources MSYQL table for data stuck in Active state
import subprocess, os, sys
import Queue
import threading
import MySQLdb
import argparse

def demote(uid, gid):
  #Ensures task is done as appropriate user
  def result():
  print('starting demotion')
  os.setgid(gid)
  os.setuid(uid)
  print('finished demotion')
  return result

def dl_check(q, freq):
  if freq == '1h':
    issue_frequency='1_Hourly'
    interval='3'
    dtype='HOUR'
  elif freq == '3h':
    issue_frequency='3_Hourly'
    interval='9'
    dtype='HOUR'
  elif freq == '6h':
    issue_frequency='6_Hourly'
    interval='12'
    dtype='HOUR'
  elif freq == '12h':
    issue_frequency='12_Hourly'
    interval='24'
    dtype='HOUR'
  elif freq == '1d':
    issue_frequency='Daily'
    interval='48'
    dtype='HOUR'
  elif freq == '1w':
    issue_frequency='Weekly'
    interval='14'
    dtype='DAY'
  elif freq == '1m':
    issue_frequency='1_Monthly'
    interval='60'
    dtype='DAY'
  elif freq == '1y':
    issue_frequency='Yearly'
    interval='400'
    dtype='DAY'
  else:
    print "no issue_frequency set"


  db=MySQLdb.connect(host="mysql001.example.com", user="user01", passwd="fakepass",
     db="database")
  c=db.cursor()
  print "issue_frequenct=%s" % issue_frequency
  print "\ninterval=%s" %interval
  print "\ndtype=%s \n" %dtype
  sql="SELECT data_source FROM data_sources WHERE current_download_state='Active' AND issue_frequency='%s' AND last_download_time &lt; ( NOW() - INTERVAL %s %s );" % (issue_frequency, interval, str(dtype),)
  print sql
  #print "debug %s %s, %s" % (sql, issue_frequency, dtype,)
  q.put(c.execute(sql))
  result=c.fetchall()
  print "debug: results\n "
  print result
  active = result
  #print active[0]
  if not c.rowcount:
    print "All %s sources downloaded &gt; %s hours ago are in 'Idle' state." % (issue_frequency, str(interval))
  else:
    for row in active:
    print "'Active' states found for %s source(s):" %issue_frequency
    #removes extra characters from tuple active and makes it a string
    line = str(active).translate(None, "(,)")
    print line
    print "\nUpdating to 'Idle'"
    sql2="UPDATE data_sources SET current_download_state='Idle' WHERE current_download_state='Active' AND issue_frequency='%s' AND data_source=%s;" % (issue_frequency, str(line),)
    q.put(c.execute(sql2))
    print "debug: %s" %sql2



def main():
  parser = argparse.ArgumentParser(description="Checks data_sources for data stuck in Active state")
  parser.add_argument('frequency', metavar='F', nargs='+', type=str, help='values: 1h, 3h, 6h, 12h, 1d, 1w, 1m, 1y')
  args = parser.parse_args()
  freqs=args.frequency
  print freqs
  q = Queue.Queue()
  for freq in freqs:
    print freq
    uid=1337
    gid=1337
    os.setgid(gid)
    os.setuid(uid)
    try:
       print "Running Check for %s downloads" %freq
       t = threading.Thread(target=dl_check, args = (q,freq))
       t.daemon = True
       t.start()
      
    except:
        print "Error: unable to start thread"
   s = q.get()
   print s


if __name__ == '__main__':
 main()</pre>
&nbsp;

&nbsp;

&nbsp;