## link リンク

- https://www.mdpi.com/2673-6470/4/1/3 https://www.mdpi.com/2673-6470/4/1/3

## title
Bias Reduction News Recommendation System


## Abstract

News recommender systems (NRS) are crucial for helping users navigate the vast amount of content available online.
ニュース・リコメンダー・システム（NRS）は、ユーザーがオンラインで利用可能な膨大な量のコンテンツをナビゲートするのを支援するために極めて重要である。
However, traditional NRS often suffer from biases that lead to a narrow and unfair distribution of exposure across news items.
しかし、**従来のNRSは、ニュースアイテム間の露出の分布が狭く不公平になるバイアスに悩まされることが多い**。
In this paper, we propose a novel approach, the Contextual-Dual Bias Reduction Recommendation System (C-DBRRS), which leverages Long Short-Term Memory (LSTM) networks optimized with a multi-objective function to balance accuracy and diversity.
本論文では、**C-DBRRS（Contextual-Dual Bias Reduction Recommendation System）という新しいアプローチを提案**する。C-DBRRSは、精度と多様性のバランスをとるために多目的関数で最適化されたLSTM（Long Short-Term Memory）ネットワークを活用する。
We conducted experiments on two real-world news recommendation datasets and the results indicate that our approach outperforms the baseline methods, and achieves higher accuracy while promoting a fair and balanced distribution of recommendations.
我々は2つの実世界のニュース推薦データセットで実験を行い、その結果、我々のアプローチがベースライン手法を上回り、推薦の公平でバランスの取れた分布を促進しながら、より高い精度を達成することを示した。
This work contributes to the development of a fair and responsible recommendation system.
この研究は、公正で責任ある推薦システムの開発に貢献するものである。

# Introduction はじめに

The proliferation of digital media and information has led to an exponential increase in the availability of news content.
デジタルメディアと情報の普及は、ニュースコンテンツの利用可能性を飛躍的に増大させた。
However, this abundance of information poses challenges for users in selecting relevant and high-quality content.
しかし、このように情報が氾濫しているため、ユーザーにとっては、適切で質の高いコンテンツを選択することが難しい。
In response, news recommender systems (NRS) [1] have become vital components of online news platforms.
これを受けて、ニュース推薦システム（NRS）[1]はオンラインニュースプラットフォームの重要な構成要素となっている。
These systems provide personalized recommendations to users based on their behavior, preferences, and interactions [2].
これらのシステムは、ユーザーの行動、嗜好、インタラクションに基づいて、パーソナライズされたレコメンデーションを提供する[2]。
The primary goal of NRS is to enhance user engagement and retention by delivering tailored news consumption experiences [3].
NRSの主な目的は、ユーザーに合わせたニュース消費体験を提供することで、ユーザーのエンゲージメントとリテンションを高めることである[3]。

We present an example of a NRS, in in Figure 1, which considers User A, who frequently reads news articles related to environmental issues and sustainability.
図1にNRSの例を示す。環境問題や持続可能性に関するニュース記事をよく読むユーザーAを考える。
An NRS that focuses solely on accuracy would continuously recommend articles related to the environment and sustainability, based on User A’s past behavior.
正確さだけに焦点を当てたNRSは、ユーザーAの過去の行動に基づいて、環境や持続可能性に関連する記事を継続的に推薦するだろう。
This can lead to an ’echo chamber’ effect [1], where the user is exposed only to news and opinions that align with their existing beliefs and interests.
これは「エコーチェンバー」効果[1]につながる可能性があり、ユーザーは自分の既存の信念や関心に沿ったニュースや意見だけにさらされることになる。
Conversely, the NRS prioritizing fairness might recommend a broader range of topics, including politics, economics, technology, and social issues.
逆に、公平性を優先するNRSは、政治、経済、テクノロジー、社会問題など、より幅広いトピックを推奨するかもしれない。

In this study, we define ’fairness’ in the context of NRS as a balance between personalized recommendations and promoting content “diversity”.
本研究では、NRSの文脈における「公平性」を、パーソナライズされたレコメンデーションとコンテンツの「多様性」の促進とのバランスと定義する。
This approach aims to broaden users’ exposure to a variety of ideas and perspectives, though it might sometimes lead to less tailored recommendations, potentially affecting user engagement and satisfaction [4].
このアプローチは、ユーザーが様々なアイデアや視点に触れる機会を広げることを目的としているが、時には、ユーザーのニーズに合った推奨が行われず、ユーザーのエンゲージメントや満足度に影響を与える可能性がある[4]。
NRS often exhibit bias by prioritizing content that aligns with a user’s existing preferences, thus reinforcing their current beliefs and interests [5,6].
NRSは多くの場合、ユーザーの既存の嗜好に沿ったコンテンツを優先することでバイアスを示し、ユーザーの現在の信念や関心を強化する[5,6]。
To counter this, fairness in NRS is about offering a diverse and representative range of content.
これに対抗するため、NRSにおける公平性とは、多様で代表的なコンテンツを提供することである。
We introduce a novel method that seeks to strike a balance between personalization and diversity, with the goal of optimizing both the relevance of recommendations and the breadth of content exposure.
パーソナライゼーションと多様性のバランスを追求する新しい方法を紹介し、レコメンデーションの関連性とコンテンツ露出の幅の両方を最適化することを目標とする。

State-of-the-art NRS predominantly concentrate on enhancing recommendation accuracy [2,7], which is commendable.
最先端のNRSは主に推薦精度を高めることに注力しており[2,7]、これは称賛に値する。
However, there is a growing recognition of the need to balance accuracy with fairness [7,8,9].
しかし、正確さと公平さのバランスをとる必要性が認識されつつある[7,8,9]。
In NRS, a focus solely on accuracy may inadvertently lead to limited content exposure, potentially creating echo chambers [10].
NRSでは、正確さだけに焦点を当てると、コンテンツへの露出が不注意に制限され、エコーチェンバーが生じる可能性がある[10]。
Conversely, a system prioritizing fairness might offer a diverse range of content but with recommendations that are less aligned with individual user preferences [11].
逆に、公平性を優先するシステムは、多様なコンテンツを提供するかもしれないが、個々のユーザーの嗜好にあまり沿わない推薦をするかもしれない[11]。
Hence, there is an imperative need for strategies that simultaneously achieve both accuracy and fairness, aiming for a more inclusive news consumption experience.
したがって、正確さと公平さを同時に達成し、より包括的なニュース消費体験を目指す戦略が急務である。

This study introduces a novel approach to news recommendation that optimizes both accuracy and fairness.
本研究では、正確性と公平性の両方を最適化するニュース推薦の新しいアプローチを紹介する。
Fairness is a wide subject, encompassing various dimensions and interpretations depending on the context.
公平性とは幅広いテーマであり、文脈によってさまざまな次元や解釈を包含する。
In the realm of information systems and algorithms [4,12], fairness often involves considerations like equal representation, unbiased treatment of different groups, and equitable distribution of resources or opportunities.
情報システムやアルゴリズム[4,12]の領域では、公平性は、しばしば、平等な代表、異なる集団の不偏の扱い、資源や機会の公平な分配といった考察を含む。
It is about ensuring that systems and decisions do not favor one group or individual over another unjustly and that they reflect a balanced and inclusive approach.
制度や決定が、あるグループや個人を不当に優遇することなく、バランスの取れた包括的なアプローチを反映するようにすることである。
This is particularly crucial in areas such as news recommendations, hiring practices, and financial services, where the impact of unfairness can be significant on both individuals and society at large.
これは特に、ニュースの推奨、雇用慣行、金融サービスなど、不公正が個人と社会全体の双方に大きな影響を与えうる分野において極めて重要である。

In this work, we particularly refer to ’diversity’ for fairness, ensuring that the recommendations cater to a wide range of interests and perspectives [13].
この作業では、特に「多様性」に言及し、勧告が幅広い関心と視点に対応することを保証し、公平性を確保する[13]。
We propose a multi-objective optimization strategy for an NRS.
我々は、NRSの多目的最適化戦略を提案する。
Our contributions include the development of an algorithm that balances multiple factors, such as user preferences, content diversity, and fairness in exposure to different news sources.
私たちの貢献には、ユーザーの嗜好、コンテンツの多様性、異なるニュースソースに接する公平性など、複数の要素をバランスさせるアルゴリズムの開発が含まれる。
This approach not only enhances the relevance of recommendations but also promotes a diverse and inclusive news consumption experience.
このアプローチは、レコメンデーションの妥当性を高めるだけでなく、多様で包括的なニュース消費体験を促進する。
Our aim is to create a more holistic and responsible NRS.
私たちの目標は、より総合的で責任あるNRSを作ることだ。

We introduce the “Contextual Dual Bias Reduction Recommendation System (C-DBRRS)”, which ensures fairness in item and exposure aspects of news recommendation.
ニュース推薦の項目と露出の公平性を確保する「文脈二重バイアス削減推薦システム（C-DBRRS）」を紹介する。
Built on LSTM networks and optimized with a multi-objective function, C-DBRRS harmonizes accuracy and diversity in news recommendations.
LSTMネットワークをベースに多目的関数で最適化されたC-DBRRSは、ニュース推薦の精度と多様性を調和させる。
The hyperparameter 𝜆
ハイパーパラメータ ↪Ll_1706

allows for a tunable balance between relevance (precision, recall, NDCG) and fairness (Gini coefficient).
は、関連性（精度、再現率、NDCG）と公平性（ジニ係数）のバランスを調整することができる。
This is a novel approach, as it recognizes the trade-offs between providing relevant recommendations to users and ensuring a fair representation of items.
これは、ユーザーに適切な推薦を提供することと、アイテムの公正な表現を確保することのトレードオフを認識した、斬新なアプローチである。

# Literature Overview 文献概要

News recommender systems (NRS) have been a widely researched topic in recent years due to the increasing amount of online news content and the need for personalized recommendations [1].
ニュース推薦システム(NRS)は、オンラインニュースコンテンツの増加とパーソナライズされた推薦の必要性から、近年広く研究されているトピックである[1]。
Traditional NRS are designed to provide users with personalized news articles based on their past behavior, preferences, and interests [14].
従来のNRSは、ユーザーの過去の行動、嗜好、関心に基づいて、パーソナライズされたニュース記事を提供するように設計されている[14]。
Collaborative filtering and content-based filtering are two common approaches used in recommender systems [15].
協調フィルタリングとコンテンツベースフィルタリングは、推薦システムで使われる2つの一般的なアプローチである[15]。
Collaborative filtering recommends news articles to a user based on the preferences of similar users, whereas content-based filtering recommends articles based on the content of the articles and the user’s past behavior.
協調フィルタリングは、類似ユーザーの嗜好に基づいてユーザーにニュース記事を推薦するのに対し、コンテンツベースのフィルタリングは、記事の内容とユーザーの過去の行動に基づいて記事を推薦する。

Accuracy is a critical factor in the performance of recommender systems [1].
精度はレコメンダーシステムのパフォーマンスにおいて重要な要素である[1]。
The accuracy of a recommender system refers to its ability to recommend items that are relevant and of interest to the user [3].
レコメンダーシステムの精度とは、ユーザーにとって関連性があり、興味のあるアイテムを推薦する能力を指す[3]。
Commonly used metrics for evaluating the accuracy of recommender systems include the Mean Absolute Error (MAE), Root Mean Square Error (RMSE), and the F1-score [16].
推薦システムの精度を評価するために一般的に使用されるメトリクスには、平均絶対誤差（MAE）、二乗平均平方根誤差（RMSE）、およびF1スコアが含まれる[16]。
Several approaches have been proposed to improve the accuracy of recommender systems, such as incorporating additional contextual information [17], or using hybrid recommendation algorithms that combine the strengths of both collaborative filtering and content-based filtering [18].
推薦システムの精度を向上させるために、追加的な文脈情報を取り入れたり[17]、協調フィルタリングとコンテンツ・ベース・フィルタリングの両方の長所を組み合わせたハイブリッド推薦アルゴリズムを使ったり[18]、といったアプローチがいくつか提案されている。

Bias in recommender systems can manifest in various ways [8,9,19,20], including popularity bias, where the system tends to recommend popular items, leading to a lack of exposure for less popular or niche items [1].
レコメンダーシステムにおけるバイアスは様々な形で現れる可能性があり[8,9,19,20]、人気のあるアイテムをシステムが推奨する傾向があり、人気のないアイテムやニッチなアイテムの露出不足につながる人気バイアスなどがある[1]。
Additionally, there might be biases related to gender, race, or other demographic factors, leading to discriminatory recommendations [21].
さらに、性別、人種、その他の人口統計学的要因に関連したバイアスが存在し、差別的な推奨につながる可能性がある [21] 。
Researchers have proposed various fairness metrics to evaluate the fairness of recommender systems.
研究者は推薦システムの公正さを評価するために様々な公正さメトリクスを提案してきた。
These include statistical parity, which requires that the recommendations are independent of a protected attribute (e.g., gender, race), and disparate impact, which measures the ratio of positive outcomes for the protected group to the positive outcomes for the non-protected group [22,23].
これには、統計的同等性（統計的パリティ）が含まれ、これは勧告が保護属性（性別、人種など）から独立していることを要求するものであり、格差影響（格差インパクト）は、保護されたグループにとっての肯定的な結果の、保護されていないグループにとっての肯定的な結果に対する比率を測定するものである[22,23]。
A related approach [24] proposed a fairness-aware ranking algorithm that considers both the utility of the recommendations to the user and the fairness towards the items.
関連するアプローチ[24]は、ユーザーに対する推薦の有用性と項目に対する公平性の両方を考慮する公平性を考慮したランキングアルゴリズムを提案した。
Another approach is to re-rank the recommendations generated by a standard recommender system to improve fairness [20,23].
もう一つのアプローチは、公平性を向上させるために、標準的な推薦システムによって生成された推薦を再ランク付けすることである[20,23]。

Fairness in recommender systems has gained attention due to the potential biases that can arise from the recommendation algorithms.
推薦システムにおける公平性は、推薦アルゴリズムから生じる可能性のあるバイアスのために注目されている。
Studies have shown that recommender systems can inadvertently reinforce existing biases in the data, leading to unfair recommendations for certain groups of users [21].
レコメンダー・システムは、データ内の既存のバイアスを不注意に強化し、特定のユーザー・グループに対して不公平なレコメンデーションを行う可能性があることが研究で示されている[21]。
For example, a study [25] showed that a music recommender system was biased towards popular artists, leading to less exposure for less popular or niche artists.
例えば、ある研究[25]は、音楽推薦システムが人気アーティストに偏っており、人気のないアーティストやニッチなアーティストの露出が少ないことを示している。
Several approaches have been proposed to address fairness in recommender systems, such as re-ranking the recommendations [22] or modifying the recommendation algorithm to incorporate fairness constraints [20].
推薦システムにおける公平性に対処するために、いくつかのアプローチが提案されている。例えば、推薦のランク付けをやり直す [22]、あるいは公平性制約を組み込むために推薦アルゴリズムを修正する [20]などである。

Recent advancements in NRS emphasize a balance between accuracy and fairness, particularly in terms of diversity [5].
最近のNRSの進歩は、特に多様性の観点から、正確さと公平さのバランスを重視している[5]。
A novel multi-objective optimization strategy has been proposed to refine recommender system models.
レコメンダーシステムのモデルを改良するために、新しい多目的最適化戦略が提案されている。
For instance, ref.
例えば、参考文献。
[26] discusses an innovative algorithm utilizing multi-objective optimization.
[26]は、多目的最適化を利用した革新的なアルゴリズムについて論じている。
Similarly, ref.
同様に、参考文献もある。
[13] proposes a framework to optimize recommender systems, emphasizing fairness across multiple stakeholders.
[13]は、複数の利害関係者間の公平性を重視し、推薦システムを最適化するフレームワークを提案している。
Moreover, the use of multi-objective optimization for recommending online learning resources is effectively demonstrated [27].
さらに、オンライン学習リソースの推薦のための多目的最適化の使用は、効果的に実証されている[27]。
Finally, ref.
最後に、参考までに。
[28] highlights the application of big data in enhancing recommendation systems through multi-objective optimization.
[28]は、多目的最適化による推薦システムの強化におけるビッグデータの応用に注目している。

There is often a trade-off between fairness and accuracy in recommender systems [29].
レコメンダーシステムでは、公正さと正確さのトレードオフがしばしば存在する[29]。
Improving fairness in the recommendations may lead to a decrease in accuracy, and vice versa.
レコメンデーションの公平性を向上させることは、精度の低下につながる可能性があり、その逆もまた然りである。
For example, a study [24] showed that incorporating fairness constraints into the recommendation algorithm led to a decrease in recommendation accuracy.
例えば、ある研究 [24] では、推薦アルゴリズムに公平性制約を組み込むと、推薦精度が低下することが示された。
Similarly, a study [30] showed that re-ranking the recommendations to improve fairness led to a decrease in accuracy.
同様に、ある研究[30]では、公平性を高めるために推奨順位を変更すると、精度が低下することが示された。
Therefore, it is important to carefully consider the trade-off between fairness and accuracy when designing and evaluating recommender systems.
したがって、レコメンダー・システムを設計・評価する際には、公平性と正確性のトレードオフを注意深く考慮することが重要である。

# Materials and Methods 材料と方法

## Data

In our study, we utilized two real-world news recommendation datasets, namely MIND-small and Outbrain Click Prediction, which offer a comprehensive view of user interactions and preferences in news consumption.
本研究では、MIND-smallとOutbrain Click Predictionという2つの実世界のニュース推薦データセットを利用した。これらのデータセットは、ニュース消費におけるユーザーの相互作用と嗜好の包括的なビューを提供する。

MIND-small [2]: Derived from the larger MIND dataset, the MIND-small dataset, curated by Microsoft team, captures the interactions of 50,000 users on Microsoft News over a one-month period.
MIND-small [2]： 大規模なMINDデータセットから派生したMIND-smallデータセットは、マイクロソフトチームによってキュレーションされ、1ヶ月間のマイクロソフトニュースにおける5万人のユーザーのインタラクションをキャプチャしている。
For our study, we focused on this subset, analyzing their interactions with news articles, and associated metadata such as titles, categories, and abstracts.
本研究では、このサブセットに焦点を当て、ニュース記事とのインタラクション、およびタイトル、カテゴリー、抄録などの関連メタデータを分析した。

Outbrain Click Prediction [31]: Sourced from a Kaggle competition hosted by Outbrain, this dataset provides an extensive record of user page views and clicks across various publisher sites in the United States over a span of 14 days.
Outbrain Click Prediction [31]： Outbrainが主催するKaggleコンペティションから入手したこのデータセットは、米国の様々なパブリッシャーサイトにおける14日間にわたるユーザーのページビューとクリックの膨大な記録を提供する。
It offers valuable insights into user behaviors regarding displayed and clicked ads.
表示された広告やクリックされた広告に関するユーザーの行動に関する貴重な洞察を提供する。

Our data preparation methodology involves several key stages to ensure the datasets were optimally configured for our recommender system.
データセットがレコメンダーシステムに最適に設定されるように、データ準備の方法論にはいくつかの重要な段階がある。
We started with fundamental data-cleaning procedures to enhance the quality and reliability of our datasets.
我々は、データセットの品質と信頼性を高めるために、基本的なデータクリーニングの手順から始めた。
This involved the removal of duplicate records and the addressing of missing or incomplete data through exclusion criteria.
これには、重複記録の削除と、除外基準によるデータの欠落や不完全なデータへの対処が含まれる。
To enrich our analysis, we extracted several critical features from the datasets:
分析を充実させるため、データセットからいくつかの重要な特徴を抽出した：

Textual Embeddings (BERT): we converted the text content of news articles into numerical vector representations using the BERT (base-uncased) model to encapsulate their semantic content.
テキスト埋め込み（BERT）： ニュース記事のテキスト内容を、BERT（base-uncased）モデルを用いて数値ベクトル表現に変換し、意味内容をカプセル化した。

Topic Modeling (LDA): articles were categorized into specific genres or themes using Latent Dirichlet Allocation (LDA).
トピックモデリング（LDA）： 記事は、LDA（Latent Dirichlet Allocation）を用いて特定のジャンルやテーマに分類された。

Sentiment Analysis (VADER): we employed the VADER [32] tool to analyze the emotional tone of articles, classifying them as positive, negative, or neutral.
センチメント分析（VADER）： VADER[32]ツールを使って、記事の感情的なトーンを分析し、ポジティブ、ネガティブ、ニュートラルに分類した。

Post feature extraction, we standardized the scale of numerical features to ensure uniformity.
特徴抽出後、統一性を確保するために数値特徴のスケールを標準化した。
Subsequently, we integrated detailed user interaction data, including clicks, views, and duration of engagement with each article, with the article features.
その後、各記事に対するクリック数、閲覧数、関与時間を含む詳細なユーザーインタラクションデータを記事の特徴と統合した。
This integration facilitated the creation of comprehensive user–article interaction profiles.
この統合により、包括的なユーザーと記事の相互作用プロファイルの作成が容易になった。

For effective processing using Long Short-Term Memory (LSTM) networks, we structured our data in the following manner:
長短期記憶（LSTM）ネットワークを用いた効果的な処理のために、我々はデータを以下のように構造化した：

Unified Input Vectors: each user–article interaction was represented as a unified vector, consolidating user behavioral data with the extracted article content features.
統一された入力ベクトル： 各ユーザーと記事の相互作用は、ユーザーの行動データと抽出された記事コンテンツの特徴を統合した統一ベクトルとして表現された。

Time Series Formation: we structured the data into time series to capture the temporal dynamics of user interactions, a crucial aspect of LSTM processing.
時系列の形成： LSTM処理の重要な側面である、ユーザーとのインタラクションの時間的ダイナミクスを捉えるために、データを時系列に構造化した。

The final stage in our data preparation was the division of the dataset into distinct sets for training, validation, and testing, following the 80-10-10 scheme in chronological temporal order.
データ準備の最終段階は、時系列順に80-10-10スキームに従って、データセットをトレーニング用、検証用、テスト用の別々のセットに分けることだった。
We combined and structured data from the MIND-small and Outbrain Click Prediction datasets to capture the temporal dynamics of user interactions with news articles.
MIND-smallデータセットとOutbrainクリック予測データセットのデータを組み合わせて構造化し、ニュース記事とユーザーの相互作用の時間的ダイナミクスを捉えた。
The following elements constitute our data structure:
以下の要素がデータ構造を構成している：

User and Article Identifiers: unique IDs for users and articles to track interactions.
ユーザーと記事の識別子： インタラクションを追跡するためのユーザーと記事のユニークなID。

Interaction Timestamps: capture the timing of each interaction, crucial for time series analysis.
交流タイムスタンプ： 時系列分析に重要な各インタラクションのタイミングをキャプチャします。

Interaction Types: categorized as clicks, views, and engagement duration.
インタラクションの種類： クリック数、ビュー数、エンゲージメント時間などに分類されます。

Content Features: textual embeddings, topic categories, and sentiment scores for articles from MIND-small.
コンテンツの特徴： MIND-smallの記事に対するテキスト埋め込み、トピック・カテゴリー、センチメント・スコア。

Sequential Interaction History: chronological sequence of user interactions, vital for learning user behavior patterns over time.
連続したインタラクション履歴： ユーザーとのインタラクションの時系列的なシーケンスで、時間の経過とともにユーザーの行動パターンを学習するのに不可欠。

## Contextual Dual Bias Reduction Recommendation System コンテキストに基づく二重バイアス低減推薦システム

In this section, we introduce the Contextual Dual Bias Reduction Recommendation System (C-DBRRS) algorithm, which is an advanced LSTM-based algorithm tailored for news recommendation.
このセクションでは、ニュース推薦のために調整された高度なLSTMベースのアルゴリズムであるC-DBRRS（Contextual Dual Bias Reduction Recommendation System）アルゴリズムを紹介する。
C-DBRRS is designed to balance content relevance and fairness by mitigating item and exposure biases while adapting to dynamic user interactions and news features.
C-DBRRSは、動的なユーザー・インタラクションやニュースの特徴に適応しながら、アイテムや露出のバイアスを軽減することで、コンテンツの関連性と公平性のバランスをとるように設計されている。
The notations used in the equations of this section are in Table 1 and the algorithm is given in Algorithm 1.
このセクションの式で使用する表記を表1に、アルゴリズムをアルゴリズム1に示す。

The C-DBRRS employs a Long Short-Term Memory (LSTM) network to process sequences of input data 𝑥=(𝑥1,𝑥2,…,𝑥𝑡) , integrating user interactions with news content features.
C-DBRRSは、入力データ𝑥=(𝑥1,𝑥2,...,𝑥1)のシーケンスを処理するためにLong Short-Term Memory (LSTM)ネットワークを採用し、ユーザーのインタラクションとニュースコンテンツの特徴を統合する。
The LSTM updates its internal state at each time step t through the following mechanisms:
LSTMは以下のメカニズムによって、各時間ステップtで内部状態を更新する：

Input Gate controls how much new information flows into the cell state:
インプット・ゲートは、細胞の状態にどれだけの新しい情報が流れ込むかを制御する：

Forget Gate determines the information to be removed from the cell state:
Forget Gateはセルの状態から削除する情報を決定する：

Cell State Update generates new candidate values for updating the cell state:
セル状態更新は、セル状態を更新するための新しい候補値を生成する：

Output Gate outputs the next hidden state reflecting the processed information:
出力ゲートは、処理された情報を反映した次の隠れ状態を出力する：

To manage the trade-off between relevance and fairness in recommendations, the system employs a hyperparameter 𝜆 (described below).
推薦における関連性と公平性のトレードオフを管理するために、システムはハイパーパラメータᜆ（後述）を採用する。
Relevance is assessed using metrics like Precision, Recall, and NDCG, whereas fairness is evaluated through the Gini coefficient.
関連性は、Precision、Recall、NDCGのような指標を用いて評価され、公平性はジニ係数によって評価される。
The optimization objective is formulated as:
最適化の目的は次のように定式化される：

In this optimization objective: 𝐿acc (Accuracy Loss) is typically the mean squared error (MSE) between the predicted and actual user interactions.
この最適化目標では 𝐿 (Accuracy Loss)は通常、予測されたユーザー・インタラクション と実際のユーザー・インタラクションの平均二乗誤差(MSE)です。
It measures how accurately the system predicts user preferences based on their interaction history and content features.
これは、ユーザーのインタラクション履歴とコンテンツの特徴に基づいて、システムがどれだけ正確にユーザーの嗜好を予測できるかを測定するものである。
𝐿item (Item Bias Loss) aims to reduce the bias towards frequently recommended items.
↪Lu_1D43F (Item Bias Loss)は、頻繁に推奨される項目への偏りを減らすことを目的としています。
It is computed by measuring the deviation of the item distribution in the recommendations from a desired distribution, such as a uniform distribution.
これは、一様分布のような望ましい分布から、推奨の項目分布の偏差を測定することによって計算される。
𝐿exp (Exposure Bias Loss) is designed to ensure that all items receive a fair amount of exposure in the recommendations.
↪Lu_1D43F (Exposure Bias Loss)は、すべての項目が推薦の中で公正な量の露出を受けるように設計されている。
This is measured as the variance in the number of times different items are recommended, penalizing the model when certain items are consistently under-represented.
これは、異なる項目が推奨される回数の分散として測定され、特定の項目が一貫して過小評価されている場合にモデルにペナルティを課す。
The hyperparameters 𝛼,𝛽,𝛾 are used to balance these different aspects of the loss function.
ハイパーパラメータ𝛼,𝛾は、損失関数のこれらの異なる側面のバランスをとるために使用される。
They are typically determined through experimentation and tuning, based on the specific characteristics of the data.
これらは通常、データの特定の特性に基づいて、実験とチューニングを通じて決定される。

# Experimental Setup 実験セットアップ

## Baseline Methods ベースラインの方法

Our evaluation of the proposed C-DBRRS includes comparisons with a range of established recommendation methods, each offering unique strengths:
提案されたC-DBRRSの評価には、確立された推薦方法の範囲との比較が含まれ、それぞれがユニークな強みを提供する：

Popularity-based Recommendation (POP): this method ranks news articles based on their overall popularity, measured by the total number of user clicks.
人気ベースの推薦（POP）： このメソッドは、ユーザーのクリック数の合計で測定される全体的な人気に基づいてニュース記事をランク付けします。

Content-based Recommendation (CB): this method suggests articles to users by aligning the content of articles with their past preferences.
コンテンツ・ベースト・レコメンデーション（CB）： この方法は、記事の内容とユーザーの過去の嗜好を一致させることで、ユーザーに記事を提案する。

Collaborative Filtering (CF): this method utilizes user behavior patterns, recommending items favored by similar users.
協調フィルタリング（CF）： ユーザーの行動パターンを利用し、類似したユーザーが好むアイテムを推薦する手法。

Matrix Factorization (MF) [3]: this method decomposes the user–item interaction matrix into lower-dimensional latent factors for inferring user interests.
行列因数分解（MF）[3]： この方法は、ユーザとアイテムの相互作用行列を低次元の潜在因子に分解し、ユーザの興味を推測する。

Neural Collaborative Filtering (NCF) [33]: this method combines neural network architectures with collaborative filtering to enhance recommendation accuracy.
ニューラル協調フィルタリング（NCF）[33]： ニューラルネットワークアーキテクチャと協調フィルタリングを組み合わせ、推薦精度を高める手法。

BERT4Rec [34]: this model employs the Bidirectional Encoder Representations from Transformers (BERT) architecture, specifically designed for sequential recommendation.
BERT4Rec [34]： このモデルは、特に逐次推薦のために設計されたBERT（Bidirectional Encoder Representations from Transformers）アーキテクチャを採用している。
It captures complex item interaction patterns and user preferences from sequential data.
逐次的なデータから複雑なアイテムのインタラクションパターンとユーザーの嗜好を捉える。
We used the BERT-base-uncased model.
我々は、BERT-base-uncased モデルを使用した。

## Evaluation Metrics 評価指標

To assess the performance of our model against the baselines, we employed several key metrics:
ベースラインに対する我々のモデルの性能を評価するために、いくつかの主要な指標を採用した：

Precision@K measures the proportion of relevant articles in the top-K recommendations, reflecting accuracy.
Precision@Kは、精度を反映し、トップKレコメンデーションに含まれる関連記事の割合を測定する。

Recall@K indicates the fraction of relevant articles captured in the top-K recommendations, highlighting the model’s retrieval ability.
Recall@Kは、トップKの推奨に含まれる関連記事の割合を示し、モデルの検索能力を強調する。

Normalized Discounted Cumulative Gain (NDCG)@K assesses ranking quality, prioritizing the placement of relevant articles higher in the recommendation list.
正規化割引累積利得(NDCG)@Kは、ランキングの質を評価し、推薦リストにおいて関連性の高い記事をより上位に配置することを優先する。

Gini Index evaluates the fairness of recommendation distribution, with lower values indicating more equitable distribution across items.
ジニ指数は推薦分布の公平性を評価するもので、値が低いほど項目間の分布が公平であることを示す。

We consider the value of top@ k as 5 (k = 5) following standard works in recommender systems theory [16].
我々は推薦システム理論の標準的な研究[16]に従い、top@ kの値を5（k = 5）と考える。

## Settings and Hyerparameters 設定とパラメータ

We temporally split the datasets into training, validation, and testing sets with a ratio of 80:10:10.
データセットを80:10:10の割合で訓練セット、検証セット、テストセットに時間的に分割した。
The hyperparameters of the models were tuned on the validation set.
モデルのハイパーパラメータは検証セットで調整した。
All experiments were conducted on a machine with an Intel Xeon processor, 32GB RAM, and an Nvidia GeForce GTX 1080 Ti GPU.
実験はすべて、インテルXeonプロセッサー、32GB RAM、Nvidia GeForce GTX 1080 Ti GPUを搭載したマシンで行った。
The set of hyperparameters is given in Table 2.
ハイパーパラメータのセットを表2に示す。

In our C-DBRRS, various hyperparameters are carefully tuned for optimal performance, as shown in Table 2.
我々のC-DBRRSでは、表2に示すように、様々なハイパーパラメータを最適な性能になるように慎重に調整する。
Hyperparameters 𝛼,𝛽,𝛾 are crucial for weighting different components of the loss function, controlling how the model balances prediction accuracy, item bias, and exposure bias, respectively.
ハイパーパラメータ𝛼,𝛾は、損失関数の異なるコンポーネントを重み付けするために重要であり、モデルが予測精度、項目バイアス、暴露バイアスをそれぞれどのようにバランスさせるかを制御します。
In particular, 𝜆 serves as a key parameter for overall balancing between relevance and fairness in the recommendation output, in line with the system’s optimization objective.
特にᜆは、システムの最適化目的に沿って、推薦出力における関連性と公平性の全体的なバランスをとるための重要なパラメータとして機能する。

## Overall Results 総合成績

Table 3 illustrates the performance of various recommendation methods on the MIND-small and Outbrain datasets, respectively, including our proposed C-DBRRS and the state-of-the-art models.
表3は、MIND-smallデータセットとOutbrainデータセットにおける様々な推薦手法の性能を示している。
The performances reported are averaged over five runs to ensure statistical reliability, with the standard deviation included to indicate performance variability.
報告された性能は、統計的信頼性を確保するために5回の走行を平均したもので、性能のばらつきを示すために標準偏差が含まれている。

The Table 3 compares the performance of different recommendation methods on two datasets, MIND-small and Outbrain, using metrics such as Precision@5, Recall@5, NDCG@5, and the Gini Index.
表3は、Precision@5、Recall@5、NDCG@5、Gini Indexといった指標を用いて、MIND-smallとOutbrainという2つのデータセットにおける異なる推薦手法のパフォーマンスを比較したものである。
In both datasets, the C-DBRRS method demonstrates higher performance, achieving the highest scores in Precision@5, Recall@5, and NDCG@5, alongside the lowest Gini Index.
両データセットにおいて、C-DBRRS法はより高い性能を示し、Precision@5、Recall@5、NDCG@5において最高スコアを達成し、ジニ指数は最低となった。
In this study, we value a lower GINI index as it indicates a desirable level of diversity in recommendations.
本研究では、GINI指数が低ければ低いほど、推奨の多様性が望ましいレベルであることを示すので、これを重視する。
However, we aim to achieve this without resorting to entirely random recommendations.
しかし、完全に無作為な推薦に頼ることなく、これを達成することを目指している。
Our goal is to strike a balance between diversity and relevance, ensuring that the recommendations are diverse yet still meaningful and aligned with user interests.
私たちのゴールは、多様性と関連性のバランスを取ることであり、レコメンデーションが多様でありながらも有意義で、ユーザーの関心に沿ったものであることを保証することです。

Other methods like POP, CB, CF, MF, NCF, and BERT4Rec show lower performance compared to C-DBRRS.
POP、CB、CF、MF、NCF、BERT4Recのような他の方法は、C-DBRRSに比べて性能が低い。
The improvement in performance metrics from simpler methods like POP to more advanced ones like C-DBRRS highlights the efficacy of sophisticated recommendation systems.
POPのような単純な手法からC-DBRRSのような高度な手法に至るまで、パフォーマンス指標が向上していることは、洗練された推薦システムの有効性を浮き彫りにしている。
Particularly, the lower Gini Index in methods like C-DBRRS highlights their capability in ensuring a more equitable distribution of recommendations (not too highly diverse).
特に、C-DBRRSのような手法のジニ指数が低いことは、より公平な（多様性が高すぎない）推薦者の分配を保証する能力を強調している。

Overall, these results suggest a clear advantage of advanced methods like C-DBRRS in enhancing both the accuracy and fairness of recommendations in News Recommendation Systems.
全体として、これらの結果は、ニュース推薦システムにおける推薦の精度と公平性の両方を高める上で、C-DBRRSのような高度な手法が明らかに有利であることを示唆している。
Because of the comparable patterns found in both datasets and the superior performance of our model on the MIND dataset, we will present the results of our subsequent experiments using the MIND dataset.
両データセットで同程度のパターンが見つかり、MINDデータセットでの我々のモデルの性能が優れていたため、MINDデータセットを使ったその後の実験結果を紹介する。

## Recommendation Distribution across Different News Categories 異なるニュースカテゴリー間の推薦分布

To assess the fairness of the C-DBRRS’s recommendation distribution across different news categories on the MIND dataset, we employed the Gini coefficient as a measure of inequality—a Gini coefficient of 0 expresses perfect equality, and a Gini coefficient of 1 implies maximal inequality among values.
C-DBRRSの推薦分布の公平性をMINDデータセットの異なるニュースカテゴリー間で評価するために、不平等の尺度としてジニ係数を採用した（ジニ係数0は完全な平等を表し、ジニ係数1は価値間の不平等が最大であることを意味する）。
We first calculated the Gini coefficients for each category in the baseline model, where no fairness constraints were applied.
まず、公平性制約が適用されていないベースラインモデルで、各カテゴリーのジニ係数を計算した。
Subsequently, we integrated the fairness constraints into the C-DBRRS model and recalculated the Gini coefficients.
その後、公平性制約をC-DBRRSモデルに統合し、ジニ係数を再計算した。

As evident from Table 4, all categories exhibit a significant reduction in the Gini coefficient, indicating a more equitable distribution of news recommendations.
表4から明らかなように、すべてのカテゴリーでジニ係数が有意に減少しており、推奨ニュースの分配がより公平であることを示している。
Specifically, the ‘Environment’ category showed the most considerable improvement, with a Gini coefficient reduction from 0.65 to 0.30, followed by the ‘Arts’ category, which reduced from 0.60 to 0.28.
具体的には、「環境」カテゴリーが最も大きな改善を示し、ジニ係数は0.65から0.30に減少し、次いで「芸術」カテゴリーが0.60から0.28に減少した。
The ‘Politics’ and ‘Sports’ categories also observed notable improvements.
政治」と「スポーツ」カテゴリーも顕著な改善が見られた。
The reduction in the Gini coefficients across all news categories indicates that the C-DBRRS model successfully addresses the challenges of item bias and exposure bias, leading to a more equitable and diverse set of recommendations.
すべてのニュースカテゴリーでジニ係数が減少していることは、C-DBRRSモデルが項目バイアスと露出バイアスの課題にうまく対処し、より公平で多様な提言のセットをもたらしていることを示している。

## Analysis of Relevance and Fairness Trade-Off 関連性と公平性のトレードオフの分析

The results presented in Figure 2 illustrate the trade-off between relevance and fairness for the C-DBRRS model.
図2に示す結果は、C-DBRRSモデルにおける関連性と公平性のトレードオフを示している。
Specifically, as the value of 𝜆 increases from 0 to 1, the model places more emphasis on fairness, leading to a decrease in relevance as measured by Precision@5, Recall@5, and NDCG@5.
具体的には、ᜆの値が0から1に増加するにつれて、モデルはより公平性を重視するようになり、Precision@5、Recall@5、NDCG@5で測定される関連性が低下する。
For example, when 𝜆 is 0 (meaning the model only considers relevance), the Precision@5, Recall@5, and NDCG@5 are highest However, when 𝜆 is increased to 1 (meaning the model only considers fairness), these values decreases.
例えば、Űが0（モデルが関連性のみを考慮することを意味する）のとき、Precision@5、Recall@5、NDCG@5が最も高い。 しかし、Űが1（モデルが公平性のみを考慮することを意味する）に増加すると、これらの値は減少する。
This indicates that there is a trade-off between achieving high relevance and high fairness, as improving fairness leads to a decrease in relevance.
これは、高い関連性を達成することと高い公平性を達成することはトレードオフの関係にあることを示している。

The Gini Index, a measure of inequality, improves (decreases) as 𝜆 increases, indicating that the recommendations are becoming more fair.
不平等の指標であるジニ指数は、ᜆが増加するにつれて改善（減少）し、推奨がより公平になっていることを示している。
For example, when 𝜆 is 0, the Gini Index is 0.10, whereas it decreases to 0.18 when 𝜆 is 0.5 and increases further when 𝜆 is 1.
例えば、 𝜆が0のとき、ジニ指数は0.10であるが、 𝜆が0.5のときは0.18に減少し、 𝜆が1のときはさらに増加する。
This shows that the C-DBRRS model is effective at improving the fairness of the recommendations while maintaining a reasonable level of relevance.
これは、C-DBRRSモデルが、妥当なレベルの妥当性を維持しながら、推薦の公平性を向上させるのに効果的であることを示している。
Researchers and practitioners using this model will need to carefully select the value of 𝜆 to balance the trade-off between relevance and fairness based on their specific application and requirements.
このモデルを使用する研究者や実務者は、特定の用途や要件に基づいて、関連性と公平性のトレードオフのバランスをとるためにᜆの値を慎重に選択する必要があります。

# Discussion 議論

## Practical and Theoratical Impact 実践的かつ理論的なインパクト

In this paper, we presented a novel approach optimized with a multi-objective function to balance the accuracy and diversity aspects of fairness.
本論文では、公平性の正確さと多様性の側面をバランスさせるために、多目的関数で最適化された新しいアプローチを提示した。
The C-DBRRS model, which forms the foundation of our approach, leverages the capability of LSTM networks to capture temporal patterns in users’ interactions with items, thereby providing more accurate and personalized recommendations.
我々のアプローチの基礎となるC-DBRRSモデルは、LSTMネットワークの能力を活用し、ユーザーとアイテムとのインタラクションの時間的パターンを捉えることで、より正確でパーソナライズされたレコメンデーションを提供する。
By predicting the next items a user is likely to interact with and ranking them based on their predicted interaction probabilities, our model can recommend the top-ranked items to the user.
ユーザーが次にインタラクションしそうなアイテムを予測し、予測されたインタラクション確率に基づいてそれらをランク付けすることで、我々のモデルは上位にランク付けされたアイテムをユーザーに推薦することができる。

Our multi-objective optimization goal is a key contribution to this work.
我々の多目的最適化目標は、この仕事への重要な貢献である。
This approach integrates multiple bias-related objectives, namely item bias and exposure bias, in addition to accuracy.
このアプローチは、正確さに加えて、項目バイアスや暴露バイアスといった、バイアスに関連する複数の目的を統合するものである。
By formulating this as a multi-objective optimization problem and minimizing the Gini coefficients of the distribution of recommended items and exposure, we encourage a more equal and unbiased distribution of recommendations and exposure.
これを多目的最適化問題として定式化し、推奨アイテムと露出の分布のジニ係数を最小化することで、推奨と露出のより平等で偏りのない分布を促します。

## Limitations 制限事項

Our approach has some limitations.
我々のアプローチにはいくつかの限界がある。
First, the computational complexity of the model may be high due to the use of LSTM networks and the need to compute Gini coefficients for user–item interactions.
第一に、LSTMネットワークの使用と、ユーザーとアイテムの相互作用に対するジニ係数を計算する必要性により、モデルの計算複雑性が高くなる可能性がある。
This may limit the scalability of our approach to very large datasets.
このため、非常に大規模なデータセットに対する我々のアプローチのスケーラビリティが制限される可能性がある。
Second, the performance of our approach may be sensitive to the choice of hyperparameters, and determining the optimal values may require extensive grid search.
第二に、我々のアプローチの性能は、ハイパーパラメータの選択に敏感である可能性があり、最適値を決定するには、広範なグリッド探索が必要になる可能性がある。
Furthermore, our approach assumes that the temporal dynamics of user–item interactions are important for making recommendations.
さらに、我々のアプローチは、ユーザーとアイテムの相互作用の時間的ダイナミクスが推薦を行う上で重要であると仮定している。
This assumption may not hold for all types of items or users.
この仮定は、すべての種類のアイテムやユーザーに対して成り立つとは限らない。
Moreover, whereas our focus is on finding biases, it is essential to acknowledge that fairness in recommendation systems is beyond diversity.
さらに、我々の焦点はバイアスを見つけることにあるが、推薦システムにおける公正さは多様性を超えるものであることを認識することが不可欠である。
Future studies should delve into nuanced facets of fairness, including equitable item representation and user recommendations.
今後の研究では、公平な項目表示やユーザーの推奨など、公平性の微妙な側面について掘り下げていく必要がある。

Future work could explore alternative optimization algorithms, different types of recurrent neural networks, and the applicability of our approach to other types of recommendation problems.
将来的には、別の最適化アルゴリズム、異なるタイプのリカレント・ニューラル・ネットワーク、そして他のタイプの推薦問題への本アプローチの適用可能性を探ることができるだろう。

## Recommender Systems Fairness in the Era of Large Language Models 大規模言語モデルの時代における推薦システムの公平性

The emergence of Large Language Models (LLMs) has brought a new dimension to the fairness of recommender systems.
大規模言語モデル(LLM)の出現は、推薦システムの公平性に新たな次元をもたらしている。
A recent survey [35] highlights the importance of integrating fairness-aware strategies in these systems, focusing on countering potential biases and promoting equality.
最近の調査[35]では、潜在的な偏見に対抗し、平等を促進することに焦点を当て、公正さを意識した戦略をこれらのシステムに統合することの重要性が強調されている。
LLMs, with their advanced deep learning architectures and extensive training on diverse datasets, excel in identifying and predicting a wide array of user preferences and behaviors.
LLMは、高度なディープラーニングアーキテクチャと多様なデータセットに対する広範なトレーニングにより、幅広いユーザーの嗜好や行動を特定し予測することに優れている。
This capability is important in counteracting the ‘echo chamber’ effect prevalent in recommender systems by offering a varied range of content.
この機能は、多様なコンテンツを提供することで、レコメンダー・システムに蔓延する「エコーチェンバー」効果を打ち消す上で重要である。
Such diversity in content exposes users to a broader spectrum of topics and perspectives, thereby promoting a more balanced consumption of information, whereas personalization is essential for user satisfaction, LLMs in recommender systems can aptly balance it with the need for recommendation diversity.
このようなコンテンツの多様性は、ユーザーをより広範なトピックや視点に触れさせることで、よりバランスの取れた情報消費を促進する。一方、ユーザーの満足度を高めるためにはパーソナライゼーションが不可欠であるが、推薦システムにおけるLLMは、推薦の多様性の必要性と適切にバランスを取ることができる。

However, the utilization of LLMs in recommender systems is accompanied by challenges.
しかし、推薦システムにおけるLLMの利用には課題が伴う。
Ensuring user privacy, managing biased training data, and maintaining transparency in the recommendation processes are critical considerations.
ユーザーのプライバシーの確保、偏ったトレーニングデータの管理、推薦プロセスにおける透明性の維持は、重要な考慮事項である。
Additionally, there is an ethical imperative to avoid manipulative practices in these systems.
さらに、このようなシステムにおいて、操作的な行為を避けることは倫理的に必須である。
LLMs, with their extensive knowledge and understanding, are adept at delivering recommendations that are not only precise but also encompass a wide spectrum of content.
広範な知識と理解を持つLLMは、的確であるだけでなく、幅広い内容を網羅した提言を行うことに長けている。

The integration of LLMs into recommender systems necessitates the development of advanced strategies to accommodate diverse user preferences and diminish biases [36].
LLMを推薦システムに統合するためには、多様なユーザーの嗜好に対応し、バイアスを減少させるための高度な戦略を開発する必要がある[36]。
The need for fairness testing in these systems to ensure equitable recommendations is emphasized in related research [37].
公平な推薦を保証するために、これらのシステムにおける公平性テストの必要性は、関連する研究で強調されている[37]。
Moreover, various evaluation approaches and assurance strategies are proposed to uphold fairness in recommender systems [38].
さらに、推薦システムの公平性を維持するために、様々な評価アプローチや保証戦略が提案されている[38]。
The significance of privacy-preserving mechanisms in LLM-based recommender systems is also required, underlining the interplay between fairness and privacy [39].
LLMベースの推薦システムでは、公平性とプライバシーの相互関係を強調する、プライバシーを保護するメカニズムの重要性も求められている[39]。
All these approaches should align with the broader goal of fairness in recommender systems, ensuring that users are presented with a balanced mix of familiar and novel content, thus avoiding the creation of echo chambers.
これらのアプローチはすべて、レコメンダーシステムにおける公平性という広範な目標に沿うものであるべきで、ユーザーに馴染みのあるコンテンツと斬新なコンテンツをバランスよく提示することで、エコーチェンバーの発生を回避する。

# Conclusions 結論

In this paper, we presented the C-DBRRS that formulates the optimization goal as a multi-objective problem to encourage a more equal and unbiased distribution of recommendations and exposure.
本論文では、最適化目標を多目的問題として定式化し、より平等で偏りのない推薦と露出の分配を促すC-DBRRSを提示した。
Our experiments on two real-world datasets demonstrated that our approach outperforms state-of-the-art methods in terms of accuracy, fairness, and balance.
実世界の2つのデータセットを用いた実験により、我々のアプローチが精度、公平性、バランスの点で最先端の手法を上回ることが実証された。
Additionally, recommendation distribution across different news categories confirmed the effectiveness of our approach in addressing item bias and exposure bias, leading to a more equitable and diverse set of recommendations.
さらに、異なるニュースカテゴリーにわたる推薦分布から、項目バイアスと露出バイアスに対処する本アプローチの有効性が確認され、より公平で多様な推薦セットへとつながった。
This is a crucial step towards developing more fair and responsible recommendation systems.
これは、より公正で責任ある推薦システムを開発するための重要な一歩である。
Future work could explore alternative optimization algorithms, different types of recurrent neural networks, LLMs and the applicability of our approach to other types of recommendation problems.
将来的には、別の最適化アルゴリズム、異なるタイプのリカレント・ニューラル・ネットワーク、LLM、そして他のタイプの推薦問題への本アプローチの適用可能性を探ることができるだろう。
Additionally, it would be interesting to investigate the impact of our approach on user satisfaction and engagement in a real-world setting.
さらに、私たちのアプローチがユーザーの満足度やエンゲージメントに与える影響を、実際の環境で調査することも興味深い。

### Abbreviations 略語

The following abbreviations are used in this manuscript:
この原稿では以下の略語を使用した：

NRS News Recommender Systems
NRS ニュース推薦システム

LSTM Long Short-Term Memory
LSTM 長短期記憶

C-DBRRS Contextual Dual Bias Reduction Recommendation System
C-DBRRS Contextual Dual Bias Reduction Recommendation System コンテクスチュアル・デュアル・バイアス・レコメンデーション・システム

BERT Bidirectional Encoder Representations from Transformers
トランスフォーマーからのBERT双方向エンコーダ表現

POP Popularity-Based Recommendation
POP人気に基づく推薦

CB Content-Based Recommendation
CBコンテンツに基づく推薦

CF Collaborative Filtering
CF協調フィルタリング

MF Matrix Factorization
MF 行列因数分解

NCF Neural Collaborative Filtering
NCF ニューラル協調フィルタリング

NDCG Normalized Discounted Cumulative Gain
NDCG 正規化割引累積利益
