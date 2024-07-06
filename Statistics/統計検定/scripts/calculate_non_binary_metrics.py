from pathlib import Path
from scipy import stats
from pydantic import BaseModel
import polars as pl
import yaml
import patito


class NonBinaryMetricResult(BaseModel):
    metric_name: str
    result_file_path: str
    variant_column_name: str
    sample_size_column_name: str
    mean_column_name: str
    variance_column_name: str
    control_variant_name: str
    treatment_variant_names: list[str]


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


def load_metrics_from_yaml(yaml_file: str) -> list[NonBinaryMetricResult]:
    with open(yaml_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        return [
            NonBinaryMetricResult(**metric)
            for metric in data["non_binary_metrics_results"]
        ]


def main(result: NonBinaryMetricResult) -> pl.DataFrame:
    # データを読み込む
    result_df = pl.read_csv(result.result_file_path)

    test_results = [
        run_t_test_ver2(
            result.metric_name,
            result.control_variant_name,
            treatment_variant,
            result_df,
            result,
        )
        for treatment_variant in result.treatment_variant_names
    ]

    return pl.DataFrame(test_results)


def run_t_test_ver2(
    metric_name: str,
    control_variant_name: str,
    treatment_variant_name: str,
    result_df: pl.DataFrame,
    result: NonBinaryMetricResult,
) -> StatisticalTestRecord:
    # control_variant, treatment_variantのデータを取得
    control = result_df.filter(
        pl.col(result.variant_column_name) == control_variant_name
    )
    treatment = result_df.filter(
        pl.col(result.variant_column_name) == treatment_variant_name
    )

    # 各variantのデータの平均値、分散、サンプルサイズをdfから取得
    control_mean = control.select(result.mean_column_name).to_series().to_list()[0]
    control_var = control.select(result.variance_column_name).to_series().to_list()[0]
    control_sample_size = (
        control.select(result.sample_size_column_name).to_series().to_list()[0]
    )
    treatment_mean = treatment.select(result.mean_column_name).to_series().to_list()[0]
    treatment_var = (
        treatment.select(result.variance_column_name).to_series().to_list()[0]
    )
    treatment_sample_size = (
        treatment.select(result.sample_size_column_name).to_series().to_list()[0]
    )

    # t-testを実行
    p_value, is_significant = _run_t_test_ver2(
        control_mean,
        control_var,
        control_sample_size,
        treatment_mean,
        treatment_var,
        treatment_sample_size,
    )

    return StatisticalTestRecord(
        test_name=f"{metric_name} ({control_variant_name} vs {treatment_variant_name})",
        control_mean=f"{control_mean:.3f} (± {control_var ** 0.5:.3f})",
        treatment_mean=f"{treatment_mean:.3f} (± {treatment_var ** 0.5:.3f})",
        relative_metric_change=f"{treatment_mean / control_mean:.3f}倍",
        p_value=f"{p_value:.2f}",
        is_significant="有意" if is_significant else "-",
    )


def _run_t_test_ver2(
    mean1: float,
    var1: float,
    n1: int,
    mean2: float,
    var2: float,
    n2: int,
) -> tuple[float, bool]:
    # t-testを実行
    acceptable_false_positive_rate = 0.05
    t_stat, p_value = stats.ttest_ind_from_stats(
        mean1, var1, n1, mean2, var2, n2, equal_var=False
    )
    is_significant = p_value < acceptable_false_positive_rate

    return p_value, is_significant


def _calc_percentage_diff(control_val: float, treatment_val: float) -> float:
    diff = treatment_val - control_val
    return diff / control_val * 100


if __name__ == "__main__":
    yaml_path = Path("/tmp/non_binary_metrics_results/non_binary_metrics_results.yml")
    non_binary_metrics_results = load_metrics_from_yaml(yaml_path)
    test_result_df = pl.concat([main(result) for result in non_binary_metrics_results])

    # カラム名を日本語に変換
    test_result_df = test_result_df.rename(StatisticalTestRecord.column_name_map())
    test_result_df.write_csv("/tmp/non_binary_metrics_test_results.csv")
    print(test_result_df)
