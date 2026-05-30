class PIDController():
    """
    Simple PID controller.
    """
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0.0
        self.prev_error = 0.0

    def reset(self) -> None:
        """Reset integral and derivative state."""
        self.integral = 0.0
        self.prev_error = 0.0
    
    def compute(self, error, dt):
        self.integral += error * dt
        derivative =  (error - self.prev_error)/ dt
        self.prev_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        