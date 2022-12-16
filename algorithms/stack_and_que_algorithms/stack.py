"""スタックとは.
- コーディングはそこまで難しくはないが、概念的に図で理解しておいた方が良い。
- Empty=Listだとみなす。
- そこに数字1をPushしている(入れている)
- その後に更に2を加えている(Pushしている)
- 1の上に2が乗っかるようなイメージ＝＞これをStackで表現している
- Listに対してPop(取り出す)する時
    - 2が上にあるので、まず２を上に取り出す
    - ＝つまり、最後に入れたものをPopで取り出す！
- コーディングする際にこの考え方を使って、色々なアルゴリズムを作っていく&解いていくケースがある。
    - 例えばアルゴリズムのクイズをやる時：
    - 1を入れて２を入れて2から取り出す…といったスタックの考え方を使うケースが多い。
"""

from typing import Any


class Stack(object):
    """Listを使って、概念的な考えで、Stackを実装してみる。
    まあ単にメソッド名をpush & popとして作っただけ。
    """

    def __init__(self) -> None:
        self.stack = []  # emptyを作る

    def push(self, data: Any) -> None:
        self.stack.append(data)  # 単純に

    def pop(self) -> Any:
        if self.stack:
            return self.stack.pop()


if __name__ == "__main__":
    stack = Stack()
    print(stack.stack)
    stack.push(1)
    print(stack.stack)
    stack.push(2)
    print(stack.stack)
    print(stack.pop())
    print(stack.stack)
    print(stack.pop())
    print(stack.stack)
