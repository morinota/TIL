import numpy as np
from utils.alternative_hypothesis_type import AlternativeHypothesisType
from utils.normal_distribution import ProbabilityDistribution
from utils.statistical_power_calculation import calculate_statistical_power


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
        for sample_size in range(100, 10**6, 10000):
            null_dist = self._create_null_distribution(control_metric_mean, sample_size)
            print(
                "「treatmentに効果がない」という仮説が正しい場合の、観測値の確率分布を計算しました。"
            )
            alternative_dist = self._create_alternative_distribution(
                control_metric_mean,
                treatment_metric_mean,
                sample_size,
            )
            print(
                f"「treatmentに+{treatment_metric_mean - control_metric_mean}の効果がある」という仮説が正しい場合の、観測値の確率分布を計算しました。"
            )
            power = calculate_statistical_power(
                null_dist,
                alternative_dist,
                self.significance_level,
                self.alternative_type,
            )
            print(
                f"サンプルサイズが {sample_size} の場合の、効果量 {treatment_metric_mean - control_metric_mean} に対する検出力は {power} です。"
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

        for sample_size in range(100, 10**7, 10000):
            null_dist = self._create_null_distribution(
                control_metric_mean,
                metric_variance,
                sample_size,
            )
            print(
                f"「treatmentに効果がない」という仮説が正しい場合の、観測値の確率分布を計算しました。"
            )
            alternative_dist = self._create_alternative_distribution(
                control_metric_mean,
                treatment_metric_mean,
                metric_variance,
                sample_size,
            )
            print(
                f"「treatmentに+{treatment_metric_mean - control_metric_mean}の効果がある」という仮説が正しい場合の、観測値の確率分布を計算しました。"
            )
            power = calculate_statistical_power(
                null_dist,
                alternative_dist,
                self.significance_level,
                AlternativeHypothesisType.GREATER_THAN,
            )
            print(
                f"サンプルサイズが {sample_size} の場合の、効果量 {treatment_metric_mean - control_metric_mean} に対する検出力は {power} です。"
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
