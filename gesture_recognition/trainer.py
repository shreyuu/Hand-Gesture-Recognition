import os
import numpy as np
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from keras.callbacks import TensorBoard
import json


class GestureTrainer:
    """Train a gesture recognition model on custom data"""

    def __init__(self, data_dir="recorded_gestures", model_path="models/custom_model"):
        self.data_dir = data_dir
        self.model_path = model_path
        self.x_train = []
        self.y_train = []
        self.gestures = []

    def load_data(self):
        """Load recorded gesture data from JSON files"""
        print("Loading gesture data...")

        if not os.path.exists(self.data_dir):
            print(f"Error: Data directory {self.data_dir} not found")
            return False

        files = [f for f in os.listdir(self.data_dir) if f.endswith(".json")]

        if not files:
            print(f"No gesture data files found in {self.data_dir}")
            return False

        for file in files:
            # Extract gesture name from filename (format: gesture_name_timestamp.json)
            gesture_name = file.split("_")[0]

            # Add to gesture list if not already there
            if gesture_name not in self.gestures:
                self.gestures.append(gesture_name)

            # Load samples
            file_path = os.path.join(self.data_dir, file)
            with open(file_path, "r") as f:
                samples = json.load(f)

            # Add samples to training data
            for sample in samples:
                self.x_train.append(sample)
                self.y_train.append(self.gestures.index(gesture_name))

        print(f"Loaded {len(self.x_train)} samples for {len(self.gestures)} gestures")
        return True

    def prepare_data(self):
        """Prepare data for training"""
        # Convert to numpy arrays
        self.x_train = np.array(self.x_train)
        self.y_train = np.array(self.y_train)

        # One-hot encode the labels
        self.y_train = tf.keras.utils.to_categorical(self.y_train)

    def build_model(self):
        """Build and compile the model"""
        model = Sequential(
            [
                LSTM(64, input_shape=(21, 2), return_sequences=True),
                LSTM(128),
                Dense(64, activation="relu"),
                Dense(len(self.gestures), activation="softmax"),
            ]
        )

        model.compile(
            optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
        )

        return model

    def train(self, epochs=50, batch_size=16):
        """Train the model"""
        if not self.load_data():
            return False

        self.prepare_data()

        model = self.build_model()
        print(f"Training model with {len(self.x_train)} samples...")

        # Create logs directory for TensorBoard
        log_dir = "logs/fit"
        tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

        # Train the model
        model.fit(
            self.x_train,
            self.y_train,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[tensorboard_callback],
        )

        # Save the model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        model.save(self.model_path)

        # Save gesture names
        with open(f"{self.model_path}_gestures.txt", "w") as f:
            f.write("\n".join(self.gestures))

        print(f"Model saved to {self.model_path}")
        return True


if __name__ == "__main__":
    trainer = GestureTrainer()
    trainer.train()
