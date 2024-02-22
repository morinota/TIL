from typing import Literal, Optional
from scipy.stats import norm
import numpy as np

from normal_distribution import NormalDistribution
from statistical_power_calculation import calculate_statistical_power





# higher-order function ver.
# def _get_rejection_region(
#     null_distribution: NormalDistribution,
#     acceptable_false_positive_rate: float,
#     alternative_type: Literal["two-sided", "larger", "smaller"],
# ) -> Callable[[float], bool]:
#     """確率変数の値がrejection regionに含まれるかどうかを判定する関数を返す"""

#     assert 0 < acceptable_false_positive_rate < 1

#     if alternative_type == "two-sided":
#         return lambda x: (x < null_distribution.ppf(acceptable_false_positive_rate / 2)) or (
#             x > null_distribution.ppf(1 - acceptable_false_positive_rate / 2)
#         )
#     if alternative_type == "larger":
#         return lambda x: x > null_distribution.ppf(1 - acceptable_false_positive_rate)

#     return lambda x: x < null_distribution.ppf(acceptable_false_positive_rate)


def test_calculate_statistical_power() -> None:
    # Arrange
    n = 100

    null_dist_mean = 0.5
    null_dist_std = np.sqrt(0.5 * (1 - 0.5) / n)
    null_distribution = NormalDistribution(mean=null_dist_mean, std=null_dist_std)
    
    alternative_dist_mean = 0.64
    alternative_dist_std = np.sqrt(0.64 * (1 - 0.64) / n)
    alternative_distribution = NormalDistribution(mean=alternative_dist_mean, std=alternative_dist_std)
    
    acceptable_false_positive_rate = 0.05
    alternative_type = "larger"

    # Act
    actual_statistical_power = calculate_statistical_power(
        null_distribution,
        alternative_distribution,
        acceptable_false_positive_rate,
        alternative_type,
    )

    # Assert
    expected_statistical_power = 0.886
    assert np.isclose(actual_statistical_power, expected_statistical_power, atol=0.01)

    # サンプルサイズの公式(van Belle, 2002, significance level=0.05, power=0.8)
    n
