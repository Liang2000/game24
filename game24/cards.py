"""牌面与抽牌。"""
import random

SUITS = ("♠", "♥", "♣", "♦")

_FACE = {1: "A", 11: "J", 12: "Q", 13: "K"}


def face_name(value):
    """牌面数值 → 牌面名称（A/J/Q/K）。"""
    return _FACE.get(value, str(value))


def draw_hand(rng=None):
    """随机抽取 4 张牌的数值（1–13）。"""
    rng = rng if rng is not None else random
    return [rng.randint(1, 13) for _ in range(4)]
