from transwarp.util.data import SearchableList
from transwarp.parser.grammar import *
from transwarp.parser.strutil import *

class Block(object):
    def __init__(self, name, expr, blocks, fields, consts, arg, comment):
        self._parent = None
        self._cmt = comment
        self._name = name
        self._expr = expr
        self.arg = arg
        self.fields = fields
        self.blocks = blocks
        for block in blocks:
            block._parent = self
        self.consts = consts
        tw = text_width(consts)
        hw = hex_width(consts)
        for const in self.consts:
            const._name_width = tw
            const._value_width = hw

    def __repr__(self):
        return "BLOCK<%s, %s, %s>{ blocks = {%s}, fields = {%s}, consts = {%s} }" % (
            self._name,
            self._expr,
            self.arg,
            ", ".join(f.name for f in self.blocks),
            ", ".join(f.name for f in self.fields),
            ", ".join(f.name for f in self.consts),
        )

    def __lt__(self, other):
        return self._name < other._name

    def __iter__(self):
        return iter(self.blocks)
