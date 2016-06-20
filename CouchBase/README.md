<h1>CouchBase</h1>

<h3>Server install</h3>
Turn off THP:
<pre>
/usr/local/sbin/THP.sh
#!/bin/sh
for i in /sys/kernel/mm/*transparent_hugepage/enabled; do
 echo never > $i;
done
for i in /sys/kernel/mm/*transparent_hugepage/defrag; do
 echo never > $i;
done
# Add script to /etc/rc.local file to run at startup reboot
</pre>

<h3>SETUP:</h3>
<pre>
wget http://packages.couchbase.com/releases/4.1.0-dp/couchbase-server-4.1.0-dp-centos7.x86_64.rpm
rpm -Uvh couchbase-server-4.1.0-dp-centos7.x86_64.rpm
</pre>
navigate to http://FQDN:8091/ and join node to cluster or start new cluster

saslauthd install/setup
<pre>
yum install cyrus-sasl cyrus-sasl-devel openssl
vim /etc/sysconfig/saslauthd
 -  MECH=pam
 + MECH=ldap
vim /etc/saslauthd.conf
 + ldap_servers: ldaps://ldap01.example.com:636, ldaps://ldap02.example.com:636
 + ldap_search_base: cn=users,cn=accounts,dc=example,dc=com
 + ldap_bind_db: uid=ldapsvc,cn=users,cn=accounts,dc=example,dc=com
 + ldap_password: fakepassword
cp /etc/saslauthd.conf /usr/local/etc/
ln -s /var/run/saslauthd /var/run/sasl2/
systemctl restart saslauthd
testsaslauthd -u user123 -p hunter2 -f /var/run/saslauthd/mux
 0: OK "Success."
</pre>


Read this first to understand couchbase's architecture and concepts: http://developer.couchbase.com/documentation/server/4.1/concepts/concepts-architecture-intro.html

<h3>Client Setup</h3>
Install CBC
<pre>
wget http://packages.couchbase.com/clients/c/couchbase-csdk-setup $ perl couchbase-csdk-setup
</pre>
  cbc n1ql 'SELECT * from `travel-sample` limit 1'

cbc works for basic querying but where this really gets powerful is its ability to pass in unstructured json documents. Below is an example written in python, they have "connectors" for most of the major languages, php, perl, C, and more.

<pre>
yum install python-devel python-pip gcc
pip install couchbase
</pre>
<h4>Test</h4>
  python -c 'import couchbase' # if return 0 then good to go

Basic upsert script, this can be extended to insert variables grabed from different sources, this is only a basic example.

<pre>
from couchbase.bucket import Bucket
from couchbase.exceptions import CouchbaseError

cb = Bucket('couchbase://machine1,machine2/DOC_EXAMPLE')
cb.upsert('"$loc_id"_"$day"', {'location': '"$loc_id"', 'country': 'CA',  'geo': {
                    'alt': 100,
                    'lat': 77.8486,
                    'lon': 40.8492
                }, 'zxid': '"$loc_id"_"$day"','uuid':'"$uuid"','date':  '"$day"',
'Weather':{ 'tmpa':2.45, 'tmpn':'-2.2','tmpx':5.0,'wdra':10, 'wesda':1.5, })
</pre>

<pre>
cbc n1ql 'SELECT *  from`default` where id=16801'
Encoded query: {"statement":"SELECT *  from`default` where id=16801"}
{
            "default": {
                "airportname": "University Park  Airport",
                "city": "State College",
                "country": "USA",
                "faa": "UPA",
                "geo": {
                    "alt": 100,
                    "lat": 77.8486,
                    "lon": 40.8492
                },
                "icao": "UPSCA",
                "id": 16801,
                "type": "airport",
                "tz": "America/New_York"
            }
        },
** N1QL Response finished
{
    "requestID": "336bb403-d8f6-4954-a7f4-49f46d058ea9",
    "signature": {
        "*": "*"
    },
    "results": [
        ],
    "status": "success",
    "metrics": {
        "elapsedTime": "17.007119ms",
        "executionTime": "16.937338ms",
        "resultCount": 1,
        "resultSize": 499
    }
}
</pre>


Other types of N1QL queries one can write, very much like mysql/postgres queries.
<pre>
cbc n1ql 'select Weather.tmpx from `DOC_EXAMPLE` where loc=2 limit 1' -U couchbase://machine1,machine2/DOC_EXAMPLE

cbc n1ql 'select zxid, Weather.* from `DOC_EXAMPLE` where date="20151212" ' -U couchbase://machine1,machine2/DOC_EXAMPLE

cbc n1ql 'update `DOC_EXAMPLE` set Weather.tmpx=5.40 where date="20151212" ' -U couchbase://machine1,machine2/DOC_EXAMPLE
</pre>