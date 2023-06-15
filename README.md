# Daghregisters Batavia

## Download
```bash
wget --wait=10 --random-wait --input-file=urls.txt --directory-prefix=images --content-disposition
```

## Make things sortable
Zero-padd every filename so that we can easily sort the files.

```bash
for f in *.tif; do
  if [[ $f =~ seq_([0-9]+) ]]; then
    number="${BASH_REMATCH[1]}";
    padded_number=$(printf "%04d" "$number");
    
    new_f="${f/seq_$number/seq_$padded_number}";

    if [[ "$f" != "$new_f" ]]; then
      mv "$f" "$new_f";
    fi;
  fi;
done
```

## OCR

Using [Tesseract](https://tesseract-ocr.github.io/) version 5.3.0
```bash
$ tesseract --version
tesseract 5.3.0
 leptonica-1.82.0
  libgif 5.1.9 : libjpeg 8d (libjpeg-turbo 2.1.1) : libpng 1.6.37 : libtiff 4.3.0 : zlib 1.2.11 : libwebp 1.2.2 : libopenjp2 2.4.0
 Found AVX2
 Found AVX
 Found FMA
 Found SSE4.1
 Found OpenMP 201511
 Found libarchive 3.6.0 zlib/1.2.11 liblzma/5.2.5 bz2lib/1.0.8 liblz4/1.9.3 libzstd/1.4.8
 Found libcurl/7.81.0 OpenSSL/3.0.2 zlib/1.2.11 brotli/1.0.9 zstd/1.4.8 libidn2/2.3.2 libpsl/0.21.0 (+libidn2/2.3.2) libssh/0.9.6/openssl/zlib nghttp2/1.43.0 librtmp/2.3 OpenLDAP/2.5.14

```


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

## Convert to PAGEXML
Latest `PageConverter.jar` downloaded from https://github.com/PRImA-Research-Lab/prima-page-converter/releases/tag/1.5.05

```bash
sourcedir="hocr/"
targetdir="pagexml/"

mkdir -p "$targetdir"

hocr_files=$(find "$sourcedir" -type f -name "*.hocr")

for hocr_file in $hocr_files; do
    relative_path="${hocr_file#"$sourcedir"/}"
    target_folder="$targetdir/$(dirname "$relative_path")"
    target_folder="${target_folder//hocr/}"
    target_folder="${target_folder#/}"
    
    mkdir -p "$target_folder"

    filename=$(basename "$hocr_file")
    filename_no_ext="${filename%.hocr}"
    target_file="$target_folder/${filename_no_ext}.xml"

    java -jar PageConverter.jar -source-xml "$hocr_file" -target-xml "$target_file" -convert-to LATEST
done
```

## Notes on use
* includes comment on digitisation on every page
* the file https://github.com/globalise-huygens/globalise-daghregisters-batavia/blob/main/Daghregisters%20-%20Inventories.csv contains metadata on the volumes (year or years from which the daily journals date, library that holds the copy that was scanned, number of pages per volume; this file also shows which copies were selected for use and which copies are considered duplicates and ignored (txt files of these volumes can be found in the folder duplicates).
