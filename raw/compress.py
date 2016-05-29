#!/usr/bin/python
# Use this script for any language where what you copy and paste sometimes
# leaves out part of a verse in a line that doesn't start with a number. If
# that's the case, make sure the file you pass doesn't have any extraneous
# section titles as this will connect together lines with their respective
# verses

import sys

def usage(program):
    print "usage:", program, "[lang_code]+"
    sys.exit()

def main(args):
    if len(args) < 2:
        usage(args[0])
    for arg in args[1:]:
        with open(arg) as f:
            content = f.readlines()

        new = []
        for l in content:
            if l[0].isdigit():
                new.append(l)
            else:
                new[len(new) - 1] = new[len(new) -1].strip() + " "
                new[len(new) - 1] += l 

        with open(arg, "w") as f:
            for l in new:
                f.write(l)
