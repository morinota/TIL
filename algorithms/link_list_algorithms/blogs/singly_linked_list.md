<!-- title: pythonでアルゴリズムとデータ構造の練習~ Linked List① Single Direction-->

# What is Linked List?

**Linked List(i.e. 連結リスト、リンクリスト)**とは、**最も基本的なデータ構造の1つ**であり、他のデータ構造の実装に使われる。リンクリスト、リンクトリストとも表記されます.

## What is Singly-linked list?

> 片方向リスト（singly-linked list）は、最も単純な連結リストであり、ノード毎に1つのリンクを持つ。

以下の特徴を持ちます。pythonで言えば`List`の中身の実装方法というイメージですね...!

- **Head(linked listの先頭の要素)**から、どんどん**ノード(DataとNextのセット)**が**連結**していく.
- Data:数値とか。Next:リンク（Nextの部分で後ろのノードと結びつける）
- データを追加したり、削除したりが、headからリンクをたどって行うのに適している構造.

# implementation

ではpythonで実装していきます。

## Linked Listの各要素: `Node`クラス

まずはlinked Listの各要素となる`Node`クラスを定義します。データ(`data` field)とリンク(`next` field)を保持さえしてくれれば良いので、`dataclasses.dataclass`で定義しました:)

```python
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Node:
    data: Any
    next: Optional["Node"] = None
```

## `SinglyLinkedList`クラス

続いて、連なった`Node` dataclass達をコントロールする`SinglyLinkedList`クラスを定義します。
コンストラクタ`__init__`では、Linked listの先頭のノード(`head_node`)をインスタンス変数に登録します。

```python
class SinglyLinkedList:
    def __init__(self, head_node: Optional[Node] = None) -> None:
        self.head_node = head_node
```

## Linked Listの最後尾にデータを追加する: `append`メソッド

続いて、Linked Listの最後尾にノードを追加する`append`メソッドを定義します。引数で追加したいデータ(`data`)を受け取り、linked Listの最後尾に登録します.
まず受け取った`data`を使って、`Node`オブジェクトを`new_node`として生成します。
Linked Listに要素が一つも登録されていない(i.e. `head_node`が`None`)のケースでは、`new_node`を先頭のノードとして登録します。
すでに要素が一つ以上登録されているケースでは、最後尾のノード(`last_node`)を探したのち、最後尾のノードの`next` fieldにnew_nodeを登録します。

```python
class SinglyLinkedList:
    # 略

    def append(self, data: Any) -> None:
        """Singly Linked Listの最後尾にノードを追加する"""
        new_node = Node(data)

        if self.head_node is None:  # Linked Listが空っぽのケース
            self.head_node = new_node
            return

        # SinglyLinkedListの最後尾のNodeを探す
        last_node = self.head_node
        while last_node.next:
            last_node = last_node.next

        last_node.next = new_node # 最後尾のNodeとnew_nodeをリンクする
```

## Linked Listの先頭にデータを追加する: `insert`メソッド

続いて、Linked Listの先頭にデータを追加する`insert`メソッドを定義します。
これは単に`new_node`をHeadとリンクさせて、Headとして登録しているNodeを置き換えるだけですね!

```python
class SinglyLinkedList:
    # 略

    def insert(self, data: Any) -> None:
        """Linked Listの先頭に要素を追加する"""
        new_node = Node(data)
        new_node.next = self.head_node
        self.head_node = new_node
```

## Linked Listから指定されたデータを取り除く: `remove`メソッド

続いて、Linked Listに登録されたデータの中から指定されたデータを取り除く`remove`メソッドを定義します。Linked Listの中に指定されたデータが複数あるケースでは、「よりHeadに近いデータのみを削除する」仕様にしてみます。

まずLinked Listの先頭(head)が削除対象のデータと一致するケースでは、headノードの次のノードをheadとして置き換えてearly returnします。

headが削除対象でないケースでは、whileループを使って、削除対象と一致するノードをheadの次から最後尾まで順番に探していきます。この際、最終的な削除処理(i.e. 削除後のリンクをつなぎ直す処理)の為に、一つ前のノードを`previous_node`としてキャッシュしておきます。

最後尾まで確認して削除対象が発見できなかったケースでは、Noneを返してearly returnします。

最後にheadより後ろで削除対象が発見されたケースでは、削除対象のノードの前後のノードをリンクさせる事で、対象ノードをLinked Listから削除します。

```python
class SinglyLinkedList:
    # 略

    def remove(self, data: Any) -> None:
        """指定したdataを持つNodeをListを取り除く.
        Linked Listの中に指定されたデータが複数あるケースでは、
        よりHeadに近いデータのみを削除する.
        """
        current_node = self.head_node # 先頭から削除対象のNodeを探していく

        if current_node and current_node.data == data:  # 先頭のNodeが削除対象のケース
            self.head_node = current_node.next
            return

        previous_node = None # 削除処理に備えて一つ前のNodeをcacheしておく
        while current_node and current_node != data:
            previous_node = current_node
            current_node = current_node.next

        # Linked list内で削除するデータが発見されなかったケース
        if current_node is None:
            return

        # current_nodeの両サイドのデータをリンクさせる
        previous_node.next = current_node.next
```

## Singly Linked Listを逆方向に並び替える: `reverse`メソッド

続いて、Singly Linked Listを逆方向に並び替える`reverse`メソッドを定義します。まずwhileループを使って実装するver.として`reverse_iterative`メソッドを定義しました。

linked listのheadから順に、対象ノード(`current_node`)の前後のノード(`previous_node`, `temp_next_node`)をキャッシュしながら順番を入れ替えていきます。
最終的には、最後尾だったノードをlinked listの先頭に登録しなおして完了です.

```python
class SinglyLinkedList:
    # 略

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

            # 次のループの為に変数を更新(対象ノードをズラシていく)
            previous_node = current_node
            current_node = temp_next_node

        self.head_node = previous_node  # 最後尾だったNodeをheadに登録
```

続いて、recursive(再帰処理)を使うver.を`reverse_recursive`メソッドとして実装しました。
recursiveは頭がこんがらがってしまい苦手ですが、やっている事は`reverse_iterative`と同様ですね:)
再帰処理の為のinnor関数`_reverse_recursive`をメソッド内で定義し、linked listのheadから処理をスタートさせています。
再帰処理もwhileループと同様にbreakの箇所を設定しなければ無限に続いてしまうので、`if not current_node:`でearly returnして再帰処理をbreakしています。この箇所が`reverse_iterative`でいうところの`while current_node:`に対応しています。
(個人的にはこの**無限に続く処理をbreakする箇所を意識する事**が、recursiveを設計・理解するtipsなのかなー...と思ったりしました...!)

```python
class SinglyLinkedList:
    # 略

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
            if not current_node:  # 最後尾に到達したケース(ここでrecursiveを抜ける!)
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
```

## 最後に動作確認

最後に、各メソッドを動作確認してみます。

linked listの中身のデータ達を確認しやすくする為に、`print_data`メソッドを定義します。このメソッドでは、linked listの中身を先頭から順に出力していきます。

```python
class SinglyLinkedList:
    # 略
    def print_data(self) -> None:
        """linked listの中身を先頭から順に出力する"""
        current_node = self.head_node
        while current_node:  # 最後尾まで順に出力
            print(current_node.data)
            current_node = current_node.next
```

動作確認用に以下の処理を実行させてみます。

```python
if __name__ == "__main__":
    singly_linked_list = SinglyLinkedList()
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
```

結果として以下が出力されました。各メソッドが想定どおりに動作してくれています:)

```
10
0
1
2
3
======remove 2======
10
0
1
2
3
====== Reverse Iter ======
3
2
1
0
10
====== Reverse Recursive======
10
0
1
2
3
```

# References

- [wikipedia](https://ja.wikipedia.org/wiki/%E9%80%A3%E7%B5%90%E3%83%AA%E3%82%B9%E3%83%88)
- [現役シリコンバレーエンジニアが教えるアルゴリズム・データ構造・コーディングテスト入門](https://www.udemy.com/course/python-algo/)
