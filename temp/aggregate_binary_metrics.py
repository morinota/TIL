import dataclasses
from scipy import stats


@dataclasses.dataclass
class BinaryMetricResult:
    metric_name: str
    control_denominator: int
    control_numerator: int
    treatment_denominator: int
    treatment_numerator: int


def calc_percentage_diff(control_val: float, treatment_val: float) -> float:
    diff = treatment_val - control_val
    return diff / control_val * 100


def run_z_test(
    control_mean: float,
    treatment_mean: float,
    control_sample_size: int,
    treatment_sample_size: int,
    acceptable_false_positive_rate: float = 0.05,
) -> bool:
    """treatment_meanがcontrol_meanよりも大きいかどうかを検定する片側検定を行う"""
    control_std = (control_mean * (1 - control_mean) / control_sample_size) ** 0.5
    treatment_std = (
        treatment_mean * (1 - treatment_mean) / treatment_sample_size
    ) ** 0.5
    z = (treatment_mean - control_mean) / (
        control_std**2 + treatment_std**2
    ) ** 0.5  # Z値(i.e. 標準正規分布に従うように)に変換した観測結果
    p_value = 1 - stats.norm.cdf(z)
    return p_value < acceptable_false_positive_rate


def main(binary_metric_results: list[BinaryMetricResult]) -> None:
    for binary_metric_result in binary_metric_results:
        control_mean = (
            binary_metric_result.control_numerator
            / binary_metric_result.control_denominator
        )
        treatment_mean = (
            binary_metric_result.treatment_numerator
            / binary_metric_result.treatment_denominator
        )
        is_significant = run_z_test(
            control_mean,
            treatment_mean,
            binary_metric_result.control_denominator,
            binary_metric_result.treatment_denominator,
        )
        percentage_diff = calc_percentage_diff(control_mean, treatment_mean)
        print(f"============={binary_metric_result.metric_name}============")
        print(
            f"現行パターン: {control_mean * 100:.2f}%\n({binary_metric_result.control_numerator}人/{binary_metric_result.control_denominator}人)"
        )
        print(
            f"テストパターン: {treatment_mean * 100:.2f}%\n({binary_metric_result.treatment_numerator}人/{binary_metric_result.treatment_denominator}人)"
        )
        print(f"absolute_diff = {treatment_mean - control_mean:.2f}")
        print(f"relative_metric_change = {treatment_mean / control_mean:.2f}倍")
        if percentage_diff > 0:
            print(f"percentage_diff = +{percentage_diff:.2f}%")
        else:
            print(f"percentage_diff = {percentage_diff:.2f}%")
        print(
            f"統計的仮説検定による判定(有意水準5%): is_significant = {is_significant}"
        )


if __name__ == "__main__":
    new_results = [
        BinaryMetricResult("メインフィードからの課金率", 39465, 29, 39578, 25),
        BinaryMetricResult(
            "枠1(話題のニュース1vs話題のニュース1)のタップ率 (全ユーザ)",
            14279,
            1874,
            14387,
            1888,
        ),
        BinaryMetricResult(
            "枠1(話題のニュース1vs話題のニュース1)のタップ率 (有料ユーザのみ)",
            1228,
            284,
            999,
            132,
        ),
        BinaryMetricResult(
            "枠1(話題のニュース1vs話題のニュース1)のタップ率 (無料ユーザのみ)",
            13059,
            1594,
            13399,
            1757,
        ),
        BinaryMetricResult(
            "枠2(ビジネスvs話題のニュース2)のタップ率 (全ユーザ)",
            8134,
            1259,
            9818,
            1174,
        ),
        BinaryMetricResult(
            "枠2(ビジネスvs話題のニュース2)のタップ率 (有料ユーザのみ)",
            806,
            141,
            707,
            99,
        ),
        BinaryMetricResult(
            "枠2(ビジネスvs話題のニュース2)のタップ率 (無料ユーザのみ)",
            7330,
            1118,
            9116,
            1075,
        ),
        BinaryMetricResult(
            "枠3(テクノロジーvs話題のニュース3)のタップ率 (全ユーザ)",
            4126,
            473,
            7224,
            907,
        ),
        BinaryMetricResult(
            "枠3(テクノロジーvs話題のニュース3)のタップ率 (有料ユーザのみ)",
            448,
            56,
            545,
            94,
        ),
        BinaryMetricResult(
            "枠3(テクノロジーvs話題のニュース3)のタップ率 (無料ユーザのみ)",
            3678,
            417,
            6681,
            813,
        ),
        BinaryMetricResult(
            "枠4(金融経済vs話題のニュース4)のタップ率 (全ユーザ)",
            6092,
            691,
            5505,
            686,
        ),
        BinaryMetricResult(
            "枠4(金融経済vs話題のニュース4)のタップ率 (有料ユーザのみ)",
            593,
            75,
            417,
            70,
        ),
        BinaryMetricResult(
            "枠4(金融経済vs話題のニュース4)のタップ率 (無料ユーザのみ)",
            5499,
            616,
            5089,
            616,
        ),
    ]
    main(new_results)
