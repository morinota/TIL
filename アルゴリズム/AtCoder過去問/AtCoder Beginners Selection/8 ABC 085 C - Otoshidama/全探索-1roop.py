# お札が N 枚 合計Y円(嘘かも)
# このような条件を満たす各金額の札(10000, 5000, 1000)の枚数の組を 1 つ求めよ。
# 嘘だったら-1-1-1と出力せよ

# 標準入力
N, Y = map(int, input().split())
# 出力の初期値
res10000, res5000, res1000 = -1, -1, -1

for a in range(N + 1):
    for b in range(N + 1):
        c = N - a - b
        if c < 0:
            continue

        total = 10000 * a + 5000 * b + 1000 * c
        if total == Y:  # 答えが見つかったら
            res10000, res5000, res1000 = a, b, c

print(res10000, res5000, res1000)
