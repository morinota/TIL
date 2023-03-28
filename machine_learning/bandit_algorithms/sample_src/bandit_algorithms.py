import abc
import random
from dataclasses import dataclass
from math import log, log2, sqrt
from typing import List

import numpy as np


@dataclass
class Arm:
    _reward: int


class AbstractBanditAlgorithm(abc.ABC):
    def __init__(
        self,
        arms_counts: List[int] = [],
        arms_ave_rewards: List[float] = [],
    ) -> None:
        self.arms_counts = arms_counts
        self.arms_ave_rewards = arms_ave_rewards

    @property
    def total_reward(self) -> float:
        return sum([count * ave_reward for count, ave_reward in zip(self.arms_counts, self.arms_ave_rewards)])

    def initialize(self, num_arms: int) -> None:
        # NOTE: 選択肢(arms)の数で初期化する.(constructerとの違いは,rewardログの有無)
        self.arms_counts = [0] * num_arms
        self.arms_ave_rewards = [0.0] * num_arms

    @abc.abstractmethod
    def select_arm(self) -> int:
        """t回目のarmを選ぶ試行"""
        raise NotImplementedError

    def update(self, chosed_arm_idx: int, reward: float) -> None:
        """t回目のactionとrewardを受け取り、propertyを更新."""
        self.arms_counts[chosed_arm_idx] = self.arms_counts[chosed_arm_idx] + 1
        arm_i_count = self.arms_counts[chosed_arm_idx]
        old_ave_reward = self.arms_ave_rewards[chosed_arm_idx]
        new_ave_reward = (old_ave_reward * (arm_i_count - 1) + reward) / arm_i_count
        self.arms_ave_rewards[chosed_arm_idx] = new_ave_reward

    @staticmethod
    def get_index_having_max_value(values: List[float]) -> int:
        """値のListに対して、最大の要素のindexを返す"""
        return max(enumerate(values), key=lambda idx_and_value: idx_and_value[1])[0]


class RandomSelect(AbstractBanditAlgorithm):
    def __init__(
        self,
        arms_counts: List[int] = [],
        arms_ave_rewards: List[float] = [],
    ) -> None:
        super().__init__(arms_counts, arms_ave_rewards)

    def initialize(self, num_arms: int) -> None:
        super().initialize(num_arms)

    def select_arm(self) -> int:
        chosen_arm_idx = random.randint(0, len(self.arms_ave_rewards) - 1)
        return chosen_arm_idx

    def update(self, chosed_arm_idx: int, reward: float) -> None:
        super().update(chosed_arm_idx, reward)


class EpsilonGreedy(AbstractBanditAlgorithm):
    def __init__(
        self,
        arms_counts: List[int] = [],
        arms_ave_rewards: List[float] = [],
        epsilon: float = 0.5,
    ) -> None:
        super().__init__(arms_counts, arms_ave_rewards)
        if not (0 <= epsilon <= 1):
            raise ValueError("please set epsilon between 0 ~ 1")
        self.epsilon = epsilon

    def initialize(
        self,
        num_arms: int,
        epsilon: float = 0.5,
    ) -> None:
        super().initialize(num_arms)
        self.epsilon = epsilon

    def select_arm(self) -> int:
        """試行毎にexploration(探索)/exploitation(活用)を決定した上で、armを選択する."""
        is_exploration = bool(int(np.random.binomial(n=1, p=self.epsilon)))

        if is_exploration:
            chosen_arm_idx = random.randint(0, len(self.arms_ave_rewards) - 1)
        else:
            chosen_arm_idx = self.get_index_having_max_value(values=self.arms_ave_rewards)
        return chosen_arm_idx

    def update(self, chosed_arm_idx: int, reward: float) -> None:
        super().update(chosed_arm_idx, reward)


class UpperConfidenceBase(AbstractBanditAlgorithm):
    """以下, UCBの考え:
    - 累積報酬を最大化する為には...最適なarmを多く引く事が重要.
    ただ選択回数が少ないarmについては、報酬が正確に推定できてない可能性(arm毎のスコアの不確実性)を考慮する必要がある.
    - UCBでは、armを選択する際に毎回以下の式で表されるスコア$\bar{\mu}_i(t)$を算出. 最もスコアの高いarmを引く.
        - $\hat{\mu}_i(t)$: 時刻tのarm iの(報酬の?)標本平均.
        - $\sqrt{\frac{\log t}{2 N_i(t)}}$: 選択回数に関する補正項
        - 選択スコア $\bar{\mu}_i(t) = 標本平均 + 補正項$
    - つまり、単純に標本平均の大きなarmが選択される時は**活用**が行われ、標本平均は小さいが、選択回数が少ないarmが選択される時は**探索**が行なわれていると解釈できる.
    - UCBでは探索と活用のバランスを上手く取りながらarmの選択を行い、報酬の最大化を目指す.
    """

    def select_arm(self) -> int:
        t = sum(self.arms_counts)  # 初期値はt=0とする.
        reg_terms = [self._calc_reg_term(arm_idx, t) for arm_idx in range(len(self.arms_counts))]
        scores = [ave_reward + reg_term for ave_reward, reg_term in zip(self.arms_ave_rewards, reg_terms)]

        return self.get_index_having_max_value(scores)

    def update(self, chosed_arm_idx: int, reward: float) -> None:
        return super().update(chosed_arm_idx, reward)

    def _calc_reg_term(self, arm_idx: int, t: int) -> float:
        log_t = np.log(t + 1)
        N_i_t = self.arms_counts[arm_idx]
        # TODO: N_i_t = 0のケースの対応を追加する必要あり.(暫定で+1)
        return np.sqrt(log_t / (2 * N_i_t + 1))


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
    num_trial = 1000
    sample_trial_datasets: List[List[float]] = [
        [random.gauss(mu=arm_mean_reward, sigma=1.0) for arm_mean_reward in arms_mean_rewards] for _ in range(num_trial)
    ]
    bandit_algorithms: List[AbstractBanditAlgorithm] = [
        RandomSelect(),
        EpsilonGreedy(),
        UpperConfidenceBase(),
    ]
    for bandit_algo in bandit_algorithms:
        bandit_trial(bandit_algo, num_arms, sample_trial_datasets)


if __name__ == "__main__":
    main()
