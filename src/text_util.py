# -*- coding: utf-8 -*-
#
#  text_util.py
#  hansard-data
#

"""
Tokenising tools.
"""

import re

import nltk
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))


def iter_tokens(text):
    for s in nltk.sent_tokenize(text):
        for w in nltk.word_tokenize(s):
            w = norm_word(w)
            if valid_word(w):
                yield w


def norm_word(w):
    w = w.lower()
    return w


def valid_word(w):
    if len(w) <= 3:
        return False

    if w in STOPWORDS:
        return False

    if re.match('^[0-9]+$', w):
        return False

    return True
