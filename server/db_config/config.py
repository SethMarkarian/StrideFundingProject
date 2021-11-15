import os
from psycopg2 import connect
from configparser import ConfigParser

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def get_db_conn():
    config = ConfigParser()
    config.read(os.path.join(CURRENT_DIRECTORY, 'database.ini'))
    if 'postgresql' not in config:
        raise("database.ini file is not found in server/db_config subdirectory")
    psqlData = config['postgresql']
    return connect(
        host=psqlData['host'],
        database=psqlData['database'],
        user=psqlData['user'],
        password=psqlData['password'],
        port=psqlData['port'])
