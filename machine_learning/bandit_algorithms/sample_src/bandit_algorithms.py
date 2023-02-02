import abc
import random
from dataclasses import dataclass
from typing import List

import numpy as np
from sympy import Abs


@dataclass
class Arm:
    _reward: int


class AbstractAlgorithm(abc.ABC):
    @abc.abstractmethod
    def __init__(self, arms_counts: List[int], arms_ave_rewards: List[float]) -> None:
        self.arms_counts = arms_counts
        self.arms_ave_rewards = arms_ave_rewards

    @abc.abstractproperty
    def total_rewards(self) -> float:
        return sum([count * ave_reward for count, ave_reward in zip(self.arms_counts, self.arms_ave_rewards)])

    @abc.abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def select_arm(self) -> int:
        """t回目のarmを選ぶ試行"""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, choses_arm: int, reward: int) -> None:
        """t回目の試行で選んだarmのrewardに基づいて、情報を更新する"""
        raise NotImplementedError


class RandomSelect(AbstractAlgorithm):
    def __init__(
        self,
        arms_counts: List[int] = [],
        arms_ave_rewards: List[float] = [],
    ) -> None:
        self.arms_counts = arms_counts
        self.arms_ave_rewards = arms_ave_rewards

    @property
    def total_rewards(self) -> float:
        return sum([count * ave_reward for count, ave_reward in zip(self.arms_counts, self.arms_ave_rewards)])

    def initialize(self, n_arms: int) -> None:
        self.arms_counts = [0] * n_arms
        self.arms_ave_rewards = [0.0] * n_arms

    def select_arm(self) -> int:
        chosen_arm_idx = random.randint(0, len(self.arms_ave_rewards) - 1)
        return chosen_arm_idx

    def update(self, chosed_arm_idx: int, reward: float) -> None:
        self.arms_counts[chosed_arm_idx] = self.arms_counts[chosed_arm_idx] + 1
        arm_i_count = self.arms_counts[chosed_arm_idx]
        old_ave_reward = self.arms_ave_rewards[chosed_arm_idx]
        new_ave_reward = (old_ave_reward * (arm_i_count - 1) + reward) / arm_i_count
        self.arms_ave_rewards[chosed_arm_idx] = new_ave_reward


class EpsilonGreedy(AbstractAlgorithm):
    pass


def main() -> None:
    num_arms = 3
    arms_mean_rewards = [random.uniform(0, 1) for _ in range(num_arms)]
    num_trial = 10
    sample_trial_datasets: List[List[float]] = [
        [random.gauss(mu=arm_mean_reward, sigma=1.0) for arm_mean_reward in arms_mean_rewards] for _ in range(num_trial)
    ]
    bandit_algo = RandomSelect()
    bandit_algo.initialize(num_arms)
    for trial_dataset in sample_trial_datasets:
        chosed_arm_idx = bandit_algo.select_arm()
        bandit_algo.update(chosed_arm_idx, reward=trial_dataset[chosed_arm_idx])

    print(bandit_algo.total_rewards)


if __name__ == "__main__":
    main()
