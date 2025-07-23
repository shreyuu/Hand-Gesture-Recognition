import tkinter as tk
from tkinter import ttk
from utils.user_profile import UserProfile


class SettingsDialog:
    def __init__(self, profile=None):
        if profile is None:
            self.profile = UserProfile()
        else:
            self.profile = profile

        self.root = tk.Tk()
        self.root.title("Gesture Recognition Settings")
        self.root.geometry("400x500")
        self.create_widgets()

    def create_widgets(self):
        """Create the settings UI elements"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Camera settings
        camera_frame = ttk.LabelFrame(main_frame, text="Camera Settings", padding="10")
        camera_frame.pack(fill=tk.X, pady=5)

        ttk.Label(camera_frame, text="Camera Index:").grid(column=0, row=0, sticky=tk.W)
        self.camera_var = tk.IntVar(value=self.profile.get("camera_index", 0))
        ttk.Spinbox(
            camera_frame, from_=0, to=10, textvariable=self.camera_var, width=5
        ).grid(column=1, row=0, padx=5)

        # Detection settings
        detect_frame = ttk.LabelFrame(
            main_frame, text="Detection Settings", padding="10"
        )
        detect_frame.pack(fill=tk.X, pady=5)

        ttk.Label(detect_frame, text="Confidence Threshold:").grid(
            column=0, row=0, sticky=tk.W
        )
        self.confidence_var = tk.DoubleVar(
            value=self.profile.get("detection_confidence", 0.7)
        )
        confidence_scale = ttk.Scale(
            detect_frame,
            from_=0.1,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.confidence_var,
        )
        confidence_scale.grid(column=1, row=0, padx=5)
        ttk.Label(detect_frame, textvariable=self.confidence_var).grid(column=2, row=0)

        # Voice settings
        voice_frame = ttk.LabelFrame(main_frame, text="Voice Settings", padding="10")
        voice_frame.pack(fill=tk.X, pady=5)

        self.voice_enabled = tk.BooleanVar(
            value=self.profile.get("enable_voice", False)
        )
        ttk.Checkbutton(
            voice_frame, text="Enable Voice", variable=self.voice_enabled
        ).grid(column=0, row=0, sticky=tk.W)

        ttk.Label(voice_frame, text="Language:").grid(
            column=0, row=1, sticky=tk.W, pady=5
        )
        self.language_var = tk.StringVar(value=self.profile.get("voice_language", "en"))
        languages = ["en", "es", "fr", "de", "it", "ja", "ko", "zh-CN"]
        language_combo = ttk.Combobox(
            voice_frame, textvariable=self.language_var, values=languages
        )
        language_combo.grid(column=1, row=1, sticky=tk.W, padx=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(
            side=tk.RIGHT, padx=5
        )
        ttk.Button(button_frame, text="Cancel", command=self.root.destroy).pack(
            side=tk.RIGHT, padx=5
        )

    def save_settings(self):
        """Save settings to profile"""
        self.profile.set("camera_index", self.camera_var.get())
        self.profile.set("detection_confidence", self.confidence_var.get())
        self.profile.set("enable_voice", self.voice_enabled.get())
        self.profile.set("voice_language", self.language_var.get())

        if self.profile.save_profile():
            self.root.destroy()

    def show(self):
        """Display the settings dialog"""
        self.root.mainloop()
        return self.profile
