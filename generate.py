#!/usr/bin/python3

import sys, os
import fileinput
import cortex
import template
from pprint import pprint
from mako.exceptions import RichTraceback

if len(sys.argv) != 2:
    print("usage: %s <stf-file>" % sys.argv[0])
    sys.exit(1)

try:
    template_file = sys.argv[1]
    print(template.generate(template_file))
except:
    traceback = RichTraceback()
    filename, lineno, function, line = traceback.traceback[-1]
    print("Error in template line %d:" % lineno)
    print()
    print(line)
    print("  %s: %s" % (str(traceback.error.__class__.__name__), traceback.error))
