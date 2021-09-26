# -*- coding: utf-8 -*-
"""
How to setup environment:
    1. Make sure Python 3.x is installed: https://www.python.org/downloads/
    2. Make sure pip is installed for your Python version:  https://pip.pypa.io/en/stable/installation/
    3. Run `python3 pip install pandas` if pandas library is not installed

How to run program on command line:
    `crosswalk.py <CIP_code> <CIP_code_year>`
    
    <CIP_code_year> == 2010 || 2020 
"""
import pandas as pd
import sys

def cleanCIPCode(CIPCode):
    return str(CIPCode).lstrip('=').strip('"')

def convertNumericalCIPCodetoString(CIPCode):
    CIPCode = str(CIPCode)
    prePoint, postPoint = CIPCode.split('.')
    if len(prePoint) == 1:
        prePoint = '0' + prePoint
    
    postPoint += ''.join(['0' for i in range(4 - len(postPoint))])
    return '.'.join([prePoint, postPoint])
    
def get2020CIPCode(CIPCode2010, fromFieldOfStudyData=False):
    CIPCode = str(CIPCode2010)
    if fromFieldOfStudyData:
        CIPCodeFormatted = '{0}'.format(CIPCode[0])
        if len(CIPCode[1:]) > 0:
            CIPCodeFormatted += '.{0}'.format(CIPCode[1:])
        CIPCode = CIPCodeFormatted
    query = CIP2010toCIP2020Df.query('Original_code == @CIPCode')['Current_code'].tolist()   
    if len(query) == 0:
        raise("2010 CIP code value {0} does not have a 2020 CIP Code.".format(CIPCode))
    else:
        return query[0]

def getSOCCodeFromCIP2020Code(CIPCode2020):
    if len(CIPCode2020) == 2:
        return CIP2020ToSOCDf.query('CIP2020CodeMain == @CIPCode2020')['SOC2018Code'].unique()
    elif len(CIPCode2020) == 5:
        return CIP2020ToSOCDf.query('CIP2020CodeSubMain == @CIPCode2020')['SOC2018Code'].unique()
    else:
        return CIP2020ToSOCDf.query('CIP2020Code == @CIPCode2020')['SOC2018Code'].unique()
    
def getSOCDataFromSOCCodes(SOCCode2018List):
    return SOCDataDf.query('OCC_CODE in @SOCCode2018List').loc[:, ['OCC_CODE', 'OCC_TITLE', 'TOT_EMP', 'A_MEAN']]
    
CIP2010toCIP2020Path = 'crosswalk.csv'
CIP2020ToSOCPath = 'CIP2020_SOC2018_Crosswalk.xlsx'
SOCDataPath = 'national_M2020_dl.xlsx'
fieldOfStudyPath = 'FieldOfStudyData1617_1718_PP.csv'


CIP2010toCIP2020Df = pd.read_csv(CIP2010toCIP2020Path)
CIP2010toCIP2020Df.columns = [column.replace(" ", "_")
                               for column in CIP2010toCIP2020Df.columns]
CIP2010toCIP2020Df['Original_code'] = CIP2010toCIP2020Df['Original_code'].apply(cleanCIPCode)
CIP2010toCIP2020Df['Current_code'] = CIP2010toCIP2020Df['Current_code'].apply(cleanCIPCode)


CIP2020ToSOCDf = pd.read_excel(CIP2020ToSOCPath, sheet_name=1)
CIP2020ToSOCDf['CIP2020Code'] = CIP2020ToSOCDf['CIP2020Code'].apply(convertNumericalCIPCodetoString)
CIP2020ToSOCDf['CIP2020CodeMain'] = CIP2020ToSOCDf['CIP2020Code'].apply(lambda x : str(x)[:2])
CIP2020ToSOCDf['CIP2020CodeSubMain'] = CIP2020ToSOCDf['CIP2020Code'].apply(lambda x : str(x)[:5])

SOCDataDf = pd.read_excel(SOCDataPath, sheet_name=0)

fieldOfStudyCols=['UNITID', 'INSTNM', 'CIPCODE', 'CREDLEV', 'EARN_MDN_HI_1YR', 'EARN_MDN_HI_2YR']
fieldOfStudyDf = pd.read_csv(fieldOfStudyPath,usecols=fieldOfStudyCols)

if __name__ == '__main__':
    try:
        CIPCode = sys.argv[1]
        CIPCodeKind = sys.argv[2]
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} <CIP_code> <CIP_code_year>")
    if CIPCodeKind == '2010':
        print(getSOCDataFromSOCCodes(getSOCCodeFromCIP2020Code(get2020CIPCode(CIPCode))))
    elif CIPCodeKind == '2020':
        print(getSOCDataFromSOCCodes(getSOCCodeFromCIP2020Code(CIPCode)))
    else:
        raise SystemExit("<CIP_code_year> == 2010 || 2020 ")
    
    
    
