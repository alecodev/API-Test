# API Test


#### ***Tecnologías***
- Docker (python:3.10.4-alpine3.16)
- Python 3.10.4 (requests, response, os, mysql.connector)
---


#### ***Plan de trabajo***
- Reconocimiento del problema
- Conocer las entradas y salidas
- Creación de pruebas
- Creación de API
- Validación de pruebas y refactorizar de ser necesario
---


#### ***Deploy***
Para ejecutar la API utiliza el siguiente comando, en caso de querer ejecutar las pruebas de los endpoint agrega al final del comando ```-t``` o ```--test```
```bash
docker run --rm --env-file .env -p 5000:5000 -it $(docker build -q .)
```
