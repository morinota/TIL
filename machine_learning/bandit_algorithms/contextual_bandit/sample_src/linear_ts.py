import numpy as np
import polars as pl


class LinTS:
    def __init__(self, v: float) -> None:
        self.v = v  # ノイズの分散パラメータ
        self.A: np.ndarray = None  # 全アーム共通のパラメータ行列
        self.b: np.ndarray = None  # 全アーム共通のパラメータベクトル
        self.is_fitted = False

    def fit(self, train_df: pl.DataFrame) -> None:
        """バンディットモデルをフィットする

        Args:
            data: カラム [user_context, arm_context, reward] を含むDataFrame
        """
        for row in train_df.iter_rows(named=True):
            user_context = np.array(row["user_context"])
            arm_context = np.array(row["arm_context"])
            reward = row["reward"]

            # user_contextとarm_contextを結合
            combined_context = np.concatenate([user_context, arm_context])

            if self.A is None:
                d = len(combined_context)
                self.A = np.eye(d)
                self.b = np.zeros(d)

            # パラメータを更新
            self.A += np.outer(combined_context, combined_context)
            self.b += reward * combined_context

        self.is_fitted = True

    def sample(self, context_df: pl.DataFrame, action_df: pl.DataFrame) -> pl.DataFrame:
        """Thompson Samplingで最適なアームを選択

        Args:
            context_df: カラム [user_context] を含むDataFrame（複数のtrialに対応）
            action_df: カラム [arm_id, arm_context] を含むDataFrame（候補アーム一覧）

        Returns:
            カラム [trial_id, arm_id, estimated_reward] を含むDataFrame（各trialで選択されたアーム）
        """
        if not self.is_fitted:
            raise ValueError("モデルがフィットされていません")

        results = []

        # 各コンテキスト（trial）に対してアーム選択を実行
        for trial_id, context_row in enumerate(context_df.iter_rows(named=True)):
            user_context = np.array(context_row["user_context"])

            # パラメータを一度サンプリング（全アーム共通）
            A_inv = np.linalg.inv(self.A)
            mu_hat = A_inv @ self.b
            Sigma_hat = self.v * A_inv
            theta_tilde = np.random.multivariate_normal(mu_hat, Sigma_hat)

            arm_rewards = {}
            for action_row in action_df.iter_rows(named=True):
                arm_id = action_row["arm_id"]
                arm_context = np.array(action_row["arm_context"])

                # user_contextとarm_contextを結合
                combined_context = np.concatenate([user_context, arm_context])

                # サンプルしたパラメータで報酬を推定
                estimated_reward = theta_tilde @ combined_context
                arm_rewards[arm_id] = estimated_reward

            # 最大報酬のアームを選択
            selected_arm = max(arm_rewards, key=arm_rewards.get)
            selected_reward = arm_rewards[selected_arm]

            results.append({"trial_id": trial_id, "arm_id": selected_arm, "estimated_reward": selected_reward})

        return pl.DataFrame(results)


if __name__ == "__main__":
    # 使用例
    import numpy as np

    # サンプルデータ作成
    n_samples = 100
    data = []
    for i in range(n_samples):
        user_context = np.random.randn(3).tolist()  # 3次元のユーザーコンテキスト
        arm_context = np.random.randn(2).tolist()  # 2次元のアームコンテキスト
        reward = np.random.randn()  # ランダム報酬
        data.append({"user_context": user_context, "arm_context": arm_context, "reward": reward})

    train_data = pl.DataFrame(data)
    print(f"{train_data=}")

    # モデル学習
    model = LinTS(v=0.1)
    model.fit(train_data)

    # モデルパラメータ確認
    print(f"モデルパラメータ A.shape: {model.A.shape}")
    print(f"モデルパラメータ b.shape: {model.b.shape}")

    # ユーザーコンテキストデータ（現在の状況）
    context_data = []
    for i in range(3):
        context_data.append({"user_context": np.random.randn(3).tolist()})
    context_df = pl.DataFrame(context_data)
    print(f"{context_df=}")

    # アクションデータ（候補アーム一覧）
    action_data = []
    for i in range(3):  # 3つのアーム候補
        action_data.append({"arm_id": f"arm_{i}", "arm_context": np.random.randn(2).tolist()})
    action_df = pl.DataFrame(action_data)
    print(f"{action_df=}")

    # Thompson Samplingでアーム選択
    result = model.sample(context_df, action_df)
    print(f"選択されたアーム: {result}")
