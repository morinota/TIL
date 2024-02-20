from logging import critical
from typing import Literal, Callable, Optional
from scipy.stats import norm
import numpy as np


class NormalDistribution:
    def __init__(self, mean: float, std: float):
        self.mean = mean
        self.std = std
        self.dist = norm(loc=mean, scale=std)

    def pdf(self, x: float) -> float:
        """probability density function"""
        return self.dist.pdf(x)

    def cdf(self, x: float) -> float:
        """cumulative distribution function"""
        return self.dist.cdf(x)

    def ppf(self, q: float) -> float:
        """percent point function(累積分布関数の逆関数)"""
        return self.dist.ppf(q)


def calculate_statistical_power(
    null_distribution: NormalDistribution,
    alternative_distribution: NormalDistribution,
    acceptable_false_positive_rate: float = 0.05,
    alternative_type: Literal["two-sided", "larger", "smaller"] = "larger",
) -> float:
    """
    Calculate statistical power.
    args:
        null_distribution: NormalDistribution
            Null distribution. パラメータを固定された確率変数の確率分布オブジェクト
        alternative_distribution: NormalDistribution
            Alternative distribution. パラメータを固定された確率変数の確率分布オブジェクト
        acceptable_false_positive_rate: float
            Acceptable false positive rate.
        alternative: Literal["two-sided", "larger", "smaller"]
            Alternative hypothesis.
    return:
        statistical_power: float
            Statistical power.
    """
    # rejection regionを算出
    left_critical_value, right_critical_value = _get_rejection_region(
        null_distribution, acceptable_false_positive_rate, alternative_type
    )

    # 対立分布のうちrejection regionに含まれる部分の面積を算出
    true_positive_area = 0
    if left_critical_value:
        true_positive_area += alternative_distribution.cdf(left_critical_value)
    if right_critical_value:
        true_positive_area += 1 - alternative_distribution.cdf(right_critical_value)

    # statistical powerを算出
    return true_positive_area / 1


def _get_rejection_region(
    null_distribution: NormalDistribution,
    acceptable_false_positive_rate: float,
    alternative_type: Literal["two-sided", "larger", "smaller"],
) -> tuple[Optional[float], Optional[float]]:
    """critical valueのタプルを返す
    - 片側検定の場合は片方のみの値が入る
    """
    assert 0 < acceptable_false_positive_rate < 1

    if alternative_type == "two-sided":
        return (
            null_distribution.ppf(acceptable_false_positive_rate / 2),
            null_distribution.ppf(1 - acceptable_false_positive_rate / 2),
        )

    if alternative_type == "larger":
        return (None, null_distribution.ppf(1 - acceptable_false_positive_rate))

    return (null_distribution.ppf(acceptable_false_positive_rate), None)


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
    print(f"null_dist: mean={null_dist_mean}, std={null_dist_std}")
    alternative_dist_mean = 0.64
    alternative_dist_std = np.sqrt(0.64 * (1 - 0.64) / n)
    alternative_distribution = NormalDistribution(mean=alternative_dist_mean, std=alternative_dist_std)
    print(f"alternative_dist: mean={alternative_dist_mean}, std={alternative_dist_std}")
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
