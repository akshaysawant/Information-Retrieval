
Instructions for running Project 1 : 

Before startning to run Project 1 follow below instructions - 
1. Program uses Beautiful Soup and stemming-1.0 libraries.
2. Make sure they are built and installed on the machine.
3. All tokens which needs to be ignored needs to be placed in a file named "ignore_tokens.txt".

Part 1: Tokenizing Documents
1. Make sure you have placed the directory in which files exists for tokenization.
2. Make sure token.py file has executable permissions.
3. Run the code with following command - 
python token.py DIRECTORY_NAME

Part 2: Inverting the index
1. Make sure part 1 execution is complete.
2. Make sure index.py has executable permissions.
3. Run the code with following command - 
./index.py

Part 3: Reading the index
1. Make sure part 2 execution is complete.
2. Make sure read_index.py has executable permissions.
3. Run the command in one of the following formats - 
    a) ./read_index.py --doc DOCNAME
    b) ./read_index.py --term TERM
    c) ./read_index.py --term TERM --doc DOCNAME



Extra Credit - 

I have attempted extra credit for part 2 of the Project 1. I have implemented part 2 in linear time with respect to the length of doc_index.txt.
