import os
import pytest
import yaml
import dice


def files_in_dir(path):
    def g(path):
        return (os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)))

    for p in g(path):
        with open(p, "r") as f:
            yield f


def pytest_generate_tests(metafunc):
    def parse_results(expression_ok):
        def get_values(key):
            value = expression_ok[key]

            if type(value) is str:
                return [dice.execute_expression(value)]
            elif type(value) in (int, float):
                return [value]
            elif type(value) is list:
                results = set()
                for result in value:
                    if type(result) in (int, float):
                        results.add(result)
                    else:
                        raise Exception()
                return results
            else:
                raise Exception()

        for i in ("r", "result", "results"):
            if i in expression_ok:
                return get_values(i)
        raise Exception()

    def parse_expressions(expression_ok):
        def get_values(key):
            value = expression_ok[key]

            if type(value) is str:
                return [value]
            elif type(value) is list:
                expressions = []
                for expression in value:
                    if type(expression) is str:
                        expressions.append(expression)
                    else:
                        raise Exception()
                return expressions
            else:
                raise Exception()

        for i in ("e", "expression", "expressions"):
            if i in expression_ok:
                return get_values(i)
        raise Exception()

    expression_ok = []
    for f in files_in_dir(os.path.join("dice", "tests", "expression_ok")):
        for test in yaml.load(f):
            expressions = parse_expressions(test)
            results = parse_results(test)

            for i in expressions:
                expression_ok.append((i, results))
    metafunc.parametrize(("expression_ok", "results"), expression_ok)


# def test_execute_error(execute_error, results):
#     pass


# def test_execute_warning(execute_warning, results):
#     pass


# def test_execute_ok(execute_ok, results):
#     pass


# def test_expression_error(expression_error, results):
#     pass


def test_expression_ok(expression_ok, results):
    if len(results) == 1:
        assert dice.execute_expression(expression_ok) in results
    elif len(results) > 1:
        hits = set()
        tries = 0
        for _ in range(2**16):
            res = dice.execute_expression(expression_ok)
            assert res in results
            hits.add(res)
        assert len(hits) == len(results)
    else:
        raise Exception()
