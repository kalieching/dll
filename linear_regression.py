# Goal: Study Jax
# Mini-project: Linear regression implemented from scratch with Jax

# Linear regression:
# loss = mean((y_pred - y_true) ^ 2)
# y_pred = X @ w + b
# w = w - learning_rate * grad_w

import jax.numpy as jnp
import jax

KEY = jax.random.PRNGKey(0)

def generate_data(w=2.0, b=1.0, noise_scale=0.1):
    X = jax.random.normal(KEY, (100, 1)) # returns 100x1 matrix of random values
    noise = jax.random.normal(KEY, (100, 1))
    data_to_regress = X * w + b + noise_scale * noise
    return data_to_regress

print(generate_data())
