import re

RE_BLANK   = re.compile("^\s+$|^\s*##.*")
RE_DOC     = re.compile("^#([^#].*)$")
RE_SECTION = re.compile("^(\w+)\s*(.*)$")
RE_FIELD   = re.compile("^    (.*)")
