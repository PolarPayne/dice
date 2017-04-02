from hypothesis import given, assume
from hypothesis.strategies import floats
from dice import execute_expression

FORMAT_PRECISION = 9
ALMOST_EQUAL_PRECISION = 6
f = floats(
    min_value=-10**(FORMAT_PRECISION),
    max_value=10**(FORMAT_PRECISION),
    allow_nan=False,
    allow_infinity=False
)


def almost_equal(a, b, prec=ALMOST_EQUAL_PRECISION):
    return abs(execute_expression(a)-execute_expression(b)) < 1*10**-prec


@given(f, f, f)
def test_distributive(a, b, c):
    assume(-10**FORMAT_PRECISION < a*(b+c) < 10**FORMAT_PRECISION)
    exprs = list(map(lambda s: s.format(a=a, b=b, c=c, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}*({b:.{prec}f}+{c:.{prec}f})",  # a*(b+c)
        "{a:.{prec}f}*{b:.{prec}f}+{a:.{prec}f}*{c:.{prec}f}"  # a*b+a*c
    ]))

    assert almost_equal(exprs[0], exprs[1])


@given(f, f)
def test_commutativity_addition(a, b):
    exprs = list(map(lambda s: s.format(a=a, b=b, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}+{b:.{prec}f}",  # a+b
        "{b:.{prec}f}+{a:.{prec}f}"  # b+a
    ]))

    assert almost_equal(exprs[0], exprs[1])


@given(f, f)
def test_commutativity_multiplication(a, b):
    exprs = list(map(lambda s: s.format(a=a, b=b, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}*{b:.{prec}f}",  # a*b
        "{b:.{prec}f}*{a:.{prec}f}"  # b*a
    ]))

    assert almost_equal(exprs[0], exprs[1])


@given(f, f, f)
def test_associativity_addition(a, b, c):
    exprs = list(map(lambda s: s.format(a=a, b=b, c=c, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}+({b:.{prec}f}+{c:.{prec}f})",  # a+(b+c)
        "({a:.{prec}f}+{b:.{prec}f})+{c:.{prec}f}"  # (a+b)+c
    ]))

    assert almost_equal(exprs[0], exprs[1])


@given(f, f, f)
def test_associativity_multiplication(a, b, c):
    assume(-10**FORMAT_PRECISION < a*b*c < 10**FORMAT_PRECISION)
    exprs = list(map(lambda s: s.format(a=a, b=b, c=c, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}*({b:.{prec}f}*{c:.{prec}f})",  # a*(b*c)
        "({a:.{prec}f}*{b:.{prec}f})*{c:.{prec}f}"  # (a*b)*c
    ]))

    assert almost_equal(exprs[0], exprs[1])


@given(f)
def test_identity_addition(a):
    exprs = list(map(lambda s: s.format(a=a, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}+0",  # a+0
        "{a:.{prec}f}"  # a
    ]))

    assert almost_equal(exprs[0], exprs[1])


@given(f)
def test_identity_multiplication(a):
    exprs = list(map(lambda s: s.format(a=a, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}*1",  # a*1
        "{a:.{prec}f}"  # a
    ]))

    assert almost_equal(exprs[0], exprs[1])


@given(f)
def test_additive_inversion(a):
    exprs = list(map(lambda s: s.format(a=a, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}+(-{a:.{prec}f})",  # a+(-a)
        "0"  # 0
    ]))

    assert almost_equal(exprs[0], exprs[1])


@given(f)
def test_multiplicative_inversion(a):
    assume(float("{:.{prec}f}".format(a, prec=FORMAT_PRECISION)) != 0)
    exprs = list(map(lambda s: s.format(a=a, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}*(1/{a:.{prec}f})",  # a*(1/a)
        "1"  # 1
    ]))

    assert almost_equal(exprs[0], exprs[1])


@given(f)
def test_zero_multiplication(a):
    exprs = list(map(lambda s: s.format(a=a, prec=FORMAT_PRECISION), [
        "{a:.{prec}f}*0",  # a*0
        "0"  # 0
    ]))

    assert almost_equal(exprs[0], exprs[1])