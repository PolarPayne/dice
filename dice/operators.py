from enum import Enum
from random import randint
from math import ceil, floor


class NumberError(Exception):
    pass


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
    def __init__(self, value, options):
        try:
            self.value = int(value)
            super().__init__(TokenType.int)
        except ValueError:
            try:
                if options["rounding_mode"] == "ceil":
                    self.value = ceil(float(value))
                    super().__init__(TokenType.int)
                elif options["rounding_mode"] == "floor":
                    self.value = floor(float(value))
                    super().__init__(TokenType.int)
                elif options["rounding_mode"] == "none":
                    self.value = float(value)
                    super().__init__(TokenType.float)
                    
                    if options["only_ints"]:
                        raise NumberError("Non-integer encountered in only_ints mode.")
                else:
                    raise NumberError("Invalid rounding mode option.")

            except ValueError:
                raise NumberError("Badly formatted number")

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

    def is_bracket(self):
        return self.is_left_bracket() or self.is_right_bracket()

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


def op_or(a, b, options):
    return a if a != 0 else b


def op_and(a, b, options):
    return a if a == 0 else b


def op_eq(a, b, options):
    return 1 if a == b else 0


def op_neq(a, b, options):
    return 1 if a != b else 0


def op_le(a, b, options):
    return 1 if a <= b else 0


def op_lt(a, b, options):
    return 1 if a < b else 0


def op_ge(a, b, options):
    return 1 if a >= b else 0


def op_gt(a, b, options):
    return 1 if a > b else 0


def op_add(a, b, options):
    return a + b


def op_sub(a, b, options):
    return a - b


def op_mul(a, b, options):
    return a * b


def op_div(a, b, options):
    if options["only_ints"]:
        return a // b
    return a / b


def op_mod(a, b, options):
    return a & b


def op_pow(a, b, options):
    return a ** b


def op_dice(a, b, options):
    if type(a) is int:
        return sum(op_udice(b, options) for _ in range(a))
    options["errors"].append("Dice operator requires ints.")


def op_udice(a, options):
    if type(a) is int:
        res = randint(1, a)
        options["dice_rolls"].append("d{} = {}".format(a, res))
        return res
    options["options"].append("Dice operator requires ints.")


def op_not(a, options):
    return 1 if a == 0 else 0


def op_usub(a, options):
    return -a


def op_id(a, options):
    return a


def op_brackets(*args):
    raise RuntimeError("Brackets are not operators!")

ops = {
    "|":  OpToken("|",  1, op_or                                 ),
    "&":  OpToken("&",  2, op_and                                ),
    "==": OpToken("==", 3, op_eq                                 ),
    "!=": OpToken("!=", 3, op_neq                                ),
    "<=": OpToken("<=", 4, op_le                                 ),
    "<":  OpToken("<",  4, op_lt                                 ),
    ">=": OpToken(">=", 4, op_ge                                 ),
    ">":  OpToken(">",  4, op_gt                                 ),
    "+":  OpToken("+",  5, op_add                                ),
    "-":  OpToken("-",  5, op_sub                                ),
    "*":  OpToken("*",  6, op_mul                                ),
    "/":  OpToken("/",  6, op_div                                ),
    "%":  OpToken("%",  6, op_mod                                ),
    "^":  OpToken("^",  7, op_pow,   left_assoc=False            ),
    "d":  OpToken("d",  7, op_dice,  left_assoc=False            ),
    "D":  OpToken("D",  8, op_udice, left_assoc=False, unary=True),
    "!":  OpToken("!",  8, op_not,                     unary=True),
    # unary minus
    "#":  OpToken("#",  8, op_usub,                    unary=True),
    # unary plus
    "$":  OpToken("$",  8, op_id,                      unary=True),

    "(":  OpToken("(",  9, op_brackets, bracket=Bracket.left     ),
    ")":  OpToken(")",  0, op_brackets, bracket=Bracket.right    )
}

binary_to_unary = {
    "-": "#",
    "+": "$",
    "d": "D"
}

op_chars = "|&=<>+-*/%^d()"
double_op_chars = "".join(set("".join(i for i in ops if len(i) == 2)))
