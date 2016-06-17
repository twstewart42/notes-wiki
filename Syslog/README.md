<!-- start content -->
<div id="mw-content-text" class="mw-content-ltr" dir="ltr" lang="en">
<div id="toc" class="toc">

And other logging programs like logrotate and LogWatch. Obviously there are much better and newer logging platform like ELK stack and graylog but this is good if you like a report each morning containing all the logs for specific machines.
<h2><span id="Configuration" class="mw-headline">Configuration</span></h2>
<h3><span id="DNS" class="mw-headline">DNS</span></h3>
DNS should be configured to provide CNAME records for <tt>loghost</tt> or <tt>log</tt> that reference the collectors.
<h3><span id="Collector" class="mw-headline">Collector</span></h3>
A collector must be configured to listen for incoming IP traffic on port 514.
<h3><span id="Device" class="mw-headline">Device</span></h3>
A device must be configured to send messages to <tt>loghost</tt> or <tt>log</tt>, as configured in DNS.
<h2><span id="Setup_on_bfesyslog001" class="mw-headline">Setup on log001</span></h2>
A CentOS 7 server
<pre>vim /etc/rsyslog.conf
##added these lines
#apc monitoring
local3.*                                                /var/log/apc.log
# switch
local5.*                                                /var/log/switch
#IBM 10GB switch
local4.*                                                /var/log/10gig
if $hostname == 'web001' then /var/log/web001
if $hostname == 'web002' then /var/log/web002
if $hostname == 'mail001' then /var/log/mailserver
if $hostname == 'sql001' then /var/log/sql001

then I went to all of the apc devices, 10gig switch and switch and configured 
them to send logs to the local# at 10.0.0[log001]:514
</pre>
<pre>#on remote machines, send logs to log001 

vim /etc/syslog

add the line
*.info;local5.none;mail.none;authpriv.none;cron.none    @log001.zedxinc.com

</pre>
<h2><span id="Logrotate" class="mw-headline">Logrotate</span></h2>
I also tweaked logrotate on log001 to compress logs and delete them after 30 days
<pre>Vim /etc/logrotate.d/syslog
/var/log/cron
/var/log/maillog
/var/log/messages
/var/log/secure
/var/log/spooler
/var/log/apc.log
/var/log/switch
/var/log/bladecenter
/var/log/10gig
/var/log/mailserver
/var/log/web001
/var/log/web001
/var/log/sql001
{
    sharedscripts
    postrotate
    compress
    maxage 15
        /bin/kill -HUP `cat /var/run/syslogd.pid 2&gt; /dev/null` 2&gt; /dev/null || true
    endscript
}

</pre>
&nbsp;
<h2><span id="LogWatch" class="mw-headline">LogWatch</span></h2>
I needed LogWatch to be able to analyze to following log files. As logWatch would only report on standard cron, mailog, messages, secure, and spooler.
<pre>/var/log/cron
/var/log/maillog
/var/log/messages
/var/log/secure
/var/log/spooler
/var/log/apc.log
/var/log/switch
/var/log/bladecenter
/var/log/10gig
/var/log/mailserver
/var/log/web001
/var/log/web002
/var/log/sql002
</pre>
<pre>create a configuration file for the specific log
cd /etc/logwatch
vim conf/logfiles/bladecenter.conf

##LogFile conf for bladecenter
LogFile = /var/log/bladecenter

Archive = bladecenter-*.gz

# Expand the repeats (actually just removes them now)
 *ExpandRepeats
############
</pre>
<pre>configure a file for the service which will do the parsing of the logs.
cd /etc/logwatch
vim conf/services/bladecenter.conf

###LogWatch service for IBM Bladecenter

Title = "IBM Bladecenter logs"

LogFile = bladecenter

########
</pre>
<pre>configure script of some sort to parse log file and only report on relevant information
cd /etc/logwatch
vim scripts/services/bladecenter

#!/usr/bin/env bash
# /etc/logwatch/scripts/services/bladecenter

# Change the line separator to split by new lines.
OLD_IFS=$IFS
IFS=$'\n'
LogFile=/var/log/bladecenter

# The contents of the log file are given in stdin.
for LINE in $( cat $LogFile ); do

    # Only lines matching this regexp will be included. can add debug, info, notice for testing
    if echo "$LINE" |egrep 'WARNING|ERROR|CRITICAL|ALERT|EMERGENCY' &amp;&gt; /dev/null; then

        # Every line we echo here will be included in the logwatch report.
        echo "$LINE"

    fi

done

IFS=$OLD_IFS
#################

</pre>
repeat as necessary for each logfile you want to have LogWatch report on. If there are no relevant logs in the logfiles to be reported on than that section will be ignored and not included in the cron.daily email report.

&nbsp;

</div>
<h2><span id="Protocol" class="mw-headline">Protocol</span></h2>
The BSD syslog protocol<sup id="cite_ref-RFC3164_1-0" class="reference"><a href="http://bfesysapp001.zedxinc.com/wiki/index.php?title=Syslog&amp;printable=yes#cite_note-RFC3164-1">[1]</a></sup> defines three types of hosts: <i>collector</i>, <i>device</i>, and <i>relay</i>. A device emits messages, a collector receives messages, and a relay receives messages and forwards them to a collector or relay.

Messages are transmitted via UDP; thus, syslog is an unreliable protocol, and may suffer from lost messages during high load on a collector or relay or network congestion.

A syslog message contains the following parts:

<dl><dt><tt>PRI</tt></dt><dd>priority; decimal representation of <tt><i>facility</i> &lt;&lt; 3 | <i>severity</i></tt> enclosed in angle brackets</dd><dt><tt>HEADER</tt></dt><dd>header

<dl><dt><tt>TIMESTAMP</tt></dt><dd>the date and time when the message was created</dd><dt><tt>HOSTNAME</tt></dt><dd>the hostname of the machine that sent the message as determined by the machine that receives the message</dd></dl></dd></dl><dl><dt><tt>MSG</tt></dt><dd>message

<dl><dt><tt>TAG</tt></dt><dd>the name of the process that created the message</dd><dt><tt>CONTENT</tt></dt><dd>message content</dd></dl></dd></dl>
<h3><span id="Facilities" class="mw-headline">Facilities</span></h3>
<table class="toc" width="100%">
<tbody>
<tr>
<th width="25%">Code</th>
<th width="75%">Facility</th>
</tr>
<tr>
<td>0</td>
<td>kernel messages</td>
</tr>
<tr>
<td>1</td>
<td>user-level messages</td>
</tr>
<tr>
<td>2</td>
<td>mail system</td>
</tr>
<tr>
<td>3</td>
<td>system daemons</td>
</tr>
<tr>
<td>4</td>
<td>security/authorization messages<sup>1</sup></td>
</tr>
<tr>
<td>5</td>
<td>messages generated internally by syslogd</td>
</tr>
<tr>
<td>6</td>
<td>line printer subsystem</td>
</tr>
<tr>
<td>7</td>
<td>network news subsystem</td>
</tr>
<tr>
<td>8</td>
<td>UUCP subsystem</td>
</tr>
<tr>
<td>9</td>
<td>clock daemon<sup>2</sup></td>
</tr>
<tr>
<td>10</td>
<td>security/authorization messages<sup>1</sup></td>
</tr>
<tr>
<td>11</td>
<td>FTP daemon</td>
</tr>
<tr>
<td>12</td>
<td>NTP subsystem</td>
</tr>
<tr>
<td>13</td>
<td>log audit<sup>1</sup></td>
</tr>
<tr>
<td>14</td>
<td>log alert<sup>1</sup></td>
</tr>
<tr>
<td>15</td>
<td>clock daemon<sup>2</sup></td>
</tr>
<tr>
<td>16</td>
<td>local use 0 (local0)</td>
</tr>
<tr>
<td>17</td>
<td>local use 1 (local1)</td>
</tr>
<tr>
<td>18</td>
<td>local use 2 (local2)</td>
</tr>
<tr>
<td>19</td>
<td>local use 3 (local3)</td>
</tr>
<tr>
<td>20</td>
<td>local use 4 (local4)</td>
</tr>
<tr>
<td>21</td>
<td>local use 5 (local5)</td>
</tr>
<tr>
<td>22</td>
<td>local use 6 (local6)</td>
</tr>
<tr>
<td>23</td>
<td>local use 7 (local7)</td>
</tr>
</tbody>
</table>
<ol>
	<li>Various operating systems have been found to utilize Facilities 4, 10, 13 and 14 for security/authorization, audit, and alert messages which seem to be similar.</li>
	<li>Various operating systems have been found to utilize both Facilities 9 and 15 for clock (cron/at) messages.</li>
</ol>
<h3><span id="Severities" class="mw-headline">Severities</span></h3>
<table class="toc" width="100%">
<tbody>
<tr>
<th width="25%">Code</th>
<th width="25%">Severity</th>
<th width="50%">Description</th>
</tr>
<tr>
<td>0</td>
<td>Emergency</td>
<td>system is unusable</td>
</tr>
<tr>
<td>1</td>
<td>Alert</td>
<td>action must be taken immediately</td>
</tr>
<tr>
<td>2</td>
<td>Critical</td>
<td>critical conditions</td>
</tr>
<tr>
<td>3</td>
<td>Error</td>
<td>error conditions</td>
</tr>
<tr>
<td>4</td>
<td>Warning</td>
<td>warning conditions</td>
</tr>
<tr>
<td>5</td>
<td>Notice</td>
<td>normal but significant condition</td>
</tr>
<tr>
<td>6</td>
<td>Informational</td>
<td>informational messages</td>
</tr>
<tr>
<td>7</td>
<td>Debug</td>
<td>debug-level message</td>
</tr>
</tbody>
</table>
<h2><span id="References" class="mw-headline">References</span></h2>
<ol class="references">
	<li id="cite_note-RFC3164-1"><span class="mw-cite-backlink"><a href="http://bfesysapp001.zedxinc.com/wiki/index.php?title=Syslog&amp;printable=yes#cite_ref-RFC3164_1-0"><span class="cite-accessibility-label">Jump up </span>↑</a></span> <span class="reference-text">Lonvick, C. The BSD syslog Protocol. IETF <a class="external mw-magiclink-rfc" href="http://tools.ietf.org/html/rfc3164" rel="nofollow">RFC 3164</a>. August 2001.</span></li>
</ol>
</div>