from transwarp.util.data import SearchableList
from transwarp.parser.grammar import *

class Field(object):
    def __init__(self, name, type, comment):
        self._name = name
        self._type = type
        self._cmt = comment

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def comment(self):
        return self._cmt
