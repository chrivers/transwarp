import textwrap

def format_comment(comment, indent, width):
    res = []
    for line in comment:
        res.extend(
            textwrap.wrap(
                line,
                initial_indent=indent,
                subsequent_indent=indent,
                width=width,
            )
        )
    return res
