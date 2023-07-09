## link リンク

https://www.thedigitalcatbooks.com/pycabook-chapter-01/
https://www.thedigitalcatbooks.com/pycabook-chapter-01/

# Chapter 1 - A day in the life of a clean system 第1章 クリーン・システムの一日

In this chapter I will introduce the reader to a (very simple) system designed with a clean architecture.
この章では、クリーンなアーキテクチャで設計された（非常にシンプルな）システムを紹介する.
The purpose of this introductory chapter is to familiarise with main concepts like separation of concerns and inversion of control, which are paramount in system design.
この入門編の目的は、システム設計において最も重要な **separation of concerns(関心事の分離)** や **inversion of control(制御の逆転)** といった主要概念に慣れることである.
While I describe how data flows in the system, I will purposefully omit details, so that we can focus on the global idea and not worry too much about the implementation.
システム内のデータの流れは説明するが、グローバルなアイデアに集中し、実装についてはあまり気にしないようにするため、あえて詳細は省く。
This example will be then explored in all its glorious details in the following chapters, so there will be time to discuss specific choices.
この例は、次の章でその栄光の詳細を掘り下げていくので、具体的な選択について議論する時間があるだろう。
For now, try to get the big picture.
今は、全体像を把握することに努めよう。

## The data flow データの流れ

In the rest of the book, we will design together part of a simple web application that provides a room renting system.
この本の残りの部分では、**部屋を借りるシステムを提供する簡単なウェブアプリケーション**の一部を一緒にデザインします。
So, let's consider that our "Rent-o-Matic" application[1] is running at https://www.rentomatic.com, and that a user wants to see the available rooms.
そこで、"Rent-o-Matic "アプリケーション[1]が https://www.rentomatic.com で稼働しているとして、**ユーザが空いている部屋を見たい状況**を考えてみよう。
They open the browser and type the address, then clicking on menus and buttons they reach the page with the list of all the rooms that our company rents.
ブラウザを開いて住所を入力し、メニューやボタンをクリックすると、当社がレンタルしているすべての部屋のリストが表示されたページにたどり着く.

Let's assume that this URL is /rooms?status=available.
このURLを `/rooms?status=available`としよう.
When the user's browser accesses that URL, an HTTP request reaches our system, where there is a component that is waiting for HTTP connections.
ユーザのブラウザがそのURLにアクセスすると、HTTPリクエストが私たちのシステムに届き、そこにはHTTP接続を待機している(=リクエストを待ってレスポンスを返そうと待機している...??)コンポーネントがある。
Let's call this component "web framework"[2].
このコンポーネントを「ウェブ・フレームワーク」と呼ぼう[2].(=componentを frameworkと呼ぶ? web serverではなくて...??:thinking:)

The purpose of the web framework is to understand the HTTP request and to retrieve the data that we need to provide a response.
ウェブ・フレームワークの目的は、HTTPリクエストを理解し、レスポンスを提供するために必要なデータを取得することだ。(正しく web server に見える...)
In this simple case there are two important parts of the request, namely the endpoint itself (/rooms), and a single query string parameter, status=available.
この単純なケースでは、リクエストの2つの重要な部分、すなわち、エンドポイント自体(`/rooms`)と、単一のクエリ文字列パラメータ、status=availableがあります。
Endpoints are like commands for our system, so when a user accesses one of them, they signal to the system that a specific service has been requested, which in this case is the list of all the rooms that are available for rent.
**エンドポイントはシステムにとってのコマンドのようなもの**で、ユーザがエンドポイントにアクセスすると、特定のサービスが要求されたことをシステムに知らせる。

The domain in which the web framework operates is that of the HTTP protocol, so when the web framework has decoded the request it should pass the relevant information to another component that will process it.
ウェブ・フレームワークが動作するドメインはHTTPプロトコルのドメインなので、**ウェブ・フレームワークがリクエストをデコードしたら、それを処理する別のコンポーネントに関連情報を渡す必要がある**. (なるほど...web serverの一部=HTTPリクエストを受け取ってデコードする component が web framework なのかな...!)(ヘキサゴナルアーキテクチャの一番外側みたいなイメージ!)
This other component is called use case, and it is the crucial and most important component of the whole clean system as it implements the business logic.
この他のコンポーネントは **use case** と呼ばれ、**ビジネスロジックを実装する**ため、クリーンシステム全体の中でも重要で最も重要な component である. (=ヘキサゴナルアーキテクチャにおけるドメインモデル層的な?)

The business logic is an important concept in system design.
ビジネス・ロジックはシステム設計において重要な概念である。
You are creating a system because you have some knowledge that you think might be useful to the world, or at the very least marketable.
あなたがシステムを作っているのは、世の中の役に立つかもしれない、あるいは少なくとも市場価値があるかもしれないと思う知識があるからだ。
This knowledge is, at the end of the day, a way to process data, a way to extract or present data that maybe others don't have.
この知識は結局のところ、データを処理する方法であり、他の人が持っていないようなデータを抽出したり提示したりする方法なのだ。
A search engine can find all the web pages that are related to the terms in a query, a social network shows you the posts of people you follow and sorts them according to a specific algorithm, a travel company finds the best options for your journey between two locations, and so on.
検索エンジンは、クエリの用語に関連するすべてのウェブページを見つけることができる。ソーシャルネットワークは、あなたがフォローしている人々の投稿を表示し、特定のアルゴリズムに従ってそれらをソートする。
All these are good examples of business logic.
これらはすべてビジネスロジックの良い例である。

- Business logic ビジネスロジック(=usecase)
- Business logic is the specific algorithm or process that you want to implement, the way you transform data to provide a service.
- ビジネス・ロジックとは、**あなたが実装したい具体的なアルゴリズムやプロセス**であり、**データを変換してサービスを提供する方法**である。
- It is the most important part of the system.
- システムの中で最も重要な部分だ。

The use case implements a very specific part of the whole business logic.
ユースケースは、ビジネス・ロジック全体の非常に特定の部分を実装している。
In this case we have a use case to search for rooms with a given value of the parameter status.
この場合、パラメータ "status" に指定された値に応じて部屋を検索する usecase がある.
This means that the use case has to extract all the rooms that are managed by our company and filter them to show only the ones that are available.
つまり、ユースケースは自社が管理するすべての部屋を抽出し、利用可能な部屋だけを表示するようにフィルタリングしなければならない。

Why can't the web framework do it? Well, the main purpose of a good system architecture is to separate concerns, that is to keep different responsibilities and domains separated.
なぜウェブ・フレームワークはそれができないのか？**優れたシステム・アーキテクチャの主な目的は、関心事を分離すること**、つまり異なる責任とドメインを分離しておくことだ。
The web framework is there to process the HTTP protocol, and is maintained by programmers that are concerned with that specific part of the system, and adding the business logic to it mixes two very different fields.
**ウェブ・フレームワーク(flaskとかDjiangoとか?)はHTTPプロトコルを処理するために存在し**、システムのその特定の部分に関係するプログラマーによって維持されている。そこにビジネス・ロジックを加えることは、2つの全く異なる分野を混在させることになる.

- Separation of concerns 関心の分離
- Different parts a system should manage different parts of the process.
- システムはプロセスの異なる部分を管理しなければならない。
- Whenever two separate parts of a system work on the same data or the same part of a process they are coupled.
- システムの2つの異なる部分が同じデータ、あるいはプロセスの同じ部分で動作する場合、それらは常に結合している。
- **While coupling is unavoidable, the higher the coupling between two components the harder is to change one without affecting the other.**
- カップリングは避けられないが、2つのコンポーネント間のカップリングが高ければ高いほど、もう一方に影響を与えずに一方を変更するのは難しくなる。

As we will see, separating layers allows us to maintain the system with less effort, making single parts of it more testable and easily replaceable.
後述するように、レイヤーを分離することで、より少ない労力でシステムを維持することができる。

In the example that we are discussing here, the use case needs to fetch all the rooms that are in an available state, extracting them from a source of data.
ここで説明する例では、usecase は、利用可能な状態にあるすべての部屋を取得し、データソースから抽出する必要があります。
This is the business logic, and in this case it is very straightforward, as it will probably consist of a simple filtering on the value of an attribute.
これはビジネスロジックであり、この場合、おそらく属性値に対する単純なフィルタリングで構成されるため、非常に簡単です。
This might however not be the case.
しかし、そうではないかもしれない。
An example of a more advanced business logic might be an ordering based on a recommendation system, which might require the use case to connect with more components than just the data source.
より高度なビジネス・ロジックの例としては、推薦システムに基づく注文があるかもしれない。

So, the information that the use case wants to process is stored somewhere.
つまり、**usecase が処理したい情報はどこかに保存されている**。
Let's call this component storage system.
このコンポーネントを **storage system** と呼ぼう。
Many of you probably already pictured a database in your mind, maybe a relational one, but that is just one of the possible data sources.
おそらく多くの人は、すでに頭の中にデータベースを思い浮かべていることだろう。リレーショナル・データベースかもしれないが、それは可能なデータ・ソースのひとつに過ぎない.
The abstraction represented by the storage system is: anything that the use case can access and that can provide data is a source.
ユースケースがアクセスでき、データを提供できるものはすべてソースである。
It might be a file, a database (either relational or not), a network endpoint, or a remote sensor.
ファイル、データベース（リレーショナルかどうかは問わない）、ネットワーク・エンドポイント、リモートセンサーなども含まれる.

- Abstraction
- 抽象化
- When designing a system, it is paramount to think in terms of abstractions, or building blocks.
- システムを設計する際には、抽象化、つまりbuilding blocksで考えることが最も重要である.
- A component has a role in the system, regardless of the specific implementation of that component.
- **コンポーネントは、そのコンポーネントの具体的な実装に関係なく、システム内で役割を持っている**。
- The higher the level of the abstraction, the less detailed are the components.
- 抽象度が高ければ高いほど、コンポーネントの詳細度は低くなる。
- Clearly, high-level abstractions don't consider practical problems, which is why the abstract design has to be then implemented using specific solutions or technologies.
- 高水準の抽象化では現実的な問題を考慮しないのは明らかで、だからこそ抽象化された設計は、特定のソリューションやテクノロジーを使って実装されなければならない.

For simplicity's sake, let's use a relational database like Postgres in this example, as it is likely to be familiar to the majority of readers, but keep in mind the more generic case.
簡単のため、この例ではPostgresのようなリレーショナル・データベースを使うことにする。

How does the use case connect with the storage system?
**usecase と storage system はどのように接続するのか？**
Clearly, if we hard code into the use case the calls to a specific system (e.g.using SQL) the two components will be strongly coupled, which is something we try to avoid in system design.
明らかに、ユースケースに特定のシステム（例えばSQLを使う）への呼び出しをハードコードすれば、2つのコンポーネントは強く結合することになる.
Coupled components are not independent, they are tightly connected, and changes occurring in one of the two force changes in the second one (and vice versa).
カップリングされたコンポーネントは独立しているわけではなく、緊密に連結しており、2つのコンポーネントの一方に生じた変化は、もう一方のコンポーネントを変化させる（逆もまた然り）。
This also means that testing components is more difficult, as one component cannot live without the other, and when the second component is a complex system like a database this can severely slow down development.
これはまた、コンポーネントのテストが難しくなることを意味する。**一方のコンポーネントはもう一方のコンポーネントなしでは生きていけないから**だ。

For example, let's assume the use case called directly a specific Python library to access PostgreSQL such as psycopg.
例えば、**psycopgのようなPostgreSQLにアクセスするための特定のPythonライブラリを直接呼び出すuse case**を想定してみましょう.
This would couple the use case with that specific source, and a change of database would result in a change of its code.
これは、ユースケースとその特定のソースを結びつけることになり、データベースを変更すれば、そのコード(=use case component)も変更されることになる.
This is far from being ideal, as the use case contains the business logic, which has not changed moving from one database system to the other.
これは理想的とはかけ離れている. ユースケースにはビジネスロジックが含まれており、これはデータベースシステムを変えても変わらないからだ。(なので理想的にはDBを変えたことによるuse caseへの影響は存在すべきでない...!)
Parts of the system that do not contain the business logic should be treated like implementation details.
ビジネスロジックを含まないシステムの一部は、実装の詳細のように扱われるべきである.

- Implementation detail 実装の詳細
- (observable behavior(観察可能な振る舞い)の対義語的な認識:thinking:)
- A specific solution or technology is called a detail when it is not central to the design as a whole.
- 特定のソリューションやテクノロジーは、デザイン全体にとって中心的でない場合、 "detail" と呼ばれる。
- The word doesn't refer to the inherent complexity of the subject, which might be greater than that of more central parts.
- この言葉は、より中心的な部分よりも大きいかもしれない、対象が本来持っている複雑さを指しているのではない。

A relational database is hundred of times richer and more complex than an HTTP endpoint, and this in turn is more complex than ordering a list of objects, but the core of the application is the use case, not the way we store data or the way we provide access to that.
リレーショナル・データベースは、HTTPエンドポイントよりも何百倍もリッチで複雑であり、オブジェクトのリストを注文するよりも複雑である。しかし、アプリケーションの核心はユースケースであり、データを保存する方法や、それへのアクセスを提供する方法ではない。
Usually, implementation details are mostly connected with performances or usability, while the core parts implement the pure business logic.
通常、実装の詳細はパフォーマンスやユーザビリティに関係することが多く、コア部分は純粋なビジネスロジックを実装する。

How can we avoid strong coupling?
どうすれば強い結合を避けることができるだろうか？
A simple solution is called inversion of control, and I will briefly sketch it here, and show a proper implementation in a later section of the book, when we will implement this very example.
**簡単な解決策は、inversion of control(制御の反転)と呼ばれるもの**で、ここではそれを簡単にスケッチし、この本の後のセクションで、まさにこの例を実装する際に、適切な実装を示すことにする。(=要はcomponent間の依存関係の矢印の向きを厳密に定義するって事??:thinking:)

Inversion of control happens in two phases.
**Inversion of controlは2段階**で起こる.
First, the called object (the database in this case) is wrapped with a standard interface.
まず、呼び出されたオブジェクト(この場合はデータベース)を**標準インターフェースでラップする**。
This is a set of functionalities shared by every implementation of the target, and each interface translates the functionalities to calls to the specific language[3] of the wrapped implementation.
これは、ターゲット(=interfaceの継承先?)のすべての実装によって共有される functionalities の set (=実装が必要なfunction集合?)であり、各インターフェースは、ラップされた実装の特定の言語[3]への呼び出しに機能性を変換します。

- Inversion of control コントロールの逆転
- A technique used to avoid strong coupling between components of a system, that involves wrapping them so that they expose a certain interface.
- システムのコンポーネント間の強い結合を避けるために使われる手法で、**特定のinterfaceを公開するようにコンポーネントをラップする**。
- A component expecting that interface can then connect to them without knowing the details of the specific implementation, and thus being strongly coupled to the interface instead of the specific implementation.
- そのインターフェイスを期待する(i.e. 参照する)コンポーネントは、特定の実装の詳細を知ることなく、インターフェイスに接続することができる。それ故、実装の詳細の代わりにそのintefaceに強く結合する.

A real world example of this is that of power plugs: electric appliances are designed to be connected not with specific power plugs, but to any power plug that is build according to the specification (size, number of poles, etc).
電気製品は、特定の電源プラグではなく、仕様(サイズ、極数など)に従って作られた電源プラグに接続できるように設計されている. (わかりやすい例...!)
When you buy a TV in the UK, you expect it to come with a UK plug (BS 1363).
英国でテレビを購入する場合、UKプラグ（BS 1363）が付属していることを期待します。
If it doesn't, you need an adapter that allows you to plug electronic devices into sockets of a foreign nation.
そうでない場合は、電子機器を外国のソケットに接続するためのアダプターが必要だ。
In this case, we need to connect the use case (TV) to a database (power system) that have not been designed to match a common interface.
この場合、use case（テレビ）とデータベース（電力システム=use caseに入力する情報を用意するから.）を接続する必要があるが、これらは共通のインターフェースで設計されていない。

In the example we are discussing, the use case needs to extract all rooms with a given status, so the database wrapper needs to provide a single entry point that we might call list_rooms_with_status.
これから説明する例では、usecaseは指定されたステータスを持つすべての部屋を抽出する必要があるため、データベース・ラッパーは、 `list_rooms_with_status` と呼ばれる単一のエントリーポイントを提供する必要があります。

![](https://www.thedigitalcatbooks.com/images/pycabook/figure04.svg)

In the second phase of inversion of control the caller (the use case) is modified to avoid hard coding the call to the specific implementation, as this would again couple the two.
**inversion of control の第2段階**では、呼び出し側（use case）を修正し、特定の実装への呼び出しをハードコーディングしないようにする.
The use case accepts an incoming object as a parameter of its constructor, and receives a concrete instance of the adapter at creation time.
このuse caseは、**入力オブジェクトをコンストラクタのパラメータとして受け取り、作成時にアダプタの具象インスタンスを受け取ります**。(やっぱりconstructorで受け取る方法が一般的なのかな...!:thinking:)
The specific technique used to implement this depends greatly on the programming language we use.
これを実装するための具体的なテクニックは、使用するプログラミング言語に大きく依存する。
Python doesn't have an explicit syntax for interfaces, so we will just assume the object we pass implements the required methods.
**Pythonにはインターフェースのための明示的な構文がない**ので、渡すオブジェクトが必要なメソッドを実装していると仮定する.

![](https://www.thedigitalcatbooks.com/images/pycabook/figure05.svg)

Now the use case is connected with the adapter and knows the interface, and it can call the entry point list_rooms_with_status passing the status available.
これで、usecaseは adapter(=DB?) と接続され、インターフェイスを知ることができるようになり、利用可能なステータスを渡してエントリポイント `list_rooms_with_status` を呼び出すことができる.
The adapter knows the details of the storage system, so it converts the method call and the parameter in a specific call (or set of calls) that extract the requested data, and then converts them in the format expected by the use case.
**adapter は storage system の詳細を知っている**ので、メソッド呼び出しとパラメータを、要求されたデータを抽出する特定の呼び出し (または呼び出しのセット) に変換し、use caseで期待される形式に変換します。(adapter = storage system wrapper??:thinking:)
For example, it might return a Python list of dictionaries that represent rooms.
例えば、部屋を表す辞書のPythonリストを返すかもしれない。

![](https://www.thedigitalcatbooks.com/images/pycabook/figure06.svg)

At this point, the use case has to apply the rest of the business logic, if needed, and return the result to the web framework.
この時点で、ユースケースは必要に応じて残りのビジネスロジックを適用し、結果をウェブフレームワークに返さなければならない。

あ、これらの図って、依存関係の向きを表す図ではなくて、sequence図か!

![](https://www.thedigitalcatbooks.com/images/pycabook/figure07.svg)

The web framework converts the data received from the use case into an HTTP response.
ウェブ・フレームワークは、ユースケースから受け取ったデータをHTTPレスポンスに変換する。
In this case, as we are considering an endpoint that is supposed to be reached explicitly by the user of the website, the web framework will return an HTML page in the body of the response, but if this was an internal endpoint, for example called by some asynchronous JavaScript code in the front-end, the body of the response would probably just be a JSON structure.
この場合、ウェブサイトのユーザによって明示的に到達されるエンドポイントを考えているので、ウェブフレームワークはレスポンスのボディにHTMLページを返しますが、これが内部エンドポイントであった場合、例えばフロントエンドの非同期JavaScriptコードによって呼び出された場合、レスポンスのボディはおそらく単なるJSON構造になるでしょう.

![](https://www.thedigitalcatbooks.com/images/pycabook/figure08.svg)

## Advantages of a layered architecture¶ レイヤーアーキテクチャーの利点

As you can see, the stages of this process are clearly separated, and there is a great deal of data transformation between them.
ご覧のように、**このプロセスの段階は明確に分かれており、その間に多くのデータ変換がある**.
Using common data formats is one of the way we achieve independence, or loose coupling, between components of a computer system.
共通のデータ・フォーマットを使うことは、コンピュータ・システムのコンポーネント間の独立性、すなわち疎結合を実現する方法のひとつである.

To better understand what loose coupling means for a programmer, let's consider the last picture.
プログラマーにとって loose coupling(緩い結合) が何を意味するかをよりよく理解するために、最後の絵を考えてみよう。
In the previous paragraphs I gave an example of a system that uses a web framework for the user interface and a relational database for the data source, but what would change if the front-end part was a command-line interface? And what would change if, instead of a relational database, there was another type of data source, for example a set of text files?
前の段落では、**ユーザ・インターフェースにウェブ・フレームワークを使い**、**データ・ソースにリレーショナル・データベースを使う**システムの例を挙げた。しかし、もしフロントエンド部分を command-line interface だったとすると、何が変わるだろう?? また、リレーショナル・データベースの代わりに別のタイプのデータ・ソース、例えばテキスト・ファイルのセットがあったらどうなるだろうか？

![](https://www.thedigitalcatbooks.com/images/pycabook/figure09.svg)

![](https://www.thedigitalcatbooks.com/images/pycabook/figure10.svg)

As you can see, both changes would require the replacement of some components.
おわかりのように、**どちらの変更もいくつかの部品の交換が必要になる。**
After all, we need different code to manage a command line instead of a web page.
結局のところ、ウェブページではなくコマンドラインを管理するには、別のコードが必要なのだ。
But the external shape of the system doesn't change, neither does the way data flows.
しかし、システムの外形は変わらず、データの流れ方も変わらない。
We created a system in which the user interface (web framework, command-line interface) and the data source (relational database, text files) are details of the implementation, and not core parts of it.
私たちは、**ユーザー・インターフェース（ウェブ・フレームワーク、コマンドライン・インターフェース）とデータ・ソース（リレーショナル・データベース、テキスト・ファイル）が実装の詳細であり、かつドメインコア部分(=use case部分)ではないシステム**を作成したとする.

The main immediate advantage of a layered architecture, however, is testability.
しかし、**レイヤーアーキテクチャーの主な利点は、テスト容易性**である。(古典派の定義による"良い単体テスト"を書きやすい...!:thinking:)
When you clearly separate components you clearly establish the data each of them has to receive and produce, so you can ideally disconnect a single component and test it in isolation.
コンポーネントを明確に分けることで、それぞれのコンポーネントが受け取るべきデータと生成すべきデータが明確になる。
Let's take the Web framework component that we added and consider it for a moment forgetting the rest of the architecture.
追加したウェブ・フレームワーク・コンポーネントを取り上げて、残りのアーキテクチャを少し忘れて考えてみよう。
We can ideally connect a tester to its inputs and outputs as you can see in the figure.
理想的には、図のようにテスターをその入力と出力に接続すればよい。

We know that the Web framework receives an HTTP request (1) with a specific target and a specific query string, and that it has to call (2) a method on the use case passing specific parameters.
Webフレームワークは、特定のターゲットと特定のクエリ文字列を持つHTTPリクエスト(1)を受け取り、特定のパラメータを渡すユースケースのメソッド(2)を呼び出さなければならないことがわかっています。
When the use case returns data (3), the Web framework has to convert that into an HTTP response (4).
ユースケースがデータを返すと(3)、ウェブフレームワークはそれをHTTPレスポンスに変換しなければならない(4)。
Since this is a test we can have a fake use case, that is an object that just mimics what the use case does without really implementing the business logic.
これはテストなので、偽のusecase(=テストダブル!)を持つことができる。つまり、ビジネスロジックを実際に実装することなく、usecaseが行うことを模倣したオブジェクトだ。
We will then test that the Web framework calls the method (2) with the correct parameters, and that the HTTP response (4) contains the correct data in the proper format, and all this will happen without involving any other part of the system.
そして、ウェブ・フレームワークが正しいパラメーターでメソッド(2)を呼び出し、HTTPレスポンス(4)が正しいフォーマットで正しいデータを含んでいることをテストする。

So, now that we had a 10,000 feet overview of the system, let's go deeper into its components and the concepts behind them.
さて、システムの概要を1万フィート（約1,000フィート）概観したところで、その構成要素と背後にあるコンセプトについてさらに深く掘り下げてみよう。
In the next chapter I will detail **how the design principles called "clean architecture" help to implement and use effectively concepts like separation of concerns, abstraction, implementation, and inversion of control**.
次の章では、**「クリーン・アーキテクチャ」と呼ばれる設計原則が、separation of concerns(関心の分離)、抽象化、実装、制御の逆転といった概念の実装と効果的な利用にどのように役立つか**を詳しく説明する。

- 1. I was inspired by the Sludge-O-Matic™ from Day of the Tentacle 1. 私は『デイ・オブ・ザ・テンタクル』のスラッジ・オーマティックにインスパイアされた。

- 2. There are many more layers that the HTTP request has to go through before reaching the actual web framework, for example the web server, but since the purpose of those layers is mostly to increase performances, I am not going to consider them until the end of the book. 2. HTTPリクエストが実際のウェブ・フレームワーク、例えばウェブ・サーバーに到達するまでに通過しなければならないレイヤーはもっとたくさんあるが、それらのレイヤーの目的はほとんどパフォーマンスを上げることなので、この本の最後まで考慮するつもりはない。

- 3. The word language, here, is meant in its broader sense. It might be a programming language, but also an API, a data format, or a protocol. 3. ここでは、言語という言葉はより広い意味で使われている。 それはプログラミング言語かもしれないし、APIかもしれないし、データフォーマットかもしれないし、プロトコルかもしれない。
