MIN_TEXT_WIDTH = 20
MIN_HEX_WIDTH = 2

def text_width(cases):
    # find the longest string, go with that
    # unless smaller than MIN_TEXT_WIDTH, then go with that instead
    return max(max(len(case[0]) for case in cases), MIN_TEXT_WIDTH)

def hex_width(cases):
    # find an even number of hex digits that will fit all fields
    # unless smaller than MIN_HEX_WIDTH, then go with that instead
    return max(max(round(len("%x" % case[1]) / 2.0) * 2 for case in cases), MIN_HEX_WIDTH)
