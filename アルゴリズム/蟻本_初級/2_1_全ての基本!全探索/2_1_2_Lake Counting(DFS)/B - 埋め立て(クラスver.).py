from collections import deque


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


# 標準入力
h, w = 10, 10
pic = []
for i in range(h):
    pic.append(list(input()))

# 10 * 10 個のインスタンスを生成し、nodesに格納する。
nodes = []

# 陸地面積を maru とする
maru = 0
for i in range(h):
    nodes.append([])
    for j in range(w):
        nodes[i].append(Node(i, j))
        # 陸地をカウントする
        if pic[i][j] == "o":
            maru += 1


# 10×10のマス目について海かどうかを判定し
# 海であれば、それを埋め立てて、陸続きかどうかをBFSで調べる。
for i in range(h):
    for j in range(w):
        # 探索候補をstackに入れる
        stack = deque()

        # 海のマス目を起点にBFSを実施する(ここが1マス埋めるってところ?)
        if pic[i][j] == "x":
            stack.append(nodes[i][j])
            nodes[i][j].sign = True

        # 陸続きの面積をcntとする
        cnt = 0

        # DFS
        # stackがなくなるまで続ける。
        while stack:
            # stackの末尾から探索候補を一つ取り出す。
            node = stack.pop()  # .popleft() にすると BFS になる
            node: Node

            # 取り出した探索候補の隣接nodeを取得する。
            nears = node.nears
            for near in nears:
                # 探索範囲が10 * 10の中である事を確認する
                if 0 <= near[0] and near[0] < h and 0 <= near[1] and near[1] < w:

                    # 探索候補が訪れたことがあるかどうかを確認する
                    if nodes[near[0]][near[1]].sign == False:
                        # 訪れていなければ、海か陸かを調べる。
                        # 陸であれば探索済みとしてstackに追加する。
                        if pic[near[0]][near[1]] == "o":
                            cnt += 1
                            nodes[near[0]][near[1]].sign = True
                            stack.append(nodes[near[0]][near[1]])

        # 陸続き面積が陸地面積と等しければ、全陸地がつながっているといえる。探索を終える。
        if cnt == maru:
            print("YES")
            exit()

        # 探索済みの陸地をすべて未探索に初期化する
        for a in range(h):
            for b in range(w):
                nodes[a][b].sign = False


# 最後までゴールにたどり着けなかった場合はNoを出力する。
print("NO")
