"""
- N個の正の整数 a_0, ..., a_{N-1} と、正の整数 Wが与えられる。
- a_0, ..., a_{N-1}の中から何個かの整数を選んで、総和をWとできるか否かを判定せよ。
"""
from collections import defaultdict


def can_combination_sum(
    k: int,
    A: list[int],
    W: int,
    memo: dict[tuple, bool],
) -> bool:
    # ベースケース
    if k == 0:
        print(f"reach to k=0 and W={W}")
        if W == 0:
            return True
        return False

    # メモをチェック(すでに計算済みなら答えをリターンする)
    if memo.get((k, W), None):
        return memo[(k, W)]

    # 答えをメモ化しながらrecursive call
    memo[(k, W)] = can_combination_sum(k - 1, A, W, memo) or can_combination_sum(k - 1, A, W - A[k - 1], memo)
    return memo[(k, W)]


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
    return can_combination_sum(N, A, W, {})


if __name__ == "__main__":
    A = [num for num in range(100)]
    print(main(A, 200))
