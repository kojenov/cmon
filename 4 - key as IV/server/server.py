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

    # unpack the cookie
    ciphertext = base64.b64decode(sessionCookie)

    try:
      # initialize cipher with IV = key
      cipher    = AES.new(key, AES.MODE_CBC, key)
      # decrypt
      decrypted = cipher.decrypt(ciphertext)
      sessJSON  = unpad(decrypted, AES.block_size)
      # deserialize
      session   = json.loads(sessJSON.decode())

    except ValueError as e:
      # oops, we have an error! be nice, tell the user
      decrypted64 = base64.b64encode(decrypted).decode('utf-8')
      response = make_response(render_template('error.html', decrypted=decrypted,
                                                             decrypted64=decrypted64))
      return response

  else:
    setCookie = True
    # create guest session object
    session = {}
    session['user'] = 'guest'
    session['role'] = 'none'
    sessJSON = json.dumps(session)
  
  # authorization
  if session['user'] == 'admin':
    response = make_response(render_template('admin.html', session=sessJSON))
  else:
    response = make_response(render_template('guest.html', session=sessJSON))

  if setCookie:
    # use encrypted key as IV, totally safe! LOL :)
    cipher = AES.new(key, AES.MODE_CBC, key)
    ciphertext = cipher.encrypt(pad(json.dumps(session).encode(), AES.block_size))
    
    # put ciphertext into the session cookie
    response.set_cookie('session', base64.b64encode(ciphertext))

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
