import re
from collections import OrderedDict
from .grammar import *
from .parser import parse_lines
from .struct import Struct

class Packet(object):
    def __init__(self, header, lines, comment):
        fields = OrderedDict()
        for item in parse_lines(iter(lines)):
            fields[item[0]] = Struct(item[0], item[2], item[3])
        self._name = header
        self._cmt = comment
        self.fields = fields

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._cmt
