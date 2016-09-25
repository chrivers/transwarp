import fileinput
import glob
import textwrap
from mako.template import Template
from mako import exceptions

import cortex

def format_comment(comment, indent, width):
    return textwrap.wrap(
        "\n".join(comment),
        initial_indent=indent,
        subsequent_indent=indent,
        width=width,
    )

def generate(tmpl):
    files = glob.glob("data/*.stf")
    sections = cortex.parse(fileinput.input(files))

    template = Template(open(tmpl).read())
    return template.render(**{
            "enums": sections["enum"],
            "flags": sections["flags"],
            "packets": sections["packet"],
            "structs": sections["struct"],

            "format_comment": format_comment,
            "lang": __import__("rust")
    }).rstrip("\n")
