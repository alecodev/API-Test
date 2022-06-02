import sys
import db
import tests


class endpoint(object):

    def do_POST(self, args=(), params={}, data=None):
        pass


class test(tests.tests):

    token = 'fd5dad2a0b92454f7490059ae9fd77d7c2cfaf074fad6a622b4eff048afa482d'

    def endpoint(self, url):
        _endpoint = '/' + \
            __file__.split('/')[-1].split('.')[0].replace('_', '/%s/') % '3'

        # Prueba de me gusta a un inmueble
        self.print_info_test('Dar me gusta a un inmueble en específico')

        response = self.make_request(
            url + _endpoint,
            'POST',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.token
            }
        )

        if not response['status']:
            self.print_status_test(response['status'])
            print('\t\t\t💬 '+response['message'])
            sys.exit(1)
        else:
            self.print_status_test(True)
