# -*- coding: utf-8 -*-
#
#  gen_names.py
#  hansard-data
#

"""
Generate a CSV file which maps nameids to names.
"""

import pandas as pd
import csv

d = pd.read_csv('output/speeches-plus.csv')
with open('output/nameids.csv', 'w') as ostream:
    wr = csv.writer(ostream).writerow
    wr(['nameid', 'name'])
    for nameid, g in d.groupby('nameid'):
        name = ' '.join(t.title() for t in g.name.unique()[0].split())
        wr([nameid, name])
