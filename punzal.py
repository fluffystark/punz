import sys
from punzparser import *
from tok_expr import *


def usage():
    sys.stderr.write('Usage: imp filename\n')
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = list()
    filename.append("Math.punz")
    filename.append(sys.argv[1])
    text = ""
    for file in filename:
        length = len(file)
        if file[length - 4:length] == "punz":
            text += open(file).read()
    tokens = lex_tokens(text)
    parse_result = punzal_parse(tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)
    ast = parse_result.value
    env = Env()
    x = ast.eval(env)
    print x
else:
    print "File is not readable"
