#!/usr/bin/python
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
 main()
