from pprint import pprint
from functools import lru_cache

import operators

NUMS = "0123456789."
WHITE_SPACE = " _\t"
VALID_CHARS = NUMS + WHITE_SPACE + "".join(operators.op_chars)

@lru_cache(maxsize=512)
def execute(s):
    return calculate(shunt(tokenize(s)))


@lru_cache(maxsize=512)
def calculate(tokens):
    out = []

    for token in tokens:
        if token.is_num():
            out.append(token.value)
        elif token.is_op():
            if token.unary:
                a = out.pop()
                out.append(token.calc(a))
            else:
                b, a = out.pop(), out.pop()
                out.append(token.calc(a, b))
        else:
            raise RuntimeError("This should never happen.")
    return out[0]


@lru_cache(maxsize=512)
def shunt(tokens):
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


@lru_cache(maxsize=512)
def tokenize(s):
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

        return operators.NumToken(out), s[a:]

    def read_op(out, s):
        if s[0] in operators.double_op_chars:
            if len(s) > 1:
                if s[1] == "=":
                    return operators.ops[s[0:2]], s[2:]

        if (len(out) == 0 or out[-1].is_op()):
            if s[0] in operators.binary_to_unary:
                s = operators.binary_to_unary[s[0]] + s[1:]
        
        return operators.ops[s[0]], s[1:]

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
    for i in sys.argv[1:]:
        try:
            a = tokenize(i)
            # pprint(a)
            a = shunt(a)
            # pprint(a)
            a = calculate(a)
            print(a)
        except RuntimeError as e:
            print(e)
