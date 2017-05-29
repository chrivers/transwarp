from transwarp.util.data import SearchableList
from transwarp.parser.grammar import *

class Const(object):
    def __init__(self, name, expr, comment):
        self._cmt = comment
        self._name = name
        self._expr = expr
        self._name_width = None
        self._value_width = None

    @property
    def name(self):
        return self._name

    @property
    def expr(self):
        return self._expr

    @property
    def comment(self):
        return self._cmt

    @property
    def aligned_name(self):
        return "{:{width}}".format(self._name, width=self._name_width)

    @property
    def hex_value(self):
        return "0x{:x}".format(self._expr)

    @property
    def aligned_hex_value(self):
        return "0x{:0{width}x}".format(int(str(self._expr), 0), width=self._value_width)
