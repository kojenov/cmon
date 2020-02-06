# Padding oracle

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
export FLASK_APP=server.py
flask run
```

## Use the application

Navigate to http://localhost:5000 and see what's going on


## Padding oracle attack

See what the app tells you. Then try to go the URL with a valid message and with an invalid one, e.g.

http://localhost:5000/send?msg=deadbeef

http://localhost:5000/send?msg=296729c7564ad3198f686f24850a16647d2a269a96d21148c1be75f45768a809396db14ddb0dc6ae1f6ee9ebe49eb49e

(your ciphertext will be different!)

Notice the app returns different code depending on the validity.

Now run the exploit (your ciphertext will be different)

```
$ ./exploit.py http://localhost:5000/send?msg=36289eda81e4895db64c84bae1468eb21b122cebcaf1b0d81232a496d77a3238df444a038398693869ac3c598b434c59
```
