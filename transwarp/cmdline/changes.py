import os
import sys
import enum
import glob
import datetime
import tempfile
import logging as log

import transwarp.template
from transwarp.cmdline.pathutils import *

class Status(enum.Enum):
    missing = 1
    stale   = 2
    fresh   = 3

class Changes(object):

    def __init__(self, output_dir, force_all, extension, filterfunc):
        self.extension = extension
        self.force_all = force_all
        self.output_dir = output_dir
        self.templates = {}
        self.filterfunc = filterfunc

    def __bool__(self):
        for item in self.templates.values():
            if item.status != Status.fresh:
                return True
        return False

    def __len__(self):
        return sum(1 for template in self.templates.values() if not template.fresh)

    def __iter__(self):
        return iter(template for template in sorted(self.templates.values()) if not template.fresh)

    def __getitem__(self, status):
        return iter(template for template in sorted(self.templates.values()) if template.status == status)

    def grouped(self):
        res = {}
        for key, value in sorted(self.templates.items()):
            res.setdefault(value.status, []).append(value)
        return res

    def output_file_name(self, name):
        return path_remove_ext(name, self.extension)

    def find_templates(self, path, minimum_mtime):
        templates = {}
        for root, _, files in os.walk(path):
            reldir = root[len(path):]
            for name in files:
                relpath = path_join(reldir, name)
                if not self.filterfunc(relpath):
                    log.debug("  ignoring %s due to filter" % relpath)
                    continue
                if path_has_ext(name, self.extension):
                    log.debug("  template %s" % relpath)
                    templates[relpath] = Template(path, relpath, self.output_dir, self.output_file_name(relpath), minimum_mtime)
            self.templates.update(templates)
        return templates

    def find_modifications(self):
        if self.force_all:
            log.debug("forcing all templates (--force)")
            for template in self.templates.values():
                template.expire()
        else:
            log.debug("scanning for templates to compile:")
            for name, template in sorted(self.templates.items()):
                log.debug("  template %s: %s" % (template.output_file, template.status.name))

class Template(object):

    def __init__(self, input_dir, input_filename, output_dir, output_filename, minimum_mtime=None):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.input_filename = input_filename
        self.output_filename = output_filename
        if minimum_mtime is None:
            self.minimum_mtime = datetime.datetime.fromtimestamp(0)
        else:
            self.minimum_mtime = minimum_mtime
        self.refresh_status()

    def __lt__(self, other):
        return self.output_file < other.output_file

    @property
    def input_file(self):
        return path_join(self.input_dir, self.input_filename)

    @property
    def output_file(self):
        return path_join(self.output_dir, self.output_filename)

    @property
    def input_mtime(self):
        return path_mtime(self.input_file)

    @property
    def output_mtime(self):
        return path_mtime(self.output_file)

    @property
    def fresh(self):
        return self._status == Status.fresh

    @property
    def status(self):
        return self._status

    def expire(self):
        self._status = Status.stale

    def refresh_status(self):
        otime = self.output_mtime
        itime = self.input_mtime
        if not otime:
            self._status = Status.missing
        elif max(self.input_mtime, self.minimum_mtime) > otime:
            self._status = Status.stale
        else:
            self._status = Status.fresh

    def render(self, compiler):
        try:
            return compiler.render(self.input_file)
        except ImportError as E:
            log.error("Compiler plugin [%s] not found for [%s]" % (E.name, self.output_file))
            log.error("  hint: Add search path with -L<path>")
            E.name
            sys.exit(2)
        except:
            transwarp.template.present_template_error()
            sys.exit(1)

    def diff(self, compiler, differ):
        text = self.render(compiler)

        with tempfile.NamedTemporaryFile() as compiled:
            compiled.write(text.encode())
            compiled.flush()
            differ.diff(
                self.output_file,
                compiled.name,
                labels=(
                    "%s (existing)" % self.output_file,
                    "%s (compiled)" % self.output_file
                )
            )

    def update(self, compiler, differ):
        text = compiler.render(self.input_file)

        target_dir = os.path.dirname(self.output_file)
        if target_dir:
            os.makedirs(target_dir, exist_ok=True)
        with open(self.output_file, "w") as output:
            output.write(text)
