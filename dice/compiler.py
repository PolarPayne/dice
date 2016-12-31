from pprint import pprint
from functools import lru_cache
from copy import deepcopy

from . import operators

NUMS = "0123456789."
WHITE_SPACE = " \t"
VALID_CHARS = NUMS + WHITE_SPACE + operators.op_chars
LITERAL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
DEFAULT_OPTIONS = {
    "only_ints": False,
    "rounding_mode": "none",  # none|ceil|floor
    "defines": {},
    "errors": [],
    "dice_rolls": []
}
GLOBALS = ["defines", "errors", "dice_rolls"]


def execute(s):
    out = []
    opts = deepcopy(DEFAULT_OPTIONS)

    # our language is line orientated
    for line in s.split("\n"):
        line = line.strip()
        no_comments = []

        # only read each line up to comment
        for char in line:
            if char == "#":
                break
            no_comments.append(char)

        i = "".join(no_comments).split()
        if len(i) == 0:
            continue

        if i[0] == "set" or i[0] == "unset":
            if len(i) > 1 and (i[1] in GLOBALS or i[1] not in DEFAULT_OPTIONS):
                opts["errors"].append("{} is not a valid option to set or unset.".format(i[1]))

        if i[0] == "set":
            if len(i) == 2:
                opts[i[1]] = True
            elif len(i) == 3:
                opts[i[1]] = i[2]
            else:
                opts["errors"].append("Wrong number of arguments to set (expected 1 or 2, got {}).".format(len(i) - 1))

        elif i[0] == "unset":
            if len(i) == 2:
                opts[i[1]] = False
            else:
                opts["errors"].append("Wrong number of arguments to unset (expected 1, got {})".format(len(i) - 1))

        elif i[0] == "define":
            if len(i) == 3:
                for char in i[1]:
                    if char not in LITERAL:
                        opts["errors"].append("Invalid literal for define.")
                        break

                opts["defines"][i[1].upper()] = i[2]
            else:
                opts["errors"].append("Wrong number of arguments to define (expected 2, got {})".format(len(i) - 1))

        elif i[0] == "undefine":
            if len(i) == 3:
                for char in i[1]:
                    if char not in LITERAL:
                        opts["errors"].append("Invalid literal for define.")
            if len(i) == 2:
                del opts["defines"][i[1].upper()]
            else:
                opts["errors"].append("Wrong number of arguments to undefine (expected 1, got {})".format(len(i) - 1))

        elif i[0] == "out":
            # if there are any errors, just skip all out commands
            if len(opts["errors"]) > 0:
                continue

            line = " ".join(i[1:])
            for k, v in opts["defines"].items():
                line = line.replace(k, v)

            try:
                a = line + " = " + str(calculate(shunt(tokenize(line, opts), opts), opts))
                a += " (" + ", ".join(opts["dice_rolls"]) + ")"

                out.append(a)
            except (operators.NumberError, operators.OperatorError) as e:
                opts["errors"].append(e.args)
            opts["dice_rolls"] = []

        else:
            opts["errors"].append("{} is not a recognized command.".format(i[0]))

    return {
        "out": out,
        "errors": opts["errors"]
    }

def execute_single(s, options=None):
    opts = DEFAULT_OPTIONS.copy()
    if options is not None:
        opts.update(options)

    return calculate(shunt(tokenize(s, opts), opts), opts)


def calculate(tokens, options=None):
    if options is None:
        options = DEFAULT_OPTIONS

    out = []

    for token in tokens:
        if token.is_num():
            out.append(token.value)
        elif token.is_op():
            if token.unary:
                a = out.pop()
                out.append(token.calc(a, options))
            else:
                b, a = out.pop(), out.pop()
                out.append(token.calc(a, b, options))
        else:
            raise RuntimeError("This should never happen.")
    if len(out) == 1:
        return out[0]
    options["errors"].append("Invalid calculation ({} values were still left in the stack (which were {})).".format(len(out), out))
    return None


def shunt(tokens, options=None):
    if options is None:
        options = DEFAULT_OPTIONS

    out = []
    ops = []

    print(tokens)

    for token in tokens:
        if token.is_num():
            out.append(token)

        elif token.is_op():
            if token.is_right_bracket():
                while True:
                    top = ops.pop()
                    if top.is_left_bracket():
                        break
                    out.append(top)

            elif len(ops) == 0 or ops[-1] <= token and token.left_assoc:
                ops.append(token)
            else:
                while len(ops) > 0 and ops[-1] > token:
                    top = ops.pop()
                    if top.is_left_bracket():
                        ops.append(top)
                        break
                    out.append(top)
                ops.append(token)
        else:
            raise RuntimeError("This should never happen.")

    while len(ops) > 0:
        out.append(ops.pop())

    return tuple(out)


def tokenize(s, options=None):
    def read_num(s):
        out = ""

        for a, i in enumerate(s):
            if i in NUMS:
                out += i
            elif i in WHITE_SPACE:
                continue
            elif i in VALID_CHARS:
                break
            else:
                raise operators.NumberError("{} is not a valid character in number.".format(i))
        else:
            a = len(s)

        return operators.NumToken(out, options), s[a:]

    def read_op(out, s):
        if s[0] in operators.double_op_chars:
            if len(s) > 1 and s[0:2] in operators.ops:
                return operators.ops[s[0:2]], s[2:]

        # there is a problem in here with recogninzing possible unary
        # opearators that are before brackets

        # brackets are special, they are not really operators
        if s[0] not in "()":
            # if the last token is an operator but not a bracket
            # then this must also be a unary operator
            print("checking", s[0])
            for token in reversed(out):
                print(token)
                # if it's a number then this is not a unary operator
                if token.is_num():
                    print("is num")
                    return operators.ops[s[0]], s[1:]

                # if it's a bracket we continue
                elif token.is_bracket():
                    print("is bracket")
                    continue

                # else it's an operator, therefore this must be a unary operator
                else:
                    print("is op")
                    s = operators.binary_to_unary(s[0]) + s[1:]
                    operators.ops[s[0]], s[1:]

            s = operators.binary_to_unary(s[0]) + s[1:]

        return operators.ops[s[0]], s[1:]

    if options is None:
        options = DEFAULT_OPTIONS

    out = []

    while len(s):
        if s[0] in WHITE_SPACE:
            s = s[1:]
            continue
        elif s[0] in NUMS:
            a, s = read_num(s)
        elif s[0] in VALID_CHARS:
            a, s = read_op(out, s)
        else:
            options["errors"].append("Invalid character.")
            return tuple()

        out.append(a)

    return tuple(out)
