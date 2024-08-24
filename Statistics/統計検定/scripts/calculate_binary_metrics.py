from enum import Enum
from math import sqrt
from pathlib import Path
from scipy import stats
import yaml
from pydantic import BaseModel
import polars as pl
import patito


class TestType(Enum):
    two_sided = "two_sided"
    greater = "greater"
    less = "less"


class BinaryMetricResult(BaseModel):
    metric_name: str
    result_file_path: str
    variant_column_name: str
    denominator_column_name: str
    numerator_column_name: str
    control_variant_name: str
    treatment_variant_names: list[str]
    test_type: TestType = TestType.greater


class StatisticalTestRecord(patito.Model):
    test_name: str
    control_mean: str
    treatment_mean: str
    relative_metric_change: str
    p_value: str
    is_significant: str

    @classmethod
    def column_name_map(cls):
        return {
            "test_name": "検定名",
            "control_mean": "現行パターン",
            "treatment_mean": "テストパターン",
            "relative_metric_change": "相対的な変化量",
            "p_value": "p値",
            "is_significant": "有意差",
        }


def load_metrics_from_yaml(yaml_file: str) -> list[BinaryMetricResult]:
    with open(yaml_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        return [
            BinaryMetricResult(**metric) for metric in data["binary_metrics_results"]
        ]


def main(result: BinaryMetricResult) -> pl.DataFrame:
    # データを読み込む
    result_df = pl.read_csv(result.result_file_path)
    print(result_df)
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
    z_test_type="weighted_mean",
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

    print(f"{control_mean=}, {control_denominator=}")
    print(f"{treatment_mean=}, {treatment_denominator=}")

    p_value, is_significant = _run_z_test(
        control_mean=control_mean,
        treatment_mean=treatment_mean,
        control_sample_size=control_denominator,
        treatment_sample_size=treatment_denominator,
    )

    return StatisticalTestRecord(
        test_name=f"{metric_name} ({control_variant_name} vs {treatment_variant_name})",
        control_mean=f"{control_mean * 100:.2f}％ ({control_numerator}/{control_denominator})",
        treatment_mean=f"{treatment_mean * 100:.2f}％ ({treatment_numerator}/{treatment_denominator})",
        relative_metric_change=(
            f"{treatment_mean / control_mean:.3f}倍" if control_mean != 0 else "-"
        ),
        p_value=f"{p_value:.3f}",
        is_significant="有意" if is_significant else "-",
    )


def _run_z_test(
    control_mean: float,
    treatment_mean: float,
    control_sample_size: int,
    treatment_sample_size: int,
    acceptable_false_positive_rate: float = 0.05,
    test_typ: TestType = TestType.greater,
) -> tuple[float, bool]:
    """treatment_meanがcontrol_meanよりも大きいかどうかを検定する片側検定を行う"""
    control_std = (control_mean * (1 - control_mean) / control_sample_size) ** 0.5
    treatment_std = (
        treatment_mean * (1 - treatment_mean) / treatment_sample_size
    ) ** 0.5

    z_value = (treatment_mean - control_mean) / sqrt(
        control_std**2 + treatment_std**2
    )  # 観測結果 (treatment_mean - control_mean)を、標準正規分布に従うように変換した値
    print(f"{z_value=}")
    print(f"{stats.norm.cdf(z_value)=}")

    if test_typ == TestType.greater:
        p_value = 1 - stats.norm.cdf(z_value)
    elif test_typ == TestType.less:
        p_value = stats.norm.cdf(z_value)
    elif test_typ == TestType.two_sided:
        # 標準正規分布の両側で、z_valueよりも確率の低い値が出る累積確率質量を計算
        p_value = (1 - stats.norm.cdf(z_value)) + (stats.norm.cdf(-z_value))
    is_significant = p_value < acceptable_false_positive_rate
    return p_value, is_significant


def _run_z_test_weighted_mean_ver(
    control_mean: float,
    treatment_mean: float,
    control_sample_size: int,
    treatment_sample_size: int,
    acceptable_false_positive_rate: float = 0.05,
    test_typ: TestType = TestType.greater,
) -> tuple[float, bool]:
    weighted_mean = (
        control_sample_size * control_mean + treatment_sample_size * treatment_mean
    ) / (control_sample_size + treatment_sample_size)

    z_value = (treatment_mean - control_mean) / sqrt(
        weighted_mean
        * (1 - weighted_mean)
        * (1 / control_sample_size + 1 / treatment_sample_size)
    )
    print(f"{z_value=}")

    if test_typ == TestType.greater:
        p_value = 1 - stats.norm.cdf(z_value)
    elif test_typ == TestType.less:
        p_value = stats.norm.cdf(z_value)
    elif test_typ == TestType.two_sided:
        # 標準正規分布の両側で、z_valueよりも確率の低い値が出る累積確率質量を計算
        p_value = (1 - stats.norm.cdf(z_value)) + (stats.norm.cdf(-z_value))

    is_significant = p_value < acceptable_false_positive_rate
    return p_value, is_significant


if __name__ == "__main__":
    yaml_file = Path("/Users/masato.morita/tmp/binary_metrics_results/config.yml")
    binary_metrics_results = load_metrics_from_yaml(yaml_file)

    test_result_df = pl.concat([main(result) for result in binary_metrics_results])

    # カラム名を日本語に変換
    test_result_df = test_result_df.rename(StatisticalTestRecord.column_name_map())
    print(test_result_df)
    test_result_df.write_csv(
        "/Users/masato.morita/tmp/binary_metrics_results/statistical_test_results.csv"
    )

    # # 二種類のz検定の結果を比較
    # control_mean = 0.0048
    # treatment_mean = 0.0053
    # control_sample_size = 132779
    # treatment_sample_size = 133315
    # p_value, is_significant = _run_z_test(
    #     control_mean,
    #     treatment_mean,
    #     control_sample_size,
    #     treatment_sample_size,
    #     test_typ=TestType.greater,
    # )
    # print(f"p_value: {p_value}, is_significant: {is_significant}")
    # # どちらの方法もほぼ同じ帰無分布 = ほぼ同じp値になるっぽい(小数点第4位くらいまで同じ)
    # p_value, is_significant = _run_z_test_weighted_mean_ver(
    #     control_mean,
    #     treatment_mean,
    #     control_sample_size,
    #     treatment_sample_size,
    #     test_typ=TestType.greater,
    # )
    # print(f"p_value: {p_value}, is_significant: {is_significant}")
