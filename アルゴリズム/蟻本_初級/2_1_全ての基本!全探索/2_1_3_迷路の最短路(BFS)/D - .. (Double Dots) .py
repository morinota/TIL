# https://qiita.com/keisuke-ota/items/6c1b4846b82f548b5dec

n, m = map(int, input().split())  # n個の部屋とm本の通路
a, b = [0] * m, [0] * m
for i in range(m):
    # 通路iは部屋a_iと部屋b_iを双方向に繋いでいる。
    # 部屋1は洞窟の入り口がある特別な部屋。
    a[i], b[i] = map(int, input().split())
