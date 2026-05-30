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
<<<<<<< HEAD
from controllers.pid import PIDController
import matplotlib.pyplot as plt
import matplotlib.patches as patches
=======
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from pid import PIDController
import matplotlib.pyplot as plt
>>>>>>> 62b0279 (Add visualization, run function, and fix small bug)

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
        theta_dot = theta_dot + theta_acc * self.DT

        self.state = np.array([x, x_dot, theta, theta_dot])

        # Check termination
        termination = (abs(x) > self.MAX_POS or abs(theta) > self.MAX_ANGLE)

        reward = 0.0 if termination else 1.0

        return self.state.copy(), reward, termination

# Run
<<<<<<< HEAD
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
=======
def run():
    env = CartPoleEnv()
    pid = PIDController(
        Kp=50.0,
        Ki=0.0,
        Kd=5.0
    )
    env.reset()
    pid.reset()

    total_reward = 0.0
    history = []
    for _ in range(1000):
        x, x_dot, theta, theta_dot = env.state # error is theta
        force = pid.compute(theta, env.DT)
        state, reward, done = env.step(force)
        total_reward += reward
        history.append(state)
        if done:
            break
    return history, total_reward


# Visualize
def visualization():
    from matplotlib.animation import FuncAnimation
    from matplotlib.patches import Rectangle
    from matplotlib.gridspec import GridSpec

    history, total_reward = run()
    history = np.array(history)
    t = np.arange(len(history)) * CartPoleEnv.DT

    POLE_LEN = CartPoleEnv.HALF_LEN * 2
    CART_W, CART_H = 0.4, 0.2
    PIVOT_Y = CART_H / 2

    fig = plt.figure(figsize=(14, 5))
    fig.suptitle(f"CartPole PID — steps survived: {len(history)}, reward: {total_reward:.0f}")
    gs = GridSpec(2, 2, figure=fig)

    # Animation (left, spans both rows)
    ax_anim = fig.add_subplot(gs[:, 0])
    ax_anim.set_xlim(-CartPoleEnv.MAX_POS - 0.5, CartPoleEnv.MAX_POS + 0.5)
    ax_anim.set_ylim(-0.5, POLE_LEN + 0.5)
    ax_anim.set_aspect('equal')
    ax_anim.axhline(0, color='gray', linewidth=0.8)
    ax_anim.axvline(CartPoleEnv.MAX_POS, color='red', linestyle='--', linewidth=0.8)
    ax_anim.axvline(-CartPoleEnv.MAX_POS, color='red', linestyle='--', linewidth=0.8)

    cart = Rectangle((-CART_W / 2, -CART_H / 2), CART_W, CART_H, color='steelblue')
    ax_anim.add_patch(cart)
    pole_line, = ax_anim.plot([], [], 'o-', color='saddlebrown', linewidth=3, markersize=6)
    time_text = ax_anim.text(0.02, 0.95, '', transform=ax_anim.transAxes)

    # Theta plot (top right)
    ax_theta = fig.add_subplot(gs[0, 1])
    ax_theta.plot(t, history[:, 2])
    ax_theta.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    ax_theta.axhline(CartPoleEnv.MAX_ANGLE, color='red', linestyle='--', linewidth=0.8, label='limit')
    ax_theta.axhline(-CartPoleEnv.MAX_ANGLE, color='red', linestyle='--', linewidth=0.8)
    ax_theta.set_ylabel("Pole angle (rad)")
    ax_theta.legend()
    theta_vline = ax_theta.axvline(0, color='black', linewidth=0.8)

    # Position plot (bottom right)
    ax_pos = fig.add_subplot(gs[1, 1])
    ax_pos.plot(t, history[:, 0])
    ax_pos.axhline(CartPoleEnv.MAX_POS, color='red', linestyle='--', linewidth=0.8, label='limit')
    ax_pos.axhline(-CartPoleEnv.MAX_POS, color='red', linestyle='--', linewidth=0.8)
    ax_pos.set_ylabel("Cart position (m)")
    ax_pos.set_xlabel("Time (s)")
    ax_pos.legend()
    pos_vline = ax_pos.axvline(0, color='black', linewidth=0.8)

    def update(frame):
        x, _, theta, _ = history[frame]
        cart.set_xy((x - CART_W / 2, -CART_H / 2))
        tip_x = x + POLE_LEN * np.sin(theta)
        tip_y = PIVOT_Y + POLE_LEN * np.cos(theta)
        pole_line.set_data([x, tip_x], [PIVOT_Y, tip_y])
        time_text.set_text(f't = {frame * CartPoleEnv.DT:.2f}s')
        theta_vline.set_xdata([t[frame], t[frame]])
        pos_vline.set_xdata([t[frame], t[frame]])
        return cart, pole_line, time_text, theta_vline, pos_vline

    ani = FuncAnimation(fig, update, frames=len(history), interval=CartPoleEnv.DT * 1000, blit=True)
    plt.tight_layout()
    plt.show()
    return ani


if __name__ == "__main__":
    visualization()
>>>>>>> 62b0279 (Add visualization, run function, and fix small bug)
