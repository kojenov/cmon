# Non-random random

This naïve "ransomware" encrypts a file which can be decrypted by getting the seed information from the file timestamp.

```
./encrypt.py document.txt
./decrypt.py document.ransom
```
