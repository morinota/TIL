"""
- 問題link: https://atcoder.jp/contests/pastbook2022/tasks/pastbook2022_a
- 問題:
    - N個の要素が1列に並んでおり、これをいくつかの区間に分割したい。
    - 各区間 [l, r) には、スコア c_{l, r} が付いている。
    - Kを N以下の自然数として、K+1個の整数 t_0, t_1, ..., t_{K} を 0 = t_0 < t_1 < ... < t_{K} =Nを満たすように取る。
    - この時、区間分割 [t_0, t_1), [t_1, t_2), ..., [t_{K-1}, t_K)のスコアを以下のように定義する。
        - c_{t_0,t_1} + c_{t_1,t_2} + ... + c_{t_{K-1},t_K}
    - N要素の区間分割の仕方をすべて考えた時、考えられるスコアの最小値を求めよ。なお、区間の個数Kも自由に選択できる。
- まず、部分問題に落とし込む(i.e. DPテーブルの定義を決める):
    - dp[i] <- 区間 [0, i)について、いくつかの区間に分割する最小コスト
- 次に、緩和について考える:
    - 区間 [0, i)を分割する方法のうち、最後に区切る場所がどこであったかで場合分けする。
    - 最後に区切る位置がj(=0, 1, ..., i-1)である時、区間[0, i)の分割のコストは、「区間[0, j)の分割に対して新たに区間[j, i)を追加したもの」とみなせる。
    - よって緩和式は、 chmin(dp[i], dp[j] + c[j][i])と表せる。
"""


from collections import defaultdict


def choose_minimum(value_1: int, value_2: int) -> int:
    # 関数にする必要はないほど短く単純な処理だが、緩和式として表現する為
    return min(value_1, value_2)


def main(
    N: int,
    scores: list[list[int]],  # 区間 [l, r)のスコア c_{l, r} = scores[l][r]
) -> int:
    # メモ化用の配列を定義
    dp_table = defaultdict(lambda: 10**8)

    # 初期状態
    dp_table[0] = 0

    for right_edge_position in range(1, N + 1):
        for separate_position in range(0, right_edge_position - 1):
            dp_table[right_edge_position] = choose_minimum(
                dp_table[right_edge_position],
                dp_table[separate_position] + scores[separate_position][right_edge_position],
            )

    return dp_table[N]


if __name__ == "__main__":
    N = int(input())
    scores = [list(map(int, input().split())) for _ in range(N + 1)]
    print(main(N, scores))  # 5
