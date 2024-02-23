from typing import Literal

import numpy as np
from alternative_hypothesis_type import AlternativeHypothesisType
from normal_distribution import NormalDistribution
from statistical_power_calculation import calculate_statistical_power


class DesirableSampleSizeSimulatorWithBinaryMetric:
    def __init__(
        self,
        significance_level: float = 0.05,
        desirable_power: float = 0.8,
        alternative_type: AlternativeHypothesisType = AlternativeHypothesisType.GREATER_THAN,
    ) -> None:
        self.significance_level = significance_level
        self.desirable_power = desirable_power
        self.alternative_type = alternative_type

    def calculate(
        self,
        control_metric_mean: float,
        treatment_metric_mean: float,
    ) -> int:

        for sample_size in range(10**10):
            power = self._calculate_power(
                control_metric_mean,
                treatment_metric_mean,
                sample_size,
            )

    def _calculate_power(
        self,
        control_metric_mean: float,
        treatment_metric_mean: float,
        n: int,
    ) -> float:
        # null distributionを作る
        null_mean = 0.0
        null_std = np.sqrt(2 * control_metric_mean * (1 - control_metric_mean) / n)
        null_dist = NormalDistribution(null_mean, null_std)

        # alternative distributionを作る
        alternative_mean = treatment_metric_mean - control_metric_mean
        alternative_std = np.sqrt(
            treatment_metric_mean * (1 - treatment_metric_mean) / n
            + control_metric_mean * (1 - control_metric_mean) / n
        )
        alternative_dist = NormalDistribution(alternative_mean, alternative_std)

        return calculate_statistical_power(
            null_dist,
            alternative_dist,
            self.significance_level,
            self.alternative_type,
        )


class DesirableSampleSizeSimulatorWithNonBinaryMetric:
    def __init__(
        self,
        significance_level: float = 0.05,
        desirable_power: float = 0.8,
    ) -> None:
        self.significance_level = significance_level
        self.desirable_power = desirable_power

    def calculate(
        self,
        control_metric_mean: float,
        treatment_metric_mean: float,
        metric_variance: float,
    ) -> int:
        pass
