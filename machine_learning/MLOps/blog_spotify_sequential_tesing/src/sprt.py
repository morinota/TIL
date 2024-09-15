import numpy as np
from loguru import logger
from scipy.stats import norm


class Runner:
    def __init__(
        self,
        p0: float,
        p1_list: list[float],
        alpha: float,
        beta: float,
        num_simulations: int,
    ):
        """シミュレーションの初期化"""
        self._p0 = p0
        self._p1_list = p1_list
        self._alpha = alpha
        self._beta = beta
        self._num_simulations = num_simulations

    def run(self) -> None:
        """シミュレーションを実行し、結果を表示する"""
        results = []

        for p1 in self._p1_list:
            n_fixed = self._calculate_fixed_sample_size_non_sequential(p1)
            m = self._calculate_fixed_sample_size_sprt(p1)
            sample_sizes, outcomes = self._simulate_sprt(p1, m)
            stats = self._calculate_statistics(sample_sizes, outcomes, n_fixed)
            result = {
                "p1": p1,
                "mean_n": stats["mean_n"],
                "std_n": stats["std_n"],
                "n_fixed": n_fixed,
                "reduction_rate": stats["reduction_rate"],
                "power": stats["power"],
                "proportion_exceed_n_fixed": stats["proportion_exceed_n_fixed"],
            }
            results.append(result)
            logger.info(f"対立仮説 p1 = {p1}")
            logger.info(f"終了回数平均値: {stats['mean_n']:.2f}")
            logger.info(f"終了回数標準偏差: {stats['std_n']:.2f}")
            logger.info(f"固定サンプルサイズ: {n_fixed}")
            logger.info(f"削減率: {stats['reduction_rate']:.2f}%")
            logger.info(f"検出力: {stats['power']:.4f}")
            logger.info(f"固定サンプルサイズ超え割合: " f"{stats['proportion_exceed_n_fixed']:.4f}\n")

        logger.info("結果のまとめ：")
        headers = [
            "対立仮説",
            "終了回数平均値",
            "終了回数標準偏差",
            "固定サンプルサイズ",
            "削減率",
            "検出力",
            "固定サンプルサイズ超え割合",
        ]
        logger.info("\t".join(headers))
        for res in results:
            logger.info(
                f"{res['p1']}\t"
                f"{int(res['mean_n'])}\t"
                f"{int(res['std_n'])}\t"
                f"{res['n_fixed']}\t"
                f"{res['reduction_rate']:.0f}%\t"
                f"{res['power']:.4f}\t"
                f"{res['proportion_exceed_n_fixed']:.4f}"
            )

    def _calculate_fixed_sample_size_non_sequential(self, p1: float) -> int:
        """固定サンプルサイズ（通常の仮説検定）を計算する"""
        z_alpha = norm.ppf(1 - self._alpha)
        z_beta = norm.ppf(1 - self._beta)
        numerator = (z_alpha * np.sqrt(self._p0 * (1 - self._p0)) + z_beta * np.sqrt(p1 * (1 - p1))) ** 2
        denominator = (p1 - self._p0) ** 2
        n_fixed = int(np.ceil(numerator / denominator))
        return n_fixed

    def _calculate_fixed_sample_size_sprt(self, p1: float) -> int:
        """SPRTのサンプルサイズ上限を計算する"""
        z_alpha = norm.ppf(1 - self._alpha)
        z_beta = norm.ppf(1 - self._beta)
        numerator = (z_alpha * np.sqrt(self._p0 * (1 - self._p0)) + z_beta * np.sqrt(p1 * (1 - p1))) ** 2
        denominator = (p1 - self._p0) ** 2
        m = int(np.ceil(numerator / denominator))
        return m

    def _calculate_sprt_boundaries(self) -> tuple[float, float]:
        """SPRTの境界値を計算する"""
        a = np.log(self._beta / (1 - self._alpha))
        b = np.log((1 - self._beta) / self._alpha)
        return a, b

    def _simulate_sprt(self, p1: float, m: int) -> tuple[list[int], list[str]]:
        """SPRTのシミュレーションを実行する"""
        a, b = self._calculate_sprt_boundaries()
        s = np.log(p1 / self._p0)  # 成功時の対数尤度比
        f = np.log((1 - p1) / (1 - self._p0))  # 失敗時の対数尤度比

        sample_sizes: list[int] = []
        outcomes: list[str] = []

        for _ in range(self._num_simulations):
            llr = 0  # 対数尤度比の初期化
            n = 0
            while n < m:
                n += 1
                x = np.random.rand() < p1
                llr += s if x else f
                if llr >= b:
                    sample_sizes.append(n)
                    outcomes.append("Reject H0")
                    break
                elif llr <= a:
                    sample_sizes.append(n)
                    outcomes.append("Accept H0")
                    break
            else:
                sample_sizes.append(n)
                outcomes.append("Accept H0")  # 未決定の場合は帰無仮説を採択

        return sample_sizes, outcomes

    def _calculate_statistics(self, sample_sizes: list[int], outcomes: list[str], n_fixed: int) -> dict:
        """結果の統計量を計算する"""
        mean_n = np.mean(sample_sizes)
        std_n = np.std(sample_sizes)
        power = outcomes.count("Reject H0") / len(outcomes)
        reduction_rate = (1 - mean_n / n_fixed) * 100
        proportion_exceed_n_fixed = sum(1 for n in sample_sizes if n >= n_fixed) / len(sample_sizes)
        return {
            "mean_n": mean_n,
            "std_n": std_n,
            "power": power,
            "reduction_rate": reduction_rate,
            "proportion_exceed_n_fixed": proportion_exceed_n_fixed,
        }


def main() -> None:
    """メイン関数"""
    alpha = 0.05  # 第一種の誤り
    beta = 0.20  # 第二種の誤り
    p0 = 0.95  # 帰無仮説の母比率
    # 対立仮説の母比率(ex. 新しいモデルの精度期待値などのイメージ...!)
    p1_list = [0.96, 0.94, 0.99, 0.90]
    num_simulations = 10_000  # シミュレーション回数

    runner = Runner(p0, p1_list, alpha, beta, num_simulations)
    runner.run()


if __name__ == "__main__":
    main()
