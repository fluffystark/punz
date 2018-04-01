from equality import *
from predef_func import *


class Statement(Equality):
    pass


class Aexp(Equality):
    pass


class Bexp(Equality):
    pass


class Env(dict):
    def __init__(self, outer=None, stmt_list=list(), funcdict=dict()):
        self.outer = outer
        self.stmt_list = stmt_list
        self.funcdict = funcdict

    def find(self, var):
        return self if (var in self) else self.outer.find(var)


class BlockStatement(Statement):
    def __init__(self, stmt_list, return_stmt):
        self.stmt_list = stmt_list
        self.return_stmt = return_stmt
        self.env = Env()

    def __repr__(self):
        return 'BlockStatement(%s, %s)' % (self.stmt_list, self.env)

    def eval(self, env):
        self.env.outer = env
        self.stmt_list.eval(self.env)
        if self.return_stmt is not None:
            self.return_stmt.eval(env)


class FunctionDict(Statement):
    def __init__(self, function_list=list()):
        self.function_list = function_list

    def __repr__(self):
        return 'FunctionDict(%s)' % (self.function_list)

    def eval(self, env):
        for function in self.function_list:
            env.funcdict[function.name] = function
        env.funcdict['main'].eval(env)


class FunctionCall(Statement):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return 'FunctionCall(%s, %s\n)' % (self.name, self.args)

    def eval(self, env=Env()):
        var = env.funcdict[self.name]
        arg_list = self.appendlist(self.args.eval(env))
        return var(arg_list)

    def appendlist(self, x=list()):
        ret = list()
        if type(x) is list:
            for i in x:
                if type(i) is list:
                    ret = self.appendlist(i)
                else:
                    ret.append(i)
        else:
            ret.append(x)
        return ret


class ReturnStatement(Statement):
    def __init__(self, ret):
        self.ret = ret

    def __repr__(self):
        return 'ReturnStatement(%s)' % (self.ret)

    def eval(self, env=None):
        print type(self.ret)
        if type(self.ret) is int:
            pass
        elif type(self.ret) is not str:
            self.ret = self.ret.eval(env)

        env['return']['VALUE'] = self.ret


class FunctionStatement(object):
    def __init__(self, name, parms, body):
        self.name, self.body = name, body
        self.parms = parms
        self.body.env['return'] = {"TYPE": 'Real', "VALUE": 0}

    def __repr__(self):
        return 'FunctionStatement(%s, %s\n)' % (self.name, self.body)

    def __call__(self, args):
        params = self.appendlist(self.parms.eval(self.body.env))
        for parm, arg in zip(params, args):
            var = self.body.env.find(parm)[parm]
            var['VALUE'] = self.cast(var['TYPE'], arg)
        self.body.eval(self.body.env)
        return self.body.env['return']['VALUE']

    def eval(self, env=Env()):
        self.parms.eval(self.body.env)
        self.body.eval(self.body.env)
        print self.body.env

    def appendlist(self, x=list()):
        ret = list()
        for i in x:
            if type(i) is list:
                ret = self.appendlist(i)
            else:
                ret.append(i)
        return ret

    def cast(self, type, value):
        if type == 'Count':
            return int(value)
        if type == 'Real':
            return float(value)


class DeclarationStatement(Statement):
    def __init__(self, name, data_type):
        self.name = name
        self.data_type = data_type

    def __repr__(self):
        return 'DeclarationStatement(%s, %s)' % (self.data_type, self.name)

    def eval(self, env):
        env[self.name] = {"TYPE": self.data_type, "VALUE": 0}
        return self.name


class ArguementExpression(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'ArguementExpression(%s, %s)\n' % (self.first, self.second)

    def eval(self, env):
        return [self.first.eval(env), self.second.eval(env)]


class ParameterExpression(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'ParameterExpression(%s, %s)\n' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)


class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.arithmeticExp = aexp

    def __repr__(self):
        return 'AssignStatement(%s, %s)\n' % (self.name, self.arithmeticExp)

    def eval(self, env):
        if type(self.name) is not str:
            self.name = self.name.eval(env)
        value = self.arithmeticExp.eval(env)
        var = env.find(self.name)
        var[self.name]['VALUE'] = self.cast(var[self.name]['TYPE'], value)

    def cast(self, data_type, value):
        if data_type == 'Count':
            return int(value)
        if data_type == 'Real':
            return float(value)


class StatementList(Statement):
    def __init__(self, statement_list=list()):
        self.statement_list = statement_list

    def __repr__(self):
        return 'StatementList(%s)\n' % (self.statement_list)

    def eval(self, env):
        for statement in self.statement_list:
            statement.eval(env)


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)\n' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)


class SelectionStatement(Statement):
    def __init__(self, if_stmt, elif_group, else_stmt):
        self.if_stmt = if_stmt
        self.elif_group = elif_group
        self.else_stmt = else_stmt

    def __repr__(self):
        return 'SelectionStatement(%s, %s, %s)\n' % (self.if_stmt, self.elif_group, self.else_stmt)

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
        return 'WhileStatement(%s, %s)\n' % (self.condition, self.body)

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
        return 'DoWhileStatement(%s, %s)\n' % (self.condition, self.body)

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
        return 'BinaryOpArithmeticExp(%s, %s, %s)\n' % (self.op, self.left, self.right)

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


class Set(Statement):
    def __init__(self, variable, size, data_type):
        self.name = variable
        self.size = size
        self.data_type = data_type

    def __repr__(self):
        return 'Set(%s %s %s)' % (self.name, self.size, self.data_type)

    def eval(self, env):
        env[self.name] = {"TYPE": self.data_type, "VALUE": list()}
        i = 0
        while(i < self.size.eval(env)):
            env[self.name]['VALUE'].append(0)
            i += 1
        return self.name
