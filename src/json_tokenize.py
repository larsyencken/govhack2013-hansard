#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tokenize.py
#  hansard-data
#

"""
Tokenize the CSV input text, outputting as JSON.
"""

import sys
from collections import Counter
import json
import csv

import text_util


def main(input_file, output_file):
    with open(input_file) as istream:
        with open(output_file, 'w') as ostream:
            for row in csv.DictReader(istream):
                toks = Counter()
                for t in text_util.iter_tokens(row['speech']):
                    toks[t] += 1

                del row['speech']
                row['tokens'] = toks
                print >> ostream, json.dumps(row)


if __name__ == '__main__':
    main(*sys.argv[1:])
