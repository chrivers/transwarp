import os
import sys
import glob
import datetime
import fileinput
import subprocess
import logging as log

import transwarp.parser
import transwarp.template
import transwarp.util.logformat
import transwarp.cmdline.arguments
from transwarp.cmdline.differ import Differ
from transwarp.cmdline.changes import Changes, Status
from transwarp.cmdline.compiler import Compiler
from transwarp.cmdline.pathutils import *

def main(args=None):
    transwarp.util.logformat.initialize()
    args = transwarp.cmdline.arguments.parse_and_validate()

    differ = Differ(["-u", "-N"])
    changes = Changes(args.outputdir, args.force, args.extension)
    compiler = Compiler()
    compiler.load_stf(args.datadir)

    log.debug("input mtime [%s]" % compiler.most_recent_mtime)
    log.debug("Searching for templates in: %s" % args.inputdir)
    if not changes.find_templates(args.inputdir, compiler.most_recent_mtime):
        log.error("No templates found (searched for %s in '%s')" % (args.extension, args.inputdir))
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
            target.diff(compiler, differ)
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
