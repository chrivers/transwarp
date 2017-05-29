import sys
import logging as log
import argparse
import transwarp.util.logformat
from transwarp.cmdline.pathutils import path_normalize
import transwarp

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

    def _get_formatter(self):
        return argparse.HelpFormatter(self.prog, max_help_position=42, width=100)

parser = ArgumentParser(prog="transwarp-%s" % transwarp.__version__, add_help=False)

_info = parser.add_argument_group("Information")

_info.add_argument(
    "-v", "--verbose",
    action="append_const",
    const=-10,
    default=[],
    dest="verbosity",
    help="Increase verbosity"
)

_info.add_argument(
    "-q", "--quiet",
    action="append_const",
    const=10,
    dest="verbosity",
    help="Decrease verbosity"
)

_info.add_argument(
    "-h", "--help",
    action="help",
    help="Show help"
)

_output = parser.add_argument_group("File output")

_output.add_argument(
    "-f", "--force",
    action="store_true",
    dest="force",
    default=False,
    help="Force recompilation of unchanged templates"
)

_output.add_argument(
    "-d", "--diff",
    action="store_const",
    const="diff",
    dest="action",
    default="diff",
    help="Unified diff mode (default)",
)

_output.add_argument(
    "-w", "--word-diff",
    action="store_const",
    const="word-diff",
    dest="action",
    help="Word-diff mode",
)

_output.add_argument(
    "-s", "--summary",
    action="store_const",
    const="summary",
    dest="action",
    default="summary",
    help="Summary mode (show changed/fresh files without diffs)",
)

_output.add_argument(
    "-u", "--update",
    action="store_const",
    const="update",
    dest="action",
    help="Write changes to files"
)

_output.add_argument(
    "-x", "--export",
    action="store",
    dest="export_mode",
    metavar="<mode>",
    help="Export data structure (supported modes: xml)"
)

_paths = parser.add_argument_group("Input and output paths")

_paths.add_argument(
    "-D", "--data-dir",
    action="store",
    dest="datadir",
    help="Directory that stores .stf files",
    metavar="<path>"
)

_paths.add_argument(
    "-L", "--ĺib-dir",
    action="append",
    dest="linkdir",
    help="Search path for compiler plugins",
    default=[],
    metavar="<path>"
)

_paths.add_argument(
    "-I", "--input-dir",
    action="store",
    dest="inputdir",
    help="Input directory for template files",
    default=".",
    metavar="<path>"
)

_paths.add_argument(
    "-O", "--output-dir",
    action="store",
    dest="outputdir",
    help="Output directory for compiled templates",
    default=".",
    metavar="<path>"
)

_paths.add_argument(
    "-F", "--filter",
    action="append",
    dest="filter",
    help="Ignore all templates outside of target <path>",
    default=[],
    metavar="<path>"
)

_paths.add_argument(
    "-e", "--extension",
    action="store",
    dest="extension",
    default="tpl",
    help="Template extension. Other files will be ignored (default: .tpl)",
    metavar="<name>"
)

def parse_and_validate():
    try:
        args = parser.parse_args()
        transwarp.util.logformat.set_level(sum(args.verbosity) + log.INFO)
        log.debug("parsed arguments: %r" % args)

        if not args.datadir:
            raise ValueError("datadir (-D) is required")
        if args.export_mode:
            args.action = "export"
        if args.outputdir != ".":
            for index, filt in enumerate(args.filter):
                if filt.startswith(args.outputdir):
                    args.filter[index] = filt[len(args.outputdir)+1:]

        args.inputdir  = path_normalize(args.inputdir)
        args.outputdir = path_normalize(args.outputdir)
        args.linkdir   = [path_normalize(linkdir) for linkdir in args.linkdir]
        args.extension = "." + args.extension.lstrip(".")
        return args
    except ValueError as E:
        print(parser.format_help(), file=sys.stderr)
        log.error("error: %s" % E)
        sys.exit(1)
