import sys
from typing import Any
import base64
from db import db
import tests


class endpoint(object):

    db = None

    def do_POST(self, args: tuple = (), params: dict = {}, data: dict | list | None = None, headers: Any = None) -> tuple[list, int]:
        if len(args) == 0 or (not args[0].isnumeric()):
            return [], 400

        id_property = int(args[0])

        _authorization = headers.get('Authorization')
        if _authorization is None or (not _authorization.startswith('Basic ')):
            return [], 401

        try:
            _authorization = base64.b64decode(
                (_authorization[6:]).encode('utf-8')).decode('utf-8').split(':')
        except Exception as e:
            return [], 400
        else:
            if len(_authorization) != 2:
                return [], 401

        _user, _pass = _authorization

        self.db = db()

        self.db.Execute("SELECT id FROM auth_user WHERE username = %s AND password = %s AND is_active = %s LIMIT 1", data=[
                        _user, _pass, 1], fields=True)

        if len(self.db.results) == 0:
            return [], 401

        id_user = self.db.results[0]['id']

        self.db.Execute("SELECT id FROM property WHERE id = %s LIMIT 1", data=[
                        id_property], fields=True)

        if len(self.db.results) == 0:
            return [], 403

        id_like = self.db.Execute("INSERT INTO property_likes SET property_id = %s, user_id = %s", data=[
                                  id_property, id_user], fields=False)
        if id_like != None and id_like > 0:
            return [], 200
        else:
            return [], 500


class test(tests.tests):

    def endpoint(self, url):
        _endpoint = '/' + \
            __file__.split('/')[-1].split('.')[0].replace('_', '/%s/') % '3'

        # Prueba de me gusta a un inmueble
        self.print_info_test('Dar me gusta a un inmueble en específico')

        _user = 'test_user'
        _pass = 'testpass123'

        response = self.make_request(
            url + _endpoint,
            'POST',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + base64.b64encode((_user + ':' + _pass).encode('utf-8')).decode('utf-8')
            }
        )

        if not response['status']:
            self.print_status_test(response['status'])
            print('\t\t\t💬 '+response['message'])
            sys.exit(1)
        else:
            self.print_status_test(True)
