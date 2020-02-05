#!/usr/bin/python3

import sys, base64


if len(sys.argv) < 2:
  print('usage: ' + sys.argv[0] + ' <session cookie>')
  sys.exit()

cookie = base64.b64decode(sys.argv[1])

# 1st block + 0 block + 1st block
forged = cookie[:16] + bytearray(16) + cookie[:16]

print(base64.b64encode(forged).decode('utf-8'))
