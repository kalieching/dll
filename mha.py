import torch
import torch.nn as nn
import torch.nn.functional as F

class MultiHeadAttention():
    def __init__(self, d_model, num_heads):
        # assert that d_model is divisible by number of heads
        assert d_model % num_heads == 0

        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # projection matrices for queries, keys, and values
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)

    def _split(self, x):
        NotImplementedError("This method will be implemented to split the data into multiple heads")

    def _merge(self, x):
        NotImplementedError("This method will be implemented to merge the data from multiple heads back into original shape")

    def scaled_dot_product(self, Q, K, V, mask=None):
        similarity_scores = torch.matmul(Q, K.transpose(-2, -1)) / torch.sqrt(torch.tensor(self.d_k, dtype=torch.float32))
        if mask is not None:
            similarity_scores = similarity_scores.masked_fill(mask == 0, float("-inf"))
        weights = F.softmax(similarity_scores, dim=-1)
        return torch.matmul(weights, V)
