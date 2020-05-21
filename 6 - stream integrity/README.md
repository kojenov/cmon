# Stream cipher integrity

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
FLASK_RUN_PORT=5006 FLASK_APP=server.py flask run
```

## Use the application

Navigate to http://localhost:5006, start browser developer tools, and examine the session cookie


## Bit flipping attack

Note the user data printed on the page, such as:
```
'{"user": "guest", "date": "2020-01-29"}'
```

This is the plaintext of the encrypted session cookie. Since the cookie is encrypted with stream cipher and re-used key, we can perform bit-flipping to obtain a ciphertext that would decrypt to desired plaintext.

First, examine the session cookie. It looks something like this:

```
9G/ySV3Ry9E=.j/3zPw9KCchD8ofdX/EaH8BNQuPhWG0x/IG3mZa67rA17FAMygLR
```
The part before the dot is the [random] nonce, and the part after the dot is the encrypted value. The actual algorithm doesn't matter much! Bit flipping works the same for all XOR-based stream ciphers.

Now, by examining `server.py` code, notice that the date value is not being used at all. So we can simply omit it in our bit flipping, i.e.:

```
'{"user": "admin"}'
```

Putting everything together:


```
$ ./flip.py '9G/ySV3Ry9E=.j/3zPw9KCchD8ofdX/EaH8BNQuPhWG0x/IG3mZa67rA17FAMygLR' '{"user": "guest", "date": "2020-01-29"}' '{"user": "admin"}'

9G/ySV3Ry9E=.j/3zPw9KCchD8oHMV+sAH5E=
```

Now, replace the encrypted part with the new value in the session cookie, refresh the page and behold the admin session!
