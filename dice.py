from pprint import pprint
from functools import lru_cache
from collections import namedtuple

NUMS = "0123456789."
WHITE_SPACE = " \t"
VALID_CHARS = NUMS + WHITE_SPACE + "()[],dD^*/+-"


class CompileError(Exception):
    pass


class ExceptionFactory:
    def __init__(self, s):
        self.s = s
        self.l = 0

    def inc(self, l):
        self.l = len(self.s) - len(l)

    def __call__(self, msg, ex_len=0):
        return CompileError(("{}\n" + " " * self.l + "^" + "~" * ex_len + " {}").format(
            self.s,
            msg
        ))


def execute(ops):
    pass


def shunt(ops):
    pass


@lru_cache(maxsize=512)
def to_tokens(s):
    def pre_parse(s):
        return s.replace(",", "),(").replace("[", "[(").replace("]", ")]")

    def read_num(s):
        out = ""

        for a, i in enumerate(s):
            if i in NUMS:
                out += i
            elif i not in VALID_CHARS:
                raise RuntimeError("Invalid character in number.")
            else:
                break
        else:
            a = len(s)

        try:
            return ("int", int(out)), s[a:]
        except ValueError:
            try:
                return ("float", float(out)), s[a:]
            except ValueError:
                raise RuntimeError("Badly formatted number")

    def read_dice(s):
        out = []
        if s[0] in "dD":
            out.append(("dice", None))
            s = s[1:]

        if s[0] in NUMS:
            a, s = read_num(s)
            if a[0] == "int":
                a = "[" + ",".join(str(i) for i in range(1, a[1]+1)) + "]"
                for i in to_tokens(a):
                    for j in i:
                        out.append(j)
            else:
                raise RuntimeError("Dice can't have non integer sides")
        elif s[0] == "[" or s[0] == "(" or s[0] in WHITE_SPACE:
            pass
            # a, s = to_tokens(s)
        else:
            raise RuntimeError("Invalid value for dice operator")

        return out, s

    out = []
    s = pre_parse(s)

    while len(s):
        # print(s)
        if s[0] in NUMS:
            a, s = read_num(s)
        elif s[0] == "(":
            a, s = ("l_paren", None), s[1:]
        elif s[0] == ")":
            a, s = ("r_paren", None), s[1:]
        elif s[0] == "[":
            a, s = ("l_brack", None), s[1:]
        elif s[0] == "]":
            a, s = ("r_brack", None), s[1:]
        elif s[0] == ",":
            a, s = ("comma", None), s[1:]
        elif s[0] in "dD":
            a, s = read_dice(s)
            # a, s = ("dice", None), s[1:]
        elif s[0] == "^":
            a, s = ("exp", None), s[1:]
        elif s[0] == "*":
            a, s = ("mult", None), s[1:]
        elif s[0] == "/":
            a, s = ("div", None), s[1:]
        elif s[0] == "+":
            a, s = ("plus", None), s[1:]
        elif s[0] == "-":
            a, s = ("minus", None), s[1:]
        elif s[0] in WHITE_SPACE:
            s = s[1:]
        else:
            return a, s
        # print(s, a, out)

        if type(a) is tuple:
            out.append(a)
        elif type(a) is list:
            for i in a:
                out.append(i)
        else:
            raise RuntimeError("a is of wrong type, was {} but expected tuple or list".format(type(a)))

    return out, s

if __name__ == "__main__":
    import sys
    for i in sys.argv[1:]:
        try:
            a, s = to_tokens(i)
        except CompileError as e:
            print(e)
        pprint(a)

