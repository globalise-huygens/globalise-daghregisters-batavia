# globalise-daghregisters-batavia

## Download
```bash
wget --wait=10 --random-wait --input-file=urls.txt --directory-prefix=images --content-disposition
```

## OCR
```bash
for f in *.tif; do tesseract $f ${f%.tif} -l nld -c tessedit_char_whitelist="-()'’.,1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ;:" -c preserve_interword_spaces=1; done
```
