from collections import defaultdict

import numpy as np
from contextual_bandit_interface import Arm, Context, ContextualBanditInterface


class LinUCB(ContextualBanditInterface):
    def __init__(self, alpha: float, arms: list[Arm]) -> None:
        self.alpha = alpha

    def select_arm(self) -> Arm:
        pass


class LinUCBController:
    def __init__(self) -> None:
        self.A_a_by_arm: dict[Arm, np.ndarray]
        self.B_a_by_arm: dict[Arm, np.ndarray]

    def run(self, alpha: float) -> None:
        time_steps = 10
        for t in range(time_steps):
            p_t_by_arm: dict[Arm, float] = defaultdict()
            arms: list[Arm] = collect_arms()
            context_by_arm: dict[Arm, np.ndarray] = collect_contexs(arms)
            for a in arms:
                x_t_a = context_by_arm[a]
                if a.is_new():
                    self.A_a_by_arm[a] = init_A_a()
                    self.B_a_by_arm[a] = init_b_a()
                A_a, B_a = self.A_a_by_arm[a], self.B_a_by_arm[a]
                hat_param_a = np.linalg.inv(A_a) * B_a
                reward_hat = hat_param_a.T * x_t_a
                reward_std = np.sqrt(x_t_a.T * np.linalg.inv(A_a) * x_t_a)
                p_t_a = reward_hat + alpha * reward_hat
                p_t_by_arm[a] = float(p_t_a)

            a_t = self._select_arm_t(p_t_by_arm)
            r_t = self._observe_reward()
            self._update_A_a(a_t, r_t)
            self._update_b_a(a_t, r_t)

    def _select_arm_t(self, p_t_by_arm: dict[Arm, float]) -> Arm:
        """alphaが大きい程、報酬の推定値の分散が大きい = 未知なアイテムを探索的に選択しやすい??"""
        return max(p_t_by_arm, key=lambda x: p_t_by_arm.get(x))

    def _observe_reward(self) -> float:
        pass

    def _update_A_a(
        self,
        selected_arm: Arm,
        reward: float,
        context_a_t: np.ndarray,
    ) -> None:
        A_a_t = self.A_a_by_arm[selected_arm]
        A_a_t_updated = A_a_t + context_a_t * context_a_t.T
        self.A_a_by_arm[selected_arm] = A_a_t_updated

    def _update_b_a(
        self,
        selected_arm: Arm,
        reward: float,
        context_a_t: np.ndarray,
    ) -> None:
        B_a_t = self.B_a_by_arm[selected_arm]
        B_a_t_updated = B_a_t + reward * context_a_t
        self.B_a_by_arm[selected_arm] = B_a_t_updated
