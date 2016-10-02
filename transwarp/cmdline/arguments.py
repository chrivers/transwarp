import sys
import logging as log
import argparse
import transwarp.util.logformat

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

    def _get_formatter(self):
        return argparse.HelpFormatter(self.prog, max_help_position=42, width=100)

parser = ArgumentParser(prog="transwarp")

parser.add_argument(
    "-a", "--all",
    action="store_true",
    dest="all",
    help="Compile all templates, instead of trying to detect changes"
)

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
    "-F", "--filter",
    action="store",
    dest="write",
    help="Ignore all templates outside of target <path>",
    metavar="<path>"
)

def parse_and_validate():
    try:
        args = parser.parse_args()
        transwarp.util.logformat.set_level(sum(args.verbosity) + log.INFO)
        log.debug("parsed arguments: %r" % args)

        if not args.datadir:
            raise ValueError("datadir (-D) is required")
        if args.inputdir and not args.outputdir:
            raise ValueError("output dir (-O) is required with input dir (-I)")
        if args.outputdir and not args.inputdir:
            raise ValueError("input dir (-I) is required with output dir (-O)")
        return args
    except ValueError as E:
        print(parser.format_help(), file=sys.stderr)
        raise
