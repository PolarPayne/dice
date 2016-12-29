from pprint import pprint
from functools import lru_cache

import operators

NUMS = "0123456789."
WHITE_SPACE = " \t"
VALID_CHARS = NUMS + WHITE_SPACE + operators.op_chars
DEFAULT_OPTIONS = {
    "only_ints": False,
    "rounding_mode": "none"  # none|ceil|floor
}
GLOBALS = []


def execute(s):
    opts = DEFAULT_OPTIONS.copy()

    for line in map(str.lower, s.split("\n")):
        i = line.strip().split()
        if len(i) == 0:
            continue

        if i[0] == "set" or i[0] == "unset":
            if i[1] in GLOBALS or i[1] not in DEFAULT_OPTIONS:
                raise RuntimeError("{} is not a valid option to set or unset.".format(i[1]))

        if i[0] == "set":
            if len(i) == 2:
                opts[i[1]] = True
            elif len(i) == 3:
                opts[i[1]] = i[2]
            else:
                raise RuntimeError("Wrong number of arguments to set (expected 1 or 2, got {}).".format(len(i)))
        
        elif i[0] == "unset":
            if len(i) == 2:
                opts[i[1]] = False
            else:
                raise RuntimeError("Wrong number of arguments to unset (expected 1, got {})".format(len(i)))
        
        elif i[0] == "out":
            yield calculate(shunt(tokenize(" ".join(i[1:]), opts), opts), opts)

        else:
            raise RuntimeError("{} is not a recognized command.".format(i[0]))


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
    raise RuntimeError("Invalid calculation.")


def shunt(tokens, options=None):
    if options is None:
        options = DEFAULT_OPTIONS
        
    out = []
    ops = []

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
            else:
                break
        else:
            a = len(s)

        return operators.NumToken(out, options), s[a:]

    def read_op(out, s):
        if s[0] in operators.double_op_chars:
            if len(s) > 1 and s[0:2] in operators.ops:
                return operators.ops[s[0:2]], s[2:]

        if len(out) == 0 or out[-1].is_op():
            if s[0] in operators.binary_to_unary:
                s = operators.binary_to_unary[s[0]] + s[1:]

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
            raise RuntimeError("Invalid character!")

        out.append(a)

    return tuple(out)

if __name__ == "__main__":
    import sys
    s = ""
    for line in sys.stdin:
        s += line
    for i in execute(s):
        print(i)
