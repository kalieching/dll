
class ReplayBuffer:
    def __init__(self, obs_dim, act_dim, max_size=int(1e6)):
        self.max_size = max_size