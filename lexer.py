import sys
import re


def lex(characters, token_expressions):
    position = 0
    tokens = []
    # not end of file
    while position < len(characters):
        match = None
    # tokenize the text
        for token_exp in token_expressions:
            pattern, tag = token_exp
            regex = re.compile(pattern)
            match = regex.match(characters, position)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %s\n' % characters[position])
            sys.exit(1)
        else:
            position = match.end(0)
    return tokens
