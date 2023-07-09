## link リンク

https://www.thedigitalcatbooks.com/pycabook-chapter-02/
https://www.thedigitalcatbooks.com/pycabook-chapter-02/

# Chapter 2 - Components of a clean architecture 第2章 クリーンなアーキテクチャの構成要素

## Components of a clean architecture クリーンなアーキテクチャの構成要素

Wait a minute.
ちょっと待ってくれ。
Wait a minute Doc, uh, are you telling me you built a time machine...out of a DeLorean?
ちょっと待って、ドク、デロリアンでタイムマシンを作ったって言うのかい？

Back to the Future, 1985
バック・トゥ・ザ・フューチャー、1985年

In this chapter I will analyse the set of software design principles collectively known as "clean architecture".
この章では、「クリーン・アーキテクチャ」と総称される一連のソフトウェア設計原則を分析する。
While this specific name has been introduced by Robert Martin, the concepts it pushes are part of software engineering, and have been successfully used for decades.
この具体的な名称はロバート・マーティンによって紹介されたものだが、この名称が押し進める概念はソフトウェア工学の一部であり、何十年もの間、うまく使われてきた。

Before we dive into a possible implementation of them, which is the core of this book, we need to analyse more in depth the structure of the clean architecture and the components you can find in the system designed following it.
本書の核心である、それらの可能な実装に飛び込む前に、クリーン・アーキテクチャの構造と、それに従って設計されたシステムに見られるコンポーネントをより深く分析する必要がある。

## Divide et impera ♪ Divide et impera

One of the main goals of a well designed system is to achieve control.
**うまく設計されたシステムの主な目標のひとつは、コントロールを達成すること**だ。
From this point of view, a software system is not different from a human working community, like an office or a factory.
この観点からすると、ソフトウェアシステムは、オフィスや工場のような人間の作業共同体と変わらない。
In such environments there are workers who exchange data or physical objects to create and deliver a final product, be it an object or a service.
このような環境では、データや物理的なオブジェクトを交換し、オブジェクトであれサービスであれ、最終的な製品を作り、提供するワーカーがいる。
Workers need information and resources to perform their own job, but most of all they need to have a clear picture of their responsibilities.
労働者は自分の仕事を遂行するために情報やリソースを必要とするが、何よりも自分の責任を明確に把握する必要がある。

While in a human society we value initiative and creativity, however, in a machine such as a software system, components shouldn't be able to do anything that is not clearly stated when the system is designed.
人間社会では自発性や創造性を重んじるものだが、ソフトウェア・システムのような機械では、システムの設計時に明示されていないことをコンポーネントができるはずがない。
Software is not alive, and despite the impressive achievements of artificial intelligence in the latter years, I still believe there is a spark in a human being that cannot be reproduced by code alone.
ソフトウェアは生きているわけではないし、近年人工知能が目覚ましい成果を上げたとはいえ、人間の中にはコードだけでは再現できない輝きがあると私は信じている。

Whatever our position on AIs, I think we all agree that a system works better if responsibilities are clear.
AIに対する立場がどうであれ、**責任の所在が明確であれば、システムはよりよく機能する**という点では、誰もが同意するところだろう。
Whether we are dealing with software or human communities, it is always dangerous to be unclear about what a component can or should do, as areas of influence and control naturally overlap.
**ソフトウェアであれ人間社会であれ、あるコンポーネントができること、あるいはすべきことが不明確であることは常に危険**である。
This can lead to all sorts of issues, from simple inefficiencies to complete deadlocks.
これは、単純な非効率から完全なデッドロックまで、あらゆる種類の問題を引き起こす可能性がある。

A good way to increase order and control in a system is to split it into subsystems, establishing clear and rigid borders between them, to regulate the data exchange.
システムの秩序と制御を高める良い方法は、システムをサブシステムに分割し、それらの間に明確かつ厳格な境界線を設けて、データのやり取りを規制することである。
This is an extension of a political concept (divide et impera) which states that it is simpler to rule a set of interconnected small systems than a single complex one.
これは、政治的な概念（**divide et impera**）の延長線上にあるもので、**複雑なひとつのシステムを支配するよりも、相互に結びついた小さなシステムの集合を支配するほうが単純だ**というものだ。

In the system we designed in the previous chapter, it is always clear what a component expects to receive when called into play, and it is also impossible (or at least, forbidden) to exchange data in a way that breaks the structure of the system.
前章で設計したシステムでは、呼び出されたコンポーネントが何を受け取ることになるかは常に明確であり、システムの構造を壊すような方法でデータを交換することは不可能である（少なくとも禁止されている）。

You have to remember that a software system is not exactly like a factory or an office.
ソフトウェア・システムは、工場やオフィスのようなものではないことを忘れてはならない。
Whenever we discuss machines we have to consider both the way they work (run time) and the way they have been built or will be modified (development time).
マシンについて議論するときは常に、**マシンが機能する方法（run time）と、マシンが構築された、あるいは今後修正される方法（development time）の両方を考慮しなければならない**。
In principle, computers don't care where data comes from and where it goes.
原則的に、コンピュータはデータがどこから来てどこへ行くかを気にしない。(気にするのは入力値と出力値のみ)
Humans, on the other hand, who have to build and maintain the system, need a clear picture of the data flow to avoid introducing bugs or killing performances.
一方、システムを構築し維持しなければならない人間は、バグの発生やパフォーマンスの低下を避けるために、**データの流れを明確に把握する必要がある.**

## Data types データ型

An important part in a system is played by data types, that is the way we encapsulate and transmit information.
システムにおいて重要な役割を果たすのがデータ型であり、情報をカプセル化して伝達する方法である。
In particular, when we discuss software systems, we need to make sure that types that are shared by different systems are known to all of them.
特に、ソフトウェア・システムについて議論する場合、異なるシステムで共有される型が、すべてのシステムで既知であることを確認する必要がある。
The knowledge of data types and formats is, indeed, a form of coupling.
**データ型やフォーマットに関する知識は、まさにカップリングの一種**である。
Think about human languages: if you have to talk to an audience, you have to use a language they understand, and this makes you coupled with your audience.
人間の言語について考えてみよう。聴衆と話さなければならないなら、彼らが理解できる言語を使わなければならない。
This book is written (tentatively) in English, which means that I am coupled with English-speaking readers.
この本は（仮に）英語で書かれているので、英語圏の読者とカップリングしていることになる。
If all English speakers in the world suddenly decided to forget the language and replace it with Italian I should write the book from scratch (but with definitely less effort).
もし世界中の英語話者が突然、その言語を忘れてイタリア語に置き換えることを決めたら、私はゼロから本を書くだろう（しかし、間違いなく労力は減る）。

When we consider a software system, thus, we need to understand which part defines the types and the data format (the "language"), and ensure that the resulting dependencies don't get in the way of the implementer.
したがって、**ソフトウェア・システムを考える場合、型とデータ・フォーマット（「言語」）を定義する部分を理解し、その結果生じる依存関係が実装者の邪魔にならないようにする必要がある**。
In the previous chapter we discovered that there are components in the system that should be considered of primary importance and represent the core of the system (use cases), and others which are less central, often considered implementation details.
前章では、**システムには、システムの中核をなす重要なcomponent(usecase)と、それほど中心的ではなく、しばしば実装の詳細とみなされるcomponent(=web framework や adapter??)があることを発見した**。
Again, mind that calling them "details" doesn't mean they are not important or that they are trivial to implement, but that replacing them with different implementations does not affect the core of the system (business logic).
繰り返しになるが、これらを「ディテール」と呼ぶことは、重要でないとか、実装が些細であるということを意味するのではなく、「**異なる実装に置き換えてもシステムの中核（ビジネス・ロジック）には影響を与えない**」ということを念頭に置いてほしい。(なるほど...! ここでの implementation detailsの意味はこれなんだ...! まあでもfunction単位での同用語と意味合いは近いのかな...:thinking:)

So, there is a hierarchy of components that spawns from the dependencies between them.
**つまり、コンポーネント間の依存関係から生まれるコンポーネントの階層があるのだ。**
Some components are defined at the very beginning of the design and do not depend on any other component, while others will come later and depend on them.
**あるコンポーネントは設計の一番最初に定義され、他のコンポーネントに依存しないが、他のコンポーネントは後から定義され、他のコンポーネントに依存する。**
When data types are involved, the resulting dependencies cannot break this hierarchy, as this would re-introduce a coupling between components that we want to avoid.
データ型が関係する場合、結果として生じる依存関係はこの階層を壊すことはできない。これは、避けたいコンポーネント間のカップリングを再び引き起こすことになるからだ。

Let's go back to the initial example of a shop that buys items from a wholesale, displays them on shelves, and sells them to customers.
卸売業者から商品を仕入れ、棚に陳列し、顧客に販売するという最初の例に戻ろう。
There is a clear dependency between two components here: the component called "shop" depends on the component called "wholesale", as the data ("items") flow from the latter to the former.
ショップ "と呼ばれるコンポーネントは、"ホールセール "と呼ばれるコンポーネントに依存している。
The size of the shelves in the shop, in turn, depends on the size of the items (types), which is defined by the wholesale, and this follows the dependency we already established.
店内の棚の大きさは、卸売業者によって定義された商品（種類）の大きさに依存する。

If the size of the items was defined by the shop, suddenly there would be another dependency opposing the one we already established, making the wholesale depend on the shop.
もしアイテムのサイズがショップによって定義されるなら、私たちがすでに確立した依存関係とは別の依存関係が突然発生し、卸売りがショップに依存することになる。
Please note that when it comes to software systems this is not a circular dependency, because the first one is a conceptual dependency while the second one happens at the language level at compile time.
なぜなら、最初の依存関係は概念的なものであり、2番目の依存関係はコンパイル時に言語レベルで発生するからである。
At any rate, having two opposite dependencies is definitely confusing, and makes it hard to replace "peripheral" components such as the shop.
いずれにせよ、2つの正反対の依存関係があることは間違いなく混乱を招くし、ショップのような **"peripheral(周辺)"コンポーネント** を置き換えることも難しくなる。

## The main four layers 主な4つの層

The clean architecture tries to capture both the conceptual hierarchy of components and the type hierarchy through a layered approach.
クリーンなアーキテクチャは、コンポーネントの概念的な階層と、レイヤーアプローチによる型の階層の両方(?)を捉えようとしている。
In a clean architecture the components of the system are categorised and belong to a specific layer, with rules relative to the communication between components belonging to the same or to different layers.
**クリーンなアーキテクチャでは、システムのcomponentは分類され、特定のレイヤーに属し、同じレイヤーまたは異なるレイヤーに属するコンポーネント間の通信(=依存関係の向き??)に関するルールがある**。
In particular, a clean architecture is a spherical structure, with inner (lower) layers completely encompassed by outer (higher) ones, and the former being oblivious of the existence of the latter.
特に、クリーン・アーキテクチャは**球状の構造**であり、内側（下層）の層は外側（上層）の層に完全に包含され、前者は後者の存在に気づかない(知らない)。

![](https://www.thedigitalcatbooks.com/images/pycabook/circles01.svg)

Remember that in computer science, the words "lower" and "higher" almost always refer to the level of abstraction, and not to the importance of a component for the system.
コンピュータ・サイエンスでは、**「より低い」「より高い」という言葉は、ほとんどの場合、抽象化のレベルを指すのであって、システムにとってのコンポーネントの重要性を指すのではない**ことを覚えておいてほしい.(高レベル=抽象度高い=観察可能な振る舞いやInterfaceのイメージ?? システム全体で言えば、外側のlayerのcomponentの方がユーザ目線では観察可能な振る舞いに近いので、高レベルなのかな:thinking:)
Each part of a system is important, otherwise it would not be there.
システムの(全て)各部分は重要であり、そうでなければ存在しない。

Let's have a look at the main layers depicted in the figure, keeping in mind that a specific implementation may require to create new layers or to split some of these into multiple ones.
図に描かれている主なレイヤーを見てみよう。特定の実装では、**新しいレイヤーを作成**したり、**これらのレイヤーのいくつかを複数のレイヤーに分割**したりする必要があるかもしれないことに留意してほしい。

### Entities エンティティ

This layer of the clean architecture contains a representation of the domain models, that is everything your system needs to interact with and is sufficiently complex to require a specific representation.
**クリーン・アーキテクチャのこのレイヤーには、ドメイン・モデルの表現が含まれる**。それは、システムが相互作用する必要があるものすべてであり、特定の表現を必要とするほど十分に複雑なものである。
For example, strings in Python are complex and very powerful objects.
例えば、Pythonの文字列は複雑で非常に強力なオブジェクトだ。
They provide many methods out of the box, so in general, it is useless to create a domain model for them.
これらは多くのメソッドを提供しているため、一般的にドメインモデルを作成するのは無駄である。
If your project was a tool to analyse medieval manuscripts, however, you might need to isolate sentences and their features, and at this point it might be reasonable to define a specific entity.
しかし、プロジェクトが中世の写本を分析するためのツールであれば、文とその特徴を分離する必要があるかもしれない。 この場合は、strを特定のEntityとして定義する道理があるかもしれない.

![https://www.thedigitalcatbooks.com/images/pycabook/circles02_entities.svg]

Since we work in Python, this layer will likely contain classes, with methods that simplify the interaction with them.
我々はPythonで仕事をしているので、このレイヤーにはおそらくクラスが含まれ、クラスとのやりとりを簡単にするメソッドがある。
It is very important, however, to understand that the models in this layer are different from the usual models of frameworks like Django.
しかし、このレイヤーのモデルは、Django のようなフレームワークの通常のモデルとは異なることを理解することが非常に重要です。
These models are not connected with a storage system, so they cannot be directly saved or queried using their own methods, they don't contain methods to dump themselves to JSON strings, they are not connected with any presentation layer.
これらのモデルは、ストレージシステムとは接続されていないので、直接保存したり、独自のメソッドを使ってクエリしたりすることはできませんし、JSON文字列にダンプするメソッドも含まれていません。
They are so-called lightweight models.
いわゆる軽量モデルだ。

This is the inmost layer.
これが最内層だ。
Entities have mutual knowledge since they live in the same layer, so the architecture allows them to interact directly.
**Entity達は同じレイヤーに住んでいるため相互知識があり、アーキテクチャによって直接相互作用することができる**。
This means that one of the Python classes that represent an entity can use another one directly, instantiating it and calling its methods.
これはすなわち、**あるEntityを表すPythonクラスの1つが、別のクラスを直接使用し、インスタンス化してそのメソッドを呼び出すことができること**を意味する。(=Interfaceではなく、具象クラスを直接初期化しても良いって事!)
Entities don't know anything that lives in outer layers, though.
**エンティティはアウターレイヤーに住むものを何も知らない**.
They cannot call the database, access methods provided by the presentation framework, or instantiate use cases.
データベースを呼び出したり、プレゼンテーション・フレームワークが提供するメソッドにアクセスしたり、usecaseをインスタンス化したりすることはできない.

The entities layer provides a solid foundation of types that the outer layers can use to exchange data, and they can be considered the vocabulary of your business.
エンティティ・レイヤーは、**外側のレイヤーが(components間の!)データ交換に使用できる型の強固な基盤**を提供するもので、**vocabulary of your business(ビジネスの語彙)**と考えることができる。(=Domain Model, Domain Languageか...!) (データクラスがEntities層に定義されるイメージ? ただData class = Value object と Entityクラスは別物だった気もする. Entities層とクラスの種類としてのEntityの意味合いは異なるのかな...??)

### Use cases

As we said before the most important part of a clean system are use cases, as they implement the business rules, which are the core reason of existence of the system itself.
先に述べたように、**クリーンなシステムの最も重要な部分はuse case**である。**use caseはビジネスルール(=コアロジック)を実装するものであり、システム自体の存在理由の中核をなすもの**だからである.
Use cases are the processes that happen in your application, where you use your domain models to work on real data.
ユースケースとは、アプリケーションの中で発生するプロセスのことで、ドメインモデル(=Entities層のデータクラスのイメージ!)を使って(=入出力のデータタイプで使ったり...!)実際のデータを操作する.
Examples can be a user logging in, a search with specific filters being performed, or a bank transaction happening when the user wants to buy the content of the cart.
例としては、ユーザがログインする、特定のフィルタを使った検索が実行される、またはユーザがカートの内容を購入したいときに銀行取引が発生する、などがあります。

![](https://www.thedigitalcatbooks.com/images/pycabook/circles03_use_cases.svg)

Use cases should be as small as possible.
**ユースケースはできるだけ小さくすべき**である.(ほうほう...!)
It is very important to isolate small actions into separate use cases, as this makes the whole system easier to test, understand and maintain.
**小さなアクションを個別のユースケースに分離することは非常に重要**で、そうすることでシステム全体のテスト、理解、保守が容易になるからだ。
Use cases have full access to the entities layer, so they can instantiate and use them directly.
**ユースケースはエンティティ・レイヤーにフルアクセスできるので、それらを直接インスタンス化して使用することができる**. (InterfaceでDIする必要ないって事??)(usecase間は、Interfaceを使ってDIするのかな.)
They can also call each other, and it is common to create complex use cases composing simple ones.
単純なusecaseを組み合わせて複雑なusecaseを作ることもよくある。

### Gateways ゲートウェイ

This layer contains components that define interfaces for external systems, that is a common access model to services that do not implement the business rules.
このレイヤーには、**外部システム用のインターフェースを定義するコンポーネントが含まれる**。つまり、ビジネスルールを実装していないサービスへの共通のアクセスモデルである。
The classic example is that of a data storage, which internal details can be very different across implementations.
**典型的な例はデータ・ストレージ**で、内部的な詳細は実装によって大きく異なることがある。
These implementations share a common interface, otherwise they would not be implementations of the same concept, and the gateway's task is to expose it.
これらの実装は共通のインターフェイスを共有しており、そうでなければ同じコンセプトの実装ではなく、ゲートウェイの仕事はそれを公開することである.

If you recall the simple example I started with, this is where the database interface would live.
先ほどの簡単な例を思い出すと、**ここがデータベース・インターフェース(=adapter??)の場所**だ。
Gateways have access to entities, so the interface can freely receive and return objects which type has been defined in that layer, as they can freely access use cases.
gateways は entities にアクセスできるので、インターフェースは、usecaseに自由にアクセスできるように、そのレイヤーで定義された型のオブジェクトを自由に受け取り、返すことができる。
Gateways are used to mask the implementation of external systems, however, so it is rare for a gateway to call a use case, as this can be done by the external system itself.
しかし、**ゲートウェイは外部システムの実装をマスクするために使用されるため**、ゲートウェイがユースケースを呼び出すことは稀である.(=じゃあ基本はGateways にある Interface を、UsecasesのクラスがDIする感じ??:thinking:)
The gateways layer is intimately connected with the external systems one, which is why the two are separated by a dashed line.
**ゲートウェイ層は外部システム層と密接に関係している(強いcoupling?)**ため、両者は破線で区切られている。

### External systems 外部システム

This part of the architecture is populated by components that implement the interfaces defined in the previous layer.
アーキテクチャのこの部分には、**前のレイヤー(Gateways)で定義されたInterface(ex. DB systemの抽象クラス=adapter?)を実装するcomponents(ex. DB systemの具象クラス??)が配置される**。
The same interface might be implemented by one or more concrete components, as your system might want to support multiple implementations of that interface at the same time.
システムがそのInterfaceの複数の実装を同時にサポートしたいかもしれないので、同じinterfaceが1つ以上の具象コンポーネントによって実装されるかもしれない。(うんうんまあまあ)
For example, you might want to expose some use cases both through an HTTP API and a command line interface, or you want to provide support for different types of storage according to some configuration value.
例えば、ある usecase をHTTP APIとコマンドライン・インターフェイスの両方で公開したいとか、ある設定値に応じて異なるタイプのストレージのサポートを提供したいとか.

![](https://www.thedigitalcatbooks.com/images/pycabook/circles05_external_systems.svg)

Please remember that the "external" adjective doesn't always mean that the system is developed by others, or that it is a complex system like a web framework or a database.
**"external"という形容詞は、必ずしもそのシステムが他者によって開発されたものであったり、ウェブ・フレームワークやデータベースのような複雑なシステムであることを意味するものではない**ことを覚えておいてほしい.
The word has a topological meaning, which shows that the system we are talking about is peripheral to the core of the architecture, that is it doesn't implement business logic.
この言葉にはトポロジー的な意味があり、私たちが話しているこれらの**システム(=components)がアーキテクチャの中核から外れた周辺的なものであること、つまりビジネス・ロジックを実装していないことを示している**.(ビジネスロジックを実装している=use cases層よりも内側, ビジネスロジックではない=Gateways層よりも外側、という感じ??:thinking:)
So we might want to use a messaging system developed in-house to send notifications to the clients of a certain service, but this is again just a presentation layer, unless our business is specifically centred around creating notification systems.
だから、社内で開発したメッセージング・システムを使って、あるサービスのクライアントに通知を送りたいかもしれない。しかし、これはまた単なるプレゼンテーション・レイヤーに過ぎない。

External systems have full access to gateways, use cases, and entities.
外部システムはゲートウェイ、ユースケース、エンティティにフルアクセスできる.
While it is easy to understand the relationship with gateways, which are created to wrap specific systems, it might be less clear what external systems should do with use cases and entities.
**特定のシステムを包むために作られるGateways層との関係を理解するのは簡単**だが、外部システムがユースケースやエンティティに対して何をすべきかは、あまり明確ではないかもしれない.
As for use cases, external systems are usually the parts of the system that trigger them, being the way users run the business logic.
usecaseに関しては、**external systemsは通常、ユーザがビジネス・ロジックを実行するためのトリガーとなる**システム部分である。
A user clicking on a button, visiting a URL, or running a command, are typical examples of interactions with an external system that runs a use case directly.
ユーザがボタンをクリックしたり、URLを訪問したり、コマンドを実行したりすることは、usecasesを直接実行するexternal systemsとのインタラクションの典型的な例である。
As for entities, an external system can directly process them, for example to return them in a JSON payload, or to map input data into a domain model.
例えば、JSONペイロードで返したり、入力データをドメインモデルにマッピングしたりする。

I want to point out a difference between external systems that are used by use cases and external systems that want to call use cases.
**usecases に使われる external systems(=InterfaceとしてDIされる様なcomponent??) と、usecases を呼び出したい external systems (=ビジネスロジックを実行する為のトリガー的なcomponent??)の違い**を指摘したい.
In the first case the direction of the communication is outwards, and we know that in the clean architecture we can't go outwards without interfaces.
前者のケースでは、通信(i.e. 依存)の方向は外側であり、クリーンなアーキテクチャでは、**インターフェイスなしでは外側に行けない**ことがわかっている。(Intefaceがあったら外側に言って良いんだ...!:thinking:)
Thus, when we access an external system from a use case we always need an interface.
したがって、**use cases から external systems にアクセスする際には、常にインターフェースが必要になる**.(InterfaceでDIすればいいんだ...!)
When the external system wants to call use cases, instead, the direction of the communication is inwards, and this is allowed directly, as external layers have full access to the internal ones.
代わりに外部システムがユースケースを呼び出したい場合、通信の方向は内側になり、外部レイヤーは内部レイヤーに完全にアクセスできるため、これは直接許可される.(具象クラスを直接参照できる...!)

This, practically speaking, translates into two extreme cases, well represented by a database and a web framework.
これは現実的に言えば、**データベース(前者のケース)とウェブ・フレームワーク(後者のケース)に代表される2つの極端なケース**になる.
When a use case accesses a storage system there should be a loose coupling between the two, which is why we wrap the storage with an interface and assume that in the use case.
**use case がストレージシステムにアクセスする場合、両者の間には緩やかな結合が必要である。これが、ストレージを Interface でラップし(これはGatewaysにあるはず??)、use case でそれを想定(i.e 参照)する理由である.**
When the web framework calls a use case, instead, the code of the endpoint doesn't need any interface to access it.
代わりに、**ウェブ・フレームワークがユースケースを呼び出すとき、エンドポイントのコードはそれにアクセスするためのインターフェースを必要としない.**

## Communication between layers レイヤー間のコミュニケーション

The deeper a layer is in this architecture, the more abstract the content is.
このアーキテクチャでは、レイヤーが深ければ深いほど(=内側に行くほど...!)、コンテンツはより抽象的になる.
The inner layers contain representations of business concepts, while the outer layers contain specific details about the real-life implementation.
内側のレイヤーにはビジネスコンセプトの表現が含まれ、外側のレイヤーには実際の実装に関する具体的な詳細が含まれる.
The communication between elements that live in the same layer is unrestricted, but when you want to communicate with elements that have been assigned to other layers you have to follow one simple rule.
同じレイヤーに住むエレメント同士の通信は自由だが、他のレイヤーに割り当てられたエレメントと通信したい場合は、**ある簡単なルール**に従わなければならない。
This rule is the most important thing in a clean architecture, possibly being the core expression of the clean architecture itself.
このルールは、**クリーン・アーキテクチャにおいて最も重要なものであり、クリーン・アーキテクチャの核となる表現そのもの**かもしれない。

**The Golden Rule: talk inwards with simple structures, talk outwards through interfaces. シンプルな構造(=具象クラス?)で内向きに話し、インターフェースで外向きに話す**

![](https://www.thedigitalcatbooks.com/images/pycabook/circles06_golden_rule.svg)

Your elements should talk inwards, that is pass data to more abstract elements, using basic structures, that is entities and everything provided by the programming language you are using.
「Your elements should talk inwards」つまり、基本的な構造、つまり、使用しているプログラミング言語が提供するエンティティやあらゆるものを使って、より抽象的な要素にデータを渡すのだ.

Your elements should talk outwards using interfaces, that is using only the expected API of a component, without referring to a specific implementation.
「Your elements should talk outwards using interfaces」つまり、特定の実装(具象クラス)を参照することなく、コンポーネントの期待されるAPIのみを使用することです。
When an outer layer is created, elements living there will plug themselves into those interfaces and provide a practical implementation.
アウターレイヤーが作られると、そこ(outer layer)に住むエレメントはそれらのInterfaceに自分自身をプラグインし、実用的な実装を提供することになる。

## APIs and shades of grey APIと灰色の影

The word API is of uttermost importance in a clean architecture.
APIという言葉は、クリーンなアーキテクチャにおいて最も重要である.
Every layer may be accessed by elements living in inner layers by an API, that is a fixed[1] collection of entry points (methods or objects).
**各レイヤーは、内部レイヤーに住むエレメントからAPIによってアクセスすることができる**。**APIとは、エントリーポイント(メソッドまたはオブジェクト)の固定されたコレクション**[1]である. (entry pointsが固定された集合? public methodが固定されてるって意味??)

The separation between layers and the content of each layer is not always fixed and immutable.
レイヤー間の分離や各レイヤーの内容は、必ずしも固定された不変のものではない。
A well-designed system shall also cope with practical world issues such as performances, for example, or other specific needs.
よく設計されたシステムは、例えばパフォーマンスなどの現実的な世界の問題や、その他の特定のニーズにも対応しなければならない。
When designing an architecture it is very important to know "what is where and why", and this is even more important when you "bend" the rules.
建築を設計する際、「何がどこにあり、なぜそうなるのか」を知ることは非常に重要であり、ルールを「曲げる」場合はなおさら重要である。
Many issues do not have a black-or-white answer, and many decisions are "shades of grey", that is it is up to you to justify why you put something in a given place.
多くの問題には白か黒かの答えがなく、多くの決定は「灰色の影」である。

Keep in mind, however, that you should not break the structure of the clean architecture, and be particularly very strict about the data flow.
ただし、クリーン・アーキテクチャーの構造を壊さないようにすること、特にデータ・フローには細心の注意を払うことを肝に銘じてほしい。
If you break the data flow, you are basically invalidating the whole structure.
データフローを壊してしまうと、基本的に構造全体を無効にしてしまうことになる。
You should try as hard as possible not to introduce solutions that are based on a break in the data flow, but realistically speaking, if this saves money, do it.
データ・フローの断絶を前提としたソリューションの導入はできるだけ避けるべきだが、現実的に言えば、これで経費が節約できるのであれば、そうすべきだ。

If you do it, there should be a giant warning in your code and your documentation explaining why you did it.
もしそうするのであれば、あなたのコードとドキュメントに、なぜそうしたのかを説明する巨大な警告があるはずだ。
If you access an outer layer breaking the interface paradigm usually it is because of some performance issues, as the layered structure can add some overhead to the communications between elements.
**インターフェイスのパラダイムを壊して外側のレイヤーにアクセスする場合、**レイヤー構造がエレメント間の通信にオーバーヘッドを追加する可能性があるため、**通常はパフォーマンス上の問題が発生する**。
You should clearly tell other programmers that this happened, because if someone wants to replace the external layer with something different, they should know that there is direct access which is implementation-specific.
もし誰かが外部レイヤーを別のものに置き換えたければ、実装固有の直接アクセスがあることを知るべきだからだ。

For the sake of example, let's say that a use case is accessing the storage layer through an interface, but this turns out to be too slow.
例として、あるusecaseがInterfaceを使ってストレージ・レイヤーにアクセスしているが、これが遅すぎることが判明したとしよう。
You decide then to access directly the API of the specific database you are using, but this breaks the data flow, as now an internal layer (use cases) is accessing an outer one (external interfaces).
その場合、使用している特定のデータベースのAPIに直接アクセスすることに決めたとする. しかしこの場合、内部レイヤー(usecase)が外部レイヤー(External System)にアクセスすることになり、データフローが壊れてしまう。
If someone in the future wants to replace the specific database you are using with a different one, they have to be aware of this, as the new database probably won't provide the same API entry point with the same data.
将来、誰かがあなたが使っている特定のデータベースを別のものに置き換えたくなった場合、新しいデータベースはおそらく同じデータで同じAPIエントリーポイントを提供しないので、このことを認識しておく必要がある.(strongly couplingになってしまう、事を認識した上で意思決定をしろと...!:thinking:)

If you end up breaking the data flow consistently maybe you should consider removing one layer of abstraction, merging the two layers that you are linking.
もし、一貫したデータフローを壊してしまうのであれば、抽象化のレイヤーを1つ取り除き、リンクしている2つのレイヤーを統合することを検討すべきかもしれない。
