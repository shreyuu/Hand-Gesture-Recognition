import json

from gesture_recognition.dataset import (
    gesture_name_from_filename,
    load_samples,
    safe_gesture_name,
)


def test_safe_gesture_name_keeps_normal_names():
    assert safe_gesture_name("  thumbs up ") == "thumbs up"
    assert safe_gesture_name("call-me_2") == "call-me_2"


def test_safe_gesture_name_strips_path_characters():
    assert "/" not in safe_gesture_name("../../etc/wave")
    assert safe_gesture_name("../../etc/wave").endswith("wave")


def test_safe_gesture_name_rejects_empty():
    assert safe_gesture_name("///") == ""


def test_simple_gesture_name():
    assert gesture_name_from_filename("index_20260709_201708.json") == "index"


def test_gesture_name_with_underscores():
    assert (
        gesture_name_from_filename("thumbs_up_20260709_201708.json") == "thumbs_up"
    )


def write_recording(tmp_path, name, samples):
    path = tmp_path / f"{name}_20260101_120000.json"
    path.write_text(json.dumps(samples))


def test_load_samples_labels_and_order(tmp_path):
    hand = [[i, i] for i in range(21)]
    write_recording(tmp_path, "wave", [hand, hand])
    write_recording(tmp_path, "fist", [hand])

    x, y, gestures = load_samples(tmp_path, normalize=False)

    # Sorted file order -> reproducible label indices
    assert gestures == ["fist", "wave"]
    assert y == [0, 1, 1]
    assert len(x) == 3
    assert x[0] == hand


def test_load_samples_normalizes(tmp_path):
    hand = [[100 + i, 200 + i] for i in range(21)]
    write_recording(tmp_path, "point", [hand])

    x, _, _ = load_samples(tmp_path, normalize=True)

    assert x[0][0] == [0.0, 0.0]  # wrist at origin
    assert max(abs(v) for pt in x[0] for v in pt) <= 1.0


def test_load_samples_ignores_non_json(tmp_path):
    (tmp_path / "notes.txt").write_text("not a recording")
    x, y, gestures = load_samples(tmp_path)
    assert (x, y, gestures) == ([], [], [])
