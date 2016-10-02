#!/usr/bin/python3
import sys, os
import glob
import fileinput

import transwarp.parser
import transwarp.template

def main(args=None):
    if len(sys.argv) != 2:
        print("usage: transwarp <tpl-file>")
        print("Available template files:")
        for name in sorted(transwarp.template.find_available()):
            print("  %s" % name)
        return 0

    try:
        template_file = sys.argv[1]
        template_data = open(template_file).read()

        # find all stf input files
        files = glob.glob("data/*.stf")

        # fileinput.input() makes all files appear as one long list of lines
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

if __name__ == "__main__":
    sys.exit(main())
