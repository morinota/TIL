- refs:
  - https://arxiv.org/abs/2411.19513
  - https://github.com/kumo-ai/ContextGNN


# ContextGNN: Beyond Two-Tower Recommendation Systems

Yiwen Yuan, Zecheng Zhang, Xinwei He, Akihiro Nitta, Weihua Hu, Dong Wang, Manan Shah, Shenyang Huang, Blaž Stojanovič, Alan Krumholz, Jan Eric Lenssen, Jure Leskovec, Matthias Fey Kumo.AI
Yiwen Yuan, Zecheng Zhang, Xinwei He, Akihiro Nitta, Weihua Hu, Dong Wang, Manan Shah, Shenyang Huang, Blaž Stojanovič, Alan Krumholz, Jan Eric Lenssen, Jure Leskovec, Matthias Fey Kumo.AI

## Abstract 概要

Recommendation systems predominantly utilize two-tower architectures, which evaluate user-item rankings through the inner product of their respective embeddings.
推薦システムは主に二塔型アーキテクチャを利用しており、これはそれぞれの埋め込みの内積を通じてユーザとアイテムのランキングを評価します。
However, one key limitation of two-tower models is that they learn a pair-agnostic representation of users and items.
しかし、二塔型モデルの一つの重要な制限は、ユーザとアイテムのペアに依存しない表現を学習することです。
In contrast, pair-wise representations either scale poorly due to their quadratic complexity or are too restrictive on the candidate pairs to rank.
対照的に、ペアワイズ表現はその二次的な複雑さのためにスケールが悪くなるか、ランキングする候補ペアに対して制約が厳しすぎます。
To address these issues, we introduce Context-based Graph Neural Networks (ContextGNNs), a novel deep learning architecture for link prediction in recommendation systems.
これらの問題に対処するために、私たちは**Context-based Graph Neural Networks（ContextGNNs）を導入**します。これは推薦システムにおけるリンク予測のための新しい深層学習アーキテクチャです。
The method employs a pair-wise representation technique for familiar items situated within a user’s local subgraph, while leveraging two-tower representations to facilitate the recommendation of exploratory items.
この手法は、**ユーザのローカルサブグラフ内に位置する馴染みのあるアイテムに対してペアワイズ表現技術を採用**し、探索的アイテムの推薦を促進するために二塔型表現を活用します。
A final network then predicts how to fuse both pair-wise and two-tower recommendations into a single ranking of items.
**最終的なネットワークは、ペアワイズとtwo-towerの推薦をどのように融合してアイテムの単一のランキングにするかを予測**します。
We demonstrate that ContextGNN is able to adapt to different data characteristics and outperforms existing methods, both traditional and GNN-based, on a diverse set of practical recommendation tasks, improving performance by 20% on average.
私たちは、ContextGNNが異なるデータ特性に適応でき、従来の手法やGNNベースの手法を超えて、さまざまな実用的な推薦タスクにおいて平均して20%のパフォーマンス向上を達成することを示します。

<!-- ここまで読んだ! -->

## 1Introduction 1 はじめに

Recommendation systems have emerged as an important application domain for predictive machine learning over the past decades(Webber,2021; He etal.,2023; Li etal.,2024). 
推薦システムは、過去数十年にわたり、予測機械学習の重要な応用分野として登場しました（Webber, 2021; He et al., 2023; Li et al., 2024）。
Given a set of users and a set of items (e.g., products available for purchase), recommendation systems aim to identify optimal item recommendations for each user (e.g., products most likely to be purchased by the user). 
ユーザの集合とアイテムの集合（例：購入可能な製品）が与えられた場合、推薦システムは各ユーザに対して最適なアイテム推薦（例：ユーザが最も購入する可能性の高い製品）を特定することを目的としています。
Traditionally, this problem is modeled via different variants of a two-tower paradigm(Hu etal.,2008; Koren etal.,2009), where one tower embeds users and the other tower embeds items, which are then matched and ranked via an inner-product decoder. 
従来、この問題は、**ユーザを埋め込む一つのタワーとアイテムを埋め込むもう一つのタワーを持つtwo-towerパラダイム**の異なるバリアント(確かにいろんな種類あるよね...:thinking:)を通じてモデル化されており、これらは**内積デコーダを介してマッチングおよびランキング**されます。
This scheme proves to be highly efficient for scaling up recommendation systems during the inference phase, as it allows to pre-compute user and item representations and to perform the final ranking via fast (approximate) maximum inner product search(Johnson etal.,2019). 
**このスキームは、推論フェーズ中に推薦システムをスケールアップするために非常に効率的であることが証明**されており、ユーザとアイテムの表現を事前に計算し、迅速な（近似的な）最大内積検索を介して最終的なランキングを実行することを可能にします（Johnson et al., 2019）。
(うんうん、本番システムで運用する上でやりやすいんだよね...:thinking:)

However, one key limitation of two-tower based architectures for recommendation is that they learn a pair-agnostic representation for users and items. 
しかし、**推薦のためのtwo-towerベースのアーキテクチャの一つの重要な制限は、ユーザとアイテムのペアに依存しない表現を学習すること**です。
That is, the user representation is not aware of the item under consideration, and similarly, the item representation is not aware of the user and thus item representations are not capturing the uniqueness of user’s view on the items. 
**つまり、ユーザの表現は考慮中のアイテムを認識せず、同様にアイテムの表現はユーザを認識せず、そのためアイテムの表現はユーザのアイテムに対する見方の独自性を捉えていません**。(いい言語化、テックブログを書く時があったら引用したい...!!:thinking:)
As such, neither of the representations on both ends capture knowledge about the pair-wise dependency they are making a prediction for. 
<!-- そのため、両端の表現は、彼らが予測を行っているペアワイズ依存性に関する知識を捉えていません。 -->
そのため、両方の埋め込み表現はどちらも、実際にtwo-towerモデルで予測したいペアワイズ依存性を捉えられていない。
For example, consider a user who restocks their cosmetic products on a regular basis. 
例えば、化粧品を定期的に補充するユーザを考えてみましょう。
In this scenario, the fine-grained context of user-cosmetic pairs is crucial, which cannot be adequately captured by two independent user and item representations alone. 
このシナリオでは、**ユーザと化粧品のペアの詳細なコンテキストが重要であり、これは二つの独立したユーザとアイテムの表現だけでは十分に捉えることができません**。
Such lack of knowledge has severe consequences on the quality of predictions, since, e.g., the model is unable to distinguish between scenarios such as familiar purchases (i.e., users who repeatedly interact with the similar set of items) vs. exploratory purchases (i.e., users who like to explore new items). 
このような知識の欠如は予測の質に深刻な影響を及ぼします。例えば、モデルは、類似のアイテムセットと繰り返し相互作用するユーザによる馴染みのある購入と、新しいアイテムを探索するのが好きなユーザによる探索的購入のシナリオを区別できません。
While pair-wise representations, which incorporate the knowledge about the pair they are making a prediction for, are able to contextualize the prediction, one would need to generate pair-wise representations for all possible user-item pairs, which is ineffable due to its quadratic complexity. 
ペアワイズ表現は、彼らが予測を行っているペアに関する知識を取り入れることで予測を文脈化することができますが、**すべての可能なユーザ-アイテムペアのためにペアワイズ表現を生成する必要があり、これは二次的な複雑さのために実行不可能**です。
Alternatively, one can pre-filter the set of candidate pairs, e.g., via content-based filtering or collaborative filtering (Ricci etal. (2010); Campana & Delmastro (2017)), but the model’s capabilities are then limited by the recall of the candidate generation procedure. 
あるいは、候補ペアのセットを事前にフィルタリングすることも可能ですが（例：コンテンツベースのフィルタリングや協調フィルタリング（Ricci et al. (2010); Campana & Delmastro (2017)））、その場合、**モデルの能力は候補生成手続きのリコールによって制限されます**。(うんうん...:thinking:)

<!-- ここまで読んだ! -->

Here, we develop Context-based Graph Neural Networks (ContextGNNs), a novel single-stage Graph Neural Network (GNN)-based recommendation system that fuses pair-wise representations and two-tower representations into a single unified architecture. 
ここでは、**ペアワイズ表現とtwo-tower表現を単一の統一アーキテクチャに融合させた新しいsingle-stageのグラフニューラルネットワーク（GNN）ベースの推薦システム**であるContext-based Graph Neural Networks（ContextGNNs）を開発します。
ContextGNN is designed to perform temporal recommendations (predict the next set of items a user will interact with) on a heterogeneous temporal graph, and leverages the best of both worlds: 
ContextGNNは、異種の時間的グラフ上で時間的推薦（ユーザが次に相互作用するアイテムのセットを予測する）を行うように設計されており、両方の利点を活用します。
The first model supports pair-wise representations for all items within a user’s local interaction graph (Zhu etal.,2021). 
最初のモデルは、ユーザのローカル相互作用グラフ内のすべてのアイテムに対してペアワイズ表現をサポートします（Zhu et al., 2021）。
For distant user-item pairs, i.e., user-item pairs that are not within the $k$-hop neighborhood of each other, the pair-wise embeddings are supplemented by a global, two-tower-based GNN, which serves as an effective fallback model. 
遠く離れたユーザ-アイテムペア、すなわち、互いに $k$ -ホップ近傍にないユーザ-アイテムペアに対しては、**ペアワイズ埋め込みがグローバルなtwo-towerベースのGNNによって補完され、これは効果的なフォールバックモデルとして機能**します。
A final network then predicts a user-specific, personalized fusion score that dictates how to merge both pair-wise and two-tower recommendations into a single ranking. 
最終的なネットワークは、ペアワイズとtwo-towerの推薦を単一のランキングに統合する方法を決定するユーザ特有のパーソナライズされた融合スコアを予測します。

<!-- ここまで読んだ! -->

The key idea behind ContextGNN is to contextualize the prediction for the area of items for which a user has rich past interactions. 
ContextGNNの背後にある重要なアイデアは、ユーザが豊富な過去の相互作用を持つアイテムの領域に対する予測を文脈化することです。
Here, pair-wise representations are able to capture fine-grained patterns of past user-item interactions, such as repeat purchases and other prior actions (e.g., clicks, tag-as-favorite, add-to-cart), or through collaborative signals (e.g., whether friends have purchased the same item). 
ここでは、ペアワイズ表現が過去のユーザ-アイテム相互作用の詳細なパターン（例：リピート購入や他の以前のアクション（例：クリック、お気に入りにタグ付け、カートに追加））を捉えることができ、また協調信号（例：友人が同じアイテムを購入したかどうか）を通じて捉えることができます。
The second component, a novel pair-agnostic two-tower model based on shallow item embeddings, allows for modeling exploratory and serendipitous recommendations. 
第二のコンポーネントは、浅いアイテム埋め込みに基づく新しいペアに依存しないtwo-towerモデルであり、探索的および偶然の推薦をモデル化することを可能にします。
For these “distant” items, where no specific user-item context exists, pair-wise representations offer minimal benefits, making the fallback to two-tower representations suitable. 
これらの「遠く離れた」アイテムにおいては、特定のユーザ-アイテムコンテキストが存在しないため、**ペアワイズ表現は最小限の利点しか提供せず、two-tower表現へのフォールバックが適切**です。
Importantly, the two-tower model is designed in such a way that it allows for integration into pair-wise architectures with little computational overhead. 
**重要なのは、two-towerモデルが計算オーバーヘッドをほとんどかけずにペアワイズアーキテクチャに統合できるように設計されていること**です。
Finally, the model learns which users prefer familiar items over exploratory purchases and adjusts the final ranking scores accordingly. 
最後に、モデルはどのユーザが探索的購入よりも馴染みのあるアイテムを好むかを学習し、最終的なランキングスコアをそれに応じて調整します。

<!-- ここまで読んだ! -->

We deploy ContextGNNs in the context of relational deep learning (Fey etal.,2024) for recommendation within relational databases. 
私たちは、関係データベース内での推薦のために、**関係深層学習（Fey et al., 2024）の文脈でContextGNNsを展開**します。(relational deep learningってなんだ?? :thinking:)
Relational databases (Robinson etal.,2024) comprise diverse sets of tables with rich multi-modal input features and rich multi-behavioral, temporal interactions, making them the perfect setting for stress-testing our model. 
関係データベース（Robinson et al., 2024）は、豊富なマルチモーダル入力特徴と豊富なマルチ行動的、時間的相互作用を持つ多様なテーブルのセットで構成されており、私たちのモデルをストレステストするための理想的な環境を提供します。
Furthermore, we examine the challenges in modeling the complex patterns of human behavior. 
さらに、私たちは人間の行動の複雑なパターンをモデル化する際の課題を検討します。
Our analysis and experimental results underscore the need for a hybrid architecture, as a single model is not sufficient to address the diversity of real-world datasets both within and across tasks effectively. 
私たちの分析と実験結果は、単一のモデルではタスク内およびタスク間の実世界のデータセットの多様性に効果的に対処するには不十分であるため、ハイブリッドアーキテクチャの必要性を強調しています。
We demonstrate that ContextGNN is able to adapt to different data characteristics, while outperforming existing models on realistic and practical recommendation tasks. 
私たちは、ContextGNNが異なるデータ特性に適応できることを示し、現実的かつ実用的な推薦タスクにおいて既存のモデルを上回ることを示します。
In particular, ContextGNN improves results by 20% on average compared to the best pair-wise representation baseline, and by 344% on average compared to the best two-tower representation baseline. 
特に、ContextGNNは、最良のペアワイズ表現ベースラインと比較して平均20％、最良の二塔表現ベースラインと比較して平均344％の結果を改善します。

<!-- ここまで読んだ! -->

## Related Work 関連研究

Recommendation systems are a long-standing research area in machine learning.  
推薦システムは、機械学習における長年の研究分野です。
The recommendation problem is often formulated as link prediction on a bipartite graph with two sets of nodes, one containing the users and another containing the items.
推薦問題は、通常、ユーザを含むノードのセットとアイテムを含むノードのセットを持つ二部グラフ上でのリンク予測として定式化されます。
Between these two node sets, past interactions are presented as links, and the goal is to predict which links are going to occur in the future.  
これらの二つのノードセットの間で、過去の相互作用はリンクとして示され、目標は将来どのリンクが発生するかを予測することです。
Traditionally, it is approached by computing the inner product of user and item embeddings, e.g., via matrix factorization (Koren et al., 2009) to discover and utilize similarity between users and items, i.e. collaborative filtering (Hu et al., 2008; Mnih & Salakhutdinov, 2007).  
従来は、ユーザとアイテムの埋め込みの内積を計算することによってアプローチされ、例えば、行列因子分解（Koren et al., 2009）を通じてユーザとアイテムの類似性を発見し、利用すること、すなわち協調フィルタリング（Hu et al., 2008; Mnih & Salakhutdinov, 2007）です。

Similar to many other areas, deep learning made an impact in recommendation systems, e.g., by predicting scores with non-linear networks (H. & C., 2017; He et al., 2017), by utilizing graph embedding techniques (Perozzi et al., 2014; Grover & Leskovec, 2016), or by sampling from distributions modeled by a variational autoencoder (Liang et al., 2018).  
他の多くの分野と同様に、深層学習は推薦システムに影響を与えました。例えば、非線形ネットワーク（H. & C., 2017; He et al., 2017）を用いてスコアを予測したり、**グラフ埋め込み技術（Perozzi et al., 2014; Grover & Leskovec, 2016）を利用**したり、変分オートエンコーダ（Liang et al., 2018）によってモデル化された分布からサンプリングしたりします。
Recently, the new field of generative recommendation deserves mentioning, utilizing large language models to provide recommendation by text generation (Wu et al., 2023).  
最近、生成的推薦の新しい分野が注目されており、大規模言語モデルを利用してテキスト生成による推薦を提供しています（Wu et al., 2023）。
Our work here relates to two lines of research: Sequential recommendation systems and recommendations with GNNs.  
ここでの私たちの研究は、**シーケンシャル推薦システムとGNNを用いた推薦の二つの研究ライン**に関連しています。

### Recommendation on Sequences. シーケンスにおける推薦

Recommendation has traditionally been modeled as a sequence prediction problem.  
推薦は従来、シーケンス予測問題としてモデル化されてきました。
Early methods utilize Markov chains (Rendle et al., 2010; He & McAuley, 2016), which have later been replaced by recurrent neural networks (Liu et al., 2018), temporal attention (Kang & McAuley, 2018; Li et al., 2017) and transformer formulations (Sun et al., 2019; Yang et al., 2022; Xia et al., 2022).  
初期の手法はマルコフ連鎖（Rendle et al., 2010; He & McAuley, 2016）を利用していましたが、後に再帰型ニューラルネットワーク（Liu et al., 2018）、時間的注意（Kang & McAuley, 2018; Li et al., 2017）、およびトランスフォーマーの定式化（Sun et al., 2019; Yang et al., 2022; Xia et al., 2022）に置き換えられました。
They also have been combined with GNNs to additionally capture collaborative signals (Ma et al., 2020).  
これらはGNNと組み合わせて、協調信号を追加で捉えることも行われています（Ma et al., 2020）。

<!-- ここまで読んだ! -->

### Recommendation with GNNs. GNNを用いた推薦

Various two-tower-based Graph Neural Networks (Hamilton et al., 2017) have been developed for link prediction tasks, based on the idea of integrating the paradigm of collaborative filtering via refining embeddings on the user-item interaction graph.  
ユーザ-アイテム相互作用グラフ上の埋め込みを洗練することによって協調フィルタリングのパラダイムを統合するというアイデアに基づいて、**リンク予測タスクのためにさまざまなtwo-towerベースのグラフニューラルネットワーク（Hamilton et al., 2017）が開発**されています。(GNNベースのtwo-towerモデルが結構あるのか...!:thinking:)
Early examples use GNN-based autoencoders (Kipf & Welling, 2016; Schlichtkrull et al., 2018) to obtain prediction on graph links.  
初期の例では、GNNベースのオートエンコーダ（Kipf & Welling, 2016; Schlichtkrull et al., 2018）を使用してグラフリンクの予測を行います。
Since GNNs propagate information locally (and thus cannot reason about the position of nodes inside a graph), it has been shown that propagating shallow user and item embeddings with deep GNNs is crucial to capture the full collaborative signal (Wang et al., 2019).
GNNは情報を局所的に伝播するため（したがって、グラフ内のノードの位置について推論できない）、浅いユーザとアイテムの埋め込みを深いGNNで伝播させることが、完全な協調信号を捉えるために重要であることが示されています（Wang et al., 2019）。
LightGCN (He et al., 2020) and UltraGCN (Mao et al., 2021) further simplify message propagation for embedding generation for improved performance on small-scale datasets.  
LightGCN（He et al., 2020）とUltraGCN（Mao et al., 2021）は、小規模データセットでのパフォーマンス向上のために埋め込み生成のメッセージ伝播をさらに簡素化します。
Another line of work strengthens GNN-based recommender systems by adding self-supervision (Wu et al., 2021; Yu et al., 2022; Cai et al., 2023), e.g., based on contrastive learning via graph augmentations.  
別の研究ラインでは、自己教師あり学習?を追加することによってGNNベースの推薦システムを強化しています（Wu et al., 2021; Yu et al., 2022; Cai et al., 2023）。例えば、グラフ拡張を通じた対照学習に基づいています。
These findings are orthogonal to our work, but still embrace a two-tower architecture under the hood.  
これらの発見は私たちの研究とは直交していますが、**依然として内部でtwo-towerアーキテクチャを採用しています**(ほ〜ん...!:thinking:)。

The line of work that comes closest to ContextGNN is related to encoding identity- and position-awareness into GNNs in order to relate user-item pairs (You et al., 2019; 2021).  
ContextGNNに最も近い研究ラインは、**ユーザ-アイテムペアを関連付けるためにGNNにアイデンティティと位置の認識をエンコードすることに関連しています**（You et al., 2019; 2021）。
For example, local subgraphs have been extended to encode positional information of user-item pairs (Zhang & Chen, 2018; Teru et al., 2020), but lack an efficient inference procedure.  
例えば、ローカルサブグラフはユーザ-アイテムペアの位置情報をエンコードするために拡張されています（Zhang & Chen, 2018; Teru et al., 2020）が、効率的な推論手続きが欠けています。
NBFNet (Zhu et al., 2021) introduces a path-based pair-wise representation model that constructs a subgraph centered around the user node, while reading out the GNN’s representations at the item nodes.  
NBFNet（Zhu et al., 2021）は、ユーザノードを中心にサブグラフを構築し、アイテムノードでGNNの表現を読み出すパスベースのペアワイズ表現モデルを導入します。
This method yields item representations that are conditioned on the specific user, thereby incorporating pair-wise information without incurring excessive computational cost.  
この手法は、特定のユーザに条件付けられたアイテム表現を生成し、過剰な計算コストをかけることなくペアワイズ情報を組み込むことができます。
However, this method constrains candidates to items within the user’s subgraph, which tremendously limits its effectiveness in scenarios involving exploratory recommendations or cold-start items.  
しかし、この手法は候補をユーザのサブグラフ内のアイテムに制約するため、探索的推薦やコールドスタートアイテムを含むシナリオでの効果を大幅に制限します。
Our local pair-wise representation model builds upon this framework, extending it to fit into the heterogeneous, multi-behavioral, and temporal recommendation system context.  
**私たちのローカルペアワイズ表現モデルはこのフレームワークに基づいており、異種、多行動、時間的推薦システムの文脈に適合するように拡張**しています。
Most importantly, we analyze and eliminate its main limitation around locality by extending it with an effective fallback model.  
最も重要なことは、効果的なフォールバックモデルで拡張することによって、局所性に関する主な制限を分析し、排除することです。

While the vast majority of related work focuses on modeling recommendation systems on static graphs, recently multiple benchmarks for temporal recommendation have appeared, such as the Temporal Graph Benchmark (Huang et al., 2023) and RelBench (Robinson et al., 2024).  
関連研究の大多数は静的グラフ上での推薦システムのモデル化に焦点を当てていますが、最近、Temporal Graph Benchmark（Huang et al., 2023）やRelBench（Robinson et al., 2024）など、時間的推薦のための複数のベンチマークが登場しています。
In this work, we adapt the temporal formulation of a recommender systems task and extensively evaluate ContextGNN in the practical setting of RelBench and show that our method significantly outperforms previous approaches.  
本研究では、推薦システムタスクの時間的定式化を適応し、RelBenchの実際の設定でContextGNNを広範に評価し、私たちの手法が以前のアプローチを大幅に上回ることを示します。

<!-- ここまで読んだ! -->

## Temporal Recommendations and Where to Find Them 

We formulate the temporal recommendation problem on a heterogeneous graph snapshot $G^{(-\infty,T]} = (V, E, \phi, \psi)$.
時間的推薦問題を、**異種グラフのスナップショット $G^{(-\infty,T]} = (V, E, \phi, \psi)$ で定式化**します。(グラフってこう定式化するのか〜:thinking:)
The result show that our proposed approaches are efficient and effective in various real-world recommendation problems.
ノードセット $V$ とエッジセット $E \subseteq V \times V$ で構成され、各ノード $v \in V$ はノードタイプ $\phi(v)$ に属し、各エッジ $e \in E$ はエッジタイプ $\psi(e)$ に属します。
We refer to $L \subset V$ as the user set and $R \subset V$ as the item set within our heterogeneous graph.
ユーザセットを $L \subset V$、アイテムセットを $R \subset V$ と呼びます。
The task is then to predict a set of ground-truth items $Y_{v}^{(T,T+i]} \subseteq R$, for which there occurred a link for the user $v \in L$ in the time interval $(T,T+i]$ for a given interval size $i$.
次に、タスクは、ユーザ $v \in L$ に対して、与えられた間隔サイズ $i$ の時間間隔 $(T,T+i]$ においてリンクが発生した、真のアイテムのセット $Y_{v}^{(T,T+i]} \subseteq R$ を予測することです。
(i.e. next-item predictionタスクね...!:thinking:)
When making the prediction, the model only has access to historical information up to timestamp $T$.
予測を行う際、モデルはタイムスタンプ $T$ までの履歴情報にのみアクセスできます。

In the simplest case, $G^{(-\infty,T]}$ is given as a bipartite graph, with node set $V = L \cup R$, and a single edge type $|\{\psi(e):e\in E\}|=1$.
最も単純な場合、$G^{(-\infty,T]}$ は**二部グラフ**として与えられ、ノードセット $V = L \cup R$ と単一のエッジタイプ $|\{\psi(e):e\in E\}|=1$ です。
However, the generalization to heterogeneous graphs allows to incorporate other node types, but most importantly, different edge types of user behaviors (e.g., click, tag-as-favorite, add-to-cart) which offer complementary signals for predicting the target behavior (e.g., purchase) (Xia et al., 2022).
しかし、異種グラフへの一般化により、他のノードタイプを組み込むことが可能になり、**特に、ターゲット行動（例：購入）を予測するための補完的な信号を提供するユーザ行動の異なるエッジタイプ（例：クリック、お気に入りにタグ付け、カートに追加）を含めることができます**（Xia et al., 2022）。
Nodes and edges may be (partially) annotated with an initial feature representation, e.g. $h^{(0)}_{v} \in \mathbb{R}^{d}, v \in V$, and with a timestamp indicating their appearance (or disappearance).
ノードとエッジは、初期の特徴表現（例：$h^{(0)}_{v} \in \mathbb{R}^{d}, v \in V$）で部分的に注釈され、出現（または消失）を示すタイムスタンプが付与される場合があります。
In the absence of timestamps, the given framework can be easily transformed into a static link prediction problem, as commonly practiced in literature (Kipf & Welling, 2016; Wang et al., 2019; He et al., 2020).
**タイムスタンプがない場合、与えられたフレームワークは、文献で一般的に行われているように、静的リンク予測問題に簡単に変換**できます（Kipf & Welling, 2016; Wang et al., 2019; He et al., 2020）。
However, this approach disregards critical information, such as the recency of past activity.
しかし、このアプローチは、過去の活動の新しさなどの重要な情報を無視します。
Note that the given framework also allows newly appearing users and items over time.
**与えられたフレームワークは、時間の経過とともに新たに現れるユーザやアイテムも許可します**。(まあこれは必須だよね...:thinking:)
However, for simplicity of notation, we assume them to be in $\mathcal{L}$ and $\mathcal{R}$ at all times.
ただし、表記の簡潔さのために、常に $L$ と $R$ に存在すると仮定します。

<!-- ここまで読んだ! -->

### Locality Score.

Developing machine learning solutions for recommendation systems is inherently challenging due to the complex patterns of human behavior (He et al., 2023).
推薦システムのための機械学習ソリューションの開発は、人間の行動の複雑なパターンのために本質的に困難です（He et al., 2023）。
Users vary significantly in preferences; some are explorers who constantly seek new experiences, while others are repeaters who prefer familiarity.
ユーザは好みにおいて大きく異なります。あるユーザは常に新しい体験を求める探検者であり、他のユーザは親しみやすさを好むリピーターです。
Such characteristics are especially noticeable across different datasets, e.g., it is more likely that a user repeats a previous purchase than that the user rates the same movie twice.
このような特性は、異なるデータセット間で特に顕著です。例えば、ユーザが以前の購入を繰り返す可能性が高いのは、同じ映画を二度評価するよりも高いです。
To understand these effects better, we introduce the locality score, which measures the fraction of ground-truth links that fall within the $k$-hop neighborhood $\mathcal{N}_{k}^{(-\infty,T]}(v)$ of the subgraph centered around a user $v \in \mathcal{L}$ up to timestamp $T$:
これらの効果をよりよく理解するために、私たちは **locality score を導入**します。これは、ユーザ $v \in L$ を中心としたサブグラフの $k$-ホップ近傍 $N_{k}^{(-\infty,T]}(v)$ 内にある真のリンクの割合を測定します。

$$
s_{k}^{(T, T+i]} = \frac{1}{|L|} 
\sum_{v \in L} \frac{N_{k}^{(-\infty,T]}(v) \cap R \cap Y_{v}^{(T,T+i]}}{|Y_{v}^{(T,T+i]}|}

\tag{1}
$$


Intuitively, the locality score quantifies how many of its future ground-truth items are local to a user.
**直感的には、locality score は、ユーザにとって将来の真のアイテムがどれだけローカルであるか**を定量化します。
Depending on the subgraph depth $k$, the score reflects different interaction patterns.
サブグラフの深さ $k$ に応じて、スコアは異なる相互作用パターンを反映します。
For a shallow subgraph ($k=1$), it captures whether the user repeats purchases or has previously interacted with the item through actions like clicks or tagging as favorite.
浅いサブグラフ（$k=1$）の場合、ユーザが購入を繰り返すか、クリックやお気に入りにタグ付けするなどのアクションを通じてアイテムと以前に相互作用したかどうかを捉えます。
As the subgraph depth increases, the score begins to incorporate collaborative filtering signals, such as whether friends have purchased the ground-truth item in the past ($k=2$), or whether the ground-truth item was previously purchased by users that have a similar buying behavior as the user under consideration ($k=3$).
**サブグラフの深さが増すにつれて、スコアは協調フィルタリング信号を取り入れ始めます**。例えば、友人が過去に真のアイテムを購入したかどうか（$k=2$）、または真のアイテムが考慮中のユーザと類似の購買行動を持つユーザによって以前に購入されたかどうか（$k=3$）です。
Note that in practice, it is infeasible to go beyond depth $k=3$ due to scalability concerns.
**実際には、スケーラビリティの懸念から、深さ $k=3$ を超えることは実現不可能であることに注意してください**。

<!-- ここまで読んだ! -->

We evaluate the locality score for varying $k$ on RelBench (Robinson et al., 2024), a relational deep learning (Fey et al., 2024) benchmark that spans a wide variety of real-world recommendation tasks with diverse characteristics (cf. Table 1).
私たちは、さまざまな $k$ に対する locality score を RelBench（Robinson et al., 2024）で評価します。これは、さまざまな特性を持つ実世界の推薦タスクの広範な範囲をカバーする関係深層学習（Fey et al., 2024）ベンチマークです（表1を参照）。
Interestingly, the locality score does not exceed 0.5 on any dataset, indicating that the majority of ground-truth items are entirely exploratory and not covered by any path of length $\leq 3$ in the graph.
**興味深いことに、locality score はどのデータセットでも 0.5 を超えず、ground-truthアイテムの大部分が完全に探索的であり、グラフ内の長さ $\leq 3$ のパスでカバーされていないことを示しています**。(ふーん、基本的には新製品を買ったりするってこと??:thinking:)
However, for $k=1$, we observe high locality scores on rel-hm and rel-stack, suggesting that users tend to frequently repeat clothing purchases or comment multiple times on the same post.
しかし、$k=1$ の場合、rel-hm と rel-stack で高い locality score を観察し、ユーザが衣料品の購入を頻繁に繰り返したり、同じ投稿に対して複数回コメントしたりする傾向があることを示唆しています。
Increasing the subgraph depth generally improves coverage as seen in datasets like rel-amazon.
サブグラフの深さを増すことで、rel-amazon のようなデータセットで見られるように、一般的にカバレッジが向上します。
While users do not usually re-purchase/rate/review the same item twice here, they tend to purchase the same products that “nearby” users bought.
**ここでは、ユーザが通常同じアイテムを二度購入/評価/レビューすることはありませんが、彼らは「近く」のユーザが購入した同じ製品を購入する傾向**があります。(CFが活きそうなケースだね...!:thinking:)
Overall, this observation suggests that while pair-wise representation architectures such as NBFNet (Zhu et al., 2021) are powerful, they often times fail to offer sufficient coverage within their candidate set, decreasing their effectiveness tremendously.
全体として、この観察は、NBFNet（Zhu et al., 2021）などのペアワイズ表現アーキテクチャが強力である一方で、候補セット内で十分なカバレッジを提供できず、その効果を大幅に低下させることが多いことを示唆しています。
This raises an interesting question of how we can leverage the benefits of pair-wise representations, while supporting the modeling of exploratory recommendations without the need for complex multi-stage approaches.
これは、複雑な多段階アプローチを必要とせずに、探索的推薦のモデル化をサポートしながら、ペアワイズ表現の利点をどのように活用できるかという興味深い問題を提起します。

<!-- ここまで読んだ! -->

## Recommendation with Context-based Graph Neural Networks

Next, we describe Context-based Graph Neural Networks (ContextGNNs), which consist of two separate GNN architectures sitting behind the same GNN backbone. 
次に、Context-based Graph Neural Networks（ContextGNN）について説明します。これは、**同じGNNバックボーンの背後にある2つの別々のGNNアーキテクチャ**で構成されています。
ContextGNN fuses both pair-wise representations and two-tower representations into a single architecture, and is thus naturally able to adapt to diverse dataset and task characteristics. 
ContextGNNは、**ペアワイズ表現とtwo-tower表現の両方を単一のアーキテクチャに統合**し、さまざまなデータセットやタスクの特性に自然に適応できるようになっています。
The first model employs pair-wise representations based on the item candidate set given within the local user-centric subgraph (cf. Sec. 4.1). 
最初のモデルは、ローカルユーザー中心のサブグラフ内で与えられたアイテム候補セットに基づくペアワイズ表現を使用します（参照：Sec. 4.1）。
The second model introduces a novel two-tower architecture based on shallow item representations, which is used to predict a ranking for all pairs of users and items outside the user’s subgraph (cf. Sec. 4.2). 
2番目のモデルは、浅いアイテム表現に基づく新しいtwo-towerアーキテクチャを導入し、**ユーザーのサブグラフ外のすべてのユーザとアイテムのペアのランキングを予測するために使用**されます（参照：Sec. 4.2）。
Finally, a user-specific fusion score, produced by an MLP on the user GNN representation, is added to the scores of the pair-wise representation model, which aligns the distinct scores of the two models and captures how exploratory a specific user is, thus given either more or less weight to the respective models (cf. Sec. 4.3). 
最後に、ユーザーGNN表現に対するMLPによって生成された**ユーザー固有の融合スコアがペアワイズ表現モデルのスコアに追加**され、2つのモデルの異なるスコアを整合させ、特定のユーザがどれだけ探索的であるかを捉え、したがって**それぞれのモデルに対してより多くまたは少ない重みを与えます**（参照：Sec. 4.3）。
We go over additional considerations and extensions in Sec. 4.4. 
追加の考慮事項と拡張についてはSec. 4.4で説明します。
An overview of ContextGNN is visualized in Fig. 1. 
ContextGNNの概要は図1に示されています。

![]()
Figure 1: Overview of Context-based Graph Neural Networks. 
図1: Context-based Graph Neural Networksの概要。
CONTEXTGNN utilizes a bidirectional GNNθ to learn user h (2) v and user-specific item representations h (2) w within a user’s local subgraph. 
ContextGNNは、双方向の $GNN_{\theta}$ を利用して、ユーザのローカルサブグラフ内でユーザ表現 $h^{(2)}_{v}$ とユーザ固有のアイテム表現 $h^{(2)}_{w}$ を学習します。
Its message passing scheme is enhanced by additionally propagating shallow item embeddings ww and seed user IDENTICATORθ representations. 
そのメッセージパッシングスキームは、浅いアイテム埋め込み $w_{w}$ とシードユーザのインジケータ $\textsc{Indicator}_{\theta}$ 表現を追加で伝播することによって強化されます。
Afterwards, item scores are produced depending on whether an item situates within a user’s subgraph.
その後、アイテムスコアは、アイテムがユーザのサブグラフ内に位置するかどうかに応じて生成されます。
A user-specific fusion score is learned via an MLPθ to produce the final ranking by offsetting the contributions of local rankings.
ユーザ固有の融合スコアは、$ MLP_{\theta}$ を介して学習され、ローカルランキングの寄与をオフセットすることによって最終的なランキングを生成します。

<!-- ここまで読んだ!  -->

### 4.1 Pair-wise Representations 4.1 ペアワイズ表現

Our local pair-wise representation model builds upon the framework proposed by Zhu et al. (2021), extending it to fit into the heterogeneous, multi-behavioral, and temporal recommendation system context.  
私たちのローカルペアワイズ表現モデルは、Zhu et al.（2021）によって提案されたフレームワークに基づいており、異種、多行動、時間的推薦システムの文脈に適合するように拡張されています。
NBFNet is a path-based method that generalizes the Bellman-Ford algorithm (Baras & Theodorakopoulos, 2010).  
NBFNetは、Bellman-Fordアルゴリズム（Baras & Theodorakopoulos、2010）を一般化したパスベースの手法です。
Rather than learning a pair-wise representation via two independent node representations $\bm{h}^{(k)}_{v}$ and $\bm{h}^{(k)}_{w}$ (i.e. via two independent subgraphs), NBFNet only utilizes the user-specific subgraph, but readouts GNN item representations from it.  
NBFNetは、2つの独立したノード表現 $h^{(k)}_{v}$ と $h^{(k)}_{w}$（すなわち、2つの独立したサブグラフを介して）を通じてペアワイズ表現を学習するのではなく、**ユーザ特有のサブグラフのみを利用し、そこからGNNアイテム表現を読み出します**。
As such, NBFNet abbreviates the pair-wise representation $\bm{h}^{(k)}_{(v,w)}$ via the user-specific item representations $\bm{h}^{(k)}_{w}$.  
そのため、NBFNetはユーザ特有のアイテム表現 $h^{(k)}_{w}$ を介して、ペアワイズ表現 $h^{(k)}_{(v,w)}$ を省略します。
Hence, it captures both knowledge about the item $w$ and the user $v$ in its representation.  
したがって、アイテム $w$ とユーザ $v$ に関する知識の両方をその表現に捉えます。
In order to let the GNN differentiate between the seed user and other users being sampled within the subgraph, an $d$-dimensional Indicator $\text{Indicator}_{\bm{\theta}}$ representation is added to the seed node (You et al., 2021).  
GNNがシードユーザとサブグラフ内でサンプリングされる他のユーザを区別できるように、シードノードに $d$ 次元の指示器 $\text{Indicator}_{\theta}$ 表現が追加されます（You et al., 2021）。
Specifically, our pair-wise representation model then looks as follows:  
具体的に、私たちのペアワイズ表現モデルは次のようになります：

1. Sample a $k$-hop subgraph $\tilde{G} \leftarrow G_{k}^{(-\infty,T]}[v]$ with node set $\tilde{V}$ around user $v \in \mathcal{L}$.  
   1. ユーザー $v \in L$ の周りにノードセット $\tilde{V}$ を持つ **$k$-ホップのサブグラフ** $\tilde{G} \leftarrow G_{k}^{(-\infty,T]}[v]$ をサンプリングします。

2. Add an indicator representation to the user seed node: $\bm{h}_{v}^{(0)} \leftarrow \bm{h}_{v}^{(0)} + \textsc{Indicator}_{\bm{\theta}}$.  
   1. ユーザシードノードにインジケーター表現を追加します：$h_{v}^{(0)} \leftarrow h_{v}^{(0)} + \textsc{Indicator}_{\bm{\theta}}$。

3. Read out both GNN user and item representations at layer $k$: $\bm{h}^{(k)}_{v}, \{\bm{h}^{(k)}_{w}:w \in \mathcal{\tilde{V}} \cap \mathcal{R}\} \leftarrow \textsc{GNN}^{(k)}_{\bm{\theta}}(\mathcal{\tilde{G}}, \bm{H}^{(0)})$.  
   1. レイヤー $k$ でGNNユーザおよびアイテム表現の両方を読み出します：$h^{(k)}_{v}, \{h^{(k)}_{w}:w \in \tilde{V} \cap R\} \leftarrow \textsc{GNN}^{(k)}_{\theta}(\tilde{G}, H^{(0)})$。

4. Compute the final ranking for all items $w \in \mathcal{\tilde{V}} \cap \mathcal{R}$: $y^{(\textrm{pair})}_{(v,w)} \leftarrow \bm{h}^{(k)}_{v} \cdot \bm{h}^{(k)}_{w}$.  
   1. すべてのアイテム $w \in \tilde{V} \cap R$ の最終ランキングを計算します：$y^{(\text{pair})}_{(v,w)} \leftarrow h^{(k)}_{v} \cdot h^{(k)}_{w}$。

In contrast to NBFNet, we read out both the user and item representations from the GNN in order to produce the ranking of local items.  
NBFNetとは対照的に、**私たちはローカルアイテムのランキングを生成するためにGNNからユーザーとアイテムの表現の両方を読み出します**。
This lets the model leverage the full $k$-hop user information, as otherwise user representations are only computed in intermediate GNN layers based on limited subgraph depths.  
これにより、モデルは完全な $k$-ホップユーザー情報を活用できるようになります。さもなければ、ユーザ表現は限られたサブグラフの深さに基づいて中間GNNレイヤーでのみ計算されます。

Further note that sampling a $k$-hop subgraph typically results in a directed computation graph towards the seed node (Fey & Lenssen, 2019).  
さらに、$k$-ホップサブグラフをサンプリングすることは、通常、シードノードに向かう有向計算グラフを生成します（Fey & Lenssen、2019）。
However, to facilitate the extraction of item node representations, the sampled subgraph must be transformed into a bidirectional graph prior to applying the GNN.  
しかし、**アイテムノード表現の抽出を容易にするために、サンプリングされたサブグラフはGNNを適用する前に双方向グラフに変換する必要があります**。(そうなんだ...!:thinking:)
This approach aligns with previous work that decouples the depth and scope of GNNs (Zeng et al., 2021).  
このアプローチは、GNNの深さと範囲を分離する以前の研究（Zeng et al.、2021）と一致します。

This approach proves particularly effective in the context of temporal, heterogeneous graphs, as the GNN naturally learns to integrate multi-behavior signals originating from different edge types.  
**このアプローチは、時間的で異種のグラフの文脈において特に効果的**であり、GNNは異なるエッジタイプから発生する多行動信号を統合することを自然に学習します。
For instance, the pair-wise representation captures all past user-item interactions, such as the recency of the last purchase or whether the item has been previously clicked or tagged.  
例えば、ペアワイズ表現は、最後の購入の最近性やアイテムが以前にクリックされたかタグ付けされたかなど、すべての過去のユーザー-アイテムインタラクションを捉えます。
Despite its expressiveness, this method is also highly efficient, as only a single GNN pass over the user subgraph is required to make predictions for the entire set of related items.  
**その表現力にもかかわらず、この手法は非常に効率的であり、関連するアイテム全体のセットに対して予測を行うためには、ユーザーサブグラフに対して1回のGNNパスのみが必要**です。
Assuming bounded subgraph sizes, training and inference over the full user set can be achieved in $\mathcal{O}(|\mathcal{L}|)$ time, which is in stark contrast to the $\mathcal{O}(|\mathcal{L}| \cdot |\mathcal{R}|)$ complexity required by two-tower models.  
制約されたサブグラフサイズを仮定すると、**全ユーザーセットに対するトレーニングと推論は $O(|L|)$ 時間で達成でき、これはtwo-towerモデルに必要な $O(|L| \cdot |R|)$の複雑さとは対照的**です。(two-towerモデルは全アイテムに対して計算する必要があるからね...!:thinking:)
Moreover, as no shallow embeddings are used, this approach naturally extends to newly appearing users and items over time.  
さらに、浅い埋め込みが使用されないため、**このアプローチは時間の経過とともに新たに現れるユーザーやアイテムに自然に拡張**されます。
Nonetheless, as discussed in Sec. 3, this method alone does not fully address the diverse requirements of modern recommendation systems due to its limited set of potential candidates.  
それにもかかわらず、セクション3で議論したように、この手法だけでは限られた候補のセットのために現代の推薦システムの多様な要件に完全には対応できません。(全部を計算するのは計算量の爆発的に無理だからだっけ??:thinking:)

<!-- ここまで読んだ! -->

### 4.2 Two-Tower Representations 4.2 二塔表現

ContextGNN’s two-tower model ranks all user-item pairs outside the user’s subgraph, serving as an effective fallback mechanism to supplement the pair-wise representations.  
ContextGNNのtwo-towerモデルは、ユーザのサブグラフの外にあるすべてのユーザ-アイテムペアをランク付けし、ペアワイズ表現を補完するための効果的なフォールバックメカニズムとして機能します。
While drawing inspiration from related two-tower architectures (Wang et al., 2019; He et al., 2020), our novel two-tower model enables an efficient integration with pair-wise architectures.  
**関連するtwo-towerアーキテクチャ（Wang et al., 2019; He et al., 2020）からインスピレーションを得ながら**、私たちの新しいtwo-towerモデルはペアワイズアーキテクチャとの効率的な統合を可能にします。
The key innovation in our two-tower model is the use of shallow item representations.  
**私たちのtwo-towerモデルの主要な革新は、浅いアイテム表現の使用**です。
Specifically, we do not deploy a GNN to compute item representations; instead we entirely rely on a shallow embedding matrix $\bm{W} \in \mathbb{R}^{|\mathcal{R}|\times d}$ to learn item representations.  
具体的には、アイテム表現を計算するためにGNNを展開せず、代わりにアイテム表現を学習するために浅い埋め込み行列 $W \in \mathbb{R}^{|R|\times d}$ に完全に依存します。
This design is inspired by multiple key observations:  
この設計は、いくつかの重要な観察に基づいています：

- **Limited information gain from applying a GNN on the item side**.  
  アイテム側にGNNを適用しても得られる情報は限られています。
  Item connections are naturally very dense.  
  アイテムの接続は自然に非常に密です。
  In extreme cases, popular items may receive over 1M interactions (an item is connected to every user that has previously interacted with it).  
  極端な場合、人気のあるアイテムは100万以上のインタラクションを受けることがあります（アイテムは、それに以前にインタラクションしたすべてのユーザに接続されています）。
  This leads to significant challenges and uncertainties in subgraph sampling, and easily exposes the GNN to oversquashing and oversmoothing issues.  
  これにより、サブグラフサンプリングにおいて重大な課題と不確実性が生じ、GNNがオーバースクワッシングやオーバースムージングの問題にさらされやすくなります。

- **Shallow embedding matrices are very effective**.  
  浅い埋め込み行列は非常に効果的です。
  Shallow item embedding matrices can capture key signals such as popularity trends, seasonal patterns, demographic preferences and item similarity just as effectively as a GNN.  
  **浅いアイテム埋め込み行列は、人気のトレンド、季節的なパターン、人口統計的な好み、アイテムの類似性などの重要な信号をGNNと同じくらい効果的にキャッチ**できます。

- **GNN item representations scale poorly during training**.  
  GNNアイテム表現は、トレーニング中にスケールが悪くなります。
  Incorporating both user and item GNN representations limits the model to only use a small number of negative samples due to memory constraints. 
  ユーザとアイテムのGNN表現の両方を組み込むと、メモリ制約のためにモデルは少数のネガティブサンプルしか使用できなくなります。
  In contrast, shallow item embeddings support training against a much larger corpus of negative samples (≈10M), which is critical for improving model performance.  
  対照的に、浅いアイテム埋め込みは、モデルのパフォーマンスを向上させるために重要な、はるかに大きなネガティブサンプルのコーパス（約1000万）に対してトレーニングをサポートします。
  This approach also eliminates the need for complex negative sampling strategies, which are often required when the number of negative samples is limited.
  このアプローチは、ネガティブサンプルの数が限られている場合にしばしば必要とされる複雑なネガティブサンプリング戦略の必要性も排除します。

Importantly, we also inject the shallow item embeddings within the user’s GNN forward pass, such that user representations can better align themselves to the corresponding item representations.  
重要なことに、**私たちはユーザのGNNのフォワードパス内に浅いアイテム埋め込みを注入し、ユーザ表現が対応するアイテム表現によりよく整合できるようにします**。
Hence, the GNN representation of users follows a similar spirit to models such as NGCF (Wang et al., 2019) or LightGCN (He et al., 2020), although we do not utilize shallow user embeddings as the GNN itself is powerful enough to learn its own rich representation without them.  
したがって、ユーザのGNN表現は、NGCF（Wang et al., 2019）やLightGCN（He et al., 2020）などのモデルと同様の精神に従いますが、GNN自体がそれなしで自分の豊かな表現を学習するのに十分強力であるため、浅いユーザ埋め込みは利用しません。
As such, our two-tower representation model can be summarized as follows:  
このようにして、私たちのtwo-tower表現モデルは次のように要約できます：

1. Sample a $k$-hop subgraph $\tilde{G} \leftarrow G_{k}^{(-\infty,T]}[v]$ with node set $\mathcal{\tilde{V}}$ around user $v \in \mathcal{L}$.  
   1. ユーザ $v \in L$ の周りにノードセット $\tilde{V}$ を持つ $k$-ホップサブグラフ $\tilde{G} \leftarrow G_{k}^{(-\infty,T]}[v]$ をサンプリングします。

2. Add the shallow embedding to all sampled items $w \in \mathcal{\tilde{V}} \cap \mathcal{R}$: $\bm{h}_{w}^{(0)} \leftarrow \bm{h}_{w}^{(0)} + \bm{w}_{w}$.  
   1. サンプリングされたすべてのアイテム $w \in \tilde{V} \cap R$ に浅い埋め込みを追加します: $\bm{h}_{w}^{(0)} \leftarrow \bm{h}_{w}^{(0)} + \bm{w}_{w}$。

3. Read out the GNN user representation at layer $k$: $\bm{h}_{v}^{(k)} \leftarrow \textsc{GNN}_{\bm{\theta}}^{(k)}(\tilde{G}, \bm{H}^{(0)})$.  
   1. レイヤー $k$ でのGNNユーザ表現を読み出します: $\bm{h}_{v}^{(k)} \leftarrow \textsc{GNN}_{\bm{\theta}}^{(k)}(\tilde{G}, \bm{H}^{(0)})$。

4. Compute the final ranking for all items $w \in \mathcal{R} \setminus \mathcal{\tilde{V}}$: $y^{(\textrm{tower})}_{(v,w)} \leftarrow \bm{h}^{(k)}_{v} \cdot \bm{w}_{w}$.
   1. すべてのアイテム $w \in R \setminus \tilde{V}$ の最終ランキングを計算します: $y^{(\textrm{tower})}_{(v,w)} \leftarrow \bm{h}^{(k)}_{v} \cdot \bm{w}_{w}$。

<!-- よくわからんかった! ここまで読んだ! -->

### 4.3 Context-based Graph Neural Networks

Our finalContextGNNarchitecture fuses both pair-wise representations and two-tower representations into a single unified architecture.
私たちの最終的なContextGNNアーキテクチャは、ペアワイズ表現とツータワー表現の両方を単一の統一されたアーキテクチャに統合します。
That is, for all items $w \in \tilde{V} \cup \mathcal{R}$ inside the local user subgraph, we leverage the scores $y^{(\textrm{pair})}_{(v,w)}$ obtained from the pair-wise representations, while we fallback to the two-tower scores $y^{(\textrm{tower})}_{(v,w)}$ for all items $w \in \tilde{V} \setminus \mathcal{R}$ outside the sampled subgraph.
つまり、ローカルユーザサブグラフ内のすべてのアイテム $w \in \tilde{V} \cup R$ に対して、ペアワイズ表現から得られたスコア $y^{(\text{pair})}_{(v,w)}$ を利用し、サンプリングされたサブグラフの外にあるすべてのアイテム $w \in \tilde{V} \setminus R$ に対してはツータワースコア $y^{(\text{tower})}_{(v,w)}$ にフォールバックします。

The observation that user behaviors are diverse is the final element that makesContextGNNwork.
**ユーザの行動が多様であるという観察は、ContextGNNが機能するための最終的な要素**です。
To accommodate such diversity across different users,ContextGNNlearns a user-specific fusion score predicted from the GNN’s user embeddings $\bm{h}^{(k)}_{v}$ via an MLP $\textrm{MLP}_{\bm{\theta}}$.
このような異なるユーザ間の多様性に対応するために、ContextGNNは**GNNのユーザ埋め込み $\bm{h}^{(k)}_{v}$ からMLP $\texm{MLP}_{\bm{\theta}}$ を介して予測されるユーザ特有の融合スコア**を学習します。
This personalized fusion score aligns the distinct scores by learning which users prefer familiar items over exploratory purchases, and adjusts the final ranking scores accordingly.
このパーソナライズされた融合スコアは、どのユーザが探索的な購入よりも馴染みのあるアイテムを好むかを学習することによって異なるスコアを整合させ、最終的なランキングスコアをそれに応じて調整します。
With this, the final score is given by
これにより、最終スコアは次のように与えられます。

$$

y_{(y, w)} = \begin{matrix}
  % もしアイテムwがユーザのさぶグラフにある場合...
  y^{(\text{pair})}_{(v,w)} + MLP_{\theta}(h_{v}^{k}) & \text{if } w \in \tilde{V} \cap R \\
  % そうでない場合...
  y^{(\text{tower})}_{(v,w)} & \text{otherwise} 
$$

InContextGNN, both pair-wise representations and two-tower representations are derived from thesameGNN backbone.
ContextGNNでは、ペアワイズ表現とツータワー表現の両方が同じGNNバックボーンから導出されます。
Since both models depend solely on the user subgraph, the user embedding $\bm{h}^{(k)}_{v}$ can be extracted in a single GNN forward pass and leveraged for downstream uses in both models.
**両方のモデルがユーザサブグラフのみに依存しているため**、ユーザ埋め込み $\bm{h}^{(k)}_{v}$ は単一のGNNフォワードパスで抽出され、両方のモデルで下流の使用に活用されます。
This streamlined approach makesContextGNNcomputationally very efficient.
この合理化されたアプローチにより、**ContextGNNは計算的に非常に効率的**になります。
ContextGNNis then trained end-to-end, optimizing both types of item scores as well as the fusion score altogether to maximize the predictive performance of future user-item interactions.
次に、**ContextGNNはエンドツーエンドでトレーニングされ**、両方のタイプのアイテムスコアと融合スコアを最適化して、将来のユーザ-アイテムインタラクションの予測性能を最大化します。
In practice, we utilize the cross entropy loss for optimization, although any other loss formulation is applicable as well (Rendle et al., 2009).
**実際には、最適化のためにクロスエントロピー損失を利用しますが、他の損失の定式化も適用可能です（Rendle et al., 2009）。**(勾配ベースの学習とかも全然できそう...!:thinking:)
During inference, we obtain top scores from the two-tower model via (approximate) maximum inner product search (Johnson et al., 2019), and merge them to the pair-wise scores in a post-processing procedure.
**推論中、私たちはツータワーモデルから（近似的な）最大内積検索（Johnson et al., 2019）を介してトップスコアを取得し、ポストプロセッシング手順でペアワイズスコアに統合**します。(ふむふむ...!:thinking:)

<!-- ここまで読んだ! -->

### 4.4 Extensions 拡張

We go over additional considerations and extensions when applying ContextGNNs in practice.  
ContextGNNsを実際に適用する際の追加の考慮事項と拡張について説明します。

#### Fitting into the Context of Relational Deep Learning. 関係深層学習の文脈への適合

ContextGNNs nicely align with the framework of relational deep learning (Fey et al., 2024), a blueprint for graph representation learning on relational databases.  
ContextGNNは、関係データベースにおけるグラフ表現学習のための青写真である関係深層学習（Fey et al., 2024）のフレームワークと適切に整合します。
Specifically, relational deep learning treats relational databases as a heterogeneous temporal graph, in which dimension and fact tables are linked through primary-foreign key relationships.  
具体的には、関係深層学習は関係データベースを異種の時間的グラフとして扱い、次元テーブルとファクトテーブルは主キーと外部キーの関係を通じてリンクされています。
Then, temporal-aware subgraph sampling is employed to generate heterogeneous subgraph snapshots $\mathcal{G}_{k}^{(-\infty,T]}[v]$ up to timestamp $T$, which are used to predict future user-item interactions.  
次に、時間に配慮したサブグラフサンプリングが使用され、タイムスタンプ $T$ までの異種サブグラフスナップショット $\mathcal{G}_{k}^{(-\infty,T]}[v]$ が生成され、これが将来のユーザとアイテムの相互作用を予測するために使用されます。
Relational databases (Robinson et al., 2024) comprise diverse set of tables with rich multi-modal input features and rich multi-behavioral, temporal interactions, making them the perfect setting for stress-testing ContextGNNs.  
関係データベース（Robinson et al., 2024）は、多様なテーブルのセットを含み、豊富なマルチモーダル入力特徴と多様な行動的・時間的相互作用を持っているため、ContextGNNをストレステストするのに最適な環境を提供します。

<!-- ここまで読んだ! -->

#### Transductive vs. Inductive Modeling. 

- ざっくりイメージメモ:thinking:
  - Transductive: 学習に使ってないアイテムは予測できない!
  - Inductive: 学習に使ってないアイテムも予測できる!

Although the pair-wise representations in ContextGNN are inductive by design, the usage of the shallow embedding matrix on the item side places it in a transductive setting.  
ContextGNNのペアワイズ表現は設計上インダクティブですが、アイテム側での浅い埋め込み行列の使用により、トランスダクティブな設定に置かれます。
This means that while ContextGNN can naturally accommodate newly appearing users over time, it is unable to handle new items at prediction time since their shallow embeddings remain uninitialized.  
これは、ContextGNNが時間の経過とともに新たに現れるユーザを自然に受け入れることができる一方で、予測時に新しいアイテムを処理できないことを意味します。なぜなら、それらの浅い埋め込みは初期化されていないからです。
To enable ContextGNN to operate in an inductive setting, we propose to replace the shallow item embedding matrix with a deep neural network on top of its item input features $\bm{h}^{(0)}_{w}$.  
ContextGNNがインダクティブな設定で動作できるようにするために、アイテム入力特徴 $\bm{h}^{(0)}_{w}$ の上に深層ニューラルネットワークを置くことで、浅いアイテム埋め込み行列を置き換えることを提案します。
This approach allows ContextGNN to scale to tasks such as marketplace or event recommendation, where handling of new items is essential.  
**このアプローチにより、ContextGNNは新しいアイテムの処理が不可欠なマーケットプレイスやイベント推薦などのタスクにスケールすることが可能になります。**

<!-- ここまで読んだ! -->

#### Sampled Softmax Formulation.   サンプリングソフトマックスの定式化

Since it is infeasible to train against the full item set $\mathcal{R}$ when optimizing ContextGNNs, in practice, we rely on a sampled softmax formulation.  
ContextGNNを最適化する際に全アイテムセット $R$ に対してトレーニングすることは不可能であるため、実際にはサンプリングソフトマックスの定式化に依存します。
This basically converts the objective of ContextGNN into a classification problem with $C$ sampled classes, shared across the entire mini-batch.  
これは基本的に、**ContextGNNの目的関数を全ミニバッチで共有される $C$ のサンプリングクラスを持つ分類問題に変換します**。(これは学習方法で回帰ベースのアプローチを採用した場合に、negativeサンプルをどう用意するねん、みたいな話??:thinking:)
The utilized sampling procedure is based on a priority queue: we ensure that (1) all ground-truth items and (2) the union of sampled subgraph items of a given mini-batch are included in the set of classes.  
使用されるサンプリング手順は優先度キューに基づいています：私たちは（1）すべての真のアイテムと（2）特定のミニバッチのサンプリングされたサブグラフアイテムの和集合がクラスのセットに含まれることを保証します。
Then, we (3) fill up the remainder of items with unexplored items outside all subgraphs of the mini-batch based on a uniform sampling procedure.  
次に、（3）均一なサンプリング手順に基づいて、ミニバッチのすべてのサブグラフの外にある未探索のアイテムで残りのアイテムを埋めます。
In practice, we have no issues to scale the number of classes $C$ to $\approx 1M$ on commodity GPUs (15GB of memory), giving ContextGNN rich signals to learn from.  
実際には、一般的なGPU（15GBのメモリ）上でクラスの数 $C$ を $\approx 1M$ にスケールすることに問題はなく、ContextGNNに学習するための豊富な信号を提供します。

<!-- ここまで読んだ! -->

## 5 Experimental Evaluation 実験評価

We perform experiments on six diverse datasets stemming from different domains, including ten different recommendation tasks.  
私たちは、異なるドメインからの6つの多様なデータセットを用いて実験を行い、10の異なる推薦タスクを含みます。

We aim to answer the following research questions:  
以下の研究質問に答えることを目指します：

- Q1: Which benefits does ContextGNN provide over each of its individual component?  
ContextGNNは、それぞれの個別のコンポーネントに対してどのような利点を提供しますか？

- Q2: How does ContextGNN perform against state-of-the-art recommendation system methods?  
ContextGNNは、最先端の推薦システム手法に対してどのようにパフォーマンスを発揮しますか？

- Q3: How does the locality score of Sec. 3 influence the model performance of ContextGNN?  
セクション3の局所性スコアは、ContextGNNのモデルパフォーマンスにどのように影響しますか？

- Q4: How efficient and scalable is ContextGNN compared to the related work?  
ContextGNNは、関連研究と比較してどの程度効率的でスケーラブルですか？

Our method Source code: https://github.com/kumo-ai/ContextGNN is implemented in PyTorch (Paszke et al., 2019) utilizing the PyTorch Geometric (Fey & Lenssen, 2019) and PyTorch Frame (Hu et al., 2024) libraries.  
私たちの手法は、PyTorch（Paszke et al., 2019）を使用して実装されており、PyTorch Geometric（Fey & Lenssen, 2019）およびPyTorch Frame（Hu et al., 2024）ライブラリを利用しています。

### 5.1 Relational Deep Learning リレーショナル深層学習

#### Dataset Description. データセットの説明

We utilize the recommendation tasks introduced in RelBench (Robinson et al., 2024), which consists of eight different realistic and temporal-aware recommendation tasks. 
私たちは、RelBench（Robinson et al., 2024）で紹介された推薦タスクを利用します。これは、**8つの異なる現実的かつ時間に配慮した推薦タスク**で構成されています。
RelBench datasets contain rich relational structure, providing a challenging environment for recommendation tasks. 
RelBenchデータセットは豊富なリレーショナル構造を含んでおり、推薦タスクにとって挑戦的な環境を提供します。
To achieve strong performance, methods must be able to leverage information across multiple relational tables. 
強力なパフォーマンスを達成するためには、手法が複数のリレーショナルテーブル間の情報を活用できる必要があります。
All datasets are publicly accessible and vary in terms of domain, size, and sparsity. 
すべてのデータセットは公開されており、ドメイン、サイズ、およびスパース性の点で異なります。
The task is to predict the top-k items given a user at a given seed time. 
タスクは、**特定のシード時間におけるユーザに対してトップkアイテムを予測すること**です。
The metric we use is Mean Average Precision (MAP)@k, where k is set per task (higher is better). 
私たちが使用する指標はMean Average Precision (MAP)@kであり、kはタスクごとに設定されます（高い方が良い）。

#### Experimental Protocols.  実験プロトコル

We compare ContextGNN to the following baseline methods: 
私たちはContextGNNを以下のベースライン手法と比較します：

- LightGBM (Ke et al., 2017) concatenates both user and item features, and feeds them into a LightGBM decision tree. 
  LightGBM（Ke et al., 2017）は、ユーザとアイテムの特徴を連結し、それをLightGBM決定木に入力します。

- MultiVAE (Liang et al., 2018) extends variational autoencoders to collaborative filtering via a user-item interaction matrix for implicit feedback. 
  MultiVAE（Liang et al., 2018）は、ユーザ-アイテム相互作用行列を介して協調フィルタリングに変分オートエンコーダを拡張します。

- GraphSAGE (Hamilton et al., 2017) employs a heterogeneous GNN on both user and item side, and ranks the produced embeddings via an inner product decoder. 
  GraphSAGE（Hamilton et al., 2017）は、ユーザとアイテムの両方に対して異種GNNを使用し、生成された埋め込みを内積デコーダを介してランク付けします。

- NGCF (Wang et al., 2019) extends GraphSAGE by propagating both shallow user and item embeddings inside the GNN. 
  NGCF（Wang et al., 2019）は、GNN内で浅いユーザとアイテムの埋め込みの両方を伝播させることによってGraphSAGEを拡張します。

- NBFNet (Zhu et al., 2021) employs pair-wise GNN representations. This is the backbone of our pair-wise representation model in ContextGNN. 
  NBFNet（Zhu et al., 2021）は、ペアワイズGNN表現を使用します。これは、ContextGNNにおけるペアワイズ表現モデルのバックボーンです。

- ShallowItem describes our two-tower model in ContextGNN, which ranks user GNN representations and shallow item embeddings via an inner product decoder. 
  ShallowItemは、ContextGNNにおける私たちの2タワーモデルを説明し、ユーザGNN表現と浅いアイテム埋め込みを内積デコーダを介してランク付けします。

Importantly, all GNN-based models utilize the same GNN backbone, which guarantees fair comparison of training procedures that are agnostic to the underlying model implementation. 
**重要なことに、すべてのGNNベースのモデルは同じGNNバックボーンを利用しており、基盤となるモデル実装に依存しないトレーニング手順の公正な比較を保証します**。(モデルアーキテクチャと入力データは全部同じってことか:thinking:)
Specifically, we use a heterogeneous GraphSAGE variant as introduced in Robinson et al. (2024), which leverages a ResNet tabular model (Gorishniy et al., 2021) to encode multi-modal input data into a shared embedding space, which then gets fed into a heterogeneous GraphSAGE variant (Hamilton et al., 2017) with sum-based neighbor aggregation. 
具体的には、Robinson et al.（2024）で紹介された異種GraphSAGEのバリアントを使用し、ResNetタブularモデル（Gorishniy et al., 2021）を活用してマルチモーダル入力データを共有埋め込み空間にエンコードし、その後、合計ベースの隣接集約を持つ異種GraphSAGEバリアント（Hamilton et al., 2017）に入力します。
For all experiments, optimization is done via Adam (Kingma & Ba, 2015) for a maximum of 20 epochs. 
すべての実験では、**最適化はAdam（Kingma & Ba, 2015）を介して最大20エポック**で行われます。
The hyper-parameters we tune for each task are: (1) the number of hidden units ∈ {32, 64, 128, 256, 512}, (2) the batch size ∈ {256, 512, 1024}, and (3) the learning rate ∈ {0.001, 0.01}. 
各タスクに対して調整するハイパーパラメータは次のとおりです：（1）隠れユニットの数 ∈ {32, 64, 128, 256, 512}、（2）バッチサイズ ∈ {256, 512, 1024}、および（3）学習率 ∈ {0.001, 0.01}。

<!-- ここまで読んだ! -->


#### Discussion.

The results are reported in Table 2. 
結果は表2に示されています。
We answer Q1 by comparing ContextGNN to its individual components NBFNet and ShallowItem, and answer Q2 by relating ContextGNN’s performance to all reported baselines. 
私たちは、ContextGNNをその個々のコンポーネントであるNBFNetとShallowItemと比較することでQ1に答え、ContextGNNのパフォーマンスをすべての報告されたベースラインに関連付けることでQ2に答えます。

ContextGNN outperforms all competing baselines, often by very significant margins. 
ContextGNNはすべての競合ベースラインを上回り、しばしば非常に大きな差で勝っています。
Notably, one can observe that the two-tower models MultiVAE, GraphSAGE and NGCF all fail to capture the pair-wise signals that both NBFNet and ContextGNN are able to leverage. 
特に、**2タワーモデルであるMultiVAE、GraphSAGE、NGCFは、NBFNetとContextGNNの両方が活用できるペアワイズ信号を捉えることができないこと**が観察されます。
This shows that two-tower representations are not powerful enough to capture the fine-grained pair-wise dependencies that are required to solve these tasks with high precision. 
これは、**2タワー表現がこれらのタスクを高精度で解決するために必要な細かいペアワイズ依存関係を捉えるには十分な力を持っていないこと**を示しています。
Among the two-tower GNN models, there is no clear winner between GraphSAGE and NGCF, indicating that shallow (user) embeddings do not significantly drive improvements (and may even hinder performance, especially in tasks with inherent temporal dynamics). 
2タワーGNNモデルの中で、GraphSAGEとNGCFの間に明確な勝者はおらず、浅い（ユーザ）埋め込みが改善を大きく促進しないこと（特に内在的な時間的ダイナミクスを持つタスクではパフォーマンスを妨げる可能性があること）を示しています。
ContextGNN improves results by 344% on average compared to the best two-tower baseline. 
ContextGNNは、最良の2タワーベースラインと比較して平均344%の結果改善を達成します。

Among the baselines, NBFNet performs the best across all tasks, while ContextGNN can consistently improve upon these strong outcomes. 
ベースラインの中で、NBFNetはすべてのタスクで最も良いパフォーマンスを発揮し、ContextGNNはこれらの強力な結果を一貫して改善できます。
On average, ContextGNN increases performance by 20% compared to NBFNet, underscoring the importance of incorporating “distant” items into the ranking process - an aspect that NBFNet overlooks by design. 
平均して、**ContextGNNはNBFNetと比較して20%のパフォーマンス向上を実現し、「遠くの」アイテムをランキングプロセスに組み込む重要性を強調**します。これは、NBFNetが設計上見落としている側面です。

Our own two-tower ShallowItem model performs comparably to other two-tower GNN baselines, despite only using shallow item information in order to improve the overall efficiency of the model. 
私たち自身の2タワーShallowItemモデルは、モデルの全体的な効率を向上させるために浅いアイテム情報のみを使用しているにもかかわらず、他の2タワーGNNベースラインと同等のパフォーマンスを発揮します。
This supports the hypothesis that a deep GNN on the item side is not particularly useful on most tasks, as the shallow embeddings can capture most of the key signals on the item side just as well as the GNN. 
これは、**アイテム側の深いGNNがほとんどのタスクで特に有用ではないという仮説**を支持します。浅い埋め込みは、GNNと同様にアイテム側の主要な信号のほとんどを捉えることができます。
However, there exists specific cases such as the condition-sponsor-run task on the rel-trial dataset, where ShallowItem underperforms relative to GraphSAGE and NGCF. 
しかし、rel-trialデータセットのcondition-sponsor-runタスクのような特定のケースでは、ShallowItemがGraphSAGEやNGCFに対して劣ることがあります。
On this task, deep GNNs on the item side play indeed a crucial role to improve results of two-tower models, which is captured in ContextGNN through its pair-wise representation model. 
このタスクでは、アイテム側の深いGNNが2タワーモデルの結果を改善するために重要な役割を果たし、これはContextGNNのペアワイズ表現モデルを通じて捉えられています。

The most noteworthy result is seen in the site-sponsor-run task on the rel-trial dataset. 
最も注目すべき結果は、rel-trialデータセットのsite-sponsor-runタスクで見られます。
Here, both pair-wise models and two-tower models achieve strong initial results. 
ここでは、**ペアワイズモデルと2タワーモデルの両方が強力な初期結果を達成**します。
Combining these two paradigms together via ContextGNN improves the final performance by ≈ 100%, indicating that each of the individual components of ContextGNN captures orthogonal signals. 
ContextGNNを介してこれら2つのパラダイムを組み合わせることで、最終的なパフォーマンスが約100%向上し、ContextGNNの各個別コンポーネントが直交信号を捉えていることを示しています。
The fusion of these paradigms yields a ranking model that excels in both local and distant item ranking, achieving superior overall performance. 
**two-towerモデルとペアワイズモデルのパラダイムの融合**は、ローカルおよび遠方のアイテムランキングの両方で優れたランキングモデルを生み出し、全体的なパフォーマンスを向上させます。

<!-- ここまで読んだ! -->

In order to answer Q3, we now analyze the relationship between the locality scores $s_{k}^{[T,T+i)}$ and the performance of ContextGNN. 
Q3に答えるために、私たちは現在、局所性スコア $s_{k}^{[T,T+i)}$ とContextGNNのパフォーマンスとの関係を分析します。
We observe that the improvements of ContextGNN compared to NBFNet are notably higher on tasks with lower locality scores. 
**ContextGNNのNBFNetに対する改善は、局所性スコアが低いタスクで顕著に高い**ことが観察されます。
This observation aligns intuitively, as ContextGNN needs to rely more heavily on its two-tower component during optimization when locality scores are lower. 
この観察は直感的に一致しており、局所性スコアが低いときにContextGNNは最適化中にその2タワーコンポーネントにより依存する必要があります。
Specifically, in tasks with the lowest locality scores (e.g., 0.168, 0.170 and 0.229 on the user-item-purchase, user-item-rate and site-sponsor-run tasks from the rel-amazon and rel-trial datasets), ContextGNN achieves substantial performance gains of 42% to 80% compared to NBFNet. 
具体的には、最低の局所性スコア（例：rel-amazonおよびrel-trialデータセットのuser-item-purchase、user-item-rate、site-sponsor-runタスクでの0.168、0.170、0.229）を持つタスクでは、ContextGNNはNBFNetに対して42%から80%の大幅なパフォーマンス向上を達成します。
Conversely, for tasks with higher locality scores (e.g., 0.417, 0.298, and 0.280 on the user-item-purchase, user-post-comment, and post-post-related tasks from the rel-hm and rel-stack datasets), the performance improvements of ContextGNN over NBFNet are more modest, ranging from 3% to 5%. 
逆に、局所性スコアが高いタスク（例：rel-hmおよびrel-stackデータセットのuser-item-purchase、user-post-comment、post-post-relatedタスクでの0.417、0.298、0.280）では、ContextGNNのNBFNetに対するパフォーマンス向上はより控えめで、3%から5%の範囲です。
These findings underscore the significant impact of the locality score on the performance of NBFNet, whereas ContextGNN demonstrates robustness, achieving stellar performance improvements regardless of task-specific characteristics. 
これらの発見は、NBFNetのパフォーマンスに対する局所性スコアの重要な影響を強調し、一方で**ContextGNNは堅牢性を示し、タスク特有の特性に関係なく優れたパフォーマンス向上を達成**します。

<!-- ここまで読んだ! -->

### 5.2 Static Link Prediction 静的リンク予測

While ContextGNN’s main focus is to excel on large-scale real-world use-cases which are temporal and heterogeneous, it can also be used in a plug-and-play fashion for any link prediction task.  
ContextGNNの主な焦点は、時間的かつ異種の大規模な実世界のユースケースで優れた性能を発揮することですが、任意のリンク予測タスクに対してプラグアンドプレイ方式で使用することもできます。
To verify, we evaluate ContextGNN on the static link prediction task of Amazon-Book (Wang et al., 2019), which is a small-scale dataset of 52,643 users and 91,599 items, which does not come with input features, only considers users with at least ten interactions, and evaluates on 10% of randomly selected interactions independent of time, cf. Table 3.  
これを検証するために、私たちはContextGNNをAmazon-Book（Wang et al., 2019）の静的リンク予測タスクで評価します。これは、52,643人のユーザと91,599アイテムからなる小規模なデータセットで、入力特徴はなく、少なくとも10回のインタラクションを持つユーザのみを考慮し、時間に依存しないランダムに選択されたインタラクションの10%で評価します（表3を参照）。
We can see that ContextGNN is able to outperform both NGCF and LightGCN, while it is slightly underperforming compared to, e.g., UltraGCN or LightGCL.  
ContextGNNは、NGCFおよびLightGCNの両方を上回る性能を発揮できることがわかりますが、例えばUltraGCNやLightGCLと比較するとやや劣っています。
Given the relatively small size of this dataset, much of the progress in GNN-based recommendation systems has centered on two key directions: (1) simplifying GNN architectures, and (2) incorporating self-supervised learning techniques.  
このデータセットの比較的小さなサイズを考慮すると、**GNNベースの推薦システムにおける進展の多くは、2つの主要な方向に集中しています：（1）GNNアーキテクチャの簡素化、（2）自己教師あり学習技術の組み込み**です。
Exploring how ContextGNN can benefit from a more lightweight GNN backbone or complementary learning signals presents an exciting direction for future research.  
ContextGNNがより軽量なGNNバックボーンや補完的な学習信号からどのように利益を得ることができるかを探ることは、今後の研究にとって興味深い方向性を示しています。

<!-- ここまで読んだ! -->

### 5.3 Temporal Next-Item Prediction

(Sequential recommendationのデータセットを使ってオフライン評価してみたよ、って話?)

We use ContextGNN to perform temporal next-item recommendation on the IJCAI Contest dataset (Xia et al., 2022), which is a common dataset to evaluate sequential recommendation models et al. (Sun et al., 2019; Xia et al., 2020; 2022).
私たちは、IJCAIコンテストデータセット（Xia et al., 2022）において、ContextGNNを使用して時間的次アイテム推薦を行います。このデータセットは、逐次推薦モデルを評価するための一般的なデータセットです（Sun et al., 2019; Xia et al., 2020; 2022）。
As per evaluation protocol, we report HitRate@k and NDCG@k over 99 sampled negatives per entity.
評価プロトコルに従い、各エンティティに対して99のサンプルネガティブに対するHitRate@kとNDCG@kを報告します。
Notably, ContextGNN excels at incorporating multi-behavioral and temporal signal, cf. Table 4.
特に、ContextGNNは多様な行動と時間的信号を取り入れるのに優れており、表4を参照してください。
We observe that ContextGNN is able to out-perform all baselines on all metrics on this task (e.g., 170% improvement on HitRate@1).
私たちは、ContextGNNがこのタスクのすべての指標で全てのベースラインを上回ることができることを観察しました（例：HitRate@1で170%の改善）。

### 5.4 Efficiency Analysis 効率分析

(計算効率の話! two-towerモデルと比べてどうなのよ! これは運用する上で重要だよなぁ...)

Our hybrid ContextGNN model is designed in such a way to have minimal overhead compared to its two components in isolation since the vast majority of the model parts are shared between the two paradigms.  
私たちのハイブリッドContextGNNモデルは、**二つのコンポーネントを単独で使用する場合と比較して、最小限のオーバーヘッドを持つように設計**されています。これは、モデルの大部分の部分が二つのパラダイム間で共有されているためです。
To answer Q4, we report the runtime in seconds to reach 1,000 optimization steps across different models, cf. Table 5.  
Q4に答えるために、異なるモデルで1,000回の最適化ステップに到達するための実行時間を秒単位で報告します（表5を参照）。
Most importantly, since ContextGNN only requires a single GNN forward pass, it is faster compared to any two-tower GNN by a very significant factor (i.e., a two-tower GNN such as GraphSAGE requires to run the GNN on both positive and negative items).  
**最も重要なのは、ContextGNNは単一のGNNフォワードパスのみを必要とするため、任意の二塔GNNと比較して非常に大きな要因で速くなります**（つまり、GraphSAGEのような二塔GNNは、正のアイテムと負のアイテムの両方でGNNを実行する必要があります）。
In particular, two-tower GNNs scale very poorly when increasing the number of negative samples to train against.  
特に、二塔GNNは、トレーニングに対して負のサンプルの数を増やすと、非常にスケールが悪くなります。
For training recommendation systems, a large number of negative examples is important to allow learning of discriminative features.  
推薦システムのトレーニングにおいては、大量の負の例が、識別的特徴の学習を可能にするために重要です。
However, in the simplest case (one negative pair per positive pair), a two-tower GNN needs to be executed three times already.  
しかし、**最も単純なケース（正のペアごとに1つの負のペア）では、二塔GNNはすでに3回実行する必要があります**。(2回じゃなくて?? ユーザタワー1回、アイテムタワー2回ってこと??:thinking:)
ContextGNN does not have this limitation and can consider up to 1M negatives before running into GPU memory limitations.  
ContextGNNはこの制限がなく、GPUメモリの制限に達する前に最大1Mの負のサンプルを考慮することができます。

## 6Conclusion 結論

We presented a novel hybrid GNN pipeline for recommendation called ContextGNN that can effectively contextualize predictions via pair-wise representations for familiar items, while falling back to two-tower representations for exploratory and serendipitous items. 
私たちは、ContextGNNと呼ばれる推薦のための新しいハイブリッドGNNパイプラインを提案しました。このパイプラインは、馴染みのあるアイテムに対してペアワイズ表現を通じて予測を効果的に文脈化し、探索的および偶然のアイテムに対しては二塔表現に戻ることができます。
We evaluated our architecture on real-world datasets on which it consistently improved upon the state-of-the-art. 
私たちは、実世界のデータセットでアーキテクチャを評価し、常に最先端の技術を上回る改善を示しました。

<!-- ここまで読んだ! -->

#### Acknowledgments 謝辞

We thank the entire Kumo.AI team for their invaluable support in bringing Hybrid-GNN into production for over dozens of customers and for any dataset scale. 
私たちは、数十の顧客に対してHybrid-GNNを製品化するための貴重なサポートを提供してくれたKumo.AIチーム全体に感謝します。また、あらゆるデータセットのスケールに対しても感謝します。
Special thanks go to Amitabha Roy, Myungwhan Kim and Federico Reyes Gómez for helpful discussions and feedback. 
特に、役立つ議論とフィードバックを提供してくれたAmitabha Roy、Myungwhan Kim、Federico Reyes Gómezに感謝します。

<!-- ここまで読んだ! -->
