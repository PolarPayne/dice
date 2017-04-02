from hypothesis import given, assume
from hypothesis.strategies import integers, random_module
from dice import execute_expression

MAX_DICE = 10**3


@given(random_module(), integers(min_value=1))
def test_dN(r, n):
    assert 1 <= execute_expression("d{}".format(n)) <= n

@given(random_module(), integers(min_value=0, max_value=MAX_DICE))
def test_Nd1(r, n):
    assert execute_expression("{}d1".format(n)) == n


@given(
    random_module(),
    integers(min_value=0, max_value=MAX_DICE),
    integers(min_value=1)
)
def test_NdX(r, n, x):
    assert n <= execute_expression("{}d{}".format(n, x)) <= n*x
