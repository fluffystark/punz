from tok_expr import *
from combinator import *
from tree import *

# Basic parsers


def keyword(kw):
    return Reserved(kw, RESERVED)

# identifies INT and changes value to integer
# we should change this to something representing real num


num = Tag(INT) ^ (lambda i: int(i))
id = Tag(ID)


# Top level parser
def imp_parse(tokens):
    ast = parser()(tokens, 0)
    return ast


def parser():
    return Phrase(stmt_list())


# Statements
def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword('=') + aexp() ^ process


def arithmeticExp():
    return precedence(arithmeticExp_term(),
                      aexp_precedence_levels,
                      process_binop)


def arithmeticExp_term():
    return arithmeticExp_value() | arithmeticExp_group()


def arithmeticExp_group():
    return keyword('(') + Lazy(arithmeticExp) + keyword(')') ^ process_group


def arithmeticExp_value():
    return (num ^ (lambda i: RealArithmeticExp(i))) | \
           (id ^ (lambda v: VariableArithmeticExp(v)))


# An IMP-specific combinator for binary operator expressions (aexp and bexp)
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

def process_binop(op):
    return lambda l, r: BinaryOpArithmeticExp(op, l, r)

def process_group(parsed):
    ((_, p), _) = parsed
    return p


def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

# Operator keywords and precedence levels


aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]
