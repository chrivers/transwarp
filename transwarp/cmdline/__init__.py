import os
import sys
import glob
import enum
import tempfile
import fileinput
import subprocess
import logging as log

from datetime import datetime

import transwarp.parser
import transwarp.template
import transwarp.util.logformat
import transwarp.cmdline.arguments

DEFAULT_TEMPLATE_EXTENSION = ".tpl"

def path_normalize(path):
    return os.path.normpath(path) + os.path.sep

def path_join(a, b):
    return os.path.normpath(os.path.join(a, b))

def path_has_ext(path, ext):
    return os.path.splitext(path)[1] == ext

def path_remove_ext(path, ext):
    if path_has_ext(path, ext):
        return path[:-len(ext)]
    else:
        return path

def output_file_name(name):
    return path_remove_ext(name, DEFAULT_TEMPLATE_EXTENSION)

def reverse_dict(data):
    res = {}
    for key, value in data.items():
        res.setdefault(value, []).append(key)
    return res

class Status(enum.Enum):
    missing = 1
    stale   = 2
    fresh   = 3

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

    if args.force:
        log.debug("forcing all templates (--force)")
        status = dict.fromkeys(templates, Status.stale)
    else:
        status = check_freshness(args.inputdir, args.outputdir, templates)

    if not set(status.values()) - set([Status.fresh]):
        log.info("All templates up-to-date")
    elif args.action == "update":
        log.info("Compiling %d of %d templates" % (len(status), len(templates)))
        for target in status:
            compile_template(
                sections,
                path_join(args.inputdir, target),
                output_file_name(path_join(args.outputdir, target)),
                args.linkdir,
            )
    elif args.action in ("diff", "word-diff"):
        log.info("Diffing %d of %d templates" % (len(status), len(templates)))
        for target in status:
            diff_template(
                sections,
                path_join(args.inputdir, target),
                output_file_name(path_join(args.outputdir, target)),
                args.linkdir,
                word_diff_mode=(args.action == "word-diff")
            )
    elif args.action in ("summary"):
        groups = reverse_dict(status)
        if Status.missing in groups:
            log.info("Will create:")
            for target in sorted(groups[Status.missing]):
                print("    %s" % target)
        if Status.stale in groups:
            log.info("Will update:")
            for target in sorted(groups[Status.stale]):
                print("    %s" % target)
        if Status.fresh in groups:
            log.info("Up to date:")
            for target in sorted(groups[Status.fresh]):
                print("    %s" % target)
    else:
        raise NotImplementedError("Unknown action [%s]" % args.action)

def get_timestamp(filename):
    return datetime.fromtimestamp(os.stat(filename).st_mtime)

def check_freshness(idir, odir, templates):
    status = {}
    log.debug("scanning for templates to compile:")
    for name in templates:
        ifile = path_join(idir, name)
        ofile = output_file_name(path_join(odir, name))
        try:
            otime = get_timestamp(ofile)
        except OSError:
            log.debug("  template %s: not found" % ofile)
            status[name] = Status.missing
            continue

        if get_timestamp(ifile) > otime:
            status[name] = Status.stale
            log.debug("  template %s: stale" % ofile)
        else:
            status[name] = Status.fresh
            log.debug("  template %s: fresh" % ofile)
    return status

def find_template_files(path, extension=DEFAULT_TEMPLATE_EXTENSION):
    path = path_normalize(path)
    log.debug("Searching for templates in: %s" % path)
    i_files = []
    for root, _, files in os.walk(path):
        reldir = root[len(path):]
        for name in files:
            if path_has_ext(name, extension):
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

def diff_template(data, input_file, output_file, link_paths, word_diff_mode):
    text = render_template(data, input_file, output_file, link_paths)

    if os.path.exists(output_file):
        diff_target = output_file
    else:
        empty = tempfile.NamedTemporaryFile()
        diff_target = empty.name

    with tempfile.NamedTemporaryFile() as compiled:
        compiled.write(text.encode())
        compiled.flush()
        args = ["colordiff", "-u", diff_target, compiled.name]
        log.debug("  running diff: %s" % args)
        proc = subprocess.Popen(args, stdout=subprocess.PIPE)
        diff_lines = proc.stdout.readlines()
        if diff_lines:
            log.info("  %s: %d lines" % (output_file, len(diff_lines)))
        proc.wait()

def compile_template(data, input_file, output_file, link_paths):
    target_dir = os.path.dirname(output_file)
    if target_dir:
        os.makedirs(target_dir, exist_ok=True)

    text = render_template(data, input_file, output_file, link_paths)
    with open(output_file, "w") as output:
        output.write(text)
    log.info("Compiled template [%s]" % output_file)

def render_template(data, input_file, output_file, link_paths):
    try:
        template_data = open(input_file).read()
        text = transwarp.template.generate(template_data, data, link_paths)
        return text
    except ImportError as E:
        log.error("Compiler plugin [%s] not found for [%s]. Add search path with -L<path>" % (E.name, output_file))
        E.name
        sys.exit(2)
    except:
        transwarp.template.present_template_error()
        sys.exit(1)
