# Import libraries
import pandas as pd
import psycopg2
from psql.config.config import config

# Take in a PostgreSQL table and outputs a pandas dataframe
def load_db_table(config_db, query):
    engine = psycopg2.connect(
        host = "139.147.9.145",
        database = "stride_db",
        user = "public_reader",
        password = "oogleBoss.23",
        port = 5432)
    data = pd.read_sql(query, con = engine)
    return data