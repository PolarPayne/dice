from pprint import pprint


class MalformedInput(Exception):
    pass

nums = "0123456789."
ops = "dD+-*/"
valid_chars = nums + ",()[]" + ops

def calc_ast(s):
    ast = []
    while len(s) > 0:
        # print("str: \"{}\"".format(s))
        if s[0] in nums:
            a, s = read_num(s)
        elif s[0] in ops:
            a, s = read_op(s)
        elif s[0] == "(":
            a, s = read_par(s)
        elif s[0] == "[":
            a, s = read_list(s)
        else:
            raise MalformedInput("{} is not a valid character.".format(s[0]))
        ast.append(a)
        # pprint(ast)
    print(ast[-1])
    return ast


def read_num(s):
    out = ""

    for a, i in enumerate(s):
        if i in nums:
            out += i
        elif i not in valid_chars:
            raise MalformedInput("{} is not a valid character.".format(i))
        else:
            break
    else:
        a = len(s)

    try:
        # print(a, s, s[a:])
        return ("int", int(out)), s[a:]
        # return float(out) if "." in out else int(out), s[a:]
    except ValueError:
        try:
            return ("float", float(out)), s[a:]
        except ValueError:
            raise MalformedInput("{} is malformed.".format(out))


def read_op(s):
    if s[0] == "D":
        t = "dice"
    elif s[0] == "d":
        t = "dice"
    elif s[0] == "+":
        t = "plus"
    elif s[0] == "-":
        t = "minus"
    elif s[0] == "/":
        t = "div"
    elif s[0] == "*":
        t = "mul"
    else:
        raise MalformedInput("{} is not an operator.", read_op(s[0]))

    return (t, None), s[1:]


def read_par(s):
    if s[0] == "(":
        out = ""
        s = s[1:]
        c = 1
        while c > 0 and len(s):
            if s[0] == "(":
                c += 1
            elif s[0] == ")":
                c -= 1
                if c == 0:
                    break
                elif c < 0:
                    raise MalformedInput()
            out += s[0]
            s = s[1:]
        return ("par", calc_ast(out)), s[1:]

    raise MalformedInput()


def read_list(s):
    if s[0] == "[":
        out = ""
        s = s[1:]
        c = 1
        while c > 0 and len(s):
            if s[0] == "[":
                c += 1
            elif s[0] == "]":
                c -= 1
                if c == 0:
                    break
                elif c < 0:
                    raise MalformedInput()
            out += s[0]
            s = s[1:]
        out = tuple(out.split(","))
        return ("list", tuple(calc_ast(i) for i in out)), s[1:]

    raise MalformedInput()

if __name__ == "__main__":
    import sys
    for i in sys.argv[1:]:
        pprint(calc_ast(i))
    # print(dice("\n".join(sys.argv[1:])))
