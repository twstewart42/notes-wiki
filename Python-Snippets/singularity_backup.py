#!/usr/bin/env python
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


