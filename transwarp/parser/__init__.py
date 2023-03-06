import os
import logging as log
from transwarp.util.data import SearchableList
from transwarp.parser.field import Field
from transwarp.parser.const import Const
from transwarp.parser.type import Type
from transwarp.parser.block import Block
from transwarp.parser.grammar import RE_DOC, RE_BLANK, RE_BLOCK_START, RE_BLOCK_FIELD, RE_BLOCK_CONST

class Parser(object):

    def __init__(self, lines):
        self.lines = lines
        self._lastline = None

    @property
    def line(self):
        return self._lastline

    def nextline(self):
        try:
            self._lastline = next(self.lines)
        except StopIteration:
            self._lastline = ""
        return self._lastline

    def parse_block(self, level=0):
        self.nextline()
        blocks = SearchableList()
        fields = SearchableList()
        consts = SearchableList()
        comment = []
        while self.line:
            if RE_BLANK.match(self.line):
                # print("BLANK: [%r]" % self.line)
                self.nextline()
                continue

            docline = RE_DOC.match(self.line)
            if docline:
                # print("DOC: %r" % (docline.groups(), ))
                curlevel = len(docline.group(1) or "") / 4
                if curlevel != level and level:
                    break
                comment.append(docline.group(2).strip())

                self.nextline()
                continue

            field = RE_BLOCK_FIELD.match(self.line)
            if field:
                # print("FIELD: %r" % (field.groups(), ))
                curlevel = len(field.group(1) or "") / 4
                if curlevel != level and level:
                    break
                fields.append(Field(field.group(2), Type.parse(field.group(3)), comment=comment))
                comment = []

                self.nextline()
                continue

            const = RE_BLOCK_CONST.match(self.line)
            if const:
                # print("CONST: %r" % (const.groups(), ))
                curlevel = len(const.group(1) or "") / 4
                if curlevel != level and level:
                    break
                consts.append(Const(const.group(2), Const.parse(const.group(3)), comment=comment))
                comment = []

                self.nextline()
                continue

            block = RE_BLOCK_START.match(self.line)
            if block:
                # print("BLOCK: %r" % (block.groups(), ))
                curlevel = len(block.group(1) or "") / 4
                if curlevel != level and level:
                    break
                _blocks, _fields, _consts = self.parse_block(level=level + 1)
                blocks.append(Block(
                    name=block.group(3),
                    expr=block.group(2),
                    blocks=_blocks,
                    fields=_fields,
                    consts=_consts,
                    comment=comment,
                ))
                comment = []
                continue

            raise ValueError("Parse error for line: %r" % self.line)

        return blocks, fields, consts

def parse(files):
    res = SearchableList()
    for name in sorted(files):
        log.debug("Parsing file [%r]" % name)
        lines = open(name)
        parser = Parser(lines)
        ident = os.path.splitext(os.path.basename(name))[0]
        blocks, fields, consts = parser.parse_block()
        res.append(Block(name=ident, expr=name, blocks=blocks, fields=fields, consts=consts, comment=name))
    return res
