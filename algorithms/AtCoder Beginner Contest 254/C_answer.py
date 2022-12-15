# https://atcoder.jp/contests/abc254/tasks/abc254_c
# 解説: https://qiita.com/u2dayo/items/e5f0a0f02c530f12b03b#c%E5%95%8F%E9%A1%8Ck-swap


# 0 <= i < Kとして、行列の各要素をa_{i+jK}の形で表す。
# すると、iが同じ要素同士(ex. 1+K , 1+2K, ...)は、バブルソート(隣り合う要素をどんどん交換)の要領でソートを繰り返す事で、自由な順番に並び変える事ができる。
# 目的はAを昇順にならび変える事。そのためには少なくとも、「iが同じグループ」の要素は、"少なくとも"昇順になっている必要がある。
# 全ての0<=i<Kについて、「iが同じグループ」を昇順にソートする。
# ＝＞こうしてできた数列が、全体として昇順になっているか確認すればOK


def judge():
    N, K = map(int, input().split())
    A = list(map(int, input().split()))

    # 正解となるソートされたaを用意しておく
    A_sorted_expected = sorted(A, reverse=False)

    # K個= 「iが同じグループ」の数の[]を作る  idxを Kで割った余り=iごとに管理する.
    k_grouping_list = [[] for _ in range(K)]

    for idx, a in enumerate(A):
        # idx % K = iの値ごとに管理する.
        # Aの各要素aを「iが同じグループ」に分割していく
        k_grouping_list[idx % K].append(a)
    # 各「iが同じグループ」毎にソートしていく。
    for i in range(K):
        k_grouping_list[i].sort()  # ソートする

    # 各グループでソートしたものを連結して(元通りになるように)、SAとして再編成
    A_sorted_actual = [0] * N
    for idx in range(N):
        print(idx % K, idx // K)
        A_sorted_actual[idx] = k_grouping_list[idx % K][idx // K]  # すなわちk_grouping_list[i][j]

    return A_sorted_actual == A_sorted_expected


print("Yes" if judge() else "No")
