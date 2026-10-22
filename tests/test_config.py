import pytest

from gesture_recognition.config import PROFILE_SETTINGS, resolve_setting, saved_setting


@pytest.fixture(autouse=True)
def no_setting_env_vars(monkeypatch):
    for env_var, _, _ in PROFILE_SETTINGS.values():
        monkeypatch.delenv(env_var, raising=False)


def test_default_when_nothing_is_set():
    assert resolve_setting("camera_index") == 0
    assert resolve_setting("camera_index", {}) == 0


def test_profile_beats_default():
    assert resolve_setting("camera_index", {"camera_index": 2}) == 2


def test_env_var_beats_profile(monkeypatch):
    monkeypatch.setenv("GESTURE_CAM_INDEX", "3")
    monkeypatch.setenv("GESTURE_DETECTION_CONF", "0.3")
    profile = {"camera_index": 1, "detection_confidence": 0.9}

    assert resolve_setting("camera_index", profile) == 3
    assert resolve_setting("detection_confidence", profile) == 0.3


def test_invalid_env_var_falls_back_to_profile(monkeypatch, capsys):
    monkeypatch.setenv("GESTURE_CAM_INDEX", "front")
    assert resolve_setting("camera_index", {"camera_index": 1}) == 1
    assert "GESTURE_CAM_INDEX" in capsys.readouterr().out


def test_profile_string_false_means_false():
    assert resolve_setting("enable_voice", {"enable_voice": "false"}) is False


def test_profile_numeric_string_is_parsed():
    assert resolve_setting("detection_confidence", {"detection_confidence": "0.3"}) == 0.3
    assert resolve_setting("detection_confidence", {"detection_confidence": 1}) == 1.0


@pytest.mark.parametrize(
    "value", ["https://example.com/stream.m3u8", "/etc/passwd", True, 1.5, [0]]
)
def test_profile_camera_index_must_be_an_int(value, capsys):
    # cv2.VideoCapture() would open a string as a URL or file
    assert resolve_setting("camera_index", {"camera_index": value}) == 0
    assert "camera_index" in capsys.readouterr().out


def test_saved_setting_ignores_env_vars(monkeypatch):
    # The settings dialog shows (and saves) this, so a one-off env override
    # must not end up written into the profile.
    monkeypatch.setenv("GESTURE_CAM_INDEX", "3")
    assert saved_setting("camera_index", {"camera_index": 1}) == 1
    assert saved_setting("camera_index", None) == 0
