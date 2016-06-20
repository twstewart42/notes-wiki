#!/usr/bin/env python
import os, sys

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


