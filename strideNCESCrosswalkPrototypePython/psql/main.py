from psql.config.config import get_project_root
from psql.src.data.db_conn import load_db_table

def getPSQLOutput(query):
    # Project root
    PROJECT_ROOT = get_project_root()
    # Read database - PostgreSQL
    df = load_db_table(config_db = 'database.ini', query = query)
    return df