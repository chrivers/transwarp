import re

RE_BLANK        = re.compile("^\s+$|^\s*##.*")
RE_DOC          = re.compile("^((?:    )*)#([^#]?.*)$")
RE_BLOCK_START  = re.compile("^((?:    )*)(\w+)\s+(\w+)(?:\((.+)\))?$")
RE_BLOCK_CONST  = re.compile("^((?:    )*)(\w+)\s*=\s*(.*)")
RE_BLOCK_FIELD  = re.compile("^((?:    )*)(\w+)\s*:\s*(.*)")
RE_TYPE         = re.compile("([\w:.]+)(?:<(.+)>)?")
RE_IDENT_SPLIT  = re.compile("(\w+)(::|\.)(.*)")
