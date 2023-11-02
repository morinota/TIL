# 例2: 再帰関数内でrecursive call を複数回行うケース = フィボナッチ数列を求める
from collections import defaultdict

"""
- フィボナッチ数列を定義する漸化式:
    - F_0 = 0
    - F_1 = 1
    - F_N = F_{N-1} + F_{N-2} (N=2,3,...)
"""

# generate_fibonacci(N)の答えをメモ化する配列
# (簡単のため、グローバル変数としているが、実際にはグローバル変数の乱用は非推奨)
# (よって対策として、memoを再帰関数の参照引数とする等の工夫が考えられる...!)
MEMO = defaultdict(lambda: -1)


def generate_fibonacci(N: int) -> int:
    """F_{N} を返す関数"""
    # ベースケース(2つ)
    if N == 0:
        return 0
    elif N == 1:
        return 1

    # メモをチェック(すでに計算済みなら答えをリターンする)
    if MEMO[N] != -1:
        return MEMO[N]

    # 答えをメモ化しながらrecursive call
    MEMO[N] = generate_fibonacci(N - 1) + generate_fibonacci(N - 2)
    return MEMO[N]


if __name__ == "__main__":
    print(generate_fibonacci(0))
    print(generate_fibonacci(1))
    print(generate_fibonacci(3))
