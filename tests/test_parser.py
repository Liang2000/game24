import pytest

from game24.parser import ParseError, evaluate, is_solution


def test_plain_expression_evaluates():
    assert evaluate("3*8*(9-8)") == 24


def test_is_solution_accepts_correct_answer():
    assert is_solution("3*8*(9-8)", [3, 8, 8, 9]) is True


def test_fullwidth_and_division_symbols():
    assert evaluate("3×8÷(9−8)") == 24
    assert is_solution("３＊８＊（９－８）", [3, 8, 8, 9]) is True


def test_rejects_number_not_in_hand():
    assert is_solution("3*8*(9-7)", [3, 8, 8, 9]) is False


def test_rejects_wrong_count():
    # 只用了 3 个数，缺一个 8
    assert is_solution("3*8*9", [3, 8, 8, 9]) is False


def test_divide_by_zero_raises():
    with pytest.raises(ParseError):
        evaluate("3*8/(9-9)")


@pytest.mark.parametrize("bad", ["", "3**8", "3*", "abc", "3++4", "3 8"])
def test_illegal_syntax_raises(bad):
    with pytest.raises(ParseError):
        evaluate(bad)
