"""
Cart-pole System
* Cart can slide left/right on a track
* A pole is balanced upright on a pivot on the top of the cart
* Goal: keep the pole from falling by pushing the cart

State of system:
* x - cart position
* x-dot - cart velocity
* theta - pole angle, 0 when upright
* theta_dot - pole angular velocity

Action is one number: Force (F) applied to the cart, left or right

* Difficult because the pole naturally wants to fall
* If it tilts right, gravity pulls it further right
* If it tilts left, gravity pulls it further left
* Must continuously push the cart to make corrections

* PID controller - computes a corrective force based on the error (how far you are from the goal):

- P (Proportional): Push harder the further the pole is tilted (Kp * theta)
- D (Derivative): Dampen oscillations - if the pole is falling fast, push harder (Kd * theta_dot)
- I (Integral): Fix any persistent bias that P+D can't handle (Ki * integral(theta)dt)

Total force: F = Kp * theta + Kd * theta_dot + Ki * integral(theta)dt

The art of classical control is tuning Kp, Kd, Ki.
"""

import numpy as np

# Physics
class CartPoleEnv:
    """
    Cart-pole physics from scratch.

    State: [x, x_dot, theta, theta_dot]
        x - cart position (meters)
        x_dot - cart velocity (meters/second)
        theta - pole angle from vertical (radians, + = right)
        theta_dot - pole angular velocity (radians/second)
    
        Action: force F applied to cart (Newtons, + = right)
    """

    # Physical constants
    GRAVITY = 9.8 # m/s^2
    MASS_CART = 1.0 # kg
    MASS_POLE = 0.1 # kg
    HALF_LEN = 0.5 # half the pole length (meters)
    DT = 0.01 # simulation timestep (seconds)

    # Episode termination thresholds
    MAX_ANGLE = 0.2095 # ~12 degrees in radians
    MAX_POS = 2.4 # meters from center

    def __init__(self):
        self.state = None
        self.reset()

    def reset(self, seed=None):
        rng = np.random.default_rng(seed)
        self.state = rng.uniform(low=-0.05, high=0.05, size=(4,))
        return self.state.copy()

    def step(self, force):
        x, x_dot, theta, theta_dot = self.state

        # Compute physics
        sin_t = np.sin(theta)
        cos_t = np.cos(theta)
        total_mass = self.MASS_CART + self.MASS_POLE

        temp = (force + self.MASS_POLE * self.HALF_LEN * theta_dot**2 * sin_t) / total_mass
        theta_acc = (self.GRAVITY * sin_t - cos_t * temp) / (self.HALF_LEN * (4.0/3.0 - self.MASS_POLE * cos_t**2 / total_mass))

        x_acc = temp - self.MASS_POLE * self.HALF_LEN * theta_acc * cos_t / total_mass

        # Update state using Euler integration
        x = x + x_dot * self.DT
        x_dot = x_dot + x_acc * self.DT
        theta = theta + theta_dot * self.DT
        theta_dot = theta_dot * theta_acc * self.DT

        self.state = np.array([x, x_dot, theta, theta_dot])

        # Check termination
        termination = (abs(x) > self.MAX_POS or abs(theta) > self.MAX_ANGLE)

        reward = 0.0 if termination else 1.0

        return self.state.copy(), reward, termination


# PID Controller
class PIDController():
    def __init__():
        pass

# Run
def run():
    pass

# Visualize
def visualization():
    pass