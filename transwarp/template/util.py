import textwrap

context = None

def _set_context(ctx):
    global context
    context = ctx

def _get_context():
    return context

def format_comment(comment, indent, width):
    res = []
    for line in comment:
        if line:
            res.extend(
                textwrap.wrap(
                    line,
                    initial_indent=indent,
                    subsequent_indent=indent,
                    width=width,
                )
            )
        else:
            res.append(indent.rstrip())
    return res
