# Encryption key used as IV

## Start the application server

Go to the server directory
```
cd server
```

Initialize venv
```
python3 -m venv venv
source venv/bin/activate
```

Install Flask and crypto
```
pip install Flask
pip install pycryptodome
```

Run the application
```
FLASK_RUN_PORT=5004 FLASK_APP=server.py flask run
```

## Use the application

Navigate to http://localhost:5004, start browser developer tools, and examine the session cookie


## Break the session cookie encryption key

First, use `forge.py` generate a forged cookie value. It is built as follows: 1st block + zero block + 1st block. For example:

```
$ ./forge.py 'w82wOFe73r0J6B41HTEWyuxT76qHBl2ferZv0EDVVloBdIYjWXhTLF/2U+r0nMi0' w82wOFe73r0J6B41HTEWygAAAAAAAAAAAAAAAAAAAADDzbA4V7vevQnoHjUdMRbK
```

Now, replace the session cookie with the result above, and refresh the web page. You should get an error like this:

```
The decrypted data is invalid:
b'{"user": "guest"w=-\xe2\xcb\x9b{\x04\xf7S\x83jJJ\xa5\x9c\\\xcd\x1d\xb7~*u\xe0x\x86q\xb3\xe3\x83P\xb8'

or in base64:
eyJ1c2VyIjogImd1ZXN0Inc9LeLLm3sE91ODakpKpZxczR23fip14HiGcbPjg1C4
```

Retrieve the encryption key with `getkey.py`, for example:

```
$ ./getkey.py eyJ1c2VyIjogImd1ZXN0Inc9LeLLm3sE91ODakpKpZxczR23fip14HiGcbPjg1C4

Retrieved session cookie encryption key: 27ef68c41b5857da58a416c686f0249a
```

Encrypt admin cookie with OpenSSL:

```
$ echo -n '{"user": "admin", "role": "none"}' | openssl enc -aes-128-cbc -in - -iv 27ef68c41b5857da58a416c686f0249a -K 27ef68c41b5857da58a416c686f0249a | base64 -w 0
wdV5aOBNAnnAvpS4SQrjXJeli1G1QWX27b/vvNpHjar1JaSd72op19+pJulXMPfI
```

In browser developer tools, replace the session cookie with the returned value, and behold the admin session!
