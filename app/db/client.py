import pyodbc

from app.core.config import Settings

config = Settings()


def get_conn():
    try:
        connection = pyodbc.connect('DRIVER=' + config.AZURE_DATABASE_DRIVER + ';SERVER=' + config.AZURE_DATABASE_URL + ';DATABASE=' + config.AZURE_DATABASE_NAME + ';UID=' + config.AZURE_DATABASE_USER + ';PWD=' + config.AZURE_DATABASE_PASSWORD)
        return connection
    except Exception as e:
        print(e)
        print('Cannot connect to SQL server')


def execute_query(query):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def fetch_query(query):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def fetch_query_with_params(query, params):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result


def execute_query_with_params(query, params):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_query_with_params_dict(query, params):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result


def execute_query_with_params_dict(query, params):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
