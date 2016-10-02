import os
import sys
import glob
import fnmatch
import fileinput
import logging as log

from datetime import datetime

import transwarp.parser
import transwarp.template
import transwarp.util.logformat
import transwarp.cmdline.arguments

DEFAULT_TEMPLATE_EXTENSION = "*.tpl"

def path_normalize(path):
    return os.path.normpath(path) + os.path.sep

def path_join(a, b):
    return os.path.normpath(os.path.join(a, b))

def main(args=None):
    transwarp.util.logformat.initialize()
    args = transwarp.cmdline.arguments.parse_and_validate()

    files = find_stf_files(args.datadir)

    # parse all sections into a unified data structure, that the
    # templates can inspect
    all_lines = fileinput.input(files=files)
    sections = transwarp.parser.parse(all_lines)

    log.debug("parsed %d stf files" % (len(files)))
    templates = find_template_files(args.inputdir)

    if args.all:
        log.debug("using all templates (--all)")
        missing, updated = templates, []
    else:
        missing, updated = check_freshness(args.inputdir, args.outputdir, templates)

    targets = set(missing) | set(updated)
    if targets:
        log.info("Compiling %d of %d templates" % (len(targets), len(templates)))
        for target in targets:
            compile_template(
                sections,
                path_join(args.inputdir, target),
                path_join(args.outputdir, target),
            )
    else:
        log.info("All templates up-to-date")

def get_timestamp(filename):
    return datetime.fromtimestamp(os.stat(filename).st_mtime)

def check_freshness(idir, odir, templates):
    missing, updated = [], []
    log.debug("scanning for templates to compile:")
    for name in templates:
        ifile = path_join(idir, name)
        ofile = path_join(odir, name)
        try:
            otime = get_timestamp(ofile)
        except OSError:
            log.debug("  template %s: not found" % ofile)
            missing.append(name)
            continue

        if get_timestamp(ifile) > otime:
            res.append(name)
            log.debug("  template %s: stale" % ofile)
        else:
            log.debug("  template %s: fresh" % ofile)
    return missing, updated

def find_template_files(path, extension_glob=DEFAULT_TEMPLATE_EXTENSION):
    path = path_normalize(path)
    log.debug("Searching for templates in: %s" % path)
    i_files = []
    for root, _, files in os.walk(path):
        reldir = root[len(path):]
        for name in files:
            if fnmatch.fnmatch(name, extension_glob):
                relpath = path_join(reldir, name)
                log.debug("  template %s" % relpath)
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

def compile_template(data, input_file, output_file):
    target_dir = os.path.dirname(output_file)
    os.makedirs(target_dir, exist_ok=True)

    template_data = open(input_file).read()
    text = render_template(data, template_data)
    with open(output_file, "w") as output:
        output.write(text)
    log.info("Compiled template [%s]" % output_file)

def render_template(data, template):
    try:
        text = transwarp.template.generate(template, data)
        return text
    except:
        transwarp.template.present_template_error()
        sys.exit(1)
