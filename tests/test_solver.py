from game24.solver import is_solvable, solve


def test_three_eight_eight_nine_known_solutions():
    sols = solve([3, 8, 8, 9])
    assert "3 * 8 * (9 - 8)" in sols
    assert "3 * 8 / (9 - 8)" in sols
    assert "3 * (9 - 8 / 8)" in sols


def test_one_five_five_five_requires_fraction():
    # 5 * (5 - 1/5) = 24 needs an intermediate fraction 1/5
    assert "5 * (5 - 1 / 5)" in solve([1, 5, 5, 5])


def test_unsolvable_returns_empty():
    assert solve([1, 1, 1, 1]) == []


def test_commutative_variants_are_deduplicated():
    sols = solve([3, 8, 8, 9])
    # 3*8 and 8*3 are the same solution; only the canonical form survives
    assert "8 * 3 * (9 - 8)" not in sols
    assert "3 * 8 * (9 - 8)" in sols


def test_solution_count_capped_at_twenty():
    assert len(solve([1, 2, 3, 4])) <= 20


def test_is_solvable():
    assert is_solvable([3, 8, 8, 9]) is True
    assert is_solvable([1, 1, 1, 1]) is False
