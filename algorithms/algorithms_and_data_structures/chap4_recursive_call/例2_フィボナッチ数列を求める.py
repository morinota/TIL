# 例2: 再帰関数内でrecursive call を複数回行うケース = フィボナッチ数列を求める

"""
- フィボナッチ数列を定義する漸化式:
    - F_0 = 0
    - F_1 = 1
    - F_N = F_{N-1} + F_{N-2} (N=2,3,...)
"""


def generate_fibonacci(N: int) -> int:
    """F_{N} を返す関数"""
    # ベースケース(2つ)
    if N == 0:
        return 0
    elif N == 1:
        return 1

    # recursive call
    return generate_fibonacci(N - 1) + generate_fibonacci(N - 2)


if __name__ == "__main__":
    print(generate_fibonacci(0))
    print(generate_fibonacci(1))
    print(generate_fibonacci(3))
