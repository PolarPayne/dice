from enum import Enum
from random import randint


class TokenType(Enum):
    op = 0
    int = 1
    float = 2


class Bracket(Enum):
    left = 0
    right = 1


class Token:
    def __init__(self, token_type):
        self.token_type = token_type

    def is_op(self):
        return self.token_type is TokenType.op

    def is_num(self):
        return not self.is_op()

    def is_int(self):
        return self.token_type is TokenType.int

    def is_float(self):
        return self.token_type is TokenType.float


class NumToken(Token):
    def __init__(self, value):
        try:
            self.value = int(value)
            super().__init__(TokenType.int)
        except ValueError:
            try:
                self.value = float(value)
                super().__init__(TokenType.float)
            except ValueError:
                raise RuntimeError("Badly formatted number")

    def __str__(self):
        return "{:<3} type={}".format(
            self.value,
            "int" if type(self.value) is int else "float"
        )

    def __repr__(self):
        return "<NumToken {}>".format(str(self))

    def __hash__(self):
        return hash((self.value, self.token_type))


class OpToken(Token):
    def __init__(self, oper, prec, calc, left_assoc=True, unary=False, bracket=None):
        super().__init__(TokenType.op)
        self.oper = oper
        self.prec = prec
        self.calc = calc
        self.left_assoc = left_assoc
        self.unary = unary
        self.bracket = bracket

    def is_left_bracket(self):
        return self.bracket is Bracket.left

    def is_right_bracket(self):
        return self.bracket is Bracket.right

    def __str__(self):
        return "{:<3} prec={} assoc={} unary={}".format(
            self.oper,
            self.prec,
            "left" if self.left_assoc else "right",
            self.unary
        )

    def __repr__(self):
        return "<OpToken  {}>".format(str(self))

    def __hash__(self):
        return hash((
            self.oper,
            self.prec,
            self.calc,
            self.left_assoc,
            self.unary,
            self.bracket
        ))

    def __lt__(self, value):
        if type(self) is not type(value):
            raise TypeError("Value is not of type OpToken.")
        return self.prec < value.prec

    def __ge__(self, value):
        if type(self) is not type(value):
            raise TypeError("Value is not of type OpToken.")
        return self.prec >= value.prec

ops = {
    "|": OpToken("|", 1, lambda a, b: a if a >= b else b),
    "&": OpToken("&", 2, lambda a, b: a if a < b else b),
    "==": OpToken("==", 3, lambda a, b: 1 if a == b else 0),
    "!=": OpToken("!=", 3, lambda a, b: 1 if a != b else 0),
    "<=": OpToken("<=", 4, lambda a, b: 1 if a <= b else 0),
    "<": OpToken("<", 4, lambda a, b: 1 if a < b else 0),
    ">=": OpToken(">=", 4, lambda a, b: 1 if a >= b else 0),
    ">": OpToken(">", 4, lambda a, b: 1 if a > b else 0),
    "+": OpToken("+", 5, lambda a, b: a + b),
    "-": OpToken("-", 5, lambda a, b: a - b),
    "*": OpToken("*", 6, lambda a, b: a * b),
    "/": OpToken("/", 6, lambda a, b: a / b),
    "%": OpToken("%", 6, lambda a, b: a % b),
    "^": OpToken("^", 7, lambda a, b: a ** b, left_assoc=False),
    "d": OpToken("d", 7, lambda a, b: sum([randint(1, b) for _ in range(a)]), left_assoc=False),
    "D": OpToken("D", 8, lambda b: sum([randint(1, b) for _ in range(1)]), left_assoc=False, unary=True),
    "!": OpToken("!", 8, lambda a: 1 if a == 0 else 0, unary=True),
    # unary minus
    "#": OpToken("#", 8, lambda a: -a, unary=True),
    # unary plus
    "$": OpToken("$", 8, lambda a: a, unary=True),
    "(": OpToken("(", 9, lambda a, b: None, bracket=Bracket.left),
    ")": OpToken(")", 0, lambda a, b: None, bracket=Bracket.right)
}

binary_to_unary = {
    "-": "#",
    "+": "$",
    "d": "D"
}

op_chars = "".join(set("".join(ops)))
double_op_chars = "".join(set("".join(i for i in ops if len(i) == 2)))
