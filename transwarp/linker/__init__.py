import logging as log
from transwarp.parser.type import Type
from pprint import pprint, pformat
from transwarp.parser.grammar import RE_IDENT_SPLIT

def lookup(root, name):
    node = root
    remainder = name
    while True:
        match = RE_IDENT_SPLIT.match(remainder)
        if match:
            step, mode, remainder = match.groups()
            node = node.get(step)
        else:
            node = node.get(remainder)
            break
    return node

def link_field(root, fd):
    fd._type = link_type(root, fd._type)

def link_type(root, tp):
    tp._args = [link_type(root, t) for t in tp._args]
    if "." in tp.name:
        blk = lookup(root, tp.name)
        if not blk:
            log.error("Could not resolve typename [%s]" % tp.name)
            return
        return Type(blk.expr, [Type(blk.name, tp._args)], link=blk)
    else:
        return tp

def link_block(root, node):
    for block in node.blocks:
        link_block(root, block)
    for field in node.fields:
        link_field(root, field)

def link(data):
    for block in data:
        link_block(data, block)
    return data
