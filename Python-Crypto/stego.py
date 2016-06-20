#install Python2.7
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


