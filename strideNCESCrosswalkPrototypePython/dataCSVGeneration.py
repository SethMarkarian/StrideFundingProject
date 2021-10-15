"""
How to setup environment:
    1. Make sure Python 3.x is installed: https://www.python.org/downloads/
    2. Make sure pip is installed for your Python version:  https://pip.pypa.io/en/stable/installation/
    3. Run `python3 pip install pandas` if pandas library is not installed
    4. Ensure that the libary crosswalk is in the same directory as this script

    All files generated in this script are stored in the database folder
"""
import pandas as pd
import math
from crosswalk import cleanCIPCode, convertNumericalCIPCodetoString

CIP2010toCIP2020Path = 'crosswalk.csv'
CIP2020ToSOCPath = 'CIP2020_SOC2018_Crosswalk.xlsx'
SOCDataPath = 'national_M2020_dl.xlsx'


CIP2010toCIP2020Df = pd.read_csv(CIP2010toCIP2020Path)
CIP2010toCIP2020Df.columns = [column.replace(" ", "_")
                               for column in CIP2010toCIP2020Df.columns]
CIP2010toCIP2020Df['Original_code'] = CIP2010toCIP2020Df['Original_code'].apply(lambda x: cleanCIPCode(x) if cleanCIPCode(x) != 'nan' else '')
CIP2010toCIP2020Df['Current_code'] = CIP2010toCIP2020Df['Current_code'].apply(lambda x: cleanCIPCode(x) if cleanCIPCode(x) != 'nan' else '')

CIP2020ToSOCDf = pd.read_excel(CIP2020ToSOCPath, sheet_name=1)

UnmatchedCIP2020Df = pd.read_excel(CIP2020ToSOCPath, sheet_name=6)
pd.concat([CIP2020ToSOCDf, UnmatchedCIP2020Df])

UnmatchedSOC2018Df = pd.read_excel(CIP2020ToSOCPath, sheet_name=7)
pd.concat([CIP2020ToSOCDf, UnmatchedCIP2020Df])

CIP2020ToSOCDf['CIP2020Code'] = CIP2020ToSOCDf['CIP2020Code'].apply(convertNumericalCIPCodetoString)
CIP2020ToSOCDf['CIP2020CodeMain'] = CIP2020ToSOCDf['CIP2020Code'].apply(lambda x : str(x)[:2])
CIP2020ToSOCDf['CIP2020CodeSubMain'] = CIP2020ToSOCDf['CIP2020Code'].apply(lambda x : str(x)[:5])

SOCDataDf = pd.read_excel(SOCDataPath, sheet_name=0)
# Pandas does not have any null value for int64 types
# HEnce 0 is used to fill empty values since it is an unexpected value for these columns
SOCDataDf['TOT_EMP'] = SOCDataDf['TOT_EMP'].fillna(0).astype(int)
SOCDataDf['A_MEAN'] = SOCDataDf['A_MEAN'].fillna(0).astype(int)
SOCDataDf['A_PCT10'] = SOCDataDf['A_PCT10'].fillna(0).astype(int)
SOCDataDf['A_PCT25'] = SOCDataDf['A_PCT25'].fillna(0).astype(int)
SOCDataDf['A_MEDIAN'] = SOCDataDf['A_MEDIAN'].fillna(0).astype(int)
SOCDataDf['A_PCT75'] = SOCDataDf['A_PCT75'].fillna(0).astype(int)
SOCDataDf['A_PCT90'] = SOCDataDf['A_PCT90'].fillna(0).astype(int)


SOCDataColumnMeaningDf = pd.read_excel(SOCDataPath, sheet_name=1, header=None, names=['Field', 'FieldDescription','NotImportant']) #NotImportant is a series of periods
SOCDataColumnMeaningDf.pop('NotImportant')
SOCDataColumnMeaningDf['Field'] = SOCDataColumnMeaningDf['Field'].apply(lambda x : str(x).upper())
SOCDataColumnMeaningDf.drop(range(10), inplace=True)
SOCDataColumnMeaningDf.drop(range(41, 47), inplace=True)


CIP2010toCIP2020Df.to_csv("CIP2010_CIP2020DBFormatted.csv", index=False)
CIP2020ToSOCDf.to_csv('CIP2020_SOC2018DBFormatted.csv', index=False)
SOCDataDf.to_csv("BLS2020EmploymentDataDBFormatted.csv", index=False)
SOCDataColumnMeaningDf.to_csv('BLS2020EmploymentFieldDescriptionDBFormatted.csv', index=False)
