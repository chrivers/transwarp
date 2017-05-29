from transwarp.util.data import SearchableList
from transwarp.parser.grammar import *
from transwarp.parser.strutil import *

class Block(object):
    def __init__(self, name, expr, blocks, fields, consts, comment):
        self._parent = None
        self._cmt = comment
        self._name = name
        self._expr = expr
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
        tw = text_width(fields)
        for field in self.fields:
            field._name_width = tw

    def __repr__(self):
        return "BLOCK<%s, %s>{ blocks = {%s}, fields = {%s}, consts = {%s} }" % (
            self._name,
            self._expr,
            ", ".join(f.name for f in self.blocks),
            ", ".join(f.name for f in self.fields),
            ", ".join(f.name for f in self.consts),
        )

    def __lt__(self, other):
        return self._name < other._name

    def __iter__(self):
        return iter(self.blocks)

    @property
    def name(self):
        return self._name

    @property
    def expr(self):
        return self._expr

    @property
    def parent(self):
        return self._parent

    @property
    def path(self):
        top = self
        res = []
        while top:
            res.append(top.name)
            top = top.parent
        res.reverse()
        return res

    @property
    def fullname(self):
        return "::".join(self.path)

    def without(self, *names):
        return self.blocks.without(*names)

    def get(self, name, default=...):
        return self.blocks.get(name, default)

    def const(self, name, default=...):
        if name in self.consts:
            return self.consts.get(name).expr
        else:
            return default
