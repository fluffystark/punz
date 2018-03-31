import sys
from punzparser import *
from tok_expr import *

def usage():
    sys.stderr.write('Usage: imp filename\n')
    sys.exit(1)

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     usage()
    filename = 'foo.imp'
    text = open(filename).read()
    tokens = lex_tokens(text)
    parse_result = punzal_parse(tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)
    ast = parse_result.value
    ast.eval()
