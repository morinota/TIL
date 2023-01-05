"""クイズ：linked listの中で,valueが偶数のものだけ並び替える
- リバースを元にインタビュークイズ
"""

from typing import Optional

from linked_list_1_single_direction import Node, SinglyLinkedList


class LinkedListWithReverseEven(SinglyLinkedList):
    def reverse_even(self) -> None:
        """linked listの中で,偶数が連続したら入れ替えていく.
        - 1,4,6,8,9=>1,8,6,4,9
        - 偶数が連続したら、その中で入れ替えていく
        - 1,2,3,4,5,6=>1,2,3,4,5,6
        """

        def _reverve_even(
            head_of_targets: Optional[Node],
            previous_node: Optional[Node],
        ) -> Node:
            """入れ替え対象範囲の先頭が変化していく.
            - current_head:入れ替え対象範囲の先頭.
            - previous_node: current_nodeの前のNodeの初期値.
            """
            if not head_of_targets:  # 最後尾に到達したケース
                return None

            current_node = head_of_targets
            while current_node and current_node.data % 2 == 0:
                temp_next_node = current_node.next  # 次のnodeを一旦cache

                current_node.next = previous_node  # 入れ替え処理(singley link listの為、 nextのみを更新)

                # 次のループの為にcache中の値をズラす
                previous_node = current_node
                current_node = temp_next_node

            if current_node != head_of_targets:  # 1つ以上偶数が連続していたケース
                # current_nodeには連続した偶数Node達の一つ後ろのnodeが入っている.
                head_of_targets.next = current_node  # 連続した偶数nodeの先頭のnextに奇数node or Noneを追加.
                _reverve_even(
                    head_of_targets=current_node,
                    previous_node=None,
                )
                return previous_node
            else:  # current_nodeがhead_of_targetsから進んでいないケース
                head_of_targets.next = _reverve_even(
                    head_of_targets=head_of_targets.next,
                    previous_node=head_of_targets,
                )  # 次のnodeからチェックする
                return head_of_targets

        self.head_node = _reverve_even(
            head_of_targets=self.head_node,
            previous_node=None,
        )


if __name__ == "__main__":
    linked_list = LinkedListWithReverseEven()
    linked_list.append(2)
    linked_list.append(4)
    linked_list.append(6)
    linked_list.append(1)
    linked_list.append(3)
    linked_list.append(5)
    linked_list.append(2)
    linked_list.append(4)
    linked_list.append(6)
    linked_list.print_data()

    print("######## Reverse Even")
    linked_list.reverse_even()
    linked_list.print_data()
