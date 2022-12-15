# https://qiita.com/keisuke-ota/items/6c1b4846b82f548b5dec#%E5%AE%9F%E8%A3%85%E4%BE%8B7-abc-138-d-%E5%95%8F%E9%A1%8C
# https://atcoder.jp/contests/abc138/tasks/abc138_d

from typing import List
from collections import deque

n, q = map(int, input().split())
pic = []
for i in range(n - 1):
    pic.append(list(map(int, input().split())))
operates = []
for j in range(q):
    operates.append(list(map(int, input().split())))


class Node:
    def __init__(self, idx: int) -> None:
        # Node （頂点） の番号を定義
        self.index = idx
        # 直接繋がっているNode idxを格納
        self.nears = []
        # 親ノードを定義(Treeにおいて親は一人なので、intで定義すればOK)
        self.par = 0
        # counterの値
        self.counter = 0
        # 先祖ノードを定義
        self.ancestors = []

    def __repr__(self) -> str:
        return f"Node index:{self.index} nears:{self.nears} par: {self.par} counter:{self.counter} ancestors:{self.ancestors}"


# n個のインスタンス(Nodes)を生成し、nodesに格納する。
nodes: List[Node] = []
for i in range(0, n + 1):  # ノード 0 も生成されるが使用しない。
    nodes.append(Node(idx=i))

# 隣接nodeをnears属性に格納する
for i in range(n - 1):
    edge_start, edge_end = pic[i][0], pic[i][1]
    nodes[edge_start].nears.append(edge_end)
    nodes[edge_end].nears.append(edge_start)

# BFSでもDFSでもOK?とりあえずBFS
# 探索対象 nodeをqueue(キュー)に入れる。
queue = deque()

# node1から探索を開始する=rootのnodeだから。queueにnode1を最初に入れる。
queue.append(nodes[1])

# nodes内の各Nodeの属性(nears, par)を整理していく。
while queue:
    # queueからnodeを一つ取り出す。取り出したノードについて調べる。
    # 取り出された node は queue から消える。
    node: Node = queue.popleft()
    # print(node)

    # 取り出された node の隣接 node 達を nears に入れる。
    # nears は子 node の候補である。
    nears = node.nears

    # 隣接 node 達が探索済みか 1 つずつ調べる。
    # 子 node を持たない node では for ループはスキップされる。
    for near in nears:

        # 未探索のnearにはparが格納されていない。
        # 子nodeはqueueに追加する。
        if nodes[near].par == 0:
            queue.append(nodes[near])

            # 子 node に親 node を保存
            nodes[near].par = node.index

            # 子 node に先祖ノードを保存
            nodes[near].ancestors = (
                nodes[near].ancestors + [node.index] + node.ancestors
            )

            # 隣接 node から親nodeを除く.
            nodes[near].nears.remove(node.index)

# 各操作を実行して nodes内の各Nodeのcounter属性を更新していく
for ope in operates:
    target_root = ope[0]
    x = ope[1]
    # 操作を実行
    for node in nodes[1:]:
        if (target_root in node.ancestors) or (target_root == node.index):
            node.counter += x

# 結果を出力
ans = [str(node.counter) for node in nodes[1:]]
print(" ".join(ans))
