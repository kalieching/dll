# Goal: Study Jax
# Mini-project: Linear regression implemented from scratch with Jax

# Linear regression:
# Compute y_pred = X @ w + b
# Compute loss = mean((y_pred - y_true) ^ 2)
# Compute gradients of loss with respect to w and b
# Update w and b using gradient w = w - learning_rate * grad_w

# After coding lessons:
# 1.) Pull values out of a jax array with .item(), .tolist(), float(), or np.array()
# 2.) An operation like X @ w collapses to the last dimension

import jax.numpy as jnp
import jax
import matplotlib.pyplot as plt
import numpy as np

KEY = jax.random.PRNGKey(0)
key1, key2 = jax.random.split(KEY)

def generate_data(w=2.0, b=1.0, noise_scale=0.1):
    X = jax.random.normal(key1, (100, 1)) # returns 100x1 matrix of random values
    noise = jax.random.normal(key2, (100, 1))
    y = X * w + b + noise_scale * noise
    return X, y

X_data, y_data = generate_data(noise_scale=0.6)
X_data, y_data = np.array(X_data), np.array(y_data)

def visualize_data(X, y, w, b):
    plt.scatter(X, y)
    plt.plot(X, w * X + b, color="red")
    plt.xlabel("X")
    plt.ylabel("y")
    plt.title("Generated Data")
    plt.show()


def predict(X, w, b):
    return X @ w + b # can also do jnp.dot(X, w) + b

def compute_loss(y_pred, y_true):
    """
    Compute mean squared error loss. MSE is used because penalizes 
    larger errors more than smaller ones. Commonly used for regression.
    """
    return jnp.mean((y_pred - y_true) ** 2)

def compute_gradients(X, y, w, b):
    grad_fn = jax.grad(lambda w, b: compute_loss(predict(X, w, b), y), argnums=(0, 1))
    grad_w, grad_b = grad_fn(w, b)
    return grad_w, grad_b

def train(num_epochs=1000, lr=0.01):
    X, y = generate_data(noise_scale=0.6)
    w, b = jnp.zeros((1, 1)), jnp.zeros((1,))
    for epoch in range(num_epochs):
        y_pred = predict(X, w, b)
        loss = compute_loss(y_pred, y)
        grad_w, grad_b = compute_gradients(X, y, w, b)
        w -= lr * grad_w
        b -= lr * grad_b
        if epoch % 100 == 0:
            print(f"Epoch {epoch+1}, Loss: {loss:.4f}, w: {w.item():.4f}, b: {b.item():.4f}")
    return w, b

w, b = train()
visualize_data(X_data, y_data, w, b)