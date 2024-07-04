import numpy as np

N = 500  # 行動空間のサイズ
K = 5
ACTIONS = list([str(num) for num in range(1, N)])
# 数字が小さいアクションほど、特徴量が大きくなるように設定
ACTION_FEATURE_MAP = {str(a): N * 1.1 - float(a) for a in ACTIONS}


class ScoreFunction:
    def __init__(self) -> None:
        # スコアをキャッシュするための辞書
        self.action_feature_score_map = {}

    def __call__(self, feature: float, action: str) -> float:
        if (feature, action) in self.action_feature_score_map.keys():
            return self.action_feature_score_map[(feature, action)]

        score = 1 + feature + ACTION_FEATURE_MAP[action]
        self.action_feature_score_map[(feature, action)] = score
        return score


def plackett_luce_sampling(f_theta: ScoreFunction, x: float) -> list[str]:
    """
    PLモデルに基づくランキングの確率的サンプリング
    """
    action_space = ACTIONS.copy()

    # 確率的にランキング作成
    ranking = []
    for k in range(K):
        # k番目のポジションに提示するアイテムを選択
        a_k = _plackett_luce_choice(f_theta, x, action_space)
        ranking.append(a_k)

        # 選択されたアイテム a_k を行動集合から削除
        action_space.remove(a_k)

    return ranking


def _plackett_luce_choice(
    f_theta: ScoreFunction,
    x: float,
    actions: list[str],
) -> str:
    """
    PLモデルに基づく選択
    """
    # 各アクションのスコアを計算
    scores = np.array([f_theta(x, a) for a in actions])

    # softmax関数を用いて確率質量関数を計算 (これを毎回やるのがボトルネック!)
    pmf = np.exp(scores) / np.sum(np.exp(scores))

    # 確率質量分布から1件サンプリングして返す
    return np.random.choice(actions, p=pmf)


def gumbel_softmax_trick_sampling(f_theta: ScoreFunction, x: float) -> list[str]:
    """
    Gumbel-Softmaxトリックで高速化した、PLモデルによるランキングを生成する
    """
    action_space = ACTIONS.copy()

    scores = np.array([f_theta(x, a) for a in action_space])
    # scoresと同じ長さの乱数を、標準Gumbel分布からサンプリング
    gumbel_noises = np.random.gumbel(size=len(action_space), loc=0, scale=1)

    perturbed_scores = scores + gumbel_noises  # perturbedの意味=「わからない」
    ## np.argsortは配列の要素を昇順のインデックスを返すので、-1をかけて降順にする
    ranking = [a for a in np.array(action_space)[np.argsort(-perturbed_scores)]]
    return ranking[:K]


if __name__ == "__main__":

    # naiveなPLモデルに基づくランキングの確率的サンプリング
    print(plackett_luce_sampling(f_theta=ScoreFunction(), x=10.0))

    # Gumbel-Softmaxトリックで高速化したPLモデルに基づくランキングの確率的サンプリング
    print(gumbel_softmax_trick_sampling(f_theta=ScoreFunction(), x=10.0))
