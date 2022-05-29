# 整数Nが与えられる。
# ここで、2つの正の整数A, Bに対して、
# F(A,B)を「十進数表記における、Aの桁数とBの桁数の内大きい方」と定義する。
# 2 つの正の整数の組 (A,B) が N=A×B を満たすように動くとき、
# F(A,B) の最小値を求めよ。

# 制限:N<=10**10
import math

N = int(input())


def calc_f(A: int, B: int) -> int:
    ord_A = int(math.log10(A) + 1)
    ord_B = int(math.log10(B) + 1)
    return max(ord_A, ord_B)


# 方針
# 探索のスタート:A=1, B=N, ゴール:A=N, B=1
# Aを全探索すれば良いが、1<=A<=Nを全探索してると間に合わない。
# 実は1<=A<=\sqrt(N)だけ探索すれば良い.
# (A*B=B*Aより、後半\sqrt(N)<=A<=Nは同じだから！)
# =>時間計算量がO(\sqrt(N))となる為間に合う！

min_f = 11  # N=10**10の時??
for A in range(1, int((N + 1) ** 0.5) + 1):  # int は切り捨てなので一応+1
    if N % A == 0:
        min_f = min(min_f, calc_f(A, int(N / A)))
    else:
        continue
print(min_f)
