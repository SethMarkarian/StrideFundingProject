from stride_data.db.database import DataLake, DataLakeConfig
import os
import re

N_GRAM_MIN = 4

def queryData(stringQuery, socMap):
    stringQuery = stringQuery.replace('=', '==').replace('%', '=%').replace('_', '=_')
    data = db_conn.execute("SELECT occ_code FROM bls2020 WHERE occ_title ILIKE %(like)s ESCAPE '=';",
     dict(like= '%'+stringQuery+'%'))
    for tupleData in data:
        if tupleData[0] not in soc_match_freq_map:
            socMap[tupleData[0]] = 1
        else:
            socMap[tupleData[0]] += 1

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


outputSocFileMatch = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
 'soc_matched.txt'), 'w')

uniqueSOCTitles = {}
for line in socFile:
    line = line.strip()
    if line not in uniqueSOCTitles:
        uniqueSOCTitles[line] = True

for key in uniqueSOCTitles:
    soc_match_freq_map = {}
    name_array = key.split()
    for item in name_array:
        item = item.strip('-')
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
        maxSoc = 'NULL'
        outputSocFileMatch.write(f'{key} -> {maxSoc}\n')
    else:
        for soc in maxSoc:
            outputSocFileMatch.write(f'{key} -> {soc}\n')

outputSocFileMatch.close()
socFile.close()
db_conn.close()