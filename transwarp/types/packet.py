from transwarp.util.data import SearchableList
from transwarp.parser.grammar import *
from transwarp.parser.parser import parse_lines
from transwarp.types.struct import Struct
from transwarp.types import SectionObject

class Packet(SectionObject):
    def __init__(self, header, lines, comment):
        fields = SearchableList()
        for item in parse_lines(iter(lines)):
            fields.append(Struct(item[0], item[2], item[3]))
        self._name = header
        self._cmt = comment
        self.fields = fields

    @property
    def name(self):
        return self._name

    @property
    def comment(self):
        return self._cmt
