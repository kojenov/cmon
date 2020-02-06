from flask import Flask, request, render_template, make_response

import base64, json, time
from os import path

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


app = Flask(__name__)

@app.route('/')
def index():
  
  # get the encryption key
  key = encryptionKey()

  # get the session cookie
  sessionCookie = request.cookies.get('session')
  
  if sessionCookie:
    
    setCookie = False

    # unpack the cookie: first 16 bytes is the IV, the rest is ciphertext
    value      = base64.b64decode(sessionCookie)
    iv         = value[:16]
    ciphertext = value[16:]

    # decrypt the session object
    cipher    = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    session   = json.loads(plaintext.decode())
    
  else:
    setCookie = True
    # create guest session object
    session = {}
    session['user'] = 'guest'
    session['date'] = time.strftime('%Y-%m-%d')  # not used currently. todo
  
  # authorization
  if session['user'] == 'admin':
    response = make_response(render_template('admin.html', session=json.dumps(session)))
  else:
    response = make_response(render_template('guest.html', session=json.dumps(session)))

  if setCookie:
    # generate a random IV and encrypt the session object
    iv     = Random.new().read(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(json.dumps(session).encode(), AES.block_size))
    
    # pack the iv and the ciphertext to the session cookie
    response.set_cookie('session', base64.b64encode(iv + ciphertext))

  return response


def encryptionKey():
  keyfile = 'sessionkey'
  if path.exists(keyfile):
    # read stored encryption key
    key = open(keyfile, 'rb').read()
  else:
    # if this is the first run:
    #  1. generate a random encryption key
    #  2. store it in the key file
    key = Random.new().read(16)
    with open(keyfile, 'wb') as file:
      file.write(key)
  return key
