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
    print(exceptions.text_error_template().render())
