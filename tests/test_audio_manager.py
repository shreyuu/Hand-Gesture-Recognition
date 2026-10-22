import hashlib
import os
import stat
import tempfile

import pytest

from gesture_recognition.services import audio_manager
from gesture_recognition.services.audio_manager import AudioManager


class FailingTTS:
    """Stands in for gTTS when the network drops mid-request.

    Like the real ``gTTS.save()``, it opens the target file before the
    request fails, leaving an empty file behind.
    """

    def __init__(self, text, lang, slow):
        pass

    def save(self, path):
        with open(path, "wb"):
            raise audio_manager.gTTSError("network down")


class WorkingTTS:
    def __init__(self, text, lang, slow):
        pass

    def save(self, path):
        with open(path, "wb") as f:
            f.write(b"ID3 fake mp3")


@pytest.fixture
def manager(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    # Keep the old shared-temp-dir location inside tmp_path too
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path / "systmp"))
    os.makedirs(tmp_path / "systmp")

    m = AudioManager()
    m.played = []
    monkeypatch.setattr(m, "_play", m.played.append)
    return m


def mp3_files(root):
    return [p for p in root.rglob("*") if p.is_file()]


def test_failed_tts_leaves_no_cached_file(manager, tmp_path, monkeypatch):
    monkeypatch.setattr(audio_manager, "gTTS", FailingTTS)

    manager._process_audio("okay", "en", False)

    assert manager.played == []
    assert mp3_files(tmp_path) == []  # neither the cache nor the temp dir


def test_tts_is_retried_after_a_failure(manager, monkeypatch):
    monkeypatch.setattr(audio_manager, "gTTS", FailingTTS)
    manager._process_audio("okay", "en", False)

    monkeypatch.setattr(audio_manager, "gTTS", WorkingTTS)
    manager._process_audio("okay", "en", False)

    assert len(manager.played) == 1
    with open(manager.played[0], "rb") as f:
        assert f.read() == b"ID3 fake mp3"


def test_cache_dir_is_private_to_the_user(manager, tmp_path):
    cache_dir = manager.cache_dir
    assert cache_dir.startswith(str(tmp_path / "cache"))
    assert stat.S_IMODE(os.stat(cache_dir).st_mode) == 0o700


def test_file_planted_in_shared_temp_dir_is_not_played(manager, tmp_path, monkeypatch):
    # Another local user pre-creates the old predictable filename in /tmp
    digest = hashlib.md5(b"okay|en|False").hexdigest()
    planted = tmp_path / "systmp" / f"gesture_{digest}.mp3"
    planted.write_bytes(b"attacker audio")
    monkeypatch.setattr(audio_manager, "gTTS", WorkingTTS)

    manager._process_audio("okay", "en", False)

    assert manager.played
    assert manager.played[0] != str(planted)
