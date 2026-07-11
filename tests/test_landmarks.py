import numpy as np

from gesture_recognition.landmarks import normalize_landmarks


def make_hand(offset_x=0, offset_y=0, scale=1):
    """A fake 21-landmark hand: wrist at the offset, fingers spread out."""
    base = [[0, 0]] + [[i * 5, i * 3] for i in range(1, 21)]
    return [[x * scale + offset_x, y * scale + offset_y] for x, y in base]


def test_wrist_is_origin():
    result = normalize_landmarks(make_hand(offset_x=123, offset_y=456))
    assert result[0] == [0.0, 0.0]


def test_translation_invariant():
    a = normalize_landmarks(make_hand())
    b = normalize_landmarks(make_hand(offset_x=200, offset_y=100))
    np.testing.assert_allclose(a, b, atol=1e-6)


def test_scale_invariant():
    a = normalize_landmarks(make_hand())
    b = normalize_landmarks(make_hand(scale=3))
    np.testing.assert_allclose(a, b, atol=1e-6)


def test_bounded_to_unit_range():
    result = np.array(normalize_landmarks(make_hand(offset_x=999, scale=7)))
    assert np.abs(result).max() <= 1.0


def test_degenerate_all_same_point():
    # All landmarks identical: no crash, all zeros
    result = normalize_landmarks([[5, 5]] * 21)
    assert np.array(result).sum() == 0
