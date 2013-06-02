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
from collections import defaultdict

import flask
import pandas as pd

import text_util


app = flask.Flask(__name__)

DATA_FILE = path.join(path.dirname(__file__), '..', 'output',
                      'speeches-plus.csv')


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/test')
def test():
    return flask.render_template('test_index.html')


@app.route('/bubble')
def bubble_speakers():
    d = pd.read_csv(DATA_FILE)
    speakers = sorted(map(int, d.nameid.unique()))
    return flask.render_template('bubble_index.html', speakers=speakers)


@app.route('/bubble/<int:speakerid>')
def bubble_speaker(speakerid):
    return flask.render_template('test_index.html', speakerid=speakerid)


@app.route('/bubble/<int:speakerid>/words.js')
def bubble_speaker_json(speakerid):
    d = pd.read_csv(DATA_FILE)

    speaker_data = d[d.nameid == speakerid]

    # get word frequency for this speaker
    freq = defaultdict(int)
    for text, polarity in zip(speaker_data.speech, speaker_data.polarity):
        for t in text_util.iter_tokens(text):
            freq[t] += 1

    return 'var data = %s;' % json.dumps([
        freq.keys(),
        freq.values()
    ])


@app.route('/wordcloud')
def wordcloud_speakers():
    d = pd.read_csv(DATA_FILE)
    speakers = sorted(map(int, d.nameid.unique()))
    return flask.render_template('wordcloud_index.html', speakers=speakers)


@app.route('/wordcloud/<int:speakerid>')
def wordcloud_speaker(speakerid):
    return 'Word cloud for speaker %d' % speakerid


if __name__ == '__main__':
    app.run(debug=True)
