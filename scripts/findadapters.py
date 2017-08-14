#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import sys
import argparse
import re


def parseargs(args):
    parser = argparse.ArgumentParser('findadapters')
    parser.add_argument('filename', metavar='PATH')
    return parser.parse_args(args)


def parse_lines(filename):
    all_lines = []
    with open(filename, 'r') as f:
         for line in f.readlines():
            all_lines.append(line.strip())
    return all_lines


def match_atgc_lines(lines):
    for i in range(0, len(lines)):
        if re.match(r'[ATGC]+$', lines[i].strip()):
            yield i


def matching_pair(i, lines):
    for j in range(i-1, i-5, -1):
        candidate = lines[j]
        if len(candidate) > 0:
            if re.match(r'[ATGC]+$', candidate):
                return None
            else:
                return {'line': i, 'adapter': lines[i], 'barcode': candidate}


def find_easy_pairs(lines):
    for i in match_atgc_lines(lines):
        # walk back lines until you find a non-blank line, if it is also a matching line
        pair = matching_pair(i, lines)
        if pair is not None:
            yield pair


def illumina(filename):
    all_lines = parse_lines(filename)
    print('LINE,KIT NAME OR BARCODE,ADAPTER')
    for pair in find_easy_pairs(all_lines):
        print('%d,%s,%s' % (pair['line'], pair['barcode'], pair['adapter']))

    
def main(args):
    opts = parseargs(args)
    illumina(opts.filename)


if __name__ == '__main__':
    main(sys.argv[1:])

