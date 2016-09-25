from mako.template import Template
from mako import exceptions
from mako.exceptions import RichTraceback

import cortex
import template.util

def generate(tmpl, sections, lang_utils):
    template = Template(tmpl)
    return template.render(**{
        "enums": sections["enum"],
        "flags": sections["flags"],
        "packets": sections["packet"],
        "structs": sections["struct"],
        "objects": sections["object"],

        "util": util,
        "lang": lang_utils,
    }).rstrip("\n")

def present_template_error():
    traceback = RichTraceback()
    filename, lineno, function, line = traceback.traceback[-1]
    print("Error in template line %d:" % lineno)
    print()
    print(line)
    print("  %s: %s" % (str(traceback.error.__class__.__name__), traceback.error))
