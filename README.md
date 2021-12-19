# Inverted-Index
The goal of this project is to build an inverted index from a list of documents and retrieve documents related to user queries.

**Steps**:
1. Change the path where the documents are placed. No need to change if its is base directory
2. Take the first word as input to start the query processing
3. Select (AND/OR/AND NOT/OR NOT operation) as per the given instructions
4. Take input for next word
5. Repeat steps 3-4
6. Enter 0 to finish taking input and see the result

**Notes**:
1. The list of file numbers will be displayed along with the full query string.
2. index.txt file will be stored inside the documents folder in JSON format

# Biword and Positional Index
**Notes**:
1. The "documents" folder and "queries.txt" should be in the current working directory
2. Positional Index Structure: Dict{Key -> word, Value -> new list [Total number of frequency , Dict{Key -> doc Number, Value -> position}]}
