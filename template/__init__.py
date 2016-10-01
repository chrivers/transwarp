import sys
from mako.template import Template
from mako import exceptions
from mako.exceptions import RichTraceback

import cortex
import cortex.data
import template.util

def find_available():
    import os
    import fnmatch
    matches = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.tpl'):
            matches.append(os.path.join(os.path.normpath(root), filename))
    return matches

def generate(tmpl, sections):
    template = Template(tmpl)
    empty = cortex.data.SearchableList()
    return template.render(**{
        "enums": sections.get("enum", empty),
        "flags": sections.get("flags", empty),
        "packets": sections.get("packet", empty),
        "structs": sections.get("struct", empty),
        "objects": sections.get("object", empty),
        "parsers": sections.get("parser", empty),

        "util": util,
    })

def present_template_error():
    print(exceptions.text_error_template().render(), file=sys.stderr)
