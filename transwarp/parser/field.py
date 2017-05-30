from transwarp.util.data import SearchableList
from transwarp.parser.grammar import *

class Field(object):
    def __init__(self, name, type, comment):
        self._name = name
        self._type = type
        self._cmt = comment
        self._name_width = 20

    def __repr__(self):
        return "FIELD{%s: %s}" % (
            self._name,
            self._type,
        )

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def comment(self):
        return self._cmt

    @property
    def aligned_name(self):
        return "{:{width}}".format(self._name, width=self._name_width)
