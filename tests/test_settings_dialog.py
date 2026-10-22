import pytest

tk = pytest.importorskip("tkinter")

from gesture_recognition.ui import settings_dialog


class FakeProfile(dict):
    saved = False

    def set(self, name, value):
        self[name] = value

    def save_profile(self):
        self.saved = True
        return True


@pytest.fixture
def dialog():
    try:
        d = settings_dialog.SettingsDialog(FakeProfile())
    except tk.TclError:
        pytest.skip("no display available")
    d.root.withdraw()
    yield d
    try:
        d.root.destroy()
    except tk.TclError:
        pass  # already closed by a successful save


def test_non_numeric_camera_index_shows_an_error(dialog, monkeypatch):
    errors = []
    monkeypatch.setattr(
        settings_dialog.messagebox, "showerror", lambda *a, **k: errors.append(a)
    )
    dialog.camera_var.set("front")

    dialog.save_settings()  # must not raise

    assert errors
    assert dialog.profile.saved is False
    assert "camera_index" not in dialog.profile


def test_valid_settings_are_saved(dialog):
    dialog.camera_var.set(2)

    dialog.save_settings()

    assert dialog.profile.saved is True
    assert dialog.profile["camera_index"] == 2
