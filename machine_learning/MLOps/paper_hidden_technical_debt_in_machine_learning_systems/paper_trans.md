## 0.1. link リンク

- https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html

## 0.2. title タイトル

Hidden Technical Debt in Machine Learning Systems
機械学習システムにおける隠れた技術的負債

## 0.3. abstract 抄録

Machine learning offers a fantastically powerful toolkit for building useful complex prediction systems quickly.
機械学習は、有用で複雑な予測システムを素早く構築するための、非常に強力なツールキットを提供する。
This paper argues it is dangerous to think of these quick wins as coming for free.
本稿では、こうした**迅速な勝利がタダで手に入ると考えるのは危険**だと主張する。
Using the software engineering framework of technical debt, we find it is common to incur massive ongoing maintenance costs in real-world ML systems.
**technical debt(技術的負債)というソフトウェア工学のフレームワーク**を用いると、**実世界のMLシステムでは、継続的に莫大なメンテナンスコストが発生するのが一般的**であることがわかる。
We explore several ML-specific risk factors to account for in system design.
我々は、**システム設計において考慮すべきML特有のリスク要因**をいくつか探っている。
These include boundary erosion, entanglement, hidden feedback loops, undeclared consumers, data dependencies, configuration issues, changes in the external world, and a variety of system-level anti-patterns.
これには、boundary erosion（境界の侵食）、entanglement（絡み合い）、hidden feedback loops（隠れたフィードバックループ）、undeclared consumers（未宣言の消費者）、data dependencies（データ依存）、configuration issues（構成問題）、changes in the external world（外界の変化）、さまざまなシステムレベルのアンチパターンが含まれる。

<!-- ここまで読んだ! -->

# 1. Introduction はじめに

As the machine learning (ML) community continues to accumulate years of experience with live systems, a wide-spread and uncomfortable trend has emerged: developing and deploying ML systems is relatively fast and cheap, but maintaining them over time is difficult and expensive.
機械学習(ML) コミュニティがライブシステムでの経験を積み重ねるにつれて、広範囲にわたる不快なトレンドが浮かび上がってきた: **MLシステムの開発(developing)と展開(deploying)は比較的迅速で安価だが、時間の経過とともにそれらを維持することは困難で高価である**。

This dichotomy can be understood through the lens of technical debt, a metaphor introduced by Ward Cunningham in 1992 to help reason about the long term costs incurred by moving quickly in software engineering.
この二律背反は、**technical debt(技術的負債)**というレンズ(=これは隠喩!=metaphor!:thinking:)を通じて理解することができる。この隠喩は、1992年にWard Cunninghamによって導入され、ソフトウェア工学において迅速に進むことによって発生する**長期的なコスト**について考えるのを助けるものである。
As with fiscal debt, there are often sound strategic reasons to take on technical debt.
fiscal debt (財政的負債)と同様に、technical debt(技術的負債)を負う理にかなった戦略的な理由がしばしばある。
Not all debt is bad, but all debt needs to be serviced.
すべての借金が悪いわけではないが、すべての借金は返済する必要がある。
Technical debt may be paid down by refactoring code, improving unit tests, deleting dead code, reducing dependencies, tightening APIs, and improving documentation [8].
技術的負債は、コードのリファクタリング、単体テストの改善、デッドコードの削除、依存関係の削減、APIの強化、ドキュメンテーションの改善によって返済することができる[8]。
The goal is not to add new functionality, but to enable future improvements, reduce errors, and improve maintainability.
**目的は新しい機能を追加することではなく、将来の改良を可能にし、エラーを減らし、保守性を向上させること**である。(つまり、システムの持続可能性を高めること...??:thinking:)
Deferring such payments results in compounding costs.
そのような**支払いを先延ばしすることは、複合的なコストを生む**。(なるほど...!)
Hidden debt is dangerous because it compounds silently.
隠れ借金は無言のうちに膨らむので危険だ。

In this paper, we argue that ML systems have a special capacity for incurring technical debt, because they have all of the maintenance problems of traditional code plus an additional set of ML-specific issues.
この論文では、**MLシステムには技術的負債が発生する特別な能力があると主張する**。なぜなら、MLシステムには、**従来のコードのメンテナンスの問題に加えて、ML特有の問題があるから**である。
This debt may be difficult to detect because it exists at the system level rather than the code level.
この負債は、コード・レベルではなくシステム・レベルに存在するため、検出が困難な場合がある。(ほうほう...?)
Traditional abstractions and boundaries may be subtly corrupted or invalidated by the fact that data influences ML system behavior.
従来のabstractions(抽象化)やboundaries(境界)は、データがMLシステムの挙動に影響を与えるという事実によって、微妙に破壊されたり無効化されたりする可能性がある。
(boundariesって、モジュラー性の向上とか関心の分離とか、ってイメージであってるかな??:thinking:)
Typical methods for paying down code level technical debt are not sufficient to address ML-specific technical debt at the system level.
**コードレベルの技術的負債を返済する一般的な方法は、システムレベルのML特有の技術的負債に対処するには不十分**である。

This paper does not offer novel ML algorithms, but instead seeks to increase the community’s awareness of the difficult tradeoffs that must be considered in practice over the long term.
この論文は、新しいMLアルゴリズムを提供するのではなく、むしろ、実践的に長期的に考慮すべき困難なトレードオフについてコミュニティの意識を高めることを目指している。
We focus on system-level interactions and interfaces as an area where ML technical debt may rapidly accumulate.
我々は、**MLの技術的負債が急速に蓄積される可能性のある領域として、システムレベルの相互作用とインターフェースに焦点を当てている**。
At a system-level, an ML model may silently erode abstraction boundaries.
システムレベルでは、MLモデルは無言のうちに抽象化の境界を侵食するかもしれない。(??)
The tempting re-use or chaining of input signals may unintentionally couple otherwise disjoint systems.
**入力信号の誘惑的な再利用や連鎖は、本来なら分離しているはずのシステムを意図せず結合させてしまうかもしれない**。(特徴量の再利用、みたいな意味??)
ML packages may be treated as black boxes, resulting in large masses of “glue code” or calibration layers that can lock in assumptions.
MLパッケージはブラックボックスとして扱われ、大量の「glue code(接着剤コード)」やキャリブレーション層が結果としてロックインされた仮定を生むかもしれない。

- (以下、この文の解釈):
  - MLパッケージがしばしばブラックボックスとして扱われる。
    - (i.e. MLアルゴリズムやモデルが、内部でどのように動作しているかを完全に理解せずに使用されること)
  - その結果、ユーザは互換性の問題や調整の必要性など、モデルを**他の部分と結合するための追加のコードやレイヤー**を作成する必要が生じる事がある。
    - これらはしばしばglue code(接着剤コード)やcalibration layers(キャリブレーション層)と呼ばれる。
    - (後処理のおまじない的なノルム正規化なども、glue codeに含まれるだろうか...??:thinking:)
  - つまり、**ユーザはモデルの内部動作を十分に理解できない為、その動作に関連する前提条件や仮定を変更する事が難しくなりがち**、という意味。

Changes in the external world may influence system behavior in unintended ways.
外界の変化は、意図しない形でシステムの挙動に影響を与える可能性がある。(ここでの外界の変化って、データの変化とか...??)
Even monitoring ML system behavior may prove difficult without careful design.
**MLシステムの動作を監視することさえ**、注意深く設計しなければ難しいかもしれない。(うん、監視は難しいよね...!:thinking:)

# 2. Complex Models Erode Boundaries 複雑なモデルが境界を侵す

Traditional software engineering practice has shown that strong abstraction boundaries using encapsulation and modular design help create maintainable code in which it is easy to make isolated changes and improvements.
**伝統的なソフトウェア工学の実践では、カプセル化とモジュール設計を使用した強力な抽象化境界(abstraction boundaries)が、維持可能なコードを作成し、単独の変更や改善を行いやすくすることがわかっている**。
(absraction boundariesは、モジュール化、関心の分離、抽象化による情報隠蔽、疎結合など、ソフトウェアの複雑性を管理する為の一連の方法論の意味...?:thinking:)
Strict abstraction boundaries help express the invariants and logical consistency of the information inputs and outputs from an given component [8].
厳密なabstraction boundariesは、与えられたコンポーネントからの情報の入力と出力の不変条件と論理的整合性を表現するのに役立つ[8]。

Unfortunately, it is difficult to enforce strict abstraction boundaries for machine learning systems by prescribing specific intended behavior.
残念なことに、特定の意図された挙動を規定することで、機械学習システムに対して厳密な抽象化境界を強制することは難しい。
Indeed, ML is required in exactly those cases when the desired behavior cannot be effectively expressed in software logic without dependency on external data.
**実際、MLが必要とされるのは、外部データへの依存なしにソフトウェアロジックで効果的に表現できない場合である**。(確かに...!:thinking:)
The real world does not fit into tidy encapsulation.
現実の世界は、整然としたカプセル化には収まらない。
Here we examine several ways that the resulting erosion of boundaries may significantly increase technical debt in ML systems.
ここでは、**境界の侵食(erosion of boundaries)がMLシステムにおける技術的負債を著しく増加させる**いくつかの方法を検討する。

## 2.1. Entanglement. 絡み合い

Machine learning systems mix signals together, entangling them and making isolation of improvements impossible.
機械学習システムは信号を混ぜ合わせ、絡め取り、改善の切り分けを不可能にする。
For instance, consider a system that uses features x1, ...xn in a model.
例えば、特徴量 $x_1, ...x_n$ をモデルで使用するシステムを考えてみましょう。
If we change the input distribution of values in x1, the importance, weights, or use of the remaining n − 1 features may all change.
$x_1$ の値の入力分布を変更すると、残りの n − 1 個の特徴量の重要性、重み、または使用方法がすべて変わるかもしれません。
This is true whether the model is retrained fully in a batch style or allowed to adapt in an online fashion.
これは、モデルがバッチ方式で完全に再学習される場合でも、オンライン方式で適応させられる場合でも同じである。
Adding a new feature xn+1 can cause similar changes, as can removing any feature xj .
新しい特徴 $x_{n+1}$ を追加すると、同様の変更が発生する可能性があり、特徴 $x_j$ を削除することも同様です。
No inputs are ever really independent.
インプットが本当に独立していることはない。(特徴量間の相互作用を完全に排斥してるMLモデルは存在しない、みたいな??:thinking:)
We refer to this here as the CACE principle: Changing Anything Changes Everything.
私たちはこれを「**CACEの原則**」と呼んでいる： **Changing Anything Changes Everything(何かを変えればすべてが変わる)**
CACE applies not only to input signals, but also to hyper-parameters, learning settings, sampling methods, convergence thresholds, data selection, and essentially every other possible tweak.
CACEは、入力信号だけでなく、ハイパーパラメータ、学習設定、サンプリング方法、収束閾値、データ選択、および基本的にすべての可能な調整に適用される。

One possible mitigation strategy is to isolate models and serve ensembles.
可能な緩和策の一つは、モデルを分離してアンサンブルを提供することである。
This approach is useful in situations in which sub-problems decompose naturally such as in disjoint multi-class settings like [14].
このアプローチは、[14]のような離散的なマルチクラス設定のように、サブ問題が自然に分解される状況で有用である。
However, in many cases ensembles work well because the errors in the component models are uncorrelated.
しかし、多くの場合、アンサンブルがうまく機能するのは、コンポーネントモデルの誤差が相関していないためである。
Relying on the combination creates a strong entanglement: improving an individual component model may actually make the system accuracy worse if the remaining errors are more strongly correlated with the other components.
組み合わせに依存することは、強い絡み合いを作り出す: 個々のコンポーネントモデルを改善すると、残りの誤差が他のコンポーネントとより強く相関している場合、システムの精度が悪化する可能性がある。

A second possible strategy is to focus on detecting changes in prediction behavior as they occur.
第二に考えられる戦略は、予測行動の変化が起こったときに、その変化を検出することに焦点を当てることである。(異常検知、みたいな??:thinking:)
One such method was proposed in [12], in which a high-dimensional visualization tool was used to allow researchers to quickly see effects across many dimensions and slicings.
そのような手法の1つが[12]で提案されたもので、高次元の可視化ツールを使用して、研究者が多くの次元とスライスにわたる効果を素早く見ることができるようにした。
Metrics that operate on a slice-by-slice basis may also be extremely useful.
また、スライス単位で評価する指標も非常に有用である。

## 2.2. Correction Cascades. (修正モデルが連鎖的に使用されること!)

There are often situations in which model ma for problem A exists, but a solution for a slightly different problem A′ is required.
問題Aに対するモデル $m_a$ が存在するが、わずかに異なる問題A′の解決策が必要な場合がしばしばある。
In this case, it can be tempting to learn a model m′ a that takes ma as input and learns a small correction as a fast way to solve the problem.
この場合、問題を素早く解く方法として、$m_a$ を入力として受け取り、小さな補正を学習するモデル $m′_a$ を学習することが誘惑されるかもしれない。

However, this correction model has created a new system dependency on ma, making it significantly more expensive to analyze improvements to that model in the future.
**しかし、この補正モデルは、$m_a$ に新しいシステム依存関係を作成し、将来そのモデルの改善を分析するコストが大幅に増加する**。(モデルの使いまわしへの警鐘...??:thinking:)
The cost increases when correction models are cascaded, with a model for problem A′′ learned on top of m′ a , and so on, for several slightly different test distributions.
補正モデルがカスケードされると、問題A′′のモデルが $m′_a$ の上に学習されたり...、また、いくつかのわずかに異なるテスト分布に対してまた別の修正モデルを学習させたり...、など、コストが増加する。
Once in place, a correction cascade can create an improvement deadlock, as improving the accuracy of any individual component actually leads to system-level detriments.
一度設置された修正カスケードは、個々のコンポーネントの精度を向上させることが、実際にはシステムレベルの不利益につながるため、**改善のデッドロックを引き起こす可能性**がある。(MLの各usecaseが密結合になってしまって、あるusecaseの為の変更の影響範囲が大きくなる...??)
Mitigation strategies are to augment ma to learn the corrections directly within the same model by adding features to distinguish among the cases, or to accept the cost of creating a separate model for A′ .
緩和策としては、ケースを区別するための特徴を追加することで、同じモデル内で直接補正を学習するようにmaを増強するか、**$A′$ 用に別のモデルを作成するコストを受け入れること**が考えられる。(後者が無難な気がするな...!:thinking:)
(この話を踏まえると、全usecase共通の基盤モデル、みたいな考え方って結構危ないのかな...??:thinking:)

## 2.3. Undeclared Consumers. 未宣言の消費者

Oftentimes, a prediction from a machine learning model ma is made widely accessible, either at runtime or by writing to files or logs that may later be consumed by other systems.
多くの場合、機械学習モデル $m_a$ からの予測は、実行時に広くアクセス可能になるか(=リアルタイム推論??)、後で他のシステムによって消費される可能性のあるファイルやログに書き込まれる。(=batch推論??)
Without access controls, some of these consumers may be undeclared, silently using the output of a given model as an input to another system.
**アクセス制御を行わなければ、これらのconsumerの中には未宣言のものがいて、特定のモデルの出力を別のシステムの入力として無言で使用しているかもしれない**。(ex. ユーザの埋め込みベクトルを、気づいたらプロダクト内のいろんな機能が使っちゃってた、みたいな??:thinking:)
In more classical software engineering, these issues are referred to as visibility debt [13].
より古典的なソフトウェア工学では、これらの問題は**visibility debt(可視性負債)**と呼ばれる[13]。

Undeclared consumers are expensive at best and dangerous at worst, because they create a hidden tight coupling of model ma to other parts of the stack.
**Undeclared consumers(未宣言の消費者)は、最悪の場合には危険であり、最高の場合でも高価である。なぜなら、$m_a$ とスタックの他の部分との間に隠れた緊密なカップリングを作り出すからである**。
Changes to ma will very likely impact these other parts, potentially in ways that are unintended, poorly understood, and detrimental.
$m_a$ への変更は、これらの他の部分に非常に大きな影響を与える可能性が高く、意図しない、理解不足、有害な方法で影響を与える可能性がある。
In practice, this tight coupling can radically increase the cost and difficulty of making any changes to ma at all, even if they are improvements.
実際には、**この緊密なカップリングは、$m_a$ に対する変更のコストと難しさを根本的に増加させる可能性があり**、たとえそれが改善であっても、$m_a$ に対する変更を行うことが非常に困難になる可能性がある。
(booking.comのsemantic model的なMLの使用って、まさにundeclared consumersだらけだと思うんだけど、この点どうなんだろう...??:thinking:)
Furthermore, undeclared consumers may create hidden feedback loops, which are described more in detail in section 4.
さらに、undecleared consumersは、隠れたフィードバックループを作り出す可能性があり、これについてはセクション4で詳しく説明する。

Undeclared consumers may be difficult to detect unless the system is specifically designed to guard against this case, for example with access restrictions or strict service-level agreements (SLAs).
未宣言の消費者は、アクセス制限や厳格なサービスレベル契約(SLA)など、このケースに対処するためにシステムが特に設計されていない限り、検出が困難である。
(ex. undeclared consumersは意識しないと簡単に作られて、検出も困難だよってこと??:thinking:)
In the absence of barriers, engineers will naturally use the most convenient signal at hand, especially when working against deadline pressures.
障壁がない場合、エンジニアは、特に締め切りのプレッシャーに対処するときに、手元にある最も便利な信号を自然に使用するだろう。

<!-- ここまで読んだ! -->

# 3. Data Dependencies Cost More than Code Dependencies データ依存はコード依存よりもコストがかかる

In [13], dependency debt is noted as a key contributor to code complexity and technical debt in classical software engineering settings.
13]では、**dependency debt(依存負債)が、古典的なソフトウェアエンジニアリングの設定におけるコードの複雑さと技術的負債の主要な要因であると指摘されている**。
We have found that data dependencies in ML systems carry a similar capacity for building debt, but may be more difficult to detect.
私たちは、**MLシステムにおけるデータ依存関係が同様の負債を生む可能性**を持っていることを発見したが、それを検出するのはより困難かもしれない。
Code dependencies can be identified via static analysis by compilers and linkers.
コードの依存関係は、コンパイラーやリンカーによる静的解析によって特定することができる。
Without similar tooling for data dependencies, it can be inappropriately easy to build large data dependency chains that can be difficult to untangle.
データ依存関係に対する同様のツールがない場合、**解きほぐすのが難しい大規模なデータ依存関係チェーンを簡単に構築することができる**。

<!-- ここまで読んだ! -->

## 3.1. Unstable Data Dependencies. 不安定なデータ依存関係。

To move quickly, it is often convenient to consume signals as input features that are produced by other systems.
**素早く進むためには、他のシステムによって生成された入力特徴量として信号を消費することがしばしば便利である**。(うんうん...!:thinking:)
However, some input signals are unstable, meaning that they qualitatively or quantitatively change behavior over time.
しかし、入力信号の中には不安定なものがある。つまり、時間と共に定性的または定量的に挙動が変化するものがある。
This can happen implicitly, when the input signal comes from another machine learning model itself that updates over time, or a data-dependent lookup table, such as for computing TF/IDF scores or semantic mappings.
これは、**入力信号が時間の経過とともに更新される他の機械学習モデル自体から来る場合**や、TF/IDFスコアやセマンティックマッピング(ex. 単語のsemantic埋め込み??)を計算するためのデータ依存ルックアップテーブルのような場合に、暗黙的に発生することがある。
It can also happen explicitly, when the engineering ownership of the input signal is separate from the engineering ownership of the model that consumes it.
また、入力信号のエンジニアリング・オーナーシップが、それを消費するモデルのエンジニアリング・オーナーシップから分離されている場合には、明示的に発生することもある。(signalの変化に気づかないって事??)
In such cases, updates to the input signal may be made at any time.
このような場合、入力信号の更新はいつでも行われる可能性がある。
This is dangerous because even “improvements” to input signals may have arbitrary detrimental effects in the consuming system that are costly to diagnose and address.
**入力信号の「改善」でさえ、診断と対処がコストがかかる消費システムに任意の悪影響をもたらす可能性があるため、これは危険である**。(まあトレードオフだよなぁ...)
For example, consider the case in which an input signal was previously mis-calibrated.
例えば、入力信号が以前に誤ってキャリブレーション(=補正?)されていた場合を考えてみましょう。
The model consuming it likely fit to these mis-calibrations, and a silent update that corrects the signal will have sudden ramifications for the model.
消費されるモデルは、このようなミスキャリブレーションに適合している可能性が高く、**入力信号を修正する無言の更新は、モデルに突然の影響を与える**だろう。

One common mitigation strategy for unstable data dependencies is to create a versioned copy of a given signal.
不安定なデータ依存性に対する一般的な緩和策の一つは、**与えられたsignalのバージョン化コピーを作成すること**である。
For example, rather than allowing a semantic mapping of words to topic clusters to change over time, it might be reasonable to create a frozen version of this mapping and use it until such a time as an updated version has been fully vetted.
たとえば、単語とトピック・クラスターのセマンティック・マッピング(=word-topicのmap??)が時間の経過とともに変化するよりは、**このマッピングの凍結バージョンを作成し、更新バージョンが十分に検証されるまでそれを使用する方が合理的かもしれない**。
Versioning carries its own costs, however, such as potential staleness and the cost to maintain multiple versions of the same signal over time.
しかし、バージョニングには、potentially staleness(=潜在的な古さ?? 信号が現在の状況と合わなくなって劣化してくる、みたいな??:thinking:)や、**時間の経過とともに同じsignalの複数のバージョンを維持するコストなど、独自のコストがかかる。**

## 3.2. Underutilized Data Dependencies. 十分に活用されていないデータ依存関係。

(i.e. あんまり価値のないdata dependencyってこと??)

In code, underutilized dependencies are packages that are mostly unneeded [13].
コードにおいて、**underutilized dependencies(十分に活用されていない依存関係)は、ほとんど不要なパッケージである**[13]。(??)
Similarly, underutilized data dependencies are input signals that provide little incremental modeling benefit.
同様に、underutilized data dependenciesは、ほとんど追加のモデリング上の利益を提供しない入力信号である。
These can make an ML system unnecessarily vulnerable to change, sometimes catastrophically so, even though they could be removed with no detriment.
これらは、**MLシステムを不必要に変更に対して脆弱にする可能性があり**、場合によっては致命的であるが、**これらを削除しても損失はないかもしれない。**

As an example, suppose that to ease the transition from an old product numbering scheme to new product numbers, both schemes are left in the system as features.
例として、古いプロダクト番号schemaから新しいプロダクト番号schemaへの移行を容易にするために、両方のschemaが特徴量としてシステムに残されているとしましょう。
(プロダクト番号schemaって、商品のIDとかのことかな??)
New products get only a new number, but old products may have both and the model continues to rely on the old numbers for some products.
**新製品には新番号のみが付与されるが、古い製品には両方が付与され、モデルは一部の製品について引き続き古い番号に依存している**。
(まさに最近underutilized data dependenciesを解消した気がするな:thinking:)
A year later, the code that stops populating the database with the old numbers is deleted.
1年後、データベースにデータを追加するコードが停止し、古い番号もデータベースから削除される。
This will not be a good day for the maintainers of the ML system.
これは、MLシステムの保守者にとっては良い日ではないだろう。

Underutilized data dependencies can creep into a model in several ways.
underutilized data dependenciesは、いくつかの方法でモデルに潜り込む可能性がある。

- **Legacy Features**.
  The most common case is that a feature F is included in a model early in its development.
  最も一般的なケースは、ある特徴量Fがモデルの開発初期に含まれていることである。
  Over time, F is made redundant by new features but this goes undetected.
  時間の経過とともに、Fは新しい特徴量によって不要になるが、これは検出されない。

- **Bundled Features**.
  Sometimes, a group of features is evaluated and found to be beneficial.
  時には、ある特徴量のグループが評価され、有益であることがわかる。
  Because of deadline pressures or similar effects, all the features in the bundle are added to the model together, possibly including features that add little or no value.
  締め切りのプレッシャーや類似の効果のために、バンドル内のすべての特徴量が一緒にモデルに追加される可能性があり、追加される特徴量の中には、ほとんど価値がないものも含まれるかもしれない。

- $\epsilon$-Features.
  As machine learning researchers, it is tempting to improve model accuracy even when the accuracy gain is very small or when the complexity overhead might be high.
  機械学習の研究者としては、精度の向上が非常に小さい場合や、複雑さのオーバーヘッドが高い場合でも、モデルの精度を向上させることに誘惑される。

- Correlated Features.
  相関する特徴量
  Often two features are strongly correlated, but one is more directly causal.
  多くの場合、2つの特徴量は強く相関しているが、1つはより直接的な因果関係がある。(目的変数と...)
  Many ML methods have difficulty detecting this and credit the two features equally, or may even pick the non-causal one.
  多くのML手法はこれを検出するのが難しく、2つの特徴を同等に評価するか、あるいは非因果的な方を選ぶことさえある。
  This results in brittleness if world behavior later changes the correlations.
  その結果、**世界の振る舞いが後に相関関係を変化させた場合、もろくなる**。

Underutilized dependencies can be detected via exhaustive leave-one-feature-out evaluations.
underutilized dependenciesは、**徹底的なleave-one-feature-out評価によって検出することができる**。(たぶん特徴量を1つずつ取り除いて、その特徴量を取り除いた場合のモデルの性能を評価する、みたいな手法っぽい? 感度解析っぽい?:thinking:)
These should be run regularly to identify and remove unnecessary features.
これらは定期的に実行し、不要な特徴量を特定して削除するべきである。

## 3.3. Static Analysis of Data Dependencies. データ依存の静的解析。

In traditional code, compilers and build systems perform static analysis of dependency graphs.
従来のコードでは、コンパイラとビルドシステムが依存グラフの静的解析を行う。
Tools for static analysis of data dependencies are far less common, but are essential for error checking, tracking down consumers, and enforcing migration and updates.
データの依存関係を静的に分析するツールはあまり一般的ではないが、エラーチェック、**消費者の追跡**、マイグレーションと更新の強制には不可欠である。
One such tool is the automated feature management system described in [12], which enables data sources and features to be annotated.
そのようなツールの1つが、[12]で説明されている自動特徴量管理システムであり、データソースと特徴量にアノテーションを付けることができる。(??)
Automated checks can then be run to ensure that all dependencies have the appropriate annotations, and dependency trees can be fully resolved.
その後、自動チェックを実行して、すべての依存関係に適切なアノテーションがあることを確認し、依存関係ツリーを完全に解決することができる。
This kind of tooling can make migration and deletion much safer in practice.
このようなツールを使えば、マイグレーションや削除をより安全に行うことができる。

<!-- ここまで読んだ! -->

# 4. Feedback Loops フィードバック・ループ

One of the key features of live ML systems is that they often end up influencing their own behavior if they update over time.
ライブMLシステムの重要な特徴の1つは、**時間経過とともに更新されると、しばしば自身の行動に影響を及ぼすことになること**だ。(ex. 推薦モデルの推薦結果を基に得られたログを使って、推薦モデルを学習し直す、みたいな??)
This leads to a form of analysis debt, in which it is difficult to predict the behavior of a given model before it is released.
これは、**analysis debt(分析負債)**の形態につながり、リリース前に特定のモデルの振る舞いを予測することが難しい。(この文献の時点でオフライン評価難しい問題が出てくるのか...!:thinking:)
These feedback loops can take different forms, but they are all more difficult to detect and address if they occur gradually over time, as may be the case when models are updated infrequently.
このようなフィードバックループは、さまざまな形を取ることができる。しかし、モデルがまれに更新される場合に起こるように、時間の経過とともに徐々に発生する場合、これらのフィードバックループは検出および対処がより困難になる。

## 4.1. Direct Feedback Loops. 直接的なフィードバック・ループ。

A model may directly influence the selection of its own future training data.
モデルは、それ自身の将来のトレーニングデータの選択に直接影響を与える可能性がある。(まさに推薦システムとかの例だな...!:thinking:)
It is common practice to use standard supervised algorithms, although the theoretically correct solution would be to use bandit algorithms.
標準的な教師ありアルゴリズムを使うのが一般的だが、**理論的にはバンディットアルゴリズムを使うのが正しい解決策である**。(確かに、そもそもバンディットアルゴリズムはfeedback loopを前提とした手法な気がするし...!:thinking:)
The problem here is that bandit algorithms (such as contextual bandits [9]) do not necessarily scale well to the size of action spaces typically required for real-world problems.
ここで問題となるのは、バンディット・アルゴリズム(例えば、contextual bandits[9])が、通常の実世界の問題に必要なアクション空間のサイズにスケーリングされない可能性があることだ。
It is possible to mitigate these effects by using some amount of randomization [3], or by isolating certain parts of data from being influenced by a given model.
ある程度のランダム化[3]を使用するか、特定のデータの一部を特定のモデルに影響を受けないように分離することで、これらの影響を緩和することができる。(これって教師あり学習を使う場合の緩和策っぽい...??)

## 4.2. Hidden Feedback Loops. 隠れたフィードバック・ループ。

(i.e. indirect feedback loop??)

Direct feedback loops are costly to analyze, but at least they pose a statistical challenge that ML researchers may find natural to investigate [3].
直接的なフィードバック・ループは分析にコストがかかるが、少なくとも、ML研究者が自然に調査する可能性がある統計的な課題を提起する[3]。
A more difficult case is hidden feedback loops, in which two systems influence each other indirectly through the world.
より難しいケースは、**2つのシステムが世界を通じて間接的に互いに影響を与えるhidden feedback loops(隠れたフィードバック・ループ)**である。

One example of this may be if two systems independently determine facets of a web page, such as one selecting products to show and another selecting related reviews.
その一例として、2つのシステムが独立してウェブページの側面を決定する場合がある。1つは表示する商品を選択し、もう1つは関連するレビューを選択する。
Improving one system may lead to changes in behavior in the other, as users begin clicking more or less on the other components in reaction to the changes.
一方のシステムを改善すると、ユーザが変更に反応して他のコンポーネントをクリックする回数が増減するため、他方のシステムの振る舞いが変わる可能性がある。
Note that these hidden loops may exist between completely disjoint systems.
これらのhidden loopsは、完全に独立したシステム間に存在する可能性があることに注意してください。
Consider the case of two stock-market prediction models from two different investment companies.
2つの異なる投資会社の2つの株式市場予測モデルの場合を考えてみよう。
Improvements (or, more scarily, bugs) in one may influence the bidding and buying behavior of the other.
一方の改善（あるいはもっと恐ろしいことにバグ）は、もう一方の入札や購買行動に影響を与えるかもしれない。
(まあ確かに...!)

<!-- ここまで読んだ! -->

# 5. ML-System Anti-Patterns

![]()

Figure 1: Only a small fraction of real-world ML systems is composed of the ML code, as shown by the small black box in the middle. The required surrounding infrastructure is vast and complex.

<!-- このセクションが、有名な図のセクションっぽい...! -->

It may be surprising to the academic community to know that only a tiny fraction of the code in many ML systems is actually devoted to learning or prediction – see Figure 1.
多くのMLシステムにおいて、実際に学習や予測に割り当てられているコードの割合はごくわずかであることを知ることは、学術コミュニティにとって驚くかもしれない。図1を参照。
In the language of Lin and Ryaboy, much of the remainder may be described as “plumbing” [11].
LinとRyaboyの言葉を借りれば、残りの多くは「**plumbing(配管)**」である[11]。

It is unfortunately common for systems that incorporate machine learning methods to end up with high-debt design patterns.
**機械学習の手法を取り入れたシステムが、high-debt(高負債)なデザインパターンで終わることは残念ながら一般的である。**
In this section, we examine several system-design anti-patterns [4] that can surface in machine learning systems and which should be avoided or refactored where possible.
このセクションでは、機械学習システムで表面化する可能性があり、可能な限り回避またはリファクタリングされるべき、いくつかのシステム設計のアンチパターン[4]を検証する。

## 5.1. Glue Code. (接着剤コード)

ML researchers tend to develop general purpose solutions as self-contained packages.
MLの研究者は、自己完結型のパッケージとして汎用的なソリューションを開発する傾向がある。
A wide variety of these are available as open-source packages at places like mloss.org, or from in-house code, proprietary packages, and cloud-based platforms.
mloss.orgのようなオープンソースのパッケージや、社内コード、プロプライエタリなパッケージ、クラウドベースのプラットフォームから、さまざまなものが利用可能である。
Using generic packages often results in a glue code system design pattern, in which a massive amount of supporting code is written to get data into and out of general-purpose packages.
**汎用パッケージを使用すると、多くの場合、汎用パッケージにデータを入力および出力するために大量のサポートコードが書かれた、グルーコード・システム設計パターンが生じる**。
Glue code is costly in the long term because it tends to freeze a system to the peculiarities of a specific package; testing alternatives may become prohibitively expensive.
**グルーコードは、長期的にはコストがかかる。なぜなら、特定のパッケージの特異性にシステムを凍結させる傾向があるためであり、代替手段のテストは非常に高価になる可能性がある。**
In this way, using a generic package can inhibit improvements, because it makes it harder to take advantage of domain-specific properties or to tweak the objective function to achieve a domain-specific goal.
このように、汎用パッケージを使用することは、改善を妨げる可能性がある。なぜなら、ドメイン固有の特性を活用したり、目的関数を調整してドメイン固有の目標を達成することが難しくなるからである。
Because a mature system might end up being (at most) 5% machine learning code and (at least) 95% glue code, it may be less costly to create a clean native solution rather than re-use a generic package.
成熟したシステムは、(最大で)5%が機械学習コードであり、(最低で)95%がグルーコードである可能性があるため、汎用パッケージを再利用するよりも、クリーンなネイティブソリューションを作成する方がコストがかからないかもしれない。

An important strategy for combating glue-code is to wrap black-box packages into common API’s.
**グルーコードに対抗するための重要な戦略は、ブラックボックス・パッケージを共通のAPIにwrapすること**である。(共通のInterfaceをもたせたFacadeパターン的な??)
This allows supporting infrastructure to be more reusable and reduces the cost of changing packages.
これにより、サポートインフラをより再利用しやすくし、パッケージの変更にかかるコストを削減することができる。

## 5.2. Pipeline Jungles. (パイプライン・ジャングル)

(時間の経過や特徴量の追加とともに複雑化し、管理が難しくなったデータ処理pipelineのことっぽい...?:thinking:)

As a special case of glue code, pipeline jungles often appear in data preparation.
glue codeの特殊なケースとして、**pipeline junglesは、データ準備においてしばしば現れる**。(**学習pipelineにおける前処理がめっちゃ生い茂ってしまう**、みたいなイメージ...??:thinking:)(元データとMLモデルを接着させるための処理だから、gule codeの一種なのかな...!:thinking:)
These can evolve organically, as new signals are identified and new information sources added incrementally.
これらは、新しいシグナルが特定され、新しい情報源が段階的に追加されるにつれて、有機的に進化することがある。
Without care, the resulting system for preparing data in an ML-friendly format may become a jungle of scrapes, joins, and sampling steps, often with intermediate files output.
**注意を払わないと、MLに適したフォーマットでデータを準備するシステムは、しばしば中間ファイルが出力されるスクレイプ、結合、サンプリングステップのジャングルになるかもしれない**。
Managing these pipelines, detecting errors and recovering from failures are all difficult and costly [1].
これらのパイプラインを管理し、エラーを検出し、障害から回復することは、すべて困難でコストがかかる[1]。
Testing such pipelines often requires expensive end-to-end integration tests.
このようなパイプラインのテストには、高価なエンド・ツー・エンドの統合テストが必要になることが多い。
All of this adds to technical debt of a system and makes further innovation more costly.
**これらはすべて、システムのtechnical debtを増やし、さらなる革新をより高価にする**。

Pipeline jungles can only be avoided by thinking holistically about data collection and feature extraction.
パイプラインのジャングルは、データ収集と特徴量抽出について全体的(総体的)に考えることでのみ回避することができる。(=要は、システム全体を総合的に考えないとだめだよってこと??)
The clean-slate approach of scrapping a pipeline jungle and redesigning from the ground up is indeed a major investment of engineering effort, but one that can dramatically reduce ongoing costs and speed further innovation.
パイプライン・ジャングルを廃棄し、ゼロから設計し直す**clean-slateアプローチ**(=要は、一から作りなおすこと??)は、確かにエンジニアリング努力の大きな投資であるが、継続的なコストを大幅に削減し、さらなる革新を加速させることができる。

Glue code and pipeline jungles are symptomatic of integration issues that may have a root cause in overly separated “research” and “engineering” roles.
glue codeとpipeline junglesは、**過度に分離された「研究」と「エンジニアリング」の役割に原因がある**可能性がある統合の問題の症状である。
When ML packages are developed in an ivorytower setting, the result may appear like black boxes to the teams that employ them in practice.
MLパッケージが象牙の塔(=俗世間から離れた場所??)のような環境で開発された場合、それを実際に使用するチームにとってはブラックボックスのように見えるかもしれない。
A hybrid research approach where engineers and researchers are embedded together on the same teams (and indeed, are often the same people) can help reduce this source of friction significantly [16].
**エンジニアと研究者が同じチームに一緒に組み込まれる(もしくは同じ人であることも多い)ような、ハイブリッド研究アプローチは、この摩擦の原因を大幅に減らすのに役立つ**[16]。(ふむふむ...!うちは大丈夫だ...!)

## 5.3. Dead Experimental Codepaths. 死んだ実験的コードパス。

A common consequence of glue code or pipeline jungles is that it becomes increasingly attractive in the short term to perform experiments with alternative methods by implementing experimental codepaths as conditional branches within the main production code.
glue codeやpipeline junglesの一般的な結果は、実験的なコードパスを、本番コード内の条件付きブランチとして実装することで、代替手法で実験を行うことがますます魅力的になっていくことである。
(ここでの"ブランチ"は、リポジトリ内のブランチの意味ではなく、PipelineのDAGの中の条件分岐のブランチの意味っぽい...!:thinking:)
(**要は、glue codeやpipeline junglesを放置していくほど、条件分岐で実験を行う事がますます魅力的になっていく**、みたいな...!:thinking:)
For any individual change, the cost of experimenting in this manner is relatively low—none of the surrounding infrastructure needs to be reworked.
個々の変更であれば、この方法で実験するコストは比較的低い。周囲のインフラストラクチャを再設計する必要はない。
However, over time, these accumulated codepaths can create a growing debt due to the increasing difficulties of maintaining backward compatibility and an exponential increase in cyclomatic complexity.
しかし、**時間の経過とともに(短期的には良さそうだが...!)**、これらの蓄積されたコードパスは、後方互換性の維持の困難さと、cyclomatic complexityの指数関数的な増加による成長する負債を生み出す可能性がある。
("後方互換性の維持の困難さ" = 新しい特徴量や変更を条件分岐で加える度に、古いコードとの互換性を保つ事が困難になる。ex. 新しいver.では必要なハイパーパラメータが、古いver.では必要ない、とか...?:thinking:)
(cyclomatic complexityの指数関数的な増加 = 条件分岐が増えると、コードの複雑さが指数関数的に増加する。これは、コードのパスの総数が増える事を意味し、コードを理解、テスト、デバッグするのが難しくなる...!:thinking:)
Testing all possible interactions between codepaths becomes difficult or impossible.
コードパス間で起こりうるすべての相互作用をテストすることは困難か不可能になる。
A famous example of the dangers here was Knight Capital’s system losing $465 million in 45 minutes, apparently because of unexpected behavior from obsolete experimental codepaths [15].
このような危険性の有名な例は、**Knight Capitalのシステムが45分で4億6500万ドルを失ったことであり、これは、時代遅れの実験的なコードパスから予期しない振る舞いが発生したため**のようだ[15]。(こわい...!:thinking:)

As with the case of dead flags in traditional software [13], it is often beneficial to periodically reexamine each experimental branch to see what can be ripped out.
**従来のソフトウェアにおけるデッドフラグ[13]の場合と同様に、実験ブランチを定期的に再検査し、何が取り除けるかを確認することは、しばしば有益**である。(うんうん...!:thinking:)
(**dead flags** = 以前に導入されたがもはや使用されていない、役にたたなくなったフラグ(設定optionや機能のオンオフを切り替える為の変数)。これらはしばしば、古い機能、実験的な機能、あるいは廃止された機能と関連していて、コードベース内に残留している。ふむふむ、ありそう...!:thinking:)
Often only a small subset of the possible branches is actually used; many others may have been tested once and abandoned.
多くの場合、実際に使用されるのは可能なブランチのごく一部だけで、他の多くのブランチは一度テストされただけで放棄されているかもしれない。

## 5.4. Abstraction Debt. 抽象化負債。

The above issues highlight the fact that there is a distinct lack of strong abstractions to support ML systems.
上記の問題は、**MLシステムをサポートする強力な抽象化が不足している**という事実を浮き彫りにしている。
Zheng recently made a compelling comparison of the state ML abstractions to the state of database technology [17], making the point that nothing in the machine learning literature comes close to the success of the relational database as a basic abstraction.
Zheng氏は最近、**MLの抽象化の状態をデータベース技術の状態と比較し、機械学習文献には、基本的な抽象化としてのリレーショナルデータベースの成功に匹敵するものはないと**指摘している[17]。
(確かに、データベースの抽象化は、SQLという共通の言語を使って、データの操作を行う事ができる。これにより、データの操作方法が統一され、データの操作が容易になる。このような共通の言語がないと、データの操作方法がバラバラになり、データの操作が困難になる...!:thinking:)
What is the right interface to describe a stream of data, or a model, or a prediction?
**データストリーム、モデル、予測を記述するための適切なインターフェースは何か**?

For distributed learning in particular, there remains a lack of widely accepted abstractions.
特に分散学習に関しては、広く受け入れられる抽象化が不足している。
It could be argued that the widespread use of Map-Reduce in machine learning was driven by the void of strong distributed learning abstractions.
機械学習でMap-Reduceが広く使われるようになったのは、強力な分散学習の抽象化がなかったからだと言える。
(Map-Reduce = 並列処理と分散処理を行う為のプログラミングモデル。Map関数とReduce関数を使って、大規模なデータセットを分割して処理する。必ずしも複雑なMLモデルの学習などに最適化されているわけではないらしい。)
Indeed, one of the few areas of broad agreement in recent years appears to be that Map-Reduce is a poor abstraction for iterative ML algorithms.
実際、近年広く合意されている数少ない領域の1つは、**Map-Reduceが反復的なMLアルゴリズムにとっては不適切な抽象化である**ということのようだ。

The parameter-server abstraction seems much more robust, but there are multiple competing specifications of this basic idea [5, 10].
parameter-serverの抽象化は、はるかに堅牢に見えるが、この基本的なアイデアには複数の競合仕様がある[5, 10]。
(パラメーターサーバ = 分散学習において、モデルのパラメータを一元管理するためのサーバ。)
The lack of standard abstractions makes it all too easy to blur the lines between components.
標準的な抽象概念がないため、コンポーネント間の境界線が曖昧になりやすい。

## 5.5. Common Smells. (一般的な匂い?)

In software engineering, a design smell may indicate an underlying problem in a component or system [7].
ソフトウェア工学では、design smell(?)はコンポーネントやシステムの根本的な問題を示すことがある[7]。
(**design smell** = ソフトウェア設計における問題点を指し示す可能性のある、コードやシステムの特徴やパターン、らしい。design smellは、ソフトウェアの設計が一般的な設計原則やベストプラクティスから逸脱している可能性を示す...!:thinking:)
(ソフトウェアの文脈では"不吉な匂い"みたいな言葉が一般的っぽい...!)
We identify a few ML system smells, not hard-and-fast rules, but as subjective indicators.
私たちは、いくつかのMLシステムの匂いを、厳密なルールではなく、主観的な指標として特定する。

- **Plain-Old-Data Type Smell**. (平易なデータ型の匂い?)
  The rich information used and produced by ML systems is all to often encoded with plain data types like raw floats and integers.
  MLシステムで使用される豊富な情報は、しばしば生の浮動小数点数や整数などのplainな(平易な?)データ型でエンコードされている。
  In a robust system, a model parameter should know if it is a log-odds multiplier or a decision threshold, and a prediction should know various pieces of information about the model that produced it and how it should be consumed.
  ロバストシステムでは、モデルパラメータは、対数オッズの乗数か決定閾値かを知っているべきであり、予測は、それを生成したモデルについてのさまざまな情報と、どのように消費されるべきかを知っているべきである。

  - (以下、解釈):
    - この問題は、システムが生の浮動小数点数や整数など、**単純なデータ型を使って複雑な情報を表現してしまっている状況**を指す。
      - ->**システム内で使用される値が持つ意味やcontextが失われ、プログラムの理解や保守が困難になってしまう...!**
    - MLモデルのパラメータや出力値は、単に数値として扱われがちだが、それぞれ特定の意味を持っている。
      - パラメータ = 対数オッズ乗数(ex. ロジスティック回帰のパラメータ)や決定閾値(ex. treeモデルのパラメータ)
      - 予測結果 = 生成されたモデルに関する情報や、どのように消費されるべきかについての情報を持っているべき。あと埋め込み表現なのか、確率なのか、とか??:thinking:
    - 具体的な解決策としては...
      - **より具体的なデータ型やクラスを定義して使用する**と、プログラムの意図をより明確に伝える事ができ、コードの可読性と保守性がup upする...!:smile:
      - ex. モデルパラメータクラスを用意し、パラメータクラスや使用方法に関する情報を保持する、とか?

- Multiple-Language Smell.
  (多言語の匂い?)
  It is often tempting to write a particular piece of a system in a given language, especially when that language has a convenient library or syntax for the task at hand.
  特定のシステムの一部を特定の言語で書くことは、しばしば魅力的である。特に、その言語が手元のタスクに便利なライブラリや構文を持っている場合。
  However, using multiple languages often increases the cost of effective testing and can increase the difficulty of transferring ownership to other individuals.
  しかし、複数の言語を使用することは、効果的なテストのコストを増やすことが多く、他の個人に所有権を移転する難しさを増加させる可能性がある。

- Prototype Smell.
  プロトタイプの匂い。
  It is convenient to test new ideas in small scale via prototypes.
  プロトタイプを通じて新しいアイデアを小規模にテストするのは便利だ。
  However, regularly relying on a prototyping environment may be an indicator that the full-scale system is brittle, difficult to change, or could benefit from improved abstractions and interfaces.
  しかし、**定期的にプロトタイピング環境に依存することは、フルスケールのシステムが壊れやすい、変更が難しい、または改善された抽象化とインターフェースを活用できる可能性があることを示す指標かもしれない**。
  Maintaining a prototyping environment carries its own cost, and there is a significant danger that time pressures may encourage a prototyping system to be used as a production solution.
  プロトタイピング環境の維持にはそれなりのコストがかかり、時間的なプレッシャーがプロトタイピング・システムをプロダクション・ソリューションとして使用することを促す危険性が大きい。
  (**これって、ABテストのコストが高いから、オフライン実験を行って良かったモデルを、そのまま本番環境に全体適用してしまう、みたいな事かな...?**:thinking:)
  Additionally, results found at small scale rarely reflect the reality at full scale.
  さらに、小規模で発見された結果が、フルスケールでの現実を反映することはほとんどない。

<!-- ここまで読んだ! -->

# 6. Configuration Debt コンフィギュレーション・デット

Another potentially surprising area where debt can accumulate is in the configuration of machine learning systems.
負債が蓄積される可能性のあるもう一つの驚くべき分野は、機械学習システムのconfigurationである。
Any large system has a wide range of configurable options, including which features are used, how data is selected, a wide variety of algorithm-specific learning settings, potential pre- or post-processing, verification methods, etc.
どんな大規模なシステムでも、使用する特徴量、データの選択方法、さまざまなアルゴリズム固有の学習設定、前処理や後処理、検証方法など、**幅広い設定オプションがある**。
We have observed that both researchers and engineers may treat configuration (and extension of configuration) as an afterthought.
私たちは、**研究者もエンジニアも、configuration(およびconfigurationの拡張)を二の次に扱うことがある**と観察している。
Indeed, verification or testing of configurations may not even be seen as important.
実際、configurationの検証やテストは、重要でないとさえ考えられないかもしれない。
In a mature system which is being actively developed, the number of lines of configuration can far exceed the number of lines of the traditional code.
**活発に開発されている成熟したシステムでは、configurationの行数が従来のコードの行数をはるかに上回ることがある**。
Each configuration line has a potential for mistakes.
それぞれのコンフィギュレーション・ラインには間違いの可能性がある。

Consider the following examples.
次の例を考えてみよう。
Feature A was incorrectly logged from 9/14 to 9/17.
特徴量 A は、9/14から9/17まで誤ってログされていた。
Feature B is not available on data before 10/7.
特徴量 B は、10/7以前のデータでは利用できない。
The code used to compute feature C has to change for data before and after 11/1 because of changes to the logging format.
特徴量Cを計算するために使用されるコードは、ログフォーマットの変更のため、11/1以前と以降のデータで変更しなければならない。
Feature D is not available in production, so a substitute features D′ and D′′ must be used when querying the model in a live setting.
特徴量 D は本番環境では利用できないため、ライブ設定でモデルをクエリする際には、代替特徴量 D' と D'' を使用しなければならない。
If feature Z is used, then jobs for training must be given extra memory due to lookup tables or they will train inefficiently.
特徴量 Z を使用する場合、トレーニング用のジョブには、ルックアップテーブルのために余分なメモリが必要であり、効率的にトレーニングされない。
Feature Q precludes the use of feature R because of latency constraints.
特徴量 Q は、遅延制約のため、特徴量 R の使用を妨げる。

All this messiness makes configuration hard to modify correctly, and hard to reason about.
このようなゴチャゴチャしたものは、configurationを正しく変更することが難しく、理解することも難しくなる。
However, mistakes in configuration can be costly, leading to serious loss of time, waste of computing resources, or production issues.
**しかし、configurationのミスはコストがかかる可能性があり、時間の大幅な損失、コンピューティングリソースの無駄遣い、本番環墮の問題を引き起こす可能性がある**。
This leads us to articulate the following principles of good configuration systems:
このことから、**優れたconfigurationシステムの原則**を次のように明確にすることができる：

- 1. It should be easy to specify a configuration as a small change from a previous configuration.
     以前のconfigurationからの小さな変更としてconfigurationを指定することは簡単であるべき。
- 2. It should be hard to make manual errors, omissions, or oversights.
     手作業によるエラーや脱落、見落としをすることが発生しづらいべき。
- 3. It should be easy to see, visually, the difference in configuration between two models.
     2つのモデルの構成の違いは、視覚的に容易に確認できるべき。
- 4. It should be easy to automatically assert and verify basic facts about the configuration: number of features used, transitive closure of data dependencies, etc.
     **configurationに関する基本的な事実を自動的にassertし、検証することが容易**であるべき：使用される特徴量の数、データ依存関係の推移閉包など。
- 5. It should be possible to detect unused or redundant settings.
     使用されていない設定や冗長な設定を検出することができるべき。
- 6. Configurations should undergo a full code review and be checked into a repository
     configurationは、完全なコードレビューを受け、リポジトリにチェックインされるべき。

<!-- ここまで読んだ! -->

# 7. Dealing with Changes in the External World 外界の変化への対応

One of the things that makes ML systems so fascinating is that they often interact directly with the external world.
MLシステムの魅力のひとつは、しばしば外界と直接相互作用することだ。(外界から得られたデータを使って継続的に学習するから。これは)
Experience has shown that the external world is rarely stable.
経験上、外界が安定していることはほとんどない。
This background rate of change creates ongoing maintenance cost.
このbackground rate of change(=外界の変化率??)は、継続的なメンテナンスコストを生み出す。

## 7.1. Fixed Thresholds in Dynamic Systems. 動的システムにおける固定閾値。

It is often necessary to pick a decision threshold for a given model to perform some action: to predict true or false, to mark an email as spam or not spam, to show or not show a given ad.
与えられたモデルが何らかのアクションを実行するために、決定的なしきい値を選択する必要があることがしばしばある: ex. 真または偽を予測するため、メールをスパムまたはスパムでないとマークするため、特定の広告を表示するかどうかを決定するため。
One classic approach in machine learning is to choose a threshold from a set of possible thresholds, in order to get good tradeoffs on certain metrics, such as precision and recall.
機械学習における古典的なアプローチの1つは、特定のメトリクス(適合率や再現率など)において良いトレードオフを得るために、可能なしきい値のセットからしきい値を選択することである。
However, such thresholds are often manually set.
しかし、**そのような閾値は手動で設定されることが多い**。
Thus if a model updates on new data, the old manually set threshold may be invalid.
**したがって、モデルが新しいデータで更新された場合、手動で設定した古いしきい値は無効になる可能性がある**。
Manually updating many thresholds across many models is time-consuming and brittle.
多くのモデルで多くのしきい値を手動で更新するのは時間がかかり、もろい。
One mitigation strategy for this kind of problem appears in [14], in which thresholds are learned via simple evaluation on heldout validation data.
この種の問題に対する1つの緩和策が[14]にあり、そこでは、しきい値は、ホールドアウトされた検証データに対する単純な評価によって学習される。
(定期的にグリッドサーチで自動で閾値を更新しますよ、っこと??:thinking:)

## 7.2. Monitoring and Testing. モニタリングとテスト。

Unit testing of individual components and end-to-end tests of running systems are valuable, but in the face of a changing world such tests are not sufficient to provide evidence that a system is working as intended.
個々のコンポーネントの単体テストや、稼働中のシステムのend-to-endテストは価値があるが、変化する世界に直面している中で、そのようなテストは、システムが意図した通りに機能していることを証明するのに十分ではない。
(MLシステムのテストが難しい話?:thinking:)
Comprehensive live monitoring of system behavior in real time combined with automated response is critical for long-term system reliability.
**システムの挙動をリアルタイムで包括的にライブ監視し、自動応答を組み合わせることは、長期的なシステムの信頼性にとって重要**である。
The key question is: what to monitor? Testable invariants are not always obvious given that many ML systems are intended to adapt over time.
**重要な問題は 何を監視するのか**？ ということである。**多くのMLシステムは時間とともに適応することを意図しているため、Testable invariants(テスト可能な不変条件)が常に明らかであるわけではない**。
We offer the following starting points.
我々は次のような出発点を提供する。

- **Prediction Bias**.
  予測バイアス。
  In a system that is working as intended, it should usually be the case that the distribution of predicted labels is equal to the distribution of observed labels.
  意図した通りに機能しているシステムでは、通常、予測されたラベルの分布が観測されたラベルの分布と等しいことが多いはずである。(=これはbooking.comの論文でいうところの応答分布分析か...!:thinking:)
  This is by no means a comprehensive test, as it can be met by a null model that simply predicts average values of label occurrences without regard to the input features.
  **これは決して包括的なテストではない。**入力特徴に関係なく、単にラベル出現の平均値を予測するnullモデルでも満たすことができるからだ。(うんうん...!:thinking:)
  However, it is a surprisingly useful diagnostic, and changes in metrics such as this are often indicative of an issue that requires attention.
  **しかし、これは驚くほど有用な診断であり、このようなメトリクスの変化は、注意を要する問題の兆候であることが多い**。(なるほど...! この指標を最適化しようとするのはだめだけど、この指標が悪くなったら何か問題があるかもしれない、という事か...!:thinking:)
  For example, this method can help to detect cases in which the world behavior suddenly changes, making training distributions drawn from historical data no longer reflective of current reality.
  例えば、この方法は、世界の振る舞いが突然変化し、過去のデータから引き出されたトレーニング分布が現在の現実を反映しなくなった場合を検出するのに役立つ。
  Slicing prediction bias by various dimensions isolate issues quickly, and can also be used for automated alerting.
  さまざまな次元で予測バイアスをスライスすることで、問題を迅速に分離し、自動アラートにも使用できる。(ex. 地域、時間帯、ユーザセグメントなどで、応答分布の偏りの変化を監視する、みたいな??:thinking:)

- **Action Limits**.
  行動制限。
  In systems that are used to take actions in the real world, such as bidding on items or marking messages as spam, it can be useful to set and enforce action limits as a sanity check.
  アイテムへの入札やメッセージをスパムとしてマークするなど、実世界でアクションを起こすために使われるシステムでは、**sanity check(=正気か否かのチェック**??:thinking:)として行動制限を設定し、強制することが有用である。
  (ex. 自動入札システムでは、入札件数を制限する。自動スパムチェックでは、スパムとしてマークするメッセージの件数を制限する、みたいな...?:thinking:)
  These limits should be broad enough not to trigger spuriously.
  これらの制限は、誤ってトリガーされないように広く設定されるべきである。(i.e. 不必要にアラートが発生しないように...!)
  If the system hits a limit for a given action, automated alerts should fire and trigger manual intervention or investigation.
  システムが特定のアクションの制限に達した場合、自動アラートが発生し、手動介入や調査がトリガーされるべきである。
- **Up-Stream Producers**.
  Data is often fed through to a learning system from various upstream producers.
  データは多くの場合、様々な上流のproducersから学習システムに供給される。
  These up-stream processes should be thoroughly monitored, tested, and routinely meet a service level objective that takes the downstream ML system needs into account.
  **これらのアップストリームプロセスは、徹底的に監視され、テストされ、ダウンストリームのMLシステムのニーズを考慮に入れたサービスレベル目標を定期的に満たすべき**である。(入力データの変化やバグを検知したい、みたいな??:thinking:)
  Further any up-stream alerts must be propagated to the control plane of an ML system to ensure its accuracy.
  さらに、**アップストリームでのアラートは、MLシステムのコントロールプレーンに伝播して、その正確性を確保する必要がある**。
  Similarly, any failure of the ML system to meet established service level objectives be also propagated down-stream to all consumers, and directly to their control planes if at all possible.
  **同様に、MLシステムが確立されたサービスレベル目標を満たすことができなかった場合も、ダウンストリームですべてのconsumersに伝わり**、可能であれば直接consumersのコントロールプレーンに伝わります。

Because external changes occur in real-time, response must also occur in real-time as well.
**外部からの変化はリアルタイムで起こるため、対応もリアルタイムでなければならない。**
Relying on human intervention in response to alert pages is one strategy, but can be brittle for time-sensitive issues.
アラートページに対する人間の介入に頼るのも一つの戦略だが、一刻を争う問題にはもろい。
Creating systems to that allow automated response without direct human intervention is often well worth the investment.
**人間が直接介入することなく自動応答を可能にするシステムを構築することは、多くの場合、投資に値する**。

<!-- ここまで読んだ! -->

# 8. Other Areas of ML-related Debt その他のML関連債務

We now briefly highlight some additional areas where ML-related technical debt may accrue.
ここで、MLに関連する技術的負債が発生する可能性のある追加的な領域をいくつか簡単に紹介する。

## 8.1. Data Testing Debt. データテストの負債。

If data replaces code in ML systems, and code should be tested, then it seems clear that some amount of testing of input data is critical to a well-functioning system.
もし、MLシステムにおいてデータがコードに置き換わり、コードをテストすべきであるとすれば、いくつかの**入力データのテストが、システムがうまく機能するためには重要**であることは明らかだ。(コードもデータも重要なんだったら、コードもデータも退行をテストすべきだよね...!みたいな話??:thinking:)
Basic sanity checks are useful, as more sophisticated tests that monitor changes in input distributions.
基本的なサニティ・チェックは、入力分布の変化を監視する、より洗練されたテストと同様に有用である。

## 8.2. Reproducibility Debt. 再現性の負債。

As scientists, it is important that we can re-run experiments and get similar results, but designing real-world systems to allow for strict reproducibility is a task made difficult by randomized algorithms, non-determinism inherent in parallel learning, reliance on initial conditions, and interactions with the external world.
科学者として、実験を再実行して似た結果を得ることができることは重要である。しかし、ランダム化されたアルゴリズム、並列学習に固有の非決定性、初期条件への依存、外界との相互作用など、厳密な再現性を許容するための実世界のシステムの設計は困難な課題である。
(ex. いろんな条件があるから、常にCTR=20%を再現しているわけじゃないよ、みたいな??:thinking:)

## 8.3. Process Management Debt. プロセス管理負債。

Most of the use cases described in this paper have talked about the cost of maintaining a single model, but mature systems may have dozens or hundreds of models running simultaneously [14, 6].
**本稿で説明したユースケースのほとんどは、単一のモデルを維持するコストについて述べてきたが、成熟したシステムでは、数十から数百のモデルが同時に実行される可能性がある**[14, 6]。
This raises a wide range of important problems, including the problem of updating many configurations for many similar models safely and automatically, how to manage and assign resources among models with different business priorities, and how to visualize and detect blockages in the flow of data in a production pipeline.
これには、多くの類似したモデルのために多くのconfigurationを安全かつ自動的に更新する問題、異なるビジネスの優先順位を持つモデル間でリソースを管理および割り当てる方法、本番パイプラインのデータフローにおけるブロックを視覚化し、検出する方法など、幅広い重要な問題が発生する。
Developing tooling to aid recovery from production incidents is also critical.
プロダクション・インシデントからの復旧を支援するツールの開発も重要だ。
An important system-level smell to avoid are common processes with many manual steps.
**避けるべき重要なsystem-level smellは、多くの手作業ステップを持つ共通プロセスである**。 (運用を自動化すべきってこと?)

## 8.4. Cultural Debt.

(=MLの研究とエンジニアリングの間に存在し得る、協力よりも対立を生じさせがちな文化的な境界、みたいな!)

There is sometimes a hard line between ML research and engineering, but this can be counter-productive for long-term system health.
ML研究とエンジニアリングの間には、時に厳しい境界線があるが、これは長期的なシステムの健康にとって逆効果となることがある。
It is important to create team cultures that reward deletion of features, reduction of complexity, improvements in reproducibility, stability, and monitoring to the same degree that improvements in accuracy are valued.
**精度の向上が評価されるのと同じ程度に、特徴量の削除、複雑さの削減、再現性、安定性、モニタリングの向上を報酬とするチーム文化を作り出すことが重要**である。(うんうん...!:thinking:)
In our experience, this is most likely to occur within heterogeneous teams with strengths in both ML research and engineering.
我々の経験では、これ(=上記のpositiveなチーム文化)は、ML研究とエンジニアリングの両方の強みを持つ異種チーム内で最も発生させやすい。(よしよし...!:thinking:)

<!-- ここまで読んだ! -->

# 9. Conclusions: Measuring Debt and Paying it Off 結論 負債の測定と返済

Technical debt is a useful metaphor, but it unfortunately does not provide a strict metric that can be tracked over time.
技術的負債は有用なメタファー(隠喩)だが、残念ながら、長期にわたって追跡できる厳密な指標を提供するものではない。(定量評価できないから??)
How are we to measure technical debt in a system, or to assess the full cost of this debt? Simply noting that a team is still able to move quickly is not in itself evidence of low debt or good practices, since the full cost of debt becomes apparent only over time.
**システムの技術的負債をどのように測定し、この負債の全体的なコストを評価するのか?** チームがまだ素早く動くことができるということだけが、低い負債や良い実践の証拠となるわけではない。なぜなら、負債の全体的なコストは時間の経過とともに明らかになるからだ。
Indeed, moving quickly often introduces technical debt.
実際、素早く動くことは、しばしば技術的負債を生む。
A few useful questions to consider are:
考慮すべき有益な質問をいくつか挙げよう：

- How easily can an entirely new algorithmic approach be tested at full scale?
  まったく新しいアルゴリズムのアプローチを、どの程度簡単にフルスケールでテストできるか？
- What is the transitive closure of all data dependencies?
  すべてのデータ依存関係のtransitive closure(=推移閉包?)は何か??
  - (メモ) transitive closure(推移閉包) = グラフ理論における、要素間の全ての直接的及び間接的な接続のこと。
  - よって、技術的負債の文脈でのこの質問は、**システム内の全てのデータ依存関係の直接的及び間接的な接続をちゃんと理解できているか否か、ちゃんと答えられる程度にデータ依存関係が少ない事が重要**だよ、みたいな意図???:thinking:
- How precisely can the impact of a new change to the system be measured?
  システムに対する新たな変更の影響をどの程度正確に測定できるか？
- Does improving one model or signal degrade others?
  あるモデルや信号を改善すると、他のモデルや信号が劣化するのか？
- How quickly can new members of the team be brought up to speed?
  チームの新しいメンバーをいかに早くスピードアップさせることができるか？

We hope that this paper may serve to encourage additional development in the areas of maintainable ML, including better abstractions, testing methodologies, and design patterns.
本稿が、より保守可能なMLの分野での追加の開発を奨励することに役立つことを願っている。これには、より良い抽象化、テスト方法論、デザインパターンが含まれる。
Perhaps the most important insight to be gained is that technical debt is an issue that engineers and researchers both need to be aware of.
**おそらく得られる最も重要な洞察は、技術的負債は、エンジニアと研究者の両方が認識している必要がある問題である**ということだ。
Research solutions that provide a tiny accuracy benefit at the cost of massive increases in system complexity are rarely wise practice.
**システムの複雑さを大幅に増大させる代償として、微小な精度の利益を提供する研究ソリューションは、滅多に賢明な実践ではない**。(うんうん...!:thinking:)
Even the addition of one or two seemingly innocuous data dependencies can slow further progress.
一見何の問題もなさそうなデータの依存関係が1つか2つ追加されただけでも、その後の進展が遅れる可能性がある。

Paying down ML-related technical debt requires a specific commitment, which can often only be achieved by a shift in team culture.
ML関連の技術的負債を返済するには、特定のコミットメントが必要であり、これはしばしばチーム文化の変化によってのみ達成されることがある。
Recognizing, prioritizing, and rewarding this effort is important for the long term health of successful ML teams.
この努力を認識し、優先し、報酬を与えることは、成功したMLチームの長期的な健康にとって重要である。

<!-- ここまで読んだ! -->
