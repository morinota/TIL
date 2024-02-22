from normal_distribution import NormalDistribution
from typing import Literal, Optional

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
