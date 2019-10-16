from _operator import add, sub, mul, eq, lt, le, gt, ge, ne
from math import sin, cos, pi, tau

from Exceptions import LexicException

import regex


def idiv(a, b):
    return int(a / b)


single_functions = {
    "sin": sin,
    "cos": cos
}
double_functions = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": idiv,
    "<=": le,
    ">=": ge,
    "!=": ne,
    "=!": ne,
    "=": eq,
    "<": lt,
    ">": gt,

}
consts = {
    'pi': pi,
    'tau': tau
}


class Interpreter:
    def __init__(self, numbered_lines):
        self.lines = numbered_lines
        self._state = {}
        self.current_line = 1

    def __getitem__(self, item):
        if item not in self._state:
            raise Exception("State with that identifier does not exist")
        return self._state[item]

    def __setitem__(self, key, value):
        self._state[key] = value

    def __contains__(self, item):
        return item in self._state

    def get_list_value(self, li, id):
        if id in self[li]:
            return self[li][id]
        return None

    def try_get_list(self, id):
        for i in range(1, len(id)):
            if id[:i] in self and type(self[id[:i]]) is dict:
                lst = id[:i]
                value = self.get_value(id[i:], False)
                return lst, value
        return None

    def set_value(self, identifier, value):
        is_list = self.try_get_list(identifier)
        if is_list is not None:
            self[is_list[0]][is_list[1]] = value
        else:
            self[identifier] = value

    def get_value(self, identifier, can_recure=True):
        try:
            return int(identifier)
        except:
            try:
                return float(identifier)
            except:
                value = self.try_get_list(identifier)
                if value is not None:
                    return self.get_list_value(value[0], value[1])
                if identifier in consts:
                    return consts[identifier]
                if identifier in self:
                    return self[identifier]

                if can_recure:
                    return self.evaluate_expression(identifier)
                raise LexicException(f"Unknown identifier {identifier}", self.current_line)

    def start_execution(self):
        while self.current_line < len(self.lines):
            if self.execute_expression(self.lines[self.current_line]):
                self.current_line += 1
        return self._state

    def evaluate_expression(self, expression):
        for fun in double_functions:

            rx = regex.search(rf"\ *(.*)\ *\{fun}\ *(.*)\ *", expression)

            if rx is not None:
                ident1, ident2 = rx.groups()
                value1 = self.get_value(ident1)
                value2 = self.get_value(ident2)

                return double_functions[fun](value1, value2)

        for fun in single_functions:
            rx = regex.search(rf"{fun}\ *(.*)\ *", expression)
            if rx is not None:
                identifier = rx.groups()[0]
                value = self.get_value(identifier)
                return single_functions[fun](value)
        if regex.match(r"^ *\[ *(\ *\d*\ *\,)* *\d* *\] *$", expression) is not None:
            groups = regex.findall(r"\ *\d+\ *", expression)
            v = dict(zip(range(len(groups)), [self.get_value(g.replace(",", ""), False) for g in groups]))
            return v

        rx = regex.search(r"^ *([^ ]*) *$", expression)

        if rx is not None:
            identifier = rx.groups()[0]
            value = self.get_value(identifier, False)
            return value
        raise LexicException("Incorrect syntax", self.current_line)

    def check_assign(self, line):
        rx = regex.search(r"^ *([^ ]*) *<- *(.*) *$", line)
        if rx is None:
            return True
        identifier, expression = rx.groups()
        self.set_value(identifier, self.evaluate_expression(expression))
        return False

    def check_if(self, expression):
        rx = regex.search(r"^ *if *\((.*)\) *(.*) *$", expression)
        if rx is None:
            return True
        condition, next_expression = rx.groups()
        if self.evaluate_expression(condition):
            self.execute_expression(next_expression, False)
        return False

    def check_goto(self, expression):
        rx = regex.search(r"^ *goto *([0-9]*) *$", expression)
        if rx is None:
            return True
        try:
            line_number = int(rx.groups()[0])
        except:
            raise LexicException("Invalid goto line number", self.current_line)
        if line_number not in self.lines:
            raise LexicException("Invalid goto line number", self.current_line)
        self.current_line = line_number
        return False

    def execute_expression(self, expression, can_if=True):
        if not self.check_assign(expression):
            return True
        if can_if and not self.check_if(expression):
            return True
        if not self.check_goto(expression):
            return False
        raise LexicException("Incorrect syntax", self.current_line)
