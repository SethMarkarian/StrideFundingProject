import sys
from psycopg2 import OperationalError, connect

class DataLakeConfig:
    def __init__(self, user: str, password: str, host: str='139.147.9.145', db: str= 'stride_db') -> None:
        self.host = host
        self.database = db
        self.user = user
        self.password = password


class DataLake:
    def __init__(self) -> None:
        self.__engine = None

    def connect(self, config: DataLakeConfig) -> None:
        try:
            self.__engine = engine = connect(
            host = config.host,
            database = config.database,
            user = config.user,
            password = config.password,
            port = 5432)
        except OperationalError as err:
            raise self.__print_psycopg2_exception(err)
    

    def close(self):
        if not self.__engine is None:
            self.__engine.close()

    def execute(self, queryFormat, queryData= None):
        if self.__engine is None:
            raise "Database has not been connected"
        elif not queryFormat.lower().startswith("select"):
            raise "Non-SELECT queries are not supported"
        
        cur = self.__engine.cursor()
        try:
            if queryData is None:
                cur.execute(queryFormat)
            else:
                cur.execute(queryFormat, queryData)
        except Exception as err:
            cur.close()
            self.__engine.rollback()
            raise self.__print_psycopg2_exception(err)
        
        data = cur.fetchall()
        self.__engine.commit()
        cur.close()
        return data
    
    def __print_psycopg2_exception(err):
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()

        # get the line number when exception occured
        line_num = traceback.tb_lineno

        # print the connect() error
        print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
        print ("psycopg2 traceback:", traceback, "-- type:", err_type)

        # psycopg2 extensions.Diagnostics object attribute
        print ("\nextensions.Diagnostics:", err.diag)

        # print the pgcode and pgerror exceptions
        print ("pgerror:", err.pgerror)
        print ("pgcode:", err.pgcode, "\n")
