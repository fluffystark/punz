import sys
from lexer import *
from tok_expr import *

if __name__ == '__main__':
<<<<<<< HEAD
    filename = 'foo.imp'
=======
    filename = sys.argv[1]
>>>>>>> 6c01e2df9f05864c3e6bd663de8c4dad72fc930b
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = lex_tokens(characters)
    for token in tokens:
        print token
