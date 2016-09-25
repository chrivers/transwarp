import textwrap

def format_comment(comment, indent, width):
    return textwrap.wrap(
        "\n".join(comment),
        initial_indent=indent,
        subsequent_indent=indent,
        width=width,
    )
