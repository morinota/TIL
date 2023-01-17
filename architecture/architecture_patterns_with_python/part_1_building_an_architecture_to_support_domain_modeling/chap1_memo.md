# 1. Chapter 1. Domain Modeling

ドメインモデリングの為のいくつかの重要なパターン: Entity, Value Object, Domain Service.

## 1.1. What is Domain Model? ドメインモデルとは？

3層アーキテクチャの中心層 = ビジネスロジック層 = ドメインモデル

- ドメイン = 解決したい課題や自動化したいプロセス
- モデル = あるプロセスや現象について、有用な性質を捉えて構造化・単純化したもの

- ドメイン駆動設計（DDD）= ドメインモデルを構築しそのモデルを中心にアーキテクチャを構築する事
  - -> モデルを外部の制約からできる限り解放し、リファクタしやすくする.

本書で例題として解決したい課題: **在庫の割り当ての新しい方法(new allocation mechanism)**を導入したい.
じゃあこの場合のドメインは、"在庫を割り当てる行為やプロセス"かな?

## 1.2. Exploring the Domain Language ドメイン言語の探索

最初のプロセスとして、ドメインに関連する様々な用語を探索・定義する必要があるっぽい.

以下は、例題における用語.

- SKU(Stock-Keeping Unit):
  - "スキュー"と発音する.
  - 商品毎を識別する文字列. (商品名っぽい.)
  - ~~(ex. 椅子10個, ランプ1個, 鉛筆12本=1ダースみたいなイメージ?)~~
  - 顧客が注文した際には、注文毎にユニークな番号が付き、SKUとその個数が保存される.

以下は在庫に関する振る舞い(こうあるべきという挙動の定義?　ビズネスルール?)

- 在庫のバッチ(=ひとかたまり, DBにおける各行?)は、reference(id), SKU, 数量を保持している.
- 在庫バッチにorder line(注文書)を割り当てると、顧客の配送先に在庫が送られ、利用可能な量が減る.
  - ex) sku=SMALL-TABLEが20台分あり、2台分の受注枠を確保しました. -> 利用可能なSMALL-TABLEが20-2=18台になる.
- 在庫バッチで利用可能な数量が注文行の数量より少ない場合、注文を割り当てる事ができない.
  - ex) テーブル1台分のバッチと、テーブル2台分のオーダーラインがある.
  - この場合、バッチにオーダーラインを割り当てる事はできない.
- 同じ注文を2回割り当てることはできない.
  - 在庫バッチが10個あり、BLUE-VASEのオーダーラインを2個分確保した.
  - このオーダーラインを同じバッチに再度割り当てても、そのバッチの利用可能数量は8個のままとなるはず.
- バッチ(=在庫??)には、現在出荷(=倉庫に来る前??)中のケースも倉庫にあるケースもある.
  - 現在出荷中の場合はETAが表示される.
  - オーダーラインが入った際には、出荷中のバッチよりも倉庫内のバッチを優先的に割り当てる.
  - 出荷バッチは、ETAが早いものから順に割り当てる. (賞味期限があるような商品をイメージするといいかも!)

## 1.3. Unit Testing Domain Models ドメインモデルの単体テスト

いくつかのユニットテストを書いて、1.2で定義・探索したビジネスルール(= ドメインはこうあるべきという挙動の定義?)を、コードで表現してみる.

ユニットテスト内で定義した名称について: (1.2の際に一緒に定義・探索したビジネスマンに見せても意味が伝わるように.)

- テスト関数名: システムから得たい動作を記述.
- 使用するクラスと変数の名前: ビジネス用語から.

↑つまり、**1.2で探索したドメイン言語(Domain Language)を反映**している!!

pythonにおいてtype hintの有無はまだ論争の的になっているらしいが(そうなの...??)、特にドメインモデルにおいては、期待される引数が何であるかを明確にしたり文書化したりするのに役立つ.

デクリメント=カウンタ等の値を一定の値だけ減算する事.

chapter1の時点ではDDD（あるいはオブジェクト指向！）を使うには、ドメインモデルがあまりに些細すぎるだろう.
しかし現実には、例えば以下の様に、多くの**ビジネスルール**や**エッジケース**が発生する.

- ex) 顧客は将来の特定の日付に配送を依頼することができ、その場合、最も早いバッチに顧客を割り当てたくないかもしれない.
- ex2) SKUによっては、バッチではなく、サプライヤーから直接オンデマンドで注文されるため、異なるロジックを持つことになる.
- ex3) 注文したユーザの地域によっては、その地域にある倉庫や出荷の一部に優先的に割り当てたりする. ただし、その地域で在庫がない場合は、別の地域の倉庫から出荷することもある.

このchapter 1 の単純なドメインモデルを、**より複雑なもののためのプレースホルダー**として、この本の残りの部分で単純なドメインモデルを拡張し、APIやデータベースやスプレッドシートの現実の世界に差し込んでいいく.
(プレースホルダー: 実際の内容を後から挿入する為に、とりあえず仮に確保した場所の事)

カプセル化と慎重なレイヤリングの原則を厳格に守ることが、 泥の玉を避けるためにどのように役立つか、私たちは知ることになる...?

### 1.3.1. おまけ: より細かい型ヒント

`typing.NewType`を使ってプリミティブ(原始的)な型(i.e. 組み込みデータ型)をラッピングすることまでできる.

```python
from dataclasses import dataclass
from typing import NewType

Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)
...

class Batch:
    def __init__(self, ref: Reference, sku: Sku, qty: Quantity):
        self.sku = sku
        self.reference = ref
        self._purchased_quantity = qty
```

これをすばらしいと思うか、ひどいと思うかは議論の分かれるところ.

### 1.3.2. データクラスはValue Objectsに最適

例題におけるビジネス言語(=Domain Language)では、オーダーは複数のラインアイテムを持ち、それぞれのラインは SKU と数量を持っています.
注文情報を含むシンプルな YAML ファイルは次のようになると想像できる.

```yaml
Order_reference: 12345 # Orderはそれを一意に識別するidを持っている.
Lines:
  - sku: RED-CHAIR # lineはそれを一意に識別するidを持っていない.
    qty: 25
  - sku: BLU-CHAIR
    qty: 25
  - sku: GRN-CHAIR
    qty: 25
```

**データを持ちながら、それを"一意に定める"IDを持たないビジネスコンセプト**がある場合、私たちはしばしば**Value Objectパターンを使ってそれを表現する**ことを選択する.
(~~逆に言えば、"それを一意に識別するid"を持っているケースではvalue objectパターンを使わない...???
下の`OrderLine`クラスは`orderid`があるが、これはOrderLineを一意に識別するidではない. あくまでOrderという単位のid.)

Value Objectパターン: それが**保持するデータによって一意に識別される**Domain Objectのこと. 通常、イミュータブル（不変）なオブジェクトにする.

```python
@dataclass(frozen=True)
class OrderLine:
    orderid: OrderReference
    sku: ProductReference
    qty: Quantity

```

データクラス(または`namedtuples`)が与えてくれる素晴らしいものの1つに、**値の等価性(value equality)**がある.
これは、「**同じ `orderid`, `sku`, `qty` を持つ2つの行は等しい**」という意味.

バリューオブジェクトのその他の例:

```python
from dataclasses import dataclass
from typing import NamedTuple
from collections import namedtuple

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str

class Money(NamedTuple):
    currency: str
    value: int

Line = namedtuple('Line', ['sku', 'qty'])

def test_equality():
    assert Money('gbp', 10) == Money('gbp', 10)
    assert Name('Harry', 'Percival') != Name('Bob', 'Gregory')
    assert Line('RED-CHAIR', 5) == Line('RED-CHAIR', 5)
```

これらのvalue objectは、その価値の仕組みについて私たちの現実世界での直感と一致している.

- ex) どの10ポンド札について話していても、すべて同じ価値を持つ.
- ex) 2つの名前は姓と名の両方が一致すれば等しい.
- ex) 2つのラインは顧客オーダー、商品コード、数量が同じなら等価.

また、value objectに対して複雑な振る舞いをさせることもできる.
実際、値に対する演算をサポートすることはよくあることで、例えば、数学演算子などが挙げられる.

### 1.3.3. Value ObjectとEntity

OrderLineは、**オーダーID、SKU、数量の3つの値によって一意に識別**され、これらの値のいずれかを変更すると、新しいLineが作成される.
=> これがまさにvalue objectの定義です。データのみで識別され、**長期間の同一性を持たない**(=一部の値を変更すると別のオブジェクトになる点??)オブジェクトのこと.

一方で、Batchはどうだろうか?
これはreferenceによって識別される.

ここでは、**長期間の同一性を持つ**ドメインオブジェクトを表すために、**Entity**という言葉を使う.

- ex)名前はValue Object, でも人間はEntity
  - Harry Percival という名前を一文字変えてみると、Barry Percival という新しい `Name` オブジェクトが得られる. `Harry Percival != Barry Percival`は明らか.
  - 一方でハリーという人間はどうだろう.
  - 人は名前を変え、配偶者の有無や性別さえも変えるが、**私たちはその人を同じ個人として認識し続ける**. それは、人間は名前と違って、**永続的なアイデンティティ**を持っていから.

```python
def test_name_equality():
    assert Name("Harry", "Percival") != Name("Barry", "Percival")
```

```python
class Person:

    def __init__(self, name: Name):
        self.name = name


def test_barry_is_harry():
    harry = Person(Name("Harry", "Percival"))
    barry = harry

    barry.name = Name("Barry", "Percival")

    assert harry is barry and barry is harry
```

EntityはValue Objectと異なり、**同一性の平等性(identity equality)を持っている**.
valueを変えても、同じものだと認識できる.
例題においては、バッチはEntiryです。
バッチに行を割り当てても、到着予定日を変えても、同じEntiryであることに変わりはない.

### 1.3.4. `__eq__`と`__hash__`で Value ObjectかEntity Objectかをより明示的に定義する.

通常は、Entityに以下のように**等号演算子(equality operator)**を実装することで、これをコードで明示する.

```python
class Batch:
    ...

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference # ユニークなidが一致している限りTrue

    def __hash__(self):
        return hash(self.reference)
```

Python の `__eq__` マジックメソッドは `==` 演算子に対するクラスの振る舞いを定義している.

EntityオブジェクトとValueオブジェクトの両方について、 `__hash__` がどのように動作するかを考えておくことも重要. (=**オブジェクト毎にユニークな値であるハッシュ値をどう生成するか**の定義??)
これは Python がオブジェクトをセットに追加したり、dict のキーとして使用したりする際に、オブジェクトの振る舞いを制御するために使用するマジックメソッド. Python ドキュメントに詳細が記載されている.

Value Objectの場合、ハッシュはすべての値属性(value attribute)に基づくべきで、オブジェクトが不変であることを保証する必要がある.
データクラスに `@frozen=True` を指定することで、これを楽に定義する事ができる.(`__hash__`の指定を代替できる?)

Entity Objectの場合、エンティティの場合、最もシンプルなオプションはハッシュが `None` であること.
これは、**そのオブジェクトがハッシュ可能ではなく**、例えば、**セット(集合)の中で使用できないこと**を意味します.
(set内で使用できる = ハッシュ可能なオブジェクト)
(ex. 同じ名前の人間が二人いたとして、それらをsetに入れても一人としてまとめられるべきではない.)
もし何らかの理由で、Entity objectに対してセットやディクショナリーを使用したい場合、ハッシュは `.reference` のような属性(i.e. **そのオブジェクトを一意に識別するid)に基づく必要がある**.
また、その"一意に識別するid"のような属性は、**読み取り専用で書き換え不可であるように**すべき.

- Warning
- これは厄介な領域で、 `__eq__` を変更せずに `__hash__` を変更すべきではない.

## 1.4. Not Everything Has to Be an Object: A Domain Service Function 何でもかんでもオブジェクトにすればいいってもんじゃない。 ドメインサービス機能

例題ではバッチを表すモデルを作ったが、実際に必要なのは、全在庫を表す"特定のバッチの集合"に対して、オーダーラインを割り当てること.

> Sometimes, it just isn’t a thing. 時には、ただモノでないこともある. Eric Evans, Domain-Driven Design

Evansさん曰く、Entity やValue Objectの中に自然な住処を持たない**Domain Service operations(ドメインサービス操作)**のアイデアを論じている.
(Domain Objectそのものが実行する操作ではない操作を、Domein Objectを操作する関数として定義するイメージ?)
バッチのセットが与えられたときに注文ラインを割り当てる操作は、関数とよく似ており、Pythonが**multiparadigm language(マルチパラダイム言語)**であることを利用して、それを関数として作ってあげれば良い. (上のpartでは`Batch`の`allocate`メソッドとして定義していた.)

`allocate`関数の設計にあたって、まず以下のようにtest-driveする.

```python
def test_prefers_current_stock_batches_to_shipments():
    """すでにあるBatch在庫に対して優先的にオーダーラインを割り当てる"""
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)  # 出荷中
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    """一番速く出荷が完了するbatch在庫に対して、優先的にオーダーラインを割り当てる"""
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    """オーダーラインをどのbatch在庫に割り当てるかの記録(Batchのユニークなid)を取得する"""
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference
```

テストコードにもとづいて、domain serviceの為のスタンドアロン関数`allocate()`を設計する.

```python
def allocate(line: OrderLine, batches: List[Batch]) -> str:
    """ある優先順でbatch在庫達を並び替え、
    最も優先順位の高いbatch在庫にオーダーラインを割り当てる.
    """
    batch = next(b for b in sorted(batches) if b.can_allocate(line))
    batch.allocate(line)
    return batch.reference
```

### 1.4.1. Python’s Magic Methods Let Us Use Our Models with Idiomatic Python Pythonのマジックメソッドでモデルを自在に操る

前のコードで `next()` を使うのが好きかどうかは別として、`Batch`のリストで `sorted()` を使える事は、素敵でidiomaticな(慣用的な? 特徴的な?) Python の利点.

これを実現するために、ドメインモデル上に マジックメソッド`__gt__` を実装する.

```python
class Batch:
    ...

    def __gt__(self, other: "Batch") -> bool:
        """オブジェクト間で大小関係を定義する.sorted(List[Batch])の時などに適用される.
        - True = selfの方が大きい(降順側になる).
        - False = otherの方が大きい. (昇順側になる.)
        """
        if self.eta is None:
            return False
        if other.eta is None:
            return True

        return self.eta > other.eta
```

### 1.4.2. Exceptions Can Express Domain Concepts Too 例外はドメインの概念も表現できる

最後にもう一つ、例外はドメインの概念を表現するために使うことができる.

ドメインエキスパート(ドメイン分野の専門家, 非エンジニア)との会話で、**在庫切れで注文が割り当てられない可能性があること**を知ったが、domain exceptionを使うことでそれを捉えることができる.

```python
def test_raises_out_of_stock_exception_if_cannot_allocate():
    """在庫切れ(out-of-stock)例外のテスト"""
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])
```

特に**ユビキタス言語(=全員で同じ言葉でコミュニケーションを行うための共通言語)**では、Entity、value object、Serviceと同様に、Exceptionの命名に気をつけるべき.

Domain exceptionを発生させる(model.py)

```python
class OutOfStock(Exception):
    pass


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(
        ...
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')
```

## 1.5. まとめ:

- Domain modeling ドメイン・モデリング:
- Distinguish entities from value objects EntityとValue Objectを区別する.
  - value objectは、その属性によって定義される. 通常、immutable型として実装するのが最適. **value objectの属性を変更すると、それは別のオブジェクトを表す**.
  - 一方でentityは、時間とともに変化する属性を持つが、それでも同一のEntityであることに変わりない.**Entityを一意に識別するもの**（通常、何らかのnameまたはreference フィールド）を定義することが重要.
- Not everything has to be an object すべてがオブジェクトである必要はない.
  - Python はマルチパラダイム言語なので、コードの中の「動詞」は関数にすべき.

That’ll probably do for now!
今のところ、これで大丈夫でしょう.

We have a domain service that we can use for our first use case.
最初のユースケースに使用できるドメインサービスがあります.

But first we’ll need a database…
しかし、まずデータベースが必要です...
