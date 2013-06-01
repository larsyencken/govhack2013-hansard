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
import nltk


WORD_FILE = 'input/AFINN-111.txt'


def main(input_file, output_file):
    scores = _load_features(WORD_FILE)
    d = pd.read_csv(input_file, index_col=None)
    
    # skip any without text
    d = d[~pd.isnull(d.speech)]

    d['polarity'] = d.speech.apply(
        lambda t: get_polarity(t, scores)
    )

    d.to_csv(output_file, index=False)


def get_polarity(text, scores):
    # simple approach: just add up any known word scores
    s = 0.0
    w = 0
    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            s += scores.get(word.lower(), 0)
            w += 1

    return s / w


def _load_features(f):
    scores = {}
    with open(f) as istream:
        for line in istream:
            # The file is tab-delimited. "\t" means "tab character"
            term, score  = line.split("\t")
            # Convert the score to an integer.
            scores[term] = int(score)

    return scores


if __name__ == '__main__':
    main(*sys.argv[1:])
