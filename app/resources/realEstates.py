import sys
import tests


class test(tests.tests):


    def endpoint(self, url):
        _endpoint = '/' + __file__.split('/')[-1].split('.')[0]

        # Prueba de inmuebles por estado
        self.print_info_test('Obtener inmueble por estado')
        _status = ['pre_venta', 'en_venta', 'vendido']
        for _state in ([''] + _status):
            payload = {}
            if _state!='':
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
                    if (_state=='' and item['status'] not in _status) or (_state!='' and item['status']!=_state):
                        self.print_status_test(False)
                        print('\t\t\t💬 La respuesta de los inmuebles tiene un estado no válido: '+item['status'])
                        sys.exit(1)

        self.print_status_test(True)

        # Prueba de inmuebles por año de construcción, Ciudad, Estado
        self.print_info_test('Obtener inmueble por año de construcción, ciudad, estado')
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
            if len(data)!=0:
                _columns = ['address', 'city', 'status', 'price', 'description']
                for item in data[0]:
                    if item not in _columns:
                        self.print_status_test(False)
                        print('\t\t\t💬 La respuesta de los inmuebles tiene un campo que no se encuentra parametrizado: '+item)
                        sys.exit(1)
                    else:
                        _columns.remove(item)

                if len(_columns)!=0:
                    self.print_status_test(False)
                    print('\t\t\t💬 La respuesta de los inmuebles no tiene los siguientes campos: %s' % ', '.join(_columns))
                    sys.exit(1)

        self.print_status_test(True)
