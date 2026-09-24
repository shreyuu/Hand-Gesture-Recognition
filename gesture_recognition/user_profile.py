import json
import os

from gesture_recognition.config import BASE_DIR


class UserProfile:
    """Manages user-specific settings and preferences"""

    def __init__(self, profile_name="default"):
        self.profile_name = profile_name
        # Only settings the user actually saved. Missing keys fall back to
        # env vars / defaults via config.resolve_setting().
        self.settings = {}

        self.profiles_dir = os.path.join(BASE_DIR, "data", "profiles")
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)

        self.load_profile()

    def load_profile(self):
        """Load user profile from file if exists"""
        profile_path = os.path.join(self.profiles_dir, f"{self.profile_name}.json")

        if os.path.exists(profile_path):
            try:
                with open(profile_path, "r", encoding="utf-8") as file:
                    loaded_settings = json.load(file)
                    self.settings.update(loaded_settings)
                print(f"Loaded profile: {self.profile_name}")
            except (OSError, json.JSONDecodeError) as e:
                print(f"Error loading profile: {e}")

    def save_profile(self):
        """Save current settings to profile file"""
        profile_path = os.path.join(self.profiles_dir, f"{self.profile_name}.json")

        try:
            with open(profile_path, "w", encoding="utf-8") as file:
                json.dump(self.settings, file, indent=4)
            print(f"Saved profile: {self.profile_name}")
            return True
        except (OSError, TypeError, ValueError) as e:
            print(f"Error saving profile: {e}")
            return False

    def get(self, setting_name, default=None):
        """Get a setting value"""
        return self.settings.get(setting_name, default)

    def set(self, setting_name, value):
        """Set a setting value"""
        self.settings[setting_name] = value
