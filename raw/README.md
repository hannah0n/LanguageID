# Raw Text Folder

This folder holds the raw text we extracted for each language before being
preprocessed into a consistent format.

## Constraints

In order to preprocess text into a consistent we ensured the following:
- Each verse was part of a line that started with a number.
- Non-verse text was part of lines that didn't begin with a number.

## Compress.py

In cases where the constraints weren't met by copying and pasting we removed the
non-verse text and ran the compress.py to compress verses spanning multiple
lines into one line. For example, the following line:

`2 Ferice de cei ce păzesc mărturiile Lui
    şi-L caută din toată inima:`

would be compressed into :

`2 Ferice de cei ce păzesc mărturiile Lui şi-L caută din toată inima:`
