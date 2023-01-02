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


from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    data: Any
    next: Optional["Node"] = None


class SinglyLinkedList:
    def __init__(self, head_node: Optional[Node] = None) -> None:
        self.head_node = head_node

    def append(self, data: Any) -> None:
        """LinkedListの最後尾にノードを追加する"""
        new_node = Node(data)

        if self.head_node is None:  # LinkedListが空っぽのケース
            self.head_node = new_node
            return

        # 現在の最後尾のNodeを探す
        last_node = self.head_node
        while last_node.next:
            last_node = last_node.next
        # 最後尾のノードのnextにnew_nodeを追加する
        last_node.next = new_node

    def insert(self, data: Any) -> None:
        """Linked Listの先頭に要素を追加する"""
        new_node = Node(data)
        new_node.next = self.head_node
        self.head_node = new_node

    def print_data(self) -> None:
        """printを簡単にするメソッド"""
        current_node = self.head_node
        while current_node:  # next属性がNone=最後尾になるまで
            print(current_node.data)
            current_node = current_node.next

    def remove(self, data: Any) -> None:
        """指定したdataを持つNodeをListを取り除く.
        Linked Listの中に指定されたデータが複数あるケースでは、
        よりHeadに近いデータのみを削除する.
        """
        current_node = self.head_node  # 先頭から削除対象のNodeを探していく

        if current_node and current_node.data == data:  # 先頭のNodeが削除対象のケース
            self.head_node = current_node.next
            current_node = None  # もう使わない→ほっといてもいいけどNoneを指定した方がメモリ消費がいい(selfに保存してないからremove完了後に消えるのでは?)
            return

        previous_node = None  # 削除処理に備えて一つ前のNodeをcacheしておく
        while current_node and current_node != data:
            previous_node = current_node
            current_node = current_node.next

        # Linked list内で削除するデータが発見されなかったケース
        if current_node is None:
            return

        # current_nodeの両サイドのデータをリンクさせる
        previous_node.next = current_node.next


if __name__ == "__main__":
    singly_linked_list = SinglyLinkedList()
    singly_linked_list.append(1)
    singly_linked_list.append(2)
    singly_linked_list.append(3)
    singly_linked_list.insert(0)

    singly_linked_list.print_data()
    singly_linked_list.remove(data=2)
    singly_linked_list.print_data()
