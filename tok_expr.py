import lexer

RESERVED = 'RESERVED'
COUNT = 'COUNT'
ID = 'ID'
REAL = 'REAL'

token_exprs = [
    (r'[ \n\t]+', None),     # nextline tab
    (r'#[^\n]*', None),      # nextline
    (r'\(', RESERVED),       # (
    (r'\)', RESERVED),       # )
    (r'{', RESERVED),       # block start
    (r'}', RESERVED),       # block end
    (r'\.', RESERVED),       # member
    (r'=', RESERVED),        # =
    (r',', RESERVED),        # ;
    (r';', RESERVED),        # ;
    (r'\[', RESERVED),        # [
    (r'\]', RESERVED),        # ]
    (r'\*', RESERVED),       # *
    (r'/', RESERVED),        # /
    (r'\+', RESERVED),       # +
    (r'-', RESERVED),        # -
    (r'<=', RESERVED),       # <=
    (r'<', RESERVED),        # <
    (r'>=', RESERVED),       # >=
    (r'>', RESERVED),        # >
    (r'!=', RESERVED),       # !=
    (r'==', RESERVED),       # ==
    (r'AND', RESERVED),  # Relational And
    (r'OR', RESERVED),  # Relational OR
    (r'!', RESERVED),  # Not
    (r'if', RESERVED),  # if
    (r'else if', RESERVED),  # have an else if
    (r'else', RESERVED),  # else
    (r'while', RESERVED),  # while
    (r'do', RESERVED),  # do
    (r'return', RESERVED),  # return
    (r'print', RESERVED),  # print
    (r'end', RESERVED),  # idk for what
    (r'Count', RESERVED),  # real number data type
    (r'Real', RESERVED),  # real number data type
    (r'Set', RESERVED),  # Set or an array
    (r'function', RESERVED),  # Initializes a function
    # (r'-?(\d+(\.\d*)?|\.\d+)', REAL),  # for real numbers
    (r'[0-9]+', COUNT),  # number has to be a float
    (r'[A-Za-z][A-Za-z0-9_]*', ID),  # identifier
]


def lex_tokens(characters):
    return lexer.lex(characters, token_exprs)
