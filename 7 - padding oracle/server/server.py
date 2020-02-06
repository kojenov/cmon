from flask import Flask, request, render_template, make_response, Response

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

  # encrypt a sample message
  iv         = Random.new().read(16)
  cipher     = AES.new(key, AES.MODE_CBC, iv)
  ciphertext = cipher.encrypt(pad('Padding oracles are real!'.encode(), AES.block_size))

  msg = (iv+ciphertext).hex()
  response = make_response(render_template('index.html', host=request.host, msg=msg))
  
  return response

@app.route('/send')
def send():

  msg = request.args['msg']
  
  # parse the message: the first 16 bytes is IV, the rest is ciphertext
  value = bytes.fromhex(msg)
  iv         = value[:16]
  ciphertext = value[16:]

  # get the encryption key
  key = encryptionKey()

  try:
    # decrypt the message
    cipher    = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    print('Decrypted: ' + plaintext.decode('utf-8'))
    
    # todo: process the message

    response = make_response(render_template('send.html'))

  except ValueError as e:
    # oops, an error! be nice and let the user know
    response = make_response(render_template('unauthorized.html'), 403)

  return response
  

def encryptionKey():
  keyfile = 'encryptionkey'
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
