<p><!-- start content --></p>
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote><p>Fabric is a Python (2.5-2.7) library and command-line tool for streamlining the use of SSH for application deployment or systems administration tasks.</p></blockquote>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ul>
<li><a class="external text" href="http://www.fabfile.org/%7C" rel="nofollow">Fab</a></li>
</ul>
<h1><span id="Install" class="mw-headline">Install</span></h1>
<pre> yum install fabric
</pre>
<p>OR</p>
<pre> pip install fabric
</pre>
<h1><span id="Run" class="mw-headline">Run</span></h1>
<p>I plan on using Fabric as a push-to config management service which will work very nicely as a secondary piece to my <a title="CFEngine" href="https://twstewart84.wordpress.com/systems-administration/cfengine/">CFEngine</a> setup. I used this to deploy a security update to 120+ hosts in under 20 minutes.</p>
<h2><span id="Standalone" class="mw-headline">Standalone</span></h2>
<pre> ]# fab -H server001 -- yum -y update glibc # will ask for password
</pre>
<h2><span id="With_fabfile" class="mw-headline">With fabfile</span></h2>
<p>one can create a fabfile.py with default settings and expanded tasks to execute, also paralled task execution can be achived.</p>
<pre> ]# vim fabfile.py
 from fabric.api import *
 from fabric.contrib.files import *
 
 env.hosts = [
         'server001',
         'server002',
         '...',
 ]
 
 env.user = "root" #it runs as parallel operations so there is no chance to enter a password for sudo users
 env.password = ""
 
 @parallel
 def install():
         run("yum -y update glibc")
</pre>
<p>Then to run:</p>
<pre> ]# fab -P install -f fabfile.py
</pre>
<h2><span id="Advanced_concepts" class="mw-headline">Advanced concepts</span></h2>
<p>The following is more advanced options that can be included within a fabfile in order to achieve different results.</p>
<pre>env.roledefs = {
      'testing': [
      'server001',
      'server002',
      ]
}
</pre>
<pre> ]# fab install:roles=testing
</pre>
<pre>def disk_check():
        run("df -hl")

def ram_check():
        run("free -h")


def check_all():
        print("Executing on %s as %s" % (env.host, env.user))
        upload_template("/tmp/fabric_hello", "/var/tmp/fabric_hello")# source, destination
        execute(disk_check)
        execute(ram_check)
</pre>
<pre> ]# fab check_all:roles=testing 
</pre>
<p>will run all tasks in order on each machine, do not use parallel execution if you expect to use the results returned to screen in anyway as parallel stdout/stderr does not return in order.</p>
<hr />
</div>
</div>
</div>
</div>
</div>