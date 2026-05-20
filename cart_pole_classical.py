
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

# Physics
class CartPoleEnv():
    def __init__():
        pass

    def step(action):
        pass

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