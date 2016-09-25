import re
from .grammar import *
from .parser import RE_DOC

class Struct(object):
    def __init__(self, header, lines, comment):
        RE_STRUCT_FIELD = re.compile("(\w+):\s*(.*)")
        fields = []
        comment = []
        for line in lines:
            doc = RE_DOC.match(line)
            if doc:
                comment.append(doc.group(1).strip())
                continue
            field = RE_STRUCT_FIELD.match(line)
            if field:
                name, typ = field.groups()
                fields.append((name, typ, comment))
                comment = []
        self._name = header
        self.fields = fields
        self._comment = comment

    @property
    def name(self):
        return self._name
