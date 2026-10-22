import json

import pytest

pytest.importorskip("tensorflow")

from gesture_recognition.trainer import GestureTrainer

HAND = [[i, i * 2] for i in range(21)]


def write_recording(data_dir, name, samples):
    (data_dir / f"{name}_20260101_120000.json").write_text(json.dumps(samples))


def make_trainer(tmp_path):
    return GestureTrainer(data_dir=str(tmp_path), model_path=str(tmp_path / "model"))


def test_refuses_to_train_on_a_single_gesture(tmp_path, monkeypatch, capsys):
    write_recording(tmp_path, "wave", [HAND] * 5)
    trainer = make_trainer(tmp_path)
    monkeypatch.setattr(trainer, "build_model", lambda: pytest.fail("trained anyway"))

    assert trainer.train(epochs=1) is False
    assert "at least two" in capsys.readouterr().out


def test_labels_have_a_column_for_every_gesture(tmp_path):
    write_recording(tmp_path, "fist", [HAND] * 2)
    write_recording(tmp_path, "peace", [HAND] * 2)
    write_recording(tmp_path, "wave", [])  # last in sorted order, no samples
    trainer = make_trainer(tmp_path)

    assert trainer.load_data()
    trainer.prepare_data()

    # Must match the model's output layer, which has one unit per gesture
    assert trainer.y_train.shape == (4, len(trainer.gestures))
