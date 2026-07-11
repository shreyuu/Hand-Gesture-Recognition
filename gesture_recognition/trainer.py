import os

import numpy as np
import tensorflow as tf
from keras.callbacks import EarlyStopping, TensorBoard
from keras.layers import Dense, Flatten, Input
from keras.models import Sequential

from gesture_recognition.config import BASE_DIR
from gesture_recognition.dataset import load_samples


class GestureTrainer:
    """Train a gesture recognition model on custom data"""

    def __init__(self, data_dir=None, model_path=None):
        self.data_dir = data_dir or os.path.join(BASE_DIR, "recorded_gestures")
        self.model_path = model_path or os.path.join(BASE_DIR, "models", "custom_model")
        self.x_train = []
        self.y_train = []
        self.gestures = []

    def load_data(self):
        """Load recorded gesture data from JSON files"""
        print("Loading gesture data...")

        if not os.path.exists(self.data_dir):
            print(f"Error: Data directory {self.data_dir} not found")
            return False

        # Samples are normalized (wrist-relative, scale-invariant) so the
        # model doesn't learn the hand's position in the frame.
        self.x_train, self.y_train, self.gestures = load_samples(
            self.data_dir, normalize=True
        )

        if not self.x_train:
            print(f"No gesture data files found in {self.data_dir}")
            return False

        print(f"Loaded {len(self.x_train)} samples for {len(self.gestures)} gestures")
        return True

    def prepare_data(self):
        """Prepare data for training"""
        self.x_train = np.array(self.x_train, dtype=np.float32)
        self.y_train = np.array(self.y_train)

        # One-hot encode the labels
        self.y_train = tf.keras.utils.to_categorical(self.y_train)

        # Shuffle so the validation split isn't a single gesture
        indices = np.random.permutation(len(self.x_train))
        self.x_train = self.x_train[indices]
        self.y_train = self.y_train[indices]

    def build_model(self):
        """Build and compile the model.

        The 21 landmarks of a single frame are a static pose, not a time
        sequence, so a small dense network on the flattened coordinates is
        both faster and a better fit than a recurrent model.
        """
        model = Sequential(
            [
                Input(shape=(21, 2)),
                Flatten(),
                Dense(64, activation="relu"),
                Dense(32, activation="relu"),
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

        callbacks = [
            TensorBoard(log_dir=os.path.join(BASE_DIR, "logs", "fit"), histogram_freq=1)
        ]

        # A validation split only makes sense with more than one class and
        # enough samples to hold some out.
        validation_split = 0.2 if len(self.x_train) >= 10 else 0.0
        if validation_split:
            callbacks.append(
                EarlyStopping(
                    monitor="val_loss", patience=10, restore_best_weights=True
                )
            )

        model.fit(
            self.x_train,
            self.y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=callbacks,
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
