<!-- title: pythonでアルゴリズムとデータ構造の練習~ ソートアルゴリズム②Bubble Sort-->

# What is Bubble sort?

以下、wikipediaからの引用です。

> バブルソート（英: bubble sort）は、隣り合う要素の大小を比較しながら整列させるソートアルゴリズム。
> アルゴリズムが単純で実装も容易である一方、最悪時間計算量は O(n2) と遅いため、一般にはマージソートやヒープソートなど、より最悪時間計算量の小さな（従って高速な）方法が利用される。
> 基本交換法、隣接交換法[1]あるいは単に交換法とも呼ばれる。

ぼんやり私の理解ですが、「**隣り合う要素を比較**して、大小関係に応じて入れ替える」を全ての要素に対して適用していきます。

1. まずlimit line(ソート対象の範囲を表す境界線、みたいなイメージ)を配列の最後尾にセット
2. 先頭の要素から「**隣り合う要素を比較**して、大小関係に応じて入れ替える」処理を順番に繰り返していく.
3. ↑の処理が一周したら、この時点で、配列の最後尾の要素は確定している状態になる.(i.e. limit lineよりも左側で最も大きい要素が、配列の最後尾に置かれている状態)
4. limit lineを一つ前にズラし、再度`2 ~ 4`の動作を繰り返す.
5. limit lineが先頭まで来た時点でソート完了.

# implementation

ではpythonでBubble Sortを実装していきます。
`run_bubble_sort`関数は、引数としてソート対象の`numbers:List[int]`を受け取りBubbleソートを実行し、昇順ソートが完了された状態のnumbersを返します。

- まず、limit lineの場所(`limit_line_idx`)をnumbersの`最後尾の要素の右側`で初期化します.
- 以下の処理を、「limit lineの左側の要素が先頭の要素1つのみ」の状態になるまでwhileループで繰り返します.
  - 「隣り合う数字を比較して昇順に入れ替える」処理を先頭からlimit line内の最後尾の一つ手前まで順番に実行する.
  - 一周したら、limit_lineの場所を1つずつ手前にずらす. (一周した時点で、numbers[limit_line_idx-1]の要素の位置が確定した為、ソート候補から外します.)

```python
from typing import List


def run_bubble_sort(numbers: List[int]) -> List[int]:
    """List[int]を受け取りBubbleソートを実行し、昇順ソートが完了された状態のListを返す
    1. limit_lineの場所をnumbersの`最後尾の要素の右側`で初期化
    2. 「隣り合う数字を比較して昇順に入れ替える」処理を、
    先頭からlimit line内の最後尾の一つ手前まで順番に実行する.
    3. limit_lineの場所を1つずつ手前にずらす
    4. limit lineの左側の要素が先頭の要素のみになった時点でソート完了

    """
    limit_line_idx = len(numbers)

    while limit_line_idx > 1:
        for j in range(limit_line_idx - 1):  # limit line内の最後尾の一つ手前まで繰り返し
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
        limit_line_idx -= 1  # limit_lineを1つずつ手前にずらす

    return numbers
```

最後に、サンプルとなる数字配列を使って、Bubble Sortを実行してみます.

```python
if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(f"[LOG]init numbers: {numbers}")
    print(f"[LOG]sorted numbers: {run_bubble_sort(numbers)}")
```

出力された結果は以下です。問題なく昇順ソートが実行されていますし、Bogo Sortよりも明らかに実行時間が短い印象です...!(ただBubbleソートも決して早いソートアルゴリズムではない...!)

```
[LOG]init numbers: [484, 954, 316, 651, 349, 823, 207, 61, 255, 61]
[LOG]sorted numbers: [61, 61, 207, 255, 316, 349, 484, 651, 823, 954]
```

# References

- [wikipedia](https://ja.wikipedia.org/wiki/%E3%83%9C%E3%82%B4%E3%82%BD%E3%83%BC%E3%83%88)
- [現役シリコンバレーエンジニアが教えるアルゴリズム・データ構造・コーディングテスト入門](https://www.udemy.com/course/python-algo/)
