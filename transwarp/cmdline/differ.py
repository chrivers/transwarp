import os
import shutil
import logging as log
import subprocess
from transwarp.cmdline.pathutils import *

class Differ(object):

    @staticmethod
    def _find_diff_util():
        return os.environ.get("DIFF") or "diff"
    
    def __init__(self, args, diff_prog=None):
        if diff_prog:
            self.diff_cmd = diff_prog
        else:
            self.diff_cmd = self._find_diff_util()

        if not shutil.which(self.diff_cmd):
            raise FileNotFoundError("Diff program [%s] not found" % self.diff_cmd)

        self.args = args

    def diff(self, file_a, file_b, labels=None, touch_if_identical=True):
        args = [self.diff_cmd]
        args.extend(self.args)
        if labels:
            args.append("--label")
            args.append(labels[0])
        args.append(file_a)
        if labels:
            args.append("--label")
            args.append(labels[1])
        args.append(file_b)
        log.debug("  running diff: %s" % args)
        proc = subprocess.Popen(args, stdin=subprocess.DEVNULL)
        retcode = proc.wait()
        if retcode == 0:
            if touch_if_identical:
                log.info("  %-32s unchanged (updating timestamp)" % (file_a))
                path_touch(file_a)
            else:
                log.info("  %-32s unchanged" % (file_a))
        elif retcode == 1:
            log.info("  %-32s modified" % (file_a))
        else:
            log.error("Failed to run diff (retcode %d)" % retcode)
            return False

