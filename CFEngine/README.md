<div id="content" role="main">

				
					
<article id="post-242" class="post-242 page type-page status-publish hentry">
	<header class="entry-header">
		<h1 class="entry-title">CFEngine</h1>
	</header><!-- .entry-header -->

	<div class="entry-content">
		<p>&nbsp;</p>
<div id="globalWrapper">
<div id="column-content">
<div id="content" class="mw-body">
<p>&nbsp;</p>
<h1 id="firstHeading" class="firstHeading"><span dir="auto">CFEngine On CentOS</span></h1>
<div id="bodyContent" class="mw-body-content">
<div id="siteSub"></div>
<p><!-- start content --></p>
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote><p>CFEngine is a policy manager that ensures each machine it is installed upon meets the policy system&#8217;s create for different groupings of machines. Can be configured to monitor, install, check, update, remove, create just about anything</p></blockquote>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<dl>
<dd><a class="external text" href="https://docs.cfengine.com/docs/3.5/new-users.html#install-and-configure-the-cfengine-server" rel="nofollow">Install CFEngine</a></dd>
<dd><a class="external text" href="https://docs.cfengine.com/docs/3.5/getting-started-installation-installing-community.html" rel="nofollow">Getting Started</a></dd>
<dd><a class="external text" href="https://docs.cfengine.com/docs/3.5/reference-components.html" rel="nofollow">CFEngine Reference Guide </a></dd>
</dl>
<h1><span id="Warning" class="mw-headline"><b>Warning</b></span></h1>
<p>CFEngine is a very powerful tool. You can make it do ANYTHING to a large number of machines. Proceed with caution, remember machines are stupid they will do EXACTLY what you tell them to do. Treat this tool with respect, start new promises with small groups before expanding cluster wide.</p>
<h1><span id="myPromises" class="mw-headline">myPromises</span></h1>
<p>A sysadmin must create promises that define what a machine should be doing, what it should be running, what it should have installed, etc. I am just showing snippets of these as these are quite long as we have many promises, mostly for ensuring all of our services are up 24/7 and if they do fail start them with 5 minutes. Systems receive emails each time a promise does not meet the expected result(i.e. repeated failures to start a daemon, disk running out of room)</p>
<p>the two most important ones are z01PromiseSetup.cf, which tells the system which promises to keep</p>
<pre>bundle common z01_promise_setup
{
vars:
    "bundles" slist     =&gt; {
                           
                                "w01_check_mysql",
                                "w01_check_httpd",
                                "w01_check_zedx_jobtoold",
                                "w01_check_hsflowd",
                                "w01_check_mesos_master",
};
   "promise_files" slist
                        =&gt; {
                       
                                "myPromises/w01checkmysql.cf",
                                "myPromises/w01checkhttpd.cf",
                                "myPromises/w01checkzedxjobtoold.cf",
                                "myPromises/w01checkhsflowd.cf",
                                "myPromises/w01checkmesosmaster.cf",
};
</pre>
<p>and z02GlobalClasses.cf, which tells CFEngine which machines fall into which class, machines can be in many classes or excluded from a class should the match a regex.</p>
<pre>bundle common z02_global_classes
{

classes:

"mesosslaves" or =&gt; {
                        regcmp("appa01","${sys.uqhost}"),
                        regcmp("appa02","${sys.uqhost}"),
                        regcmp("appa03","${sys.uqhost}"),
                        regcmp("appa04","${sys.uqhost}"),

        };

        "app" or =&gt; {
                        regcmp("app[0-9]{3}","${sys.uqhost}"),
                        regcmp("appb02","${sys.uqhost}"),
        };

        "web" or =&gt; {
                        regcmp("web[a-z]{3}[0-9]{3}",
                        "${sys.uqhost}"),regcmp("funame",
                        "${sys.uqhost}"),regcmp("who",
                        "${sys.uqhost}"),
                        regcmp("idk","${sys.uqhost}"),
                        regcmp("fakename","${sys.uqhost}"),

}
</pre>
<h1><span id="Promise_Format" class="mw-headline">Promise Format</span></h1>
<p>Below is the format of a promise to ensure all machines in the base group that are not centos_5 or Centos_4 machines have sssd running.</p>
<p>w01checksssd.cf</p>
<pre>bundle agent w01_check_sssd
{
methods:
# tells it which group that can run this chech_sssd
        base.!centos_5.!dhcp.!centos_4::
        "w01checksssd" usebundle =&gt; check_sssd;

}

bundle agent check_sssd
{

vars:
        "grep_name" slist =&gt; { "sssd" }; # similar to ps fax | grep sssd
        "service" slist =&gt; { "sssd" }; # name of executable in /etc/init.d
        "init_scripts_path" string =&gt; "/etc/init.d";

processes:

        "$(grep_name)"
        comment =&gt; "Check if the process for '$(service)'",
        restart_class =&gt; "restart_$(service)";

commands:

        "${init_scripts_path}/${service} start"
        comment =&gt; "Restarting the service",
        ifvarclass =&gt; "restart_${service}";

reports:
        done::
         "Heads up - the $(this.promise_filename) promise restarted $(service) on $(sys.fqhost). "      ;

        !done::
        "$(service) is running on $(sys.fqhost).";

}

</pre>
<h1><span id="myTemplates" class="mw-headline">myTemplates</span></h1>
<p>A user can have files/packages/libraries, etc that need distributed to each machine in the policy group.<br />
first copy the file to mastercf:/var/cfengine/masterfile/myTemplates<br />
from there I have it sub divided by the same groupings as in z02GlobalClasses.cf<br />
rename it so it ends in a .txt .conf .cf or cfengine will ignore it.</p>
<p>then make a promise to distribute, example b21ManageConfig.cf to copy the ssh message of the day to each machine.</p>
<pre>bundle agent b21_manage_config
{

methods:
#all machine in the zedxinc domain are in "base"
    base::                                              # &lt;1&gt;
    "b21manageconf" usebundle
                        =&gt; b21_run ;

}

bundle agent b21_run
{

vars:
# notice the source dir is /var/cfengine/inputs and NOT /var/cfengine/masterfiles. When cfengine distributes policies to each machine that is bootstrapped to the master, the cf-agent can only execute local files in /var/cfengine/inputs.
    "source_dir" string
                        =&gt; "/var/cfengine/inputs/myTemplates" ;   # &lt;2&gt;

    "source_file" string
                        =&gt; "$(source_dir)/motd.txt" ;


files:
#creates file and assigns permissions
    "/tmp/motd"
    perms               =&gt; mog("640","root","root"),
    create              =&gt; "true",
    edit_defaults       =&gt; empty,
    edit_line           =&gt; expand_template("$(source_file)") ;    # &lt;3&gt;

}

</pre>
<ol>
<li>remember to always update z01PromiseSetup.cf each time you add a new promise or it will not be kept.</li>
</ol>
<h1><span id="Commands" class="mw-headline">Commands</span></h1>
<p>Checks consistency of policy file to ensure nothing is incorrect syntax wise. If there is a syntax issue ALL machines start complaining.</p>
<pre> $ cf-agent -f /var/cfengine/masterfiles/promises.cf 
</pre>
<p>Updates available policies for slave machines. copies to /var/cfengine/inputs</p>
<pre> $ cf-agent -IKf /var/cfengine/masterfiles/update.cf 
</pre>
<p>Machines should check in every five minutes but if you are testing sometimes this is too slow.</p>
<p>&nbsp;</p>
<p>Pull the latest promise update from the server on the agent machine:</p>
<pre> $ cf-agent -IKf /var/cfengine/inputs/update.cf
</pre>
<p>Immediately execute promises:</p>
<pre> $ cf-agent -IKf /var/cfengine/inputs/promises.cf
</pre>
<p>Show how much of each promise is able to be kept on the agent machine</p>
<pre> $ cf-agent -vn
</pre>
<h1><span id="Bootstrap.2FInstall" class="mw-headline">Bootstrap/Install</span></h1>
<p>To install the agents on slave machines with cfengine&#8217;s install script.</p>
<pre> $ wget -O- <a class="external free" href="https://s3.amazonaws.com/cfengine.packages/quick-install-cfengine-community.sh" rel="nofollow">https://s3.amazonaws.com/cfengine.packages/quick-install-cfengine-community.sh</a> | sudo bash
 $ cf-agent --bootstap 10.0.0.[CF]
</pre>
<h2><span id="For_Private-DMZ" class="mw-headline">For Private Networks</span></h2>
<p>or for any local install that you wish to not go out to the internet to get the latest version for your servers</p>
<pre> $ rpm -Uvh <a class="external free" href="http://rpm.zedxinc.com/ZedX/7/cfengine-community-3.8.1-1.x86_64.rpm" rel="nofollow">http://rpm.example.com/ZedX/7/cfengine-community-3.8.1-1.x86_64.rpm</a>
 $ cf-agent --bootstap 10.0.0.[CF]
</pre>
<p>The cfengine-community package is practically OS version agnostic and will install on CentOS 4,5,6, and 7 without any dependencies.</p>
<h1></h1>
<p>&nbsp;</p>
<hr />
</div>
</div>
</div>
</div>
</div>