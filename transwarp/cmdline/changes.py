import os
import enum
import glob
import datetime
import logging as log

from transwarp.cmdline.pathutils import *

class Status(enum.Enum):
    missing = 1
    stale   = 2
    fresh   = 3

class Changes(object):

    def __init__(self, output_dir, force_all, extension):
        self.extension = extension
        self.force_all = force_all
        self.output_dir = output_dir
        self.templates = {}

    @staticmethod
    def find_stf_files(datadir):
        files = glob.glob("%s/*.stf" % datadir)
        if files:
            newest = datetime.datetime.fromtimestamp(0)
            log.debug("found stf files:")
            for name in files:
                log.debug("  %s" % name)
                newest = max(newest, path_mtime(name))
            return files, newest
        else:
            raise LookupError("Could not find any .stf files in %r" % datadir)

    def __bool__(self):
        for item in self.templates.values():
            if item.status != Status.fresh:
                return True
        return False

    def __len__(self):
        return sum(1 for template in self.templates.values() if not template.fresh)

    def __iter__(self):
        return iter(template for template in self.templates.values() if not template.fresh)

    def __getitem__(self, status):
        return iter(template for template in self.templates.values() if template.status == status)

    def grouped(self):
        res = {}
        for key, value in self.templates.items():
            res.setdefault(value.status, []).append(value)
        return res

    def output_file_name(self, name):
        return path_remove_ext(name, self.extension)

    def find_templates(self, path, minimum_mtime):
        for root, _, files in os.walk(path):
            reldir = root[len(path):]
            templates = {}
            for name in files:
                if path_has_ext(name, self.extension):
                    relpath = path_join(reldir, name)
                    log.debug("  template %s" % relpath)
                    templates[relpath] = Template(path, relpath, self.output_dir, self.output_file_name(relpath), minimum_mtime)
            self.templates.update(templates)
        return templates

    def find_modifications(self):
        if self.force_all:
            log.debug("forcing all templates (--force)")
            status = dict.fromkeys(templates, Status.stale)
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

    def refresh_status(self):
        otime = self.output_mtime
        itime = self.input_mtime
        if not otime:
            self._status = Status.missing
        elif max(self.input_mtime, self.minimum_mtime) > otime:
            self._status = Status.stale
        else:
            self._status = Status.fresh
