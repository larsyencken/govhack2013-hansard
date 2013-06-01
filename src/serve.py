# -*- coding: utf-8 -*-
#
#  bubble.py
#  hansard-data
#

"""
Run a bubble chart visualisation.
"""

import flask

app = flask.Flask(__name__)


@app.route('/bubble')
def bubble():
    return flask.render_template('bubble.html')


if __name__ == '__main__':
    app.run(debug=True)
