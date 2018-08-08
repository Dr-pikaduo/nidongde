#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import argparse

import load

parser = argparse.ArgumentParser(description='Load av')
parser.add_argument('-s', dest='style', action='store', metavar='STLYE', default=None, help='the style of the movies')
parser.add_argument('-i', dest='index', action='store', metavar='INDEX', nargs='+', type=int, help='the indexes')
parser.add_argument('-f', dest='folder', action='store', metavar='FOLDER', default=None, help='the folder where the movies are saved')

args = parser.parse_args()

load.load(args.index, args.folder)