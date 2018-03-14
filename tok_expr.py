import lexer

RESERVED = 'RESERVED'
INT = 'INT'
ID = 'ID'

token_exprs = [
    (r'[ \n\t]+', None),     # nextline tab
    (r'#[^\n]*', None),      # nextline
    (r'\(', RESERVED),       # (
    (r'\)', RESERVED),       # )
    (r'{', RESERVED),       # block start
    (r'}', RESERVED),       # block end
    (r'\.', RESERVED),       # member
    (r'=', RESERVED),        # =
    (r';', RESERVED),        # ;
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
    (r'end', RESERVED),  # idk for what
    (r'Real', RESERVED),  # real number data type
    (r'Set', RESERVED),  # Set or an array
    (r'Function', RESERVED),  # Initializes a function
    (r'[0-9]+', INT),  # number has to be a float
    (r'[A-Za-z][A-Za-z0-9_]*', ID),  # identifier
]


def lex_tokens(characters):
    return lexer.lex(characters, token_exprs)
