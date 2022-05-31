#!/usr/bin/env python3
import os
import sys
import json
import signal
import time
from tests import tests


if __name__ == '__main__':


    # Función para notificar el cierre del proceso
    def def_handler(sig, frame):
        print("\n\n[!] Saliendo...\n")
        sys.exit(1)


    # Ctrl + C
    signal.signal(signal.SIGINT, def_handler)


    # Configuración de variables de entorno
    INTERNAL_HOST = os.environ['APP_INTERNAL_HOST']
    HOST = os.environ['APP_HOST']
    PORT = os.environ['APP_PORT']
    URL = 'http://%s:%s' % (HOST, str(PORT))


    # Validación de sí existen argumentos en la línea de comandos
    if (len(sys.argv) - 1) > 0:
        arguments = sys.argv[1:]
        if '-t' in arguments or '--test' in arguments:
            tests().run(url=URL)
            sys.exit(0)

    # Animación de que la API se encuentra funcionando
    _msg = '[ ] API Running %s on port %s' % (str(HOST), str(PORT))
    sys.stdout.write(_msg)
    sys.stdout.flush()
    sys.stdout.write('\b' * (len(_msg)-2)) # return to start of line, after '['

    i = 0
    while True:
        time.sleep(0.1)

        if i == 0:
            sys.stdout.write('\b/')
        elif i == 1:
            sys.stdout.write('\b-')
        elif i == 2:
            sys.stdout.write('\b\\')
        elif i == 3:
            sys.stdout.write('\b|')
        sys.stdout.flush()

        i += 1
        if i == 4:
            i = 0
