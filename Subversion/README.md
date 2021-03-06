<h1>SVN</h1>
<blockquote>
The goal of the Subversion project is to build a version control system that is a compelling replacement for CVS in the open source community.
</blockquote>


; HTTP/HTTPS access    
: Access to the Subversion server is provided via the HTTP protocol, *not* the svn protocol.    
; LDAP authentication  
: Only authenticated users can access the Subversion server.  Authentication is provided by an LDAP server.  Access is restricted to members of the <code>svn</code> group.    


<h2>Links</h2>
<a href=https://tortoisesvn.net/>TortoiseSVN</a> - GUI SVN interface for Windows.  
<a href=https://subversion.apache.org/>Apache Subversion</a>


<h2>Access and Use</h2>
<h3>Creating a Repository</h3>
   $ '''svnadmin create''' ''dir''

<h3>Checking Out a Working Copy from a Repository</h3>
   $ '''svn checkout '''''repo'' [ ''dir'' ]

* Do not check out the same module over and over again.

<h3>Updating a Working Copy from the Repository</h3>
   $ '''svn update''' [ ''file ...'' ]

* Update frequently, usually whenever you sit down to work on the project.

<h3>Adding a File/Directory to a Repository</h3>
   $ '''svn add''' [ ''file ...'' ]

* Adding a file or directory does not auto-commit it, you will need to run a commit afterwards.

<h3>Adding Files that are Missing from Repository</h3>
  svn status | grep "^\?" | sed 's/^\? \*//g' | xargs svn ads

* Removing a file or directory does not auto-commit it, you will need to run a commit afterwards.

<h3>Committing a Working Copy to a Repository</h3>
   $ '''svn commit''' [ ''file ...'' ] '''-m''' "''your message here''"

* Do not commit broken code.

<h3>Removing a File/Directory from a Repository</h3>
  $ '''svn remove''' [ ''file ...'' ]

* Removing a file or directory does not auto-commit it, you will need to run a commit afterwards.

<h4>Removing Files that were Manually Deleted</h4>
  svn status | grep "^\!" | sed 's/^\! \*//g' | xargs svn rm

* Removing a file or directory does not auto-commit it, you will need to run a commit afterwards.

<h3>Adding New Users</h3>
* use ldapadmin to add the field "memberUid lastf123" to the svn user group. This is a hidden attribute as ipa doesn't use the legacy ldap memeberUid to authenticate but httpd's AuthzLDAPMemberKey does.


<h2>Administration</h2>
Systems has created two scripts to help the development team create and remove repositories in svn. They run with special sudo access on bfesysutl004 only by individuals in the svnadmin ldap group.

sudo /var/www/svn/create reponame
<pre>
#!/bin/bash

#script to create repo and add basic {trunk, branches, releases} directory trees
repo=$1
echo "creating $repo on http://svn.example.com/svn"
echo "svnadmin create /var/www/svn/$repo"
svnadmin create /var/www/svn/$repo
chown -R apache:apache /var/www/svn/$repo
echo "importing svn-template for $repo"
svnadmin dump /var/www/svn/svn-template > /tmp/svn-template.dump
svnadmin load /var/www/svn/$repo < /tmp/svn-template.dump
chown -R apache:apache /var/www/svn/$repo
echo "Done!"
echo "repo created at http://svn.example.com/svn/$repo/"
</pre>

'''! This one does full deletions be warned'''

sudo /var/www/svn/delete reponame
<pre>
#!/bin/bash

#Script for removing repositories in svn

repo=$1
read -p "You are about to delete /var/www/svn/$repo "
read -p 'Are you sure? yes/no: ' answer

        if [ "$answer" == "yes" ]
        then
                echo "Backing up $repo - just in case"
                svnadmin dump /var/www/svn/$repo > /nfs/subversion/bkup/.deleted/dump_$repo
                echo "removing $repo from http://svnhostname.example.com/svn/"
                rm -r /var/www/svn/$repo/
                echo "$repo has been removed"
        else
                echo "Nothing was deleted."
fi

</pre>

<h3>Apache Config</h3>
Our svn is available via http access so one can visually browse the repositories.
<pre>
#/etc/httpd/conf.d/svn.conf
LoadModule dav_svn_module     modules/mod_dav_svn.so
LoadModule authz_svn_module   modules/mod_svn_ldap.so
LoadModule authnz_ldap_module modules/mod_authnz_ldap.so
ErrorLog /var/log/svn/httpd_error_log
CustomLog /var/log/svn/httpd_access_log common

LDAPTrustedGlobalCert CA_BASE64 "/etc/ipa/ca.crt"
LDAPVerifyServerCert off


<Location /svn>

        DAV svn
        SVNParentPath /var/www/svn
        SVNListParentPath on
        SVNIndexXSLT /svnindex.xsl
        Require host svnhostname.example.com
        #SSLRequireSSL
   AuthType Basic
   AuthName "Subversion repositories"
        AuthBasicProvider ldap
        AuthLDAPURL "ldaps://ldap01.example.com:636/cn=users,cn=accounts,dc=example,dc=com?uid?sub"
        AuthLDAPInitialBindAsUser off
        AuthLDAPBindDN  "uid=ldapro,cn=users,cn=accounts,dc=example,dc=com"
        AuthLDAPBindPassword "fakepass"
        AuthLDAPGroupAttribute member
        Require valid-user
        Require group cn=svn,cn=groups,cn=accounts,dc=example,dc=com
</Location>
</pre>

<h2>Merge to Beta/Production</h2>
<h3>On dev:</h3>
Login as your username
  cd /var/www/projectname/html
  svn commit example.php
  continue with any other files that need to be included in the release.


<h3>On windows using tortoiseSVN: </h3> 
svn checkout http://svn.example.com/projectname  
if it is a new file   
   in trunk ctrl-c to copy file, navigate to C:\SVN\projectname\release\beta\, right click in directory -> TortoiseSVN -> Paste (copies release history)  
elif file already exists (most likely case):  
   go to release\beta, right click the file you want to update (example.php), TortoiseSVN -> merge, merge from trunk release if beta  
svn commit  

<h3>On beta:</h3>    
Login as your username  
cd /var/www/projectname/html  
svn status # make note of revision number, so if you need to roll back that can be done much easier. Revision: 1234  
svn update  
  # in most projects 'scripts' dir, there should be an executable to fix any permission conflicts to match the project's account.  

<h3>If it breaks beta: </h3>
cd /var/www/projectname/html  
svn up -r 1234 # rolls back to same <a href=http://blog.ekini.net/2008/04/30/svn-revert-to-a-previous-revision-after-a-wrong-update/> revision</a> number as listed when you ran svn status  




