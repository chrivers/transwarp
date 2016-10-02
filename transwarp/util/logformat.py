import sys
import logging
import datetime

class Formatter(object):
    def __init__(self, color=None, include_date=False):
        self._include_date = include_date
        if color is None:
            color = sys.stdin.isatty()

        if color:
            self.color = {
                "normal":    "\033[m",
                "fg_green":  "\033[32;1m",
                "fg_yellow": "\033[33;1m",
                "fg_red":    "\033[31;1m",
                "fg_blue":   "\033[34;1m",
                "fg_purple": "\033[35;1m",
                "fg_white":  "\033[;1m",
            }
        else:
            self.color = {}

        self.levelsymbols = {
            10: "D",
            20: "*",
            30: "W",
            40: "E",
            50: "F",
        }
        self.levelcolors = {
            10: self.color["fg_green"],
            20: self.color["fg_green"],
            30: self.color["fg_yellow"],
            40: self.color["fg_red"],
            50: self.color["fg_purple"],
        }

    def format_date(self):
        if self._include_date:
            return "%s%s " % (self.color("fg_white"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            return ""

    def format(self, record):
        level = record.levelno
        if record.name == "root":
            name = ""
        else:
            name = "%s: " % record.name
        cl = self.color
        return "%s%s[%s%s%s]%s %s%s" % (
            self.format_date(),
            cl["fg_blue"],
            self.levelcolors[level],
            self.levelsymbols[level],
            cl["fg_blue"],
            cl["normal"],
            name,
            record.msg
        )

def set_level(level):
    loggin.getLogger().setLevel(level)

def initialize(level=logging.INFO, **kwargs):
    fmt = Formatter(**kwargs)
    logging.basicConfig(level=level)
    logging.getLogger().handlers[0].setFormatter(fmt)

if __name__ == "__main__":
    initialize(logging.DEBUG)
    logging.debug("This is debug")
    logging.info("This is info")
    logging.warning("This is warning")
    logging.error("This is error")
    logging.critical("This is critical")
