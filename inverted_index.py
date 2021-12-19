'''
@Author: Ayesha Siddika Nipu
Description: The goal for this program is to build an inverted index from a list of documents and 
retrieve documents related to user queries.
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

# Set Folder Path
path = os.path.abspath(os.getcwd()) + '\\documents'
os.chdir(path)
stop_words = set(stopwords.words('english')) 
myDict = {}
loadDict = {}
sortedDict = {}
fileFound = []
wordsForSearch = []
operationForSearch = []
allDocsList = []
totalFiles = -1

#Save an index in JSON format        
def SaveAndLoadIndex():
    json.dump(sortedDict, open("index.txt",'w'))
    loadDict = json.load(open("index.txt"))
    #print(loadDict)

#Sorting a dictionary using value    
def SortDictionaryPostings():
    for key in myDict:
        value = myDict[key]
        sorted_val = sorted(value)
        sortedDict[key] = sorted_val
        #print(sortedDict)

#Calculating the size of an index    
def CalculateIndexSize():
    print("\n\nThe size of the index is: ", sys.getsizeof(myDict), " bytes\n")

#Using PorterStemmer for word stemming    
def StemmingWord(word):
    word_low = word.lower()
    #str_without_punc = word_low.translate(str.maketrans('', '', string.punctuation))
    stemmer = tk. stem . PorterStemmer ()
    stemmed_word = stemmer.stem(word)
    #print(stemmed_word)
    return stemmed_word

#Performing cleanup for each sentence i.e. removing punctuation, tokenizing and stemming    
def StemmingSentence(sen):
    text_string = sen.lower()
    str_without_punc = text_string.translate(str.maketrans('', '', string.punctuation))
    toks = tk. word_tokenize ( str_without_punc )
    stemmer = tk. stem . PorterStemmer ()
    stemmed_words = [ stemmer . stem ( word ) for word in toks ]
    filtered_sentence = [w for w in stemmed_words if not w. lower () in stop_words ]
    return filtered_sentence

#Provide instruction to user regarding the operation they want to perform for the query        
def ChooseOperation():
    print('Press 1 to perform AND operation')
    print('Press 2 to perform OR operation')
    print('Press 3 to perform AND NOT operation')
    print('Press 4 to perform OR NOT operation')
    print('Press 0 to exit')
    return input('Choose next operation: ')

#Mapping the operations of user query
def MapOperationString(op):
    operation_str = ""
    if op == "1":
        operation_str = " AND "
    elif op == "2":
        operation_str = " OR "
    elif op == "3":
        operation_str = " AND NOT "
    elif op == "4":
        operation_str = " OR NOT "
    #print(operation_str)
    return operation_str

#Performing and/or operations between two sets of list
def PerformOperation(option, posting1, posting2):
    if option == "1":
        return list(set(posting1) & set(posting2))
    elif option == "2":
        return list(set(posting1) | set(posting2))
    elif option == "3":
        notWord2 = set(allDocsList).difference(set(posting2))
        return list(set(posting1) & notWord2)
    elif option == "4":
        notWord2 = set(allDocsList).difference(set(posting2))
        return list(set(posting1) | notWord2)
            
#Performing search based on the user input
def PerformSearch():
    #print("Please enter the first word to continue query processing: ")
    word1 = input('Please enter the first word to continue query processing: ')
    stemmed_word1 = StemmingWord(word1)
    #print("stemmed word 1", stemmed_word1)
    queryStr = word1 + " "
    posting1 = posting2 = ""
    res = []
    if stemmed_word1 in sortedDict:
        posting1 = sortedDict[stemmed_word1]
    while(True):
        op = ChooseOperation()
        if op == "0":
            #print("Program Completed!")
            #print(len(queryStr))
            #print(len(queryStr.split()))
            if len(queryStr.strip().split()) == 1:
                print("Invalid input! Need at least two valid words to perform the query.")
            elif len(res) == 0:
                print("No index found for the following query: ", queryStr)
            else:    
                print("(", queryStr, ") found in the following documents: ", res)
            break;
        
        #print("Please enter the next word: ")
        word2 = input('Please enter the next word: ')
        queryStr += MapOperationString(op) + word2
        
        stemmed_word2 = StemmingWord(word2)
        #print("stemmed word 2", stemmed_word2)
        if stemmed_word2 in sortedDict:
            posting2 = sortedDict[stemmed_word2]
        res = PerformOperation(op, posting1, posting2)
        posting1 = res

#Load dataset from the directory and extract the name of the file        
def main():
    for file in os.listdir():
    # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            with open(file_path, 'r') as f:
                filename = os.path.basename(file_path)
                if filename != "index.txt":
                    filename_without_ext = os.path.splitext(filename)[0]
                    filename_int = int(filename_without_ext.split("_")[1])      
                    frequency = {}
                    document_text = f.read()
                    filtered_sentence = StemmingSentence(document_text)
                    occurrences = collections.Counter(filtered_sentence) 
                    for word in occurrences:
                        if word in myDict:
                            myDict[word].append(filename_int)
                        else:
                            myDict[word] = [filename_int]
    SortDictionaryPostings()
    CalculateIndexSize()            
    SaveAndLoadIndex()
    PerformSearch()

#Calculates total number of files    
totalFiles = len([name for name in os.listdir(path) if name.startswith('file_') and os.path.isfile(name)])
allDocsList = list(range(1, totalFiles+1))
#print(allDocsList)
if __name__ == "__main__":
    main()

