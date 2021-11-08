from socket import socket
import pandas as pd
import sys
from psql.main import getPSQLOutput
from textblob import TextBlob


def generate_ngrams(data, num):
    n_grams = TextBlob(data).ngrams(num)
    print(n_grams)
    return [ ' '.join(grams) for grams in n_grams]

def SOCLookup(title, df):
    pd.set_option('display.max_rows', None)
    newdf = df[df['soc2018codetitle'].str.contains(title, case = False)]
    newdf = newdf.drop_duplicates()
    # print(newdf.to_string(index = False))
    soc_list = newdf['soc2018code'].tolist()
    return soc_list

def importingAndSetup():
    SOCdf = getPSQLOutput('SELECT SOC2018CodeTitle, SOC2018Code FROM cip2020_soc2018')
    SOCdf = SOCdf[['soc2018codetitle', 'soc2018code']].copy()
    return SOCdf

def most_frequent(List):
    return max(set(List), key = List.count)

def main():
    jobTitle = input("Enter Job Title: ")
    if jobTitle == '':
        sys.exit()
    df = importingAndSetup()
    if jobTitle.split(" ").__len__() > 1:
        ngrams = generate_ngrams(jobTitle, 2)
        # print(ngrams)
        total_soc_list = []
        for ngram in ngrams:
            total_soc_list += SOCLookup(ngram, df)
        print(most_frequent(total_soc_list))
    else:
        total_soc_list = SOCLookup(jobTitle, df)
        print(total_soc_list)
    main()

if __name__ == '__main__':
    main()
    