#!/usr/bin/python

import sys
import base64

if len(sys.argv) < 4:
  print('usage: ' + sys.argv[0] + ' <ciphertext> <original plaintext> <desired plaintext>')
  sys.exit()

ciphertext = base64.b64decode(sys.argv[1])
original   = sys.argv[2]
desired    = sys.argv[3]

# create byte arrays from the first blocks
cBytes = bytearray(ciphertext)[:16]
oBytes = bytearray(original)[:16]
dBytes = bytearray(desired)[:16]

# bitwise XOR on all three arrays
newIV = bytes(''.join(chr(c^o^d) for c,o,d in zip(cBytes,oBytes,dBytes)))

# print the result
print(base64.b64encode(newIV + ciphertext[16:]))
