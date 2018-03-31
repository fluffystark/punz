from equality import *


class Statement(Equality):
    pass


class ArithmeticExp(Equality):
    pass


class BooleanExp(Equality):
    pass


class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.arithmeticExp = aexp

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.arithmeticExp)

    def eval(self, env):
        value = self.aexp.eval(env)
        env[self.name] = value


class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)


class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt, elif_condition, elif_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt
        self.elif_condition = elif_condition
        self.elif_stmt = elif_stmt

    def __repr__(self):
        return 'IfStatement(%s, %s)ElseIfStatement(%s, %s)ElseStatement(%s)' % (self.condition,
                                                                                self.true_stmt,
                                                                                self.elif_condition,
                                                                                self.elif_stmt,
                                                                                self.false_stmt)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        elif_condition_value = self.elif_condition(env)
        if condition_value:
            self.true_stmt.eval(env)
        elif elif_condition_value:
            if self.elif_stmt:
                self.elif_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)


class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)


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


class RealArithmeticExp(ArithmeticExp):
    def __init__(self, r):
        self.r = r

    def __repr__(self):
        return 'RealArithmeticExp(%d)' % self.r

    def eval(self, env):
        return self.r


class VariableArithmeticExp(ArithmeticExp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VariableArithmeticExp(%s)' % self.name

    def eval(self, env):
        if self.name in env:
            return env[self.name]
        else:
            return 0


class BinaryOpArithmeticExp(ArithmeticExp):
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


class RelOpBooleanExp(BooleanExp):
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


class AndBooleanExp(BooleanExp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBooleanExp(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value and right_value


class OrBooleanExp(BooleanExp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBooleanExp(%s, %s)' % (self.left, self.right)

    def eval(self, env):
        left_value = self.left.eval(env)
        right_value = self.right.eval(env)
        return left_value or right_value


class NotBooleanExp(BooleanExp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBooleanExp(%s)' % self.exp

    def eval(self, env):
        value = self.exp.eval(env)
        return not value
