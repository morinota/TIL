# https://atcoder.jp/contests/abc088/tasks/abc088_d
# https://qiita.com/keisuke-ota/items/6c1b4846b82f548b5dec#%E5%AE%9F%E8%A3%85%E4%BE%8B4abc-088-d-%E5%95%8F%E9%A1%8C%E6%9C%80%E7%9F%AD%E7%B5%8C%E8%B7%AF%E9%95%B7%E3%82%92%E6%B1%82%E3%82%81%E3%82%8B%E5%95%8F%E9%A1%8C

# 縦 H マス横 W マスにマス目が広がっている。通路を .、壁を # とするとき、通路だけを通って左上のマスから右下のマスを結ぶ最短経路を調べ、最短経路と壁を除く通路の面積を求めよ。

from cmath import pi
from collections import deque
from typing import List


h, w = map(int, input().split())  # h行, w列
# 外側を堀(黒)で囲むようにする。
pic = [list("#" * (w + 2))]
for i in range(h):
    pic.append(list("#" + input() + "#"))
pic.append(list("#" * (w + 2)))


class Node:
    def __init__(self, row: int, col: int) -> None:
        # Node （頂点） の番号を定義
        self.row = row
        self.col = col
        # 直接繋がっているNode idxを格納
        self.nears = [[row + 1, col], [row - 1, col], [row, col + 1], [row, col - 1]]
        # 探索済みかどうかを定義
        self.sign = -1

    def __repr__(self) -> str:
        return (
            f"Node row:{self.row} col:{self.col} nears:{self.nears} sign: {self.sign}"
        )


# h*w個のインスタンス(Node)を生成し、nodesに格納する
# + 壁の面積を保存しておく
nodes: List[List[Node]] = []
area_wall = 0
for i in range(h + 2):
    nodes.append([])
    for j in range(w + 2):
        node = Node(row=i, col=j)
        nodes[i].append(node)
        if pic[i][j] == "#":
            area_wall += 1

# wall_areaから追加した外側の壁の分を取り除いておく.
area_wall = area_wall - ((h + 2) * (w + 2) - h * w)

# BFS(最短経路の探索)
# 探索対象 nodeをqueue(キュー)に入れる。
queue = deque()
# 本問では左上から探索を開始する為,nodes[0][0]を最初に入れる。

queue.append(nodes[1][1])
nodes[1][1].sign = 1


# queueがなくなるまで探索を続ける.
while queue:
    node: Node = queue.popleft()
    # print(node)

    nears = node.nears

    for near in nears:
        # 探索候補が訪れたことがあるかどうかを確認する
        if nodes[near[0]][near[1]].sign == -1:
            # 訪れていなければ、通路か壁かゴールか堀かを調べる。
            # 道であれば探索済みとしてqueueに追加する。
            if pic[near[0]][near[1]] == ".":
                # いくつ目の白マスかを記録??
                nodes[near[0]][near[1]].sign = 1 + node.sign
                queue.append(nodes[near[0]][near[1]])

        # ゴールであれば探索を終了する。(BFS全探索だから最初に見つかったルートが最短経路のはず...?)
        if near[0] == h and near[1] == w:
            area_root = nodes[near[0]][near[1]].sign
            answer = h * w - area_root - area_wall
            print(answer)
            exit()

print(-1)
