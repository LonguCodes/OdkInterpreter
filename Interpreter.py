import sys
import os.path
import regex
from Exceptions import LexicException, FileException
from Structures import Interpreter


def get_numbered_line(data):
    line, expected_number = data
    dot_index = line.find(".")
    number = int(line[:dot_index])
    if number != expected_number:
        raise LexicException("Line number not in order", expected_number)
    return expected_number, line[dot_index + 1:]


def execute(path):
    if not os.path.exists(path):
        raise FileException("No file on given path")
    file = open(path, 'r')
    lines = list(map(lambda x: str.replace(x, "\n", ""), file.readlines()))
    numbered_lines = dict(map(get_numbered_line, zip(lines, range(1, len(lines) + 1))))
    if regex.match("\ *end\ *", numbered_lines[len(numbered_lines)].lower()) is None:
        raise LexicException("There is no end statement", len(numbered_lines))
    interpreter = Interpreter(numbered_lines)

    return interpreter.start_execution()


def main():
    DEBUG = False
    arguments = sys.argv
    if "-d" in arguments or "--debug" in arguments:
        DEBUG = True

    path = None
    output_path = "results.txt"
    if "-f" in arguments:
        path = arguments[arguments.index("-f") + 1]

    if "--file" in arguments:
        path = arguments[arguments.index("--file") + 1]

    if "-o" in arguments:
        output_path = arguments[arguments.index("-o") + 1]

    if "--output" in arguments:
        output_path = arguments[arguments.index("--output") + 1]

    if path is None:
        print(f"Error : no file path given")
        return

    try:
        results = execute(path)
    except FileException as e:
        print(f"Error : {e.args[0]}")
        if DEBUG:
            raise e
    except LexicException as e:
        print(f"Error on line {e.args[1]} : {e.args[0]}")
        if DEBUG:
            raise e
    else:
        if DEBUG:
            print(results)
        with open(output_path, "w+") as f:
            for id, value in results.items():
                if type(value) is dict:
                    f.write(f"{id} : {list(value.values())}\n")
                else:
                    f.write(f"{id} : {value}\n")


if __name__ == '__main__':
    main()
