#!/usr/bin/python

import sys, base64


if len(sys.argv) < 4:
  print('usage: ' + sys.argv[0] + ' <ciphertext> <original plaintext> <desired plaintext>')
  sys.exit()

ciphertext = sys.argv[1]
original   = sys.argv[2]
desired    = sys.argv[3]

# convert input data to byte arrays
cBytes = bytearray(base64.b64decode(ciphertext))
oBytes = bytearray(original)
dBytes = bytearray(desired)

# perform bitwise XOR with all 3 arrays
newCipherText = ''.join(chr(c^o^d) for c,o,d in zip(cBytes,oBytes,dBytes))

# print the result
print(base64.b64encode(newCipherText))
