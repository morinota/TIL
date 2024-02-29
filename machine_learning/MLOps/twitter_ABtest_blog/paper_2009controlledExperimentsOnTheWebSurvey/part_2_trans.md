## refs

- https://ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf

# 5. Implementation architecture 実装アーキテクチャ

Implementing an experiment on a website involves three components.
ウェブサイトでの実験には、**3つのcomponent**が関わっている。
The first component is the randomization algorithm, which is a function that maps end users to variants.
**最初のコンポーネントはランダム化アルゴリズム**で、エンドユーザとvariantをマッピングする関数です。
The second component is the assignment method, which uses the output of the randomization algorithm to determine the experience that each user will see on the website.
第二のコンポーネントは、ランダム化アルゴリズムの出力を使用して、各ユーザがウェブサイトで見る体験を決定する**assignment method(割り当て方法)**です。
The third component is the data path, which captures raw observation data as the users interact with the website, aggregates it, applies statistics, and prepares reports of the experiment’s outcome.5
**第3の構成要素はdata path**で、ユーザがウェブサイトとやり取りする際に、生の観測データをキャプチャし、集計し、統計を適用し、実験の結果のレポートを準備します。

## 5.1. Randomization algorithm 無作為化アルゴリズム

Finding a good randomization algorithm is critical because the statistics of controlled experiments assume that each variant of an experiment is assigned a random sample of end users.
統制実験の統計は、実験の各バリアントがエンドユーザーのランダムサンプルを割り当てられることを前提としているため、**良い無作為化アルゴリズムを見つけることは非常に重要**である。
Randomization algorithms must have the following three properties to support statistically correct experiments (using the methodology presented above): 1.
統計的に正しい実験（上記の方法論を使用）をサポートするために、**ランダム化アルゴリズムは以下の3つの特性**を持っていなければならない：

- 1. End users must be equally likely to see each variant of an experiment (assuming a 50–50 split).
     **エンドユーザは、実験の各バリアントを見る可能性が等しくなければならない**（半々を想定）。
     There should be no bias toward any particular variant.
     特定のバリアントに対するバイアスがないようにする必要がある。
- 2. Repeat assignments of a single end user must be consistent; the end user should be assigned to the same variant on each successive visit to the site. 2.**一人のエンドユーザーの繰り返し割り当ては一貫していなければならない**。エンドユーザは、サイトを連続して訪問するたびに、同じバリアントに割り当てられるべきである。
     (エンドユーザの割り当ては一貫してなければならない、というのは、実験単位がユーザである場合だけの話なのかな...?? 実験単位が ユーザ/日 やユーザ/sessionの場合は??)
- 3. When multiple experiments are run, there must be no correlation between experiments. An end user’s assignment to a variant in one experiment must have no effect on the probability of being assigned to a variant in any other experiment.
     **複数の実験を実行する場合、実験間に相関がないことが必要**。エンドユーザが1つの実験でvariantに割り当てられた場合、他の実験でvariantに割り当てられる確率に影響を与えてはならない。

Randomization algorithms may optionally support the following two desirable properties: 4.
無作為化アルゴリズムは、任意で以下の2つの望ましい特性をサポートすることができる:

- 4. The algorithm may support monotonic ramp-up, meaning that the percentage of users who see a Treatment can be slowly increased without changing the assignments of users who were previously assigned to that Treatment.
     **アルゴリズムは、treatmentを見るユーザーの割合をゆっくりと増加させることができる**。これにより、以前にその処置に割り当てられていたユーザーの割り当てを変更することなく、処置を見るユーザーの割合をゆっくりと増加させることができる。
     Supporting this property allows the Treatment percentage to be slowly increased without impairing the user experience or damaging the validity of the experiment.
     このプロパティをサポートすることで、処置を見るユーザーの割合をゆっくりと増加させることができる。これにより、以前にその処置に割り当てられていたユーザーの割り当てを変更することなく、処置を見るユーザーの割合をゆっくりと増加させることができる。
- 5.The algorithm may support external control, meaning that users can be manually forced into and out of variants.
  アルゴリズムは、外部制御をサポートすることができる。つまり、ユ**ーザを手動でvariantに強制的に割り当てたり、割り当てを解除したりすることができる**。
  This property makes it easier to test the experimental site.
  この特性により、実験サイトのテストが容易になる。

The remainder of this section will only consider techniques that satisfy at least the first three properties.
このセクションの残りの部分では、少なくとも最初の3つの特性を満たす技術のみを考慮します。

### 5.1.1 Pseudorandom with caching キャッシュ付き擬似乱数

A standard pseudorandom number generator can be used as the randomization algorithm when coupled with a form of caching.
標準的な擬似乱数生成器は、キャッシュの形式と組み合わせてランダム化アルゴリズムとして使用することができる。
A good pseudorandom number generator will, by itself, satisfy the first and third requirements of the randomization algorithm.
**優れた擬似乱数生成器は、それ自体で乱数化アルゴリズムの第1と第3の要件を満たす**。

We tested several popular random number generators on their ability to satisfy the first and third requirements.
私たちは、いくつかの一般的な乱数ジェネレーターが第1と第3の要件を満たす能力をテストした。
We tested five simulated experiments against one million sequential user IDs, running chi-square tests to look for interactions.
100万人の連続したユーザIDに対して、5つの模擬実験を行い、相互作用を探すためにカイ二乗検定を行った。
We found that the random number generators built into many popular languages (for example, C#) work well as long as the generator is seeded only once at server startup.
多くの一般的な言語（例えば、C#）に組み込まれた乱数ジェネレーターは、サーバの起動時に一度だけseedを与える限り、うまく機能することがわかった。
Seeding the random number generator on each request may cause adjacent requests to use the same seed which may (as it did in our tests) introduce noticeable correlations between experiments.
各リクエストで乱数発生器にseedを与えると、隣接するリクエストが同じseedを使用する可能性があり、実験間で相関が生じる可能性がある（私たちのテストでは）。
In particular, we found that the technique employed by Eric Peterson using Visual Basic (Peterson 2005) creates two-way interactions between experiments.
特に Eric Peterson がVisual Basicを使用しているテクニックは、実験間で双方向の相互作用を生じさせることがわかった。

To satisfy the second requirement, the algorithm must introduce state: the assignments of end users must be cached once they visit the site.
**2つ目の要件を満たすためには、アルゴリズムはstateを導入する必要がある**：エンドユーザの割り当ては、サイトを訪れた時点でキャッシュされなければならない。(同一ユーザの同一variantへの割当の保証の話...!)
The caching can be accomplished either on the server side (by storing the assignments for all users in some form of database), or on the client side (by storing a user’s assignment in a cookie).
キャッシュは、サーバ側で（すべてのユーザの割り当てを何らかの形でデータベースに保存することによって）、またはクライアント側で（ユーザーの割り当てをクッキーに保存することによって）達成することができます。

The database approach is expensive (in hardware), and has space requirements that increase linearly with the number of experiments and the number of users.
データベース・アプローチは（ハードウェア的に）高価であり、実験数とユーザ数が線形に増加するスペース要件がある。
However, it easily satisfies the fifth property by allowing the user assignment database to be modified.
しかし、ユーザ割り当てデータベースを変更できるようにすることで、5つ目の特性を簡単に満たすことができる。
The cookie approach is significantly cheaper, requiring no database and costing only a linear amount of space in the number of experiments (this time within the user’s cookie).
クッキーのアプローチは、データベースを必要とせず、実験数に対して線形のスペースしか必要とせず、かなり安価である。
It will not work for users with cookies turned off.
クッキーをオフにしているユーザーには機能しません。

Both forms of this approach are difficult to scale up to a large system with a large fleet of servers.
このアプローチはどちらも、大規模なサーバ群を持つシステムにスケールアップするのは難しい。
The server making the random assignment must communicate its state to all the other servers (including those used for backend algorithms) in order to keep assignments consistent.
ランダム割り当てを行うサーバーは、割り当ての一貫性を保つために、その状態を他のすべてのサーバー(バックエンドアルゴリズムに使用されるサーバーを含む)に伝えなければならない。(ふむふむ...!user_idで固定してるケースは、つまり単一の外部DB使うのかな。)
This sort of propagation is expensive and difficult to implement correctly.
この種の伝搬は高価で、正しく実装するのは難しい。

The fourth requirement (monotonic ramp-up) is difficult to implement using this method, and so many systems ignore the requirement altogether.
第4の要件（単調なランプアップ）は、この方法では実装が難しいため、多くのシステムは要件を完全に無視している。
Regardless of which approach is used to maintain state, the system would need to carefully reassign Control users who visit the site after a ramp-up.
どのような方法で状態を維持するにしても、システムは、立ち上がり後にサイトを訪れたコントロールユーザーを注意深く再配置する必要がある。
The difficulty comes in determining the percentage Treatment to assign to these users so that the overall Treatment percentage reaches the desired value.
問題は、これらのユーザに割り当てるTreatmentの割合を決定することであり、全体のTreatmentの割合が目標の値に達するようにすることが難しい。

### 5.1.2 Hash and partition ハッシュとパーティション

This method eliminates the need for caching by replacing the random number generator with a hash function.
この方法は、**ランダム数生成器をハッシュ関数に置き換えることで、キャッシュの必要性を排除する**。(stateの保持が不要になる??)
Unlike a random number generator, which produces randomly distributed numbers independent of any input, a (good) hash function produces randomly distributed numbers as a function of a specific input.
どのような入力からも独立してランダムに分布する数値を生成する乱数生成器とは異なり、**(優れた)ハッシュ関数は特定の入力の関数としてランダムに分布する数値を生成する**。(なるほど...!)
The method works as follows: each user is assigned a single unique identifier which is maintained either through a database or a cookie.
この方法は次のように機能する: 各ユーザには、データベースまたはクッキーによって管理される一意の識別子が割り当てられる。
Likewise, each experiment is assigned a unique identifier.
同様に、各実験には固有の識別子が割り当てられる。
A hash function is applied to the combination of the user identifier and the experiment identifier (e.g.by concatenating them together) to obtain an integer that is uniformly distributed on a range of values.
**ハッシュ関数は、ユーザ識別子と実験識別子の組み合わせに適用され（例えば、それらを連結することによって）、値の範囲に一様に分布する整数を得る**。
The range is then partitioned, with each variant represented by a partition.
そして、各variantはパーティションで表されるように、範囲がパーティションされる。(つまり一様分布の中で、variantに割り当てる範囲を固定するってことか...!:thinking_face:)
The unique user identifier may be reused across any number of experiments.
一意のユーザ識別子は、任意の数の実験にわたって再利用することができる。(まさにuser_idか...!)

This method is very sensitive to the choice of hash function.
この方法は、ハッシュ関数の選択に非常に敏感である。
If the hash function has any funnels (instances where adjacent keys map to the same hash code) then the first property (uniform distribution) will be violated.
ハッシュ関数にファネル(隣接するキーが同じハッシュコードにマップされるインスタンス)がある場合、第1の特性(一様分布)が違反される。
And if the hash function has characteristics (instances where a perturbation of the key produces a predictable perturbation of the hash code), then correlations may occur between experiments.
また、ハッシュ関数に**特性(キーの摂動がハッシュコードの予測可能な摂動を生じる**インスタンス)がある場合、実験間で相関が生じる可能性がある。(うんうん...!)
Few hash functions are sound enough to be used in this technique.
**この手法に使えるほど健全なハッシュ関数はほとんどない**。(うん、そんな感じがする...!)

We tested this technique using several popular hash functions and a methodology similar to the one we used on the pseudorandom number generators.
我々は、いくつかの一般的なハッシュ関数と、擬似乱数ジェネレーターで使用した方法と同様の方法を用いて、このテクニックをテストした。
While any hash function will satisfy the second requirement (by definition), satisfying the first and third is more difficult.
**どんなハッシュ関数でも（定義上）2番目の要件は満たすが、1番目と3番目の要件を満たすのはより難しい**。(一方で疑似乱数ジェネレーターは、2番目の要件を満たすのに工夫が必要なんだよね...!:thinkinkg)
We tested five simulated experiments against one million sequential user IDs.
100万人の連続したユーザIDに対して、5つの模擬実験を行った。
We ran chi-square tests to look for violations of the first and third requirements of a randomization algorithm and found that only the cryptographic hash function MD5 generated no correlations between experiments.
無作為化アルゴリズムの第1と第3の要件に違反していないかどうかを調べるためにカイ二乗検定を行ったところ、**暗号ハッシュ関数MD5だけが実験間の相関を生じないことがわかった**。
SHA256 (another cryptographic hash) came close, requiring a five-way interaction to produce a correlation.
SHA256（別の暗号ハッシュ）は、相関を生じさせるために5つの相互作用が必要であった。(要は、頑張ったら要件を満たせたってこと??)
Other hash functions (including the string hashing algorithm built into .net) failed to pass even a two-way interaction test.
他のハッシュ関数（.netに組み込まれた文字列ハッシュアルゴリズムを含む）は、双方向の相互作用テストにさえ合格しなかった。(要はだめだったってことか?)

The running-time performance of the hash and partition approach is limited by the running-time performance of the hash function, which can be an issue because cryptographic hashes like MD5 are expensive and clever attempts to improve the performance through partial caching generally fail.
hash and partition法の実行時間の性能は、ハッシュ関数の実行時間の性能によって制限されるため、MD5のような暗号ハッシュは高価である。そして部分的なキャッシュを通じて性能(=実行時間)を向上させるための巧妙な試みは一般的に失敗することがある。
For example, one system attempted to compute separate hashes of both the experiment name and the end user which would then be XOR’d together.
例えば、あるシステムは、実験名とエンドユーザーのハッシュを別々に計算し、それをXOR結合しようとしていた。
(XOR=排他的論理和。ex. 2つのbit列の両者が同じ場合0, 異なる場合1 :thinking_face:)
The intent was to avoid the cost of MD5 by caching the hashed experiment name in the experiment, caching the hashed end user id in the user’s cookie, and executing only the final XOR at assignment time.
その意図は、ハッシュ化された実験名を実験にキャッシュし、ハッシュ化されたエンドユーザIDをユーザのクッキーにキャッシュし、割り当て時に最後のXORだけを実行することで、MD5のコストを回避することであった。(i.e. 高速化を測った。)
This technique produces severe correlations between experiments:
この技法は実験間に深刻な相関をもたらす：
assuming two experiments with two variants each running at 50/50, if the most significant bit of the hashes of the experiment names for two experiments matched, users would always get the same assignment across both experiments.
2つの実験が、それぞれ50/50で実行され2つのvariantがあると仮定すると、2つの実験名のハッシュの最上位ビットが一致した場合、ユーザは常に両方の実験で同じ割り当てを受けることになる。
If they did not match, users would get exactly the opposite assignment between experiments.
もし両者が一致しなければ、ユーザは実験間でまったく逆の割り当てを受けることになる。
Either way, the third property is violated and results of both experiments are confounded.
**いずれにせよ、3つ目の性質に違反し、両実験の結果は混乱する**。

Satisfying the fifth property (external control) is very difficult with a raw hash and partition approach.
第5の特性（外部からのコントロール）を満たすことは、生のハッシュとパーティションのアプローチでは非常に難しい。
The simplest way to satisfy this property is to use a hybrid approach, combining the hash and partition method with either a small database or limited use of cookies.
この特性を満たす最も簡単な方法は、hash and partition法を小規模データベースかクッキーの限定的な使用と組み合わせたハイブリッド・アプローチを使用することである。
Because the set of users subject to external control is typically small (e.g.users designed by a test team), this hybrid approach should not encounter the full disadvantages of the pseudorandom with caching technique.
外部制御の対象となるユーザの集合は一般的に小さいため（テストチームによって設計されたユーザーなど）、このハイブリッド・アプローチは、キャッシュ技法による疑似ランダムの完全な欠点に遭遇することはないはずである。

(こういうランダム化の難しさの話を聞くと、Multi variate testingにならないようにした方が良さそうって思っちゃうな...! でも前者の疑似乱数生成器のアプローチだと、相互作用問題は大丈夫なんだっけ??)

<!-- ここまで読んだ -->

## 5.2. Assignment method 割り当て方法

The assignment method is the piece of software that enables the experimenting website to execute a different code path for different end users.
割り当て方法は、実験サイトが**異なるエンドユーザに対して異なるコードパスを実行することを可能にする**ソフトウェアの一部である。(=要はvariantによって処理を切り替える仕組みが必要って話...??)
A good assignment method can manipulate anything from visible website content to backend algorithms.
**優れた割り当て方法は、目に見えるウェブサイトのコンテンツからバックエンドのアルゴリズムまで、あらゆるものを操作することができる**。(なるほど...!)
There are multiple ways to implement an assignment method.
割り当てメソッドを実装する方法は複数ある。
In the remainder of this section, we compare several common assignment methods and recommend best practices for their use.
このセクションの残りの部分では、いくつかの一般的な割り当て方法を比較し、それらの使用に関するベストプラクティスを推奨する。

### 5.2.1. Traffic splitting トラフィックの分割

![traffic splitting]()

Traffic splitting refers to a family of assignment methods that involve implementing each variant of an experiment on a different logical fleet of servers.
トラフィックの分割は、**実験の各variantを異なる論理フリートのサーバーに実装すること**を含む割り当て方法の一群を指す。(variant毎に別のサーバインスタンスにアクセスするってこと?)
These can be different physical servers, different virtual servers, or event different ports on the same machine.
これらは、異なる物理サーバ、異なる仮想サーバ、または同じマシン上の異なるポートの場合がある。
The website uses either a load balancer or proxy server to split traffic between the variants and the randomization algorithm must be embedded at this level.
ウェブサイトはロードバランサーかプロキシサーバーを使ってバリアント間でトラフィックを分割し、ランダム化アルゴリズムはこのレベルに組み込まれなければならない。
Traffic splitting has the advantage of being non-intrusive; no changes to existing code are required to implement an experiment.
トラフィックの分割は非侵入的であるという利点があり、実験を実施するために既存のコードを変更する必要はない。
However, the approach has significant disadvantages:
しかし、このアプローチには大きな欠点がある：

1. Running experiments on small features is disproportionately difficult because the entire application must be replicated regardless of the size of the change. 1.小さな機能で実験を実行する場合、**変更のサイズに関係なく、アプリケーション全体を複製する必要があるため、不釣り合いに難しい**。
2. 2.Setting up and configuring parallel fleets is typically expensive. 2.並列フリートの設定と構成には、通常コストがかかる。
   The Control fleet must have sufficient capacity to take 100% of the traffic in the event that the experiment needs to be shut down.
   コントロール・フリートは、実験がシャットダウンされる必要が生じた場合、トラフィックの100％を引き受けるのに十分な容量を持っていなければならない。
   The Treatment fleet(s) may be smaller, but their size will limit the maximum percentage that may be assigned to each Treatment.
   Treatmentフリートは小さくてもよいが、そのサイズによって、各Treatmentに割り当てられる最大パーセンテージが制限される。
3. Running multiple experiments requires the fleet to support one partition for each combination of variants across all experiments. 3.複数の実験を実行するには、すべての実験にわたって、variantのすべての組み合わせに対して1つのパーティションをサポートする必要がある。
   This number increases as the number of tested combinations increases (potentially exponentially in the number of simultaneous experiments).
   この数は、テストされる組み合わせの数が増加するにつれて増加する（同時実験の数に応じて指数関数的に増加する可能性がある）。
4. Any differences between the fleets used for each variant may confound the experimental results.
   各バリアントに使用されるフリート間の違いは、実験結果を混乱させる可能性がある。
   Ideally, the hardware and network topology of each fleet will be identical and A/A tests will be run to confirm the absence of fleet-related effects.
   理想的には、各フリートのハードウェアとネットワーク・トポロジーは同一とし、A/Aテストを実施して、フリート関連の影響がないことを確認する。

The drawback of traffic splitting is that it is an expensive way to implement an experiment, even though the method appears cheap because it minimizes IT/developer involvement.
トラフィック分割の欠点は、IT/開発者の関与を最小限に抑えるため、安価に見えるものの、実験を実施するための高価な方法であるということです。
We recommend this method for testing changes that introduce significantly different code, such as migration to a new website platform, the introduction of a new rendering engine, or a complete upgrade of a website.
新しいウェブサイト・プラットフォームへの移行、新しいレンダリング・エンジンの導入、またはウェブサイトの完全なアップグレードなど、**大幅に異なるコードを導入する変更をテストするためにこの方法を推奨**します。
(ex. EC2で動いてたサーバをECSに移行する場合とか...!)

<!-- ここまで読んだ! -->

### 5.2.2. Page rewriting ページの書き換え

Page rewriting is an assignment method that incorporates a special type of proxy server that modifies HTML content before it is presented to the end user.
ページ書き換えは、エンドユーザーに提示される前にHTMLコンテンツを修正する**特殊なタイプのproxyサーバ(=代理サーバ)**を組み込んだ割り当て方法である。
Using this approach, the end-user’s browser sends a request to the proxy server, which forwards it on to the experimenting website after recording some data.
このアプローチでは、エンドユーザのブラウザはproxyサーバにリクエストを送信し、一部のデータを記録した後、実験用ウェブサイトに転送される。
Then, the HTML response from the experimenting website passes back through the proxy server on its way to the end user’s browser.
そして、実験用ウェブサイトからのHTMLレスポンスは、エンドユーザーのブラウザに届く途中でproxyサーバを通過する。
The proxy server applies the randomization algorithm, selects variants for one or more experiments, and modifies the HTML according to the selected variants (e.g.by applying substitution rules expressed as regular expressions or XPath queries).
プロキシサーバはランダム化アルゴリズムを適用し、1つ以上の実験に対してvariantを選択し、**選択されたvariantに従ってHTMLを修正する**（例えば、正規表現やXPathクエリとして表現された置換ルールを適用する）。
The server then sends the modified HTML to the end user’s browser.
その後、proxyサーバは修正されたHTMLをエンドユーザのブラウザに送信する。
At least one commercial provider (SiteSpect 2008) offers a solution based on this method.
少なくとも1つの商用プロバイダー（SiteSpect 2008）は、この方法に基づいたソリューションを提供している。
Like traffic splitting, this method is non-intrusive.
traffic splittingと同様に、この方法はnon-intrusiveである。(non-intrusiveってなんだっけ??)
However, it still incurs some disadvantages:
しかし、それでもいくつかの欠点がある：

1. Page render time is impacted by the action of the proxy server.
   ページのレンダリング時間は、proxyサーバの動作によって影響を受ける。
   Render time will be affected by both the time required to rewrite the HTML and the network latency between the proxy server and the web server.
   レンダリング時間は、HTMLの書き換えに要する時間と、proxyサーバとウェブサーバとのネットワークの遅延の両方に影響を受ける。
2. Experimentation on large sites requires significant hardware.
   大規模なサイトでの実験には、かなりのハードウェアが必要となる。
   Because the proxy servers both need to handle all potential traffic to the site and may become a point of failure, a large number of servers may be required to ensure scalability and availability of the website.
   **proxyサーバはサイトへのすべての潜在的なトラフィックを処理する必要があり**、障害の原因となる可能性があるため、ウェブサイトの拡張性と可用性を確保するためには多数のproxyサーバが必要となる場合がある。
3. Development and testing of variant content is more difficult and more error-prone than with other methods. Each variant must be expressed as a set of rules for modifying HTML code rather than as the HTML code itself.
   variantコンテンツの開発とテストは、他の方法よりも難しく、エラーが起こりやすい。各variantは、HTMLコードそのものではなく、HTMLコードを修正するためのルールセットとして表現する必要がある。(確かに...!難しそう)
4. Running experiments on backend algorithms is difficult because the assignment decision is made after the page is rendered by the website.
   バックエンドのアルゴリズムで実験を行うことは困難である。なぜなら、ウェブサイトがページをレンダリングした後に割り当ての決定が行われるからだ。(フロントエンドの実験限定のアプローチなのか)
5. Running experiments on encrypted traffic (in particular, pages served via https) is resource-intensive because the proxy server must decrypt, modify, and re-encrypt the content.
   暗号化されたトラフィック（特にhttps経由で提供されるページ）で実験を実行することは、リソースを多く必要とする。なぜなら、proxyサーバはコンテンツを復号し、(variant毎にHTMLを)修正し、再度暗号化する必要があるからだ。
   This represents a significant problem because the most interesting parts of a website (such as the checkout page) are commonly encrypted.
   これは大きな問題を表している。なぜなら、ウェブサイトの最も興味深い部分（チェックアウトページなど）は一般的に暗号化されているからだ。

Page rewriting can be a cheap method for experimenting on front-end content because it minimizes IT/developer involvement.
ページの書き換えは、IT/開発者の関与を最小限に抑えるため、**フロントエンドのコンテンツを実験するための安価な方法**となる。
However, it is not appropriate for testing backend changes or platform migrations.
しかし、バックエンドの変更やプラットフォームの移行をテストするには適していない。

<!-- ここまで読んだ! -->

### 5.2.3. Client-side assignment クライアント側の割り当て

Client-side page modification is the most popular assignment method found in third-party experimentation platforms.
クライアント側のページ修正は、サードパーティの実験プラットフォームに見られる最も一般的な割り当て方法である。
It is supported by numerous products including Google Website Optimizer (2008), Omniture’s Offermatica (Omniture 2008), Interwoven’s Optimost (2008), Widemile (2008), and Verster (2008).
Google Website Optimizer (2008), Omniture's Offermatica (Omniture 2008), Interwoven's Optimost (2008), Widemile (2008), Verster (2008) など数多くの製品でサポートされている。
All of these products can run an experiment without making any decisions on the server.
これらの製品はすべて、サーバー上で何も決定することなく実験を実行することができる。
A developer implements an experiment by inserting JavaScript code that instructs the end user’s browser to invoke an assignment service at render time.
開発者は、レンダリング時に割り当てサービスを呼び出すようエンドユーザーのブラウザに指示するJavaScriptコードを挿入することで、実験を実施する。
The service call returns the appropriate variant for the end user, and triggers a JavaScript callback that instructs the browser to dynamically alter the page being presented to the user, typically by modifying the DOM.
サービスコールはエンドユーザーに適切なバリアントを返し、JavaScriptのコールバックをトリガーして、ユーザーに表示されるページを動的に変更するようにブラウザに指示します。
The modification must occur before any part of the page renders, so any latency in the service call will add to the overall page render time.
修正はページのどの部分がレンダリングされる前にも行わなければならないので、サービス呼び出しの待ち時間はページ全体のレンダリング時間に追加される。
The content for each variant can either be cleverly embedded into the page or can be served by the assignment service.
各バリアントのコンテンツは、ページに巧妙に埋め込むか、割り当てサービスによって提供することができます。
This method, although intrusive, can be very easy to implement: all the developer needs to do is add a small snippet of JavaScript to a page.
この方法は押しつけがましいが、実装は非常に簡単だ： 開発者がすべきことは、JavaScriptの小さなスニペットをページに追加することだけだ。
However, it has some key limitations: 1.
しかし、これにはいくつかの重要な限界がある： 1.
The client-side assignment logic executes after the initial page is served and therefore delays the end user experience, especially if the assignment service gets overloaded or if the end user is on a slow connection or is located far from the assignment server.2.The method is difficult to employ on complex sites that rely on dynamic content because complex content can interact with the JavaScript code that modifies the page.3.End users can determine (via the browser’s View Source command) that a page is subject to experimentation, and may even (in some implementations) be able to extract the content of each variant.
クライアント側の割り当てロジックは、最初のページが提供された後に実行されるため、特に割り当てサービスが過負荷になったり、エンドユーザーが遅い接続を使用していたり、割り当てサーバーから遠く離れた場所にいる場合、エンドユーザーのエクスペリエンスが遅れます。2.複雑なコンテンツがページを修正するJavaScriptコードと相互作用する可能性があるため、動的コンテンツに依存する複雑なサイトでこの方法を採用するのは困難です。3.エンドユーザーは、ページが実験対象であることを（ブラウザのView Sourceコマンドを介して）判断でき、（実装によっては）各バリアントのコンテンツを抽出することさえできます。
Note: some implementations of this method attempt to optimize render time by avoid the service call if the end user is known (via cookie) to be in the Control.
注意 このメソッドのいくつかの実装は、エンドユーザが(クッキーを介して)コントロール内にいることが分かっている場合、サービスコールを回避することによってレンダリング時間を最適化しようとします。
This optimization is incorrect (and should not be used) because it causes the render time delay to become correlated with variant assignment, thereby adding a confounding factor to the experiment.
この最適化は、レンダリング時間の遅延がバリアントの割り当てと相関を持つようになり、実験に交絡因子を追加することになるため、正しくない（使うべきではない）。
This method is best for experiments on front-end content that is primarily static.
この方法は、主に静的なフロントエンド・コンテンツの実験に最適である。

### 5.2.4. Server-side assignment サーバー側の割り当て

Server-side assignment refers to a family of methods that use code embedded into the website’s servers to produce a different user experience for each variant.
サーバーサイド・アサインとは、ウェブサイトのサーバーに埋め込まれたコードを使用して、バリアントごとに異なるユーザーエクスペリエンスを提供する一連の方法を指します。
The code takes the form of an API call placed at the point where the website logic differs between variants.
コードは、ウェブサイトのロジックがバリアント間で異なる箇所に配置されたAPIコールの形をとります。
The API invokes the randomization algorithm and returns the identifier of the variant to be displayed for the current user.
APIは無作為化アルゴリズムを起動し、現在のユーザーに表示されるバリアントの識別子を返す。
The calling code uses this information to branch to a different code path for each variant.
呼び出しコードはこの情報を使って、バリアントごとに異なるコード・パスに分岐する。
The API call can be placed anywhere on the server side, in front-end rendering code, back-end algorithm code, or even in the site’s content-management system.
APIコールは、フロントエンドのレンダリングコード、バックエンドのアルゴリズムコード、あるいはサイトのコンテンツ管理システムなど、サーバーサイドのどこにでも置くことができる。
A complex experiment may make use of multiple API calls inserted into the code at different places.
複雑な実験では、コードに挿入された複数のAPIコールをさまざまな場所で利用することがある。
While the API can be implemented as a local function call, it typically uses an external service to ensure that the assignment logic stays consistent across a large server fleet.
APIはローカル関数呼び出しとして実装することもできるが、通常、大規模なサーバー群全体で割り当てロジックの一貫性を保つために外部サービスを使用する。
Server-side assignment is very intrusive; it requires deep changes to the experimenting application’s code.
サーバーサイドの割り当ては、実験アプリケーションのコードに深い変更を加える必要があるため、非常に侵入的である。
Nonetheless, server-side assignment has three distinct advantages: 1.
それにもかかわらず、サーバーサイド割り当てには3つの明確な利点がある： 1.
It is an extremely general method; it is possible to experiment on virtually any aspect of a page simply by modifying its code.2.It places the experimentation code in the best logical place—right where decisions are made about a change.
これは極めて一般的な方法であり、コードを修正するだけで、事実上、ページのあらゆる側面について実験することが可能である。
In particular, it is possible to experiment on backend features (for example, search and personalization algorithms) without touching the front end.3.Experimentation is completely transparent to end users.
特に、フロントエンドに触れることなく、バックエンドの機能（例えば、検索やパーソナライゼーション・アルゴリズム）を実験することが可能である。
End users experience only minimal delay and cannot discern that an experiment is running on the site.
エンドユーザーが経験する遅延はごくわずかで、サイト上で実験が行われていることを見分けることはできない。
Server-side assignment also has a number of disadvantages, all of which are stem from its intrusiveness:
サーバーサイドの割り当てにもいくつかの欠点があり、そのすべてがその押しつけがましさに起因している：

1. Initial implementation is expensive. Depending on the complexity of the site, implementing the necessary server-side code changes can be difficult. 2. Because the method requires a developer to change code deep in the page logic for each experiment, implementing an experiment introduces risk. The risk is greatest on complex features whose code is spread across many pages and/or services. 3. Some variations of this method require code changes to be manually undone to complete an experiment. Specifically, a programmer must remove the code path that implements the losing treatment along with the conditional logic that reacts to the end user’s treatment assignment. While this simply refers to code clean-up, leaving the losing treatment code in there can yield a very messy codebase, while removing it adds risk since production code will be modified. While this process is trivial for a simple one-page experiment, it can be a painful process if API calls are spread throughout the code, and all such code changes introduce additional risk. Server-side assignment can be integrated into a content management system to greatly reduce the cost of running experiments using this method. When so integrated, experiments are configured by changing metadata instead of code. The metadata may be represented by anything from an editable configuration file to a relational database managed by a graphical user interface. The method is best illustrated with an example from a real system running at Amazon.com. Amazon’s home page is built on a content management system that assembles the page from individual units called slots (Kohavi et al. 2004). The system refers to page metadata at render time to determine how to assemble the page. Non-technical content editors schedule pieces of content in each slot through a graphical user interface that edits this page metadata. Content can include anything from an advertisement, to a product image, to a snippet of text filled with links, to a widget that displays dynamic content (such as personalized recommendations). A typical experiment would be to try various pieces of content in different locations. For example, do the recommendations receive higher clickthrough on the left or on the right? To enable this sort of experiment, the content management system is extended to allow pieces of content to be scheduled with respect to a specific experiment. As the page request comes in, the system executes the assignment logic for each scheduled experiment and saves the results to page context where the page assembly mechanism can react to it. The content management system only needs to be modified once; from then on, experiments can be designed, implemented, and removed by modifying the page metadata through the user interface. 初期導入には費用がかかる。 サイトの複雑さによっては、必要なサーバーサイドのコード変更を実装するのが難しい場合がある。2.この方法では、開発者が実験ごとにページロジックの奥深くにあるコードを変更する必要があるため、実験を実装するにはリスクが伴う。 そのリスクは、コードが多くのページやサービスにまたがっている複雑な機能で最大となる。3.この方法のいくつかのバリエーションでは、実験を完了させるためにコードの変更を手動で元に戻す必要がある。 具体的には、プログラマーは、エンドユーザーの治療割り当てに反応する条件ロジックとともに、負けた治療を実装するコードパスを削除しなければならない。 これは単にコードのクリーンアップを意味するが、敗戦処理のコードをそのままにしておくと、コードベースが非常に乱雑になる可能性がある。 単純な1ページの実験であればこのプロセスは些細なことだが、APIコールがコード全体に広がっている場合は骨の折れるプロセスとなる。 サーバーサイドの割り当てをコンテンツ管理システムに統合することで、この方法を使った実験の実行コストを大幅に削減することができる。 このように統合された場合、実験はコードの代わりにメタデータを変更することで設定される。 メタデータは、編集可能なコンフィギュレーション・ファイルから、グラフィカル・ユーザー・インターフェースで管理されるリレーショナル・データベースまで、あらゆるもので表現することができる。 この方法は、Amazon.comで実際に稼動しているシステムの例で説明するのが一番わかりやすい。 アマゾンのホームページは、スロットと呼ばれる個々の単位からページを組み立てるコンテンツ管理システムで構築されている（Kohavi et al.2004）。 システムはレンダリング時にページのメタデータを参照し、ページの組み立て方を決定する。 技術者でないコンテンツ編集者は、このページのメタデータを編集するグラフィカル・ユーザー・インターフェースを通じて、各スロットにコンテンツの断片をスケジュールする。 コンテンツには、広告から商品画像、リンクで埋め尽くされたテキストの断片、動的コンテンツ（パーソナライズされたおすすめ商品など）を表示するウィジェットまで、あらゆるものが含まれる。 典型的な実験は、さまざまな場所でさまざまなコンテンツを試してみることだろう。 例えば、左と右のどちらがクリックスルー率が高いか？このような実験を可能にするために、コンテンツ管理システムを拡張し、特定の実験に関してコンテンツの断片をスケジューリングできるようにする。 ページ要求が来ると、システムはスケジュールされた各実験の割り当てロジックを実行し、その結果をページ組立メカニズムが対応できるページコンテキストに保存する。 コンテンツマネジメントシステムは一度だけ修正すればよい。それ以降は、ユーザーインターフェイスを通じてページのメタデータを修正することで、実験の設計、実施、削除が可能になる。

### 5.2.5. Summary 概要

The following table summarizes the relative advantages and disadvantages of all of the assignment methods described above.
次の表は、上記のすべての割り当て方法の相対的な長所と短所をまとめたものである。

![]()

## 5.3. Data path データパス

In order to compare metrics across experiment variants, a website must first record the treatment assignments of all end users who visit the site during an experiment.
実験のバリアント間でメトリクスを比較するためには、ウェブサイトはまず、実験中にサイトを訪れたすべてのエンドユーザーのトリートメント割り当てを記録する必要があります。
Then, the website must collect raw data such as page views, clicks, revenue, render time, or customer-feedback selections.
次に、ウェブサイトは、ページビュー、クリック数、収益、レンダリング時間、または顧客フィードバックの選択などの生データを収集しなければならない。
Each row of this raw data must be annotated with the identifier of the variant of each experiment that the user saw on the page request.
この生データの各行は、ユーザーがページリクエストで見た各実験のバリアントの識別子で注釈されていなければならない。
The system must then convert this raw data into metrics—numerical summaries that can be compared between variants of an experiment to determine the outcome.
そしてシステムは、この生データを、結果を決定するために実験のバリエーション間で比較できるメトリクス-数値サマリー-に変換しなければならない。
Metrics can range from simple aggregates (total page views) all the way to complex inferred measures (customer satisfaction or search relevance).
指標は、単純な集計（総ページビュー）から複雑な推論指標（顧客満足度や検索関連性）まで多岐にわたる。
To compute metrics, the system applies basic transformations and then aggregates the observations, grouping by experiment, variant, and any other dimensions that the experimenter wishes to analyze (for example, demographics or user agent).
メトリクスを計算するために、システムは基本的な変換を適用し、次にオブザベーションを集約し、実験、バリアント、および実験者が分析したい他の次元（例えば、人口統計やユーザーエージェント）でグループ化する。
Additional transformations may be applied at this point to produce more complex measures.
より複雑な尺度を作成するために、この時点で追加の変換を適用することができる。
From here, we create a table of metric values, broken down by dimensions, experiment, and (most importantly) variant.
ここから、ディメンション別、実験別、（最も重要な）バリアント別に分けた指標値の表を作成する。
We can now compare metric values between variants and determine statistical significance using either any of a number of statistical tests.
バリアント間のメトリック値を比較し、いくつかの統計的検定のいずれかを使用して統計的有意性を決定することができます。
Although the basic analysis techniques closely resemble those used in online analytic processing (OLAP), website experimentation raises some specific data issues.5.3.1 Event-triggered filtering Data collected from web traffic on a large site typically has tremendous variability, thereby making it difficult to run an experiment with sufficient power to detect effects on smaller features.
基本的な分析テクニックはオンライン分析処理（OLAP）で使用されるものに酷似しているが、ウェブサイトでの実験にはいくつかの特有のデータ問題がある。
One critical way to control this variability is to restrict the analysis to only those users who were impacted by the experiment (see Sect.3.2.3).
このばらつきを抑制する重要な方法のひとつは、分析の対象を、実験の影響を受けた ユーザーのみに限定することである（3.2.3節参照）。
We can further restrict the analysis to the portion of user behavior that was affected by the experiment.
さらに、実験によって影響を受けたユーザー行動の部分に分析を限定することができる。
We refer to these data restrictions as event-triggered filtering.
このようなデータ制限をイベントトリガーフィルタリングと呼ぶ。

Event-triggered filtering is implemented by tracking the time at which each user first saw content that was affected by the experiment.
イベントトリガーによるフィルタリングは、各ユーザーが実験の影響を受けたコンテンツを最初に見た時刻を追跡することで実施される。
This data can be collected directly (by recording an event when a user sees experimental content) or indirectly (by identifying experimental content from page views or other parts of the existing raw data stream).
このデータは、（ユーザーが実験的コンテンツを見たときのイベントを記録することによって）直接収集することも、（ページビューや既存の生データストリームの他の部分から実験的コンテンツを特定することによって）間接的に収集することもできる。
It is also possible to integrate event-triggered filtering directly into the assignment method.5.3.2 Raw data collection Collecting the raw observations is similar to basic website instrumentation.
5.3.2 生のデータ収集 生のオブザベーションの収集は、基本的なウェブサイトのインスツルメンテーションに似ている。
However, the needs of experimentation make some options more attractive than others.5.3.2.1 Using existing (external) data collection Many websites already have some data collection in place, either through an in-house system or an external metrics provider like Omniture or Webmetrics.
5.3.2.1既存の（外部）データ収集の利用 多くのウェブサイトは、社内システム、またはOmnitureやWebmetricsのような外部のメトリクス・プロバイダーを通じて、すでに何らかのデータ収集を行っている。
For these websites, a simple approach is to push the treatment assignment for each user into this system so that it becomes available for analysis.
このようなウェブサイトの場合、単純なアプローチは、各ユーザーの治療割り当てをこのシステムにプッシュし、分析に利用できるようにすることである。
While this approach is simple to set up, most existing data collection systems are not designed for the statistical analyses that are required to correctly analyze the results of a controlled experiment.
この方法はセットアップが簡単であるが、既存のデータ収集システムのほとんどは、対照実験の結果を正しく分析するために必要な統計分析用に設計されていない。
Therefore, analysis requires manual extraction of the data from the external system, which can be expensive and also precludes real-time analysis.
そのため、分析には外部システムから手動でデータを抽出する必要があり、コストがかかるだけでなく、リアルタイムの分析もできない。
Moreover, the existing code needs to be modified each time a new experiment is run to add the treatment assignment to all of the recorded observations.
さらに、新しい実験が実行されるたびに、記録されたすべてのオブザベーションに治療割り当てを追加するために、既存のコードを修正する必要がある。
We recommend this approach only in situations where no other approach can be used.5.3.2.2 Local data collection Using this method, the website records data locally, either through a local database or log files.
5.3.2.2.ローカルデータ収集 この方法では、ウェブサイトはローカルデータベースまたはログファイルを通じて、ローカルにデータを記録します。
The data is collected locally on each server in the fleet and must be sorted and aggregated before analysis can begin.
データはフリート内の各サーバーでローカルに収集され、分析を開始する前にソートして集計する必要がある。
This method can be made to scale up to very large websites.
この方法は、非常に大規模なウェブサイトにも対応できる。
However, as the fleet scales up, collecting these logs in near real-time while minimizing data loss becomes extremely difficult.
しかし、フリートの規模が拡大するにつれ、データ損失を最小限に抑えながら、これらのログをほぼリアルタイムで収集することは非常に難しくなる。
Moreover, this method makes it difficult to collect data from sources other than the webserver (like backend services or even the user’s browser via JavaScript); every additional source of data increases the complexity of the log gathering infrastructure.5.3.2.3 Service-based collection Under this model, the website implements a service specifically designed to record and store observation data.
さらに、この方法はウェブサーバ以外のソース（バックエンドサービスやJavaScriptを介した ユーザーのブラウザなど）からデータを収集することを難しくします。
Service calls may be placed in a number of locations, including web servers, application servers, backend algorithm services, and even the end user’s browser (called via JavaScript).
サービス・コールは、ウェブ・サーバー、アプリケーション・サーバー、バックエンドのアルゴリズム・サービス、さらにはエンド・ユーザーのブラウザー（JavaScript経由で呼び出される）など、さまざまな場所に置かれる可能性がある。
Implementations of this model typically cache some data locally to avoid making an excessive number of physical service calls.
このモデルの実装では、通常、物理的なサービスコールの回数が過剰になるのを避けるために、いくつかのデータをローカルにキャッシュする。
This approach has the advantage of centralizing all observation data, making it available for easy analysis.
この方法には、すべての観測データを一元化し、簡単に分析できるという利点がある。
In particular, it makes it easy to combine observations from backend services with client-side JavaScript data collection that is necessary to accurate capture user behavior on pages making extensive use of DHTML and Ajax.
特に、DHTMLやAjaxを多用するページでユーザーの行動を正確に把握するために必要な、クライアントサイドのJavaScriptデータ収集とバックエンド・サービスからの観察を簡単に組み合わせることができます。
This method also makes it easier to experiment on large websites built on heterogeneous architectures.
この方法はまた、異種アーキテクチャ上に構築された大規模なウェブサイトでの実験を容易にする。

Unlike with assignment methods, there is a clear winner among data collection techniques: service-based collection is the most flexible and therefore preferred when possible.
割り当て方法とは異なり、データ収集技術には明確な勝者がいる： サービスベースの収集が最も柔軟であり、したがって可能な限り望ましい。

# 6. Lessons learned 教訓

The difference between theory and practice is larger in practice than the difference between theory and practice in theory – Jan L.A.van de Snepscheut
**理論と実践の間の差は、理論的には小さいように見えるが、実際にはもっと大きい** - Jan L.A.van de Snepscheut
(皮肉めいた言い回しだから分かりづらい...!想定よりも差が大きいよって話か...!)

Many theoretical techniques seem well suited for practical use and yet require significant ingenuity to apply them to messy real world environments.
多くの理論的な技術は、実用的には適しているように見えるが、実際の乱雑な現実世界の環境に適用するにはかなりの独創性が必要である。
Controlled experiments are no exception.
対照実験も例外ではない。
Having run a large number of online experiments, we now share several practical lessons in three areas: (i) analysis; (ii) trust and execution; and (iii) culture and business.
多くのオンライン実験を実施してきた私たちは、3つの分野でいくつかの実践的な教訓を共有する： (i)分析、(ii)信頼と実行、(iii)文化とビジネス。

## 6.1. Analysis 分析

The road to hell is paved with good intentions and littered with sloppy analysis – Anonymous
地獄への道は善意で舗装され、ずさんな分析で汚れている - Anonymous

### 6.1.1. Mine the data データをマイニングする

A controlled experiment provides more than just a single bit of information about whether the difference in OECs is statistically significant.
**対照実験では、「OECの差が統計的に有意かどうか」という単一の情報以上の情報が提供される**。(うんうん...!)
Rich data is typically collected that can be analyzed using machine learning and data mining techniques.
通常、機械学習やデータマイニング技術を使用して分析できる豊富なデータが収集される。
For example, an experiment showed no significant difference overall, but a population of users with a specific browser version was significantly worse for the Treatment.
例えば、ある実験では、全体としては有意な差は見られなかったが、特定のブラウザ・バージョンを持つユーザの集団では、トリートメントに対して有意に悪い結果が出た。(セグメントの分析?? でも多重検定みたいなリスクはある?? 検定ではなく示唆を得るという点では有効か...!)
The specific Treatment feature, which involved JavaScript, was buggy for that browser version and users abandoned.
JavaScriptを含む特定のtrearment機能は、そのブラウザバージョンに対してバグがあり、ユーザーが離れてしまった。
Excluding the population from the analysis showed positive results, and once the bug was fixed, the feature was indeed retested and was positive.
この母集団を分析から除外したところ、肯定的な結果が得られた。**バグが修正された後、この機能は実際に再テストされ、肯定的な結果が得られた**。(これは大事だと思う...!多重検定で終わらない!)

### 6.1.2. Speed matters スピードが重要

A Treatment might provide a worse user experience because of its performance.
トリートメントは、そのパフォーマンスのために、より悪いユーザ体験を提供するかもしれない。(ex. 予測精度が高いMLモデルを採用しても、推論速度が遅いと、ユーザ体験が悪化するかも...!)
Linden (2006b, p.15), wrote that experiments at Amazon showed a 1% sales decrease for an additional 100msec, and that a specific experiment at Google, which increased the time to display search results by 500 msecs reduced revenues by 20% (based on a talk by Marissa Mayer at Web 2.0).
Linden(2006b,p.15)は、アマゾンでの実験では、**100ミリ秒の追加で1％の売上減少**が見られ、グーグルでの具体的な実験では、検索結果の表示時間を500ミリ秒増加させたところ、売上が20％減少したと書いている(Web 2.0でのマリッサ・メイヤーの講演に基づく)。(レイテンシーをわざと悪化させるABテストか...!)
Recent experiments at Microsoft Live Search (Kohavi 2007, p.12) showed that when the search results page was slowed down by one second, queries per user declined by 1% and ad clicks per user declined by 1.5%; when the search results page was slowed down by two seconds, these numbers more than doubled to 2.5% and 4.4%.
マイクロソフト・ライブサーチでの最近の実験（Kohavi 2007, p.12）によると、検索結果ページを1秒遅くした場合、ユーザーあたりのクエリは1％、ユーザーあたりの広告クリックは1.5％減少し、検索結果ページを2秒遅くした場合、これらの数字は2.5％、4.4％と2倍以上に増加した。

If time is not directly part of your OEC, make sure that a new feature that is losing is not losing because it is slower.
時間が直接OECの一部でない場合、負けている新機能が遅いから負けているのではないことを確認してください。

### 6.1.3. Test one factor at a time (or not) 一度に1つの要因をテストする（あるいはしない）

Several authors (Peterson 2004, p.76; Eisenberg 2005) recommend testing one factor at a time.
いくつかの著者（Peterson 2004, p.76; Eisenberg 2005）は、一度に1つのfactorをテストすることを推奨している。(i.e. multi variate testingを避けよう...!って話?)
We believe the advice, interpreted narrowly, is too restrictive and can lead organizations to focus on small incremental improvements.
私たちは、この忠告を狭く解釈すると、制約が多すぎ、組織が小さな漸進的な改善に集中することになりかねないと考えている。(同時に1つのABテストしかしちゃいけない、みたいな?)
Conversely, some companies are touting their fractional factorial designs and Taguchi methods, thus introducing complexity where it may not be needed.
逆に、分数階乗設計やタグチメソッドを売り物にする企業もあり、必要ないところに複雑さを持ち込んでいる。
While it is clear that factorial designs allow for joint optimization of factors, and are therefore superior in theory (Mason et al.1989; Box et al.2005) our experience from running experiments in online web sites is that interactions are less frequent than people assume (van Belle 2002), and awareness of the issue is enough that parallel interacting experiments are avoided.
factorial designsは複数のfactorの共同最適化を可能にし、したがって理論的には優れていることは明らかです(Mason et al.1989; Box et al.2005)。(=理論的には...!)
しかし、我々がオンラインウェブサイトで実験を実施してきた経験から、相互作用は人々が想定するほど頻繁ではないこと（van Belle 2002）と、この問題に対する認識が十分であるため、相互作用する実験を避けることができるということがわかりました。(=実際には共同最適化しなくても大丈夫ぽいよってこと??)

Our recommendations are therefore:
従って、**我々の推奨は以下の通り**である：

- Conduct single-factor experiments for gaining insights and when you make incremental changes that could be decoupled.
  デカップリングできる増分変更を行うときや洞察を得るために、**single-factor実験**を実施する。
- Try some bold bets and very different designs.
  大胆な賭けや非常に異なるデザインを試してみる。
  For example, let two designers come up with two very different designs for a new feature and try them one against the other.
  例えば、2人のデザイナーが新機能のために全く異なる2つのデザインを考え、1対1で試してみる。
  You might then start to perturb the winning version to improve it further.
  その後、優勝したバージョンをさらに改良するために手を加え始めるかもしれない。
  For backend algorithms it is even easier to try a completely different algorithm (e.g., a new recommendation algorithm).
  バックエンドアルゴリズムの場合、まったく別のアルゴリズム（例えば新しい推薦アルゴリズム）を試すのはさらに簡単だ。
  Data mining can help isolate areas where the new algorithm is significantly better, leading to interesting insights.
  データマイニングは、新しいアルゴリズムが著しく優れている部分を特定するのに役立ち、興味深い洞察につながる。
- Use full or fractional factorial designs suitable for estimating interactions when several factors are suspected to interact strongly.
  **いくつかのfactorが強く相互作用することが疑われる場合**、相互作用の推定に適した完全または分数階計画を用いる。
  Limit the number of values per factor and assign the same percentage to the treatments as to the control.
  各factorの値の数を制限し(=variantの数を2つにしようってこと?その方がサンプルサイズ設計とかはシンプルなんだよね...!)、トリートメントに割り当てる割合をコントロールと同じにする。
  This gives your experiment maximum power to detect effects.
  これにより、実験が効果を検出するための最大限の力を得ることができる。(検出力?)

## 6.2. Trust and execution 信頼と実行

In God we trust, all others pay cash – Jean Shepherd

### 6.2.1 Run continuous A/A tests

Run A/A tests (see Sect.3.1) and validate the following.
A/Aテスト（3.1節参照）を実行し、以下を検証する。

- 1. Are users split according to the planned percentages? ユーザーは計画された割合で分割されているか？
- 2. Is the data collected matching the system of record? 収集されたデータは記録システムと一致しているか？
- 3. Are the results showing non-significant results 95% of the time? 結果は95%の確率で有意でない結果を示しているか？

Continuously run A/A tests in parallel with other experiments.
他の実験と並行してA/Aテストを継続的に実行する。

### 6.2.2 Automate ramp-up and abort

As discussed in Sect.3.3, we recommend that experimenters gradually increase the percentage of users assigned to the Treatment(s).
3.3節で議論したように、**実験者はtreatmentに割り当てられたユーザの割合を徐々に増やすことを推奨**します。
An experimentation system that analyses the experiment data in near-real-time can automatically shut-down a Treatment if it is significantly underperforming relative to the Control.
ほぼリアルタイムで実験データを分析する実験システムは、**treatmentがコントロールに比べて著しく不調である場合、自動的にtreatmentをシャットダウンすることができる**。
An auto-abort simply reduces the percentage of users assigned to the underperforming Treatment to zero.
自動中止は、単に不調なトリートメントに割り当てられているユーザの割合をゼロに減らすだけです。
Since the system will automatically reduce the risk of exposing many users to egregious errors, the organization can make bold bets and innovate faster.
システムが自動的に多くのユーザに酷いエラーをさらすリスクを減らすため、組織は大胆な賭けをし、より速く革新することができる。
Ramp-up is quite easy to do in online environments, yet hard to do in offline studies.
ランプアップはオンライン環境では非常に簡単だが、オフラインの研究では難しい。
We have seen no mention of these practical ideas in the literature, yet they are extremely useful.
これらの実用的なアイデアについての文献での言及は見当たりませんが、非常に有用です。

### 6.2.3 Determine the minimum sample size

Decide on the statistical power, the effect you would like to detect, and estimate the variability of the OEC through an A/A test.
統計的検出力、検出したい効果を決定し、A/A検定によってOECの変動を推定する。
Based on this data you can compute the minimum sample size needed for the experiment and hence the running time for your web site.
このデータに基づいて、実験に必要な最小サンプルサイズを計算し、したがってウェブサイトの実行時間を決定することができます。
A common mistake is to run experiments that are underpowered.
**よくある間違いは、underpoweredな実験を実行すること**です。
Consider the techniques mentioned in Sect.3.2 point 3 to reduce the variability of the OEC.
OECの変動を減らすために、3.2節で述べたテクニックを検討する。
Also recognize that some metrics have poor power characteristics in that their power actually degrades as the experiment runs longer.
**また、メトリクスの中には、実験時間が長くなるにつれてパワーが低下するという、パワー特性が悪いものがあることも認識してください。**(ん？？:thinking_face:)
For these metrics it is important that you get an adequate number of users into the test per day and that the Treatment and Control groups are of equal size.
これらのメトリックについては、1日あたりのテストユーザ数が十分であり、TreatmentとControlのグループが同じサイズであることが重要です。

### 6.2.4 Assign 50% of users to treatment

One common practice among novice experimenters is to run new variants for only a small percentage of users.
初心者の実験者の間でよく見られる実践の1つは、新しいvariantをわずかな割合のユーザだけに実行することです。
The logic behind that decision is that in case of an error only few users will see a bad Treatment, which is why we recommend Treatment ramp-up.
この決断の背景にある論理は、エラーの場合、わずかなユーザだけが悪いTreatmentを見ることになるため、Treatment ramp-upを推奨しています。
In order to maximize the power of an experiment and minimize the running time, we recommend that 50% of users see each of the variants in an A/B test.
**実験のパワーを最大化し、実行期間を最小化するために、A/Bテストでは50%のユーザが各variantを見ることをお勧めします**。(この論文では、全ユーザの50%にいきなり新しいvariantを見せる事を推奨してるのか...?? twitterさんのブログでは非推奨だったよね。あっちはそもそもテスト対象のユーザ割合を減らそうって話かな。controlとtreatmentの割合は1対1にしようって意味だったらどっちも共通の見解か...!)
Assuming all factors are fixed, a good approximation for the multiplicative increase in running time for an A/B test relative to 50%/50% is 1/4p(1 − p) where the Treatment receives portion p of the traffic.
すべての要素が固定されていると仮定すると、 50%/50%の場合の実行期間に対する、Treatmentがトラフィックの一部 $p$ を受け取る場合のA/Bテストの実行時間の乗算的な増加の良い近似値は $1/4p(1 − p)$ 倍です。(これってnull ditrbutionとalternative distributionの分散から導出してるっぽい...?:thinking_face:)
For example, if an experiment is run at 99%/1%, then it will have to run about 25 times longer than if it ran at 50%/50%.
例えば、実験を99%/1%で実行する場合、50%/50%で実行する場合よりも約25倍長く実行する必要がある。
(具体例を考えると、全ユーザにおけるABテスト対象ユーザの割合の話ではなく、テスト対象ユーザ集合におけるcontrolとtreatmentの割合の話っぽい...!)

### 6.2.5 Beware of day of week effects 曜日効果に注意

Even if you have a lot of users visiting the site, implying that you could run an experiment for only hours or a day, we strongly recommend running experiments for at least a week or two, then continuing by multiples of a week so that day-of-week effects can be analyzed.
サイトを訪れるユーザが多く、数時間または1日だけでunder-poweredな実験を実行できるということを意味していても、**少なくとも1週間または2週間の実験を実行し、その後、週の倍数で続けること**を強くお勧めします。そうすることで、曜日効果を分析することができます。
(そういう場合は特に、全ユーザをテスト対象に割り当てない方が良さそう...!というか全ユーザを割り当てちゃったらサンプルサイズ増え過ぎちゃいそうだし...!:thinking_face:)
For many sites the users visiting on the weekend represent different segments, and analyzing them separately may lead to interesting insights.
多くのサイトでは、週末に訪れるユーザは異なるセグメントであり、それらを個別に分析することで、興味深い洞察が得られるかもしれない。
This lesson can be generalized to other time-related events, such as holidays and seasons, and to different geographies: what works in the US may not work well in France, Germany, or Japan.
この教訓は、祝日や季節など、時間に関連する他の行事や、異なる地域にも一般化できる： アメリカではうまくいっても、フランス、ドイツ、日本ではうまくいかないかもしれない。

Putting 6.2.3, 6.2.4, and 6.2.5 together, suppose that the power calculations imply that you need to run an A/B test for a minimum of 5 days, if the experiment were run at 50%/50%.
6.2.3、6.2.4、6.2.5をまとめると、実験が50％／50％で実施された場合、最小で5日間実施する必要があるというパワー計算が示されたとします。
We would then recommend running it for a week to avoid day-of-week effects and to increase the power over the minimum.
その場合、**曜日効果を避け、最小限のパワーを上回るために、1週間実施することを推奨**します。
However, if the experiment were run at 95%/5%, the running time would have to be increased by a factor of 5–25 days, in which case we would recommend running it for four weeks.
しかし、実験を95％／5％で実施した場合、実施期間を5～25日増やす必要があり、その場合は4週間実施することを推奨する。
Such an experiment should not be run at 99%/1% because it would require over 125 days, a period we consider too long for reliable result; factors, such as cookie churn, that have secondary impact in experiments running for a few weeks may start contaminating the data.
このような実験は99％／1％で実施すべきではありません。なぜなら、信頼性のある結果を得るには長すぎる期間であると考えるからです。数週間実施される実験には二次的な影響を与えるクッキーのチャーンなどの要因(??)が、データを汚染し始める可能性があります。

<!-- ここまで読んだ! -->

## 6.3. Culture and business ♪文化とビジネス

It is difficult to get a man to understand something when his salary depends upon his not understanding it.
給料がそれを理解しないことに依存している場合、人を理解させるのは難しい

– Upton Sinclair

### 6.3.1 Agree on the OEC upfront OECを事前に合意する

One of the powers of controlled experiments is that it can objectively measure the value of new features for the business.
制御された実験の強みの1つは、**ビジネスの新機能の価値を客観的に測定できる**ことです。
However, it best serves this purpose when the interested parties have agreed on how an experiment is to be evaluated before the experiment is run.
しかし、実験が実施される前に、関係者が実験の評価方法に合意している場合に、この目的に最もよく役立ちます。

While this advice may sound obvious, it is infrequently applied because the evaluation of many online features is subject to several, often competing objectives.
このアドバイスは当たり前のように聞こえるかもしれないが、多くのオンライン機能の評価は、**しばしば競合する複数の目標に従っているため、この教訓はあまり適用されていないことがある**。
OECs can be combined measures, which transform multiple objectives, in the form of experimental observations, into a single metric.
OECは、実験的観察の形で**複数の目標を変換する複合測定値であり、単一のメトリックになりうる**。
In formulating an OEC, an organization is forced to weigh the value of various inputs and decide their relative importance.
OECを策定する際、組織は様々なインプットの価値を計量し、それらの相対的な重要性を決定する必要に迫られる。
A good technique is to assess the lifetime value of users and their actions.
良いテクニックは、ユーザの生涯価値とその行動を評価することである。
For example, a search from a new user may be worth more than an additional search from an existing user.
例えば、新規ユーザからの検索は、既存ユーザからの追加検索よりも価値があるかもしれない。
Although a single metric is not required for running experiments, this hard up-front work can align the organization and clarify goals.
実験を実施するために単一のメトリックが必要というわけではありませんが、このような前もってのハードワークは、組織を整え、目標を明確にすることができる。(単一のmetricを作っておけると、意思決定しやすくて最高だよねってことか!)

### 6.3.2 Beware of launching features that “do not hurt” users ユーザに「損害を与えない」機能をリリースすることに注意

When an experiment yields no statistically significant difference between variants, this may mean that there truly is no difference between the variants or that the experiment did not have sufficient power to detect the change.
実験がバリアント間で統計的に有意な差を示さない場合、これは本当にvariant間に差がないか、あるいは実験が変化を検出するための十分なパワーを持っていなかったことを意味するかもしれません。
In the face of a “no significant difference” result, sometimes the decision is made to launch the change anyway “because it does not hurt anything.” It is possible that the experiment is negative but underpowered.
**「有意な差なし」という結果を前にして、"何も損しないから"とにかく変更を開始するという決定がなされることがあ**る。実験が負の結果であるが、パワーが不足している可能性がある。
(やっぱりunderpoweredな実験を避ける事には価値がある...!:thinking_face:)

### 6.3.3 Weigh the feature maintenance costs 機能のメンテナンスコストの重み付け

An experiment may show a statistically significant difference between variants, but choosing to launch the new variant may still be unjustified because of maintenance costs.
実験はバリアント間で統計的に有意な差を示すかもしれませんが、新しいバリアントをローンチすることは、メンテナンスコストのために正当化されないかもしれません。
A small increase in the OEC may not outweigh the cost of maintaining the feature.
**OECのわずかな増加は、その機能を維持するためのコストを上回らないかもしれない**。
(統計的に有意な差が、ビジネス的に価値のある差とは限らないって話だ...!:thinking_face:)

### 6.3.4. Change to a data-driven culture データ主導の文化への変革

Running a few online experiments can provide great insights into how customers are using a feature.
いくつかのオンライン実験を行うことで、顧客がその機能をどのように使用しているかについての素晴らしい洞察を得ることができる。
Running frequent experiments and using experimental results as major input to company decisions and product planning can have a dramatic impact on company culture.
**頻繁に実験を行い、実験結果を企業の意思決定と製品計画の主要なインプットとして使用することは、企業文化に大きな影響を与えるかもしれません**。
As Mike Moran said in his wonderful book “Do it Wrong Quickly” (Moran 2007) “Sometimes you have to kiss a lot of frogs to find one prince. So how can you find your prince faster? By finding more frogs and kissing them faster and faster.”
Mike Moranは彼の素晴らしい本「Do it Wrong Quickly」（Moran 2007）で次のように述べています。「**王子様を見つけるためには、たくさんのカエルにキスしなければならないことがあります。では、どうすればより速く王子様を見つけることができるでしょうか？ より多くのカエルを見つけ、それらをより速く、そしてより速くキスすることです。**」
Software organizations shipping classical software developed a culture where features are completely designed prior to implementation.
古典的なソフトウェアを出荷するソフトウェア組織は、実装前に機能が完全に設計される文化を築いてきました。(iterativeじゃない開発プロセスか...!)
In a web world, we can integrate customer feedback directly through prototypes and experimentation.
ウェブの世界では、プロトタイプや実験を通じて、顧客のフィードバックを直接取り入れることができる。
If an organization has done the hard work to agree on an OEC and vetted an experimentation system, experimentation can provide real data and move the culture towards attaining shared goals rather than battle over opinions.
もし組織がOECに合意し、実験システムを検証するためのハードワークを行っているなら、実験は実際のデータを提供し、意見の戦いではなく共有の目標を達成するための文化を進めることができる。

<!-- ここまで読んだ! -->

# 7. Summary 要約

Almost any question can be answered cheaply, quickly and finally, by a test campaign.
ほとんどどんな質問にも、テストキャンペーンによって、安く、早く、そして最終的に答えることができる。
And that’s the way to answer them – not by arguments around a table.
テーブルを囲んで議論するのではなく、それがその答え方なのだ。
Go to the court of last resort – buyers of your products.
最後の頼みの綱である、あなたの製品の買い手に訴えよう。
– Claude Hopkins, Scientific Advertising, 1923

…the ability to experiment easily is a critical factor for Web-based applications.
The online world is never static.
ネットの世界は決して静的なものではない。
There is a constant flow of new users, new products and new technologies.
新しいユーザー、新しい製品、新しい技術が絶えず生まれている。
Being able to figure out quickly what works and what doesn’t can mean the difference between survival and extinction.
何が効果的で何が効果的でないかを素早く見極められるかどうかが、生き残りと絶滅の分かれ目になる。
– Hal Varian, 2007

Classical knowledge discovery and data mining provide insight, but the patterns discovered are correlational and therefore pose challenges in separating useful actionable patterns from those caused by “leaks” (Kohavi et al.2004).
**古典的な知識発見とデータマイニングは、洞察を提供するが、発見されたパターンは相関的であるため、有用な実用的パターンと“leaks”によるパターンを分離するのに課題がある**（Kohavi et al.2004）。(leaksって、擬似相関的な意味合いかな...!:thinking_face:)
Controlled experiments neutralize confounding variables by distributing them equally over all values through random assignment (Keppel et al.1992), thus establishing a causal relationship between the changes made in the different variants and the measure(s) of interest, including the Overall Evaluation Criterion (OEC).
対照実験は、無作為割付けによってすべての値に等しく配分することで、交絡変数を中和し(Keppel et al.1992)、その結果、**異なるvariantで行われた変更と興味のある指標（OECを含む）との因果関係を確立する**。
Using data mining techniques in this setting can thus provide extremely valuable insights, such as the identification of segments that benefit from a feature introduced in a controlled experiment, leading to a virtuous cycle of improvements in features and better personalization.
この設定でデータマイニング技術を使用することで(i.e. オンライン実験のデータを使うことで...?)、対照実験で導入された機能に利益をもたらすセグメントの特定など、非常に貴重な洞察を提供することができ、その結果、機能の改善とより良いパーソナライゼーションの好循環をもたらす。

The basic ideas in running controlled experiments are easy to understand, but a comprehensive overview for the web was not previously available.
対照実験の基本的な考え方は理解しやすいが、ウェブ用の包括的な概要はこれまでなかった。
In addition, there are important new lessons and insights that we shared throughout the paper, including generalized architectures, ramp-up and aborts, the practical problems with randomization and hashing techniques, and organizational issues, especially as they relate to OEC.
さらに、本稿全体を通じて共有した重要な新しい教訓や洞察があり、一般的なアーキテクチャ、ランプアップと中止、ランダム化とハッシング技術の実用的な問題、特にOECに関連する組織的な問題などがある。

Software features in products today are commonly determined by the same way medicine was prescribed prior to World War II: by people who were regarded as experts, not by using scientific methods, such as controlled experiments.
今日の製品のソフトウェア機能は、第二次世界大戦前に医薬品が処方されていたのと同じ方法で決定されるのが一般的だ： つまり、専門家とみなされる人々によって決定されるのであって、管理された実験などの科学的方法によって決定されるのではない。
We can do better today, especially with our access to customer behavior online.
**特にオンラインで顧客の行動にアクセスできる現代では、もっとうまくやれるはずだ。**
In The Progress of Experiment: Science and Therapeutic Reform in the United States, 1900–1990 (Marks 2000, p.3), the author wrote about the increasing importance of designed experiments in the advance of medical knowledge: “Reformers in the second half of the century abandoned their predecessors’ trust in the judgment of experienced clinicians.In its place, they offered an impersonal standard of scientific integrity: the double-blind, randomized, controlled clinical trial.”
実験の進歩： The Progress of Experiment: Science and Therapeutic Reform in the United States, 1900-1990 (Marks 2000, p.3)の中で、著者は医学知識の進歩における計画された実験の重要性の高まりについて書いている： 「世紀後半の改革者たちは，経験豊かな臨床医の判断に対する先人たちの信頼を捨てた。 その代わりに，彼らは科学的完全性の非人間的基準を提示した： 二重盲検無作為化比較臨床試験」。

Many organizations have strong managers who have strong opinions, but lack data, so we started to use the term HiPPO, which stands for Highest Paid Person’s Opinion, as a way to remind everyone that success really depends on the users’ perceptions.
多くの組織には、意見が強い強力なマネージャーがいるが、データがないため、**私たちは成功は本当にユーザの認識に依存していることを思い出させるために、HiPPOという用語を使い始めた**。HiPPOとは、Highest Paid Person’s Opinionの略である。
Some authors have called experimentation the “New Imperative for Innovation” (Thomke 2001) and point out that “new technologies are making it easier than ever to conduct complex experiments quickly and cheaply.” We agree and believe that companies can accelerate innovation through experimentation because it is the customers’ experience that ultimately matters, and we should listen to them all the time by running experiments.
一部の著者は、**実験を「イノベーションのための新たな必須条件」（Thomke 2001）と呼び**、"新しいテクノロジーによって、複雑な実験を迅速かつ安価に実施することがかつてないほど容易になっている "と指摘している。**なぜなら、最終的に重要なのは顧客の経験であり、実験を行うことで顧客の声に常に耳を傾けるべきだからだ**。

<!-- ここまで読んだ! -->

# Appendix A

When randomization by user-ID is not appropriate
user-IDによるランダム化が適切でない場合 (実験単位がユーザでないケースの話...??:thinking_face:)

The approach we describe in this paper is to randomly assign users to one group or another and compare these groups of users to determine which experience (i.e. Treatment) is best.
本稿で説明するアプローチは、ユーザをランダムに1つのグループまたは他のグループに割り当て、これらのユーザグループを比較して、どの体験（すなわちTreatment）が最良かを決定することです。
There are some experimentation objectives where this approach will not work.
このアプローチが機能しない実験目的がいくつかあります。
We will describe three of these and alternative approaches to randomization in an online environment.
これらの3つを説明し、オンライン環境でのランダム化の代替アプローチを説明します。

## Control may affect the effectiveness of the Treatment and vice versa コントロールはトリートメントの効果に影響を与える可能性があり、その逆もまた然り

Bidding on Ebay.
Ebayでの入札。
Suppose the Treatment is to give an incentive (perhaps a $5 discount or certain percent off the final bid price) for a user to be the first bidder and no such incentive exists for the Control.
Treatmentがユーザが最初の入札者であるためのインセンティブ（たとえば、最終入札価格から$5割引または一定の割合割引）を与えることであり、Controlにはそのようなインセンティブが存在しないとします。
Assume the success metric (OEC) is the ratio of the final sales price to the minimum bid for each item.
成功メトリック（OEC）は、各アイテムの最終販売価格と最低入札価格の比率であるとします。
If some users have this incentive and others do not, the presence of the Treatment will affect all items so we cannot get a true measure of the effectiveness of making this change.
もし、一部のユーザにこのインセンティブがあり、他のユーザにはない場合、Treatmentの存在はすべてのアイテムに影響を与えるため、この変更を行う効果の真の測定値を得ることはできません。
In this case you can randomly assign one group of items in the auction to be in the Control and the rest to be in the Treatment and compare the OEC for these two groups. i.e. randomly assign the items in the auction, not the users.
この場合、オークションのアイテムの1グループをControlに、残りをTreatmentにランダムに割り当て、これら2つのグループのOECを比較します。**つまり、ユーザではなく、オークションのアイテムをランダムに割り当てます**。(実験単位=アイテムのケースか)

## Not desirable to randomize based on user ユーザに基づいてランダム化することは望ましくない

Price elasticity study.
価格弾力性の研究。
The usual randomization based on user is not desirable because bad customer relations could result if it’s exposed that some customers are getting a different price than other customers (everything else being equal) as Amazon.com discovered when it ran such a study (Weiss 2000).
通常のユーザに基づくランダム化は望ましくないです。なぜなら、Amazon.comがそのような研究を行ったときに発覚したように、他のすべてが同じである場合、一部の顧客が他の顧客と異なる価格を得ていることが明らかになると、悪い顧客関係が生じる可能性があるからです（Weiss 2000）。
Here also, the items involved in the study can be randomly assigned to the Treatment or Control instead of randomizing the users.
ここでも、ユーザをランダム化するのではなく、研究に関与するアイテムをTreatmentまたはControlにランダムに割り当てることができます。

## Not possible to randomize on user ユーザにランダム化することができない

Search Engine Optimization (SEO).
検索エンジン最適化（SEO）。
Most robots do not set cookies so they would not be in any experiment.
ほとんどのロボットはクッキーを設定しないため、実験には含まれません。
If you wanted to conduct a test on robot behavior (e.g. clickthroughs by robots or other) you cannot randomize based on a user ID.
ロボットの動作（たとえば、ロボットによるクリックスルーなど）に関するテストを実施したい場合、ユーザIDに基づいてランダム化することはできません。
Instead you can take groups of pages on your site that are similar and randomly assign pages within each group to Treatment or Control and compare robot behavior for the two groups of pages.
代わりに、類似したサイトのページのグループを取り、各グループ内のページをTreatmentまたはControlにランダムに割り当て、2つのページグループのロボットの動作を比較することができます。
