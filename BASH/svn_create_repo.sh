#!/bin/bash
#execute: sudo /var/www/svn/create $reponame
#script to create repo and add basic {trunk, branches, releases} directory trees
repo=$1
echo "creating $repo on http://svn.example.com/svn"
echo "svnadmin create /var/www/svn/$repo"
svnadmin create /var/www/svn/$repo
chown -R apache:apache /var/www/svn/$repo
echo "importing svn-template for $repo"
svnadmin dump /var/www/svn/svn-template &gt; /tmp/svn-template.dump
svnadmin load /var/www/svn/$repo &lt; /tmp/svn-template.dump
chown -R apache:apache /var/www/svn/$repo
echo "Done!"
echo "repo created at http://svn.example.com/svn/$repo/"
