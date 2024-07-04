from pathlib import Path
from scipy import stats
import yaml
from pydantic import BaseModel
import polars as pl
import patito


class BinaryMetricResult(BaseModel):
    metric_name: str
    result_file_path: str
    variant_column_name: str
    denominator_column_name: str
    numerator_column_name: str
    control_variant_name: str
    treatment_variant_names: list[str]


class StatisticalTestRecord(patito.Model):
    test_name: str
    control_mean: str
    treatment_mean: str
    relative_metric_change: str
    percentage_diff: str
    absolute_diff: str
    p_value: str
    is_significant: str


def load_metrics_from_yaml(yaml_file: str) -> list[BinaryMetricResult]:
    with open(yaml_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        return [
            BinaryMetricResult(**metric) for metric in data["binary_metrics_results"]
        ]


def main(result: BinaryMetricResult) -> pl.DataFrame:
    # データを読み込む
    result_df = pl.read_csv(result.result_file_path)
    test_results = [
        run_z_test(
            result.metric_name,
            result.control_variant_name,
            treatment_variant,
            result_df,
            result,
        )
        for treatment_variant in result.treatment_variant_names
    ]
    return pl.DataFrame(test_results)


def run_z_test(
    metric_name: str,
    control_variant_name: str,
    treatment_variant_name: str,
    result_df: pl.DataFrame,
    result: BinaryMetricResult,
) -> StatisticalTestRecord:
    # controlとtreatmentのデータを取得
    control = result_df.filter(
        pl.col(result.variant_column_name) == control_variant_name
    )
    treatment = result_df.filter(
        pl.col(result.variant_column_name) == treatment_variant_name
    )

    # 各variantのデータの分母、分子を取得
    # (ここはnon binary metricと合わせて、平均と分散を取得するようにしてもいいかも?)
    control_denominator = (
        control.select(result.denominator_column_name).to_series().to_list()[0]
    )
    control_numerator = (
        control.select(result.numerator_column_name).to_series().to_list()[0]
    )
    treatment_denominator = (
        treatment.select(result.denominator_column_name).to_series().to_list()[0]
    )
    treatment_numerator = (
        treatment.select(result.numerator_column_name).to_series().to_list()[0]
    )
    control_mean = control_numerator / control_denominator
    treatment_mean = treatment_numerator / treatment_denominator

    p_value, is_significant = _run_z_test(
        control_mean=control_mean,
        treatment_mean=treatment_mean,
        control_sample_size=control_denominator,
        treatment_sample_size=treatment_denominator,
    )

    return StatisticalTestRecord(
        # test_name=f"{metric_name} ({control_variant_name} vs {treatment_variant_name})",
        test_name=f"{metric_name} ({control_variant_name} vs {treatment_variant_name})",
        control_mean=f"{control_mean:.4f}",
        treatment_mean=f"{treatment_mean:.4f}",
        relative_metric_change=(
            f"{treatment_mean / control_mean:.2f}倍" if control_mean != 0 else "-"
        ),
        percentage_diff=(
            f"{_calc_percentage_diff(control_mean, treatment_mean):.2f}％"
            if control_mean != 0
            else "-"
        ),
        absolute_diff=f"{treatment_mean - control_mean:.2f}",
        p_value=f"{p_value:.2f}",
        is_significant="有意" if is_significant else "-",
    )


def _calc_percentage_diff(control_val: float, treatment_val: float) -> float:
    diff = treatment_val - control_val
    return diff / control_val * 100


def _run_z_test(
    control_mean: float,
    treatment_mean: float,
    control_sample_size: int,
    treatment_sample_size: int,
    acceptable_false_positive_rate: float = 0.05,
) -> tuple[float, bool]:
    """treatment_meanがcontrol_meanよりも大きいかどうかを検定する片側検定を行う"""
    control_std = (control_mean * (1 - control_mean) / control_sample_size) ** 0.5
    treatment_std = (
        treatment_mean * (1 - treatment_mean) / treatment_sample_size
    ) ** 0.5
    z = (treatment_mean - control_mean) / (
        control_std**2 + treatment_std**2
    ) ** 0.5  # Z値(i.e. 標準正規分布に従うように)に変換した観測結果
    p_value = 1 - stats.norm.cdf(z)
    is_significant = p_value < acceptable_false_positive_rate
    return p_value, is_significant


if __name__ == "__main__":
    yaml_file = Path("Statistics/統計検定/scripts/binary_metrics_results.yml")
    binary_metrics_results = load_metrics_from_yaml(yaml_file)
    test_result_df = pl.concat([main(result) for result in binary_metrics_results])

    print(test_result_df)
    test_result_df.write_csv("/tmp/binary_metrics_test_results.csv")
