#!/usr/bin/python
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
  




