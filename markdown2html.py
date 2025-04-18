#!/usr/bin/python3
""" converts markdown to html """

import os
import sys

#checks for 2 arguments
if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    sys.exit(1)

# variable for the args
input_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.isfile(input_file):
    sys.stderr.write(f"Missing {input_file}\n")
    sys.exit(1)

sys.exit(0)
