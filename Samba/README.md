# Samba
"Samba is Free Software licensed under the GNU General Public License, the Samba project is a member of the Software Freedom Conservancy.

Since 1992, Samba has provided secure, stable and fast file and print services for all clients using the SMB/CIFS protocol, such as all versions of DOS and Windows, OS/2, Linux and many others.

Samba is an important component to seamlessly integrate Linux/Unix Servers and Desktops into Active Directory environments. It can function both as a domain controller or as a regular domain member."

## Links

- <a href=https://www.samba.org/>Main Website</a>
- <a href=https://support.microsoft.com/en-us/kb/2696547>Fix for Windows 10 Clients</a>
- <a href=https://www.samba.org/samba/news/symlink_attack.html>No Symlinks aloud</a>


## Installation
All of this was done on a standard CentOS 7 install.

    yum install samba-4.1 samba-client samba-common samba-libs
    

Make the smb.conf match the following settings
<pre>
        workgroup = EXAMPLE
        server string = SMB EX Fileserver
        smb ports = 139
        oplocks = yes
        posix locking = no
        netbios name = smb01
        hosts allow = 10.0.0., 127.
        interfaces = lo 10.0.0.[S]/24
        max protocol = SMB3
        idmap config * : backend = ldapsam:ldap://ldap01.example.com
        follow symlinks = yes
        wide links = no
        socket options = TCP_NODELAY SO_RCVBUF=8192 SO_SNDBUF=8192
        username map = /etc/samba/smbusers
        security = ads
        realm = example.com
        password server = winad.example.com
        encrypt passwords = yes
</pre>
A single example of a smb/cifs share is below
<pre>
  [documentation]
        comment = Documentation Location
        path = /home/documentation
        valid users = @documentation
        force group = documentation
        writeable = yes
        create mask = 0777
        directory mask = 0777
</pre>
Users must exist in the local /etc/group file for permissions to work correctly. 
    gpasswd -a usern123 documentation

Any changes and there must be a full service restart, a reload does not appear to do anything. It took me a long time to realize this
  systemctl restart smb

## Connecting
### From Linux
Any machine with the samba-client software installed can be used to test connections.
<pre>
  > smbclient -L smb01 -U EXAMPLE/user123
  Enter EXAMPLE/user123's password:
  Domain=[EXAMPLE] OS=[Unix] Server=[Samba 4.1.12]
  
        Sharename       Type      Comment
        ---------       ----      -------
        vartmp          Disk      Local Disk Testing
        nfshome         Disk      Home Directories
        net-tmp         Disk      Backup/Temp directory
        documentation   Disk      Documentation Location
        systems         Disk      Administrative Shares
        IPC$            IPC       IPC Service (SMB EX Fileserver)
        user123        	Disk      Home directory of stewt318
  Domain=[EXAMPLE] OS=[Unix] Server=[Samba 4.1.12]
</pre>
### From Windows
Using Windows Explorer, navigate to \\smb01\, if things are configured correctly one should not have to enter their credentials, those should be forwarded by windows automatically! Always check that sensitive data is protected by correct user permissions as configured in the smb.conf.

### Windows 10
There seems to be some protocol mismatch that causes windows 10 to not be able to communicate properly with the Samba Server. The fix is to disable SMBv3 for the Windows 10 client. It will then use SMBv1 and those clients will now be able to access the shared resources.

Open power shell as an admin, execute the next 2 lines  
  
    sc.exe config lanmanworkstation depend= bowser/mrxsmb10/nsi
    sc.exe config mrxsmb20 start= disabled
  
Restart the machine, then test if the user/machine can access the shared samba drive

## Adding Users
The user must exist in AD and on ldap01. They should also be added to the local "Domain Users" group and any other groups that are pertinent to their job.

    gpasswd -a usern123 "Domain Users"


