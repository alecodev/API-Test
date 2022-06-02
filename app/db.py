import sys
import os
import mysql.connector


class db(object):

    # Instancia de la conexión
    _conn = None
    # Cursor de la conexión con la base de datos
    _stmt = None
    # Atributo con los datos obtenidos de la consulta
    results = []

    # Método para crear conexión
    def __init__(self):
        try:
            self._conn = mysql.connector.connect(
                host=str(os.environ['DB_HOST']),
                database=str(os.environ['DB_DATABASE']),
                user=str(os.environ['DB_USER']),
                password=str(os.environ['DB_PASS']),
                port=int(os.environ['DB_PORT']),
                use_unicode=True,
                charset='utf8'
            )
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.ER_ACCESS_DENIED_ERROR:
                print('🔥 Error en usuario o contraseña de base de datos')
            elif err.errno == mysql.connector.ER_BAD_DB_ERROR:
                print('🔥 Error la base de datos "%s" no existe' %
                      str(os.environ['DB_DATABASE']))
            else:
                print(f'🔥 Error en la conexión a la base de datos: {err}')
            sys.exit(1)
        else:
            self._stmt = self._conn.cursor(buffered=True)

    # Método para almacenar los datos obtenidos de la consulta
    def GetData(self):
        self.results = []
        for row in self._stmt.fetchall():
            dat = {}
            for i, column in enumerate(self._stmt.column_names):
                dat[column] = row[i]
            self.results.append(dat)

    # Método para ejecutar sentencias preparadas
    def Execute(self, sql='', data=None, fields=False):
        try:
            self._stmt.execute(sql, params=data, multi=False)
        except mysql.connector.Error as err:
            print(f'🔥 Error al ejecutar la consulta:\n{err}\n{sql}')
            sys.exit(1)
        else:
            # COMMIT SQL
            self._conn.commit()
            # Obtener los datos de la consulta
            if fields:
                self.GetData()
            elif 'INSERT' in sql.upper():
                return self._stmt.lastrowid

    # Método para cerrar conexiones con la base de datos
    def Close(self):
        if self._stmt is not None:
            self._stmt.close()
            self._stmt = None

        if self._conn is not None:
            self._conn.commit()
            self._conn.close()
            self._conn = None

    def __del__(self):
        self.Close()
