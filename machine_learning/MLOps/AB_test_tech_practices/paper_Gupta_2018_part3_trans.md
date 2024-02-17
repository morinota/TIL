# 8. Computation of Experiment Analysis and Metrics 8. 実験分析と測定基準の計算

## 8.1. Problem # 8.1.Problem

When 100s of experiments are running simultaneously on millions of users each, having an automated, reliable and efficient way to compute metrics for these experiments at scale is crucial to create a culture where OCEs are the norm.
数百万人のユーザーに対して100以上の実験が同時に実行される場合、OCEが規範となる文化を創造するためには、これらの実験のためのメトリクスをスケールに応じて計算する自動化された信頼性の高い効率的な方法を持つことが極めて重要である。
The system to compute experiment results can be viewed as a pipeline.
実験結果を計算するシステムは、パイプラインとみなすことができる。
It starts with the product collecting telemetry data points instrumented to measure user response, like clicks on a particular part of the product.
それは、製品の特定の部分をクリックするなど、ユーザーの反応を測定するために計測されたテレメトリーデータポイントを製品が収集することから始まる。
The product uploads telemetry to a cloud store.
この製品はテレメトリーをクラウドストアにアップロードする。
This telemetry is seldom used in raw form for any analysis.
このテレメトリが生のまま分析に使われることはめったにない。
Further data processing, commonly called cooking, joins this data with other data logs, like experiment assignment logs, and organizes it in a set of logs in standard format, called a cooked log.
一般にクッキングと呼ばれる、さらなるデータ処理は、このデータを実験割り当てログのような他のデータログと結合し、クックドログと呼ばれる標準フォーマットのログの集合に整理する。
Most reporting and experiment analysis occur on top of the cooked log.
レポートや実験分析のほとんどは、調理されたログの上で行われる。
For running experiments at scale, it is important to have a system for defining metrics of interest on top of these logs and actually computing metrics for each experiment running over millions of users.
スケールの大きな実験を行うには、これらのログの上に関心のあるメトリクスを定義し、何百万人ものユーザーを対象とした各実験のメトリクスを実際に計算するシステムを持つことが重要です。
In addition, the system must support further ad hoc analysis of experiments so that data scientists can try different metrics and methods to find better ways of analyzing results.
さらに、データサイエンティストがさまざまな測定基準や方法を試して、結果を分析するためのより良い方法を見つけることができるように、システムは実験のアドホック分析をさらにサポートしなければならない。
There are a few key properties of a good system that help in running experiments at scale.
優れたシステムには、大規模な実験に役立ついくつかの重要な特性がある。
Each part of the system must be efficient and fast to scale to 100s of experiments over millions of users each.
システムの各部分は、それぞれ数百万人のユーザーを対象とした100回以上の実験にスケールアップするために、効率的で高速でなければならない。
It must be decentralized so that many people in the organization can configure and use the system to fulfill their needs.
組織内の多くの人が、それぞれのニーズを満たすためにシステムを構成し、使用できるように、分散化されていなければならない。
It must also have some level of quality control to ensure that the results are trustworthy.
また、結果が信頼に足るものであることを保証するために、ある程度の品質管理も行わなければならない。
Finally, it must be flexible enough to support the diverse needs of feature teams who are constantly working on adding new features and new telemetry, and data scientists working on new metrics and methodologies to extract insights from these experiments.
最後に、常に新機能や新テレメトリーの追加に取り組むフィーチャー・チームや、これらの実験から洞察を引き出すための新しいメトリクスや方法論に取り組むデータ・サイエンティストの多様なニーズをサポートするのに十分な柔軟性がなければならない。
This system forms the core of experimentation analysis for any product.
このシステムは、あらゆる製品の実験分析の中核をなす。
If done well, it empowers feature teams to run 100s of experiments smoothly and get trustworthy insights in an automated and timely manner.
うまくいけば、フィーチャー・チームが100以上の実験をスムーズに実行し、自動化されたタイムリーな方法で信頼できるインサイトを得ることができるようになる。
It helps them understand if the treatment succeeded or failed in moving the key OEC metric and gives insight into why it happened.
これは、治療がOECの主要な指標を動かすことに成功したのか失敗したのかを理解するのに役立ち、なぜそうなったのかについての洞察を与えてくれる。
These insights are crucial in taking next steps on an experiment: investigating a failure or investing further in successful areas.
これらの洞察は、実験の次のステップを踏む上で極めて重要である： 失敗を調査するか、成功した分野にさらに投資するか。
Conversely, if this system does not have the desired properties mentioned above, it often becomes a bottleneck for scaling experimentation operations and getting value from experiments.
逆に、このシステムが上記のような望ましい特性を備えていない場合、実験業務を拡大し、実験から価値を得るためのボトルネックになることが多い。

## 8.2. Common Solutions and Challenges 

### 8.2.1. Data Management and Schema 8.2.1. データ管理とスキーマ

The structure and schema of cooked logs affect how data is processed in downstream data pipelines, such as metric definitions and experiment analysis.
調理されたログの構造とスキーマは、メトリックの定義や実験分析など、下流のデータパイプラインでデータがどのように処理されるかに影響する。
There is a clear tradeoff between reliability and flexibility.
信頼性と柔軟性の間には明確なトレードオフがある。
If the rules and constraints are strict, the data will be reliable and can be consumed consistently across different use cases.
ルールと制約が厳密であれば、データは信頼性が高く、異なるユースケースでも一貫して利用できる。
At the same time, having too strict constraints can slow down the implementation of the logging, and thus decelerate experimentation and product development.
同時に、制約が厳しすぎると、ロギングの実施に時間がかかり、実験や製品開発のスピードが落ちてしまう。
Different companies have different ways of solving this issue.
企業によって、この問題を解決する方法は異なる。
At Netflix, there is a single cooked log where each row is a JSON array containing all data collected.
Netflixでは、各行が収集されたすべてのデータを含むJSON配列である単一の調理されたログがあります。
JSON structure allows flexibility and extensibility.
JSON構造は、柔軟性と拡張性を可能にする。
There is a risk that the log may keep quickly changing.
ログがどんどん変わっていく危険性がある。
This must be managed by development practices to ensure that key telemetry is not lost due to a code change.
これは、コード変更によって重要な遠隔測定が失われないように、開発プラクティスによって管理されなければならない。
A similar approach is used by MSN and Bing at Microsoft.
同様のアプローチは、マイクロソフトのMSNやBingでも使われている。
The bring-your-own-data approach is followed at LinkedIn, Airbnb, and Facebook.
LinkedIn、Airbnb、Facebookでは、データ持ち込み方式が採用されている。
Each product team is responsible for creating data streams and metrics for each experiment unit every day.
各製品チームは毎日、各実験ユニットのデータストリームとメトリクスの作成に責任を負う。
These streams follow certain guidelines that enable any experiment to use these streams to compute metrics for that experiment.
これらのストリームは、どの実験でもこれらのストリームを使用してその実験のメトリックスを計算できるように、一定のガイドラインに従っている。
Products, like Microsoft Office, have an event-view schema, where each event is on a separate row.
マイクロソフト・オフィスのような製品は、イベント・ビュー・スキーマを持ち、各イベントは別々の行にある。
This format is also extensible with a more structured schema.
このフォーマットは、より構造化されたスキーマで拡張することもできる。
Another approach followed by some products is to have a fixed-set of key columns required to compute key metrics, and a propertybag column that contains all other information.
一部の製品で採用されているもう1つのアプローチは、主要な測定基準を計算するために必要な固定されたキー列のセットと、その他のすべての情報を含むプロパティバッグ列を持つことである。
This allows stability for key columns and flexibility to add new telemetry to the log.
これにより、主要カラムの安定性と、ログに新しいテレメトリを追加する柔軟性が得られる。

### 8.2.2. Timely and Trustworthy Experiment Analysis 8.2.2. タイムリーで信頼できる実験分析

Many companies track hundreds of metrics in experiments to understand the impact of a new feature across multiple business units, and new metrics are added all the time.
多くの企業は、複数の事業部門にまたがる新機能の影響を理解するために、実験で何百ものメトリクスを追跡しており、常に新しいメトリクスが追加されている。
Computing metrics and providing analysis of an experiment on time is a big challenge for experimentation platforms.
メトリックスを計算し、実験の分析を時間通りに行うことは、実験プラットフォームにとって大きな課題である。
As previously mentioned, in many companies, like LinkedIn, Facebook and Airbnb, the metrics framework and experimentation platform are separate, so that each product team or business unit own their metrics and is responsible for them.
前述したように、LinkedIn、Facebook、Airbnbのような多くの企業では、メトリクスのフレームワークと実験プラットフォームは分離されており、各プロダクトチームやビジネスユニットがそれぞれのメトリクスを所有し、それらに責任を持つようになっている。
The experimentation platform is only responsible for the computation of metrics for experiment analysis.
実験プラットフォームは、実験分析のためのメトリクスの計算のみを担当する。
In other companies, like Microsoft, Google, Booking.com and Lyft, the metric computation is usually done by the experimentation team right from telemetry or cooked logs.
マイクロソフト、グーグル、Booking.com、Lyftのような他の企業では、指標計算は通常、テレメトリーや調理されたログから実験チームによって行われる。
Individual metrics and segments can have data quality issues, delays or be computationally expensive.
個々のメトリクスやセグメントには、データ品質に問題があったり、遅延があったり、計算コストが高かったりすることがある。
To resolve these issues, companies segment metrics in various ways.
こうした問題を解決するために、企業はさまざまな方法で指標をセグメント化している。
Having ‘tiers’ or metrics so that high-tier metrics are prioritized and thoroughly tested is a way to consume reliable experiment results.
高位のメトリクスが優先され、徹底的にテストされるように、「階層」またはメトリクスを持つことは、信頼できる実験結果を消費する方法である。
Also, if not all metrics have to be pre-computed, experimentation platforms can offer an on-demand calculation of the metrics to save computation resources.
また、すべてのメトリクスを事前に計算する必要がない場合、実験プラットフォームは、計算リソースを節約するために、メトリクスのオンデマンド計算を提供することができる。
Telemetry data from apps may have large delay getting uploaded from a section of devices.
アプリからの遠隔測定データは、デバイスの一部からアップロードされる際に大きな遅延が発生する可能性があります。
It is important to incorporate this latearriving data in experiment analysis to avoid selection bias.
選択バイアスを避けるためには、このような後発のデータを実験分析に組み込むことが重要である。
Some companies like Facebook leave a placeholder for these metric values and fill it in once enough data arrives.
フェイスブックのように、これらの指標値のプレースホルダーを残しておき、十分なデータが届いてから記入する企業もある。
In other companies, like LinkedIn and Microsoft, these metric values are computed with the data received at the time and then recomputed later to update the results.
リンクトインやマイクロソフトのような他の企業では、これらの指標値はその時点で受け取ったデータで計算され、後で結果を更新するために再計算される。
Usually there is a definite waiting period after which the metric value is no longer updated.
通常、明確な待機期間があり、それを過ぎるとメトリック値は更新されなくなる。
A few companies put additional steps to ensure that metrics are good quality.
いくつかの企業は、メトリクスの品質を保証するための追加措置を講じている。
Some companies like LinkedIn have a committee to approve adding new metrics or modifying existing metrics to ensure metric quality.
LinkedInのように、メトリクスの質を保証するために、新しいメトリクスの追加や既存のメトリクスの変更を承認する委員会を設けている企業もある。
At a few companies, the metrics must be tested to ensure that they are sensitive enough to detect a meaningful difference between treatment groups.
いくつかの企業では、治療群間の有意差を検出するのに十分な感度を確保するために、測定基準をテストしなければならない。
To save computational resources, the experimentation platform can require a minimum statistical power on the metrics or place metrics in specific formats.
計算資源を節約するために、実験プラットフォームはメトリクスに最小限の統計的検出力を要求したり、メトリクスを特定のフォーマットで配置したりすることができる。
Booking.com has an automated process to detect data and metric quality issues which includes having two separate data and metric computation pipelines and process to compare the final results from both [41].
Booking.comは、データとメトリックの品質の問題を検出するための自動化されたプロセスを持っている。これには、2つの別々のデータとメトリック計算パイプラインを持ち、両方の最終結果を比較するプロセスが含まれる[41]。

### 8.2.3. Metric ownership 8.2.3. メートル法の所有権

Metrics often have an implicit or explicit owner who cares about the impact on that metric.
メトリクスには、そのメトリクスへの影響を気にする暗黙的または明示的な所有者がいることが多い。
In a large organization running 100s of experiments every day, scalable solutions ensure that these metric owners know about the experiments that move their metric, and that experiment owners know who to talk with when a particular metric moves.
毎日100以上の実験を実行している大規模な組織では、スケーラブルなソリューションによって、これらのメトリック所有者がメトリックを動かす実験について知っていること、そして特定のメトリックが動いたときに実験所有者が誰と話すべきかを知っていることが保証される。
In many cases, it is easy to view the results of any experiment, and metric owners look for experiments that impact their metrics.
多くの場合、どのような実験の結果も簡単に見ることができ、メトリクスの所有者は自分のメトリクスの影響を与える実験を探す。
Team organization structure also helps in this case.
チーム編成もこの場合に役立つ。
If there is a special performance team in the organization, it becomes clear to experiment owners to talk with that team when performance metrics start degrading.
組織内に特別なパフォーマンス・チームがあれば、パフォーマンス指標が低下し始めたときに、実験オーナーがそのチームと話し合うことが明確になる。
Some companies like Microsoft built automated systems for informing both experiment owners and metric owners when large movements are seen in a particular metric.
マイクロソフトのように、特定のメトリクスに大きな動きが見られたときに、実験オーナーとメトリクスオーナーの両方に通知する自動化システムを構築した企業もある。
Some teams, like performance teams, may have additional tools to search through multiple experiments to find ones that impact their metrics.
パフォーマンス・チームのように、自分たちの測定基準に影響を与えるものを見つけるために、複数の実験を検索するための追加ツールを持っているチームもあるだろう。

### 8.2.4. Supporting Exploratory and Advanced Experiment Analysis Pipelines 8.2.4. 探索的で高度な実験分析パイプラインのサポート

Very often, an experiment requires additional ad hoc analysis that cannot be supported by the regular computation pipeline.
実験では、通常の計算パイプラインでは対応できないアドホックな解析が必要になることが非常に多い。
It is important that data scientists can easily conduct ad hoc analysis for experiments.
データサイエンティストは、実験のためのアドホック分析を簡単に行えることが重要である。
Some ad hoc analyses may quickly find application in many more experiments.
いくつかのアドホックな分析は、すぐに多くの実験に応用できるだろう。
It is a challenge for experimentation platforms to keep up with supporting new ways of analyzing experiments while maintaining reliability and trustworthiness.
実験プラットフォームにとって、信頼性と信用性を維持しながら、新しい実験分析方法をサポートし続けることは挑戦である。
While there was no common solution to solving this problem across different companies, there are some common considerations for supporting a new analysis method: • Is the new analysis method reliable and generalizable for all metrics and experiments? • Is the benefit from the new method worth the additional complexity and computation? • Which result should we rely on if the results of the experiment are different between various methods? • How can we share the guideline so that the results are interpreted correctly?
異なる企業間でこの問題を解決するための共通の解決策はなかったが、新しい分析手法をサポートするための共通の考慮事項がいくつかある： - 新しい分析手法は、すべての測定基準や実験に対して信頼でき、一般化可能か？- 新しい分析手法は信頼でき、すべての測定基準や実験に対して一般化できるか？- 実験結果が様々な手法で異なる場合、どの結果を信頼すべきか？- 結果を正しく解釈するために、どのようにガイドラインを共有すればよいか？

# 9. Dealinig with Client Bloat 9. クライアントの肥大化に対処する

## 9.1. Problem # 9.1.Problem

Many experiments are run on client software (e.g., desktop and mobile).
多くの実験は、クライアントソフトウェア（デスクトップやモバイルなど）で実行される。
In these experiments, a new feature is coded behind a flag switched off by default.
これらの実験では、新機能はデフォルトでオフになるフラグの後ろにコード化される。
During an experiment, the client downloads a configuration, that may turn the feature flag on for that device.
実験中、クライアントはコンフィギュレーションをダウンロードし、そのデバイスの機能フラグをオンにすることができる。
As more and more experiments are run over time, the configuration files that need to be sent keep growing larger and increase client bloat.
時間をかけてより多くの実験が実行されるにつれて、送信する必要のある設定ファイルはどんどん大きくなり、クライアントの肥大化を招く。
This eventually starts to affect the performance of the client.
これはやがてクライアントのパフォーマンスに影響を及ぼし始める。

## 9.2. Common Solutions # 9.2.Common Solutions

While it may seem that if feature F is successful it will need the flag set to ON forever, that’s not the case if the experimentation system is aware of versions and which versions expect a setting for F.
機能Fが成功すれば、永遠にフラグをオンに設定する必要があるように見えるかもしれないが、実験システムがバージョンを認識し、どのバージョンがFの設定を期待しているかを認識していれば、そうではない。
A key observation is that at some point when feature F is successful, it is integrated into the codebase, and from that point on, the configuration of F is NOT needed.
重要な観測点は、ある時点で機能Fが成功すると、それはコードベースに統合され、その時点からFのコンフィギュレーションは不要になるということだ。
Here is a description of this scenario: V10.1: Feature F is in code but not finished.
以下は、このシナリオの説明である： V10.1: V10.1：機能Fはコードに入っているが、まだ完成していない。
- Default (in code) = Off.
- デフォルト（コード内）＝オフ。
- Config: No F V10.2 (experiment): Feature F is done.
- コンフィグ Fなし V10.2（実験）： フィーチャーFは終了しました。
- Default (in code) = Off - Config: F is on/off at 50/50 If the idea fails, stop sending config for F.
- デフォルト（コード内） = オフ - コンフィグ： Fは50/50でオン/オフ アイデアが失敗したら、Fのコンフィグ送信を停止する。
If the idea succeeds, Config: F=On.
アイデアが成功すれば、コンフィグ： F=Onとなる。
The key observation is that the config system must send F=On for every release that needs F as config by default, 10.2 and higher V10.3 – Other features are evaluated.
コンフィグシステムは、デフォルトでコンフィグとしてFを必要とするすべてのリリース、10.2以上、V10.3 - その他の機能を評価するために、F=Onを送信しなければならないということが重要な観察点です。
- Config: F=On, G=On… V10.4 – Code is cleaned.
- コンフィグ： F=On, G=On... V10.4 - コードをクリーンアップ。
- F=On in code.
- コードではF=オン。
No need for F in config Config system should stop sending F for V10.4 and higher.
V10.4以降では、コンフィグシステムはFを送信しないようにする。
Every feature then has [Min version] and after cleanup [Min Version, Max version].
そして、すべての機能には[最小バージョン]があり、クリーンアップ後に[最小バージョン、最大バージョン]がある。
If we assume every release has 100 new features driven by config and 1/3 of these features are successful, the number of configuration features on the server grows at 100/3 ~ 33 per release, but only successful features should be maintained.
リリースごとに100の新機能がコンフィグによって駆動され、そのうちの1/3が成功したと仮定すると、サーバー上のコンフィグ機能の数はリリースごとに100/3 ~ 33で増加するが、成功した機能だけが維持されるべきである。
The number of features sent to the client is bounded by those that must be experimented and those not cleaned.
クライアントに送信されるフィーチャーの数は、実験が必要なものとクリーニングされないものによって制限される。
Assuming three releases are needed to experiment and clean, there are 100 features in config for experiments and 100 (33 \* 3 releases) maintained waiting for cleanup.
実験とクリーンアップに3つのリリースが必要だとすると、実験用のconfigには100の機能があり、クリーンアップ待ちのconfigには100(33㌽* 3リリース)の機能が維持されていることになる。
This means that the total configurations are about 200, and that does not grow.
つまり、全コンフィギュレーションは約200であり、これが増えることはない。

# 10. Network Interactions 10. ネットワークの相互作用

## 10.1. Problem # 10.1.Problem

Network interactions are a significant concern in A/B testing.
ネットワークの相互作用は、A/Bテストにおいて重要な問題である。
Traditional A/B test assume a stable user treatment value (SUTVA) to accurately analyze the treatment effect.
従来のA/Bテストは、治療効果を正確に分析するために、安定したユーザー治療値（SUTVA）を前提としている。
SUTVA implies that the response of an experiment unit (user) is independent of the response of another experiment unit under treatment [73].
SUTVAは、ある実験単位（利用者）の反応が、治療を受けている別の実験単位の反応から独立していることを意味する[73]。
A network interaction can occur when a user’s behavior is influenced by another user’s, so that users in the control group are influenced by actions taken by members in the treatment group.
ネットワーク相互作用は、あるユーザーの行動が他のユーザーの行動に影響されるときに起こる。
As a result, the control group is only a control group in name and no longer reflect outcomes that would be observed if the treatment did not exist.
その結果、対照群は名ばかりの対照群であり、もはや治療が存在しなかった場合に観察されるであろう結果を反映していない。
If you ignore network interactions, you get a biased estimate of the treatment effect.
ネットワーク相互作用を無視すると、治療効果の推定値に偏りが生じる。

## 10.2. Common Solutions and Challenges 

These network interactions are an inherent outcome of the products and scenarios where changes are being tested.
このようなネットワークの相互作用は、変更がテストされる製品やシナリオに固有の結果である。
There does not seem to be one single method that can mitigate the impact of network interactions on the accuracy of the estimated treatment effect.
治療効果の推定精度に対するネットワーク相互作用の影響を緩和できる唯一の方法はないようである。
Here are some common cases and the methods to deal with them.
よくあるケースとその対処法を紹介しよう。

### 10.2.1. Producer and Consumer Model 10.2.1. 生産者と消費者のモデル

At LinkedIn, there is a meaningful producer/consumer distinction between user roles for a feature.
LinkedInでは、ある機能に対するユーザーの役割には、生産者と消費者という意味のある区別がある。
For instance, there are producers and consumers of the hashtags feature for the main feed on LinkedIn.
例えば、LinkedInのメインフィードのハッシュタグ機能の生産者と消費者がいる。
In these cases, LinkedIn typically uses two-sided randomization.
このような場合、リンクトインは通常、両側無作為化を用いる。
Two orthogonal experiments are run together: one controlling the production experience and one controlling the consumption experience.
2つの直交実験が一緒に実行される： ひとつは生産経験をコントロールする実験、もうひとつは消費経験をコントロールする実験である。
For the hashtags example, this implies that the production experiment allows users in treatment to add hashtags to their posts, and the consumption experiment allows users in treatment to see hashtags on their feed.
ハッシュタグの例でいえば、生産実験では処理対象のユーザーが自分の投稿にハッシュタグをつけることができ、消費実験では処理対象のユーザーがフィード上でハッシュタグを見ることができる。
The production experience starts at a low ramp percentage with consumption one at a high percentage, and then gradually ramping the production experience.
生産経験は低いランプ率から始まり、消費は高い割合で行われ、その後徐々に生産経験を増やしていく。
If we do a simple A/B test lumping both features together, then things go wrong: The producer effect is underestimated because there are too few potential consumers.
単純なA/Bテストで両方の機能を一緒にすると、うまくいかない： 潜在的な消費者が少なすぎるため、プロデューサー効果は過小評価される。
For our example, if a user in treatment in the production experiment can post hashtags but not everybody can see them, then the user is likely to engage less with the platform.
この例でいえば、本番実験において、あるユーザーがハッシュタグを投稿できるにもかかわらず、そのハッシュタグを誰もが見ることができない場合、そのユーザーはプラットフォームとの関わりが薄くなる可能性が高い。
The consumer effect is underestimated because there are too few potential producers.
潜在的な生産者が少なすぎるため、消費者効果は過小評価されている。
Being able to see hashtags may make users more engaged, but not if too few people (i.e.only treated members) use them.
ハッシュタグを見ることができるようになれば、ユーザーのエンゲージメントは高まるかもしれないが、ハッシュタグを使う人が少なすぎる（つまり、扱われたメンバーだけ）のであれば、そうはならない。
Using two sided randomization helps: when 95% of consumers can see the produced content, then the effect of producers (say at 50% ramp) is more accurate; when 95% of producers are “enabled,” then the consumer test (say 50% ramp) is more accurate.
両側無作為化を使用することは有効である： 消費者の95％が生産されたコンテンツを見ることができる場合、生産者の効果（例えば50％ランプ）はより正確である。生産者の95％が「有効」である場合、消費者テスト（例えば50％ランプ）はより正確である。
This method may not account for competition effects between producers, in which case we typically use a 95% ramp over 50% ramp if enough power is available.
この方法は、生産者間の競争効果を考慮していない可能性があり、その場合、十分な電力が利用可能であれば、通常、50％ランプよりも95％ランプを使用する。
Further, it may not be possible to disentangle consumption from production in a feature.
さらに、消費と生産を切り離すことができない場合もある。
For instance, if a user mentions another user using ‘@ mention’ feature, then the consumer of the feature must be notified about being mentioned.
例えば、あるユーザーが「@ mention」機能を使って他のユーザーについて言及した場合、言及されたことをその機能の利用者に通知しなければならない。

### 10.2.2. Known Influence Network Model 10.2.2. 既知の影響力ネットワーク・モデル

In many products at LinkedIn and Facebook, the network over which users can influence each other is known.
リンクトインやフェイスブックの多くの製品では、ユーザー同士が影響し合えるネットワークが知られている。
This information is helpful for designing better controlled experiments.
この情報は、より良い対照実験を計画するのに役立つ。
LinkedIn typically uses its egoClusters method, creating about 200,000 ego-networks, comprised of an “ego” (the individual whose metrics are measured) and “alters,” who receive treatments but whose metrics are not of interest.
LinkedInは通常、egoClustersメソッドを使用し、"ego"（測定基準が測定される個人）と "alters"（治療を受けるが、その測定基準には関心がない）で構成される約20万のegoネットワークを作成する。
Clusters are designed to have egos representative of LinkedIn users and their networks, and treatment is allocated as follows: in all clusters, egos are treated.
クラスターは、リンクトインのユーザーとそのネットワークを代表するエゴを持つように設計され、扱いは次のように割り当てられる： すべてのクラスターで、エゴは扱われます。
In “treated” clusters, all alters are treated.
扱われる」クラスターでは、すべてのオルターが扱われる。
In control clusters, all alters remain in control.
コントロールクラスターでは、すべてのオルターがコントロールを維持する。
A simple two-sample t-test between egos of treated clusters and egos of control clusters gives the approximate first-order effect of having all their connections treated versus none.
処理されたクラスターのエゴと、対照クラスターのエゴとの単純な2標本のt検定により、すべてのコネクションが処理された場合とされなかった場合の、おおよその一次効果がわかる。
Facebook and Google employ similar cluster based randomization techniques [20, 26].
フェイスブックとグーグルは、同様のクラスターベースのランダム化技術を採用している[20, 26]。
These designs are the subject of recent academic papers [9].
これらの設計は、最近の学術論文の主題となっている[9]。

### 10.2.3. One-to-One Communication 10.2.3. 一対一のコミュニケーション

When the feature being tested is one-to-one communication, LinkedIn typically uses model-based approaches when analyzing one-to-one messaging experiments, counting messages explicitly according to four categories: those that stay within the treatment group, those that stay within the control group, and those that cross (one way or the other).
テストされる機能が1対1のコミュニケーションである場合、リンクトインは通常、1対1のメッセージング実験を分析するときにモデルベースのアプローチを使用し、4つのカテゴリに従って明示的にメッセージをカウントします： トリートメント・グループ内に留まるもの、コントロール・グループ内に留まるもの、（一方的に）交差するもの。
The total number of messages of these categories are contrasted with the help of a model and permutation testing to measure the impact of network interactions.
これらのカテゴリーのメッセージ総数は、ネットワーク相互作用の影響を測定するために、モデルと並べ替え検定の助けを借りて対比される。
At Skype, some experiments related to call quality are randomized at the call level, where each call has an equal probability of being treatment or control.
Skypeでは、通話品質に関連するいくつかの実験は、呼レベルでランダム化 されており、各呼が処理または対照になる確率は等しい。
Note that a single user may make multiple calls during the experiment.
1人のユーザーが実験中に複数の通話をする可能性があることに注意。
This approach does not account for within-user effect from a treatment but tends to have much greater statistical power for detecting the treatment effect on the call metrics.
このアプローチでは、治療によるユーザー内効果は考慮されないが、通話メトリクスに対する治療効果を検出するための統計的検出力ははるかに高くなる傾向がある。

### 10.2.4. Market Effects 10.2.4. 市場効果

In a two-sided marketplace, different users’ behavior is correlated with each other due to a demand-and-supply curve.
両側市場においては、需給曲線によって異なるユーザーの行動は互いに相関する。
If we look at a ride service, when a driver is matched to a passenger, it lowers the probability that other drivers in vicinity are matched.
ライドサービスに目を向けると、ドライバーが乗客とマッチングすると、近くにいる他のドライバーがマッチングする確率が低くなる。
Simple randomization of passengers or drivers into Treatment and Control groups causes changes in market conditions, therefore biases the estimated Treatment effect.
乗客や運転手を単純に治療群と対照群に無作為に振り分けると、市場の状況が変化するため、治療効果の推定値に偏りが生じる。
To reduce the network interactions between users, Lyft conducts cluster sampling by randomizing across spatial regions or time intervals of varying size, ensuring similarity in market conditions between variants.
利用者間のネットワーク相互作用を軽減するために、Lyftは、空間的地域または様々な大きさの時間間隔にわたって無作為化することによってクラスター・サンプリングを実施し、変種間の市場状況の類似性を確保している。
The coarser the experimental units are, the less interference bias persists, although it comes with the cost of increased variance in the estimate [29].
実験単位が粗ければ粗いほど、干渉バイアスは少なくなるが、その代償として推定値の分散が大きくなる[29]。
Uber has tried introducing the treatment to a random set of markets and have a synthetic control to predict the counterfactual [1, 34].
ウーバーは、ランダムな市場セットに治療を導入し、反事実を予測するための合成コントロールを持っている[1, 34]。
Similar market effects also affect online ads.
同様の市場効果はオンライン広告にも影響する。
In this hypothetical example, assume that all budget for a set of advertisers is being spent.
この仮定の例では、一組の広告主の予算がすべて使われていると仮定する。
For the experiment, the treatment increases ad load from these advertisers therefore increasing ad consumption.
実験では、治療によってこれらの広告主からの広告負荷が増加し、広告消費が増加する。
In this experiment, you would observe that revenue in the treatment group goes up.
この実験では、治療グループの収益が上がることが観察されるだろう。
But the treatment group is stealing budget from the control group, and there will be no increase in revenue when the treatment ships to all users.
しかし、治療グループは対照グループから予算を盗んでおり、治療が全ユーザーに行き渡ったところで収入は増えない。
One way to prevent budget stealing is to split the ad budget of all ad providers in proportion to the percentage of user traffic exposed to the treatment and control groups.
予算泥棒を防止する一つの方法は、すべての広告プロバイダーの広告予算を、トリートメントグループとコントロールグループに露出するユーザートラフィックの割合に比例して分割することである。
While this addresses the problem of budget stealing, it does not help us understand if the treatment will cause an increase in revenue.
これは予算泥棒の問題に対処するものではあるが、治療が増収をもたらすかどうかを理解する助けにはならない。
Higher use of budgets not being entirely spent or an increase in budget from advertisers spending their entire budget may be a better indicator of increase in revenue.
予算がすべて使われなかったり、広告主が予算をすべて使ったために予算が増えたりした場合の利用率が高いほうが、収益増加の指標になるかもしれない。

### 10.2.5. Multiple Identities for the Same Person 10.2.5. 同一人物の複数のアイデンティティ

Similar statistical issues arise when the same user has several accounts or cookies.
同じユーザーが複数のアカウントやクッキーを持つ場合、同様の統計的問題が発生する。
Instead of spillover occurring from one user to another, it may occur from one account to another, within the same user.
スピルオーバーは、あるユーザーから別のユーザーへ起こるのではなく、同じユーザー内で、あるアカウントから別のアカウントへ起こる可能性がある。
A natural level of randomization is user.
自然なレベルの無作為化はユーザーである。
However, this requires knowing which accounts belong to the same user.
しかし、そのためには、どのアカウントが同じユーザーに属しているかを知る必要がある。
If this is unknown or imperfectly known, randomization at the account-level may be the only alternative.
これが不明、あるいは不完全な場合は、口座レベルでの無作為化が唯一の選択肢となる。
Account-level randomization generally tends to suffer from attenuation bias.
アカウントレベルの無作為化は一般に減衰バイアスに悩まされる傾向がある。
Studies in Facebook have indicated that cookie level randomization can underestimate person level effects by a factor of 2 or 3 [15].
フェイスブックでの研究によると、クッキー・レベルの無作為化は、個人レベ ルの効果を2～3倍過小評価する可能性があることが示されている [15]。
Attenuation bias is also one of the main pitfalls in running long-term experiments because the chances of within-user spillover increases with time [23].
減衰バイアスは、長期的な実験を行う際の主な落とし穴の一つでもある。

# 11. Interactions between Multiple Experiments 11. 複数の実験間の相互作用

## 11.1. Problem # 11.1.Problem

If there are non-independent treatment effects in two experiments, then those experiments are said to be interacting: 𝐴𝑇𝐸(𝑇1 ) + 𝐴𝑇𝐸(𝑇2 ) ≠ 𝐴𝑇𝐸(𝑇1𝑇2) A textbook example of interaction between two experiments is where the treatment in the first experiment changes the foreground color to blue and the treatment in the second experiment changes the background color to blue.
2つの実験に独立でない治療効果がある場合、それらの実験は相互作用していると言われる： 𝐴 + 𝑇𝐸(𝐴) ≠ 𝑇𝐸(𝐴𝑇) ≠ 𝑇𝐸(𝐴𝑇) 2つの実験間の相互作用の教科書的な例は、1つ目の実験の治療が前景色を青に変え、2つ目の実験の治療が背景色を青に変える場合である。最初の実験の処置は前景色を青に変え、2番目の実験の処置は背景色を青に変える。
In this example let us assume that there are positives for each experiment in isolation, but the impact of both treatments is catastrophic.
この例では、各実験単独ではプラスだが、両治療の影響は壊滅的であると仮定する。
A user who experiences both treatments at the same time sees a blue screen.
両方の治療を同時に受けたユーザーはブルースクリーンを見る。
In products where 100s of experiments run concurrently this can be a serious issue.
何百もの実験が同時に行われる製品では、これは深刻な問題になりうる。
Ideally you want to prevent contamination where the treatment effect measured in one experiment may become biased because that experiment interacts with another experiment.
理想的には、ある実験で測定された治療効果が、その実験と別の実験との相互作用によって偏りが生じるようなコンタミネーションを防ぎたい。
At the same time, you need to make a joint ship decision for interacting experiments.
同時に、相互作用する実験のための共同船の決定を下す必要がある。
As in the case of the text book example above, individually both treatments are good ship candidates but jointly you can only ship one.
上の教科書の例のように、どちらの治療法も個々には良い船候補だが、共同では1つしか出荷できない。

## 11.2. Common Solutions and Challenges 

From our experience, it is rare that two interacting experiments cause enough contamination that it changes the ship decision.
私たちの経験では、2つの実験が相互作用して、船の決定を変えるほどの汚染を引き起こすことはまれである。
Most products are well architected and small teams work independently of most other teams working on different areas of the product.
ほとんどの製品はうまく設計されており、小さなチームは製品のさまざまな分野で働く他のほとんどのチームから独立して働いている。
The chances of interaction between two experiments are highest when both experiments are being run by the same sub team who are changing the same part of the product.
2つの実験が相互作用する可能性が最も高いのは、製品の同じ部分を変更する同じサブチームによって両方の実験が実行されている場合である。
To prevent interaction between these types of experiments, the Microsoft and Google experimentation platforms have the concept of numberlines or layers [46, 68].
これらのタイプの実験間の相互作用を防ぐために、マイクロソフトとグーグルの実験プラットフォームには、ナンバーラインやレイヤーという概念がある[46, 68]。
Experiments that run on the same numberline or layer are guaranteed to get an exclusive random sample of the user population, so no user is exposed to two experiments being run concurrently in the same layer or numberline.
同じ数列またはレイヤー上で実行される実験は、ユーザー母集団の排他的ランダムサンプルを得ることが保証されているため、ユーザーは同じレイヤーまたは数列で同時に実行されている2つの実験にさらされることはありません。
This limits the number of users who can be part of an experiment.
このため、実験に参加できるユーザー数が制限される。
If the first experiment is exposed to half of all users, then the second experiment cannot be exposed to more than remaining half of the user base.
最初の実験が全ユーザーの半分に公開された場合、2番目の実験は残りの半分以上のユーザーには公開できない。
Small teams manage a group of numberlines or layers.
小チームが数列またはレイヤーのグループを管理する。
Based on their understanding of the treatments in different experiments, the teams can decide whether to run the experiments in the same numberline/layer.
異なる実験における処置についての理解に基づいて、チームは同じ数列／層で実験を行うかどうかを決定することができる。
To detect interactions between two experiments running in two different layers, Microsoft runs a daily job that tests each pair of experiments for additivity of their treatment effects: 𝜇(𝑇1𝐶2 ) − 𝜇(𝐶1𝐶2 ) ≠ 𝜇(𝑇1𝑇2 ) − 𝜇(𝐶1𝑇2 ).
2つの異なるレイヤーで実行されている2つの実験間の相互作用を検出するために、マイクロソフトは、各ペアの実験が治療効果の加法性をテストするジョブを毎日実行する： 𝜇(𝑇) - 𝐶2 ) - 𝜇(𝑇) ≠ 𝐶(𝐶2 ) - 𝜇(𝐶1𝑇2 ).
It is rare to detect interactions between two experiments as experiment owners already try to isolate experiments that may conflict by running them on the same numberline or layer.
実験オーナーはすでに、同じ番号線やレイヤー上で実験を実行することによって、衝突する可能性のある実験を分離しようとしているので、2つの実験間の相互作用を検出することはまれである。
To address the problem of joint decision making, you can run both experiments on different numberlines or layers—if we know that the combination of two experiments cannot lead to a catastrophic result.
共同決定の問題に対処するには、2つの実験の組み合わせが破滅的な結果を招かないことがわかっていれば、両方の実験を異なる数列またはレイヤーで実行すればよい。
In this case, you can analyze the factorial combination of both experiments to understand the effect of treatment from each experiment individually and the effect of treatments from both experiments.
この場合、両実験の要因結合を分析することで、各実験の処置の効果を個別に理解し、両実験の処置の効果を理解することができる。

# 12. Conclusion 12. 結論

This is the first paper that brings together the top practical challenges in running OCEs at scale from thirty-four experts in thirteen different organizations with experience in testing more than one hundred thousand treatments last year alone.
これは、昨年だけで10万件以上の治療をテストした経験を持つ、13の異なる組織の34人の専門家が、OCEを大規模に実行する上での実践的な最重要課題をまとめた初めての論文である。
These challenges broadly fall into four categories: analysis of experiments, culture and engineering, deviations from traditional A/B tests, and data quality.
これらの課題は、大きく4つのカテゴリーに分類される： 実験の分析、文化とエンジニアリング、伝統的なA/Bテストからの逸脱、そしてデータの質である。
In Sections 3-5, we discussed the problem that while most experiments run for a short period of time, we want to estimate the long term impact of a treatment and define an overall evaluation criteria (OEC) to make ship decisions for all experiments in a consistent and objective manner while taking into account the heterogenous treatment effects across different product and user segments.
セクション3-5では、ほとんどの実験が短期間実施される一方で、治療の長期的な影響を推定し、異なる製品やユーザーセグメントにわたる不均一な治療効果を考慮しながら、一貫した客観的な方法ですべての実験の出荷決定を行うための総合評価基準（OEC）を定義したいという問題について議論した。
In sections 6-9, we discussed the importance of culture and engineering systems in running OCEs at scale.
セクション6-9では、OCEを大規模に運営する上での文化とエンジニアリングシステムの重要性について論じた。
We discussed common challenges and approaches in making OCEs the default method for testing any product change and scaling OCE expertise across the company.
我々は、OCEをあらゆる製品変更をテストするための既定の方法とし、OCEの専門知識を全社的に拡大するための共通の課題とアプローチについて議論した。
We also discussed some common challenges and solutions for computation of experiment analysis and metrics, and client bloat due to configurations from a large number of OCEs.
また、実験分析とメトリクスの計算、および多数のOCEからのコンフィギュレーションによるクライアントの肥大化について、一般的な課題と解決策を議論した。
In Sections 10 and 11, we discussed problems and challenges arising from some common deviations from traditional OCEs due to inherent network interactions in different product scenarios and interactions between experiments.
第 10 節と第 11 節では、異なる製品シナリオにおける固有のネットワーク相互作用と実験間の相互作用に起因 する、従来の OCE からの一般的な逸脱から生じる問題と課題について議論した。
There are many more issues of great importance like privacy, fairness and ethics that are handled in each company individually and often form the underlying subtext of the analysis methods and best practices including expert supervision and review described in this paper.
プライバシー、公正さ、倫理といった非常に重要な問題は、各企業で個別に扱われ、本稿で説明する専門家の監督やレビューを含む分析手法やベストプラクティスの根底をなすことが多い。
We hope to discuss these topics in more detail in future summits/meetups.
今後のサミット／ミーティングでは、これらのトピックについてより詳しく議論したい。
We hope this paper sparks further research and cooperation in academia and industry on these problems.
私たちは、この論文がこれらの問題に関して学界と産業界のさらなる研究と協力に火をつけることを願っている。