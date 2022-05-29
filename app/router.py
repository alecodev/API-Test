#!/usr/bin/env python3
import os
import sys
import json
import signal
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
            tests(url=URL)
