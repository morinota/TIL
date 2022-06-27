# https://qiita.com/keisuke-ota/items/6c1b4846b82f548b5dec

from collections import deque
from typing import List


n, m = map(int, input().split())  # n個の部屋とm本の通路
a, b = [0] * m, [0] * m
for i in range(m):
    # 通路iは部屋a_iと部屋b_iを双方向に繋いでいる。
    # 部屋1は洞窟の入り口がある特別な部屋。
    a[i], b[i] = map(int, input().split())

# 部屋1以外のどの部屋についても以下の条件を満たす事が目標.
# その部屋から出発し、「いまいる部屋にある道しるべを見て、それが指す部屋に移動する」ことを繰り返すと、部屋 1 に最小の移動回数でたどり着く。

# この問題では、部屋をnodeとし通路をedgeとして考える
# Node1をrootとし、rootへの最短経路を考える。
# Node1を除く全てのNodeが Node1とedgeで繋がっている(直接or間接)場合、Yesを出力。
# Node 1と繋がっていないNodeが1つでもある場合、Noを出力する。


class Node:
    def __init__(self, idx: int) -> None:
        # Node （頂点） の番号を定義
        self.index = idx
        # 直接繋がっているNode idxを格納
        self.nears = []
        # 探索済みかどうかを定義
        self.sign = -1

    def __repr__(self) -> str:
        return f"Node index:{self.index} nears:{self.nears} sign: {self.sign}"


# n個のインスタンス(Node)を生成し、nodesに格納する
nodes: List[Node] = []
for i in range(0, n + 1):
    nodes.append(Node(idx=i))

# 隣接 nodeをnears属性に格納する
for j in range(m):
    edge_start, edge_end = a[j], b[j]
    nodes[edge_start].nears.append(edge_end)
    nodes[edge_end].nears.append(edge_start)  # 有向グラフの場合は消す

# BFS
# 探索対象 nodeを queue(キュー)に入れる。
queue = deque()
# 本問では node1から探索を開始する為、queueにnode1を最初に入れる。
queue.append(nodes[1])
# queueがなくなるまで探索を続ける.
while queue:
    # queueからnodeを一つ取り出す。取り出したノードについて調べる。
    # 取り出された node は queue から消える。
    node: Node = queue.popleft()  # .pop() にすると DFS になる
    # node: Node = queue.pop()  # .popleft() にすると BFS になる

    # print(node)

    nears = node.nears

    for near in nears:
        # 未探索の隣接nodeは queueに追加する。
        # 取り出してきた親nodeは道標となる為、子nodeのsignメソッドに追加する。
        if nodes[near].sign == -1:
            queue.append(nodes[near])
            nodes[near].sign = node.index  # 繋がってる親ノードを記録

# yesまたはNoを表示
if -1 in [node.sign for node in nodes[2:]]:
    print("No")
    exit()
else:
    print("Yes")

# 道しるべを表示
for k in range(2, n + 1):
    print(nodes[k].sign)
