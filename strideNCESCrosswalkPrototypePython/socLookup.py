import pandas as pd
import sys

def SOCLookup(title, df):
    pd.set_option('display.max_rows', None)
    print(df[df['SOC2018Title'].str.contains(title, case = False)])
    main()


def importingAndSetup():
    CIP2020ToSOCPath = 'CIP2020_SOC2018_Crosswalk.xlsx'
    CIP2020ToSOCDf = pd.read_excel(CIP2020ToSOCPath, sheet_name=1)  
    SOCdf = CIP2020ToSOCDf[['SOC2018Title', 'SOC2018Code']].copy()
    return SOCdf

def main():
    jobTitle = input("Enter Job Title: ")
    if jobTitle == '':
        sys.exit()
    df = importingAndSetup()
    SOCLookup(jobTitle, df)

if __name__ == '__main__':
    main()
    