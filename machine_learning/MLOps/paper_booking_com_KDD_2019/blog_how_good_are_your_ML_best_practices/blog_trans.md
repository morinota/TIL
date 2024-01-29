## link リンク

https://booking.ai/how-good-are-your-ml-best-practices-fd7722262437
https://booking.ai/how-good-are-your-ml-best-practices-fd7722262437

# How good are your ML best practices? MLのベストプラクティスはどの程度か？

## Introduction 

In Software engineering, best practices serve as an important part of the discussion on how to develop good quality software, which can be easily maintained, scaled, extended, and tested.
ソフトウェア工学では、ベストプラクティスは、保守、拡張、テストが容易な良質なソフトウェアを開発する方法に関する議論の重要な一翼を担っている。
Why do we mention maintenance, scalability, extendability or testing? These are only a few of the possible attributes you might wish to consider when defining quality for your particular software product.
なぜメンテナンス、スケーラビリティ、拡張性、テストに言及するのでしょうか？これらは、あなたが特定のソフトウェア製品の品質を定義する際に考慮したい可能性のある属性のほんの一部に過ぎません。
There are many more, and they heavily depend on your use case.
他にもたくさんあるが、それらはあなたのユースケースに大きく依存する。
Machine Learning Systems pose their own specific challenges, that is why we developed a Quality Model for machine learning.
機械学習システムには特有の課題があり、そのため私たちは機械学習のための品質モデルを開発した。

Having defined the quality model and attributes of interest, we can start thinking about what best practices we can apply, to cover these attributes.
品質モデルと関心のある属性を定義したら、これらの属性をカバーするために、どのようなベストプラクティスを適用できるかを考え始めることができる。
The list of possible best practices one might apply is extensive, and there are many resources available such as [3], [4], [5].
適用可能なベストプラクティスのリストは広範囲に及び、[3]、[4]、[5]など多くのリソースが利用可能である。
These lists can seem overwhelming, and in reality not all of them can be always applied to the fullest extent.
これらのリストには圧倒されるように思えるかもしれないし、現実にはそのすべてが常に最大限に適用できるわけではない。
It usually is required to prioritise one over the other, and there has been little discussion on how to perform such prioritisation.
通常、どちらかに優先順位をつけることが求められるが、その優先順位のつけ方についてはほとんど議論されてこなかった。
Additionally a single practice can contribute to many attributes, so how can we choose the right combination of best practices to cover the attributes we need to fulfil.
さらに、ひとつのプラクティスが多くの属性に貢献することもある。では、満たすべき属性をカバーするために、ベストプラクティスの適切な組み合わせを選ぶにはどうすればいいのか。

For example, if you had to choose only 5 of best practices from [3], which would you choose and why, given your constraints and requirements? To answer this question, we propose a framework to prioritise best practices.
例えば、[3]からベストプラクティスを5つだけ選ばなければならないとしたら、制約や要件がある中で、どれを選び、なぜ選ぶのか？この問いに答えるために、ベストプラクティスに優先順位をつけるフレームワークを提案する。

## The elements of the prioritisation framework 優先順位決定フレームワークの要素

The goal of applying best practices is to improve the quality of your ML system.
ベストプラクティスを適用する目的は、MLシステムの質を向上させることである。
But how do we define quality?
しかし、品質をどのように定義すればいいのだろうか？

The standard approach to define quality in software is the use of Quality Models.
ソフトウェアの品質を定義する標準的なアプローチは、品質モデルの使用である。
“A quality model provides the framework towards a definition of quality” [1].
「品質モデルは、品質の定義に向けた枠組みを提供する」[1]。
It is the set of characteristics and the relationships between them that provides the basis for specifying quality requirements and evaluation [2].
品質要件と評価を規定するための基礎となるのは、特性の集合とそれらの間の関係である[2]。
There does not exist a Quality Model for Machine Learning Systems, that’s why we introduced our own.
機械学習システムのための品質モデルは存在しない。

Once the Quality Model is defined and we understand what attributes (sub-characteristics in our model) of software we need to cover, we need a set of best practices which we can apply.
品質モデルが定義され、私たちがカバーする必要があるソフトウェアの属性（私たちのモデルではサブ特性）を理解したら、私たちは適用できる一連のベストプラクティスを必要とする。
Adopting a best practice can bring us closer to solving a particular sub-characteristic, or it can completely solve it — it depends on the best practice and the extent to which it has been implemented.
ベストプラクティスを採用することで、特定の下位特性の解決に近づくこともあれば、完全に解決することもある。
For example, writing complete documentation with all the important assumptions made during the development of an ML system can fully solve Understandability but can also improve Repeatability since documentation makes it easier to repeat the lifecycle of a given ML system
例えば、MLシステムの開発中に行われた全ての重要な仮定を含む完全なドキュメントを書くことは、理解可能性を完全に解決することができますが、ドキュメントを書くことで与えられたMLシステムのライフサイクルを繰り返すことが容易になるため、再現可能性も改善することができます。

The extent of implementation and the number of best practices we can afford to implement depends on the designated effort budget and desired quality coverage, something that varies a lot between projects.
どの程度のベストプラクティスを導入するか、また導入できるベストプラクティスの数は、指定された労力予算と希望する品質範囲によって決まる。

We built a list of best practices from external resources such as [3], [4], [5] and surveyed our Machine Learning community and conducted interviews with practitioners, to find out which best practices are used in our company.
私たちは、[3]、[4]、[5]などの外部リソースからベスト・プラクティスのリストを作成し、機械学習コミュニティを調査し、実践者にインタビューを行い、社内でどのベスト・プラクティスが使われているかを調べました。

## Quality Model meets Best Practices 品質モデルはベストプラクティスを満たす

Once the Quality Model has been built and the list of best practices has been established, the missing link is the relationship between each quality model sub-characteristic and the individual best practices.
品質モデルが構築され、ベストプラクティスのリストが確立された後、欠落しているリンクは、各品質モデルのサブ特性と個々のベストプラクティスとの関係である。
To give an example, if we remove all redundant features from our Machine Learning System , do we solve the Accuracy of the system? Does testability improve? Does our system scale better, or is it easier to Monitor? To answer these questions, we need a mapping from a (sub-characteristic, best practice) pair to a number that represents how much the sub-characteristic benefits from the best-practice.
例を挙げると、機械学習システムから冗長な特徴をすべて取り除いた場合、システムの精度は向上するか？テスト性は向上するか？システムのスケールは向上するのか、モニターは容易になるのか？これらの質問に答えるためには、（サブ特性、ベストプラクティス）のペアから、そのサブ特性がベストプラクティスからどれだけ恩恵を受けるかを表す数値へのマッピングが必要です。
We decided to use a scale of 0–4, where 0 means that a particular sub-characteristic has no relevance to a given best practice, and 4 means that a particular sub-characteristic is covered (meaning that is completely addressed) by a given best practice.
0～4の尺度を用いることにした。0は、ある特定の下位特性が、あるベストプラクティスと関連性がないことを意味し、4は、ある特定の下位特性が、あるベストプラクティスによってカバーされている（完全に対処されていることを意味する）ことを意味する。
We assume the scores are additive.
得点は加法的であると仮定する。
If a sub-characteristic is covered, i.e.we apply best practices whose contributions sum up to 4, we assume more work on this particular sub-characteristic is not necessary.
あるサブ特性がカバーされている場合、すなわち貢献度の合計が4となるベストプラクティスを適用している場合、この特定のサブ特性に関するさらなる作業は必要ないと仮定する。

## Score elicitation スコアの引き出し

To obtain the scores for the (sub-characteristic, best practice) pairs , we organised a training for experienced machine learning practitioners (machine learning scientists, and engineers) on the quality model and best practices to make sure both are well understood and then asked them for scores for each possible (sub-characteristic, best practice) pair.
(サブ特性、ベストプラクティス)のペアのスコアを得るために、経験豊富な機械学習の実務者(機械学習科学者、エンジニア)を対象に、品質モデルとベストプラクティスに関するトレーニングを実施し、両者が十分に理解されていることを確認し、可能性のある(サブ特性、ベストプラクティス)の各ペアのスコアを求めた。
To verify that these scores are consistent, we computed inter-annotator agreement, which proved a good agreement between the practitioners (see section 4.3 Inter-annotator Agreement in our paper).
これらのスコアが一貫していることを検証するために、我々は注釈者間の一致を計算し、実務者間の良好な一致を証明した（我々の論文の4.3節注釈者間の一致を参照）。
The final relationship of a (sub-characteristic, best practice) is computed using a statistic of the collected scores such as mean or median.
サブ特性、ベストプラクティス）の最終的な関係は、平均値や中央値など、収集されたスコアの統計値を用いて計算される。

## Which practices should I choose? どの練習を選ぶべきか？

Having obtained the relationship between a quality model and best practices, we can solve the problem of which practices should I select, given a budget expressed in the number of practices and a subset of quality sub-characteristics (we might be interested in not solving all of them, e.g.a proof of concept system might not care about scalability).
品質モデルとベストプラクティスの関係を得たことで、プラクティスの数と品質サブ特性のサブセットで表される予算が与えられた場合、どのプラクティスを選択すべきかという問題を解くことができる（例えば、概念実証システムはスケーラビリティを気にしないかもしれない）。

​​The objective of our optimization problem is to choose a subset of practices that maximizes the coverage of the quality model under a budget constraint.
我々の最適化問題の目的は、予算制約の下で品質モデルのカバー率を最大化するような診療のサブセットを選択することである。

## Optimisation algorithms 最適化アルゴリズム

To solve the optimization problem of finding the set of practices that maximises the quality coverage we consider 2 algorithms: a) brute force and b) greedy.
品質カバレッジを最大化するプラクティスのセットを見つけるという最適化問題を解くために、2つのアルゴリズムを検討する： a)総当り、b)貪欲。
The brute force algorithm very quickly leads to a combinatorial explosion of the search space even for a small number of practices and budget, hence in practice we use the greedy algorithm for which we found that rarely yields sub-optimal results and is much faster.
ブルートフォース・アルゴリズムは、少ない練習回数と予算であっても、すぐに探索空間の組み合わせ論的爆発につながるため、実際には貪欲なアルゴリズムを使用する。
You can find the exact algorithms in our paper.
正確なアルゴリズムは我々の論文に掲載されている。

## Applications アプリケーション

Ok, we have a framework that we can use to score and prioritize best practices.
よし、ベストプラクティスの採点と優先順位付けに使えるフレームワークができた。
But what can we do with it? Below we provide three applications of the framework which helped us get a better understanding of ML best practices.
しかし、それを使って何ができるのだろうか？以下に、MLのベストプラクティスの理解を深めるのに役立った、フレームワークの3つの応用例を示す。

### #1: Analyzing sets of best practices #1: ベストプラクティスの分析

An application of our framework is to analyze sets of best practices.
私たちのフレームワークの応用例として、ベストプラクティスのセットを分析することがある。
Given a set of practices, we can score each practice against each quality sub-characteristic and then visualize the total contributions of the sub-characteristics to assess which sub-characteristics receive a lot of attention and which are underrepresented.
一組のプラクティスが与えられたら、それぞれのプラクティスを各品質のサブ特性に対して採点し、サブ特性の貢献度の合計を可視化することで、どのサブ特性が注目され、どのサブ特性が過小評価されているかを評価することができる。

We do this exercise for the internal set of 41 practices that we apply at Booking.com and we can see the results in the figure below.
Booking.comで適用している41の社内プラクティスについてこの演習を行い、その結果を下図に示す。
In the figure we marked the threshold k=24 contribution points which we used for indicating if a sub-characteristic is covered (for more details refer to the Section 4.2 of the paper).
図では、あるサブキャラクターがカバーされているかどうかを示すために使用した閾値k=24の寄与点をマークした（詳細については、論文のセクション4.2を参照）。

From the figure we see that while most of the sub-characteristics are covered, there are a few which are not, such as standards-compliance, scalability or discoverability.
図から、ほとんどのサブ特性がカバーされている一方で、標準準拠、拡張性、発見可能性など、カバーされていないものもいくつかあることがわかる。
This insight helped us identify gaps in our set of practices and helped us create new ones that can address those gaps.
この洞察は、私たちの一連のプラクティスにおけるギャップを特定し、それらのギャップに対処できる新しいプラクティスを生み出すのに役立った。
We also got our first learning:
初めての習い事もした：

Learning #1: We can identify gaps in sets of practices, by analyzing their coverage on each quality sub-characteristic.
学習その1： 各品質のサブ特性に関するカバー率を分析することで、一連のプラクティスにおけるギャップを特定することができる。

Some examples of practices that we created are:
私たちが生み出した練習の例をいくつか挙げよう：

To address the gap in Vulnerability, we created an ML security inspection process and we created a practice called “Request an ML system security inspection”.
脆弱性のギャップを解決するために、私たちはMLのセキュリティ検査プロセスを作り、「MLシステムのセキュリティ検査を依頼する」というプラクティスを作りました。

To address the gap in Responsiveness, we created the practice: “Latency and throughput requirements are defined”, which means that the model builder should be aware of latency and throughput requirements when developing.
Responsivenessのギャップに対処するために、私たちはプラクティスを作成しました： 「これは、モデルビルダーが開発時にレイテンシとスループットの要件を意識することを意味します。

To address the gap in Discoverability, we created the practice: “Register the ML system in an accessible registry” and we made sure that all the systems are being registered and visible.
ディスカバビリティのギャップに対処するため、私たちはプラクティスを作成した： 「MLシステムをアクセス可能なレジストリに登録し、すべてのシステムが登録され、可視化されていることを確認しました。

We also did this exercise using 3 open source sets of practices ([3], [4], [5]) and we found that while each set in isolation covers only a subset of the sub-characteristics, when combined, they complement each other! You can find the details in our paper.
私たちはまた、3つのオープンソースのプラクティスセット（[3]、[4]、[5]）を使用してこの演習を行い、各セットが単独ではサブ特性のサブセットしかカバーしていない一方で、組み合わせると互いに補完し合うことがわかりました！詳細は論文でご覧いただけます。

### #2: Assessing how many practices are enough #2: 十分な練習量を評価する

The second exercise we did is to find how many practices are needed in order to maximize the quality coverage.
私たちが行った2つ目の練習は、質の高いカバレッジを最大化するために必要な練習の数を見つけることである。
To do this, we combined the 3 open source with the internal set of practices (after removing those that overlap) and we ended up with 101 practices in total.
そのため、3つのオープンソースと社内のプラクティスを組み合わせ（重複するものを除外した後）、合計101のプラクティスを作成した。
We then find the top N practices from the combined set using our greedy algorithm, for N increasing from 1 to 101, and compute the coverage percentage for each N, which we plot in the figure below.
次に、Nが1から101まで増加するように、貪欲なアルゴリズムを使用して、結合されたセットから上位Nのプラクティスを見つけ、各Nに対するカバー率を計算し、下図にプロットする。

We find that by applying 5 practices, we already cover 40% of the sub-characteristics, 10 practices cover 70% and 24 are needed to cover 96% which is the maximum (we do not reach 100% because discoverability is never fully covered even if we combine all the sets).
5つのプラクティスを適用することで、すでにサブ特性の40％をカバーし、10のプラクティスで70％をカバーし、最大値である96％をカバーするためには24のプラクティスが必要であることがわかった（すべてのセットを組み合わせても、発見性が完全にカバーされることはないため、100％には達しない）。
This means that by using 24 practices, we achieve a similar result in terms of quality as with 101 practices! This is because many practices overlap in terms of the quality attributes they contribute to, which leads us to our second learning:
つまり、24のプラクティスを使用することで、101のプラクティスを使用した場合と品質面で同様の結果が得られるということである！これは、多くのプラクティスが、貢献する品質属性において重複しているためである：

Learning #2: When applying the right set of practices, we can achieve a significant reduction in the effort of adoption!
学習その2： 適切なプラクティスを適用すれば、採用の労力を大幅に削減できる！

#3: Identifying the best of the best practices
#3: ベストプラクティスを見極める

Since we can identify how many practices are enough to maximize the quality coverage, we can also find which are actually those practices.
質の高いカバレッジを最大化するのに十分な練習の数を特定することができるため、実際にそのような練習を行っているのはどの練習なのかを見つけることもできる。
To do this, we run the greedy algorithm using as budget 24 practices, and we find that the ones the set which maximizes coverage is the following:
そのために、24の実践を予算として貪欲なアルゴリズムを実行し、カバレッジを最大化するセットが以下のものであることを発見する：

Versioning for Data, Model, Configurations and Scripts [5]
データ、モデル、コンフィギュレーション、スクリプトのバージョン管理 [5］

Continuously Monitor the Behaviour of Deployed Models [5]
導入モデルの挙動を継続的に監視する [5］

Unifying and automating ML workflow [4]
MLワークフローの統一化と自動化 [4］

Remove redundant features [3]
冗長な機能を削除する [3］

Continuously Measure Model Quality and Performance [5]
モデルの品質とパフォーマンスを継続的に測定する [5］

All input feature code is tested [3]
入力された機能コードはすべてテストされる[3]。

Automate Model Deployment [5]
モデル展開の自動化 [5］

Use of Containarized Environment [6]
コンテナ化された環境の利用 [6］

Unified Environment for all Lifecycle Steps [6]
すべてのライフサイクルステップのための統一環境 [6］

Enable Shadow Deployment [5]
シャドー展開の有効化 [5］

The ML system outperforms a simple baseline [3]
MLシステムは、単純なベースライン[3]よりも優れている。

Have Your Application Audited [5]
アプリケーションの監査 [5］

Monitor model staleness [3]
モデルの陳腐化を監視する [3］

Use A Collaborative Development Platform [5]
共同開発プラットフォームの利用 [5］

Explain Results and Decisions to Users [5]
結果と決定をユーザーに説明する [5］

The ML system has a clear owner [6]
MLシステムには明確なオーナーがいる[6]。

Assign an Owner to Each Feature and Document its Rationale [5]
各フィーチャーに所有者を割り当て、その根拠を文書化する [5] 。

Computing performance has not regressed [3]
コンピューティング性能は後退していない [3] 。

Communicate, Align, and Collaborate With Others [5]
他者とのコミュニケーション、連携、協働 [5］

Perform Risk Assessments [5]
リスクアセスメントの実施 [5］

Peer Review Training Scripts [5]
ピアレビュー・トレーニング・スクリプト [5］

Establish Responsible AI Values [5]
責任あるAIバリューの確立 [5］

Write documentation about the ML system [6]
MLシステムに関するドキュメントを書く [6］

Write Modular and Reusable Code [6]
モジュラーで再利用可能なコードを書く [6］

Using this set we can narrow down which practices we should prioritize pushing forward in our organization in order to ensure holistic quality coverage and avoid the adoption of practices aiming at the same goals.
このセットを使えば、全体的な品質カバーを確保し、同じゴールを目指すプラクティスの採用を避けるために、組織で優先的に推進すべきプラクティスを絞り込むことができる。
We should note though that to create this optimal set, we considered equal importance for each sub-characteristic and the same adoption effort per practice, so we advise careful adoption of this set with consideration of your organization’s needs.
しかし、この最適なセットを作成するために、各サブ特性の重要度を等しくし、1つの実践につき同じ採用努力をすることを考慮した。
For example, if safety is top priority, practices focusing on robustness should be prioritized.
例えば、安全性を最優先するのであれば、堅牢性に焦点を当てた練習を優先すべきである。
This takes us to our last learning:
これが最後の学習につながる：

Learning #3: The optimal set of practices for an organization is possible to be specified, however it depends on the exact organization’s needs.
学習その3： 組織にとって最適なプラクティスのセットを特定することは可能であるが、それは組織のニーズによって異なる。

## Conclusion 結論

Adopting practices at random or based on their popularity is sub-optimal since each practice targets different quality sub-characteristics and in many cases they overlap.
それぞれのプラクティスが異なる品質サブ特性を対象としており、多くの場合、それらは重複しているため、無作為に、あるいはその人気に基づいてプラクティスを採用することは最適とは言えない。
Due to this, we implemented a framework to analyze and prioritize machine learning practices and we used it to identify gaps in the practices we have adopted at Booking.com.
このため、機械学習のプラクティスを分析し、優先順位をつけるためのフレームワークを導入し、Booking.comで採用しているプラクティスのギャップを特定するために使用しました。
We also found that even though there is a proliferation of machine learning best practices, only a few are needed to achieve high coverage of all quality aspects.
また、機械学習のベストプラクティスは数多く存在するが、すべての品質面を高いレベルでカバーするために必要なものはごくわずかであることもわかった。

If you want to learn more, you can read our full paper at and you can also use the code of the framework in our Github page.
さらに詳しくお知りになりたい方は、私たちの論文の全文をご覧ください。
We are always more than happy to discuss any thoughts or feedback on the framework, so don’t hesitate to reach out.
フレームワークに関するご意見やご感想は、いつでも喜んでお伺いいたしますので、遠慮なくご連絡ください。