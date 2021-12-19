'''
@Author: Ayesha Siddika Nipu
Description: The program creates a positional index for the given documents and 
shows result for the multiword search query. 
'''

import os
import re
import string
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
myDict = {} # key -> term, value -> subDict
subDict = {} # Key -> doc id, value -> positions
# Initialize the dictionary.
pos_index = {}
#myDefaultdic = defaultdict(int)
loadDict = {}
sortedDict = {}
fileFound = []
biwordQueryList = []
allDocsList = []
totalFiles = -1
filename = "queries.txt"    
file_map = {}
positionList = []
    
def readlines(fname):
    mypath = os.getcwd() + "\\" + filename
    """Return contents of file as a list of strings"""
    f = open(mypath, 'r')  #Open file for reading
    lines = f.readlines()       #Read contents as a list of strings
    lines = [line.rstrip() for line in lines] #removes \n from each line
    f.close()   #Return file resources to the operating system
    return lines
    
def SaveAndLoadIndex():
    os.chdir("..")
    json.dump(myDict, open("positional_index.txt",'w'))
    loadDict = json.load(open("positional_index.txt"))
    #print(loadDict)
    
def SortDictionary():
    for key in myDict:
        value = myDict[key]
        sorted_val = sorted(value)
        sortedDict[key] = sorted_val
        
    sorted(sortedDict.keys())
    #print(sortedDict)
    
def CalculateIndexSize():
    print("\n\nThe size of the positional index is: ", sys.getsizeof(myDict), " bytes\n")
    
def StemmingWord(word):
    word_low = word.lower()
    #str_without_punc = word_low.translate(str.maketrans('', '', string.punctuation))
    stemmer = nltk. stem . PorterStemmer ()
    stemmed_word = stemmer.stem(word)
    #print(stemmed_word)
    return stemmed_word
    
def StemmingSentence(sen):
    text_string = sen.lower()
    str_without_punc = text_string.translate(str.maketrans('', '', string.punctuation))
    toks = nltk. word_tokenize ( str_without_punc )
    stemmer = nltk. stem . PorterStemmer ()
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

def MatchedDoc(query):
    stemmed_query = StemmingSentence(query)
    #print("stemmed query: ", stemmed_query)
    w1 = []
    w2 = []
    res_doc = {}
    for i in range(0, len(stemmed_query)):
        if stemmed_query[i] not in myDict:
            break
        else:
            word2 = myDict[stemmed_query[i]]
            if i==0:
                word1 = word2
                w1 = word1[1]
                    
            else:
                w2 = word2[1]
                res_doc = w1.keys() & w2.keys()
                                
    return list(res_doc)
                
def PerformSearch():
    queries = readlines(filename)
    for query in queries:
        res = []
        res_doc = MatchedDoc(query) 
        #print(res_doc)   
        stemmed_query = StemmingSentence(query)
        #print("stemmed query: ", stemmed_query)
        w1 = []
        w2 = []
        #res_doc = {}
        for doc in res_doc:
            listofPos = []
            matched_pos = {}
            for i in range(0,len(stemmed_query)):
                word = myDict[stemmed_query[i]][1]
                #print("word: ", stemmed_query[i], word)
                if doc in word:
                    word_pos = word[doc]
                    for j in range(0,len(word_pos)):
                        word_pos[j] = word_pos[j] - i
                        listofPos.append(word_pos)    
                #print("word", stemmed_query[i]," word pos: ", word_pos, "doc ID: ", doc)
            matched_pos = list(set.intersection(*map(set, listofPos)))
            #print("list pos: ", matched_pos) 
            if matched_pos:
                if doc not in res:
                    res.append(doc)
          
        if res:
            res_sort = sorted(res, key = int)
            print("The query [", query, "] found in the following documents: ", str(res_sort) , "\n")
        else:
            print("The query [", query, "] not found in the positional index!\n")
                
def main():
    fileno = 0
    for file in os.listdir():
    # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            with open(file_path, 'r') as f:
                filename = os.path.basename(file_path)
                filename_without_ext = os.path.splitext(filename)[0]
                fileno = filename_without_ext.split("_")[1]     
                frequency = {}
                document_text = f.read()
                stemmed_words = StemmingSentence(document_text)
                for word_pos, word in enumerate(stemmed_words):
                    if word in myDict:
                        myDict[word][0] = myDict[word][0] + 1
                        if fileno in myDict[word][1]:
                            myDict[word][1][fileno].append(word_pos)
                        else:
                            myDict[word][1][fileno] = [word_pos]
                    else:
                        myDict[word] = []
                        myDict[word].append(1)
                        myDict[word].append({})
                        myDict[word][1][fileno] = [word_pos]
                #print(filename)
                file_map[fileno] = filename
                
    
    #print("File map list: \n")
    #print(file_map)
    #print(myDict)                
    #print(myDict)
    #SortDictionary()
    CalculateIndexSize()            
    SaveAndLoadIndex()
    PerformSearch()
    
totalFiles = len([name for name in os.listdir(path) if name.startswith('file_') and os.path.isfile(name)])
allDocsList = list(range(1, totalFiles+1))

#print(allDocsList)
if __name__ == "__main__":
    main()

