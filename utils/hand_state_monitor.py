import time


class HandStateMonitor:
    """Monitors when hands enter and leave the camera view"""

    def __init__(self, entry_delay=0.5, exit_delay=1.0):
        self.hand_present = False
        self.last_hand_time = 0
        self.entry_delay = entry_delay  # How long before registering hand entry
        self.exit_delay = exit_delay  # How long before registering hand exit
        self.entry_callbacks = []
        self.exit_callbacks = []

    def update(self, hand_detected):
        """Update hand presence state and trigger callbacks if needed"""
        current_time = time.time()

        if hand_detected and not self.hand_present:
            # Check if hand has been present long enough to count as "entered"
            if (
                self.last_hand_time > 0
                and (current_time - self.last_hand_time) >= self.entry_delay
            ):
                self.hand_present = True
                self._trigger_callbacks(self.entry_callbacks)
            elif self.last_hand_time == 0:
                # First detection
                self.last_hand_time = current_time
        elif hand_detected:
            # Hand continues to be present
            self.last_hand_time = current_time
        elif not hand_detected and self.hand_present:
            # Hand was present but now gone
            if (current_time - self.last_hand_time) >= self.exit_delay:
                self.hand_present = False
                self._trigger_callbacks(self.exit_callbacks)

    def on_hand_enter(self, callback):
        """Register callback for when hand enters the frame"""
        self.entry_callbacks.append(callback)

    def on_hand_exit(self, callback):
        """Register callback for when hand leaves the frame"""
        self.exit_callbacks.append(callback)

    def _trigger_callbacks(self, callbacks):
        """Trigger all registered callbacks"""
        for callback in callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in callback: {e}")
