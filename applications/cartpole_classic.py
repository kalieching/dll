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
from controllers.pid import PIDController
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

# Run
def run_episode(env, controller, max_steps=500, render=True):
    state = env.reset()
    controller.reset()

    history = {
        'x': [],
        'x_dot': [],
        'theta': [],
        'theta_dot': [],
        'force': [],
        'reward': [],
    }

    if render:
        fig, axes = setup_render()

    for step in range(max_steps):
        x, x_dot, theta, theta_dot = state
        force = controller.compute(theta, theta_dot)
        state, reward, terminated = env.step(force)

        history['x'].append(x)
        history['x_dot'].append(x_dot)
        history['theta'].append(theta)
        history['theta_dot'].append(theta_dot)
        history['force'].append(force)
        history['reward'].append(reward)

        if render:
            visualization(axes, state, force, step)

        if terminated:
            break

    return history

def setup_render():
    """Create the matplotlib figure for animation."""
    plt.ion()   # interactive mode — updates without blocking
    fig, axes = plt.subplots(2, 1, figsize=(8, 7))
    fig.tight_layout(pad=3.0)
    return fig, axes

def visualization(axes, state, force, step):
    """Draw one frame of the simulation."""
    x, x_dot, theta, theta_dot = state

    ax_cart, ax_plot = axes

    # Cart-pole drawing
    ax_cart.cla()
    ax_cart.set_xlim(-3, 3)
    ax_cart.set_ylim(-0.5, 1.5)
    ax_cart.set_aspect('equal')
    ax_cart.axhline(0, color='gray', linewidth=1)       # track
    ax_cart.axvline(2.4,  color='red', linewidth=1, linestyle='--')   # boundary
    ax_cart.axvline(-2.4, color='red', linewidth=1, linestyle='--')

    # Cart
    cart = patches.FancyBboxPatch(
        (x - 0.3, -0.15), 0.6, 0.3,
        boxstyle="round,pad=0.02",
        linewidth=1.5, edgecolor='steelblue', facecolor='lightsteelblue'
    )
    ax_cart.add_patch(cart)

    # Pole
    pole_len = 1.0   # visual length (2 * HALF_LEN)
    pole_x = x + pole_len * np.sin(theta)
    pole_y = pole_len * np.cos(theta)
    ax_cart.plot([x, pole_x], [0, pole_y],
                 color='darkorange', linewidth=4, solid_capstyle='round')
    ax_cart.plot(pole_x, pole_y, 'o', color='darkorange', markersize=8)

    # Force arrow
    if abs(force) > 0.1:
        ax_cart.annotate('', xy=(x + np.sign(force)*0.6, 0),
                         xytext=(x, 0),
                         arrowprops=dict(arrowstyle='->', color='green', lw=2))

    ax_cart.set_title(f'Step {step}   θ={np.degrees(theta):.1f}°   '
                      f'x={x:.2f}m   F={force:.1f}N')
    ax_cart.set_xlabel('Position (m)')

    # Time series of pole angle
    ax_plot.cla()
    ax_plot.set_title('Pole angle over time')
    ax_plot.set_xlabel('Step')
    ax_plot.set_ylabel('Angle (degrees)')
    ax_plot.axhline(0,    color='gray',  linewidth=0.8, linestyle='--')
    ax_plot.axhline(12,   color='red',   linewidth=0.8, linestyle='--', label='limit')
    ax_plot.axhline(-12,  color='red',   linewidth=0.8, linestyle='--')
    ax_plot.set_ylim(-20, 20)

    plt.pause(0.001)   # tiny pause lets matplotlib redraw


def plot_history(history):
    """
    Plot full episode statistics.
    """
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.suptitle('Episode Summary', fontsize=13)

    steps = range(len(history['theta']))

    axes[0].plot(steps, history['theta'], color='darkorange')
    axes[0].axhline(12,  color='red', linestyle='--', linewidth=0.8)
    axes[0].axhline(-12, color='red', linestyle='--', linewidth=0.8)
    axes[0].set_ylabel('Pole angle (°)')
    axes[0].set_title('Pole angle — red dashes are termination limits')

    axes[1].plot(steps, history['x'], color='steelblue')
    axes[1].axhline(2.4,  color='red', linestyle='--', linewidth=0.8)
    axes[1].axhline(-2.4, color='red', linestyle='--', linewidth=0.8)
    axes[1].set_ylabel('Cart position (m)')
    axes[1].set_title('Cart position — watch it drift')

    axes[2].plot(steps, history['force'], color='green')
    axes[2].set_ylabel('Force (N)')
    axes[2].set_xlabel('Step')
    axes[2].set_title('PID controller output')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    env = CartPoleEnv()
    controller = PIDController(Kp=50.0, Kd=10.0, Ki=1.0)

    history = run_episode(env, controller, max_steps=500, render=True)
    plot_history(history)
