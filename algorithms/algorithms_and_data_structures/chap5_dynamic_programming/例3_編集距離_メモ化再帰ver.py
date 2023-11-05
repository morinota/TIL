"""
- 問題:
    - 2つの文字列S, T。
    - Sに以下の3通りの操作を繰り返し施す事でTに変換したい:
        - 変更: S中の文字を1つ選び、任意の文字に変更する
        - 削除: S中の文字を1つ選び、削除する
        - 挿入: S中の好きな箇所に、任意の文字を1文字挿入する
    - 一連の操作のうち、操作回数の最小値を求めよ。なおこの最小値をSとTの編集距離と呼ぶ。
- DPに落とし込む:
    - 最初に、以下の2つの操作が等価である事に着目する:
        - 挿入操作 = Tの文字を1つ選び削除する(その文字はもう考慮しなくて良くなるから??)
- DPテーブル(i.e. 部分問題)を定義してみる:
    - dp[i][j] <- Sの最初のi文字分と、Tの最初のj文字分との間の編集距離。
- 初期条件を考える:
    - dp[0][0] = 0: 両方とも空文字列で一致。
- 遷移を考える:
    - Sの最初のi文字分とTの最初のj文字分とで、最後の1文字をどのように対応付したかで場合分けする。
    - 変更操作:
        - S[i-1] == T[j-1]の時、dp[i][j] <- dp[i-1][j-1]
        - S[i-1] != T[j-1]の時、dp[i][j] <- dp[i-1][j-1] + 1
    - 削除操作(Sのi文字目を削除):
        - Sのi文字目が不要なケースなので dp[i][j] <- dp[i-1][j] + 1
    - 挿入操作(Tのj文字目を削除):
        - Tのj文字目が不要なケースなので dp[i][j] <- dp[i][j-1] + 1
"""

# メモ化用の配列を定義
from collections import defaultdict


MAX_EDIT_DISTANCE = 10**8


def calc_edit_distance(
    i: int,
    j: int,
    S: str,
    T: str,
    dp_table: dict[tuple, int],
):
    """Sの最初のi文字とTの最初のj文字との間の編集距離を計算する"""
    # ベースケース
    if i == 0 and j == 0:  # ともに空文字列
        dp_table[(i, j)] = 0
        return dp_table[(i, j)]

    # メモをチェック(すでに計算済みなら答えをリターンする)
    if dp_table[(i, j)] != MAX_EDIT_DISTANCE:
        return dp_table[(i, j)]

    # 答えをメモ化しながらrecursive call
    edit_distance_candidates = []
    ## 変更操作
    if i > 0 and j > 0:  # i or jが負になってしまわないように。
        if S[i - 1] == T[j - 1]:
            edit_distance_candidates.append(calc_edit_distance(i - 1, j - 1, S, T, dp_table))
        else:
            edit_distance_candidates.append(calc_edit_distance(i - 1, j - 1, S, T, dp_table) + 1)

    # 削除操作
    if i > 0:
        edit_distance_candidates.append(calc_edit_distance(i - 1, j, S, T, dp_table) + 1)
    # 挿入操作
    if j > 0:
        edit_distance_candidates.append(calc_edit_distance(i, j - 1, S, T, dp_table) + 1)

    dp_table[(i, j)] = min(edit_distance_candidates)
    return dp_table[(i, j)]


def main(S: str, T: str) -> int:
    DP_MEMO = defaultdict(lambda: MAX_EDIT_DISTANCE)  # key=(i,j), value=edit_distance
    return calc_edit_distance(len(S), len(T), S, T, DP_MEMO)


if __name__ == "__main__":
    print(main("bag", "big"))  # 1
    print(main("kodansha", "danshari"))  # 4
    print(main("logistic", "algorithm"))  # 6
