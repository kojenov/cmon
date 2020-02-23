#!/usr/bin/python3

# https://www.hackerearth.com/practice/notes/extracting-pixel-values-of-an-image-in-python/

import sys, re
from PIL import Image
from Crypto import Random
from Crypto.Cipher import AES

def encryptImage(fname, mode):

  # open the image and remove the alpha (transparencey) channel
  im = Image.open(fname).convert(mode='RGB')

  # get the image pixel data
  pixels = im.tobytes()

  # generate a random key
  # note: we don't store the key anywhere
  print('\ngenerating a random encryption key...')
  key = Random.new().read(16)

  if mode == 'ECB':
    # ECB mode... very cool!
    print('encrypting with ECB mode...')
    cipher = AES.new(key, AES.MODE_ECB)
  else:
    # CBC mode requires an IV
    print('encrypting with CBC mode...')
    iv  = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
  # actual encryption
  encrypted = cipher.encrypt(pixels)

  # create a new image object from encrypted bytes
  imEnc = Image.frombytes(mode='RGB', size=im.size, data=encrypted)

  # save encrypted image as a new file
  fnameEnc = re.sub('(?P<name>.+)\.', '\g<name>-' + mode + '.', fname)
  imEnc.save(fnameEnc)

  print('Encrypted image saved as ' + fnameEnc)

  # optional: byte frequencey analysis
  
  #d = {}
  #for b in encrypted:
    #d[b] = d.setdefault(b, 0) + 1
    
  #freq = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}

  #print('Byte frequency analysis:')
  #print(freq)
  

if len(sys.argv) < 2:
  print('usage: ' + sys.argv[0] + ' <image file>')
  sys.exit()
  
fname = sys.argv[1]

encryptImage(fname, 'CBC')
encryptImage(fname, 'ECB')

