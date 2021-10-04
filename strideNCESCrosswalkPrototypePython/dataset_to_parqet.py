import pandas as pd

df = pd.read_csv('crosswalk.csv')
df.to_parquet('crosswalk.parquet')

df = pd.read_csv('FieldOfStudyData1617_1718_PP.csv')
df.to_parquet('FieldOfStudyData1617_1718_PP.parquet')

df = pd.read_excel('CIP2020_SOC2018_Crosswalk.xlsx', sheet_name = 1)
df.to_parquet('CIP2020_SOC2018_Crosswalk.parquet')

# Below returns an error for some reason
# df = pd.read_excel('national_M2020_dl.xlsx', sheet_name = 0)
# df.to_parquet('national_M2020_dl.parquet')