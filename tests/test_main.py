import sys

import pytest

pytest.importorskip("tensorflow")
pytest.importorskip("mediapipe")

import main


def test_typo_at_mode_prompt_is_an_error(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    monkeypatch.setattr("builtins.input", lambda prompt: "trian")
    monkeypatch.setattr(
        main, "GestureRecognitionApp", lambda **kw: pytest.fail("started recognition")
    )

    with pytest.raises(SystemExit) as exc:
        main.main()
    assert exc.value.code == 2


def test_path_like_profile_is_rejected(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", "settings", "--profile", "../../tmp/x"])
    monkeypatch.setattr(main, "SettingsDialog", lambda p: pytest.fail("opened dialog"))

    with pytest.raises(SystemExit) as exc:
        main.main()
    assert exc.value.code == 2
