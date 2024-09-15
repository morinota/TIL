import numpy as np
from loguru import logger
from scipy.stats import norm


class Runner:
    def __init__(self, p0: float, p1_list: list[float], alpha: float, beta: float, num_simulations: int):
        """シミュレーションの初期化"""
        self.p0 = p0
        self.p1_list = p1_list
        self.alpha = alpha
        self.beta = beta
        self.num_simulations = num_simulations

    def run(self) -> None:
        """シミュレーションを実行し、結果を表示する"""
        for p1 in self.p1_list:
            # 固定サンプルサイズの計算
            m = self._calculate_fixed_sample_size(p1)
            # シミュレーションの実行
            sample_sizes, outcomes = self._simulate_sprt(p1, m)
            # 統計量の計算
            mean_n, std_n, power = self._calculate_statistics(sample_sizes, outcomes)
            # 結果のログ出力
            logger.info(f"対立仮説 p1 = {p1}")
            logger.info(f"固定サンプルサイズ m = {m}")
            logger.info(f"平均終了回数: {mean_n:.2f}")
            logger.info(f"終了回数の標準偏差: {std_n:.2f}")
            logger.info(f"実際の検出力: {power:.4f}\n")

    def _calculate_fixed_sample_size(self, p1: float) -> int:
        """固定サンプルサイズを計算する"""
        q0 = 1 - self.p0
        q1 = 1 - p1
        Z_alpha = norm.ppf(1 - self.alpha)
        Z_beta = norm.ppf(1 - self.beta)
        numerator = (Z_alpha * np.sqrt(self.p0 * q0) + Z_beta * np.sqrt(p1 * q1)) ** 2
        denominator = (p1 - self.p0) ** 2
        m = int(np.ceil(numerator / denominator))
        return m

    def _calculate_sprt_boundaries(self) -> tuple[float, float]:
        """SPRTの境界値を計算する"""
        a = np.log(self.beta / (1 - self.alpha))
        b = np.log((1 - self.beta) / self.alpha)
        return a, b

    def _simulate_sprt(self, p1: float, m: int) -> tuple[list[int], list[str]]:
        """SPRTのシミュレーションを実行する"""
        a, b = self._calculate_sprt_boundaries()
        s = np.log(p1 / self.p0)  # 成功時の対数尤度比
        f = np.log((1 - p1) / (1 - self.p0))  # 失敗時の対数尤度比

        sample_sizes: list[int] = []
        outcomes: list[str] = []

        for _ in range(self.num_simulations):
            LLR = 0  # 対数尤度比の初期化
            n = 0
            while n < m:
                n += 1
                # p1に基づくベルヌーイ試行
                X = np.random.rand() < p1
                # 対数尤度比の更新
                LLR += s if X else f
                # 境界値との比較
                if LLR >= b:
                    # 帰無仮説を棄却
                    sample_sizes.append(n)
                    outcomes.append("Reject H0")
                    break
                elif LLR <= a:
                    # 帰無仮説を採択
                    sample_sizes.append(n)
                    outcomes.append("Accept H0")
                    break
            else:
                # 最大サンプルサイズに達した場合
                sample_sizes.append(n)
                outcomes.append("Accept H0")  # 未決定の場合は帰無仮説を採択

        return sample_sizes, outcomes

    def _calculate_statistics(self, sample_sizes: list[int], outcomes: list[str]) -> tuple[float, float, float]:
        """結果の統計量を計算する"""
        mean_n = np.mean(sample_sizes)
        std_n = np.std(sample_sizes)
        power = outcomes.count("Reject H0") / len(outcomes)
        return mean_n, std_n, power


def main() -> None:
    # シミュレーション条件
    alpha = 0.05  # 第一種の誤り
    beta = 0.20  # 第二種の誤り
    p0 = 0.95  # 帰無仮説の母比率
    p1_list = [0.96, 0.94, 0.99, 0.90]  # 対立仮説の母比率
    num_simulations = 10000  # シミュレーション回数

    # Runnerクラスのインスタンスを作成し、シミュレーションを実行
    runner = Runner(p0, p1_list, alpha, beta, num_simulations)
    runner.run()


if __name__ == "__main__":
    main()
