#!/usr/bin/python3

import base64, sys
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


if len(sys.argv) < 2:
  print('usage: ' + sys.argv[0] + ' [sha|pbkdf2]')
  sys.exit()
  

password = 'pinkfloyd'

# get random salt
salt  = Random.new().read(16)

fname = sys.argv[1]
out = open(fname, 'w+')

if fname == 'sha':
  # SHA256
  # really straight forward

  h = hashlib.sha256()
  h.update(salt.hex().encode())
  h.update(password.encode())
  digest = h.digest()

  print('# SHA-256 with random salt', file=out)
  print('root:' + digest.hex() + '$' + salt.hex(), file=out)

  print('saved to: ' + fname)
  print('brute force with: john-the-ripper --format=dynamic_61 ' + fname)

else:
  # PBKDF2-HMAC-SHA256
  # the generated format is really annoying, it is explained here:
  # https://www.openwall.com/lists/john-users/2018/06/09/2

  iterations = 500000

  dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, 32)

  pbsalt = base64.b64encode(salt).decode().translate(str.maketrans({'+':'.', '=':None}))
  pbhash = base64.b64encode(dk).decode().translate(str.maketrans({'+':'.', '=':None}))[:43]

  print('# PBDKF2-HMAC-SHA256 with random salt', file=out)
  print('$pbkdf2-sha256$%d$%s$%s' % (iterations, pbsalt, pbhash), file=out)

  print('saved to: ' + fname)
  print('brute force with: john-the-ripper --format=PBKDF2-HMAC-SHA256 ' + fname)

out.close()
