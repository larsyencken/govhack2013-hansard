# -*- coding: utf-8 -*-
#
#  extend_stopwords.py
#  hansard-data
#

"""
Generate extra stopword data specific to hansard text.
"""

import sys
from collections import Counter
import json


def main(input_file, output_file):
    freq = Counter()
    i = 0
    with open(input_file) as istream:
        for l in istream:
            row = json.loads(l)
            for tok, count in row['tokens'].iteritems():
                freq[tok] += count
            i += 1
            if i % 1000 == 0:
                print i
                sys.stdout.flush()

    with open(output_file, 'w') as ostream:
        for tok, count in freq.most_common(500):
            print >> ostream, tok.encode('utf8'), count


if __name__ == '__main__':
    main(*sys.argv[1:])
