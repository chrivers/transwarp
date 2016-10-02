import sys
from contextlib import contextmanager

from mako import exceptions
from mako.template import Template
from mako.exceptions import RichTraceback

import transwarp.parser
import transwarp.template
import transwarp.template.util
from transwarp.util.data import SearchableList

context = None

@contextmanager
def mako_context(ctx):
    global context
    context = ctx
    yield
    context = None

@contextmanager
def scoped_search_paths(paths):
    for p in paths:
        sys.path.insert(0, p)
    yield
    for p in paths:
        if p in sys.path:
            sys.path.remove

def find_available():
    import os
    import fnmatch
    matches = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.tpl'):
            matches.append(os.path.join(os.path.normpath(root), filename))
    return matches

def generate(tmpl, sections, link_paths):
    template = Template(tmpl)
    empty = SearchableList()
    context = {
        "enums": sections.get("enum", empty),
        "flags": sections.get("flags", empty),
        "packets": sections.get("packet", empty),
        "structs": sections.get("struct", empty),
        "objects": sections.get("object", empty),
        "parsers": sections.get("parser", empty),

        "util": transwarp.template.util,
    }
    with mako_context(context):
        with scoped_search_paths(link_paths):
            result = template.render(**context).rstrip("\n")
    return result

def present_template_error():
    print(exceptions.text_error_template().render(), file=sys.stderr)
