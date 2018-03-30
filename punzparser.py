from tok_expr import *
from combinator import *
<<<<<<< HEAD
from punzal_ast import *
=======
from tree import *
>>>>>>> 6c01e2df9f05864c3e6bd663de8c4dad72fc930b

# Basic parsers


def keyword(kw):
    return Reserved(kw, RESERVED)

# identifies INT and changes value to integer
# we should change this to something representing real num


num = Tag(INT) ^ (lambda i: int(i))
id = Tag(ID)


# Top level parser
<<<<<<< HEAD
def punzal_parse(tokens):
=======
def imp_parse(tokens):
>>>>>>> 6c01e2df9f05864c3e6bd663de8c4dad72fc930b
    ast = parser()(tokens, 0)
    return ast


def parser():
    return Phrase(stmt_list())


# Statements
def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


<<<<<<< HEAD
def stmt():
    return assign_stmt() | \
        if_stmt() | \
        while_stmt()


=======
>>>>>>> 6c01e2df9f05864c3e6bd663de8c4dad72fc930b
def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
<<<<<<< HEAD
    return id + keyword('=') + arithmetic_expression() ^ process


def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return keyword('if') + boolean_expression() + \
        keyword('then') + Lazy(stmt_list) + \
        Opt(keyword('else') + Lazy(stmt_list)) + \
        keyword('end') ^ process


def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + keyword('(') + boolean_expression() + keyword(')') + \
        keyword('{') + Lazy(stmt_list) + \
        keyword('}') ^ process

# Boolean expressions


def boolean_expression():
    return precedence(boolean_expression_term(),
                      boolean_expression_precedence_levels,
                      process_logic)


def boolean_expression_term():
    return boolean_expression_not() | \
        boolean_expression_relational_operation() | \
        boolean_expression_group()


def boolean_expression_not():
    return keyword('not') + Lazy(boolean_expression_term) ^ (lambda parsed: NotBooleanExp(parsed[1]))


def boolean_expression_relational_operation():
    relational_operators = ['<', '<=', '>', '>=', '=', '!=']
    return arithmetic_expression() + any_operator_in_list(relational_operators) \
        + arithmetic_expression() ^ process_relational_operation


def boolean_expression_group():
    return keyword('(') + Lazy(boolean_expression) + keyword(')') ^ process_group

# Arithmetic expressions


def arithmetic_expression():
    return precedence(arithmetic_expression_term(),
                      arithmetic_expression_precedence_levels,
                      process_binary_operation)


def arithmetic_expression_term():
    return arithmetic_expression_value() | arithmetic_expression_group()


def arithmetic_expression_group():
    return keyword('(') + Lazy(arithmetic_expression) + keyword(')') ^ process_group


def arithmetic_expression_value():
=======
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
>>>>>>> 6c01e2df9f05864c3e6bd663de8c4dad72fc930b
    return (num ^ (lambda i: RealArithmeticExp(i))) | \
           (id ^ (lambda v: VariableArithmeticExp(v)))


<<<<<<< HEAD
# An IMP-specific combinator for binary operator expressions (arithmetic_expression and bexp)
=======
# An IMP-specific combinator for binary operator expressions (aexp and bexp)
>>>>>>> 6c01e2df9f05864c3e6bd663de8c4dad72fc930b
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

<<<<<<< HEAD

def process_binary_operation(op):
    return lambda l, r: BinaryOpArithmeticExp(op, l, r)


def process_relational_operation(parsed):
    ((left, op), right) = parsed
    return RelOpBooleanExp(op, left, right)


def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBooleanExp(l, r)
    elif op == 'or':
        return lambda l, r: OrBooleanExp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)


=======
def process_binop(op):
    return lambda l, r: BinaryOpArithmeticExp(op, l, r)

>>>>>>> 6c01e2df9f05864c3e6bd663de8c4dad72fc930b
def process_group(parsed):
    ((_, p), _) = parsed
    return p


def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

# Operator keywords and precedence levels


<<<<<<< HEAD
arithmetic_expression_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

boolean_expression_precedence_levels = [
    ['and'],
    ['or'],
]
=======
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]
>>>>>>> 6c01e2df9f05864c3e6bd663de8c4dad72fc930b
