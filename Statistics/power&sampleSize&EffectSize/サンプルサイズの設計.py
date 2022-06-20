import math
from typing import List
from numpy import power
from scipy.stats import norm
from statsmodels.stats.power import normal_sample_size_one_tail
from scipy.stats import chi2, chi2_contingency
import pandas as pd


def sample_power_probtest(
    p1: float, p2: float, power: float = 0.8, sig: float = 0.05
) -> int:
    z_half_alpha = norm.isf([sig / 2])
    z_beta = -1 * norm.isf([power])
    p = (p1 + p2) / 2
    print(f"effect size is {p}")
    return math.ceil(
        (2 * p * (1 - p) * ((z_half_alpha + z_beta) ** 2)) / ((p1 - p2) ** 2)
    )


if __name__ == "__main__":
    p1 = 0.1
    p2 = 0.11
    # 理想的なサンプルサイズの算出
    sample_size = sample_power_probtest(p1, p2)
    # よってA/Bテストを仮定した場合、14752*2~29504人に無作為に施策AとBのいずれかを提示して、その結果に対し、検定を行えばよいことになる。
    print(sample_size * 2)
