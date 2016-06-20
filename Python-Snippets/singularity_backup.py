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
