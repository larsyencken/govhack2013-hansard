#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bubble.py
#  hansard-data
#

"""
Run a bubble chart visualisation.
"""

import json
from os import path
from collections import Counter, namedtuple, defaultdict

import flask
import pandas as pd
import numpy as np

Speaker = namedtuple('Speaker', 'nameid name')


app = flask.Flask(__name__)

SPEAKER_DIR = path.join(path.dirname(__file__), '../output/speakers')
NAMES_FILE = path.join(path.dirname(__file__), '../output/nameids.csv')
STOP_FILE = path.join(path.dirname(__file__),
                      '../input/stopwords-extra-manual.txt')


@app.route('/')
def index():
    return flask.redirect('/bubble/')
    #return flask.render_template('index.html')


@app.route('/bubble/')
def bubble_speakers():
    d = pd.read_csv(NAMES_FILE)
    speakers = sorted(Speaker(*s) for s in zip(d.nameid, d.name))
    return flask.render_template('bubble_index.html', speakers=speakers)


@app.route('/bubble/<int:speakerid>')
def bubble_speaker(speakerid):
    d = pd.read_csv(NAMES_FILE)
    speaker_data = d[d.nameid == speakerid]
    speaker, = [Speaker(*s) for s in zip(speaker_data.nameid,
                                         speaker_data.name)]
    return flask.render_template('bubble.html', speaker=speaker)


@app.route('/bubble/<int:speakerid>/words.js')
def bubble_speaker_json(speakerid):
    stopwords = set(l.strip() for l in open(STOP_FILE))

    freq = Counter()
    word_pol = defaultdict(list)
    for row in speaker_data(speakerid):
        polarity = float(row['polarity'])
        for tok, count in row['tokens'].iteritems():
            if tok not in stopwords:
                freq[tok] += 1
                word_pol[tok].append(polarity)

    freq = dict(freq.most_common(100))

    pol = {w: np.mean(p) for (w, p) in word_pol.iteritems()}

    return 'var data = %s;' % json.dumps([
        freq.keys(),
        freq.values(),
        pol.keys(),
        pol.values(),
    ])


@app.route('/wordcloud')
def wordcloud_speakers():
    d = pd.read_csv(NAMES_FILE)
    speakers = sorted(Speaker(*s) for s in zip(d.nameid, d.name))
    return flask.render_template('wordcloud_index.html', speakers=speakers)


@app.route('/wordcloud/<int:speakerid>')
def wordcloud_speaker(speakerid):
    return 'Word cloud for speaker %d' % speakerid


def speaker_data(nameid):
    f = path.join(SPEAKER_DIR, '%s.json' % nameid)
    with open(f) as istream:
        for l in istream:
            yield json.loads(l)


if __name__ == '__main__':
    #app.run('0.0.0.0', debug=True)
    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('', 3002), app)
    http_server.serve_forever()
