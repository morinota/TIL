"""単方向リンクリストを逆方向に並び替える
- リスト型のreverseメソッドをリンクリストで作る
- コード例（2種類）
    - whileループでやるver
    - 再帰処理(recucible)でやるver
"""


# from linked_list_1_single_direction import LinkedList


from typing import Optional

from linked_list_1_single_direction import Node, SinglyLinkedList


class LinkedListWithReverse(SinglyLinkedList):
    def reverse_iterative(self) -> None:
        """List型のreverseメソッドをLinkedListで実装.
        - 対象ノードをcurrent_nodeとして取得.
        - current_nodeの前のノードを、current_node.nextへリンク
        while ループを使うver.
        """
        previous_node = None  # 入れ替え処理の為、前のnodeをcacheしておく
        current_node = self.head_node  # headから順番に
        while current_node:
            temp_next_node = current_node.next  # 次のnodeを一旦cache

            current_node.next = previous_node  # 入れ替え処理

            previous_node = current_node  # 前のnodeを更新
            current_node = temp_next_node  # cacheしたnext_nodeでcurrent_nodeを更新

        self.head_node = previous_node  # 最後尾だったNodeをheadに登録

    def reverse_recursive(self) -> None:
        """List型のreverseメソッドをLinkedListで実装.
        - 対象ノードをcurrent_nodeとして取得.
        - current_nodeの前のノードを、current_node.nextへリンク
        recursive(再帰処理)を使うver.
        """

        def _reverse_recursive(
            current_node: Optional[Node],
            previous_node: Optional[Node],
        ) -> Node:
            """innor関数"""
            if not current_node:  # 最後尾に到達したケース
                return previous_node  # reverse前で最後尾だったノードを返す

            temp_next_node = current_node.next  # 次のnodeを一旦cache

            current_node.next = previous_node  # 入れ替え処理

            # 次のループの為に変数を更新(対象ノードをズラシていく)
            previous_node = current_node
            current_node = temp_next_node
            return _reverse_recursive(current_node, previous_node)

        self.head_node = _reverse_recursive(
            current_node=self.head_node,  # headからスタート
            previous_node=None,
        )


if __name__ == "__main__":
    singly_linked_list = LinkedListWithReverse()
    singly_linked_list.append(0)
    singly_linked_list.append(1)
    singly_linked_list.append(2)
    singly_linked_list.append(3)
    singly_linked_list.insert(10)
    singly_linked_list.print_data()

    print("====== Remove 2======")
    singly_linked_list.remove(2)
    singly_linked_list.print_data()

    print("====== Reverse Iter ======")
    singly_linked_list.reverse_iterative()
    singly_linked_list.print_data()

    print("====== Reverse Recursive======")
    singly_linked_list.reverse_recursive()
    singly_linked_list.print_data()
