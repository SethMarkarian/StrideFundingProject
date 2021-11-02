from socket import socket
import pandas as pd
import sys
from psql.main import getPSQLOutput

def SOCLookup(title, df):
    pd.set_option('display.max_rows', None)
    newdf = df[df['soc2018codetitle'].str.contains(title, case = False)]
    newdf = newdf.drop_duplicates()
    print(newdf.to_string(index = False))
    main()

def importingAndSetup():
    SOCdf = getPSQLOutput('SELECT SOC2018CodeTitle, SOC2018Code FROM cip2020_soc2018')
    SOCdf = SOCdf[['soc2018codetitle', 'soc2018code']].copy()
    return SOCdf

def main():
    jobTitle = input("Enter Job Title: ")
    if jobTitle == '':
        sys.exit()
    df = importingAndSetup()
    SOCLookup(jobTitle, df)

if __name__ == '__main__':
    main()
    