'''
@Author: Ayesha Siddika Nipu
Description: This program creates a biword index for the given documents and 
shows result for multiword search query. 
'''

import os
import re
import string
import collections
import nltk as tk
import nltk
import json
import sys

from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

# Folder Path
path = os.path.abspath(os.getcwd()) + '\\documents'
os.chdir(path)
stop_words = set(stopwords.words('english')) 
myDict = {}
#myDefaultdic = defaultdict(int)
loadDict = {}
sortedDict = {}
fileFound = []
biwordQueryList = []
allDocsList = []
totalFiles = -1
filename = "queries.txt"
    
def readlines(fname):
    mypath = os.getcwd() + "\\"+ filename
    """Return contents of file as a list of strings"""
    f = open(mypath, 'r')  #Open file for reading
    lines = f.readlines()       #Read contents as a list of strings
    lines = [line.rstrip() for line in lines] #removes \n from each line
    f.close()   #Return file resources to the operating system
    return lines
    
def SaveAndLoadIndex():
    os.chdir("..")
    json.dump(myDict, open("biword_index.txt",'w'))
    loadDict = json.load(open("biword_index.txt"))
    #print(loadDict)
    
def SortDictionary():
    for key in myDict:
        value = myDict[key]
        sorted_val = sorted(value)
        sortedDict[key] = sorted_val
        
    sorted(sortedDict.keys())
    #print(sortedDict)
    
def CalculateIndexSize():
    print("\n\nThe size of the biword index is: ", sys.getsizeof(myDict), " bytes\n")
    
def StemmingWord(word):
    word_low = word.lower()
    #str_without_punc = word_low.translate(str.maketrans('', '', string.punctuation))
    stemmer = tk. stem . PorterStemmer ()
    stemmed_word = stemmer.stem(word)
    #print(stemmed_word)
    return stemmed_word
    
def StemmingSentence(sen):
    text_string = sen.lower()
    str_without_punc = text_string.translate(str.maketrans('', '', string.punctuation))
    toks = tk. word_tokenize ( str_without_punc )
    stemmer = tk. stem . PorterStemmer ()
    stemmed_words = [ stemmer . stem ( word ) for word in toks ]
    #filtered_sentence = [w for w in stemmed_words if not w. lower () in stop_words ]
    return stemmed_words

# Function to convert  
def listToString(s): 
    
    # initialize an empty string
    str1 = " " 
    # return string  
    return (str1.join(s))

def getBiwordListQuery(stemmedQuery):
    biword_query = []
    for i in range (0, len(stemmedQuery)-1):
        biword = str(stemmedQuery[i]) + ' ' + str(stemmedQuery[i+1])
        biword_query.append(biword)
    #print("\nbiword list: ", biword_query, "\n\n")
    return biword_query
        
            
def PerformSearch():
    queries = readlines(filename)
    for query in queries:
        res = set(allDocsList)
        stemmed_query = StemmingSentence(query)
        biwordQueryList = getBiwordListQuery(stemmed_query)
        #print(biwordQueryList)
        for i in range(0, len(biwordQueryList)):
            #print("inside for loop")
            if biwordQueryList[i] not in myDict.keys():
                #print("inside no match!\n")
                res = []
                break
            else: 
                #print("dictionary key: ", myDict[biwordQueryList[i]], "\n")
                res = set(res) & set(myDict[biwordQueryList[i]])
        
        #print("res", res)        
        if list(res):
            print("The query [", query, "] found in the following documents: ", sorted(list(res)) , "\n")
        else:
            print("The query [", query, "] not found in the biword index!\n")
        
def main():
    for file in os.listdir():
    # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            with open(file_path, 'r') as f:
                filename = os.path.basename(file_path)
                filename_without_ext = os.path.splitext(filename)[0]
                filename_int = int(filename_without_ext.split("_")[1])      
                frequency = {}
                document_text = f.read()
                stemmed_words = StemmingSentence(document_text)
                #occurrences = collections.Counter(stemmed_words) 
                for i in range (0, len(stemmed_words)-1):
                    biword = str(stemmed_words[i]) + ' ' + str(stemmed_words[i+1])
                    if biword in myDict:
                        if filename_int not in myDict[biword]:
                            myDict[biword].append(filename_int)
                    else:
                        myDict[biword] = [filename_int]
                #myDefaultdic[str(stemmed_words[i]) + ' ' + str(stemmed_words[i+1])] += 1
                    
    #print(myDict)
    SortDictionary()
    CalculateIndexSize()            
    SaveAndLoadIndex()
    PerformSearch()
    
totalFiles = len([name for name in os.listdir(path) if name.startswith('file_') and os.path.isfile(name)])
allDocsList = list(range(1, totalFiles+1))
#print(allDocsList)
if __name__ == "__main__":
    main()

