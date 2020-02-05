from flask import Flask, request, render_template, make_response

import base64, json, time
from os import path

from Crypto import Random
from Crypto.Cipher import Salsa20


app = Flask(__name__)

@app.route('/')
def index():
  
  # get the encryption key
  key = encryptionKey()

  # get the session cookie
  sessionCookie = request.cookies.get('session')
  
  if sessionCookie:
    
    setCookie = False

    # the cookie consists of two parts separated by '.'
    # - Salsa20 nonce
    # - ciphertext
    values     = sessionCookie.split('.')
    nonce      = base64.b64decode(values[0])
    cipherText = base64.b64decode(values[1])
    
    # decrypt cookie using Salsa20
    cipher  = Salsa20.new(key, nonce)
    session = json.loads(cipher.decrypt(cipherText).decode())
    
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
    # encrypt the session object
    cipher     = Salsa20.new(key)
    cipherText = cipher.encrypt(json.dumps(session).encode())
    
    # pack the nonce and the ciphertext to the session cookie
    response.set_cookie('session', base64.b64encode(cipher.nonce).decode() + '.' + 
                                   base64.b64encode(cipherText).decode())

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
