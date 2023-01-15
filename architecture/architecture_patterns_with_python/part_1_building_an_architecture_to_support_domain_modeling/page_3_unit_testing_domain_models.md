## Unit Testing Domain Models

本書ではTDDの仕組みは紹介しませんが、このビジネスの会話からどのようにモデルを構築していくかを紹介したいと思います。

- EXERCISE FOR THE READER
  - この問題を自分で解決してみるのはどうでしょう？いくつかのユニットテストを書いて、ビジネスルールのエッセンスをきれいなコードで表現できるかどうか試してみましょう。
  - GitHub にいくつかのユニットテストのテンプレートがありますが、ゼロから始めることもできますし、好きなように組み合わせたり書き直したりすることもできます。

最初のテストのひとつは、こんな感じです。

A first test for allocation (test_batches.py)

```python
def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('order-ref', "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18
```

ユニットテストの名前は、私たちがシステムから得たい動作を記述しており、使用するクラスと変数の名前は、ビジネス用語から取られている。
このコードを技術者でない同僚に見せれば、これがシステムの動作を正しく記述していることに同意してくれるだろう。

そして、これが私たちの要求を満たすドメインモデルです。

バッチのドメインモデルの最初のカット (model.py)

```python
@dataclass(frozen=True) # 1, # 2
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]  2
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_quantity = qty

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.qty  3
```

- #1: `OrderLine`は、動作のないイミュータブルなデータクラスである2。
- #2: 私たちは、コードをきれいに保つために、ほとんどのコードリストでインポートを表示しません。これはdataclasses import dataclassから来たものだと推測してほしい。同様に、typing.Optionalとdatetime.dateもそうである。もし何かを再確認したいのであれば、各章のブランチ（例：chapter_01_domain_model）で完全な作業コードを見ることができます。
- #3: **タイプヒント**はPythonの世界ではまだ論争の的となっています。ドメインモデルについては、期待される引数が何であるかを明確にしたり文書化したりするのに役立つことがあり、IDEを持つ人々はしばしばそれをありがたがることがあります。あなたは、可読性という点で支払った代償が高すぎると判断するかもしれません。

`Batch`は単に整数の`available_quantity`をラップし、割り当て時にその値をデクリメントしています。ある数字から別の数字を引くだけのコードを大量に書きましたが、私たちのドメインを正確にモデル化することが報われると考えています3。

Let’s write some new failing tests:

Testing logic for what we can allocate (test_batches.py)

```python
def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch("batch-001", sku, batch_qty, eta=date.today()),
        OrderLine("order-123", sku, line_qty)
    )


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("ELEGANT-LAMP", 20, 2)
    assert large_batch.can_allocate(small_line)

def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("ELEGANT-LAMP", 2, 20)
    assert small_batch.can_allocate(large_line) is False

def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line("ELEGANT-LAMP", 2, 2)
    assert batch.can_allocate(line)

def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", 100, eta=None)
    different_sku_line = OrderLine("order-123", "EXPENSIVE-TOASTER", 10)
    assert batch.can_allocate(different_sku_line) is False
```

ここでは、あまり予想外のことはありません。テストスイートをリファクタリングして、同じ SKU に対してバッチとラインを作成するために**同じ行を繰り返さないようにし**、新しいメソッド `can_allocate` に対して 4 つのシンプルなテストを書きました。ここでも、私たちが使っている名前はドメインエキスパートの言語を反映しており、私たちが合意した例は直接コードに書き込まれていることに注目してください。

A new method in the model (model.py)

```python
def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
```
