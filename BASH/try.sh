#!/bin/sh
yell() { echo "$0: $*" &gt;&amp;2; echo "$@ failed with exit code $?"| \
 mail -s "TEST FAIL" me@mail.com ;}
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }
try ping -c 1 10.0.0.1 #should pass
try ping -c 1 10.0.0.2578 #should fail and alert
try ping -c 1 www.google.com # should pass
