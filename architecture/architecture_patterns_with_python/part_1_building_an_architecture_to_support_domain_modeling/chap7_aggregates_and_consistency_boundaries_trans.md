# 1. Chapter 7. Aggregates and Consistency Boundaries 第7章 集計と整合性バウンダリー

In this chapter, we’d like to revisit our domain model to talk about invariants and constraints, and see how our domain objects can maintain their own internal consistency, both conceptually and in persistent storage.
この章では、Domain Model を再検討し、**invariants(不変量?)**と**constraints(制約?)**について説明する. また、 **Domain Object が、概念的にも永続記憶域においても、どのように内部の一貫性を維持できるか**を見ていく.
We’ll discuss the concept of a consistency boundary and show how making it explicit can help us to build high-performance software without compromising maintainability.
**consistency boundary(一貫性境界?)**の概念について説明し、それを明示することで、保守性を損なわずに高性能なソフトウェアを構築するのに役立つことを紹介する.

Figure 7-1 shows a preview of where we’re headed: we’ll introduce a new model object called `Product` to wrap multiple batches, and we’ll make the old `allocate()` domain service available as a method on `Product` instead.
図 7-1 は、私たちが向かう先のプレビューである. 複数のバッチをラップするために `Product` という新しいModel Object を導入し、代わりに `Product` のメソッドとして古い `allocate()` Domain Service を利用できるようにする.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0701.png)

Why?
なぜなのか？
Let’s find out.
それを確かめよう.

TIP
ヒント

The code for this chapter is in the appendix_csvs branch on GitHub:
この章のコードは、GitHubのappendix_csvsブランチにある.

```
git clone https://github.com/cosmicpython/code.git
cd code
git checkout appendix_csvs
# or to code along, checkout the previous chapter:
git checkout chapter_06_uow
```

## 1.1. Why Not Just Run Everything in a Spreadsheet? なぜすべてをスプレッドシートで実行しないのか？

What’s the point of a domain model, anyway?
そもそもドメインモデルってなんだろう？
What’s the fundamental problem we’re trying to address?
根本的な問題は何なのか？

Couldn’t we just run everything in a spreadsheet?
すべてを表計算ソフトで実行できないか？
Many of our users would be delighted by that.
そうすれば、多くのユーザーが喜ぶだろう.
Business users like spreadsheets because they’re simple, familiar, and yet enormously powerful.
ビジネスユーザーがスプレッドシートを好むのは、シンプルで親しみやすく、それでいて非常に強力だからである.

In fact, an enormous number of business processes do operate by manually sending spreadsheets back and forth over email.
実際、膨大な数のビジネスプロセスが、電子メールでスプレッドシートを手動でやり取りすることで運用されている.
This “CSV over SMTP” architecture has low initial complexity but tends not to scale very well because it’s difficult to apply logic and maintain consistency.
この「**CSV over SMTP**」アーキテクチャは、初期の複雑性は低いものの、ロジックの適用と一貫性の維持が困難なため、あまり拡張できない傾向にある.

Who is allowed to view this particular field?
この特定のフィールドを閲覧できるのは誰か？
Who’s allowed to update it?
誰が更新できるのか？
What happens when we try to order –350 chairs, or 10,000,000 tables?
350脚の椅子、または10,000,000台のテーブルを注文しようとすると、どうなりますか?
Can an employee have a negative salary?
従業員の給与がマイナスになることはありますか?

These are the constraints of a system.
これがシステムの**constraint(制約)**である.
Much of the domain logic we write exists to enforce these constraints in order to maintain the invariants of the system.
私たちが書くドメインロジックの多くは、**システムのinvariant(不変量)を維持するために、これらのconstraint(制約)を強制するために**存在する.
The invariants are the things that have to be true whenever we finish an operation.
**invariant(不変量)とは、ある操作を終えたときに必ず真でなければならないもの**(ex. 在庫の数が正になっているなど?).

## 1.2. Invariants, Constraints, and Consistency 不変量、制約、一貫性

The two words are somewhat interchangeable, but a constraint is a rule that restricts the possible states our model can get into, while an invariant is defined a little more precisely as a condition that is always true.
Constraintとは、**モデルが取り得る状態を制限するルール**のことで、Invariantとは、もう少し正確に言うと、**常に真である条件のこと**で、この2つの単語は、多少入れ替えて考えることができる.(i.e. 同じような意味って事...?)

If we were writing a hotel-booking system, we might have the constraint that double bookings are not allowed.
ホテルの予約システムを書くとしたら、**ダブルブッキングは許されないというConstraint**を設けるかもしれない.
This supports the invariant that a room cannot have more than one booking for the same night.
これは、**1つの部屋には同じ晩に2つ以上の予約を持つ事ができないというInvariant**をサポートするものである.

Of course, sometimes we might need to temporarily bend the rules.
もちろん、時には一時的にルールを曲げる必要があるかもしれない.
Perhaps we need to shuffle the rooms around because of a VIP booking.
例えば、VIPの予約のために部屋を移動させる必要があるかもしれない.
While we’re moving bookings around in memory, we might be double booked, but our domain model should ensure that, when we’re finished, we end up in a final consistent state, where the invariants are met.
メモリ内で予約を移動している間に、ダブルブッキングが発生するかもしれない. しかし、**Domain Model は、終了したときに、最終的に一貫した状態になり、Invariant が満たされることを保証する必要がある**.
If we can’t find a way to accommodate all our guests, we should raise an error and refuse to complete the operation.
もし、すべてのゲストを収容する方法が見つからない場合は、エラーを発生させ、**操作の完了を拒否**する必要がある.
cdd
Let’s look at a couple of concrete examples from our business requirements; we’ll start with this one:
ビジネス要件から具体的な例をいくつか見てみよう. まずはこの例から.

> An order line can be allocated to only one batch at a time.
> オーダーラインは、一度に1つのバッチにしか割り当てられない.
> The business
> ビジネス

This is a business rule that imposes an invariant.
これは、Invariantを課すビジネスルールである.
The invariant is that an order line is allocated to either zero or one batch, but never more than one.
このInvariantは、一つのOrderLineはゼロまたは一つのバッチに割り当てられるが、二つ以上には割り当てられないというものである.
We need to make sure that our code never accidentally calls `Batch.allocate()` on two different batches for the same line, and currently, there’s nothing there to explicitly stop us from doing that.
コードが誤って同じLineの2つの異なるバッチで `Batch.allocate()` を呼び出さないようにする必要があるが、現在のところ、それを明示的に阻止するものは何もない.

### 1.2.1. Invariants, Concurrency, and Locks 不変量、並行処理、ロック

Let’s look at another one of our business rules:
もう一つのビジネスルールを見てみましょう。

> We can’t allocate to a batch if the available quantity is less than the quantity of the order line.
> オーダーラインの数量よりも利用可能数量が少ない場合、バッチに割り当てることができない.
> The business
> ビジネス

Here the constraint is that we can’t allocate more stock than is available to a batch, so we never oversell stock by allocating two customers to the same physical cushion, for example.
ここでは、バッチに利用可能な量以上の在庫を割り当てられないというConstraintがある. したがって、たとえば、2人の顧客を同じ物理クッションに割り当てて在庫を過剰に販売することはない.
Every time we update the state of the system, our code needs to ensure that we don’t break the invariant, which is that the available quantity must be greater than or equal to zero.
システムの状態を更新するたびに、**利用可能な数量がゼロ以上でなければならないというInvariant**を破らないように、コードが保証される必要があります。

In a single-threaded, single-user application, it’s relatively easy for us to maintain this invariant.
シングルスレッド(=窓口が一つ, みたいな?)、シングルユーザーのアプリケーションでは、この不変性を維持するのは比較的簡単である.
We can just allocate stock one line at a time, and raise an error if there’s no stock available.
一度に一行ずつストックを確保し、ストックがない場合はエラーを出せばよい.

This gets much harder when we introduce the idea of concurrency.
しかし、**同時並行処理という考え方を導入すると、これが非常に難しくなる**.
Suddenly we might be allocating stock for multiple order lines simultaneously.
突然、複数の OrderLine に対して同時に在庫を割り当てることになるかもしれない.
We might even be allocating order lines at the same time as processing changes to the batches themselves.
さらに、バッチ自体の変更処理と同時に、オーダーラインを割り当てることもあるかもしれない.

We usually solve this problem by applying locks to our database tables.
この問題は、通常、**データベースのテーブルにロックをかけること**で解決する.
This prevents two operations from happening simultaneously on the same row or same table.
これにより、同じ行や同じテーブルに対して同時に2つの操作が行われるのを防ぐことができる.

As we start to think about scaling up our app, we realize that our model of allocating lines against all available `batches` may not scale.
アプリのスケールアップを考え始めたとき、利用可能なすべての `バッチ` に対して行を割り当てるというモデルはスケールしないかもしれないことに気づいた. (??)
If we process tens of thousands of orders per hour, and hundreds of thousands of order lines, we can’t hold a lock over the whole batches table for every single one—we’ll get deadlocks or performance problems at the very least.
1時間に何万件ものOrderを処理し、何十万件ものOrderLineを処理する場合、すべてのOrderLineに対してBatchsテーブル全体をロックすることはできないし、少なくともデッドロックやパフォーマンスの問題が発生するだろう.

## 1.3. What Is an Aggregate? 集計って何？

OK, so if we can’t lock the whole database every time we want to allocate an order line, what should we do instead?
では、**OrderLineを割り当てるたびにデータベース全体をロックすることができないのであれば、代わりに何をすべき**なのだろうか?
We want to protect the invariants of our system but allow for the greatest degree of concurrency.
私たちは、**システムのInvariantを守りつつ、最大限の並行処理を可能にしたい**.
Maintaining our invariants inevitably means preventing concurrent writes; if multiple users can allocate `DEADLY-SPOON` at the same time, we run the risk of overallocating.
もし複数のユーザーが `DEADLY-SPOON` を同時に割り当てることができるならば、Over allocation の危険性がある.

On the other hand, there’s no reason we can’t allocate `DEADLY-SPOON` at the same time as `FLIMSY-DESK`.
一方、`DEADLY-SPOON` を `FLIMSY-DESK` と同時に割り当てることができない理由はない.
It’s safe to allocate two products at the same time because there’s no invariant that covers them both.
**2つの製品を同時に割り当てることが安全なのは、その両方をカバーするInvariantが存在しないから**である.
We don’t need them to be consistent with each other.
2つの製品が互いに矛盾しないようにする必要はない.

The Aggregate pattern is a design pattern from the DDD community that helps us to resolve this tension.
**Aggregate Pattern** は、この緊張を解消するのに役立つDDDコミュニティの design pattern である.
An aggregate is just a domain object that contains other domain objects and lets us treat the whole collection as a single unit.
**Aggregateは、他のDomain Object を含む単なる Domain Object**であり、コレクション全体を単一のユニットとして扱うことができる.

The only way to modify the objects inside the aggregate is to load the whole thing, and to call methods on the aggregate itself.
Aggregate内のオブジェクトを変更する唯一の方法は、全体をロードし、Aggregate自体のメソッドを呼び出すことである.

As a model gets more complex and grows more entity and value objects, referencing each other in a tangled graph, it can be hard to keep track of who can modify what.
**Model(=Domain Model)がより複雑になり、より多くの Entity や Value Object が増え、絡み合ったグラフでお互いを参照するようになると、誰が何を変更できるかを追跡することが難しくなる**.
Especially when we have collections in the model as we do (our batches are a collection), it’s a good idea to nominate some entities to be the single entrypoint for modifying their related objects.
特に、私たちのように**モデル内にcollection(??)を持つ場合**（私たちのバッチはcollectionらしい...）、いくつかのEntityを、**関連するオブジェクトを修正するための単一のエントリポイントとして指名する**のは良いアイデアである.
It makes the system conceptually simpler and easy to reason about if you nominate some objects to be in charge of consistency for the others.
いくつかのオブジェクトを他のオブジェクトの一貫性を担当するように指名すると、システムが概念的に単純になり、推論が容易になる.

For example, if we’re building a shopping site, the Cart might make a good aggregate: it’s a collection of items that we can treat as a single unit.
例えば、ショッピングサイトを構築する場合、Cartは良いAggregateになるかもしれない.
Importantly, we want to load the entire basket as a single blob from our data store.
重要なのは、データストアからバスケット(=Cart)全体を単一のブロブとしてロードすることである.
We don’t want two requests to modify the basket at the same time, or we run the risk of weird concurrency errors.
2つのリクエストで同時にバスケットを変更すると、並行処理エラーが発生する危険性がある.
Instead, we want each change to the basket to run in a single database transaction.
その代わり、バスケットへの各変更は単一のデータベーストランザクションで実行されるようにする.

We don’t want to modify multiple baskets in a transaction, because there’s no use case for changing the baskets of several customers at the same time.
複数の顧客のバスケットを同時に変更するユースケースがないため、1つのトランザクションで複数のバスケットを変更することを望んでいない.
Each basket is a single consistency boundary responsible for maintaining its own invariants.
各バスケットは、それ自身のInvariantを維持する責任を負う単一のconsistency boundaryです。

> An AGGREGATE is a cluster of associated objects that we treat as a unit for the purpose of data changes.
> AGGREGATEは関連するオブジェクトのクラスタ(集合)であり、**データ変更の目的のために1つの単位として扱う**.
> Eric Evans, Domain-Driven Design blue book
> エリック・エバンス著「ドメイン駆動設計の青本

Per Evans, our aggregate has a root entity (the Cart) that encapsulates access to items.
Evansによると、我々のAggregateは**アイテム(より細かい単位のDomain Object)へのアクセスをカプセル化するRoot Entity（Cart）**を持っている.
Each item has its own identity, but other parts of the system will always refer to the Cart only as an indivisible whole.
各アイテムはそれ自身のアイデンティティを持つが、システムの他の部分は常に不可分な全体としてのみCartを参照する.

- TIP ヒント
- Just as we sometimes use `_leading_underscores` to mark methods or functions as “private,” you can think of aggregates as being the “public” classes of our model, and the rest of the entities and value objects as “private.” メソッドや関数を "private" とマークするために `_leading_underscores` を使うことがあるように、**Aggregateはモデルの "public" クラスであり、残りの Entity や Value Object は "private" である**と考えることができる.

## 1.4. Choosing an Aggregate 集計の選択

What aggregate should we use for our system?
私たちのシステムには、**どのようなAggregateを用いるべきでだろうか**?
The choice is somewhat arbitrary, but it’s important.
この選択は多少任意ですが、重要である.
The aggregate will be the boundary where we make sure every operation ends in a consistent state.
**Aggregate は、すべての操作が一貫した状態(consistent state)で終了することを確認する境界線になりなる**.
This helps us to reason about our software and prevent weird race issues.
これは、私たちのソフトウェアについて推論し、奇妙なレース問題(??)を防ぐのに役立つ.
We want to draw a boundary around a small number of objects—the smaller, the better, for performance—that have to be consistent with one another, and we need to give this boundary a good name.
私たちは、少数のオブジェクトの周りに境界線を引きたいと考えている. 小さいほどパフォーマンスのために良いのですが、それらは互いに一貫している必要があり、この境界線に良い名前を付ける必要がある.

The object we’re manipulating under the covers is `Batch`.
私たちが隠れて操作しているオブジェクトは `Batch` である.
What do we call a collection of batches?
Batchの集合体をどう呼ぶか？
How should we divide all the batches in the system into discrete islands of consistency?
システム内のすべてのバッチを、一貫性のある離島にどのように分割すればいいのだろうか...?

We could use `Shipment` as our boundary.
境界線として `Shipment`(出荷) を使用することができる.
Each shipment contains several batches, and they all travel to our warehouse at the same time.
各ShipmentはいくつかのBatchを含んでおり、それらはすべて同時に倉庫に移動する.
Or perhaps we could use `Warehouse` as our boundary: each warehouse contains many batches, and counting all the stock at the same time could make sense.
あるいは、`Warehouse`(倉庫)を境界として使うこともできる. 各Warehouseには多くのBatchがあり、同時にすべての在庫を数えることは理にかなっている.

Neither of these concepts really satisfies us, though.
しかし、どちらのコンセプトも私たちを満足させるものではない.
We should be able to allocate `DEADLY-SPOONs` and `FLIMSY-DESKs` at the same time, even if they’re in the same warehouse or the same shipment.
たとえ同じWarehouseや同じShipmentにあったとしても、`DEADLY-SPOON`と`FLIMSY-DESK`を同時に割り当てることができるはず.
These concepts have the wrong granularity.
これらの概念は粒度が間違っているのである.

When we allocate an order line, we’re interested only in batches that have the same SKU as the order line.
OrderLineを割り当てるとき、そのOrderLineと同じSKUを持つバッチにのみ興味がある.
Some sort of concept like `GlobalSkuStock` could work: a collection of all the batches for a given SKU.
`GlobalSkuStock`のようなコンセプトで、**指定されたあるSKUの全てのBatchのcollection**を作成することができる.

It’s an unwieldy name, though, so after some bikeshedding via `SkuStock`, `Stock`, `ProductStock`, and so on, we decided to simply call it `Product`—after all, that was the first concept we came across in our exploration of the domain language back in Chapter 1.
しかし、扱いにくい名前なので、`SkuStock`、`Stock`、`ProductStock`などを経て、単純に`Product`と呼ぶことにしました。結局、これは第1章の **Domain Language の探索**で最初に出会った概念だった.

So the plan is this: when we want to allocate an order line, instead of Figure 7-2, where we look up all the `Batch` objects in the world and pass them to the `allocate()` domain service…
図 7-2 のように、世界中のすべての `Batch` オブジェクトを検索して `allocate()` Domain Service に渡すのではなく、OrderLineを割り当てたいときに...。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0702.png)

…we’ll move to the world of Figure 7-3, in which there is a new Product object for the particular SKU of our order line, and it will be in charge of all the batches for that SKU, and we can call a .allocate() method on that instead.
...図 7-3 の世界に移動して、OrderLineの特定の SKU に対して新しい Product オブジェクトが存在し、その SKU のすべてのバッチを担当することになる.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0703.png)

Let’s see how that looks in code form:
それでは、コード形式で見てみよう.

Our chosen aggregate, Product (src
私たちが選んだAggregate = `Product`（src

```python
class Product:

    def __init__(self, sku: str, batches: List[Batch]):
        self.sku = sku  1
        self.batches = batches  2

    def allocate(self, line: OrderLine) -> str:  3
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_allocate(line)
            )
            batch.allocate(line)
            return batch.reference
        except StopIteration:
            raise OutOfStock(f'Out of stock for sku {line.sku}')
```

1. `Product`’s main identifier is the `sku`. `Product`の主な識別子(=ユニークなインスタンスを識別する情報)は「sku」である.

2. Our `Product` class holds a reference to a collection of `batches` for that SKU. 私たちの `Product` クラスは、その SKU のための `batches` のcollection への参照を保持する.

3. Finally, we can move the `allocate()` domain service to be a method on the `Product` aggregate. 最後に、`allocate()` Domain Service を `Product` 集合体のメソッドに移動させる.

- NOTE 注
- This `Product` might not look like what you’d expect a `Product` model to look like. No price, no description, no dimensions. Our allocation service doesn’t care about any of those things. This is the power of bounded contexts; the concept of a product in one app can be very different from another. See the following sidebar for more discussion. この `Product` は、あなたが期待する `Product` のモデルとは異なるかもしれない. 価格も、説明も、寸法もない. 私たちのallocate サービス(=Domain Service)は、そのようなことは一切気にしない. これが境界のあるコンテキストの力である. あるアプリケーションの製品のコンセプトは、別のアプリケーションとはまったく異なることがある. 詳しくは、次のサイドバーをご覧あれ.

- AGGREGATES, BOUNDED CONTEXTS, AND MICROSERVICES アグリゲート、バウンデッドコンテキスト、マイクロサービス
- One of the most important contributions from Evans and the DDD community is the concept of bounded contexts. EvansとDDDコミュニティの最も重要な貢献の1つは、**bounded context**の概念である.

  - In essence, this was a reaction against attempts to capture entire businesses into a single model. The word customer means different things to people in sales, customer service, logistics, support, and so on. Attributes needed in one context are irrelevant in another; more perniciously, concepts with the same name can have entirely different meanings in different contexts. Rather than trying to build a single model (or class, or database) to capture all the use cases, it’s better to have several models, draw boundaries around each context, and handle the translation between different contexts explicitly. 要するに、ビジネス全体を一つのモデルに取り込もうとする動きに対する反発であった. customerという言葉は、営業、カスタマーサービス、ロジスティクス、サポートなど、さまざまな立場の人にとって異なる意味を持つ. あるcontext(文脈?)で必要とされる属性は、別のcontextでは無関係である. さらに悪質なことに、同じ名前の概念が、異なるcontextではまったく異なる意味を持つこともある. **すべてのユースケースを網羅する単一のモデル（またはクラス、データベース）を構築しようとするよりも、複数のモデルを用意し、それぞれのcontextに境界線を引いて、異なるcontext間の変換を明示的に処理する方が良い**.
  - This concept translates very well to the world of microservices, where each microservice is free to have its own concept of “customer” and its own rules for translating that to and from other microservices it integrates with. このコンセプトは、Micro Service の世界にも非常によく通じる. 各Micro Service は、「customer」という独自のコンセプトと、それを統合する他のMicro Service との間で変換するための独自のルールを自由に持つことができるのである.
  - In our example, the allocation service has `Product(sku, batches)`, whereas the ecommerce will have `Product(sku, description, price, image_url, dimensions, etc...)`. As a rule of thumb, your domain models should include only the data that they need for performing calculations. この例では、allocationサービスは `Product(sku, batches)` を持ち、eコマースでは `Product(sku, description, price, image_url, dimensions, etc...)` を持つことになる. 経験則として、Domain Model には、計算を行うために必要なデータだけを含めるべき.
  - Whether or not you have a microservices architecture, a key consideration in choosing your aggregates is also choosing the bounded context that they will operate in. By restricting the context, you can keep your number of aggregates low and their size manageable. Micro Serviceアーキテクチャを採用しているかどうかにかかわらず、**Aggregateを選択する際に考慮すべき重要な点は、Aggregateが動作する限定されたcontextを選択することでもある**. contextを制限することで、Aggregateの数を少なくし、そのサイズを管理しやすくすることができる.
  - Once again, we find ourselves forced to say that we can’t give this issue the treatment it deserves here, and we can only encourage you to read up on it elsewhere. The Fowler link at the start of this sidebar is a good starting point, and either (or indeed, any) DDD book will have a chapter or more on bounded contexts. もう一度言いますが、私たちはこの問題にふさわしい処置をここで施すことができず、他の場所で読むことをお勧めするしかない. このサイドバーの最初にあるFowlerのリンクは良い出発点ですし、DDDの本にはbounded Contextに関する章がいくつかある.

## 1.5. One Aggregate = One Repository (1つの集合体 = 1つのリポジトリ)

Once you define certain entities to be aggregates, we need to apply the rule that they are the only entities that are publicly accessible to the outside world.
**あるEntityをAggregateと定義したら、そのEntityだけが外部に公開される**、というルールを適用する必要がある.
In other words, the only repositories we are allowed should be repositories that return aggregates.
言い換えれば、私たちが許可されるRepositoryは、Aggregateを返すRepositoryだけであるべき.

- NOTE 注
  - The rule that repositories should only return aggregates is the main place where we enforce the convention that aggregates are the only way into our domain model. Be wary of breaking it! リポジトリはAggregate を返すだけでよいというルールは、"**AggregateがDomain Modelへの唯一の道である**"という慣習を強制する主な方法である. これを破らないように注意しよう.

In our case, we’ll switch from `BatchRepository` to `ProductRepository`:
今回は、`BatchRepository`から`ProductRepository`に切り替えてみる.

Our new UoW and repository (unit_of_work.py and repository.py)
新しいUoWとリポジトリ(unit_of_work.pyとrepository.py)

```python
class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractProductRepository

...

class AbstractProductRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, product):
        ...

    @abc.abstractmethod
    def get(self, sku) -> model.Product:
        ...
```

The ORM layer will need some tweaks so that the right batches automatically get loaded and associated with `Product` objects.
ORMレイヤーは、正しいBatchが自動的にロードされ、`Product`オブジェクトと関連付けられるように、いくつかの微調整が必要である.
The nice thing is, the Repository pattern means we don’t have to worry about that yet.
素晴らしいことに、Repository Patternはまだその心配をする必要がないことを意味する.
We can just use our `FakeRepository` and then feed through the new model into our service layer to see how it looks with `Product` as its main entrypoint:
`FakeRepository`を使って、新しいモデルを Service Layer に送り込み、`Product` を主なエントリポイントとしてどのように見えるかを確認することができる.

Service layer (src
サービス層（src

```python
def add_batch(
        ref: str, sku: str, qty: int, eta: Optional[date],
        uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()


def allocate(
        orderid: str, sku: str, qty: int,
        uow: unit_of_work.AbstractUnitOfWork
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f'Invalid sku {line.sku}')
        batchref = product.allocate(line)
        uow.commit()
    return batchref
```

## 1.6. What About Performance? What About Performance?

We’ve mentioned a few times that we’re modeling with aggregates because we want to have high-performance software, but here we are loading all the batches when we only need one.
私たちがAggregateでモデリングしているのは、高性能なソフトウェアを使いたいから(??)だと何度か述べたが、ここでは1つだけ必要なときにすべてのBatchをロードしている.
You might expect that to be inefficient, but there are a few reasons why we’re comfortable here.
これは非効率的だと思われるかもしれないが、ここが快適なのにはいくつかの理由がある.

First, we’re purposefully modeling our data so that we can make a single query to the database to read, and a single update to persist our changes.
まず、**意図的にデータをモデル化しているので、データベースへの問い合わせは1回で済むし、更新も1回で済み、変更内容を持続させることができる**.
This tends to perform much better than systems that issue lots of ad hoc queries.
これは、その場しのぎのクエリを大量に発行するシステムよりも、はるかに優れたパフォーマンスを発揮する傾向がある.
In systems that don’t model this way, we often find that transactions slowly get longer and more complex as the software evolves.
このようなモデル化をしていないシステムでは、ソフトウェアの進化に伴い、トランザクションが徐々に長く、複雑になっていくことがよくある.

Second, our data structures are minimal and comprise a few strings and integers per row.
第二に、データ構造は最小で、1行あたり数個の文字列と整数で構成されている.
We can easily load tens or even hundreds of batches in a few milliseconds.
数十から数百のBatchを数ミリ秒で簡単にロードすることができる.

Third, we expect to have only 20 or so batches of each product at a time.
第三に、各Productのロット数(=Aggregate内のBatchの数)は一度に20程度を想定している.
Once a batch is used up, we can discount it from our calculations.
1バッチを使い切ったら、計算から除外することができる.
This means that the amount of data we’re fetching shouldn’t get out of control over time.
つまり、**データの取得量が時間とともに制御不能になることはないはず**である.

If we did expect to have thousands of active batches for a product, we’d have a couple of options.
もし、**1つのProductに対して何千ものアクティブなBatchが存在する**ケースでは、いくつかのオプションがある.

For one, we could use lazy-loading for the batches in a product.
ひとつは、商品のBatchに**lazy-loading(?)**を使うことである.
From the perspective of our code, nothing would change, but in the background, SQLAlchemy would page through data for us.
コードの観点からは何も変わりませんが、バックグラウンドでは、SQLAlchemy が私たちのためにデータをpaging(?)してくれる.
This would lead to more requests, each fetching a smaller number of rows.
これは、より多くのリクエストにつながり、それぞれがより少ない数の行を取得することになる.
Because we need to find only a single batch with enough capacity for our order, this might work pretty well.
なぜなら、私たちはOrderLineを割り当てるのに十分な容量を持つ、たった一つのBatchを見つける必要があるからである.

- EXERCISE FOR THE READER 読書運動
- You’ve just seen the main top layers of the code, so this shouldn’t be too hard, but we’d like you to implement the `Product` aggregate starting from `Batch`, just as we did. 今、コードの主要なトップレイヤーを見たので、これはそれほど難しくないはず. しかし、私たちがやったように、`Batch`から始めて`Product` Aggregateを実装してほしいと考えている.
- Of course, you could cheat and copy/paste from the previous listings, but even if you do that, you’ll still have to solve a few challenges on your own, like adding the model to the ORM and making sure all the moving parts can talk to each other, which we hope will be instructive. もちろん、ズルをしてコピーすることも可能.
- You’ll find the code on GitHub. We’ve put in a “cheating” implementation in the delegates to the existing `allocate()` function, so you should be able to evolve that toward the real thing. GitHubにコードがある. 既存の `allocate()` 関数のデリゲートに「ごまかし」の実装を入れたので、それを本番に向けて進化させることができるはず.
- We’ve marked a couple of tests with `@pytest.skip()`. After you’ve read the rest of this chapter, come back to these tests to have a go at implementing version numbers. Bonus points if you can get SQLAlchemy to do them for you by magic! いくつかのテストに `@pytest.skip()` という印をつけた この章の残りを読み終えたら、これらのテストに戻ってバージョン番号を実装してみよう. SQLAlchemy にマジックでバージョン番号を書かせることができれば、ボーナスポイントです!

If all else failed, we’d just look for a different aggregate.
もし失敗したら、別のAggregateを探せばいいだけ!
Maybe we could split up batches by region or by warehouse.
地域別や倉庫別にBatchを分割することもできる.
Maybe we could redesign our data access strategy around the shipment concept.
あるいは、Shipment の概念に基づいて、データアクセス戦略を再設計することもできる.
The Aggregate pattern is designed to help manage some technical constraints around consistency and performance.
**Aggregateパターンは、一貫性とパフォーマンスに関するいくつかの技術的な制約を管理するために設計されている**.
There isn’t one correct aggregate, and we should feel comfortable changing our minds if we find our boundaries are causing performance woes.
**正しいAggregateは一つではない**ので、もし自分の境界線がパフォーマンスの問題を引き起こしていることがわかったら、気軽に考えを変えてみるべき...!

## 1.7. Optimistic Concurrency with Version Numbers バージョン番号による最適化された同時並行処理

We have our new aggregate, so we’ve solved the conceptual problem of choosing an object to be in charge of consistency boundaries.
新しいAggregateができたので、**consistency boundary を担当するオブジェクトを選択する**という概念的な問題は解決された.
Let’s now spend a little time talking about how to enforce data integrity at the database level.
それでは、データベースレベルでデータの整合性を強制する方法について、少し時間をかけて説明しよう.

- NOTE 注
- This section has a lot of implementation details; for example, some of it is Postgres-specific. But more generally, we’re showing one way of managing concurrency issues, but it is just one approach. Real requirements in this area vary a lot from project to project. You shouldn’t expect to be able to copy and paste code from here into production. このセクションには多くの実装の詳細がある. 例えば、Postgresに特有のものもある. しかし、より一般的には、**我々は並行処理の問題を管理する1つの方法を示しているが、それは1つのアプローチに過ぎない**. この分野の実際の要件は、プロジェクトによって大きく異なる. ここからコードをコピーして本番環境に貼り付けられると期待しない方が良いだろう.

We don’t want to hold a lock over the entire `batches` table, but how will we implement holding a lock over just the rows for a particular SKU?
しかし、**特定のSKUの行だけをロックすること**は、どのように実装すればよいのでだろうか?

One answer is to have a single attribute on the `Product` model that acts as a marker for the whole state change being complete and to use it as the single resource that concurrent workers can fight over.
一つの答えは、`Product`モデル上に、**全体の状態変化が完了したことを示すマーカーとして機能する単一の属性を持ち**、それを**同時実行ワーカー**が争うことができる単一のリソースとして使用することである.
If two transactions read the state of the world for `batches` at the same time, and both want to update the `allocations` tables, we force both to also try to update the `version_number` in the `products` table, in such a way that only one of them can win and the world stays consistent.
2つのトランザクションが同時に `batches` の世界の状態を読み取り、どちらも `allocations` テーブルを更新したい場合、どちらか一方だけが勝利して世界の一貫性を保つことができるように、どちらも `products` テーブルの `version_number` も更新しようとするように強制される.

Figure 7-4 illustrates two concurrent transactions doing their read operations at the same time, so they see a `Product` with, for example, `version=3`.
図7-4は、2つのトランザクションが同時に読み取り操作を行い、例えば `version=3` の `Product` を見ている様子を示している.
They both call `Product.allocate()` in order to modify a state.
2人とも状態を変更するために `Product.allocate()` を呼び出している.
But we set up our database integrity rules such that only one of them is allowed to `commit` the new `Product` with `version=4`, and the other update is rejected.
しかし、データベースの整合性ルールを設定して、一方のトランザクションだけが `version=4` の新しい `Product` を `commit` することができ、**他方の更新は拒否される**ようにした.

- TIP ヒント
- Version numbers are just one way to implement optimistic locking. You could achieve the same thing by setting the Postgres transaction isolation level to `SERIALIZABLE`, but that often comes at a severe performance cost. Version numbers also make implicit concepts explicit. **バージョン番号はoptimistic locking(楽観的ロック)を実装するための1つの方法に過ぎない**. Postgresのトランザクション分離レベルを `SERIALIZABLE` に設定すれば同じことを実現できますが、多くの場合、性能に大きな犠牲を払うことになる. バージョン番号はまた、暗黙の概念を明示する...!!(明示化...!良いね!)

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0704.png)

- Optimisitc Concurrency Control and Retries 楽観的並行性制御とリトライ

  - What we’ve implemented here is called optimistic concurrency control because our default assumption is that everything will be fine when two users want to make changes to the database. We think it’s unlikely that they will conflict with each other, so we let them go ahead and just make sure we have a way to notice if there is a problem. ここで実装したのは**Optimisitc Concurrency Control(楽観的同時実行制御?)**と呼ばれるもので、**2人のユーザがデータベースに変更を加えようとするとき、すべてうまくいくだろうというのが私たちのデフォルトの仮定**である. 2人のユーザがお互いに衝突する可能性は低いと考えているので、2人を先に進ませ、問題が発生したときに気づく方法を確保するだけである.
  - Pessimistic concurrency control works under the assumption that two users are going to cause conflicts, and we want to prevent conflicts in all cases, so we lock everything just to be safe. In our example, that would mean locking the whole `batches` table, or using `SELECT FOR UPDATE`—we’re pretending that we’ve ruled those out for performance reasons, but in real life you’d want to do some evaluations and measurements of your own. 一方で**Pessimistic concurrency control(悲観的な同時実行制御)**は、**2人のユーザーが衝突を起こすという前提**で動作する. あらゆる場合に衝突を防ぎたいので、念のためにすべてをロックする. この例では、`batches`テーブル全体をロックしたり、`SELECT FOR UPDATE`を使用することになる. ここでは、パフォーマンス上の理由からこれらを除外したことにしているが、実際のところ、自分自身で評価や測定を行いたいとこだろう.
  - With pessimistic locking, you don’t need to think about handling failures because the database will prevent them for you (although you do need to think about deadlocks). With optimistic locking, you need to explicitly handle the possibility of failures in the (hopefully unlikely) case of a clash. **pessimistic locking**では、データベースが失敗を防いでくれるので、失敗の処理について考える必要はない (デッドロックについては考える必要がありますが). optimistic lockingでは、（できれば起こりそうもないことですが）**衝突した場合の失敗の可能性を明示的に処理する必要**がある.
  - The usual way to handle a failure is to retry the failed operation from the beginning. Imagine we have two customers, Harry and Bob, and each submits an order for `SHINY-TABLE`. Both threads load the product at version 1 and allocate stock. The database prevents the concurrent update, and Bob’s order fails with an error. When we retry the operation, Bob’s order loads the product at version 2 and tries to allocate again. If there is enough stock left, all is well; otherwise, he’ll receive `OutOfStock`. Most operations can be retried this way in the case of a concurrency problem. **失敗を処理する通常の方法は、失敗した操作を最初からやり直すこと**である. ハリーとボブという二人の顧客がいて、それぞれが `SHINY-TABLE` の注文を出したとする. 両方のスレッドが製品をバージョン 1 でロードし、在庫を割り当てる. データベースは同時更新を阻止し、ボブの注文はエラーで失敗する. 操作を再試行すると、ボブさんの注文は商品をバージョン2でロードし、再度割り当てを試みる. 十分な在庫が残っていれば問題ないが、そうでない場合は `OutOfStock` を受け取る. ほとんどの操作は、並行処理の問題が発生した場合にこの方法で再試行することができる.
  - Read more on retries in “Recovering from Errors Synchronously” and “Footguns”. 再試行については、「同期的にエラーから回復する」と「フットガン」で詳しく説明している.

### 1.7.1. Implementation Options for Version Numbers バージョン番号の実装オプション

There are essentially three options for implementing version numbers:
バージョン番号の実装には、基本的に3つの選択肢がある.

1. `version_number` lives in the domain; we add it to the `Product` constructor, and `Product.allocate()` is responsible for incrementing it. バージョン番号 `version_number` はドメイン内に存在する. これを `Product` コンストラクタに追加し、 `Product.allocate()` がこれをインクリメント(+1)する役割を担う.
2. The service layer could do it! The version number isn’t strictly a domain concern, so instead our service layer could assume that the current version number is attached to `Product` by the repository, and the service layer will increment it before it does the `commit()`. Service Layerがそれを行うことができる! バージョン番号は厳密にはDomainの問題ではないので、代わりにService Layerは、現在のバージョン番号がリポジトリによって `Product` にアタッチされており、Service Layerが `commit()` を実行する前にそれをインクリメントすると仮定できる.
3. Since it’s arguably an infrastructure concern, the UoW and repository could do it by magic. The repository has access to version numbers for any products it retrieves, and when the UoW does a commit, it can increment the version number for any products it knows about, assuming them to have changed. **version numberは間違いなくインフラストラクチャの問題**なので、UoWとRepositoryはマジックでそれを行うことができる. Repositoryは取得した製品のバージョン番号にアクセスでき、UoWがコミットするときに、それが知っているすべての製品のバージョン番号を、それらが変更されたと仮定してインクリメントすることができる.

Option 3 isn’t ideal, because there’s no real way of doing it without having to assume that all products have changed, so we’ll be incrementing version numbers when we don’t have to.1
というのも、すべての製品が変更されたと仮定する必要がないため、バージョン番号を増加させる必要があるからである.

Option 2 involves mixing the responsibility for mutating state between the service layer and the domain layer, so it’s a little messy as well.
選択肢2は、Service LayerとDomain Layerの間で状態の変異の責任を混在させることになり、同様に少し面倒.

So in the end, even though version numbers don’t have to be a domain concern, you might decide the cleanest trade-off is to put them in the domain:
ですから、最終的には、**バージョン番号はDomainに関係ないとしても、最もクリーンなトレードオフとして、Domainに入れるべき**だと判断することもある.

Our chosen aggregate, Product (src
私たちが選んだ集合体である製品（src

```python
class Product:

    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):  1
        self.sku = sku
        self.batches = batches
        self.version_number = version_number  1

    def allocate(self, line: OrderLine) -> str:
        try:
            batch = next(
                b for b in sorted(self.batches) if b.can_allocate(line)
            )
            batch.allocate(line)
            self.version_number += 1  1
            return batch.reference
        except StopIteration:
            raise OutOfStock(f'Out of stock for sku {line.sku}')
```

1. There it is! あった！

- TIP ヒント
- If you’re scratching your head at this version number business, it might help to remember that the number isn’t important. What’s important is that the `Product` database row is modified whenever we make a change to the `Product` aggregate. The version number is a simple, human-comprehensible way to model a thing that changes on every write, but it could equally be a random UUID every time. もしあなたがこのバージョン番号ビジネスで頭を悩ませているなら、番号は重要ではないことを思い出すのに役立つかもしれない. 重要なのは、 `Product` データベースの行(row)は、 `Product` 集計に変更を加えるたびに変更されることである. **バージョン番号は、書き込みのたびに変更されるものをモデル化するための、シンプルで人間が理解しやすい方法ですが、毎回ランダムな UUID にすることも可能**である.

## 1.8. Testing for Our Data Integrity Rules データ完全性ルールのテスト

Now to make sure we can get the behavior we want: if we have two concurrent attempts to do allocation against the same `Product`, one of them should fail, because they can’t both update the version number.
もし、同じ `Product` に対して同時に 2 つのアロケーションを行おうとしたら、どちらかが失敗するはずです。なぜなら、両方ともバージョン番号を更新できないからです。

First, let’s simulate a “slow” transaction using a function that does allocation and then does an explicit sleep:2
まず、割り当てを行い、明示的にスリープさせる関数を使って、「遅い」トランザクションをシミュレートしてみましょう2。

time.sleep can reproduce concurrency behavior (tests
time.sleepは並行処理の挙動を再現することができる（テスト

```python
def try_to_allocate(orderid, sku, exceptions):
    line = model.OrderLine(orderid, sku, 10)
    try:
        with unit_of_work.SqlAlchemyUnitOfWork() as uow:
            product = uow.products.get(sku=sku)
            product.allocate(line)
            time.sleep(0.2)
            uow.commit()
    except Exception as e:
        print(traceback.format_exc())
        exceptions.append(e)
```

Then we have our test invoke this slow allocation twice, concurrently, using threads:
そして、テストでは、このスローアロケーションをスレッドを使って2回、同時に呼び出すようにします。

An integration test for concurrency behavior (tests
並行処理動作の統合テスト（テスト

```python
def test_concurrent_updates_to_version_are_not_allowed(postgres_session_factory):
    sku, batch = random_sku(), random_batchref()
    session = postgres_session_factory()
    insert_batch(session, batch, sku, 100, eta=None, product_version=1)
    session.commit()

    order1, order2 = random_orderid(1), random_orderid(2)
    exceptions = []  # type: List[Exception]
    try_to_allocate_order1 = lambda: try_to_allocate(order1, sku, exceptions)
    try_to_allocate_order2 = lambda: try_to_allocate(order2, sku, exceptions)
    thread1 = threading.Thread(target=try_to_allocate_order1)  1
    thread2 = threading.Thread(target=try_to_allocate_order2)  1
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    [[version]] = session.execute(
        "SELECT version_number FROM products WHERE sku=:sku",
        dict(sku=sku),
    )
    assert version == 2  2
    [exception] = exceptions
    assert 'could not serialize access due to concurrent update' in str(exception)  3

    orders = list(session.execute(
        "SELECT orderid FROM allocations"
        " JOIN batches ON allocations.batch_id = batches.id"
        " JOIN order_lines ON allocations.orderline_id = order_lines.id"
        " WHERE order_lines.sku=:sku",
        dict(sku=sku),
    ))
    assert len(orders) == 1  4
    with unit_of_work.SqlAlchemyUnitOfWork() as uow:
        uow.session.execute('select 1')
```

1. We start two threads that will reliably produce the concurrency behavior we want: `read1, read2, write1, write2`. 私たちが望む並行処理を確実に行うために、`read1, read2, write1, write2` という2つのスレッドを開始します。

2. We assert that the version number has been incremented only once. バージョン番号は1回だけインクリメントされていると断言します。

3. We can also check on the specific exception if we like. また、お好みで特定の例外を確認することもできます。

4. And we double-check that only one allocation has gotten through. そして、1つの割り当てだけが通過していることを再確認します。

### 1.8.1. Enforcing Concurrency Rules by Using Database Transaction Isolation Levels データベーストランザクションの分離レベルを使用した同時実行ルールの適用

To get the test to pass as it is, we can set the transaction isolation level on our session:
このままテストに合格するには、セッションにトランザクション分離レベルを設定すればよいでしょう。

Set isolation level for session (src
セッションのアイソレーションレベルを設定 (src

```python
DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine(
    config.get_postgres_uri(),
    isolation_level="REPEATABLE READ",
))
```

- TIP ヒント

Transaction isolation levels are tricky stuff, so it’s worth spending time understanding the Postgres documentation.3
トランザクションの分離レベルは厄介なものなので、Postgres のドキュメントを理解するのに時間を費やす価値があります。

### 1.8.2. Pessimistic Concurrency Control Example: SELECT FOR UPDATE 悲観的同時実行制御の例。 更新のために選択する

There are multiple ways to approach this, but we’ll show one.
このアプローチには複数の方法がありますが、ここではそのうちの一つを紹介します。
`SELECT FOR UPDATE` produces different behavior; two concurrent transactions will not be allowed to do a read on the same rows at the same time:
SELECT FOR UPDATE`は異なる動作をします。2つの同時実行トランザクションが同時に同じ行の読み取りを行うことはできません。

`SELECT FOR UPDATE` is a way of picking a row or rows to use as a lock (although those rows don’t have to be the ones you update).
SELECT FOR UPDATE`は、ロックする行を選択する方法です（ただし、これらの行は更新する行である必要はありません）。 If two transactions both try to `SELECT FOR UPDATE`a row at the same time, one will win, and the other will wait until the lock is released. 2つのトランザクションが同時に行を`SELECT FOR UPDATE` しようとすると、一方が勝者となり、もう一方はロックが解除されるまで待つことになります。
So this is an example of pessimistic concurrency control.
つまり、これは悲観的な同時実行制御の一例です。

Here’s how you can use the SQLAlchemy DSL to specify `FOR UPDATE` at query time:
ここでは、SQLAlchemy DSL を使って、クエリ時に `FOR UPDATE` を指定する方法を紹介します。

SQLAlchemy with_for_update (src
SQLAlchemy with_for_update (src)

```python
    def get(self, sku):
        return self.session.query(model.Product) \
                           .filter_by(sku=sku) \
                           .with_for_update() \
                           .first()
```

This will have the effect of changing the concurrency pattern from
これは、同時実行パターンを次のように変更する効果があります。

```
read1, read2, write1, write2(fail)
```

to
まで

```
read1, write1, read2, write2(succeed)
```

Some people refer to this as the “read-modify-write” failure mode.
これを「read-modify-write」障害モードと呼ぶ人もいます。
Read “PostgreSQL Anti-Patterns:
PostgreSQLアンチパターン "を読んでください。
Read-Modify-Write Cycles” for a good overview.
Read-Modify-Write Cycles" を読むと概要がよくわかります。

We don’t really have time to discuss all the trade-offs between `REPEATABLE READ` and `SELECT FOR UPDATE`, or optimistic versus pessimistic locking in general.
PREPEATABLE READ`と`SELECT FOR UPDATE` の間のトレードオフや、一般的な楽観的ロックと悲観的ロックについて議論している時間は本当にありません。
But if you have a test like the one we’ve shown, you can specify the behavior you want and see how it changes.
しかし、今回紹介したようなテストがあれば、欲しい動作を指定して、それがどのように変化するかを確認することができます。
You can also use the test as a basis for performing some performance experiments.
また、このテストを元に性能実験を行うこともできます。

## 1.9. Wrap-Up まとめ

Specific choices around concurrency control vary a lot based on business circumstances and storage technology choices, but we’d like to bring this chapter back to the conceptual idea of an aggregate: we explicitly model an object as being the main entrypoint to some subset of our model, and as being in charge of enforcing the invariants and business rules that apply across all of those objects.
並行処理制御に関する具体的な選択肢は、ビジネスの状況やストレージ技術の選択によって大きく異なりますが、この章では、集約の概念に戻りたいと思います。つまり、あるオブジェクトをモデルのサブセットへの主要なエントリポイントとして明示的にモデル化し、それらのオブジェクトすべてに適用される不変性とビジネスルールを実施する役割を果たします。

Choosing the right aggregate is key, and it’s a decision you may revisit over time.
正しい集計方法を選択することが重要であり、時間の経過とともに見直される可能性のある決定です。
You can read more about it in multiple DDD books.
この点については、複数のDDD関連書籍で詳しく述べられています。
We also recommend these three online papers on effective aggregate design by Vaughn Vernon (the “red book” author).
また、「red book」の著者であるVaughn Vernonによる効果的な集合体設計に関する3つのオンラインペーパーもお勧めします。

Table 7-1 has some thoughts on the trade-offs of implementing the Aggregate pattern.
表7-1に、Aggregateパターンを実装する際のトレードオフに関する考察がある。

- Pros 長所

- Python might not have “official” public and private methods, but we do have the underscores convention, because it’s often useful to try to indicate what’s for “internal” use and what’s for “outside code” to use. Choosing aggregates is just the next level up: it lets you decide which of your domain model classes are the public ones, and which aren’t. Pythonには「公式」のpublicメソッドとprivateメソッドがないかもしれませんが、アンダースコアの規約があります。これは、何が「内部」用で何が「外部コード」用かを示すのに便利なことが多いからです。 集約の選択は、その次の段階です。ドメインモデルのクラスのうち、どれを公開し、どれを公開しないかを決定することができます。

- Modeling our operations around explicit consistency boundaries helps us avoid performance problems with our ORM. 明示的な一貫性境界を中心に操作をモデル化することで、ORMの性能問題を回避することができます。

- Putting the aggregate in sole charge of state changes to its subsidiary models makes the system easier to reason about, and makes it easier to control invariants. 集合体は、その子モデルの状態変化を単独で担当することで、システムの推論が容易になり、不変量の制御が容易になる。

- Cons 短所

- Yet another new concept for new developers to take on. Explaining entities versus value objects was already a mental load; now there’s a third type of domain model object? 新しい開発者にとって、また新しいコンセプトが増えました。 エンティティやバリューオブジェクトを説明するのは、すでに精神的な負担になっていました。

- Sticking rigidly to the rule that we modify only one aggregate at a time is a big mental shift. 一度に1つの集合体しか修正しないというルールに固執するのは、大きな精神的な変化です。

- Dealing with eventual consistency between aggregates can be complex. 集合体間の最終的な整合性を扱うのは、複雑な場合があります。

- AGGREGATES AND CONSISTENCY BOUNDARIES RECAP アグリゲートとコンシステンシーバウンダリーのリキャップ

- Aggregates are your entrypoints into the domain model 集計はドメインモデルへの入口である

- By restricting the number of ways that things can be changed, we make the system easier to reason about. 物事の変更方法を制限することで、システムを推論しやすくしているのです。

- Aggregates are in charge of a consistency boundary アグリゲートは一貫性のある境界を担当する

- An aggregate’s job is to be able to manage our business rules about invariants as they apply to a group of related objects. It’s the aggregate’s job to check that the objects within its remit are consistent with each other and with our rules, and to reject changes that would break the rules. アグリゲートの仕事は、関連するオブジェクトのグループに適用される不変量に関するビジネスルールを管理できるようにすることです。 アグリゲートの仕事は、その権限内のオブジェクトが互いに、そして私たちのルールと一致していることを確認し、ルールを破るような変更を拒否することです。

- Aggregates and concurrency issues go together 集計と並行性の問題は両立する

- When thinking about implementing these consistency checks, we end up thinking about transactions and locks. Choosing the right aggregate is about performance as well as conceptual organization of your domain. これらの一貫性チェックの実装を考えるとき、結局はトランザクションとロックについて考えることになる。 正しいアグリゲートを選択することは、パフォーマンスだけでなく、ドメインの概念的な構成にも関わることです。

## 1.10. Part I Recap Part I Recap

Do you remember Figure 7-5, the diagram we showed at the beginning of Part I to preview where we were heading?
第1部の冒頭で、これから向かう先を予習するために示した図7-5を覚えているだろうか。

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0705.png)

So that’s where we are at the end of Part I. What have we achieved?
さて、ここまでが第一部の終わりです。
We’ve seen how to build a domain model that’s exercised by a set of high-level unit tests.
私たちは、一連のハイレベルなユニットテストによって実行されるドメインモデルを構築する方法を見ました。
Our tests are living documentation: they describe the behavior of our system—the rules upon which we agreed with our business stakeholders—in nice readable code.
テストは生きたドキュメントであり、システムの動作や、ビジネス関係者と合意したルールを、読みやすいコードで記述します。
When our business requirements change, we have confidence that our tests will help us to prove the new functionality, and when new developers join the project, they can read our tests to understand how things work.
また、新しい開発者がプロジェクトに参加したときにも、テストを読んでどのように動作するかを理解することができます。

We’ve decoupled the infrastructural parts of our system, like the database and API handlers, so that we can plug them into the outside of our application.
データベースやAPIハンドラなど、システムのインフラ部分を切り離し、アプリケーションの外部にプラグインできるようにしたのです。
This helps us to keep our codebase well organized and stops us from building a big ball of mud.
これにより、コードベースが整理され、大きな泥の塊になるのを防ぐことができます。

By applying the dependency inversion principle, and by using ports-and-adapters-inspired patterns like Repository and Unit of Work, we’ve made it possible to do TDD in both high gear and low gear and to maintain a healthy test pyramid.
依存関係逆転の原則を適用し、RepositoryやUnit of Workといったports and-adaptersにインスパイアされたパターンを使うことで、ハイギアでもローギアでもTDDを行うことができ、健全なテストピラミッドを維持することができるようになったのです。
We can test our system edge to edge, and the need for integration and end-to-end tests is kept to a minimum.
システムの端から端までテストすることができ、統合テストやエンドツーエンドテストの必要性は最低限に抑えられます。

Lastly, we’ve talked about the idea of consistency boundaries.
最後に、一貫性の境界の考え方についてお話しました。
We don’t want to lock our entire system whenever we make a change, so we have to choose which parts are consistent with one another.
変更を加えるたびにシステム全体をロックすることは避けたいので、どの部分が互いに一貫しているかを選択する必要があります。

For a small system, this is everything you need to go and play with the ideas of domain-driven design.
小規模なシステムであれば、ドメイン駆動設計のアイデアを活用するために必要なものは、これですべて揃います。
You now have the tools to build database-agnostic domain models that represent the shared language of your business experts.
あなたは今、ビジネスエキスパートたちの共有言語を表す、データベースにとらわれないドメインモデルを構築するためのツールを手に入れました。
Hurrah!
万歳!

- NOTE 注

- At the risk of laboring the point—we’ve been at pains to point out that each pattern comes at a cost. Each layer of indirection has a price in terms of complexity and duplication in our code and will be confusing to programmers who’ve never seen these patterns before. If your app is essentially a simple CRUD wrapper around a database and isn’t likely to be anything more than that in the foreseeable future, you don’t need these patterns. Go ahead and use Django, and save yourself a lot of bother. 私たちは、それぞれのパターンが犠牲を伴うものであることを苦心して指摘してきた。 間接的なレイヤーを重ねるごとに、コードの複雑さや重複が発生し、これらのパターンを見たことがないプログラマーは混乱するでしょう。 もしあなたのアプリケーションが本質的にデータベースの周りの単純な CRUD ラッパーで、当面それ以上にはなりそうにないのなら、これらのパターンは必要ないでしょう。 どうぞ、Django を使って、多くの手間を省いてください。

In Part II, we’ll zoom out and talk about a bigger topic: if aggregates are our boundary, and we can update only one at a time, how do we model processes that cross consistency boundaries?
パートIIでは、より大きなトピックについて説明します。アグリゲートが境界であり、一度に1つしか更新できない場合、一貫性の境界を越えるプロセスをどのようにモデル化するのでしょうか。

1. Perhaps we could get some ORM/SQLAlchemy magic to tell us when an object is dirty, but how would that work in the generic case—for example, for a `CsvRepository`? おそらく、いくつかのORMを手に入れることができるでしょう。

2. `time.sleep()` works well in our use case, but it’s not the most reliable or efficient way to reproduce concurrency bugs. Consider using semaphores or similar synchronization primitives shared between your threads to get better guarantees of behavior. 2. `time.sleep()` は私たちの使用例ではうまく機能しますが、並行処理のバグを再現するための最も信頼できる、または効率的な方法ではありません。 より良い動作保証を得るために、スレッド間で共有されるセマフォや類似の同期プリミティブを使うことを検討してください。

3. If you’re not using Postgres, you’ll need to read different documentation. Annoyingly, different databases all have quite different definitions. Oracle’s `SERIALIZABLE` is equivalent to Postgres’s `REPEATABLE READ`, for example. Postgresを使用していない場合は、別のドキュメントを読む必要があります。 困ったことに、データベースによって定義が全く異なるのです。 例えば、Oracleの `SERIALIZABLE` はPostgresの `REPEATABLE READ` と同等です。
