import sys
from lexer import *
from tok_expr import *

if __name__ == '__main__':
    filename = 'foo.imp'
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = lex_tokens(characters)
    for token in tokens:
        print token
