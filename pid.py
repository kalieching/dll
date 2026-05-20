class PIDController():
    """
    Controls pole angle theta to zero.
    Outputs a force to apply to the cart.
    """
    def __init__(self, Kp=50.0, Kd=10.0, Ki=1.0, dt=0.02):
        """
        Kp: proportional gain - reacts to current angle
        Kd: derivative gain - reacts to angular velocity
        Ki: integral gain - corrects persistent offset
        dt: timestamp, must match CartPoleEnv.DT
        """
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.dt = dt

        self._integral = 0.0

    def reset(self):
        """Called at the start of each episode."""
        self._integral = 0.0
    
    def compute(self, theta, theta_dot):
        """
        Compute the force to apply to the cart.
        """
        # Proportional term - big angle = big force
        p_term = self.Kp * theta

        # Derivative term - fast fall = extra force to brake it
        d_term = self.Kd * theta_dot 

        self._integral += theta * self.dt
        i_term = self.Ki * self._integral

        force = p_term + d_term + i_term

        return force
