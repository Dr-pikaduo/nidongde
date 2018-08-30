#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse
import base
import load
import search

def _load(args):
    load.load(args.index, args.folder)

def _search(args):
    for a in search.search(args.keyword, args.style):
        print(a)

class IndexParseAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, *args, **kwargs):
        super(IndexParseAction, self).__init__(option_strings, dest, *args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, base.str2index(values))

parser = argparse.ArgumentParser(description='Load Avs')
subparsers = parser.add_subparsers(title='Loading/Searching Command')
parser_l = subparsers.add_parser('load', help='Load avs with indexes')
parser_l.add_argument('-i', dest='index', metavar='INDEX', help='the indexes', action=IndexParseAction)
parser_l.add_argument('-f', dest='folder', action='store', metavar='FOLDER', default=None, help='the folder where the movies are saved')
parser_l.set_defaults(func=_load)

parser_s = subparsers.add_parser('search', help='Search avs with keywords')
parser_s.add_argument('-k', dest='keyword', action='store', metavar='KEYWORD', help='any keyword')
parser_s.add_argument('-s', dest='style', action='store', metavar='STLYE', default=None, help='the style of the movies')
parser_s.set_defaults(func=_search)

args = parser.parse_args()

args.func(args)
