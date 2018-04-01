from equality import *


class Statement(Equality):
    pass


class Aexp(Equality):
    pass


class Bexp(Equality):
    pass


class Env(dict):
    def __init__(self, outer=None, stmt_list=list()):
        self.outer = outer
        self.stmt_list = stmt_list

    def find(self, var):
        return self if (var in self) else self.outer.find(var)


class BlockStatement(Statement):
    def __init__(self, stmt_list):
        self.stmt_list = stmt_list
        self.env = Env()

    def __repr__(self):
        return 'BlockStatement(%s, %s)' % (self.stmt_list, self.env)

    def eval(self, env):
        Env.outer = env
        self.stmt_list.eval(self.env)
        print self.env


class FunctionStatement(object):

    def __init__(self, name, parms, body):
        self.name, self.body = name, body
        self.parms = parms

    def __repr__(self):
        return 'FunctionStatement(%s, %s)' % (self.name, self.body)

    def __call__(self, *args):
        return self.eval(self.body, Env(self.parms, args,))

    def eval(self, env=None):
        self.parms.eval(self.body.env)
        self.body.eval(env)


class DeclarationStatement(Statement):
    def __init__(self, name, data_type):
        self.name = name
        self.data_type = data_type

    def __repr__(self):
        return 'DeclarationStatement(%s, %s)' % (self.data_type, self.name)

    def eval(self, env):
        env[self.name] = {"TYPE": self.data_type, "VALUE": 0}


class ParameterExpression(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'ParameterExpression(%s, %s)' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)


class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.arithmeticExp = aexp

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.arithmeticExp)

    def eval(self, env):
        value = self.arithmeticExp.eval(env)
        var = env.find(self.name)[self.name]
        var['VALUE'] = self.cast(var['TYPE'], value)

    def cast(self, type, value):
        if type == 'Count':
            return int(value)
        if type == 'Real':
            return float(value)


class StatementList(Statement):
    def __init__(self, statement_list=list()):
        self.statement_list = statement_list

    def __repr__(self):
        return 'StatementList(%s)' % (self.statement_list)

    def eval(self, env):
        for statement in self.statement_list:
            statement.eval(env)


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)


class SelectionStatement(Statement):
    def __init__(self, if_stmt, elif_group, else_stmt):
        self.if_stmt = if_stmt
        self.elif_group = elif_group
        self.else_stmt = else_stmt

    def __repr__(self):
        return 'SelectionStatement(%s, %s, %s)' % (self.if_stmt, self.elif_group, self.else_stmt)

    def eval(self, env):
        if_value = self.if_stmt.eval(env)
        if if_value is None:
            if self.elif_group is not None:
                elif_val = self.elif_group.eval(env)
                if elif_val is None:
                    if self.else_stmt:
                        self.else_stmt.eval(env)
            else:
                if self.else_stmt:
                    self.else_stmt.eval(env)


class IfStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'IfStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.body.eval(env)
        else:
            None


class ElseIfList(Statement):
    def __init__(self, elif_list=list()):
        self.elif_list = elif_list

    def __repr__(self):
        return 'ElseIfList(%s)' % (self.elif_list)

    def eval(self, env):
        for elif_stmt in self.elif_list:
            if elif_stmt.eval(env) is None:
                break


class ElseIfStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'ElseIfStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.body.eval(env)
        else:
            None


class ElseStatement(Statement):
    def __init__(self, stmt):
        self.stmt = stmt

    def __repr__(self):
        return 'ElseStatement(%s)' % (self.stmt)

    def eval(self, env):
        self.stmt.eval(env)


class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.env = Env()

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        self.env.outer = env
        condition_value = self.condition.eval(self.env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(self.env)


class DoWhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'DoWhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        self.body.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)


class RealArithmeticExp(Aexp):
    def __init__(self, r):
        self.r = r

    def __repr__(self):
        return 'RealArithmeticExp(%d)' % self.r

    def eval(self, env):
        return self.r


class VariableArithmeticExp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VariableArithmeticExp(%s)' % self.name

    def eval(self, env):
        return env.find(self.name)[self.name]['VALUE']


class BinaryOpArithmeticExp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinaryOpArithmeticExp(%s, %s, %s)' % (self.op, self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value


class RelOpBooleanExp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'RelOpBooleanExp(%s, %s, %s)' % (self.op, self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value


class AndBooleanExp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBooleanExp(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value


class OrBooleanExp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBooleanExp(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value


class NotBooleanExp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBooleanExp(%s)' % self.exp

    def eval(self, env):
        value = self.exp.eval(env)
        return not value

