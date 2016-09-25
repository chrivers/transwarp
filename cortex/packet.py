import re
from .grammar import *
from .parser import parse_lines
from .struct import Struct

class Packet(object):
    def __init__(self, header, lines, comment):
        fields = [Struct(c[0], c[2], c[3]) for c in parse_lines(iter(lines))]
        self._name = header
        self._cmt = comment
        self.fields = fields

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._cmt
