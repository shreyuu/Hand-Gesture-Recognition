import os
import json


class UserProfile:
    """Manages user-specific settings and preferences"""

    def __init__(self, profile_name="default"):
        self.profile_name = profile_name
        self.settings = {
            "enable_voice": False,
            "voice_language": "en",
            "detection_confidence": 0.7,
            "camera_index": 1,
            "theme": "default",
        }

        self.profiles_dir = "profiles"
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir)

        self.load_profile()

    def load_profile(self):
        """Load user profile from file if exists"""
        profile_path = os.path.join(self.profiles_dir, f"{self.profile_name}.json")

        if os.path.exists(profile_path):
            try:
                with open(profile_path, "r") as file:
                    loaded_settings = json.load(file)
                    self.settings.update(loaded_settings)
                print(f"Loaded profile: {self.profile_name}")
            except Exception as e:
                print(f"Error loading profile: {e}")

    def save_profile(self):
        """Save current settings to profile file"""
        profile_path = os.path.join(self.profiles_dir, f"{self.profile_name}.json")

        try:
            with open(profile_path, "w") as file:
                json.dump(self.settings, file, indent=4)
            print(f"Saved profile: {self.profile_name}")
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False

    def get(self, setting_name, default=None):
        """Get a setting value"""
        return self.settings.get(setting_name, default)

    def set(self, setting_name, value):
        """Set a setting value"""
        self.settings[setting_name] = value
