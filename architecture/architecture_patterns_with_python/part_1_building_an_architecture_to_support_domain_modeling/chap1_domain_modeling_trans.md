# Chapter 1. Domain Modeling 第1章 ドメイン・モデリング

This chapter looks into how we can model business processes with code, in a way that’s highly compatible with TDD.
この章では、TDDと親和性の高い方法で、ビジネスプロセスをコードでモデル化する方法について検討します。
We’ll discuss why domain modeling matters, and we’ll look at a few key patterns for modeling domains:
なぜドメインモデリングが重要なのかについて説明し、ドメインをモデリングするためのいくつかの重要なパターンを見ていきます。
Entity, Value Object, and Domain Service.
エンティティ、バリューオブジェクト、そしてドメインサービスです。

Figure 1-1 is a simple visual placeholder for our Domain Model pattern.
図1-1は、ドメインモデルパターンの簡単な視覚的プレースホルダーです。
We’ll fill in some details in this chapter, and as we move on to other chapters, we’ll build things around the domain model, but you should always be able to find these little shapes at the core.
この章では詳細を詰めていきます。他の章に進むにつれて、ドメインモデルを中心にしたものを構築していきますが、常に核となるこの小さな図形を見つけることができるようになるはずです。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0101.png)

## What is Domain Model? ドメインモデルとは？

In the introduction, we used the term business logic layer to describe the central layer of a three-layered architecture.
序章では、3層アーキテクチャの中心層を表すために、ビジネスロジック層という用語を使いました。
For the rest of the book, we’re going to use the term domain model instead.
この本の残りの部分では、代わりにドメインモデルという用語を使うことにします。
This is a term from the DDD community that does a better job of capturing our intended meaning (see the next sidebar for more on DDD).
これはDDDコミュニティからの用語で、私たちの意図する意味をよりよく捉えています（DDDについての詳細は次のサイドバーをご覧ください）。

The domain is a fancy way of saying the problem you’re trying to solve.
ドメインとは、あなたが解決しようとしている問題を表現する空想的な方法です。
Your authors currently work for an online retailer of furniture.
あなたの著者は現在、家具のオンライン小売業者で働いています。
Depending on which system you’re talking about, the domain might be purchasing and procurement, or product design, or logistics and delivery.
どのシステムについて話すかによって、ドメインは購買や調達、製品設計、または物流や配送になるかもしれません。
Most programmers spend their days trying to improve or automate business processes; the domain is the set of activities that those processes support.
多くのプログラマーは、ビジネスプロセスの改善や自動化に日々取り組んでいますが、ドメインとは、それらのプロセスがサポートする一連の活動のことです。

A model is a map of a process or phenomenon that captures a useful property.
モデルとは、あるプロセスや現象について、有用な性質を捉えた写像のことである。
Humans are exceptionally good at producing models of things in their heads.
人間は、頭の中で物事のモデルを作ることが非常に得意です。
For example, when someone throws a ball toward you, you’re able to predict its movement almost unconsciously, because you have a model of the way objects move in space.
例えば、誰かがボールを投げてきたとき、ほとんど無意識にその動きを予測することができるのは、空間における物体の動き方のモデルを持っているからです。
Your model isn’t perfect by any means.
しかし、このモデルは決して完璧ではありません。
Humans have terrible intuitions about how objects behave at near-light speeds or in a vacuum because our model was never designed to cover those cases.
光速に近い速度や真空での物体の動きについては、人間の直感は非常に鈍いものです。なぜなら、このモデルはそのようなケースを想定して設計されていないからです。
That doesn’t mean the model is wrong, but it does mean that some predictions fall outside of its domain.
だからといってモデルが間違っているわけではなく、ある予測はモデルの範囲外であることを意味します。

The domain model is the mental map that business owners have of their businesses.
ドメインモデルとは、ビジネスオーナーが自分のビジネスについて持っているメンタルマップのことです。
All business people have these mental maps—they’re how humans think about complex processes.
すべてのビジネスパーソンは、このメンタルマップを持っています。

You can tell when they’re navigating these maps because they use business speak.
このようなマップをナビゲートするとき、彼らはビジネス用語を使うのでわかります。
Jargon arises naturally among people who are collaborating on complex systems.
専門用語は、複雑なシステムで共同作業をしている人々の間で自然に生まれます。

Imagine that you, our unfortunate reader, were suddenly transported light years away from Earth aboard an alien spaceship with your friends and family and had to figure out, from first principles, how to navigate home.
もし、あなたが不幸にも友人や家族と一緒に宇宙船に乗って地球から何光年も離れた場所に突然飛ばされ、どうやって家に帰ろうかと第一原理から考えなければならなくなったと想像してください。

In your first few days, you might just push buttons randomly, but soon you’d learn which buttons did what, so that you could give one another instructions.
最初の数日は、ただ適当にボタンを押すだけかもしれませんが、すぐにどのボタンが何をするのかを覚えて、お互いに指示を出し合えるようになります。
“Press the red button near the flashing doohickey and then throw that big lever over by the radar gizmo,” you might say.
「点滅しているボタンの近くにある赤いボタンを押して、レーダー装置のそばにある大きなレバーを投げてください」と言うかもしれません。

Within a couple of weeks, you’d become more precise as you adopted words to describe the ship’s functions:
数週間もすれば、船の機能を説明する言葉を採用することで、より正確な表現ができるようになります。
“Increase oxygen levels in cargo bay three” or “turn on the little thrusters.”
「貨物室3の酸素濃度を上げる" "小型スラスターをオンにする"。
After a few months, you’d have adopted language for entire complex processes:
数カ月後には、複雑なプロセス全体を表す言葉を採用するようになる。
“Start landing sequence” or “prepare for warp.”
"着陸態勢に入る "とか "ワープに備える "とか
This process would happen quite naturally, without any formal effort to build a shared glossary.
このようなプロセスは、共有の用語集を作るような正式な努力なしに、ごく自然に起こるものである。

- THIS IS NOT A DDD BOOK. YOU SHOULD READ A DDD BOOK. これはDDの本ではありません。 DDDの本を読むべきでしょう。

- Domain-driven design, or DDD, popularized the concept of domain modeling,1 and it’s been a hugely successful movement in transforming the way people design software by focusing on the core business domain. Many of the architecture patterns that we cover in this book—including Entity, Aggregate, Value Object (see Chapter 7), and Repository (in the next chapter)—come from the DDD tradition. ドメイン駆動設計（DDD）は、ドメインモデリングの概念を普及させ1、中核となるビジネスドメインに焦点を当てることで、ソフトウェアを設計する方法を変革し、大きな成功を収めました。 本書で取り上げるEntity、Aggregate、Value Object（第7章参照）、Repository（次章参照）などのアーキテクチャパターンの多くは、DDDの伝統に由来するものである。

- In a nutshell, DDD says that the most important thing about software is that it provides a useful model of a problem. If we get that model right, our software delivers value and makes new things possible.

- If we get the model wrong, it becomes an obstacle to be worked around. In this book, we can show the basics of building a domain model, and building an architecture around it that leaves the model as free as possible from external constraints, so that it’s easy to evolve and change. モデルを間違えると、それが障害となり、回避することができなくなります。 本書では、ドメインモデルを構築し、そのモデルを中心にアーキテクチャを構築することで、モデルを外部の制約からできる限り解放し、進化や変更を容易にするための基本的な方法を紹介することができます。

- But there’s a lot more to DDD and to the processes, tools, and techniques for developing a domain model. We hope to give you a taste of it, though, and cannot encourage you enough to go on and read a proper DDD book: しかし、DDDとドメインモデルを開発するためのプロセス、ツール、テクニックには、もっとたくさんのものがあります。 しかし、私たちはその一端に触れることができ、適切なDDDの本を読むことをお勧めします。

- The original “blue book,” Domain-Driven Design by Eric Evans (Addison-Wesley Professional) 青い本」の元祖、エリック・エバンス著「ドメイン駆動設計」（アディソンウェスリープロフェッショナル社）

- The “red book,” Implementing Domain-Driven Design by Vaughn Vernon (Addison-Wesley Professional) 赤い本」Implementing Domain-Driven Design by Vaughn Vernon (Addison-Wesley Professional)

So it is in the mundane world of business.
ビジネスのありふれた世界でもそうである。
The terminology used by business stakeholders represents a distilled understanding of the domain model, where complex ideas and processes are boiled down to a single word or phrase.
ビジネス関係者が使う用語は、複雑なアイデアやプロセスを一つの単語やフレーズに煮詰めた、ドメインモデルの蒸留された理解を表しています。

When we hear our business stakeholders using unfamiliar words, or using terms in a specific way, we should listen to understand the deeper meaning and encode their hard-won experience into our software.
私たちは、ビジネス関係者が聞き慣れない言葉を使っていたり、特定の方法で用語を使っていたりするのを聞いたとき、深い意味を理解するために耳を傾け、彼らが苦労して得た経験をソフトウェアにコード化する必要があります。

We’re going to use a real-world domain model throughout this book, specifically a model from our current employment.
この本では、実世界のドメインモデル、特に私たちが現在勤めている会社のモデルを使うことにします。
MADE.com is a successful furniture retailer.
MADE.comは、成功した家具小売業者です。
We source our furniture from manufacturers all over the world and sell it across Europe.
私たちは世界中のメーカーから家具を調達し、ヨーロッパ全土で販売しています。

When you buy a sofa or a coffee table, we have to figure out how best to get your goods from Poland or China or Vietnam and into your living room.
ソファやコーヒーテーブルを購入する場合、ポーランドや中国、ベトナムから商品をどうやってリビングルームに運ぶのがベストなのかを考えなければなりません。

At a high level, we have separate systems that are responsible for buying stock, selling stock to customers, and shipping goods to customers.
大まかに言えば、在庫を買うシステム、顧客に在庫を売るシステム、顧客に商品を出荷するシステムが別々に存在します。
A system in the middle needs to coordinate the process by allocating stock to a customer’s orders; see Figure 1-2.
中間に位置するシステムは、顧客の注文に対して在庫を割り当てることで、このプロセスを調整する必要があります（図1-2参照）。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0102.png)

For the purposes of this book, we’re imagining that the business decides to implement an exciting new way of allocating stock.
本書では、ある企業が在庫配分の新しい方法を導入することを決定したと仮定します。
Until now, the business has been presenting stock and lead times based on what is physically available in the warehouse.
これまで、在庫とリードタイムは、倉庫にある物理的な在庫に基づいて表示されていました。
If and when the warehouse runs out, a product is listed as “out of stock” until the next shipment arrives from the manufacturer.
倉庫に在庫がなくなると、メーカーから次の出荷があるまで、その製品は「在庫切れ」と表示されます。

Here’s the innovation: if we have a system that can keep track of all our shipments and when they’re due to arrive, we can treat the goods on those ships as real stock and part of our inventory, just with slightly longer lead times.
もし、すべての出荷とその到着予定日を追跡できるシステムがあれば、それらの出荷された商品を実際の在庫として扱い、リードタイムを少し長くするだけで、在庫の一部として扱うことができるのです。
Fewer goods will appear to be out of stock, we’ll sell more, and the business can save money by keeping lower inventory in the domestic warehouse.
在庫切れの商品は少なくなり、販売量も増え、国内の倉庫の在庫を減らすことで経費も削減できます。

But allocating orders is no longer a trivial matter of decrementing a single quantity in the warehouse system.
しかし、オーダーの割り当ては、もはや倉庫システムで1つの数量をデクリメントするという些細な問題ではありません。
We need a more complex allocation mechanism.
もっと複雑な割り当てメカニズムが必要なのです。
Time for some domain modeling.
ドメイン・モデリングの時間だ。

## Exploring the Domain Language ドメイン言語の探索

Understanding the domain model takes time, and patience, and Post-it notes.
ドメインモデルを理解するには、時間と忍耐とポストイット・ノートが必要です。
We have an initial conversation with our business experts and agree on a glossary and some rules for the first minimal version of the domain model.
私たちは、ビジネスエキスパートと最初に話し合い、ドメインモデルの最初の最小バージョンのための用語集といくつかのルールに合意します。
Wherever possible, we ask for concrete examples to illustrate each rule.
可能な限り、各ルールを説明するための具体例を求めます。

We make sure to express those rules in the business jargon (the ubiquitous language in DDD terminology).
そのルールをビジネス用語（DDD用語でいうところのユビキタス言語）で表現するようにします。
We choose memorable identifiers for our objects so that the examples are easier to talk about.
オブジェクトの識別子には覚えやすいものを選び、事例が話しやすいようにします。

“Some Notes on Allocation” shows some notes we might have taken while having a conversation with our domain experts about allocation.
「アロケーションに関するメモ」は、アロケーションについて専門家と会話したときのメモを掲載しています。

- SOME NOTES ON ALLOCATION 割り付けに関する注意事項

- A product is identified by a SKU, pronounced “skew,” which is short for stock-keeping unit. Customers place orders. An order is identified by an order reference and comprises multiple order lines, where each line has a SKU and a quantity. For example: SKUとは、Stock-Keeping Unitの略で、「スキュー」と発音され、商品を識別する。 顧客は注文をする。 注文は注文参照番号で識別され、複数の注文行から構成され、各行にはSKUと数量がある。 例えば

- 10 units of RED-CHAIR RED-CHAIR10台

- 1 unit of TASTELESS-LAMP TASTELESS-LAMP 1台

- The purchasing department orders small batches of stock. A batch of stock has a unique ID called a reference, a SKU, and a quantity. 購買部門は、小ロットの在庫を発注する。 在庫のバッチは、リファレンスと呼ばれる一意のID、SKU、および数量を持っています。

- We need to allocate order lines to batches. When we’ve allocated an order line to a batch, we will send stock from that specific batch to the customer’s delivery address. When we allocate x units of stock to a batch, the available quantity is reduced by x. For example: バッチに注文書を割り当てる必要があります。 バッチにオーダーラインを割り当てると、そのバッチから顧客の配送先に在庫を送ることになる。 バッチに x 個の在庫を割り当てると、使用可能な数量が x 個減ります。たとえば、次のようになります。

- We have a batch of 20 SMALL-TABLE, and we allocate an order line for 2 SMALL-TABLE. SMALL-TABLEが20台分あり、SMALL-TABLE2台分の受注枠を確保しました。

- The batch should have 18 SMALL-TABLE remaining. バッチには、18個のSMALL-TABLEが残っているはずです。

- We can’t allocate to a batch if the available quantity is less than the quantity of the order line. For example: 使用可能な数量が注文行の数量より少ない場合、バッチに割り当てることができません。 例えば

- We have a batch of 1 BLUE-CUSHION, and an order line for 2 BLUE-CUSHION. BLUE-CUSHIONは、1台分のロットと2台分のオーダーラインがあります。

- We should not be able to allocate the line to the batch. バッチに回線を割り当てることはできないはずです。

- We can’t allocate the same line twice. For example: 同じ行を2回割り当てることはできません。 例えば

- We have a batch of 10 BLUE-VASE, and we allocate an order line for 2 BLUE-VASE. BLUE-VASEのロットが10個あり、BLUE-VASEの受注ラインを2個分確保しました。

- If we allocate the order line again to the same batch, the batch should still have an available quantity of 8. この注文書を同じバッチに再度割り当てると、そのバッチの利用可能数量は8個のままとなるはずです。

- Batches have an ETA if they are currently shipping, or they may be in warehouse stock. We allocate to warehouse stock in preference to shipment batches. We allocate to shipment batches in order of which has the earliest ETA. バッチには、現在出荷中の場合はETAが表示され、また、倉庫の在庫にある場合もあります。 出荷バッチよりも倉庫在庫に優先的に割り当てます。 出荷バッチは、ETAが早いものから順に割り当てる。

## Unit Testing Domain Models ドメインモデルの単体テスト

We’re not going to show you how TDD works in this book, but we want to show you how we would construct a model from this business conversation.
本書ではTDDの仕組みは紹介しませんが、このビジネスの会話からどのようにモデルを構築していくかを紹介したいと思います。

EXERCISE FOR THE READER
読書運動

Why not have a go at solving this problem yourself?
この問題を自分で解決してみるのはどうでしょう？
Write a few unit tests to see if you can capture the essence of these business rules in nice, clean code.
いくつかのユニットテストを書いて、ビジネスルールのエッセンスをきれいなコードで表現できるかどうか試してみてください。

You’ll find some placeholder unit tests on GitHub, but you could just start from scratch, or combine
GitHubにいくつかのユニットテストの候補がありますが、ゼロから始めるか、あるいは

Here’s what one of our first tests might look like:
最初のテストのひとつは、こんな感じです。

A first test for allocation (test_batches.py)
割り当ての最初のテスト(test_batches.py)

```python
def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine('order-ref', "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18
```

The name of our unit test describes the behavior that we want to see from the system, and the names of the classes and variables that we use are taken from the business jargon.
ユニットテストの名前は、私たちがシステムから得たい動作を記述しており、使用するクラスと変数の名前は、ビジネス用語から取られています。
We could show this code to our nontechnical coworkers, and they would agree that this correctly describes the behavior of the system.
このコードを技術者でない同僚に見せても、これがシステムの動作を正しく記述していることに同意してくれるでしょう。

And here is a domain model that meets our requirements:
そして、ここに我々の要求を満たすドメインモデルがある。

First cut of a domain model for batches (model.py)
バッチ用ドメインモデルのファーストカット(model.py)

```python
@dataclass(frozen=True)  12
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

- `OrderLine` is an immutable dataclass with no behavior.2 OrderLine` は振る舞いのないイミュータブルなデータクラスです。

- We’re not showing imports in most code listings, in an attempt to keep them clean. We’re hoping you can guess that this came via `from dataclasses import dataclass`; likewise, `typing.Optional` and datetime.date. If you want to double-check anything, you can see the full working code for each chapter in its branch (e.g., chapter_01_domain_model). 私たちは、コードをきれいに保つために、ほとんどのコードリストでインポートを表示していません。 これは `from dataclasses import dataclass`; 同様に `typing.Optional` と datetime.date から来ていると推測できるかと思います。 もし何かを再確認したいのであれば、各章のブランチで完全な作業コードを見ることができます (例: chapter_01_domain_model)。

- Type hints are still a matter of controversy in the Python world. For domain models, they can sometimes help to clarify or document what the expected arguments are, and people with IDEs are often grateful for them. You may decide the price paid in terms of readability is too high. タイプヒントはPythonの世界ではまだ論争の的になっています。 ドメインモデルについては、期待される引数が何であるかを明確にしたり文書化したりするのに役立つことがあり、IDEを持つ人々はしばしばそれをありがたがることがあります。 あなたは、可読性という点で支払った代償が高すぎると判断するかもしれません。

Our implementation here is trivial: a `Batch` just wraps an integer `available_quantity`, and we decrement that value on allocation.
バッチは単に整数の `available_quantity` をラップして、オーダーラインの割り当て時にその値をデクリメント(カウンタ等の値を一定の値だけ減算する事)しています。
We’ve written quite a lot of code just to subtract one number from another, but we think that modeling our domain precisely will pay off.3
ある数字から別の数字を引くだけのコードを大量に書いてしまいましたが、私たちのドメインを正確にモデル化することで、その成果を得ることができると考えています3。

Let’s write some new failing tests:
新しい失敗するテストを書いてみましょう。

Testing logic for what we can allocate (test_batches.py)
割り当て可能なロジックのテスト (test_batches.py)

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

There’s nothing too unexpected here.
ここでは、あまり予想外のことはありません。
We’ve refactored our test suite so that we don’t keep repeating the same lines of code to create a batch and a line for the same SKU; and we’ve written four simple tests for a new method `can_allocate`.
テストスイートをリファクタリングして、同じ SKU に対してバッチとラインを作成するために同じコードの行を繰り返し続けることがないようにしました。
Again, notice that the names we use mirror the language of our domain experts, and the examples we agreed upon are directly written into code.
繰り返しになりますが、私たちが使っている名前はドメインエキスパートの言語を反映しており、私たちが合意した例は直接コードに書き込まれていることに注意してください。

We can implement this straightforwardly, too, by writing the `can_allocate` method of `Batch`:
これも、 `Batch` の `can_allocate` メソッドを書けば、素直に実装できる。

A new method in the model (model.py)
モデル(model.py)に新しいメソッドを追加しました。

```python
    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
```

So far, we can manage the implementation by just incrementing and decrementing `Batch.available_quantity`, but as we get into `deallocate()` tests, we’ll be forced into a more intelligent solution:
今のところ、`Batch.available_quantity` をインクリメント、デクリメントするだけで実装を管理できますが、 `deallocate()` テストに入ると、よりインテリジェントな解決策を迫られることになります。

This test is going to require a smarter model (test_batches.py)
このテストでは、よりスマートなモデル(test_batches.py)が必要になりそうです。

```python
def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20
```

In this test, we’re asserting that deallocating a line from a batch has no effect unless the batch previously allocated the line.
このテストでは、バッチからオーダーの割り当てを解除しても、そのバッチが以前にそのオーダーを割り当てていない限り、何の効果もないことを主張しています。
For this to work, our `Batch` needs to understand which lines have been allocated.
これが動作するためには、`Batch` がどのオーダーが割り当てられたかを理解する必要があります。
Let’s look at the implementation:
では、その実装を見てみましょう。

The domain model now tracks allocations (model.py)
ドメインモデルがアロケーションを追跡するようになりました(model.py)

```python
class Batch:
    def __init__(
        self, ref: str, sku: str, qty: int, eta: Optional[date]
    ):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: Set[OrderLine]

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

```

Figure 1-3 shows the model in UML.
図 1-3 に UML によるモデルを示す。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0103.png)

Now we’re getting somewhere!
今、私たちはどこかに向かっているのです
A batch now keeps track of a set of allocated `OrderLine` objects.
バッチは、割り当てられた `OrderLine` オブジェクトのセットを追跡するようになりました。
When we allocate, if we have enough available quantity, we just add to the set.
割り当て時に、十分な空き数量があれば、そのセットに追加するだけです。
Our `available_quantity` is now a calculated property: purchased quantity minus allocated quantity.
この `available_quantity` は、購入数量から割り当て数量を引いた、計算されたプロパティです。

Yes, there’s plenty more we could do.
そうです、もっとできることがたくさんあるのです。
It’s a little disconcerting that both `allocate()` and `deallocate()` can fail silently, but we have the basics.
allocate()`と`deallocate()` の両方がサイレントで失敗する可能性があるのは少し気になりますが、基本はできています。

Incidentally, using a set for `._allocations` makes it simple for us to handle the last test, because items in a set are unique:
ちなみに、`._allocations`にセットを使用すると、セット内のアイテムが一意になるので、最後のテストを簡単に処理することができます。

Last batch test!
最後のバッチテスト!
(test_batches.py)
(test_batches.py)

```python
def test_allocation_is_idempotent():
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18
```

At the moment, it’s probably a valid criticism to say that the domain model is too trivial to bother with DDD (or even object orientation!).
現時点では、DDD（あるいはオブジェクト指向！）を使うには、ドメインモデルがあまりに些細すぎるという批判は、おそらく妥当なものでしょう。
In real life, any number of business rules and edge cases crop up: customers can ask for delivery on specific future dates, which means we might not want to allocate them to the earliest batch.
現実には、多くのビジネスルールやエッジケースが発生します。顧客は将来の特定の日付に配送を依頼することができ、その場合、最も早いバッチに顧客を割り当てたくないかもしれません。
Some SKUs aren’t in batches, but ordered on demand directly from suppliers, so they have different logic.
SKUによっては、バッチではなく、サプライヤーから直接オンデマンドで注文されるため、異なるロジックを持つことになります。
Depending on the customer’s location, we can allocate to only a subset of warehouses and shipments that are in their region—except for some SKUs we’re happy to deliver from a warehouse in a different region if we’re out of stock in the home region.
お客様の地域によっては、その地域にある倉庫や出荷の一部に割り当てることができます。ただし、その地域で在庫がない場合は、別の地域の倉庫から出荷することもあります。
And so on.
といった具合です。
A real business in the real world knows how to pile on complexity faster than we can show on the page!
現実の世界のビジネスは、私たちがページ上で紹介するよりも早く、複雑さを積み重ねる方法を知っているのです。

But taking this simple domain model as a placeholder for something more complex, we’re going to extend our simple domain model in the rest of the book and plug it into the real world of APIs and databases and spreadsheets.
しかし、この単純なドメインモデルを、より複雑なもののためのプレースホルダー(実際の内容を後から挿入する為に、とりあえず仮に確保した場所の事)として、この本の残りの部分で単純なドメインモデルを拡張し、APIやデータベースやスプレッドシートの現実の世界に差し込んでいきます。
We’ll see how sticking rigidly to our principles of encapsulation and careful layering will help us to avoid a ball of mud.
カプセル化と慎重なレイヤリングの原則を厳格に守ることが、 泥の玉を避けるためにどのように役立つか、私たちは知ることになるでしょう。

---

MORE TYPES FOR MORE TYPE HINTS
より多くのタイプのヒントを得るために

- If you really want to go to town with type hints, you could go so far as wrapping primitive types by using `typing.NewType`: もし、本当に型ヒントを使いたいのであれば、`typing.NewType`を使ってプリミティブな型をラッピングすることまでできます。

Just taking it way too far, Bob
やりすぎだよ ボブ

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

That would allow our type checker to make sure that we don’t pass a `Sku` where a `Reference` is expected, for example.
これにより、例えば `Reference` が期待されるところに `Sku` を渡さないように、型チェッカが確認することができます。

Whether you think this is wonderful or appalling is a matter of debate.4
これをすばらしいと思うか、ひどいと思うかは議論の分かれるところです4。

---

### Dataclasses Are Great for Value Objects データクラスはバリューオブジェクトに最適です。

We’ve used `line` liberally in the previous code listings, but what is a line?
これまでのコード一覧では、`line`を自由に使ってきましたが、lineとは何でしょうか？
In our business language, an order has multiple line items, where each line has a SKU and a quantity.
私たちのビジネス言語では、注文は複数の行アイテムを持ち、それぞれの行は SKU と数量を持っています。
We can imagine that a simple YAML file containing order information might look like this:
注文情報を含むシンプルな YAML ファイルは次のようになると想像できます。

Order info as YAML
注文情報（YAML

```yaml
Order_reference: 12345
Lines:
  - sku: RED-CHAIR
    qty: 25
  - sku: BLU-CHAIR
    qty: 25
  - sku: GRN-CHAIR
    qty: 25
```

Notice that while an order has a reference that uniquely identifies it, a line does not.
注文はそれを一意に識別する参照を持っていますが、行は持っていないことに注意してください。
(Even if we add the order reference to the `OrderLine` class, it’s not something that uniquely identifies the line itself.)
(注文の参照を `OrderLine` クラスに追加したとしても、行そのものを一意に識別するものではありません)。

Whenever we have a business concept that has data but no identity, we often choose to represent it using the Value Object pattern.
データを持ちながらIDを持たないビジネスコンセプトがある場合、私たちはしばしばValue Objectパターンを使ってそれを表現することを選択します。
A value object is any domain object that is uniquely identified by the data it holds; we usually make them immutable:
バリューオブジェクトとは、それが保持するデータによって一意に識別されるドメインオブジェクトのことで、通常、イミュータブル（不変）なオブジェクトにします。

OrderLine is a value object
OrderLine はバリューオブジェクト

```python
@dataclass(frozen=True)
class OrderLine:
    orderid: OrderReference
    sku: ProductReference
    qty: Quantity

```

One of the nice things that dataclasses (or namedtuples) give us is value equality, which is the fancy way of saying, “Two lines with the same `orderid`, `sku`, and `qty` are equal.”
データクラス(または`namedtuples`)が与えてくれる素晴らしいものの1つに、値の等価性があります。これは、「同じ `orderid`, `sku`, `qty` を持つ2つの行は等しい」という空想的な言い方です。

More examples of value objects
バリューオブジェクトのその他の例

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

These value objects match our real-world intuition about how their values work.
これらのバリューオブジェクトは、その価値の仕組みについて私たちの現実世界での直感と一致しています。
It doesn’t matter which £10 note we’re talking about, because they all have the same value.
どの10ポンド札について話していても、すべて同じ値を持つので問題ありません。
Likewise, two names are equal if both the first and last names match; and two lines are equivalent if they have the same customer order, product code, and quantity.
同様に、2つの名前は姓と名の両方が一致すれば等しいし、2つの行は顧客オーダー、商品コード、数量が同じなら等価である。
We can still have complex behavior on a value object, though.
しかし、値オブジェクトに対して複雑な振る舞いをさせることもできる。
In fact, it’s common to support operations on values; for example, mathematical operators:
実際、値に対する演算をサポートすることはよくあることで、例えば、数学演算子などがある。

Math with value objects
バリューオブジェクトを使った数学

```python
fiver = Money('gbp', 5)
tenner = Money('gbp', 10)

def can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner

def can_subtract_money_values():
    assert tenner - fiver == fiver

def adding_different_currencies_fails():
    with pytest.raises(ValueError):
        Money('usd', 10) + Money('gbp', 10)

def can_multiply_money_by_a_number():
    assert fiver * 5 == Money('gbp', 25)

def multiplying_two_money_values_is_an_error():
    with pytest.raises(TypeError):
        tenner * fiver
```

### Value Objects and Entities バリューオブジェクトとエンティティ

An order line is uniquely identified by its order ID, SKU, and quantity; if we change one of those values, we now have a new line.
オーダーラインは、オーダーID、SKU、数量によって一意に識別され、これらの値のいずれかを変更すると、新しいラインが作成されます。
That’s the definition of a value object: any object that is identified only by its data and doesn’t have a long-lived identity.
これがバリューオブジェクトの定義です。データのみで識別され、長期間の同一性を持たないオブジェクトのことです。
What about a batch, though?
しかし、バッチはどうでしょうか？
That is identified by a reference.
これは参照によって識別されます。

We use the term entity to describe a domain object that has long-lived identity.
ここでは、長期間の同一性を持つドメインオブジェクトを表すために、エンティティという言葉を使います。
On the previous page, we introduced a `Name` class as a value object.
前のページで、値オブジェクトとして `Name` クラスを紹介しました。
If we take the name Harry Percival and change one letter, we have the new `Name` object Barry Percival.
Harry Percival という名前を一文字変えてみると、Barry Percival という新しい `Name` オブジェクトが得られます。

It should be clear that Harry Percival is not equal to Barry Percival:
ハリー・パーシバルとバリー・パーシバルがイコールでないことは明らかでしょう。

A name itself cannot change…
名前そのものは変えられない...。

```python
def test_name_equality():
    assert Name("Harry", "Percival") != Name("Barry", "Percival")
```

But what about Harry as a person?
でも、ハリーという人間はどうでしょう。
People do change their names, and their marital status, and even their gender, but we continue to recognize them as the same individual.
人は名前を変え、配偶者の有無や性別さえも変えますが、私たちはその人を同じ個人として認識し続けています。
That’s because humans, unlike names, have a persistent identity:
それは、人間は名前と違って、永続的なアイデンティティを持っているからです。

But a person can!
でも、人はできる!

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

Entities, unlike values, have identity equality.
実体は価値と異なり、同一性の平等性を持っている。
We can change their values, and they are still recognizably the same thing.
値を変えても、同じものだと認識できる。
Batches, in our example, are entities.
この例では、バッチはエンティティです。
We can allocate lines to a batch, or change the date that we expect it to arrive, and it will still be the same entity.
バッチに行を割り当てても、到着予定日を変えても、同じエンティティであることに変わりはない。

We usually make this explicit in code by implementing equality operators on entities:
通常は、エンティティに等号演算子を実装することで、これをコードで明示する。

Implementing equality operators (model.py)
等号演算子の実装(model.py)

```python
class Batch:
    ...

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)
```

Python’s `__eq__` magic method defines the behavior of the class for the `==` operator.5
Python の `__eq__` マジックメソッドは `==` 演算子に対するクラスの振る舞いを定義しています5。

For both entity and value objects, it’s also worth thinking through how `__hash__` will work.
エンティティオブジェクトとバリューオブジェクトの両方について、 `__hash__` がどのように動作するかを考えておくことも重要です。
It’s the magic method Python uses to control the behavior of objects when you add them to sets or use them as dict keys; you can find more info in the Python docs.
これは Python がオブジェクトをセットに追加したり、dict のキーとして使用したりする際に、オブジェクトの振る舞いを制御するために使用する魔法のメソッドです; Python ドキュメントに詳細が記載されています。

For value objects, the hash should be based on all the value attributes, and we should ensure that the objects are immutable.
値オブジェクトの場合、ハッシュはすべての値属性に基づくべきで、オブジェクトが不変であることを保証する必要があります。
We get this for free by specifying `@frozen=True` on the dataclass.
データクラスに `@frozen=True` を指定することで、これを無料で手に入れることができます。

For entities, the simplest option is to say that the hash is `None`, meaning that the object is not hashable and cannot, for example, be used in a set.
エンティティの場合、最もシンプルなオプションはハッシュが `None` であることです。これは、そのオブジェクトがハッシュ可能ではなく、例えばセットの中で使用できないことを意味します。
If for some reason you decide you really do want to use set or dict operations with entities, the hash should be based on the attribute(s), such as `.reference`, that defines the entity’s unique identity over time.
何らかの理由で、エンティティに対してセットやディクショナリーを使用したい場合、ハッシュは `.reference` のような属性に基づく必要があります。
You should also try to somehow make that attribute read-only.
また、その属性は読み取り専用にするようにしましょう。

- WARNING 警告

- This is tricky territory; you shouldn’t modify `__hash__` without also modifying `__eq__`. If you’re not sure what you’re doing, further reading is suggested. “Python Hashes and Equality” by our tech reviewer Hynek Schlawack is a good place to start. これは厄介な領域で、 `__eq__` を変更せずに `__hash__` を変更することはできません。 もし、自分が何をしているのかわからない場合は、さらに詳しい情報を読むことをお勧めします。 私たちの技術レビュアーである Hynek Schlawack による "Python Has and Equality" が良い手始めです。

## Not Everything Has to Be an Object: A Domain Service Function 何でもかんでもオブジェクトにすればいいってもんじゃない。 ドメインサービス機能

We’ve made a model to represent batches, but what we actually need to do is allocate order lines against a specific set of batches that represent all our stock.
バッチを表すモデルを作りましたが、実際に必要なのは、全在庫を表す特定のバッチの集合に対して、注文行を割り当てることです。

> Sometimes, it just isn’t a thing.
> 時には、ただモノでないこともある。
> Eric Evans, Domain-Driven Design
> エリック・エバンス、ドメイン駆動型設計

Evans discusses the idea of Domain Service operations that don’t have a natural home in an entity or value object.6 A thing that allocates an order line, given a set of batches, sounds a lot like a function, and we can take advantage of the fact that Python is a multiparadigm language and just make it a function.
Evansは、エンティティやバリューオブジェクトの中に自然な住処を持たないドメインサービス操作のアイデアを論じている。6 バッチのセットが与えられたときに注文ラインを割り当てるものは、関数とよく似ており、Pythonがマルチパラダイム言語であることを利用して、それを関数にすればよいのである。

Let’s see how we might test-drive such a function:
では、このような機能をどのように試せばよいのでしょうか。

Testing our domain service (test_allocate.py)
ドメインサービスのテスト(test_allocate.py)

```python
def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow) # 出荷中
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None)
    shipment_batch = Batch("shipment-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow)
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference
```

And our service might look like this:
そして、私たちのサービスはこんな感じかもしれません。

A standalone function for our domain service (model.py)
ドメインサービスのスタンドアロン関数(model.py)

```python
def allocate(line: OrderLine, batches: List[Batch]) -> str:
    batch = next(
        b for b in sorted(batches) if b.can_allocate(line)
    )
    batch.allocate(line)
    return batch.reference
```

### Python’s Magic Methods Let Us Use Our Models with Idiomatic Python Pythonのマジックメソッドでモデルを自在に操る

You may or may not like the use of `next()` in the preceding code, but we’re pretty sure you’ll agree that being able to use `sorted()` on our list of batches is nice, idiomatic Python.
前のコードで `next()` を使うのが好きかどうかは別として、バッチのリストで `sorted()` を使えるのは素敵でイディオムな Python であることには同意していただけると思います。

To make it work, we implement `__gt__` on our domain model:
これを実現するために、ドメインモデル上に `__gt__` を実装する。

Magic methods can express domain semantics (model.py)
マジックメソッドでドメインセマンティクスを表現できる(model.py)

```python
class Batch:
    ...

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta
```

That’s lovely.
それは素敵ですね。

### Exceptions Can Express Domain Concepts Too 例外はドメインの概念も表現できる

We have one final concept to cover: exceptions can be used to express domain concepts too.
最後にもう一つ、例外はドメインの概念を表現するために使うことができます。
In our conversations with domain experts, we’ve learned about the possibility that an order cannot be allocated because we are out of stock, and we can capture that by using a domain exception:
ドメインエキスパートとの会話で、在庫切れで注文が割り当てられない可能性があることを知りましたが、ドメイン例外を使うことでそれを捉えることができます。

Testing out-of-stock exception (test_allocate.py)
在庫切れ例外のテスト(test_allocate.py)

```python
def test_raises_out_of_stock_exception_if_cannot_allocate():
    """在庫切れ(out-of-stock)例外のテスト"""
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today)
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    with pytest.raises(OutOfStock, match='SMALL-FORK'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])
```

- DOMAIN MODELING RECAP ドメインモデリング再録

- Domain modeling ドメイン・モデリング

- This is the part of your code that is closest to the business, the most likely to change, and the place where you deliver the most value to the business. Make it easy to understand and modify. これは、あなたのコードの中で、ビジネスに最も近く、最も変更されやすい部分であり、あなたがビジネスに最も価値を提供する場所です。 理解しやすく、変更しやすいコードにする。

- Distinguish entities from value objects エンティティとバリューオブジェクトを区別する

- A value object is defined by its attributes. It’s usually best implemented as an immutable type. If you change an attribute on a Value Object, it represents a different object. In contrast, an entity has attributes that may vary over time and it will still be the same entity. It’s important to define what does uniquely identify an entity (usually some sort of name or reference field). 値オブジェクトは、その属性によって定義されます。 通常、immutable型として実装するのが最適です。 バリューオブジェクトの属性を変更すると、それは別のオブジェクトを表します。 これに対して、エンティティは、時間とともに変化する属性を持ちますが、それでも同じエンティティであることに変わりはありません。 エンティティを一意に識別するもの（通常、何らかの名前または参照フィールド）を定義することが重要です。

- Not everything has to be an object すべてがオブジェクトである必要はない

- Python is a multiparadigm language, so let the “verbs” in your code be functions. For every `FooManager`, `BarBuilder`, or `BazFactory`, there’s often a more expressive and readable `manage_foo()`, `build_bar()`, or `get_baz()` waiting to happen. Python はマルチパラダイム言語なので、コードの中の「動詞」は関数にしましょう。 すべての `FooManager` や `BarBuilder` 、 `BazFactory` に対して、より表現力豊かで読みやすい `manage_foo()` や `build_bar()` 、 `get_baz()` が待っていることが多いのです。

- This is the time to apply your best OO design principles 今こそ、最高のOO設計の原則を適用する時です

- Revisit the SOLID principles and all the other good heuristics like “has a versus is-a,” “prefer composition over inheritance,” and so on. SOLIDの原則や、「has a対is-a」「継承より合成を優先する」などの優れたヒューリスティックを再確認してください。

- You’ll also want to think about consistency boundaries and aggregates 一貫性の境界と集約についても考えたいところです

- But that’s a topic for Chapter 7. しかし、それは第7章のテーマです。

We won’t bore you too much with the implementation, but the main thing to note is that we take care in naming our exceptions in the ubiquitous language, just as we do our entities, value objects, and services:
実装についてはあまり説明しませんが、主な注意点は、ユビキタス言語では、エンティティ、バリューオブジェクト、サービスと同様に、例外の命名に気をつけるということです。

Raising a domain exception (model.py)
ドメイン例外を発生させる(model.py)

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

Figure 1-4 is a visual representation of where we’ve ended up.
図1-4は、その行き着いた先をビジュアルに表したものです。

![Figure 1-4. Our domain model at the end of the chapter](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0104.png)

That’ll probably do for now!
今のところ、これで大丈夫でしょう
We have a domain service that we can use for our first use case.
最初のユースケースに使用できるドメインサービスがあります。
But first we’ll need a database…
しかし、まずデータベースが必要です...

1. DDD did not originate domain modeling. Eric Evans refers to the 2002 book Object Design by Rebecca Wirfs-Brock and Alan McKean (Addison-Wesley Professional), which introduced responsibility-driven design, of which DDD is a special case dealing with the domain. But even that is too late, and OO enthusiasts will tell you to look further back to Ivar Jacobson and Grady Booch; the term has been around since the mid-1980s. DDDはドメインモデリングを起源とするものではありません。 Eric Evansは、Rebecca Wirfs-BrockとAlan McKeanによる2002年の本「Object Design」（Addison-Wesley Professional）を参照し、責任駆動型設計を紹介しているが、その中でDDDはドメインを扱う特殊なケースであると述べている。 しかし、それさえも遅すぎる。OOの愛好家は、Ivar JacobsonとGrady Boochのさらに昔を調べろと言うだろう。この言葉は1980年代半ばからあったのだ。

2. In previous Python versions, we might have used a namedtuple. You could also check out Hynek Schlawack’s excellent attrs. 以前のPythonのバージョンでは、namedtupleを使ったかもしれません。 Hynek Schlawackの素晴らしいattrsをチェックすることもできます。

3. Or perhaps you think there’s not enough code? What about some sort of check that the SKU in the `OrderLine` matches `Batch.sku`? We saved some thoughts on validation for Appendix E. それとも、コードが足りないと思っているのでしょうか？ OrderLine`の SKU が`Batch.sku` と一致するかどうかをチェックするのはどうでしょうか？ 検証に関するいくつかの考えは、付録Eに保存しました。

4. It is appalling. Please, please don’t do this. —Harry 呆れるほどです。 お願いだから、こんなことしないで。 -ハリー

5. The `__eq__` method is pronounced “dunder-EQ.” By some, at least. eq\_\_`メソッドは、"ダンダーイーク "と発音します。 少なくとも一部の人には。

6. Domain services are not the same thing as the services from the service layer, although they are often closely related. A domain service represents a business concept or process, whereas a service-layer service represents a use case for your application. Often the service layer will call a domain service. ドメインサービスとサービスレイヤーのサービスは、しばしば密接に関連しますが、同じものではありません。 ドメインサービスはビジネスのコンセプトやプロセスを表しますが、 サービスレイヤーのサービスはアプリケーションのユースケースを表します。 多くの場合、サービスレイヤーはドメインサービスを呼び出します。
