# https://qiita.com/u2dayo/items/e5f0a0f02c530f12b03b#c%E5%95%8F%E9%A1%8Ck-swap


def judge() -> bool:
    n, k = map(int, input().split())
    a_list = list(map(int, input().split()))
    amari_list = [[] for _ in range(k)]  # i を Kで割った余りごとに管理
    a_list_expected = a_list.sort()


print("Yes" if judge() else "No")
