import sys
import os.path
from _operator import add, sub, mul, eq, lt, le, gt, ge, ne
from math import sin, cos, pi, tau
import regex
from Exceptions import LexicException, FileException


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
    "=": eq,
    "<": lt,
    ">": gt,
    "<=": le,
    ">=": ge,
    "!=": ne,
    "=!": ne
}
consts = {
    'pi': pi,
    'tau': tau
}


def get_numbered_line(data):
    line, expected_number = data
    dot_index = line.find(".")
    number = int(line[:dot_index])
    if number != expected_number:
        raise LexicException("Line number not in order", expected_number)
    return expected_number, line[dot_index + 1:]


class Interpreter:
    def __init__(self, numbered_lines):
        self.lines = numbered_lines
        self.state = {}
        self.current_line = 1

    def get_value(self, identifier):
        try:
            return int(identifier)
        except:
            try:
                return float(identifier)
            except:
                if identifier in consts:
                    return consts[identifier]
                if identifier in self.state:
                    return self.state[identifier]
                raise LexicException(f"Unknown identifier: {identifier}", self.current_line)

    def start_execution(self):
        while self.current_line < len(self.lines):
            if self.execute_expression(self.lines[self.current_line]):
                self.current_line += 1

    def evaluate_expression(self, expression):
        for fun in single_functions:
            rx = regex.search(rf"{fun}\ *([^\ ]*)\ *", expression)
            if rx is not None:
                identifier = rx.groups()[0]
                value = self.get_value(identifier)
                return single_functions[fun](value)

        for fun in double_functions:
            rx = regex.search(rf"\ *([^\ ]*)\ *\{fun}\ *([^\ ]*$)\ *", expression)
            if rx is not None:
                ident1, ident2 = rx.groups()
                value1 = self.get_value(ident1)
                value2 = self.get_value(ident2)

                return double_functions[fun](value1, value2)

        rx = regex.search(r"^ *([^ ]*) *$", expression)

        if rx is not None:
            identifier = rx.groups()[0]
            value = self.get_value(identifier)
            return value
        raise LexicException("Incorrect syntax", self.current_line)

    def check_assign(self, line):
        rx = regex.search(r"^ *([^ ]*) *<- *(.*) *$", line)
        if rx is None:
            return True
        identifier, expression = rx.groups()
        self.state[identifier] = self.evaluate_expression(expression)
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


def execute(path):
    if not os.path.exists(path):
        raise FileException("No file on given path")
    file = open(path, 'r')
    lines = list(map(lambda x: str.replace(x, "\n", ""), file.readlines()))
    numbered_lines = dict(map(get_numbered_line, zip(lines, range(1, len(lines) + 1))))

    interpreter = Interpreter(numbered_lines)
    interpreter.start_execution()

    for id, value in interpreter.state.items():
        print(f"{id} : {value}")


DEBUG = False


def main():
    arguments = sys.argv
    if "-d" in arguments or "--debug" in arguments:
        DEBUG = True

    path = None

    if "-f" in arguments:
        path = arguments[arguments.index("-f") + 1]

    if "--file" in arguments:
        path = arguments[arguments.index("--file") + 1]

    if path is None:
        print(f"Error : no file path given")
        return

    try:
        execute(path)
    except FileException as e:
        print(f"Error : {e.args[0]}")
        if DEBUG:
            raise e
    except LexicException as e:
        print(f"Error on line {e.args[1]} : {e.args[0]}")
        if DEBUG:
            raise e


if __name__ == '__main__':
    main()
