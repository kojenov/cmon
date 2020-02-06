# Stream cipher key reuse

```
echo "Super secret message" | ./encrypt.py "Super secret key" > cipher1
head -c 21 /dev/zero | ./encrypt.py "Super secret key" > cipher2
./xor.py cipher1 cipher2
```

```
./encryptimage.py alexei.png smile.png
```
Then open in GIMP and layer difference

`sudo apt install gmic`

https://stackoverflow.com/a/40049271
```
gmic alexei-encrypted.png smile-encrypted.png -blend xor -o xor1.png
gmic alexei-encrypted.png smile-encrypted.png smile.png -blend xor -o xor2.png
```


Images:

- https://www.publicdomainpictures.net/en/view-image.php?image=128827&picture=clip-art-smiley-face
