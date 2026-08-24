from game24.challenge import QUESTIONS_PER_LEVEL, ChallengeGame


def _game():
    g = ChallengeGame()
    g.hand = [3, 8, 8, 9]
    return g


def test_correct_answer_scores_and_advances():
    g = _game()
    out = g.submit("3*8*(9-8)")
    assert out.feedback == "correct"
    assert out.level_over is False
    assert g.score == 1
    assert g.question_number == 2


def test_wrong_answer_decrements():
    g = _game()
    out = g.submit("3*8*(9-7)")
    assert out.feedback == "wrong"
    assert g.score == -1


def test_invalid_expression_is_wrong():
    g = _game()
    out = g.submit("abc")
    assert out.feedback == "wrong"
    assert g.score == -1


def test_declare_no_solution_when_unsolvable():
    g = _game()
    g.hand = [1, 1, 1, 1]
    out = g.declare_no_solution()
    assert out.feedback == "correct"
    assert g.score == 1


def test_declare_no_solution_when_solvable_is_wrong():
    g = _game()  # [3,8,8,9] 有解
    out = g.declare_no_solution()
    assert out.feedback == "wrong"
    assert g.score == -1


def test_skip_scores_zero_and_advances():
    g = _game()
    out = g.skip()
    assert out.feedback == "skipped"
    assert g.score == 0
    assert g.question_number == 2


def test_reaching_eight_passes_level_immediately():
    g = _game()
    g.score = 7
    out = g.submit("3*8*(9-8)")
    assert out.feedback == "correct"
    assert out.level_over is True
    assert out.passed is True


def test_score_can_go_negative():
    g = _game()
    g.submit("3*8*(9-7)")
    assert g.score == -1


def test_fails_after_ten_questions_below_eight():
    g = _game()
    g.question_index = QUESTIONS_PER_LEVEL - 1  # 最后一题
    g.score = 5
    out = g.submit("3*8*(9-7)")  # 错误 → score 4
    assert out.level_over is True
    assert out.passed is False


def test_finish_returns_record():
    g = _game()
    g.score = 9
    g.passed = True
    rec = g.finish()
    assert rec["level"] == 1
    assert rec["score"] == 9
    assert rec["passed"] is True
    assert isinstance(rec["timestamp"], str)
    assert rec["duration"] >= 0
