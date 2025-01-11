<https://netflixtechblog.com/ml-platform-meetup-infra-for-contextual-bandits-and-reinforcement-learning-4a90305948ef>

# ML Platform Meetup: Infra for Contextual Bandits and Reinforcement Learning  

## Faisal Siddiqi

Netflix Technology Blog
Follow
Netflix TechBlog
447
2
Listen
Share

Infrastructure for Contextual Bandits and Reinforcement Learning —theme of the ML Platform meetup hosted at Netflix, Los Gatos on Sep 12, 2019.
文脈バンディットと強化学習のためのインフラストラクチャ — 2019年9月12日にNetflixのロスガトスで開催されたMLプラットフォームミートアップのテーマです。

Contextual and Multi-armed Bandits enable faster and adaptive alternatives to traditional A/B Testing.
文脈バンディットとマルチアームバンディットは、従来のA/Bテストに対するより迅速で適応的な代替手段を提供します。

They enable rapid learning and better decision-making for product rollouts.
これにより、製品の展開において迅速な学習とより良い意思決定が可能になります。

Broadly speaking, these approaches can be seen as a stepping stone to full-on Reinforcement Learning (RL) with closed-loop, on-policy evaluation and model objectives tied to reward functions.
広く言えば、これらのアプローチは、closed-loop、on-policy評価、およびモデル目的が報酬関数に結びついている完全な強化学習（RL）へのステップストーンとして見ることができます。

- 上記の文の意味がよくわからないのでメモ
  - ざっくりbanditの手法は...
    - 簡易的な「試して学ぶシステム」
    - リアルタイムで行動してフィードバックを受け取って学ぶ（Closed-loop）
    - 行動ルール（ポリシー）を評価しながら改善していく（On-policy evaluation）
  - という感じで、「強化学習の基礎練習」として見做せるよって話...??:thinking:

At Netflix, we are running several such experiments.
Netflixでは、私たちはそのような実験をいくつか実施しています。
For example, one set of experiments is focussed on personalizing our artwork assets to quickly select and leverage the “winning” images for a title we recommend to our members.
例えば、ある実験のセットは、私たちのアートワーク資産をパーソナライズし、会員に推奨するタイトルの「勝利」画像を迅速に選択して活用することに焦点を当てています。

As with other traditional machine learning and deep learning paths, a lot of what the core algorithms can do depends upon the support they get from the surrounding infrastructure and the tooling that the ML platform provides.
他の従来の機械学習や深層学習の道と同様に、コアアルゴリズムができることの多くは、周囲のインフラストラクチャとMLプラットフォームが提供するツールからのサポートに依存しています。
Given the infrastructure space for RL approaches is still relatively nascent, we wanted to understand what others in the community are doing in this space.
**RLアプローチのためのインフラストラクチャの領域はまだ比較的新しいため、私たちはこの分野でコミュニティの他の人々が何をしているのかを理解したいと考えました**。
(meet upに参加・発表する動機としてめちゃめちゃ素敵だ...!:thinking:)

This was the motivation for the meetup’s theme.
これがミートアップのテーマの動機でした。
It featured three relevant talks from LinkedIn, Netflix and Facebook, and a platform architecture overview talk from first time participant Dropbox.
LinkedIn、Netflix、Facebookからの3つの関連する講演と、初参加のDropboxからのプラットフォームアーキテクチャの概要講演が行われました。

<!-- ここまで読んだ -->

# LinkedIn

[Slides](https://www.slideshare.net/FaisalZakariaSiddiqi/linkedin-talk-at-netflix-ml-platform-meetup-sep-2019) スライド

After a brief introduction on the theme and motivation of its choice, the talks were kicked off by Kinjal Basu from LinkedIn who talked about Online Parameter Selection for Web-Based Ranking via Bayesian Optimization.  
テーマとその選択の動機についての簡単な紹介の後、LinkedInのKinjal Basuによる「Bayesian Optimizationを用いたWebベースのランキングのためのオンラインパラメータ選択」についての講演が始まりました。
In this talk, Kinjal used the example of the LinkedIn Feed, to demonstrate how they use bandit algorithms to solve for the optimal parameter selection problem efficiently.  
この講演では、KinjalはLinkedIn Feedの例を用いて、**最適なパラメータ選択問題を効率的に解決するためにバンディットアルゴリズムをどのように使用しているか**を示しました。

He started by laying out some of the challenges around inefficiencies of engineering time when manually optimizing for weights/parameters in their business objective functions.  
彼は、**ビジネス目的関数における重みやパラメータを手動で最適化する際のエンジニアリング時間の非効率性に関するいくつかの課題**を説明することから始めました。
The key insight was that by assuming a latent Gaussian Process (GP) prior on the key business metric actions like viral engagement, job applications, etc., they were able to reframe the problem as a straight-forward black-box optimization problem.  
重要な洞察は、バイラルエンゲージメントや求人応募などの主要なビジネスメトリックアクションに対して潜在的なガウス過程（GP）事前分布を仮定することで、問題を単純なブラックボックス最適化問題として再定義できたことです。
This allowed them to use BayesOpt techniques to solve this problem.  
これにより、彼らはBayesOpt技術を使用してこの問題を解決することができました。

The algorithm used to solve this reformulated optimization problem is a popular E/E technique known as Thompson Sampling.  
この再定義された最適化問題を解決するために使用されるアルゴリズムは、**Thompson Samplingとして知られる人気のあるE/E技術 (探索/活用!)**です。
He talked about the infrastructure used to implement this.  
彼はこれを実装するために使用されるインフラストラクチャについて話しました。
They have built an offline BayesOpt library, a parameter store to retrieve the right set of parameters, and an online serving layer to score the objective at serving time given the parameter distribution for a particular member.  
彼らは、**オフラインのBayesOptライブラリ、適切なパラメータセットを取得するためのパラメータストア、および特定のメンバーのパラメータ分布に基づいて提供時に目的をスコアリングするためのオンラインサービングレイヤーを構築**しました。

He also described some practical considerations, like member-parameter stickiness, to avoid per session variance in a member’s experience.  
彼はまた、メンバーの体験におけるセッションごとのばらつきを避けるためのメンバー-パラメータの粘着性のような実用的な考慮事項についても説明しました。
Their offline parameter distribution is recomputed hourly, so the member experience remains consistent within the hour.  
**彼らのオフラインパラメータ分布は毎時再計算されるため、メンバーの体験は1時間内で一貫性を保ちます**。(学習は1時間に1回なのか...!:thinking:)
Some simulation results and some online A/B test results were shared, demonstrating substantial lifts in the primary business metrics, while keeping the secondary metrics above preset guardrails.  
いくつかのシミュレーション結果とオンラインA/Bテスト結果が共有され、**主要なビジネスメトリックにおいて大幅な向上が示される一方で、二次的なメトリックは事前に設定されたガードレールを上回ることが維持**されました。

He concluded by stressing the efficiency their teams had achieved by doing online parameter exploration instead of the much slower human-in-the-loop manual explorations.  
彼は、**はるかに遅い人間の介入による手動探索の代わりにオンラインパラメータ探索を行うことで、彼らのチームが達成した効率性**を強調して締めくくりました。

In the future, they plan to explore adding new algorithms like UCB, considering formulating the problem as a grey-box optimization problem, and switching between the various business metrics to identify which is the optimal metric to optimize.  
今後、彼らはUCBのような新しいアルゴリズムの追加を検討し、問題をグレーボックス最適化問題として定式化し、さまざまなビジネスメトリックの間で切り替えて最適なメトリックを特定することを計画しています。

<!-- ここまで読んだ -->

# Netflix

Slides スライド

The second talk was by Netflix on our Bandit Infrastructure built for personalization use cases.
2番目の講演は、パーソナライズのユースケースのために構築された私たちのバンディットインフラストラクチャに関するNetflixによるものでした。
Fernando Amat and Elliot Chow jointly gave this talk.
Fernando AmatとElliot Chowが共同でこの講演を行いました。

Fernando started the first part of the talk and described the core recommendation problem of identifying the top few titles in a large catalog that will maximize the probability of play.
Fernandoは講演の最初の部分を始め、**大規模なカタログの中から再生の確率を最大化するための上位数タイトルを特定するというコアな推薦問題**について説明しました。
Using the example of evidence personalization — images, text, trailers, synopsis, all assets that come together to add meaning to a title — he described how the problem is essentially a slate recommendation task and is well suited to be solved using a Bandit framework.
evidence personalization(証拠パーソナライズ?)（画像、テキスト、トレーラー、要約など、タイトルに意味を加えるために組み合わさるすべての資産）の例を用いて、彼はこの問題が本質的にスレート推薦タスクであり、バンディットフレームワークを使用して解決するのに適していることを説明しました。

(evidence personalization=ユーザにコンテンツを表示する際に、一緒に表示する捕捉情報を個々のユーザに合わせて最適化すること...!:thinking:)
(slate recommendation task=推薦タスクの中でも、「複数のアイテムをまとめて（スレート=
ひとまとまりのリスト）ユーザに提示するタスク」のこと...!:thinking:)

If such a framework is to be generic, it must support different contexts, attributions and reward functions.
**このようなフレームワークが一般的であるためには、異なるコンテキスト、属性情報、報酬関数をサポートする必要があり**ます。
He described a simple Policy API that models the Slate tasks.
彼はスレートタスクをモデル化するシンプルなポリシーAPIについて説明しました。
This API supports the selection of a state given a list of options using the appropriate algorithm and a way to quantify the propensities, so the data can be de-biased.
このAPIは、適切なアルゴリズムを使用してオプションのリストから状態を選択することをサポートし、傾向を定量化する方法を提供するため、データのバイアスを除去できます。
Fernando ended his part by highlighting some of the Bandit Metrics they implemented for offline policy evaluation, like Inverse Propensity Scoring (IPS), Doubly Robust (DR), and Direct Method (DM).
Fernandoは、オフラインポリシー評価のために実装したいくつかのバンディットメトリクス（逆傾向スコアリング（IPS）、ダブリーロバスト（DR）、直接法（DM）など）を強調して彼の部分を締めくくりました。（しっかりしてるなぁ...!:thinking:）

For Bandits, where attribution is a critical part of the equation, it’s imperative to have a flexible and robust data infrastructure.
attributionが方程式の重要な部分であるバンディットにとって、柔軟で堅牢なデータインフラストラクチャを持つことが不可欠です。
Elliot started the second part of the talk by describing the real-time framework they have built to bring together all signals in one place making them accessible through a queryable API.
Elliotは、**すべての信号(=x, a, rのこと??)を1か所に集約し、クエリ可能なAPIを通じてアクセスできるようにするために構築したリアルタイムフレームワーク**について説明することで、講演の2番目の部分を始めました。
These signals include member activity data (login, search, playback), intent-to-treat (what title/assets the system wants to impress to the member) and the treatment (impressions of images, trailers) that actually made it to the member’s device.
これらの信号には、メンバーの活動データ（ログイン、検索、再生）、intent-to-treat（システムがメンバーに印象付けたいタイトル/資産）、および実際にメンバーのデバイスに表示されたtreatment（画像、トレーラーの印象）が含まれます。
(i.e. ここでの"信号"というのは、文脈x, 行動a, 報酬rのことを指しているのかな...?:thinking:)

Elliot talked about what is involved in “Closing the loop”.
Elliotは「ループを閉じる」ことに関与する内容について話しました。
First, the intent-to-treat needs to be joined with the treatment logging along the way, the policies in effect, the features used and the various propensities.
まず、intent-to-treatは、途中でtreatmentログと結合され、有効なポリシー、使用される特徴、さまざまな傾向が必要です。
Next, the reward function needs to be updated, in near real time, on every logged action (like a playback) for both short-term and long-term rewards.
次に、報酬関数は、短期的および長期的な報酬のために、記録されたすべてのアクション（再生など）に対して、ほぼリアルタイムで更新する必要があります。
And finally each new observation needs to update the policy, compute offline policy evaluation metrics and then push the policy back to production so it can generate new intents to treat.
最後に、各新しいobservationはポリシーを更新し、オフラインポリシー評価メトリクスを計算し、その後ポリシーを本番環境に戻して新しいintent-to-treatを生成する必要があります。

To be able to support this, the team had to standardize on several infrastructure components.
これをサポートするために、チームはいくつかのインフラストラクチャコンポーネントを標準化する必要がありました。
Elliot talked about the three key components — a) Standardized Logging from the treatment services, b) Real-time stream processing over Apache Flink for member activity joins, and c) an Apache Spark client for attribution and reward computation.
Elliotは、3つの主要コンポーネントについて話しました — a) treatmentサービスからの標準化されたログ記録、b) メンバー活動データの結合のためのApache Flink上のリアルタイムストリーム処理、およびc) 属性と報酬の計算のためのApache Sparkクライアント。
The team has also developed a few common attribution datasets as “out-of-the-box” entities to be used by the consuming teams.
チームは、消費チームが使用するための「すぐに使える」エンティティとして、いくつかの共通のattributionデータセットも開発しました。

Finally, Elliot ended by talking about some of the challenges in building this Bandit framework.
最後に、Elliotはこのバンディットフレームワークを構築する際のいくつかの課題について話しました。
In particular, he talked about the misattribution potential in a complex microservice architecture where often intermediary results are cached.
特に、彼はしばしば中間結果がキャッシュされる複雑なマイクロサービスアーキテクチャにおける誤帰属の可能性について話しました。
He also talked about common pitfalls of stream-processed data like out of order processing.
彼はまた、**順序が乱れた処理のようなストリーム処理データの一般的な落とし穴**についても話しました。

This framework has been in production for almost a year now and has been used to support several A/B tests across different recommendation use cases at Netflix.
このフレームワークは、ほぼ1年間本番環境で稼働しており、Netflixのさまざまな推薦ユースケースでいくつかのA/Bテストをサポートするために使用されています。

<!-- ここまで読んだ -->

# Facebook

Slides
After a short break, the second session started with a talk from Facebook focussed on practical solutions to exploration problems.
短い休憩の後、第二セッションはFacebookからの発表で始まり、探索問題に対する実践的な解決策に焦点を当てました。

Sam Daulton described how the infrastructure and product use cases came along.
サム・ダルトンは、インフラストラクチャと製品のユースケースがどのように進展したかを説明しました。

He described how the adaptive experimentation efforts are aimed at enabling fast experimentation with a goal of adding varying degrees of automation for experts using the platform in an ad hoc fashion all the way to no-human-in-the-loop efforts.
彼は、適応的実験の取り組みが、プラットフォームをアドホックに使用する専門家のために、さまざまな自動化の程度を追加することを目指して迅速な実験を可能にすることを説明しました。

He dived into a policy search problem they tried to solve: How many posts to load for a user depending upon their device’s connection quality.
彼は、彼らが解決しようとしたポリシー検索の問題に深く入り込みました：ユーザーのデバイスの接続品質に応じて、どれだけの投稿を読み込むべきか。

They modeled the problem as an infinite-arm bandit problem and used Gaussian Process (GP) regression.
彼らはこの問題を無限アームバンディット問題としてモデル化し、ガウス過程（GP）回帰を使用しました。

They used Bayesian Optimization to perform multi-metric optimization — e.g., jointly optimizing decrease in CPU utilization along with increase in user engagement.
彼らはベイズ最適化を使用してマルチメトリック最適化を実行しました — 例えば、CPU使用率の低下とユーザーエンゲージメントの増加を共同で最適化しました。

One of the challenges he described was how to efficiently choose a decision point, when the joint optimization search presented a Pareto frontier in the possible solution space.
彼が説明した課題の一つは、共同最適化検索が可能な解空間においてパレートフロンティアを示すときに、どのように効率的に意思決定ポイントを選択するかということでした。

They used constraints on individual metrics in the face of noisy experiments to allow business decision makers to arrive at an optimal decision point.
彼らは、ノイズの多い実験に直面して個々のメトリックに制約を使用し、ビジネスの意思決定者が最適な意思決定ポイントに到達できるようにしました。

Not all spaces can be efficiently explored online, so several research teams at Facebook use Simulations offline.
すべての空間がオンラインで効率的に探索できるわけではないため、Facebookのいくつかの研究チームはオフラインでシミュレーションを使用します。

For example, a ranking team would ingest live user traffic and subject it to a number of ranking configurations and simulate the event outcomes using predictive models running on canary rankers.
例えば、ランキングチームはライブユーザートラフィックを取り込み、いくつかのランキング構成にさらし、カナリアランカーで動作する予測モデルを使用してイベントの結果をシミュレートします。

The simulations were often biased and needed de-biasing (using multi-task GP regression) for them to be used alongside online results.
シミュレーションはしばしばバイアスがかかっており、オンライン結果と一緒に使用するためにはデバイアス（マルチタスクGP回帰を使用）する必要がありました。

They observed that by combining their online results with de-biased simulation results they were able to substantially improve their model fit.
彼らは、オンライン結果とデバイアスされたシミュレーション結果を組み合わせることで、モデルの適合度を大幅に改善できることを観察しました。

To support these efforts, they developed and open sourced some tools along the way.
これらの取り組みを支援するために、彼らはいくつかのツールを開発し、オープンソース化しました。

Sam described Ax and BoTorch — Ax is a library for managing adaptive experiments and BoTorch is a library for Bayesian Optimization research.
サムはAxとBoTorchについて説明しました — Axは適応実験を管理するためのライブラリであり、BoTorchはベイズ最適化研究のためのライブラリです。

There are many applications already in production for these tools from both basic hyperparameter exploration to more involved AutoML use cases.
これらのツールには、基本的なハイパーパラメータ探索からより複雑なAutoMLユースケースまで、すでに多くのアプリケーションが本番環境で使用されています。

The final section of Sam’s talk focussed on Constrained Bayesian Contextual Bandits.
サムの発表の最後のセクションは、制約付きベイズコンテキストバンディットに焦点を当てました。

They described the problem of video uploads to Facebook where the goal is to maximize the quality of the video without a decrease in reliability of the upload.
彼らは、Facebookへの動画アップロードの問題を説明しました。この問題の目標は、アップロードの信頼性を低下させることなく、動画の品質を最大化することです。

They modeled it as a Thompson Sampling optimization problem using a Bayesian Linear model.
彼らはこれをベイズ線形モデルを使用したトンプソンサンプリング最適化問題としてモデル化しました。

To enforce the constraints, they used a modified algorithm, Constrained Thompson Sampling, to ensure a non-negative change in reliability.
制約を強制するために、彼らは修正されたアルゴリズムである制約付きトンプソンサンプリングを使用して、信頼性の非負の変化を確保しました。

The reward function also similarly needed some shaping to align with the constrained objective.
報酬関数もまた、制約された目的に合わせるためにいくつかの調整が必要でした。

With this reward shaping optimization, Sam shared some results that showed how the Constrained Thompson Sampling algorithm surfaced many actions that satisfied the reliability constraints, where vanilla Thompson Sampling had failed.
この報酬調整最適化により、サムは制約付きトンプソンサンプリングアルゴリズムが、バニラトンプソンサンプリングが失敗した信頼性制約を満たす多くのアクションを浮き彫りにした結果を共有しました。

# Dropbox

Slides
The last talk of the event was a system architecture introduction by Dropbox’s Tsahi Glik.
イベントの最後の講演は、DropboxのTsahi Glikによるシステムアーキテクチャの紹介でした。

As a first time participant, their talk was more of an architecture overview of the ML Infra in place at Dropbox.
初めての参加者として、彼の講演はDropboxにおけるMLインフラのアーキテクチャの概要に関するものでした。

Tsahi started off by giving some ML usage examples at Dropbox like Smart Sync which predicts which file you will use on a particular device, so it’s preloaded.
Tsahiは、特定のデバイスで使用するファイルを予測し、事前にロードするSmart SyncのようなDropboxでのML使用例をいくつか紹介しました。

Some of the challenges he called out were the diversity and size of the disparate data sources that Dropbox has to manage.
彼が指摘したいくつかの課題は、Dropboxが管理しなければならない多様で大規模な異なるデータソースのことでした。

Data privacy is increasingly important and presents its own set of challenges.
データプライバシーはますます重要になっており、それ自体の課題を提示しています。

From an ML practice perspective, they also have to deal with a wide variety of development processes and ML frameworks, custom work for new use cases and challenges with reproducibility of training.
MLの実践の観点から、彼らはさまざまな開発プロセスやMLフレームワーク、新しいユースケースのためのカスタム作業、トレーニングの再現性に関する課題にも対処しなければなりません。

He shared a high level overview of their ML platform showing the various common stages of developing and deploying a model categorized by the online and offline components.
彼は、オンラインおよびオフラインコンポーネントによって分類されたモデルの開発と展開のさまざまな共通ステージを示すMLプラットフォームの高レベルの概要を共有しました。

He then dived into some individual components of the platform.
その後、彼はプラットフォームのいくつかの個別のコンポーネントに深く掘り下げました。

The first component he talked about was a user activity service to collect the input signals for the models.
彼が最初に話したコンポーネントは、モデルの入力信号を収集するためのユーザーアクティビティサービスでした。

This service, Antenna, provides a way to query user activity events and summarizes the activity with various aggregations.
このサービス、Antennaは、ユーザーアクティビティイベントをクエリし、さまざまな集約でアクティビティを要約する方法を提供します。

The next component he dived deeper into was a content ingestion pipeline for OCR (optical character recognition).
次に、彼がさらに深く掘り下げたコンポーネントは、OCR（光学文字認識）のためのコンテンツ取り込みパイプラインでした。

As an example, he explained how the image of a receipt is converted into contextual text.
例として、彼はレシートの画像がどのように文脈に応じたテキストに変換されるかを説明しました。

The pipeline takes the image through multiple models for various subtasks.
このパイプラインは、さまざまなサブタスクのために画像を複数のモデルに通します。

The first classifies whether the image has some detectable text, the second does corner detection, the third does word box detection followed by deep LSTM neural net that does the core sequence based OCR.
最初のモデルは画像に検出可能なテキストがあるかどうかを分類し、2番目はコーナー検出を行い、3番目はワードボックス検出を行い、その後にコアシーケンスベースのOCRを行う深層LSTMニューラルネットが続きます。

The final stage performs some lexicographical post processing.
最終段階では、いくつかの辞書的な後処理が行われます。

He talked about the practical considerations of ingesting user content — they need to prevent malicious content from impacting the service.
彼はユーザーコンテンツの取り込みに関する実際的な考慮事項について話しました — 彼らは悪意のあるコンテンツがサービスに影響を与えるのを防ぐ必要があります。

To enable this they have adopted a plugin based architecture and each task plugin runs in a sandbox jail environment.
これを実現するために、彼らはプラグインベースのアーキテクチャを採用し、各タスクプラグインはサンドボックスの監獄環境で実行されます。

Their offline data preparation ETLs run on Spark and they use Airflow as the orchestration layer.
彼らのオフラインデータ準備ETLはSpark上で実行され、Airflowをオーケストレーションレイヤーとして使用しています。

Their training infrastructure relies on a hybrid cloud approach.
彼らのトレーニングインフラはハイブリッドクラウドアプローチに依存しています。

They have built a layer and command line tool called dxblearn that abstracts the training paths, allowing the researchers to train either locally or leverage AWS.
彼らはdxblearnと呼ばれるレイヤーとコマンドラインツールを構築し、トレーニングパスを抽象化し、研究者がローカルでトレーニングするか、AWSを活用することを可能にしています。

dxblearn also allows them to fire off training jobs for hyperparameter tuning.
dxblearnはまた、ハイパーパラメータチューニングのためのトレーニングジョブを開始することを可能にします。

Published models are sent to a model store in S3 which are then picked up by their central model prediction service that does online inferencing for all use cases.
公開されたモデルはS3のモデルストアに送信され、その後、すべてのユースケースのオンライン推論を行う中央モデル予測サービスによって取得されます。

Using a central inferencing service allows them to partition compute resources appropriately and having a standard API makes it easy to share and also run inferencing in the cloud.
中央推論サービスを使用することで、計算リソースを適切に分割でき、標準APIを持つことで共有やクラウドでの推論実行が容易になります。

They have also built a common “suggest backend” that is a generic predictive application that can be used by the various edge and production facing services that regularizes the data fetching, prediction and experiment configuration needed for a product prediction use case.
彼らはまた、さまざまなエッジおよびプロダクション向けサービスが使用できる一般的な予測アプリケーションである共通の「suggest backend」を構築しました。これは、製品予測ユースケースに必要なデータ取得、予測、および実験設定を標準化します。

This allows them to do live experimentation more easily.
これにより、彼らはライブ実験をより簡単に行うことができます。

The last part of Tsahi’s talk described a product use case leveraging their ML Platform.
Tsahiの講演の最後の部分では、彼らのMLプラットフォームを活用した製品ユースケースについて説明しました。

He used the example of a promotion campaign ranker, (eg “Try Dropbox business”) for up-selling.
彼は、アップセルのためのプロモーションキャンペーンランカー（例：「Dropboxビジネスを試してみて」）の例を挙げました。

This is modeled as a multi-armed bandit problem, an example well in line with the meetup theme.
これはマルチアームバンディット問題としてモデル化されており、ミートアップのテーマに沿った例です。

The biggest value of such meetups lies in the high bandwidth exchange of ideas from like-minded practitioners.
このようなミートアップの最大の価値は、同じ志を持つ実践者からのアイデアの高帯域幅の交換にあります。

In addition to some great questions after the talks, the 150+ attendees stayed well past 2 hours in the reception exchanging stories and lessons learnt solving similar problems at scale.
講演後の素晴らしい質問に加えて、150人以上の参加者は、レセプションで2時間以上も滞在し、同様の問題を大規模に解決する際に得たストーリーや教訓を交換しました。

In the Personalization org at Netflix, we are always interested in exchanging ideas about this rapidly evolving ML space in general and the bandits and reinforcement learning space in particular.
Netflixのパーソナライズ組織では、一般的にこの急速に進化するML分野や、特にバンディットおよび強化学習の分野についてアイデアを交換することに常に興味を持っています。

We are committed to sharing our learnings with the community and hope to discuss progress here, especially our work on Policy Evaluation and Bandit Metrics in future meetups.
私たちはコミュニティと学びを共有することにコミットしており、ここでの進捗について話し合うことを望んでいます。特に、今後のミートアップでのポリシー評価とバンディットメトリクスに関する私たちの作業についてです。

If you are interested in working on this exciting space, there are many open opportunities on both engineering and research endeavors.
このエキサイティングな分野での作業に興味がある場合、エンジニアリングと研究の両方の取り組みに多くのオープンな機会があります。

## Sign up to discover human stories that deepen your understanding of the world

世界の理解を深める人間の物語を発見するためにサインアップしてください。

## Free 無料

Distraction-free reading. No ads.  
気を散らさない読書。広告なし。

Organize your knowledge with lists and highlights.  
リストやハイライトを使って知識を整理しましょう。

Tell your story. Find your audience.  
自分の物語を語り、聴衆を見つけましょう。

## Membership メンバーシップ

Read member-only stories
メンバー限定のストーリーを読む

Support writers you read most
最もよく読む作家をサポートする

Earn money for your writing
自分の執筆でお金を稼ぐ

Listen to audio narrations
オーディオナレーションを聞く

Read offline with the Medium app
Mediumアプリでオフラインで読む

447
447

2
2

## Published inNetflix TechBlog 発表内容

Learn about Netflix’s world class engineering efforts, company culture, product developments and more.
Netflixの世界クラスのエンジニアリング努力、企業文化、製品開発などについて学びましょう。

## Written byNetflix Technology Blog 著者: Netflixテクノロジーブログ

Learn more about how Netflix designs, builds, and operates our systems and engineering organizations
Netflixがどのようにシステムとエンジニアリング組織を設計、構築、運用しているかについて、さらに詳しく学びましょう。

## More from Netflix Technology Blog and Netflix TechBlog NetflixテクノロジーブログおよびNetflix TechBlogからのさらなる情報

In
Netflix TechBlog
by
Netflix Technology Blog
において

## Netflix’s Distributed Counter Abstraction  

### By: Rajiv Shringi, Oleksii Tkachuk, Kartik Sathyanarayanan

著者: Rajiv Shringi, Oleksii Tkachuk, Kartik Sathyanarayanan
In
Netflix TechBlog
に掲載
by
Netflix Technology Blog

## Introducing Netflix’s TimeSeries Data Abstraction Layer  

### By Rajiv Shringi, Vinay Chella, Kaidan Fullerton, Oleksii Tkachuk, Joey Lynch

Netflix TechBlog による
Netflix Technology Blog

## Java 21 Virtual Threads - Dude, Where’s My Lock?  

### Getting real with virtual threads

Java 21の仮想スレッド - ねえ、私のロックはどこ？  

### 仮想スレッドの実際の利用

Netflix Technology Blog

## My Path Towards Data @ Netflix  

### by Lisa Herzog  

私のNetflixにおけるデータへの道  

### リサ・ヘルツォーク  

## Recommended from Medium

In
Towards Data Science
by
Massimiliano Costacurta
の中で

## Dynamic Pricing with Contextual Bandits: Learning by Doing  

### Adding context to your dynamic pricing problem can increase opportunities as well as challenges

文脈を動的価格設定の問題に追加することで、機会と同様に課題も増加する可能性があります。

In  
Towards Data Science  
による  
Ugur Yildirim  

## An Overview of Contextual Bandits コンテキストバンディットの概要

### A dynamic approach to treatment personalization 治療のパーソナライズに向けた動的アプローチ

## Lists リスト

## Predictive Modeling w/ Python 予測モデリング w/ Python

## Practical Guides to Machine Learning 実践的な機械学習ガイド

## Natural Language Processing 自然言語処理

## The New Chatbots: ChatGPT, Bard, and Beyond 新しいチャットボット：ChatGPT、Bard、そしてその先

In
tech-at-instacart
by
David Vengerov
にて
デイビッド・ヴェンゲロフによる

## Using Contextual Bandit models in large action spaces at Instacart  

### David Vengerov, Vinesh Gudla, Tejaswi Tenneti, Haixun Wang, Kourosh Hakhamaneshi

Instacartにおける大規模アクション空間での文脈バンディットモデルの使用  

### デイビッド・ヴェンゲロフ、ヴィネシュ・グドラ、テジャスウィ・テネティ、ハイシュン・ワン、クーロシュ・ハカマネシ  

In  
Netflix TechBlog  
による  
Netflix Technology Blog  

## Recommending for Long-Term Member Satisfaction at Netflix  

### By Jiangwei Pan, Gary Tang, Henry Wang, and Justin Basilico  

Netflixにおける長期会員満足度のための推薦  

### 著者: Jiangwei Pan, Gary Tang, Henry Wang, Justin Basilico  

In  
Lyft Engineering  
による  
Jonas Timmermann  

## Lyft’s Reinforcement Learning Platform Lyftの強化学習プラットフォーム  

### Tackling decision making problems with a platform for developing & serving Reinforcement Learning models with a focus on Contextual Bandits

意思決定問題に取り組むための、Contextual Banditsに焦点を当てた強化学習モデルの開発と提供のためのプラットフォーム  
In
Picnic Engineering
による  
by
Thijs Sluijter
著  

## Generating your shopping list with AI: recommendations at Picnic  

AIを使ったショッピングリストの生成：Picnicでの推薦

### How we find the best items for our customers  

私たちがどのように顧客に最適な商品を見つけるか。

Help  
ヘルプ

Status  
ステータス

About  
会社概要

Careers  
キャリア

Press  
プレス

Blog  
ブログ

Privacy  
プライバシー

Terms  
利用規約

Text to speech  
テキスト読み上げ

Teams  
チーム
