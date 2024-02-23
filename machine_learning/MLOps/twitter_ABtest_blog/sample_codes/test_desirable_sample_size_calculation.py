from desirable_sample_size_calculation import (
    DesirableSampleSizeSimulatorWithBinaryMetric,
    DesirableSampleSizeSimulatorWithNonBinaryMetric,
)


def test_desirable_sample_size_calculation_with_binary_metric() -> None:
    # Arrange
    control_metric_mean = 0.1
    treatment_metric_mean = 0.12
    significance_level = 0.05  # i.e. acceptable false positive rate
    desirable_power = 0.8
    sut = DesirableSampleSizeSimulatorWithBinaryMetric(
        significance_level,
        desirable_power,
    )

    # Act
    desirable_sample_size_actual = sut.calculate(
        control_metric_mean,
        treatment_metric_mean,
    )

    # Assert
    assert desirable_sample_size_actual == 10000


def test_desirable_sample_size_calculation_with_non_binary_metric() -> None:
    control_metric_mean = 0.1
    treatment_metric_mean = 0.12
    metric_variance = 0.05
    significance_level = 0.05
    desirable_power = 0.8
    sut = DesirableSampleSizeSimulatorWithNonBinaryMetric(
        significance_level,
        desirable_power,
    )

    # Act
    desirable_sample_size_actual = sut.calculate(
        control_metric_mean,
        treatment_metric_mean,
        metric_variance,
    )
    assert desirable_sample_size_actual == 10000
