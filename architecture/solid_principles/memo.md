## Link

- https://qiita.com/baby-degu/items/d058a62f145235a0f007

# SOLID Principles

## S(Single Responsibility) 単一責任の原則:

- クラスに多くの責任があると、バグが発生する可能性が高くなる.
- なぜなら、その責任の1つに変更を加えると、知らないうちに他の責任に影響を与える可能性があるからである.
- この原則は、変更の結果としてバグが発生しても、他の無関係な動作に影響を与えないように、動作を分離することを目的としている.

## O(Open-Closed) オープン-クローズドの原則: 「**クラスは、拡張にはオープンで、変更にはクローズドであるべきだ**」

- クラスの現在の動作を変更すると、そのクラスを使用するすべてのシステムに影響を与える.
- クラスでより多くの関数を実行したい時、理想的な方法は、既存の関数に追加することであり、変更しない事である.
- この原則は、**クラスの既存の動作を変更することなく、クラスの動作を拡張すること**を目的としている. これは、そのクラスが使用されている場所でバグが発生するのを避けるためである.

## L(Liskov Substitution) リスコフの置換原則: 「SがTのサブタイプである場合、プログラム内のT型のオブジェクトをS型のオブジェクトに置き換えても、そのプログラムの特性は何も変わらない.」

- 子クラスが親クラスと同じ動作を実行できない場合、バグになる可能性がある.
- 子クラスは、**親クラスと同じリクエストを処理し、同じ結果か、同様の結果を提供できなければならない**.
  - ex) このイラストでは、親クラスがコーヒーを提供しています（コーヒーの種類は問いません）
  - 子クラスがカプチーノを提供することは、カプチーノがコーヒーの一種なので許容されます. しかし、水を提供することは許容されません。(子クラスが拡張しすぎ??)
- この原則は、親クラスやその子クラスがエラーなしで同じ方法で使用できるように、**一貫性を保つこと**を目的としている.

## I(Interface Segregation) インターフェース分離の原則

「クライアントが使用しないメソッドへの依存を、強制すべきではない。」

この原則は、**動作のセットをより小さく分割して、クラスが必要なもののみを実行すること**を目的としている.

## D(Dependency Inversion) 依存性逆転の原則

「上位モジュールは下位モジュールに依存してはならない.どちらも抽象化に依存すべきだ.」
「抽象化(Interfaceクラス?)は詳細(implementedクラス?)に依存してはならない. 詳細が抽象化に依存すべきだ.」(そりゃそうだ...!!)

以下、上で使用されている用語の簡単な定義:

- 上位(high-level)モジュール（またはクラス）：ツールを使って動作を実行するクラス
- 下位(low-level)モジュール（またはクラス）：動作を実行するために必要なツール
- 抽象化：2つのクラスをつなぐインターフェース.
- 詳細：ツールの動作方法.(インターフェース ではない implemented クラスの事?)

クラスもInterfaceクラス も、詳細(implementedクラス)の動作方法を知るべきではない.
一方で詳細(implementedクラス)は、抽象化(Interfaceクラス)の仕様を満たす必要がある.(i.e. implementedクラスはinterfaceクラスに依存している.)

目的: この原則は、**Interfaceを導入することにより**、上位レベルのクラスが下位レベルのクラスに依存するのを減らすことを目的としている.(あ、そもそもInterfaceを使いましょうって話?)