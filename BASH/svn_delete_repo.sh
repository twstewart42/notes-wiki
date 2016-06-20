#!/bin/bash
#execute: sudo /var/www/svn/delete $reponame
#Script for removing repositories in svn

repo=$1
read -p "You are about to delete /var/www/svn/$repo "
read -p 'Are you sure? yes/no: ' answer
    if [ "$answer" == "yes" ]
    then
        echo "Backing up $repo - just in case"
        svnadmin dump /var/www/svn/$repo &gt; /nfs/subversion/bkup/.deleted/dump_$repo
        echo "removing $repo from http://svn.example.com/svn/"
        rm -r /var/www/svn/$repo/
        echo "$repo has been removed"
    else
        echo "Nothing was deleted."
fi
