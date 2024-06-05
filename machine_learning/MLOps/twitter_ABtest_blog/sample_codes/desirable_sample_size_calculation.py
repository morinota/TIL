import numpy as np
from alternative_hypothesis_type import AlternativeHypothesisType
from normal_distribution import ProbabilityDistribution
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
        for sample_size in range(100, 10**10, 100):
            null_dist = self._create_null_distribution(control_metric_mean, sample_size)
            alternative_dist = self._create_alternative_distribution(
                control_metric_mean,
                treatment_metric_mean,
                sample_size,
            )
            power = calculate_statistical_power(
                null_dist,
                alternative_dist,
                self.significance_level,
                self.alternative_type,
            )
            if power >= self.desirable_power:
                return sample_size
        else:
            raise ValueError(
                "The desirable sample size is not found. expected effect size is too small."
            )

    def _create_null_distribution(
        self,
        control_metric_mean: float,
        n: int,
    ) -> ProbabilityDistribution:
        null_mean = control_metric_mean - control_metric_mean
        null_std = np.sqrt(2 * control_metric_mean * (1 - control_metric_mean) / n)
        return ProbabilityDistribution(null_mean, null_std)

    def _create_alternative_distribution(
        self,
        control_metric_mean: float,
        treatment_metric_mean: float,
        n: int,
    ) -> ProbabilityDistribution:
        alternative_mean = treatment_metric_mean - control_metric_mean
        alternative_std = np.sqrt(
            treatment_metric_mean * (1 - treatment_metric_mean) / n
            + control_metric_mean * (1 - control_metric_mean) / n
        )
        return ProbabilityDistribution(alternative_mean, alternative_std)


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

        for sample_size in range(100, 10**10, 100):
            null_dist = self._create_null_distribution(
                control_metric_mean,
                metric_variance,
                sample_size,
            )
            alternative_dist = self._create_alternative_distribution(
                control_metric_mean,
                treatment_metric_mean,
                metric_variance,
                sample_size,
            )
            power = calculate_statistical_power(
                null_dist,
                alternative_dist,
                self.significance_level,
                AlternativeHypothesisType.GREATER_THAN,
            )
            if power >= self.desirable_power:
                return sample_size
        else:
            raise ValueError(
                "The desirable sample size is not found. Please re-design the experiment."
            )

    def _create_null_distribution(
        self,
        control_metric_mean: float,
        metric_variance: float,
        n: int,
    ) -> ProbabilityDistribution:
        null_mean = control_metric_mean - control_metric_mean
        null_std = np.sqrt(2 * metric_variance / n)
        return ProbabilityDistribution(null_mean, null_std)

    def _create_alternative_distribution(
        self,
        control_metric_mean: float,
        treatment_metric_mean: float,
        metric_variance: float,
        n: int,
    ) -> ProbabilityDistribution:
        alternative_mean = treatment_metric_mean - control_metric_mean
        alternative_std = np.sqrt(2 * metric_variance / n)
        return ProbabilityDistribution(alternative_mean, alternative_std)
