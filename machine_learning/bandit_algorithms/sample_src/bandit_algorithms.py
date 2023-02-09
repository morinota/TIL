import abc
import random
from dataclasses import dataclass
from typing import List

import numpy as np


def get_index_having_max_value(values: List[float]) -> int:
    """値のListに対して、最大の要素のindexを返す"""
    return max(enumerate(values), key=lambda idx_and_value: idx_and_value[1])[0]


@dataclass
class Arm:
    _reward: int


class AbstractBanditAlgorithm(abc.ABC):
    def __init__(self, arms_counts: List[int], arms_ave_rewards: List[float]) -> None:
        self.arms_counts = arms_counts
        self.arms_ave_rewards = arms_ave_rewards

    @property
    def total_reward(self) -> float:
        return sum([count * ave_reward for count, ave_reward in zip(self.arms_counts, self.arms_ave_rewards)])

    @abc.abstractmethod
    def initialize(self, num_arms: int) -> None:
        # NOTE: 選択肢(arms)の数で初期化する.
        raise NotImplementedError

    @abc.abstractmethod
    def select_arm(self) -> int:
        """t回目のarmを選ぶ試行"""
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, choses_arm: int, reward: float) -> None:
        """t回目の試行で選んだarmのrewardに基づいて、情報を更新する"""
        raise NotImplementedError


class RandomSelect(AbstractBanditAlgorithm):
    def __init__(
        self,
        arms_counts: List[int] = [],
        arms_ave_rewards: List[float] = [],
    ) -> None:
        self.arms_counts = arms_counts
        self.arms_ave_rewards = arms_ave_rewards

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


class EpsilonGreedy(AbstractBanditAlgorithm):
    def __init__(
        self,
        arms_counts: List[int] = [],
        arms_ave_rewards: List[float] = [],
        epsilon: float = 0.5,
    ) -> None:
        if not (0 <= epsilon <= 1):
            raise ValueError("please set epsilon between 0 ~ 1")
        self.arms_counts = arms_counts
        self.arms_ave_rewards = arms_ave_rewards
        self.epsilon = epsilon

    def initialize(
        self,
        n_arms: int,
        epsilon: float = 0.5,
    ) -> None:
        self.arms_counts = [0] * n_arms
        self.arms_ave_rewards = [0.0] * n_arms
        self.epsilon = epsilon

    def select_arm(self) -> int:
        """試行毎にexploration(探索)/exploitation(活用)を決定した上で、armを選択する."""
        is_exploration = bool(int(np.random.binomial(n=1, p=self.epsilon)))

        if is_exploration:
            chosen_arm_idx = random.randint(0, len(self.arms_ave_rewards) - 1)
        else:
            chosen_arm_idx = get_index_having_max_value(values=self.arms_ave_rewards)
        return chosen_arm_idx

    def update(self, chosed_arm_idx: int, reward: float) -> None:
        self.arms_counts[chosed_arm_idx] = self.arms_counts[chosed_arm_idx] + 1
        arm_i_count = self.arms_counts[chosed_arm_idx]
        old_ave_reward = self.arms_ave_rewards[chosed_arm_idx]
        new_ave_reward = (old_ave_reward * (arm_i_count - 1) + reward) / arm_i_count
        self.arms_ave_rewards[chosed_arm_idx] = new_ave_reward


def bandit_trial(
    bandit_algo: AbstractBanditAlgorithm,
    num_arms: int,
    sample_trial_datasets: List[List[float]],
) -> None:
    bandit_algo.initialize(num_arms)
    for trial_dataset in sample_trial_datasets:
        chosed_arm_idx = bandit_algo.select_arm()
        bandit_algo.update(chosed_arm_idx, reward=trial_dataset[chosed_arm_idx])

    print(bandit_algo.total_reward)


def main():
    num_arms = 3
    arms_mean_rewards = [random.uniform(0, 1) for _ in range(num_arms)]
    num_trial = 10
    sample_trial_datasets: List[List[float]] = [
        [random.gauss(mu=arm_mean_reward, sigma=1.0) for arm_mean_reward in arms_mean_rewards] for _ in range(num_trial)
    ]
    bandit_algorithms = [RandomSelect(), EpsilonGreedy()]
    for bandit_algo in bandit_algorithms:
        bandit_trial(bandit_algo, num_arms, sample_trial_datasets)


if __name__ == "__main__":
    main()
