# Must have this installed in psql
# 'CREATE EXTENSION fuzzystrmatch;'

from socket import socket
import pandas as pd
import sys
from psql.main import getPSQLOutput

def runQueryOnJob(job_name, metaphone_index):
    SOCdf = getPSQLOutput('SELECT SOC2018CodeTitle, SOC2018Code FROM cip2020_soc2018 where metaphone(SOC2018CodeTitle,' + str(metaphone_index) + ') = metaphone(' + "'" + job_name + "'" + ', ' + str(metaphone_index) + ')')
    SOCdf = SOCdf[['soc2018codetitle', 'soc2018code']].copy()
    return SOCdf

def main():
    jobTitle = input("Enter Job Title: ")
    if jobTitle == '':
        sys.exit()
    index = 10
    df = pd.DataFrame()
    while df.empty:
        index = index - 1
        df = runQueryOnJob(jobTitle, index)
    df = df.drop_duplicates()
    print(df.to_string(index = False) + '\n')
    main()

if __name__ == '__main__':
    main()