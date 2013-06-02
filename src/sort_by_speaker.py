# -*- coding: utf-8 -*-
#
#  sort_by_speaker.py
#  hansard-data
#

import os
import sys
import json
import shutil


def main(input_file, output_dir):
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    os.mkdir(output_dir)

    dests = {}
    with open(input_file) as istream:
        for l in istream:
            row = json.loads(l)
            nameid = row['nameid']
            if nameid not in dests:
                dests[nameid] = open(output_dir + '/%s.json' % nameid, 'w')

            print >> dests[nameid], json.dumps(row)

    for v in dests.itervalues():
        v.close()


if __name__ == '__main__':
    main(*sys.argv[1:])
