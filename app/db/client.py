from typing import Optional

import pyodbc

from app.core.config import Settings

config = Settings()


class DatabaseClient:
    connection: Optional[pyodbc.Connection] = None

    def __init__(self):
        self.connection = pyodbc.connect('DRIVER=' + config.AZURE_DATABASE_DRIVER + ';SERVER=' + config.AZURE_DATABASE_URL + ';DATABASE=' + config.AZURE_DATABASE_NAME + ';UID=' + config.AZURE_DATABASE_USER + ';PWD=' + config.AZURE_DATABASE_PASSWORD)

    def get_conn(self) -> pyodbc.Cursor:
        try:
            if self.connection is None:
                self.connection = pyodbc.connect('DRIVER=' + config.AZURE_DATABASE_DRIVER + ';SERVER=' + config.AZURE_DATABASE_URL + ';DATABASE=' + config.AZURE_DATABASE_NAME + ';UID=' + config.AZURE_DATABASE_USER + ';PWD=' + config.AZURE_DATABASE_PASSWORD)

            cursor = self.connection.cursor()
            return cursor
        except Exception as e:
            print(e)
            print('Cannot connect to SQL server')
            self.close_connection()

    def commit(self) -> None:
        try:
            self.connection.commit()
        except Exception as e:
            print(e)
            print('Cannot commit changes to SQL server')
            self.close_connection()

    def close_connection(self) -> None:
        try:
            self.connection.close()
        except Exception as e:
            print(e)
            print('Cannot close connection to SQL server')


database_client = DatabaseClient()
