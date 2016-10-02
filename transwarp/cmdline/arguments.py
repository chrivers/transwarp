from argparse import ArgumentParser, HelpFormatter

parser = ArgumentParser(formatter_class = lambda prog: HelpFormatter(prog, max_help_position=42, width=80))

parser.prog = "transwarp"

parser.add_argument(
    "-v", "--verbose",
    action="append_const",
    const=-10,
    default=[],
    dest="verbosity",
    help="Increase verbosity"
)

parser.add_argument(
    "-q", "--quiet",
    action="append_const",
    const=10,
    dest="verbosity",
    help="Decrease verbosity"
)

parser.add_argument(
    "-w", "--word-diff",
    action="store_true",
    dest="worddiff",
    help="Use word-diff mode",
)

parser.add_argument(
    "-D", "--data-dir",
    action="store",
    dest="datadir",
    help="Directory that stores .stf files",
    metavar="<path>"
)

parser.add_argument(
    "-I", "--input-dir",
    action="store",
    dest="inputdir",
    help="Input directory for template files",
    metavar="<path>"
)

parser.add_argument(
    "-O", "--output-dir",
    action="store",
    dest="outputdir",
    help="Output directory for compiled templates",
    metavar="<path>"
)

parser.add_argument(
    "-W", "--write",
    action="store_true",
    dest="write",
    help="Render all templates to the output directory",
)

parser.add_argument(
    "-U", "--update",
    action="store_true",
    dest="write",
    help="Update all templates, skipping unchanged ones",
)
