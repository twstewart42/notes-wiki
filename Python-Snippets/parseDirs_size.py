#!/usr/bin/python
import os, sys, os.path, string, math
from glob import glob
from math import log
from decimal import *

getcontext().prec = 7       # Set a new precision

size = 0
quotient = 0

def sizeof_fmt(num):
	
	quotient = Decimal(num / 1024**3)
	return Decimal(quotient)

def get_size(start_path='.'):
    total_size = 0
    seen = {}
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                stat = os.stat(fp)
            except OSError:
                continue

            try:
                seen[stat.st_ino]
            except KeyError:
                seen[stat.st_ino] = True
            else:
                continue

            total_size += Decimal(stat.st_size)
			
    return Decimal(sizeof_fmt(total_size))

print get_size()
def parseDir(aDir):
	files = glob(aDir)
	for f in files:
		if os.path.isfile(f):
			pass
		if os.path.isdir(f):
		
			size = get_size(start_path=f)
			print os.path.abspath(f), Decimal(size)
			parseDir(f + "/*")
		
if __name__ == "__main__":
	parseDir(".")

