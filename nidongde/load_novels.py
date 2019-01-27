#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import re
import pickle
import pathlib

import website
import base, utils


defaultWebsite = website.web_novel

defaultANFolder = pathlib.Path('ANs')

class Novel(base.LoadItem):
    """docstring for Novel"""
    website = defaultWebsite
    folder = defaultANFolder

    def __str__(self):
        return '{0.title} (0.chapter)\n{0.body}'.fromat(self)

    @classmethod
    def fromURL(cls, URL):
        """find novel in url, url -> novel
        
        Arguments:
            URL {str}
        
        Returns:
            Novel
        """

        return cls.website.get_novel(URL, cls)

    def save(self, folder=None, filename=None):
        if folder is None:
            folder = self.folder
        if not folder.exists():
            folder.mkdir(parents=True)
        if filename is None:
            filename = 'Novel%d.txt' % self.index
        path = folder / filename
        body = self.body
        path.write_text(body, encoding='utf-8')


Novel.load(index=32291)
