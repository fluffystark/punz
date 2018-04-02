from tok_expr import *
from combinator import *
from punzal_ast import *

# Basic parsers


def keyword(kw):
    return Reserved(kw, RESERVED)

# identifies INT and changes value to integer
# we should change this to something representing real num


num = Tag(REAL) ^ (lambda i: float(i))
id = Tag(ID)
string = Tag(STRING)
counter = Tag(COUNT)


# Top level parser
def punzal_parse(tokens):
    ast = parser()(tokens, 0)
    return ast


def parser():
    return Phrase(func_list())


def func_list():
    def process(parsed):
        func_list = parsed
        return FunctionDict(func_list)
    return Rep(func_stmt()) ^ process


def func_stmt():
    def process(parsed):
        (((((_, name), _), parms), _), body) = parsed
        return FunctionStatement(name, parms, body)
    return keyword('function') + id + keyword('(') + Opt(param_list()) + keyword(')') + block_stmt() ^ process


def func_call():
    def process(parsed):
        ((((name, _), args), _), _) = parsed
        return FunctionCall(name, args)
    return id + keyword('(') + Opt(args_list()) + keyword(')') + keyword(';') ^ process


def built_func_call():
    def process(parsed):
        ((name, _), args) = parsed
        return BuiltFunctionCall(name, args)
    return id + keyword('.') + class_func_call() ^ process


def class_func_call():
    def process(parsed):
        ((((name, _), args), _), _) = parsed
        return ClassFunctionCall(name, args)
    return id + keyword('(') + Opt(args_list()) + keyword(')') + keyword(';') ^ process


def args_list():
    separator = keyword(',') ^ (lambda x: lambda l, r: ArguementExpression(l, r))
    return Exp(arithmetic_expression_value(), separator)


def block_stmt():
    def process(parsed):
        (((_, stmt), return_stmt), _) = parsed
        return BlockStatement(stmt, return_stmt)
    return keyword('{') + stmt_list() + Opt(return_stmt()) + keyword('}') ^ process


def param_list():
    # variable = parser PROCESS function
    separator = keyword(',') ^ (lambda x: lambda l, r: ArguementExpression(l, r))
    return Exp(declaration_stmt(), separator)


def declaration_stmt():
    return primitive_declaration() | aggregate_declaration()


def primitive_declaration():
    def process(parsed):
        ((data_type, variable), _) = parsed
        return DeclarationStatement(variable, data_type)
    return any_data_type_in_list() + id + Opt(keyword(';')) ^ process


def aggregate_declaration():
    def process(parsed):
        (((((data_type, variable), _), size), _), _) = parsed
        return Set(variable, size, data_type)
    return keyword('Set') + id + keyword('[') + \
        Opt(arithmetic_expression_value()) + keyword(']') + Opt(keyword(';')) ^ process


def aggregate_assignment():
    def process(parsed):
        (((variable, _), pos), _) = parsed
        return SetAssignment(variable, pos)
    return id + keyword('[') + arithmetic_expression_value() + keyword(']') ^ process


def print_stmt():
    def process(parsed):
        (((_, strings), _), _) = parsed
        return PrintStatement(strings)
    return keyword('Print') + keyword('(') + print_term() + keyword(')') + keyword(';') ^ process


def print_term():
    return print_args() | string_term()


def print_args():
    separator = keyword('+') ^ (lambda x: lambda l, r: ArguementExpression(l, r))
    return Exp(string_term(), separator)


def string_term():
    return string_stmt() | arithmetic_expression()


def string_stmt():
    return (string ^ (lambda i: StringStatement(i)))


# Statements
def stmt_list():
    def process(parsed):
        stmt_list = parsed
        return StatementList(stmt_list)
    return Rep(stmt()) ^ process


def stmt():
    return assign_stmt() | \
        selection_stmt() | \
        iteration_stmt() | \
        func_call() | \
        declaration_stmt() | \
        print_stmt() | built_func_call()


def return_stmt():
    def process(parsed):
        ((_, ret), _) = parsed
        return ReturnStatement(ret)
    return keyword('return') + arithmetic_expression() + keyword(';') ^ process


def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        if type(exp) is tuple:
            (exp, _) = exp
        return AssignStatement(name, exp)
    return assignment_term() + keyword('=') + assignment_group() ^ process


def assignment_term():
    return aggregate_assignment() | declaration_stmt() | id


def assignment_group():
    return arithmetic_expression() + keyword(';') | \
        func_call() | aggregate_dataset() | aggregate_assignment() + keyword(';') \
        | built_func_call()


def aggregate_dataset():
    def process(parsed):
        (((_, args), _), _) = parsed
        return args
    return keyword('{') + args_list() + keyword('}') + keyword(';') ^ process


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


def elseif_stmt():
    def process(parsed):
        ((((((_, _), condition), _), _), body), _) = parsed
        return ElseIfStatement(condition, body)
    return keyword('else if') + keyword('(') + boolean_expression() + keyword(')') +\
        keyword('{') + Lazy(stmt_list) + keyword('}') ^ process


def elseif_list():
    def process(parsed):
        elif_list = parsed
        return ElseIfList(elif_list)
    return Rep(elseif_stmt()) ^ process


def selection_stmt():
    def process(parsed):
        ((if_stmt, elseif_stmt,), else_stmt) = parsed
        return SelectionStatement(if_stmt, elseif_stmt, else_stmt)
    return if_stmt() + Opt(elseif_list()) + Opt(else_stmt()) ^ process


def iteration_stmt():
    return while_stmt() | do_while_stmt()


def while_stmt():
    def process(parsed):
        ((((((_, _), condition), _), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + keyword('(') + boolean_expression() + keyword(')') + \
        keyword('{') + Lazy(stmt_list) + \
        keyword('}') ^ process


def do_while_stmt():
    def process(parsed):
        (((((((_, _), body), _), _), _), condition), _) = parsed
        return DoWhileStatement(condition, body)
    return keyword('do') + keyword('{') + Lazy(stmt_list) + \
        keyword('}') + keyword('while') + keyword('(') + boolean_expression() + keyword(')') ^ process


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
    relational_operators = ['<', '<=', '>', '>=', '==', '!=']
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


def any_data_type_in_list():
    return keyword('Counter') | keyword('Real')


# Operator keywords and precedence levels


arithmetic_expression_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

boolean_expression_precedence_levels = [
    ['AND'],
    ['OR'],
]
