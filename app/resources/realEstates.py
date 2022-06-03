import sys
from typing import Any
from db import db
import tests


class endpoint(object):

    db = None

    def do_GET(self, args: tuple = (), params: dict = {}, data: dict | list | None = None, headers: Any = None) -> tuple[list, int]:
        self.db = db()
        _data = []

        # Filtro por estado
        _status = ['pre_venta', 'en_venta', 'vendido']
        if 'status' in params:
            _status = list(filter(lambda x: x in params['status'], _status))

        if len(_status) == 0:
            return [], 200

        _sql = 'WHERE s.name ' + \
            ('= %s' if len(_status) == 1 else (
                'IN (' + ('%s, ' * len(_status)).rstrip(', ') + ')'))
        _data += _status

        # Filtro por año de construcción
        if 'year' in params:
            _year = list(map(lambda x: int(x), filter(
                lambda x: x.isnumeric(), params['year'])))

            if len(_year) == 0:
                return [], 200

            _sql += ' AND p.`year` ' + \
                ('= %s' if len(_year) == 1 else (
                    'IN (' + ('%s, ' * len(_year)).rstrip(', ') + ')'))
            _data += _year

        # Filtro por ciudad
        if 'city' in params:
            _city = list(map(lambda x: str(x), params['city']))

            _sql += ' AND p.city ' + \
                ('= %s' if len(_city) == 1 else (
                    'IN (' + ('%s, ' * len(_city)).rstrip(', ') + ')'))
            _data += _city

        self.db.Execute(
            """
            SELECT p.address, p.city, s.name AS status, p.price, p.description
            FROM property p
            INNER JOIN (
                SELECT property_id, status_id
                FROM (
                    SELECT a.*,
                    @r := CASE
                        WHEN a.property_id = @prevcol THEN @r + 1
                        WHEN (@prevcol := a.property_id) = null THEN null
                        ELSE 1 END AS rn
                    FROM (
                        SELECT id, property_id, status_id
                        FROM status_history
                        ORDER BY property_id, id DESC
                        LIMIT 18446744073709551615
                    ) a,
                    (SELECT @r := 0, @prevcol := null) X
                    ORDER BY a.property_id, a.id DESC
                ) a
                WHERE a.rn=1
            ) sh ON p.id=sh.property_id
            INNER JOIN `status` s ON sh.status_id=s.id
            """
            + _sql,
            data=_data,
            fields=True
        )

        return self.db.results, 200


class test(tests.tests):

    def endpoint(self, url):
        _endpoint = '/' + __file__.split('/')[-1].split('.')[0]

        # Prueba de inmuebles por estado
        self.print_info_test('Obtener inmueble por estado')
        _status = ['pre_venta', 'en_venta', 'vendido']
        for _state in ([''] + _status):
            payload = {}
            if _state != '':
                payload['status'] = _state

            response = self.make_request(
                url + _endpoint,
                'GET',
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                params=payload
            )

            if not response['status']:
                self.print_status_test(response['status'])
                print('\t\t\t💬 '+response['message'])
                sys.exit(1)
            else:
                response['response'].encoding = 'utf-8'
                data = response['response'].json()
                for item in data:
                    if (_state == '' and item['status'] not in _status) or (_state != '' and item['status'] != _state):
                        self.print_status_test(False)
                        print(
                            '\t\t\t💬 La respuesta de los inmuebles tiene un estado no válido: '+item['status'])
                        sys.exit(1)

        self.print_status_test(True)

        # Prueba de inmuebles por año de construcción, Ciudad, Estado
        self.print_info_test(
            'Obtener inmueble por año de construcción, ciudad, estado')
        payload = {
            'year': 2020,
            'city': 'pereira',
            'status': 'vendido'
        }

        response = self.make_request(
            url + _endpoint,
            'GET',
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            params=payload
        )

        if not response['status']:
            self.print_status_test(response['status'])
            print('\t\t\t💬 '+response['message'])
            sys.exit(1)
        else:
            response['response'].encoding = 'utf-8'
            data = response['response'].json()
            if len(data) != 0:
                _columns = ['address', 'city',
                            'status', 'price', 'description']
                for item in data[0]:
                    if item not in _columns:
                        self.print_status_test(False)
                        print(
                            '\t\t\t💬 La respuesta de los inmuebles tiene un campo que no se encuentra parametrizado: '+item)
                        sys.exit(1)
                    else:
                        _columns.remove(item)

                if len(_columns) != 0:
                    self.print_status_test(False)
                    print('\t\t\t💬 La respuesta de los inmuebles no tiene los siguientes campos: %s' % ', '.join(
                        _columns))
                    sys.exit(1)

        self.print_status_test(True)
