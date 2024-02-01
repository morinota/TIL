import math
from scipy.stats import norm


def calcurate_sample_size(
    control_ctr_expected: float,
    treatment_ctr_expected: float,
    statistical_power: float = 0.8,
    significance_level: float = 0.05,
) -> int:
    """ABテストにおけるサンプルサイズの設計。(片側検定を想定)
    CTRをprimary decision metricとして、click数が二項分布に従うと仮定した場合のサンプルサイズを算出する。
    Args:
        control_ctr_expected (float): コントロール群のCTRの期待値
        treatment_ctr_expected (float): トリートメント群のCTRの期待値
        statistical_power (float, optional): 統計的仮説検定の検出力. Defaults to 0.8.
        significance_level (float, optional): 統計的仮説検定の有意水準. Defaults to 0.05.
    Returns:
        int: 望ましいサンプルサイズ (単位: 人)
    """
    # 二項検定の検定統計量 z値の算出
    z_alpha = norm.ppf(1 - significance_level)  # これはなに?= 有意水準を下回るz値の境界値を算出
    z_beta = norm.ppf(statistical_power)  # これはなに?= 検出力を下回るz値の境界値を算出

    # effect sizeの算出
    effect_size = abs(treatment_ctr_expected - control_ctr_expected)

    # 両variantのCTRの平均値(=二項分布のparameter p)の算出
    pooled_ctr = (control_ctr_expected + treatment_ctr_expected) / 2
    # 両variantのCTRの標準偏差(二項分布の標準偏差の式)
    std_ctr = math.sqrt(2 * pooled_ctr * (1 - pooled_ctr))  # 二項分布の標準偏差

    # サンプルサイズの算出
    sample_size = (z_alpha * std_ctr + z_beta * std_ctr) ** 2 / effect_size**2  # 両variantのサンプルサイズの合計
    return math.ceil(sample_size)  # 小数点以下切り上げて返す


if __name__ == "__main__":
    control_ctr_mean_expected = 0.20
    treatment_ctr_mean_expected = 0.22
    statistical_power = 0.8
    significance_level = 0.05

    sample_size = calcurate_sample_size(
        control_ctr_mean_expected,
        treatment_ctr_mean_expected,
        statistical_power,
        significance_level,
    )
    print(f"サンプルサイズ: {sample_size}人")
