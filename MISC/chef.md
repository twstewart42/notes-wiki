#Chef

This documentation is probably pretty out of date, and I have only setup and explored chef 1 time so I may not have the best understanding of all the pieces of it. I struggled to use it as our web and database servers are very "custom", I remember trying to hack up some cookbooks to install a full <a href=http://mapserver.org/introduction.html>OSGeo Mapserver</a>, but I was unable to do so at the time.

<h2>Server Config</h2>
wget https://opscode-omnibus-packages.s3.amazonaws.com/el/6/x86_64/chef-server-11.0.11-1.el6.x86_64.rpm


http://www.getchef.com/chef/install/


$ cd /opt/chef-server/bin
$ chef-server-ctl reconfigure
$ sudo chef-server-ctl test

NEXT: set up the workstation


Make sure you have FQDN set correctly or things may get messed up.

That is it for now. I set up the workstation on the server for convenience but they can be separate machines. 

<h2> workstation </h2>
I installed the workstation on the chef-server

curl -L https://www.opscode.com/chef/install.sh | bash

From <http://www.getchef.com/chef/install/> 


	1) Get the installer from link above
	2) Install git
	3) Cd /var/chef
	4) git clone git://github.com/opscode/chef-repo.git
	5) mkdir -p /var/chef/chef-repo/.chef
	6) echo '.chef' >> ./chef/.gitignore
	7) knife configure --initital
	8) cp those .pem and knife.rb files to .chef directory
	9) echo 'export PATH="/opt/chef/embedded/bin:$PATH"' >> ~/.bash_profile && source ~/.bash_profile
	10) Knife client list
	11) If you got to server:433 those clients will be listed under "Clients" they may have defaulted to generic names life chef-validator and chef-webui if you did not change them in the knife configure --initial

<h2>Node</h2>
You have to bootstrap the node

From main server:
Knife bootstrap node1.example.com -x root

This will install the chef-client on the machine

You can see the machine on the chef Server web util under Nodes

<h2>Cookbooks</h2>
This is the bread and butter of chef

https://learnchef.opscode.com/tutorials/create-your-first-cookbook/#configureapacheonlinux

Above is a handy tutorial to setup a cookbook that install httpd on a client

There are a host of premade cookbooks like https://github.com/opscode-cookbooks/mysql more can be found on getchef.com

Using the mysql as an example:

Log onto the workstation
Cd /var/chef/chef-repo/cookbooks
Git clone https://github.com/opscode-cookbooks/mysql.git
Cd mysql
You can edit defaults and options in the various setup files
$ knife cookbook upload mysql
Go to web interface
Find the node you want to add the cookbook too, and edit the node
Drag the Available recipe to the Run List
Ssh to the machine and run "chef-client" or you can do it via the workstation by
$ knife ssh machine.example.com 'chef-client' -m -x root -P 
The cookbook should be applied at that moment.
