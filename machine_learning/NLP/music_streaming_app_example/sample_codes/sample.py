import abc


class EnvironmentInterface(abc.ABC):
    @abc.abstractmethod
    def reacts(self):
        raise NotImplementedError

    @abc.abstractmethod
    def best_actions(self):
        raise NotImplementedError


class ContexualEnviromnent:
    def __init__(self, user_features, n_recs):
        self.user_features = user_features
        self.n_recs = n_recs

    def reacts(self):
        """Computes expected reward for each user given their recommendations"""
