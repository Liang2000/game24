from game24.hint import HintModel
from game24.ui.hint_window import hint_message


def test_pick_fills_first_empty_in_order():
    m = HintModel()
    assert m.pick(3) is True
    assert m.pick(8) is True
    assert m.selected == [3, 8, None, None]


def test_pick_when_full_is_rejected():
    m = HintModel()
    for v in (1, 2, 3, 4):
        m.pick(v)
    assert m.is_full() is True
    assert m.pick(5) is False
    assert m.selected == [1, 2, 3, 4]


def test_clear_slot_then_refill():
    m = HintModel()
    m.pick(3)
    m.pick(8)
    m.clear(0)
    assert m.selected == [None, 8, None, None]
    m.pick(9)
    assert m.selected == [9, 8, None, None]


def test_duplicates_allowed():
    m = HintModel()
    for _ in range(4):
        assert m.pick(8) is True
    assert m.selected == [8, 8, 8, 8]


def test_numbers_and_full():
    m = HintModel()
    m.pick(3)
    m.pick(8)
    assert m.numbers() == [3, 8]
    assert m.is_full() is False


def test_solve_requires_full():
    m = HintModel()
    m.pick(3)
    assert m.solve() == []
    m.pick(8)
    m.pick(8)
    m.pick(9)
    sols = m.solve()
    assert "3 * 8 * (9 - 8)" in sols


def test_hint_message_when_not_full():
    m = HintModel()
    m.pick(3)
    assert hint_message(m) == "请先选择 4 个数字。"


def test_hint_message_when_full_unsolvable():
    m = HintModel()
    for v in (3, 4, 10, 11):  # J = 11，无解
        m.pick(v)
    assert m.is_full() is True
    assert hint_message(m) == "这组数字无解。"


def test_hint_message_when_solvable():
    m = HintModel()
    for v in (3, 8, 8, 9):
        m.pick(v)
    msg = hint_message(m)
    assert "解法" in msg
    assert "3 * 8 * (9 - 8) = 24" in msg


def test_clear_all_clears_every_slot():
    m = HintModel()
    for v in (3, 4, 10, 11):
        m.pick(v)
    assert m.is_full() is True
    m.clear_all()
    assert m.selected == [None, None, None, None]
    assert m.is_full() is False


def test_clear_all_on_partial_selection():
    m = HintModel()
    m.pick(3)
    m.pick(8)
    m.clear_all()
    assert m.selected == [None, None, None, None]
