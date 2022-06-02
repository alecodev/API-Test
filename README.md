# API Test


#### ***Tecnologías***
- Docker (python:3.10.4-alpine3.16)
- Python (requests, urllib3, mysql-connector, dicttoxml, xmltodict)
---


#### ***Plan de trabajo***
- Reconocimiento del problema
- Conocer las entradas y salidas
- Creación de pruebas
- Creación de API
- Validación de pruebas y refactorizar de ser necesario
---


#### ***Deploy***
Configura las credenciales de la base de datos en el archivo `.env`
```.env
DB_HOST=
DB_DATABASE=
DB_USER=
DB_PASS=
DB_PORT=
```

Para ejecutar la API utiliza el siguiente comando, en caso de querer ejecutar las pruebas de los endpoints agrega al final del comando ```-t``` o ```--test```
```bash
docker run --rm --env-file .env -p 5000:5000 -it $(docker build -q .)
```
