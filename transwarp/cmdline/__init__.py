import sys
import glob
import fileinput
import logging as log

import transwarp.parser
import transwarp.template
import transwarp.util.logformat
import transwarp.cmdline.arguments

def main(args=None):
    transwarp.util.logformat.initialize()
    args = transwarp.cmdline.arguments.parse_and_validate()

    files = find_stf_files(args.datadir)

    # parse all sections into a unified data structure, that the
    # templates can inspect
    all_lines = fileinput.input(files=files)
    sections = transwarp.parser.parse(all_lines)
    log.debug("parsed %d stf files" % (len(files)))

def find_stf_files(datadir):
    # find all stf input files
    files = glob.glob("%s/*.stf" % datadir)
    if files:
        log.debug("found stf files:")
        for name in files:
            log.debug("  %s" % name)
        return files
    else:
        raise LookupError("Could not find any .stf files in %r" % datadir)

def render_template(template_data, input_file, output_file):
    try:
        template_data = open(template_file).read()
        text = transwarp.template.generate(template_data, sections)
        return text
    except:
        transwarp.template.present_template_error()
        raise
