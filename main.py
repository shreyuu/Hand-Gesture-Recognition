import argparse
import sys
from gesture_recognition_app import GestureRecognitionApp
from gesture_recorder import record_gesture
from gesture_trainer import GestureTrainer
from utils.settings_dialog import SettingsDialog
from utils.user_profile import UserProfile


def main():
    """Main entry point with command line argument parsing"""
    parser = argparse.ArgumentParser(description="Hand Gesture Recognition System")

    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")

    # Recognition mode (default)
    recognize_parser = subparsers.add_parser(
        "recognize", help="Run gesture recognition"
    )
    recognize_parser.add_argument(
        "--profile", type=str, default="default", help="User profile to load"
    )

    # Recording mode
    record_parser = subparsers.add_parser("record", help="Record gesture data")
    record_parser.add_argument(
        "--gesture", type=str, help="Name of the gesture to record"
    )

    # Training mode
    train_parser = subparsers.add_parser(
        "train", help="Train a model on recorded gestures"
    )
    train_parser.add_argument(
        "--epochs", type=int, default=50, help="Number of training epochs"
    )
    train_parser.add_argument(
        "--batch-size", type=int, default=16, help="Training batch size"
    )

    # Settings mode
    settings_parser = subparsers.add_parser(
        "settings", help="Configure application settings"
    )
    settings_parser.add_argument(
        "--profile", type=str, default="default", help="User profile to configure"
    )

    # Parse arguments
    args = parser.parse_args()

    # When no subcommand is given, ask interactively (default: recognize)
    mode = args.mode
    if mode is None and len(sys.argv) == 1:
        choice = input(
            "Enter mode (recognize/record/train/settings) [recognize]: "
        ).strip().lower()
        mode = choice or "recognize"

    # Handle different modes
    if mode == "record":
        record_gesture()
    elif mode == "train":
        trainer = GestureTrainer()
        trainer.train(
            epochs=getattr(args, "epochs", 50),
            batch_size=getattr(args, "batch_size", 16),
        )
    elif mode == "settings":
        profile = UserProfile(getattr(args, "profile", "default"))
        dialog = SettingsDialog(profile)
        dialog.show()
    else:  # Default to recognize mode
        profile = UserProfile(getattr(args, "profile", "default"))
        app = GestureRecognitionApp(profile=profile)
        app.run()


if __name__ == "__main__":
    main()
