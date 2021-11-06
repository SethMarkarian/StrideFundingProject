from stride_data.db.database import DataLake, DataLakeConfig
import os
import re
import pandas as pd

df = pd.DataFrame()

def queryData(stringQuery, socMap):
    stringQuery = stringQuery.replace('=', '==').replace('%', '=%').replace('_', '=_')
    data = db_conn.execute("SELECT occ_title, occ_code FROM bls2020 WHERE occ_title ILIKE %(like)s ESCAPE '=';",
     dict(like= '%'+stringQuery+'%'))
    for tupleData in data:
        if tupleData[0] not in soc_match_freq_map:
            socMap[tupleData] = 1
        else:
            socMap[tupleData] += 1

databaseFile = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
 'database_init.txt'), 'r')

username, password = None, None
for line in databaseFile:
    username, password = line.split()

config = DataLakeConfig(username, password)
db_conn = DataLake()
db_conn.connect(config)

socFile = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
 'soc_unmatched.txt'), 'r')

uniqueSOCTitles = {}
for line in socFile:
    line = line.strip()
    if line not in uniqueSOCTitles:
        uniqueSOCTitles[line] = True

nullKeys = 0
finalList = []
for key in uniqueSOCTitles:
    soc_match_freq_map = {}
    name_array = re.split(r'\W+', key)
    for item in name_array:
        if len(item) > 1:
            queryData(item, soc_match_freq_map)
    maxSoc = []
    maxFreq = 0
    for mapKey, value in soc_match_freq_map.items():
        if value > maxFreq:
            maxSoc = [mapKey]
            maxFreq = value
        elif value == maxFreq:
            maxSoc.append(mapKey)

    if len(maxSoc) == 0:
        nullKeys += 1
        finalList.append([key, 'NULL', 'NULL'])
    else:
        for soc in maxSoc:
            finalList.append([key, soc[0], soc[1]])

totalNames = len(uniqueSOCTitles)
matchedNames = totalNames - nullKeys
print('ANALYSIS'.ljust(50), '\n')
print(f'Total job titles analyzed -> {totalNames}'.ljust(50), '(1)\n')
print(f'Total matched -> {matchedNames}'.ljust(50), '(2)\n')
print(f'Percentage matched -> {(matchedNames*100.0)/totalNames}'.ljust(50), '(3)\n')
print('Output written in matched_soc.csv'.ljust(50), '(4)\n')
df = df.append(finalList, ignore_index=True)
df.columns = ['Original_Occupation_Name', 'Matched_SOC_Title', 'Matched_SOC_Code']
df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),
 'matched_soc.csv'), index=False)
socFile.close()
db_conn.close()