# 解説 https://qiita.com/u2dayo/items/e5f0a0f02c530f12b03b#d%E5%95%8F%E9%A1%8Ctogether-square
# 問題 https://atcoder.jp/contests/abc254/tasks/abc254_d

# 平方数とは、「全ての因数の次数が偶数である数」のこと。
# iを固定して、1 <= i <= Nで全探索する。
# a,b,cを正の整数とする。
# iを平方数で割れるだけ割って、i = a * b ^2の形で表す。
# i * jが平方数になるには、jの因数にaが含まれていなければならない。
# そうでないと、次数が１の素因数が存在する事になり、i*jが平方数にならない。
# つまりj = a * c^2で表される必要がある。
# このとき、i*j = (abc)^2となり、たしかに平方数である。

# iを決めると、a, bは一意に定まる。よって、j = a * c^2のcを１から全探索して、j>Nになったら打ち切れば良い.
# cは最大でも\sqrt{N}程度にしかならないので、全体の計算量はO(N * \sqrt{N})

from itertools import count


def calc_odd_factor_prod(n):
    """次数が奇数の素因数の積を得る（わかりづらかったら、普通に素因数分解して、次数が奇数のものをかけ合わせてください"""
    for i_2 in (i**2 for i in count(start=2, step=1)):  # 2<=iでforループ
        if i_2 > n:
            break
        while n % i_2 == 0:  # もしi^2がnの因数であれば...
            n //= i_2  # nをi^2で割って、次の因数を探す.

    return n


def main():
    N = int(input())
    ans = 0
    for i in range(1, N + 1):
        odd = calc_odd_factor_prod(i)  # 上式のa(次数が奇数の素因数の積)を求める.
        # j = a * c^2のcを１から全探索
        for c in range(1, N + 1):
            j = odd * (c**2)
            if j > N:
                break
            ans += 1

    print(ans)


if __name__ == "__main__":
    main()
