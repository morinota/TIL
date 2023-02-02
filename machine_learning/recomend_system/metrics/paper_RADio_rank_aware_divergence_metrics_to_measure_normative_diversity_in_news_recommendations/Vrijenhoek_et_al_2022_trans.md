## 0.1. link

- [pdf](https://arxiv.org/pdf/2209.13520.pdf) pdf](https:

## 0.2. title タイトル

RADio – Rank-Aware Divergence Metrics to Measure Normative Diversity in News Recommendations
RADio - ニュース推薦における規範的多様性を測定するためのランク認識型ダイバージェンスメトリクス

## 0.3. abstract アブストラクト

In traditional recommender system literature, diversity is often seen as the opposite of similarity, and typically defined as the distance between identified topics, categories or word models.
従来の推薦システムの文献では、**多様性は類似性の反対と見なされる**ことが多く、一般に識別されたトピック、カテゴリ、または単語モデル間の距離として定義される.
However, this is not expressive of the social science’s interpretation of diversity, which accounts for a news organization’s norms and values and which we here refer to as normative diversity.
しかし、これは、**報道機関の規範や価値観を考慮した社会科学的な多様性の解釈を表現しておらず**、ここでは**規範的多様性**と呼ぶことにする.
We introduce RADio, a versatile metrics framework to evaluate recommendations according to these normative goals.
我々は、これらの規範的な目標に従って推薦を評価するための汎用的なメトリックフレームワークである**RADio**を紹介する.
RADio introduces a rank-aware Jensen Shannon (JS) divergence.
RADioはランクを考慮したジェンセン・シャノン（JS）ダイバージェンスを導入している.
This combination accounts for (i) a user’s decreasing propensity to observe items further down a list and (ii) full distributional shifts as opposed to point estimates.
この組み合わせは、(i)ユーザーがリストのさらに下のアイテムを観察する傾向が減少すること、(ii)点推定ではなく、完全な分布シフトを説明するものである.
We evaluate RADio’s ability to reflect five normative concepts in news recommendations on the Microsoft News Dataset and six (neural) recommendation algorithms, with the help of our metadata enrichment pipeline.
我々は、**Microsoft News Dataset**と6つの推薦アルゴリズム（ニューラル）において、**RADioが5つの規範的概念をニュース推薦に反映する能力**を、我々のメタデータ強化パイプラインの助けによって評価した.
We find that RADio provides insightful estimates that can potentially be used to inform news recommender system design.
その結果、**RADioはニュース推薦システムの設計に利用できる可能性のある**、洞察に満ちた推定値を提供することがわかった.

# 1. Introduction はじめに

For centuries, the interplay between journalists and news editors has shaped how news items are created and how they are shown to their readers [82].
何世紀にもわたって、ジャーナリストとニュース編集者の間の相互作用は、ニュースアイテムがどのように作成され、それらがどのように読者に示されるかを形作ってきた[82].
With the digitization of society, much has changed: while before, people would typically limit themselves to reading one type of newspaper, they now have a wealth of information available to them at the click of a button [63] – more than anyone could possibly be expected to read or make sense of.
社会のデジタル化に伴い、多くのことが変化した. 以前は、人々は通常、1種類の新聞を読むことに限定していたが、今では、ボタンをクリックするだけで利用できる豊富な情報 [63]を手に入れることができ、誰もが読み、理解することを期待できる量を超えている.
News recommender systems can filter the enormous amount of information available to just those news items that are in some way interesting or relevant to their users [8, 52].
ニュース推薦システムは、利用可能な膨大な情報を、ユーザーにとって何らかの形で興味深い、あるいは関連性のあるニュースアイテムだけに絞り込むことができる[8, 52].
The use of news recommender systems is widespread, not just for personalized news recommendations, but also to automatically populate the front page of a news website [53], or present the reader of a particular news article with other articles about the same topic, but from a different perspective [54].
ニュース推薦システムは，パーソナライズされたニュースを推薦するだけでなく，ニュースウェブサイトのフロントページを自動的に生成したり [53]，特定のニュース記事の読者に同じトピックに関する他の記事を異なる視点から提示したり [54]するために広く利用されている．
The use of news recommender systems has a wide range of benefits.
ニュース推薦システムの利用には、さまざまな利点がある.
They can increase engagement [55] and help raise informed citizens [28].
**engagementを高める(?)**ことができ [55]、情報通の市民を育てるのに役立つ [28].
A news recommender system may broaden the horizons of their users by presenting diverse recommendations, including items different from what they are used to or expect seeing.
**ニュース推薦システムは、ユーザーが見慣れているもの、あるいは期待しているものとは異なるものを含む多様な推薦を提示することによって、ユーザーの視野を広げることができるかもしれない**.
They could even foster tolerance and understanding [29, 66], and counter so-called filter bubbles or echo chambers [52, 58].
さらに、**寛容さと理解を育み** [29、66]、いわゆるフィルターバブルやエコーチェンバーに対抗できるかもしれない [52、58].

To realize the potential benefits of news recommender systems, much attention has been given to generating recommendations that reflect the user’s interests and preferences [39].
**ニュース推薦システムの潜在的な利点を実現するために**、ユーザーの興味や嗜好を反映した推薦文を生成することに注目が集まっている[39].
However, with news recommenders taking over the role of human editors in news selection, they are becoming gatekeepers in what news is shown to audiences and have thus a democratic role to play in society.
しかし，ニュースレコメンダーは，ニュース選択における人間の編集者の役割を引き継ぎ，どのようなニュースが視聴者に示されるかのゲートキーパーとなりつつあり，社会的に民主的な役割を担っている．
As such, their evaluation has different requirements than those of other types of recommender systems [4, 5, 72, 75].
そのため，**その評価は他のタイプのレコメンダーシステムとは異なる要件を持つ** [4, 5, 72, 75].
Recent controversies have shown that merely optimizing for click-through rates and engagement may promote sensationalist content [68], and is particularly conducive to the spread of misinformation.1
**最近の論争では、click-through率やengagementを最適化するだけでは、センセーショナルなコンテンツを助長しかねず[68]、特に誤報の拡散を助長することが示されている**.
This observation is not limited to the academic literature – an increasing number of media organizations, both public service and commercial, have acknowledged the difficulties in translating their editorial norms into concrete metrics that can inform recommender system design [9, 32].
この観察は、学術的な文献に限ったことではなく、公共サービスや商業の両方のメディア組織が、編集規範をレコメンダーシステムの設計に役立つ具体的な指標に変換することの難しさを認めています [9、32].
News recommender systems exist in a complex space consisting of many different areas and disciplines, each with their own goals and challenges; think of balancing diversity and accuracy [57], nudging [50] or even identifying user preferences [6, 49] and biases [74].
ニュース推薦システムは、多様性と正確さのバランス [57]、ナッジング [50]、あるいはユーザーの好み [6, 49]やバイアス [74]の特定など、多くの異なる分野や領域からなる複雑な空間に存在し、それぞれが独自のゴールと課題を抱えている.
In this paper, we focus on the process of translating normative theory (i.e., what it means for a recommendation to be diverse) into metrics that are usable and understandable for both technical and editorial purposes.
この論文では、規範的な理論（すなわち、推薦が多様であることの意味）を、技術的および編集的な目的のために使用可能で理解しやすいメトリクスに変換するプロセスに焦点を当てる.
We build on the work of Helberger [33], who provides a theoretical foundation for conceptualizing diversity, and of Vrijenhoek et al. [71], who propose a new set of metrics (DART) that reflect this theory.
我々は、多様性を概念化するための理論的基礎を提供したHelberger [33]の仕事と、この理論を反映した新しいメトリクス（DART）のセットを提案したVrijenhoekら[71]の仕事を基礎としている.
The DART metrics represent a first step towards a normative interpretation of diversity in news recommendations.
DARTメトリクスは、ニュース推薦における多様性の規範的解釈への第一歩となるものである.
We identify a number of possible shortcomings in these metrics: there could be more consideration for the theory of metrics and distance functions, generalizability to other normative concepts, unification under one framework, and rankawareness.
我々は、これらのメトリクスの欠点として、メトリクスの理論や距離関数への配慮、他の規範的概念への一般化、一つの枠組みの下での統一、ランク認識などが考えられることを挙げている.
In this paper, we focus on the mathematical aspects of a rank-aware metric, versatile to different normative concepts and as such addressing these shortcomings.
この論文では、ランク認識メトリックの数学的側面に焦点を当て、異なる規範概念に汎用性があり、その結果、これらの欠点に対処している.
We refer to our framework as the Rank-Aware Divergence metrIcs to measure nOrmative diversity (RADio).
我々はこのフレームワークを**Rank-Aware Divergence metrIcs to measure nOrmative diversity (RADio)**と呼んでいる.

Our contribution consists of a diversity metric that is (i) versatile to any normative concept and expressed as the divergence between two (discrete) distributions; (ii) rank-aware, taking into account the position of an item in a recommendation set; and (iii) mathematically grounded in distributional divergence statistics.
我々の貢献は、(i)あらゆる規範的概念に汎用性があり、2つの（離散）分布間の発散として表現され、(ii)推薦セット内の項目の位置を考慮し、ランクを意識し、(iii)分布発散統計に数学的根拠を持つ多様性メトリックから構成される.
We demonstrate the effectiveness of this formulation of the metrics by defining a natural language processing (NLP) metadata enrichment pipeline (e.g., sentiment analysis, named entity recognition) and running it against the MIND dataset [80].
我々は、自然言語処理（NLP）メタデータエンリッチメントパイプライン（例：感情分析、名前付き実体認識）を定義し、MINDデータセット[80]に対してそれを実行することにより、この定式化の有効性を実証している.
Figure 1 illustrates the operationalization.
図1はその運用を説明するもの.
The pipeline and the code produced for metadata enrichment and metric computation are available online.2 The goal of RADio is not to serve as thresholds or strict guidelines for “diverse recommendations,” but to provide developers of recommender systems with the tools to evaluate their systems on normative principles.
**RADioの目的**は、「多様な推薦」のための閾値や厳格なガイドラインとして機能することではなく、**推薦システムの開発者に規範的な原則に基づいてシステムを評価するためのツールを提供すること**である.

# 2. Related Work 関連作品

We first highlight recent work on the formal mathematical work on diversity in news recommendation, before citing related work on the normative aspect of diversity.
まず、ニュース推薦における多様性に関する形式的な数学的作業に関する最近の研究を紹介し、その後、多様性の規範的側面に関する関連研究を引用する.
Finally we describe the gap that exists between descriptive and normative diversity.3
最後に、記述的な多様性と規範的な多様性の間に存在するギャップについて述べる.

## 2.1. Descriptive (General-Purpose) Diversity Descriptive (汎用) 多様性

Diversity is a central concept in Information Retrieval literature [17, 62], albeit with a different interpretation than the normative diversity described in the previous section.
多様性は、前節で説明した規範的な多様性とは異なる解釈ではあるが、情報検索の文献[17, 62]では中心的な概念である.
During the development of news recommender systems, there is currently a large focus on the predictive power of an algorithm.
ニュース推薦システムの開発では、**現在、アルゴリズムの予測力に大きな焦点が当てられている**.
However, this may unduly promote content similar to what a user has interacted with before, and lock them in loops of “more of the same.”
しかし、これでは、**ユーザーが過去に接したことのあるコンテンツと類似したものを不当に促進し、"more of the same "のループにユーザーを閉じ込めてしまう可能性がある**.
To tackle this, “diversity” is introduced, which is typically defined as the “opposite of similarity” [11].
これに取り組むために，"**diversity**"が導入される．これは，典型的には"opposite of similarity"と定義される[11]．
Its goal is to prevent users from being shown the same type of items in their recommendations list and is often expressed as intra-list-diversity (ILD) [11, 13, 19, 23, 24, 38, 48, 70]: mean pairwise dissimilarity between recommended item lists.
その目的は、ユーザーが推薦リストで同じ種類のアイテムを表示されるのを防ぐことであり、しばしば **intra-list-diversity (ILD)** [11, 13, 19, 23, 24, 38, 48, 70]: 推薦アイテムリスト間の平均ペアワイズ非類似度として表現される.
ILD requires the specification of a distance function between lists, and thus leaves it up to interpretation as to what it means for two lists to be distant.
**ILDはリスト間の距離関数を指定する必要がある(=2つのアイテム間の距離を何らかの方法で定量化する必要がある?)**ため、2つのリストが離れていることの意味については解釈次第となる.
In theory, it could still be interpreted with a metric that accounts for the presence of different sources or viewpoints [25].
理論的には，異なる情報源や視点の存在を考慮した指標で解釈することも可能である[25]．
However, in practice, diversity is most often implemented as a descriptive distance metric such as cosine similarity between two bag-of-words models or word embeddings [43, 48].
しかし、実際には2つのbag-of-wordsモデルや単語埋め込みのcosine similarityのような記述的な距離指標として実装されることがほとんどである[43, 48].

Other popular “beyond-accuracy” metrics related to diversity are novelty (how different is this item from what the user has seen in the past), serendipity (is the user positively surprised by this item), and coverage (what percentage of articles are recommended to at least one user).
多様性に関連する他の人気のある **"beyond-accuracy(精度を超えた)"メトリクス** は、以下がある.

- **novelty(新規性)**（ユーザーが過去に見たものとこのアイテムがどれだけ違うか).
- **serendipity**（ユーザーがこのアイテムにポジティブに驚いたか).
- **coverage**（少なくとも1人のユーザーに推薦された記事の割合）.

These metrics can be taken into account at different points in the machine learning pipeline [43, 81].
これらの指標は、**機械学習パイプラインの異なるポイントで考慮(??)**することができる.

One can optimize for these descriptive notions of diversity (i) before training, by clustering users based on their profile diversity with JS divergence [27], (ii) directly at training time (e.g., for learning-to-rank [10, 13, 70], collaborative filtering [60], graphs [30, 59] or bandits [21, 84]), (iii) by re-ranking a recommendation set and balance diversity vs. relevance [16] or popularity vs. relevance [15], and (iv) by defining a post-recommendation metric to measure diversity for each recommendation set or at user-level (e.g., the generalist-specialist score [2, 73]).
このような多様性の概念は，学習パイプラインにおいて以下の**４つの時点**で対応する事が可能である.

- (i)学習前に，JS divergence [27]を用いてプロファイルの多様性に基づいてユーザーをクラスタリングする，
- (ii)学習時に直接最適化できる（例：learning-to-rank [10, 13, 70], collaborative filter [60], graph [30, 59] or bandits [21, 84]．また、
- (iii) 推薦セットの再ランク付けを行い、多様性と関連性のバランスをとる [16]、あるいは人気と関連性のバランスをとる [15] 、
- (iv) 推薦後の指標を定義し、推薦セットごとあるいはユーザ単位で多様性を測る（例：一般主義-専門主義スコア [2, 73]）

With any of these four methods, a trade-off must be made between the relevance of a recommendation issued to users and the level of descriptive diversity, though there have also been studies indicating that increasing diversity does not necessarily need to negatively affect relevance [48].
この4つの方法のいずれにおいても、ユーザに提示する推薦文の関連性とdescriptive diversity のレベルはトレードオフの関係にあるが、**多様性を高めることが必ずしも関連性に悪影響を与える必要はない**ことを示す研究もある[48]。
Nevertheless, this encouraged recent efforts in training neural-based recommenders that explicitly make a trade-off between accuracy and diversity [61].
しかし、近年では、**多様性と精度のトレードオフを明示的に行う**ニューラル・ベース・レコメンダーが注目されている[61].
Also recently, there have been studies that differentiate between diversity needs of users [83].
また、最近では、ユーザの多様性ニーズを区別する研究も行われている[83].

## 2.2. Normative Diversity Normative Diversity (規範的多様性)

Diversity is extensively discussed as a normative concept in literature, and has a role in many different areas of science [46, 65], spanning from ecological diversity to diversity as a proxy for fairness in machine learning systems [51].
多様性は規範的な概念として文献で広く議論されており、生態系の多様性から機械学習システムにおける公平性の代理としての多様性[51]まで、科学の多くの異なる分野で役割を担っている[46, 65].
While these interpretations of diversity are often related, they do not fully cover the nuances of a diverse news recommender system, the work on which stems from democratic theory and the role of media in society.
これらの多様性の解釈はしばしば関連しているが，民主主義理論や社会におけるメディアの役割に由来する，多様なニュース推薦システムのニュアンスを完全にカバーするものではない.
Following Helberger [33], we define a normatively diverse news recommendation as one that succeeds in informing the user and supports them in fulfilling their role in democratic society.
Helberger [33]に従い、我々は**規範的に多様なニュース推薦を、ユーザーに情報を提供することに成功し、民主主義社会における役割を果たすことを支援するもの**と定義する.
Out of the many theoretical models that exist in literature, Helberger [33] describes four different models from the normative framework of democracy, each with a different view on what it means to properly inform citizens:
文献に存在する多くの理論モデルのうち、Helberger [33]は、民主主義の規範的枠組みから**4つの異なるモデル**を説明し、それぞれ、市民に適切に情報を提供することの意味について異なる見解を示している.

- the Liberal model, which aims to enable personal development and autonomy,
- 自由主義モデル：個人の成長と自律を可能にすること、
- the Participatory model, which aims to enable users to fulfill their role as active citizens in a democratic society,
- 参加型モデル：民主主義社会における積極的な市民としての役割をユーザーが果たせるようにすること、
- the Deliberative model, which aims to foster discussion and debate by equally presenting different viewpoints and opinions in a rational and neutral way, and
- 審議型モデル：異なる視点や意見を合理的かつ中立的に平等に提示し、議論や討論を促すこと、
- the Critical model, which aims to challenge the status quo and to inspire the readers to take action against existing injustices in society.
- 批判モデル：現状に挑戦し、社会の既存の不公平に対して行動を起こすように読者を鼓舞することである。

For more details regarding the different models, and what a recommender system following each of these models would look like, we refer to Helberger [33].
各モデルの詳細や、**各モデルに従った推薦システムがどのようなものか**については、Helberger [33]を参照してください.
Which model is followed is a decision that needs to be made by the media organization itself, and should be in line with their norms and values.
**どのモデルに従うかは、報道機関自身が決定すべきこと**であり、その規範や価値観に沿ったものであるべきである.

Based on these models, the DART metrics [71] take a first step towards normative diversity for recommender systems and reflect the nuances of the different democratic models described above:
これらのモデルに基づいて、**DART Metrics** [71] は推薦システムのための規範的な多様性への第一歩を踏み出し、上述した異なる民主主義モデルのニュアンスを反映させたものである:

- Calibration
- Fragmentation
- Activation
- Representation
- Alternative Voices.

Table 1 provides an overview of the DART metrics and their expected value ranges for the different models, and will be further elaborated later in the paper.
表1は、DART Metricsの概要と、異なるモデルに対する期待値の範囲を示しており、この論文の後半でさらに詳しく説明する予定である.

## 2.3. The Gap Between Normative and Descriptive Diversity

The descriptive diversity metrics described in Section 2.1 are generalpurpose and meant to be applicable in all domains of recommendation.
セクション2.1で説明した **descriptive diversity metrics は汎用的であり、すべての推薦のドメインに適用できる**ことを意図している.
However, in their simplicity a large gap can be observed between this interpretation of diversity and the social sciences’ perspective on media diversity that is detailed in Section 2.2.
しかし、**その単純さゆえに、この多様性の解釈と、セクション2.2で詳述するメディアの多様性に関する社会科学の観点との間に大きなギャップが見られる**.
In their comprehensive work on the implementation of media diversity across different domains, Loecherbach et al. [46] note that there is “little to no overlap between concepts and operationalizations (of diversity) used in the different fields interested in media diversity.”
Loecherbachら[46]は、異なる領域にわたるメディアの多様性の実現に関する包括的な研究の中で、"メディアの多様性に関心を持つ異なる分野で使用される（多様性の）概念と運用の間にはほとんど重複がない"ことを指摘している.
As such, a recommendation that would score high on diversity according to traditional information retrieval-based metrics [17, 62], may not be considered to be diverse according to the criteria maintained by newsroom editors.
そのため、従来の情報検索に基づく評価基準[17, 62]では多様性で高得点を得られる推薦文も、ニュースルームの編集者が保持する基準では多様性があるとは見なされない可能性がある. (i.e. **diversityの評価方法がまちまちだって話!**)
Both Loecherbach et al. [46] and Bernstein et al. [7] call for truly interdisciplinary research in bridging this gap, where Bernstein et al. [7] argue for close collaboration between academia and industry and the foundation of joint labs.
Loecherbachら[46]とBernsteinら[7]は、このギャップを埋めるために真に学際的な研究を求めており、Bernsteinら[7]は、学術界と産業界の密接な協力と共同ラボの創設を主張している.
This work is a step in that direction, as we provide a versatile and mathematically grounded **rank-aware metric** that can be used by practitioners to monitor their normative goals.
この研究はその方向への一歩であり、我々は、**実務家が規範的目標を監視するために使用できる、汎用的で数学的根拠のある rank-aware metric**を提供するからである.

# 3. Operationalizing Normative Diversity for News Recommendation ニュース推薦のための規範的多様性の運用

With our RADio framework, we further refine the DART metrics that were defined by Vrijenhoek et al. [71] in order to resolve a number of the shortcomings of the metrics’ initial formalizations.
RADioフレームワークでは、Vrijenhoekら[71]が定義した**DARTメトリクスをさらに改良**し、metricsの初期形式化の欠点をいくつか解決している.
In their current form, each of the metrics has different value ranges; for example, Activation has a value range [−1, 1], where a higher score indicates a higher degree of activating content, and Calibration has a range of [0, ∞], where a lower score indicates a better Calibration.
例えば、Activationは[-1, 1]の値域を持ち、スコアが高いほど活性化するコンテンツの程度が高いことを示し、Calibrationは[0, ∞]の範囲を持っており、スコアが低いほどCalibrationが良いことを示している.
These different value ranges reduce the interpretability of the metrics, making them harder to explain and as such less likely to be adopted by news editors.
これらの異なる値域は、metricsの解釈可能性を低下させ、説明が難しくなり、その結果、ニュース編集者が採用する可能性が低くなる.
Furthermore, the proposed metrics do not take the position of an article in a recommendation into account.
さらに、提案されたmetricsは、**レコメンデーションにおける記事の位置を考慮に入れていない**.
News recommendations are ranked lists of articles that are typically presented to users in such a way that the likelihood of a recommended article to be considered by the user decreases further down the ranking.
ニュース推薦文は通常、推薦された記事がユーザーによって読まれる可能性がランキングの下方に行くほど低くなるようにランク付けされたリストである.
As such, in the evaluation of the diversity of the recommender system we should also account for the position of an article in the recommendation ranking, rather than considering the set as a whole (e.g. ILD).
そのため、レコメンデーションシステムの多様性を評価する際には、集合全体（ILDなど）を考慮するのではなく、**レコメンデーションランキングにおける記事の位置**も考慮する必要がある.

Thus, the two major challenges that we seek to address are that (i) scores should be comparable between the metrics and across recommendation systems, and (ii) scoring of both unranked and ranked sets of recommendations should be possible.
このように、我々は以下の二つの大きな課題を解決しようとするものである.

- (i) metrics間および推薦システム間でスコアが比較可能であること
- (ii) ランク付けされていない推薦セットとランク付けされた推薦セットの両方のスコアが可能であること.

In this section, we first detail these requirements (Section 3.1), then describe how we reformulate the metrics to each use the same divergence-based approach (Section 3.2).
本節では、まずこれらの要求を詳述し（セクション 3.1）、次にmetricをどのように再定式化し、それぞれが同じdivergence ベースのアプローチを用いるかを説明する（セクション 3.2）．
We then add the rank-aware aspect to the metrics (Section 3.3), before applying them to the five concrete DART metrics (Section 3.4).
そして、メトリクスにランクを意識した側面を追加し（セクション3.3）、それらを5つの具体的なDARTメトリクスに適用する（セクション3.4）.

## 3.1. Requirements 必要条件

We first enunciate the classical definition of a distance metric, before specifying three desirable metric criteria for news recommendations.
まず、**distance metric** の古典的な定義を明らかにした後、ニュース推薦に望ましい3つのmetricの基準を規定する.
Take a set $X$ of random variables and $x, y,z \in X$, then a metric $D$ is a proper distance measure if $D(x,y) = 0 <=> x =y, D(x,y) = D(y,x)$ and $D(x,y) \leq D(x,z) + D(z,y)$.
確率変数の集合$X$をとり、$x, y,z \in X$とすると、$D(x,y)=0 <=> x = y, D(x,y) = D(y,x)$ かつ $D(x,y) \leq D(x,z) + D(z,y)$ ならdistance measureが適切であると言える.

These are respectively the axioms of identity, symmetry and triangle inequality, that express intuitions about concepts of distance [56].
これらはそれぞれ、distanceの概念に関する直観を表す、同一性(identity)、対称性(symmetry)、三角形の不等式(triangle inequality)という公理である[56].

We add that our distance measure should (i) be bounded by [0; 1], for comparisons of different recommendation algorithms (ii) be unified, so as to fairly consider different diversity aspects (as opposed to e.g. using weighted averages or maxima in [18]) and (iii) allow for discrete rank-based distribution sets, to fit the ranked recommendation setting.
また、[18]での加重平均や最大値とは対照的に、(i)異なる推薦アルゴリズムの比較のために、[0; 1]で境界され、(ii)異なる多様性の側面を公正に考慮するために統一され、(iii) ランク付きの推薦設定に合うように、離散ランクベースの分布セットを可能にするべきであることを付け加える.

## 3.2. f-Divergence ♪ f-ダイバージェンス

We model the task of measuring diversity as a comparison between probability distributions: the difference in distribution between the issued recommendations (𝑄) and its context (𝑃).
**diversity を測定する作業は、確率分布の比較としてモデル化される**.
つまり、発行された推薦(Q)とそのcontext(P)の間の分布の違いである.
Each diversity metric prescribes its own 𝑄 and 𝑃.
各ダイバーシティ指標は独自の Qと P を規定する.
The elements in the distribution 𝑄 can be recommendation items (cf. Calibrated Recommendations [64]), but can also be higher-level concepts, such as distributions of topics and viewpoints.
分布Qの要素は推薦アイテム（cf. Calibrated Recommendations [64]）である場合もあるが、トピックや視点の分布など、より高いレベルの概念である場合もある.
The context 𝑃 may refer to either the overall supply of available items, the user profile, such as the reading history or explicitly stated preferences, or the recommendations that were issued to other users (see Figure 1).
context P は、利用可能なアイテムの全体的な供給量、読書履歴や明示的な好みなどのユーザープロファイル、他のユーザーに発行された推薦文のいずれかを参照することができる（図1参照）.
Intuitively, when 𝑃 is linked to the same user as 𝑄, we measure within user diversity (e.g., towards preventing getting locked in “filter bubbles”).
直感的には、Pが Q と同じユーザにリンクされている場合、ユーザ内の多様性を測定する（例えば、「フィルターバブル」に閉じ込められるのを防ぐために）.
When 𝑃 is linked to another user than 𝑄, we measure diversity across users (e.g., monitoring diversity of viewpoints represented across personalized homepages).
Pが Q 以外のユーザにリンクされている場合、ユーザ間の多様性を測定する（例えば、個人化されたホームページで表現される視点の多様性を監視する）.
In the following, we formalize the role of 𝑃 and 𝑄 in two different metric settings, starting with the simple and common KL divergence metric, before presenting its refinement (JensenShannon divergence) as our preferred metric.
以下では、P と Q の役割を、単純で一般的なKL divergence metric から始めて、その改良版（JensenShannonダイバージェンス）を我々の好ましいメトリックとして提示する2種類のmetric設定において正式に説明する.

### 3.2.1. Kullback-Leibler Divergence.

The concept of relative entropy or KL (Kullback–Leibler) divergence [42] between two probability mass functions P and Q (here, a recommendation and its context) is defined as:
2つの確率質量関数 Pと Q（ここではrecommendation と そのcontext）の間の相対entropyまたはKL（Kullback-Leibler）ダイバージェンス［42］の概念は次のように定義されている:

$$
D_{KL}(P, Q) = - \sum_{x\in X}{P(x)\log_{2}{Q(x)}}
+ \sum_{x\in X}{P(x)\log_{2}{P(x)}}
\tag{1}
$$

Often also expressed as $D_{KL}(𝑃, 𝑄) = 𝐻(𝑃, 𝑄)−𝐻(𝑃)$, with $𝐻(𝑃, 𝑄)$ the cross entropy of 𝑃 and 𝑄, and $𝐻(𝑃)$ the entropy of P.
しばしば、$D_{KL}(𝑄) = H(P,Q) - H(P)$とも表され、$H(P,Q)$はPとQとのクロスエントロピー、$H(P)$はPのエントロピーであるとする.
Both cross entropy and KL divergence can be thought of as measurements of how far the probability distribution 𝑄 is from the reference probability distribution 𝑃.
クロスエントロピーとKLダイバージェンスはともに、**確率分布 Q が参照確率分布P からどれだけ離れているか**を測定するものと考えることができる.
When $P = Q$, $D_{KL}(P, Q) = D_{KL}(P, P) = 0$, that identity property is not guaranteed by cross entropy alone.
P = Q$のとき、$D*{KL}(P, Q) = D*{KL}(P, P) = 0$となり、その同一性はクロスエントロピーだけでは保証されない.
This is the main reason to prefer KL divergence over cross entropy.
これが**クロスエントロピーよりもKLダイバージェンスを好む主な理由**である.
Though KL Divergence satisfies the identity requirement, the symmetry and triangle inequality are not fulfilled.
KL Divergence はidentityの要件を満たすが、symmetryとtriangle inequality は満たさない.
This can be resolved by further refining KL Divergence.
これは、KL Divergenceをさらに洗練させることで解決することができる.

### 3.2.2. Jensen–Shannon Divergence.

A succession of steps from KL divergence lead to Jensen-Shannon (JS) divergence.
KL divergence から段階を経て、**Jensen-Shannon (JS) divergence** に至る.
KL divergence was first turned symmetric [37] and then upper bounded [45], to lead to...
KLダイバージェンスはまず対称化され[37]、次に上界化され[45]、次のように導かれるようになった...

$$
D_{JS}(P, Q) = - \sum_{x\in X}\frac{P(x)+Q(x)}{2} \log_{2}{\frac{P(x)+Q(x)}{2}}
\\
+ \frac{1}{2} \sum_{x\in X}{P(x)\log_{2}{P(x)}}
+ \frac{1}{2} \sum_{x\in X}{Q(x)\log_{2}{Q(x)}}
\tag{2}
$$

When the base 2 logarithm is used, the JS divergence bounds are $0 \leq D_{JS}(P, Q) \leq 1$.
基底2対数を用いた場合、JS divergenceの境界は $0 \leq D_{JS}(P, Q) \leq 1$となる.
Additionally, Endres and Schindelin [26] show that $\sqrt{𝐷_{JS}}$ is a proper distance which fulfills the identity, symmetry and the triangle inequality properties.
またEndres and Schindelin [26]は、$\sqrt{D_{JS}}$がidentity、symmetry、triangle inequality の性質を満たす適切なdistance(=distance metric?)であることを示している.
When we refer to $𝐷_{JS}$ or $JS$ divergence below, we therefore implicitly refer to the square root of the JS formulation with log base 2.
以下、$D_{JS}$または JS Divergence と表記する場合、**log base 2**のJS定式化の平方根を暗黙に指すことになる.
Liese and Vajda [44] defined f-Divergence[$D_f$]: a generic formulation of several divergence metrics.
Liese and Vajda [44]は**f-Divergence**[$D_f$]を定義した：**いくつかの divergence metricsの一般的な定式化**である.
Among them are the JS and KL divergences.
Further along the text, we use $D_f$ as a shorthand notation for KL and JS divergences.
その中には、JS divergence とKL divergence がある. さらに本文では、**KL divergence とJS divergence の略記法として$D_f$を用いる**.
$D_f$ in discrete form is...
離散形式の$D_f$は...

$$
D_f(P,Q) = \sum_{x}{Q(x)f(\frac{P(x)}{Q(x)})}
\tag{3}
$$

where $f_{KL}(t) = t \log{t}$ and $f_{JS}(t) = \frac{1}{2}[(t+1)\log{\frac{2}{t+1}} +t \log{t}]$.
ここで、$f_{KL}(t) = t \log{t}$, $f_{JS}(t) = \frac{1}{2}[(t+1)\log{frac{2}{t+1}} +t \log{t}]$ とする.

To avoid misspecified metrics [64], we write $\bar{P}$ and $\bar{Q}$:
metricsの指定ミスを避けるため[64]、$bar{P}$, $bar{Q}$と表記する.

$$
\bar{Q}(x) = (1 - a)Q(x) + a P(x), \\
\bar{P}(x) = (1 - a)P(x) + a Q(x),
\tag{4}
$$

where a is a small number close to zero.
ここで、aはゼロに近い小さな数である.
$\bar{P}$ prevents artificially setting $D_f$ to zero when a category (e.g., a news topic) is represented in Q and not in P.
Qで表現され、Pで表現されないカテゴリ（例えば、ニューストピック）がある場合、$D_f$を人為的にゼロにすることを防ぐために$bar{P}$が使用される.
In the opposite case (when a category is represented in 𝑃 and not in 𝑄), $\bar{Q}$ avoids zero divisions.
逆の場合(あるカテゴリが𝑃で表され、𝑄で表されない場合)、$bar{Q}$はゼロ除算を避けることができる。
In order for the entire probabilistic distributions $\bar{P}$ and $\bar{Q}$ to remain proper statistical distributions, we normalize them to ensure $\sum_{x}\bar{P}(x) = \sum_{x}\bar{Q}(x) = 1$.
確率分布全体 $bar{P}$ と $tar{Q}$ が適切な統計分布であり続けるために、$Θsum_{x} Θbar{P}(x) = \sum_{x} Θbar{Q}(x) = 1$となるように正規化します。
To avoid notation congestion, 𝑃 and 𝑄 will implicitly refer to $\bar{P}$ and $\bar{Q}$, in the following sections.
表記の混雑を避けるため、以下の節では、𝑃と𝑄は暗黙に$Θbar{P}$と$Θbar{Q}$を指すことにする。

## 3.3. Rank-Aware f-Divergence Metrics 順位考慮型 f-ダイバージェンスメトリクス

Our ranked recommendation setting (characteristic (iii) above) motivates a further reformulation of our f-Divergence metric.
ランク付け推薦の設定（上記の特性(iii)）はf-Divergenceメトリクスの更なる再定式化を動機づける。
It is well entrenched in Learning To Rank (LTR) literature [67, 85], and by extension in conventional descriptive diversity metrics [13] that a user is a lot less likely to see items further down a recommended ranked list (i.e., diminishing inspection probabilities).
Learning To Rank (LTR) の文献 [67, 85]、ひいては従来の記述的多様性指標 [13]では、ユーザが推奨ランクリストのさらに下のアイテムを見る可能性はかなり低い（すなわち、検査確率が逓減する）ということがよく理解されています。
Note that the ranking oftentimes reflects relevance to the user, but it is not always the case for news (e.g., editorial layout of a news homepage).
また，ランキングはしばしばユーザとの関連性を反映するが，ニュースの場合は必ずしもそうではない（例えば，ニュースのホームページの編集レイアウト）ことに注意されたい．
We extend our metrics with an optional discount factor for 𝑃 and 𝑄 to weigh down the importance of results lower in the ranked recommendation list.
我々は、ランク付けされた推薦リストで下位の結果の重要性を重み付けするために、ᵄとᵄにオプションの割引係数を付けて我々のメトリックを拡張します。
The ranking relevancy metrics Mean Reciprocal Rank (MRR) and Normalized Discounted Cumulative Gain (NDCG) are popular rank-aware metrics for LTR [14, 36], in particular for news recommendation [80].
ランキング関連性指標であるMean Reciprocal Rank (MRR) と Normalized Discounted Cumulative Gain (NDCG) は，LTR [14, 36]，特にニュース推薦 [80] でよく用いられるランク考慮型指標である．
In line with the LTR literature, we first define the discrete probability distribution of a ranked recommendation set $𝑄^∗$ , given each item 𝑖 in the recommendation list 𝑅:
LTRの文献に沿って、まず、推薦リスト𝑅の各項目𝑖を与えて、ランク付けされた推薦セット$ᵄ^∗$の離散確率分布を定義する。

$$
\tag{5}
$$

where $𝑤_{𝑅𝑖}$ , the weight of a rank for item 𝑖, can be different depending on the discount form.
ここで、項目𝑖のランクの重み$𝑤_{ǔ𝑖}$は割引形式によって異なることがある。
For MMR, $𝑤_{𝑅𝑖} = \frac{1}{Ri}$ , for NDCG, $𝑤_{𝑅𝑖} =  \frac{1}{\log_2{Ri+1}}$ When $𝑤_{𝑅𝑖} = 1$, $𝑄^∗$ is not discounted (i.e., $𝑄^∗ = 𝑄$).
MMRの場合、$𝑤𝑖} = \frac{1}{Ri}$ 、NDCGの場合、$𝑤𝑖} = \frac{1}{log_2{Ri+1}$ $𝑅𝑖} = 1$ 時、$ᵄ^∗$は割引かれない（すなわち$ᵄ^∗ = 𝑄$）。

In news recommendation, the sparsity bias plays a predominant role: users will interact with a small fraction of a large item collection, such as scrollable news recommendation websites [40].
ニュース推薦では，スパース性バイアスが支配的な役割を果たす．スクロール可能なニュース推薦ウェブサイト[40]のように，ユーザーは大きなアイテムコレクションのごく一部とインタラクションする．
We thus opt for weighing based on MRR rather than NDCG, because it applies a heavier discount along the ranking than NDCG.
そのため，NDCGよりもMRRに基づく重み付けを選択する。これは，NDCGよりもランキングに沿ってより重い割引を適用するためである。
Note that the latter is said to be more suited for query-related rankings, where the user has a particular information need related to a query and thus higher propensity to scroll down a page [14].
後者は、ユーザーがクエリに関連した特定の情報ニーズを持っており、したがってページをスクロールする傾向がより高い、クエリ関連のランキングに適していると言われていることに注意してください[14]。

The context distribution 𝑃 is discounted in the same manner, when it is a ranked recommendation list.
コンテキスト分布 ᵄ は、ランク付けされた推薦リストである場合、同じように割り引かれる。
When 𝑃 is a user’s reading history (see Figure 1), the discount on 𝑃 increases with time: articles read recently are weighted higher than articles read longer ago.
𝑃がユーザーの読書履歴の場合（図1参照）、𝑃の割引率は時間と共に増加する：最近読んだ記事は、より昔に読んだ記事より高く評価される。
There are situations when rank-awareness is not applicable, for example when 𝑃 is the entire pool of available articles.5 With rankaware $𝑄^∗$ and optionally rank-aware $𝑃^∗$ , we formulate RADio, our rank-aware f-Divergence metric:
ランクを考慮した$ᵄ^∗$と任意でランクを考慮した$𝑃^∗$で、ランクを考慮したf-DivergenceメトリックであるRADioを定式化する。

$$
\tag{6}
$$

$𝑄^∗(𝑥)$ and $𝑃^∗(𝑥)$ accommodate for multiple situations: for example, $𝑄^∗(𝑐
𝑅)$ is the rank-aware distribution of news categories 𝑐 over the recommendation set 𝑅. In the following, we specify $𝑃^∗(𝑥

## 3.4. Normative Diversity metrics as Rank-Aware f-Divergences 順位を考慮したf-Divergencesとしての規範的な多様性メトリクス

In this section, we describe the RADio formalization of the general f-Divergence formulation above to the five DART metrics.
このセクションでは、上記の一般的なf-Divergenceの定式化を5つのDARTメトリクスにRADioで定式化したものについて説明する。
We leave the exact implementation of the metrics in practice for a particular open news recommendation dataset to the next section.
特定のオープンなニュース推薦データセットに対する実際のメトリクスの正確な実装は次のセクションに譲ります。
More formally, we define the following global parameters:
より正式には、以下のグローバルパラメータを定義する。

- 𝑆: The list of news articles the recommender system could make its selection from, also referred to as the “supply.” 𝑆: レコメンダーシステムが選択しうるニュース記事のリストで、"供給 "とも呼ばれる。

- 𝑅: The ranked list of articles in the recommendation set. 𝑅: 推薦セットに含まれる記事のランク付けされたリスト。

- 𝐻: The list of articles in a user’s reading history, ranked by recency. 𝐻: ユーザーの読書履歴にある記事のリストで、新着順に表示されます。

$𝑅_{i}^u \in {1, 2, 3, \cdots}$ refers to the rank of an item 𝑖 in a ranked list of recommendations for user 𝑢.
𝑅\_{i}^u \in {1, 2, 3, \cdots}$ は、ユーザー𝑢に対する推奨リストにおけるアイテム 𝑖のランクを意味する。
In this work, metrics are defined for a specific user at a certain point in time, therefore 𝑅 implicitly refers to $𝑅^𝑢$, unless stated otherwise.
この作業では、メトリックはある時点の特定のユーザーに対して定義されるため、特に断らない限り、𝑅は暗黙的に$𝑢$を意味する。
While this section contains some contextualization of the DART metrics [71], the original paper contains further normative justifications.
このセクションはDARTメトリクス[71]の文脈を含んでいますが、元の論文はさらに規範的な正当性を含んでいます。

### 3.4.1. Calibration. キャリブレーションを行います。

(Equation 7) measures to what extent the recommendations are tailored to a user’s preferences. The user’s preferences are deduced from their reading history (𝐻). Calibration can have two aspects: the divergence of the recommended articles’ categories and complexity. The former is expected to be extracted from news metadata and thus categorical by nature, the latter is a binned (categorical) probabilistic measure extracted via a language model. As such, we compare $𝑃^∗(𝑐
𝐻)$, the rank-aware distribution of categories or complexity score bins 𝑐 over the users’ reading history, and $𝑄^∗(𝑐

### 3.4.2. Fragmentation. フラグメンテーション

(Equation 8) reflects to what extent we can speak of a common public sphere, or whether the users exist in their own bubble. We measure Fragmentation as the divergence between every pair of users’ recommendations. Here we consider$ 𝑃^∗(𝑒
𝑅^𝑢)$ as the rank-aware distribution of news events 𝑒 over the recommendations 𝑅 for user 𝑢, and $𝑄^∗(𝑒

### 3.4.3. Activation. アクティベーション

(Equation 9) Most off-the-shelf sentiment analysis tools analyze a text, and return a value (0, 1] when the text expresses a positive emotion, a value [−1, 0) when the expressed sentiment is negative, and 0 if it is completely neutral. The more extreme the value, the stronger the expressed sentiment is. As proposed in [71], we use an article’s absolute sentiment score as an approximation to determine the height of the emotion and therefore the level of Activation expressed in a single article. This then yields a continuous value between 0 and 1. $𝑃(𝑘
𝑆)$ denotes the distribution of (binned) article Activation score 𝑘 within the pool of items that were available at that point (𝑆). $𝑄^∗(𝑘

### 3.4.4. Representation. 表現

(Equation 10) aims to approximate a notion of viewpoint diversity (e.g. mentions of political topics or political parties), where the viewpoints are expressed categorically. Here 𝑝 refers to the presence of a particular viewpoint, and $𝑃(𝑝
𝑆)$ is the distribution of these viewpoints within the overall pool of articles, while $𝑄^∗(𝑝

### 3.4.5. Alternative Voices. オルタナティブ・ヴォイス

(Equation 11) is related to the Representation metric in the sense that it also aims to reflect an aspect of viewpoint diversity.
(式11）は、視点の多様性の一面を反映させるという意味で、Representation指標と関連している。
Rather than focusing on the content of the viewpoint, it focuses on the viewpoint holder, and specifically whether they belong to a “protected group” or not.
これは、視点の内容ではなく、視点の持ち主、特に「保護された集団」に属しているか否かに着目したものである。
Examples of such protected
保護された集団の例

$$
\tag{11}
$$

# 4. Experimental Setup 実験セットアップ

TUP In order to demonstrate RADio’s potential effectiveness, we developed an NLP pipeline to retrieve input features to the metrics in Section 3.4 and ran them on a public dataset.
TUP RADioの潜在的な有効性を実証するために、我々はセクション3.4のメトリクスへの入力特徴を取得するNLPパイプラインを開発し、公開データセットで実行した。
It should be noted that this pipeline is an imperfect approximation, and that each metric individually would benefit from more sophisticated methods.
このパイプラインは不完全な近似であり、各メトリクスは個々に、より洗練された手法から利益を得ることができることに留意する必要がある。
The MIND dataset [80] contains the interactions of 1 million randomly sampled and anonymized users with the news items on MSN News between October 12 and November 22 2019.
MINDデータセット[80]には、2019年10月12日から11月22日の間にMSNニュースのニュース項目と、ランダムにサンプリングされ匿名化された100万人のユーザーとのインタラクションが含まれています。
Each interaction contains an impression log, listing which articles were presented to the user, which were clicked on and the user’s reading history.
各インタラクションには、どの記事がユーザーに提示され、どれがクリックされたか、ユーザーの読書履歴をリスト化したインプレッションログが含まれています。
The MIND dataset was published accompanied by a performance comparison on news recommender algorithms trained on this dataset,8 including news-specific neural recommendation methods NPA [78], NAML [77], LSTUR [1] and NRMS [79].
MINDデータセットは、このデータセットで学習されたニュース推薦アルゴリズムに関する性能比較8を伴って公開され、その中にはニュース専用のニューラル推薦手法NPA [78]、NAML [77]、LSTUR [1] およびNRMS [79]が含まれています。
It was shown that these algorithms outperform general-purpose ones [80] or common collaborative filtering models (such as alternating least squares (ALS)), in particular due to the short lifespan of news items [31].
これらのアルゴリズムは，特にニュースアイテムの寿命が短いことから，汎用的なもの [80] や一般的な協調フィルタリングモデル（交互最小二乗法 (ALS) など）よりも優れていることが示されています [31]．また，ニュースアイテムの寿命が短いことから，これらのアルゴリズムは，一般的なものよりも優れていることが示されています．
These algorithms are trained on the impression logs in order to predict which items the users are most likely to click on.
これらのアルゴリズムは、ユーザがどのアイテムをクリックする可能性が高いかを予測するために、インプレッション・ログに対して学習されます。
For the purpose of this paper we will evaluate these neural recommendation methods with the RADio framework (on the DART metrics) and compare their performance with two naive baseline methods, based on a reasonable set of candidates (the original impression log): a random selection, and a selection of the most popular items, where the popularity of the item is approximated by the number of recorded clicks in the dataset.
この論文では、RADioフレームワークでこれらのニューラル・レコメンデーション手法を評価し（DARTメトリクスで）、妥当な候補の集合（元のインプレッションログ）に基づく2つのナイーブなベースライン手法とそのパフォーマンスを比較します：ランダム選択と、アイテムの人気度がデータセットで記録されたクリック数で近似される最も人気のあるアイテムを選択する方法です。

Since RADio computes the average of all {𝑃, 𝑄} pairs, we retrieve confidence intervals over paired distances too, as illustrated in the sensitivity analyses below.
RADioはすべての{u_1D443}のペアの平均を計算するので、以下の感度分析で示されるように、我々はペアの距離に対する信頼区間も取得します。
In a traditional model evaluation setting, it would be desirable to generate confidence intervals via different model seeds or cross-validation splits.
伝統的なモデル評価の設定では、異なるモデルシードまたはクロスバリデーション分割によって信頼区間を生成することが望ましいと思われる。
We refrain from doing this for our metric evaluation as this would introduce a multidimensional confidence interval (e.g., over {𝑃, 𝑄} pairs and over model seeds).
これは多次元信頼区間（例えば、{u, 𝑃のペアとモデルシード以上）を導入するので、我々のメトリック評価のためにこれを行うことを控える。）
We scrape articles via the URLs provided in the MIND dataset.
MINDデータセットで提供されるURLを介して記事をスクレイピングする。
Each article’s metadata is enriched with five methods:
各記事のメタデータは5つのメソッドでエンリッチされている。

(1) Complexity analysis:
(1)複雑さ分析。
Each item is assigned a complexity score based on the Flesch-Kincaid reading ease test [41], implemented in the Python module py-readability-metrics [20].
各項目はPythonモジュールpy-readability-metrics [20]で実装されたFlesch-Kincaid read ease test [41]に基づいて複雑さのスコアを割り当てられる。
Complexity is then discretized into bins, to accommodate for the discrete form of $𝐷^*_f$.
その後、$𝐷^*_f$の離散形式を考慮し、複雑度をビンに離散化する。

(2) Story clustering:
(2) ストーリーのクラスタリング
The individual news items are clustered into so-called news story chains, which means that stories about the same event will be grouped together.
個々のニュース項目はいわゆるニュースストーリーチェーンにクラスタリングされる。つまり、同じ出来事に関するストーリーはグループ化されることになる。
This way, we add a level of analysis between individual news items and higher level categories (see Section 3.4).
このようにして，個々のニュース項目と上位カテゴリとの間に分析レベルを追加する（セクション3.4参照）．
We use a TF-IDF based unsupervised clustering algorithm based on cosine similarity and a three days moving window, following the setup of Trilling and van Hoof [69].
我々はTrilling and van Hoof [69]の設定に従って、コサイン類似度と3日間の移動窓に基づいて、TF-IDFベースの教師なしクラスタリングアルゴリズムを使用しています。

(3) Sentiment analysis:
(3) センチメント分析。
Using the textBlob open source NLP library we assign each article a sentiment polarity score [47].
オープンソースのNLPライブラリtextBlobを使用して、各記事にセンチメント極性スコア[47]を割り当てます。
Our focus is on the relative neutrality of articles, we thus take the absolute value of the negative
我々は記事の相対的な中立性に着目しているため、ネガティブな記事の絶対値を取る。

(4) Named entity recognition:
(4)名前付き実体の認識
Using spaCy, we identify the people, organizations and locations mentioned in the text [34], and count their frequency.
spaCyを用いて、テキストに記載されている人物、組織、場所を特定し[34]、その頻度をカウントする。

(5) Named entity augmentation:
(5）名前付きエンティティの増強。
For the entities identified in the text in the previous step, we attempt to link them to their Wikidata9 entry through fuzzy name matching, to figure out if they are politicians, or in the case of organizations, political parties.10
前のステップでテキストから特定されたエンティティについて、ファジー名照合により、そのエンティ ティを Wikidata9 のエントリにリンクし、それらが政治家かどうか、組織の場合は政党かどうかを判 断しようとする10。

We implement RADio with the pipeline above.
上記のようなパイプラインでRADioを実装します。
Table 2 links the numbered list above with the DART metrics.
表2は、上記の番号付きリストとDARTメトリクスをリンクさせたものです。
It provides an overview of the different metrics and their respective context distribution 𝑃 over normative concepts.
これは、異なるメトリクスと、規範的な概念に対するそれぞれの文脈分布ᵄの概要を提供するものである。
The code for this implementation is available online.11
この実装のコードはオンラインで入手可能である11。

We evaluate the outcome of our RADio framework for different recommender strategies (LSTUR, NAML, NPA, NRMS, most popular and random), with both KL Divergence and Jensen-Shannon as divergence metrics, with and without discounting for the position in the recommendation and at different ranking cutoffs.
我々は、異なる推薦戦略（LSTUR、NAML、NPA、NRMS、最も人気のある、ランダム）に対して、KL DivergenceとJensen-Shannonの両方をダイバージェンスメトリクスとして、推薦における位置に対する割引の有無、異なるランキングカットオフでRADioフレームワークの結果を評価した。

# 5. Results 結果

Having described our methodology and experimental setup around the operationalization of DART metrics, we analyze the results of the experiments on MIND.
DARTメトリクスの運用にまつわる我々の方法論と実験セットアップを説明した後、MINDでの実験結果を分析する。
We separate descriptive analysis of the results in Section 5 from the interpretation of normative interpretation of the metrics in Section 6.
セクション5での結果の記述的分析と、セクション6でのメトリクスの規範的な解釈を分けて説明します。
We choose to implement RADio with rank-awareness and JS divergence with a rank cutoff @N (the entire ranking list) as our default.
我々は、ランクを意識したRADioの実装と、ランクカットオフ@N（ランキングリスト全体）をデフォルトとしたJSダイバージェンスを選択しました。
After commenting on the overall results, we further motivate that choice with a sensitivity analysis to different hyperparameters.
全体的な結果についてコメントした後、異なるハイパーパラメータに対する感度分析を行い、この選択の動機付けをさらに行う。
We alter the divergence metric (KL or JS), rank-awareness (with and without a discount) and ranking cutoffs ($@n, with 𝑛 = 1, 2, 5, 10, 20, 𝑁$) for the different recommender models.
我々は、異なるレコメンダーモデルについて、ダイバージェンスメトリック（KLまたはJS）、ランク認識（割引あり・なし）、ランキングカットオフ（$@n、𝑛 = 1, 2, 5, 10, 20, 𝑁$）を変更した。

Table 3 displays results for RADio with rank-aware JS divergence.12 Higher values imply higher divergence scores, but whether high or low divergence is desired depends on the goal of the recommender system, which we will further elaborate in Section 6.
表 3 は、RADIO がランクを意識した JS ダイバージェンスを行った結果を示している。12 値が高いほどダイバージェンススコアが高いことを意味するが、ダイバージェンスが高いか低いかは、推薦システムの目標に依存する（セクション 6 でさらに詳しく説明する）。
The random recommender scores highest on divergence for all metrics and is also one of the least relevant by definition (see NDCG score).
ランダム・レコメンダーはすべての指標でダイバージェンス のスコアが最も高く、また定義上最も関連性の低いレコメン ダーである（NDCG スコア参照）。
Most popular and random have comparable NDCG results.
最も人気のあるレコメンダーとランダムの NDCG スコアは同程度である。
Popularity scores for the articles are derived from the clicks recorded in the MIND interaction logs, and many articles have zero or only one click recorded.
記事の人気度スコアはMINDのインタラクションログに記録されたクリック数から導かれ、多くの記事はゼロか1クリックしか記録されていません。
When the candidate list contains exclusively articles with a similar number of clicks this forces the most popular recommender to a random choice, which explains the artificial similarity between most popular and random in terms of the NDCG score.
候補リストに同程度のクリック数の記事しか含まれていない場合、最も人気のあるレコメンダーはランダムな選択を余儀なくされるため、NDCGスコアの観点から見ると、最も人気のあるものとランダムなものの間に人工的な類似性があることを説明しています。
Between the neural recommenders, most scores for LSTUR, NPA, NRMS and NAML are in lower ranges.
ニューラルレコメンダーのうち、LSTUR、NPA、NRMS、NAMLのスコアはほとんどが低い範囲にある。
Note that they produce similar recommendations (see NDCG values and Wu et al. [80]).
これらは類似のレコメンデーションを生成することに注意する（NDCG値およびWuら[80]を参照）。
Some notable differences can be observed when comparing these neural methods to the baselines.
これらのニューラルメソッドをベースラインと比較すると、いくつかの顕著な違いが観察される。
For example, we see that the neural recommenders are more Calibrated to the items present in people’s reading history, though the most popular baseline performs marginally better in terms of Calibration of complexity.
例えば、最も人気のあるベースラインは複雑さのCalibrationという点ではわずかに優れているが、ニューラル・リコメンダーは人々の読書履歴に存在するアイテムに対してよりCalibrationされていることが分かる。
In the following, we further analyse the entire distribution of individual recommendation list divergences and test the sensitivity of RADio to different settings.
以下では、さらに個々の推薦リストの発散の分布全体を分析し、異なる設定に対するRADioの感度をテストします。
Boxplots for all metrics and all recommender strategies are available in the online repository, where we highlight the importance of rank-awareness.
すべてのメトリックとすべてのレコメンダー戦略の箱ひげ図はオンラインリポジトリで入手可能であり、ランク意識の重要性を強調しています。

## 5.1. Sensitivityto the Divergence Metric ♪ 発散メトリックへの感度

JS divergence is our preferred implementation of universal diversity metrics.
JSダイバージェンスは我々が推奨する普遍的多様性メトリクスの実装である。
It is a proper distance metric and bounded between 0 and 1 (see Section 3.2).
これは適切な距離指標であり、0と1の間で境界が設定されています（セクション3.2参照）。
Figure 2 substantiates that claim empirically, visualizing the sensitivity of RADio to the two described f-Divergence metrics:
図2はその主張を実証的に示しており、2つのfダイバージェンスメトリクスに対するRADioの感度を可視化したものである。
KL and JS Divergence.
KLダイバージェンスとJSダイバージェンスです。
Clear differences can be observed in the distributions; KL divergence is skewed towards lower divergence, while JS divergence yields a more centered distribution of values.
KLダイバージェンスは低ダイバージェンスに偏り、JSダイバージェンスはより中心的な分布を示しています。
Additionally, JS divergence applies more contrast between the neural recommender systems and the naive recommendation methods and especially the random baseline.
さらに、JSダイバージェンスは、ニューラル推薦システムとナイーブ推薦手法、特にランダムベースラインとの間に、より多くのコントラストを適用しています。
Due to the large sample in MIND, the random baseline is an approximation of a diverse recommendation set, given the candidate articles.
MINDではサンプルが多いため、ランダムベースラインは候補記事があれば、多様な推薦セットの近似となる。
In certain cases KL introduces consequential skew in the distribution of individual 𝑃,𝑄 comparison pairs across recommendation models; this does not occur to that extent with JS.
KLは推薦モデル間で個々のᵄ,ᵄ比較ペアの分布に結果的に歪みをもたらす場合があるが、JSではそのようなことはない。
Although KL Divergence is a well-known metric that can be found in many applications and is simpler to express mathematically, we found the JS divergence to be a better fit both theoretically and empirically.
KLダイバージェンスは多くのアプリケーションで見られる有名な指標であり、数学的に表現するのも簡単であるが、我々はJSダイバージェンスが理論的にも経験的にもより適合していることを発見した。

## 5.2. Sensitivity to Rank-awareness ランク認識への感度

In the original formulation of DART metrics [71], rank-awareness was not considered for most of the defined metrics.
DARTメトリクスのオリジナルの定式化[71]では、定義されたメトリクスのほとんどについて、ランクを意識していませんでした。
In our formalization, rank-awareness is the default.
我々の定式化では、ランクアウェアネスがデフォルトである。
In Figure 3, we visualize the effect of removing the rank-awareness (in blue) on Fragmentation and compare to the original rank-aware Fragmentation (in orange).
図3では、Fragmentationにおけるランク考慮の削除の効果（青）と、元のランク考慮Fragmentation（オレンジ）の比較を可視化しています。
Rank-awareness allows for better differentiation between methods:
ランクを意識することで、手法間の区別がより明確になる。
LSTUR and “most popular” seem to be similarly distributed without a rank discount.
LSTURと "最も人気のある "手法は、ランク割引を行わなくても同じように分布しているように見える。
Introducing rank-awareness shifts LSTUR towards a larger divergence, whereas “most popular” remains largely the same.
ランクを意識することで、LSTURはより大きな乖離にシフトするが、"一番人気 "はほとんど変わらない。

## 5.3. Sensitivity @n 感性@n

One could also consider adding a cut-off point where only the top 𝑛 recommendations are considered for evaluation, the results of which are shown in Figure 4.
また、上位𝑛個のレコメンデーションのみを評価対象とするカットオフポイントを追加することも考えられるが、その結果は図4に示すとおりである。
The figure shows that the effect of rank-awareness becomes stronger with a higher cut-off point, and causes the divergence score to stabilize after roughly 10 recommendations.
この図から、ランク意識の効果はカットオフポイントが高いほど強くなり、およそ10個のレコメンデーションで乖離スコアが安定することがわかる。
This is because our MMR rank-awareness strongly discounts values further down the ranking.
これは、MMRのランク意識がランキングのさらに下位の値を強く割り引くためである。
@20 and @N (no cutoff) are similar for all metrics because MIND rarely contains more than 20 recommendation candidates.
20と@N（カットオフなし）は、MINDが20以上の推薦候補を含むことはほとんどないため、すべてのメトリクスで同様な結果が得られます。
Note that when calculating the divergence score for Activation, Representation or Alternative Voices without rank-awareness and without cutoff point, there is no divergence to be reported as recommendation and target distribution are identical in these cases.13
なお、ランクを意識せず、カットオフポイントを設けず、Activation、Representation、Alternative Voicesの発散スコアを計算した場合、推薦と目標分布が同一であるため、報告される発散はない13。

## 5.4. Normative Evaluation #規範的評価

By comparing divergence scores across different recommender strategies, we can draw conclusions on the way they influence exposure of news to users.
異なるレコメンダー戦略のダイバージェンススコアを比較することで、ユーザーへのニュースの露出に影響を与える方法について結論を導き出すことができる。
This is especially the case when comparing neural methods to the random recommender, which should reflect the characteristics of the overall pool of data.
これは特にニューラル手法をランダムレコメンダーと比較する場合に顕著であり、データプール全体の特性を反映するはずである。
Combining this with DART’s different theoretical models of democracy (summarized in Table 1), one can make informed decisions on which recommender system is better suited to one’s normative stance than others.
これをDARTの民主主義に関するさまざまな理論モデル（表1にまとめた）と組み合わせることで、どのレコメンダーシステムが他よりも自分の規範的スタンスに適しているか、情報に基づいた判断ができるようになります。
Imagine, for example, a public service media organization that aims to reflect Participatory norms and values in their recommendations.
例えば、参加型規範と価値をレコメンデーションに反映させることを目指す公共サービスメディア機関を想像してください。
The Participatory model prescribes low Fragmentation and low Activation, which is shown in the scores of the neural recommenders.
Participatoryモデルは低Fragmentationと低Activationを規定し、それはニューラル・レコメンダーのスコアに示されます。
This would indicate that those models are more suitable for this organization’s goals.
これは、それらのモデルがこの組織の目標により適していることを示すものだろう。
In comparison, imagine a large media organization that wants to dedicate a small section of their website to Critical principles, consisting of one element with recommendations called “A different perspective.”
これと比較して、ウェブサイトの小さなセクションをCriticalの原則に充てたいと考えている大規模なメディア組織を想像してみましょう。"A different perspective "というレコメンデーションを持つ1つの要素で構成されています。
The Critical model calls for a high divergence score in both Representation and Alternative Voices.
Critical モデルでは、Representation と Alternative Voices の両方で高い発散スコアを要求しています。
Given that the random recommender scores best according to these principles, the neural recommenders would not be very suitable for this goal.
これらの原則に従ってランダムレコメンダーが最も良いスコアを出すことを考えると、ニューラルレコメンダーはこの目標にはあまり適さないでしょう。
Nevertheless, the conclusion that a random recommender is suitable for Critical norms and values is moot.
とはいえ、ランダムレコメンダーがCriticalな規範や価値観に適しているという結論はムリです。
Additional steps should be taken to further improve upon these scores: recommendation algorithm developers could tweak the trade-off between different target values in the recommendation, or even explicitly optimize on these metrics.
レコメンデーションアルゴリズムの開発者は、レコメンデーションにおける異なる目標値間のトレードオフを微調整したり、あるいはこれらの指標を明示的に最適化したりすることができるだろう。

# 6. Discussion ディスカッション

Choosing an f-Divergence score as the base for our metrics allows us to construct a single base formalization with a clear interpretation amongst all metrics; when the value is 0, the distribution between the recommendations and the chosen context is identical.
f-Divergenceスコアを測定基準のベースとして選択することで、すべての測定基準の間で明確な解釈を持つ単一のベース形式を構築することができます。値が0の場合、推奨と選択したコンテキスト間の分布は同一となります。
The larger the measurements, the larger the divergence is.
測定値が大きくなればなるほど、乖離は大きくなります。
However, it also comes with a number of limitations.
しかし、これにはいくつかの制約もある。
For one, f-Divergence does not take the relations between categorical values into account, and the ordering of the categorical values in the input vector is arbitrary.
ひとつは、f-Divergenceはカテゴリ値間の関係を考慮しておらず、入力ベクトルにおけるカテゴリ値の順序は任意であることである。
For example, two left-wing political parties in the Representation metric may be more similar than an extremely left-wing and an extremely right-wing party, but this is currently not taken into account.
例えば、Representation メトリクスの2つの左翼政党は、極端な左翼政党と極端な右翼政党よりも類似しているかもしれないが、現状ではこの点は考慮されていない。
Related to this, in order to make continuous values suitable for our general discrete definition of f-Divergence, they need to be discretized into arbitrarily defined bins.
これに関連して、連続値を我々の一般的なf-Divergenceの離散的定義に適合させるためには、それらを任意に定義されたビンに離散化する必要がある。
This means that two very similar values may end up in different binsFuture work may propose a different approach for calculating divergence between continuous variables.
このことは、非常に似た2つの値が異なるビンに入る可能性があることを意味する。将来的には、連続変数間のダイバージェンスを計算するための異なるアプローチを提案する可能性がある。
Regarding the data enrichment pipeline, we identify a number of enhancement points.
データエンリッチメントパイプラインについては、いくつかの強化ポイントがあることがわかった。
While some metrics, such as topic Calibration, work with simple data on news topics that is often directly available in a dataset, other metrics require a more sophisticated data enrichment pipeline.
トピックキャリブレーションなどのいくつかのメトリクスは、しばしばデータセットで直接利用可能なニューストピックに関する単純なデータで動作するが、他のメトリクスはより洗練されたデータエンリッチメントパイプラインを必要とする。
The differences in these approaches appear in the results: the metrics with more trivial metadata retrieval setups show clear and distinct patterns for different recommender algorithms, but this is not the case for the more complicated ones.
これらのアプローチの違いは結果にも現れている。より些細なメタデータ検索設定を用いたメトリクスは、異なるレコメンダーアルゴリズムに対して明確で異なるパターンを示すが、より複雑なものについてはそうではない。
Furthermore, it is not possible to determine the quality of the pipeline, as we do not have a ground truth for evaluation.
さらに、評価のためのグランドトゥルースを持っていないため、パイプラインの品質を決定することはできない。
For future work, we suggest to take the base formalizations as constructed in this paper as a starting point, and work to improve the extraction of the relevant parameters for metrics such as Representation, Alternative Voices and Activation.
今後の課題としては、本論文で構築した基本的な形式化を出発点として、Representation、Alternative Voices、Activationといったメトリクスに関連するパラメータの抽出を改善する作業を行うことを提案する。
Especially for the first two, there is already a large body of work that can facilitate this process [3, 22].
特に、最初の2つについては、このプロセスを促進するための大規模な作業がすでに存在します[3, 22]。
Human evaluation, including the input from editorial teams, would then be a promising way to evaluate these three normative metrics, similar to the work in the context of language generation bias [18].
編集チームからのインプットを含む人間による評価は、言語生成バイアスの文脈における作業と同様に、これら3つの規範的なメトリクスを評価する有望な方法となるでしょう[18]。
Additionally, more insight needs to be gained on the influence of the choice of dataset.
さらに、データセットの選択の影響について、より多くの洞察を得る必要があります。
The MIND dataset contains a significant amount of so-called soft news, including articles on lifestyle, sport and entertainment, whereas the DART metrics are mostly applicable to hard news.
MINDデータセットには、ライフスタイル、スポーツ、エンターテイメントに関する記事など、いわゆるソフトニュースが大量に含まれていますが、DARTメトリクスはハードニュースにほとんど適用されます。
The influence of the chosen dataset needs to be investigated in more detail, which can then lead to more informed decision-making on the trade-off between diversity and click-through rate, and what can reasonably be expected of a news recommender system.
その結果、多様性とクリックスルー率のトレードオフや、ニュース推薦システムに期待される合理性について、より詳細な情報を得た上での意思決定につながるでしょう。

# 7. Conclusion 結論

In this paper we have made a first attempt at constructing and implementing new evaluation criteria for news recommender systems, with a foundation in normative theory.
本論文では、規範理論を基礎とした、ニュース推薦システムの新しい評価基準の構築と実装を初めて試みた。
Based on the DART metrics, first theoretically conceptualized in earlier work, we propose to look at diversity as a divergence score, observing differences between the issued recommendations and a metric-specific target distribution.
先行研究で初めて理論的に概念化されたDARTメトリクスをベースに、発行された推薦文とメトリクス固有の目標分布との差異を観察し、ダイバージェンススコアとして多様性を見ることを提案する。
We proposed RADio, a unified rank-aware f-Divergence metric framework that is mathematically grounded and that fits several possible use cases within the original DART metrics and we hope beyond in future work.
このフレームワークは数学的な根拠があり、元のDARTメトリクスのいくつかの可能なユースケースに適合し、将来の研究においてそれを超えることを期待している。
We showed that JS divergence was preferred over other divergence metrics.
我々は、JSダイバージェンスが他のダイバージェンスメトリクスよりも好ましいことを示した。
At first mathematically, as JS is a proper distance metric, and empirically, via a sensitivity analysis to different cutoff, rank-awareness and divergence metric regimes.
まず数学的に、JSは適切な距離指標であること、そして経験的に、異なるカットオフ、ランク認識、ダイバージェンス指標のレジームに対する感度分析を通じて、JSダイバージェンスが他のダイバージェンスメトリクスよりも好ましいことを示した。
When our approach is adopted in practice, it enables the evaluation of news recommender systems on normative principles beyond user relevance.
我々のアプローチが実際に採用された場合、ユーザーとの関連性を超えた規範的な原則に基づいてニュース推薦システムを評価することが可能となる。
Finally, we wish to emphasize that the metrics proposed are meant to supplement standard recommender system evaluation metrics, in the same way that current beyond-accuracy metrics do.
最後に、提案する評価指標は、現在の精度を超えた評価指標がそうであるように、標準的な推薦システム評価指標を補完するものであることを強調したいと思います。
Most importantly, they are meant to bridge the gap between different disciplines involved in the process of news recommendation and to support more informed discussion between them.
また、最も重要なことは、ニュース推薦のプロセスに関わる様々な分野の間のギャップを埋め、より多くの情報に基づいた議論をサポートすることである。
We hope for future research to foster interdisciplinary teams, leveraging each fields’ unique skills and specialties.
今後の研究では、各分野のユニークなスキルや専門性を生かした学際的なチームを育成することを期待している。
