# 標準入力
from typing import List


A = [""] * 10
for x in range(10):
    A[x] = list(input())

# １ますを埋め立てた時に一つの島にできるか判定せよ。

# スタート地点を探す(最初の陸○の地点)
start_x, start_y = -1, -1
for x in range(10):
    for y in range(10):
        if A[x][y] == "o":
            start_x, start_y = x, y
            break
    if start_x >= 0:
        break

# 深さ優先探索:
landfill_count = 0


# 現在地に隣接する陸地を海に置き換える
def dfs(x, y):
    global A, new_A:list, landfill_count
    # 今いる場所をxに置き換える。
    if new_A[x][y] == 'o':
        new_A[x][y]

    # 上下左右への移動パターンで再帰していく.
    dfs(x + 1, y)
    dfs(x - 1, y)
    dfs(x, y + 1)
    dfs(x, y - 1)


def check():
    global A
    for i in range(10):
        for j in range(10):
            if A[i][j] == "o":
                return False

    return True


# スタート位置から深さ優先対策
dfs(x=start_x, y=start_y)
if check():
    print("YES")
else:
    print("NO")
