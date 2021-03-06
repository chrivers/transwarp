MIN_TEXT_WIDTH = 0
MIN_HEX_WIDTH = 2

def text_width(cases):
    # find the longest string, go with that
    # unless smaller than MIN_TEXT_WIDTH, then go with that instead
    if cases:
        return max(max(len(case.name) for case in cases), MIN_TEXT_WIDTH)
    else:
        return 0

def hex_width(cases):
    # find an even number of hex digits that will fit all fields
    # unless smaller than MIN_HEX_WIDTH, then go with that instead
    if cases:
        return max(max(round(len("%x" % case.expr) / 2.0) * 2 for case in cases), MIN_HEX_WIDTH)
    else:
        return 0
