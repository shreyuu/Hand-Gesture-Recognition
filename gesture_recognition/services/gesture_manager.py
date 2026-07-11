import numpy as np
from keras.models import load_model


class GestureManager:
    """Manages gesture data, model loading, and prediction"""

    def __init__(self, model_path, names_path):
        self.model_path = model_path
        self.names_path = names_path
        self.model = None
        self.class_names = []
        self.load_resources()

    def load_resources(self):
        """Load model and class names"""
        self.model = load_model(self.model_path)

        # Load class names (ignore blank lines from trailing newlines)
        with open(self.names_path, "r") as f:
            self.class_names = [line.strip() for line in f if line.strip()]

        print(f"Loaded {len(self.class_names)} gestures: {', '.join(self.class_names)}")

    def predict_gesture(self, landmarks):
        """Predict gesture from landmarks.

        Calls the model directly instead of ``model.predict()`` — for
        single-sample, per-frame inference the ``predict()`` machinery adds
        significant overhead.
        """
        inputs = np.asarray([landmarks], dtype=np.float32)
        prediction = np.asarray(self.model(inputs, training=False))
        class_id = int(np.argmax(prediction[0]))
        class_name = self.class_names[class_id]
        confidence = float(prediction[0][class_id])

        return class_name, confidence

    def add_gesture(self, name):
        """Add a new gesture to the class names file"""
        if name not in self.class_names:
            self.class_names.append(name)
            with open(self.names_path, "w") as f:
                f.write("\n".join(self.class_names))
            print(f"Added new gesture: {name}")
            return True
        return False
