import pytest

from gesture_recognition.user_profile import UserProfile, validate_profile_name


@pytest.mark.parametrize("name", ["default", "work laptop", "alice_2", "kid-mode"])
def test_normal_profile_names_are_accepted(name):
    assert validate_profile_name(name) == name


@pytest.mark.parametrize(
    "name", ["../../tmp/x", "/tmp/x", "a/b", "..", "x.json", "", "   ", "a\\b"]
)
def test_path_like_profile_names_are_rejected(name):
    with pytest.raises(ValueError):
        validate_profile_name(name)


def test_user_profile_refuses_to_leave_profiles_dir():
    with pytest.raises(ValueError):
        UserProfile("../../../tmp/escaped")
