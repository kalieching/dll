
#### 05-01-2026

I am beginning a daily journey to improve my deep learning, robotics, and general engineering skills. This will serve as a journal to record my progress over time.

The main concepts I will cover:
- Fundamentals (MNIST)
- Transformers
- Action Chunking Transformers
- Diffusion Policy
- Reinforcement Learning (SAC, Q-Learning, etc.)

#### 05-03-2026 - Transformers

I read this chapter: https://d2l.ai/chapter_attention-mechanisms-and-transformers/queries-keys-values.html

Key notes:
- Keys and values are the pairings that exist in a database, while queries are requests to that database.

#### 05-04-2026 - Transformers

I read this chapter: https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html 

Key notes:
- Why use dot product?
    - It's a very intuitive method to capture the "distance" between two vectors Q and K to compute a similarity score.
    - When you have two vectors, 


#### 05-05-2026 - Transformers

Given a sequence of tokens, attention lets each token determine which tokens it should pay attention to.
- Q: What am I looking for?
- K: What do I tell about myself?
- V: What do I contribute if my associated key is selected?

The key equation is Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V.


#### 05-06-2026 - Whole-Body Control Using RL for Humanoids

I have been working on a side project to bring up a whole-body control RL policy, train using sim, and deploy on a simulated humanoid robot. So far, I completed the full IsaacSim and IsaacLab setup and got comfortable with the tools. I trained two policies for ants and robot dogs. The policies use RSL-RL's OnPolicyRunner which uses PPO by default.

##### Proximal Policy Optimization (PPO)

Goal: improving the training stability of our policy by limiting the change made to the policy at each training epoch, thus avoiding large policy updates. This is to increase the likelihood of converging to an optimal solution. We can think of taking too large of a step during policy update as "falling off the cliff" and getting a bad policy, which is difficult or impossible to recover from.

We calculate a ratio between the current and former policy to ensure the policy has not changed too much. This ratio is clipped to a range [1 - eps, 1 + eps].

#### 05-09-2026

Background
- The core task of transformers is to do sequence modeling - given some input sequence (words, tokens, characters) produce some output
- Sequence modeling useful for translation (language), summarization, generation (prompt completion)
- Words depend on other words that are sometimes far from each other in the sentence
- Prior to transformers, the dominant approach was Recurrent Neural Networks (RNNs) where a sequence was processed one at a time, left to right, carrying forward the hidden state

Attention Scoring Functions
- Distance functions are more expensive to compute than dot products

#### 05-19-2026

Started soft-actor critic policy implementation from scratch.

#### 5-20-2026

Started classical PID controller and cart-pole application from scratch. The goal is to create a library of algorithms and models that I personally manually implemented and can pull in for other projects.

Next goals:
- Finish classical PID controller
- Create an RL controller for cart-pole
- Finish SAC policy
- Design an interface to plug and play my personally implemented models