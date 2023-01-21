## 0.1. link 0.1. リンク

https:
httpsを使用しています。

https:
httpsを使用しています。

## 0.2. title 0.2. タイトル

Countering Popularity Bias by Regularizing Score Differences
スコア差の正則化による人気度バイアスの対策

## 0.3. abstruct 0.3. abstruct

Recommendation system often suffers from popularity bias.
レコメンデーションシステムはしばしば人気度バイアスに悩まされる。
Often the training data inherently exhibits long-tail distribution in item popularity (data bias).
多くの場合、学習データはアイテムの人気度においてロングテール分布を示している（データバイアス）。
Moreover, the recommendation systems could give unfairly higher recommendation scores to popular items even among items a user equally liked, resulting in over-recommendation of popular items (model bias).
さらに、推薦システムは、ユーザが同じように好きなアイテムであっても、人気のあるアイテムに不当に高い推薦スコアを与えることがあり、その結果、人気のあるアイテムを過剰に推薦してしまう（モデルの偏り）。
In this study we propose a novel method to reduce the model bias while maintaining accuracy by directly regularizing the recommendation scores to be equal across items a user preferred.
そこで本研究では，ユーザが好むアイテム間で推薦スコアが等しくなるように直接正則化することで，精度を維持したままモデルの偏りを低減する新しい手法を提案する．
Akin to contrastive learning, we extend the widely used pairwise loss (BPR loss) which maximizes the score differences between preferred and unpreferred items, with a regularization term that minimizes the score differences within preferred and unpreferred items, respectively, thereby achieving both high debias and high accuracy performance with no additional training.
コントラスト学習と同様に，好みのアイテムとそうでないアイテムのスコア差を最大化するペアワイズロス（BPRロス）を，好みのアイテムとそうでないアイテムのスコア差をそれぞれ最小化する正則化項で拡張し，追加の学習なしに高いデビアスと高い精度の性能を実現する．
To test the effectiveness of the proposed method, we design an experiment using a synthetic dataset which induces model bias with baseline training; we showed applying the proposed method resulted in drastic reduction of model bias while maintaining accuracy.
提案手法の有効性を検証するため、ベースライン学習によりモデルの偏りを誘発する合成データセットを用いた実験を行い、提案手法を適用することで、精度を維持したままモデルの偏りを大幅に削減できることを示した。
Comprehensive comparison with earlier debias methods showed the proposed method had advantages in terms of computational validity and efficiency.
また、従来のデバイアス手法との包括的な比較により、提案手法は計算の妥当性と効率の面で優れていることを示した。
Further empirical experiments utilizing four benchmark datasets and four recommendation models indicated the proposed method showed general improvements over performances of earlier debias methods.
さらに，4つのベンチマークデータセットと4つの推薦モデルを用いた実証実験を行った結果，提案手法は従来のデビアス手法と比較して全般的に性能が向上していることが示された．
We hope that our method could help users enjoy diverse recommendations promoting serendipitous findings.
本手法が、セレンディピティに基づく多様なレコメンデーションをユーザが楽しむための一助となれば幸いである。
Code available at https:
コードは https で公開しています。

![](https://developers.cyberagent.co.jp/blog/wp-content/uploads/2022/10/popularity_bias_fig1-768x296.jpg)

# 1. Introduction 1. はじめに

Recommendation systems are used in many domains such as ecommerce, movie, and music [4, 5, 19].
推薦システムは，電子商取引，映画，音楽など多くの領域で利用されている [4, 5, 19]．
Often recommendation systems learn the user preference from the implicit feedback information such as clicks, purchase, and item consumption [17, 26, 42].
推薦システムはしばしば，クリック，購入，消費などの暗黙のフィードバック情報からユーザの好みを学習する[17, 26, 42]．
Meanwhile, the systems are prone to popularity bias, which can come in many forms [2, 8, 9, 29].
一方，推薦システムは人気度バイアスに陥りやすく，様々な形で現れる[2, 8, 9, 29]．
From the data side, the user-item feedback data shows long tail distribution in item frequency with most interaction focused on small number of popular items (data bias) [2, 25].
データ側では，ユーザ・アイテムのフィードバックデータは，アイテム頻度のロングテール分布を示し，多くのインタラクションが少数の人気アイテムに集中する（データバイアス）[2, 25]．
From the model side, the recommendation systems, trained on such data, often give higher recommendation scores to more popular items even among items equally liked by a user, resulting in overrecommending popular items (model bias) [3, 34, 42].
一方，モデル側では，このようなデータをもとに学習した推薦システムは，ユーザが同じように好きなアイテムでも，より人気のあるアイテムに高い推薦スコアを与えることが多く，結果として人気のあるアイテムを過剰に推薦してしまう（モデルバイアス） [3, 34, 42]．
Furthermore, such biased recommendations to users could form a feedback loop which may result in filter bubble or echo chamber [6, 12, 22, 23].
さらに，このような偏った推薦がフィードバックループを形成し，フィルタバブルやエコーチェンバーを引き起こす可能性がある [6, 12, 22, 23]．

These varied forms of popularity bias often require individual approaches and solutions.
これらの多様な形の人気度バイアスは，しばしば個別のアプローチや解決策を必要とする．
The data bias could be solved in the data collection stage by controlling exposure bias [8, 9].
データバイアスは，データ収集の段階で露出バイアスを制御することで解決できる[8, 9]．
On the other hand, the model bias is a result of incorrect model training of the collected data [34, 42].
一方，モデルバイアスは収集したデータのモデル学習が正しく行われていないことが原因である[34, 42]．
Hence the model engineer needs to correctly train the model to give fair recommendations across all the items the user liked, instead of giving prioritized recommendations of popular items.
したがって，モデルエンジニアは，人気のあるアイテムを優先的に推薦するのではなく，ユーザが気に入った全てのアイテムに対して公平な推薦ができるようにモデルを正しく学習させる必要がある．
In this work, we focus on the solution of the model bias.
この研究では、モデルの偏りを解決することに焦点を当てる。
Our effort can be combined with additional solutions for data bias and feedback loop to systematically eliminate popularity bias.
我々の取り組みは、データの偏りやフィードバックループに対する追加の解決策と組み合わせることで、人気度バイアスを体系的に除去することができる。

A variety of methods have been proposed to tackle the popularity bias.
人気度バイアスに対処するために、様々な方法が提案されている。
These methods include inverse propensity weighting (IPW) [16, 27, 29], causal intervention [34, 36, 38, 40], and reranking [2, 37].
これらの手法には，逆傾向重み付け（IPW）[16, 27, 29]，因果関係介入[34, 36, 38, 40]，再ランキング[2, 37]が含まれる．
IPW aims to produce unbiased model prediction by weighting the imbalanced data with propensity weights [16, 27, 29].
IPWは、不均衡なデータを傾向性重みで重み付けすることにより、不偏のモデル予測を行うことを目的としている [16, 27, 29]。
Causal intervention methods attempt to model and remove the causal effect that item popularity has on the recommendation score [34, 36, 38].
因果的介入法はアイテムの人気が推薦スコアに与える因果的効果をモデル化し除去することを試みる[34, 36, 38]。
Reranking methods apply post-hoc ranking adjustment to the recommendation result [2, 37].
再ランキング法は，推薦結果に対してポストホックランキング調整を適用する[2, 37]．

However, these methods have limitations in solving model bias since they often suffer the accuracy-debias tradeoff.
しかし，これらの方法は，精度とバイアスのトレードオフに悩まされることが多く，モデルの偏りを解決するには限界がある．
These methods adjust the biased recommendation scores (or ranks) in proportion to item popularity; scores of popular items are discounted and unpopular items are boosted [1, 2, 8, 27, 34, 36].
このような手法では，アイテムの人気度に比例して，偏った推薦スコア（またはランク）を調整することができる．
Such mechanism may sacrifice the scores of positive items to uplift the scores of negative items [1, 2, 8, 34, 36], potentially harming accuracy.
このような機構は，ネガティブな項目のスコアを上げるためにポジティブな項目のスコアを犠牲にする可能性があり[1, 2, 8, 34, 36]，精度を損なう可能性がある．
Often such methods require extensive hyperparameter tuning to find an appropriate balance of accuracy and debias performance [34, 36, 42].
このような手法では，しばしば精度とデビアス性能の適切なバランスを見つけるために大規模なハイパーパラメータのチューニングが必要となる[34, 36, 42]．
A debias method that does not involve collective score
集合スコア

To this end, we propose a novel debias method to reduce model bias.
このため、我々はモデルの偏りを低減するための新しいデビアス法を提案する。
We refer to earlier studies of contrastive learning [11, 21], and propose to add a regularization term to the loss function to aid the recommendation system to predict equal recommendation scores across positive items for each user.
我々は対照学習に関する先行研究[11, 21]を参照し、推薦システムが各ユーザーのポジティブ項目間で等しい推薦スコアを予測することを支援するために、損失関数に正則化項を追加することを提案する。
Specifically, we extend the Bayesian Personalized Ranking Loss [26] which maximizes the score differences between positive and negative items, with a regularization term which minimizes the score differences within positive and negative items, respectively.
具体的には、正項目と負項目のスコア差を最大化するベイズパーソナライズランキングロス[26]に、正項目と負項目内のスコア差をそれぞれ最小化する正則化項を追加し、拡張したものである。
As a result, the recommendation system model will predict equal scores across positive items, solving the model bias.
その結果、推薦システムモデルは、ポジティブ項目間で同じスコアを予測し、モデルのバイアスを解決する。
Simultaneously, the model will contrast item scores for positive and negative items, maintaining high accuracy.
同時に、ポジティブ項目とネガティブ項目のスコアを対比させ、高い精度を維持することができる。
Few prior research took the similar approach of regulating the scores only for positive items [7, 42].
このような正則化項を導入した先行研究はほとんどない[7, 42]．
These studies introduced a regularization term penalizing the size of the Pearson correlation between item popularity and scores of positive items.
これらの研究では、項目の人気度とポジティブ項目のスコアとの間のピアソン相関の大きさにペナルティを課す正則化項を導入している。
Our method shares similar motivation while improving performance and cost efficiency.
本手法では，性能とコスト効率を向上させながら，同様の動機を共有する．

Our research proceeds as follows.
我々の研究は以下のように進められる。
We propose to extend the BPR loss with a new regularization term to achieve both high accuracy and high debias performance.
BPR損失を新しい正則化項で拡張し、高精度と高いデビアス性能を両立させることを提案する。
To systematically test the effectiveness of our method, we design a synthetic experiment.
本手法の有効性を系統的に検証するために、合成実験を計画する。
We design a data with explicit popularity bias which induces model bias when training a recommendation system using the baseline BPR loss.
まず，BPR損失を用いて推薦システムを学習する際に，モデルに偏りを生じさせるような明示的な人気度バイアスを持つデータを作成する．
We then apply our regularization term and analyze its performance.
そして、我々の正則化項を適用し、その性能を分析する。
As a result, our method outperformed earlier debias methods in terms of accuracy and debias performance.
その結果，本手法は従来のデビアス手法を精度およびデビアス性能の点で凌駕していた．
Additional comparison shows our method has advantages over the earlier methods in terms of computational validity and efficiency.
また，追加的な比較により，本手法が計算の妥当性と効率性の点で先行する手法よりも優れていることが示された．

We further conduct extensive empirical experiments utilizing 4 benchmark datasets [10, 13, 31–33], and 4 recommendation models:
さらに、4つのベンチマークデータセット[10, 13, 31-33]と4つの推薦モデルを用いた広範な実証実験を行った。
MF [26], NeuCF [15], NGCF [35], and LightGCN [14].
MF [26], NeuCF [15], NGCF [35], LightGCN [14]の4つの推薦モデルを用いた実証実験を行った．
The proposed method showed high accuracy and debias performance across MF, NGCF, LightGCN models in 3 of the 4 datasets, whereas the earlier methods failed to show consistent performance.
提案手法は，4つのデータセットのうち3つのデータセットにおいて，MF, NGCF, LightGCNモデルに対して高い精度とデビアス性能を示したが，先行手法では一貫した性能を示すことができなかった．
Hence, the proposed method showed general improvement over the earlier methods.
その結果，提案手法は，従来の手法に比べて全般的に改善されていることがわかった．

The contributions of our work are summarized as follows:
本研究の貢献は、以下のようにまとめられる。

- We propose a novel method to reduce model bias, by extending the existing BPR loss with a new regularization term which regulates the score differences within positive and negative items, respectively. 我々は、既存のBPRロスを拡張し、ポジティブ項目とネガティブ項目内のスコア差をそれぞれ調節する新たな正則化項でモデルの偏りを軽減する新しい方法を提案する。

- The proposed method shows high debias performance, minimal sacrifice in accuracy, with no additional training. 提案手法は、高いデビアス性能を示し、精度の犠牲は最小限であり、追加の学習は不要である。

- Quantitative and qualitative evaluation using a synthetic data is conducted to show advantages over earlier debias methods. 合成データを用いた定量的・定性的な評価を行い、従来のデビアス手法に対する優位性を示す。

- Empircal experiments using 4 benchmark datasets and 4 recommendation system models show the proposed method generally improved over earlier debias methods. 4つのベンチマークデータセットと4つの推薦システムモデルを用いた実証実験により，提案手法は従来のデバイアス手法よりも全般的に改善されていることが示された．

# 2. Related Work 2. 関連作品

## 2.1. Popularity Bias 2.1. ポピュラリティ・バイアス

Various studies have been conducted on popularity bias.
人気度バイアスについては様々な研究が行われている．
First, the popularity bias can be understood in terms of data (data bias) [2, 8, 25, 36, 38].
まず，人気度バイアスはデータの観点から理解することができる（データバイアス）[2, 8, 25, 36, 38]．
The user-item interaction data usually shows a long tail distribution in item popularity [2, 25].
ユーザとアイテムのインタラクションデータは，通常，アイテムの人気度にロングテールの分布を示す[2, 25]．
This may be due to selective item exposure [8, 9], as well as unequal preference of the users [38, 39].
これは，アイテムの選択的な露出[8, 9]や，ユーザの不平等な嗜好[38, 39]によるものと思われる．

On the other hand, the popularity bias also can be understood in terms of the recommendation system model (model bias).
一方，人気度の偏りは，推薦システムのモデル（モデルバイアス）の観点からも理解することができる．
Some studies addressed how the recommendation system trained on imbalanced data can amplify the bias in the data by over-recommending popular items than the data warrants [3, 7, 34, 38, 42].
アンバランスなデータに対して学習させた推薦システムが，データよりも人気のある項目を過剰に推薦することによって，データの偏りを増幅することを取り上げた研究がある [3, 7, 34, 38, 42]．
In particular, [42] defined such model bias as the degree the model gives higher scores to more popular positive items among positive items equally liked by a user.
特に，[42]では，モデルの偏りを「ユーザが同じように好きな正のアイテムの中で，より人気のある正のアイテムに高いスコアを与える度合い」と定義している．
Such model bias results in the recommendation system not being able to produce personalized recommendation, which could harm user experience.
このようなモデルの偏りは，推薦システムが個人化された推薦を行うことができなくなり，ユーザエクスペリエンスを損なう可能性がある．
In addition, some studies explore how over-recommendation can cause a feedback loop resulting in filter bubble or echo chamber [12, 22, 23].
また，過剰な推薦がフィードバックループを引き起こし，フィルタバブルやエコーチェンバーを引き起こすという研究もある [12, 22, 23]．

The varied forms of popularity bias require individual approaches and solutions.
人気度バイアスは様々な形で発生するため，個別のアプローチと解決策が必要である．
Since the data bias is caused by external selection bias [8, 9], a solution should be applied by controlling external factors in the data collection stage; simple debiasing of the collected data may distort the user preference shown in the data [38, 39].
データの偏りは外部からの選択バイアス[8, 9]に起因するため，データ収集段階で外部要因を制御することで解決する必要があり，収集したデータを単純にデビアスすると，データに示されるユーザの嗜好が歪んでしまう[38, 39]．
In contrast, the model bias is a computational problem where the model fails to learn the user preference from the collected data.
一方，モデルの偏りは，モデルが収集されたデータから ユーザーの嗜好を学習できない計算上の問題である．
Hence proper model training is required to remedy such bias, and allow the model to recommend items fairly across items of different popularity.
そのため，このようなバイアスを改善し，異なる人気度のアイテムを公平に推薦できるようにするためには，適切なモデル学習が必要である．
In addition, some researchers investigated solving the feedback loops or the filter bubble, which takes place in the online setting where the live system gives continual recommendation [6, 22].
さらに，オンラインシステムが継続的に推薦を行う際に生じるフィードバックループやフィルタバブルの解決についても研究されている [6, 22]．

Among various types of popularity biases, our work mainly focuses on the model bias.
様々な種類の人気度バイアスのうち、私たちは主にモデルバイアスに着目して研究を行っています。

## 2.2. Countering Popularity Bias 2.2. 人気度バイアスに対抗する

Various methods were proposed to address popularity bias, such as the inverse propensity weighting (IPW) [16, 27], causal intervention [34, 36, 38, 40], and reranking [2, 37].
人気度バイアスに対処するために，逆傾向重み付け（IPW）[16, 27]，因果関係介入[34, 36, 38, 40]，再ランキング[2, 37]など様々な方法が提案された．
IPW weights each training instance with the inverse of the item popularity to produce unbiased model prediction [16, 27, 29].
IPWは不偏のモデル予測を行うために、各トレーニングインスタンスをアイテムの人気度の逆数で重み付けする [16、27、29]。
Causal intervention often assumes a causal graph which models the effect item popularity has on the recommendation score, and computes counterfactual recommendation scores by removing such effect [34, 36, 38].
Causal interventionは，項目人気度が推薦スコアに与える影響をモデル化した因果グラフを仮定し，その影響を除去することで反実仮想的な推薦スコアを計算することが多い[34, 36, 38]．
Some works utilizes unbiased data to better learn the item embeddings [40].
また，アイテムの埋め込みをより適切に学習するために，不偏のデータを利用する研究もある[40]．
Reranking methods conduct ranking adjustment of item recommendation list [2, 37].
再順位付け法は，項目推薦リストの順位を調整する[2, 37]．

The above debias methods shares the logic of lowering the recommendation score of popular items and lifting those of unpopular items.
上記のデビアス法は、人気アイテムの推薦スコアを下げ、不人気アイテムの推薦スコアを上げるという論理を共有している。
For instance the IPW method lowers the training weights of popular items while lifting those of unpopular items [27, 29].
例えば、IPW法は人気アイテムの学習ウエイトを下げ、不人気アイテムの学習ウエイトを上げる[27, 29]。
The causal intervention methods often removes the causal effect of item popularity by discounting the recommendation scores proportionally to the item popularity [34, 36, 38].
因果的介入法は，アイテムの人気に比例して推薦スコアを割り引くことで，アイテムの人気による因果的効果を取り除くことが多い[34, 36, 38]．
The reranking method explicitly boosts the rank of the tail items while sacrificing the rank of popular items [2, 37].
また，再ランク付け法は，人気アイテムのランクを犠牲にする一方で，テールアイテムのランクを明示的にブーストする[2, 37]．
Although these measures could alleviate the model bias by balancing the recommendation scores, it holds the risk of overly penalizing the scores of positive items while compensating those of negative items.
これらの方法は，推薦スコアのバランスをとることでモデルのバイアスを軽減することができるが，ネガティブなアイテムのスコアを補う一方で，ポジティブなアイテムのスコアに過度にペナルティを与える危険性がある．
Hence accuracy may be sacrificed as part of the debias process.
そのため，デバイアス処理の一環として精度が犠牲になる可能性がある．

A debias method that regulates the recommendation score imbalance only for positive items may lead to successful debias with minimal sacrifice in accuracy.
また，推薦スコアのアンバランスを正項目のみで規制するデビアス手法は，精度を犠牲にすることなくデビアスに成功する可能性がある．
Few studies took such approach [7, 42].
このようなアプローチをとる研究はほとんどない[7, 42]．
The studies similarly proposed a method to regulate the Pearson correlation of item popularity and item score for positive items such that the recommendation scores can be independent of item popularity.
これらの研究では，アイテムの人気度とアイテムスコアのピアソン相関を正則化することで，アイテムの人気度に依存しないレコメンデーションスコアを実現する方法が提案されている．
However, the approach has two limitations: regularizing the correlation coefficient may not necessarily lead to independence, and computation is costly.
しかし，相関係数を正則化しても独立になるとは限らないこと，計算コストがかかること，という2つの制約がある．

Our work overcomes limitations of the earlier methods and proposes a cost-efficient debias method to reduce model bias while maintaining accuracy by regularizing recommendation scores.
本研究では、これまでの手法の限界を克服し、推薦スコアを正則化することで精度を維持しつつモデルの偏りを低減する、コスト効率の良いデビアス手法を提案する。

## 2.3. Contrastive Learning 2.3. 対照的な学習

Metric learning is a branch of machine learning which utilizes the distance or similarity of the training data to enhance learning [21].
計量学習は機械学習の一分野であり，学習データの距離や類似性を利用して学習を促進する[21]．
A related approach is contrastive learning which compares and contrasts training instances for efficient representation learning [18].
関連するアプローチとして、訓練事例を比較対照して効率的な表現学習を行う対照学習がある[18]。
Contrastive loss [11], triplet loss [28], infoNCE loss [24] are representative loss functions in contrastive learning which follow the basic principles - 1) learning similar representations for instances of the same category, and 2) learning contrasting representations for instances of different categories.
対照学習における代表的な損失関数として、Contrastive loss [11], triplet loss [28], infoNCE loss [24] があり、1）同じカテゴリのインスタンスに対しては類似表現を学習し、2）異なるカテゴリのインスタンスに対しては対照表現を学習するという基本原理に従っている。

A similar contrastive approach is used in the training of recommendation system models.
推薦システムモデルの学習においても、同様の対比的アプローチが用いられている。
The pairwise ranking loss [26] such as the Bayesian Personalized Ranking (BPR) loss is often used to train the relative ranking of positive and negative items by contrasting the recommendation scores.
推薦スコアを対比して肯定的項目と否定的項目の相対順位を学習するために、Bayesian Personalized Ranking (BPR) loss などのペアワイズランキングロス [26] がよく使われる。
However, unlike the contrastive learning losses, the BPR loss does not include a term to minimize the score differences within positive and negative items, respectively.
しかし、BPR損失は対比学習損失と異なり、肯定的項目と否定的項目それぞれの中のスコア差を最小化する項を含んでいない。
Extending the BPR loss to include a term to minimize the score differences within positive(negative) items can help in reducing the model bias while maintaining accuracy.
BPR損失を拡張し、正（負）項目内のスコア差を最小化する項を追加することで、精度を維持しつつモデルのバイアスを軽減することができる。

Although a few works studied contrastive learning in the context of recommendation systems [20, 41], these studies focused on the sampling scheme of negative items, and did not discuss how minimizing the positive and negative scores, respectively, can reduce the model bias.
推薦システムの文脈で対比学習を研究した研究はいくつかあるが[20, 41]，これらの研究では，ネガティブ項目のサンプリング方式に着目し，ポジティブスコアとネガティブスコアをそれぞれ最小化することでモデルのバイアスをどのように軽減できるかは議論されていない．
One study outside the context of contrastive learning took a similar approach of penalizing the score differences of the average recommendation scores across different item groups to promote fairness [43].
対照学習の文脈以外では，異なる項目群の平均推薦スコアのスコア差にペナルティを課すことで，公平性を促進するという同様のアプローチをとった研究がある[43]．
However, this study did not suggest a method to reduce the score differences at the individual item level.
しかし，この研究では，個々の項目レベルでのスコア差異を低減する方法は提案されていない．
To the best of our knowledge, our work is the first to introduce a method to reduce model bias while maintaining accuracy with a regularization term that minimizes the score differences within positive and negative items, respectively.
我々の知る限り，正項目内と負項目内のスコア差をそれぞれ最小化する正則化項を用いて，精度を維持しつつモデルの偏りを低減する方法を導入したのは，本研究が初めてである．

# 3. Preliminaries 3. 前段階

## 3.1. Implicit Recommendation System and Bayesian Personalized Ranking Loss 3.1. 暗黙のレコメンデーションシステムとベイズ型パーソナライズドランキングロス

Implicit recommendation systems are trained with implicit user feedback [14, 17, 26].
暗黙の推薦システムは，暗黙のユーザフィードバックを用いて学習する[14, 17, 26]．
Implicit data consists of tuple (u,i) meaning that a user $u \in U$ consumed an item $i \in I$.
暗黙のデータは，ユーザ$uがアイテム$iを消費したことを意味するタプル(u,i)から構成される．
We denote the set of items user u consumed as $Po_{s_u}$, since the items implicitly show the positive preference of u. In contrast, we denote the items that u did not consume as $Ne_{g_u}$.
uが消費したアイテムの集合を$Po_{s_u}$と呼ぶ．これは，uが消費しなかったアイテムを$Ne_{g_u}$と呼ぶ．
The recommendation system learns the preference of the users to produce a recommendation score $\hat{y_{ui}}$ based on the predicted preference useru has on itemi.
推薦システムは、ユーザの嗜好を学習し、ユーザuがアイテムiに対して持つ予測嗜好に基づき、推薦スコア$Chat{y_{ui}}$を生成する。
Subsequently, the item with the highest predicted score is recommended to the user.
その後、予測スコアが最も高い項目がユーザに推薦される。
Implicit recommendation systems are usually trained using the pairwise ranking loss such as the Bayesian Personalized Ranking (BPR) loss [14, 15, 26].
暗黙の推薦システムは通常、Bayesian Personalized Ranking (BPR) loss などのペアワイズランキング損失を用いて学習される[14, 15, 26]。
The BPR loss is given as Equation (1), where $\sigma()$ refers to the sigmoid function.
BPR損失は、式(1)のように与えられ、$ghesigma()$はシグモイド関数を指す。
The L2 regularization term is omitted for brevity.
L2正則化項は簡潔にするため省略した。

$$
Loss_{BPR} = - \sum_{u \in U} \sum_{p \in Po_{s_u}, n \in Ne_{g_u}} \log \sigma(\hat{y}_{u,p} - \hat{y}_{u,n})
\tag{1}
$$

During training, positive and negative items of each user are paired and the recommendation system learns to maximize the score differences between the paired items.
学習時には、各ユーザーのポジティブ項目とネガティブ項目をペアにして、ペアとなった項目間のスコア差を最大にするように推薦システムが学習する。
The accuracy of the recommendation system is evaluated based on how accurately the model scores positive items higher than negative items.
推薦システムの精度は、モデルがどれだけ正確に正の項目を負の項目より高く採点したかに基づいて評価される。
Common accuracy metrics such as Hit, NDCG [17] is computed based on the ranking of the positive test item relative to the negative test items.
Hit, NDCG [17]などの一般的な精度指標は、ネガティブテスト項目に対するポジティブテスト項目の相対的な順位に基づいて計算される。

## 3.2. Popularity Bias in Model Prediction (Model Bias) 3.2. モデル予測における人気の偏り（モデルバイアス）

The data used to train recommendation systems usually exhibits long-tail distribution in item popularity [2, 25].
推薦システムの学習に用いられるデータは，通常，アイテムの人気度がロングテール分布をしている[2, 25]．
Often, the recommendation systems trained with such data produce higher recommendation scores to more popular items even among items equally liked by a user [3, 34, 42].
このようなデータを用いて学習させた推薦システムでは，ユーザが同じように好きなアイテムであっても，より人気の高いアイテムの推薦スコアが高くなることがよくある[3, 34, 42]．
The tendency that recommendation systems show popularity bias in model prediction is what we refer to as model bias.
このように，推薦システムの予測に人気の偏りが生じることを，我々はモデルの偏りと呼んでいる．

A few prior research suggested metrics to measure the model bias [7, 42].
いくつかの先行研究では，モデルの偏りを測定するための指標を提案している[7, 42]．
One study [42] suggested a metric computing the popularityrank correlation for items (PRI).
ある研究[42]では，アイテムの人気度順位相関（PRI）を計算する指標を提案した．
PRI computes the Spearman rank correlation coefficient (SRC) of item popularity and the average ranking position, conditioned on the positive items.
PRIはアイテムの人気度と平均ランキング位置のスピアマン順位相関係数(SRC)を計算し，正項目を条件とする．
The PRI is given as in Equation (2):
PRIは式(2)のように与えられる。

$$
\text{PRI} = - \text{SRC} (\text{popularity} (I), \text{ave_rank} (I))
\tag{2}
$$

where the `ave_rank` of each item i is computed as follows: for each item i, we locate each user u who have i in Posu and compute the rank position quantile of i within $Po_{s_u}$.
ここで、各項目iの `ave_rank` は以下のように計算される：各項目iについて、Posuにiを持つ各ユーザーuを探し出し、$Po_{s_u}$内でのiのランク位置の分位数を計算する。
Then the rank position quantile is averaged across all user u who have i in $Po_{s_u}$.
次に、$Po_{s_u}$内でiを持つ全てのユーザuの順位位置の分位数を平均する。
Note that an item with smaller average rank quantile close to 0 means the item on average scores higher among the $Po_{s_u}$ of each user, whereas a greater average rank quantile close to 1 means that the item generally scores lower than other positive items.
なお、平均順位分位が0に近いほど小さい項目は、各ユーザーの$Po_{s_u}$の中で平均的にスコアが高い項目を意味し、1に近いほど大きい平均順位分位は、他の正の項目よりも一般的にスコアが低い項目を意味します。
Hence, a PRI value close to 1 implies the model gives higher scores to more popular items, and a PRI value close to 0 implies the model shows less model bias, since the popularity of positive items and the recommendation score ranking shows no correlation.
したがって，PRI 値が 1 に近いほど，人気のあるアイテムに高いスコアを与えるモデルであり，PRI 値が 0 に近いほど，ポジティブなアイテムの人気と推薦スコアランキングに相関がないため，モデルの偏りが少ないことを意味する．

We further propose a metric computing the average popularity quantile of the top scoring positive items of each user (PopQ@1) as in Equation (3):
さらに、各ユーザーの正項目の得点上位の平均人気度分位値（PopQ@1）を計算する指標を式（3）のように提案する。

$$
PopQ@1 = \frac{1}{|U|}\sum_{u\in U} \text{PopQuantile}_u(\argmax_{x\in Po_{s_u}}(\hat{y}_{ui}))
\tag{3}
$$

where $\text{PopQuantile}_u$ returns the popularity quantile of the item conditioned on $Po_{s_u}$ .
ここで、$text{PopQuantile}_u$ は、$Po_{s_u}$ を条件とするアイテムの人気度分位を返す。
The item of $Po_{s_u}$ which has the highest global popularity has a $\text{PopQuantile}_u$ of 0, and the item with the lowest global popularity has a $\text{PopQuantile}_u$ of 1. Hence, a` PopQ@1` value close to 0 implies high model bias, since the top scoring positive items of each user is usually the positive item with the highest global popularity.
Po_{s_u}$ のうち、グローバルな人気が最も高いアイテムは $text{PopQuantile}_u$ が 0 で、グローバルな人気が最も低いアイテムは $text{PopQuantile}_u$ が 1 である。したがって、各ユーザの正項目の得点上位は、通常グローバルな人気が最も高い正項目になるので、` PopQ@1` が 0 に近い場合はモデルの偏りが大きいことを意味する。
A `PopQ@1` value close to 0.5 implies no model bias, since the popularity quantile of the top scoring positive items is likely to be spread out across 0 and 1. Whereas the PRI computes the overall correlation between the item popularity and the average rank for all positive items, `PopQ@1` focuses on the popularity quantile only for the top scoring positive items which has a high chance of being recommended.
一方、PopQ@1 の値が 0.5 に近い場合は、人気度分位が 0 と 1 の間に分散している可能性が高いため、モデルの偏りがないことを意味する。 PRI がアイテムの人気度と全正項目の平均順位との相関を計算するのに対し、PopQ@1 は推奨される可能性の高いトップスコア正項目の人気度分位に注目するものである。
The two metrics allow detailed evaluation of the model bias.
この2つの指標により、モデルの偏りを詳細に評価することができる。

A recommendation system should be trained to achieve both high accuracy and low model bias.
推薦システムは、高い精度と低いモデルバイアスの両方を達成するように学習させる必要がある。
The accuracy and debias performance of a recommendation system is often orthogonal.
推薦システムの精度とデビアス性能は直交していることが多い。
Accuracy metrics measure how well the system distinguishes between positive and negative preference, while debias metrics assess how item popularity is (un)correlated with recommendation score conditioned on positive items.
精度の指標はシステムがどの程度ポジティブな嗜好とネガティブな嗜好を区別できるかを評価し、デビアスの指標はアイテムの人気がポジティブなアイテムを条件とした推薦スコアとどの程度（非）相関しているかを評価するものである。
Note that it is important for the recommendation system to maintain accuracy while reducing model bias.
推薦システムにとって重要なことは、モデルの偏りを抑えながら精度を維持することである。
A system with low model bias but also low accuracy can not give personalized recommendations.
モデルの偏りが少なくても精度が低ければ、個人に合った推薦を行うことはできません。
For instance, a model giving random recommendation would show no model bias but does not consider the user preference at all.
例えば、ランダムな推薦を行うモデルは、モデルの偏りを示さないが、ユーザの嗜好を全く考慮しない。

## 3.3. Visual Illustration on Synthetic Data 3.3. 合成データでの視覚的な説明

Throughout the study, we design a synthetic data with explicit data bias to illustrate model bias and subsequent debias performance of various methods.
本研究では、モデルの偏りとそれに続く様々な手法のデバイアス性能を説明するために、データの偏りを明示した合成データを設計する。
The synthetic data is a 200 x 200 user-item interaction matrix R. The matrix is filled with binary interaction information such that the item popularity linearly decreases as the item index increases, as seen in Equation (4).
合成データは200 x 200のユーザとアイテムの相互作用行列Rであり、式（4）に見られるように、アイテムのインデックスが増加するにつれてアイテムの人気が直線的に減少するように、行列はバイナリ相互作用情報で満たされている。
Although such data deviates from the sparse and noisy real-world data, it provides a systematic way to observe how a recommendation system exhibits model bias.
このようなデータは、疎でノイズの多い実世界のデータからは逸脱しているが、推薦システムがどのようにモデルの偏りを示すかを観察する体系的な方法を提供するものである。

$$
R[u,i] = 1 ( \text{if} i + j <= 200) \\
R[u, i] = 0 ( o.w. )
\tag{4}
$$

Using such data, we train a matrix factorization (MF) model, which is a basic collaborative filtering recommendation system [30].
このようなデータを用いて、協調フィルタリング推薦システムの基本である行列因子法（MF）モデルを学習する[30]。
We use BPR loss as the loss function [26].
損失関数としてBPR損失を用いる[26]。
Figure 1a shows the synthetic data in matrix form: the white area corresponds to positive items, and the black negative items.
図1aは合成データを行列形式で表したもので、白い部分が正の項目、黒い部分が負の項目に相当する。
Figure 1b shows the recommendation score of the trained MF model, showing salient model bias.
図1bは学習したMFモデルの推薦スコアであり、モデルの偏りが顕著に表れている。
The popular items (smaller item index) shows higher score even when conditioned on the positive items.
肯定的な項目を条件とした場合でも、人気のある項目（項目インデックスが小さい）ほど高いスコアを示している。
For instance, for user index 100, the model predicts higher score to popular items of index 0 ~ 20, even though the user equally consumed items from index 0 ~ 100.
例えば、ユーザインデックスが100の場合、ユーザはインデックス0〜100のアイテムを同じように消費しているにもかかわらず、モデルはインデックス0〜20の人気アイテムに高いスコアを予測する。

The accuracy and debias performance of the model was quantitatively evaluated.
モデルの正確さとデビアス性能は定量的に評価された．
To measure accuracy, the average frequency of the positive item being scored higher than the negative item was computed over all positive-negative item pairs.
精度は，正項目と負項目の組で，正項目が負項目より高いスコアを獲得する頻度の平均を計算した．
We report the error rate ((1-accuracy)\*100) of 0.01%.
その結果，誤差（(1-accuracy)Γ*100）は0.01%であった．
Hence, the model trained with the BPR loss shows high accuracy.
したがって，BPR損失を用いて学習したモデルは高い精度を示していることがわかる．
The debias performance was evaluated using the PRI and `PopQ@1` metrics.
また、PRIとPopQ@1`という指標を用いてデビアス性能を評価した。
Figure 1c shows the average item rank quantile of the items, where the x axis shows the item index of the synthetic data (items with smaller x index is more popular).
図1cは、x軸が合成データのアイテムインデックスを示し、アイテムの平均ランク分位を示したものである（xインデックスが小さいアイテムほど人気がある）。
Specifically, we see the most popular item on average is ranked at the top 0.0% among the positive items; and as the item popularity decreases, the item no longer has the highest rank.
具体的には、平均的に最も人気のあるアイテムは、正のアイテムの中で上位0.0%にランクされており、アイテムの人気が低下すると、そのアイテムはもはや最高ランクではなくなりました。
This indicates high model bias, and the PRI is also computed at 0.99.
これはモデルの偏りが大きいことを示しており、PRIも0.99と計算される。
Figure 1d shows the histogram of the popularity quantile of top scoring positive items of each user.
図1dは、各ユーザの肯定的なアイテムの上位得点の人気度分位をヒストグラムにしたものである。
We see the popularity quantile is focused around 0, meaning the top scoring positive items mostly consists of the most popular positive items of each user.
人気度分位は0付近に集中しており、上位得点の正項目はほとんど各ユーザーの最も人気のある正項目で構成されていることが分かります。
Taking the mean of the 200 quantiles, the `PopQ@1` is computed at 0.02.
200の分位数の平均をとると、`PopQ@1`は0.02となる。
Both PRI and `PopQ@1` metrics indicate the model trained with the BPR loss showing high model bias.
PRIとPopQ@1`の両メトリクスは、BPR損失で学習したモデルが高いバイアスを示していることを示している。

# 4. Proposed Method 4. 提案された方法

## 4.1. Regularization Term ot Minimize Score Difference 4.1. スコア差を最小化する正則化項

To reduce model bias, we propose a method to extend the BPR loss with an additional regularization term which minimizes the score differences between positive and negative items, respectively.
モデルの偏りを減らすために、我々はBPR損失に正則化項を追加して拡張し、正負項目間のスコア差をそれぞれ最小化する方法を提案する。
Thus while the BPR loss contrasts the recommendation scores between positive and negative items, the regularization term will additionally force the scores to be equal within positive(negative) items.
このように、BPR損失はポジティブ項目とネガティブ項目の推薦スコアを対比させるが、正則化項はさらに、ポジティブ（ネガティブ）項目内でスコアが等しくなるように強制する。
Thus the model can achieve both high accuracy and debias performance.
このように、このモデルは高い精度とデビアス性能の両方を達成することができる。
We propose a total loss function of the following form as in Equation (5):
我々は、式(5)のような形の全損失関数を提案する。

$$
\text{Total Loss} = \text{BPR Loss} + \text{Reg Term} \tag{5}
$$

We propose two variations of regularization term:
我々は、正則化項のバリエーションを2つ提案する。

- Pos2Neg2 Term : 2 positive and 2 negative items are sampled per user at a time, and the score difference of the positive(negative) items are minimized, respectively. Pos2Neg2 Term : 1ユーザにつき2つの正項目と2つの負項目を同時にサンプリングし、それぞれ正項目（負項目）のスコア差を最小にする。

$$
\text{Reg Term} = - \sum_{u \in U} \sum_{p_1, p_2 \in Po_{s_u}, n_1, n_2 \in Ne_{g_u}}
\log (1 - \tanh(|\hat{y}_{u, p_1} - \hat{y}_{u, p_2}|))
+ \log (1 - \tanh(|\hat{y}_{u, n_1} - \hat{y}_{u, n_2}|))
\tag{6}
$$

- Zerosum Term : 1 positive and 1 negative item is sampled per user at a time, and the sum of the recommendation scores of positive and negative items is regularized to be close to 0. Through training, the regularization will propagate across random positive-negative item pairs of the user, forcing the positive and negative items to have symmetric recommendation scores. Eventually, the scores of the positive items of the user will converge to a single value, while the scores of the negative items converge to a symmetric value. ゼロサム項 : 一人のユーザに対して正項目と負項目をそれぞれ1つずつ抽出し、正項目と負項目の推薦スコアの和が0に近づくように正則化する。学習により、正則化はユーザのランダムな正負項目ペアに伝播し、正項目と負項目が対称的な推薦スコアを持つことを余儀なくされる。 最終的には、肯定的な項目のスコアは単一の値に収束し、否定的な項目のスコアは対称的な値に収束する。

$$
\text{Reg Term} = - \sum_{u \in U} \sum_{p \in Po_{s_u}, n \in Ne_{g_u}}
\log (1 - \tanh(|\hat{y}_{u, p} + \hat{y}_{u, n}|))
\tag{7}
$$

Both of the regularization terms aim to reduce model bias by leading the model to give equal scores to positive(negative) items.
どちらの正則化項も、正（負）の項目に対して等しいスコアを与えるようにモデルを導くことで、モデルの偏りを減らすことを目的としている。
Such approach has two advantages.
このようなアプローチには2つの利点がある．
First, it is robust to the accuracydebias tradeoff.
第一に，精度とバイアスのトレードオフに対してロバストである．
In contrast to debias methods collectively adjusting the scores for all items, the proposed method does not sacrifice the scores of positive items to boost those of the negative items.
全項目のスコアを一括して調整するデビアス手法とは対照的に，提案手法は正項目のスコアを犠牲にして負項目のスコアを上げることがない．
The second advantage is the simplicity.
第二の利点は，単純であることである．
The proposed method is applicable to any model which uses the BPR loss, with no additional training.
提案手法はBPR損失を用いるどのようなモデルにも適用可能であり，追加の学習は不要である．

Finally, experiments showed only regularizing the scores of positive items lead to deteriorated accuracy, hence regularization is applied for both positive and negative items.
最後に、実験では正項目のスコアだけを正則化すると精度が悪化することがわかったので、正項目と負項目の両方に正則化を適用している。

## 4.2. Illustration of the Proposed Method on the Synthetic Data 4.2. 合成データにおける提案手法の説明

We test the debias performance of the proposed methods using the synthetic data.
合成データを用いて、提案手法のデビアス性能を検証する。
We add the regularization term to the BPR loss and train the matrix factorization model to see if the model bias exhibited in the baseline training is alleviated.
BPR損失に正則化項を追加し、行列分解モデルを学習させ、ベースライン学習で見られたモデルの偏りが緩和されるかどうかを確認する。
Note, the baseline refers to the method of using BPR loss for training.
なお、ベースラインとは、BPR損失を用いて学習を行う方法のことである。
Figure 2 shows the model prediction when using the baseline BPR loss as well as the proposed methods.
図2は、ベースラインBPR損失と提案手法を用いた場合のモデル予測値である。
Whereas the baseline BPR loss resulted in high model bias in Figure 2a, the proposed methods show equal scores across positive items for each user (Figure 2b, 2c), while accurately contrasting the scores between positive and negative items.
ベースラインBPRロスを用いた場合、図2aではモデルの偏りが大きくなるのに対し、提案手法では、各ユーザーのポジティブ項目でスコアが均等になり（図2b、2c）、ポジティブ項目とネガティブ項目のスコアが正確に対比されることがわかります。
Such qualitative analysis shows high debias and accuracy performance of the proposed methods.
このような定性的な分析から、提案手法の高いデビアス性能と精度性能が示されました。

Next we quantitatively analyze the accuracy and debias performance.
次に、精度とデビアス性能を定量的に分析する。
Table 1 shows the error rate of the proposed methods compared to the baseline.
表1は提案手法の誤差をベースラインと比較したものである．
Both Pos2Neg2 and Zerosum method show low error rate, and the Zerosum method even shows higher accuracy than the baseline.
Pos2Neg2法、Zerosum法ともに誤差が少なく、Zerosum法はベースラインよりも高い精度を示しています。
For the debias performance, the upper graph of Figure 2d, 2e, 2f show the average rank quantile of the positive items.
デビアス性能については、Figure 2d, 2e, 2fの上段のグラフは、正項目の平均順位分位数を示しています。
For the proposed methods, we see the average rank is around 0.25 ~ 0.75 for most of the items including the popular items (small item index), meaning the ranking is no longer affected by popularity.
提案手法では、人気アイテム（小アイテムインデックス）を含むほとんどのアイテムで平均順位が0.25～0.75程度となり、順位が人気の影響を受けなくなったことがわかる。
However, the few tail items with least popularity (item index 190 ~ 200) is still ranked at the bottom on average, indicating the debias was not effective for tail items.
しかし、人気度の低いテールアイテム（アイテムインデックス190〜200）は依然として平均順位が最下位であり、テールアイテムに対してデビアスは有効でなかったことがわかる。
Similarly, Table 1 shows the PRI of the proposed methods are reduced from 0.99 to 0.42 and 0.50, respectively.
同様に、表1より提案手法のPRIはそれぞれ0.99から0.42、0.50に減少していることがわかる。
The lower graph of Figure 2d, 2e, 2f show the histogram of popularity quantiles of the top scoring positive items of each user.
図2d, 2e, 2fの下のグラフは、各ユーザの正項目の得点上位の人気度分位値のヒストグラムである。
For both Pos2Neg2 and Zerosum methods, the popularity quantiles are spread across 0 ~ 1. We see in Table 1 that the `PopQ@1` is computed at 0.62 and 0.61, respectively, which is closer to the ideal 0.5.
Pos2Neg2法、Zerosum法ともに、人気度分位は0〜1に広がっている。表1より、PopQ@1`はそれぞれ0.62、0.61と計算され、理想の0.5により近づいていることがわかる。
All of these results show that both of the proposed regularization terms have the effect of reducing model bias while maintaining high accuracy.
これらの結果から、提案した正則化項はいずれも高い精度を維持しつつ、モデルの偏りを低減する効果があることがわかる。

Finally, we compare the proposed methods.
最後に、提案手法を比較する。
The Zerosum method reports higher accuracy than the Pos2Neg2 method.
Zerosum法はPos2Neg2法よりも高い精度を報告した。
We suggest two explanations.
我々は2つの説明を提案する．
One reason may be due to the wider range of item pairing of the Zerosum method.
一つは、Zerosum法の方が項目の組合せの範囲が広いためと考えられる。
Figure 2b shows the Pos2Neg2 method failing to distinguish positive and negative preference for users with low item consumption (user index 180 ~ 200), whereas in Figure 2c the Zerosum method showed accurate predictions for the same users.
図2bは、Pos2Neg2法がアイテム消費量の少ないユーザ（ユーザ指数180～200）に対して、ポジティブ嗜好とネガティブ嗜好を区別できないことを示しているのに対し、図2cではZerosum法が同じユーザに対して正確な予測を示している。
For users with small positive item consumptions, the Pos2Neg2 method may suffer from limited choices in positive item pairing, whereas the Zerosum method selects a pair for the positive items from the negative items.
Pos2Neg2法は、正項目の消費量が少ないユーザに対して、正項目と負項目の組を選択することができますが、Zerosum法は、負項目と正項目の組を選択するため、正項目の消費量が少ないユーザに対しては、正項目の組の選択肢が少なくなることが予想されます。
Consequently, the Pos2Neg2 method may not be able to learn the preference of some users due to limited range of training samples.
その結果，Pos2Neg2法は，学習サンプルの範囲が狭く，一部のユーザの嗜好を学習できない可能性がある．
The second reason may be due to the symmetric scoring effect of the Zerosum method.
第二の理由は，Zerosum法の対称的なスコアリング効果によるものと考えられる．
Figure 2b shows the Pos2Neg2 method gives unequal scores for negative items for different users, whereas Figure 2c shows the Zerosum method gives equal scores to negative items across different users, which also forms a symmetry with the positive items.
図2bは、Pos2Neg2法がユーザごとに負の項目に対して不均等なスコアを与えているのに対し、図2cは、Zerosum法がユーザごとに負の項目に対して均等なスコアを与え、それが正の項目と対称性を形成していることを示しています。
The different score distribution of the Pos2Neg2 method may lead to unequal training for item pairs of different users, whereas the training is uniform for those of the Zerosum method.
Pos2Neg2法のスコア分布が異なるため、ユーザが異なると項目ペアの学習が不均等になるのに対し、Zerosum法のものは均一に学習されることが考えられます。
In sum, we conclude that the Zerosum is more than a simplified version of the Pos2Neg2 method but has additional effect of promoting accuracy.
以上のことから、ZerosumはPos2Neg2法の簡易版である以上に、精度を向上させる効果があることがわかった。
Hence, we present the Zerosum term as our main proposed method and contribution.
したがって、我々はZerosum項を主要な提案手法として提示し、貢献する。

# 5. Advangtages of the Proposed Method 5. 提案手法の長所

We compare the performance of the proposed method with earlier debias methods: inverse propensity weighting (IPW) [16, 27], causal intervention [36, 38, 40], reranking [2, 37], and Pearson regularization method [42].
我々は提案手法の性能を，先行するデビアス手法である逆傾向重み付け(IPW) [16, 27]，因果関係介入[36, 38, 40]，再ランク[2, 37]，Pearson正規化法 [42] と比較検討する．
The IPW method applies weights to the training instance to reduce the data bias, where the weight is inverse to the item popularity [16, 27].
IPW法はデータの偏りを減らすために学習インスタンスに重みを適用し、ここで重みは項目の人気度に逆である[16, 27]。
Causal intervention models the causal effect the item popularity has on the recommendation score and removes such effect [36, 38].
Causal intervention はアイテムの人気度が推薦スコアに与える因果関係をモデル化し，その効果を除去する[36, 38]．
We select the state of the art PD (Popularity-bias Deconfounding) method for comparison [38].
比較のために，最先端の PD (Popularity-bias Deconfounding) 法を選択する[38]．
The reranking method applies post-hoc rank adjustment of the recommendation list.
この手法では，推薦リストのランクを事後的に調整する．
However, in the context of model bias this corresponds to the oracle method, hence comparison is not appropriate.
しかし，モデルバイアスの文脈では，これはオラクル法に相当するため，比較は適切でない．
Finally [42] suggested to reduce the model bias by adding a regularization term to the loss function to force the Pearson correlation of item popularity and recommendation score to be close to 0, conditioned on the positive items.
最後に[42]は，損失関数に正則化項を追加し，正の項目を条件として，項目の人気度と推薦スコアのピアソン相関を0に近づけることで，モデルの偏りを軽減することを提案している．
We first overview the debias performance of IPW, PD, and Pearson methods, then conduct in-depth comparison with the proposed method.
本稿では，まずIPW法，PD法，Pearson法のデビアス性能を概観し，次に提案手法との詳細な比較を行う．

## 5.1. Performances of Earlier Methods 5.1. 先行手法の性能

Each debias methods (IPW, PD, Pearson) was applied to the training of MF model on the synthetic dataset.
合成データセットに対するMFモデルの学習には，各デビアス手法（IPW，PD，Pearson）が適用された．
Figure 3 shows the model score results.
図3はモデルのスコア結果である。
Figure 3a shows the IPW method was not able to clearly distinguish the contrasting preference between positive and negative items.
図3aより、IPW法はポジティブ項目とネガティブ項目の対比的な選好を明確に区別することができないことがわかる。
Moreover, the method was not able to reduce model bias as seen in the results of Figure 3d.
また、図3dの結果からわかるように、この手法はモデルの偏りを減らすことができなかった。
Figure 3b shows the PD method performed satisfactory debias performance, while also accurately distinguishing positive and negative preference.
図3bは、PD法が満足のいくデビアス性能を発揮し、かつ、ポジティブとネガティブの嗜好を正確に区別していることを示している。
However the debias is not even throughout the items.
しかし、デビアスは全ての項目で均一ではありません。
This is also reflected in Figure 3e, where the upper graph of Figure 3e shows the average item rank quantile exhibiting a curved shape, with the most popular item still being ranked at the top.
これは図3eにも反映されており、図3eの上側のグラフでは、平均的な項目のランク分位が曲線的な形状を示し、最も人気のある項目が依然として上位にランクされていることがわかる。
The lower graph shows about half of the popularity quantiles focused on value close to 0. Figure 3c shows the Pearson method resulted in low scores of popular items for some users (e.g. user index 0 ~ 20) while it is high for other users (e.g. user index 100 ~ 200).
図3cは、Pearson法では、あるユーザ（例：ユーザインデックス0〜20）では人気アイテムのスコアが低く、他のユーザ（例：ユーザインデックス100〜200）では高くなることを示している。
This indicates the method penalized the scores of popular items for some users to force the Pearson correlation coefficient close to 0. However, such superficial balancing of scores is undesirable because it introduces additional model bias of different directions.
これは、ピアソン相関係数を0に近づけるために、一部のユーザの人気アイテムのスコアにペナルティを与えていることを示している。しかし、このような表面的なスコアのバランスは、異なる方向のモデルのバイアスを追加するため、望ましくない。
For instance, now the popular items are under-recommended to users of index 0 ~ 20.
例えば、現在、指数0〜20のユーザには、人気アイテムはあまり推奨されていない。
The upper graph of Figure 3f shows that the average rank quantile of the popular items (item index 0 ~ 20) is close to 0.5, but the model bias is not reduced for the rest of the items.
図3fの上のグラフは、人気アイテム（アイテムインデックス0〜20）の平均ランク分位が0.5に近いことを示しているが、残りのアイテムについてはモデルのバイアスが減少していないことがわかる。
The lower graph of Figure 3f shows fair spread of popularity quantiles.
図3fの下側のグラフは、人気順位の分位数が公平に広がっていることを示している。

The accuracy and debias performance metrics of the earlier methods is reported in Table 2.
表2は、先行手法の精度とデビアス性能の指標を示したものである。
All of the earlier methods showed worse accuracy performance compared to the Zerosum method.
すべての先行手法はZerosum手法に比べ、精度が低いことがわかった。
The methods also showed worse debias performance with IPW showing no debias effect; PD reporting PRI value of –0.52, indicating the model favoring unpopular items; and the Pearson method reporting a high PRI value of 0.80.
IPWはデビアス効果を示さず，PDは-0.52のPRI値を報告しており，これはモデルが不人気な項目を好んでいることを示している．
Both PD and Pearson reports a `PopQ@1` value around 0.3, which is farther from 0.5 than the Zerosum method.
PDとPearsonは共に`PopQ@1`の値を0.3程度と報告し、Zerosum法よりも0.5から遠い。

## 5.2. Comparing the Zerosum Method with the PD Method 5.2. Zerosum 法と PD 法の比較

The PD method has two limitations in terms of computational validity and efficiency compared to the Zerosum method.
PD法は、Zerosum法と比較して、計算の妥当性と効率の面で2つの制約がある。
Methods such as PD adjusts the biased recommendation scores by lowering the scores of popular items while boosting the scores of unpopular items.
PD法のような方法は、人気のある項目のスコアを下げ、不人気の項目のスコアを上げることで、偏った推薦スコアを調整する。
This score adjusting scheme can lower the scores of positive items while boosting those of negative items, potentially leading to accuracy-debias tradeoff.
このスコア調整方式は、ポジティブな項目のスコアを下げ、ネガティブな項目のスコアを上げるため、精度とバイアスのトレードオフを引き起こす可能性がある。

Such debias method has further limitation in terms of computational validity because the score adjusting scheme is often heuristically designed instead of being based on the computational mechanism of the recommendation model [36, 38, 42].
このようなデビアス法は、スコア調整方式が推薦モデルの計算機構に基づくのではなく、ヒューリスティックに設計されることが多いため、計算の妥当性の点でさらなる限界がある[36, 38, 42]。
For instance the PD method uses the formula $\text{model score} = ELU (debiased score)\times(item pop)^a$ to derive the debiased score [38].
例えば、PD法では、$text{model score} = ELU (debiased score)\times(item pop)^a$という式を用いて、debiased scoreを導出している[38]。
However, this formula may not generalize to other recommendation models with different computational process.
しかし、この式は、計算過程の異なる他の推薦モデルに対して一般化できない可能性がある。
In contrast, the logic of the Zerosum method is generalizable to other models.
これに対し、Zerosum法の論理は他のモデルにも一般化可能である。
To elaborate, we test how the Zerosum and PD method perform when switching the recommendation system model from matrix factorization to a different model such as NeuCF [15].
そこで、推薦システムのモデルを行列分解法からNeuCF[15]などの別のモデルに変更した場合、Zerosum法とPD法がどのように作用するかを検証する。
The score result of the baseline BPR loss, Zerosum, and PD method, when training the NeuCF model is compared.
NeuCFモデルを学習させたときのベースラインBPR損失、Zerosum、PD法のスコア結果を比較する。
Figure 4a shows the baseline prediction of the NeuCF model differs from when using matrix factorization.
図4aより、NeuCFモデルのベースライン予測は、行列分解を用いた場合とは異なることがわかる。
Figure 4c shows PD method performed poorly despite extensive hyperparameter tuning, whereas Figure 4b shows the Zerosum method continued to excel.
図4cは、PD法がハイパーパラメータを大幅に調整したにもかかわらず、パフォーマンスが低いことを示しており、図4bは、Zerosum法が引き続き優れていることを示しています。
This is also seen in Table 3.
このことは表3にも表れています。
In terms of computational efficiency, methods such as PD often require costly hyperparameter tuning to adjust the accuracy and debias performance.
計算効率の面では、PD法などは精度やデビアス性能を調整するために、コストのかかるハイパーパラメータのチューニングが必要になることが多いのです。
In contrast, the Zerosum method trains the model to simultaneously achieve high accuracy and debias performance without additional hyperparameter tuning.
これに対し、Zerosum法では、ハイパーパラメータのチューニングを追加することなく、高精度とデビアス性能を同時に達成するようにモデルをトレーニングします。

## 5.3. Comparing the Zerosum Method with the Pearson Method 5.3. Zerosum 法と Pearson 法の比較

Some works suggested penalizing the size of the correlation value between item popularity and item scores conditioned on the positive items, in addition to the original loss function [7, 42].
いくつかの研究では，本来の損失関数に加えて，項目人気度と項目得点の相関値の大きさを正の項目で条件づけることを提案している[7, 42]．
This strategy aims to balance only the scores of positive items without boosting the negative items.
この方法は，ネガティブアイテムをブーストすることなく，ポジティブアイテムのスコアのみをバランスさせることを目的としている．
Therefore, such method can be more robust to accuracy-debias tradeoff.
したがって，この方法は精度とバイアスのトレードオフに対してよりロバストである．
Indeed, the Zerosum method shares similar motivation.
実際，Zerosum 法も同様の動機を持っている．

However such Pearson regularization method also has two limitations.
しかし、このようなPearson正則化法にも2つの限界がある。
In terms of computational validity, we see from Figure 3c that the Pearson method selectively lowered the scores of popular items to bring the correlation coefficient close to 0; without achieving the intended independence between item popularity and score.
計算の妥当性という点では、図3cから、Pearson法は人気項目のスコアを選択的に下げて相関係数を0に近づけており、意図した項目の人気とスコアの独立性が達成されていないことがわかる。
In contrast, the Zerosum method employs a simpler logic which is effective in directly predicting debiased scores.
これに対し、Zerosum法はより単純なロジックを採用しており、劣化したスコアを直接予測するのに有効である。
In terms of computational efficiency, the Pearson method requires the costly computation of all positive items scores for one step of training.
計算効率の面では、Pearson法では1回の学習ですべての正項目のスコアを計算する必要があり、計算コストがかかる。
In contrast, the Zerosum method allows efficient mini-batch training which integrates naturally with the BPR loss.
これに対し、Zerosum法では、BPRの損失と自然に統合された効率的なミニバッチ学習が可能である。

# 6. Empirical Experiments 6. 実証実験

We conduct experiments to validate the effectiveness of the proposed method.
提案手法の有効性を検証するために、実験を行う。

## 6.1. Experimental Settings 6.1. 実験設定

6.1.1 Data.
6.1.1 データ
We use Movielens [13], Gowalla [10], Goodreads [32, 33], and Ciao [31] datasets.
我々は、Movielens [13], Gowalla [10], Goodreads [32, 33], and Ciao [31] datasetsを使用する。
The datasets were preprocessed to filter out users and items with too few interactions.
これらのデータセットは、インタラクションが少なすぎるユーザーとアイテムをフィルタリングするために前処理された。
The details of the preprocessed data is in Table 4.
前処理されたデータの詳細は表 4 にある．

6.1.2 Recommendation Systems Models.
6.1.2 推薦システムモデル。
We used BPR-MF [26], NeuCF [15], NGCF [35], and LightGCN [14]; ranging from classical matrix factorization to the state of the art graph neural networks models.
我々は、BPR-MF [26], NeuCF [15], NGCF [35], LightGCN [14] を用いた。古典的な行列分解から最新のグラフニューラルネットワークモデルに至るまで、様々なモデルを使用した。

6.1.3 Comparison Methods.
6.1.3 比較方法。
The following methods are compared.
以下の方法を比較する。
Baseline is training the model with the BPR loss [26].
ベースラインはBPR損失でモデルを学習する[26]。
IPW weights each training instance with the inverse of item popularity [27].
IPWは各訓練インスタンスに項目人気度の逆数で重み付けを行う[27]。
PD is a causal intervention method which divides a factor proportional to the item popularity from the predicted score.
PD は予測スコアからアイテム人気度に比例した因子を除算する因果的介入法である．
The hyperparameter $\gamma$ was tuned in the range of $\gamma \in [0.05, 0.25]$ [38].
ハイパーパラメータ$gamma$は$gamma \in [0.05, 0.25]$の範囲でチューニングされている[38]。
MACR is a causal intervention method that subtracts a factor proportional to the item popularity from the predicted score.
MACRは予測スコアから項目人気度に比例した係数を減算する因果的介入法である．
The hyperparameter c was tuned in the range of $c \in [0, 30]$ [36].
ハイパーパラメータcは$c \in [0, 30]$ [36]の範囲でチューニングされている。
Pearson method regulates the square of the Pearson correlation between the item popularity and item recommendation scores of positive items.
Pearson 法は，正項目の人気度と項目推薦スコアの Pearson 相関の二乗を調節する．
The weight of the regularization term was tuned in the range of ${1e1, 1e2, 1e3, 1e4}$ [42].
正則化項の重みは${1e1, 1e2, 1e3, 1e4}$の範囲でチューニングされている[42]．
Post-Process reduces the model bias by adjusting the model scores according to item popularity.
ポストプロセスでは，アイテムの人気度に応じてモデルのスコアを調整し，モデルの偏りを軽減する．
The hyperparameter α, β was tuned in the range of $\alpha \in [0.1, 1.5]$, $\beta \in [0.0, 1.0]$ [42].
ハイパーパラメータα、βは$alpha \in [0.1, 1.5]$, $beta \in [0.0, 1.0]$ の範囲でチューニングされている[42]。
Zerosum is the proposed method which extends the BPR loss with a term which regulates the sum of paired positive and negative item scores of each user to be close to 0. The weight of the term is fixed at 0.1 for all experiments.
Zerosumは、各ユーザーの正負の項目スコアの和が0に近くなるように制御する項をBPR損失に追加する提案手法であり、すべての実験において項の重みは0.1に固定されている。

6.1.4 Training.
6.1.4 トレーニング
Positive data was split into 60%, 20%, 20% for train, test, validation.
ポジティブデータを60%, 20%, 20%に分割し、トレーニング、テスト、バリデーションを行った。
For each user, 100 test negative items were selected before training.
各ユーザについて、学習前にテスト用のネガティブアイテムを100個選択した。
The same learning rate (0.001), batch size (2048), and embedding size (64 dim for MF, NeuCF model, and 10 dim with 3 GCN layers for NGCF, LightGCN) was used for each combination of (data, model, debias method).
学習率（0.001）、バッチサイズ（2048）、埋め込みサイズ（MF、NeuCFモデルは64dim、NGCF、LightGCNはGCN3層で10dim）は、（データ、モデル、デバイアス方法）の組み合わせ毎に同じものを使用した。

6.1.5 Evaluation.
6.1.5 評価
To evaluate the accuracy, each positive test item was paired with the 100 test negative items, andHit@10, NDCG@10 was measured.
精度を評価するために，各陽性テスト項目と100個のテスト陰性項目のペアを作り，Hit@10, NDCG@10を測定した．
Higher value means higher accuracy.
値が高いほど精度が高いことを意味する．
To evaluate the debias performance, we used the PopQ@1 metric.
デビアス性能の評価には，PopQ@1 メトリクスを使用した．
We computed the value for users having at least 5 positive test items, since too few positive test items can misleadingly result in extreme popularity quantile.
正項目が少なすぎると人気度分位が極端になるため，正項目が5つ以上あるユーザーを対象に計算した．
A PopQ@1 score close to 0.5 is desirable.
PopQ@1 のスコアは 0.5 に近いことが望ましい．
For methods requiring hyperparameter search, we report the best result in terms of accuracy loss, since good performance in debias is meaningful when the model first reports high accuracy
ハイパーパラメータ探索を必要とする手法については，モデルが最初に高い精度を報告するときに，デビアスでの良好なパフォーマンスが意味を持つので，精度の損失という観点から最良の結果を報告する．

## 6.2. Results & Discussion 6.2. 結果と考察

Table 5 shows the experiments results.
表 5 に実験結果を示す．
The bold font emphasizes the results showing an accuracy (Hit@10) loss within 2% compared to the baseline method, while also showing an improvement of at least 0.07 for the debias performance (PopQ@1).
太字は、ベースライン法と比較して精度（Hit@10）損失が2%以内であり、デビアス性能（PopQ@1）が0.07以上向上している結果を強調したものである。

The Zerosum method showed high accuracy and debias performance in the Movielens, Gowalla, and Goodreads datasets when using the MF, NGCF, and LightGCN models.
Zerosum法は、MF、NGCF、LightGCNモデルを用いた場合、Movielens、Gowalla、Goodreadsデータセットにおいて高い精度とデビアス性能を発揮した。
However, Zerosum method generally did not show high performance when using the NeuCF model or the Ciao dataset.
しかし、NeuCFモデルやCiaoデータセットを用いた場合、Zerosum法は概して高い性能を示さなかった。
Other methods such as PD and Pearson sometimes showed good performances but this was not consistent; the PD method did not show good performance in the Movielens and Gowalla datasets when using the NGCF and LightGCN method; the Pearson method showed high accuracy loss when using the NGCF or LightGCN method when training the Movielens dataset.
PD法はNGCFとLightGCNを用いた場合，MovielensとGowallaのデータセットで良い性能を示さず，Pearson法はNGCFとLightGCNを用いた場合，Movielensデータセットで高い精度損失を示している．
Based on the consistent performance of the Zerosum method in addition to the computational advantages discussed earlier, we conclude the Zerosum method to be more effective than earlier methods.
先に述べた計算上の利点に加え、Zerosum法の安定した性能に基づき、Zerosum法は以前の方法よりも効果的であると結論づけた。
Finally, IPW, MACR, and Post-Process often showed excessive accuracy loss and did not show competent performance.
最後に、IPW、MACR、Post-Processは、しばしば過度の精度低下を示し、有能な性能を発揮することができなかった。

Finally we discuss why Zerosum method did not show debias effect with the Ciao dataset.
最後に、Zerosum法がCiaoデータセットでdebian効果を示さなかった理由について考察する。
We observed the debias performance of the Zerosum method depends on baseline model accuracy.
Zerosum法のデビアス効果は、ベースラインモデルの精度に依存することが分かった。
Figure 5 shows the NeuCF scores of positive (blue), negative (orange) items of one user.
図5は、あるユーザの正項目（青）、負項目（オレンジ）のNeuCFスコアを示している。
Smaller x index indicates higher popularity.
x指数が小さいほど人気度が高いことを示している。
The Zerosum method predicted scores focused on symmetric values of +2 and -2 as intended.
Zerosum法は意図したとおり、+2と-2の対称的な値に着目してスコアを予測した。
However, since the model accuracy is low when training with the baseline BPR loss, the model trained with the Zerosum method (which extends the BPR loss) also inaccurately scored -2 for some positive items.
しかし、ベースラインのBPR損失で学習した場合、モデルの精度が低いため、BPR損失を拡張したZerosum法で学習したモデルでも、一部のポジティブアイテムに対して-2という不正確なスコアになってしまう。
Hence, although the Zerosum method balances the scores for items predicted to be positive, such balancing may be misdirected since the predicted items can differ from actual positive items.
したがって，Zerosum法では正と予測される項目のスコアをバランスさせるが，予測される項目が実際の正項目と異なる場合があるため，そのバランスは誤った方向へ向かう可能性がある．
Hence the Zerosum method may have limited debias effect if the baseline model accuracy is low.
したがって、ベースライン・モデルの精度が低い場合、Zerosum法のデビアス効果は限定的であると考えられる。
However, this also hints the effectiveness of the Zerosum method can increase proportionally with baseline model accuracy.
しかし、これはゼロサム法の効果がベースラインモデルの精度に比例して増加することを示唆するものでもある。

# 7. Conclusion 7. まとめ

In this study we tackle the popularity bias, particularly model bias, where the recommendation systems give higher score to popular items among items the user equally liked.
本研究では，人気度バイアス，特に，ユーザが同じように好きなアイテムの中で人気のあるアイテムに高いスコアを与えてしまうモデルバイアスに着目し，これを解決する．
We propose a novel approach to extend the BPR loss with a regularization term which tries to minimize the score differences within positive and negative items, respectively, thus reducing model bias while maintaining high accuracy.
我々は、BPR損失を正則化項によって拡張し、ポジティブ項目とネガティブ項目それぞれにおけるスコア差を最小化することで、高い精度を維持しつつモデルの偏りを低減する新しいアプローチを提案する。
We conduct an experiment to test our method: we embedded explicit popularity bias in a synthetic dataset, which results in model bias in naive training setting.
本手法を検証するため，合成データセットに明示的な人気度バイアスを埋め込んだところ，素朴な学習設定においてモデルのバイアスが発生した．
We apply our method to counter such model bias.
そこで、本手法を適用し、モデルの偏りに対処する。
The results showed our method outperformed earlier debias methods in terms of accuracy and debias performance.
その結果，本手法は従来のデビアス手法を精度およびデビアス性能の点で凌駕することが示された．
We further conducted empirical experiments using four benchmark datasets and four recommendation models.
さらに，4つのベンチマークデータセットと4つの推薦モデルを用いて実証実験を行った．
The proposed method showed consistent debias performance with minimal accuracy loss in 3 of the 4 datasets, in which earlier debias methods lacked consistency.
その結果，提案手法は，4つのデータセットのうち3つのデータセットにおいて，従来のデビアス手法では整合性に欠けていた精度の低下を最小限に抑え，安定したデビアス性能を示すことがわかった．
Our work provides a new way of reducing model bias which can be applied both in academic and industrial settings.
本研究は、モデルの偏りを低減する新しい方法を提供するものであり、学術・産業の両分野で応用が可能である。
For future work, we plan to further investigate improved regularization methods.
今後の課題として、正則化手法の改良をさらに検討する予定である。
We hope that our method can promote diverse recommendations.
本手法が多様なレコメンデーションを促進することを期待する。

# References リファレンス

- [1] Himan Abdollahpouri, Robin Burke, and Bamshad Mobasher. 2017. Controlling popularity bias in learning-to-rank recommendation. In Proceedings of the eleventh ACM conference on recommender systems. 42–46. [1] Himan Abdollahpouri, Robin Burke, and Bamshad Mobasher. 2017. Controlling popularity bias in learning-to-rank recommendation. In Proceedings of the eleventh ACM conference on recommender systems. 42-46.

- [2] Himan Abdollahpouri, Robin Burke, and Bamshad Mobasher. 2019. Managing popularity bias in recommender systems with personalized re-ranking. In The thirty-second international flairs conference. [2] Himan Abdollahpouri, Robin Burke, and Bamshad Mobasher. 2019. パーソナライズされた再ランキングによる推薦システムにおける人気度バイアスの管理. In The thirty-second international flairs conference.

- [3] Himan Abdollahpouri, Masoud Mansoury, Robin Burke, and Bamshad Mobasher. 2020. The connection between popularity bias, calibration, and fairness in recommendation. In Fourteenth ACM conference on recommender systems. 726–731. [3] Himan Abdollahpouri, Masoud Mansoury, Robin Burke, and Bamshad Mobasher. 2020. このような場合、「recommendation.com」は、「recommendation.com」を「recommendation.com」と呼ぶことにする。 In Fourteenth ACM conference on recommender systems. 726-731.

- [4] Gediminas Adomavicius, Alexander Tuzhilin, Shlomo Berkovsky, Ernesto W De Luca, and Alan Said. 2010. Context-awareness in recommender systems: research workshop and movie recommendation challenge. In Proceedings of the fourth ACM conference on Recommender systems. 385–386. 4] Gediminas Adomavicius, Alexander Tuzhilin, Shlomo Berkovsky, Ernesto W De Luca, and Alan Said. 2010. また、このような場合、「萌え萌え」と呼ばれる。 そのため、このような場合、「曖昧さ」を解消することが重要である。 385-386.

- [5] Ashton Anderson, Lucas Maystre, Ian Anderson, Rishabh Mehrotra, and Mounia Lalmas. 2020. Algorithmic effects on the diversity of consumption on spotify. In Proceedings of The Web Conference 2020. 2155–2165. 5] Ashton Anderson, Lucas Maystre, Ian Anderson, Rishabh Mehrotra, and Mounia Lalmas. 2020. Algorithmic effects on the diversity of consumption on spotify. In Proceedings of The Web Conference 2020. 2155-2165.

- [6] Guy Aridor, Duarte Goncalves, and Shan Sikdar. 2020. Deconstructing the filter bubble: User decision-making and recommender systems. In Fourteenth ACM Conference on Recommender Systems. 82–91. 6] Guy Aridor, Duarte Goncalves, and Shan Sikdar. 2020. フィルターバブルを解体する。 を、「ユーザー意思決定とレコメンダーシステム」. In Fourteenth ACM Conference on Recommender Systems. 82-91.

- [7] Ludovico Boratto, Gianni Fenu, and Mirko Marras. 2021. Connecting user and item perspectives in popularity debiasing for collaborative recommendation. Information Processing & Management 58, 1 (2021), 102387. 7】ルドヴィコ・ボラット、ジャンニ・フェヌ、ミルコ・マラス。 2021. Connecting user and item perspectives in popularity debiasing for collaborative recommendation（協調推薦のための人気度デビアスにおけるユーザーとアイテムの視点の接続）。 情報処理と経営 58, 1 (2021), 102387.

- [8] Jiawei Chen, Hande Dong, Xiang Wang, Fuli Feng, Meng Wang, and Xiangnan He. 2020. Bias and debias in recommender system: A survey and future directions. arXiv preprint arXiv:2010.03240 (2020). [8] Jiawei Chen, Hande Dong, Xiang Wang, Fuli Feng, Meng Wang, and Xiangnan He. 2020. レコメンダーシステムにおけるバイアスとデビアス。 このように、"recommender "は、"recommender "と "recommender "の中間的な位置づけにある。

- [9] Jiawei Chen, Xiang Wang, Fuli Feng, and Xiangnan He. 2021. Bias Issues and Solutions in Recommender System: Tutorial on the RecSys 2021. In Fifteenth ACM Conference on Recommender Systems. 825–827. 9】Jiawei Chen, Xiang Wang, Fuli Feng, and Xiangnan He. 2021. レコメンダーシステムにおけるバイアスの問題と解決策: RecSys 2021 のチュートリアル。 In Fifteenth ACM Conference on Recommender Systems. 825-827.

- [10] Eunjoon Cho, Seth A Myers, and Jure Leskovec. 2011. Friendship and mobility: user movement in location-based social networks. In Proceedings of the 17th ACM SIGKDD international conference on Knowledge discovery and data mining. 1082–1090. 10] Eunjoon Cho, Seth A Myers, and Jure Leskovec. 2011. このような場合、「曖昧さ」を解消することが重要である。 このような場合、「曖昧さ」を解消することが重要である。 1082-1090.

- [11] Sumit Chopra, Raia Hadsell, and Yann LeCun. 2005. Learning a similarity metric discriminatively, with application to face verification. In 2005 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR’05), Vol. 1. IEEE, 539–546. 11] Sumit Chopra, Raia Hadsell, and Yann LeCun. 2005. このような場合，そのような情報を利用することで，より効率的かつ効果的な情報収集が可能となる． また、このような場合、「顔認証のための類似性メトリックの識別的学習」 が必要となる。 IEEE, 539-546.

- [12] Yingqiang Ge, Shuya Zhao, Honglu Zhou, Changhua Pei, Fei Sun, Wenwu Ou, and Yongfeng Zhang. 2020. Understanding echo chambers in e-commerce recommender systems. In Proceedings of the 43rd international ACM SIGIR conference on research and development in information retrieval. 2261–2270. 12] Yingqiang Ge, Shuya Zhao, Honglu Zhou, Changhua Pei, Fei Sun, Wenwu Ou, and Yongfeng Zhang. 2020. 電子商取引レコメンダーシステムにおけるエコーチェンバーの理解。 このような場合、「情報検索における研究と開発に関する第43回国際ACM SIGIR会議」の議事録に記載されている。 2261-2270.

- [13] F Maxwell Harper and Joseph A Konstan. 2015. The movielens datasets: History and context. Acm transactions on interactive intelligent systems (tiis) 5, 4 (2015), 1–19. 13] F Maxwell Harper and Joseph A Konstan. 2015. The movielens datasets: 歴史と文脈。 Acm transactions on interactive intelligent systems (tiis) 5, 4 (2015), 1-19.

- [14] Xiangnan He, Kuan Deng, Xiang Wang, Yan Li, Yongdong Zhang, and Meng Wang. 2020. Lightgcn: Simplifying and powering graph convolution network for recommendation. In Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval. 639–648. 14] Xiangnan He, Kuan Deng, Xiang Wang, Yan Li, Yongdong Zhang, and Meng Wang. 2020. Lightgcn: を使用することで、より効果的な推薦のためのグラフ畳み込みネット ワークを実現することができる。 このような場合、「情報検索」の研究開発に関する第 43 回国際 ACM SIGIR 会議の予稿集に記載されています。 639-648.

- [15] Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, and Tat-Seng Chua. 2017. Neural collaborative filtering. In Proceedings of the 26th international conference on world wide web. 173–182. 15] Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, and Tat-Seng Chua. 2017. ニューラル協調フィルタリング. In Proceedings of the 26th international conference on world wide web. 173-182.

- [16] Thorsten Joachims, Adith Swaminathan, and Tobias Schnabel. 2017. Unbiased learning-to-rank with biased feedback. In Proceedings of the Tenth ACM International Conference on Web Search and Data Mining. 781–789. 16] Thorsten Joachims, Adith Swaminathan, and Tobias Schnabel. 2017. バイアスのかかったフィードバックによる偏りのない学習-順位。 In Proceedings of the Tenth ACM International Conference on Web Search and Data Mining. 781-789.

- [17] Yehuda Koren. 2008. Factorization meets the neighborhood: a multifaceted collaborative filtering model. In Proceedings of the 14th ACM SIGKDD international conference on Knowledge discovery and data mining. 426–434. [17] Yehuda Koren. 2008. Factorization meets the neighborhood: a multifaceted collaborative filtering model. 第14回ACM SIGKDD国際会議（Knowledge discovery and data mining）予稿集. 426-434.

- [18] Phuc H Le-Khac, Graham Healy, and Alan F Smeaton. 2020. Contrastive representation learning: A framework and review. IEEE Access 8 (2020), 193907–193934. 18] Phuc H Le-Khac, Graham Healy, and Alan F Smeaton. 2020. 対比的表現学習。 A framework and review. IEEE Access 8 (2020), 193907-193934.

- [19] Mingyang Li, Hongchen Wu, and Huaxiang Zhang. 2019. Matrix factorization for personalized recommendation with implicit feedback and temporal information in social ecommerce networks. IEEE Access 7 (2019), 141268–141276. 19] Mingyang Li, Hongchen Wu, and Huaxiang Zhang. 2019. ソーシャルeコマースネットワークにおける暗黙のフィードバックと時間情報を用いたパーソナライズド・レコメンデーションのためのマトリックスファクトリゼーション。 IEEE Access 7 (2019), 141268-141276.

- [20] Zhuang Liu, Yunpu Ma, Yuanxin Ouyang, and Zhang Xiong. 2021. Contrastive learning for recommender system. arXiv preprint arXiv:2101.01317 (2021). 20】Zhuang Liu, Yunpu Ma, Yuanxin Ouyang, and Zhang Xiong. 2021. Contrastive learning for recommender system. arXiv preprint arXiv:2101.01317 (2021).

- [21] Jiwen Lu, Junlin Hu, and Jie Zhou. 2017. Deep metric learning for visual understanding: An overview of recent advances. IEEE Signal Processing Magazine 34, 6 (2017), 76–84. 21] Jiwen Lu, Junlin Hu, and Jie Zhou. 2017. 視覚理解のためのディープメトリック学習。 最近の進歩の概要。 IEEE Signal Processing Magazine 34, 6 (2017), 76-84.

- [22] Masoud Mansoury, Himan Abdollahpouri, Mykola Pechenizkiy, Bamshad Mobasher, and Robin Burke. 2020. Feedback loop and bias amplification in recommender systems. In Proceedings of the 29th ACM international conference on information & knowledge management. 2145–2148. 

- [23] Tien T Nguyen, Pik-Mai Hui, F Maxwell Harper, Loren Terveen, and Joseph A Konstan. 2014. Exploring the filter bubble: the effect of using recommender systems on content diversity. In Proceedings of the 23rd international conference on World wide web. 677–686. 23] Tien T Nguyen, Pik-Mai Hui, F Maxwell Harper, Loren Terveen, and Joseph A Konstan. 2014. Exploring the filter bubble: the effect of using recommender systems on content diversity. In Proceedings of the 23rd international conference on World wide web. 677-686.

- [24] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 2018. Representation learning with contrastive predictive coding. arXiv preprint arXiv:1807.03748 (2018). 24] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 2018. Representation learning with contrastive predictive coding. arXiv preprint arXiv:1807.03748 (2018).

- [25] Yoon-Joo Park and Alexander Tuzhilin. 2008. The long tail of recommender systems and how to leverage it. In Proceedings of the 2008 ACM conference on Recommender systems. 11–18. 25] Yoon-Joo Park and Alexander Tuzhilin. 2008. このような場合、recommender system は、"recommender "システムと呼ばれる。 というのも、"recommender "は "recommender "を意味するからである。 11-18.

- [26] Steffen Rendle, Christoph Freudenthaler, Zeno Gantner, and Lars Schmidt-Thieme. 2012. BPR: Bayesian personalized ranking from implicit feedback. arXiv preprint arXiv:1205.2618 (2012). 26] Steffen Rendle, Christoph Freudenthaler, Zeno Gantner, and Lars Schmidt-Thieme. 2012. BPR: 暗黙のフィードバックからのベイズ型パーソナライズランキング。

- [27] Tobias Schnabel, Adith Swaminathan, Ashudeep Singh, Navin Chandak, and Thorsten Joachims. 2016. Recommendations as treatments: Debiasing learning and evaluation. In international conference on machine learning. PMLR, 1670– 1679. 27] Tobias Schnabel, Adith Swaminathan, Ashudeep Singh, Navin Chandak, and Thorsten Joachims. 2016. トリートメントとしてのレコメンデーション． Debiasing learning and evaluation. In international conference on machine learning. pmlr, 1670- 1679.

- [28] Florian Schroff, Dmitry Kalenichenko, and James Philbin. 2015. Facenet: A unified embedding for face recognition and clustering. In Proceedings of the IEEE conference on computer vision and pattern recognition. 815–823. 28] Florian Schroff, Dmitry Kalenichenko, and James Philbin. 2015. Facenet: A unified embedding for face recognition and clustering. In Proceedings of the IEEE conference on computer vision and pattern recognition. 815-823.

- [29] Harald Steck. 2011. Item popularity and recommendation accuracy. In Proceedings of the fifth ACM conference on Recommender systems. 125–132. 29] Harald Steck. 2011. アイテムの人気度と推薦精度. このような場合、"recommender "という言葉を使う。 125-132.

- [30] Gábor Takács, István Pilászy, Bottyán Németh, and Domonkos Tikk. 2008. Matrix factorization and neighbor based algorithms for the netflix prize problem. In Proceedings of the 2008 ACM conference on Recommender systems. 267–274. 30] Gábor Takács, István Pilászy, Bottyán Németh, and Domonkos Tikk. 2008.  このような場合、「曖昧さ」を解消することが重要である。 267-274.

- [31] Jiliang Tang, Huiji Gao, and Huan Liu. 2012. mTrust: Discerning multi-faceted trust in a connected world. In Proceedings of the fifth ACM international conference on Web search and data mining. 93–102. 31] Jiliang Tang, Huiji Gao, and Huan Liu. 2012. mTrust: このような場合、「曖昧さ」を回避するために、"曖昧さ "と "曖昧さ "の間の距離を縮める必要がある。  93-102.

- [32] Mengting Wan and Julian J. McAuley. 2018. Item recommendation on monotonic behavior chains. In Proceedings of the 12th ACM Conference on Recommender Systems, RecSys 2018, Vancouver, BC, Canada, October 2-7, 2018, Sole Pera, Michael D. Ekstrand, Xavier Amatriain, and John O’Donovan (Eds.). ACM, 86–94. https://doi.org/10.1145/3240323.3240369 [32] Mengting Wan and Julian J. McAuley. 2018. 単調な行動連鎖上のアイテム推薦。 In Proceedings of the 12th ACM Conference on Recommender Systems, RecSys 2018, Vancouver, BC, Canada, October 2-7, 2018, Sole Pera, Michael D. Ekstrand, Xavier Amatriain, and John O'Donovan (Eds.). ACM, 86-94. https:

- [33] Mengting Wan, Rishabh Misra, Ndapa Nakashole, and Julian J. McAuley. 2019. Fine-Grained Spoiler Detection from Large-Scale Review Corpora. In Proceedings of the 57th Conference of the Association for Computational Linguistics, ACL 2019, Florence, Italy, July 28- August 2, 2019, Volume 1: Long Papers, Anna Korhonen, David R. Traum, and Lluís Màrquez (Eds.). Association for Computational Linguistics, 2605–2610. https://doi.org/10.18653/v1/p19-1248 33] Mengting Wan, Rishabh Misra, Ndapa Nakashole, and Julian J. McAuley. 2019. 大規模なレビューコーパからのきめ細かいスポイラー検出。 Proceedings of the 57th Conference of the Association for Computational Linguistics, ACL 2019, Florence, Italy, July 28- August 2, 2019, Volume 1: Long Papers, Anna Korhonen, David R. Traum, and Lluís Màrquez (Eds.). Association for Computational Linguistics, 2605-2610. https:

- [34] Wenjie Wang, Fuli Feng, Xiangnan He, Xiang Wang, and Tat-Seng Chua. 2021. Deconfounded recommendation for alleviating bias amplification. In Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining. 1717–1725. 34] Wenjie Wang, Fuli Feng, Xiangnan He, Xiang Wang, and Tat-Seng Chua. 2021. このような場合，"recommendation "を用いて，"bias amplification "を緩和する． In Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining. 1717-1725.

- [35] Xiang Wang, Xiangnan He, Meng Wang, Fuli Feng, and Tat-Seng Chua. 2019. Neural graph collaborative filtering. In Proceedings of the 42nd international ACM SIGIR conference on Research and development in Information Retrieval. 165–174. 35] Xiang Wang, Xiangnan He, Meng Wang, Fuli Feng, and Tat-Seng Chua. 2019. ニューラル・グラフ協調フィルタリング(Neural graph collaborative filtering). In Proceedings of the 42nd international ACM SIGIR conference on Research and development in Information Retrieval（情報検索の研究と開発に関する第42回国際ACM SIGIR会議）. 165-174.

- [36] Tianxin Wei, Fuli Feng, Jiawei Chen, Ziwei Wu, Jinfeng Yi, and Xiangnan He. 2021. Model-agnostic counterfactual reasoning for eliminating popularity bias in recommender system. In Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining. 1791–1800. 36] Tianxin Wei, Fuli Feng, Jiawei Chen, Ziwei Wu, Jinfeng Yi, and Xiangnan He. 2021. このような場合、「recommender」システムにおける人気度バイアスを排除するためのモデル不可知論的反実仮想推論。 In Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining. 1791-1800.

- [37] Mi Zhang and Neil Hurley. 2008. Avoiding monotony: improving the diversity of recommendation lists. In Proceedings of the 2008 ACM conference on Recommender systems. 123–130. 37] Mi Zhang and Neil Hurley. 2008. このような場合、「曖昧さ」を解消することが重要である。 というのも、"recommender "は "recommender "を意味するからです。 123-130.

- [38] Yang Zhang, Fuli Feng, Xiangnan He, Tianxin Wei, Chonggang Song, Guohui Ling, and Yongdong Zhang. 2021. Causal intervention for leveraging popularity bias in recommendation. In Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval. 11–20. 38] Yang Zhang, Fuli Feng, Xiangnan He, Tianxin Wei, Chonggang Song, Guohui Ling, and Yongdong Zhang. 2021. 2021年、推薦における人気バイアスを活用するための因果的介入。 In Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval. 11-20.

- [39] Zihao Zhao, Jiawei Chen, Sheng Zhou, Xiangnan He, Xuezhi Cao, Fuzheng Zhang, and Wei Wu. 2021. Popularity Bias Is Not Always Evil: Disentangling Benign and Harmful Bias for Recommendation. arXiv preprint arXiv:2109.07946 (2021). 39] Zihao Zhao, Jiawei Chen, Sheng Zhou, Xiangnan He, Xuezhi Cao, Fuzheng Zhang, and Wei Wu. 2021. Popularity Bias Is Not Always Evil: Disentangling Benign and Harmful Bias for Recommendation. arXiv preprint arXiv:2109.07946 (2021).

- [40] Yu Zheng, Chen Gao, Xiang Li, Xiangnan He, Yong Li, and Depeng Jin. 2021. Disentangling user interest and conformity for recommendation with causal embedding. In Proceedings of the Web Conference 2021. 2980–2991. 40] Yu Zheng, Chen Gao, Xiang Li, Xiangnan He, Yong Li, and Depeng Jin. 2021. causal embedding を用いた推薦のためのユーザーの興味と適合性の切り分け． Web Conference 2021 の予稿集に掲載。 2980-2991.

- [41] Chang Zhou, Jianxin Ma, Jianwei Zhang, Jingren Zhou, and Hongxia Yang. 2021. Contrastive learning for debiased candidate generation in large-scale recommender systems. In Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining. 3985–3995. 41] Chang Zhou, Jianxin Ma, Jianwei Zhang, Jingren Zhou, and Hongxia Yang. 2021. 大規模推薦システムにおけるデビアス候補生成のための対照学習。 In Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining. 3985-3995.

- [42] Ziwei Zhu, Yun He, Xing Zhao, Yin Zhang, Jianling Wang, and James Caverlee. 2021. Popularity-opportunity bias in collaborative filtering. In Proceedings of the 14th ACM International Conference on Web Search and Data Mining. 85–93. 42] Ziwei Zhu, Yun He, Xing Zhao, Yin Zhang, Jianling Wang, and James Caverlee. 2021. このような場合、「李舜臣」（Richard Huang）は、「李舜臣」と呼ばれる。 In Proceedings of the 14th ACM International Conference on Web Search and Data Mining. 85-93.

- [43] Ziwei Zhu, Jianling Wang, and James Caverlee. 2020. Measuring and mitigating item under-recommendation bias in personalized ranking systems. In Proceedings of the 43rd international ACM SIGIR conference on research and development in information retrieval. 449–458. 43] Ziwei Zhu, Jianling Wang, and James Caverlee. 2020. このような場合、「李錬學」は、「李錬學」と「李錬學」と「李錬學」の中間的な位置づけにある。 このような場合、「情報検索における研究開発に関する第43回国際ACM SIGIR会議」の議事録に記載されています。 449-458.