refs: https://arxiv.org/html/2504.02137v1

# Enhancing Embedding Representation Stability in Recommendation Systems with Semantic ID
# セマンティックIDを用いた推薦システムにおける埋め込み表現の安定性向上

## Abstract

The exponential growth of online content has posed significant challenges to ID-based models in industrial recommendation systems, ranging from extremely high cardinality and dynamically growing ID space, to highly skewed engagement distributions, to prediction instability as a result of natural id life cycles (e.g, the birth of new IDs and retirement of old IDs).  
オンラインコンテンツの指数関数的な成長は、IDベースのモデルに対して重要な課題を提起しています。これには、**非常に高いカーディナリティや動的に成長するID空間**、偏ったエンゲージメント分布、自然なIDライフサイクル（例：新しいIDの誕生や古いIDの引退）による予測の不安定性が含まれます。
To address these issues, many systems rely on random hashing to handle the id space and control the corresponding model parameters (i.e embedding table). 
これらの問題に対処するために、多くのシステムはID空間を処理し、対応するモデルパラメータ（すなわち埋め込みテーブル）を制御するためにランダムハッシングに依存しています。
(特徴量に基づく埋め込みモデルみたいな意味??:thinking:)
However, this approach introduces data pollution from multiple ids sharing the same embedding, leading to degraded model performance and embedding representation instability.
しかし、このアプローチは、同じ埋め込みを共有する複数のIDからのデータ汚染を引き起こし、モデルのパフォーマンスの低下や埋め込み表現の不安定性をもたらします。

<!-- ここまで読んだ! -->

This paper examines these challenges and introduces Semantic ID prefix ngram, a novel token parameterization technique that significantly improves the performance of the original Semantic ID.  
本論文では、これらの課題を検討し、元のセマンティックIDのパフォーマンスを大幅に向上させる新しいトークンパラメータ化技術であるSemantic ID prefix ngramを紹介します。
Semantic ID prefix ngram creates semantically meaningful collisions by hierarchically clustering items based on their content embeddings, as opposed to random assignments.  
Semantic ID prefix ngramは、ランダムな割り当てではなく、コンテンツ埋め込みに基づいてアイテムを階層的にクラスタリングすることにより、意味的に有意義な衝突を生成します。
Through extensive experimentation, we demonstrate that Semantic ID prefix ngram not only addresses embedding instability but also significantly improves tail id modeling, reduces overfitting, and mitigates representation shifts.  
広範な実験を通じて、Semantic ID prefix ngramが埋め込みの不安定性に対処するだけでなく、テールIDモデリングを大幅に改善し、過学習を減少させ、表現のシフトを緩和することを示します。
We further highlight the advantages of Semantic ID prefix ngram in attention-based models that contextualize user histories, showing substantial performance improvements.  
さらに、**ユーザの履歴を文脈化するattentionベースのモデル**におけるSemantic ID prefix ngramの利点を強調し、実質的なパフォーマンスの向上を示します。
We also report our experience of integrating Semantic ID into Meta production Ads Ranking system, leading to notable performance gains and enhanced prediction stability in live deployments.  
また、Semantic IDをMetaの製品広告ランキングシステムに統合した経験を報告し、ライブ展開における顕著なパフォーマンス向上と予測の安定性の向上をもたらしました。

<!-- ここまで読んだ! -->

## 1Introduction 1 はじめに

Item recommendation can involve many signal-rich features, including categorical features corresponding to item IDs. 
アイテム推薦は、アイテムIDに対応するカテゴリカル特徴を含む、多くの信号豊富な特徴を含むことがあります。
The raw item IDs are usually mapped to embeddings, which are then further processed by deep learning-based model architectures such as the widely deployed Deep Learning Recommendation Model (DLRM)(Covington etal.,2016; Naumov etal.,2019). 
**生のアイテムIDは通常、埋め込みにマッピングされ**(=entity embedding)、その後、広く展開されている深層学習推薦モデル（DLRM）（Covington etal.,2016; Naumov etal.,2019）などの深層学習ベースのモデルアーキテクチャによってさらに処理されます。
However, in industry-scale online settings, several key data-related challenges have emerged in learning item embedding representations. 
しかし、産業規模のオンライン環境では、**アイテム埋め込み表現を学習する際にいくつかの重要なデータ関連の課題**が浮上しています。
In particular, item cardinality, the huge number of total items; impression skew, the fact that only a few items comprise most user impressions or conversions(Milojević,2010); and ID drifting, or the majority of items entering and leaving the system within short time periods(Gama etal.,2014). 
特に、アイテムのカーディナリティ（総アイテム数の巨大さ）、インプレッションの偏り（ほとんどのユーザーインプレッションやコンバージョンを占めるのはごく少数のアイテムである事実（Milojević,2010））、およびIDの漂流（短期間にシステムに出入りするアイテムの大多数）（Gama etal.,2014）です。

<!-- ここまで読んだ! -->

A popular and simple approach to learning embedding representations is random hashing, where raw item IDs are randomly hashed to share the same embedding(Zhang etal.,2020). 
埋め込み表現を学習するための一般的でシンプルなアプローチは、ランダムハッシングであり、生のアイテムIDがランダムにハッシュされて同じ埋め込みを共有します（Zhang etal.,2020）。
Hashing is used due to the large item cardinality and system constraints on embedding table sizes. 
ハッシングは、大きなアイテムカーディナリティと埋め込みテーブルサイズに対するシステムの制約のために使用されます。
However, random hashing and ID drifting together lead to undesirable embedding representation instability when the model is trained over long time periods. 
しかし、ランダムハッシングとIDの漂流が組み合わさると、モデルが長期間にわたってトレーニングされる際に望ましくない埋め込み表現の不安定性を引き起こします。
This is due to the nature of random hash collisions, which result in contradictory gradient updates to the embedding weights. 
これは、ランダムハッシュの衝突の性質によるもので、埋め込み重みへの矛盾した勾配更新をもたらします。
Further, as the items in the system change over time from ID drifting, the learning from old items is lost and the embedding weights for new items are essentially random. 
さらに、システム内のアイテムがIDの漂流により時間とともに変化するにつれて、古いアイテムからの学習が失われ、新しいアイテムの埋め込み重みは本質的にランダムになります。
This approach is ill-suited for items with few impressions, which are the majority of items due to impression skew. 
このアプローチは、インプレッションの偏りにより大多数を占めるインプレッションの少ないアイテムには不適切です。

<!-- ここまで読んだ! ランダムハッシングはまだよくわかってないけど -->

To mitigate these drawbacks, a stable ID space is needed. 
**これらの欠点を軽減するためには、安定したID空間が必要**です。
A stable ID space ideally ensures that a learned embedding representation has a stable meaning as the model learns from more data. 
理想的な安定したID空間は、モデルがより多くのデータから学習するにつれて、学習された埋め込み表現が安定した意味を持つことを保証します。
In this work, we investigate a recently proposed item representation approach called Semantic ID(Singh etal.,2023; Rajput etal.,2024) as a candidate for a stable ID space. 
**本研究では、安定したID空間の候補として、Semantic ID（Singh etal.,2023; Rajput etal.,2024）と呼ばれる最近提案されたアイテム表現アプローチを調査**します。
Semantic ID derives item IDs based on hierarchical clusters learned from the semantic similarity of items as given by their text, image, or video content. 
Semantic IDは、テキスト、画像、またはビデオコンテンツによって与えられたアイテムの意味的類似性から学習された階層的クラスタに基づいてアイテムIDを導出します。
A given item’s Semantic ID is then mapped to embedding representations via a parameterization scheme. 
特定のアイテムのSemantic IDは、**パラメータ化スキームを介して埋め込み表現にマッピング**されます。(意味よくわかってない...!:thinking:)
Importantly, the ID space of Semantic ID is fixed a priori and has semantic meaning – meaning that it can address embedding representation instability. 
重要なことに、Semantic IDのID空間は事前に固定されており、意味的な意味を持っています。つまり、埋め込み表現の不安定性に対処できるということです。(?)
However, one challenge in using Semantic ID in recommendation modeling is defining a mapping from its cluster assignments to the embedding table. 
しかし、推薦モデリングにおけるSemantic IDの使用における一つの課題は、そのクラスタ割り当てから埋め込みテーブルへのマッピングを定義することです。

The main contributions of this paper are: 
本論文の主な貢献は以下の通りです：

- Using experiments on a simplified version of Meta’s production ads ranking model, we deepen the empirical understanding of how Semantic ID improves embedding representation stability. 
Metaの製品広告ランキングモデルの簡略化されたバージョンに関する実験を使用して、**Semantic IDが埋め込み表現の安定性をどのように改善するかについての経験的理解**を深めます。
We further propose Semantic ID prefix-ngram, a novel token parameterization technique on top of Semantic ID that brings significant performance gains compared to the original Semantic ID introduced in(Singh etal.,2023). 
さらに、Semantic IDの上に新しいトークンパラメータ化技術であるSemantic ID prefix-ngramを提案し、（Singh etal.,2023）で導入された元のSemantic IDと比較して重要な性能向上をもたらします。

- We characterize the item data distribution in terms of the number of items (item cardinality), the fact that most items have few impressions (impression skew), and the short item lifetime in the system (ID drifting) and explain their connection with embedding representation stability. 
アイテムデータ分布を、アイテムの数（アイテムカーディナリティ）、ほとんどのアイテムが少ないインプレッションを持つ事実（インプレッションの偏り）、およびシステム内の短いアイテムライフタイム（ID漂流）の観点から特徴付け、それらの埋め込み表現の安定性との関係を説明します。

- We describe the productionization of Semantic ID prefix-ngram into both sparse and sequential features in Meta’s production system. 
Semantic ID prefix-ngramをMetaの製品システムにおけるスパースおよび逐次特徴の両方に本番活用(productionization)する方法を説明します。
We show that adding these features brings online performance gains and improves online prediction stability. 
これらの特徴を追加することでオンラインパフォーマンスの向上が得られ、オンライン予測の安定性が向上することを示します。

<!-- ここまで読んだ! -->

In offline experiments on Meta’s ads ranking data, we show that Semantic ID improves generalization and is less sensitive to distribution shift compared to random hashing. 
Metaの広告ランキングデータに関するオフライン実験では、Semantic IDが一般化を改善し、ランダムハッシングと比較して分布のシフトに対して敏感でないことを示します。
Confirming our hypothesis on impression skew, we find that most gains from Semantic ID come from the long tail of the item distribution. 
インプレッションの偏りに関する私たちの仮説を確認し、Semantic IDからのほとんどの利益がアイテム分布のロングテールから来ることを発見しました。
We show that by incorporating hierarchical cluster information, the proposed prefix-ngram is crucial to Semantic ID’s effectiveness. 
階層的クラスタ情報を取り入れることで、提案されたprefix-ngramがSemantic IDの効果にとって重要であることを示します。
We also demonstrate that semantic similarity translates to prediction similarity in both online and offline settings (Section 6.3 and Section 7.4). 
また、意味的類似性がオンラインおよびオフラインの両方の設定において予測の類似性に変換されることを示します（セクション6.3およびセクション7.4）。
Further, Semantic ID results in outsized gains when incorporated in contextualizing models of users’ item interaction history. 
さらに、**Semantic IDはユーザーのアイテムインタラクション履歴を文脈化するモデルに組み込まれると、過大な利益をもたらします**。

In an online setting, we describe the implementation of Semantic ID prefix-ngram features in Meta’s production ads recommendation system, where they serve as the top sparse features by feature importance and result in 0.15% online performance gain. 
オンライン環境では、Metaの製品広告推薦システムにおけるSemantic ID prefix-ngram特徴の実装を説明します。ここでは、特徴の重要性によってトップスパース特徴として機能し、0.15%のオンラインパフォーマンス向上をもたらします。
Finally, we find that incorporating Semantic ID features significantly reduces the model’s prediction variance for the same item. 
最後に、Semantic ID特徴を組み込むことで、同じアイテムに対するモデルの予測分散が大幅に減少することがわかります。
This is crucial to ensure advertisers’ trust in Meta’s recommendation system and to improve stability of the final item ranking. 
これは、広告主がMetaの推薦システムを信頼することを保証し、最終的なアイテムランキングの安定性を向上させるために重要です。

<!-- ここまで読んだ! -->

The remaining sections are organized as follows: 
残りのセクションは以下のように構成されています：
Section 2 explains related work. 
セクション2では関連研究を説明します。
Section 3 provides an overview of the ranking model. 
セクション3ではランキングモデルの概要を提供します。
Section 4 introduces Semantic ID and token parameterization. 
セクション4ではSemantic IDとトークンパラメータ化を紹介します。
Section 5 explains the three item impression distribution challenges. 
セクション5では3つのアイテムインプレッション分布の課題を説明します。
Section 6 describes the offline experiments. 
セクション6ではオフライン実験を説明します。
Section 7 describes the productionization of Semantic ID at Meta and the online experiments. 
セクション7ではMetaにおけるSemantic IDの生産化とオンライン実験を説明します。
Section 8 concludes. 
セクション8で結論を述べます。

<!-- ここまで読んだ! -->

## 2Related Work 2関連研究

#### Item representations in recommendation 推薦におけるアイテム表現

Many modern deep learning recommendation models use trained embeddings to represent categorical (“sparse”) features(Covington etal.,2016; Naumov etal.,2019; Naumov,2019). 
**多くの現代の深層学習推薦モデルは、訓練された埋め込みを使用してカテゴリカル（「スパース」）特徴を表現します**（Covington etal.,2016; Naumov etal.,2019; Naumov,2019）。(=これがいわゆるentity embedding!:thinking:)
A simple solution to high item cardinality is to use random hashing(Weinberger etal.,2009), but random hash collisions can be undesirable. 
高いアイテムのカーディナリティに対する簡単な解決策は、ランダムハッシングを使用することです（Weinberger etal.,2009）が、ランダムハッシュの衝突は望ましくない場合があります。
One option is to modify the hashing procedure. 
1つの選択肢は、ハッシング手順を修正することです。
Under this category, collision-free hashing(Liu etal.,2022)introduces individual embeddings for each item by dynamically free the memory of embeddings for retired items.  
このカテゴリの下では、collision-free hashing（Liu etal.,2022）が、**退役アイテムの埋め込みのメモリを動的に解放すること**によって、各アイテムの個別の埋め込みを導入します。(うん、特にニュース推薦だとretired itemsあるよなぁ...:thinking:)
Double hashing(Zhang etal.,2020)utilizes two independent hash functions to reduce memory usage, but still has random collision. 
Double hashing（Zhang etal.,2020）は、メモリ使用量を削減するために2つの独立したハッシュ関数を利用しますが、依然としてランダムな衝突があります。
Learning to hash methods(Wang etal.,2017)focus on similarity preserving by training ML-based hash functions. 
Learning to hash手法（Wang etal.,2017）は、MLベースのハッシュ関数を訓練することによって類似性を保持することに焦点を当てています。
There have also been works that address impression skew through contrastive learning or clustering(Yao etal.,2021; Chang etal.,2024); we view these as complementary approaches. 
対照学習やクラスタリングを通じて印象の偏りに対処する研究もあります（Yao etal.,2021; Chang etal.,2024）；私たちはこれらを補完的なアプローチと見なしています。
We take a holistic approach of designing a stable ID space, to minimize the need for hashing and to address embedding representation shifting directly. 
私たちは、ハッシングの必要性を最小限に抑え、埋め込み表現のシフトに直接対処するために、安定したID空間を設計する包括的なアプローチを取ります。

<!-- ここまで読んだ! -->

#### Stable embedding representation 安定埋め込み表現

Stable ID is inspired by tokenization approaches in NLP, which learn a fixed vocabulary of tokens to represent text in language modeling(Sennrich,2015; Kudo,2018; Devlin,2018). 
Stable IDは、NLPにおけるトークン化アプローチに触発されており、言語モデリングにおいてテキストを表現するための固定されたトークンの語彙を学習します(Sennrich,2015; Kudo,2018; Devlin,2018)。
In designing a tokenization scheme for item recommendation, Hou et al. (2023) proposes to vector-quantize the embeddings learned from an item content understanding model; 
アイテム推薦のためのトークン化スキームを設計するにあたり、Hou et al. (2023)はアイテムコンテンツ理解モデルから学習した埋め込みをベクトル量子化することを提案しています。
Qu et al. (2024) introduce a masked vector-quantizer to transfer the learned representations from collaborative filtering models to a generative recommender. 
Qu et al. (2024)は、協調フィルタリングモデルから生成的レコメンダーへの学習した表現を転送するために、マスク付きベクトル量子化器を導入しています。
Semantic ID is introduced concurrently in (Singh et al., 2023; Rajput et al., 2024), which is based on (Hou et al., 2023) and uses an RQ-VAE for quantization, showing its benefits in generalization performance and sequential recommendation, respectively. 
Semantic IDは(Singh et al., 2023; Rajput et al., 2024)で同時に導入されており、(Hou et al., 2023)に基づいており、量子化のためにRQ-VAEを使用し、一般化性能と逐次推薦におけるその利点をそれぞれ示しています。
In this work, we adapt Semantic ID as our stable ID method and analyze its effectiveness in addressing the three challenges in online item recommendation. 
本研究では、Semantic IDを私たちの安定ID手法として適応させ、オンラインアイテム推薦における3つの課題に対処する効果を分析します。

<!-- ここまで読んだ! -->

## 3Ranking Model Overview 3 ランキングモデルの概要

The recommendation problem is posed as a classification task, where a data point is the user- and item-side features associated with an item impression or conversion and a binary label indicating whether or not the user interacted or converted for that item. 
推薦問題は分類タスクとして定式化され、データポイントはアイテムのインプレッションまたはコンバージョンに関連するユーザ側およびアイテム側の特徴と、そのアイテムに対してユーザが相互作用したかどうかを示すバイナリラベルで構成されます。(うんうん、典型的なbandit feedbackの構造だ:thinking:)
We now give a brief overview of the ranking model architecture.
ここでは、ランキングモデルのアーキテクチャについて簡単に概説します。

### 3.1 Model モデル

(DLRMって主要な方法論なのかな。初めて聞いた...!:thinking:)

The recommendation system follows a deep neural architecture based on the DLRM (Covington et al., 2016; Naumov et al., 2019). 
推薦システムは、DLRM（Covington et al., 2016; Naumov et al., 2019）に基づく深層ニューラルアーキテクチャに従います。
The model consists of three stacked sections. 
モデルは、3つのスタックされたセクションで構成されています。
First is the information aggregation section, where the sparse (i.e., categorical), dense, and user history-based features are processed independently. 
最初は情報集約セクションで、ここではスパース（すなわち、カテゴリカル）、デンス、およびユーザ履歴に基づく特徴が独立して処理されます。
The output of each of these modules is a list of embedding vectors. 
これらのモジュールの出力は、埋め込みベクトルのリストです。
Second, these are concatenated into a single list which goes through the interaction layer, where dot products (or higher order interactions) are taken between all pairs of vectors. 
次に、これらは1つのリストに連結され、相互作用層を通過します。ここでは、すべてのベクトルのペア間でドット積（または高次の相互作用）が計算されます。
Third, the output of the interaction layer is transformed via an MLP to produce the logit score and a sigmoid is taken to output a probability. 
第三に、相互作用層の出力はMLPを介して変換され、ロジットスコアが生成され、シグモイドが取られて確率が出力されます。
The model is trained using cross-entropy loss. 
モデルはクロスエントロピー損失を使用して訓練されます。(=つまり2値分類タスクが代理学習問題なのかな...!:thinking:)
In the remainder of the paper we focus on the information aggregation section of the model. 
論文の残りの部分では、モデルの情報集約セクションに焦点を当てます。

<!-- ここまで読んだ! -->

#### Embedding module 埋め込みモジュール

Let $I$ be the total number of raw IDs in the system and let $[1..N]$ denote the integers from $1$ to $N$.
$I$をシステム内の生のIDの総数とし、$[1..N]$を$1$から$N$までの整数とします。

The embedding table is a matrix $\mathbf{E} \in \mathbb{R}^{H \times d_{m}}$, where $d_{m}$ is the embedding dimension and $H$ is the number of embeddings.
埋め込みテーブルは行列 $\mathbf{E} \in \mathbb{R}^{H \times d_{m}}$ であり、$d_{m}$ は埋め込み次元、$H$ は埋め込みの数です。
Let $f=(f_{1},\dots,f_{G}):[1..I]\to[1..H]^{G}$ be an embedding lookup function that maps a raw ID to $G$ embedding table row indices.
$f=(f_{1},\dots,f_{G}):[1..I]\to[1..H]^{G}$を、生のIDを$G$個の埋め込みテーブル行インデックスにマッピングする埋め込みルックアップ関数とします。
Then for each raw ID $x \in [1..I]$, the sparse module looks up embedding rows $\mathbf{e}_{f_{1}}(x),\dots,\mathbf{e}_{f_{G}}(x)$ and produces a single output embedding via sum-pooling, $\mathbf{e}_{f}(x):=\sum_{i=1}^{G}\mathbf{e}_{f_{i}}(x)$.
次に、各生のID $x \in [1..I]$について、スパースモジュールは埋め込み行$\mathbf{e}_{f_{1}}(x),\dots,\mathbf{e}_{f_{G}}(x)$を参照し、合計プーリングを介して単一の出力埋め込み $\mathbf{e}_{f}(x):=\sum_{i=1}^{G}\mathbf{e}_{f_{i}}(x)$ を生成します。

$$
\mathbf{e}_{f}(x):=\sum_{i=1}^{G}\mathbf{e}_{f_{i}}(x)
$$

<!-- ここまで読んだ! -->

#### Sparse module スパースモジュール

A sparse feature is a set $\mathbf{x}:=\{x_{1},\dots,x_{n}\}$ of raw IDs. 
スパース特徴は、生のIDの集合 $\mathbf{x}:=\{x_{1},\dots,x_{n}\}$ です。
For instance, this could be a set of $n$ product category IDs a given item belongs to. 
例えば、これは**特定のアイテムが属する $n$ 個の製品カテゴリIDの集合**である可能性があります。
We usually produce a single embedding $\mathbf{e}_{f}(\mathbf{x})$ by sum-pooling embeddings $\mathbf{e}_{f}(x_{i})$ for constituent raw IDs. 
私たちは通常、構成する生のIDの埋め込み $\mathbf{e}_{f}(x_{i})$ を**合計プーリング**して、単一の埋め込み $\mathbf{e}_{f}(\mathbf{x})$ を生成します。

<!-- ここまで読んだ! -->

#### User history module ユーザ履歴モジュール

We model a user’s item interaction history as a sequence of sparse features 𝐱u:=(𝐱1u,…,𝐱Tu) assigns superscript 𝐱𝑢 superscript subscript 𝐱1𝑢… superscript subscript 𝐱𝑇𝑢 
私たちは、ユーザのアイテムインタラクション履歴をスパース特徴のシーケンスとしてモデル化します $\mathbf{x}^{u}:=(\mathbf{x}_{1}^{u},\dots,\mathbf{x}_{T}^{u})$。
and the corresponding interaction timestamps. 
および対応するインタラクションのタイムスタンプ。
When working with these features, there are system constraints due to the number of items and the sequence length $T$. 
これらの特徴を扱う際には、**アイテムの数とシーケンスの長さ $T$ によるシステム制約**があります。
We include item interaction history for up to three months, which brings the item cardinality for the model to process to over one billion. 
私たちは、**最大三ヶ月のアイテムインタラクション履歴を含めており、モデルが処理するアイテムのカーディナリティは10億を超えます**。
It is important for the user history module to contextualize the sequence of features before they are further processed downstream. 
ユーザ履歴モジュールが、これらの特徴のシーケンスを文脈化することは、さらなる下流処理の前に重要です。
We describe the architecture below. 
以下にアーキテクチャを説明します。

First, we use the sparse module to embed each sparse feature 𝐱iusuperscriptsubscript𝐱𝑖𝑢 
まず、スパースモジュールを使用して各スパース特徴 $\mathbf{x}_{i}^{u}$ を埋め込みます。
and obtain a learned timestamp embedding; the sum is 𝐞fu(𝐱iu)superscriptsubscript𝐞𝑓𝑢superscriptsubscript𝐱𝑖𝑢 
学習されたタイムスタンプ埋め込みを取得し、その合計は $\mathbf{e}_{f}^{u}(\mathbf{x}_{i}^{u})$ です。
Let 𝐗=[𝐞fu(x1u);…;𝐞fu(xTu)]⊺∈ℝT×dm 
$\mathbf{X}=\left[\mathbf{e}_{f}^{u}(x_{1}^{u});\dots;\mathbf{e}_{f}^{u}(x_{T}^{u})\right]^{\intercal}\in\mathbb{R}^{T\times d_{m}}$ とします。
denote the resulting encoding. 
これは結果のエンコーディングを示します。
We then contextualize this sequence of embeddings via an aggregation module. 
次に、**集約モジュールを介してこの埋め込みのシーケンスを文脈化**します。
We use one of the following three aggregation module architectures: Bypass, Transformer, and Pooled Multihead Attention (PMA), which are defined in Appendix A. 
次の3つの集約モジュールアーキテクチャのいずれかを使用します：バイパス、トランスフォーマー、およびプールされたマルチヘッドアテンション（PMA）。これらは付録Aで定義されています。

<!-- ここまで読んだ! -->

### 3.2Metrics メトリクス

#### Normalized Entropy 正規化エントロピー

We measure model performance by normalized entropy (NE), defined as the model cross-entropy divided by the cross-entropy from predicting the data mean frequency of positive labels. 
モデルの性能は、正規化エントロピー（NE）によって測定され、これはモデルのクロスエントロピーを、正のラベルのデータ平均頻度を予測することによるクロスエントロピーで割ったものとして定義されます。
The NE equation is
NEの方程式は

$$
NE = \frac{-\frac{1}{N} \sum_{i=1}^{N} y_{i} \log(p_{i})}{-\frac{1}{N} \sum_{i=1}^{N} y_{i} \log(p)}
$$


where $N$ is the number of training examples, $y_{i} \in \{0,1\}$ is the label for example $i$, $p_{i}$ is the model prediction for example $i$, and $p = \frac{\sum_{i=1}^{N} y_{i}}{N}$. 
ここで、$N$はトレーニング例の数、$y_{i} \in \{0,1\}$は例$i$のラベル、$p_{i}$は例$i$のモデル予測、$p = \frac{\sum_{i=1}^{N} y_{i}}{N}$です。
Lower is better.
値が低いほど良いです。

<!-- ここまで読んだ! -->

## 4Semantic ID and Parameterizations

The primary motivation for Semantic ID is to design an efficient clustering schema to represent items that allows knowledge sharing between items with shared semantics. 
Semantic IDの主な動機は、**共有された意味を持つアイテム間で知識を共有できるようにアイテムを表現する効率的なクラスタリングスキーマを設計すること**です。
Intuitively, if we have hundreds of ads about pizza that different users clicked on, we would want an example involving one of the ads to be informed by the other ads’ representations. 
**直感的に言えば、異なるユーザーがクリックしたピザに関する数百の広告がある場合、私たちはその広告の一つに関する例が他の広告の表現から情報を得ること**を望むでしょう。
We craft the design of Semantic ID to potentially address the data-related challenges of item cardinality, impression skew, and ID drifting described in Section 5. 
私たちは、セクション5で説明されているアイテムのカーディナリティ、インプレッションの偏り、IDの漂流というデータ関連の課題に対処する可能性のあるSemantic IDの設計を考案します。
Compared to embedding representations based on random clusters, semantics-based representations will likely be more stable over time. 
**ランダムクラスタに基づく埋め込み表現と比較して、意味に基づく表現は時間とともにより安定する可能性があります**。
Semantics-based clustering will also allow tail items to learn from more training examples. 
意味に基づくクラスタリングは、テールアイテムがより多くのトレーニング例から学ぶことを可能にします。
The learning from items that have left the system can also be utilized, and embedding weights for new items do not have to be learned from scratch. 
**システムから離れたアイテムからの学習も活用でき、新しいアイテムの埋め込み重みはゼロから学習する必要はありません。** (それこそ用途としてはtwo-towerでも満たせる感じなのかな...!:thinking:)
We investigate these hypotheses empirically in Section 6. 
私たちは、これらの仮説をセクション6で実証的に調査します。

First, we give an overview of Semantic ID in Section 4.1. 
まず、セクション4.1でSemantic IDの概要を説明します。
We then describe token parameterization in Section 4.2. 
次に、セクション4.2でトークンのパラメータ化について説明します。
This step is crucial to incorporate Semantic ID into the recommendation model. 
このステップは、Semantic IDを推薦モデルに組み込むために重要です。

<!-- ここまで読んだ! -->

### 4.1 概要

Semantic IDs are learned for items in two stages: first, apply a content understanding model to the items’ text, image, or video to produce dense content embeddings. 
Semantic IDは、アイテムに対して2段階で学習されます。まず、アイテムのテキスト、画像、または動画にコンテンツ理解モデルを適用して、**密なコンテンツ埋め込み**を生成します。 
Then, train an RQ-VAE(Zeghidour etal.,2021)on the content embeddings to obtain a vector quantization for each item, which is represented as a sequence of coarse-to-fine discrete codes called the item’s Semantic ID.
次に、コンテンツ埋め込みに対してRQ-VAE（Zeghidour et al., 2021）を訓練し、各アイテムの**ベクトル量子化**を取得します。これは、アイテムのSemantic IDと呼ばれる粗から細への離散コードのシーケンスとして表されます。

(あ、ツイートで見たのは、なんで密な埋め込みのままではダメで、わざわざ離散化するんだろう? モチベーション何? っていう話だったな...!:thinking:)

![]()

Figure 1: The RQVAE model with L=3.
図1：L=3のRQ-VAEモデル。

Let $L$ be the number of layers (i.e., length of the sequence) and $K$ be the codebook size (i.e., number of clusters at each layer). 
$L$ を層の数（すなわち、シーケンスの長さ）とし、$K$ をコードブックのサイズ（すなわち、各層のクラスタ数, 1~Kのクラスタに各アイテムが所属するってことか...!:thinking:）とします。
RQ-VAE consists of an encoder that maps the content embedding $\mathbf{x} \in \mathbb{R}^{D}$ to a continuous latent representation, $\mathbf{z} \in \mathbb{R}^{D^{\prime}}$, a residual quantizer that quantizes $\mathbf{z}$ into a series of discrete codes $\mathbf{c}:=(c_{1},\dots,c_{L}) \in K^{L}$, and a decoder that reconstructs $\mathbf{x}$ from $\mathbf{c}$. 
RQ-VAEは、コンテンツ埋め込み$\mathbf{x} \in \mathbb{R}^{D}$を連続的な潜在表現$\mathbf{z} \in \mathbb{R}^{D^{\prime}}$ にマッピングするエンコーダ、$\mathbf{z}$を一連の離散コード$\mathbf{c}:=(c_{1},\dots,c_{L}) \in K^{L}$に量子化する残差量子化器、および$\mathbf{c}$から$\mathbf{x}$を再構築するデコーダで構成されています。
This is done by associating each layer $l$ with a codebook which is a set of $K$ vectors $\{\mathbf{v}^{l}_{k}\}_{k=1}^{K}$. 
これは、各層 $l$ を $K$ 個のベクトル集合 $\{\mathbf{v}^{l}_{k}\}_{k=1}^{K}$ に関連付けることによって行われます。
The sequence of discrete codes is hierarchical: $c_{l}$ corresponds to the codebook vector $\mathbf{v}^{l}_{c_{l}}$ that approximates $\mathbf{r}_{l}$, the remaining residual from $\mathbf{z}$ after recursively applying the codebook vectors from layers $(l-1)$ to 1, i.e.,
離散コードのシーケンスは階層的です: $c_{l}$ は、$\mathbf{r}_{l}$ を近似するコードブックベクトル $\mathbf{v}^{l}_{c_{l}}$ に対応し、これは $\mathbf{z}$ からの残りの残差であり、層 $(l-1)$ から1までのコードブックベクトルを再帰的に適用した後のものです。

$$
r_{l} := z - \sum_{i=1}^{l-1} v^{i}_{c_{i}},
c_{l} := \arg\min_{c} \| v^{l}_{c} - r_{l} \|_{2}.
\tag{2}
$$

In Section 4.2, we provide more intuition on the nature of RQ-VAE’s hierarchical clustering and how it informs the choice of token parameterization.
セクション4.2では、**RQ-VAEの階層的クラスタリングの性質**と、それがトークンのパラメータ化の選択にどのように影響するかについて、より直感的な説明を提供します。

The RQ-VAE is trained using two loss terms, a reconstruction loss and a loss that encourages the residuals and codebook vectors to be close to each other, 
RQ-VAEは、再構築損失と残差とコードブックベクトルが互いに近くなるように促す損失の2つの損失項を使用して訓練されます。

$$
L_{RQ-VAE} = ||x - dec(c)||^2 + 
$$

where $\text{dec}(\mathbf{c})$ is the result of applying the decoder to the codes $\mathbf{c}$, $\text{sg}(\cdot)$ corresponds to the stop-gradient operator, and $\beta$ is a hyperparameter we set to 0.5 in the experiments. 
ここで、$\text{dec}(\mathbf{c})$は、コード$\mathbf{c}$にデコーダを適用した結果であり、$\text{sg}(\cdot)$はストップグラデイント演算子に対応し、$\beta$は実験で0.5に設定したハイパーパラメータです。

A Semantic ID is defined as the sequence of discrete codes $(c_{1},\dots,c_{L})$ produced by the encoder and residual quantizer.
Semantic IDは、エンコーダと残差量子化器によって生成された離散コードのシーケンス$(c_{1},\dots,c_{L})$として定義されます。

<!-- ここまで読んだ! -->

### 4.2 Token Parameterization トークンのパラメータ化

In our experiments, we use the same codebook size for each level, resulting in $K^{L}$ total clusters. 
私たちの実験では、各レベルに対して同じコードブックサイズを使用し、$K^{L}$の合計クラスタを得ました。
An important feature of RQ-VAE is that it produces hierarchical clusters. 
RQ-VAEの重要な特徴は、階層的なクラスタを生成することです。

Assuming $L=3$ for simplicity, a raw item ID is mapped to a sequence $(c_{1},c_{2},c_{3})$. 
簡単のために$L=3$と仮定すると、生のアイテムIDはシーケンス$(c_{1},c_{2},c_{3})$にマッピングされます。

The precision of vector quantization increases as one moves from the first token $c_{1}$ to the deeper token $c_{2}$, and finally $c_{3}$. 
ベクトル量子化の精度は、最初のトークン$c_{1}$からより深いトークン$c_{2}$、そして最終的に$c_{3}$に移動するにつれて向上します。

The first token $c_{1}$ represents the coarsest bucket: e.g., all ads related to food. 
最初のトークン$c_{1}$は最も粗いバケットを表します：例えば、食べ物に関連するすべての広告です。

The second token $c_{2}$ refines this information, e.g., $(c_{1},c_{2})$ may represent all ads related to pizza. 
2番目のトークン$c_{2}$はこの情報を洗練させます。例えば、$(c_{1},c_{2})$はピザに関連するすべての広告を表すかもしれません。

The last token $c_{3}$ further refines this information, e.g., $(c_{1},c_{2},c_{3})$ may represent all ads related to pizza and written in a specific language such as English. 
最後のトークン$c_{3}$はこの情報をさらに洗練させます。例えば、$(c_{1},c_{2},c_{3})$はピザに関連し、英語などの特定の言語で書かれたすべての広告を表すかもしれません。

Due to this, we can control the amount and the structure of the information that the recommendation model receives from Semantic ID. 
これにより、推薦モデルがSemantic IDから受け取る情報の量と構造を制御できます。

Notably, supplying the most fine-grained information (all possible $(c_{1},c_{2},\dots,c_{L})$ tuples) is often not feasible due to high cardinality of the possible combinations. 
特に、最も詳細な情報（すべての可能な$(c_{1},c_{2},\dots,c_{L})$タプル）を提供することは、可能な組み合わせの高い基数のためにしばしば実現不可能です。

Hence, a tradeoff exists between the cardinality of the token parameterization and the amount of information the model receives from Semantic ID. 
したがって、トークンのパラメータ化の基数とモデルがSemantic IDから受け取る情報の量との間にはトレードオフが存在します。

![]()
table1: token parameterization techniques.

Lets $(x):[1..I] \to K^{L}$ be the Semantic ID lookup that maps raw IDs to Semantic IDs learned by RQ-VAE. 
$L$をSemantic IDのルックアップとし、生のIDをRQ-VAEによって学習されたSemantic IDにマッピングします。
Keeping the hierarchical nature of the tokens in mind, we must specify a token parameterization that maps a Semantic ID to embedding table rows, $p(\mathbf{c};H):K^{L} \to [1..H]^{G}$. 
トークンの階層的な性質を考慮し、Semantic IDを埋め込みテーブルの行にマッピングするトークンパラメータ化を指定する必要があります。

Table 1 defines several possible parameterizations. 
表1は、いくつかの可能なパラメータ化を定義しています。

When the Semantic ID cardinality is larger than the embedding size, a modulo hash function is applied. 
Semantic IDの基数が埋め込みサイズより大きい場合、モジュロハッシュ関数が適用されます。

When there are multiple IDs, a shifting factor is added to avoid the collision between different positions. 
複数のIDがある場合、異なる位置間の衝突を避けるためにシフトファクターが追加されます。

Among all the parameterization techniques, only Prefix-ngram consists of all possible tuples from different granularity. 
すべてのパラメータ化技術の中で、Prefix-ngramのみが異なる粒度からのすべての可能なタプルで構成されています。

Table 2: 
表2：

NE performance for different tokenization parameterizations 
異なるトークン化パラメータ化に対するNEパフォーマンス

Table 2 summarizes the model performance across different token parameterizations. 
表2は、異なるトークンパラメータ化におけるモデルのパフォーマンスを要約しています。

We draw the following conclusions: 
私たちは以下の結論を導きます：

i) Prefix-ngram is the best parameterization. 
i) Prefix-ngramが最良のパラメータ化です。

This indicates that incorporating the hierarchical nature of the clustering in the embedding table mapping is necessary for effectiveness, as it allows for knowledge sharing among more items than a flat mapping; 
これは、埋め込みテーブルのマッピングにおいてクラスタリングの階層的な性質を取り入れることが効果的であるために必要であることを示しています。これは、フラットマッピングよりも多くのアイテム間での知識共有を可能にします。

ii) Increasing the depth of Prefix-ngram improves NE performance; 
ii) Prefix-ngramの深さを増すことでNEパフォーマンスが向上します。

iii) increasing the RQ-VAE cardinality improves NE performance. 
iii) RQ-VAEの基数を増やすことでNEパフォーマンスが向上します。

<!-- 後で読む! -->

## 5Item Impression Distribution Issues 5アイテムのインプレッション分布の問題

In this section, we discuss the data distribution aspects that present challenges for recommendation modeling in Meta ads ranking and how we address them with the use of Semantic ID. 
このセクションでは、Meta広告ランキングにおける推薦モデルに対する課題を提示するデータ分布の側面と、Semantic IDを使用してそれらにどのように対処するかについて議論します。

#### Item cardinality

For certain features, such as the target item, the number of distinct items $I$ considered by the model can be much larger than a feasible embedding table size $H$ in the sparse module. 
特定の特徴、例えばターゲットアイテムに対して、モデルが考慮する異なるアイテムの数 $I$ (=カーディナリティ)は、スパースモジュールにおける実行可能な埋め込みテーブルサイズ $H$ よりもはるかに大きくなる可能性があります。
In such cases the mapping function $f(\mathbf{x})$ introduces collisions: two or more raw IDs will map to the same row. 
**このような場合、マッピング関数 $f(\mathbf{x})$ は衝突を引き起こします：2つ以上の生のIDが同じ行にマッピングされます**。
The mapping function $f(\mathbf{x})$ is often chosen to be a simple hash. 
マッピング関数 $f(\mathbf{x})$ は、しばしば単純なハッシュとして選択されます。
Since the initial raw IDs are randomly generated at the time of item creation, the resulting collisions will essentially be random. 
初期の生のIDはアイテム作成時にランダムに生成されるため、結果として生じる衝突は本質的にランダムになります。
Such random collisions can negatively affect the resulting representation quality of embeddings and serve as an obstacle to effective knowledge sharing across items. 
このようなランダムな衝突は、埋め込みの結果としての表現品質に悪影響を及ぼし、アイテム間の効果的な知識共有の障害となる可能性があります。

<!-- ここまで読んだ! -->

#### Impression skew インプレッションの偏り

Figure 2: Figure 2:Impression Skew – cumulative impressions as a function of the share of items considered. As items are sorted by the impression count, one sees that the majority of impressions comes from a fraction of most popular items.
図2: インプレッションの偏り – 考慮されたアイテムの割合に対する累積インプレッション。アイテムがインプレッション数でソートされると、ほとんどのインプレッションが最も人気のあるアイテムの一部から来ていることがわかります。

For the target item feature, the item distribution in the training data is highly skewed.
ターゲットアイテムの特徴に関して、**トレーニングデータ内のアイテム分布は非常に偏っています**。
Figure 2 shows that in our system, a small percentage of items dominates the item impression distribution: 
図2は、私たちのシステムにおいて、少数のアイテムがアイテムインプレッション分布を支配していることを示しています。
when sorting the items by popularity, the top 0.1% “head” items have 25% of all item impressions, 
アイテムを人気順に並べると、上位0.1%の「ヘッド」アイテムが全アイテムインプレッションの25%を占め、
the next 5.5% “torso” items have 50% of cumulative impressions, 
次の5.5%の「トルソ」アイテムが累積インプレッションの50%を占め、
while the remaining 94.4% “tail” items account for the remaining 25% of impressions.
残りの94.4%の「テイル」アイテムが残りの25%のインプレッションを占めています。

As tail items have few training examples, it can be challenging to learn embedding representations $\mathbf{e}(\mathbf{x})$ that generalize well.
**テイルアイテムはトレーニング例が少ないため、一般化の良い埋め込み表現 $\mathbf{e}(\mathbf{x})$ を学習することは困難**です。
(うーん、じゃあ特にlifetimeが短いニュース推薦においては、アイテムのentity embeddingを学習するのってあんまり価値発揮しなさそうだな...!!:thinking:)
Random hashing doesn’t allow the head and torso items to effectively share knowledge with semantically similar tail items since the assignment of several items to a single embedding is random.
ランダムハッシングは、複数のアイテムを単一の埋め込みにランダムに割り当てるため、ヘッドアイテムとトルソアイテムが意味的に類似したテイルアイテムと効果的に知識を共有することを許しません。
(でもアイテム特徴量を使えば知識を共有できるよね、って話かな。じゃあやっぱりtwo-towerは特徴量としてのrichなitem embeddingを作るとしても価値がありそう...!!:thinking:)

<!-- ここまで読んだ! -->

#### ID drifting IDの漂流

![]()

Figure 3:ID Drift – share of items that remain active in the initial corpus as a function of time. Half of the original corpus exits the system after 6 days. An equal number of new items enters the system, creating a severe item distribution drift.
図3: IDの漂流 – 時間の関数として、最初のコーパスでアクティブなままでいるアイテムの割合。元のコーパスの半分は6日後にシステムを退出します。同数の新しいアイテムがシステムに入り、深刻なアイテム分布の変化を引き起こします。

The existing item ID space is highly dynamic with large numbers of old items retiring (Figure3) and new items entering the system. 
既存のアイテムID空間は非常に動的で、多くの古いアイテムが退役し（図3）、新しいアイテムがシステムに入ってきます。 (それこそニュース推薦だと顕著だよね...!:thinking:)
We call this item distribution shift in our system “raw ID drifting.” 
このアイテム分布の変化を私たちのシステムでは「**生のID漂流（raw ID drifting）**」と呼びます。 (そういう呼び方をするのか...!:thinking:)
The raw ID drifting phenomenon stems from the nature of online recommendation systems, where new ads are created on a daily basis and most ads have a relatively short lifespan. 
生のID漂流現象は、オンライン推薦システムの特性に起因しており、新しい広告が日々作成され、ほとんどの広告は比較的短い寿命を持っています。(なるほど。広告推薦もニュース推薦と近い性質を持ってるんだな...!:thinking:)

As a byproduct, a recommendation model based on random hashing experiences severe embedding representation drift over time: a given embedding $\mathbf{e}$ represents different items over time as items enter and exit the system. 
その副産物として、ランダムハッシングに基づく推薦モデルは、時間の経過とともに深刻な埋め込み表現の漂流を経験します：特定の埋め込み $\mathbf{e}$ は、アイテムがシステムに入ったり出たりするにつれて、時間とともに異なるアイテムを表します。

<!-- ここまで読んだ! -->

#### Item representation with Semantic ID アイテム表現とセマンティックID

We hypothesize that switching from raw IDs to Semantic IDs can effectively address the issues above.  
私たちは、生のIDからセマンティックIDに切り替えることで、上記の問題に効果的に対処できると仮定します。(semantic情報を反映させたidってこと?? two-towerの出力と何が違うんだろ??:thinking:)

When an advertiser introduces a new ad $\mathbf{x}$ to the system and retires the previous one $\mathbf{y}$, the fine-grained content details of the new ad may be different from the retired one, but the broad semantic category of the product usually remains the same.  
広告主が新しい広告 $\mathbf{x}$ をシステムに導入し、以前の広告 $\mathbf{y}$ を引退させるとき、新しい広告の詳細なコンテンツは引退した広告とは異なる場合がありますが、製品の広範なセマンティックカテゴリは通常同じままです。
(なるほど。同じ広告主が同じ商品を売るために新しい広告を出す場合、細かい内容は変わっても、セマンティックなカテゴリは変わらないよね、ってことか...!:thinking:)
Therefore, the new and retired ads’ Semantic IDs will match (or at least share a prefix).  
したがって、新しい広告と引退した広告のセマンティックIDは一致するか（少なくとも接頭辞を共有します）。
Hence, the item impression distribution in Semantic ID space exhibits much less drift compared to the raw ID space as long as the broad semantic categories remain temporally stable.  
したがって、**広範なセマンティックカテゴリが時間的に安定している限り、セマンティックID空間におけるアイテムのインプレッション分布は、生のID空間と比較してはるかに少ないドリフトを示します**。

Similarly, if a tail item $\mathbf{x}$ has similar content to a head or torso item $\mathbf{y}$, their Semantic IDs will match (or at least share a prefix).  
同様に、テールアイテム $\mathbf{x}$ がヘッドまたはトルソーアイテム $\mathbf{y}$ と類似の内容を持つ場合、彼らのセマンティックIDは一致するか（少なくとも接頭辞を共有します）。
The resulting item impression distribution in Semantic ID space exhibits less skew compared to the raw ID space (see Appendix B).  
セマンティックID空間における結果のアイテムインプレッション分布は、生のID空間と比較して歪みが少なくなります（付録Bを参照）。

In both of the cases above, the embeddings $\mathbf{e(x)}$ and $\mathbf{e(y)}$ will be equal (or similar if the Semantic IDs only share a prefix).  
上記の両方のケースでは、埋め込み $\mathbf{e(x)}$ と $\mathbf{e(y)}$ は等しくなります（セマンティックIDが接頭辞のみを共有する場合は類似します）。
(ここでxとyは、同じセマンティックカテゴリに属するアイテムを指している感じ...!:thinking:)
This is a way for the model to transfer knowledge from item $\mathbf{y}$ with many training examples to item $\mathbf{x}$.
これは、モデルが多くのトレーニング例を持つアイテム $\mathbf{y}$ からアイテム $\mathbf{x}$ へ知識を転送する方法です。(要するにアイテム特徴量を使ったencoderと役割は近そうだよなぁ...:thinking:)
Summarizing, temporal stability of semantic concepts results in stability of Semantic ID encoding, which mitigates embedding representation instability for the model.  
要約すると、**セマンティック概念の時間的安定性は、セマンティックIDエンコーディングの安定性をもたらし、モデルの埋め込み表現の不安定性を軽減**します。(この文章はいいな! 要するにsemanticな特徴量は時間的に安定しているから、学習時に価値を発揮しやすいembeddingになるよね、ってことだよな...!:thinking:)


Table 3:  Performance of three item representation approaches over various item segments.  
表3:さまざまなアイテムセグメントにおける3つのアイテム表現アプローチの性能。

<!-- ここまで読んだ! -->

## 6Offline Experiments 6オフライン実験

To investigate our hypotheses about the advantages of Semantic ID over baseline item representation approaches, we conduct a suite of offline experiments. 
Semantic IDのベースラインアイテム表現アプローチに対する利点に関する仮説を調査するために、一連のオフライン実験を実施します。

We use a simplified version of Meta’s production ads ranking model, keeping all the dense features and the user’s item interaction history, but including only the target item in the sparse module (and removing $O(100)$ other sparse features). 
Metaのプロダクション広告ランキングモデルの簡略化版を使用し、すべての密な特徴とユーザのアイテムインタラクション履歴を保持しますが、スパースモジュールにはターゲットアイテムのみを含め（$O(100)$の他のスパース特徴を削除します）。
We train on production user interaction data from a four-day time period, processing the training data sequentially and training for a single epoch. 
**4日間の期間にわたるプロダクションユーザインタラクションデータでトレーニングを行い、トレーニングデータを逐次処理し、1エポックのトレーニングを行います。**
We evaluate the model on the first six hours of the next day of data. 
**次の日のデータの最初の6時間でモデルを評価します。**

<!-- ここまで読んだ! -->

### 6.1 ベースライン

In Section 5, we outlined data-related challenges and opportunities in designing a good embedding lookup function $f(\mathbf{x})$ for embedding-based item representations. 
第5節では、埋め込みベースのアイテム表現のための良い埋め込みルックアップ関数 $f(\mathbf{x})$ を設計する際のデータ関連の課題と機会について概説しました。
We describe two baseline approaches, individual embeddings (IE) and random hashing (RH), and compare those to Semantic ID (SemID). 
個別埋め込み（IE）とランダムハッシュ（RH）の2つのベースラインアプローチを説明し、それらをSemantic ID（SemID）と比較します。
(前者IEがentity embeddingかな!:thinking:)

#### Individual embeddings 個別埋め込み

Each raw ID gets its own embedding table row, I=H𝐼𝐻I=Hitalic_I = italic_HandfIE(x):=xassignsubscript𝑓IE𝑥𝑥f_{\text{IE}}(x):=xitalic_f start_POSTSUBSCRIPT IE end_POSTSUBSCRIPT ( italic_x ) := italic_x. 
各生のIDは独自の埋め込みテーブルの行を持ち、$I=H$、$f_{\text{IE}}(x):=x$ です。 
(うん。普通のentity embeddingっぽいな!:thinking:)
While unrealistic in production scenarios due to system constraints, we consider this model for illustration purposes. 
これは**システムの制約により実際の運用シナリオでは非現実的**ですが、説明のためにこのモデルを考慮します。 
During evaluation, IDs that are not seen during training are mapped to a randomly initialized untrained embedding. 
**評価中、トレーニング中に見られなかったIDは、ランダムに初期化された未学習の埋め込みにマッピングされます**。(うんうん。多分unknownトークン的なやつ!:thinking:)

#### Random hashing ランダムハッシング

In the case where $I \approx a \cdot H$ for some $a > 1$, we can randomly hash raw IDs to embedding table rows, 
$I \approx a \cdot H$のとき、$a > 1$のために、私たちは**生のIDを埋め込みテーブルの行にランダムにハッシュする**ことができます。(i.e. アイテムカーディナリティが埋め込みテーブルサイズよりも大きい場合!:thinking:)

$$
f_{\text{RH}}(x) := h(x)
$$

where $h(x): [1..I] \to [1..H]$ is one of the standard hash functions such as modulo hash. 
ここで、$h(x): [1..I] \to [1..H]$ は、モジュロハッシュなどの標準的なハッシュ関数の1つです。

This creates random collisions with an average collision factor of $a$.
これにより、平均衝突因子 $a$ を持つランダムな衝突が生成されます。
(つまり、埋め込みテーブルの1行につき平均してa個のアイテムが割り当てられる、って話...!:thinking:)

<!-- ここまで読んだ! -->

#### Semantic ID セマンティックID

The items’ content embeddings are obtained from a multimodal image and text foundation model. 
**アイテムのコンテンツ埋め込みは、マルチモーダルな画像とテキストの基盤モデルから取得されます。** (i.e. 事前学習ずみモデルを使ったsemantic埋め込み...!:thinking:)
The foundation model is pre-trained on a large training set of items using image and text alignment objectives (Radford et al., 2021). 
この基盤モデルは、画像とテキストの整合性目標を使用して、大規模なアイテムのトレーニングセットで事前学習されています（Radford et al., 2021）。
The RQ-VAE is then trained on the content embeddings of all target items from the past three months, with $L=3$ and $K=2048$. 
次に、RQ-VAEは過去3か月のすべてのターゲットアイテムのコンテンツ埋め込みに対して訓練され、$L=3$ および $K=2048$ とします。
We use the prefix $f_{\text{SemId}}=p\circ s$ from Section 4.2. 
私たちは、セクション4.2からの接頭辞 $f_{\text{SemId}}=p\circ s$ を使用します。
(これが必要なのかわかってないんだよなぁ。semanticなcontent embeddingだけではダメなのか:thinking:)

<!-- ここまで読んだ! -->

The analyses in Section 6.2 and Section 6.3 focus on the target item sparse feature. 
セクション6.2およびセクション6.3の分析は、ターゲットアイテムのスパース特徴に焦点を当てています。
We train three versions of the recommendation model using the above three embedding lookup functions. 
上記の3つの埋め込みルックアップ関数を使用して、推薦モデルの3つのバージョンを訓練します。
The size of the item embedding table is equal to the total number of items for IE and set to a smaller size for RH and SemID, with the average collision factor of 3. 
アイテム埋め込みテーブルのサイズは、IEのアイテムの場合は総数と等しく、RHおよびSemIDのために小さいサイズに設定され、平均衝突係数は3です。
(ってことは、RHとSemIDはアイテムカーディナリティの1/3のサイズの埋め込みテーブルを使うってことか...!:thinking:)
The user history features are mapped using random hashing. 
ユーザ履歴の特徴は、ランダムハッシングを使用してマッピングされます。(これ、どういう意味?? ユーザidをランダムハッシュしてembeddingに変換してるって話??:thinking:)

In Section 6.4, we use Semantic ID for the user history features and study its effect on aggregation module architectures. 
セクション6.4では、ユーザ履歴の特徴にセマンティックIDを使用し、集約モジュールアーキテクチャへの影響を研究します。
The item interaction history sequence length is fixed to $O(100)$. 
アイテムの相互作用履歴のシーケンス長は $O(100)$ に固定されています。
We pad or truncate the user history to fit the desired length. 
ユーザ履歴を希望の長さに合わせるために、パディングまたは切り詰めを行います。
(うんうん。ここは普通だ...!:thinking:)

<!-- ここまで読んだ! -->

### 6.2 セグメント分析

(注意: 論文中の"NE"は評価指標のNormalized Entropyのこと!:thinking:)

(ここの分析方法とか参考になりそう...!:thinking:)

To understand the effect of impression skew on each approach, we segment the data based on the item’s number of impressions in the training period. 
各アプローチに対するインプレッションの偏りの影響を理解するために、トレーニング期間中のアイテムのインプレッション数に基づいてデータをセグメント化します。
We sort all items by impression count. 
すべてのアイテムをインプレッション数でソートします。
As before, we segment items into head, torso, and tail items according to whether they generate 25%, 75%, or 100% of the cumulative impression count in this sorted order. 
前回と同様に、**ソートされた順序で累積インプレッション数の25%、75%、または100%を生成するかどうかに応じて、アイテムをヘッド、トルソー、テールアイテムにセグメント化**します。
Due to the impression skew, the percentage of items that are head, torso, or tail items are 0.1%, 5.5%, or 94.4%, respectively. 
インプレッションの偏りにより、ヘッド、トルソー、またはテールアイテムの割合はそれぞれ0.1%、5.5%、または94.4%です。
We also evaluate on the segment of new items that only appear in the evaluation period and were not seen during training. 
**トレーニング中に見られなかった評価期間中にのみ現れる新しいアイテムのセグメント**でも評価を行います。
The performance of the three item representation approaches is shown in Table 3(a). 
3つのアイテム表現アプローチのパフォーマンスは、表3(a)に示されています。

![]()
table3: hoge

Compared to the baselines, Semantic ID improves generalization for tail items, is NE neutral for head items, and slightly beneficial for torso items. 
**ベースラインと比較して、Semantic IDはテールアイテムの一般化を改善し、ヘッドアイテムにはNE中立で、トルソーアイテムにはわずかに有益**です。
As this is also relative to the individual embeddings approach, Semantic ID is not simply better at clustering than random hashing, but we find that the target item feature benefits from semantics-based knowledge sharing. 
これは個別の埋め込みアプローチに対しても相対的であり、Semantic IDはランダムハッシングよりも単にクラスタリングが優れているわけではなく、ターゲットアイテムの特徴(=id embedding)が**意味に基づく知識共有から利益を得ている**ことがわかります。
(知識共有=knowledge sharingっていう表現を、今後説明するときに使っていきたい...!:thinking:)

Specifically, the knowledge sharing occurs through the shared embedding weights, which receive updates for semantically-related items. 
具体的には、知識共有は、意味的に関連するアイテムの更新を受け取る共有埋め込み重みを通じて行われます。
Knowledge sharing benefits are largest on the new items segment, where SemID achieves large gains over both RH and IE (−0.41% and −0.33%, respectively). 
**知識共有の利益は新しいアイテムセグメントで最大であり、SemIDはRHおよびIEに対して大きな利益を達成します（それぞれ−0.41%および−0.33%）。** (これは感覚通りというか意図通りの効果だよね...!:thinking:)
New items use pre-trained weights from semantically similar items seen during training for prediction, rather than using a non-relevant weight (RH) or an untrained weight (IE). 
新しいアイテムは、トレーニング中に見られた意味的に類似したアイテムからの事前トレーニングされた重みを予測に使用し、無関係な重み（RH）や未トレーニングの重み（IE）を使用するのではありません。(うんうん...!:thinking:)

<!-- ここまで読んだ! -->

To measure the effect of embedding representation drifting on model performance, we evaluate the trained models back on the training data but on two different temporal segments. 
埋め込み表現の漂流がモデルのパフォーマンスに与える影響を測定するために、トレーニングデータに対してトレーニングされたモデルを評価しますが、2つの異なる時間的セグメントで評価します。
We take NE on 42-48 hours prior to the end of the training epoch and subtract NE on the last six hours of training. 
トレーニングエポックの終了42-48時間前のNEを取得し、トレーニングの最後の6時間のNEを引きます。
A smaller value indicates that the embedding representation shift caused by ID drifting affects model fit less. 
小さい値は、IDの漂流によって引き起こされる埋め込み表現のシフトがモデルの適合に与える影響が少ないことを示します。
This is because our model is trained time-sequentially for one epoch, so the resulting model learns to fit the latest training time period at the end of training. 
これは、私たちのモデルが1エポックの間に時間的に順次トレーニングされるため、結果として得られるモデルはトレーニングの最後に最新のトレーニング時間帯に適合することを学習するからです。
The results are in Table 3(b). 
結果は表3(b)に示されています。

![]()
table3(b)

Individual embeddings approach has a smaller performance gap compared with random hashing. 
**個別の埋め込みアプローチは、ランダムハッシングと比較してパフォーマンスのギャップが小さい**です。
This highlights that random hashing suffers from ID drifting – the embedding representations lose capability to represent older items over time as the weights are updated using new item examples. 
これは、**ランダムハッシングがIDの漂流に苦しんでいることを強調しています**。埋め込み表現は、重みが新しいアイテムの例を使用して更新されるにつれて、古いアイテムを表現する能力を失います。
In contrast, Semantic ID matches the performance of individual embeddings, indicating that its learned representations are more stable over time. 
対照的に、Semantic IDは個別の埋め込みのパフォーマンスに匹敵し、その学習された表現が時間とともにより安定していることを示しています。(あ、でも"匹敵"くらいなのか...!新規アイテムへの対応とはまたやや違う性能評価の話だからかな:thinking:)

We conjecture that this improved representation stability also allows the model to generalize better over much longer training durations, where ID drifting becomes even more pronounced. 
**この改善された表現の安定性が、IDの漂流がさらに顕著になる長期間のトレーニングにおいてモデルがより良く一般化できることを可能にする**と推測します。(なるほどID driftは長期間の学習で問題になるのか...!期間ごとにインプレッションが観測されるidが異なるから...!:thinking:)
We train the RH and SemID models over a 20-day period and compare them to corresponding models trained only for the last four days of the period. 
**RHおよびSemIDモデルを20日間トレーニングし、期間の最後の4日間のみトレーニングされた対応するモデルと比較**します。
The results in Table 4 show that compared to random hashing, the performance of Semantic ID scales better with training data over a longer period. 
表4の結果は、ランダムハッシングと比較して、Semantic IDのパフォーマンスがより長い期間にわたってトレーニングデータに対してより良くスケールすることを示しています。

Table 4: NE improvement from training for 20 days of data instead of 4 days. 
表4: 4日間ではなく20日間のデータでトレーニングした際のNEの改善。
(学習期間を過去に伸ばした方が性能は基本下がっちゃってるのか...!:thinking:)

<!-- ここまで読んだ! -->

### 6.3 アイテム表現空間

To gain a better understanding of the item embedding representations, we extract the learned embedding weights from each trained model. 
アイテム埋め込み表現をよりよく理解するために、各トレーニング済みモデルから学習された埋め込み重みを抽出します。
One can view random hashing and Semantic ID as two different ways to partition the raw item ID corpus. 
ランダムハッシングとSemantic IDは、生のアイテムIDコーパスを分割する2つの異なる方法と見なすことができます。
We wish to see whether the semantics-based partition produced by Semantic ID is better suited for the recommendation problem than the random partition produced by random hashing. 
私たちは、**Semantic IDによって生成された意味に基づく分割が、ランダムハッシングによって生成されたランダムな分割よりも推薦問題に適しているかどうかを確認したい**と考えています。(普通に考えると絶対良さそうだけど...!:thinking:)

When several items are assigned to the same partition, they get mapped to the same embedding by the embedding lookup module. 
複数のアイテムが同じパーティションに割り当てられると、それらは埋め込みルックアップモジュールによって同じ埋め込みにマッピングされます。
We view this embedding vector as a summary of the per-item embeddings learned by the individual embeddings model. 
私たちは、この埋め込みベクトルを、個々の埋め込みモデルによって学習されたアイテムごとの埋め込みの要約と見なします。
While we fit the individual embeddings model for illustration purposes in this paper, IE is impractical in industry-level settings. 
この論文では説明のために個々の埋め込みモデルを適合させますが、**IEは産業レベルの設定では実用的ではありません**。
A partition with lower intra-partition embedding variance and higher inter-partition distances can be viewed as a more effective summary of individual embeddings. 
**より低い内部パーティション埋め込み分散とより高い外部パーティション距離を持つパーティションは、個々の埋め込みのより効果的な要約と見なすことができます**。(なるほど。この観点から埋め込み表現の良し悪しを評価するのか...!:thinking:)
We compute these metrics for the RH and SemID partitions of the embeddings learned by the IE model. 
私たちは、IEモデルによって学習された埋め込みのRHおよびSemIDパーティションに対してこれらの指標を計算します。

We set the collision factor to 5555 for this experiment. 
この実験では、衝突係数を5555に設定しました。(=つまり、埋め込みテーブルの1行に平均して5555個のアイテムが割り当てられるってことか...!:thinking:)
As a result, the resulting clusters for RH and SemID partitions contain 5555 items on average. 
その結果、RHおよびSemIDパーティションのクラスターは平均して5555アイテムを含みます。(うんうん...!:thinking:)
However, since Semantic ID is the latent codes learned by an RQ-VAE model, the resulting cluster sizes are highly variable. 
ただし、Semantic IDはRQ-VAEモデルによって学習された潜在コードであるため、結果として得られるクラスターサイズは非常に変動します。
We compute metrics for two groups of Semantic ID clusters, small clusters with 4-10 items each and the top 1,000 clusters, where each cluster contains thousands of items. 
私たちは、4〜10アイテムを含む小さなクラスターと、各クラスターが数千のアイテムを含む上位1,000クラスターの2つのグループのSemantic IDクラスターに対して指標を計算します。
Table 5 contains the average variances and average pairwise distances, with standard deviations in parentheses. 
表5には、平均分散と平均ペアワイズ距離が含まれており、標準偏差は括弧内に示されています。
The metrics are averaged across the embedding dimensions to produce single scalars for comparison. 
これらの指標は、比較のために埋め込み次元全体で平均化され、単一のスカラー値が生成されます。

![]()
Table 5: Intra- and inter-cluster variances and pairwise distances for random hashing and SemID-based partitions. 
表5：ランダムハッシングおよびSemIDベースのパーティションのための内部および外部クラスターの分散とペアワイズ距離。

We observe that the Semantic ID partitions produce clusters with lower intra-cluster variance compared to random hashing. 
私たちは、**Semantic IDパーティションがランダムハッシングと比較して、より低い内部クラスター分散を持つクラスターを生成すること**を観察します。
However, the resulting pairwise distances send a mixed signal. 
しかし、結果として得られるペアワイズ距離は混合信号を送ります。
We hypothesize that the low pairwise distances between the top 1,000 clusters is because RQ-VAE places multiple centroids into the regions with highest data density to minimize the model loss. 
私たちは、上位1,000クラスター間の低いペアワイズ距離は、RQ-VAEがモデル損失を最小化するために、データ密度が最も高い領域に複数のセントロイドを配置するためであると仮定します。

<!-- ここまで読んだ! -->

### 6.4 ユーザ履歴モデリング

In this section, we explore the effect of Semantic ID on user history modeling. 
このセクションでは、**Semantic IDがユーザ履歴モデリングに与える影響**を探ります。
(ユーザ履歴 = アイテムidのsequence! :thinking:)
One role of the module is to contextualize and summarize the user history. 
モジュールの役割の一つは、ユーザ履歴を文脈化し要約することです。

We find that using Semantic ID and a contextualizing attention-based aggregation module (PMA or Transformer) brings outsized gains compared to a baseline that does not contextualize the sequence (Bypass). 
私たちは、**Semantic IDと文脈化された注意ベースの集約モジュール（PMAまたはTransformer）を使用することで、シーケンスを文脈化しないベースライン（Bypass）と比較して大きな利益が得られること**を発見しました。

These results are summarized in Table 6. 
これらの結果は表6にまとめられています。


![]()
Table 6: Performance for three aggregation modules. Baseline: model with RH for each module. Semantic ID brings larger gains to the contextualizing modules.
表6： 3種の文脈モジュールのパフォーマンス。ベースライン：各モジュールにRHを使用したモデル。セマンティックIDは文脈化モジュールにより大きな利益をもたらします。
（文脈モジュールの違いによらず、semantic idの方が性能が良かったみたい!:thinking:）

<!-- ここまで読んだ! 以下のサブセクションの内容はまだよくわかってない! -->

To understand how using Semantic ID changes the learned attention patterns in PMA and Transformer aggregation modules, we compute four metrics on the attention scores on a random subset of 1,000 evaluation examples.
Semantic IDを使用することでPMAおよびTransformer集約モジュールにおける学習された注意パターンがどのように変化するかを理解するために、1,000の評価例のランダムなサブセットに対する注意スコアの4つのメトリックを計算します。

Let $\mathbf{A} \in \mathbb{R}^{T \times S}$ be the attention score matrix, where $T$ is the target sequence length and $S$ is the source sequence length. 
$\mathbf{A} \in \mathbb{R}^{T \times S}$を注意スコア行列とし、$T$はターゲットシーケンスの長さ、$S$はソースシーケンスの長さとします。
We have $T = S$ for Transformer and Bypass, and $T = 32$ for PMA. 
TransformerおよびBypassの場合、$T = S$であり、PMAの場合は$T = 32$です。
Each row $\mathbf{a}_{i,:}$ of $\mathbf{A}$ represents a probability distribution over the source tokens. 
$\mathbf{A}$の各行$\mathbf{a}_{i,:}$はソーストークンに対する確率分布を表します。
The metrics we consider are defined as follows. 
私たちが考慮するメトリックは以下のように定義されます。

First source token attention: 
最初のソーストークンの注意：

Padding token attention: 
パディングトークンの注意：

Entropy: 
エントロピー：

Token self-attention: 
トークン自己注意：

![]()
Table 7: Attention score-based evaluation metrics for random hashing and SemID-based models for the user history item interaction features. 
表7：ユーザ履歴アイテム相互作用機能に対するランダムハッシングおよびSemIDベースのモデルの注意スコアに基づく評価メトリック。

From the metric readings in Table 7, we see that models trained with Semantic ID have lower entropy, token self-attention, and padding token attention, and higher attention score on the first source token in the sequence. 
表7のメトリックの読み取りから、Semantic IDで訓練されたモデルはエントロピー、トークン自己注意、パディングトークンの注意が低く、シーケンス内の最初のソーストークンに対する注意スコアが高いことがわかります。
This means that Semantic ID-based models place more weight on higher-signal tokens (i.e., the first and most recent item in the sequence, rather than earlier and potentially stale tokens or padding tokens), have attention score distributions that are less diffuse over the entire sequence (i.e., lower entropy), and for Transformer, place higher weights on other tokens rather than self-attending. 
これは、Semantic IDベースのモデルが高信号トークン（すなわち、シーケンス内の最初のアイテムおよび最も最近のアイテム）により多くの重みを置き、全体のシーケンスに対する注意スコア分布がより分散していない（すなわち、エントロピーが低い）ことを意味し、Transformerの場合は自己注意ではなく他のトークンにより高い重みを置くことを示しています。
These metrics are promising signals that Semantic ID item representations are more stable and meaningful than their random hashing-based counterparts in user history modeling. 
**これらのメトリックは、Semantic IDアイテム表現がユーザ履歴モデリングにおいてランダムハッシングベースの対応物よりもより安定しており、意味があることを示す有望な信号**です。

<!-- ここまで読んだ! -->

## 7Productionization 7生産化

The Semantic ID features have been productionized in Meta Ads Recommendation System for more than a year. 
Semantic ID特徴量は、Meta Ads Recommendation Systemで1年以上にわたり本番活用されています。
They serve as top sparse features in the existing ads ranking models according to feature importance studies. 
**それらは、特徴重要度の研究に基づいて、既存の広告ランキングモデルにおける主要なスパース特徴として機能しています。**
In this section, we provide an overview of the online serving pipeline and key implementation details. 
このセクションでは、オンラインサービングパイプラインと主要な実装の詳細について概説します。

### 7.1 オフライン RQ-VAE トレーニング

The RQ-VAE models are trained on Content Understanding (CU) models for ads ranking at Meta. 
RQ-VAEモデルは、**Metaの広告ランキングのためのコンテンツ理解（CU）モデル**でトレーニングされます。
The CU models are pre-trained on the public CC100 dataset Conneau (2020) and then fine-tuned on internal ads datasets. 
CUモデルは、**公開されたCC100データセット（Conneau, 2020）で事前トレーニングされ、その後、内部広告データセットでファインチューニング**されます。(なるほど...! こういう手もあるのか...! CC100はただ言語モデル用のデータセットだった。ニュース推薦モデルを自社データで学習する前にMINDデータセットで事前学習する、みたいな手もあるのかな...??:thinking:)
We sample ad IDs and their corresponding content embeddings from the past three months’ data and train the RQ-VAE model offline. 
私たちは、過去3か月のデータから広告IDとそれに対応するコンテンツ埋め込みをサンプリングし、RQ-VAEモデルをオフラインでトレーニングします。
For production models, we train RQ-VAEs with $L=6$ and $K=2048$, and Semantic ID follows the design of prefix-5gram from Section 4.2 with $H=O(50M)$. 
プロダクションモデルでは、$L=6$および$K=2048$でRQ-VAEをトレーニングし、Semantic IDはセクション4.2のprefix-5gramの設計に従い、$H=O(50M)$となります。
After training, we use a frozen RQ-VAE checkpoint for online serving. 
トレーニング後、オンラインサービスのためにフローズンRQ-VAEチェックポイントを使用します。

<!-- ここまで読んだ! -->

### 7.2 Online Semantic ID Serving System 7.2 オンラインセマンティックIDサービングシステム

![]()
Figure 4: 図4:Semantic ID serving pipeline. セマンティックIDサービングパイプライン。

Figure 4 shows the online serving pipeline of real-time Semantic ID features. 
図4は、リアルタイムセマンティックID機能のオンラインサービングパイプラインを示しています。
At ad creation time, we process the ad content information and provide it to the CU models. 
**広告作成時に、広告コンテンツ情報を処理し、それをCUモデルに提供**します。(うんうん、streamlingもしくはマイクロバッチで処理する感じかな...!:thinking:)
The output CU embeddings are then passed through the RQ-VAE model which computes the Semantic ID signal for each raw ID. 
出力されたCU埋め込みは、RQ-VAEモデルを通過し、各生IDのセマンティックID信号(=ここではidなのか...!:thinking:)を計算します。
The signal is then stored in the Entity Data Store. 
その信号は、エンティティデータストアに保存されます。(=feature store的なやつ!:thinking:)
At the feature generation stage, the target item raw ID and user engagement raw ID histories are enriched with the Semantic ID signal from the Entity Data Store to produce semantic features. 
特徴(=idのembedding)生成段階では、ターゲットアイテムの生IDとユーザーエンゲージメントの生ID履歴が、エンティティデータストアからのセマンティックID信号で強化され、セマンティック特徴(=ここでidからembeddingになる!:thinking:)が生成されます。
When serving requests arrive, the precomputed features are fetched and passed to the downstream ranking models. 
**リクエストが到着すると、事前計算された特徴が取得され、下流のランキングモデルに渡されます**。(うんうん。リアルタイム推論時には事前計算されたembeddingを取得するだけ!:thinking:)

<!-- ここまで読んだ! -->


### 7.3 生産性能の向上

We created six sparse and one sequential feature from different content embedding sources, including text, image, and video, and report the NE gain on the flagship Meta ads ranking model in Table 8. 
私たちは、テキスト、画像、動画を含むさまざまなコンテンツ埋め込みソースから6つのスパース特徴と1つのシーケンシャル特徴を作成し、表8のフラッグシップMeta広告ランキングモデルにおけるNEの向上を報告します。
In Meta ads ranking, an offline NE gain larger than 0.02% is considered significant. 
**Meta広告ランキングでは、オフラインのNEの向上が0.02%を超えるとsignificant**と見なされます。
Overall, across multiple ads ranking models, incorporating the Semantic ID features have yielded a 0.15% gain in performance on our top-line online metric. 
全体として、複数の広告ランキングモデルにおいて、Semantic ID特徴を組み込むことで、私たちの主要なオンライン指標で0.15%の性能向上が得られました。
As the Meta Ads recommender serves billions of users and has been one of the most optimized models in the company, a 0.15% online performance gain is considered significant. 
**Meta Adsレコメンダーは数十億のユーザーにサービスを提供し、会社の中で最も最適化されたモデルの1つであるため、0.15%のオンライン性能向上はsignificantと見なされます。**(価値のある効果量ってことね...!:thinking:)

![]()
Table 8: NE improvement from incorporating Semantic ID features in the flagship Meta ads ranking model. 
表8：フラッグシップMeta広告ランキングモデルにおけるSemantic ID特徴を組み込むことによるNEの改善。

<!-- ここまで読んだ! -->

### 7.4 Semanic and Prediction Similarity 7.4 セマンティックおよび予測類似性

Intuitively, one may think that if two items are semantically similar, their user engagement patterns will also be similar. 
直感的には、2つのアイテムがセマンティックに類似している場合、それらのユーザーエンゲージメントパターンも類似していると考えるかもしれません。しかし、**ユーザーの行動や認識はより微妙であり、セマンティクスに関して予測可能に連続しているわけではありません**。(=要するに、ユーザの嗜好って内容ベースだけじゃないよね、みたいな話??:thinking:)
For robust delivery performance with Semantic ID, we must ensure a degree of continuity (or correlation) of the ranking model’s behaviour with respect to the semantic similarity relation between the items in our system. 
Semantic IDを用いた堅牢な配信パフォーマンスを実現するためには、システム内のアイテム間のセマンティック類似性関係に関して、ランキングモデルの挙動の連続性（または相関）を確保する必要があります。

To measure this correlation, we conduct an online A/B test where we select a set $S$ of items that are recommended to a user by our system. 
この相関を測定するために、私たちはオンラインA/Bテストを実施し、システムによってユーザに推薦されるアイテムのセット$S$を選択します。
For a given user, with 50% probability, we mutate the set $S$ to $S'$ by randomly swapping an item in $S$ with a different item with the same prefix from Semantic ID. 
**特定のユーザーに対して、50%の確率で、セット$S$のアイテムをSemantic IDの同じプレフィックスを持つ別のアイテムとランダムに入れ替えることによって、セット$S$を$S'$に変異させます**。
This operation results in a ...
この操作結果は...

$$
\text{Click Loss Rate} = \frac{\text{CTR on S'} - \text{CTR on S}}{\text{CTR on S}}
\tag{3}
$$

The click loss rate decrease from using deeper prefixes from Semantic ID is summarized in Figure 5. 
Semantic IDからのより深いプレフィックスを使用することによるクリック損失率の減少は、図5にまとめられています。

Figure 5: Click Loss Rate reduction from Semantic ID. 
図5：Semantic IDからのクリック損失率の減少。

Since Semantic ID partitions the item corpus based on item semantics, we conclude that prediction similarity is correlated to semantic similarity. 
Semantic IDがアイテムのセマンティクスに基づいてアイテムコーパスを分割するため、**予測類似性はセマンティック類似性と相関している**と結論付けます。
This supports the representation space analysis result in Section 6.3. 
これは、セクション6.3の表現空間分析結果を支持します。
Moreover, the hierarchy of codes in Semantic ID effectively captures the finer-grained details of an item’s semantics: deeper prefixes monotonically reduce the click loss rate. 
さらに、**Semantic IDのコードの階層は、アイテムのセマンティクスのより細かい詳細を効果的に捉えています：より深いプレフィックスはクリック損失率を単調に減少させます**。

(単に一括で埋め込みに変換するよりも、こうやって明示的に階層的にした方が、いい感じにセマンティクスを捉えられたりするのかな...!:thinking:)

<!-- ここまで読んだ! -->

### 7.5A/A Variance 7.5 A/A分散

Yet another disadvantage of a ranking model based on random hashing is inherent model prediction variance, resulting in downstream ad delivery variance. 
ランダムハッシングに基づくランキングモデルのもう一つの欠点は、固有のモデル予測分散であり、これが下流の広告配信の分散を引き起こします。
Specifically, one can create a copy of an item with a different raw item ID. 
具体的には、異なる生のアイテムIDを持つアイテムのコピーを作成することができます。
Then, both the original and item copy enter the recommendation system. 
その後、元のアイテムとそのコピーの両方が推薦システムに入ります。
Because the embeddings will be different for the original and item copy after hashing, the model predictions and delivery system behavior will also differ. 
ハッシング後、元のアイテムとそのコピーの埋め込みが異なるため、モデルの予測と配信システムの動作も異なります。
We call this phenomenon the A/A variance, where “A/A” signifies that we consider an exact copy of the original item. 
私たちはこの現象をA/A分散と呼びます。「A/A」は、元のアイテムの正確なコピーを考慮することを示しています。
A related type of a ranking model variance is the A/A’ variance where one instead considers minor item differences instead of exact copies, such as two images with the same object in the foreground, but with backgrounds of different colors. 
ランキングモデルの分散の関連するタイプはA/A’分散であり、正確なコピーの代わりに、前景に同じオブジェクトがあるが背景の色が異なる2つの画像のような、わずかなアイテムの違いを考慮します。
This variance is undesirable since it reduces the robustness of the downstream ad ranking orders and the system’s ability to accurately target correct audiences. 
この分散は望ましくなく、下流の広告ランキングの順序の堅牢性を低下させ、システムが正しいオーディエンスを正確にターゲットする能力を減少させます。
Semantic ID helps reduce the A/A variance by eliminating the randomness caused by random hashing – exact copies or very similar items will often have the same $k$-prefix Semantic ID. 
Semantic IDは、ランダムハッシングによって引き起こされるランダム性を排除することにより、A/A分散を減少させるのに役立ちます。正確なコピーや非常に似たアイテムは、しばしば同じ$k$-プレフィックスのSemantic IDを持ちます。

A/A variance A/A分散

A related type of a ranking model variance is the A/A’ variance where one instead considers minor item differences instead of exact copies, such as two images with the same object in the foreground, but with backgrounds of different colors. 
ランキングモデルの分散の関連するタイプはA/A’分散であり、正確なコピーの代わりに、前景に同じオブジェクトがあるが背景の色が異なる2つの画像のような、わずかなアイテムの違いを考慮します。

We set up an online shadow ads experiment where we measure the relative A/A prediction difference (AAR) for a given model. 
私たちは、特定のモデルに対する相対的なA/A予測差（AAR）を測定するオンラインシャドー広告実験を設定しました。

For an A/A pair $(a_{1}, a_{2})$, 
A/Aペア $(a_{1}, a_{2})$ に対して、

where $p(a_{i})$ is the ranking model prediction for item $a_{i}$. 
ここで、$p(a_{i})$ はアイテム $a_{i}$ に対するランキングモデルの予測です。

The production model with six Semantic ID sparse features achieves a $43\%$ reduction in average AAR compared to the same model without the six features. 
6つのSemantic IDスパース特徴を持つ生産モデルは、6つの特徴がない同じモデルと比較して、平均AARを$43\%$削減します。
We believe that the majority of AAR reduction is from the tail items, as studied in Section 6.2. 
私たちは、AAR削減の大部分がセクション6.2で研究されたテールアイテムから来ていると考えています。

<!-- このサブセクションはちゃんと読んでないが一旦OK! -->

## 8Conclusion 結論

We show how Semantic ID can be used to create a stable ID space for item representation and propose Semantic ID prefix-ngram, which significantly improves Semantic ID’s performance in ranking models. 
私たちは、Semantic IDがアイテム表現のための安定したID空間を作成する方法を示し、Semantic ID prefix-ngramを提案します。これは、ランキングモデルにおけるSemantic IDの性能を大幅に向上させます。
In offline experiments, we study trained ranking models and find that under Semantic ID, the harmful effects of embedding representation instability are mitigated compared to random hashing and individual embeddings baselines. 
オフライン実験では、訓練されたランキングモデルを研究し、Semantic IDの下では、ランダムハッシングや個別の埋め込みベースラインと比較して、埋め込み表現の不安定性の有害な影響が軽減されることを発見しました。
We detail the successful productionization of Semantic ID features in Meta’s ads recommendation system, and show that the online production system obtains significant performance gains as well as reduced downstream ad delivery variance. 
私たちは、Metaの広告推薦システムにおけるSemantic ID機能の成功した製品化の詳細を説明し、オンライン製品システムが重要な性能向上と下流の広告配信のばらつきの減少を達成することを示します。

<!-- ここまで読んだ! -->

## Appendix A Aggregation Module Architectures 付録A 集約モジュールのアーキテクチャ

### Bypass. バイパス。

Apply a linear weight matrix $\mathbf{W} \in \mathbb{R}^{d_{m} \times d_{m}}$ to each embedding separately,  
各埋め込みに対して線形重み行列 $\mathbf{W} \in \mathbb{R}^{d_{m} \times d_{m}}$ を適用します。

$$
Bypass(X) := XW
\tag{5}
$$


### Transformer (Vaswani, 2017). 

Apply a Transformer layer to the embedding sequence. The attention submodule is defined as  
埋め込みシーケンスにTransformer層を適用します。注意サブモジュールは次のように定義されます。

$$
Attention(X) := \text{softmax}\left(\frac{XW^{Q}(XW^{K})^{T}}{\sqrt{d_{m}}}\right)XW^{V}
\tag{6}
$$

where $\mathbf{W}^{Q}, \mathbf{W}^{K}, \mathbf{W}^{V} \in \mathbb{R}^{d_{m} \times d_{a}}$ are the query, key, and value weight matrices, respectively, and $d_{a}$ is the query/key/value vector dimension. The full Transformer module is given by  
ここで、$\mathbf{W}^{Q}, \mathbf{W}^{K}, \mathbf{W}^{V} \in \mathbb{R}^{d_{m} \times d_{a}}$ はそれぞれクエリ、キー、バリューの重み行列であり、$d_{a}$ はクエリ/キー/バリューのベクトル次元です。完全なTransformerモジュールは次のように与えられます。

$$
X^{(1)} = Attention(LayerNorm(X)) + X
\tag{7}
$$

$$
X^{(2)} = MLP(LayerNorm(X^{(1)})) + X^{(1)}
\tag{8}
$$

where LayerNorm and MLP designate the standard layer norm and position-wise MLP layers. We add standard positional embeddings to the encoding before applying Transformer or PMA modules.  
ここで、LayerNormとMLPは標準のレイヤーノルムと位置ごとのMLP層を指定します。TransformerまたはPMAモジュールを適用する前に、エンコーディングに標準的な位置埋め込みを追加します。

### Pooled Multihead Attention (PMA) (Lee et al., 2019). 

Apply a Transformer layer to the embedding sequence, but replace the attention query vectors with $d_{s}$ learnable weight vectors. The PMA attention submodule is defined as  
埋め込みシーケンスにTransformer層を適用しますが、注意クエリベクトル ($d_{m}$) を$d_{s}$の学習可能な重みベクトルに置き換えます。PMA注意サブモジュールは次のように定義されます。

$$
PMAttention(X) := \text{softmax}\left(\frac{S(XW^{K})^{T}}{\sqrt{d_{m}}}\right)XW^{V}
\tag{9}
$$

where $\mathbf{S} \in \mathbb{R}^{d_{s} \times d_{a}}$ is comprised of $d_{s}$ learnable query vectors, or seeds. In our experiments, $d_{s} = 32$.  
ここで、$\mathbf{S} \in \mathbb{R}^{d_{s} \times d_{a}}$ は$d_{s}$の学習可能なクエリベクトル、またはシードから構成されます。私たちの実験では、$d_{s} = 32$です。

The PMA module is formed using the same equations as for the Transformer module (Equations 7 and 8), except that PMAttention is used in place of Attention.  
PMAモジュールは、Transformerモジュールと同じ方程式（方程式7および8）を使用して形成されますが、Attentionの代わりにPMAttentionが使用されます。

<!-- ここまで読んだ! -->

## Appendix B セマンティックIDのクリック分布

Appendix B  
図6:  
Figure 6  
The 30-day click distribution in raw ID and Semantic ID spaces.  
30日間の生IDおよびセマンティックID空間におけるクリック分布。  
The click distribution in Semantic ID space (Figure 6) clearly exhibits less skew compared to the click distribution in the raw ID space.  
セマンティックID空間におけるクリック分布（図6）は、生ID空間におけるクリック分布と比較して明らかに偏りが少ないことを示しています。  
Note that while Figure 2 shows the cumulative distribution of impressions, Figure 6 shows the marginal distribution of clicks.  
図2がインプレッションの累積分布を示すのに対し、図6はクリックの周辺分布を示していることに注意してください。  



##### Report Github Issue GitHubの問題報告

LATE
LATE

A
A

E
E

xml
xml



## Instructions for reporting errors エラー報告の手順

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. 
私たちは論文のHTMLバージョンを改善し続けており、あなたのフィードバックはアクセシビリティとモバイルサポートの向上に役立ちます。 
To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:
HTMLのエラーを報告するには、以下のいずれかの方法を選択してください。

- Click the "Report Issue" button.
- "Report Issue"ボタンをクリックします。
- Open a report feedback form via keyboard, use "Ctrl + ?".
- キーボードを使用して報告フィードバックフォームを開くには、「Ctrl + ?」を使用します。
- Make a text selection and click the "Report Issue for Selection" button near your cursor.
- テキストを選択し、カーソルの近くにある「選択の問題を報告」ボタンをクリックします。
- You can use Alt+Y to toggle on and Alt+Shift+Y to toggle off accessible reporting links at each section.
- 各セクションでアクセシブルな報告リンクをオン/オフするには、Alt+Yを使用します。

Our team has already identified the following issues. 
私たちのチームはすでに以下の問題を特定しています。 
We appreciate your time reviewing and reporting rendering errors we may not have found yet. 
私たちは、まだ見つけていない可能性のあるレンダリングエラーをレビューし報告するためにあなたが費やす時間に感謝します。 
Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. 
あなたの努力は、すべての読者のためにHTMLバージョンを改善するのに役立ちます。なぜなら、障害は研究へのアクセスの障壁であってはならないからです。 
Thank you for your continued support in championing open access for all.
すべての人にオープンアクセスを推進するための継続的なサポートに感謝します。

Have a free development cycle? Help support accessibility at arXiv! 
開発サイクルに余裕がありますか？arXivでのアクセシビリティをサポートしてください！ 
Our collaborators at LaTeXML maintain a list of packages that need conversion, and welcome developer contributions.
私たちのLaTeXMLの協力者は、変換が必要なパッケージのリストを維持しており、開発者の貢献を歓迎します。
