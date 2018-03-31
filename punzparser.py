from tok_expr import *
from combinator import *
from punzal_ast import *

# Basic parsers


def keyword(kw):
    return Reserved(kw, RESERVED)

# identifies INT and changes value to integer
# we should change this to something representing real num


num = Tag(INT) ^ (lambda i: int(i))
id = Tag(ID)


# Top level parser
def punzal_parse(tokens):
    ast = parser()(tokens, 0)
    return ast


def parser():
    return Phrase(func())


def block_stmt():
    def process(parsed):
        ((_, stmt), _) = parsed
        return BlockStatement(stmt)
    return keyword('{') + stmt_list() + keyword('}') ^ process


def param_list():
    # variable = parser PROCESS function
    separator = keyword(',') ^ (lambda x: lambda l, r: ParameterExpression(l, r))
    return Exp(param_stmt(), separator)


def param_stmt():
    return id


def func():
    def process(parsed):
        (((((_, name), _), parms), _), body) = parsed
        return FunctionStatement(name, parms, body)
    return keyword('function') + id + keyword('(') + param_list() + keyword(')') + block_stmt() ^ process


# Statements
def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


def stmt():
    return assign_stmt() | \
        selection_stmt() | \
        while_stmt()


def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword('=') + arithmetic_expression() ^ process


def if_stmt():
    def process(parsed):
        ((((((_, _), condition), _), _), body), _) = parsed
        return IfStatement(condition, body)
    return keyword('if') + keyword('(') + boolean_expression() + keyword(')') +\
        keyword('{') + Lazy(stmt_list) + keyword('}') ^ process


def else_stmt():
    def process(parsed):
        (((_, _), stmt), _) = parsed
        return ElseStatement(stmt)
    return keyword('else') + keyword('{') + Lazy(stmt_list) + keyword('}') ^ process


def elseif_term():
    return elseif_stmt() | \
        elseif_group()


def elseif_stmt():
    def process(parsed):
        ((((((_, _), condition), _), _), body), _) = parsed
        return ElseIfStatement(condition, body)
    return keyword('else if') + keyword('(') + boolean_expression() + keyword(')') +\
        keyword('{') + Lazy(stmt_list) + keyword('}')


def elseif_group():
    def process(parsed):
            ((((((((_, _), condition), _), _), true_stmt), _), elif_parsed), false_parsed) = parsed
            if elif_parsed:
                ((((((_, _), elif_condition), _), _), elif_stmt), _) = elif_parsed
            else:
                elif_stmt = elif_condition = None
            if false_parsed:
                (((_, _), false_stmt), _) = false_parsed
            else:
                false_stmt = None
            return IfStatement(condition, true_stmt, false_stmt, elif_condition, elif_stmt)
    return Lazy(elseif_stmt()) + Opt(elseif_term()) ^ process


def selection_stmt():
    def process(parsed):
        (if_stmt, else_stmt) = parsed
        return SelectionStatement(if_stmt, else_stmt)
    return if_stmt() + Opt(else_stmt()) ^ process

# def selection_stmt():
#     def process(parsed):
#         ((((((((_, _), condition), _), _), true_stmt), _), elif_parsed), false_parsed) = parsed
#         if elif_parsed:
#             ((((((_, _), elif_condition), _), _), elif_stmt), _) = elif_parsed
#         else:
#             elif_stmt = elif_condition = None
#         if false_parsed:
#             (((_, _), false_stmt), _) = false_parsed
#         else:
#             false_stmt = None
#         return IfStatement(condition, true_stmt, false_stmt, elif_condition, elif_stmt)
#     return keyword('if') + keyword('(') + boolean_expression() + keyword(')') +\
#         keyword('{') + Lazy(stmt_list) + keyword('}') + Opt(elseif_stmt()) + \
#         Opt(keyword('else') + keyword('{') + Lazy(stmt_list) + keyword('}')) ^ process


def while_stmt():
    def process(parsed):
        ((((((_, _), condition), _), _), body), _) = parsed
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
    return (num ^ (lambda i: RealArithmeticExp(i))) | \
           (id ^ (lambda v: VariableArithmeticExp(v)))


# An IMP-specific combinator for binary operator expressions (arithmetic_expression and bexp)
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser


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


def process_group(parsed):
    ((_, p), _) = parsed
    return p


def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

# Operator keywords and precedence levels


arithmetic_expression_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

boolean_expression_precedence_levels = [
    ['and'],
    ['or'],
]
