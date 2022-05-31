import os
import sys
import importlib
import requests
from requests.exceptions import HTTPError


class tests(object):


    def run(self, url):
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
            if (not hasattr(module, 'test')) or (not hasattr(module.test, 'endpoint')):
                print('\t\t❌ Error el Endpoint ' + file + ' no tiene pruebas')
                sys.exit(1)
            else:
                module.test().endpoint(url)

        print('-'*40)


    def print_info_test(self, _msg):
        sys.stdout.write('\t\t👉 '+_msg+' 🧪')
        sys.stdout.flush()
        sys.stdout.write('\b')


    def print_status_test(self, _status):
        if _status:
            sys.stdout.write('\b✅')
        else:
            sys.stdout.write('\b❌')
        sys.stdout.flush()
        sys.stdout.write('\b\n')


    def make_request(self, _url, _method='GET', **kwargs):
        try:
            response = requests.request(_method, _url, **kwargs)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            return {'status': False, 'response': response, 'message': f'HTTP error occurred: {http_err}'}
        except Exception as err:
            return {'status': False, 'response': response, 'message': f'Other error occurred: {err}'}
        else:
            return {'status': True, 'response': response}
