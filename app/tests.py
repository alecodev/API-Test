import os
import sys
import glob
import importlib
from inspect import isfunction
import requests



class tests(object):


    _url = None


    def __init__(self, url):
        self._url = url
        print(
            '-'*40+'\n' \
            + '|'+' '*13+'🤖 Run Tests'+' '*13+'|\n' \
            + '-'*40+'\n'
        )

        endpoints = list(
            map(
                lambda x: x.split('.')[0],
                filter(
                    lambda x: x.endswith('.py') and x!='__init__.py',
                    next(os.walk('./resources'), (None, None, []))[2]
                )
            )
        )
        print('Endpoints detectados: '+str(len(endpoints))+'\n')

        for file in endpoints:
            print('\t[+] ' + file)

            module = importlib.import_module('resources.'+file)
            if not hasattr(module, 'test_endpoint'):
                print('\t\t❌ Error el Endpoint ' + file + ' no tiene pruebas')
                sys.exit(1)
            else:
                module.test_endpoint()

        print('-'*40)
