#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import utils
import load_movies

def _load(args):
    print('Start to Load adult movie %s' % utils.index2str(args.index))
    load_movies.Movie.load(args.index, args.folder, args.verbose)

def _search(args):
    print('Start to search with keyword %s' % args.keyword)
    for m in load_movies.Movie.search(args.keyword, args.style):
        if args.mask:
            f = "Find {0:%s}" % args.mask
            print(f.format(m))
        else:
            print(m)

class IndexParseAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, *args, **kwargs):
        super(IndexParseAction, self).__init__(option_strings, dest, *args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, utils.str2index(values))

parser = argparse.ArgumentParser(description='Load Avs')
parser.add_argument('-a', dest='agent', metavar='USER_AGENT', help='a fake agent')
subparsers = parser.add_subparsers(title='Loading/Searching Command')
parser_l = subparsers.add_parser('load', help='Load avs with indexes')
parser_l.add_argument('-i', dest='index', metavar='INDEX', help='the indexes', action=IndexParseAction)
parser_l.add_argument('-f', dest='folder', action='store', metavar='FOLDER', default=None, help='the folder where the movies are saved')
parser_l.add_argument('-v', dest='verbose', action='store_true', default=False, help='print the info of the loading movie')
parser_l.set_defaults(func=_load)

parser_s = subparsers.add_parser('search', help='Search avs with keywords')
parser_s.add_argument('-k', dest='keyword', action='store', metavar='KEYWORD', help='any keyword')
parser_s.add_argument('-s', dest='style', action='store', metavar='STLYE', default=None, help='the style of the movies')
parser_s.add_argument('-m', dest='mask', action='store', default='', metavar='MASK', help='mask sensitive words, mask|random|caesar')
parser_s.set_defaults(func=_search)

args = parser.parse_args()

args.func(args)
