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
import transwarp.export.xml
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
    for path in args.linkdir:
        compiler.add_link_dir(path)
    compiler.load_stf(args.datadir)
    compiler.compile()

    if args.action == "export":
        if args.export_mode == "xml":
            transwarp.export.xml.export(compiler.data)
            return True
        else:
            raise NotImplementedError("Unknown export mode [%s]" % args.export_mode)

    log.debug("input mtime [%s]" % compiler.most_recent_mtime)
    log.debug("Searching for templates in: %s" % args.inputdir)
    if not changes.find_templates(args.inputdir, compiler.most_recent_mtime):
        log.error("No templates found (searched for %s in '%s')" % (args.extension, args.inputdir))
        log.error("  hint: you can specify target dir with -I <path>")
        return False

    changes.find_modifications()

    groups = changes.grouped()
    if not changes and args.action != "summary":
        log.info("All templates up-to-date")
    elif args.action == "update":
        for target in changes:
            log.info("Updated %s" % target.output_file)
            target.update(compiler, differ)
    elif args.action in ("diff", "word-diff"):
        log.info("Diffing %d of %d templates" % (len(changes), len(changes.templates)))
        for target in changes:
            target.diff(compiler, differ)
    elif args.action == "summary":
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
