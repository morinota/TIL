# https://atcoder.jp/contests/abc204/tasks/abc204_c
# https://qiita.com/keisuke-ota/items/6c1b4846b82f548b5dec#%E5%AE%9F%E8%A3%85%E4%BE%8B5abc-204-c-%E5%95%8F%E9%A1%8C
from collections import deque

from typing import List


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


def main():
    # 標準入力を受け取る
    n, m = map(int, input().split())  # n個の都市とm個の道路
    pic = []
    for j in range(m):
        pic.append(list(map(int, input().split())))
        # 都市A_jからB_jへ移動できる。逆は無理.=>有向グラフ!!
    # スタート地点とゴール地点の都市の組つぃて考えられるものは何通りあるか??

    # n個のインスタンス(node)を生成し、nodesに格納する
    nodes: List[Node] = []
    for i in range(0, n + 1):  # 0は使わないが利便性の為に生成しておく
        nodes.append(Node(idx=i))

    # 隣接するNodeをnears属性に格納する。
    for j in range(m):
        edge_start, edge_end = pic[j][0], pic[j][1]
        nodes[edge_start].nears.append(edge_end)
        # nodes[edge_end].nears.append(edge_start) # 無向グラフの場合は必要!

    count = 0

    # BFS
    # 探索対象の NodeをQueue(キュー)に入れる。
    queue = deque()

    for i in range(1, n + 1):
        # スタート地点をキューに入れる.
        queue.append(nodes[i])
        # 道路を0本使う場合のカウントをsignに記録しておく(ex. start, goal=1, 1)
        nodes[i].sign = nodes[i].index
        # queueがなくなるまで探索を続ける
        while queue:
            # queueからnodeを一つ取り出す。取り出したノードについて調べる。
            # 取り出されたnodeはqueueから消える。
            node: Node = queue.popleft()

            nears = node.nears

            for near in nears:
                # 未探索の隣接nodeは、queueに追加する。
                # 取り出してきた親nodeは道標となる為、子nodeのsignメソッドに追加する。
                if nodes[near].sign == -1:
                    queue.append(nodes[near])
                    nodes[near].sign = node.index  # 繋がってる親ノードを記録

        # 都市iからスタートする組み合わせの数を記録
        count += len([v.sign for v in nodes if v.sign != -1])
        # 探索済みの都市を全て未探索に初期化する
        for i in range(1, n + 1):
            nodes[i].sign = -1

    # start goalの組み合わせの数を出力する。
    print(count)


if __name__ == "__main__":
    main()
