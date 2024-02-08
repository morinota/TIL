## link リンク

- https://syedhasan010.medium.com/pipe-and-filter-architecture-bd7babdb908 https://syedhasan010.medium.com/pipe-and-filter-architecture-bd7babdb908

# Pipe and Filter Architecture パイプとフィルターの構造

## Definition

定義

Pipe and Filter is another architectural pattern, which has independent entities called **filters** (components) which perform transformations on data and process the input they receive, and **pipes**, which serve as connectors for the stream of data being transformed, each connected to the next component in the pipeline.
パイプ・アンド・フィルターはもうひとつのアーキテクチャ・パターンであり、**filters（コンポーネント）**と呼ばれる独立したエンティティがあり、データに変換を行い、受け取った入力を処理する。そして、パイプは、変換されるデータのストリームのコネクタとして機能し、それぞれがパイプライン内の次のコンポーネントに接続される。

Many systems are required to transform streams of discrete data items, from input to output.
多くのシステムは、入力から出力まで、離散的なデータ項目のストリームを変換する必要がある。
Many types of transformations occur repeatedly in practice, and **so it is desirable to create these as independent, reusable parts, Filters.**
多くの種類の変換は、実際には繰り返し行われるため、独立した再利用可能なパーツ、フィルターとして作成することが望ましい。
(Len Bass, 2012)
(レン・バス、2012年）

## Description of the Pattern

パターンの説明

The pattern of interaction in the pipe-and-filter pattern is characterized by successive
パイプ・アンド・フィルター・パターンにおける相互作用のパターンは、次のような特徴を持っている。

transformations of streams of data.
データストリームの変換。
As you can see in the diagram, the data flows in one direction.
図を見てわかるように、データは一方向に流れる。
It starts at a data source, arrives at a filter’s input port(s) where processing is done at the component, and then, is passed via its output port(s) through a pipe to the next filter, and then eventually ends at the data target.
データソースから始まり、フィルタの入力ポートに到着し、そこでコンポーネントでの処理が行われ、出力ポートからパイプを経由して次のフィルタに渡され、最終的にデータターゲットで終了する。

A single filter can consume data from, or produce data to, one or more ports.
1つのフィルターが、1つ以上のポートからデータを消費したり、1つ以上のポートにデータを生成したりすることができる。
They can also run concurrently and are not dependent.
また、同時進行も可能で、依存関係もない。
The output of one filter is the input of another, hence, the order is very important.
あるフィルタの出力は別のフィルタの入力となるため、順序は非常に重要である。

A pipe has a single source for its input and a single target for its output.
パイプの入力ソースは1つで、出力ターゲットは1つである。
It preserves the sequence of data items, and it does not alter the data passing through.
データ項目の順序を保持し、通過するデータを変更することはない。

Advantages of selecting the pipe and filter architecture are as follows:
pipe and filterアーキテクチャを選択する利点は次のとおりである：

- Ensures loose and flexible coupling of components, filters.

  - コンポーネント、フィルター間の緩やかで柔軟なカップリングを保証する。

- Loose coupling allows filters to be changed without modifications to other filters.

  - ルースカップリングにより、他のフィルターに変更を加えることなくフィルターを交換することができる。

- Conductive to parallel processing.

  - 並列処理に適している。

- Filters can be treated as black boxes.
  フィルターはブラックボックスとして扱うことができる。
  Users of the system don’t need to know the logic behind the working of each filter.
  システムのユーザは、各フィルターの動作の背後にあるロジックを知る必要はない。

- Re-usability.
  再利用性。
  Each filter can be called and used over and over again.
  それぞれのフィルターは何度でも呼び出して使うことができる。

However, there are a few drawbacks to this architecture and are discussed below:
しかし、このアーキテクチャにはいくつかの**欠点**があり、以下に説明する：

- Addition of a large number of independent filters may reduce performance due to excessive computational overheads.
  独立したフィルターを多数追加すると、計算オーバーヘッドが多すぎて性能が低下する可能性がある。

- Not a good choice for an interactive system.
  インタラクティブなシステムには向かない。(これはbatchかonlineか、というよりは、対話的に何度もクライアントとやり取りするようなシステム、ようはサーバに向かないってこと? 高速って感じではないからかな??:thinking: onlineでもストリーミングpipelineは存在する気がするし?)

- Pipe-and-fitter systems may not be appropriate for long-running computations.
  pipe and fitter(=filterの誤り?)システムは、長時間実行される計算には適していないかもしれない。(なんで??)

## Applications of the Pattern

パターンの応用

In software engineering, a pipeline consists of a chain of processing elements (processes, threads, functions, etc.), arranged so that the output of each element is the input of the next.
ソフトウェア工学では、**パイプラインは処理要素 (processes, threads, functions, etc.) の連鎖であり、それぞれの要素の出力が次の要素の入力になるように配置されている**(Wiki、n.d.)。
(Wiki、n.d.）。

The architectural pattern is very popular and used in many systems, such as the text-based utilities in the UNIX operating system.
このアーキテクチャパターンは非常に人気があり、UNIXオペレーティングシステムのテキストベースのユーティリティなど、多くのシステムで使われている。
Whenever different data sets need to be manipulated in different ways, you should consider using the pipe and filter architecture.
異なるデータセットを異なる方法で操作する必要がある場合は、パイプとフィルター・アーキテクチャの使用を検討すべきである。
More specific implementations are discussed below:
より具体的な実装については後述する：

### 応用例1: Compilers: コンパイラー:

A compiler performs language transformation: Input is in language A and output is in language B.
コンパイラは言語変換を行う： 入力は言語Aで、出力は言語Bである。
In order to do that the input goes through various stages inside the compiler — these stages form the pipeline.
そのために、入力はコンパイラー内部でさまざまな段階を経て、パイプラインを形成する。
The most commonly used division consists of 3 stages: front-end, middle-end, and back-end.
最もよく使われる区分は3つのステージからなる： フロントエンド、ミドルエンド、バックエンド。(つまり filter数は3つ??)

The front-end is responsible for parsing the input language and performing syntax and semantic and then transforms it into an intermediate language.
フロントエンドは、入力言語を解析し、構文と意味論を実行し、それを中間言語に変換する。
The middle-end takes the intermediate representation and usually performs several optimization steps on it, the resulting transformed program in is passed to the back-end which transforms it into language B.
ミドルエンドは中間的な表現を受け取り、通常いくつかの最適化ステップを実行し、その結果変換されたプログラムはバックエンドに渡され、バックエンドはそれを言語Bに変換する。

Each level consists of several steps as well, and everything together forms the pipeline of the compiler.
各レベルもいくつかのステップから構成され、すべてを合わせてコンパイラのパイプラインを形成する。(あ、じゃあfilter数は必ずしも3つってわけではないのかも)

![working of a compiler](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*AvosU3Xbsa5ebVB5gLtxZw.png)

### 応用例2: UNIX Shell: UNIXシェル：

The Pipeline is one of the defining features of the UNIX shell, and obviously, the same goes for Linux, MacOS, and any other Unix-based or inspired systems.
パイプラインはUNIXシェルの特徴の1つであり、もちろん、Linux、MacOS、およびその他のUnixベースまたはインスパイアされたシステムにも同じことが言える。

- (メモ):
  - UNIX shellとは?
    - UNIXなどのOSで使われるcommand interpreterのこと。
  - **command interpreter**とは?
    - 利用者が打ち込む指令(command)を読み込み/解釈し、それに対応する動作を実行するプログラムのことを指す。
  - shell(殻)という名前の由来:
    - カーネル(OS)と利用者の中間に位置し、カーネルを包み込んでいることから、貝の殻(shell)になぞらえて名付けられた。
  - shellの活用法:
    - ユーザからのcommandを対話的に処理できる。
    - **shell scriptというファイルを作成することにより、一連の処理をbatch(i.e. 一括して連続的に) 実行できる**。(=なるほど、これがshell scriptなのか...!)
  - UNIX用のshellにはいくつか種類がある
    - Bourne shell, C shell, Korn shell, bash(Bourne Again SHell).

In a nutshell, it allows you to tie the output of one program to the input of another.
一言で言えば、**あるプログラムの出力を別のプログラムの入力に結びつけることができる**。
The benefit it brings is that you don’t have to save the results of one program before you can start processing it with another.
その利点は、あるプログラムの結果を保存してから別のプログラムで処理を始める必要がないことだ。
The long-term and even more important benefit is that it encourages programs to be small and simple.
長期的でさらに重要な利点は、小規模でシンプルなプログラムを奨励することだ。

There is no need for every program to include a word-counter if they can all be piped into wc.
すべてのプログラムがwc(word-counter)にパイプで渡されるため、それぞれのプログラムがワードカウンターを含める必要はない。
Similarly, no program needs to offer its own built-in pattern matching facilities, as it can be piped into grep.
同様に、grepにパイプで渡すことができるため、どのプログラムもそれ自身の組み込みのパターンマッチング機能を提供する必要はない。
(shellの`|`って、pipe & filter architectureにおけるpipeの意味だったんだ...!)

In the provided example, the input.txt is read and the output is then provided to grep as input which searches for the pattern “text” and then passes the results to sort, which sorts the results and outputs into the file, output.txt.
この例では、input.txtが読み込まれ、その出力が入力としてgrepに提供される。grepはパターン "text "を検索し、その結果をsortに渡し、sortは結果をソートしてoutput.txtに出力する。

```
cat input.txt | grep "text" | sort > output.txt
```

![example: pipelining in the UNIX shell](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*oer6RybDlSY81IlCulguZg.png)

References
参考文献

Len Bass, P.C. a. R. K., 2012. Software Architectures in Practice.3rd ed.
ソフトウェア・アーキテクチャの実践.第3版.

Wiki, n.d.Pipelining (Software).
Available at: https://en.wikipedia.org/wiki/Pipeline_(software)
