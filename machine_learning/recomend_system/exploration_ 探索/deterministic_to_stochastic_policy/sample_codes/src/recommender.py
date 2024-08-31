import numpy as np
from models import InferenceType
from type_aliases import UserId, MovieId, Vector, PreferenceScore


class Recommender:
    def __init__(
        self,
        user_vectors: dict[UserId, Vector],
        movie_vectors: dict[MovieId, Vector],
    ):
        self.user_vectors = user_vectors
        self.movie_vectors = movie_vectors

    def predict(
        self, user_id: UserId, k: int, inference_type: InferenceType
    ) -> list[tuple[MovieId, PreferenceScore]]:
        """ユーザベクトルとコンテンツベクトルの内積をpreference scoreとして算出し、降順にk個のコンテンツを返す
        - 内積計算は、コンテンツベクトル集合をmatrixとして扱い、ユーザベクトルとの行列積を計算することで一括計算する
        """
        user_vector = self.user_vectors.get(user_id)
        if user_vector is None:
            raise ValueError(f"user embeddings not found for user_id: {user_id}")

        if inference_type == InferenceType.STOCHASTIC_PLACKETT_LUCE:
            return self._stochastic_predict_with_plackett_luce(user_vector, k)
        elif inference_type == InferenceType.STOCHASTIC_PLACKETT_LUCE_CACHED:
            return self._stochastic_predict_with_plackett_luce_cached(user_vector, k)
        elif inference_type == InferenceType.STOCHASTIC_GUMBEL_SOFTMAX_TRICK:
            return self._stochastic_predict_with_gumbel_softmax_trick(user_vector, k)
        elif inference_type == InferenceType.STOCHASTIC_EPSILON_GREEDY:
            return self._stochastic_predict_with_epsilon_greedy(user_vector, k)
        elif inference_type == InferenceType.DETERMINISTIC:
            return self._deterministic_predict(user_vector, k)
        else:
            raise ValueError(f"unsupported inference type: {inference_type}")

    def _deterministic_predict(
        self, user_vector: Vector, k: int
    ) -> list[tuple[MovieId, PreferenceScore]]:
        """決定的な推薦を行う"""
        preference_score_by_id = self._calc_preference_scores(user_vector)

        # preference scoreの降順にk個のコンテンツを決定的に返す
        top_k_content_id_scores = sorted(
            preference_score_by_id.items(),
            key=lambda id_score: id_score[1],
            reverse=True,
        )[:k]
        return top_k_content_id_scores

    def _stochastic_predict_with_plackett_luce(
        self, user_vector: Vector, k: int, temperature: float = 1.0
    ) -> list[tuple[MovieId, PreferenceScore]]:
        """プラケット・ルースモデルを用いた確率的推薦を行う"""
        preference_score_by_id = self._calc_preference_scores(user_vector)
        candidates = list(preference_score_by_id.keys())
        ranking = []
        for i in range(1, k + 1):
            # ソフトマックス関数を使って確率質量関数(probability mass function)を計算
            pmf = np.exp(
                [preference_score_by_id[id] / temperature for id in candidates]
            ) / np.sum(
                np.exp([preference_score_by_id[id] / temperature for id in candidates])
            )
            # 確率分布に基づいてi番目のポジションの推薦アイテムを選択
            a_i = np.random.choice(candidates, p=pmf)
            ranking.append((a_i, preference_score_by_id[a_i]))

            # 選択されたアイテム a_i を行動集合candidatesから削除
            candidates.remove(a_i)
        return ranking

    def _stochastic_predict_with_plackett_luce_cached(
        self, user_vector: Vector, k: int, temperature: float = 1.0
    ) -> list[tuple[MovieId, PreferenceScore]]:
        """プラケット・ルースモデルを用いた確率的推薦を行う（キャッシュあり）"""
        preference_score_by_id = self._calc_preference_scores(user_vector)
        candidates = list(preference_score_by_id.keys())
        ranking = []

        # 各アイテムのpreference scoreを指数関数の値を事前に計算してキャッシュする
        exponential_score_by_id = {
            movie_id: np.exp(score) / temperature
            for movie_id, score in preference_score_by_id.items()
        }

        for i in range(1, k + 1):
            # ソフトマックス関数を使って確率質量関数(probability mass function)を計算
            pmf = np.array([exponential_score_by_id[id] for id in candidates]) / np.sum(
                [exponential_score_by_id[id] for id in candidates]
            )

            # 確率分布に基づいてi番目のポジションの推薦アイテムを選択
            a_i = np.random.choice(candidates, p=pmf)
            ranking.append((a_i, preference_score_by_id[a_i]))

            # 選択されたアイテム a_i を行動集合candidatesから削除
            candidates.remove(a_i)
        return ranking

    def _stochastic_predict_with_gumbel_softmax_trick(
        self, user_vector: Vector, k: int, temperature: float = 1.0
    ) -> list[tuple[MovieId, PreferenceScore]]:
        """Gumbel Softmax Trickを用いた確率的推薦を行う"""
        preference_score_by_id = self._calc_preference_scores(user_vector)
        # scoresと同じ長さの乱数を、標準Gumbel分布からサンプリング
        gumbel_noises = np.random.gumbel(
            size=len(preference_score_by_id), loc=0.0, scale=1.0
        )

        perturbed_score_by_id = {
            movie_id: score + noise
            for (movie_id, score), noise in zip(
                preference_score_by_id.items(), gumbel_noises
            )
        }
        # 摂動されたpreference scoreの降順にk個のコンテンツを返す
        top_k_content_id_scores = sorted(
            perturbed_score_by_id.items(),
            key=lambda id_score: id_score[1],
            reverse=True,
        )[:k]
        return top_k_content_id_scores

    def _stochastic_predict_with_epsilon_greedy(
        self, user_vector: Vector, k: int, epsilon: float = 0.1
    ) -> list[tuple[MovieId, PreferenceScore]]:
        """ε-greedy法を用いた確率的推薦を行う"""
        preference_score_by_id = self._calc_preference_scores(user_vector)
        candidates = list(preference_score_by_id.keys())
        ranking = []

        for i in range(1, k + 1):
            # 確率 epsilon で探索(ランダムに推薦アイテムを選択)
            if np.random.rand() < epsilon:
                a_i = np.random.choice(candidates)
            # 確率 1-epsilon で活用(最適なアイテムを選択)
            else:
                # cantidatesから最もpreference scoreが高いアイテムを選択
                a_i = max(candidates, key=lambda id: preference_score_by_id[id])

            ranking.append((a_i, preference_score_by_id[a_i]))
            # 選択されたアイテム a_i を行動集合candidatesから削除
            candidates.remove(a_i)
        return ranking

    def _calc_preference_scores(
        self, user_vector: np.ndarray
    ) -> dict[MovieId, PreferenceScore]:
        """ユーザベクトルとコンテンツベクトルの内積を使ってpreference scoreを計算する"""
        movie_vectors_array = np.array(list(self.movie_vectors.values()))
        preference_scores = np.dot(user_vector, movie_vectors_array.T)
        return dict(zip(self.movie_vectors.keys(), preference_scores))
