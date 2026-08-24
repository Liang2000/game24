import random

from game24.cards import draw_hand, face_name


def test_face_name_mapping():
    assert face_name(1) == "A"
    assert face_name(11) == "J"
    assert face_name(12) == "Q"
    assert face_name(13) == "K"
    assert face_name(5) == "5"


def test_draw_hand_four_values_in_range():
    hand = draw_hand(random.Random(0))
    assert len(hand) == 4
    assert all(1 <= v <= 13 for v in hand)
