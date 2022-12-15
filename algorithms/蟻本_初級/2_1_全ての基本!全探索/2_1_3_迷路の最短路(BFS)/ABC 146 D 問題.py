# https://atcoder.jp/contests/abc146/tasks/abc146_d
# https://qiita.com/keisuke-ota/items/6c1b4846b82f548b5dec#%E5%AE%9F%E8%A3%85%E4%BE%8B6abc-146-d-%E5%95%8F%E9%A1%8C

from collections import deque

from typing import List


n = int(input())
pic = []
for i in range(n - 1):
    pic.append(list(map(int, input().split())))


class Node:
    def __init__(self, idx: int) -> None:
        # Node （頂点） の番号を定義
        self.index = idx
        # 直接繋がっているNode idxを格納
        self.nears = []
        # 親nodeと繋がっているエッジの色を定義
        self.color: int = None
        # 親ノードを定義(Treeにおいて親は一人なので、intで定義すればOK)
        self.par = 0

    def __repr__(self) -> str:
        return f"Node index:{self.index} nears:{self.nears} color: {self.color} par: {self.par}"


# n個のインスタンス(Nodes)を生成し、nodesに格納する。
nodes: List[Node] = []
for i in range(0, n + 1):  # ノード 0 も生成されるが使用しない。
    nodes.append(Node(idx=i))

# 隣接nodeをnears属性に格納する
for i in range(n - 1):
    edge_start, edge_end = pic[i][0], pic[i][1]
    nodes[edge_start].nears.append(edge_end)
    nodes[edge_end].nears.append(edge_start)

# BFSでもDFSでもOK?今回はBFS
# 探索対象 nodeをqueue(キュー)に入れる。
queue = deque()

# node1から探索を開始する=rootのnodeだから。queueにnode1を最初に入れる。
queue.append(nodes[1])

while queue:
    # queueからnodeを一つ取り出す。取り出したノードについて調べる。
    # 取り出された node は queue から消える。
    node: Node = queue.popleft()

    # 取り出された node の隣接 node 達を nears に入れる。
    # nears は子 node の候補である。
    nears = node.nears

    # 子 nodeに使う色の候補を用意
    color_list = list(range(len(nears) + 2))

    # 親 node と繋がっているedgeの色をcolor_listから削除しておく.
    # 親 nodeを持たない node(root node)では IndexErrorが返されるので、回避
    try:
        del color_list[node.color]
    except:
        pass

    # 隣接 node 達が探索済みか 1 つずつ調べる。
    # 子 node を持たない node では for ループはスキップされる。
    for near, color in zip(nears, color_list[1:]):

        # 未探索のnearには色がついていない。
        # 色がついてないnode は子nodeとしてqueueに追加する。
        if nodes[near].color is None:
            queue.append(nodes[near])

            # 子 nodeから見て、親 node と何色で繋がるのか決める.
            nodes[near].color = color

            # 子 node に親 node を保存
            nodes[near].par = node.index

            # 隣接 node から親nodeを除く.
            nodes[near].nears.remove(node.index)

    # print(node)  # コメントアウトを外すと BFS の様子を追跡できる。

# ans リストを作成
answers = []

# edge の順番で答えを追加する。
for edge in pic:

    # edge が結ぶ 2 つの node のうち、どちらが子 node であるのかを調べ、子 node の color メソッドを ans に追加する。
    # node 1 は root なので子 node にはならない。
    if edge[0] == 1:
        answers.append(nodes[edge[1]].color)
    elif nodes[edge[0]].par == edge[1]:  # edge_0の親ノードがedge_1
        # edge_0が子ノード
        answers.append(nodes[edge[0]].color)
    else:
        # edge_1が子ノード
        answers.append(nodes[edge[1]].color)

# Tree 全体で使う色の数を出力
print(max(answers))
# 各Edgeの色を出力
for ans in answers:
    print(ans)
