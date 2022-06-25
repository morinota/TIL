import sys

sys.setrecursionlimit(10**7)  # 再起回数の設定


# スタートからゴールまで辿り着けるかを判定する問題。

# 標準入力
H, W = map(int, input().split())
# C = [[0] * W] * H
C = [""] * H
for i in range(H):
    C[i] = list(input())

# 家の座標を取得する。
start_x, start_y = 0, 0
for h in range(H):
    for w in range(W):
        if C[h][w] == "s":
            start_x, start_y = h, w

# 深さ優先探索
def dfs(x, y):
    global C
    # 範囲外の場合は終了
    if y >= W or y < 0 or x >= H or x < 0:
        return
    # 壁の場合も終了
    elif C[x][y] == "#":
        return

    # ゴールにたどり着けば終了
    if C[x][y] == "g":
        print("Yes")
        exit()  # プログラムを終了させる。

    # 確認したルートは壁にしておく。(一度通った場所は通れないから)
    C[x][y] = "#"

    # 上下左右への移動パターンで再帰していく.
    dfs(x + 1, y)
    dfs(x - 1, y)
    dfs(x, y + 1)
    dfs(x, y - 1)


# スタート位置から深さ優先対策
dfs(x=start_x, y=start_y)
print("No")  # exit()せずに最後までいけばNO!
