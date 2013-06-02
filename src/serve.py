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
from collections import Counter, namedtuple

import flask
import pandas as pd

import text_util

Speaker = namedtuple('Speaker', 'nameid name')


app = flask.Flask(__name__)

DATA_FILE = path.join(path.dirname(__file__), '../output/speeches-plus.csv')
NAMES_FILE = path.join(path.dirname(__file__), '../output/nameids.csv')


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/test')
def test():
    return flask.render_template('test_index.html')


@app.route('/bubble')
def bubble_speakers():
    d = pd.read_csv(NAMES_FILE)
    speakers = sorted(Speaker(*s) for s in zip(d.nameid, d.name))
    return flask.render_template('bubble_index.html', speakers=speakers)


@app.route('/bubble/<int:speakerid>')
def bubble_speaker(speakerid):
    d = pd.read_csv(DATA_FILE)
    speaker_data = d[d.nameid == speakerid]
    name = ' '.join(t.title() for t in speaker_data.name.unique()[0].split())
    return flask.render_template('test_index.html', speakerid=speakerid,
                                 name=name)


@app.route('/bubble/<int:speakerid>/words.js')
def bubble_speaker_json(speakerid):
    d = pd.read_csv(DATA_FILE)

    speaker_data = d[d.nameid == speakerid]

    # get word frequency for this speaker
    freq = Counter()
    for text, polarity in zip(speaker_data.speech, speaker_data.polarity):
        for t in text_util.iter_tokens(text):
            freq[t] += 1

    freq = dict(freq.most_common(100))

    return 'var data = %s;' % json.dumps([
        freq.keys(),
        freq.values()
    ])


@app.route('/wordcloud')
def wordcloud_speakers():
    d = pd.read_csv(NAMES_FILE)
    speakers = sorted(Speaker(*s) for s in zip(d.nameid, d.name))
    return flask.render_template('wordcloud_index.html', speakers=speakers)


@app.route('/wordcloud/<int:speakerid>')
def wordcloud_speaker(speakerid):
    return 'Word cloud for speaker %d' % speakerid


if __name__ == '__main__':
    app.run(debug=True)
