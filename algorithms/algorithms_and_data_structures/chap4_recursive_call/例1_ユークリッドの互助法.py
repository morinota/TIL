# 再帰の例1: ユークリッドの互助法

"""
- 2つの整数m, nの最大公約数 (以下、GCD(m,n)と表記する)を求めるアルゴリズム
- 以下の最大公約数の性質を使う:「mをnで割った時の余りをrとすると、GCD(m,n) = GCD(n,r)が成り立つ」
- 以下は手順:
    - m を n で割った時の余りをrとする。
    - r = 0であれば、この時点でのnが求める最大公約数である(これは自明)。(=ベースケース)
    - r != 0 の場合、m <- n, n <-rとして、手順1に戻る。
- 計算量は m >= n > 0 として O(log n)
"""


def GCD(m: int, n: int) -> int:
    # ベースケース
    if n == 0:
        return m

    # recursive call
    return GCD(n, m % n)


def main() -> None:
    print(GCD(51, 15))  # 3
    print(GCD(15, 51))  # 3


if __name__ == "__main__":
    main()
