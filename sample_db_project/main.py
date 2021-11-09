from stride_data.db.database import DataLake, DataLakeConfig
import os

#Always important to read authentication passcode and username
#from a non-indexed file

databaseFile = None
try:
    databaseFile = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
 'database_init.txt'), 'r')
except os.error:
    print("File database_init.txt does not exist. Please add it to the file directory containing main.py\n")
    quit()

username, password = None, None
for line in databaseFile:
    try:
        username, password = line.split()
    except:
        print("database_init.txt must contain one line with format 'username password'")
        print(" where 'username' and 'password' are the login credentials for the database")
        quit()
    break #Reading only first line

config = DataLakeConfig(username, password)
db_conn = DataLake()
db_conn.connect(config)

data = db_conn.execute("SELECT CIP2010Code, cip2010Title from cip2010_cip2020 limit 10")

print('CIP_CODE'.ljust(20) +'CIP_TITLE\n')
for info in data:
    cipCode, cipTitle = info
    print(f'{cipCode}'.ljust(20) + f'{cipTitle}\n')

#Always close database after all queries have been done
db_conn.close()

