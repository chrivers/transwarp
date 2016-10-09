import fileinput
from transwarp.parser.file import File
from transwarp.parser.grammar import RE_PARSER_DEF, RE_STRUCT_FIELD, RE_DOC, RE_BLANK, RE_BLOCK, RE_FIELD

class Parser(object):

    def __init__(self, lines):
        self.lines = lines

    def nextline(self):
        try:
            return next(self.lines)
        except StopIteration:
            return ""

    def parse_file(self):
        blocks = []
        comment = []
        line = self.nextline()
        while line:
            if RE_BLANK.match(line):
                line = self.nextline()
                continue
            docline = RE_DOC.match(line)
            if docline:
                comment.append(docline.group(1).strip())
                line = self.nextline()
                continue

            block = RE_BLOCK.search(line)
            if block:
                block_comment = comment[:]
                block_lines = []
                comment = []
                while line:
                    line = self.nextline()
                    if RE_BLANK.match(line):
                        continue

                    field = RE_FIELD.match(line)
                    if field:
                        block_lines.append(field.group(1))
                    else:
                        typ, header = block.groups()
                        blocks.append((typ, header, block_lines, block_comment))
                        break
                continue
            else:
                raise ValueError("Unknown line: %r" % line)
        return blocks

from pprint import pprint
def parse(files):
    lines = fileinput.input(files=files)
    parser = Parser(lines)
    pprint(parser.parse_file())

    return {}
