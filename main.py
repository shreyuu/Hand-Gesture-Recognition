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

    # Handle different modes
    if args.mode == "record" or (
        len(sys.argv) == 1
        and input("Enter mode (recognize/record/train/settings): ").lower() == "record"
    ):
        record_gesture()
    elif args.mode == "train":
        trainer = GestureTrainer()
        trainer.train(epochs=args.epochs, batch_size=args.batch_size)
    elif args.mode == "settings":
        profile = UserProfile(args.profile)
        dialog = SettingsDialog(profile)
        dialog.show()
    else:  # Default to recognize mode
        profile_name = args.profile if hasattr(args, "profile") else "default"
        profile = UserProfile(profile_name)
        app = GestureRecognitionApp()
        app.run()


if __name__ == "__main__":
    main()
