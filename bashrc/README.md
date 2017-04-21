
<h1>bashrc</h1>

<p>Some parts of my bashrc file that I use to alias simple keystrokes into very powerful commands. Some I have borrowed from examples online. I use a mix of special functions and aliases to help increase my speed when trying to figure out an issue.</p>
<h2>ENV</h2>
<p>Setup basic user env information to help inform commonly used programs, paths, etc.</p>
<pre>export SVN_EDITOR=vim
export PATH=/nfs/user_home/scripts:/nfs/user_home/bin:$PATH</pre>
<h2>Sign in</h2>
<p>When I sign into a server I immediately like to see a report of basic system info/stats, and also know that my .bashrc file was correctly loaded</p>
<pre>#this is at the very end of my ~/.bashrc file
cv() { cat /etc/redhat-release ;}
function machine()
{
 echo -e "\nMachine information:" ; uname -a; cv;
 echo -e "\nUsers logged on:" ; w -h
 echo -e "\nCurrent date :" ; date
 echo -e "\nMachine status :" ; uptime
 echo -e "\nMemory status :" ; free
 echo -e "\nFilesystem status :"; df -hl
}
echo "Welcome to $HOSTNAME, $USER"
echo "$(machine)"
echo "All Settings are a go! DO NOT PANIC!"</pre>
<h2>Set terminal colors</h2>
<p>I have putty set to default white background with black letters, I find it much easier to read than the defaults, the color settings below are mostly for fun and show.</p>
<pre>#Color
#Set variables for foreground colors
fgRed=$(tput setaf 2) ; fgGreen=$(tput setaf 2) ; fgBlue='\e[0;34m' ;
fgMagenta='\e[1;35m' ; fgYellow='\e[0;33m' ; fgCyan=$(tput setaf 5) ;
fgWhite='\e[1;37m' ; fgBlack='\e[0;90m' ; fgText='\e[0;90m' ;
#Set variables for background colors
bgRed='\e[1;101m' ; bgGreen='\e[0;32m' ; bgBlue='\e[0;34m' ;
bgMagenta='\e[0;35m' ; bgYellow='\e[1;33m' ; bgCyan='\e[1;36m' ;
bgWhite='\e[0m' ; bgBlack=$(tput setab 4) ;

#Set variables for font weight and text decoration
B=$(tput bold) ; U=$(tput smul) ; C=$(tput sgr0) ; X=$(tput smso);
#NOTE: ${C} clears the current formatting

if [[ $USER = "root" ]]; then
   PS1="\[\e[1;35m\]\A\[\e[m\] \[\e[1;34m\]\u@\h &gt;\[\e[m\] \[\e[0;31m\]"
else
   PS1="\[\033\$(if [[ \$? == 0 ]]; then echo \"\[\033[01;32m\]|;)\"; else echo \"\[\033[01;31m\]|;(\"; fi) $(if [[ ${EUID} == 0 ]]; then echo '\[\033[1;35m\]\A\[\e[m\] \[\e[1;34m\]\u@\h'; else echo '\[\033[1;35m\]\A\[\e[m\] \[\e[1;34m\]\u@\h'; fi)\[\033[01;34m\] \w &gt;\[\e[\033[0m\] "
   #add ${C} to line above to end background color

fi

</pre>
<p><strong><span style="color:#00ff00;">|;)</span> <span style="color:#ff00ff;">08:20</span> <span style="color:#0000ff;">me@web001 ~ &gt;</span></strong> #if the last command returns anything other than exit(0) the green smiley face will turn into a red frowny face.</p>
<p><strong><span style="color:#ff0000;">|;(</span> <span style="color:#ff00ff;">08:20</span> <span style="color:#0000ff;">me@web001 ~ &gt;</span></strong></p>
<h2>Test Mail</h2>
<p>Test that sendmail is working on the server</p>
<pre>testmail() { echo "test from $HOSTNAME"| mail -s "TEST MAIL"  me@mail.com ;}</pre>
<h2>PANIC</h2>
<p>Shut off the NIC if one believes the server to be compromised.</p>
<pre>PANIC() {
 echo "You said to PANIC"
 echo "Sending alert"
 echo "Something bad has occured and $USER is intervening on $HOSTNAME \n \ 
 $USER is shutting off network access"| mail -s "$HOSTNAME has been taken \ 
 offline" me@mail.com
 echo "Shutting off network access"
 ifdown -a

}</pre>
<h2>Try</h2>
<p>try a command, and alert if failed</p>
<pre>yell() { echo "$0: $*" &gt;&amp;2; echo "$@ failed with exit code $?"| \ 
       mail -s "TEST FAIL" me@mail.com ;}
die() { yell "$*"; exit 111; }
try() { "$@" || die "cannot $*"; }</pre>
<p>&nbsp;</p>
<h2>Extract</h2>
<p>Tired of remembering if you should gunzip or tar -xvzf a file, this takes away all of that confusion. I did not come up with this one, <a href="http://www.tldp.org/LDP/abs/html/sample-bashrc.html">I found it here</a>.</p>
<pre>extract() {
    if [ -z "$1" ]; then
       # display usage if no parameters given
       echo "Usage: extract &lt;path/file_name&gt;.&lt;zip|rar|bz2|gz|tar|tbz2|tgz|Z|7z|xz|ex|tar.bz2|tar.gz|tar.xz&gt;"
    else
       if [ -f $1 ] ; then
          NAME=${1%.*}
          mkdir $NAME &amp;&amp; cd $NAME
          case $1 in
              *.tar.bz2) tar xvjf ../$1 ;;
              *.tar.gz) tar xvzf ../$1 ;;
              *.tar.xz) tar xvJf ../$1 ;;
              *.lzma) unlzma ../$1 ;;
              *.bz2) bunzip2 ../$1 ;;
              *.rar) unrar x -ad ../$1 ;;
              *.gz) gunzip ../$1 ;;
              *.tar) tar xvf ../$1 ;;
              *.tbz2) tar xvjf ../$1 ;;
              *.tgz) tar xvzf ../$1 ;;
              *.zip) unzip ../$1 ;;
              *.Z) uncompress ../$1 ;;
              *.7z) 7z x ../$1 ;;
              *.xz) unxz ../$1 ;;
              *.exe) cabextract ../$1 ;;
              *) echo "extract: '$1' - unknown archive method" ;;
               esac
        else
            echo "$1 - file does not exist"
        fi
  fi
}</pre>
<p>&nbsp;</p>
<h2>alias list</h2>
<pre># User specific aliases
mcd() { mkdir -pv $1 &amp;&amp; cd $1 ;}
cls() { cd "$1"; ls; }
backup() { cp "$1"{,.bak};}
#keyboard mistypes
alias sl='ls'
alias ll='ls -lha'
alias kk=ll
alias xs='cd'
alias vf='cd'
#sudo access
alias sv='sudo vim'
alias sd='sudo'
alias do='sudo'
alias suu='sudo su -'
alias root=suu
#look back
alias c='clear'
alias h='history'
alias histg='history | grep'
alias hg=histg
#processes and files
alias ps?='ps aux | grep'
alias psf='ps fax'
alias findp='sudo find . -type f -mmin +720 -print'
alias finddel='sudo find . -type f -mmin +720 -delete'
alias cdl='cd "$@" &amp;&amp; ls -al'
alias cdh='cd ~'
alias ..='cd ..'
alias ...='cd ../../'
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias mkdir='mkdir -pv'
alias now='date +"%T"'
alias nowtime=now
alias nowdate='date +"%d-%m-%Y"'
#networking
alias ports='netstat -tulanp'
alias iptlist='sudo /sbin/iptables -L -n -v --line-numbers'
alias iptlistin='sudo /sbin/iptables -L INPUT -n -v --line-numbers'
alias iptlistout='sudo /sbin/iptables -L OUTPUT -n -v --line-numbers'
alias iptlistfw='sudo /sbin/iptables -L FORWARD -n -v --line-numbers'
alias firewall=iptlist
alias listen="sudo lsof -P -i -n"
alias lso80='sudo lsof -i :80'
alias lso443='sudo lsof -i :443'
alias lso25='sudo lsof -i :25'
alias lso3306='sudo lsof -i :3306'
alias lso5432='sudo lsof -i :5432'
alias cmount='mount | column -t'
#other
alias install='sudo yum install'
alias update='sudo yum update'
alias updatey='sudo yum -y update'
alias meminfo='free -m -l -t'
alias bashrc='vim ~/.bashrc &amp;&amp; source ~/.bashrc'
alias get_alias='cat ~/.bashrc | grep alias'

alias fuck='shutdown -h now'
alias fucker='reboot'
alias busy='cat /dev/urandom | hexdump -C | grep "ca fe"'
alias genpasswd="strings /dev/urandom | grep -o '[[:alnum:]]' | head -n 15 | tr -d '\n'; echo"
alias tree="ls -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/ /' -e 's/-/|/'"</pre>
<p>&nbsp;</p>
<p>&nbsp;</p>
