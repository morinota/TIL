"""
- N個の正の整数 a_0, ..., a_{N-1} と、正の整数 Wが与えられる。
- a_0, ..., a_{N-1}の中から何個かの整数を選んで、総和をWとできるか否かを判定せよ。
"""
from collections import defaultdict

MEMO: dict[tuple, bool] = defaultdict(lambda: -1)  # (注意! メモする答え自体がboolなので、memoしてない事を意味する-1を活用する)


def can_combination_sum(
    i: int,
    A: list[int],
    W: int,
) -> bool:
    """
    - 配列Aからidx = 0 ~ i-1の整数を選んで Wを作れるか否かを返す。
    - グローバル変数 MEMO[(i, W)] にcan_combination_sum(i, A, W)の結果を保存する。
    """
    # ベースケース
    if i == 0:
        print(f"reach to k=0 and W={W}")
        MEMO[i, W] = W == 0
        return MEMO[i, W]

    # メモをチェック(すでに計算済みなら答えをリターンする)
    if MEMO[(i, W)] != -1:
        return MEMO[(i, W)]

    # 答えをメモ化しながらrecursive call
    if can_combination_sum(i - 1, A, W):
        MEMO[(i, W)] = True
    elif can_combination_sum(i - 1, A, W - A[i - 1]):
        MEMO[(i, W)] = True
    else:
        MEMO[(i, W)] = False
    return MEMO[(i, W)]


def main(A: list[int], W: int) -> bool:
    """
    - まず以下の2つの場合に分けて考える:
        - a_{N-1} を選ばない時 -> a_1, ..., a_{N-2}から総和をWにできるかという小問題に帰着。
        - a_{N-1} を選ぶ時 -> a_1, ..., a_{N-2}から総和をW-a_{N-1}にできるかという小問題に帰着。
    - 2つの小問題のうち、少なくとも一方がYesであれば元の答えもYesになる。両方ともNoであれば元の答えもNoになる。
    - 同様にして、N-1個の整数問題をN-2個の整数問題に帰着し、...,と再帰的に繰り返す。
    -> 最終的に「0個の整数を使って、ある整数を作れるか」という問題に帰着する。->0個の整数の総和は常に0なので、ある整数に0が含まれていれば答えはYesになる。
    """
    N = len(A)
    return can_combination_sum(N, A, W)


if __name__ == "__main__":
    A = [1 for _ in range(30)]
    print(main(A, 20))
