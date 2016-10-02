import sys
import glob
import fileinput
import logging as log

import transwarp.parser
import transwarp.template
import transwarp.util.logformat
import transwarp.cmdline.arguments

def main(args=None):
    argparser = transwarp.cmdline.arguments.parser
    args = argparser.parse_args()
    transwarp.util.logformat.initialize(sum(args.verbosity) + 20)

    if len(sys.argv) == 1:
        argparser.print_help()
        return 0
    try:
        template_file = sys.argv[1]
        template_data = open(template_file).read()

        # find all stf input files
        files = glob.glob("data/*.stf")
        all_lines = fileinput.input(files)

        # parse all sections into a unified data structure, that the
        # templates can inspect
        sections = transwarp.parser.parse(all_lines)

        print("Compiling [%s]" % template_file, file=sys.stderr)
        # generate the template, and print it
        print(transwarp.template.generate(template_data, sections))
    except:
        transwarp.template.present_template_error()
        return 10
