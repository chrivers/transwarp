import os
import sys
import glob
import fnmatch
import fileinput
import logging as log

import transwarp.parser
import transwarp.template
import transwarp.util.logformat
import transwarp.cmdline.arguments

DEFAULT_TEMPLATE_EXTENSION = "*.tpl"

def normalize_path(path):
    return os.path.normpath(path) + os.path.sep

def main(args=None):
    transwarp.util.logformat.initialize()
    args = transwarp.cmdline.arguments.parse_and_validate()

    files = find_stf_files(args.datadir)

    # parse all sections into a unified data structure, that the
    # templates can inspect
    all_lines = fileinput.input(files=files)
    sections = transwarp.parser.parse(all_lines)
    log.debug("parsed %d stf files" % (len(files)))
    find_template_files(args.inputdir, "")
    # log.info("Compiling [%s]" % template_file)

def find_template_files(idir, odir, update=True, extension_glob=DEFAULT_TEMPLATE_EXTENSION):
    path = normalize_path(idir)
    log.debug("Searching for templates in: %s" % path)
    i_files = []
    for root, _, files in os.walk(path):
        reldir = root[len(path):]
        for name in files:
            if fnmatch.fnmatch(name, extension_glob):
                relpath = os.path.join(reldir, name)
                log.debug("template file [%s]" % relpath)
                i_files.append(relpath)
    return i_files

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
