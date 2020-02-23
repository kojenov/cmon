#!/usr/bin/python3

import sys
from PIL import Image
from Crypto import Random
from Crypto.Cipher import ARC4
import re

def encrypt(fname, key):
  # open the image and remove the alpha (transparencey) channel
  im = Image.open(fname).convert(mode='RGB')

  # get the image pixel data
  pixels = im.tobytes()

  # encrypt with RC4 and the provided key
  cipher = ARC4.new(key)
  encrypted = cipher.encrypt(pixels)

  # create a new image object from encrypted bytes
  imEnc = Image.frombytes(mode='RGB', size=im.size, data=encrypted)

  # save encrypted image as a new file
  fnameEnc = re.sub('(?P<name>.+)\.', '\g<name>-enc.', fname)
  imEnc.save(fnameEnc)
  print('Encrypted image saved as ' + fnameEnc)
  

if len(sys.argv) < 3:
  print('usage: ' + sys.argv[0] + ' <image1> <image2>')
  sys.exit()
  
# generate a truly random encryption key
print('\ngenerating a random encryption key...')
key = Random.new().read(16)

# encrypt both images
encrypt(sys.argv[1], key)
encrypt(sys.argv[2], key)
