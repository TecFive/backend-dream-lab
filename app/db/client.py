from typing import Optional

import pyodbc

from app.core.config import Settings

config = Settings()


class DatabaseClient:
    connection: Optional[pyodbc.Connection] = None

    def __init__(self):
        self.connection = pyodbc.connect(f"Driver={config.AZURE_DATABASE_DRIVER};Server=tcp:{config.AZURE_DATABASE_URL},1433;Database={config.AZURE_DATABASE_NAME};Uid={config.AZURE_DATABASE_USER};Pwd={config.AZURE_DATABASE_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;")

    def get_conn(self) -> pyodbc.Cursor:
        try:
            self.connection = pyodbc.connect(f"Driver={config.AZURE_DATABASE_DRIVER};Server=tcp:{config.AZURE_DATABASE_URL},1433;Database={config.AZURE_DATABASE_NAME};Uid={config.AZURE_DATABASE_USER};Pwd={config.AZURE_DATABASE_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;")

            cursor = self.connection.cursor()
            return cursor
        except Exception as e:
            if e.__class__ == pyodbc.ProgrammingError:
                return self.get_conn()

    def commit(self) -> None:
        try:
            self.connection.commit()
        except Exception as e:
            print(e)
            print('Cannot commit changes to SQL server')

    def close(self) -> None:
        try:
            self.connection.close()
        except Exception as e:
            print(e)
            print('Cannot close connection to SQL server')
