import pytest

pytest.importorskip("keras")

from gesture_recognition.services import gesture_manager


class FakeModel:
    output_shape = (None, 3)


@pytest.fixture
def fake_model(monkeypatch):
    monkeypatch.setattr(gesture_manager, "load_model", lambda path: FakeModel())


def test_names_file_must_match_model_outputs(tmp_path, fake_model):
    names = tmp_path / "names.txt"
    names.write_text("fist\npeace\n")  # model predicts 3 classes

    with pytest.raises(ValueError, match="2 gestures"):
        gesture_manager.GestureManager("model", str(names))


def test_matching_names_file_loads(tmp_path, fake_model):
    names = tmp_path / "names.txt"
    names.write_text("fist\npeace\nwave\n")

    manager = gesture_manager.GestureManager("model", str(names))

    assert manager.class_names == ["fist", "peace", "wave"]
