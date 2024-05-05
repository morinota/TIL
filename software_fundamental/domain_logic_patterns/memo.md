## refs:

- [ドメインロジックのパターンは、ドメインモデルだけなの？](https://masuda220.jugem.jp/?eid=319)
- [Catalog of Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/)
- [PoEAA Part 1 Chapter 2 Organizing Domain Logic](https://wand-ta.hatenablog.com/entry/2019/02/02/202542)

# ドメインロジックのパターン

## そもそもドメインロジックってなんだっけ?

- そもそもドメインロジック (ビジネスロジック, ビジネスプロセス)とは?
  - **特定のビジネスやプロダクト固有の問題の解決方法**を、ソフトウェアシステムに落とし込んだもの?
    - コアロジックと言い換えても良い?:thinking:
  - ex.
    - 在庫管理
    - 価格計算
    - ユーザ認証
- ドメインロジックでないロジックは??
  - -> アプリケーションサービスロジック
    - システムがスムーズに動作するためのコード?
- 一般的には、ユーザインターフェースやデータベース管理システムから分離して実装される。

## ドメインロジックの3パターン

- ドメインロジックをいい感じに設計・構成・実装するかに焦点を当てたアーキテクチャパターンが3種類ある。
  - 1. Domain Model (ドメインモデル)
  - 2. Transaction Script (トランザクションスクリプト)
  - 3. Table Module (テーブルモジュール)

なんとなくググってみてた印象:

- **実現したいビジネスロジックがシンプルであればTransaction Scriptパターン。ビジネスロジックが複雑であるほど、Table Moduleパターン -> Domain Modelパターンが有効になってくるのかも**...?:thinking:
- ただそもそも、3つの設計思想は排他的なものではなく、組み合わせて使うこともある??:thinking:

## パターン1. Domain Model (ドメインモデル)について

- 複雑なビジネスロジックを、オブジェクト指向の原則を使用して表現する設計パターン。
  - 実世界のビジネスEntityをクラスとして表現し、これらのクラス間で関係を定義する。
  - **ビジネスロジックをEntityクラスの操作としてカプセル化**し、実世界のビジネスオペレーションを直感的に反映する構造を持っている。
- うちの会社も、メインはこれかも...!
  - 「ドメインモデル + サービス層 + Repository」みたいな!
  - ex. 顧客登録のアプリケーションの例:
    - CustomerRegisterService クラス (UIとの境界に、薄いサービス層)
    - Customer クラス (ドメインオブジェクト)
    - CustomerRepositoryクラス (データアクセスとの境界、仮想のデータベース)

## パターン2. Transaction Script (トランザクションスクリプト)について

- **サービス層のクラスに、ドメインの知識、ビシネスルールを集めていくのがTransaction Scriptパターン**。

  - 上述した顧客登録のアプリケーションの例で言うと...
    - CustomerRegisterServiceクラスはそのままに、ここにビジネスの知識を書き込んでいく。
    - 純粋なデータの入れ物クラスとして、Customerクラスを使う手はあるかも。
      - ちゃんとしたTransaction Scriptパターンならば、必要なデータは、サービスクラス内のインスタンス変数として持つのかも。
    - データベースアクセスのロジックは、Transaction Script(=ドメインのロジック)とは分離しておきたいので、Repositoryパターンはそのまま使うのかも。
    - なので、**Transaction Scriptパターンでは以下の2クラス構成**になる。
      - CustomerRegisterServiceクラス(トランザクションスクリプト = ビジネスロジックが書き込まれたサービスクラス)
      - CustomerRepositoryクラス (データアクセスとの境界、仮想のデータベース)

### "Transaction"との関係性は??

- そもそも "Transaction"って?

  - **一連の操作が完全に完了するか、ダメだったら全く行われないように保証する**ための手法。
  - **Transactionが満たす4つの特性**(=ACID特性)。
    - Atomicity (原子性):
      - トランザクションは、全ての操作が完了するか、全く行われないかのどちらかであるかを保証する。一部だけが実行されることはない。
    - Consistency (一貫性):
      - トランザクションが成功した場合、データベースは一貫性のある状態を保つことを保証する。
    - Isolation (独立性):
      - 各transactionは他の同時実行transactionから独立して実行されることを保証する。
    - Durability (永続性):
      - transactionが成功した場合、その変更はデータベースに永続的に保存されることを保証する。システム障害が発生しても、この変更は失われない。
  - 上記の4つの特性により、Transactionという方法論は、アプリケーション上でデータを安全かつ正確に扱うことができる。

- Transaction Scriptは、ビジネスロジックを1つの手続き(Script)にまとめるアプローチ。
  - データを扱う際にTransactionの原理 (特にAtomicityとConsistency)を用いて、一連のビジネスロジックを安全に実行するための方法を提供する。
  - シンプルなアプリケーションであればあるほど、この手法は効果的。ビジネスロジックが一箇所に集中しているため、変更が容易。
  - 逆に、全てのビジネスロジックを単一のスクリプトにまとめるため、複雑なビジネスロジックを表現するのは難しい。スクリプトが肥大化して、条件分岐が多くなったりするから??

## パターン3. Table Module (テーブルモジュール)について

- **Repositoryクラスに、ドメインの知識、ビジネスルールを集めていくのがTable Moduleパターン**。
  - 顧客登録のアプリケーションの例で言うと...
    - CustomerRepositoryクラスに、ビジネスロジックを書き込んでいく。
    - なので、**Table Moduleパターンでは以下の1クラス構成**になる??
      - CustomerRepositoryクラス (データアクセスとビジネスロジックが書き込まれたクラス)
- (特定のDBテーブルに対するgateway的なクラスを作るのがTable Moduleパターン??:thinking:)

# でも結局はドメインモデル??

## データの入れ物はほしい

- どのパターンでも、実アプリケーションになれば、コード量が増え、変更も色々発生してくる。
- で、読みやすく、扱いやすいコードを目指してリファクタリングしていくとどうなるか??
  - -> **データの入れ物はほしい**
  - Transaction Scriptパターンでも、Table Moduleパターンでも、顧客を表すデータの入れ物は欲しくなる気がする。
- -> そうすると、個々のデータ毎の制約ルール(形式や値の範囲、ようはContract??)などやビジネスの知識は、データの入れ物の方に移動していくのかもしれない。
  - Transaction Scriptパターンの場合、登録サービスクラス(CustomerRegisterService)と変更サービスクラス(CustomerUpdateService)とで、そういった制約ルールのコードを重複させなくてすむので...!
- -> そんな感じで設計を改善していくと、単なるデータの入れ物クラスだったものが、ドメインオブジェクトとして成長していく。
  - なので、Transaction Scriptパターンをリファクタリングしていくと、ドメインモデルパターンと似ていくのかも...??

## データアクセスロジックの分離

- Transaction Scriptパターンでも、Table Moduleパターンでも、「ドメインの知識を表現してる箇所」と「データアクセスの手続き」はもちろん分離すべき。
  - そのほうが、コードの見通しが良くなるし、変更も簡単&安全になる。
- なので、Table Moduleパターンから「データアクセスの手続き」を外だしして、ドメインのロジックに抽象化していくと、結局こっちもドメインモデルパターンに近づいていくのかも...??

## ドメインモデルパターンだけじゃないけど、結局はドメインモデル??

Transaction Scriptパターンでも、Table Moduleパターンでも、

- 関心の分離
- カプセル化
- 変更の影響範囲の局所化

などの設計原則を追いかけてリファクタリングしていくと、

- 関連するデータ
- 関連するロジック

を、いい感じに凝集したドメインオブジェクトが増え、ドメインモデルパターンとして成長していくのかもしれない。
最初はTransaction ScriptパターンやTable Moduleパターンでドメインロジックを表現していても、ソフトウェアを改良しながら育てていくと、結局ドメインモデルパターンに近づいていくのかもしれない。

# Service Layerについて

## 一般的なアプリケーションのレイヤー構成

- Presentation Layer: インターフェース的なもの。
- Domain Layer: ビジネスロジックを表現する。
- Data Source Layer: データベースアクセスを表現する。

## Service Layerの役割って??

ドメイン層(Domain Layer)を更に2分割することは一般的。

- 上: Service Layer
- 下: Domain Model, Table Module
- Transaction Scriptを適用すべき単純なケースでは、そもそも分割する必要はなさそう。
  - といいつつ、データの入れ物としてdomain objectが使われる場合は、Service layer (Transaction Script)と simple domain object (Table Module)に分割され得る。

その場合、**Service LayerとDomain Model(or Table Module)のように分割されがち**。

Service Layerの役割ってどんな感じ? どこまで仕事させる?? これは設計思想による!

- 1. 仕事させないver. (Facade):
  - domain model や table module に対する操作を単純に呼び出すだけ。
  - Transactionの性質を満たすための操作、セキュリティチェックでWrapするなど。
- 2. 仕事させるver. (Transaction Script):
  - Service Layer内にTransaction Scriptをガリガリ書く!
  - 下側の層は簡素なデータの入れ物になる。
  - (もう少し作り込んで) Domain Modelチックにするとしても、1つのDBのレコードに1つのdomain modelが紐づくような、単純なActive Recordになる。
    - Active Record = データベースのテーブルに対応するクラスが、そのテーブルの行を表すオブジェクトとして振る舞うような感じ...??:thinking:
    - (ビジネスロジックの多くはService Layerにあるってことか...!:thinking:)
    - (うちの場合は割とこっちっぽい...??:thinking:)
- 3. その中間ver. (controller-entityスタイル!):
  - (たぶん、**上層と下層の両方にビジネスロジックを分散させてる様な設計**!!)
  - 上層のService Layerは、**controller (use-case controller)**として機能する。
    - 単一のビジネストランザクションや特定のusecase特有のビジネスロジックをTransaction Scriptとして実装する。
  - 下層はentity = Domain Model(Acitive Record)として機能する。
    - 複数のusecaseで共通のビジネスロジックはこちらで表現される。
