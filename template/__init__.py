from mako.template import Template
from mako import exceptions
from mako.exceptions import RichTraceback

import cortex
import cortex.data
import template.util

def generate(tmpl, sections, lang_utils):
    template = Template(tmpl)
    empty = cortex.data.SearchableList()
    return template.render(**{
        "enums": sections.get("enum", empty),
        "flags": sections.get("flags", empty),
        "packets": sections.get("packet", empty),
        "structs": sections.get("struct", empty),
        "objects": sections.get("object", empty),

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
