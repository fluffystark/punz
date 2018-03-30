import sys
from punzparser import *
from tok_expr import lex_tokens

if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     sys.stderr.write('usage: %s filename parsername\n' % sys.argv[0])
    #     sys.exit(1)
    filename = 'foo.imp'
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = lex_tokens(characters)
<<<<<<< HEAD
    parser = stmt()
=======
    parser = arithmeticExp()
>>>>>>> 6c01e2df9f05864c3e6bd663de8c4dad72fc930b
    result = parser(tokens, 0)
    print result
