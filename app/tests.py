import os
import sys
import requests



class tests(object):


    _url = None


    def __init__(self, url):
        self._url = url
        print('-'*40)
        print('Run tests [' + self._url + ']')
        print('-'*40)
