import glob
import datetime
import fileinput
import logging as log

import transwarp.template

from transwarp.cmdline.pathutils import *

class Compiler(object):

    def __init__(self):
        self.link_paths = set()
        self.files = set()

    def add_link_dir(self, link_dir):
        self.link_paths.add(link_dir)

    def load_stf(self, datadir):
        files = glob.glob("%s/*.stf" % datadir)
        if files:
            log.debug("found stf files:")
            for name in files:
                log.debug("  %s" % name)
                self.files.add(name)
        else:
            raise LookupError("Could not find any .stf files in %r" % datadir)

    @property
    def most_recent_mtime(self):
        newest = datetime.datetime.fromtimestamp(0)
        for name in self.files:
            newest = max(newest, path_mtime(name))
        return newest

    def compile(self):
        all_lines = fileinput.input(files=self.files)
        log.debug("parsed %d stf files" % (len(self.files)))
        self.data = transwarp.parser.parse(all_lines)

    def render(self, template):
        return transwarp.template.generate(
            template,
            self.data,
            self.link_paths,
        )
