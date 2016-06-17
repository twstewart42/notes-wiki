More for fun than actual system's administration, I was inspired by the <a href="http://www.toolswatch.org/2013/04/book-review-violent-python-a-cookbook-for-hackers-forensic-analysts-penetration-testers-and-security-engineers/">Violent Python</a> book and attempted writing my own encryption programs, <a href="https://en.wikipedia.org/wiki/Steganography">Steganography</a> programs, and some other scripts exploring other faucets of security.
<h2>scramble.py</h2>
This uses a very simply cipher list to translate each letter of a text file into a list of numbers, and is also able to de-scramable the cipher to translate back to English. If you understand that arrays start at 0, it is a very simply cipher, where the number at the index of the character matched within the array is used as the key for each character in the return file.
<pre>import os, sys

#text = raw_input("Write a phrase: ")
text_array = []
edit_array = []
new_array = []
de_array = []
#This could be in any order, to further obfuscate the pattern.
alpha = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', 
 '5', '6', '7', '8', '9', ' ', '\n', '.', ',', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
 'H', 'I', 'J', 'K', 'M', 'N', 'L', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X',
 'Y', 'Z', '-', '!', '@', '#', '$', '%', '^', '&amp;', '*', '(', ')', '[', ']', ';',
 ':', '&lt;', '&gt;', '?', '/', '\\', '|']


def scramble(text, filename):
   print text
   outFile = os.path.join(os.path.dirname(filename), "(scrambled)"+os.path.basename(filename)) 
   for l in text:
      text_array.append(l)
 
   edit_array = text_array
   print edit_array
 
   for c in edit_array:
       num = alpha.index(c)
       new_array.append(num)

   #print new_array
   clean = str(new_array)
   output = clean.translate(None, "[,]")
   print output
   oF = open(outFile, 'w')
   oF.write(output)

##descramble portion
def descramble(text):
   new_array = text.translate(None, "[,]")
   print "secret code: " + str(new_array)
   for d in new_array.split(' '):
   intd = int(d)
   index = alpha[intd]
   de_array.append(index)

   output = ''.join(de_array)
   print output

option = raw_input("Do you want to [S]cramble or [D]escramble? ")
if option == "scramble" or option == "S":
   file_scram = raw_input("name of file to scramble: ")
   f = open(file_scram, 'r')
   text = f.read()
   scramble(text, file_scram)
elif option == "descramble" or option == "D":
   file_scram = raw_input("name of the file to descramble: ")
   F = open(file_scram, 'r')
   text = []
   text = F.read()
   descramble(text)
else:
 sys.exit(0)

</pre>
<pre>&gt;dir
README.txt scramble.py
&gt;python scramble.py
Do you want to [S]cramble or [D]escramble? S
name of file to scramble: README.txt
Try to crack the very simple code without using the descrambler - scramble.py. Have fun!
['T', 'r', 'y', ' ', 't', 'o', ' ', 'c', 'r', 'a', 'c', 'k', ' ', 't', 'h', 'e', ' ', 'v', 'e', 'r', 'y', ' ', 's', 'i', 'm', 'p', 'l', 'e', ' ', 'c', 'o', 'd', 'e', ' ', 'w', 'i', 't', 'h', 'o', 'u', 't', ' ', 'u', 's', 'i', 'n', 'g', ' ', 't', 'h', 'e', ' ', 'd', 'e', 's', 'c', 'r', 'a', 'm', 'b', 'l', 'e', 'r', ' ', '-', ' ', 's', 'c', 'r', 'a', 'm', 'b', 'l', 'e', '.', 'p', 'y', '.', ' ', 'H', 'a', 'v', 'e', ' ', 'f', 'u', 'n', '!']
59 17 24 36 19 14 36 2 17 0 2 10 36 19 7 4 36 21 4 17 24 36 18 8 12 15 11 4 36 2 14 3 4 36 22 8 19 7 14 20 19 36 20 18 8 13 6 36 19 7 4 36 3 4 18 2 17 0 12 1 11 4 17 36 65 36 18 2 17 0 12 1 11 4 38 15 24 38 36 47 0 21 4 36 5 20 13 66
&gt;dir
(scrambled)README.txt README.txt scramble.py
&gt;cat (scrambled)README.txt
59 17 24 36 19 14 36 2 17 0 2 10 36 19 7 4 36 21 4 17 24 36 18 8 12 15 11 4 36 2 14 3 4 36 22 8 19 7 14 20 19 36 20 18 8 13 6 36 19 7 4 36 3 4 18 2 17 0 12 1 11 4 17 36 65 36 18 2 17 0 12 1 11 4 38 15 24 38 36 47 0 21 4 36 5 20 13 66
&gt;python scramble.py
Do you want to [S]cramble or [D]escramble? D
name of the file to descramble: (scrambled)README.txt
secret code: 59 17 24 36 19 14 36 2 17 0 2 10 36 19 7 4 36 21 4 17 24 36 18 8 12 15 11 4 36 2 14 3 4 36 22 8 19 7 14 20 19 36 20 18 8 13 6 36 19 7 4 36 3 4 18 2 17 0 12 1 11 4 17 36 65 36 18 2 17 0 12 1 11 4 38 15 24 38 36 47 0 21 4 36 5 20 13 66
Try to crack the very simple code without using the descrambler - scramble.py. Have fun!

</pre>
&nbsp;
<h2>encryptor.py</h2>
This uses AES + a passphrase to encrypt every file within a directory.
<pre>#install Python2.7
#pip install pycrypto
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random, sys

def encrypt(key, filename):
   chunksize = 64 * 1024
   outFile = os.path.join(os.path.dirname(filename), "(encrypted)"+os.path.basename(filename))
   filesize = str(os.path.getsize(filename)).zfill(16)
   IV = ''
 
   for i in range(16):
       IV += chr(random.randint(0, 0xFF))
 
       encryptor = AES.new(key, AES.MODE_CBC, IV)
 
       with open(filename, "rb") as infile:
       with open(outFile, "wb") as outfile:
       outfile.write(filesize)
       outfile.write(IV)
       while True:
           chunk = infile.read(chunksize)
 
           if len(chunk) == 0:
               break
 
           elif len(chunk) % 16 !=0:
               chunk += ' ' * (16 - (len(chunk) % 16))
 
           outfile.write(encryptor.encrypt(chunk))
 
def decrypt(key, filename):
    outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[11:]))
    chunksize = 64 * 1024
    with open(filename, "rb") as infile:
    filesize = infile.read(16)
    IV = infile.read(16)
 
    decryptor = AES.new(key, AES.MODE_CBC, IV)
 
    with open(outFile, "wb") as outfile:
         while True:
             ch unk = infile.read(chunksize)
             if len(chunk) == 0:
                 break
 
             outfile.write(decryptor.decrypt(chunk))
 
         outfile.truncate(int(filesize))
 
def allfiles():
   allFiles = []
   for root, subfiles, files in os.walk(os.getcwd()):
       for names in files:
           allFiles.append(os.path.join(root, names))
  
    return allFiles

choice = raw_input("Do you want to (E)ncrypt or (D)ecrypt? ")
password = raw_input("Enter the password: ")

encFiles = allfiles()

if choice == "E":
   for Tfiles in encFiles:
       if os.path.basename(Tfiles).startswith("(encrypted)"):
           print "%s is already encrypted" %str(Tfiles)
           pass
 
       elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
            pass
       else:
            encrypt(SHA256.new(password).digest(), str(Tfiles))
            print "Done encrypting %s" %str(Tfiles)
            os.remove(Tfiles)
 
elif choice == "D":
    filename = raw_input("Enter the filename to decrypt: ")
    if not os.path.exists(filename):
        print "The file does not exist"
        sys.exit(0)
    elif not filename.startswith("(encrypted)"):
        print "%s is already not encrypted" %filename
        sys.exit()
    else:
        decrypt(SHA256.new(password).digest(), filename)
        print "Done decrypting %s" %filename
        os.remove(filename)
 
else:
      print "Please choose a valid command."
      sys.exit()</pre>
&nbsp;
<h2>encode.py</h2>
This script uses <a href="https://en.wikipedia.org/wiki/Steganography">Steganography</a> to encode a message within an image file
<pre>#install Python2.7
#install PIL
#pip install stepic
#this program encodes messages within an image.

import Image
import stepic, os, sys

def encode(pic, stegpic, message):
    im=Image.open(pic)
    im2=stepic.encode(im, message)
    im2.save(stegpic)
    im2.show()
    return stegpic
 
def decode(pic):
    im1=Image.open(pic)
    s=stepic.decode(im1)
    data=s.decode()
    print data
    return data
 
choice = raw_input("Do you want to (E)ncode or (D)ecode? ")
pic = raw_input("Enter the filename: ")
#make sure it is a .png, .jpg does not work very well

if choice == "E":
    message = raw_input("Enter the secret message: ")
    stegpic = "steg" + str(pic)
    if not os.path.exists(pic):
        print "The file does not exist"
        sys.exit()
    else:
        encode(pic, stegpic, message)
        print "Done encoding %s" %stegpic
 
elif choice == "D":
    if not os.path.exists(pic):
       print "The file does not exist"
       sys.exit()
    else:
        decode(pic)
        print "Done decoding %s" %pic
else:
    print "please choose a valid command"
    sys.exit()

</pre>
&nbsp;
<h2>portscan.py</h2>
My version of the portscan.py example in Violent Python, updated for Python2.7
<pre>import argparse
from socket import *

def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        print '[+]%d/tcp open'% tgtPort
        connSkt.close()
    except:
        print '[-]%d/tcp closed'% tgtPort
 
def portScan(tgtHost, tgtPorts):
   try:
       tgtIP = gethostbyname(tgtHost)
   except:
       print "[-] Cannot resolve '%s': Unknown host" %tgtHost
       return
   try:
       tgtName = gethostbyaddr(tgtIP)
       print '\n[+] Scan Results for: ' + tgtName[0]
   except:
       print '\n[+] Scan Results for: ' + tgtIP  
   setdefaulttimeout(1)
   print 'debug: tgtPorts - '+ str(tgtPorts)
   for tgtPort in tgtPorts:
       print 'Scanning port ' + tgtPort
       connScan(tgtHost, int(tgtPort))
 
def main():
    parser = argparse.ArgumentParser(description='-H &lt;target host&gt; -p &lt;target port&gt;')
    parser.add_argument('-H', dest='tgtHost', type=str, help='specify target host')
    parser.add_argument('-p', dest='tgtPort', nargs='+', type=str, help='specify target port[s] separated by comma')
    options = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts=options.tgtPort
    print str(tgtPorts)
    if (tgtHost == None) | (tgtPorts[0] == None):
       print '[-] You must specify a target host and port[s].'
       exit(0)
    for port in tgtPorts:
       portScan(tgtHost, tgtPorts)
 
if __name__ == '__main__':
    main()
</pre>
<pre>&gt;python portscan.py -H 127.0.0.1 -p 3000 80
['3000', '80']

[+] Scan Results for: [redacted].example.com
debug: tgtPorts - ['3000', '80']
Scanning port 3000
[+]3000/tcp open
Scanning port 80
[-]80/tcp closed

[+] Scan Results for: [redacted].example.com
debug: tgtPorts - ['3000', '80']
Scanning port 3000
[+]3000/tcp open
Scanning port 80
[-]80/tcp closed</pre>
<h2>iplocate.py</h2>
Another example from the Violent Python book, kind of a homemade whois script. <a href="http://dev.maxmind.com/geoip/legacy/geolite/">GeoLiteCity.dat</a>, download this file to the same directory you will be executing the code from. Could be used to locate an unkown address in say an httpd_access_log that is pegging your website.
<pre>import pygeoip
import argparse
gi = pygeoip.GeoIP('GeoLiteCity.dat')
def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    city = rec['city']
    region = rec['region_code']
    country = rec['country_name']
    long = rec['longitude']
    lat = rec['latitude']
    print '[*] Target: ' + tgt + ' Geo-located. '
    print '[+] '+str(city)+', '+str(region)+', '+str(country)
    print '[+] Latitude: '+str(lat)+', Longitude: '+str(long)

def main():
   parser = argparse.ArgumentParser(description='finds geolocation of an IP address')
   parser.add_argument('ipaddr', metavar='I', nargs='+', type=str, help='8.8.8.8')
   args = parser.parse_args()
   tgts = args.ipaddr
   for tgt in tgts:
       printRecord(tgt)

if __name__ == '__main__':
    main()</pre>
<pre>&gt;python iplocate.py 8.8.8.8 8.8.4.4
[*] Target: 8.8.8.8 Geo-located.
[+] Mountain View, CA, United States
[+] Latitude: 37.3845, Longitude: -122.0881
[*] Target: 8.8.4.4 Geo-located.
[+] None, None, United States
[+] Latitude: 38.0, Longitude: -97.0</pre>
&nbsp;

&nbsp;

&nbsp;

&nbsp;