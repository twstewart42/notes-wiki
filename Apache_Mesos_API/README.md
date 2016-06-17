<p><!-- start content --></p>
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<blockquote><p>This section is for information on how to interact with all of the parts of mesos and its frameworks and their respective API&#8217;s</p></blockquote>
<p>See <a title="Apache Mesos" href="https://twstewart84.wordpress.com/systems-administration/apache-mesos-master/">Apache Mesos</a> for additional information.</p>
<h1><span id="Links" class="mw-headline">Links</span></h1>
<p>External links to the API docs for each of these projects</p>
<dl>
<dd>
<ul>
<li><a class="external text" href="http://mesos.apache.org/documentation/latest/" rel="nofollow">Mesos</a></li>
<li><a class="external text" href="http://airbnb.github.io/chronos/#API" rel="nofollow">Chronos</a></li>
<li><a class="external text" href="https://mesosphere.github.io/marathon/docs/rest-api.html#post-/v2/apps" rel="nofollow">Marathon</a></li>
<li><a class="external text" href="https://github.com/HubSpot/Singularity/blob/master/Docs/reference/api.md" rel="nofollow">Singularity</a></li>
<li><a class="external text" href="https://mesosphere.github.io/marathon/docs/native-docker.html" rel="nofollow">Docker(Experimental)</a></li>
</ul>
</dd>
</dl>
<h1><span id="Mesos_Execute_Example" class="mw-headline">Mesos Execute Example</span></h1>
<p>Submit jobs from any master or slave, this is not super recommended as the other frameworks do a better job of task scheduling.</p>
<p>mesos execute &#8211;command=&#8221;/opt/test.py&#8221; &#8211;master=&#8221;master001.example.com:5050&#8243; &#8211;name=&#8221;test&#8221;</p>
<h1><span id="Singularity_Example" class="mw-headline">Singularity Example</span></h1>
<p>For singularity you have to submit both a request and a task to deploy a job.</p>
<pre>substitute a unique identifier for Ruuid and Duuid
#make request
curl -i -X POST -H 'Content-Type: application/json' -d '{"id": "'"$Ruuid"'", 
   "owners": ["me@example.com"], "daemon": false }, "state": "ACTIVE", 
   "instances": 1, "hasMoreThanOneInstance": false, "canBeScaled": false }' 
    master001:8082/singularity/api/requests

#deploy request
curl -i -X POST -H 'Content-Type: application/json' -d '{"deploy":{"requestId": 
   "'"$Ruuid"'", "id":"'"$Duuid"'", "command":"/exec/mesos_test/dev/test.py", 
   "resources":{"cpus":0.1,"memoryMb": 128, "numPorts":0} } }' 
    master001:8082/singularity/api/deploys

#run request
curl -i -X POST master001001:8082/singularity/api/requests/request/$Ruuid/run

#Remove a task
curl -i -X DELETE http://master001.example.com:8082/singularity/api/tasks/task/test-new_test-1433015100646-1-master001.example.com-DEFAULT

</pre>
<h1><span id="Chronos_Example" class="mw-headline">Chronos Example</span></h1>
<p>Chronos&#8217;s syntax is nearly identical to singularity the only &#8220;fallback&#8221; is that you cannot query for individual success/failures of a job, you can only query for status of ALL jobs. Also it&#8217;s date syntax is a little &#8220;weird&#8221;.</p>
<pre># date syntax
date=`date -u +%Y-%m-%d`
time=`date -u +%T`
date time is R0/$date\T$time\Z/PT2S
</pre>
<pre>#submit task to chronos
curl -i -H 'Content-Type: application/json' -X POST -d '{ "schedule": 
   "R0/'"$date"'T'"$time"'Z/PT2S", "name": "'$uuid'", "epsilon": "PT30S", 
   "command": "/exec/mesos_test/dev/test.py", "owner": "me@example.com", 
   "async": false }' master001:8081/scheduler/iso8601

#run task
curl -i -X PUT master001:8081/scheduler/job/$uuid

</pre>
<p>&nbsp;</p>
<h1><span id="Marathon_Example" class="mw-headline">Marathon Example</span></h1>
<p>We could experiment with php5.4&#8217;s built in web server and run a million tiny versions of websites, coupled with <a class="external text" href="https://twstewart84.wordpress.com/systems-administration/haproxy/" rel="nofollow">HAProxy</a>, this would increase our ability to scale our webservices/apis as we add customers. command: /usr/bin/php -S `hostname`:$PORT0 /opt/info.php</p>
<pre>Deploy a docker image with marathon 
vim testdev.json 
{ 
  "container": { 
    "type": "DOCKER", 
    "docker": { 
      "image": "docker001.example.com:5000/testdev", 
      "network": "BRIDGE", 
      "portMappings": [ 
        { "containerPort": 80, "hostPort": 0, "protocol": "tcp"} 
        ] 
    } 
  }, 
  "id": "testdev", 
  "instances": 1, 
  "cpus": 0.5, 
  "mem": 512, 
  "uris": [], 
  "ports": [49153], 
  "cmd": "" 
} 
  
curl -X POST -H "Content-Type: application/json" http://master001:8080/v2/apps  
-d@testdev.json

</pre>
<h1><span id="Using_It" class="mw-headline">Using It</span></h1>
<p>I have created &#8220;sample&#8221; bash scripts to show how all this can be managed and executed from anywhere in the cluster.</p>
<p>Queue_task_singularity.sh queues 15 jobs at once (can be set to any arbitrary number)</p>
<pre>#/bin/sh
##queuses up numerous tasks for singularity/mesos stress test

i=0
while [ $i -lt 15 ]; do

#create uuid edit out dashes, singularity does not allow them for names
uuid=`uuidgen | sed 's/-//g'`
echo $uuid
Rname=DEVreqTEST$uuid
Dname=DEVdepTEST$uuid
##send IDs to tmp for cleanup/referencing in other scripts
echo "----------$i--------------" &gt;&gt; /tmp/singhistory
echo "request ID is $Rname" &gt;&gt; /tmp/singhistory
echo "deploy ID is $Dname" &gt;&gt; /tmp/singhistory
#make request
curl -i -X POST -H 'Content-Type: application/json' -d '{"id": "'"$Rname"'", "owners": ["me@example.com"], "daemon": false }, "state": "ACTIVE", "instances": 1, "hasMoreThanOneInstance": false, "canBeScaled": false }' master00101:8082/singularity/api/requests

#deploy request
curl -i -X POST -H 'Content-Type: application/json' -d '{"deploy":{"requestId": "'"$Rname"'", "id":"'"$Dname"'", "command":"/exec/mesos_test/dev/test.py", "resources":{"cpus":0.1,"memoryMb": 128, "numPorts":0} } }' master001:8082/singularity/api/deploys

#run request
curl -i -X POST master001:8082/singularity/api/requests/request/$Rname/run

i=$((i + 1))
done
</pre>
<p>run_singularity.sh will re-run the last 15 jobs submitted.</p>
<pre>#!/bin/bash
# I made this very early in my understanding of API's which is 
# why there are some "strange" things happening
#command to get history on deploys
#curl -i -X GET http://master001:8082/singularity/api/history/request/requestTEST/deploy/hafu4waoihaehroaehf0aer0f003428502409430hq0oia980

r_array=(`grep "request ID" /tmp/singhistory | awk 'match($0,"is"){print substr($0,RSTART+3,50)}'`)
echo "request array is ${r_array[*]}"


#d_array=(`grep "deploy ID" /tmp/history | awk 'match($0,"is"){print substr($0,RSTART+3,50)}'`)
#echo "Deploy array is ${d_array[*]}"

num=${#r_array[@]}
for (( i=0; i&lt;${num}; i++));
        do
        #for deploy in "${d_array[@]}"
        #do
        echo $i

                Rname=${r_array[$i]}
                echo $request
                echo "curl -i -X POST master001:8082/singularity/api/requests/request/$Rname/run"
                curl -i -X POST master001:8082/singularity/api/requests/request/$Rname/run



done
</pre>
<p>cleanup_singularity.sh removes tasks/deploys/requests that are no longer valid or needed. Checks job status to make sure they have succeeded first before removing them.</p>
<pre>#!/bin/bash

#command to get history on deploys
#curl -i -X GET http://master001:8082/singularity/api/history/request/requestTEST/deploy/hafu4waoihaehroaehf0aer0f003428502409430hq0oia980

r_array=(`grep "request ID" /tmp/singhistory | awk 'match($0,"is"){print substr($0,RSTART+3,50)}'`)
echo "request array is ${r_array[*]}"


d_array=(`grep "deploy ID" /tmp/singhistory | awk 'match($0,"is"){print substr($0,RSTART+3,50)}'`)
echo "Deploy array is ${d_array[*]}"

num=${#r_array[@]}
for (( i=0; i&lt;${num}; i++));
        do
        #for deploy in "${d_array[@]}"
        #do
        echo $i

                request=${r_array[$i]}
                deploy=${d_array[$i]}
                echo $request
                echo $deploy
                echo "checking if successful"
                curl -i -X GET http://master001:8082/singularity/api/history/request/$request/deploy/$deploy &gt; /tmp/singcheck
                success=`awk 'match($0,"SUCCEEDED") {print substr($0,RSTART+0,9)}' /tmp/singcheck`
                echo "checking if failed"
                failed=`awk 'match($0,"FAILED") {print substr($0,RSTART+0,6)}' /tmp/singcheck`

                #find deploy state in history file
                #answer=`awk 'match($0,"deployState") {print substr($0,RSTART+14,9)}' check`
                if [[ "$success" == "SUCCEEDED" ]];
                then
                #removing successful request
                echo "you can delete request $request with deply $deploy"
                curl -i -X DELETE http://master001001:8082/singularity/api/requests/request/$request
                echo "curl -i -X DELETE http://master001:8082/singularity/api/requests/request/$request"
                else
                echo "investigate request $request and deploy $deploy did not complete successfully" &gt; sing_investigate
                sendmail -F singularity@example.com -it &lt;&lt;END_MESSAGE
                To: me@example.com
                Subject: tasks failed on singularity

                $(cat sing_investigate)
END_MESSAGE

fi
##clean up temp text files
cat /dev/null &gt; /tmp/singhistory
cat /dev/null &gt; /tmp/singcheck
cat /dev/null &gt; /tmp/singrequest

</pre>
<p>I created similar examples for interacting with chronos</p>
<h1><span id="Watching_It" class="mw-headline">Watching It</span></h1>
<p>You can view status of all jobs by navigating to <a href="http://master001:5050/#/" rel="nofollow">http://master001:5050/#/</a>. If jobs do not show up then some communication error is most likely the culprit. For old jobs view &#8220;sandbox&#8221; and there are links to stderr and stdout for individual tasks which make debugging very handy and easy.</p>
</div>