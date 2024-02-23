from typing import Literal, Optional
from scipy.stats import norm
import numpy as np
from alternative_hypothesis_type import (
    AlternativeHypothesisType,
)
from normal_distribution import NormalDistribution
from statistical_power_calculation import calculate_statistical_power


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
    alternative_type = AlternativeHypothesisType.GREATER_THAN

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
