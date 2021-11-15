# Must have this installed in psql
# 'CREATE EXTENSION fuzzystrmatch;'

from socket import socket
import pandas as pd
import sys
from psql.main import getPSQLOutput

def importingAndSetup(job_name):
    SOCdf = getPSQLOutput('SELECT SOC2018CodeTitle, SOC2018Code FROM cip2020_soc2018 where soundex(SOC2018CodeTitle) = soundex(' + "'" + job_name + "'" + ')')
    SOCdf = SOCdf[['soc2018codetitle', 'soc2018code']].copy()
    return SOCdf

def main():
    jobTitle = input("Enter Job Title: ")
    if jobTitle == '':
        sys.exit()
    df = importingAndSetup(jobTitle)
    df = df.drop_duplicates()
    print(df.to_string(index = False))
    main()
s
if __name__ == '__main__':
    main()