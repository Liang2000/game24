"""单人挑战游戏逻辑：关卡、计分、抽牌。"""
from dataclasses import dataclass
from datetime import datetime

from .cards import draw_hand
from .parser import ParseError, is_solution
from .solver import is_solvable

QUESTIONS_PER_LEVEL = 10
PASS_SCORE = 8

MESSAGES = {
    "correct": "你太棒了，完全正确。",
    "wrong": "很遗憾，你的算法出错！",
    "skipped": "已跳过本题。",
}


@dataclass
class Outcome:
    feedback: str  # "correct" | "wrong" | "skipped"
    level_over: bool
    passed: bool  # 仅在 level_over 为真时有意义


class ChallengeGame:
    def __init__(self, rng=None, now=None, level=1):
        self._rng = rng
        self._now = now or datetime.now
        self.level = level
        self.score = 0
        self.question_index = 0  # 0..9
        self.hand = draw_hand(self._rng)
        self._start = self._now()
        self.level_over = False
        self.passed = False

    @property
    def question_number(self):
        return self.question_index + 1

    def _advance(self, feedback):
        if self.score >= PASS_SCORE:
            self.level_over = True
            self.passed = True
            return Outcome(feedback, True, True)
        self.question_index += 1
        if self.question_index >= QUESTIONS_PER_LEVEL:
            self.level_over = True
            self.passed = False
            return Outcome(feedback, True, False)
        self.hand = draw_hand(self._rng)
        return Outcome(feedback, False, False)

    def submit(self, expression):
        if self.level_over:
            return Outcome("", True, self.passed)
        try:
            correct = is_solution(expression, self.hand)
        except ParseError:
            correct = False
        if correct:
            self.score += 1
            return self._advance("correct")
        self.score -= 1
        return self._advance("wrong")

    def declare_no_solution(self):
        if self.level_over:
            return Outcome("", True, self.passed)
        if is_solvable(self.hand):
            self.score -= 1
            return self._advance("wrong")
        self.score += 1
        return self._advance("correct")

    def skip(self):
        if self.level_over:
            return Outcome("", True, self.passed)
        return self._advance("skipped")

    def finish(self):
        """结束本关，返回成绩记录。"""
        duration = (self._now() - self._start).total_seconds()
        return {
            "timestamp": self._start.isoformat(),
            "level": self.level,
            "score": self.score,
            "passed": self.passed,
            "duration": round(duration, 1),
        }
