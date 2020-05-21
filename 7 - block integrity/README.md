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
FLASK_RUN_PORT=5007 FLASK_APP=server.py flask run
```

## Use the application

Navigate to http://localhost:5007, start browser developer tools, and examine the session cookie


## Bit flipping attack

Note the user data printed on the page, such as:
```
{"user": "guest", "date": "2020-01-29"}
```

This is the plaintext of the encrypted session cookie. Since the application does not validate the ciphertext integrity, we can perform bit-flipping to obtain a ciphertext that would decrypt to desired plaintext.

We are lucky because the most critical part of the session cookie is within the first block (i.e. 16 bytes), so we only need to bit flip one block. It's easy to do by manipulating the IV.

Putting everything together (this is just an example, your cipher text will be different):


```
$ ./flip.py prPhoAqyxpoCXsnmFklgCmB3IWlwG56VDS0JP/WGyBNNhiRxIl2lutCk9F2hZUn8NcbttVvEK6I6TpPOlmFFew== '{"user": "guest"' '{"user": "admin"'

prPhoAqyxpoCXs/3HlN6CmB3IWlwG56VDS0JP/WGyBNNhiRxIl2lutCk9F2hZUn8NcbttVvEK6I6TpPOlmFFew==
```

Now, replace the encrypted part with the new value in the session cookie, refresh the page and behold the admin session!
