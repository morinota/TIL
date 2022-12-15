from collections import deque
import sys

sys.setrecursionlimit(10**7)  # 再起回数の設定


class Node:
    def __init__(self, row, col) -> None:
        # Node （頂点） の番号を定義
        self.col = col
        self.row = row
        # 隣接 Node のリストを定義
        self.nears = [[row, col + 1], [row, col - 1], [row + 1, col], [row - 1, col]]
        # 探索済みかどうかを定義
        self.sign = False

    def __repr__(self) -> str:
        return f"Node row:{self.row} Node col:{self.col} nears:{self.nears} sign: {self.sign}"


def main():
    # 標準入力
    h, w = map(int, input().split())
    # 外側を堀で囲むようにする。
    C = [list("#" * (w + 2))]
    for i in range(h):
        C.append(list("#" + input() + "#"))
    C.append(list("#" * (w + 2)))
    # 探索候補をstackに入れる
    stack = deque()

    # インスタンス(Node)を生成し、nodesに格納する。
    nodes = []

    for i in range(h + 2):
        nodes.append([])
        for j in range(w + 2):
            nodes[i].append(Node(i, j))
            nodes: list[list[Node]]
            # スタート位置のnodeはstackに入れる。
            # スタート位置のnodeを探索済みとし、signメソッドにTrueを入れる。
            if C[i][j] == "s":
                stack.append(nodes[i][j])
                nodes[i][j].sign = True

    # DFS
    # stackがなくなるまで続ける。
    while stack:
        # stackから探索候補を一つ取り出す。
        node = stack.pop()  # .popleft() にすると BFS になる
        node: Node
        # print(node)  # コメントアウトを外すと現在地がわかる。BFS と DFS で比べてみるとよい。
        # 取り出した探索候補の隣接nodeを取得する。
        nears = node.nears
        for near in nears:
            # 探索候補が訪れたことがあるかどうかを確認する
            if nodes[near[0]][near[1]].sign == False:
                # 訪れていなければ、道かゴールか堀かを調べる。
                # 道であれば探索済みとしてstackに追加する。
                # ゴールであれば探索を終了する。
                if C[near[0]][near[1]] == ".":
                    nodes[near[0]][near[1]].sign = True
                    stack.append(nodes[near[0]][near[1]])
                elif C[near[0]][near[1]] == "g":
                    print("Yes")
                    exit()

    # 最後までゴールにたどり着けなかった場合はNoを出力する。
    print("No")


if __name__ == "__main__":
    main()
