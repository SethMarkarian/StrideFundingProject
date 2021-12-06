import pandas as pd
from psql.main import getPSQLOutput
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import math

# The number of times a word appears in a document divded by the total number of 
# words in the document. Every document has its own term frequency.
def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

# The log of the number of documents divided by the number of documents that 
# contain the word w. Inverse data frequency determines the weight of rare words 
# across all documents in the corpus.
def computeIDF(documents):
    idfDict = {}
    N = len(documents)

    idfDict = dict.fromkeys(documents[0].keys(), 0)

    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))

    return idfDict


# The TF-IDF is simply the TF multiplied by IDF.
def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf

def importingAndSetup():
    SOCdf = getPSQLOutput('SELECT SOC2018CodeTitle, SOC2018Code FROM cip2020_soc2018')
    SOCdf = SOCdf[['soc2018codetitle', 'soc2018code']].copy()
    return SOCdf

def runTFIDF(documentA, documentB): 
    # Machine learning algorithms cannot work with raw text directly. Rather, the text must be converted 
    # into vectors of numbers. In natural language processing, a common technique for extracting features 
    # from text is to place all of the words that occur in the text in a bucket. This aproach is called a 
    # bag of words model or BoW for short. It’s referred to as a “bag” of words because any information 
    # about the structure of the sentence is lost.
    bagOfWordsA = documentA.split(' ')
    bagOfWordsB = documentB.split(' ')

    # Removes duplicate words
    uniqueWords = set(bagOfWordsA).union(set(bagOfWordsB))

    # Creates a dictionary of words and their counts
    numOfWordsA = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsA:
        numOfWordsA[word] += 1
    numOfWordsB = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsB:
        numOfWordsB[word] += 1

    # Computes the term frequency for each word
    stopwords.words('english')

    # Compute the term frequency for each of our documents.
    tfA = computeTF(numOfWordsA, bagOfWordsA)
    tfB = computeTF(numOfWordsB, bagOfWordsB)

    # The IDF is computed once for all documents.
    idfs = computeIDF([numOfWordsA, numOfWordsB])

    # Compute the TF-IDF scores for all the words in the corpus.
    tfidfA = computeTFIDF(tfA, idfs)
    tfidfB = computeTFIDF(tfB, idfs)

    df = pd.DataFrame([tfidfA, tfidfB])

    # Rather than manually implementing TF-IDF ourselves, we could use the class provided by sklearn.
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([documentA, documentB])
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)

    return df

if __name__ == "__main__":
    documentA = str(input("Enter a title: "))
    SOCdf = importingAndSetup()
    finaldf = pd.DataFrame(columns=['SOCtitle', 'SOCcode'])
    # Loop over all the rows in the SOCdf
    for i in range(0, len(SOCdf)):
        df = runTFIDF(documentA, SOCdf['soc2018codetitle'][i])
        # Use the standerd deviation to determine the similarity
        if(df.stack().std() < 0.25):
            newdf = pd.DataFrame({'SOCtitle': [SOCdf['soc2018codetitle'][i]], 'SOCcode': [SOCdf['soc2018code'][i]]})
            finaldf = finaldf.append(newdf)
    print(finaldf.drop_duplicates())