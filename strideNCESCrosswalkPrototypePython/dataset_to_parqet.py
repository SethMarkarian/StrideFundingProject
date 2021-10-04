import pandas as pd

df1 = pd.read_csv('crosswalk.csv')
df1.to_parquet('crosswalk.parquet')

df2 = pd.read_csv('FieldOfStudyData1617_1718_PP.csv')
df2.to_parquet('FieldOfStudyData1617_1718_PP.parquet')

df3 = pd.read_excel('CIP2020_SOC2018_Crosswalk.xlsx', sheet_name = 1)
df3.to_parquet('CIP2020_SOC2018_Crosswalk.parquet')

# Below returns an error for some reason
df4 = pd.read_excel('national_M2020_dl.xlsx', sheet_name = 0)
df4.to_parquet('national_M2020_dl.parquet')