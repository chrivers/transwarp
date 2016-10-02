import os
import sys
import glob
import datetime
import tempfile
import fileinput
import subprocess
import logging as log

import transwarp.parser
import transwarp.template
import transwarp.util.logformat
import transwarp.cmdline.arguments
from transwarp.cmdline.changes import Changes, Status
from transwarp.cmdline.pathutils import *

DEFAULT_TEMPLATE_EXTENSION = ".tpl"

def main(args=None):
    transwarp.util.logformat.initialize()
    args = transwarp.cmdline.arguments.parse_and_validate()

    changes = Changes(args.outputdir, args.force, DEFAULT_TEMPLATE_EXTENSION)

    files, newest_date = changes.find_stf_files(args.datadir)

    # parse all sections into a unified data structure, that the
    # templates can inspect
    all_lines = fileinput.input(files=files)
    log.debug("parsed %d stf files" % (len(files)))
    sections = transwarp.parser.parse(all_lines)

    log.debug("Searching for templates in: %s" % args.inputdir)
    if not changes.find_templates(args.inputdir, newest_date):
        log.error("No templates found (searched for %s in '%s')" % (DEFAULT_TEMPLATE_EXTENSION, args.inputdir))
        log.error("  hint: you can specify target dir with -I <path>")
        return False

    changes.find_modifications()

    groups = changes.grouped()
    if not changes:
        log.info("All templates up-to-date")
    elif args.action == "update":
        log.info("Compiling %d of %d templates" % (len(changes), len(changes.templates)))
        for target in changes:
            compile_template(
                sections,
                target.input_file,
                target.output_file,
                args.linkdir,
            )
    elif args.action in ("diff", "word-diff"):
        log.info("Diffing %d of %d templates" % (len(changes), len(changes.templates)))
        for target in changes:
            diff_template(
                sections,
                target.input_file,
                target.output_file,
                args.linkdir,
                word_diff_mode=(args.action == "word-diff")
            )
    elif args.action in ("summary"):
        if Status.missing in groups:
            log.info("Will create:")
            for target in sorted(groups[Status.missing]):
                print("    %s" % target.output_file)
        if Status.stale in groups:
            log.info("Will update:")
            for target in sorted(groups[Status.stale]):
                print("    %s" % target.output_file)
        if Status.fresh in groups:
            log.info("Up to date:")
            for target in sorted(groups[Status.fresh]):
                print("    %s" % target.output_file)
    else:
        raise NotImplementedError("Unknown action [%s]" % args.action)


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
        else:
            log.info("  %-32s unchanged (updating timestamp)" % (output_file))
            path_touch(output_file)
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
        log.error("Compiler plugin [%s] not found for [%s]" % (E.name, output_file))
        log.error("  hint: Add search path with -L<path>")
        E.name
        sys.exit(2)
    except:
        transwarp.template.present_template_error()
        sys.exit(1)
