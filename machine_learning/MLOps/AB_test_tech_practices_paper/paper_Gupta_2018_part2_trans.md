# 5. Heterogeniety in Treatment Effects(HTE) 5. 治療効果における異質性(HTE)

## 5.1. Problem # 5.1.Problem

Without loss of generality, we consider the case that there is only one treatment and one control.
一般性を損なわないように、治療と対照が1つずつしかない場合を考える。
Under the potential outcome framework, (𝑌(1), 𝑌(0)) is the potential outcome pairs and 𝜏 = 𝑌(1) − 𝑌(0) is the individual treatment effect.
潜在的アウトカムの枠組みでは、$(Y(1), Y(0))$ は潜在的なアウトカムのペアであり、$\tau = Y(1) - Y(0)$ は個々の治療効果である。
The primary goal of an A/B test is to understand the average treatment effect (ATE), 𝐸(𝜏).
A/Bテストの主な目的は、**average treatment effect (ATE)**、$E(\tau)$ を理解することである。
Although it is obvious that knowing individual effect is ideal, it is also impossible as we cannot observe the counterfactual.
個々の効果を知ることが理想的であることは明らかだが、反実仮想を観察することは不可能である。
The closest thing is the conditional average treatment effect (CATE) [74], 𝐸(𝜏|𝑋), where 𝑋 is some attribute or side information about each individual that is not affected by the treatment.
最も近いものは、**conditional average treatment effect（CATE）**[74]、$E(\tau|X)$ であり、$X$ は治療に影響を受けない各個人に関する属性や副情報である。
This makes CATE the best regression prediction of individual treatment effect 𝜏 based on 𝑋.
これにより、CATEは $X$ に基づく個々の治療効果 $\tau$ の最良の回帰予測となる。

Attributes 𝑋 can be either discrete/categorical or continuous.
属性 $X$ は離散的/カテゴリー的であるか、連続的であるかのいずれかである。
Categorical 𝑋 segments the whole population into subpopulations, or segments.
**カテゴリー $X$ は、全人口をサブポピュレーション、またはセグメントに分割する**。
In practice, the industry almost entirely uses categorical attributes.
実際には、業界はほとんどすべてカテゴリー属性を使用している。
Even continuous attributes are made discrete and considered ordered categorical segments.
連続的な属性も離散的なものとされ、順序付けられたカテゴリー区分とみなされる。(なるほど...?そうなのか...!)

Perhaps the most interesting cases are when treatment moves the same metric in different directions, or when the same metric has statistically significant movement in one segment but not in another segment.
おそらく最も興味深いケースは、複数のセグメントでtreatmentが同じメトリックを異なる方向に動かす場合、または同じメトリックが1つのセグメントで統計的に有意な動きを示すが、別のセグメントではそうではない場合である。
Assume, for a given segment, say market, a metric moves positively for some markets but negatively for another, both highly statistically significant.
あるセグメント（例えば市場）において、ある指標がある市場ではプラスに動き、別の市場ではマイナスに動き、どちらも統計的に非常に有意であったとする。
Making the same ship decision for all segments would be sub-optimal.
すべてのセグメントで同じship(=適用)の決定をすることは、最適ではないだろう。
Such cases uncover key insights about the differences between segments.
このような事例から、セグメント間の違いに関する重要な洞察が明らかになる。
Further investigation is needed to understand why the treatment was not appreciated in some markets and identify opportunities for improvement.
このtrearmentがいくつかの市場で評価されなかった理由を理解し、改善の機会を特定するためには、さらなる調査が必要である。
In some cases adaptive models can be used to fit different treatments on different types of users [6, 52, 53, 77].
場合によっては、適応モデルを使用して、異なるタイプのユーザーに異なる治療を適合させることができる[6, 52, 53, 77]。

However, most common cases of HTE only show difference in magnitude, not direction.
しかし、一般的なHTE(Heterogeniety Treatment Effects)のケースのほとんどは、方向ではなく、大きさの違いを示すだけである。
Knowledge of these differences can be valuable for detecting outlier segments that may be indicative of bugs affecting a segment, or for encouraging further investment into different segments based on results.
これらの違いの知識は、セグメントに影響を与えるバグの指標となる可能性のあるアウトライアーセグメントを検出するために貴重であり、結果に基づいて異なるセグメントへのさらなる投資を奨励するためにも役立つ。

<!-- ここまで読んだ -->

## 5.2. Common Solutions and Challenges

### 5.2.1. Common Segments 5.2.1. 共通セグメント

It is a very common practice to define key segments based on product and user knowledge.
製品やユーザの知識に基づいて主要セグメントを定義するのは、ごく一般的なやり方だ。
Where possible, it is preferred to define segments so that the treatment does not interact with the segment definition to avoid bias.
可能であれば、バイアスを避けるために、セグメント定義とtreatmentが相互作用しないようにセグメントを定義することが望ましい。(RCTのランダム化がセグメント定義と相関しないように、みたいなことかな?)
Here are some of commonly defined segments for many software products and services:
以下は、多くのソフトウェア製品やサービスにおいて一般的に定義されているセグメントである

#### Market/country:

Market is commonly used by all companies with global presence who are running experiments and shipping features across different markets.
市場は、異なる市場に実験を実施し、機能をリリースしているグローバル企業によって一般的に使用されている。
When there are too many markets, it is useful to put them into larger categories or buckets like markets already with high penetration and growing markets or markets clustered by language.
市場が多すぎる場合、市場がすでに浸透している市場や成長市場、言語によってクラスター化された市場など、より大きなカテゴリーやバケットに分類することが有効である。

#### 2.User activity level:

Classifying users based on their activity level into heavy, light and new users can show interesting HTE.
ユーザの活動レベルに基づいてユーザを重度、軽度、新規ユーザに分類することで、興味深いHTEが示されることがある。
It is important to have this classification based on data before the experiment started to avoid any bias.
バイアスを避けるために、実験が開始される前のデータに基づいてこの分類を行うことが重要である。

#### 3.Device and platform:

Today most products have both desktop and mobile application.
今日、ほとんどの製品はデスクトップとモバイルアプリケーションの両方を持っている。
We can test most backend server-side features across devices and platforms.
デバイスやプラットフォームを問わず、ほとんどのバックエンドサーバーサイドの機能をテストすることができます。
With device and platform fragmentation, it is getting harder to eliminate bugs for all devices and platforms.
デバイスやプラットフォームの分散化により、すべてのデバイスやプラットフォームのバグを排除するのが難しくなっています。
Using device and platform segments in A/B testing is essential to flag potential bugs using live traffic.
A/Bテストでデバイスとプラットフォームのセグメントを使用することは、ライブトラフィックを使用して潜在的なバグをフラグ付けするために不可欠である。(??)
For example, in a recent experiment, a feature of the Outlook mobile app was moving key metrics on all Android devices except a few versions, which indicated further investigation was needed.
例えば、最近の実験では、Outlookモバイルアプリの機能が、一部のバージョンを除いてすべてのAndroidデバイスで主要なメトリックを移動していたため、さらなる調査が必要であることが示された。
Device and platforms also represent different demographics.
デバイスやプラットフォームもまた、さまざまな層を表している。
Many studies show a difference between iOS users and Android users.
多くの調査で、iOSユーザーとAndroidユーザーの違いが示されている。

#### 4.Time and day of week:

Another common segment used is time.
もう一つの一般的に使用されるセグメントは時間である。
Plotting the effects delta or percent delta by day can show interesting patterns, such as the weekday and weekend effect, reveal a novelty effect [13], and help flag data quality issues.
日ごとに効果のデルタ(=差分)やパーセントデルタをプロットすることで、平日と週末の効果、新規性の効果[13]など、興味深いパターンが明らかになり、データ品質の問題をフラグ付けするのに役立つ。

#### 5.Product specific segments:

LinkedIn segmented users by normal user and recruiter.
LinkedInは、通常のユーザとリクルータによってユーザをセグメント化している。
On Twitter, some handles can belong to a single user, so it is useful to segment Twitter handles by primary or secondary account.
Twitterでは、いくつかのハンドルが1人のユーザに属することがあるため、Twitterハンドルを主要アカウントと副次アカウントによってセグメント化することが有用である。
For Netflix, network speed and device types have proved to be good segments.
Netflixの場合、ネットワーク速度とデバイスの種類が良いセグメントであることが証明されている。
Airbnb has found that segments of customers based on whether they have booked before and based on from where they first arrived on Airbnb site are useful.
Airbnbは、以前に予約したかどうかや、Airbnbのサイトを最初に訪れた場所に基づいて顧客をセグメントすることが有効であることを発見した。

### 5.2.2. Methodology and Computation 5.2.2. 方法論と計算

Our community recognizes a lot of recent work from both academia and industry.
私たちのコミュニティは、学界と産業界の両方から多くの最近の仕事を認めている。
The most common mental model is the linear model with a first-order interaction term between treatment assignment and covariates 𝑋: 𝑌 = 𝜃 + 𝛿𝑇 + 𝛽 × 𝑇 × 𝑋 + 𝜖 .
最も一般的なメンタル・モデルは、treatment割り当てと共変量 $X$ の間の1次の相互作用項を持つ線形モデルである：$Y = \theta + \delta T + \beta \times T \times X + \epsilon$。

Most useful segments used by the community are categorical, so the linear model suffices.
コミュニティで使用されるほとんどの有用なセグメントはカテゴリカルであるため、線形モデルで十分である。
There is consensus that the first-order treatment effect adjustment by a single covariate, such as a segment of one categorical variable, is the most actionable.
1つの共変量（例えば、1つのカテゴリカル変数のセグメント）による1次治療効果の調整が最も実行可能であるという合意がある。
One active area of research is adapting more MLMs for identifying HTE [74].
HTEを特定するために、より多くのMLM(=??)を適応させることが、活発な研究分野の1つである[74]。

Nevertheless, there are a lot of outstanding challenges: 1.
とはいえ、未解決の課題も多い：

- 1. **Computation scale:** Because A/B tests routinely analyze hundreds or thousands of metrics on millions of experiment units (users), the resources and time spent on an automatically scheduled analysis cannot be too much to ensure that results are not delayed and are not too expensive to generate.
     計算規模： A/Bテストは、何百ものメトリックを何百万もの実験単位（ユーザ）で定期的に分析するため、結果が遅れることなく、生成に高すぎないことを保証するために、自動スケジュールされた分析に費やされるリソースと時間は多すぎてはならない。
     There is a desire to use a simple algorithm directly formulated using sufficient statistics, instead of using individual-unit level data.
     個体レベルのデータを使用する代わりに、十分な統計量を使用して直接定式化された単純なアルゴリズムを使用したいという要望がある。
- 2.**Low Signal Noise Ratio (SNR)**: A/B testing is already dealing with low power to estimate the average treatment effect.
  低信号雑音比（SNR）： A/Bテストはすでに平均治療効果を推定するための低いパワーを扱っている。
  Learning HTE is even harder than learning ATE because of the reduced sample sizes in each subpopulation.
  HTEを学習することは、各サブポピュレーションのサンプルサイズが減少するため、ATEを学習するよりもさらに難しい。

- 3.**Multiple Testing Problem** [66]: There is a severe multiple testing problem when looking at many metrics, and many possible ways to segment the population. 3.多重検定問題 [66]．多くの指標を見る場合、また母集団を区分する多くの可能な方法を見る場合、深刻な多重検定の問題がある。
  This issue, along with low SNR further complicates HTE estimations.
  この問題は、低SNRとともにHTE推定をさらに複雑にする。

- 4.**Interpretable and memorable results**: Most experimenters are not experts in statistics or machine learning. 4.解釈可能で記憶に残る結果： ほとんどの実験者は統計や機械学習の専門家ではない。
  You must have concise and memorable result summaries to facilitate experimenters to act.
  実験者が行動するためには、簡潔で記憶に残る結果の要約が必要である。
- 5.Absolute vs. Relative: While determining the HTE, you must decide whether you will use absolute CATE or relative CATE (as a percentage of average value of the metric in control).
  絶対的対相対的： HTEを決定する際、絶対的CATEを使用するか、相対的CATE（管理対象の指標の平均値に対するパーセンテージ）を使用するかを決定しなければならない。
  In many cases it makes sense to use the relative CATE as the baseline or the average value of a control metric can be very different for different segments, like different countries.
  多くの場合、ベースラインとして相対的なCATEを使用することは理にかなっている。あるいは、コントロール指標の平均値は、異なる国のように異なるセグメントで大きく異なることがある。
  Use a relative CATE to normalize the treatment effect in different segments.
  異なるセグメントにおける治療効果を正規化するために、相対的CATEを使用する。
  (絶対値か、何倍、みたいな相対的な表現を使うか、みたいな話...??:thinking_face:)

To tackle these challenges, there are common approaches companies take.
これらの課題に対処するために、企業が取る一般的なアプローチがある。

- 1. Separate on-demand and scheduled analysis.
     For ondemand analysis, people are willing to spend more resources and wait longer to get results.
     オンデマンド分析では、人々は結果を得るためにより多くのリソースを費やし、より長く待つことを厭わない。
     For this kind of one-off analysis, linear regression with sparsity (L1 and elastic net) and tree-based algorithms, like causal tree, are very popular.
     このような一回限りの分析には、スパース性を持つ線形回帰（L1やエラスティックネット）や、因果木のような木ベースのアルゴリズムが非常によく使われる。
     Double ML also gained a lot of attention recently [14].
     最近では、Double MLも多くの注目を集めている[14]。
- 2. Because of the challenge of low SNR and multiple testing, sparse modeling is a must. 2.低SNRと多重検定の課題のため、スパースモデリングは必須である。
     Even if the ground truth is not sparse, there are limited resources that experimenters can spend on learning and taking actions based on HTE.
     ground-truthがスパースでなくても、実験者がHTEに基づいて学習し、行動を起こすために費やすことができるリソースは限られている。
     Sparse modeling forces concise results.
- 3. To make results memorable, when certain segment has many values, markets might have a lot of values, it is desired to merge those values based on a common effect. 3.結果を記憶に残るものにするために、あるセグメントが多くの値を持つ場合、市場は多くの値を持つ可能性があり、共通の効果に基づいてそれらの値をマージすることが望まれる。
     For instance, the effect might be different for Asian markets compared to rest of the world.
     **例えば、アジア市場とそれ以外の市場では効果が異なるかもしれない**。
     Instead of reporting market HTE and list treatment effect estimates for individual markets, it is better to merge Asian markets and the rest of the world, and report only two different effect estimates.
     個々の市場について、市場HTEとリスト治療効果推定値を報告する代わりに、アジア市場とその他の市場を統合し、2つの異なる効果推定値のみを報告する方がよい。
     Algorithms that can perform regression and clustering is preferred in these cases, including Fused Lasso [69] and Total Variation Regularization.
     このようなケースでは、Fused Lasso [69]やTotal Variation Regularizationなど、回帰とクラスタリングを実行できるアルゴリズムが好まれます。

<!-- ↑の章よくわかってない...! -->

### 5.2.3. Correlation is not Causation 5.2.3. 相関関係は因果関係ではない

Another difficulty in acting based on HTE results is more fundamental: HTE results are not causal, only correlational.
HTEの結果に基づいて行動することのもう一つの難しさは、より根本的なものである： HTEの結果は因果関係ではなく、相関関係にすぎない。
HTE is a regression to predict individual treatment effect based on covariates 𝑋.
**HTEは、共変量𝑋に基づいて個々の治療効果を予測する回帰である。** (HTEってそうなのか...!)
There is no guarantee that predictor 𝑋 explains the root cause of the HTE.
予測変数𝑋がHTEの根本原因を説明するという保証はない。
In fact, when covariates 𝑋 are correlated, there might be even issues like collinearity.
実際、共変量𝑋が相関している場合、共線性のような問題さえあるかもしれない。
For example, we may find HTE in devices showing iOS users and Android users have different effect.
例えば、iOSユーザーとアンドロイド・ユーザーでは、HTEが異なる効果を示すデバイスが見つかるかもしれない。
Do we know if device is the reason why the treatment effects are different? Of course not.
治療効果が異なる理由がデバイスにあるのかどうか、わかっているのだろうか？もちろんわからない。
iOS and Android users are different in many ways.
iOSとアンドロイドのユーザーは多くの点で異なっている。
To help experimenters investigate the difference, an HTE model that can adjust the contribution of devices by other factors would be more useful.
実験者がその違いを調査するためには、他の要因によってデバイスの貢献度を調整できるHTEモデルがより有用であろう。
Historical patterns and knowledge about whether investigating a segment 𝑋 helped to understand HTE of a metric 𝑀 could provide extra side information.
歴史的なパターンや、あるセグメントを調査することがその指標のHTEを理解するのに役立ったかどうかについての知識は、余分なサイド情報を提供する可能性がある。

# 6. Developing Experimentation Culture 6. 実験文化の発展

<!-- section 5の理解は一旦飛ばそう! section 6が大事そう...! -->

## 6.1. Problem # 6.1.Problem

Culture is the tacit social order of an organization.
**文化とは、組織の暗黙の社会秩序**である。
It shapes attitudes and behaviors in wide-ranging and durable ways.
それは、広範かつ永続的な方法で態度や行動を形成する。
Cultural norms define what is encouraged, discouraged, accepted, or rejected within a group [35].
**文化的規範は、集団の中で何が奨励され、何が落胆され、何が受け入れられ、何が拒否されるかを規定するもの**である［35］。
There is a big challenge in creating an experiment-driven product development culture in an organization.
組織内に実験主導の製品開発文化を生み出すには、大きな課題がある。

Cultural change involves transformation of an organization through multiple phases.
文化的変化には、複数の段階を経た組織の変革が含まれる。
There may be hubris at first, where every idea of the team is considered a winner.
最初は思い上がりがあり、チームのすべてのアイデアが勝者とみなされるかもしれない。
Then there may be introduction of some skepticism as the team begins experimentation and its intuition gets challenged.
チームが実験を開始し、その直感が問われるようになると、懐疑的な見方が導入されるかもしれない。
Finally, a culture develops where there is humility about our value judgement of different ideas, and better understanding of the product and customers [3].
最終的には、異なるアイデアに対する価値判断に謙虚になり、製品や顧客に対する理解を深める文化が育まれる[3]。

It is well known that our intuition is a poor judge for the value of ideas.
私たちの直感がアイデアの価値を判断するのに適していないことはよく知られている。
Case studies at Microsoft showed a third of all ideas tested through an OCE succeed in showing statistically significant improvements in key metrics of interest, and a third showed statistically significant regressions.
Microsoftの事例研究では、OCEを通じてテストされたすべてのアイデアのうち、3分の1が興味のある主要なメトリックで統計的に有意な改善を示し、3分の1が統計的に有意な退行をしめした。
Similar results have been noted by many major software companies [3, 17, 28, 47, 56, 60].
同様の結果は、多くの大手ソフトウェア会社でも指摘されている[3, 17, 28, 47, 56, 60]。
Yet it can be hard to subject your idea to an OCE and receive negative feedback, especially when you have spent a lot of time working on implementing it and selling it to your team.
**とはいえ、自分のアイデアをOCEの対象にして否定的なフィードバックを受けるのは、特に、そのアイデアの実装やチームへの売り込みに多くの時間を費やしてきたときには、つらいことかもしれない**。
This phenomenon is not unique to the software industry.
この現象はソフトウェア業界に限ったことではない。
It is generally referred to as Semmelweis Reflex, based on the story of the long and hard transition of mindset among doctors about the importance of hygiene and having clean hands and scrubs before visiting a patient [65].
これは一般にセンメルワイス反射と呼ばれるもので、医師が患者を訪問する前に清潔な手とスクラブを使い、衛生を保つことの重要性について、長く厳しい意識改革を行ったというエピソードに基づいている[65]。
It takes a while to transition from a point where negative experiment results feel like someone telling you that your baby is ugly.
否定的な実験結果が、誰かに「あなたの赤ちゃんは醜い」と言われたように感じるところから移行するには、しばらく時間がかかる。
You must enact a paradigm shift to put your customers and business in focus and listen to customer responses.
顧客とビジネスに焦点を当て、顧客の反応に耳を傾けるパラダイム・シフトを実施しなければならない。
At that point, negative experiment results are celebrated as saving customers and your business from harm.
その時点で、**否定的な実験結果は、顧客とあなたのビジネスを害から救うものとして称賛される**。
Note that not only bad ideas (including bloodletting [11]) appear as great ideas to a human mind, we are also likely to discount the value of great ideas (including good hand hygiene for doctors [65]).
人間の心には、悪いアイデア（瀉血[11]を含む）が素晴らしいアイデアに見えるだけでなく、**素晴らしいアイデア（医師の手指衛生の良さ[65]を含む）の価値も割り引いて考えてしまう可能性があることに注意しよう**。
There are cases where an idea that languished in the product backlog for months as no one thought it was valuable turns out to be one of the best ideas for the product in its history [51].
誰もそれが価値があるとは思わなかったために、何ヶ月も製品のバックログに放置されていたアイデアが、その製品の歴史上最高のアイデアの1つであることが判明した事例もある[51]。

A culture of working together towards the common goal of improving products through OCEs amplifies the benefits of controlled experimentation at scale [32].
OCEを通じて製品を改善するという共通の目標に向かって協力する文化は、大規模な実験の利点を増幅させる[32]。
This paves the way for frictionless integration of OCEs into the development process, and makes it easy to run an OCE to test an idea, get automated and trustworthy analysis of this experiment quickly, and interpret the results to take the next step: ship the feature, iterate, or discard the idea.
これにより、OCEを開発プロセスに摩擦なく統合する道が開かれ、アイデアをテストし、この実験の自動化された信頼性のある分析を迅速に行い、結果を解釈して次のステップを踏むことが容易になる：機能をリリースする、反復する、またはアイデアを破棄する。
A strong experimentation culture ensures that all changes to the product are tested using OCEs and teams benefit from OCEs discovering valuable improvements while not degrading product quality.
強力な実験文化は、製品へのすべての変更がOCEを使用してテストされ、チームが製品の品質を低下させることなく、価値ある改善を発見するOCEから利益を得ることを保証する。
It allows you to streamline product development discussions so everyone understands the OEC for the product and can take an objective decision to ship a feature based on the impact on the OEC metric.
これにより、**製品開発の議論を効率化し、製品のOECを理解しているすべての人が、OEC指標への影響に基づいて機能をリリースするための客観的な意思決定を行うことができる**。(OECの作り方大事だよな...!)
This gives developers freedom to build and test different ideas with minimum viable improvements without having to sell the entire team on the idea beforehand.
これによって開発者は、最小限の改善を伴うさまざまなアイデアを構築し、テストする自由を持つことができ、事前にチーム全体にアイデアを売り込む必要がなくなる。
And allows the team to make future decisions to invest in a product area based on changes to the OEC metric due to features seen in that area.
また、その領域で見られる機能によるOEC指標の変化に基づいて、製品領域に投資するための将来の意思決定をチームに行うことができる。

<!-- ここまで読んだ! -->

## 6.2. Common Solutions and Challenges

There are many cultural aspects to adoption of OCEs at scale to have a trustworthy estimate of the impact of every change made to a product.
製品に加えられたすべての変更の影響を信頼できるように評価するために、OCEの大規模な採用には多くの文化的側面がある。

### 6.2.1. Experimentation Platform and Tools 6.2.1. 実験プラットフォームとツール

First, we need to make sure that the experimentation platform has the right set of capabilities to support the team.
**まず、実験プラットフォームがチームをサポートする適切な機能を備えていることを確認する必要がある**。
It must be able to test the hypothesis of interest to the product team.
製品チームにとって関心のある仮説を検証できなければならない。
To do that one of the of the most important things required is a set of trustworthy and easily interpretable metrics to evaluate a change made to the product.
そのために必要な最も重要なものの1つは、**製品に加えられた変更を評価するための信頼性のあるかつ簡単に解釈できるmetricsのセット**である。
In addition, it’s useful if there are easy tools to manage multiple experiments and clearly communicate results from these experiments.
さらに、複数の実験を管理し、実験結果を明確に伝えるための簡単なツールがあると便利である。

### 6.2.2. Practices, Policies and Capabilities 6.2.2. 実践、方針、能力

The second aspect deals with creating right set of practices, policies, and capabilities to encourage teams to test every change made to their product using OCEs.
第二の側面は、OCEを使用して製品に加えられたすべての変更をテストすることをチームに奨励するための、**適切なプラクティス、ポリシー、および能力のセットを作成すること**である。
The following are strategies that different companies use to achieve this goal.
以下は、この目標を達成するために各企業が採用している戦略である。

#### High Touch:

Once per quarter, the LinkedIn experimentation team handpicks a few business-critical teams, prioritizes these teams, and then works closely with them on their needs.
LinkedInの実験チームは、四半期に一度、ビジネスクリティカルなチームを数チーム選び、優先順位をつけ、そのチームのニーズと密接に連携します。
At the end of the quarter the team agrees they’ll use that experiment platform going forward, and the experimentation team continues to monitor them.
四半期の終わりには、チームはその実験プラットフォームを今後も使用することに同意し、実験チームはそれを監視し続ける。
Over several years a data-driven culture is built.
数年かけてデータ主導の文化が構築される。
Managers and directors now rely on development teams running experiments before features launch.
今やマネージャーやディレクターは、開発チームが機能を立ち上げる前に実験を行うことに依存している。

The Microsoft experimentation team selects product teams to onboard based on factors indicative of the impact experimentation has on the product.
マイクロソフトの実験チームは、実験が製品に与える影響を示す要因に基づいて、参加する製品チームを選択する。
The experimentation team works very closely with product teams over multiple years to advance the adoption of experimentation and its maturity over time.
**実験チームは、複数年にわたり製品チームと密接に協力し、実験の導入とその成熟を長期的に進める**。(うちのチームの場合は、実験チーム = プロダクトチームかも。)
The downside of the High Touch approach is the large overhead in having a deep engagement with every team, and it may become a bottleneck for scaling.
ハイ・タッチ・アプローチの欠点は、すべてのチームとの深い関与による大きなオーバーヘッドであり、スケーリングのボトルネックになる可能性がある。

#### Top down buy in:

It can help if there is a buy-in into experimentation by leadership and they expect every change tested in a controlled experiment.
リーダーシップ層が実験に賛同し、管理された実験ですべての変更がテストされることを期待している場合、それは助けになる。
Further they can set team goals based on moving a metric in controlled experiments.
さらに、彼らは管理された実験で指標を動かすことに基づいてチームの目標を設定することができる。
This creates a culture where all ship decisions are talked about in terms of their impact on key metrics.
これにより、**すべての船の決定が主要な指標への影響という観点から語られる文化が生まれる**。
The product teams celebrate shipping changes that improve key metrics, and equally importantly, celebrate not shipping changes that would cause a regression in key metrics.
**製品チームは、主要メトリクスを改善する変更を出荷することを祝い、同様に重要なことは、主要メトリクスを後退させるような変更を出荷しないことを祝う**。
It is important that the team’s key metrics are determined beforehand and agreed upon by the team.
**チームの重要な指標を事前に決定し、チームで合意しておくことが重要である**。(うんうん...!)
It is prudent to be cautious about preventing the gaming of metrics or over fitting metric flaws, where the metrics of interest move but are not indicative of improvement in the product.
メトリクスのゲーミングやメトリクスの欠陥の過剰適合を防ぐことに注意することが賢明である。興味のあるメトリクスが動くが、製品の改善を示していない場合がある。
At Netflix a long-standing culture of peer review of experiment results is organized around frequent “Product Strategy” forums where results are summarized and debated amongst experimenters, product managers, and leadership teams before an experiment is “rolled out”.
ネットフリックスでは、実験結果の長年にわたる**同僚による査読文化**が、実験が「ロールアウト」される前に、実験者、製品マネージャー、リーダーシップチームの間で結果が要約され、議論される頻繁な「製品戦略」フォーラムの周りに組織されている。

#### Negative and positive case studies:

Stories about surprising negative results where a feature that is widely acclaimed as a positive causes a large regression in key metrics, or a surprising positive incident where a small change no one believed would be of consequence causes a large improvement in a metric were great drivers for cultural change.
広く称賛されている機能が大きな主要メトリクスの後退を引き起こすという驚くべき否定的な結果や、誰もが重要であるとは思わなかった小さな変更が大きなメトリクスの改善を引き起こすという驚くべき肯定的な**事例についての話は、文化の変化を促進する大きな要因**であった。(オフライン評価の話はまさにこれかも...!)
These cases drive home a humbling point that our intuition is not a good judge of the value of ideas.
これらのケースは、私たちの直感はアイデアの価値を判断するのに適していないという謙虚な指摘を突きつけている。
There are some documented examples the best OCEs with surprising outcomes [4].
驚くべき結果をもたらした最高のOCEの例がいくつか文書化されている[4]。
For instance, an engineer at Bing had the idea to make ad titles longer for ads with very short titles.
例えば、**Bingのエンジニアが、非常に短いタイトルの広告に対して広告タイトルを長くするアイデアを持っていた**。
The change was a simple and cheap, but it was not developed for many months as neither the developer nor the team had much confidence in the idea.
この変更はシンプルで安価なものだったが、開発者もチームもこのアイデアにあまり自信を持っていなかったため、何カ月も開発が進まなかった。
When it was finally tested, it caused one of the biggest increases in Bing revenue in history [51].
**最終的にテストされたときには、Bing史上最大級の収益の増加を引き起こした**[51]。

#### Safe Rollout:

It is easier to get a team to adopt experimentation when it fits into their existing processes and makes them better.
**実験がチームの既存のプロセスに適合し、それらのプロセスをより良くすると、実験を採用することは簡単である**。
Some teams at Microsoft and Google began using experimentation as a way to do safe feature rollouts to all users, where an A/B test runs automatically during deployment as the feature is gradually turned on for a portion of users (Treatment) and others (Control) don’t have the feature turned on.
マイクロソフトやグーグルの一部のチームは、**全ユーザに安全に機能をロールアウトする方法として、実験を使い始めた**。そこでは、一部のユーザ (Treatment)には機能を徐々にオンにし、他のユーザー（Control）には機能をオンにしないように、**デプロイ時にA/Bテストを自動的に実行する**。
During this controlled feature rollout, the feature’s impact estimate on key reliability and userbehavior metrics helped find bugs.
この管理された機能ロールアウトの間、**主要な信頼性とユーザ行動のメトリクスに対する機能の影響の推定値がバグを見つけるのに役立った**。(=このバグを見つけるのに役立った、というのが「チームの既存のプロセスをより良くしている」という点なのか...!:thinking_face:)

This method helps gain a toe hold in the feature team’s development process.
この方法は、機能チームの開発プロセスにおける足場を得るのに役立つ。
Over time, as the feature team started seeing value in experimentation, they looked forward to using experimentation to test more hypotheses.
時が経つにつれて、機能チームは実験を使ってさらに多くの仮説をテストすることを楽しみにしていた。

#### Report cards and Gamification:

Microsoft found that they encourage the adoption of OCEs in a set of teams by having a report card for each team that assesses their experimentation maturity level [31].
マイクロソフトは、**各チームに対して実験の成熟度レベルを評価する成績表を持つことで、一連のチームにOCEの採用を奨励することができる**ことを発見した[31]。
This report card gives the team a way to think about the potential of using experiments to improve the product.
この成績表は、実験を使って製品を改善する可能性について考える方法をチームに与える。
It gives the team a measure of its status and relative status among other teams and helps highlight key areas where they can invest to further improve.
これにより、チームの地位と他のチームとの相対的な地位が測定され、さらなる改善のために投資できる重要な分野が浮き彫りになる。

Booking.com is experimenting with gamification in their experimentation platform where users of the platform can receive badges to encourage the adoption of good practices.
Booking.comは、**彼らの実験プラットフォームでゲーミフィケーションを試しており、プラットフォームのユーザは、良い実践の採用を奨励するためにバッジを受け取ることができる**。

Twitter and Microsoft also use mascots, like duck [70] and HiPPO [37] to spread awareness about experimentation in their companies.
ツイッター社やマイクロソフト社も、アヒル[70]やHiPPO[37]のようなマスコットを使って、自社における実験についての認識を広めている。(??)

#### Education and support:

When a company tests thousands of experiments a year, it is impossible for experimentation teams to monitor each experiment to ensure that experiment analysis is trustworthy.
企業が年間何千もの実験をテストする場合、**実験チームが各実験を監視して実験分析が信頼できることを確認することは不可能**である。
It is important that each team has subject matter experts to help them run experiments and ensure that they obtain reliable and trustworthy results.
各チームが実験を行い、信頼できる結果を得られるようにするためには、各分野の専門家がいることが重要である。
Educating team members on how to use OCEs to test hypotheses and how to avoid common pitfalls is critical in scaling experimentation adoption.
**仮説を検証するためにOCEをどのように使用し、よくある落とし穴をどのように避けるかについてチームメンバーを教育することは、実験の採用を拡大する上で極めて重要**である。
We will discuss this important point in detail in section 7.
この重要な点については、第7節で詳述する。

<!-- ここまで読んだ! -->

# 7. Training Others in the Organisation to scale Experimentation 7. 実験規模を拡大するために組織内の他者を訓練する

## 7.1. Problem # 7.1.Problem

While the concept of an A/B test is simple, there can be complex practical issues in designing an experiment to test a particular feature and analyzing the results of the experiment.
A/Bテストのコンセプトはシンプルだが、特定の機能をテストするための実験を設計し、実験結果を分析するには、複雑な現実的問題が発生する可能性がある。
Product teams need custom support when running experiments, because they often have very specific questions that cannot be answered with a simple set of frequently answered questions.
製品チームは、実験を行う際にカスタムサポートを必要とする。なぜなら、よくある質問の単純なセットでは答えられないような、非常に具体的な質問がよくあるからだ。
A centralized support function does not scale very well.
中央集権的なサポート機能は、あまりうまくスケールしない。
Central teams end up spending too much time on support and not enough on other things.
セントラル・チームはサポートに多くの時間を費やし、他のことに十分な時間を割けなくなってしまう。
Additionally, specific product domain knowledge is often required to provide support.
さらに、サポートを提供するためには、特定の製品分野の知識が必要になることも多い。
A centralized support function requires deep knowledge of all supported products, which is often not feasible.
サポート機能を一元化するには、すべてのサポート対象製品に関する深い知識が必要だが、それはしばしば実現不可能である。
Conversely, anyone providing support needs fundamental experimentation knowledge, which might be easier to scale.
逆に、サポートを提供する人は、基礎的な実験の知識が必要で、その方がスケールアップしやすいかもしれない。
Such democratization of knowledge and expertise enables a better experimentation culture.
このような知識と専門知識の民主化によって、より良い実験文化が可能になる。

## 7.2. Common Solutions and Challenges

Across different companies, there are a few key practical challenges in spreading the expertise about OCEs that enable experimentation at scale.
様々な企業において、大規模な実験を可能にするOCEに関する専門知識を普及させるには、いくつかの重要な現実的課題がある。
• How do we set up a community to support experimenters? • How do we incorporate them in the experiment lifecycle? • How do we incentivize these people? • How do we quantify their impact? • How do we train them? • How do we maintain quality standards? Here are examples from several companies on how they tried to solve these challenges.

- 実験者を支援するコミュニティをどのように立ち上げるか？- 実験者を実験のライフサイクルに組み込むには？- 実験者にインセンティブを与えるには？- 彼らの影響をどのように定量化するか？- どのように彼らを訓練するか？- どうやって品質基準を維持するのか？これらの課題をどのように解決しようとしたのか、いくつかの企業の例を紹介しよう。

### 7.2.1. Yandex: “Experts on Experiment” 7.2.1. ヤンデックス "実験のエキスパート"

At Yandex, a program called “Experts on Experiment” exists to scale support.
ヤンデックスでは、サポートを拡大するために「Experts on Experiment」と呼ばれるプログラムが存在する。
These Experts are handpicked from product teams by the central experimentation group.
これらのエキスパートは、中央実験グループによって製品チームから厳選される。
Any experiments must be approved by an Expert before they are allowed to ship.
いかなる実験も、出荷前にエキスパートの承認を得なければならない。
Experts are motivated because their product needs approval before shipping, so they voluntarily sign up to be an Expert.
エキスパートのモチベーションは、出荷前に製品の承認が必要なため、自発的にエキスパートとして登録することだ。
Their application is then reviewed by the central experimentation group.
その後、中央の実験グループが申請を審査する。
Experts are motivated by the status provided by being an Expert.
専門家は、専門家であることによってもたらされる地位によって動機づけられる。
They get a digital badge in internal staff systems, so their status is visible to others.
社内のスタッフ・システムにはデジタル・バッジが表示され、そのステータスは他のスタッフにもわかるようになっている。
There are no clear KPIs for the program.
プログラムの明確なKPIはない。
There is a checklist of minimum experience and an informal interview process involved in becoming an expert.
エキスパートになるためには、最低限の経験に関するチェックリストと非公式の面接プロセスがある。

### 7.2.2. Amazon: “Weblab Bar Raisers” 7.2.2. アマゾン "ウェブラボ・バーレイザー"

Weblab is Amazon’s experimentation platform.
ウェブラボはアマゾンの実験プラットフォームだ。
In 2013, Amazon’s Personalization team piloted a “Weblab Bar Raisers” program in their local organization with the intention of raising the overall quality of experimental design, analysis, and decision making.
2013年、アマゾンのパーソナライゼーション・チームは、実験デザイン、分析、意思決定の全体的な質を高めることを意図して、「Weblab Bar Raisers」プログラムを現地組織で試験的に実施した。
The initial Bar Raisers were selected to be high-judgment, experienced experimenters, with an ability to teach and influence.
最初のバーレイザーは、判断力が高く、経験豊富な実験者であり、教える能力と影響力を持つ者が選ばれた。
Expectations for the role were clearly defined and documented and, after a few iterations, the program was expanded company wide.
役割に対する期待は明確に定義され、文書化され、何度か繰り返された後、このプログラムは全社的に拡大された。
Bar Raiser review is not mandatory for all organizations; often because not enough Bar Raisers are available.
バーレイザーの審査は、すべての団体に義務付けられているわけではない。
Bar Raisers spend about 2–4 hours per week providing OCE support.
バー・レイザーは、OCEのサポートに週2～4時間程度を費やしている。
Incentives rely on Bar Raisers buying into the mission of the program, which contributes to their personal growth and status within the company.
インセンティブは、バー・レイザーがプログラムの使命を理解し、個人的な成長と社内での地位向上に貢献することに依存している。
A mentorship program, where existing Bar Raisers train new ones, exists to ensure that new Bar Raisers are brought up to speed quickly.
既存のバー・レイザーが新しいバー・レイザーを教育するメンターシップ・プログラムがあり、新しいバー・レイザーが迅速にスピードアップできるようになっている。

### 7.2.3. Twitter: “Experiment Shepherds” 7.2.3. ツイッター 「シェパードの実験

At Twitter, the “Experiment Shepherds” program, founded three years ago by a product group including the current CTO, now has approximately 50 shepherds.
ツイッター社では、現CTOを含む製品グループが3年前に設立した「エクスペリメント・シェパード」プログラムがあり、現在約50人のシェパードがいる。
Most of these are engineers with experience running experiments.
そのほとんどは実験の経験を持つエンジニアだ。
There are strict entry requirements.
厳しい入団条件がある。
Experiment owners implicitly opt-in for review: either pre-test or pre-launch.
実験所有者は暗黙のうちにレビューをオプトインする： プレテストまたはプレローンチ。
Shepherds have on-call duty one week a year to triage incoming requests.
シェパードは年に1週間、オンコール当番があり、寄せられる依頼をトリアージする。
Incentives include feelings of responsibility for the product and acknowledgement of contribution during performance review.
インセンティブには、製品に対する責任感や、業績評価時に貢献が認められることなどが含まれる。
There are no clear impact KPIs, but qualitatively impact seems to exist.
明確なインパクトKPIはないが、定性的にはインパクトがあるようだ。
There is a structured training program consisting of one hour of classroom training per week for two months.
2ヶ月間、週1時間の座学研修からなる体系的な研修プログラムがある。
These classes cover seven topics (e.g.dev cycle, ethics, metrics, stats 101).
これらのクラスは7つのトピック（開発サイクル、倫理、メトリクス、統計101など）をカバーしている。
There are also case study-based discussions.
ケーススタディに基づいたディスカッションもある。

### 7.2.4. Booking.com: “Experimentation Ambassadors” 7.2.4. ブッキング・ドットコム "実験大使"

At Booking.com, the “Experimentation Ambassadors” program started about six months ago.
ブッキング・ドットコムでは、半年ほど前から「実験大使」プログラムを開始した。
The central experimentation organization handpicked people (~15) with experimentation experience and interest in providing support in product organizations that seemed to need the most support.
中央の実験組織は、実験経験があり、最もサポートを必要としていると思われる製品組織でサポートを提供することに関心のある人々（〜15人）を厳選した。
Ambassadors form the first line of support with a clear escalation path and priority support from the central organization.
アンバサダーは、明確なエスカレーション・パスと中央組織からの優先的なサポートによって、サポートの第一線を形成する。
Ambassadors are hooked into the central support ticketing system so that they are aware of other open support questions and can pick up tickets as they see fit.
アンバサダーは中央のサポートチケットシステムに接続され、他の未解決のサポートに関する質問を把握し、適切と思われるチケットをピックアップすることができます。
They are included in the experimentation organization’s internal communications, to keep them aware of current developments or issues.
実験組織の内部コミュニケーションに参加させ、現在の進展や問題を常に把握させる。
There is a monthly meeting to discuss product needs and concerns.
製品のニーズや懸念事項を話し合う月例会議がある。
Incentives for Ambassadors include feeling responsible for the product, getting priority support from the central organization, and acknowledgement on their performance review.
アンバサダーへのインセンティブとしては、製品に対する責任を感じること、中央組織からの優先的なサポートを受けること、業績評価で認められることなどがある。
There are no clear impact or quality KPIs, but there are plans to include these as the program scales.
明確な影響や質のKPIはないが、プログラムの規模が拡大するにつれて、これらを含める計画がある。
There is no specific training for Ambassadors, but there is extensive general experiment training for all experimenters, including Ambassadors.
アンバサダーのための特別なトレーニングはないが、アンバサダーを含むすべての実験者を対象とした広範な一般実験トレーニングがある。

### 7.2.5. Booking.com: “Peer-Review Program” 7.2.5. ブッキング・ドットコム 「ピアレビュー・プログラム

Booking.com also has a separate “Peer-Review Program” aimed at getting people involved in providing pro-active feedback to experimenters.
Booking.comはまた、実験者に積極的なフィードバックを提供するために人々を巻き込むことを目的とした「ピアレビュー・プログラム」を別途用意している。
Anyone in the company can opt-in to the program.
社内の誰でもこのプログラムに参加することができる。
Every week participants are paired with a random counterpart.
毎週、参加者はランダムな相手とペアを組む。
Currently approximately 80 people participate.
現在約80人が参加している。
Each pair picks a random experiment to review.
各ペアがランダムに実験を選び、レビューする。
The experiment platform includes a “give me a random experiment” button for this purpose.
実験プラットフォームには、この目的のために「ランダムな実験をする」ボタンが用意されている。
The platform also supports built-in commenting and threading as part of the reporting interface.
また、このプラットフォームは、レポーティング・インターフェースの一部として、ビルトインのコメントとスレッディングをサポートしている。
Incentives to participate include making new friends, learning new things, and reward badges displayed on the platform interface.
新しい友達を作ったり、新しいことを学んだり、プラットフォームのインターフェイスに表示される報酬バッジなど、参加へのインセンティブがある。
There are KPIs defined around reviews and comments.
レビューとコメントに関するKPIが定義されている。
Newcomers are paired with experienced users the first few times to ensure that they are brought up to speed.
新人は、最初の数回は経験豊富なユーザーとペアを組み、スピードアップを図る。
A one-page guide for writing good reviews is also available [33].
良いレビューを書くための1ページのガイドも用意されている[33]。

### 7.2.6. Microsoft: Center of Excellence Model 7.2.6. マイクロソフト センター・オブ・エクセレンス・モデル

At Microsoft, a data scientist or two from the central experimentation platform team (Analysis & Experimentation) work very closely with a product team.
マイクロソフトでは、中央の実験プラットフォームチーム（分析と実験）のデータサイエンティストが1人か2人、製品チームと密接に連携している。
At first, the data scientists from the experimentation platform handle almost all support needs for the product and gain good insight into the product, business, customers, technology, and data.
最初のうちは、実験プラットフォームのデータサイエンティストが製品に関するほぼすべてのサポートニーズに対応し、製品、ビジネス、顧客、テクノロジー、データに関する優れた洞察を得る。
At the same time, the data scientists work on transferring knowledge and expertise to champions in the product team.
同時に、データサイエンティストは知識と専門知識を製品チームのチャンピオンに伝える作業も行う。
The expectation is that over time, as more experiments are run, the product team will become more self-sufficient in running trustworthy experiments, and the person from the central experimentation platform team helps with a smaller and smaller percentage of experiments—those that are unique or have issues.
時間の経過とともに、より多くの実験が実行されるにつれて、製品チームは信頼できる実験の実行においてより自立的になり、中央の実験プラットフォームチームからの担当者は、ユニークな実験や問題のある実験など、より少ない割合の実験を支援するようになることが期待される。
The data scientists from the central team and champions from the product team usually conduct further training to educate the entire product team on best practices and processes for running experiments.
中央チームのデータサイエンティストと製品チームのチャンピオンは、通常、実験を実行するためのベストプラクティスとプロセスについて製品チーム全体を教育するために、さらなるトレーニングを実施する。
The experimentation team maintains a monthly scorecard to measure the goals of each product onboarding for running trustworthy experiments at scale.
実験チームは、信頼に足る実験を大規模に行うために、各製品のオンボーディングの目標を測定するスコアカードを毎月管理している。
These goals are set at the beginning of every year.
これらの目標は毎年初めに設定される。
Every six weeks, the data scientists and champions review the experimentation operations in the product where successes and failures from the past are highlighted along with a plan to address gaps and opportunities.
6週間ごとに、データサイエンティストとチャンピオンは、製品における実験オペレーションをレビューし、過去の成功例と失敗例が、ギャップとチャンスに対処するための計画とともに強調される。
The incentives for data scientists and champions are partially tied to the success of experimentation in their respective products.
データサイエンティストとチャンピオンのインセンティブは、それぞれの製品における実験の成功に部分的に結びついている。
The central experimentation team holds a weekly experiment review, where any experiment owner can share their experiment and request feedback from the data scientists.
中央実験チームは毎週実験レビューを開催し、実験オーナーは誰でも自分の実験を共有し、データサイエンティストからのフィードバックを求めることができる。
The central experimentation team also conducts a monthly Introduction to Experimentation class and Experiment Analysis lab open to everyone at Microsoft.
中央実験チームはまた、マイクロソフトの誰もが参加できる実験入門クラスと実験分析ラボを毎月開催している。
In addition, twice a year the team hosts a meeting focused on experiments and discusses the best controlled experiments.
さらに、年に2回、チームは実験に焦点を当てたミーティングを開催し、最善の対照実験について議論している。
This provides product teams an opportunity to showcase their strengths in experimentation and learn from other teams.
これは、製品チームが実験において自分たちの強みを発揮し、他のチームから学ぶ機会を提供する。

### 7.2.7. Google: Just-in-time Education Model 7.2.7. グーグル ジャスト・イン・タイムの教育モデル

Google has used a variety of approaches, but one of the most successful relies heavily on just-in-time education [67].
グーグルはさまざまなアプローチを使っているが、最も成功しているのは、ジャスト・イン・タイム教育に大きく依存しているものだ[67]。
For example, for experiment design, they have a checklist that asks experimenters a series of questions, ranging from “what is your hypothesis?” to “how will you measure success?” and “how big of a change do you need to detect?” Google has an “experiment council” of experts who review the checklists, and have found consistently that the first time through, an experimenter needs handholding.
例えば、実験デザインについては、"仮説は何か？"から "どのように成功を測定するのか？"、"どの程度の変化を検出する必要があるのか？"まで、一連の質問を実験者に投げかけるチェックリストがある。グーグルには、チェックリストを見直す専門家からなる "実験評議会 "があり、初回は実験者が手取り足取り教える必要があることを一貫して発見している。
But on subsequent experiments, less handholding is needed, and the experimenter starts teaching their team members.
しかし、その後の実験では、手取り足取り教える必要はなくなり、実験者はチームメンバーに教え始める。
As they become more experienced, some experimenters can become experts and perform reviews.
経験を積むにつれて、専門家になってレビューを行う実験者も出てくる。
Some teams have sufficient expertise that they can retire the entire checklist process.
チームによっては、チェックリストの全プロセスを引退させることができるほどの専門知識を持っている。
For analysis, Google has an experiment review similar to Microsoft.
分析に関しては、グーグルはマイクロソフトと同様の実験レビューを行っている。
The advantage is both just-in-time education to experimenters about interpreting experiment results and metaanalysis by experts to find the larger patterns.
その利点は、実験結果の解釈に関する実験者へのジャストインタイムの教育と、より大きなパターンを見つけるための専門家によるメタ分析の両方である。
