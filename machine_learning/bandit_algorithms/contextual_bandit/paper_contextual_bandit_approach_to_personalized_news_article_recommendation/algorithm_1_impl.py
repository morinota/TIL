from collections import defaultdict
from operator import inv
from typing import Any

import numpy as np


class LinUCBDisjoint:
    def __init__(self, alpha: float, dimension: int) -> None:
        self.alpha = alpha
        self.d = dimension
        self.D_a_by_arm = defaultdict()  # training input : D_a in R^{m * d}
        self.A_a_by_arm: dict[Any, np.ndarray] = defaultdict()  # A_a := D_{a}^T D_{a} + I_{d}
        self.b_a_by_arm: dict[Any, np.ndarray] = defaultdict()  # b_a := D_{a}^T * responce_vector(c_{a})

    def run(self, T: int) -> None:
        for t in range(1, T + 1):
            # Observe features of all arms a in A_t: x_{t,a} in R^{d}
            A_t = self._fetch_item_pool(t)
            context_a_t_of: dict[Any, np.ndarray] = self._observe_context_of_items(A_t)

            theta_a_hat_of: dict[Any, np.ndarray] = defaultdict()
            payoff_hat_of: dict[Any, float] = defaultdict()
            for a in A_t:
                if self._is_new_arm(a):
                    # initialize A_a and b_a
                    self.A_a_by_arm[a] = np.identity(self.d)
                    self.b_a_by_arm[a] = np.zeros(self.d)
                # update parameter & estimate payoff expectation
                theta_a_hat_of[a] = self.A_a_by_arm[a] ** (-1) * self.b_a_by_arm[a]
                payoff_hat_of[a] = theta_a_hat_of[a] + self.alpha * np.sqrt(
                    context_a_t_of[a].T * np.linalg.inv(self.A_a_by_arm[a]) * context_a_t_of[a]
                )

            # choose a_{t} and observe a real-valud payoff r_{t}
            a_t = self._select_arm()
            r_t = self._observe_real_valued_payoff(a_t)
            # update A_a and b_a
            self.A_a_by_arm[a_t] = self.A_a_by_arm[a_t] + context_a_t_of[a_t] * context_a_t_of[a_t].T
            self.b_a_by_arm[a_t] = self.b_a_by_arm[a_t] + r_t * context_a_t_of[a_t]

    def _fetch_item_pool(self, trial_idx: int) -> set[Any]:
        """get item pool of trial t: A_t"""
        pass

    def _observe_context_of_items(self, items: set[Any]) -> dict:
        """各a in items の x_{t,a} を観測する"""
        pass

    def _is_new_arm(self, item: Any) -> bool:
        pass

    def _select_arm(self) -> Any:
        pass

    def _observe_real_valued_payoff(self, selected_arm: Any) -> Any:
        pass
