#!/usr/bin/python
# This script goes through the raw texts, removes any extra stuff (such as verse
# numbers and html jargon) and tokenizes the file into the format we'll be using
# in our data for our model

import os, sys, re

def tokenize(infile, outfile, lang):
    for line in infile.readlines():
        # Skip this line if it doesn't start with a number
        if not line[0].isdigit():
            continue

        # Replace all [.*], numbers, and line initial spaces  with nothing
        line = re.sub("\[.*\]|\d+", "", line)
        line = re.sub("^ ", "", line)

        # Is this Latin? If so it has no punctuation so let's just consider each
        # verse a line
        if lang == "la":
            outfile.write(line)
            continue

        # Replace all existing newlines with a space
        line = re.sub("\n"," ",line)

        # Replace all .!?: that aren't sentence-final with distinctive
        # strings, e.g., KEEPTHISPERIOD.

        # If there's nothing to read don't write it out
        if (line.strip() is ''): continue

        # Handle three dots.
        line = re.sub(r'([^.])\.{3}([^.])', '\g<1>KEEPTHIS_E_\g<2>', line)
      
        map = {"." : "_P_", "!" : "_B_", "?" : "_Q_", ":" : "_C_"}

        for c in map:
          line = re.sub(r' \%s ' % (c), ' KEEPTHIS%s ' % (map[c]), line)
          line = re.sub(r'\%s(\w| +[a-z])' % (c), 'KEEPTHIS%s\g<1>' % (map[c]), line)
        line = re.sub(r'([A-Z]\w*)\%s ([A-Z])' % ('.'), '\g<1>KEEPTHIS%s \g<2>' % (map['.']), line)

        # Change .!?: followed by a " to a special symbol, e.g., PERIODQUOTE.
        # NB " is a special character in Python, and needs to be escaped.
        for c in map:
          line = re.sub(r'\%s"' % (c), '%sQUOTE' % (map[c]), line)

        # Change any space following a remaining .!?: to a newline.
        line = re.sub(r'([?!.:]) ', '\g<1>\n', line)

        # Replace all KEEPTHISPERIOD etc. to the punctuation they represent.
        for c in map:
          line = re.sub(r'KEEPTHIS%s' % (map[c]), '%s' % (c), line)

        # Replace all PERIODQUOTE with the punctuation and a newline:
        for c in map:
          line = re.sub(r'%sQUOTE' % (map[c]), '%s"\n' % (c), line)

        line = re.sub(r'KEEPTHIS_E_', "...", line)

        # The following is for beautification of the output

        # Remove any line-initial spaces:
        # Remove any spaces before a new line:
        # Compress a sequence of spaces into just one:
        line = re.sub(r' *\n *', '\n', line)
        line = re.sub(r' +', ' ', line)

        # Print the refurbished line to the output.
        outfile.write(line)

def usage(program):
    print "usage:", program, "[lang_code]+"

def main(args):
    langs = "ca da de en es fo fr fy is it la nb nl nn pt ro sv tl".split()
    if len(args) > 1:
        for lang in args[1:]:
            if lang not in langs:
                print lang, "is not a valid language code"
                usage(args[0])
                return
        langs = args[1:]
    for lang in langs:
        with open("data/%s.txt" % lang, "w") as outf:
            infiles = os.listdir("raw/%s" % lang)
            for f in infiles:
                with open("raw/%s/%s" % (lang, f)) as inf:
                    tokenize(inf, outf, lang)
     

if __name__ == "__main__":
    main(sys.argv)
