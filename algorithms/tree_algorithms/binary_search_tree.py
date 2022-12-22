"""
- そもそもツリー構造とは
    - 配列やリスト、ディクショナリー等と同様に、"複数のデータを表す場合に有効"なデータ型.
    - ↑に挙げたデータ構造は、"階層を持つデータ"の集まりを表すことは苦手.
    - それが得意なのが、ツリー構造.
- Binary search treeとは
    - tree構造はたくさんの種類がある(wikipediaより)
    - 今回はその中で、binary treeについてみていく
- Binary Tree
    - Binary の意味：０と１＝＞2つの分岐
    - Binary search treeとHeapの2種類を見ていく
- まずBinary search treeの概要
    - inputの先頭の数字を置いて、それ以降、他の数字との大小を比較する
    - -> 置かれている数字よりも小さければ左へ、大きければ右へ枝を伸ばしていく
- 利点:
    - 例えば２を検索したいときに、シンプルなリストよりも早い
    - ソートしたいときも枝の生え方でソートできる（ex. 昇順の場合、左に生えてるかどうか)
- 削除の仕方:
    - １を削除しようとすると、ツリー構造が壊れる
    - １を削除したら、２を上にもってくる
    - ↑の様に、削除するノードから枝が一つしか生えていない場合は簡単。
    - 削除したいノードが"枝が下に２つ生えているノードのケース"はどうなるか？
        - 右のものを上に持ってくる
        - （↑によって親が左の子より大きいという法則が崩れない)
- Binary Search Treeのinorderとsearch:
    - Inorder: ツリーの中身を表示する
    - Search: 特定のvalueの場所を検索する
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    value: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def insert_to_binary_tree(
    value: int,
    node: Optional[Node] = None,
) -> Node:
    """insert対象のvalueと、insertされるNodeを指定して、insert後のNodeを返す
    - nodeが空であれば、そこにvalueを格納したnodeを作る
    - value < node.valueであれば、Treeの左側へ
    - value >= node.valueであれば、Treeの右側へ
    """
    if node is None:
        return Node(value=value)
    if value < node.value:
        node.left = insert_to_binary_tree(value, node.left)
    else:
        node.right = insert_to_binary_tree(value, node.right)
    return node


def inorder_binary_tree(node: Optional[Node] = None) -> None:
    """Treeの中身を順番に表示していく(i.e. Tree構造の中のvalueを昇順に出力していく)
    - Inorder:Left,root(根元),Right 今回はコレ
    - Preorder:root,Left,Right
    - Postorder:Left,Right,Root
    """
    if node is None:
        return None
    inorder_binary_tree(node=node.left)
    print(node.value)
    inorder_binary_tree(node=node.right)


def search_value_in_binary_tree(target_value: int, node: Optional[Node] = None) -> bool:
    """binary Treeの中にtarget_valueがあるかどうかを判定して返す"""
    if node is None:
        return False
    if target_value == node.value:
        return True
    elif target_value < node.value:
        return search_value_in_binary_tree(
            target_value,
            node=node.left,
        )
    elif target_value > node.value:
        return search_value_in_binary_tree(
            target_value,
            node=node.right,
        )


def min_value(node: Node) -> Node:
    """渡したnode以下で最もvalueが小さいnodeを返す(removeで重要)"""
    current_node = node
    while current_node.left is not None:  # いずれNoneのNodeに当たる
        current_node = current_node.left
    return current_node


def remove(node: Node, value: int) -> Node:
    if node is None:
        return node
    if value < node.value:
        node.left = remove(node=node.left, value=value)  # 左側を見るために再帰で呼び出す
    elif value > node.value:
        node.right = remove(node=node.right, value=value)  # 右側を見るために再帰で呼び出す

    else:  # 一致した場合(以下は、削除した後、下のNode達をどう繋ぐかの処理)
        if node.left is None:  # node.leftがないケース(Treeにおけるnode以下の部分でvalueが最小のケース)、nodeを削除してnode.rightを上に持ってくる
            return node.right
        elif node.right is None:  # node.rightがないケース
            return node.left

        # leftもrightもNoneでないケース(ex. target=6のケース)
        min_node_right_side = min_value(node=node.right)
        node.value = min_node_right_side.value  # 削除したいvalueを右側で最小のノードで置き換える
        node.right = remove(node=node.right, value=min_node_right_side.value)

    return node


if __name__ == "__main__":
    root_node = None
    root_node = insert_to_binary_tree(3, root_node)
    root_node = insert_to_binary_tree(6, root_node)
    root_node = insert_to_binary_tree(5, root_node)
    root_node = insert_to_binary_tree(7, root_node)
    root_node = insert_to_binary_tree(1, root_node)
    root_node = insert_to_binary_tree(10, root_node)
    root_node = insert_to_binary_tree(2, root_node)

    inorder_binary_tree(node=root_node)
    print(search_value_in_binary_tree(5, root_node))
    root_node = remove(root_node, value=6)
    inorder_binary_tree(root_node)
