import re

RE_BLANK        = re.compile("^\s+$|^\s*##.*")
RE_DOC          = re.compile("^#([^#]?.*)$")
RE_SECTION      = re.compile("^(\w+)\s*(.*)$")
RE_FIELD        = re.compile("^    (.*)")
RE_ENUM_FIELD   = re.compile("(\w+)\s*=\s*(\w+)")
RE_STRUCT_FIELD = re.compile("(\w+):\s*(.*)")
RE_TYPE         = re.compile("(\w+)(?:<(?:(.+?)(?:,\s*(.+))?)>)?$")
