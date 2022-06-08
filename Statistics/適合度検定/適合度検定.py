from typing import List
import scipy as sp
from scipy.stats import chi2


def calcurate_chi_squared(observed: List[int], ideal: List[int]) -> float:

    chi_squared = 0
    for i in range(7):

        temp = (observed[i] - ideal[i]) ** 2 / ideal[i]
        chi_squared += temp

    return chi_squared


def main():
    observed = [25, 12, 15, 22, 14, 26, 26]  # 得られた観測値
    ideal = [20] * 7  # 理想的な分布

    # 観測値から計算される検定統計量を取得
    chi_squared_observed = calcurate_chi_squared(observed, ideal)
    print(f"chi_squared_observed is {chi_squared_observed}")

    # 有意水準の設定
    alpha = 0.05
    # 自由度
    freedom = len(observed) - 1

    # カイ二乗分布の累積確率から、横軸の値を求める
    rejection_boundly = chi2.ppf(q=1 - alpha, df=freedom)
    print(rejection_boundly)
    if chi_squared_observed >= rejection_boundly:
        print("帰無仮説を棄却。対立仮説を採択")
    else:
        print("帰無仮説を棄却できない。")


if __name__ == "__main__":
    main()
