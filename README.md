# globalise-daghregisters-batavia

## Download
```bash
wget --wait=10 --random-wait --input-file=urls.txt --directory-prefix=images --content-disposition
```

## OCR

```bash
# hocr
mkdir hocr

for f in images/*.tif; do
  output_file="hocr/$(basename "${f%.tif}")"
  tesseract "$f" "$output_file" \
    -l nld \
    -c tessedit_char_whitelist="\"-()'’.,1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ;:" \
    -c tessedit_create_hocr=1 \
    -c hocr_font_info=0
done

# txt
mkdir txt

for f in images/*.tif; do
  output_file="txt/$(basename "${f%.tif}")"
  tesseract "$f" "$output_file" \
  -l nld \
  -c tessedit_char_whitelist="\"-()'’.,1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ;:" \
  -c preserve_interword_spaces=1;
done
```

## Sort files

```bash
sourcedir="txt/"
prefixes=$(find "$sourcedir" -type f -name "*.txt" -exec basename {} \; | awk -F '-seq' '{print $1}' | sort -u)

for prefix in $prefixes; do
    folder_path="$sourcedir/$prefix"
    mkdir -p "$folder_path"

    mv "$sourcedir/$prefix"* "$folder_path/"
done
```

```bash
sourcedir="hocr/"
prefixes=$(find "$sourcedir" -type f -name "*.hocr" -exec basename {} \; | awk -F '-seq' '{print $1}' | sort -u)

for prefix in $prefixes; do
    folder_path="$sourcedir/$prefix"
    mkdir -p "$folder_path"

    mv "$sourcedir/$prefix"* "$folder_path/"
done
```
