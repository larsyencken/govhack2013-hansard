# -*- coding: utf-8 -*-
#
#  gen_polarity.py
#  govhack
#

"""
Add polarity to each speech item.
"""

import sys

import pandas as pd
import csv
import nltk


WORD_FILE = 'input/AFINN-111.txt'
FIELDS = ['name', 'party', 'electorate', 'speech', 'time', 'polarity']


def main(input_file, output_file):
    scores = _load_features(WORD_FILE)

    i = 0
    with open(input_file) as istream:
        with open(output_file, 'w') as ostream:
            wr = csv.DictWriter(ostream, FIELDS).writerow
            wr(dict(zip(FIELDS, FIELDS)))
            for r in csv.DictReader(istream):
                # ignore empty speech
                if not r['speech'].strip():
                    continue

                r['polarity'] = get_polarity(r['speech'], scores)
                wr(r)
                i += 1

                if i % 1000 == 0:
                    print i
                    sys.stdout.flush()


def get_polarity(text, scores):
    # simple approach: just add up any known word scores
    s = 0.0
    w = 0
    text = text.replace('\u2014', ' - ')
    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            s += scores.get(word.lower(), 0)
            w += 1

    return s / w


def _load_features(f):
    d = pd.read_csv(f, sep='\t')
    scores = dict(zip(d.word, d.polarity))
    return scores


if __name__ == '__main__':
    main(*sys.argv[1:])
