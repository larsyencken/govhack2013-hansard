# -*- coding: utf-8 -*-
#
#  extend_stopwords.py
#  hansard-data
#

"""
Generate extra stopword data specific to hansard text.
"""

import sys
from collections import defaultdict
import csv

import text_util


def main(input_file, output_file):
    freq = defaultdict(int)
    i = 0
    for row in csv.DictReader(open(input_file)):
        for text in row['speech']:
            for tok in text_util.iter_tokens(text):
                freq[tok] += 1
        i += 1
        if i % 200 == 0:
            print i
            sys.stdout.flush()

    with open(output_file, 'w') as ostream:
        for tok, count in freq.most_common(100):
            print >> ostream, tok


if __name__ == '__main__':
    main(*sys.argv[1:])
