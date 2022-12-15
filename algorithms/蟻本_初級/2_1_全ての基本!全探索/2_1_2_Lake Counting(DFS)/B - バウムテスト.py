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
n, m = map(int, input().split())
pic = []
for i in range(m):
    pic.append(input().split())
