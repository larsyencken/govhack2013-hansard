# -*- coding: utf-8 -*-
#
#  bubble.py
#  hansard-data
#

"""
Run a bubble chart visualisation.
"""

import flask
import pandas as pd
from os import path

app = flask.Flask(__name__)

DATA_FILE = path.join(path.dirname(__file__), '..', 'output',
                      'speeches-plus.csv')


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/bubble')
def bubble_speakers():
    d = pd.read_csv(DATA_FILE)
    speakers = sorted(map(int, d.session_talker_id.unique()))
    return flask.render_template('bubble_index.html', speakers=speakers)


@app.route('/bubble/<int:speakerid>')
def bubble_speaker(speakerid):
    return flask.render_template('bubble.html')


@app.route('/wordcloud')
def wordcloud_speakers():
    d = pd.read_csv(DATA_FILE)
    speakers = sorted(map(int, d.session_talker_id.unique()))
    return flask.render_template('wordcloud_index.html', speakers=speakers)


@app.route('/wordcloud/<int:speakerid>')
def wordcloud_speaker(speakerid):
    return 'Word cloud for speaker %d' % speakerid


if __name__ == '__main__':
    app.run(debug=True)
