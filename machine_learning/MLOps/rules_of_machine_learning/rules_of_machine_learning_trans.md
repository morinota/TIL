refs: https://developers.google.com/machine-learning/guides/rules-of-ml

# Rules of Machine Learning 機械学習のルール

- On this page このページでは
- Terminology 用語
- Overview 概要
- Before Machine Learning 機械学習の前に
- ML Phase I: Your First Pipeline MLフェーズI: あなたの最初のパイプライン
  - Monitoring 監視
  - Your First Objective あなたの最初の目標
- ML Phase II: Feature Engineering MLフェーズII: 特徴量エンジニアリング
  - Human Analysis of the System システムの人間による分析
  - Training-Serving Skew トレーニングとサービングのずれ
- ML Phase III: Slowed Growth, Optimization Refinement, and Complex Models MLフェーズIII: 成長の鈍化、最適化の洗練、複雑なモデル
- Related Work 関連研究
- Acknowledgements 謝辞
- Appendix 付録
  - YouTube Overview YouTubeの概要
  - Google Play Overview Google Playの概要
  - Google Plus Overview Google Plusの概要
- YouTube Overview YouTubeの概要
- Google Play Overview Google Playの概要
- Google Plus Overview Google Plusの概要

## AI-generated Key Takeaways AI生成された主なポイント(LLMが要約したやつ)

- Prioritize building robust infrastructure and simple models before incorporating complex machine learning algorithms.  
  **複雑な機械学習アルゴリズムを取り入れる前に、堅牢なインフラとシンプルなモデルの構築を優先してください**。

- Leverage existing heuristics and domain knowledge to enhance model performance and system intuition.  
  既存のヒューリスティックやドメイン知識を活用して、モデルのパフォーマンスとシステムの直感を向上させてください。

- Continuously iterate and refine models through feature engineering and addressing potential pitfalls like training-serving skew.  
  特徴量エンジニアリングを通じてモデルを継続的に反復し洗練させ、トレーニングとサービングのずれのような潜在的な落とし穴に対処してください。

- Align machine learning objectives with measurable product goals and prioritize long-term user satisfaction.  
  **機械学習の目標を測定可能な製品目標と整合させ、長期的なユーザー満足を優先**してください。

- Explore new data sources and features when performance plateaus, considering user relationships and external information.  
  パフォーマンスが停滞した際には、新しいデータソースや特徴を探求し、ユーザーの関係や外部情報を考慮してください。

<!-- ここまで読んだ! -->

# Best Practices for ML Engineering 最良のMLエンジニアリングの実践
Martin Zinkevich マーチン・ジンケビッチ

This document is intended to help those with a basic knowledge of machine learning get the benefit of Google's best practices in machine learning. 
この文書は、機械学習の基本的な知識を持つ人々が、Googleの機械学習における最良の実践を活用できるようにすることを目的としています。
It presents a style for machine learning, similar to the Google C++ Style Guide and other popular guides to practical programming. 
これは、Google C++スタイルガイドや他の人気のある実用的なプログラミングガイドに似た、機械学習のスタイルを提示します。
If you have taken a class in machine learning, or built or worked on a machine-learned model, then you have the necessary background to read this document. 
もしあなたが機械学習のクラスを受講したり、機械学習モデルを構築または作業したことがあるなら、この文書を読むための必要な背景を持っています。

<!-- ここまで読んだ! -->

## Terminology 用語

The following terms will come up repeatedly in our discussion of effective machine learning:
効果的な機械学習に関する議論で繰り返し登場する用語は以下の通りです。

- Instance: The thing about which you want to make a prediction. 
  - インスタンス: 予測を行いたい対象のこと。例えば、インスタンスは「猫について」または「猫についてではない」と分類したいウェブページかもしれません。

- Label: An answer for a prediction task either the answer produced by a machine learning system, or the right answer supplied in training data. 
  - ラベル: 予測タスクのための答え。機械学習システムによって生成された答え、またはトレーニングデータに提供された正しい答えのいずれかです。例えば、ウェブページのラベルは「猫について」かもしれません。

- Feature: A property of an instance used in a prediction task. 
  - 特徴量: 予測タスクで使用されるインスタンスの特性。例えば、ウェブページには「'cat'という単語を含む」という特徴があるかもしれません。

- Feature Column: A set of related features, such as the set of all possible countries in which users might live. An example may have one or more features present in a feature column. "Feature column" is Google-specific terminology. A feature column is referred to as a "namespace" in the VW system (at Yahoo/Microsoft), or a field.
  - 特徴量列: 関連する特徴量の集合。例えば、**ユーザーが住んでいる可能性のあるすべての国の集合**などです。例は、特徴列に1つ以上の特徴を持つことがあります。「特徴列」はGoogle特有の用語です。特徴列は、VWシステム（Yahoo/Microsoft）では「namespace」と呼ばれ、afieldとも呼ばれます。(これって結局multivarentな特徴量のこと？:thinking:)

- Example: An instance (with its features) and a label. 
  - 例: インスタンス（その特徴を含む）とラベル。

- Model: A statistical representation of a prediction task. 
  - モデル: 予測タスクの統計的表現。例を用いてモデルをトレーニングし、そのモデルを使用して予測を行います。

- Metric: A number that you care about. May or may not be directly optimized. 
  - メトリック: あなたが重要視する数値。直接最適化される場合もあれば、されない場合もあります。

- Objective: A metric that your algorithm is trying to optimize. 
  - 目的: あなたのアルゴリズムが最適化しようとしているメトリック。

- Pipeline: The infrastructure surrounding a machine learning algorithm. 
  - パイプライン: 機械学習アルゴリズムを取り巻くインフラストラクチャ。フロントエンドからデータを収集し、トレーニングデータファイルに格納し、1つ以上のモデルをトレーニングし、モデルを本番環境にエクスポートすることを含みます。

- Click-through Rate: The percentage of visitors to a web page who click a link in an ad. 
  - クリック率: ウェブページの訪問者のうち、広告のリンクをクリックする割合。

<!-- ここまで読んだ! -->

## Overview 概要

To make great products:
素晴らしい製品を作るためには：
**do machine learning like the great engineer you are, not like the great
machine learning expert you aren’t.**
**あなたが優れたエンジニアであるように機械学習を行い、あなたが優れた機械学習の専門家でないように行わないでください**。

Most of the problems you will face are, in fact, engineering problems. 
実際、あなたが直面する問題のほとんどはエンジニアリングの問題です。
Even with all the resources of a great machine learning expert, most of the gains
come from great features, not great machine learning algorithms. 
**優れた機械学習の専門家のすべてのリソースを持っていても、ほとんどの利益は優れた特徴量から得られ、優れた機械学習アルゴリズムからは得られません。**

So, the basic approach is:
したがって、基本的なアプローチは次のとおりです：

1. Make sure your pipeline is solid end to end.
   1. パイプラインがエンドツーエンドで堅牢であることを確認してください。
2. Start with a reasonable objective.
   1. 妥当な目標から始めてください。
4. Add common-sense features in a simple way.
   1. 常識的な特徴をシンプルな方法で追加してください。
5. Make sure that your pipeline stays solid.
   1. パイプラインが堅牢であり続けることを確認してください。

This approach will work well for a long period of time. 
このアプローチは長期間にわたってうまく機能します。
Diverge from this approach only when there are no more simple tricks to get you any farther. 
これ以上の進展を得るためのシンプルなトリックがなくなったときだけ、このアプローチから逸脱してください。
Adding complexity slows future releases.
複雑さを追加すると、将来のリリースが遅くなります。

Once you've exhausted the simple tricks, cutting-edge machine learning might
indeed be in your future. 
シンプルなトリックを使い果たしたら、最先端の機械学習があなたの未来にあるかもしれません。
See the section on Phase III machine learning projects.
フェーズIIIの機械学習プロジェクトに関するセクションを参照してください。

This document is arranged as follows:
この文書は次のように構成されています：
1. The first part should help you understand whether
the time is right for building a machine learning system.
1. 最初の部分は、機械学習システムを構築するのに適した時期かどうかを理解するのに役立ちます。
2. The second part is about deploying your
first pipeline.
2. 第二部は、最初のパイプラインを展開することについてです。
3. The third part is about launching and
iterating while adding new features to your pipeline, how to evaluate models
and training-serving skew.
3. 第三部は、パイプラインに新しい機能を追加しながら立ち上げと反復を行うこと、モデルの評価方法、トレーニングとサービングのずれについてです。
4. The final part is about what to do when you reach a plateau.
4. 最後の部分は、停滞に達したときに何をすべきかについてです。
5. Afterwards, there is a list of related work and an appendix with some
background on the systems commonly used as examples in this document.
その後、関連する作業のリストと、この文書で一般的に例として使用されるシステムに関する背景情報を含む付録があります。

<!-- ここまで読んだ! -->

## Before Machine Learning 機械学習の前に  

#### Rule #1: Don’t be afraid to launch a product without machine learning.　ルール #1: 機械学習なしで製品を立ち上げることを恐れないでください。  

Machine learning is cool, but it requires data.  
機械学習は魅力的ですが、データが必要です。  
Theoretically, you can take data from a different problem and then tweak the model for a new product, but this will likely underperform basicheuristics.  
理論的には、異なる問題からデータを取得し、新しい製品のためにモデルを調整することができますが、これは基本的なヒューリスティックに劣る可能性が高いです。  
If you think that machine learning will give you a 100% boost, then a heuristic will get you 50% of the way there.  
もし機械学習が100%の向上をもたらすと考えているなら、ヒューリスティックは50%のところまで到達させてくれます。  
For instance, if you are ranking apps in an app marketplace, you could use the install rate or number of installs as heuristics.  
例えば、アプリマーケットプレイスでアプリをランキングする場合、インストール率やインストール数をヒューリスティックとして使用できます。  
If you are detecting spam, filter out publishers that have sent spam before.  
スパムを検出する場合、以前にスパムを送信した出版社を除外してください。  
Don’t be afraid to use human editing either.  
人間の編集を使用することを恐れないでください。  
If you need to rank contacts, rank the most recently used highest (or even rank alphabetically).  
もし連絡先をランク付けする必要があるなら、最も最近使用したものを最上位にランク付けするか（またはアルファベット順にランク付けしてください）。  
If machine learning is not absolutely required for your product, don't use it until you have data.  
**もし機械学習があなたの製品に絶対に必要でないなら、データが得られるまで使用しないでください。**

<!-- ここまで読んだ! -->

#### Rule #2: First, design and implement metrics. 

Before formalizing what your machine learning system will do, track as much as possible in your current system. 
まず、機械学習システムが何をするかを正式に定義する前に、現在のシステムでできるだけ多くのことを追跡してください。
Do this for the following reasons: 
以下の理由からこれを行ってください：

1. It is easier to gain permission from the system’s users earlier on. 
   1. システムのユーザーから早期に許可を得る方が簡単です。
2. If you think that something might be a concern in the future, it is better to get historical data now. 
   1. 将来的に何かが懸念事項になる可能性があると思うなら、今のうちに履歴データを取得する方が良いです。
3. If you design your system with metric instrumentation in mind, things will go better for you in the future. 
   1. メトリックの計測を考慮してシステムを設計すれば、将来的に物事がうまくいくでしょう。
    Specifically, you don’t want to find yourself grepping for strings in logs to instrument your metrics! 
    具体的には、メトリックを計測するためにログ内の文字列をgrepするような状況にはなりたくありません！

4. You will notice what things change and what stays the same. 
   1. 何が変わり、何が変わらないかに気づくでしょう。
    For instance, suppose you want to directly optimize one-day active users. 
    例えば、1日あたりのアクティブユーザーを直接最適化したいとします。
    However, during your early manipulations of the system, you may notice that dramatic alterations of the user experience don’t noticeably change this metric.
    しかし、システムの初期操作中に、ユーザー体験の劇的な変更がこのメトリックに明らかな変化をもたらさないことに気づくかもしれません。

Google Plus　team measures expands per read, reshares per read, plusones per read, comments/read, comments per user, reshares per user, etc. which they use in computing the goodness of a post at serving time. 
Google Plus　teamは、読み取りごとの拡張、読み取りごとの再共有、読み取りごとのプラスワン、コメント/読み取り、ユーザーごとのコメント、ユーザーごとの再共有などを測定し、投稿の良さを計算する際に使用します。
Also, note that an experiment framework, in which you can group users into buckets and aggregate statistics by experiment, is important. 
**また、ユーザーをバケットにグループ化し、実験ごとに統計を集計できる実験フレームワークが重要**です。
See Rule #12. 
ルール#12を参照してください。

<!-- ここまで読んだ! -->

By being more liberal about gathering metrics, you can gain a broader picture of your system. 
メトリックの収集に対してより自由であれば、システムの全体像を把握できます。
Notice a problem? Add a metric to track it! 
問題に気づきましたか？それを追跡するためのメトリックを追加してください！
Excited about some quantitative change on the last release? 
最後のリリースでの定量的な変化に興奮していますか？
Add a metric to track it! 
それを追跡するためのメトリックを追加してください！

<!-- ここまで読んだ! -->

#### Rule #3: Choose machine learning over a complex heuristic. ルール #3: 複雑なヒューリスティックよりも機械学習を選択する。

A simple heuristic can get your product out the door. 
単純なヒューリスティックは、あなたの製品を市場に出すことができます。
A complex heuristic is unmaintainable. 
**複雑なヒューリスティックは、メンテナンスが困難**です。
Once you have data and a basic idea of what you are trying to accomplish, move on to machine learning. 
データと達成しようとしている基本的なアイデアが得られたら、機械学習に移行しましょう。
As in most software engineering tasks, you will want to be constantly updating your approach, whether it is a heuristic or a machine-learned model, 
ほとんどのソフトウェア工学のタスクと同様に、ヒューリスティックであれ機械学習モデルであれ、アプローチを常に更新したいと思うでしょう。
and you will find that the machine-learned model is easier to update and maintain (see Rule #16). 
そして、**機械学習モデルの方が更新やメンテナンスが容易であること**がわかるでしょう（ルール #16を参照）。

<!-- ここまで読んだ! -->

## ML Phase I: Your First Pipeline MLフェーズI: あなたの最初のパイプライン

Focus on your system infrastructure for your first pipeline. 
最初のパイプラインのために、システムインフラストラクチャに焦点を当ててください。
While it is fun to think about all the imaginative machine learning you are going to do, 
あなたが行うすべての想像力豊かな機械学習について考えるのは楽しいですが、
it will be hard to figure out what is happening if you don’t first trust your pipeline. 
最初にパイプラインを信頼しなければ、何が起こっているのかを理解するのは難しいでしょう。

<!-- ここまで読んだ! -->

#### Rule #4: Keep the first model simple and get the infrastructure right. ルール #4: 最初のモデルはシンプルに保ち、インフラを正しく整える。

The first model provides the biggest boost to your product, so it doesn't need to be fancy. 
最初のモデルはあなたの製品に最も大きなブーストを提供するため、派手である必要はありません。
But you will run into many more infrastructure issues than you expect. 
**しかし、あなたが予想しているよりも多くのインフラの問題に直面することになります。** (確かに実感する...!:thinking:)
Before anyone can use your fancy new machine learning system, you have to determine: 
誰もあなたの派手な新しい機械学習システムを使用できる前に、あなたは以下を決定する必要があります。

- How to get examples to your learning algorithm. 
  - 学習アルゴリズムに例をどのように提供するか。
- A first cut as to what "good" and "bad" mean to your system. 
  - あなたのシステムにとって「良い」と「悪い」が何を意味するかの初期の判断。
- How to integrate your model into your application. 
  - あなたのモデルをアプリケーションに統合する方法。
    You can either apply the model live, or precompute the model on examples offline and store the results in a table. 
    モデルをリアルタイムで適用するか、オフラインで例に基づいてモデルを事前計算し、結果をテーブルに保存することができます。(リアルタイム推論 or バッチ推論の話:thinking:)
    For example, you might want to preclassify web pages and store the results in a table, but you might want to classify chat messages live. 
    例えば、ウェブページを事前に分類して結果をテーブルに保存したいかもしれませんが、チャットメッセージをリアルタイムで分類したいかもしれません。

Choosing simple features makes it easier to ensure that: 
**シンプルな特徴量を選ぶこと**で、以下のことを確実にするのが容易になります。

- The features reach your learning algorithm correctly. 
  - 特徴量が学習アルゴリズムに正しく届くこと。
- The model learns reasonable weights. 
  - モデルが合理的な重みを学習すること。
- The features reach your model in the server correctly. 
  - 特徴量がサーバー内のモデルに正しく届くこと。

Once you have a system that does these three things reliably, you have done most of the work. 
これらの3つのことを信頼性高く行うシステムができれば、あなたはほとんどの作業を終えたことになります。
Your simple model provides you with baseline metrics and a baseline behavior that you can use to test more complex models. 
あなたのシンプルなモデルは、**より複雑なモデルをテストするために使用できるベースラインのメトリクスとベースラインの動作を提供**します。
Some teams aim for a "neutral" first launch: a first launch that explicitly deprioritizes machine learning gains, to avoid getting distracted. 
一部のチームは**「中立的」な初回ローンチ**を目指します。これは、機械学習の利益を明示的に優先順位を下げて、気を散らさないようにする初回ローンチです。

- メモ: "neutral" first launchって? 
  - 最初はシンプルなモデルとインフラ重視で、「とりあえず動かしてみる」ことがめちゃ大事。
  - 「中立」っていう意味は、機械学習でどれくらい精度が上がるかとか、変化にワクワクしすぎて本質忘れちゃわないように、MLの貢献をあえて優先しない方針にする感じ。
  - **目的は、現場のインフラやデータパイプラインがちゃんと安定してるかとか、「イケてる技術」が正しく組み込めてるかをまず確認すること！**

<!-- ここまで読んだ! -->

#### Rule #5: Test the infrastructure independently from the machine learning. 　ルール #5: 機械学習とは独立してインフラストラクチャをテストすること。

Make sure that the infrastructure is testable, and that the learning parts of the system are encapsulated so that you can test everything around it. 
インフラストラクチャがテスト可能であることを確認し、システムの学習部分がカプセル化されているため、周囲のすべてをテストできるようにします。
Specifically: 
具体的には：

1. Test getting data into the algorithm. 
   アルゴリズムにデータを取り込むテストを行います。
   Check that feature columns that should be populated are populated. 
   満たされるべき特徴列が満たされていることを確認します。
   Where privacy permits, manually inspect the input to your training algorithm. 
   プライバシーが許可される場合は、トレーニングアルゴリズムへの入力を手動で検査します。
   If possible, check statistics in your pipeline in comparison to statistics for the same data processed elsewhere. 
   可能であれば、パイプライン内の統計を、他の場所で処理された同じデータの統計と比較して確認します。

2. Test getting models out of the training algorithm. 
   トレーニングアルゴリズムからモデルを取り出すテストを行います。
   Make sure that the model in your training environment gives the same score as the model in your serving environment (see Rule #37). 
   トレーニング環境のモデルが、serving環境のモデルと同じスコアを出すことを確認します（ルール #37を参照）。
   (これはTraining-Serving Skewの話か??:thinking:)

Machine learning has an element of unpredictability, so make sure that you have tests for the code for creating examples in training and serving, and that you can load and use a fixed model during serving. 
機械学習には予測不可能な要素があるため、トレーニングと提供における例を作成するコードのテストがあることを確認し、提供中に固定モデルをロードして使用できるようにします。
Also, it is important to understand your data: see Practical Advice for Analysis of Large, Complex Data Sets. 
また、データを理解することも重要です：[大規模で複雑なデータセットの分析に関する実用的なアドバイス](http://www.unofficialgoogledatascience.com/2016/10/practical-advice-for-analysis-of-large.html)を参照してください。

<!-- ここまで読んだ! -->

#### Rule #6: Be careful about dropped data when copying pipelines. 
#### ルール #6: パイプラインをコピーする際にデータが失われないように注意する。

Often we create a pipeline by copying an existing pipeline (i.e., cargo cult programming), and the old pipeline drops data that we need for the new pipeline. 
私たちはしばしば、既存のパイプラインをコピーすることによって新しいパイプラインを作成します（つまり、カゴカルトプログラミング）が、古いパイプラインは新しいパイプラインに必要なデータを失っています。
For example, the pipeline for Google Plus What’s Hot drops older posts (because it is trying to rank fresh posts). 
例えば、Google PlusのWhat’s Hotのパイプラインは古い投稿を削除します（新しい投稿をランク付けしようとしているためです）。
This pipeline was copied to use for Google Plus Stream, where older posts are still meaningful, but the pipeline was still dropping old posts. 
このパイプラインは、古い投稿がまだ意味を持つGoogle Plus Streamで使用するためにコピーされましたが、パイプラインは依然として古い投稿を削除していました。
Another common pattern is to only log data that was seen by the user. 
もう一つの一般的なパターンは、ユーザーが見たデータのみをログに記録することです。
Thus, this data is useless if we want to model why a particular post was not seen by the user, because all the negative examples have been dropped. 
したがって、特定の投稿がユーザーに見られなかった理由をモデル化したい場合、このデータは無意味です。なぜなら、すべてのネガティブな例が削除されてしまっているからです。
A similar issue occurred in Play. 
Playでも同様の問題が発生しました。
While working on Play Apps Home, a new pipeline was created that also contained examples from the landing page for Play Games without any feature to disambiguate where each example came from. 
Play Apps Homeに取り組んでいる際に、新しいパイプラインが作成され、Play Gamesのランディングページからの例も含まれていましたが、各例がどこから来たのかを明確にする機能はありませんでした。

<!-- ここまで読んだ! -->

#### Rule #7: Turn heuristics into features, or handle them externally. ルール #7: ヒューリスティックを特徴量に変換するか、外部で処理する。

Usually the problems that machine learning is trying to solve are not completely new. 
通常、機械学習が解決しようとしている問題は全く新しいものではありません。
There is an existing system for ranking, or classifying, or whatever problem you are trying to solve. 
ランキングや分類、あるいはあなたが解決しようとしている問題に対する既存のシステムがあります。
This means that there are a bunch of rules and heuristics. 
これは、多くのルールやヒューリスティックが存在することを意味します。
These same heuristics can give you a lift when tweaked with machine learning. 
これらのヒューリスティックは、機械学習で調整されると、あなたに助けを与えることができます。
Your heuristics should be mined for whatever information they have, for two reasons. 
あなたのヒューリスティックは、2つの理由から、持っている情報を掘り起こすべきです。
First, the transition to a machine learned system will be smoother. 
第一に、機械学習システムへの移行がスムーズになります。
Second, usually those rules contain a lot of the intuition about the system you don’t want to throw away. 
第二に、通常、これらのルールには、捨てたくないシステムに関する多くの直感が含まれています。
There are four ways you can use an existing heuristic: 
**既存のヒューリスティックを使用する方法は4つ**あります。

- Preprocess using the heuristic. 
  - **ヒューリスティックを使用して前処理**を行います。
    If the feature is incredibly awesome, then this is an option. 
    その特徴が非常に優れている場合、これは選択肢です。
    For example, if, in a spam filter, the sender has already been blacklisted, don’t try to relearn what "blacklisted" means. 
    **例えば、スパムフィルターで送信者がすでにブラックリストに載っている場合、「ブラックリストに載っている」とは何かを再学習しようとしないでください。**
    Block the message. 
    メッセージをブロックします。
    This approach makes the most sense in binary classification tasks. 
    このアプローチは、二項分類タスクで最も理にかなっています。

- Create a feature. 
  - 特徴量を作成します。
    Directly creating a feature from the heuristic is great. 
    **ヒューリスティックから直接特徴量を作成するのは素晴らしい**です。
    For example, if you use a heuristic to compute a relevance score for a query result, you can include the score as the value of a feature. 
    例えば、クエリ結果の関連スコアを計算するためにヒューリスティックを使用する場合、そのスコアを特徴量の値として含めることができます。
    Later on you may want to use machine learning techniques to massage the value (for example, converting the value into one of a finite set of discrete values, or combining it with other features) but start by using the raw value produced by the heuristic. 
    後で、機械学習技術を使用してその値を調整したい場合（例えば、値を有限の離散値のセットの1つに変換するか、他の特徴量と組み合わせるなど）、まずはヒューリスティックによって生成された生の値を使用します。

- Mine the raw inputs of the heuristic. 
  - ヒューリスティックの生の入力を掘り起こします。
    If there is a heuristic for apps that combines the number of installs, the number of characters in the text, and the day of the week, then consider pulling these pieces apart, and feeding these inputs into the learning separately. 
    **インストール数、テキストの文字数、曜日を組み合わせたアプリ用のヒューリスティックがある場合、これらの要素を分けて、これらの入力を別々に学習に供給することを検討してください**。
    Some techniques that apply to ensembles apply here (see Rule #40). 
    アンサンブルに適用されるいくつかの技術がここでも適用されます（ルール #40を参照）。

- Modify the label. 
  - ラベルを修正します。
    This is an option when you feel that the heuristic captures information not currently contained in the label. 
    これは、ヒューリスティックが現在ラベルに含まれていない情報を捉えていると感じるときの選択肢です。
    For example, if you are trying to maximize the number of downloads, but you also want quality content, then maybe the solution is to multiply the label by the average number of stars the app received. 
    **例えば、ダウンロード数を最大化しようとしているが、質の高いコンテンツも望んでいる場合、解決策はラベルをアプリが受け取った平均星数で掛け算することかもしれません。** (報酬関数・目的関数の設計、みたいな話??:thinking:)
    There is a lot of leeway here. 
    ここには多くの余地があります。
    See "Your First Objective". 
    「あなたの最初の目標」を参照してください。

Do be mindful of the added complexity when using heuristics in an ML system. 
**MLシステムでヒューリスティックを使用する際の追加の複雑さに注意**してください。
Using old heuristics in your new machine learning algorithm can help to create a smooth transition, but think about whether there is a simpler way to accomplish the same effect. 
古いヒューリスティックを新しい機械学習アルゴリズムで使用することは、スムーズな移行を助けることができますが、同じ効果を達成するためのより簡単な方法があるかどうかを考えてください。

<!-- ここまで読んだ! -->

### Monitoring 監視

In general, practice good alerting hygiene, such as making alerts actionable 
一般的に、アラートを実行可能にするなど、良好なアラート管理を実践してください。
and having a dashboard page.
そして、ダッシュボードページを持つことです。

#### Rule #8: Know the freshness requirements of your system. ルール #8: システムの新鮮さの要件を理解する

How much does performance degrade if you have a model that is a day old? 
モデルが1日古い場合、パフォーマンスはどの程度低下しますか？
A week old? A quarter old? 
1週間古い場合は？ 1四半期古い場合は？
This information can help you to understand the priorities of your monitoring. 
この情報は、監視の優先順位を理解するのに役立ちます。
If you lose significant product quality if the model is not updated for a day, 
モデルが1日更新されない場合に製品の品質が大幅に低下するなら、
it makes sense to have an engineer watching it continuously. 
エンジニアが継続的に監視することは理にかなっています。
Most ad serving systems have new advertisements to handle every day, and must update daily. 
ほとんどの広告配信システムは毎日新しい広告を扱い、日々更新する必要があります。
For instance, if the ML model for Google Play Search is not updated, 
例えば、Google Play SearchのMLモデルが更新されない場合、
it can have a negative impact in under a month. 
1ヶ月以内に悪影響を及ぼす可能性があります。
Some models for What’s Hot in Google Play have no post identifier in their model so they can export these models infrequently. 
Google PlayのWhat’s Hotの一部のモデルには投稿識別子がないため、これらのモデルを頻繁にエクスポートすることはできません。(特徴量にidを含まないので、頻繁に更新する必要がない、という話??:thinking:)
Other models that have post identifiers are updated much more frequently. 
一方、投稿識別子を持つ他のモデルは、はるかに頻繁に更新されます。(CF系アプローチとかね...!:thinking:)
Also notice that freshness can change over time, especially when feature columns are added or removed from your model. 
また、新しい特徴量がモデルに追加または削除されると、特に時間の経過とともに新鮮さが変化する可能性があることに注意してください。

<!-- ここまで読んだ! -->

#### Rule #9: Detect problems before exporting models. ルール #9: モデルをエクスポートする前に問題を検出する。

(export = 多分デプロイとかリリースの意味合いっぽい...!:thinking:)

Many machine learning systems have a stage where you export the model to serving. 
多くの機械学習システムには、モデルを提供するためにエクスポートする段階があります。
If there is an issue with an exported model, it is a user-facing issue. 
エクスポートされたモデルに問題がある場合、それはユーザに影響を与える問題です。

Do sanity checks right before you export the model. 
モデルをエクスポートする直前に、サニティチェックを行ってください。
Specifically, make sure that the model’s performance is reasonable on held out data. 
具体的には、モデルの性能が保持されたデータに対して合理的であることを確認してください。
Or, if you have lingering concerns with the data, don’t export a model. 
また、データに対して懸念が残っている場合は、モデルをエクスポートしないでください。
Many teams continuously deploying models check the area under the ROC curve (or AUC) before exporting. 
**モデルを継続的にデプロイしている多くのチームは、エクスポートする前にROC曲線の下の面積（AUC）を確認します。** (デプロイ前にオフライン評価でチェックしようって話か...!:thinking:)
Issues about models that haven’t been exported require an email alert, but issues on a user-facing model may require a page. 
エクスポートされていないモデルに関する問題はメールアラートが必要ですが、ユーザーに影響を与えるモデルの問題はページが必要な場合があります。
So better to wait and be sure before impacting users. 
したがって、ユーザーに影響を与える前に待って確実にする方が良いです。

<!-- ここまで読んだ! -->

#### Rule #10: Watch for silent failures. ルール #10: サイレントフェイルに注意する。

This is a problem that occurs more for machine learning systems than for other kinds of systems. 
これは、他の種類のシステムよりも機械学習システムでより多く発生する問題です。
Suppose that a particular table that is being joined is no longer being updated. 
特定のテーブルが結合されているが、もはや更新されていないと仮定します。
The machine learning system will adjust, and behavior will continue to be reasonably good, decaying gradually. 
機械学習システムは調整され、動作は合理的に良好であり続け、徐々に劣化します。
Sometimes you find tables that are months out of date, and a simple refresh improves performance more than any other launch that quarter! 
**時には、数ヶ月も古いテーブルが見つかり、単純なリフレッシュがその四半期の他のどのローンチよりもパフォーマンスを向上させることがあります**！
The coverage of a feature may change due to implementation changes: for example a feature column could be populated in 90% of the examples, and suddenly drop to 60% of the examples.
特徴量のカバレッジは、実装の変更により変わる可能性があります。例えば、特徴量列が90%の例で埋められていたのが、突然60%の例に減少することがあります。
Play once had a table that was stale for 6 months, and refreshing the table alone gave a boost of 2% in install rate. 
**かつてPlayは6ヶ月間古くなったテーブルを持っており、そのテーブルをリフレッシュするだけでインストール率が2%向上しました。**
If you track statistics of the data, as well as manually inspect the data on occasion, you can reduce these kinds of failures. 
**データの統計を追跡し、時折データを手動で検査することで、これらの種類の失敗を減らすことができます。**

<!-- ここまで読んだ! -->

#### Rule #11: Give feature columns owners and documentation. ルール #11: フィーチャーカラムの所有者とドキュメントを提供する。

If the system is large, and there are many feature columns, know who created or is maintaining each feature column. 
**システムが大規模で、多くのフィーチャーカラムがある場合は、各フィーチャーカラムを誰が作成または維持しているかを把握してください**。
If you find that the person who understands a feature column is leaving, make sure that someone has the information. 
フィーチャーカラムを理解している人が退職することがわかった場合は、誰かがその情報を持っていることを確認してください。
Although many feature columns have descriptive names, it's good to have a more detailed description of what the feature is, where it came from, and how it is expected to help. 
多くのフィーチャーカラムには説明的な名前がありますが、フィーチャーが何であるか、どこから来たのか、どのように役立つと期待されているのかについて、より詳細な説明を持つことが重要です。

<!-- ここまで読んだ!ここまだ十分にできてないな...:thinking: -->

### Your First Objective 最初の目標

You have many metrics, or measurements about the system that you care about, 
あなたは、関心のあるシステムに関する多くのメトリック（指標）や測定値を持っていますが、 
but your machine learning algorithm will often require a single objective, a number that your algorithm is "trying" to optimize. 
あなたの機械学習アルゴリズムはしばしば単一の目的、つまりアルゴリズムが「最適化しようとしている」数値を必要とします。 
I distinguish here between objectives and metrics: a metric is any number that your system reports, which may or may not be important. 
ここで、目的とメトリックの違いを説明します：メトリックは、システムが報告する任意の数値であり、それが重要であるかどうかは関係ありません。 
See also Rule #2. 
ルール#2も参照してください。

<!-- ここまで読んだ! -->

#### Rule #12: Don’t overthink which objective you choose to directly optimize. ルール #12: どの目的を直接最適化するかを考えすぎないこと。

You want to make money, make your users happy, and make the world a better place. 
あなたはお金を稼ぎ、ユーザーを幸せにし、世界をより良い場所にしたいと思っています。
There are tons of metrics that you care about, and you should measure them all (see Rule #2). 
**あなたが気にする指標はたくさんあり、すべてを測定すべき**です（ルール #2を参照）。
However, early in the machine learning process, you will notice them all going up, even those that you do not directly optimize. 
しかし、機械学習プロセスの初期段階では、直接最適化していない指標でさえもすべてが上昇していることに気付くでしょう。
For instance, suppose you care about number of clicks and time spent on the site. 
例えば、クリック数とサイトでの滞在時間を気にしているとしましょう。
If you optimize for number of clicks, you are likely to see the time spent increase. 
クリック数を最適化すると、滞在時間が増加する可能性が高いです。

So, keep it simple and don’t think too hard about balancing different metrics when you can still easily increase all the metrics. 
**ですので、シンプルに保ち、すべての指標を簡単に増加させることができるときに、異なる指標のバランスを考えすぎないようにしましょう。**
Don’t take this rule too far though: do not confuse your objective with the ultimate health of the system (see Rule #39). 
ただし、このルールを行き過ぎて適用しないでください: あなたの目的とシステムの最終的な健全性を混同しないでください（ルール #39を参照）。
And, if you find yourself increasing the directly optimized metric, but deciding not to launch, some objective revision may be required. 
**そして、直接最適化された指標が増加しているのに、ローンチしないことを決定した場合は、目的の見直しが必要かもしれません。** (確かに、じゃあなんでその目的を最適化してるんだ、って話になるからね...!:thinking:)

<!-- ここまで読んだ! -->

#### Rule #13: Choose a simple, observable and attributable metric for your first objective. ルール #13: 最初の目標には、シンプルで観察可能かつ帰属可能な指標を選択してください。

Often you don't know what the true objective is. 
しばしば、あなたは真の目標が何であるかを知りません。
You think you do but then as you stare at the data and side-by-side analysis of your old system and new ML system, you realize you want to tweak the objective. 
あなたはそう思っていても、データを見つめ、古いシステムと新しい機械学習システムの並行分析を行うと、目標を調整したくなることに気づきます。
Further, different team members often can't agree on the true objective. 
さらに、異なるチームメンバーはしばしば真の目標について合意できません。
The ML objective should be something that is easy to measure and is a proxy for the "true" objective. 
機械学習の目標は、測定が容易であり、「真の」目標の代理となるものであるべきです。
In fact, there is often no "true" objective (see Rule #39). 
実際、しばしば「真の」目標は存在しません（ルール #39を参照）。
So train on the simple ML objective, and consider having a "policy layer" on top that allows you to add additional logic (hopefully very simple logic) to do the final ranking. 
**したがって、シンプルな機械学習の目標でトレーニングし、最終的なランキングを行うために追加のロジック（できれば非常にシンプルなロジック）を追加できる「ポリシーレイヤー」を上に持つことを検討してください。**
The easiest thing to model is a user behavior that is directly observed and attributable to an action of the system: 
**モデル化する最も簡単なことは、直接観察可能でシステムのアクションに帰属可能なユーザーの行動**です：
(以下はいずれも、わかりやすく観察可能で、システムのアクションに対して「すぐ」わかるし「誰が何をどうしたか」がはっきりしてるmetrics...!:thinking:)

- Was this ranked link clicked? 
  - このランク付けされたリンクはクリックされましたか？
- Was this ranked object downloaded? 
  - このランク付けされたオブジェクトはダウンロードされましたか？
- Was this ranked object forwarded/replied to/emailed? 
  - このランク付けされたオブジェクトは転送/返信/メールされましたか？
- Was this ranked object rated? 
  - このランク付けされたオブジェクトは評価されましたか？
- Was this shown object marked as spam/pornography/offensive? 
  - この表示されたオブジェクトはスパム/ポルノ/攻撃的としてマークされましたか？

Avoid modeling indirect effects at first: 
**最初は間接的な効果のモデル化を避けてください**：
(以下は最初は避けたほうが良いってこと??:thinking:)
("indirect" = 直接的ではなく、観測されるまで時間がかかったり、他の要因が絡む可能性があるもの、みたいな意味合い??:thinking:)

- Did the user visit the next day? 
  - ユーザーは翌日訪問しましたか？
- How long did the user visit the site? 
  - ユーザーはどのくらいの時間サイトを訪れましたか？
- What were the daily active users? 
  - 日々のアクティブユーザーはどのくらいでしたか？

Indirect effects make great metrics, and can be used during A/B testing and during launch decisions. 
**間接的な効果は優れた指標を作り、A/Bテストやローンチの決定時に使用できます。** (オンライン評価のmetricsとして有効だけど、最初の目的関数としては避けたほうが良い、って話か...!:thinking:)
Finally, don’t try to get the machine learning to figure out: 
最後に、機械学習に以下を解決させようとしないでください：

- Is the user happy using the product? 
  - ユーザーは製品を使用して満足していますか？
- Is the user satisfied with the experience? 
  - ユーザーは体験に満足していますか？
- Is the product improving the user’s overall wellbeing? 
  - 製品はユーザーの全体的な幸福を向上させていますか？
- How will this affect the company’s overall health? 
  - これは会社の全体的な健康にどのように影響しますか？

These are all important, but also incredibly hard to measure. 
これらはすべて重要ですが、**測定するのは非常に難しい**です。
Instead, use proxies: if the user is happy, they will stay on the site longer. 
**代わりに代理指標を使用してください：ユーザーが満足していれば、彼らはサイトに長く留まります。**
If the user is satisfied, they will visit again tomorrow. 
ユーザーが満足していれば、彼らは明日再び訪れます。
Insofar as well-being and company health is concerned, human judgement is required to connect any machine learned objective to the nature of the product you are selling and your business plan. 
幸福や会社の健康に関しては、販売している製品の性質やビジネスプランに機械学習された目標を結びつけるために人間の判断が必要です。

<!-- ここまで読んだ! -->

#### Rule #14: Starting with an interpretable model makes debugging easier. ルール #14: 解釈可能なモデルから始めることでデバッグが容易になる。

Linear regression, logistic regression, and Poisson regression are directly motivated by a probabilistic model. 
線形回帰、ロジスティック回帰、およびポアソン回帰は、確率モデルに直接基づいています。
Each prediction is interpretable as a probability or an expected value. 
各予測は、確率または期待値として解釈可能です。
This makes them easier to debug than models that use objectives (zero-one loss, various hinge losses, and so on) that try to directly optimize classification accuracy or ranking performance. 
**これにより、分類精度やランキング性能を直接最適化しようとする目的（ゼロ-ワン損失、さまざまなヒンジ損失など）を使用するモデルよりもデバッグが容易になります**。
For example, if probabilities in training deviate from probabilities predicted in side-by-sides or by inspecting the production system, this deviation could reveal a problem. 
例えば、トレーニング中の確率がサイドバイサイドで予測された確率や生産システムを検査した際の確率から逸脱している場合、この逸脱は問題を明らかにする可能性があります。

For example, in linear, logistic, or Poisson regression, there are subsets of the data where the average predicted expectation equals the average label (1-moment calibrated, or just calibrated). 
例えば、線形回帰、ロジスティック回帰、またはポアソン回帰では、平均予測期待値が平均ラベル（1-モーメントキャリブレーション、または単にキャリブレーション）に等しいデータのサブセットがあります。
This is true assuming that you have no regularization and that your algorithm has converged, and it is approximately true in general. 
これは、正則化がなく、アルゴリズムが収束していると仮定した場合に真であり、一般的にはおおよそ真です。
If you have a feature which is either 1 or 0 for each example, then the set of 3 examples where that feature is 1 is calibrated. 
各例に対して1または0のいずれかである特徴がある場合、その特徴が1である3つの例の集合はキャリブレーションされています。
Also, if you have a feature that is 1 for every example, then the set of all examples is calibrated. 
また、すべての例に対して1である特徴がある場合、すべての例の集合はキャリブレーションされています。

With simple models, it is easier to deal with feedback loops (see Rule #36). 
**単純なモデルでは、フィードバックループ（ルール #36を参照）に対処するのが容易**です。
Often, we use these probabilistic predictions to make a decision: e.g. rank posts in decreasing expected value (i.e. probability of click/download/etc.). 
しばしば、これらの確率的予測を使用して意思決定を行います：例えば、期待値が減少する順に投稿をランク付けします（すなわち、クリック/ダウンロードなどの確率）。
However, remember when it comes time to choose which model to use, the decision matters more than the likelihood of the data given the model (see Rule #27). 
**ただし、どのモデルを使用するかを選択する際には、モデルに与えられたデータの尤度よりもその決定が重要であることを忘れないでください**（ルール #27を参照）。
(スコアの予測精度ではなく、そのスコアを使って最終的にどういう意思決定をするか、が重要、だからオフライン評価時に注意しよう、って話か...!:thinking:)

<!-- ここまで読んだ! -->

#### Rule #15: Separate Spam Filtering and Quality Ranking in a Policy Layer. ルール #15: ポリシーレイヤーにおけるスパムフィルタリングと品質ランキングの分離。

Quality ranking is a fine art, but spam filtering is a war. 
品質ランキングは繊細な技術ですが、スパムフィルタリングは戦争です。
The signals that you use to determine high quality posts will become obvious to those who use your system, and they will tweak their posts to have these properties. 
**高品質な投稿を判断するために使用する信号は、あなたのシステムを使用する人々に明らかになり、彼らはその特性を持つように投稿を調整します。**　 (Twitterとかね...!:thinking:)
Thus, your quality ranking should focus on ranking content that is posted in good faith. 
したがって、あなたの品質ランキングは、善意で投稿されたコンテンツのランキングに焦点を当てるべきです。
You should not discount the quality ranking learner for ranking spam highly. 
スパムを高く評価する品質ランキング学習者を軽視すべきではありません。
Similarly, "racy" content should be handled separately from Quality Ranking. 
**同様に、「刺激的な」コンテンツは品質ランキングとは別に扱うべき**です。
Spam filtering is a different story. 
スパムフィルタリングは別の話です。
You have to expect that the features that you need to generate will be constantly changing. 
生成する必要のある特徴量が常に変化することを予期しなければなりません。
Often, there will be obvious rules that you put into the system (if a post has more than three spam votes, don’t retrieve it, et cetera). 
**しばしば、システムに組み込む明白なルールが存在します（投稿にスパム投票が3つ以上ある場合は取得しないなど）。**
Any learned model will have to be updated daily, if not faster. 
学習されたモデルは、日々更新される必要があり、場合によってはそれ以上の頻度で更新される必要があります。
The reputation of the creator of the content will play a great role. 
コンテンツの作成者の評判は大きな役割を果たします。

At some level, the output of these two systems will have to be integrated. 
ある程度、これら二つのシステムの出力は統合される必要があります。
Keep in mind, filtering spam in search results should probably be more aggressive than filtering spam in email messages. 
検索結果におけるスパムフィルタリングは、メールメッセージにおけるスパムフィルタリングよりもおそらくより積極的であるべきです。
Also, it is a standard practice to remove spam from the training data for the quality classifier. 
また、**品質分類器のトレーニングデータからスパムを除去することは標準的な手法**です。

<!-- ここまで読んだ! -->

## ML Phase II: Feature Engineering MLフェーズII: 特徴量エンジニアリング

In the first phase of the lifecycle of a machine learning system, the
important issues are to get the training data into the learning system, get any metrics of interest instrumented, and create a serving infrastructure.
機械学習システムのライフサイクルの最初のフェーズでは、重要な問題は、トレーニングデータを学習システムに取り込み、関心のあるメトリクスを計測し、推論のインフラストラクチャを作成することです。
After you have a working end to end system with unit and system tests instrumented,
Phase II begins.
ユニットテストとシステムテストが計測された動作するエンドツーエンドシステムが完成した後、フェーズIIが始まります。

In the second phase, there is a lot of low-hanging fruit. There are a variety
of obvious features that could be pulled into the system.
第二のフェーズでは、多くの手軽に取り組める課題があります。システムに取り込むことができる明らかな特徴がさまざまに存在します。
Thus, the second phase of machine learning involves pulling in as many features as possible and
combining them in intuitive ways.
したがって、**機械学習の第二のフェーズは、できるだけ多くの特徴量を取り込み、それらを直感的な方法で組み合わせること**を含みます。
During this phase, all of the metrics should still be rising.
**このフェーズでは、すべてのメトリクスが引き続き上昇している必要があります。**
There will be lots of launches, and it is a great time to
pull in lots of engineers that can join up all the data that you need to
create a truly awesome learning system.
多くのローンチが行われ、真に素晴らしい学習システムを作成するために必要なすべてのデータを統合できる多くのエンジニアを引き入れる絶好の機会です。

<!-- ここまで読んだ! -->

#### Rule #16: Plan to launch and iterate. ルール #16: 発表と反復を計画する。

Don’t expect that the model you are working on now will be the last one that you will launch, or even that you will ever stop launching models. 
**今取り組んでいるモデルが最後のモデルになるとは期待しないでください。また、モデルの発表を永遠にやめることもないでしょう。**
Thus consider whether the complexity you are adding with this launch will slow down future launches. 
**したがって、この発表で追加する複雑さが将来の発表を遅らせるかどうかを考慮してください。**
Many teams have launched a model per quarter or more for years. 
多くのチームは、数年間にわたり四半期ごとにモデルを発表してきました。
There are three basic reasons to launch new models: 
新しいモデルを発表する基本的な理由は3つあります。

- You are coming up with new features. 
  - 新しい特徴を考案している。
- You are tuning regularization and combining old features in new ways. 
  - 正則化を調整し、古い特徴を新しい方法で組み合わせている。
- You are tuning the objective. 
  - 目的を調整している。

Regardless, giving a model a bit of love can be good: looking over the data feeding into the example can help find new signals as well as old, broken ones. 
いずれにせよ、モデルに少し手を加えることは良いことです。例に供給されるデータを見直すことで、新しい信号や古い壊れた信号を見つけるのに役立ちます。
So, as you build your model, think about how easy it is to add or remove or recombine features. 
**したがって、モデルを構築する際には、特徴を追加、削除、または再結合するのがどれほど簡単かを考えてください。**
Think about how easy it is to create a fresh copy of the pipeline and verify its correctness. 
**パイプラインの新しいコピーを作成し、その正確性を確認するのがどれほど簡単かを考えてください。**　(= これってつまり、controlモデルとtreatmentモデルを並行して動かすのがどれほど簡単か、って話か!! A/Bテストしやすさが重要観点だ!!:thinking:)
Think about whether it is possible to have two or three copies running in parallel. 
**2つまたは3つのコピーを並行して実行することが可能かどうかを考えてください。**
Finally, don’t worry about whether feature 16 of 35 makes it into this version of the pipeline.
最後に、35の特徴のうち16がこのバージョンのパイプラインに含まれるかどうかを心配しないでください。(??)
You’ll get it next quarter. 
次の四半期にはそれを手に入れることができます。

<!-- ここまで読んだ! -->

#### Rule #17: Start with directly observed and reported features as opposed to learned features. ルール #17: 学習された特徴ではなく、直接観察され報告された特徴量から始める。

This might be a controversial point, but it avoids a lot of pitfalls. 
これは議論の余地がある点かもしれませんが、多くの落とし穴を避けることができます。
First of all, let’s describe what a learned feature is. 
まず、**学習された特徴量**とは何かを説明しましょう。
A learned feature is a feature generated either by an external system (such as an unsupervised clustering system) or by the learner itself (e.g. via a factored model or deep learning). 
学習された特徴とは、外部システム（例えば、教師なしクラスタリングシステム）または学習者自身（例えば、因子モデルや深層学習を通じて）によって生成される特徴量です。
Both of these can be useful, but they can have a lot of issues, so they should not be in the first model. 
**どちらも有用である可能性がありますが、多くの問題を抱える可能性があるため、最初のモデルには含めるべきではありません。**

If you use an external system to create a feature, remember that the external system has its own objective. 
外部システムを使用して特徴量を作成する場合、その外部システムには独自の目的があることを忘れないでください。
The external system's objective may be only weakly correlated with your current objective. 
外部システムの目的は、あなたの現在の目的と弱くしか相関していない可能性があります。
If you grab a snapshot of the external system, then it can become out of date. 
外部システムのスナップショットを取得すると、それが古くなる可能性があります。
If you update the features from the external system, then the meanings may change. 
外部システムからの特徴を更新すると、その意味が変わる可能性があります。
If you use an external system to provide a feature, be aware that this approach requires a great deal of care. 
外部システムを使用して特徴を提供する場合、このアプローチには多くの注意が必要であることを認識してください。

The primary issue with factored models and deep models is that they are nonconvex. 
因子モデルや深層モデルの主な問題は、それらが非凸であることです。
Thus, there is no guarantee that an optimal solution can be approximated or found, and the local minima found on each iteration can be different. 
したがって、最適な解を近似または見つけることができる保証はなく、各イテレーションで見つかる局所的最小値は異なる可能性があります。
This variation makes it hard to judge whether the impact of a change to your system is meaningful or random. 
この変動により、システムへの変更の影響が意味のあるものかランダムなものかを判断するのが難しくなります。
By creating a model without deep features, you can get an excellent baseline performance. 
**深い特徴を持たないモデルを作成することで、優れたベースラインパフォーマンスを得ることができます。**
After this baseline is achieved, you can try more esoteric approaches. 
**このベースラインが達成された後、より難解なアプローチを試すことができます。**

<!-- ここまで読んだ! -->

#### Rule #18: Explore with features of content that generalize across contexts. ルール #18: コンテキストを超えて一般化するコンテンツの特徴量を探索する。

Often a machine learning system is a small part of a much bigger picture. 
機械学習システムはしばしば、はるかに大きな全体の一部に過ぎません。
For example, if you imagine a post that might be used in What’s Hot, many people will plus-one, reshare, or comment on a post before it is ever shown in What's Hot. 
たとえば、「What's Hot」で使用される可能性のある投稿を想像すると、多くの人々はその投稿が「What's Hot」に表示される前に、プラスワンしたり、再共有したり、コメントしたりします。
If you provide those statistics to the learner, it can promote new posts that it has no data for in the context it is optimizing. 
これらの統計を学習者に提供すると、最適化しているコンテキストにおいてデータがない新しい投稿を促進することができます。
YouTube Watch Next could use number of watches, or co-watches (counts of how many times one video was watched after another was watched) from YouTube search. 
YouTube Watch Nextは、YouTube検索からの視聴回数や共同視聴（ある動画が視聴された後に別の動画が視聴された回数）を使用できます。
You can also use explicit user ratings. 
明示的なユーザー評価も使用できます。
Finally, if you have a user action that you are using as a label, seeing that action on the document in a different context can be a great feature. 
最後に、ラベルとして使用しているユーザーアクションがある場合、そのアクションが異なるコンテキストで文書に現れることは素晴らしい特徴となる可能性があります。
All of these features allow you to bring new content into the context. 
**これらすべての特徴により、新しいコンテンツをコンテキストに取り入れることができます。** (他の出面でのログも使って特徴量にしよう! そしたらコールドスタートアイテム問題も軽減できるよね、みたいな話かな...!:thinking:)
Note that this is not about personalization: figure out if someone likes the content in this context first, then figure out who likes it more or less. 
これはパーソナライズに関するものではありません。**まず、このコンテキストで誰かがそのコンテンツを好むかどうかを判断し**、その後、誰がより好むか、またはあまり好まないかを判断します。

<!-- ここまで読んだ! -->

#### Rule #19: Use very specific features when you can. ルール #19: 可能な限り非常に特定の特徴を使用すること。

With tons of data, it is simpler to learn millions of simple features than a few complex features. 
大量のデータがある場合、少数の複雑な特徴量を学ぶよりも、数百万の単純な特徴量を学ぶ方が簡単です。
Identifiers of documents being retrieved and canonicalized queries do not provide much generalization, but align your ranking with your labels on head queries. 
取得される文書の識別子や標準化されたクエリはあまり一般化を提供しませんが、ヘッドクエリに対するラベルとランキングを整合させます。
Thus, don’t be afraid of groups of features where each feature applies to a very small fraction of your data, but overall coverage is above 90%. 
**したがって、各特徴量がデータのごく一部にしか適用されない特徴のグループを恐れないでください**。ただし、全体のカバレッジは90％を超えています。
You can use regularization to eliminate the features that apply to too few examples. 
正則化を使用して、あまりにも少ない例にしか適用されない特徴を排除することができます。

<!-- ここまで読んだ! -->

#### Rule #20: Combine and modify existing features to create new features in human-understandable ways.
#### ルール #20: 既存の特徴を組み合わせて修正し、人間が理解できる方法で新しい特徴を作成する。

There are a variety of ways to combine and modify features. 
特徴量を組み合わせて修正する方法はさまざまです。
Machine learning systems such as TensorFlow allow you to pre-process your data through transformations. 
TensorFlowのような機械学習システムは、変換を通じてデータを前処理することを可能にします。
The two most standard approaches are "discretizations" and "crosses". 
**最も一般的なアプローチは「離散化」と「クロス」です。**

Discretization consists of taking a continuous feature and creating many discrete features from it. 
離散化は、連続的な特徴量を取り、それから多くの離散的な特徴量を作成することです。
Consider a continuous feature such as age. 
年齢のような連続的な特徴を考えてみましょう。
You can create a feature which is 1 when age is less than 18, another feature which is 1 when age is between 18 and 35, et cetera. 
年齢が18未満のときに1となる特徴や、年齢が18歳から35歳の間のときに1となる別の特徴などを作成できます。
Don’t overthink the boundaries of these histograms: basic quantiles will give you most of the impact. 
これらのヒストグラムの境界を深く考えすぎないでください：**基本的な分位数がほとんどの影響を与えます。**

Crosses combine two or more feature columns. 
クロスは、2つ以上の特徴列を組み合わせます。
A feature column, in TensorFlow's terminology, is a set of homogenous features, (e.g. {male, female}, {US, Canada, Mexico}, et cetera). 
TensorFlowの用語では、特徴列とは同質の特徴のセットです（例：{男性、女性}、{米国、カナダ、メキシコ}など）。
A cross is a new feature column with features in, for example, {male, female} × {US, Canada, Mexico}. 
クロスは、例えば、{男性、女性} × {米国、カナダ、メキシコ}の特徴を持つ新しい特徴列です。
This new feature column will contain the feature (male, Canada). 
この新しい特徴列には、特徴(male, Canada)が含まれます。
If you are using TensorFlow and you tell TensorFlow to create this cross for you, this (male, Canada) feature will be present in examples representing male Canadians. 
TensorFlowを使用していて、このクロスを作成するように指示すると、この(male, Canada)特徴は男性カナダ人を表す例に存在します。
Note that it takes massive amounts of data to learn models with crosses of three, four, or more base feature columns. 
3つ、4つ、またはそれ以上の基本的な特徴列のクロスを持つモデルを学習するには、大量のデータが必要であることに注意してください。

Crosses that produce very large feature columns may overfit. 
非常に大きな特徴列を生成するクロスは、過剰適合する可能性があります。
For instance, imagine that you are doing some sort of search, and you have a feature column with words in the query, and you have a feature column with words in the document. 
例えば、何らかの検索を行っていて、クエリ内の単語を含む特徴列と、文書内の単語を含む特徴列があると想像してください。
You can combine these with a cross, but you will end up with a lot of features (see Rule #21). 
これらをクロスで組み合わせることができますが、多くの特徴が生成されることになります（ルール #21を参照）。

When working with text there are two alternatives. 
テキストを扱う際には、2つの選択肢があります。
The most draconian is a dot product. 
最も厳格な方法はドット積です。
A dot product in its simplest form simply counts the number of words in common between the query and the document. 
ドット積は、その最も単純な形では、クエリと文書の間で共通する単語の数を単にカウントします。
This feature can then be discretized. 
この特徴はその後、離散化することができます。
Another approach is an intersection: thus, we will have a feature which is present if and only if the word "pony" is in both the document and the query, 
別のアプローチは交差です：したがって、「pony」という単語が文書とクエリの両方に存在する場合にのみ存在する特徴を持つことになります。
and another feature which is present if and only if the word "the" is in both the document and the query. 
そして、「the」という単語が文書とクエリの両方に存在する場合にのみ存在する別の特徴を持つことになります。

<!-- ここまで読んだ! -->

#### Rule #21: The number of feature weights you can learn in a linear model is roughly proportional to the amount of data you have.
#### ルール #21: 線形モデルで学習できる特徴量の重みの数は、持っているデータの量に大まかに比例します。

There are fascinating statistical learning theory results concerning the appropriate level of complexity for a model, but this rule is basically all you need to know. 
モデルの適切な複雑さに関する興味深い統計的学習理論の結果がありますが、このルールが基本的に知っておくべきすべてです。
I have had conversations in which people were doubtful that anything can be learned from one thousand examples, or that you would ever need more than one million examples, because they get stuck in a certain method of learning. 
私は、ある特定の学習方法に固執しているため、1000の例から何かを学ぶことができるのか、または100万の例以上が必要になることはないのではないかと疑問を持つ人々との会話を持ったことがあります。
The key is to scale your learning to the size of your data: 
重要なのは、データのサイズに合わせて学習をスケールさせることです。

1. If you are working on a search ranking system, and there are millions of different words in the documents and the query and you have 1000 labeled examples, then you should use a dot product between document and query features, TF-IDF, and a half-dozen other highly human-engineered features. 1000 examples, a dozen features. 
   1. もし検索ランキングシステムに取り組んでいて、文書やクエリに数百万の異なる単語があり、1000のラベル付き例がある場合、文書とクエリの特徴の間でドット積を使用し、TF-IDFや他の数個の高度に人間が設計した特徴を使用すべきです。1000の例、約12の特徴。

2. If you have a million examples, then intersect the document and query feature columns, using regularization and possibly feature selection. 
   1. もし100万の例があるなら、文書とクエリの特徴列を交差させ、正則化とおそらく特徴選択を使用します。
    This will give you millions of features, but with regularization you will have fewer. Ten million examples, maybe a hundred thousand features. 
    これにより数百万の特徴が得られますが、正則化を使用すると数は少なくなります。1000万の例があれば、約10万の特徴になるかもしれません。

3. If you have billions or hundreds of billions of examples, you can cross the feature columns with document and query tokens, using feature selection and regularization. 
   1. もし数十億または数百億の例があるなら、特徴列を文書とクエリのトークンと交差させ、特徴選択と正則化を使用できます。
    You will have a billion examples, and 10 million features. 
    これにより、10億の例と1000万の特徴が得られます。
    Statistical learning theory rarely gives tight bounds, but gives great guidance for a starting point. 
    統計的学習理論は厳密な境界を示すことは稀ですが、出発点としての優れた指針を提供します。

In the end, use Rule #28 to decide what features to use. 
最終的には、ルール #28を使用してどの特徴を使用するかを決定します。

<!-- ここまで読んだ! -->

#### Rule #22: Clean up features you are no longer using. ルール #22: もはや使用していない機能を整理する。

Unused features create technical debt. 
未使用の特徴量は技術的負債を生み出します。 
If you find that you are not using a feature, and that combining it with other features is not working, then drop it out of your infrastructure. 
もし特徴量を使用していないことがわかり、他の特徴量と組み合わせても効果がない場合は、その特徴量をインフラから削除してください。 
You want to keep your infrastructure clean so that the most promising features can be tried as fast as possible. 
インフラをクリーンに保ち、最も有望な特徴量をできるだけ早く試せるようにしたいのです。 
If necessary, someone can always add back your feature. 
必要であれば、誰かがあなたの特徴量を再追加することができます。

Keep coverage in mind when considering what features to add or keep. 
どの特徴量を追加または保持するかを考える際には、カバレッジを考慮してください。 
How many examples are covered by the feature? 
その特徴量によってカバーされる例はどのくらいありますか？ 
For example, if you have some personalization features, but only 8% of your users have any personalization features, it is not going to be very effective. 
例えば、パーソナライズ特徴量がいくつかあるが、ユーザのうち8%しかパーソナライズ特徴量を持っていない場合、それはあまり効果的ではありません。

At the same time, some features may punch above their weight. 
同時に、いくつかの特徴量はその重さ以上の効果を発揮することがあります。 
For example, if you have a feature which covers only 1% of the data, but 90% of the examples that have the feature are positive, then it will be a great feature to add. 
例えば、データの1%しかカバーしていない特徴量があるが、その特徴量を持つ例の90%がポジティブである場合、それは追加するのに素晴らしい特徴量となります。

<!-- ここまで読んだ! -->

### Human Analysis of the System システムの人間分析

Before going on to the third phase of machine learning, it is important to 
機械学習の第三段階に進む前に、重要なことがあります。
focus on something that is not taught in any machine learning class: how to 
機械学習の授業では教えられないことに焦点を当てることです。それは、
look at an existing model, and improve it. This is more of an art than a 
既存のモデルを見て、それを改善する方法です。これは科学というよりも芸術であり、
science, and yet there are several antipatterns that it helps to avoid. 
それでも、避けるべきいくつかのアンチパターンがあります。

#### Rule #23: You are not a typical end user. ルール #23: あなたは典型的なエンドユーザーではありません。

This is perhaps the easiest way for a team to get bogged down. 
これは、おそらくチームが行き詰まる最も簡単な方法です。
While there are a lot of benefits to fishfooding (using a prototype within your team) and dogfooding (using a prototype within your company), employees should look at whether the performance is correct. 
フィッシュフーディング（チーム内でプロトタイプを使用すること）やドッグフーディング（会社内でプロトタイプを使用すること）には多くの利点がありますが、従業員はパフォーマンスが正しいかどうかを確認する必要があります。
While a change which is obviously bad should not be used, anything that looks reasonably near production should be tested further, either by paying laypeople to answer questions on a crowdsourcing platform, or through a live experiment on real users. 
**明らかに悪い変更は使用すべきではありませんが、製品に近いと思われるものは、クラウドソーシングプラットフォームで素人に質問に答えてもらうか、実際のユーザーに対するライブ実験を通じて、さらにテストする必要があります**。

There are two reasons for this. 
これには二つの理由があります。
The first is that you are too close to the code. 
第一の理由は、あなたがコードに近すぎることです。
You may be looking for a particular aspect of the posts, or you are simply too emotionally involved (e.g. confirmation bias). 
あなたは投稿の特定の側面を探しているか、単に感情的に関与しすぎている可能性があります（例：確証バイアス）。
The second is that your time is too valuable. 
第二の理由は、あなたの時間が非常に貴重であることです。
Consider the cost of nine engineers sitting in a one hour meeting, and think of how many contracted human labels that buys on a crowdsourcing platform. 
9人のエンジニアが1時間の会議に座っているコストを考慮し、それがクラウドソーシングプラットフォームでどれだけの契約された人間のラベルを購入できるかを考えてみてください。

If you really want to have user feedback, use user experience methodologies. 
もし本当にユーザーフィードバックを得たいのであれば、ユーザーエクスペリエンスの手法を使用してください。
Create user personas (one description is in Bill Buxton’s Sketching User Experiences) early in a process and do usability testing (one description is in Steve Krug’s Don’t Make Me Think) later. 
プロセスの初期段階でユーザーペルソナ（ビル・バクストンの『Sketching User Experiences』に一つの説明があります）を作成し、後でユーザビリティテスト（スティーブ・クルーグの『Don’t Make Me Think』に一つの説明があります）を行ってください。
User personas involve creating a hypothetical user. 
ユーザーペルソナは仮想のユーザーを作成することを含みます。
For instance, if your team is all male, it might help to design a 35-year-old female user persona (complete with user features), and look at the results it generates rather than 10 results for 25-to-40 year old males. 
例えば、チームが全員男性である場合、35歳の女性ユーザーペルソナ（ユーザーの特徴を含む）を設計し、25歳から40歳の男性に対する10の結果ではなく、それが生成する結果を見てみると良いでしょう。
Bringing in actual people to watch their reaction to your site (locally or remotely) in usability testing can also get you a fresh perspective. 
実際の人々を招いて、ユーザビリティテストであなたのサイトに対する反応を見てもらうこと（ローカルまたはリモートで）も、新しい視点を得ることができます。

#### Rule #24: Measure the delta between models. ルール #24: モデル間の差分を測定する。

One of the easiest and sometimes most useful measurements you can make before any users have looked at your new model is to calculate just how different the new results are from production. 
ユーザが新しいモデルを見ていない段階で行える最も簡単で、時には最も有用な測定の一つは、新しい結果が本番環境とどれほど異なるかを計算することです。
For instance, if you have a ranking problem, run both models on a sample of queries through the entire system, and look at the size of the symmetric difference of the results (weighted by ranking position). 
例えば、ランキングの問題がある場合、両方のモデルをサンプルクエリのセットでシステム全体に通して実行し、結果の対称差の大きさ（ランキング位置で重み付けされた）を見てください。
If the difference is very small, then you can tell without running an experiment that there will be little change. 
もし差が非常に小さい場合、実験を行わなくても、ほとんど変化がないことがわかります。
If the difference is very large, then you want to make sure that the change is good. 
もし差が非常に大きい場合、その変化が良いものであることを確認したいです。
Looking over queries where the symmetric difference is high can help you to understand qualitatively what the change was like. 
対称差が大きいクエリを見直すことで、変化がどのようなものであったかを定性的に理解するのに役立ちます。
Make sure, however, that the system is stable. 
ただし、システムが安定していることを確認してください。
Make sure that a model when compared with itself has a low (ideally zero) symmetric difference. 
モデルが自分自身と比較したときに、低い（理想的にはゼロの）対称差を持つことを確認してください。

<!-- ここまで読んだ! -->

#### Rule #25: When choosing models, utilitarian performance trumps predictive power. 
#### ルール #25: モデルを選択する際には、実用的なパフォーマンスが予測力を上回る。

Your model may try to predict click-through rate. 
あなたのモデルはクリック率を予測しようとするかもしれません。
However, in the end, the key question is what you do with that prediction. 
しかし、最終的には、その予測をどのように利用するかが重要な問いです。
If you are using it to rank documents, then the quality of the final ranking matters more than the prediction itself. 
**もしそれを文書のランキングに使用しているのであれば、最終的なランキングの質が予測そのものよりも重要です。**
If you predict the probability that a document is spam and then have a cutoff on what is blocked, then the precision of what is allowed through matters more. 
もし文書がスパムである確率を予測し、ブロックするもののカットオフを設定するのであれば、通過を許可するものの精度がより重要です。
Most of the time, these two things should be in agreement: when they do not agree, it will likely be on a small gain. 
ほとんどの場合、これら二つのことは一致しているべきです：もし一致しない場合、それはおそらく小さな利益に関することです。
Thus, if there is some change that improves log loss but degrades the performance of the system, look for another feature. 
**したがって、ログ損失を改善するがシステムのパフォーマンスを低下させるような変更がある場合は、別の特徴量を探してください。**
When this starts happening more often, it is time to revisit the objective of your model. 
このようなことがより頻繁に起こり始めたら、あなたのモデルの目的を再検討する時です。

<!-- ここまで読んだ! -->

#### Rule #26: Look for patterns in the measured errors, and create new features. 
#### ルール #26: 測定された誤差のパターンを探し、新しい特徴を作成する。

Suppose that you see a training example that the model got "wrong". 
モデルが「間違った」と判断したトレーニング例を見たとしましょう。
In a classification task, this error could be a false positive or a false negative. 
分類タスクでは、この誤りは偽陽性または偽陰性である可能性があります。
In a ranking task, the error could be a pair where a positive was ranked lower than a negative. 
ランキングタスクでは、誤りはポジティブがネガティブよりも低くランク付けされたペアである可能性があります。
The most important point is that this is an example that the machine learning system knows it got wrong and would like to fix if given the opportunity. 
**最も重要な点は、これは機械学習システムが間違ったことを認識しており、機会があれば修正したいと考えている例であるということです**。
If you give the model a feature that allows it to fix the error, the model will try to use it. 
もしあなたがモデルに誤りを修正するための特徴を与えれば、モデルはそれを使おうとします。

On the other hand, if you try to create a feature based upon examples the system doesn’t see as mistakes, the feature will be ignored. 
一方で、システムが誤りと見なさない例に基づいて特徴を作成しようとすると、その特徴は無視されます。
For instance, suppose that in Play Apps Search, someone searches for "free games". 
例えば、Play Apps Searchで誰かが「無料ゲーム」を検索したとしましょう。
Suppose one of the top results is a less relevant gag app. 
トップの結果の一つがあまり関連性のないギャグアプリであるとします。
So you create a feature for "gag apps". 
そこで、「ギャグアプリ」のための特徴を作成します。
However, if you are maximizing number of installs, and people install a gag app when they search for free games, the "gag apps" feature won’t have the effect you want. 
しかし、インストール数を最大化しようとしている場合、ユーザーが「無料ゲーム」を検索したときにギャグアプリをインストールするなら、「ギャグアプリ」特徴はあなたが望む効果を持たないでしょう。

Once you have examples that the model got wrong, look for trends that are outside your current feature set. 
モデルが間違った例を持っている場合は、現在の特徴セットの外にあるトレンドを探してください。
For instance, if the system seems to be demoting longer posts, then add post length. 
例えば、システムが長い投稿を降格させているようであれば、投稿の長さを追加します。
Don’t be too specific about the features you add. 
追加する特徴についてあまり具体的にならないでください。
If you are going to add post length, don’t try to guess what long means, just add a dozen features and let the model figure out what to do with them (see Rule #21). 
**投稿の長さを追加する場合は、「長い」が何を意味するかを推測しようとせず、十数個の特徴を追加し、モデルにそれらをどう扱うかを考えさせてください**（ルール #21を参照）。
That is the easiest way to get what you want. 
それがあなたが望むものを得る最も簡単な方法です。

<!-- ここまで読んだ! -->

#### Rule #27: Try to quantify observed undesirable behavior. ルール #27: 観察された望ましくない行動を定量化しよう。

Some members of your team will start to be frustrated with properties of the system they don’t like which aren’t captured by the existing loss function. 
チームの一部のメンバーは、既存の損失関数に捉えられていないシステムの特性に対して不満を持ち始めるでしょう。
At this point, they should do whatever it takes to turn their gripes into solid numbers. 
この時点で、彼らは自分たちの不満を具体的な数値に変えるために何でもするべきです。
For example, if they think that too many "gag apps" are being shown in Play Search, they could have human raters identify gag apps. 
例えば、彼らがPlay Searchにおいて「ギャグアプリ」が多すぎると考えている場合、人間の評価者にギャグアプリを特定させることができます。
(You can feasibly use humanlabelled data in this case because a relatively small fraction of the queries account for a large fraction of the traffic.) 
（この場合、比較的小さな割合のクエリが大きな割合のトラフィックを占めるため、人間がラベル付けしたデータを実際に使用することができます。）

If your issues are measurable, then you can start using them as features, objectives, or metrics. 
**もしあなたの問題が測定可能であれば、それらを特徴、目的、または指標として使用し始めることができます**。
The general rule is "measure first, optimize second". 
**一般的なルールは「まず測定し、次に最適化する」です。**

<!-- ここまで読んだ! -->

#### Rule #28: Be aware that identical short-term behavior does not imply identical long-term behavior. 
#### ルール #28: 同一の短期的な挙動が同一の長期的な挙動を意味しないことに注意してください。

Imagine that you have a new system that looks at every doc_id and exact_query, 
新しいシステムがすべてのdoc_idとexact_queryを見ていると想像してください。
and then calculates the probability of click for every doc for every query. 
そして、すべてのクエリに対して各ドキュメントのクリック確率を計算します。
You find that its behavior is nearly identical to your current system in both 
あなたは、その挙動が現在のシステムとほぼ同一であることを、サイドバイサイドテストとA/Bテストの両方で確認します。
side by sides and A/B testing, so given its simplicity, you launch it. 
そのシンプルさを考慮して、それを導入します。
However, you notice that no new apps are being shown. Why? 
しかし、新しいアプリが表示されていないことに気付きます。なぜでしょうか？
Well, since your system only shows a doc based on its own history with that query, 
実際、あなたのシステムはそのクエリに対する自身の履歴に基づいてのみドキュメントを表示するため、
there is no way to learn that a new doc should be shown. 
新しいドキュメントを表示すべきであることを学ぶ方法がありません。
The only way to understand how such a system would work long-term is to have 
そのようなシステムが長期的にどのように機能するかを理解する唯一の方法は、
it train only on data acquired when the model was live. 
モデルが稼働しているときに取得したデータのみでトレーニングさせることです。
This is very difficult. 
これは非常に難しいことです。



### Training-Serving Skew トレーニング-サービングのずれ

Training-serving skew is a difference between performance during training and performance during serving. 
トレーニング-サービングのずれとは、トレーニング中のパフォーマンスとサービング中のパフォーマンスの違いです。
This skew can be caused by:
このずれは、以下の要因によって引き起こされる可能性があります。
- A discrepancy between how you handle data in the training and serving pipelines.
- トレーニングとサービングのパイプラインでデータを処理する方法の不一致。
- A change in the data between when you train and when you serve.
- トレーニング時とサービング時のデータの変化。
- A feedback loop between your model and your algorithm.
- モデルとアルゴリズムの間のフィードバックループ。

We have observed production machine learning systems at Google with training-serving skew that negatively impacts performance. 
私たちは、Googleの生産機械学習システムにおいて、パフォーマンスに悪影響を及ぼすトレーニング-サービングのずれを観察しました。
The best solution is to explicitly monitor it so that system and data changes don’t introduce skew unnoticed.
最良の解決策は、システムやデータの変更が気づかれずにずれを引き起こさないように、明示的に監視することです。



#### Rule #29: 

The best way to make sure that you train like you serve is to save the set of features used at serving time, and then pipe those features to a log to use them at training time. 
トレーニングがサービングと同じように行われることを確実にする最良の方法は、サービング時に使用される特徴のセットを保存し、それらの特徴をログにパイプしてトレーニング時に使用することです。

Even if you can’t do this for every example, do it for a small fraction, such that you can verify the consistency between serving and training (see Rule #37). 
すべての例に対してこれを行うことができなくても、一部の例に対して行い、サービングとトレーニングの一貫性を確認できるようにします（Rule #37を参照）。

Teams that have made this measurement at Google were sometimes surprised by the results. 
Googleでこの測定を行ったチームは、結果に驚くことがありました。

YouTube home page switched to logging features at serving time with significant quality improvements and a reduction in code complexity, and many teams are switching their infrastructure as we speak. 
YouTubeのホームページは、サービング時に特徴をログに記録するように切り替え、品質の大幅な改善とコードの複雑さの削減を実現しました。そして、多くのチームが現在、インフラを切り替えています。



#### Rule #30: Importance-weight sampled data, don’t arbitrarily drop it! ルール #30: 重要度重み付けされたサンプルデータを使用し、恣意的に削除しないこと！

When you have too much data, there is a temptation to take files 1-12, and ignore files 13-99. 
データが多すぎると、ファイル1-12を選び、ファイル13-99を無視したくなる誘惑があります。 
This is a mistake. 
これは間違いです。 
Although data that was never shown to the user can be dropped, importance weighting is best for the rest. 
ユーザーに一度も表示されなかったデータは削除できますが、残りのデータには重要度重み付けが最適です。 
Importance weighting means that if you decide that you are going to sample example X with a 30% probability, then give it a weight of 10/3. 
重要度重み付けとは、例Xを30%の確率でサンプリングすることに決めた場合、その重みを10/3にすることを意味します。 
With importance weighting, all of the calibration properties discussed in Rule #14 still hold. 
重要度重み付けを使用すると、ルール#14で議論されたすべてのキャリブレーション特性が依然として保持されます。



#### Rule #31: Beware that if you join data from a table at training and serving time, the data in the table may change.

Rule #31: トレーニング時とサービング時にテーブルからデータを結合する場合、テーブル内のデータが変更される可能性があることに注意してください。

Say you join doc ids with a table containing features for those docs (such as number of comments or clicks).

ドキュメントIDを、コメント数やクリック数などの特徴を含むテーブルと結合するとします。

Between training and serving time, features in the table may be changed.

トレーニング時とサービング時の間に、テーブル内の特徴が変更される可能性があります。

Your model's prediction for the same document may then differ between training and serving.

その結果、同じドキュメントに対するモデルの予測がトレーニング時とサービング時で異なる場合があります。

The easiest way to avoid this sort of problem is to log features at serving time (see Rule #32).

この種の問題を避ける最も簡単な方法は、サービング時に特徴をログに記録することです（Rule #32を参照）。

If the table is changing only slowly, you can also snapshot the table hourly or daily to get reasonably close data.

テーブルがゆっくりとしか変化しない場合は、テーブルを毎時または毎日スナップショットして、合理的に近いデータを取得することもできます。

Note that this still doesn’t completely resolve the issue.

ただし、これでも問題が完全に解決されるわけではないことに注意してください。



#### Rule #32: Re-use code between your training pipeline and your serving pipeline whenever possible.

Batch processing is different than online processing. 
バッチ処理はオンライン処理とは異なります。

In online processing, you must handle each request as it arrives (e.g. you must do a separate lookup for each query), whereas in batch processing, you can combine tasks (e.g. making a join). 
オンライン処理では、リクエストが到着するたびにそれを処理しなければなりません（例えば、各クエリに対して別々のルックアップを行う必要があります）が、バッチ処理ではタスクを結合することができます（例えば、結合を行うことができます）。

At serving time, you are doing online processing, whereas training is a batch processing task. 
サービング時にはオンライン処理を行い、トレーニングはバッチ処理タスクです。

However, there are some things that you can do to re-use code. 
ただし、コードを再利用するためにできることがいくつかあります。

For example, you can create an object that is particular to your system where the result of any queries or joins can be stored in a very human readable way, and errors can be tested easily. 
例えば、システムに特有のオブジェクトを作成し、クエリや結合の結果を非常に人間が読みやすい方法で保存し、エラーを簡単にテストできるようにすることができます。

Then, once you have gathered all the information, during serving or training, you run a common method to bridge between the human-readable object that is specific to your system, and whatever format the machine learning system expects. 
次に、すべての情報を収集したら、サービングまたはトレーニング中に、システムに特有の人間が読みやすいオブジェクトと、機械学習システムが期待する形式との間を橋渡しする共通のメソッドを実行します。

This eliminates a source of training-serving skew. 
これにより、トレーニングとサービングのずれの原因が排除されます。

As a corollary, try not to use two different programming languages between training and serving. 
その結果として、トレーニングとサービングの間で異なる2つのプログラミング言語を使用しないようにしてください。

That decision will make it nearly impossible for you to share code. 
その決定は、コードを共有することをほぼ不可能にします。



#### Rule #33: If you produce a model based on the data until January 5th, test the model on the data from January 6th and after.
ルール #33: 1月5日までのデータに基づいてモデルを作成した場合、1月6日以降のデータでモデルをテストしてください。

In general, measure performance of a model on the data gathered after the data you trained the model on, as this better reflects what your system will do in production.
一般的に、モデルを訓練したデータの後に収集したデータでモデルの性能を測定してください。これは、あなたのシステムが本番環境でどのように機能するかをよりよく反映します。

If you produce a model based on the data until January 5th, test the model on the data from January 6th.
1月5日までのデータに基づいてモデルを作成した場合、1月6日のデータでモデルをテストしてください。

You will expect that the performance will not be as good on the new data, but it shouldn’t be radically worse.
新しいデータでの性能がそれほど良くないことを予想するでしょうが、劇的に悪くなるべきではありません。

Since there might be daily effects, you might not predict the average click rate or conversion rate, but the area under the curve, which represents the likelihood of giving the positive example a score higher than a negative example, should be reasonably close.
日々の影響があるかもしれないので、平均クリック率やコンバージョン率を予測できないかもしれませんが、正の例に負の例よりも高いスコアを与える可能性を表す曲線の下の面積は、合理的に近いはずです。



#### Rule #34: In binary classification for filtering (such as spam detection or determining interesting emails), make small short-term sacrifices in performance for very clean data.

ルール #34: フィルタリング（スパム検出や興味のあるメールの判定など）のための二項分類において、非常にクリーンなデータのために短期的にパフォーマンスを少し犠牲にすること。

In a filtering task, examples which are marked as negative are not shown to the user. 

フィルタリングタスクでは、ネガティブとしてマークされた例はユーザーに表示されません。

Suppose you have a filter that blocks 75% of the negative examples at serving. 

例えば、提供時に75%のネガティブ例をブロックするフィルタがあるとします。

You might be tempted to draw additional training data from the instances shown to users. 

ユーザーに表示されたインスタンスから追加のトレーニングデータを引き出したくなるかもしれません。

For example, if a user marks an email as spam that your filter let through, you might want to learn from that. 

例えば、ユーザーがフィルタを通過させたメールをスパムとしてマークした場合、それから学びたいと思うかもしれません。

But this approach introduces sampling bias. 

しかし、このアプローチはサンプリングバイアスを引き起こします。

You can gather cleaner data if instead during serving you label 1% of all traffic as "held out", and send all held out examples to the user. 

代わりに、提供時に全トラフィックの1%を「保持」としてラベル付けし、すべての保持された例をユーザーに送信することで、よりクリーンなデータを収集できます。

Now your filter is blocking at least 74% of the negative examples. 

これで、フィルタは少なくとも74%のネガティブ例をブロックしています。

These held out examples can become your training data. 

これらの保持された例は、あなたのトレーニングデータとなる可能性があります。

Note that if your filter is blocking 95% of the negative examples or more, this approach becomes less viable. 

フィルタが95%以上のネガティブ例をブロックしている場合、このアプローチはあまり実行可能ではなくなります。

Even so, if you wish to measure serving performance, you can make an even tinier sample (say 0.1% or 0.001%). 

それでも、提供パフォーマンスを測定したい場合は、さらに小さなサンプル（例えば0.1%または0.001%）を作成できます。

Ten thousand examples is enough to estimate performance quite accurately. 

1万の例があれば、パフォーマンスをかなり正確に推定するのに十分です。



#### Rule #35: Beware of the inherent skew in ranking problems. 
#### ルール #35: ランキング問題に内在する偏りに注意せよ。

When you switch your ranking algorithm radically enough that different results show up, you have effectively changed the data that your algorithm is going to see in the future. 
ランキングアルゴリズムを大幅に変更して異なる結果が表示される場合、実質的に将来アルゴリズムが見るデータを変更したことになります。

This kind of skew will show up, and you should design your model around it. 
この種の偏りは現れるため、モデルをそれに基づいて設計する必要があります。

There are multiple different approaches. 
いくつかの異なるアプローチがあります。

These approaches are all ways to favor data that your model has already seen. 
これらのアプローチはすべて、モデルがすでに見たデータを優遇する方法です。

1. Have higher regularization on features that cover more queries as opposed to those features that are on for only one query. 
1. 一つのクエリのみに関連する特徴ではなく、より多くのクエリをカバーする特徴に対して高い正則化を持たせること。

This way, the model will favor features that are specific to one or a few queries over features that generalize to all queries. 
このようにすることで、モデルはすべてのクエリに一般化する特徴よりも、一つまたは少数のクエリに特化した特徴を優遇します。

This approach can help prevent very popular results from leaking into irrelevant queries. 
このアプローチは、非常に人気のある結果が無関係なクエリに漏れ出すのを防ぐのに役立ちます。

Note that this is opposite the more conventional advice of having more regularization on feature columns with more unique values. 
これは、より多くのユニークな値を持つ特徴列に対してより多くの正則化を行うという従来のアドバイスとは逆であることに注意してください。

2. Only allow features to have positive weights. 
2. 特徴が正の重みを持つことのみを許可する。

Thus, any good feature will be better than a feature that is "unknown". 
したがって、良い特徴は「未知」の特徴よりも優れたものになります。

3. Don’t have document-only features. 
3. ドキュメント専用の特徴を持たない。

This is an extreme version of #1. 
これはルール#1の極端なバージョンです。

For example, even if a given app is a popular download regardless of what the query was, you don’t want to show it everywhere. 
例えば、特定のアプリがクエリに関係なく人気のダウンロードであっても、それをどこにでも表示したくはありません。

Not having document-only features keeps that simple. 
ドキュメント専用の特徴を持たないことで、それがシンプルになります。

The reason you don’t want to show a specific popular app everywhere has to do with the importance of making all the desired apps reachable. 
特定の人気アプリをどこにでも表示したくない理由は、すべての望ましいアプリにアクセス可能にすることの重要性に関係しています。

For instance, if someone searches for "bird watching app", they might download "angry birds", but that certainly wasn’t their intent. 
例えば、誰かが「バードウォッチングアプリ」を検索した場合、彼らは「アングリーバード」をダウンロードするかもしれませんが、それは確かに彼らの意図ではありませんでした。

Showing such an app might improve download rate, but leave the user’s needs ultimately unsatisfied. 
そのようなアプリを表示することはダウンロード率を向上させるかもしれませんが、最終的にユーザーのニーズを満たさない結果になります。



#### Rule #36: Avoid feedback loops with positional features. ルール #36: 位置特徴によるフィードバックループを避ける。

The position of content dramatically affects how likely the user is to interact with it. 
コンテンツの位置は、ユーザーがそれに対してどれだけインタラクトする可能性に大きく影響します。

If you put an app in the first position it will be clicked more often, 
アプリを最初の位置に置くと、より頻繁にクリックされるでしょう、

and you will be convinced it is more likely to be clicked. 
そして、それがクリックされる可能性が高いと確信することになります。

One way to deal with this is to add positional features, i.e. features about the position of the content in the page. 
これに対処する一つの方法は、位置特徴、つまりページ内のコンテンツの位置に関する特徴を追加することです。

You train your model with positional features, and it learns to weight, for example, the feature "1stposition" heavily. 
位置特徴を用いてモデルを訓練すると、例えば「1stposition」という特徴に重みを付けることを学習します。

Your model thus gives less weight to other factors for examples with "1stposition=true". 
その結果、モデルは「1stposition=true」の例に対して他の要因に対して少ない重みを与えます。

Then at serving you don't give any instances the positional feature, 
その後、提供時には、いかなるインスタンスにも位置特徴を与えず、

or you give them all the same default feature, 
またはすべてに同じデフォルトの特徴を与えます、

because you are scoring candidates before you have decided the order in which to display them. 
なぜなら、表示する順序を決定する前に候補をスコアリングしているからです。

Note that it is important to keep any positional features somewhat separate from the rest of the model because of this asymmetry between training and testing. 
訓練とテストの間のこの非対称性のために、位置特徴をモデルの他の部分からある程度分離しておくことが重要です。

Having the model be the sum of a function of the positional features and a function of the rest of the features is ideal. 
位置特徴の関数と他の特徴の関数の合計としてモデルを構成することが理想的です。

For example, don’t cross the positional features with any document feature. 
例えば、位置特徴を任意のドキュメント特徴と交差させないでください。



#### Rule #37: Measure Training/Serving Skew. ルール #37: トレーニング/サービングの偏りを測定する。

There are several things that can cause skew in the most general sense. 
最も一般的な意味での偏りを引き起こす要因はいくつかあります。

Moreover, you can divide it into several parts: 
さらに、これをいくつかの部分に分けることができます。

- The difference between the performance on the training data and the holdout data. 
- トレーニングデータとホールドアウトデータのパフォーマンスの違い。

In general, this will always exist, and it is not always bad. 
一般的に、これは常に存在し、必ずしも悪いことではありません。

- The difference between the performance on the holdout data and the "next-day" data. 
- ホールドアウトデータと「翌日」データのパフォーマンスの違い。

Again, this will always exist. 
再び、これは常に存在します。

You should tune your regularization to maximize the next-day performance. 
翌日のパフォーマンスを最大化するために、正則化を調整する必要があります。

However, large drops in performance between holdout and next-day data may indicate that some features are time-sensitive and possibly degrading model performance. 
ただし、ホールドアウトデータと翌日データの間でパフォーマンスが大幅に低下する場合は、いくつかの特徴が時間に敏感であり、モデルのパフォーマンスを低下させている可能性があることを示しているかもしれません。

- The difference between the performance on the "next-day" data and the live data. 
- 「翌日」データとライブデータのパフォーマンスの違い。

If you apply a model to an example in the training data and the same example at serving, it should give you exactly the same result (see Rule #5). 
トレーニングデータの例にモデルを適用し、サービング時に同じ例に適用した場合、正確に同じ結果を返すべきです（ルール #5を参照）。

Thus, a discrepancy here probably indicates an engineering error. 
したがって、ここでの不一致はおそらくエンジニアリングエラーを示しています。



## ML Phase III: Slowed Growth, Optimization Refinement, and Complex Models MLフェーズIII: 成長の鈍化、最適化の洗練、複雑なモデル

There will be certain indications that the second phase is reaching a close. 
第二フェーズが終わりに近づいていることを示すいくつかの兆候があります。

First of all, your monthly gains will start to diminish. 
まず第一に、あなたの月次の利益は減少し始めるでしょう。

You will start to have tradeoffs between metrics: you will see some rise and others fall in some experiments. 
メトリクス間でトレードオフが発生し始めます：いくつかの実験では、ある指標が上昇し、他の指標が下降するのを見るでしょう。

This is where it gets interesting. 
ここが面白くなるところです。

Since the gains are harder to achieve, the machine learning has to get more sophisticated. 
利益を得ることが難しくなるため、機械学習はより洗練される必要があります。

A caveat: this section has more blue-sky rules than earlier sections. 
注意点：このセクションには、以前のセクションよりも多くの理想的なルールがあります。

We have seen many teams go through the happy times of Phase I and Phase II machine learning. 
私たちは、多くのチームがフェーズIとフェーズIIの機械学習の幸せな時期を経験するのを見てきました。

Once Phase III has been reached, teams have to find their own path. 
フェーズIIIに達すると、チームは自分たちの道を見つけなければなりません。



#### Rule #38: Don’t waste time on new features if unaligned objectives have become the issue.

#### ルール #38: 一致しない目標が問題になっている場合、新しい機能に時間を浪費しないこと。

As your measurements plateau, your team will start to look at issues that are outside the scope of the objectives of your current machine learning system. 
測定値が横ばいになると、チームは現在の機械学習システムの目標の範囲外にある問題に目を向け始めます。

As stated before, if the product goals are not covered by the existing algorithmic objective, you need to change either your objective or your product goals. 
前述のように、製品の目標が既存のアルゴリズムの目標に含まれていない場合、目標または製品の目標のいずれかを変更する必要があります。

For instance, you may optimize clicks, plus-ones, or downloads, but make launch decisions based in part on human raters. 
例えば、クリック数、プラスワン、ダウンロードを最適化することはできますが、リリースの決定は部分的に人間の評価者に基づいて行うことがあります。



#### Rule #39: Launch decisions are a proxy for long-term product goals. 

Rule #39: ローンチの決定は長期的な製品目標の代理である。

Alice has an idea about reducing the logistic loss of predicting installs. 
アリスは、インストール予測のロジスティック損失を減少させるアイデアを持っています。

She adds a feature. 
彼女は新しい機能を追加します。

The logistic loss drops. 
ロジスティック損失は低下します。

When she does a live experiment, she sees the install rate increase. 
彼女がライブ実験を行うと、インストール率が増加するのが見えます。

However, when she goes to a launch review meeting, someone points out that the number of daily active users drops by 5%. 
しかし、彼女がローンチレビュー会議に行くと、誰かが日次アクティブユーザー数が5%減少していることを指摘します。

The team decides not to launch the model. 
チームはそのモデルをローンチしないことを決定します。

Alice is disappointed, but now realizes that launch decisions depend on multiple criteria, only some of which can be directly optimized using ML. 
アリスは失望しますが、ローンチの決定は複数の基準に依存しており、そのうちのいくつかはMLを使用して直接最適化できることに気づきます。

The truth is that the real world is not dungeons and dragons: there are no "hit points" identifying the health of your product. 
真実は、現実の世界はダンジョンズ＆ドラゴンズではなく、製品の健康状態を示す「ヒットポイント」は存在しないということです。

The team has to use the statistics it gathers to try to effectively predict how good the system will be in the future. 
チームは収集した統計を使用して、将来システムがどれほど良くなるかを効果的に予測しようとしなければなりません。

They need to care about engagement, 1 day active users (DAU), 30 DAU, revenue, and advertiser’s return on investment. 
彼らはエンゲージメント、1日アクティブユーザー（DAU）、30日DAU、収益、広告主の投資収益率を気にする必要があります。

These metrics that are measurable in A/B tests in themselves are only a proxy for more longterm goals: satisfying users, increasing users, satisfying partners, and profit, 
A/Bテストで測定可能なこれらの指標は、ユーザーを満足させ、ユーザーを増やし、パートナーを満足させ、利益を上げるというより長期的な目標の代理に過ぎません。

which even then you could consider proxies for having a useful, high quality product and a thriving company five years from now. 
これらは、今後5年間で有用で高品質な製品と繁栄する会社を持つことの代理と見なすことができます。

The only easy launch decisions are when all metrics get better (or at least do not get worse). 
すべての指標が改善される（または少なくとも悪化しない）ときだけが、簡単なローンチの決定です。

If the team has a choice between a sophisticated machine learning algorithm, and a simple heuristic, if the simple heuristic does a better job on all these metrics, it should choose the heuristic. 
チームが洗練された機械学習アルゴリズムと単純なヒューリスティックの間で選択肢がある場合、単純なヒューリスティックがすべての指標でより良い結果を出すなら、ヒューリスティックを選ぶべきです。

Moreover, there is no explicit ranking of all possible metric values. 
さらに、すべての可能な指標値の明示的なランキングは存在しません。

Specifically, consider the following two scenarios: 
具体的には、次の2つのシナリオを考えてみてください。

If the current system is A, then the team would be unlikely to switch to B. 
現在のシステムがAであれば、チームはBに切り替える可能性は低いでしょう。

If the current system is B, then the team would be unlikely to switch to A. 
現在のシステムがBであれば、チームはAに切り替える可能性は低いでしょう。

This seems in conflict with rational behavior; however, predictions of changing metrics may or may not pan out, and thus there is a large risk involved with either change. 
これは合理的な行動と矛盾しているように見えますが、指標の変化の予測は実現するかどうかわからず、したがってどちらの変更にも大きなリスクが伴います。

Each metric covers some risk with which the team is concerned. 
各指標は、チームが懸念しているリスクの一部をカバーしています。

Moreover, no metric covers the team’s ultimate concern, "where is my product going to be five years from now"? 
さらに、どの指標もチームの最終的な懸念である「私の製品は5年後にどこにあるのか？」をカバーしていません。

Individuals, on the other hand, tend to favor one objective that they can directly optimize. 
一方、個人は直接最適化できる1つの目標を好む傾向があります。

Most machine learning tools favor such an environment. 
ほとんどの機械学習ツールは、そのような環境を好みます。

An engineer banging out new features can get a steady stream of launches in such an environment. 
新機能を次々と開発するエンジニアは、そのような環境で安定したローンチの流れを得ることができます。

There is a type of machine learning, multi-objective learning, which starts to address this problem. 
この問題に取り組み始める機械学習の一種であるマルチオブジェクティブラーニングがあります。

For instance, one can formulate a constraint satisfaction problem that has lower bounds on each metric, and optimizes some linear combination of metrics. 
例えば、各指標に下限を持つ制約充足問題を定式化し、指標のいくつかの線形結合を最適化することができます。

However, even then, not all metrics are easily framed as machine learning objectives: 
しかし、それでもすべての指標が機械学習の目的として簡単に定義できるわけではありません。

if a document is clicked on or an app is installed, it is because that the content was shown. 
ドキュメントがクリックされたりアプリがインストールされたりするのは、そのコンテンツが表示されたからです。

But it is far harder to figure out why a user visits your site. 
しかし、ユーザーがあなたのサイトを訪れる理由を見つけるのははるかに難しいです。

How to predict the future success of a site as a whole is AI-complete: as hard as computer vision or natural language processing. 
サイト全体の将来の成功を予測することはAI完全であり、コンピュータビジョンや自然言語処理と同じくらい難しいです。



#### Rule #40: Keep ensembles simple. ルール #40: アンサンブルはシンプルに保つ。

Unified models that take in raw features and directly rank content are the easiest models to debug and understand. 
生の特徴を取り込み、コンテンツを直接ランク付けする統一モデルは、デバッグや理解が最も容易なモデルです。しかし、an ensemble of models (a "model" which combines the scores of other models) can work better. 
しかし、他のモデルのスコアを組み合わせる「モデル」であるアンサンブルモデルは、より良い結果を出すことがあります。To keep things simple, each model should either be an ensemble only taking the input of other models, or a base model taking many features, but not both. 
シンプルに保つために、各モデルは他のモデルの入力のみを受け取るアンサンブルであるか、多くの特徴を受け取るベースモデルであるべきであり、両方であってはいけません。If you have models on top of other models that are trained separately, then combining them can result in bad behavior. 
別々に訓練されたモデルの上に他のモデルがある場合、それらを組み合わせると悪い動作を引き起こす可能性があります。

Use a simple model for ensembling that takes only the output of your "base" models as inputs. 
アンサンブルには、あなたの「ベース」モデルの出力のみを入力として受け取るシンプルなモデルを使用してください。You also want to enforce properties on these ensemble models. 
また、これらのアンサンブルモデルに特性を強制したいと思います。For example, an increase in the score produced by a base model should not decrease the score of the ensemble. 
例えば、ベースモデルによって生成されたスコアの増加は、アンサンブルのスコアを減少させてはなりません。Also, it is best if the incoming models are semantically interpretable (for example, calibrated) so that changes of the underlying models do not confuse the ensemble model. 
また、入ってくるモデルが意味的に解釈可能（例えば、キャリブレーションされている）であることが望ましく、基礎モデルの変更がアンサンブルモデルを混乱させないようにします。Also, enforce that an increase in the predicted probability of an underlying classifier does not decrease the predicted probability of the ensemble. 
さらに、基礎分類器の予測確率の増加がアンサンブルの予測確率を減少させないように強制します。



#### Rule #41: When performance plateaus, look for qualitatively new sources of information to add rather than refining existing signals.

Rule #41: パフォーマンスが横ばいになったときは、既存の信号を洗練させるのではなく、質的に新しい情報源を追加することを検討してください。

You’ve added some demographic information about the user. 
ユーザに関するいくつかの人口統計情報を追加しました。

You've added some information about the words in the document. 
文書内の単語に関する情報も追加しました。

You have gone through template exploration, and tuned the regularization. 
テンプレートの探索を行い、正則化を調整しました。

You haven’t seen a launch with more than a 1% improvement in your key metrics in a few quarters. 
ここ数四半期で、主要な指標に1%以上の改善をもたらすローンチを見たことがありません。

Now what? 
さて、次はどうしますか？

It is time to start building the infrastructure for radically different features, such as the history of documents that this user has accessed in the last day, week, or year, or data from a different property. 
このユーザが過去1日、1週間、または1年にアクセスした文書の履歴や、別のプロパティからのデータなど、根本的に異なる機能のためのインフラを構築し始める時です。

Use wikidata entities or something internal to your company (such as Google’s knowledge graph). 
Wikidataエンティティや、あなたの会社内部の何か（例えばGoogleの知識グラフ）を使用してください。

Use deep learning. 
深層学習を使用してください。

Start to adjust your expectations on how much return you expect on investment, and expand your efforts accordingly. 
投資に対するリターンの期待値を調整し、それに応じて努力を拡大し始めてください。

As in any engineering project, you have to weigh the benefit of adding new features against the cost of increased complexity. 
どんなエンジニアリングプロジェクトでもそうですが、新しい機能を追加することの利点と、複雑さの増加に伴うコストを天秤にかける必要があります。



#### Rule #42: Don’t expect diversity, personalization, or relevance to be as correlated with popularity as you think they are.
ルール #42: 多様性、パーソナライズ、または関連性が人気と同じくらい相関していると期待しないでください。

Diversity in a set of content can mean many things, with the diversity of the source of the content being one of the most common. 
コンテンツのセットにおける多様性は多くの意味を持ち、コンテンツのソースの多様性が最も一般的なものの一つです。

Personalization implies each user gets their own results. 
パーソナライズは、各ユーザーが自分自身の結果を得ることを意味します。

Relevance implies that the results for a particular query are more appropriate for that query than any other. 
関連性は、特定のクエリに対する結果が他のどの結果よりもそのクエリに適していることを意味します。

Thus all three of these properties are defined as being different from the ordinary. 
したがって、これらの3つの特性はすべて、通常とは異なるものとして定義されます。

The problem is that the ordinary tends to be hard to beat. 
問題は、通常のものが打ち負かすのが難しい傾向があることです。

Note that if your system is measuring clicks, time spent, watches, +1s, reshares, et cetera, you are measuring the popularity of the content. 
あなたのシステムがクリック、費やした時間、視聴、+1、再共有などを測定している場合、あなたはコンテンツの人気を測定していることに注意してください。

Teams sometimes try to learn a personal model with diversity. 
チームは時々、多様性を持つ個人モデルを学ぼうとします。

To personalize, they add features that would allow the system to personalize (some features representing the user’s interest) or diversify (features indicating if this document has any features in common with other documents returned, such as author or content), and find that those features get less weight (or sometimes a different sign) than they expect. 
パーソナライズするために、彼らはシステムがパーソナライズできるようにする特徴（ユーザーの興味を表すいくつかの特徴）や多様化できる特徴（この文書が他の返された文書と共通の特徴を持っているかどうかを示す特徴、例えば著者やコンテンツ）を追加し、これらの特徴が期待したよりも重みが少ない（または時には異なる符号を持つ）ことを発見します。

This doesn’t mean that diversity, personalization, or relevance aren’t valuable. 
これは、多様性、パーソナライズ、または関連性が価値がないという意味ではありません。

As pointed out in the previous rule, you can do postprocessing to increase diversity or relevance. 
前のルールで指摘されたように、あなたは多様性や関連性を高めるために後処理を行うことができます。

If you see longer term objectives increase, then you can declare that diversity/relevance is valuable, aside from popularity. 
もし長期的な目標が増加するのを見た場合、あなたは多様性/関連性が人気とは別に価値があると宣言することができます。

You can then either continue to use your postprocessing, or directly modify the objective based upon diversity or relevance. 
その後、あなたは後処理を続けるか、多様性や関連性に基づいて目標を直接修正することができます。



#### Rule #43: Your friends tend to be the same across different products. Your interests tend not to be.
ルール #43: あなたの友人は異なる製品間で同じ傾向がありますが、あなたの興味はそうではありません。

Teams at Google have gotten a lot of traction from taking a model predicting the closeness of a connection in one product, and having it work well on another.
Googleのチームは、ある製品における接続の近さを予測するモデルを取り入れ、それが別の製品でもうまく機能することで多くの成果を上げています。

Your friends are who they are. 
あなたの友人はそのままの友人です。

On the other hand, I have watched several teams struggle with personalization features across product divides.
一方で、私はいくつかのチームが製品間のパーソナライズ機能に苦労しているのを見てきました。

Yes, it seems like it should work. 
はい、うまくいくはずのように思えます。

For now, it doesn’t seem like it does. 
現時点では、うまくいっているようには見えません。

What has sometimes worked is using raw data from one property to predict behavior on another.
時には、あるプロパティからの生データを使用して別のプロパティでの行動を予測することがうまくいくことがあります。

Also, keep in mind that even knowing that a user has a history on another property can help.
また、ユーザーが別のプロパティでの履歴を持っていることを知っているだけでも役立つことを忘れないでください。

For instance, the presence of user activity on two products may be indicative in and of itself.
例えば、2つの製品におけるユーザー活動の存在自体が示唆的である可能性があります。



## Related Work 関連研究

There are many documents on machine learning at Google as well as externally.
Google内外には、機械学習に関する多くの文書があります。
- Machine Learning Crash Course:
an introduction to applied machine learning.
- Machine Learning Crash Course: 実用的な機械学習への入門。
- Machine Learning: A Probabilistic Approach by Kevin Murphy for an understanding of the field of machine learning.
- Machine Learning: A Probabilistic Approach（ケビン・マーフィー著）: 機械学習の分野を理解するための書籍。
- Good Data Analysis:
a data science approach to thinking about data sets.
- Good Data Analysis: データセットについて考えるためのデータサイエンスアプローチ。
- Deep Learning by Ian Goodfellow et al for learning nonlinear models.
- Deep Learning（イアン・グッドフェロー他著）: 非線形モデルを学ぶための書籍。
- Google paper on technical debt, which has a lot of general advice.
- Googleの技術的負債に関する論文: 多くの一般的なアドバイスが含まれています。
- Tensorflow Documentation.
- Tensorflowのドキュメント。



## Acknowledgements 謝辞

Thanks to David Westbrook, Peter Brandt, Samuel Ieong, Chenyu Zhao, Li Wei,
Michalis Potamias, Evan Rosen, Barry Rosenberg, Christine Robson, James Pine,
Tal Shaked, Tushar Chandra, Mustafa Ispir, Jeremiah Harmsen, Konstantinos
Katsiapis, Glen Anderson, Dan Duckworth, Shishir Birmiwal, Gal Elidan, Su Lin
Wu, Jaihui Liu, Fernando Pereira, and Hrishikesh Aradhye for many corrections,
suggestions, and helpful examples for this document. 
この文書に対する多くの修正、提案、役立つ例を提供してくれたDavid Westbrook、Peter Brandt、Samuel Ieong、Chenyu Zhao、Li Wei、Michalis Potamias、Evan Rosen、Barry Rosenberg、Christine Robson、James Pine、Tal Shaked、Tushar Chandra、Mustafa Ispir、Jeremiah Harmsen、Konstantinos Katsiapis、Glen Anderson、Dan Duckworth、Shishir Birmiwal、Gal Elidan、Su Lin Wu、Jaihui Liu、Fernando Pereira、そしてHrishikesh Aradhyeに感謝します。
Also, thanks to Kristen Lefevre, Suddha Basu, and Chris Berg who helped with an earlier version. 
また、以前のバージョンを手伝ってくれたKristen Lefevre、Suddha Basu、Chris Bergにも感謝します。
Any errors, omissions, or (gasp!) unpopular opinions are my own.
いかなる誤り、脱落、または（驚愕！）不人気な意見は私自身のものです。



## Appendix 付録

There are a variety of references to Google products in this document. 
この文書には、Google製品に関するさまざまな参照があります。
To provide more context, I give a short description of the most common examples below.
より多くの文脈を提供するために、最も一般的な例について簡単に説明します。



### YouTube Overview YouTubeの概要

YouTube is a streaming video service. 
YouTubeはストリーミングビデオサービスです。

Both YouTube Watch Next and YouTube Home Page teams use ML models to rank video recommendations. 
YouTube Watch NextチームとYouTubeホームページチームの両方が、ビデオ推薦をランク付けするためにMLモデルを使用しています。

Watch Next recommends videos to watch after the currently playing one, 
Watch Nextは、現在再生中のビデオの後に視聴するビデオを推薦します。

while Home Page recommends videos to users browsing the home page. 
一方、ホームページは、ホームページを閲覧しているユーザーにビデオを推薦します。



### Google Play 概要

Google Play has many models solving a variety of problems. 
Google Playには、さまざまな問題を解決する多くのモデルがあります。
Play Search, Play Home Page Personalized Recommendations, and ‘Users Also Installed’ apps all use machine learning.
Play Search、Playホームページのパーソナライズされた推奨、そして「ユーザーがインストールしたアプリ」すべてが機械学習を使用しています。



### Google Plus Overview 概要

Google Plus used machine learning in a variety of situations: ranking posts in the "stream" of posts being seen by the user, ranking "What’s Hot" posts (posts that are very popular now), ranking people you know, et cetera. 
Google Plusは、ユーザーが見ている「ストリーム」の投稿のランキング、現在非常に人気のある投稿である「What’s Hot」投稿のランキング、知っている人のランキングなど、さまざまな状況で機械学習を使用しました。
Google Plus closed down all personal accounts in 2019, and was replaced by Google Currents for business accounts on July 6, 2020. 
Google Plusは2019年にすべての個人アカウントを閉鎖し、2020年7月6日にビジネスアカウント用にGoogle Currentsに置き換えられました。

Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License. 
特に記載がない限り、このページの内容はクリエイティブ・コモンズ 表示 4.0 ライセンスの下でライセンスされており、コードサンプルはApache 2.0ライセンスの下でライセンスされています。
For details, see the Google Developers Site Policies. 
詳細については、Google Developers Site Policiesを参照してください。
Java is a registered trademark of Oracle and/or its affiliates. 
JavaはOracleおよびその関連会社の登録商標です。
Last updated 2025-08-25 UTC. 
最終更新日 2025年8月25日 UTC。

- ConnectBlogBlueskyInstagramLinkedInX (Twitter)YouTube
- Blog
- Bluesky
- Instagram
- LinkedIn
- X (Twitter)
- YouTube
- ProgramsGoogle Developer ProgramGoogle Developer GroupsGoogle Developer ExpertsAcceleratorsGoogle Cloud & NVIDIA
- Google Developer Program
- Google Developer Groups
- Google Developer Experts
- Accelerators
- Google Cloud & NVIDIA
- Developer consolesGoogle API ConsoleGoogle Cloud Platform ConsoleGoogle Play ConsoleFirebase ConsoleActions on Google ConsoleCast SDK Developer ConsoleChrome Web Store DashboardGoogle Home Developer Console
- Google API Console
- Google Cloud Platform Console
- Google Play Console
- Firebase Console
- Actions on Google Console
- Cast SDK Developer Console
- Chrome Web Store Dashboard
- Google Home Developer Console



### Connect 接続

- Blog ブログ
- Bluesky ブルースカイ
- Instagram インスタグラム
- LinkedIn リンクトイン
- X (Twitter) X（ツイッター）
- YouTube ユーチューブ



### Programs プログラム

- Google Developer Program
- Google Developer Groups
- Google Developer Experts
- Accelerators
- Google Cloud & NVIDIA



### Developer consoles 開発者コンソール
- Google API Console
- Google Cloud Platform Console
- Google Play Console
- Firebase Console
- Actions on Google Console
- Cast SDK Developer Console
- Chrome Web Store Dashboard
- Google Home Developer Console
- Android
- Chrome
- Firebase
- Google Cloud Platform
- Google AI
- All products
- Terms
- Privacy
- Manage cookies
- English
- Deutsch
- Español
- Español – América Latina
- Français
- Indonesia
- Italiano
- Polski
- Português – Brasil
- Tiếng Việt
- Türkçe
- Русский
- עברית
- العربيّة
- فارسی
- हिंदी
- বাংলা
- ภาษาไทย
- 中文 – 简体
- 中文 – 繁體
- 日本語
- 한국어
