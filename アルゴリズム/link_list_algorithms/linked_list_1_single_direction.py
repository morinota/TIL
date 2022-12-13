"""単方向リンクリスト(Linked list)
- 連結リストとも呼ばれる
    - Head(頭)から、どんどんノード(DataとNextのセット)が連結していく
    - Data:数字とか、next:リンク（nextの部分で後ろのノードと結びつける）
- リストの中身の実装方法というイメージ
- データを追加したり、削除したりが、headからリンクをたどって行うのに適している構造
- 実際に現場で実装することはないかもしれないけど、構造を知っておくことで役立つかも！
- テストでも出る基本的な構造
- 基本のデータ構造としてリンクリストを抑えておくといい
"""

from __future__ import annotations

from symbol import return_stmt
from typing import Any, Optional


class Node(object):
    def __init__(self, data: Any, next_node: Optional[Node] = None) -> None:
        # Any：なんでも入れていいですよ
        self.data = data
        self.next = next_node


class LinkedList(object):
    def __init__(self, head: Optional[Node] = None) -> None:
        self.head = head

    def append(self, data: Any) -> None:
        """LinkedListの最後尾にノードを追加する"""
        new_node = Node(data)
        if self.head is None:  # LinkedListが空っぽの場合
            self.head = new_node
            return

        # 現在の最後尾のNodeを探す
        last_node = self.head
        while last_node.next:  # Noneになるまで
            last_node = last_node.next
        # 最後尾のノードのnextにnew_nodeを追加する
        last_node.next = new_node

    def insert(self, data: Any) -> None:
        """先頭に要素を追加する"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def print(self) -> None:
        """printを簡単にするメソッド"""
        current_node = self.head
        while current_node:  # next属性がNone=最後尾になるまで
            print(current_node.data)
            current_node = current_node.next

    def remove(self, data: Any) -> None:
        """指定したdataを持つNodeをListを取り除く"""
        current_node = self.head

        # もし先頭のNodeが削除対象だったら
        if current_node and current_node.data == data:
            self.head = current_node.next
            current_node = None  # もう使わない→ほっといてもいいけどNoneを指定した方がメモリ消費がいい(selfに保存してないからremove完了後に消えるのでは?)
            return

        previous_node = None
        while current_node and current_node != data:
            previous_node = current_node
            current_node = current_node.next

        # 削除するデータが見つからなかった状態でwhileループを抜けたパターン
        if current_node is None:
            return

        # current_nodeを削除
        previous_node.next = current_node.next
