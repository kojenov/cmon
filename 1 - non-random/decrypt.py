#!/usr/bin/python3

import os, sys, time, string, re
import random
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


if len(sys.argv) < 2:
  print('usage: ' + sys.argv[0] + ' <file>')
  sys.exit()

fname = sys.argv[1]

# seed the PRNG with file modification time
seed = int(os.path.getmtime(fname))
random.seed(seed)
#print(seed)

# generate 128-bit data encryption key
key = bytearray()
for i in range(16):
  key.append(random.randint(0,255))

# open and read the encrypted file
with open(fname, 'rb') as file:
  iv    = file.read(16)
  encrypted = file.read()
  
# decrypt the file
cipher = AES.new(key, AES.MODE_CBC, iv)
plain = unpad(cipher.decrypt(encrypted), AES.block_size)

# print the decrypted contents
print("Successfully decrypted data:")
print(plain.decode('utf-8'))
