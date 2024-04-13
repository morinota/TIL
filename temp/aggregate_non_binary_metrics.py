from pathlib import Path
import pandas as pd
from scipy import stats


def calc_percentage_diff(control_val: float, treatment_val: float) -> float:
    diff = treatment_val - control_val
    return diff / control_val * 100


def run_t_test(
    sample_df: pd.DataFrame,
    metric_col: str,
    variant_col: str,
) -> None:
    # variantカラムが示すユーザグループに基づいてデータを分割
    control = sample_df[sample_df[variant_col] == "EXISTING"][metric_col]
    treatment = sample_df[sample_df[variant_col] == "SHOW_FEATURE_TREND_NEWS_5"][
        metric_col
    ]

    # t-testを実行
    acceptable_false_positive_rate = 0.05
    t_stat, p_value = stats.ttest_ind(control, treatment, equal_var=False)
    is_significant = p_value < acceptable_false_positive_rate

    control_mean = control.mean()
    treatment_mean = treatment.mean()

    # 結果を出力
    print(f"============={metric_col}============")
    print(
        f"control: mean={control.mean()}, sample_size={len(control)}, sample_std={control.std()}"
    )
    print(
        f"treatment: mean={treatment.mean()}, sample_size={len(treatment)}, sample_std={treatment.std()}"
    )
    print(
        f"p-value0={p_value}, is_significant={is_significant} (acceptable_false_positive_rate={acceptable_false_positive_rate})"
    )
    print(f"absolute_diff = {treatment_mean - control_mean:.2f}")
    print(f"relative_metric_change = {treatment_mean / control_mean:.2f}倍")
    percentage_diff = calc_percentage_diff(control_mean, treatment_mean)
    if percentage_diff > 0:
        print(f"percentage_diff = +{percentage_diff:.2f}%")
    else:
        print(f"percentage_diff = {percentage_diff:.2f}%")


def main(data_path: Path) -> None:
    # データを読み込む
    sample_df = pd.read_csv(data_path)

    # t-testを実行
    run_t_test(sample_df, "unique_news_count", "pattern")


if __name__ == "__main__":
    exsisting_users_read_news_count_path = "average_read_news_count_exsisting_user.csv"
    exsisting_users_read_premiun_news_count_path = (
        "average_read_premium_news_count_exsisting_user.csv"
    )
    new_users_read_news_count_path = "average_read_news_count_new_user.csv"
    main(exsisting_users_read_news_count_path)
    main(exsisting_users_read_premiun_news_count_path)
    main(new_users_read_news_count_path)
