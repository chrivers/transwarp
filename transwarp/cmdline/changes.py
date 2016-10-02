import os
import enum
import glob
import datetime
import logging as log

from transwarp.cmdline.pathutils import *

class Status(enum.Enum):
    unknown = 0
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

    def find_templates(self, path):
        for root, _, files in os.walk(path):
            reldir = root[len(path):]
            templates = {}
            for name in files:
                if path_has_ext(name, self.extension):
                    relpath = path_join(reldir, name)
                    log.debug("  template %s" % relpath)
                    templates[relpath] = Template(relpath, name, self.output_dir, name)
            self.templates.update(templates)
            return templates

    def find_modifications(self, deadline=None):
        if self.force_all:
            log.debug("forcing all templates (--force)")
            status = dict.fromkeys(templates, Status.stale)
        else:
            log.debug("scanning for templates to compile:")
            for template in self.templates.values():
                log.debug("  template %s: %s" % (template.output_file, template.check_freshness(deadline)))

class Template(object):

    def __init__(self, input_dir, input_filename, output_dir, output_filename):
        self.status = Status.unknown
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.input_filename = input_filename
        self.output_filename = output_filename

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
        
    def check_freshness(self, deadline):
        otime = self.output_mtime
        if not otime:
            return Status.missing
        elif max(path_mtime(ifile), newest_date) > otime:
            return Status.stale
        else:
            return Status.fresh

