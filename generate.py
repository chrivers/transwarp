#!/usr/bin/python3
import sys, os
import glob
import fileinput

import cortex
import template

if len(sys.argv) != 2:
    print("usage: %s <stf-file>" % sys.argv[0])
    sys.exit(1)

try:
    template_file = sys.argv[1]
    template_data = open(template_file).read()

    # find the base dir for the template
    # example: "rust/templates/client.rs" -> "rust"
    base_dir = template_file.split(os.path.sep)[0]

    # try to load language utils from the base dir
    try:
        lang_mod = __import__(base_dir)
    except ImportError:
        lang_mode = {}

    # find all stf input files
    files = glob.glob("data/*.stf")

    # fileinput.input() makes all files appear as one long list of lines
    all_lines = fileinput.input(files)

    # parse all sections into a unified data structure, that the
    # templates can inspect
    sections = cortex.parse(all_lines)

    # generate the template, and print it
    print(template.generate(template_data, sections, lang_utils=lang_mod))
except:
    template.present_template_error()
