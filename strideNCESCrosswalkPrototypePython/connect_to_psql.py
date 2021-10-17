#pip install psycopg2

import psycopg2
from config import config
from configparser import ConfigParser

def config(filename = 'database.ini', section = 'postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

# Connects to the PostgreSQL database
def connect():
    conn = None

    try:
        param = config()

        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        print("PostgreSQL database version: ")
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    connect()