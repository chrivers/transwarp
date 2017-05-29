import os
import sys
from contextlib import contextmanager

from mako import exceptions
from mako.template import Template as MakoTemplate
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

def generate(tmplfile, files, link_paths):
    template = MakoTemplate(filename=os.path.abspath(tmplfile))
    empty = SearchableList()
    context = {
        "enums": files.get("enums", empty),
        "flags": files.get("flags", empty),
        "structs": files.get("structs", empty),
        "objects": files.get("objects", empty),
        "server": files.get("server", empty),
        "client": files.get("client", empty),
        "parsers": files.get("parser", empty),
        "files": files,
        "util": transwarp.template.util,
    }
    with mako_context(context):
        with scoped_search_paths(link_paths):
            return template.render(**context)

def present_template_error():
    print(exceptions.text_error_template().render(), file=sys.stderr)
