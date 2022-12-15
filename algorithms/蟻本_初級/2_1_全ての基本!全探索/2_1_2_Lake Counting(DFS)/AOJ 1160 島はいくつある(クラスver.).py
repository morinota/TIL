from collections import deque


class Node:
    def __init__(self, row, col) -> None:
        # Node （頂点） の番号を定義
        self.col = col
        self.row = row
        # 隣接 Node のリストを定義
        self.nears = [
            [row, col + 1],
            [row, col - 1],
            [row + 1, col],
            [row - 1, col],
            [row + 1, col + 1],
            [row + 1, col - 1],
            [row - 1, col + 1],
            [row - 1, col - 1],
        ]
        # 探索済みかどうかを定義
        self.sign = False

    def __repr__(self) -> str:
        return f"Node row:{self.row} Node col:{self.col} nears:{self.nears} sign: {self.sign}"


# 標準入力
w, h = map(int, input().split())
pic = []
for i in range(h):
    pic.append(input().split())

    # pic[x][y] = 0なら海。1なら陸。
    # 縦 or 横 or 斜め方向に隣接していれば 一つの島。
    # 全部で島がいくつあるか？

# h * w個のインスタンスを生成し、nodesに格納する。
nodes = []
for i in range(h):
    nodes.append([])
    for j in range(w):
        nodes[i].append(Node(i, j))

count = 0

# h×wのマス目について陸かどうかを判定し
# 陸であれば、周囲に陸があるかを調べる。
for i in range(h):
    for j in range(w):
        # 探索候補をstackに入れる
        stack = deque()

        # そのマス目が陸　且つ　まだ確認していなければ...
        if pic[i][j] == "1" and nodes[i][j].sign == False:
            stack.append(nodes[i][j])
            nodes[i][j].sign = True
            # 一つの島としてカウント
            count += 1

        while stack:
            # stackの末尾から探索候補を一つ取り出す。
            node = stack.pop()  # .popleft() にすると BFS になる
            node: Node

            # 取り出した探索候補の隣接nodeを取得する。
            nears = node.nears
            for near in nears:
                # 探索範囲がh * wの中である事を確認する
                if 0 <= near[0] and near[0] < h and 0 <= near[1] and near[1] < w:
                    # 探索候補が訪れたことがあるかどうかを確認する
                    if nodes[near[0]][near[1]].sign == False:
                        # 訪れていなければ、海か陸かを調べる。
                        # 陸であれば探索済みとしてstackに追加する。
                        if pic[near[0]][near[1]] == "1":
                            nodes[near[0]][near[1]].sign = True
                            stack.append(nodes[near[0]][near[1]])


print(count)
