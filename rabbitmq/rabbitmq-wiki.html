<a href="http://www.rabbitmq.com/">RabbitMQ</a> is a message broker systems that can be used for data delivery, non-blocking operations, push notifications, asynchronous processing, and work queues. It gives applications a common platform to send and receive messages and is nearly language agnostic with open source client APIs written in nearly every major programming language.
<h1><span id="Links" class="mw-headline">Links</span></h1>
<ul>
	<li><a class="external text" href="http://www.rabbitmq.com/" rel="nofollow">RabbitMQ Main website</a></li>
	<li><a class="external text" href="https://blog.pivotal.io/pivotal/case-studies/800000-messagesminute-how-nokias-here-uses-rabbitmq-to-make-real-time-traffic-maps" rel="nofollow">8,000,000 messages per minute with RabbitMQ</a></li>
	<li><a class="external text" href="https://blog.pivotal.io/pivotal/products/rabbitmq-hits-one-million-messages-per-second-on-google-compute-engine" rel="nofollow">Google compute, 1 Million messager/min</a></li>
	<li><a class="external text" href="http://blogs.vmware.com/vfabric/2013/04/how-instagram-feeds-work-celery-and-rabbitmq.html" rel="nofollow">How Instagram Uses Celery and RabbitMQ</a></li>
</ul>
<h1>Install</h1>
I set RabbitMQ up on a three node cluster, 1 server was CentOS 6 and the other 2 were CentOS 7.
<pre>##Erlang must be the same version for every server in the cluster
&gt; rpm --import http://packages.erlang-solutions.com/rpm/erlang_solutions.asc
&gt; vim /etc/yum.repo.d/erlang.repo
+ [erlang-solutions]
+ name=Centos $releasever - $basearch - Erlang Solutions
+ baseurl=http://packages.erlang-solutions.com/rpm/centos/$releasever/$basearch
+ gpgcheck=1
+ gpgkey=http://packages.erlang-solutions.com/rpm/erlang_solutions.asc
+ enabled=1
&gt; yum install erlang
&gt; systemctl start erlang

&gt; rpm --import https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
&gt; yum install http://www.rabbitmq.com/releases/rabbitmq-server/v3.6.0/rabbitmq-server-3.6.0-1.noarch.rpm
</pre>
<h1>Configuration</h1>
<pre>&gt; systemctl start rabbitmq
&gt; cat /var/lib/rabbitmq/.erlang.cookie
#copy the erlang.cookie to each of the other rabbitmq servers
&gt; systemctl restart rabbitmq
&gt; rabbitmqctl stop_app
&gt; rabbitmqctl join_cluster rabbit@appa03
   Clustering node rabbit@appa01 with rabbit@appa03
&gt; rabbitmqctl change_cluster_node_type ram
&gt; rabbitmqctl start_app

All 3 should have the same info
&gt; rabbitmqctl cluster_status
Cluster status of node rabbit@appa01 ...
[{nodes,[{disc,[rabbit@appa01,rabbit@appa02,
                rabbit@appa03]}]},
 {running_nodes,[rabbit@appa02,rabbit@appa03,rabbit@appa01]},
 {cluster_name,&lt;&lt;"rabbit@appa03.example.com"&gt;&gt;},
 {partitions,[]}]

more advanced /etc/rabbitmq/rabbitmq.config, make this file the same on all 
rabbitmq servers.

%% ----------------------------------------------------------------------------
%% RabbitMQ Sample Configuration File.
%%
%% See http://www.rabbitmq.com/configure.html for details.
%% ----------------------------------------------------------------------------
[
 %%{ssl, [{versions, ['tlsv1.2', 'tlsv1.1', tlsv1]}]},
 {rabbit,
 [
 {tcp_listeners, [5672]},
 {default_vhost, &lt;&lt;"/"&gt;&gt;},
 {default_user, &lt;&lt;"guest"&gt;&gt;},
 {default_pass, &lt;&lt;"guest"&gt;&gt;},
 {default_permissions, [&lt;&lt;".*"&gt;&gt;, &lt;&lt;".*"&gt;&gt;, &lt;&lt;".*"&gt;&gt;]},
 {ssl_listeners, [5671]},
 {ssl_options, [{cacertfile,"/etc/rabbitmq/excert/example.com.ca-bundle"},
 {certfile,"/etc/rabbitmq/excert/example.com.crt"},
 {keyfile,"/etc/rabbitmq/excert/example.com.key"},
 {versions, ['tlsv1.2', 'tlsv1.1', 'tlsv1']},
 {verify,verify_peer},
 {fail_if_no_peer_cert,false}]},
 %%{cluster_nodes, [{disc,[rabbit@appa03]}, {ram,[rabbit@appa02,rabbit@appa01]}]},
 %%{cluster_name,&lt;&lt;"rabbit@appa03.example.com"&gt;&gt;},
 {partitions,[]}
 ]
 },
 {kernel,
 []
 },
 {rabbitmq_management,
 [{listener, [{port, 15671},
 {ssl, true},
 {ssl_opts, [{cacertfile, "/etc/rabbitmq/excert/example.com.ca-bundle"},
 {certfile, "/etc/rabbitmq/excert/example.com.crt"},
 {keyfile, "/etc/rabbitmq/excert/example.com.key"}
 ]}
 ]}]
 },
 {rabbitmq_shovel,
 [{shovels,
 []
 }]
 },
 {rabbitmq_stomp,
 []
 },
 {rabbitmq_mqtt,
 []
 },
 {rabbitmq_amqp1_0,
 []
 },
 {rabbitmq_auth_backend_ldap,
 []
 }

].

</pre>
&nbsp;
<pre>&gt; service rabbitmq-server start
&gt; rabbitmqctl cluster_status
Cluster status of node rabbit@appa01 ...
[{nodes,[{disc,[rabbit@appa01]},
 {ram,[rabbit@appa02,rabbit@appa01]}]},
 {running_nodes,[rabbit@appa02,rabbit@appa01,rabbit@appa03]},
 {cluster_name,&lt;&lt;"rabbit@appa01.example.com"&gt;&gt;},
 {partitions,[]}]

</pre>
<h2>Setup Users and permissions</h2>
I dedicated one server to be the "true" master of the cluster where I launch all of my admin type commands from.
<pre>&gt; rabbitmqctl add_user username password
&gt; rabbitmqctl list_users
&gt; rabbitmqctl set_user_tags username administrator
&gt; rabbitmqctl authenticate_user username password
&gt; rabbitmqctl set_permissions -p / username "^username-.*" ".*" ".*"
&gt; rabbitmqctl add_vhost test #one can segregate messages into different vhosts \
   within RabbitMQ
&gt; rabbitmqctl set_permissions -p test username ".*" ".*" ".*"
&gt; rabbitmqctl list_bindings
#now make a 2nd user that is NOT an administrator that will be used in applications
to submit and listen for messages
&gt; rabbitmqctl add_user execute password
&gt; rabbitmqctl set_permissions -p test execute ".*" ".*" ".*"

#install rabbitmq_management plugin to give yourself a nice plugin
&gt; rabbitmq-plugins enable rabbitmq_management
now navigate to https://appa01.example.com:15671/ You must enable this on every
host in the cluster.

</pre>
<h2><span id="Now_the_Fun_begins" class="mw-headline">Now the Fun begins</span></h2>
An example of a remote task execution queue made with Python and RabbitMQ. This was a working example, and was being developed to superseded the <a href="https://twstewart84.wordpress.com/systems-administration/apache-mesos-apis/">Apache Mesos/Singularity API</a>. One thing I would really recommend building, is a task evaluate, so if perhaps a nasty message like 'rm-rf /' gets put into the data stream the system would no to ignore that message, but that would take a bit more intelligence than the example displayed below.
<h3><span id="runtask.py" class="mw-headline">runtask.py</span></h3>
<pre>#!/usr/bin/evn python
from __future__ import absolute_import
import subprocess

def demote(user_uid, user_gid):
   '<a href="http://stackoverflow.com/questions/1770209/run-child-processes-as-different-user-from-a-long-running-process">Demote</a> task to run as non-root user'
   def result():
       print('starting demotion')
       os.setgid(user_gid)
       os.setuid(user_uid)
       print('finished demotion')
   return result

class Tasker:
        'Sets up task to run on host'

        def __init__(self, uid, taskstr):
                self.uid = uid
                self.taskstr = taskstr

        def task_do(self):
                gid = 1005
                uid = 1005
                print self.uid, self.taskstr
                run_task = subprocess.Popen([self.taskstr], 
                   preexec_fn=demote(uid, gid), shell=True, stdout=subprocess.PIPE)
                taskout, taskerr = run_task.communicate()
                print taskout, taskerr

</pre>
<h3><span id="rpc_server.py" class="mw-headline">rpc_server.py</span></h3>
<pre>#!/usr/bin/env python
import pika
from runtask import Tasker

credentails = pika.PlainCredentials('execute', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='appa01', port=5672, credentials=credentails, virtual_host='test'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
        if n == 0:
                return 0
        elif n == 1:
                return 1
        else:
                return fib(n-1) + fib(n-2)

def on_request(ch, method, props, body):
        #n = int(body)

        if body == 'fib':
                n = sum(c != ' ' for c in body)
                print(" [.] fib(%s)" % n)

                response = fib(n)
        else:
                print " [x] Received %r" % (body,)
                print " uuid %r: " % (props.correlation_id,)
                response = Tasker(props.correlation_id, body)
                #response = Tasker(12345, body)
                response.task_do()
                print(" [x] Done")

        ch.basic_publish(exchange='',routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = \
          props.correlation_id),body=str(response))
        ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()

</pre>
In a 2nd session launch the message listener:
<pre>&gt;  python rpc_server.py
 [x] Awaiting RPC requests
</pre>
<h3><span id="rpc_client.py" class="mw-headline">rpc_client.py</span></h3>
<pre>#!/usr/bin/env python
import pika
import uuid
import sys

class RpcClient(object):
    def __init__(self):
        credentails = pika.PlainCredentials('execute', 'password')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                 host='appa01', port=5672, credentials=credentails, virtual_host='test'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

def main():
    parser = argparse.ArgumentParser(description="Submits task with UID")
    parser.add_argument('-u', dest='uid', type=str, help='Unique Identifier for task')
    parser.add_argument('-t', dest='task', type=str, help='Task to be ran')
    args = parser.parse_args()

    if args.uid is None:
          uid = str(uuid.uuid4())
    else:
          uid = args.uid

    if args.task is None:
          message = "echo Hello World"
    else:
          message = args.task
   
    rpc = RpcClient()
    print(" [x] Requesting rpc")
    response = rpc.call(message, uid)
    print(" [.] Got %r" % response)

if __name__ == '__main__':
 main()

</pre>
<pre> &gt; python rpc_client.py -u 1287198319hfwhdfa -t "ping -c 4 8.8.8.8"
 [x] Requesting rpc
</pre>
Now in the 2nd window that is listening for tasks
<pre>[x] Received 'ping -c 4 8.8.8.8'
 uuid '1287198319hfwhdfa':
 1287198319hfwhdfa ping -c 4 8.8.8.8
 PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
 64 bytes from 8.8.8.8: icmp_seq=1 ttl=53 time=24.0 ms
 64 bytes from 8.8.8.8: icmp_seq=2 ttl=53 time=23.6 ms
 64 bytes from 8.8.8.8: icmp_seq=3 ttl=53 time=23.6 ms
 64 bytes from 8.8.8.8: icmp_seq=4 ttl=53 time=23.7 ms
 
 --- 8.8.8.8 ping statistics ---
 4 packets transmitted, 4 received, 0% packet loss, time 3028ms
 rtt min/avg/max/mdev = 23.689/23.803/24.046/0.145 ms
 [x] Done
</pre>
Client receives response that task was completed, and exits
<pre> &gt; python rpc_client.py -u 1287198319hfwhdfa -t "ping -c 4 8.8.8.8"
 [x] Requesting rpc
 [.] Got '&lt;runtask.Tasker instance at 0x1dcf2d8&gt;'
 &gt;
</pre>
<h2>Celery</h2>
The <a href="http://docs.celeryproject.org/en/latest/index.html">celery plugin</a> allows for pluralization of task execution over many RabbitMQ nodes.
<pre>#on all hosts
&gt; pip install celery
#on workere nodes
&gt; cd /work/
&gt; mkdir proj
&gt; touch proj/__init__.py
&gt; vim proj/celery.py
###
from __future__ import absolute_import
from celery import Celery

app = Celery('tasks', broker='amqp://execute:password@appa01:5672/test', 
backend='amqp://execute:password@appa01:5672//', include=['proj.tasks'])

app.conf.update(
 CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
 app.start()
###

&gt; vim proj/tasks.py
####
from __future__ import absolute_import
from proj.celery import app

@app.task
def add(x, y):
   z = x + y
   return z

@app.task
def mul(x, y):
   z = x * y
   return z

@app.task
def diff(x, y):
   z = x - y
   return z
#####

&gt; celery multi start w2 -A proj -l info
#on 1 master node, w2 is name of worker make this unique for each node/worker, 
can have multiple workers on a machine if so desired.
&gt; <a href="https://github.com/mher/flower">pip install flower</a>
#flower is a managment interface for celery and makes it easier to view if tasks 
are being completed properly.
&gt; vim celery_flower_www_server_start
+ #!/bin/sh
+ celery flower --broker=amqp://execute:passwprd@appa01:5672/test \
   --address=10.0.0.[eth0] &amp;
&gt; ./celery_flower_www_server_start
http://appa01:5555/dashboard
&gt;vim celery_task.py
####
#!/usr/bin/python
from celery import Celery
from proj.tasks import *

app = Celery('tasks', broker='amqp://execute:password@appa01:5672/test')

x = 4
y = 4
res = mul.delay(x, y)

res.get()
print res.state
&gt; python celery_task.py #will submit mul to celery cluster for execution. 
#remember the mul function is actually in proj/tasks.py</pre>