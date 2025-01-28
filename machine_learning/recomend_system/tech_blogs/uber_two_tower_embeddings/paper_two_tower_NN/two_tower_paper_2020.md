https://storage.googleapis.com/gweb-research2023-media/pubtools/6090.pdf
<!-- Google Playの推薦の話っぽい! あとリクルートさんのブログでtwo-towerモデルで引用してるやつ -->
# Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations  

### ABSTRACT 要約
Learning query and item representations is important for building large scale recommendation systems. 
クエリとアイテムの表現を学習することは、大規模な推薦システムを構築するために重要です。

In many real applications where there is a huge catalog of items to recommend, the problem of efficiently retrieving top k items given user’s query from deep corpus leads to a family of factorized modeling approaches where queries and items are jointly embedded into a low-dimensional space. 
推奨するアイテムの巨大なカタログが存在する多くの実際のアプリケーションでは、ユーザのクエリに基づいて深いコーパスから効率的に上位kアイテムを取得する問題が、クエリとアイテムが共同で低次元空間に埋め込まれる因子化モデリングアプローチのファミリーにつながります。
In this paper, we first showcase how to apply a two-tower neural network framework, which is also known as dual encoder in the natural language community, to improve a large-scale, production app recommendation system. 
本論文では、まず、**自然言語コミュニティでデュアルエンコーダとしても知られる**二塔ニューラルネットワークフレームワークを適用して、大規模なプロダクションアプリ推薦システムを改善する方法を示します。
Furthermore, we offer a novel negative sampling approach called Mixed Negative Sampling (MNS). 
さらに、Mixed Negative Sampling (MNS)と呼ばれる新しいネガティブサンプリングアプローチを提案します。
In particular, different from commonly used batch or unigram sampling methods, MNS uses a mixture of batch and uniformly sampled negatives to tackle the selection bias of implicit user feedback. 
特に、一般的に使用されるバッチまたはユニグラムサンプリング手法とは異なり、MNSはバッチと均等にサンプリングされたネガティブの混合を使用して、暗黙のユーザフィードバックの選択バイアスに対処します。
We conduct extensive offline experiments using large-scale production dataset and show that MNS outperforms other baseline sampling methods. 
私たちは、大規模なプロダクションデータセットを使用して広範なオフライン実験を行い、MNSが他のベースラインサンプリング手法を上回ることを示します。
We also conduct online A/B testing and demonstrate that the two-tower retrieval model based on MNS significantly improves retrieval quality by encouraging more high-quality app installs. 
また、オンラインA/Bテストを実施し、MNSに基づく二塔取得モデルがより多くの高品質なアプリインストールを促進することによって、取得品質を大幅に改善することを示します。

<!-- ここまで読んだ -->

### KEYWORDS キーワード
Information Retrieval, Neural Networks, Context-aware Recommender Systems, Extreme Classification
情報検索、ニューラルネットワーク、コンテキスト対応推薦システム、極端な分類

**ACM Reference Format:** Ji Yang, Xinyang Yi, Derek Zhiyuan Cheng, Lichan Hong, Yang Li, Simon Xiaoming Wang, Taibai Xu, and Ed H. Chi. 2020. Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations. 
**ACM 参考フォーマット:** Ji Yang, Xinyang Yi, Derek Zhiyuan Cheng, Lichan Hong, Yang Li, Simon Xiaoming Wang, Taibai Xu, および Ed H. Chi. 2020. 推薦における二塔型ニューラルネットワーク学習のための混合ネガティブサンプリング。

In _Companion Proceedings of the Web Conference 2020 (WWW ’20 Companion), April 20–24, 2020, Taipei, Taiwan. ACM, New York, NY, USA, 7 pages._ 
_2020年ウェブ会議（WWW ’20 Companion）付録論文集において、2020年4月20日から24日、台湾台北。ACM、ニューヨーク、NY、アメリカ、7ページ。_

This paper is published under the Creative Commons Attribution 4.0 International (CC-BY 4.0) license. 
この論文は、クリエイティブ・コモンズ 表示 4.0 国際（CC-BY 4.0）ライセンスの下で公開されています。

Authors reserve their rights to disseminate the work on their personal and corporate Web sites with the appropriate attribution. 
著者は、適切な帰属をもって、個人および法人のウェブサイトで作品を配布する権利を留保します。

_WWW ’20 Companion, April 20–24, 2020, Taipei, Taiwan_ 
_WWW ’20 Companion、2020年4月20日から24日、台湾台北_

© 2020 IW3C2 (International World Wide Web Conference Committee), published under Creative Commons CC-BY 4.0 License. 
© 2020 IW3C2（国際ワールドワイドウェブ会議委員会）、クリエイティブ・コモンズ CC-BY 4.0 ライセンスの下で公開。

ACM ISBN 978-1-4503-7024-0/20/04. 
ACM ISBN 978-1-4503-7024-0/20/04。

[https://doi.org/10.1145/3366424.3386195](https://doi.org/10.1145/3366424.3386195)
[https://doi.org/10.1145/3366424.3386195](https://doi.org/10.1145/3366424.3386195)

## 1 INTRODUCTION はじめに

Recommendation systems are important in connecting users to a large number of relevant items and content. 
推薦システムは、ユーザーを多数の関連アイテムやコンテンツに接続する上で重要です。 
One of the most critical challenges in building real-world recommenders is to accurately score millions to billions of items in real time. 
実世界のレコメンダーを構築する上での**最も重要な課題の一つは、数百万から数十億のアイテムをリアルタイムで正確にスコアリングすること**です。 
Many industry-scale systems [7, 9] have a two-stage architecture where a retrieval model first retrieves a small fraction of relevant items from item corpus, and a ranking model is applied to re-ranks the retrieved items based on users’ feedback such as clicks or ratings on impressions. 
多くの業界規模のシステム[7, 9]は、2段階のアーキテクチャを持ち、最初にリトリーバルモデルがアイテムコーパスから関連アイテムの小さな部分を取得し、次にランキングモデルがユーザーのフィードバック（クリックやインプレッションに対する評価など）に基づいて取得したアイテムを再ランク付けします。 
In this paper, we focus on the retrieval problem and showcase how we improve the app retrieval system of Google Play, one of the largest commercial mobile app stores, by jointly learning query and app representations via deep neural networks. 
**本論文では、リトリーバルの問題に焦点を当て**、深層ニューラルネットワークを通じてクエリとアプリの表現を共同学習することにより、最大の商業モバイルアプリストアの一つであるGoogle Playのアプリリトリーバルシステムをどのように改善するかを示します。 

<!-- ここまで読んだ! この論文で議論するtwo-towerモデルは 2段階推薦における1段階目retrieveの部分に焦点を当てた話!-->

Recently, lots of research has been developed on embedding-based retrieval models. 
最近、埋め込みベースのリトリーバルモデルに関する多くの研究が進展しています。 
Matrix factorization (MF) (e.g., [14]) is one of most popular approaches for learning query and item latent factors in building retrieval systems. 
行列分解（MF）（例：[14]）は、リトリーバルシステムを構築する際にクエリとアイテムの潜在因子を学習するための最も人気のあるアプローチの一つです。 
One challenge of MF is cold-start, i.e., it’s hard for this method to generalize to items that have no user interaction. 
MFの課題の一つはコールドスタートであり、すなわち、この手法はユーザーのインタラクションがないアイテムに一般化するのが難しいということです。
A body of recommendation research (e.g., [4, 13, 21]) addresses this challenge by further leveraging item’s content features, which can be loosely defined as a wide variety of features describing items beyond their ids. 
推薦に関する研究の一部（例：[4, 13, 21]）は、この課題に対処するために、アイテムのコンテンツ特徴をさらに活用します。これらの特徴は、アイテムのIDを超えてアイテムを説明するさまざまな特徴として緩やかに定義できます。 
For instance, content features of an app could be text descriptions, creators, categories, etc. 
例えば、アプリのコンテンツ特徴には、テキストの説明、クリエイター、カテゴリなどが含まれます。 
As deep learning has demonstrated tremendous successes in computer vision and natural language processing, there are many works [3, 7] that apply extreme multi-class classification model to learn query embedding via multi-layer perceptions. 
深層学習がコンピュータビジョンや自然言語処理で驚異的な成功を収めているため、クエリ埋め込みを多層パーセプトロンを介して学習するために極端な多クラス分類モデルを適用する多くの研究[3, 7]があります。 
Despite the non-linearity on the query side, each item is still represented by a single embedding. 
クエリ側の非線形性にもかかわらず、各アイテムは依然として単一の埋め込みで表現されます。(これどういう意味だろ、コンテキスト考慮してないじゃん、みたいなこと?...!!:thinking_face:)
Hence, similar to MF, this method fails to represent a collection of items features with various formats. 
したがって、MFと同様に、この手法はさまざまな形式のアイテム特徴のコレクションを表現することに失敗します。 

Most recently, two-tower neural networks, with towers referring to encoders based on deep neural network (DNN), attains growing interests [24], and are applied to tackle the challenge of cold-start issue of MF and multi-class extreme classification models. 
最近、2タワーのニューラルネットワーク（タワーは深層ニューラルネットワーク（DNN）に基づくエンコーダを指します）が注目を集めており[24]、MFと多クラス極端分類モデルのコールドスタート問題に対処するために適用されています。 
The basic idea is to further incorporate items’ content features through a multi-layer neural network that would generalize to fresh or tail items with no training data. 
**基本的なアイデアは、トレーニングデータがない新しいアイテムやテールアイテムに一般化する多層ニューラルネットワークを通じてアイテムのコンテンツ特徴をさらに組み込むこと**です。
See Figure 1 for an illustration of the model architecture. 
モデルアーキテクチャの図は図1を参照してください。 
This model framework is also closely connected to the dual encoder framework [8, 23] in language models. 
このモデルフレームワークは、**言語モデルにおけるデュアルエンコーダフレームワーク[8, 23]とも密接に関連**しています。 
This paper lies in this line of work. 
本論文はこの研究の流れに位置しています。 
We focus on applying the two-tower framework to improve the retrieval system of Google Play, which is one of the largest commercial mobile app stores, connecting millions of apps to billions of users across the world.  
私たちは、世界中の数十億のユーザーに数百万のアプリを接続する最大の商業モバイルアプリストアの一つであるGoogle Playのリトリーバルシステムを改善するために、2タワーフレームワークを適用することに焦点を当てています。

Similar to language tasks, negative sampling plays a critical role in training two-tower neural networks in recommendations.  
言語タスクと同様に、ネガティブサンプリングは推薦におけるツータワーニューラルネットワークのトレーニングにおいて重要な役割を果たします。
Especially, in recommendation, users’ positive feedback are often collected, and counterfactuals on items not shown are very hard to obtain.  
特に推薦においては、ユーザーのポジティブフィードバックがしばしば収集され、表示されていないアイテムに関する**反事実**を得ることは非常に困難です。(ここで反実仮想の観点が出てきてる...!)
A popular sampling approach [1, 7] for fitting a softmax output distribution is to sample according to the unigram distribution of items.  
ソフトマックス出力分布にフィットさせるための一般的なサンプリングアプローチ[1, 7]は、アイテムのユニグラム分布に従ってサンプリングすることです。
The work in [24] extends unigram sampling to the two-tower setting by using batch negatives, i.e., using the positive items in a mini batch as shared negatives for all queries in the same batch.  
文献[24]では、バッチネガティブを使用することによってユニグラムサンプリングをツータワー設定に拡張しています。つまり、ミニバッチ内のポジティブアイテムを同じバッチ内のすべてのクエリに対する共有ネガティブとして使用します。
(**このあたりの話は、結局無理やりnegative sampleを用意して教師あり学習として解こうとしてるって話で、自分が気にしてる話ではないな...!:thinking_face:**)
We note that unigram-sampled or batch negatives have the limit of selection bias in training data.  
ユニグラムサンプリングまたはバッチネガティブには、トレーニングデータにおける選択バイアスの制限があることに注意します。
This is because the training data is derived from user feedback logs, and users often interact with a small set of popular items suggested by existing recommender system.  
これは、トレーニングデータがユーザーフィードバックログから派生しており、ユーザーが既存の推薦システムによって提案された少数の人気アイテムとしばしば相互作用するためです。
Items that are not favored by the existing system are less likely to get user feedback.  
既存のシステムに好まれないアイテムは、ユーザーフィードバックを得る可能性が低くなります。
Accordingly, sampling batch negatives only from training data will end up with a model lacking resolution for long-tail apps, which seldom appear in the training data.  
したがって、トレーニングデータからのみバッチネガティブをサンプリングすると、トレーニングデータにほとんど現れないロングテールアプリに対する解像度が欠けたモデルになります。


Inspired by the aforementioned constraint of batch negatives, we propose a novel sampling approach called Mixed Negative Sampling (MNS), where the idea is to use a mixture of unigram and uniform distributions.  
前述のバッチネガティブの制約に触発されて、ユニグラムと一様分布の混合を使用する新しいサンプリングアプローチであるMixed Negative Sampling (MNS)を提案します。
In particular, in addition to the negatives sampled from batch training data, we uniformly sample negatives from the candidate corpus to serve as additional negatives.  
特に、バッチトレーニングデータからサンプリングされたネガティブに加えて、候補コーパスからネガティブを一様にサンプリングして追加のネガティブとして使用します。
This two-stream negative sampling enables us to: (1) reduce selection bias by bringing in samples from the entire candidate corpus; (2) adjust the sampling distribution by changing the number of additional negative samples from the corpus.  
この二重ストリームネガティブサンプリングにより、次のことが可能になります：(1) 全候補コーパスからサンプルを取り入れることで選択バイアスを減少させること；(2) コーパスからの追加ネガティブサンプルの数を変更することでサンプリング分布を調整すること。
We further demonstrate the effectiveness of our retrieval system with both offline and online experiments on Google Play.  
さらに、Google Playでのオフラインおよびオンライン実験を通じて、私たちの検索システムの有効性を示します。
Offline studies showed that MNS significantly improves retrieval quality.  
オフラインの研究では、MNSが検索品質を大幅に改善することが示されました。
In addition, online A/B testing shows that the two-tower model trained with MNS leads to more high-quality app installs from for Google Play.  
さらに、オンラインA/Bテストでは、MNSでトレーニングされたツータワーモデルがGoogle Playからの高品質なアプリインストールを増加させることが示されています。
The lessons from this case study sheds light for other large-scale recommendation systems dealing with huge item catalogs.  
このケーススタディからの教訓は、大規模なアイテムカタログを扱う他の大規模推薦システムに光を当てます。

In summary, our contributions are:  
要約すると、私たちの貢献は次のとおりです：

- Real-world application. We showcase how to apply the dual-encoder framework to improve a large scale, production app recommendation system.  
- 実世界の応用。私たちは、デュアルエンコーダーフレームワークを適用して大規模な生産アプリ推薦システムを改善する方法を示します。
In particular, we show how to leverage the item tower to mitigate the well-known cold-start problem of embedding-based approaches. 
特に、埋め込みベースのアプローチのよく知られた**コールドスタート問題を軽減するためにアイテムタワーを活用する方法**を示します。(MFと比べてって話か)

- Mixed negative sampling. 
- 混合ネガティブサンプリング。(これはtwo-towerモデルの学習方法の話なので、あまり興味ない...!:thinking_face:)
We present the problem of selection bias in the commonly used unigram and batch negative sampling methods, and propose a novel negative sampling approach called mixed negative sampling. 
一般的に使用されるユニグラムおよびバッチネガティブサンプリング手法における選択バイアスの問題を提示し、混合ネガティブサンプリングと呼ばれる新しいネガティブサンプリングアプローチを提案します。 

- Offline and online experiments. 
- オフラインおよびオンライン実験。 
We conduct extensive offline and online experiments in Google Play to demonstrate the effectiveness of MNS, and report that the new system we build can encourage significantly more high-quality app installs from users. 私たちは、MNSの効果を示すためにGoogle Playで広範なオフラインおよびオンライン実験を行い、私たちが構築した新しいシステムがユーザーからの高品質なアプリインストールを大幅に促進できることを報告します。 

<!-- ここまで読んだ! -->

### 2 RELATED WORK 関連研究

In the decade, deep learning has demonstrated tremendous successes in recommender systems, ranging from video recommendation [7], news recommendation [20], to visual discovery in social networks [15, 25].  
この10年間、深層学習は、ビデオ推薦[7]、ニュース推薦[20]、ソーシャルネットワークにおける視覚的発見[15, 25]に至るまで、推薦システムにおいて驚異的な成功を収めてきました。
Cheng et al. [5] introduces a wide-n-deep framework for reranking task in app recommendations.  
Chengら[5]は、アプリ推薦における再ランキングタスクのためのワイド・アンド・ディープフレームワークを紹介しています。
For the retrieval task, there has also been growing interests in applying DNN-based representation learning approaches.  
**検索タスクにおいても、DNNベースの表現学習アプローチを適用することへの関心が高まっています**。
Covington et al. [7] treats the retrieval task as an extreme multi-class classification trained with multi-layer perceptron (MLP) [10] model using sampled softmax as its loss function.  
Covingtonら[7]は、検索タスクをサンプリングされたソフトマックスを損失関数として使用する多層パーセプトロン（MLP）[10]モデルでトレーニングされた極端な多クラス分類として扱います。
Despite achieving lots of success, such a model architecture relies on a predetermined item vocabulary and does not generalize well to new items.  
多くの成功を収めているにもかかわらず、そのようなモデルアーキテクチャは、あらかじめ決定されたアイテム語彙に依存しており、新しいアイテムに対してはうまく一般化しません。

A big challenge in training multi-class classification model with softmax is the training cost when the number of classes is huge (e.g., millions).  
ソフトマックスを使用した多クラス分類モデルのトレーニングにおける大きな課題は、クラス数が膨大な場合（例：数百万）のトレーニングコストです。
Hierarchical softmax [11, 18] and sampled softmax [1, 2] are two most common approaches used to improve training speed.  
階層的ソフトマックス[11, 18]とサンプリングされたソフトマックス[1, 2]は、トレーニング速度を改善するために使用される最も一般的な2つのアプローチです。
Hierarchical softmax defines a tree for categories based on their attributes and makes hierarchical decisions traversing the tree to get the final category.  
階層的ソフトマックスは、属性に基づいてカテゴリのためのツリーを定義し、ツリーを横断して最終カテゴリを取得するための階層的な決定を行います。
On the other hand, sampled softmax specifies a sampling distribution Q from which a subset of the label space is drawn to approximate the gradient.  
一方、サンプリングされたソフトマックスは、勾配を近似するためにラベル空間のサブセットが引き出されるサンプリング分布Qを指定します。
Researchers usually use simple distributions, e.g., unigram or bigram distributions based on sample frequency [1, 2], or a power-raised distribution of the unigram [17].  
研究者は通常、サンプル頻度に基づくユニグラムまたはバイグラム分布[1, 2]、またはユニグラムのべき乗分布[17]などの単純な分布を使用します。
However, neither hierarchical softmax nor sampled softmax is applicable to our two-tower architecture where label is associated with a rich set of content features.  
しかし、階層的ソフトマックスもサンプリングされたソフトマックスも、ラベルが豊富なコンテンツ特徴に関連付けられた私たちのツータワーアーキテクチャには適用できません。

People started to adopt two-tower DNNs to learn representation from content features in language models [6, 16, 19].  
人々は、**言語モデル[6, 16, 19]におけるコンテンツ特徴から表現を学習するためにツータワーDNNを採用し始めました**。(そういう経緯なのか...!:thinking_face:)
Two-tower DNNs have also been introduced for retrieval task to leverage rich content feature on item side in recommender systems with application in video recommendations [24], where batch negative sampling based on item frequency estimation is adopted to correct sampling bias.  
ツータワーDNNは、アイテム側の豊富なコンテンツ特徴を活用するために検索タスクにも導入されており、ビデオ推薦[24]におけるアプリケーションでは、アイテム頻度推定に基づくバッチネガティブサンプリングが採用されてサンプリングバイアスを修正しています。
In contrast, our work found it important to reduce the selection bias brought by batch negative sampling in the application for app recommendations, which has not been considered in existing works to the best of our knowledge.  
対照的に、私たちの研究では、アプリ推薦のアプリケーションにおいてバッチネガティブサンプリングによってもたらされる選択バイアスを減少させることが重要であると考えています。これは、既存の研究では考慮されていないと私たちの知る限りではあります。
(まあ反実仮想的な部分をどうにか考慮する必要があるよね、という議論はあるんだな)

<!-- ここまで読んだ! -->

## 3 MODELING FRAMEWORK モデリングフレームワーク

In this section, we first provide a mathematical formulation for the retrieval task in large-corpus recommender systems. 
このセクションでは、まず大規模コーパス推薦システムにおける検索タスクの数学的定式化を提供します。
We then present the modeling approach based on a two-tower deep neural network and describe how we train the model using in-batch negative sampling. 
次に、2タワー深層ニューラルネットワークに基づくモデリングアプローチを提示し、バッチ内負のサンプリングを使用してモデルをどのように訓練するかを説明します。
Finally, we introduce the Mixed Negative Sampling (MNS) technique to address the selection bias of the batch negatives. 
最後に、バッチの負のサンプルの選択バイアスに対処するために、Mixed Negative Sampling (MNS)技術を紹介します。

### 3.1 問題の定式化

The retrieval task in recommendation systems aims to quickly select Query Embedding B Candidate Item Embedding B **_B_** hundreds to thousands of candidate items from the entire item corpus given a certain query. 
推薦システムにおける検索タスクは、特定のクエリが与えられたときに、全アイテムコーパスから数百から数千の候補アイテムを迅速に選択することを目的としています。 
In particular, a query could be a piece **Label matrix** of text, an item (e.g., an app), a user, or a mixture of these. 
特に、クエリはテキストの一部（ラベル行列）、アイテム（例：アプリ）、ユーザー、またはこれらの混合である可能性があります。 
Here both 1 queries and items can be represented as feature vectors capturing 1 . . 0 Training data **_B_** wide variety of information. 
ここでは、クエリとアイテムの両方が、さまざまな情報を捉える特徴ベクトルとして表現できます。 
We treat the retrieval problem as a multi-class classification problem, and the likelihood of suggesting (Query-item pairs) Batch B 0 . . 1 an item from a large corpus (classes) C is formulated as a softmax  probability:  
私たちは検索問題を多クラス分類問題として扱い、**大規模コーパス（クラス）Cからアイテム（クエリ-アイテムペア）を提案する可能性をソフトマックス確率として定式化**します: 

$$
P(y|x) = \frac{e^{\epsilon(x,y)}}{\sum_{j \in C} e^{\epsilon(x,y_j)}}
$$

where ε(x, _y) denotes the logits provided by the retrieval model, with feature vectors x and y representing the query and the item respectively. 
ここで、ε(x, _y)は検索モデルによって提供されるロジットを示し、特徴ベクトルxとyはそれぞれクエリとアイテムを表します。

(logit = ロジット: 最もらしさを表すスコア的な意味合い?? two-towerモデルの場合は内積)

<!-- ここまで読んだ! -->

### 3.2 モデリングアプローチ

We adopt a two-tower DNN model architecture for computing logits ε(x, _y). 
私たちは、logits $\epsilon(x, y)$を計算するために、二塔DNNモデルアーキテクチャを採用します。
As shown in Figure 1, the left tower and right tower learn latent representations of given query and item separately. 
図1に示すように、左の塔と右の塔は、与えられたクエリとアイテムの潜在表現をそれぞれ学習します。
Formally, we denote the two DNN towers by functions u(x; _θ_ ) and _v(y;_ _θ_ ), which map query and item features x and y to a shared embedding space. 
形式的には、2つのDNNタワーを関数 $u(x; \theta)$ と $v(y; \theta)$ で表し、**クエリとアイテムの特徴 $x$ と $y$ を共有埋め込み空間にマッピング**します。
Here θ denotes all the model parameters. 
ここで、$\theta$はすべてのモデルパラメータを示します。
The model outputs the inner product of query and item embeddings as logits in Equation (1), i.e., 
モデルは、式(1)において**クエリとアイテムの埋め込みの内積をlogitsとして出力**します。すなわち、

$$
\epsilon(x, y) = \langle u(x; \theta), v(y; \theta) \rangle.
$$

To simplify notations, we denote u as the embedding for a given query x and vj as the embedding for item j from the corpus C. 
記法を簡略化するために、$u$を与えられたクエリ$x$の埋め込み、$v_j$をコーパス$C$からのアイテム$j$の埋め込みとします。
The cross-entropy loss for a {query (x), item (y_l, positive label)} pair becomes: 
{クエリ(x)、アイテム(y_l, 正のラベル)}ペアのクロスエントロピー損失は次のようになります：

<!-- ここまで読んだ! 正直、この辺りの損失関数はあんまり今回は興味ない!結局ケースバイケースなので:thinking_face:) -->

$$
L = -\log(P(y_l | x)) = -\log \left( \frac{e^{\langle u, v_l \rangle}}{\sum_{j \in C} e^{\langle u, v_j \rangle}} \right). 
$$

Taking gradient of Equation (2) with respect to parameter θ gives  
式(2)のパラメータ$\theta$に関する勾配を取ると、

$$
勾配の式
$$

The second term represents the expectation of ∇θ (⟨u,vj⟩) with respect to P(·|x) (referred to as target distribution). It is generally impractical to compute the second term over all items in a huge corpus. As a result, we approximate this expectation by sampling a small number of items using importance sampling [2].
第二項は P(·|x)に関する∇θ (⟨u,vj⟩)の期待値を表しており（これをターゲット分布と呼びます）、巨大なコーパス内のすべてのアイテムに対して第二項を計算することは一般的に実用的ではありません。その結果、重要サンプリングを使用して、この期待値を少数のアイテムで近似します[2]。
Specifically, we sample a subset of items C′ from the corpus with a predefined distribution Q with Qj being the sampling probability of item j and estimate the second term in Equation (3) as:
具体的には、事前定義された分布Qを使用してコーパスからアイテムのサブセット$C'$をサンプリングし、アイテム$j$のサンプリング確率が$Q_j$であるとして、式(3)の第二項を次のように推定します：

$$
\mathbb{E}_P [\nabla_\theta (\langle u, v_j \rangle)] \approx \sum_{j' \in C'} \omega_j \nabla_\theta (\langle u, v_{j'} \rangle), 
$$

where $\omega_j = e^{\langle u, v_j \rangle - \log(Q_j)}$ incorporates the logQ correction utilized in sampled softmax [1, 2]. 
ここで、$\omega_j = e^{\langle u, v_j \rangle - \log(Q_j)}$は、サンプリングされたソフトマックスで使用されるlogQ補正を組み込みます[1, 2]。

A commonly-used sampling strategy for two-tower DNN model is the batch negative sampling. 
二塔DNNモデルの一般的に使用されるサンプリング戦略は、バッチネガティブサンプリングです。
Specifically, batch negative sampling treats other items in the same training batch as sampled negatives and therefore the sampling distribution Q follows the unigram distribution based on item frequency. 
具体的には、バッチネガティブサンプリングは、同じトレーニングバッチ内の他のアイテムをサンプリングされたネガティブとして扱い、したがってサンプリング分布$Q$はアイテムの頻度に基づくユニグラム分布に従います。
It avoids feeding additional negative samples to the right tower and thus saves computation cost. 
これにより、右の塔に追加のネガティブサンプルを供給することを避け、計算コストを節約します。
Figure 2 shows the computation process in one training batch. 
図2は、1つのトレーニングバッチにおける計算プロセスを示しています。
Given B pairs of {query, item} in a batch, features of B queries and B items go through the left and right towers of the model, respectively, producing B × K (K is the embedding dimension) embedding matrices U and V. 
バッチ内にBペアの{クエリ、アイテム}が与えられると、B個のクエリとB個のアイテムの特徴がそれぞれモデルの左の塔と右の塔を通過し、B × K（Kは埋め込み次元）埋め込み行列$U$と$V$を生成します。
Then the logits matrix can be calculated as $L = UV^T$. 
次に、logits行列は$L = UV^T$として計算できます。
While the batch negative sampling significantly improves training speed, we discuss its problems in the next sub-section and propose an alternative sampling strategy accordingly. 
バッチネガティブサンプリングはトレーニング速度を大幅に改善しますが、次の小節でその問題について議論し、それに応じて代替のサンプリング戦略を提案します。

<!-- ここまで読んだ! -->

### 3.3 Mixed Negative Sampling 混合ネガティブサンプリング

Controlling bias and variance of the gradient estimator is critical to model quality. 
**勾配推定器のバイアスと分散を制御することは、モデルの品質にとって重要**です。(OPEやOPLっぽい観点だ...!:thinking_face:)
There are two ways to reduce bias and variance [2]: (1) increasing the sample size; (2) reducing the discrepancy between proposed Q distribution and target distribution P.
バイアスと分散を減少させる方法は2つあります[2]： (1) サンプルサイズの増加; (2) 提案されたQ分布とターゲット分布Pとの不一致を減少させることです。
(結局Q分布とか使ってるってことは、どちらかというとDM推定量的な話なのかな...!:thinking_face:)

In case of training two-tower DNN models, batch negative sampling implicitly sets sampling distribution Q to be unigram item frequency distribution. 
2タワーDNNモデルのトレーニングの場合、**バッチネガティブサンプリングは暗黙的にサンプリング分布Qをユニグラムアイテム頻度分布に設定**します。
It has 2 problems in recommendation scenarios:
推薦シナリオには2つの問題があります：
- (1) Selection bias: for example, an item with no user feedback will not be included as a candidate app in the training data. 
  - (1) 選択バイアス：例えば、ユーザーフィードバックのないアイテムは、トレーニングデータの候補アプリとして含まれません。
  Thus it will never be sampled as a negative with batch negative sampling. 
  したがって、バッチネガティブサンプリングではネガティブとしてサンプリングされることは決してありません。
  Consequently, the model lacks capability to differentiate items with sparse feedback w.r.t other items.
  結果として、モデルは他のアイテムに対してスパースフィードバックを持つアイテムを区別する能力を欠いています。
- (2) Lack of flexibility to adjust sampling distribution: The implicit sampling distribution Q is determined by the training data and cannot be further adjusted. 
  - (2) サンプリング分布を調整する柔軟性の欠如：暗黙のサンプリング分布Qはトレーニングデータによって決定され、さらに調整することはできません。
  Deviation of Q from target distribution P might result in a significant amount of bias.
  Qがターゲット分布Pから逸脱すると、重要なバイアスが生じる可能性があります。

We propose Mixed Negative Sampling (MNS) to tackle these problems. 
これらの問題に対処するために、混合ネガティブサンプリング（MNS）を提案します。
It uniformly samples B[′] items from another data stream.
これは、別のデータストリームからB[′]アイテムを均等にサンプリングします。
We refer the additional data stream as index data, which is a set composed of items from the entire corpus. 
追加のデータストリームをインデックスデータと呼び、これは全体のコーパスからのアイテムで構成されるセットです。
These items serve as additional negatives for every single batch. 
これらのアイテムは、各バッチの追加のネガティブとして機能します。
Figure 3 shows the computation process for a training batch. 
図3は、トレーニングバッチの計算プロセスを示しています。
In addition to the B × K query embedding matrix UB, and the B × K candidate item embedding matrix VB, B[′] candidate items uniformly sampled from the index data are fed into the right tower to produce a B[′] × K candidate item embedding matrix VB[′].
B × Kクエリ埋め込み行列UBおよびB × K候補アイテム埋め込み行列VBに加えて、インデックスデータから均等にサンプリングされたB[′]候補アイテムが右のタワーに供給され、B[′] × K候補アイテム埋め込み行列VB[′]が生成されます。
We concatenate VB and VB[′] to get a (B + B[′]) × K candidate item embedding matrix V.
VBとVB[′]を連結して、(B + B[′]) × K候補アイテム埋め込み行列Vを取得します。
Eventually we have the B × (B + B[′]) logits matrix L = UV _[T]_.
最終的に、B × (B + B[′])ロジット行列L = UV _[T]_を得ます。
The label matrix therefore becomes B ×(B + B[′]) with an all 0 B × B[′] matrix appended to the original B × B diagonal matrix. 
したがって、ラベル行列は、元のB × B対角行列にすべて0のB × B[′]行列が追加されたB ×(B + B[′])になります。
Accordingly, the loss function for a training batch becomes 
したがって、トレーニングバッチの損失関数は次のようになります。

$$
LB ≈− B[1] e [⟨u[i], v[i]⟩] \log( ), (5) i ∈[B] e [⟨u[i], v[i]⟩] + [j] j ∈[B+B[′]], j≠i w_{ij}
$$

where $w_{ij} = e [⟨u[i], v[j]⟩−\log(Q_{j*})]$ with $u_i$ being the ith row of $U$ and $v_j$ denoting the jth row of $V$. 
ここで、$w_{ij} = e [⟨u[i], v[j]⟩−\log(Q_{j*})]$ であり、$u_i$ は $U$ のi行目、$v_j$ は $V$ のj行目を示します。
Here the sampling distribution $Q_{*}$ becomes a mixture of item frequency based unigram sampling and uniform sampling, characterized by a ratio between the batch size $B$ and $B[′]$. 
ここで、サンプリング分布 $Q_{*}$ は、アイテム頻度に基づくユニグラムサンプリングと一様サンプリングの混合になり、バッチサイズ $B$ と $B[′]$ の比率によって特徴付けられます。

MNS tackles the two problems associated with batch softmax described above: (1) Reducing selection bias: all items in the corpus have a chance to serve as negatives so that the retrieval model has better resolution towards fresh and long-tail items; 
MNSは、上記のバッチソフトマックスに関連する2つの問題に対処します。(1) 選択バイアスの軽減：コーパス内のすべてのアイテムがネガティブとして機能する機会を持つため、取得モデルは新鮮なアイテムやロングテールアイテムに対してより良い解像度を持ちます。
(2) Enabling more flexibility in controlling sampling distribution: the effective sampling distribution $Q$ is a mixture of item frequency based unigram distribution from training data and uniform distribution from index data. 
(2) サンプリング分布の制御における柔軟性の向上：効果的なサンプリング分布 $Q$ は、トレーニングデータからのアイテム頻度に基づくユニグラム分布とインデックスデータからの一様分布の混合です。
With a fixed batch size $B$, we are able to experiment with different $Q$ by adjusting $B[′]$. 
固定バッチサイズ $B$ を使用することで、$B[′]$ を調整することにより、異なる $Q$ を実験することができます。
$B[′]$ here can be tuned as a hyperparameter. 
ここでの $B[′]$ はハイパーパラメータとして調整可能です。

<!-- ここまで読んだ! あんま読んでないけど -->

### 4 CASE STUDY: GOOGLE PLAY APP RECOMMENDATION ケーススタディ: GOOGLE PLAY アプリ推薦

This section introduces how we apply the two-tower DNN modeling approach for the app recommendation in Google Play, as a realworld case study to experiment with our proposed method.
このセクションでは、提案した方法を実験するための実世界のケーススタディとして、Google Playにおけるアプリ推薦のために二塔DNNモデリングアプローチをどのように適用するかを紹介します。

### 4.1 System Overview システム概要

The app recommendation system for the app landing page in Google Play provides a slate of recommended apps to users when they are browsing a particular app (referred to as seed app). 
Google Playのアプリランディングページのアプリ推薦システムは、ユーザが特定のアプリ（シードアプリと呼ばれる）を閲覧しているときに、推奨アプリのリストを提供します。 
Figure 4 illustrates the high-level architecture of the system. 
図4は、システムの高レベルのアーキテクチャを示しています。 
Given a query represented as a concatenation of user, context, and seed app features, the system serves personalized app recommendations in a two-phase manner. 
ユーザ、コンテキスト、およびシードアプリの特徴を連結したクエリが与えられると、システムは二段階の方法でパーソナライズされたアプリ推薦を提供します。 
The system contains multiple candidate generation modules for retrieval, including both human-crafted rules and machine-learned models. 
システムは、手作りのルールと機械学習モデルの両方を含む、複数の候補生成モジュールを持っています。 
These modules retrieve hundreds of apps from the app corpus. 
これらのモジュールは、アプリコーパスから数百のアプリを取得します。 
Afterwards, all the apps retrieved are ranked by a reranking model. 
その後、取得されたすべてのアプリは、再ランキングモデルによってランク付けされます。

### 4.2 Google Playの二塔DNNモデル

![]()

We apply two-tower DNN model architecture for the retrieval problem in Google Play app recommendation. 
私たちは、Google Playアプリ推薦における検索問題のために二塔DNNモデルアーキテクチャを適用します。
As shown in Figure 5, the left tower and right tower learn latent representations of given query and candidate app, respectively. 
図5に示すように、左の塔と右の塔は、それぞれ与えられたクエリと候補アプリの潜在表現を学習します。
Here query features can be a mixture of features representing user, context and seed app, while candidate app features can be both sparse app IDs and content features (e.g., the category of an app). 
ここで、**クエリの特徴はユーザ、コンテキスト、シードアプリを表す特徴の混合であり、候補アプリの特徴はスパースなアプリIDとコンテンツ特徴量（例：アプリのカテゴリ）の両方**である可能性があります。
Our training data is constructed from logged user implicit feedback in the form of {query, candidate app} pairs, where candidate app is the next app which user installed from recommended apps. 
私たちのトレーニングデータは、{クエリ、候補アプリ}ペアの形で記録されたユーザの暗黙的フィードバックから構成されており、候補アプリはユーザが推薦されたアプリからインストールした次のアプリです。
To apply MNS, we prepare an index data including all of the candidate apps and corresponding content features with values from the most recent snapshot. 
MNSを適用するために、最新のスナップショットからの値を持つすべての候補アプリと対応するコンテンツ特徴を含むインデックスデータを準備します。

### 4.3 Indexing and Model Serving インデクシングとモデルサービング

In order to serve recommendations specially tailored based users’ real-time updates, we compute query embedding on the fly via the left tower in the model, while the candidate app embeddings are computed and indexed offline. 
ユーザのリアルタイム更新に特化した推薦を提供するために、モデルの左タワーを介してクエリ埋め込みを即座に計算し、**候補アプリの埋め込みはオフラインで計算およびインデックス化**します。
We build a fast nearest neighbor search service to retrieve top K most relevant candidate apps in the embedding space. 
埋め込み空間で最も関連性の高いトップKの候補アプリを取得するために、高速な最近傍探索サービスを構築します。
The indexer of the nearest neighbor search is built off-line by applying quantizied hashing and tree search algorithms [12, 22], enabling us to efficiently retrieve hundreds of candidate apps in real-time from a large corpus of millions of apps.
最近傍探索のインデクサーは、量子化ハッシングとツリー探索アルゴリズム[12, 22]を適用して**オフラインで構築**されており、数百万のアプリの大規模コーパスからリアルタイムで数百の候補アプリを効率的に取得できるようにしています。

<!-- ここまで読んだ! -->

### 5 EXPERIMENT RESULTS 実験結果

We demonstrate the effectiveness of our proposed technique via extensive offline experiments on real-world Google Play data. 
私たちは、実世界のGoogle Playデータに基づく広範なオフライン実験を通じて、提案した手法の有効性を示します。
In addition, live experiments on Google Play also show that the twotower model with MNS delivered significant top-line metric wins.
さらに、Google Playでのライブ実験でも、MNSを用いたtwotowerモデルが重要なトップラインメトリックの勝利をもたらしたことが示されています。

### 5.1 オフライン研究

We train the model on 30 days’ rolling window of Google Play’s logged data and evaluate on the 31st day. 
私たちは、Google Playのログデータの30日間のローリングウィンドウでモデルを訓練し、31日目に評価を行います。 
To account for weekly pattern, we repeat the evaluation for 7 times and each time we move the rolling window by 1 day. 
週ごとのパターンを考慮するために、評価を7回繰り返し、毎回ローリングウィンドウを1日ずつ移動させます。 
We report the average metric across the 7 train-eval datasets. 
7つの訓練-評価データセット全体の平均指標を報告します。 
For a given {query, candidate app} pair in the eval-set, we find the top k nearest neighbors in the embedding space for the query. 
評価セット内の特定の{クエリ、候補アプリ}ペアに対して、クエリの埋め込み空間内で上位kの最近傍を見つけます。 
Recall is the main optimization objective in the retrieval phase of our app recommendation system. 
リコールは、私たちのアプリ推薦システムの取得フェーズにおける主要な最適化目標です。 
We thus report Recall@K, i.e., the average probability for the candidate apps to appear among the top k nearest neighbors retrieved for the query, as our offline metric. 
したがって、私たちはRecall@K、すなわち、候補アプリがクエリのために取得された上位kの最近傍に現れる平均確率をオフライン指標として報告します。 

**Effectiveness of MNS. To understand the effectiveness of MNS,** 
**MNSの効果を理解するために、** 

we experiment with the following 3 algorithms: 
次の3つのアルゴリズムを実験します： 

(1) MLP with sampled softmax without app content features. 
(1) アプリコンテンツ特徴量なしのサンプリングソフトマックスを用いたMLP。
This is the latest production retrieval system and thus serves as our baseline; 
これは最新のプロダクション取得システムであり、したがって私たちのベースラインとなります； 
(2) Two-tower DNN with batch negative sampling; 
(2) バッチネガティブサンプリングを用いたツータワーDNN； 
(3) Two-tower DNN with MNS. 
(3) MNSを用いたツータワーDNN。 
Table 1 reports the results. 
表1は結果を報告します。 

For MLP with sampled softmax model, we use a two-layer DNN with hidden layer sizes [1024, 128] to encode query. 
サンプリングソフトマックスモデルのMLPでは、隠れ層サイズ[1024, 128]の2層DNNを使用してクエリをエンコードします。 
For the twotower model, we use feed forward layers with hidden layer sizes [512, 128] for both left and right towers. 
**ツータワーモデルでは、左と右のタワーの両方に対して隠れ層サイズ[512, 128]のフィードフォワード層を使用**します。
(つまり、入力層 -> 隠れ層1:512次元 -> 隠れ層2:128次元 = 埋め込み表現ってことか??:thinking_face: 128が埋め込み次元ってことかな??:thinking_face:)
It is worth noting that the two-tower and MLP models have roughly the same number of model parameters, 
**ツータワーとMLPモデルはほぼ同じ数のモデルパラメータを持つことに注意**する価値があります。 
since each of the two towers has half the size of the MLP model and the same embedding sizes are used for the input features across all models. 
各タワーはMLPモデルの半分のサイズを持ち、すべてのモデルで入力特徴に同じ埋め込みサイズが使用されているためです。 
We ensure that the effective sample size in negative sampling is 2048 across all the 3 models as shown in Table 1. 
表1に示すように、ネガティブサンプリングにおける有効サンプルサイズが3つのモデルすべてで2048であることを確認します。 
We train both types of models using Adagrad as optimizer with learning rate at 0.01. 
両方のタイプのモデルを、**学習率0.01のAdagradを最適化手法として使用**して訓練します。 
ReLU is used as activation function for all hidden layers except that no activation is used for top hidden layers. 
**ReLUは、最上位の隠れ層には活性化が使用されない以外のすべての隠れ層の活性化関数として使用されます**。 

From Table 1, we observe that batch negative sampling performs worse than sampled softmax even it incorporates extra app content features. 
表1から、バッチネガティブサンプリングはサンプリングソフトマックスよりもパフォーマンスが劣ることがわかりますが、追加のアプリコンテンツ特徴を組み込んでいます。 
We observe quite a few irrelevant tail apps in its retrieval results. 
その取得結果には、無関係なテールアプリがかなり多く見られます。 
This observation supports our hypothesis that batch softmax suffers from selection bias. 
この観察は、バッチソフトマックスが選択バイアスに苦しんでいるという私たちの仮説を支持します。 
Low-quality tail apps do not appear as negatives frequent enough. 
低品質のテールアプリは、ネガティブとして十分に頻繁に現れません。 
As such, they are not demoted as they should have been during training. 
そのため、彼らは訓練中にそうあるべきだったように降格されません。 
Another observation from Table 1 is that Mixed Negative Sampling performs the best as expected. 
表1からのもう一つの観察は、Mixed Negative Samplingが期待通りに最も良いパフォーマンスを発揮することです。 
Compared with MLP with sampled softmax, MNS includes extra app content features. 
サンプリングソフトマックスを用いたMLPと比較して、MNSは追加のアプリコンテンツ特徴を含みます。 
Compared with batch negative sampling, it reduces the selection bias. 
バッチネガティブサンプリングと比較して、選択バイアスを減少させます。 

**Hyper-parameter B[′] for MNS.** We further explore the MNS strategy by looking at how Recall@K changes under different index data batch size B[′] with a fixed training batch size B. 
**MNS戦略をさらに探る。** 固定されたトレーニングバッチサイズBで、異なるインデックスデータバッチサイズB[′]の下でRecall@Kがどのように変化するかを見ることで、MNS戦略をさらに探ります。
Table 2 reports the results. 
表2は結果を報告します。 
Our model performs the best when B[′] is 8192, according to offline tuning of B[′] as a hyper-parameter. 
私たちのモデルは、B[′]をハイパーパラメータとしてオフラインで調整した結果、B[′]が8192のときに最も良いパフォーマンスを発揮します。 
We conjecture that although further increasing B[′] results in a larger sample size, it leads to a sampling distribution too close to the uniform distribution. 
B[′]をさらに増加させるとサンプルサイズが大きくなるものの、サンプリング分布が一様分布に近づきすぎると推測します。 
It deviates from the desired serving time distribution and thus hurts the model quality. 
それは望ましいサービス時間分布から逸脱し、したがってモデルの品質を損ないます。 
Besides, large index batch size B[′] significantly increases the training cost and therefore a reasonable size B[′] is preferred. 
さらに、大きなインデックスバッチサイズB[′]は訓練コストを大幅に増加させるため、合理的なサイズのB[′]が好まれます。  

<!-- ここまで読んだ! -->

### 5.2 Online A/B testing オンラインA/Bテスト

Beyond offline studies, we conduct live experiments (A/B testing) for 2 weeks. 
オフライン研究を超えて、私たちは2週間のライブ実験（A/Bテスト）を実施します。
The control group consists of 1% randomly selected users, who are presented with app suggestions made by the production recommendation system using a sampled softmax model. 
コントロールグループは、サンプリングされたソフトマックスモデルを使用して、製品推薦システムによって作成されたアプリの提案を提示される**1%のランダムに選ばれたユーザ**ーで構成されています。
Similarly, we set up two 1% experiment groups to present app suggestions from two-tower models with batch negative sampling, and with MNS, respectively. 
同様に、バッチネガティブサンプリングを使用したツータワーモデルとMNSからのアプリ提案を提示するために、**2つの1%の実験グループ**を設定します。(合計3%のユーザを対象にオンラインテストしたのか...!:thinking_face:)
We report High-quality App Install Gain as our top-line metric here. 
ここでは、高品質アプリインストール増加を私たちの主要な指標として報告します。
We define High-quality App Install as the number of apps that users actually used after installing, as opposed to uninstalling within 1 day or having no usage. 
高品質アプリインストールを、ユーザーがインストール後に実際に使用したアプリの数と定義します。これは、1日以内にアンインストールしたり、使用しなかったりすることとは対照的です。

As shown in Table 3, compared with the production sampled softmax model, two-tower using batch softmax is significantly worse, while using MNS improves High-quality App Installs by +1.54% with statistical significance. 
表3に示すように、製品のサンプリングされたソフトマックスモデルと比較して、バッチソフトマックスを使用したツータワーは著しく劣っており、一方でMNSを使用すると高品質アプリインストールが+1.54%改善され、統計的に有意です。
In our side-by-side comparisons, we also observe more relevant app recommendations from two-tower model with MNS. 
私たちの並行比較では、**MNSを使用したツータワーモデルからより関連性の高いアプリの推薦**も観察されます。(item2itemの推薦にもいい感じに適用できたってことか...!:thinking_face:)

<!-- ここまで読んだ! -->

### 6 CONCLUSION 結論

This paper introduced novel sampling approach called Mixed Negative Sampling for training two-tower neural network for large corpus item retrieval in recommendations. 
本論文では、推薦における大規模コーパスアイテムの取得のために、二塔型ニューラルネットワークを訓練するための新しいサンプリングアプローチであるMixed Negative Samplingを紹介しました。
We discussed the selection bias of the commonly used batch negative sampling method, and showed that MNS is effective in reducing such bias by additionally sampling uniform negatives from the item corpus. 
一般的に使用されるバッチネガティブサンプリング法の選択バイアスについて議論し、アイテムコーパスから均一なネガティブを追加でサンプリングすることで、MNSがそのバイアスを減少させるのに効果的であることを示しました。
We applied the MNS-based two-tower modeling approach to build a retrieval model for Google Play. 
MNSに基づく二塔型モデリングアプローチを適用して、Google Playのための取得モデルを構築しました。
This new model is able to incorporate rich content features of apps, and thus resolves the cold-start problem of the old system. 
この新しいモデルは**アプリの豊富なコンテンツ特徴を取り入れることができ、古いシステムのコールドスタート問題を解決**します。(これがtwo-towerモデルの利点の一つなのかな...!:thinking_face:)
Lastly, we demonstrated the effectiveness of our approach by showing both offline and online improvements. 
最後に、オフラインおよびオンラインの改善を示すことで、私たちのアプローチの効果を実証しました。

<!-- ここまで読んだ! -->

### REFERENCES 参考文献

[1] Yoshua Bengio and Jean-Sébastien Sénécal. 2003. Quick Training of Probabilistic Neural Nets by Importance Sampling. In Proceedings of the conference on Artificial _Intelligence and Statistics (AISTATS)._  
[1] ヨシュア・ベンジオとジャン＝セバスチャン・セネカル。2003年。重要度サンプリングによる確率的ニューラルネットの迅速なトレーニング。人工知能と統計に関する会議の議事録において。

[2] Y. Bengio and J. S. Senecal. 2008. Adaptive Importance Sampling to Accelerate Training of a Neural Probabilistic Language Model. Trans. Neur. Netw. 19, 4 (April [2008), 713–722. https://doi.org/10.1109/TNN.2007.912312](https://doi.org/10.1109/TNN.2007.912312)  
[2] Y. ベンジオと J. S. セネカル。2008年。ニューラル確率的言語モデルのトレーニングを加速するための適応的な重要度サンプリング。神経ネットワークのトランザクション 19, 4 (2008年4月), 713–722。

[3] Minmin Chen, Alex Beutel, Paul Covington, Sagar Jain, Francois Belletti, and Ed Chi. 2018. Top-K Off-Policy Correction for a REINFORCE Recommender System.  
[3] ミンミン・チェン、アレックス・ビュートル、ポール・コビントン、サガル・ジャイン、フランソワ・ベレッティ、エド・チー。2018年。REINFORCE推薦システムのためのTop-Kオフポリシー補正。

[arXiv:cs.LG/1812.02353](https://arxiv.org/abs/cs.LG/1812.02353)  
[arXiv:cs.LG/1812.02353](https://arxiv.org/abs/cs.LG/1812.02353)

[4] Tianqi Chen, Weinan Zhang, Qiuxia Lu, Kailong Chen, Zhao Zheng, and Yong Yu. 2012. SVDFeature: A Toolkit for Feature-based Collaborative Filtering. J.  
[4] ティアンチー・チェン、ウェイナン・ジャン、キュウシア・ル、カイロン・チェン、ジャオ・ジェン、ヨン・ユー。2012年。SVDFeature: 特徴ベースの協調フィルタリングのためのツールキット。J.

_[Mach. Learn. Res. 13, 1 (Dec. 2012), 3619–3622. http://dl.acm.org/citation.cfm?](http://dl.acm.org/citation.cfm?id=2503308.2503357)_  
_[Mach. Learn. Res. 13, 1 (2012年12月), 3619–3622。](http://dl.acm.org/citation.cfm?id=2503308.2503357)_

[id=2503308.2503357](http://dl.acm.org/citation.cfm?id=2503308.2503357)  
[id=2503308.2503357](http://dl.acm.org/citation.cfm?id=2503308.2503357)

[5] Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra, Hrishi Aradhye, Glen Anderson, Greg Corrado, Wei Chai, Mustafa Ispir, Rohan Anil, Zakaria Haque, Lichan Hong, Vihan Jain, Xiaobing Liu, and Hemal Shah. 2016. Wide & Deep Learning for Recommender Systems. arXiv:1606.07792 (2016).  
[5] チェン・ヘンツェ、レヴェント・コク、ジェレマイア・ハームセン、タル・シャケド、トゥシャール・チャンドラ、フリシ・アラディエ、グレン・アンダーソン、グレッグ・コラード、ウェイ・チャイ、ムスタファ・イスピル、ロハン・アニル、ザカリア・ハク、リチャン・ホン、ヴィハン・ジャイン、シャオビン・リウ、ヘマル・シャー。2016年。推薦システムのためのWide & Deep Learning。arXiv:1606.07792 (2016年)。

[http://arxiv.org/abs/1606.07792](http://arxiv.org/abs/1606.07792)  
[http://arxiv.org/abs/1606.07792](http://arxiv.org/abs/1606.07792)

[6] Muthuraman Chidambaram, Yinfei Yang, Daniel Cer, Steve Yuan, Yun-Hsuan Sung, Brian Strope, and Ray Kurzweil. 2018. Learning Cross-Lingual Sentence Representations via a Multi-task Dual-Encoder Model. CoRR abs/1810.12836 (2018).  
[6] ムトゥラマン・チダンバラム、インフェイ・ヤン、ダニエル・セール、スティーブ・ユアン、ユン・シュアン・スン、ブライアン・ストロープ、レイ・カーツワイル。2018年。マルチタスクデュアルエンコーダモデルを介したクロスリンガル文表現の学習。CoRR abs/1810.12836 (2018年)。

[7] Paul Covington, Jay Adams, and Emre Sargin. 2016. Deep Neural Networks for YouTube Recommendations. In Proceedings of the 10th ACM Conference on _Recommender Systems. New York, NY, USA._  
[7] ポール・コビントン、ジェイ・アダムス、エムレ・サルギン。2016年。YouTube推薦のための深層ニューラルネットワーク。第10回ACM推薦システム会議の議事録において。

[8] Daniel Gillick, Alessandro Presta, and Gaurav Singh Tomar. 2018. End-to-End [Retrieval in Continuous Space. arXiv:cs.IR/1811.08008](https://arxiv.org/abs/cs.IR/1811.08008)  
[8] ダニエル・ギリック、アレッサンドロ・プレスタ、ガウラブ・シン・トマール。2018年。連続空間におけるエンドツーエンドの検索。arXiv:cs.IR/1811.08008。

[9] Carlos A. Gomez-Uribe and Neil Hunt. 2015. The Netflix Recommender System: Algorithms, Business Value, and Innovation. ACM Trans. Manage. Inf. Syst. 6, 4, [Article 13 (Dec. 2015), 19 pages. https://doi.org/10.1145/2843948](https://doi.org/10.1145/2843948)  
[9] カルロス・A・ゴメス・ウリベとニール・ハント。2015年。Netflix推薦システム: アルゴリズム、ビジネス価値、イノベーション。ACM管理情報システムトランザクション 6, 4, [記事13 (2015年12月), 19ページ。](https://doi.org/10.1145/2843948)

[10] Ian Goodfellow, Yoshua Bengio, and Aaron Courville. 2016. Deep Learning. MIT [Press. http://www.deeplearningbook.org.](http://www.deeplearningbook.org)  
[10] イアン・グッドフェロー、ヨシュア・ベンジオ、アーロン・クールビル。2016年。深層学習。MITプレス。

[11] Joshua Goodman. 2001. Classes for Fast Maximum Entropy Training. In ICASSP.  
[11] ジョシュア・グッドマン。2001年。迅速な最大エントロピー学習のためのクラス。ICASSPにおいて。

[12] Ruiqi Guo, Sanjiv Kumar, Krzysztof Choromanski, and David Simcha. 2016. Quantization based Fast Inner Product Search. In Proceedings of the 19th International _Conference on Artificial Intelligence and Statistics, Vol. 51. PMLR._  
[12] ルイチ・グオ、サンジブ・クマール、クシシュトフ・コロマンスキー、デイビッド・シムチャ。2016年。量子化に基づく高速内積検索。第19回国際人工知能と統計に関する会議の議事録において、ボリューム51。

[13] Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, and Tat-Seng Chua. 2017. Neural Collaborative Filtering. In Proceedings of the 26th International _Conference on World Wide Web (Perth, Australia) (WWW ’17). International World_ Wide Web Conferences Steering Committee, Republic and Canton of Geneva,  
[13] シャンナン・ハ、リジ・リャオ、ハンワン・ジャン、リキアン・ニエ、シャ・フー、タット・セン・チュア。2017年。ニューラル協調フィルタリング。第26回国際ワールドワイドウェブ会議の議事録において（パース、オーストラリア）（WWW '17）。国際ワールドワイドウェブ会議運営委員会、ジュネーブ共和国とカントン。

-----
Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations WWW ’20 Companion, April 20–24, 2020, Taipei, Taiwan  
[Mixed Negative Sampling for Learning Two-tower Neural Networks in Recommendations WWW ’20 Companion, April 20–24, 2020, Taipei, Taiwan](https://doi.org/10.1145/3038912.3052569)

[14] Y. Hu, Y. Koren, and C. Volinsky. 2008. Collaborative Filtering for Implicit Feedback Datasets. In 2008 Eighth IEEE International Conference on Data Mining.  
[14] Y. フー、Y. コレン、C. ボリンスキー。2008年。暗黙のフィードバックデータセットのための協調フィルタリング。2008年第8回IEEE国際データマイニング会議において。

[263–272. https://doi.org/10.1109/ICDM.2008.22](https://doi.org/10.1109/ICDM.2008.22)  
[263–272.](https://doi.org/10.1109/ICDM.2008.22)

[15] David C. Liu, Stephanie Rogers, Raymond Shiau, Dmitry Kislyuk, Kevin C. Ma, Zhigang Zhong, Jenny Liu, and Yushi Jing. 2017. Related Pins at Pinterest: The Evolution of a Real-World Recommender System. In WWW.  
[15] デイビッド・C・リウ、ステファニー・ロジャース、レイモンド・シャイアウ、ドミトリー・キスリュク、ケビン・C・マ、ジガン・ジョン、ジェニー・リウ、ユシ・ジン。2017年。Pinterestにおける関連ピン: 実世界の推薦システムの進化。WWWにおいて。

[16] Lajanugen Logeswaran and Honglak Lee. 2018. An efficient framework for learning sentence representations. In International Conference on Learning Repre_[sentations. https://openreview.net/forum?id=rJvJXZb0W](https://openreview.net/forum?id=rJvJXZb0W)_  
[16] ラジャヌゲン・ロゲスワランとホンラク・リー。2018年。文表現を学習するための効率的なフレームワーク。表現学習に関する国際会議において。

[17] Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean. 2013. Efficient Estimation of Word Representations in Vector Space. abs/1301.3781 (2013).  
[17] トマス・ミコロフ、カイ・チェン、グレッグ・コラード、ジェフリー・ディーン。2013年。ベクトル空間における単語表現の効率的な推定。abs/1301.3781 (2013年)。

[18] Frederic Morin and Yoshua Bengio. 2005. Hierarchical Probabilistic Neural Network Language Model. In AISTATS.  
[18] フレデリック・モランとヨシュア・ベンジオ。2005年。階層的確率的ニューラルネットワーク言語モデル。AISTATSにおいて。

[19] Paul Neculoiu, Maarten Versteegh, and Mihai Rotaru. 2016. Learning Text Similarity with Siamese Recurrent Networks. In Proceedings of the 1st Workshop _on Representation Learning for NLP. Association for Computational Linguistics,_  
[19] ポール・ネクルオイウ、マールテン・フェルステーグ、ミハイ・ロタル。2016年。双子の再帰ネットワークを用いたテキスト類似性の学習。NLPのための表現学習に関する第1回ワークショップの議事録において。

[Berlin, Germany, 148–157. https://doi.org/10.18653/v1/W16-1617](https://doi.org/10.18653/v1/W16-1617)  
[ベルリン、ドイツ、148–157。](https://doi.org/10.18653/v1/W16-1617)

[20] Shumpei Okura, Yukihiro Tagami, Shingo Ono, and Akira Tajima. 2017.  
[20] 大倉俊平、田上幸宏、小野慎吾、田島明。2017年。

Embedding-based News Recommendation for Millions of Users. In KDD.  
数百万のユーザーのための埋め込みベースのニュース推薦。KDDにおいて。

[21] S. Rendle. 2010. Factorization Machines. In 2010 IEEE International Conference on _[Data Mining. 995–1000. https://doi.org/10.1109/ICDM.2010.127](https://doi.org/10.1109/ICDM.2010.127)_  
[21] S. レンドル。2010年。因子分解マシン。2010年IEEE国際データマイニング会議において。

[22] Xiang Wu, Ruiqi Guo, Ananda Theertha Suresh, Sanjiv Kumar, Daniel N Holtmann-Rice, David Simcha, and Felix Yu. 2017. Multiscale Quantization for Fast Similarity Search. In Advances in Neural Information Processing Systems _30._  
[22] シャン・ウー、ルイチ・グオ、アナンダ・ティールタ・スレッシュ、サンジブ・クマール、ダニエル・N・ホルトマン・ライス、デイビッド・シムチャ、フェリックス・ユー。2017年。高速類似検索のためのマルチスケール量子化。神経情報処理システムの進歩において、30。

[23] Yinfei Yang, Steve Yuan, Daniel Cer, Sheng-Yi Kong, Noah Constant, Petr Pilar, Heming Ge, Yun-hsuan Sung, Brian Strope, and Ray Kurzweil. 2018. Learning Semantic Textual Similarity from Conversations. In Proceedings of The Third _Workshop on Representation Learning for NLP. Association for Computational_  
[23] インフェイ・ヤン、スティーブ・ユアン、ダニエル・セール、シェン・イー・コン、ノア・コンスタント、ペトル・ピラール、ヘミング・ゲ、ユン・シュアン・スン、ブライアン・ストロープ、レイ・カーツワイル。2018年。会話からの意味的テキスト類似性の学習。NLPのための表現学習に関する第3回ワークショップの議事録において。

[Linguistics, Melbourne, Australia, 164–174. https://www.aclweb.org/anthology/](https://www.aclweb.org/anthology/W18-3022) [W18-3022](https://www.aclweb.org/anthology/W18-3022)  
[言語学、メルボルン、オーストラリア、164–174。](https://www.aclweb.org/anthology/W18-3022)

[24] Xinyang Yi, Ji Yang, Lichan Hong, Derek Zhiyuan Cheng, Lukasz Heldt, Aditee Ajit Kumthekar, Zhe Zhao, Li Wei, and Ed Chi. 2019. Sampling-Bias-Corrected Neural Modeling for Large Corpus Item Recommendations. 13th ACM Conference _on Recommender Systems. Copenhagen, Denmark (2019)._  
[24] シンヤン・イー、ジ・ヤン、リチャン・ホン、デレク・ジーユアン・チェン、ルカシュ・ヘルド、アディテ・アジット・クムテカール、ゼ・ジャオ、リ・ウェイ、エド・チー。2019年。大規模コーパスアイテム推薦のためのサンプリングバイアス補正ニューラルモデリング。第13回ACM推薦システム会議。コペンハーゲン、デンマーク（2019年）。

[25] Andrew Zhai, Dmitry Kislyuk, Yushi Jing, Michael Feng, Eric Tzeng, Jeff Donahue, Yue Li Du, and Trevor Darrell. 2017. Visual Discovery at Pinterest. (02 2017).  
[25] アンドリュー・ザイ、ドミトリー・キスリュク、ユシ・ジン、マイケル・フェン、エリック・ツェン、ジェフ・ドナヒュー、ユエ・リ・デュ、トレバー・ダレル。2017年。Pinterestにおける視覚的発見。(2017年2月)。
