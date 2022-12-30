<!-- title: pythonでアルゴリズムとデータ構造の練習~ ソートアルゴリズム①Bogo Sort(Random Sort, Shotgun Sort, Monkey Sort)-->

# What is Bogo sort?

以下、wikipediaからの引用です.

> ボゴソート (bogosort) は、ソートのアルゴリズムの一つ。平均的な計算時間はO(n×n!)で、非常に効率の悪いアルゴリズムとして知られている。
> 英語では、**random sort**(ランダムソート), **shotgun sort**(「数撃ちゃ当たる」ソート), **monkey sort**(「猿でもできる」ソート) などといった表現がある。

要するに「**配列内の数字をランダムに(適当に)を並び替えて、ソートされているか確認する」をソートが完了するまで繰り返す**という、非常にシンプルなソートアルゴリズムですね...!

# implementation

ではpythonで実装していきます.

まずは配列(List)が昇順ソートされた状態か否かを判定して返す、`is_in_order()`関数を定義しておきます。
`numbers`を先頭からチェックしていき、`前の要素 > 後ろの要素`となる箇所が見つかった時点でFalseを返します。

```python
def is_in_order(numbers: List[int]) -> bool:
    """numbersが昇順ならTrueを返す関数を定義"""
    for i in range(len(numbers)-1):
        if numbers[i] > numbers[i+1]:
            return False
    return True
```

ちなみにリスト内包表記を使ったverは以下です.
やっている事は↑と同じで、build-in関数`all()`は引数で渡された`Iterator[bool]`内の要素が全て`True`の場合に`True`を返します.

```python
def is_in_order(numbers: List[int]) -> bool:
    """numbersが昇順ならTrueを返す関数を定義"""
    # list内包表記ver.
    return all([numbers[i] <= numbers[i + 1] for i in range(len(numbers) - 1)])
```

では、以下がBogoソートの実装です. 引数で受け取った`List[int]`を上で定義した`is_in_order`で判定しTrueを返すまで、`random.shuffle()`関数でランダムにシャッフルし続けています.

```python
import random


def run_bogo_sort(numbers: List[int]) -> List[int]:
    """List[int]を受け取りBogoソートを実行し、昇順ソートが完了された状態のListを返す.
    - 配列内の数字をランダムに(適当に)を並び替えて、ソートされているか確認する
    - 上の処理をソートが完了するまで繰り返す.
    """
    while not is_in_order(numbers): # is_in_order()がTrueにならない限り並び替え続ける
        random.shuffle(numbers)

    return numbers  # Trueになったら処理から抜ける
```

最後に、サンプルの配列を作って、実際にまわしてみます.

```python
if __name__ == "__main__":
    numbers = [random.randint(0, 1000) for _ in range(10)]
    print(f"[LOG]init numbers: {numbers}")
    print(f"[LOG]sorted numbers: {run_bogo_sort(numbers)}")
```

出力された結果は以下です。明らかに実行時間が長いですが、とりあえず昇順ソートされたnumbersが出力されました...!

```
[LOG]init numbers: [324, 689, 988, 603, 324, 95, 290, 787, 870, 997]
[LOG]sorted numbers: [95, 290, 324, 324, 603, 689, 787, 870, 988, 997]
```

# References

- [wikipedia](https://ja.wikipedia.org/wiki/%E3%83%9C%E3%82%B4%E3%82%BD%E3%83%BC%E3%83%88)
- [現役シリコンバレーエンジニアが教えるアルゴリズム・データ構造・コーディングテスト入門](https://www.udemy.com/course/python-algo/)
