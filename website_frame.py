#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import utils
import website


# Define website: www.417mm.com


class web417(metaclass=website.WebsiteLike):
    """Define methods to operate urls
    
    Variables:
        home {str} -- the home
        styles {dict} -- styles of the movies
        default_style {str}
    """

    # home = 'http://www.417mm.com'

    # styles = {ll:27, rq:28, tp:29, xs:34, jr:54, rh:55, om:56, dm:58}
    # default_style = rq

    # movie_title_rx = re.compile(r'((?P<chapter>\d{1,2})-)?(?P<title>.+)')

    @staticmethod
    def index2url(index):
        """Translate an index to a completed url
        
        Arguments:
            index {int} -- index of the movie
        
        Returns:
            str -- url of the movie
        """


    @staticmethod
    def style2url(style, page=1):
        """Translate style to url
        
        Arguments:
            style {str} -- style of the movie
        
        Keyword Arguments:
            page {number} -- the number of the page (default: {1})
        
        Returns:
            str -- url
        """

    @staticmethod
    def get_page(style):
        """get the number of pages and max index of the movies in certain style
        
        Arguments:
            style {str} -- style of the movie
        
        Returns:
            tuple -- (number of pages, max index)
        """

        #
        # return pages, index

    @staticmethod
    def get_movie(URL, cls=None):
        """find movie in url, url -> movie
        
        Arguments:
            URL {str}
        
        Returns:
            cls
        """
        soup = utils.url2soup(URL)
        #

    @staticmethod
    def search_in_page(keyword, URL, cls=None):
        soup = utils.url2soup(URL)

        #
