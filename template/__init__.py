import fileinput
import glob
from mako.template import Template

def generate(cortex, tmpl):
    files = glob.glob("data/*.stf")
    sections = cortex.parse(fileinput.input(files))

    template = Template(open(tmpl).read())
    print(template.render(**{
        "enums": sections["enum"],
        "flags": sections["flags"],
    }).rstrip("\n"))
