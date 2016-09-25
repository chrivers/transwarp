import fileinput
import glob
from mako.template import Template
import textwrap

def format_comment(comment, indent, width=80):
    return textwrap.wrap(
        "\n".join(comment),
        initial_indent=indent,
        subsequent_indent=indent,
        width=width,
    )

def generate(cortex, tmpl):
    files = glob.glob("data/*.stf")
    sections = cortex.parse(fileinput.input(files))

    template = Template(open(tmpl).read())
    print(template.render(**{
        "enums": sections["enum"],
        "flags": sections["flags"],
        "packets": sections["packet"],
        "format_comment": format_comment,
    }).rstrip("\n"))
