#!/usr/bin/python3

import sys

if len(sys.argv) < 3:
  print('usage: ' + sys.argv[0] + ' <file1> <file2>')
  sys.exit()

# read both files into byte arrays
bytes1 = bytearray(open(sys.argv[1], 'rb').read())
bytes2 = bytearray(open(sys.argv[2], 'rb').read())

# XOR the two arrays, byte by byte, and print the result
print(''.join(chr(x^y) for x,y in zip(bytes1, bytes2)))
