## これは何?

- StrategyパターンとTemplate Methodパターンについて整理したメモ。

## refs

- ロバストPython
- [【Strategyパターン】すべての開発者が知っておくべき強力なツール](https://qiita.com/hankehly/items/1848f2fd8e09812d1aaf)
- [Template MethodパターンとStarategyパターンについて](https://bmf-tech.com/posts/Template%20Method%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3%E3%81%A8Starategy%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6#:~:text=b.Play()%20%7D-,Strategy%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3%E3%81%A8%E3%81%AF,%E4%BB%96%E3%81%8C%E5%8F%AF%E5%A4%89%E3%81%A8%E3%81%84%E3%81%A3%E3%81%9F%E3%82%A4%E3%83%A1%E3%83%BC%E3%82%B8%E3%80%82)


## ざっくりStrategyパターンとTemplate Methodパターンの比較

- どちらのパターンも、プログラムを **composable(コンポーザブル、組み合わせ可能)** で **plugable(プラガブル、差し替え可能) にするためのデザインパターン**の一種。
- Strategyパターンの構造:
  - 共通のinterfaceを持つ複数のstrategyクラス + strategyを渡すcontextクラス。
- Template Methodパターンの構造:
  - 処理の骨組み(i.e. テンプレート)を定義した抽象クラス + 具体的な処理の中身をorgverrideする具体クラス。

# Strategy パターン

- Strategyパターンとは??
  - プログラムを **composable(組み合わせ可能)** で **plugable(差し替え可能)** にするためのデザインパターンの1つ。
- 概要
  - **同じinterfaceを実装する (i.e. 同じinterfaceを継承してる) 交換可能な(plugableな)「アルゴリズム」**をいくつか定義して、プログラム実行時に適切なアルゴリズムを選択する。
    - ここでの「アルゴリズム」の意味合いは「複数あるやり方のうちの、1つのやり方」的なニュアンス...! (アルゴリズムが"Strategy"ってこと??:thinking:)
    - ex.) ファイルをアップロードする機能の場合、S3にアップロードするか、GCSにアップロードするか、あるいはローカルファイルシステムの`/mnt`ディレクトリに書き込むか。この場合、それぞれの方法を「アルゴリズム」と見做す。
  - 実際にアルゴリズムを使うのが「コンテキスト」と呼ばれるクラス。
    - コンテキストクラスの初期化時にアルゴリズムオブジェクトを渡して、インスタンス変数に保存する。
    - このような「コンテキストがアルゴリズムを持つ」関係を、**コンポジション(Composition)**と呼ぶ。

```python:context.py
class Context:
    # Contextクラスのconstructにstrategy(アルゴリズム?)を渡して、インスタンス変数に保存
    def __init__(self, strategy):
        self.strategy = strategy

    def upload(self):
        # コンテキストはstrategy(アルゴリズム)のメソッドを呼ぶ。
        # (コンテキストは、どのアルゴリズムを持ってるかは知る必要がない -> plugable!!)
        self.strategy.upload()
```

エントリーポイントから例えば以下のように実行できる。

```python:app.py
if url.startswith("s3://"):
    context = Context(strategy=S3())
elif url.startswith("gs://"):
    context = Context(strategy=GoogleCloudStorage())
else:
    context = Context(strategy=LocalStorage())
```

## Strategyパターンはいつ使う？？

以下のような場合に使うことが多い:

- 1. いくつかの関連しているアルゴリズムの「やること」が同じで「やり方」だけ違う時
  - ex.) MLモデルを、RandomForest で作っても DeepLearning で作っても「モデルを作っている」という観察可能な振る舞い(i.e. observable bahavior)は同じ。異なるのは、学習/予測のアルゴリズム(i.e. 実装の詳細??:thinking:)だけ。
- 2. ディスク容量、実行時間、ネットワーク速度のような物理的制限を考慮して実装する時
  - ex.) ネットワークが遅い時は、画像の画質を多少落として送信すると、ファイルサイズが小さくなるのでもっと早く送信できる。**Strategyパターンで、動的に「ネットワーク速度」に応じて「画像を送信するアルゴリズム」を入れ替えることができる**。
    - (なるほど、こういう使い方は意識してなかった)
- 3. メソッドの振る舞いを if/else で分岐して実装している時
  - if/else の分岐条件をそれぞれ「アルゴリズム(i.e. strategy?)」として切り離して実装すると、if/else が少なくなり、実装したアルゴリズムを他のところで再利用できる。

## Strategyパターンの構造

以下の3つのメンバーで構成されている:

- 1. Strategy
  - アルゴリズムが実装する、共通のinterface
- 2. ConcreteStrategy
  - Strategy interfaceの実装クラス (ex. RandomForest, LinearRegression)
- 3. Context
  - ConcreteStrategyをインスタンス変数として持つクラス (Composition)
  - ConcreteStrategyのメソッドを呼ぶことで、一部の処理を委託する。
    - (全アルゴリズムで共通の処理は、Contextクラスに実装する??:thinking:)


こんなイメージ!

```python
import abc


class Strategy(abc.ABC):
    """
    アルゴリズム（ConcreteStrategy）が実装する共通のインターフェイス
    """
    @abc.abstractmethod
    def operation(self):
        pass


class ConcreteStrategyA(Strategy):
    """
    Strategy インターフェイスを実装するクラス
    """
    def operation(self):
        print("A")


class Context:
    """
    ConcreteStrategy をインスタンス変数として持つクラス
    """
    def __init__(self, strategy: Strategy):
        # Strategyインターフェースを引数として指定することで、Contextからアルゴリズムの実装の詳細を隠蔽している。後からアルゴリズムが増えてもContextのコードを修正する必要はない。
        self.strategy = strategy

    def operation(self):
        # ConcreteStrategy のメソッドを呼ぶことで、一部の処理を委託する
        self.strategy.operation()


context = Context(strategy=ConcreteStrategyA())
context.operation()
```

- Strategyパターンを採用することで...
  - アルゴリズムとコンテキスト を分離でき、それぞれの役割が明確になる。
  - アルゴリズムを交換できる(plugable)ので、コンテキストのコードを変更しなくても、多様なパターンに対応させやすくなる。

# Template Method パターン

- Template Methodパターンの特徴
  - アルゴリズムの骨組み(テンプレート)を抽象クラスで定義し、具体的な処理はサブクラスで実装する。
    - 抽象クラス(i.e. テンプレート) = 処理の流れ、骨組みを定義
    - 具体クラス = 必要な処理をoverrideして実装
