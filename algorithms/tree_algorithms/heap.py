"""
- heapのpopとpushのロジックは
- heapとbinary search treeは理解しておくといい。
"""
import sys
from typing import Optional


class MiniHeap(object):
    def __init__(self) -> None:
        self.heap = [-1 * sys.maxsize]  # 先頭、最も小さくなる数字を入れる(図における-xの部分)
        self.current_size = 0  # heapのサイズ

    def get_parent_index(self, index: int) -> int:
        return index // 2

    def get_left_child_index(self, index: int) -> int:
        return index * 2

    def get_right_child_index(self, index: int) -> int:
        return index * 2 + 1

    def swap(self, index1: int, index2: int) -> None:
        """数字(value)同士の場所(index)を交換する"""
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def heapify_up(self, index: int) -> None:
        """heapify = 入れ替えてやっていくという意味あい.
        親ノードと比較してheapifyしていく
        """
        while self.get_parent_index(index) > 0:  #  最小の数字を上まで(=親がいなくなるまで)持っていく
            if self.heap[index] < self.heap[self.get_parent_index(index)]:
                self.swap(index, self.get_parent_index(index))  # parentより小さければスワップして上へ
            index = self.get_parent_index(index)  # 対象のindexを置き換える

    def push(self, value: int) -> None:
        """heapに値を入れる"""
        self.heap.append(value)  # まずは最後尾にvalueを入れる
        self.current_size += 1
        self.heapify_up(self.current_size)  # index = 今回入れた最後尾のindexでheapfiy

    def min_child_index(self, index: int) -> int:
        """left childとright childで小さい方のindex番号を返す"""
        if self.get_right_child_index(index) > self.current_size:  # leftしか存在しないケース
            return self.get_left_child_index(index)
        else:  # leftとright両方存在するケース
            if self.heap[self.get_left_child_index(index)] < self.heap[self.get_right_child_index(index)]:
                return self.get_left_child_index(index)
            else:
                return self.get_right_child_index(index)

    def heapify_down(self, index: int) -> None:
        """先頭の値を適切な位置までおろしていく"""
        while self.get_left_child_index(index) <= self.current_size:  # 一番下の段に到着するまで
            min_child_index = self.min_child_index(index)  # left childとright childで小さい方のindex番号を返す
            if self.heap[index] > self.heap[min_child_index]:
                self.swap(index, min_child_index)  # もし子ノードよりも小さい場合は入れ替え
            index = min_child_index  # 先頭の値が入ったindex位置を更新(どんどん下へ降りていく)

    def pop(self) -> Optional[int]:
        """一番小さなの値(i.e. 先頭、heapの最も上にある値)を取り出す.
        取り出した後、heapのルールを満たすように残りのノードを整理する
        """
        if len(self.heap) == 1:  # early return
            return

        root = self.heap[1]  # 先頭を取得する(返り値)

        data = self.heap.pop()  # 最後尾を取得する(樹を作り直す為)

        if len(self.heap) == 1:  # early return
            return root

        # [-x, 5, 6, 2, 9, 13, 11]
        self.heap[1] = data  # 最後尾を先頭へ
        self.current_size -= 1

        self.heapify_down(1)  # 先頭に持ってこられた最後尾のvalue(data)を適切な位置までおろしていく
        return root


if __name__ == "__main__":
    min_heap = MiniHeap()
    min_heap.push(5)
    min_heap.push(6)
    min_heap.push(2)
    min_heap.push(9)
    min_heap.push(13)
    min_heap.push(11)
    min_heap.push(1)
    print(min_heap.heap)
    print(min_heap.pop())
    print(min_heap.heap)
