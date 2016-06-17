<!-- start content -->
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote>Vagrant is a tool for building complete development environments. With an easy-to-use workflow and focus on automation, Vagrant lowers development environment setup time, increases development/production parity, and makes the "works on my machine" excuse a relic of the past.</blockquote>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ul>
	<li><a class="external text" href="https://www.vagrantup.com/about.html" rel="nofollow">Vagrant</a></li>
	<li><a class="external text" href="https://www.virtualbox.org/wiki/Downloads" rel="nofollow">VirtualBox</a></li>
	<li><a class="external text" href="https://git-scm.com/downloads" rel="nofollow">Git for Windows</a></li>
</ul>
<h1><span id="Install" class="mw-headline">Install</span></h1>
The point of this project is to grant our developers a complete but equal development environment on their local desktops. So they can develop while systems brings up an Alpha, beta, and production environment. The install guide refers to Windows machines only.
<ol>
	<li>Install virtual box: <a class="external free" href="https://www.virtualbox.org/wiki/Downloads" rel="nofollow">https://www.virtualbox.org/wiki/Downloads</a></li>
	<li>Install git for windows(needed for 'vagrant ssh' command): <a class="external free" href="https://git-scm.com/downloads" rel="nofollow">https://git-scm.com/downloads</a></li>
	<li>Install vagrant : <a class="external free" href="https://www.vagrantup.com/downloads.html" rel="nofollow">https://www.vagrantup.com/downloads.html</a></li>
</ol>
<h1><span id="Example" class="mw-headline">Example</span></h1>
I created an example project that setups a CentOS 7 VM with <a href="https://twstewart84.wordpress.com/systems-administration/lapp-stack/">httpd2.4/php-fpm</a>, <a href="https://twstewart84.wordpress.com/systems-administration/kickstart/">mapserver</a>, plus <a href="https://twstewart84.wordpress.com/systems-administration/postgresql/">postgres</a> w/ postgis all in one single machine. This uses a sample project to demonstrate a working machine that meets our regular requirements. Later in the Vagrantfile section you should see that I "mount" a local copy of the sample project to the /var/www directory on the VM. This can be in done in a similar fashion for any project. Since this is local development I did not think there was much need to setup SSL and I prefer it that way we are not passing our keys around to every single developer. If it was a need I would setup their web service to use a dummy localcert for testing.
<pre> svn checkout https://svn.example.com/svn/vagrant-example #using tortoiseSVN
 open cmd
 cd C:\SVN\vagrant-example\branches\mapserver\
 vagrant up
 # if all the above is installed a virtual machine should be downloaded, 
 booted, and configured based on the VagrantFile, it takes about 15-20 minutes 
 the first time, remember mapserver is a big install w/ lots of dependencies
 vagrant ssh # will log you into the virtual machine so that you can adjust 
              setting/do work

</pre>
The beauty of this is that the developer has full control of the local machine, try anything if it breaks just type 'vagrant destroy' then 'vagrant up' and a fresh install will occur with no damage done. When things work and/or make things run better, they can tell systems so we can incorporate these changes into our preexisting dev, beta, prod environments.
<h1><span id="Vagrant_Commands" class="mw-headline">Vagrant Commands</span></h1>
<pre> C:\SVN\vagrant-example\branches\mapserver\&gt; vagrant suspend 
      # saves machine state, then turns virtual machine off, 
       can also use vagrant halt
 C:\SVN\vagrant-example\branches\mapserver\&gt; vagrant resume 
      # turns virtual machine back on
 C:\SVN\vagrant-example\branches\mapserver\&gt; vagrant reload 
      # restarts machine and updates any configs set in the Vagrantfile
 C:\SVN\vagrant-example\branches\mapserver\&gt; vagrant provision 
      # you do not need to run this very often, only if change is made to 
       Vagrantfile, but any changes are completely redone on server so it 
       is best to 'vagrant destroy' then 'vagrant up' and start with a 
       "clean machine" after any major changes to the Vagrantfile.
 C:\SVN\vagrant-example\branches\mapserver\&gt; vagrant destroy 
      # deletes machine and any data/settings that were not saved externally
</pre>
<h1><span id="Vagrantfile" class="mw-headline">Vagrantfile</span></h1>
The Vagrantfile is the most important piece to all of this as it informs vagrant on how it should setup the machine. This file could be modified to meet each individual projects needs that way no matter who is developing the application, everything stays the same and is locked in with SVN. An example is posted below
<pre># -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "bento/centos-7.1"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  config.vm.box_check_update = true

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder "sample-project/", "/var/www"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
     vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
     vb.memory = "1024"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: &lt;&lt;-SHELL
  $defaultvhost = &lt;&lt;-SCRIPT
  sudo yum -y install epel-release;
  sudo yum clean all ;
  sudo yum -y install httpd php-fpm mod_fcgi;
  sudo echo "
  &lt;IfModule mod_proxy.c&gt;
        ProxyTimeout 300
        Timeout 300
  &lt;/IfModule&gt;

  &lt;IfModule mod_fcgid.c&gt;
        FcgidConnectTimeout 300
        FcgidMinProcessesPerClass 0
        FcgidMaxProcessesPerClass 700
        FcgidMaxRequestLen 268435456
        FcgidBusyTimeout 300
        FcgidIOTimeout 300
  &lt;/IfModule&gt;" &gt;&gt; /etc/httpd/conf/httpd.conf 
  sudo echo "
  &lt;VirtualHost *:80&gt;
		DirectoryIndex index.php
	    DocumentRoot /var/www/html
        &lt;Directory /var/www/html&gt;
                Options FollowSymLinks ExecCGI
                AllowOverride AuthConfig
                require all granted
        &lt;/Directory&gt;
	ProxyPassMatch ^/(.*\.php(/.*)?)$ fcgi://127.0.0.1:9000/var/www/html/$1 connectiontimeout=300 timeout=300
  &lt;/VirtualHost&gt; " &gt;&gt; /etc/httpd/conf.d/default.conf;
  sudo mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.no
  #cd /opt; sudo wget http://jpgraph.net/download/download.php?p=5 ;
  echo "Building Mapserver Requirements"
  cd /opt; sudo wget http://kickstart.example.com/kickstart/ks/c7_new_prdweb.sh ;
  sudo chmod 0700 /opt/c7_new_prdweb.sh ;
  sudo /opt/c7_new_prdweb.sh; #configures the mapserver requirements 
  sudo systemctl start httpd;
  sudo systemctl start php-fpm;
  sudo su - postgres -c "/usr/pgsql-9.4/bin/initdb /var/lib/pgsql/9.4/data";
  sudo su - postgres -c "/usr/pgsql-9.4/bin/pg_ctl -D /var/lib/pgsql/9.4/data -l /var/lib/pgsql/pg_startup.log start"
  #sudo systemctl start postgresql;
  SCRIPT
  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: $defaultvhost
end
</pre>
&nbsp;

<hr />

</div>