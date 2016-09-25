import fileinput
import glob
from mako.template import Template
from mako import exceptions
from mako.exceptions import RichTraceback
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
    try:
        print(template.render(**{
            "enums": sections["enum"],
            "flags": sections["flags"],
            "packets": sections["packet"],
            "format_comment": format_comment,
        }).rstrip("\n"))
    except:
        traceback = RichTraceback()
        filename, lineno, function, line = traceback.traceback[-1]
        print("Error in template line %d:" % lineno)
        print()
        print(line)
        print("  %s: %s" % (str(traceback.error.__class__.__name__), traceback.error))
