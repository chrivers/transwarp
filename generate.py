#!/usr/bin/python3

import sys, os
import fileinput
from pprint import pprint
import cortex

if len(sys.argv) < 3:
    print("usage: %s <language> <stf-files..>" % sys.argv[0])
    sys.exit(1)

try:
    language = __import__(sys.argv[1])
except ImportError:
    print("Could not load language [%s]" % sys.argv[1])
    sys.exit(2)

language.generate(cortex, *sys.argv[2:])
