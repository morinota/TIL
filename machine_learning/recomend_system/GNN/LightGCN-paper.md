refs: https://arxiv.org/pdf/2002.02126


タイトル: LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation  LightGCN: 推薦のためのグラフ畳み込みネットワークの簡素化と強化  

## 1. ABSTRACT  

Graph Convolution Network (GCN) has become new state-of-the-art for collaborative filtering. 
**グラフ畳み込みネットワーク（GCN）は、協調フィルタリングの新しい最先端技術**となりました。(GNNはCFの一種なのか...!:thinking:)
Nevertheless, the reasons of its effectiveness for recommendation are not well understood. 
しかし、その推薦に対する効果の理由は十分に理解されていません。 
Existing work that adapts GCN to recommendation lacks thorough ablation analyses on GCN, which is originally designed for graph classification tasks and equipped with many neural network operations. 
GCNを推薦に適応させた既存の研究は、グラフ分類タスクのために元々設計され、多くのニューラルネットワーク操作を備えたGCNに対する徹底的なアブレーション分析が欠けています。 
However, we empirically find that the two most common designs in GCNs — feature transformation and nonlinear activation — contribute little to the performance of collaborative filtering. 
しかし、私たちは経験的に、GCNにおける最も一般的な2つの設計—特徴変換と非線形活性化—が協調フィルタリングの性能にほとんど寄与しないことを発見しました。 
Even worse, including them adds to the difficulty of training and degrades recommendation performance. 
さらに悪いことに、それらを含めることはトレーニングの難易度を増し、推薦性能を低下させます。 

In this work, we aim to simplify the design of GCN to make it more concise and appropriate for recommendation. 
本研究では、GCNの設計を簡素化し、より簡潔で推薦に適したものにすることを目指します。 
We propose a new model named LightGCN, including only the most essential component in GCN — neighborhood aggregation — for collaborative filtering. 
私たちは、協調フィルタリングのためにGCNの最も重要なコンポーネント—近隣集約—のみを含む新しいモデルLightGCNを提案します。 
Specifically, LightGCN learns user and item embeddings by linearly propagating them on the user-item interaction graph, and uses the weighted sum of the embeddings learned at all layers as the final embedding. 
具体的には、LightGCNはユーザとアイテムの埋め込みをユーザ-アイテム相互作用グラフ上で線形に伝播させて学習し、すべての層で学習された埋め込みの加重和を最終的な埋め込みとして使用します。 
Such simple, linear, and neat model is much easier to implement and train, exhibiting substantial improvements (about 16.0% relative improvement on average) over Neural Graph Collaborative Filtering (NGCF) — a state-of-the-art GCN-based recommender model — under exactly the same experimental setting. 
このようなシンプルで線形かつ整然としたモデルは、実装とトレーニングがはるかに容易であり、まったく同じ実験設定の下で、最先端のGCNベースの推薦モデルであるNeural Graph Collaborative Filtering (NGCF)に対して、実質的な改善（平均約16.0%の相対改善）を示します。 
Further analyses are provided towards the rationality of the simple LightGCN from both analytical and empirical perspectives. 
さらに、シンプルなLightGCNの合理性について、分析的および経験的な視点からの分析が提供されます。 
Our implementations are available in both TensorFlow[1] and PyTorch[2]. 
私たちの実装は、TensorFlow[1]とPyTorch[2]の両方で利用可能です。 

### 1.1. KEYWORDS  
Collaborative Filtering, Recommendation, Embedding Propagation, Graph Neural Network  
協調フィルタリング、推薦、埋め込み伝播、グラフニューラルネットワーク  

## 2. INTRODUCTION  

To alleviate information overload on the web, recommender system has been widely deployed to perform personalized information filtering [7, 45, 46]. 
ウェブ上の情報過多を緩和するために、推薦システムは個別化された情報フィルタリングを行うために広く展開されています [7, 45, 46]。 
The core of recommender system is to predict whether a user will interact with an item, e.g., click, rate, purchase, among other forms of interactions. 
推薦システムの核心は、ユーザがアイテムと相互作用するかどうかを予測することです。例えば、クリック、評価、購入などの相互作用の形態があります。 
As such, collaborative filtering (CF), which focuses on exploiting the past user-item interactions to achieve the prediction, remains to be a fundamental task towards effective personalized recommendation [10, 19, 28, 39]. 
そのため、過去のユーザ-アイテム相互作用を利用して予測を行うことに焦点を当てた協調フィルタリング（CF）は、効果的な個別化推薦に向けた基本的なタスクであり続けます [10, 19, 28, 39]。 

The most common paradigm for CF is to learn latent features (a.k.a. embedding) to represent a user and an item, and perform prediction based on the embedding vectors [6, 19]. 
CFの最も一般的なパラダイムは、ユーザとアイテムを表現する潜在特徴（別名埋め込み）を学習し、埋め込みベクトルに基づいて予測を行うことです [6, 19]。 
Matrix factorization is an early such model, which directly projects the single ID of a user to her embedding [26]. 
行列分解はそのような初期のモデルであり、ユーザの単一IDを彼女の埋め込みに直接投影します [26]。 
Later on, several research find that augmenting user ID with the her interaction history as the input can improve the quality of embedding. 
その後、いくつかの研究が、ユーザIDに彼女の相互作用履歴を入力として追加することで埋め込みの質を向上させることができることを発見しました。 
For example, SVD++ [25] demonstrates the benefits of user interaction history in predicting user numerical ratings, and Neural Attentive Item Similarity (NAIS) [18] differentiates the importance of items in the interaction history and shows improvements in predicting item ranking. 
例えば、SVD++ [25]はユーザの数値評価を予測する際のユーザ相互作用履歴の利点を示し、Neural Attentive Item Similarity (NAIS) [18]は相互作用履歴におけるアイテムの重要性を区別し、アイテムランキングの予測における改善を示します。 
In view of user-item interaction graph, these improvements can be seen as coming from using the subgraph structure of a user — more specifically, her one-hop neighbors — to improve the embedding learning. 
ユーザ-アイテム相互作用グラフの観点から、これらの改善は、ユーザのサブグラフ構造—より具体的には、彼女の1ホップ隣接者—を使用して埋め込み学習を改善することから来ていると見ることができます。 

To deepen the use of subgraph structure with high-hop neighbors, Wang et al. [39] recently proposes NGCF and achieves state-of-the-art performance for CF. 
サブグラフ構造を高ホップ隣接者とともに深めるために、Wangら [39] は最近NGCFを提案し、CFにおいて最先端の性能を達成しました。 
It takes inspiration from the Graph Convolution Network (GCN) [14, 23], following the same propagation rule to refine embeddings: feature transformation, neighborhood aggregation, and nonlinear activation. 
それはグラフ畳み込みネットワーク（GCN） [14, 23] からインスピレーションを得て、埋め込みを洗練するために同じ伝播ルールに従います：特徴変換、近隣集約、非線形活性化。 
Although NGCF has shown promising results, we argue that its designs are rather heavy and burdensome — many operations are directly inherited from GCN without justification. 
NGCFは有望な結果を示していますが、その設計はかなり重く負担が大きいと主張します—多くの操作は正当化なしにGCNから直接継承されています。 
As a result, they are not necessarily useful for the CF task. 
その結果、それらはCFタスクにとって必ずしも有用ではありません。 
To be specific, GCN is originally proposed for node classification on attributed graph, where each node has rich attributes as input features; 
具体的には、GCNは元々、各ノードが入力特徴として豊富な属性を持つ属性グラフ上でのノード分類のために提案されました； 
whereas in user-item interaction graph for CF, each node (user or item) is only described by a one-hot ID, which has no concrete semantics besides being an identifier. 
一方、CFのためのユーザ-アイテム相互作用グラフでは、各ノード（ユーザまたはアイテム）は一意のIDによってのみ記述され、識別子以外の具体的な意味はありません。 
In such a case, given the ID embedding as the input, performing multiple layers of nonlinear feature transformation — which is the key to the success of modern neural networks [16] — will bring no benefits, but negatively increases the difficulty for model training. 
このような場合、ID埋め込みを入力として与えた場合、複数層の非線形特徴変換を行うこと—これは現代のニューラルネットワークの成功の鍵です [16]—は利益をもたらさず、モデルのトレーニングの難易度を逆に増加させます。 

To validate our thoughts, we perform extensive ablation studies on NGCF. 
私たちの考えを検証するために、NGCFに対して広範なアブレーション研究を行います。 
With rigorous controlled experiments (on the same data splits and evaluation protocol), we draw the conclusion that the two operations inherited from GCN — feature transformation and nonlinear activation — has no contribution on NGCF’s effectiveness. 
厳密に制御された実験（同じデータ分割と評価プロトコルで）を行い、GCNから継承された2つの操作—特徴変換と非線形活性化—がNGCFの効果に寄与しないという結論を導きます。 
Even more surprising, removing them leads to significant accuracy improvements. 
さらに驚くべきことに、それらを取り除くことで大幅な精度向上が得られます。 
This reflects the issues of adding operations that are useless for the target task in graph neural network, which not only brings no benefits, but rather degrades model effectiveness. 
これは、グラフニューラルネットワークにおいて、ターゲットタスクに対して無駄な操作を追加することの問題を反映しており、利益をもたらすどころか、モデルの効果を低下させます。 

Motivated by these empirical findings, we present a new model named LightGCN, including the most essential component of GCN — neighborhood aggregation — for collaborative filtering. 
これらの経験的な発見に動機づけられ、私たちは協調フィルタリングのためにGCNの最も重要なコンポーネント—近隣集約—を含む新しいモデルLightGCNを提案します。 
Specifically, after associating each user (item) with an ID embedding, we propagate the embeddings on the user-item interaction graph to refine them. 
具体的には、各ユーザ（アイテム）をID埋め込みに関連付けた後、ユーザ-アイテム相互作用グラフ上で埋め込みを伝播させて洗練します。 
We then combine the embeddings learned at different propagation layers with a weighted sum to obtain the final embedding for prediction. 
次に、異なる伝播層で学習された埋め込みを加重和で組み合わせて、予測のための最終的な埋め込みを取得します。 
The whole model is simple and elegant, which not only is easier to train, but also achieves better empirical performance than NGCF and other state-of-the-art methods like Mult-VAE [28]. 
全体のモデルはシンプルでエレガントであり、トレーニングが容易であるだけでなく、NGCFやMult-VAE [28]のような他の最先端の手法よりも優れた経験的性能を達成します。 

To summarize, this work makes the following main contributions: 
要約すると、本研究は以下の主要な貢献を行います： 
We empirically show that two common designs in GCN, feature transformation and nonlinear activation, have no positive effect on the effectiveness of collaborative filtering. 
私たちは、GCNにおける2つの一般的な設計、特徴変換と非線形活性化が協調フィルタリングの効果に対して正の効果を持たないことを経験的に示します。 
We propose LightGCN, which largely simplifies the model design by including only the most essential components in GCN for recommendation. 
私たちは、推薦のためにGCNの最も重要なコンポーネントのみを含むことで、モデル設計を大幅に簡素化するLightGCNを提案します。 
We empirically compare LightGCN with NGCF by following the same setting and demonstrate substantial improvements. 
私たちは、同じ設定に従ってLightGCNとNGCFを経験的に比較し、実質的な改善を示します。 
In-depth analyses are provided towards the rationality of LightGCN from both technical and empirical perspectives. 
LightGCNの合理性について、技術的および経験的な視点からの詳細な分析が提供されます。 

#### 2.0.1. 2 PRELIMINARIES  
We first introduce NGCF [39], a representative and state-of-the-art GCN model for recommendation. 
まず、推薦のための代表的で最先端のGCNモデルであるNGCF [39]を紹介します。 
We then perform ablation studies on NGCF to judge the usefulness of each operation in NGCF. 
次に、NGCFに対してアブレーション研究を行い、NGCF内の各操作の有用性を判断します。 
The novel contribution of this section is to show that the two common designs in GCNs, feature transformation and nonlinear activation, have no positive effect on collaborative filtering. 
このセクションの新しい貢献は、GCNにおける2つの一般的な設計、特徴変換と非線形活性化が協調フィルタリングに対して正の効果を持たないことを示すことです。  

**Table 1: Performance of NGCF and its three variants.**  
**表1: NGCFとその3つのバリアントの性能。**  
**Gowalla** **Amazon-Book**  
**recall** **ndcg** **recall** **ndcg**  
NGCF 0.1547 0.1307 0.0330 0.0254  
NGCF-f 0.1686 0.1439 0.0368 0.0283  
NGCF-n 0.1536 0.1295 0.0336 0.0258  
NGCF-fn 0.1742 0.1476 0.0399 0.0303  

#### 2.0.2. 2.1 NGCF Brief  
In the initial step, each user and item is associated with an ID embedding. 
最初のステップでは、各ユーザとアイテムがID埋め込みに関連付けられます。 
Let $e_u^{(0)}$ denote the ID embedding of user $u$ and $e_i^{(0)}$ denote the ID embedding of item $i$. 
ユーザ$u$のID埋め込みを$e_u^{(0)}$、アイテム$i$のID埋め込みを$e_i^{(0)}$とします。 



. Let eu[(0)] [denote the ID embedding of user][ u][ and][ e]i[(0)] denote the ID embedding of item i. 
. eu[(0)]をユーザuのID埋め込み、ei[(0)]をアイテムiのID埋め込みとします。

Then NGCF leverages the user-item interaction graph to propagate embeddings as:
次に、NGCFはユーザ-アイテム相互作用グラフを利用して埋め込みを伝播させます。

$$
e_u^{(k+1)} = \sigma(W_1 e_u^{(k)}) + \sum_{i \in N_u} (W_1 e_i^{(k)} + W_2 (e_i^{(k)} \odot e_u^{(k)}))
$$

$$
e_i^{(k+1)} = \sigma(W_1 e_i^{(k)}) + \sum_{u \in N_i} (W_1 e_u^{(k)} + W_2 (e_u^{(k)} \odot e_i^{(k)}))
$$

(1) where eu[(k)] and ei[(k)] respectively denote the refined embedding of user u and item i after k layers propagation, 
（1）ここで、eu[(k)]とei[(k)]はそれぞれ、k層の伝播後のユーザuとアイテムiの洗練された埋め込みを示します。

σ is the nonlinear activation function, 
σは非線形活性化関数です。

Nu denotes the set of items that are interacted by user u, 
Nuはユーザuが相互作用するアイテムの集合を示します。

Ni denotes the set of users that interact with item i, 
Niはアイテムiと相互作用するユーザの集合を示します。

and W1 and W2 are trainable weight matrix to perform feature transformation in each layer. 
W1とW2は各層で特徴変換を行うための学習可能な重み行列です。

By propagating L layers, NGCF obtains _L + 1 embeddings to describe a user (eu[(0)][,][ e]u[(1)][, ...,][ e]u[(][L][)][) and an item]_ (ei[(0)][,][ e]i[(1)][, ...,][ e]i[(][L][)][). 
L層を伝播させることで、NGCFはユーザを表す_L + 1の埋め込み（eu[(0)][,][ e]u[(1)][, ...,][ e]u[(][L][)][）とアイテムを表す埋め込み（ei[(0)][,][ e]i[(1)][, ...,][ e]i[(][L][)][）を取得します。

It then concatenates these][ L][ + 1 embeddings to] obtain the final user embedding and item embedding, using inner product to generate the prediction score. 
その後、これらのL + 1の埋め込みを連結して最終的なユーザ埋め込みとアイテム埋め込みを取得し、内積を使用して予測スコアを生成します。

NGCF largely follows the standard GCN [23], including the use of nonlinear activation function σ (·) and feature transformation matrices W1 and W2. 
NGCFは主に標準的なGCN [23]に従い、非線形活性化関数σ(·)と特徴変換行列W1およびW2を使用します。

However, we argue that the two operations are not as useful for collaborative filtering. 
しかし、私たちはこれらの2つの操作が協調フィルタリングにはそれほど有用ではないと主張します。

In semi-supervised node classification, each node has rich semantic features as input, such as the title and abstract words of a paper. 
半教師ありノード分類では、各ノードは論文のタイトルや要約の単語など、豊富な意味的特徴を入力として持っています。

Thus performing multiple layers of nonlinear transformation is beneficial to feature learning. 
したがって、複数層の非線形変換を行うことは特徴学習に有益です。

Nevertheless, in collaborative filtering, each node of user-item interaction graph only has an ID as input which has no concrete semantics. 
それにもかかわらず、協調フィルタリングでは、ユーザ-アイテム相互作用グラフの各ノードは具体的な意味を持たないIDのみを入力として持っています。

In this case, performing multiple nonlinear transformations will not contribute to learn better features; 
この場合、複数の非線形変換を行ってもより良い特徴を学習することには寄与しません。

even worse, it may add the difficulties to train well. 
さらに悪いことに、うまくトレーニングするのが難しくなる可能性があります。

In the next subsection, we provide empirical evidence on this argument. 
次の小節では、この主張に関する実証的証拠を提供します。

#### 2.0.3. 2.2 Empirical Explorations on NGCF
#### 2.0.4. 2.2 NGCFに関する実証的探求

We conduct ablation studies on NGCF to explore the effect of nonlinear activation and feature transformation. 
私たちは、非線形活性化と特徴変換の効果を探るためにNGCFに関するアブレーションスタディを実施します。

We use the codes released by the authors of NGCF[3], running experiments on the same data splits and evaluation protocol to keep the comparison as fair as possible. 
私たちは、NGCFの著者によって公開されたコード[3]を使用し、同じデータ分割と評価プロトコルで実験を実行して、比較をできるだけ公平に保ちます。

Since the core of GCN is to refine embeddings by propagation, we are more interested in the embedding quality under the same embedding size. 
GCNの核心は埋め込みを伝播によって洗練させることなので、私たちは同じ埋め込みサイズの下での埋め込みの質により関心があります。

Thus, we change the way of obtaining final embedding from concatenation (i.e., eu[∗] = eu[(0)] [∥· · · ∥][e]u[(][L][)][) to] sum (i.e., eu[∗] = eu[(0)] [+][ · · ·][ +] [e]u[(][L][)][). 
したがって、最終埋め込みを連結（すなわち、eu[∗] = eu[(0)] [∥· · · ∥][e]u[(][L][)から]合計（すなわち、eu[∗] = eu[(0)] [+][ · · ·][ +] [e]u[(][L][)に変更します。

Note that this change has little effect 
この変更はほとんど影響がないことに注意してください。

|Col1|Gowalla|Amazon-Book| 
|---|---|---| 
|recall ndcg|recall ndcg| 
|NGCF|0.1547 0.1307|0.0330 0.0254| 
|NGCF-f NGCF-n NGCF-fn|0.1686 0.1439 0.1536 0.1295 0.1742 0.1476|0.0368 0.0283 0.0336 0.0258 0.0399 0.0303|  

0.030  
0.025  
0.020  
0.015  
0.010  
0.005  
0.000  

0.030  
0.025  
0.020  
0.015  
0.010  
0.005  
0.000  

0.18  
0.16  
0.14  
0.12  
0.10  
0.08  

|Col1|Gowalla| 
|---|---| 

|Col1|Amazon-Book| 
|---|---| 

0 100 200 300 400 500 Epoch  
0 25 50 75 100 125 150 175 Epoch  

|Gowalla|Col2| 
|---|---| 

|0|100 200 300 400 500 Epoch|  
(a) Training loss on Gowalla  
(b) Testing recall on Gowalla  
(c) Training loss on Amazon-Book  
(d) Testing recall on Amazon-Book  
**Figure 1: Training curves (training loss and testing recall) of NGCF and its three simplified variants.**  
**図1: NGCFとその3つの簡略化されたバリアントのトレーニング曲線（トレーニング損失とテストリコール）。**  

on NGCF’s performance, but makes the following ablation studies more indicative of the embedding quality refined by GCN. 
NGCFの性能には影響しませんが、次のアブレーションスタディがGCNによって洗練された埋め込みの質をより示すものになります。

We implement three simplified variants of NGCF: 
私たちはNGCFの3つの簡略化されたバリアントを実装します：

- NGCF-f, which removes the feature transformation matrices W1 and W2. 
- NGCF-fは、特徴変換行列W1とW2を削除します。

- NGCF-n, which removes the non-linear activation function σ. 
- NGCF-nは、非線形活性化関数σを削除します。

- NGCF-fn, which removes both the feature transformation matrices and non-linear activation function. 
- NGCF-fnは、特徴変換行列と非線形活性化関数の両方を削除します。

For the three variants, we keep all hyper-parameters (e.g., learning rate, regularization coefficient, dropout ratio, etc.) same as the optimal settings of NGCF. 
これらの3つのバリアントについて、すべてのハイパーパラメータ（例：学習率、正則化係数、ドロップアウト比率など）をNGCFの最適設定と同じに保ちます。

We report the results of the 2-layer setting on the Gowalla and Amazon-Book datasets in Table 1. 
表1にGowallaおよびAmazon-Bookデータセットにおける2層設定の結果を報告します。

As can be seen, removing feature transformation (i.e., NGCF-f) leads to consistent improvements over NGCF on all three datasets. 
ご覧のように、特徴変換を削除する（すなわち、NGCF-f）は、すべての3つのデータセットでNGCFに対して一貫した改善をもたらします。

In contrast, removing nonlinear activation does not affect the accuracy that much. 
対照的に、非線形活性化を削除しても精度にはそれほど影響しません。

However, if we remove nonlinear activation on the basis of removing feature transformation (i.e., NGCF-fn), the performance is improved significantly. 
しかし、特徴変換を削除した上で非線形活性化を削除すると（すなわち、NGCF-fn）、性能が大幅に改善されます。

From these observations, we conclude the findings that: 
これらの観察から、次のような発見を結論付けます：

(1) Adding feature transformation imposes negative effect on NGCF, since removing it in both models of NGCF and NGCF-n improves the performance significantly; 
（1）特徴変換を追加するとNGCFに悪影響を及ぼします。なぜなら、NGCFとNGCF-nの両方のモデルでそれを削除すると性能が大幅に改善されるからです。

(2) Adding nonlinear activation affects slightly when feature transformation is included, but it imposes negative effect when feature transformation is disabled. 
（2）非線形活性化を追加すると、特徴変換が含まれている場合にはわずかに影響しますが、特徴変換が無効にされると悪影響を及ぼします。

(3) As a whole, feature transformation and nonlinear activation impose rather negative effect on NGCF, since by removing them simultaneously, NGCF-fn demonstrates large improvements over NGCF (9.57% relative improvement on recall). 
（3）全体として、特徴変換と非線形活性化はNGCFに対してかなり悪影響を及ぼします。なぜなら、これらを同時に削除することで、NGCF-fnはNGCFに対して大幅な改善（リコールでの9.57%の相対改善）を示すからです。

To gain more insights into the scores obtained in Table 1 and understand why NGCF deteriorates with the two operations, we plot the curves of model status recorded by training loss and testing recall in Figure 1. 
表1で得られたスコアに関するさらなる洞察を得て、なぜNGCFがこれらの2つの操作で劣化するのかを理解するために、図1にトレーニング損失とテストリコールで記録されたモデルの状態の曲線をプロットします。

As can be seen, NGCF-fn achieves a much lower training loss than NGCF, NGCF-f, and NGCF-n along the whole training process. 
ご覧のように、NGCF-fnはトレーニングプロセス全体にわたってNGCF、NGCF-f、およびNGCF-nよりもはるかに低いトレーニング損失を達成します。

Aligning with the curves of testing recall, we find that such lower training loss successfully transfers to better recommendation accuracy. 
テストリコールの曲線と一致して、こうした低いトレーニング損失がより良い推薦精度に成功裏に移行することがわかります。

The comparison between NGCF and NGCF-f shows the similar trend, except that the improvement margin is smaller. 
NGCFとNGCF-fの比較は同様の傾向を示しますが、改善の幅は小さいです。

From these evidences, we can draw the conclusion that the deterioration of NGCF stems from the training difficulty, rather than overfitting. 
これらの証拠から、NGCFの劣化は過学習ではなく、トレーニングの難しさに起因するという結論を導き出すことができます。

Theoretically speaking, NGCF has higher representation power than NGCF-f, since setting the weight matrix W1 and W2 to identity matrix I can fully recover the NGCF-f model. 
理論的に言えば、NGCFはNGCF-fよりも高い表現力を持っています。なぜなら、重み行列W1とW2を単位行列Iに設定することで、NGCF-fモデルを完全に復元できるからです。

However, in practice, NGCF demonstrates higher training loss and worse generalization performance than NGCF-f. 
しかし、実際には、NGCFはNGCF-fよりも高いトレーニング損失と悪い一般化性能を示します。

And the incorporation of nonlinear activation further aggravates the discrepancy between representation power and generalization performance. 
さらに、非線形活性化の導入は、表現力と一般化性能の間の不一致をさらに悪化させます。

To round out this section, we claim that when designing model for recommendation, it is important to perform rigorous ablation studies to be clear about the impact of each operation. 
このセクションを締めくくるために、推薦モデルを設計する際には、各操作の影響を明確にするために厳密なアブレーションスタディを行うことが重要であると主張します。

Otherwise, including less useful operations will complicate the model unnecessarily, increase the training difficulty, and even degrade model effectiveness. 
そうでなければ、あまり有用でない操作を含めることは、モデルを不必要に複雑にし、トレーニングの難しさを増し、さらにはモデルの効果を低下させる可能性があります。

#### 2.0.5. 3 METHOD  
#### 2.0.6. 3 方法  

The former section demonstrates that NGCF is a heavy and burdensome GCN model for collaborative filtering. 
前のセクションでは、NGCFが協調フィルタリングにとって重く負担の大きいGCNモデルであることを示しました。

Driven by these findings, we set the goal of developing a light yet effective model by including the most essential ingredients of GCN for recommendation. 
これらの発見に基づき、私たちは推薦のためにGCNの最も重要な要素を含む軽量かつ効果的なモデルを開発することを目指します。

The advantages of being simple are severalfold — more interpretable, practically easy to train and maintain, technically easy to analyze the model behavior and revise it towards more effective directions, and so on. 
シンプルであることの利点は多岐にわたります。— より解釈しやすく、実際にトレーニングやメンテナンスが容易であり、技術的にモデルの挙動を分析し、より効果的な方向に修正するのが容易です。

In this section, we first present our designed Light Graph _Convolution Network (LightGCN) model, as illustrated in Figure 2._ 
このセクションでは、まず私たちが設計したLight Graph Convolution Network（LightGCN）モデルを紹介します（図2に示されています）。

We then provide an in-depth analysis of LightGCN to show the rationality behind its simple design. 
次に、LightGCNの詳細な分析を提供し、そのシンプルな設計の背後にある合理性を示します。

Lastly, we describe how to do model training for recommendation. 
最後に、推薦のためのモデルトレーニングの方法を説明します。

#### 2.0.7. 3.1 LightGCN  
#### 2.0.8. 3.1 LightGCN  

The basic idea of GCN is to learning representation for nodes by smoothing features over the graph [23, 40]. 
GCNの基本的なアイデアは、グラフ上で特徴を平滑化することによってノードの表現を学習することです[23, 40]。

To achieve this, it performs graph convolution iteratively, i.e., aggregating the features of neighbors as the new representation of a target node. 
これを実現するために、グラフ畳み込みを反復的に実行し、すなわち、隣接ノードの特徴を集約してターゲットノードの新しい表現とします。

Such neighborhood aggregation can be abstracted as:
このような近隣集約は次のように抽象化できます：

$$
e_u^{(k+1)} = AGG(e_u^{(k)}, \{e_i^{(k)} : i \in N_u\}) 
$$

(2)  
(2)  

The AGG is an aggregation function — the core of graph convolution — that considers the k-th layer’s representation of the target node and its neighbor nodes. 
AGGは集約関数であり、グラフ畳み込みの核心であり、ターゲットノードとその隣接ノードのk層目の表現を考慮します。

Many work have specified the AGG, such as the weighted sum aggregator in GIN [42], LSTM aggregator in GraphSAGE [14], and bilinear interaction aggregator in BGNN [48] etc. 
多くの研究がAGGを特定しており、GIN [42]の加重和集約器、GraphSAGE [14]のLSTM集約器、BGNN [48]の双線形相互作用集約器などがあります。

However, most of the work ties feature transformation or nonlinear activation with the AGG function. 
しかし、ほとんどの研究は特徴変換や非線形活性化をAGG関数に結びつけています。

Although they perform well on node or graph classification tasks that have semantic input features, they could be burdensome for collaborative filtering (see preliminary results in Section 2.2) 
彼らは意味的入力特徴を持つノードやグラフ分類タスクでうまく機能しますが、協調フィルタリングには負担になる可能性があります（セクション2.2の予備結果を参照）。


```md
. Although they perform well on node or graph classification tasks that have semantic input features, they could be burdensome for collaborative filtering (see preliminary results in Section 2.2).  
ノードまたはグラフ分類タスクにおいて、意味的な入力特徴を持つ場合には良好な性能を発揮しますが、協調フィルタリングにおいては負担になる可能性があります（セクション2.2の予備結果を参照）。

-----
Prediction
**Layer Combination (weighted sum)**  
予測  
**Layer Combination (加重和)**  

**Normalized Sum**  
**正規化和**  

**neighbors of i4**  
**i4の隣接ノード**  

**Light Graph Convolution (LGC)**  
**ライトグラフ畳み込み（LGC）**  
of a user (an item):  
ユーザ（アイテム）の：  
$$
e_u = \alpha_k e_u[k]; \quad e_i = \alpha_k e_i[k],
$$  
$$
_k = 0 \quad _k = 0
$$  

|Col2|Col3|Col4|Col5|  
|---|---|---|---|  
| | | | |  
| | | | |  
|ۺ܉ܡ܍ܚ| |ۺ܉ܡ܍ܚ| |  
|ۺ܉ܡ܍ܚ| |ۺ܉ܡ܍ܚ| |  
|ۺ܉ܡ܍ܚ| |ۺ܉ܡ܍ܚ| |  
|ۺ܉ܡ܍ܚ| |ۺ܉ܡ܍ܚ| |  
|ۺ܉ܡ܍ܚ| |ۺ܉ܡ܍ܚ| |  
|ۺ܉ܡ܍ܚ = Normalized Sum| |ۺ܉ܡ܍ܚ = Normalized Sum| |  
| | | | |  
|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|  
|---|---|---|---|---|---|---|---|  
| | | | | | | | |  
| | | | | | | | |  
|ۺ܉ܡ܍ܚ = Normalized Sum| |ۺ܉ܡ܍ܚ = Normalized Sum| |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | | | |  
| | | | | | |


## 3. 0 R

**A =** **R[T]** **0**  
**A =** **R[T]** **0**  

Let the 0-th layer embedding matrix be $E^{(0)} \in R^{(M + N) \times T}$, where T is the embedding size. 
0層の埋め込み行列を $E^{(0)} \in R^{(M + N) \times T}$ とし、Tは埋め込みサイズです。 

Then we can obtain the matrix equivalent form of LGC as: 
次に、LGCの行列同等形式を得ることができます：

$$
E^{(k+1)} = (D^{-1/2} A D^{-1/2}) E^{(k)},
$$  
$$
E^{(k+1)} = (D^{-1/2} A D^{-1/2}) E^{(k)},
$$  

where D is a $(M + N) \times (M + N)$ diagonal matrix, in which each entry $D_{ii}$ denotes the number of nonzero entries in the i-th row vector of the adjacency matrix A (also named as degree matrix). 
ここで、Dは $(M + N) \times (M + N)$ の対角行列であり、各エントリ $D_{ii}$ は隣接行列Aのi行ベクトルの非ゼロエントリの数を示します（これを次数行列とも呼びます）。 

Lastly, we get the final embedding matrix used for model prediction as: 
最後に、モデル予測に使用される最終的な埋め込み行列を次のように得ます：

$$
E = \alpha_0 E^{(0)} + \alpha_1 E^{(1)} + \alpha_2 E^{(2)} + ... + \alpha_K E^{(K)},
$$  
$$
E = \alpha_0 E^{(0)} + \alpha_1 E^{(1)} + \alpha_2 E^{(2)} + ... + \alpha_K E^{(K)},
$$  

GCN model that integrates self-connection into graph convolution; this analysis shows that by doing layer combination, LightGCN subsumes the effect of self-connection thus there is no need for LightGCN to add self-connection in adjacency matrix. 
自己接続をグラフ畳み込みに統合したGCNモデル；この分析は、層の組み合わせを行うことで、LightGCNが自己接続の効果を包含することを示しており、したがってLightGCNが隣接行列に自己接続を追加する必要はありません。 

Then we discuss the relation with the Approximate Personalized Propagation of Neural Predictions (APPNP) [24], which is recent GCN variant that addresses oversmoothing by inspiring from Personalized PageRank [15]; 
次に、最近のGCNの変種であるApproximate Personalized Propagation of Neural Predictions (APPNP) [24]との関係について議論します。これは、Personalized PageRank [15]からインスパイアを受けてオーバースムージングに対処します。 

this analysis shows the underlying equivalence between LightGCN and APPNP, thus our LightGCN enjoys the same benefits in propagating long-range with controllable oversmoothing. 
この分析は、LightGCNとAPPNPの間の根本的な同等性を示しており、したがって私たちのLightGCNは、制御可能なオーバースムージングで長距離を伝播する際の同じ利点を享受します。 

Lastly we analyze the second-layer LGC to show how it smooths a user with her second-order neighbors, providing more insights into the working mechanism of LightGCN. 
最後に、2層目のLGCを分析して、どのようにしてユーザーが彼女の2次近隣とスムーズにするかを示し、LightGCNの動作メカニズムに関するさらなる洞察を提供します。 

_3.2.1_ _Relation with SGCN. In [40], the authors argue the_ unnecessary complexity of GCN for node classification and propose SGCN, which simplifies GCN by removing nonlinearities and collapsing the weight matrices to one weight matrix. 
_3.2.1_ _SGCNとの関係。文献[40]では、著者はノード分類に対するGCNの不必要な複雑さを主張し、非線形性を排除し、重み行列を1つの重み行列に圧縮することでGCNを簡素化するSGCNを提案しています。 

The graph convolution in SGCN is defined as: 
SGCNにおけるグラフ畳み込みは次のように定義されます：

$$
E^{(k+1)} = (D + I)^{-1/2} (A + I) (D + I)^{-1/2} E^{(k)},
$$  
$$
E^{(k+1)} = (D + I)^{-1/2} (A + I) (D + I)^{-1/2} E^{(k)},
$$  

where $I \in R^{(M + N) \times (M + N)}$ is an identity matrix, which is added on **A to include self-connections. 
ここで、$I \in R^{(M + N) \times (M + N)}$ は単位行列であり、自己接続を含めるために**Aに追加されます。 

In the following analysis, we omit the $(D + I)^{-1/2}$ terms for simplicity, since they only re-scale embeddings. 
以下の分析では、埋め込みを再スケールするだけなので、簡単のために $(D + I)^{-1/2}$ の項を省略します。 

In SGCN, the embeddings obtained at the last layer are used for downstream prediction task, which can be expressed as: 
SGCNでは、最後の層で得られた埋め込みが下流の予測タスクに使用され、次のように表現できます：

$$
E^{(K)} = (A + I) E^{(K-1)} = (A + I)^K E^{(0)} 
$$  
$$
E^{(K)} = (A + I) E^{(K-1)} = (A + I)^K E^{(0)} 
$$  

The above derivation shows that, inserting self-connection into A and propagating embeddings on it, is essentially equivalent to a weighted sum of the embeddings propagated at each LGC layer. 
上記の導出は、Aに自己接続を挿入し、それに埋め込みを伝播させることが、実質的に各LGC層で伝播された埋め込みの加重和に等しいことを示しています。 

_3.2.2_ _Relation with APPNP. In a recent work [24], the authors_ connect GCN with Personalized PageRank [15], inspiring from which they propose a GCN variant named APPNP that can propagate long range without the risk of oversmoothing. 
_3.2.2_ _APPNPとの関係。最近の研究[24]では、著者はGCNをPersonalized PageRank [15]と接続し、そこからインスパイアを受けて、オーバースムージングのリスクなしに長距離を伝播できるGCNの変種APPNPを提案しています。 

Inspired by the teleport design in Personalized PageRank, APPNP complements each propagation layer with the starting features (i.e., the 0-th layer embeddings), which can balance the need of preserving locality (i.e., staying close to the root node to alleviate oversmoothing) and leveraging the information from a large neighborhood. 
Personalized PageRankのテレポート設計にインスパイアを受けて、APPNPは各伝播層を開始特徴（すなわち、0層の埋め込み）で補完し、局所性を保持する必要性（すなわち、オーバースムージングを緩和するためにルートノードに近く留まること）と大きな近隣からの情報を活用することのバランスを取ります。 

The propagation layer in APPNP is defined as: 
APPNPにおける伝播層は次のように定義されます：

$$
E^{(k+1)} = \beta E^{(0)} + (1 - \beta) A \tilde{E}^{(k)},
$$  
$$
E^{(k+1)} = \beta E^{(0)} + (1 - \beta) A \tilde{E}^{(k)},
$$  

where $\beta$ is the teleport probability to control the retaining of starting features in the propagation, and $\tilde{A}$ denotes the normalized adjacency matrix. 
ここで、$\beta$は伝播における開始特徴の保持を制御するためのテレポート確率であり、$\tilde{A}$は正規化された隣接行列を示します。 

In APPNP, the last layer is used for final prediction, i.e., 
APPNPでは、最後の層が最終予測に使用されます。すなわち、

$$
E^{(K)} = \beta E^{(0)} + (1 - \beta) A \tilde{E}^{(K-1)},
$$  
$$
E^{(K)} = \beta E^{(0)} + (1 - \beta) A \tilde{E}^{(K-1)},
$$  

= $\beta E^{(0)} + \beta(1 - \beta) A \tilde{E}^{(0)} + (1 - \beta) \tilde{A}^{(2)} E^{(K-2)}$  
= $\beta E^{(0)} + \beta(1 - \beta) A \tilde{E}^{(0)} + \beta(1 - \beta) \tilde{A}^{(2)} E^{(0)} + ... + (1 - \beta) \tilde{A}^{(K)} E^{(0)}.$  
= $\beta E^{(0)} + \beta(1 - \beta) A \tilde{E}^{(0)} + \beta(1 - \beta) \tilde{A}^{(2)} E^{(0)} + ... + (1 - \beta) \tilde{A}^{(K)} E^{(0)}.$  
= $\beta E^{(0)} + \beta(1 - \beta) A \tilde{E}^{(0)} + \beta(1 - \beta) \tilde{A}^{(2)} E^{(0)} + ... + (1 - \beta) \tilde{A}^{(K)} E^{(0)}.$  

The weight matrix in SGCN can be absorbed into the 0-th layer embedding parameters, thus it is omitted in the analysis.  
SGCNにおける重み行列は0層の埋め込みパラメータに吸収できるため、分析では省略されます。  

Aligning with Equation (8), we can see that by setting $\alpha_k$ accordingly, LightGCN can fully recover the prediction embedding used by APPNP. 
式(8)に合わせると、$\alpha_k$を適切に設定することで、LightGCNはAPPNPで使用される予測埋め込みを完全に回復できることがわかります。 

As such, LightGCN shares the strength of APPNP in combating oversmoothing — by setting the $\alpha$ properly, we allow using a large K for long-range modeling with controllable oversmoothing. 
このように、LightGCNはオーバースムージングに対抗するAPPNPの強みを共有しています。$\alpha$を適切に設定することで、制御可能なオーバースムージングで長距離モデリングのために大きなKを使用することを可能にします。 

Another minor difference is that APPNP adds self-connection into the adjacency matrix. 
もう一つの小さな違いは、APPNPが隣接行列に自己接続を追加することです。 

However, as we have shown before, this is redundant due to the weighted sum of different layers. 
しかし、前述のように、これは異なる層の加重和による冗長性があります。 

_3.2.3_ _Second-Order Embedding Smoothness. Owing to the linearity_ and simplicity of LightGCN, we can draw more insights into how does it smooth embeddings. 
_3.2.3_ _2次埋め込みの滑らかさ。LightGCNの線形性と単純さのおかげで、埋め込みをどのようにスムーズにするかについてより多くの洞察を得ることができます。 

Here we analyze a 2-layer LightGCN to demonstrate its rationality. 
ここでは、2層のLightGCNを分析してその合理性を示します。 

Taking the user side as an example, intuitively, the second layer smooths users that have overlap on the interacted items. 
ユーザー側を例に取ると、直感的に、2層目は相互作用したアイテムに重複があるユーザーをスムーズにします。 

More concretely, we have: 
より具体的には、次のようになります：

$$
e^{(2)}_u = \frac{1}{|N_u|} \sum_{i \in N_u} \frac{1}{|N_i|} e^{(1)}_i = \frac{1}{|N_u|} \sum_{i \in N_u} \sum_{v \in N_i} \frac{1}{|N_v|} e^{(0)}_v,
$$  
$$
e^{(2)}_u = \frac{1}{|N_u|} \sum_{i \in N_u} \frac{1}{|N_i|} e^{(1)}_i = \frac{1}{|N_u|} \sum_{i \in N_u} \sum_{v \in N_i} \frac{1}{|N_v|} e^{(0)}_v,
$$  

We can see that, if another user $v$ has co-interacted with the target user $u$, the smoothness strength of $v$ on $u$ is measured by the coefficient (otherwise 0): 
他のユーザー$v$がターゲットユーザー$u$と共に相互作用した場合、$u$に対する$v$の滑らかさの強さは係数によって測定されます（そうでない場合は0）：

$$
c_{v \to u} = \frac{1}{|N_u|} \sum_{i \in N_u \cap N_v} \frac{1}{|N_i|}.
$$  
$$
c_{v \to u} = \frac{1}{|N_u|} \sum_{i \in N_u \cap N_v} \frac{1}{|N_i|}.
$$  

This coefficient is rather interpretable: the influence of a second-order neighbor $v$ on $u$ is determined by 1) the number of co-interacted items, the more the larger; 2) the popularity of the co-interacted items, the less popularity (i.e., more indicative of user personalized preference) the larger; and 3) the activity of $v$, the less active the larger. 
この係数は非常に解釈可能です：2次近隣$v$が$u$に与える影響は、1) 共に相互作用したアイテムの数、より多いほど大きい；2) 共に相互作用したアイテムの人気、人気が少ないほど（すなわち、ユーザーの個別の好みを示す）大きい；3) $v$の活動性、活動が少ないほど大きいことによって決まります。 

Such interpretability well caters for the assumption of CF in measuring user similarity [2, 37] and evidences the reasonability of LightGCN. 
このような解釈可能性は、ユーザーの類似性を測定する際のCFの仮定にうまく対応し、LightGCNの合理性を証明します。 

Due to the symmetric formulation of LightGCN, we can get similar analysis on the item side. 
LightGCNの対称的な定式化により、アイテム側でも同様の分析を行うことができます。 

#### 3.0.1. 3.3 Model Training
The trainable parameters of LightGCN are only the embeddings of the 0-th layer, i.e., $\Theta = \{E^{(0)}\}$; in other words, the model complexity is same as the standard matrix factorization (MF). 
#### 3.0.2. 3.3 モデルのトレーニング
LightGCNの学習可能なパラメータは0層の埋め込みのみであり、すなわち、$\Theta = \{E^{(0)}\}$です。言い換えれば、モデルの複雑さは標準的な行列分解（MF）と同じです。 

We employ the Bayesian Personalized Ranking (BPR) loss [32], which is a pairwise loss that encourages the prediction of an observed entry to be higher than its unobserved counterparts:  
私たちは、観測されたエントリの予測が未観測の対応物よりも高くなることを促すペアワイズ損失であるBayesian Personalized Ranking (BPR)損失 [32]を採用します：

$$
L_{BPR} = -\sum_{u=1}^{M} \sum_{i \in N_u} \ln \sigma(\hat{y}_{ui} - \hat{y}_{uj}) + \lambda ||E^{(0)}||_2^2
$$  
$$
L_{BPR} = -\sum_{u=1}^{M} \sum_{i \in N_u} \ln \sigma(\hat{y}_{ui} - \hat{y}_{uj}) + \lambda ||E^{(0)}||_2^2
$$  

where $\lambda$ controls the L2 regularization strength. 
ここで、$\lambda$はL2正則化の強さを制御します。 

We employ the Adam [22] optimizer and use it in a mini-batch manner. 
私たちはAdam [22]オプティマイザを採用し、ミニバッチ方式で使用します。 

We are aware of other advanced negative sampling strategies which might improve the LightGCN training, such as the hard negative sampling [31] and adversarial sampling [9]. 
私たちは、ハードネガティブサンプリング [31]や敵対的サンプリング [9]など、LightGCNのトレーニングを改善する可能性のある他の高度なネガティブサンプリング戦略を認識しています。 

We leave this extension in the future since it is not the focus of this work. 
これは本研究の焦点ではないため、将来の拡張として残します。 

Note that we do not introduce dropout mechanisms, which are commonly used in GCNs and NGCF. 
GCNやNGCFで一般的に使用されるドロップアウトメカニズムを導入しないことに注意してください。 

The reason is that we do not have feature transformation weight matrices in LightGCN, thus enforcing L2 regularization on the embedding layer is sufficient to prevent overfitting. 
その理由は、LightGCNには特徴変換重み行列がないため、埋め込み層にL2正則化を強制するだけで過学習を防ぐのに十分だからです。 

This showcases LightGCN’s advantages of being simple — it is easier to train and tune than NGCF which additionally requires to tune two dropout ratios (node dropout and message dropout) and normalize the embedding of each layer to unit length. 
これは、LightGCNがシンプルであるという利点を示しています。NGCFよりもトレーニングとチューニングが容易であり、さらに2つのドロップアウト比率（ノードドロップアウトとメッセージドロップアウト）を調整し、各層の埋め込みを単位長に正規化する必要があります。 

Moreover, it is technically viable to also learn the layer combination coefficients $\{\alpha_k\}_{k=0}^{K}$, or parameterize them with an attention network. 
さらに、層の組み合わせ係数 $\{\alpha_k\}_{k=0}^{K}$ を学習することや、注意ネットワークでパラメータ化することも技術的に可能です。 

However, we find that learning $\alpha$ on training data does not lead improvement. 
しかし、トレーニングデータで $\alpha$ を学習することは改善につながらないことがわかりました。 

This is probably because the training data does not contain sufficient signal to learn good $\alpha$ that can generalize to unknown data. 
これは、おそらくトレーニングデータに未知のデータに一般化できる良い $\alpha$ を学習するのに十分な信号が含まれていないためです。 

We have also tried to learn $\alpha$ from validation data, as inspired by [5] that learns hyper-parameters on validation data. 
私たちは、バリデーションデータでハイパーパラメータを学習する[5]にインスパイアを受けて、バリデーションデータから $\alpha$ を学習しようとしました。 

The performance is slightly improved (less than 1%). 
パフォーマンスはわずかに改善されました（1%未満）。 

We leave the exploration of optimal settings of $\alpha$ (e.g., personalizing it for different users and items) as future work. 
最適な $\alpha$ の設定（例えば、異なるユーザーやアイテムに対して個別化すること）の探求は将来の作業として残します。 

#### 3.0.3. 4 EXPERIMENTS
We first describe experimental settings, and then conduct detailed comparison with NGCF [39], the method that is most relevant with LightGCN but more complicated (Section 4.2). 
#### 3.0.4. 4 実験
まず実験設定を説明し、次にLightGCNに最も関連するがより複雑な方法であるNGCF [39]との詳細な比較を行います（セクション4.2）。 

We next compare with other state-of-the-art methods in Section 4.3. 
次に、セクション4.3で他の最先端の方法と比較します。 

To justify the designs in LightGCN and reveal the reasons of its effectiveness, we perform ablation studies and embedding analyses in Section 4.4. 
LightGCNの設計を正当化し、その効果の理由を明らかにするために、セクション4.4でアブレーションスタディと埋め込み分析を行います。 

The hyper-parameter study is finally presented in Section 4.5. 
ハイパーパラメータの研究は、最後にセクション4.5で提示されます。 

#### 3.0.5. 4.1 Experimental Settings
To reduce the experiment workload and keep the comparison fair, we closely follow the settings of the NGCF work [39]. 
#### 3.0.6. 4.1 実験設定
実験の作業負荷を減らし、比較を公平に保つために、NGCFの設定 [39] に厳密に従います。 

We request the experimented datasets (including train/test splits) from the authors, for which the statistics are shown in Table 2. 
実験されたデータセット（トレーニング/テストの分割を含む）を著者から要求し、その統計は表2に示されています。 

The Gowalla and Amazon-Book are exactly the same as the NGCF paper used, so we directly use the results in the NGCF paper. 
GowallaとAmazon-Bookは、使用されたNGCF論文とまったく同じであるため、NGCF論文の結果を直接使用します。 

The only exception is the Yelp2018 data, which is a revised version. 
唯一の例外は、改訂版のYelp2018データです。 

According to the authors, the previous version did not filter out cold-start items in the testing set, and they shared us the revised version only. 
著者によると、以前のバージョンはテストセットのコールドスタートアイテムをフィルタリングしておらず、改訂版のみを共有してくれました。 

Thus we re-run NGCF on the Yelp2018 data. 
したがって、Yelp2018データでNGCFを再実行しました。 

The evaluation metrics are recall@20 and ndcg@20 computed by the all-ranking protocol — all items that are not interacted by a user are the candidates. 
評価指標は、すべてのアイテムがユーザーによって相互作用されていない候補である全ランキングプロトコルによって計算されたrecall@20とndcg@20です。 

_4.1.1_ _Compared Methods. The main competing method is NGCF,_ which has shown to outperform several methods including GCN-based models GC-MC [35] and PinSage [45], neural network-based models NeuMF [19] and CMN [10], and factorization-based models MF [32] and HOP-Rec [43]. 
_4.1.1_ _比較手法。主な競合手法はNGCFであり、GCNベースのモデルGC-MC [35]やPinSage [45]、ニューラルネットワークベースのモデルNeuMF [19]やCMN [10]、および因子分解ベースのモデルMF [32]やHOP-Rec [43]を含むいくつかの手法を上回ることが示されています。 

As the comparison is done on the same datasets under the same evaluation protocol, we do not further compare with these methods. 
比較は同じデータセットで同じ評価プロトコルの下で行われるため、これらの手法とさらに比較することはありません。 

In addition to NGCF, we further compare with two relevant and competitive CF methods: 
NGCFに加えて、関連性のある競争力のあるCF手法とさらに比較します：

Mult-VAE [28]. This is an item-based CF method based on the variational autoencoder (VAE). 
Mult-VAE [28]。これは、変分オートエンコーダ（VAE）に基づくアイテムベースのCF手法です。 

It assumes the data is generated from a multinomial distribution and using variational inference for parameter estimation. 
データは多項分布から生成され、パラメータ推定のために変分推論を使用することを前提としています。



. This is an item-based CF method based on the variational autoencoder (VAE). 
これは、変分オートエンコーダ（VAE）に基づくアイテムベースの協調フィルタリング（CF）手法です。

It assumes the data is generated from a multinomial distribution and using variational inference for parameter estimation. 
データは多項分布から生成され、パラメータ推定のために変分推論を使用することを前提としています。

We run the codes released by the authors[5], tuning the dropout ratio in [0, 0.2, 0.5], and the β in [0.2, 0.4, 0.6, 0.8]. 
私たちは、著者によって公開されたコードを実行し、ドロップアウト比率を[0, 0.2, 0.5]に、βを[0.2, 0.4, 0.6, 0.8]に調整しました。

The model architecture is the suggested one in the paper: 600 200 600. 
モデルアーキテクチャは、論文で提案されたもので、600 200 600です。

→ →
GRMF [30]. 
GRMF [30]。

This method smooths matrix factorization by adding the graph Laplacian regularizer. 
この手法は、グラフラプラシアン正則化項を追加することで行列因子分解を滑らかにします。

For fair comparison on item recommendation, we change the rating prediction loss to BPR loss. 
アイテム推薦の公正な比較のために、評価予測損失をBPR損失に変更します。

The objective function of GRMF is: 
GRMFの目的関数は次の通りです：

$$
\mathcal{L} = -\sum_{u \in N_i} \ln \sigma(e^T u [e][i] - e^T u [e][j]) + \lambda_d ||e_u - e_i||^2 + \lambda ||E||^2,
$$
$$
u=1 \quad i \in N_u \quad j \notin N_u
$$
ここで、$\lambda_d$は[1e^{-5}, 1e^{-4}, ..., 1e^{-1}]の範囲で探索されます。

Moreover, we compare with a variant that adds normalization to graph Laplacian: 
さらに、グラフラプラシアンに正規化を追加した変種と比較します：

$$
\lambda_d || \sqrt{e_u} \sqrt{e_i} |N_u| - |N_i| ||^2,
$$
which is termed as GRMF-norm. 
これはGRMF-normと呼ばれます。

Other hyper-parameter settings are same as LightGCN. 
他のハイパーパラメータ設定はLightGCNと同じです。

The two GRMF methods benchmark the performance of smoothing embeddings via Laplacian regularizer, while our LightGCN achieves embedding smoothing in the predictive model. 
2つのGRMF手法は、ラプラシアン正則化を介して埋め込みの平滑化の性能をベンチマークしますが、私たちのLightGCNは予測モデルにおいて埋め込みの平滑化を達成します。

_4.1.2_ _Hyper-parameter Settings. 
_4.1.2_ ハイパーパラメータ設定。

Same as NGCF, the embedding size is fixed to 64 for all models and the embedding parameters are initialized with the Xavier method [12]. 
NGCFと同様に、埋め込みサイズはすべてのモデルで64に固定され、埋め込みパラメータはXavier法[12]で初期化されます。

We optimize LightGCN with Adam [22] and use the default learning rate of 0.001 and default mini-batch size of 1024 (on Amazon-Book, we increase the minibatch size to 2048 for speed). 
私たちはAdam [22]でLightGCNを最適化し、デフォルトの学習率0.001とデフォルトのミニバッチサイズ1024を使用します（Amazon-Bookでは、速度向上のためにミニバッチサイズを2048に増やします）。

The L2 regularization coefficient $\lambda$ is searched in the range of {1e^{-6}, 1e^{-5}, ..., 1e^{-2}}, and in most cases the optimal value is 1e^{-4}. 
L2正則化係数$\lambda$は{1e^{-6}, 1e^{-5}, ..., 1e^{-2}}の範囲で探索され、ほとんどの場合、最適値は1e^{-4}です。

The layer combination coefficient $\alpha_k$ is uniformly set to $1 + \frac{1}{K}$ [where $K$ is the number of layers]. 
層の組み合わせ係数$\alpha_k$は均等に$1 + \frac{1}{K}$に設定されます[ここで$K$は層の数です]。

We test $K$ in the range of 1 to 4, and satisfactory performance can be achieved when $K$ equals to 3. 
私たちは$K$を1から4の範囲でテストし、$K$が3のときに満足のいく性能が達成されます。

The early stopping and validation strategies are the same as NGCF. 
早期停止と検証戦略はNGCFと同じです。

Typically, 1000 epochs are sufficient for LightGCN to converge. 
通常、1000エポックでLightGCNは収束します。

Our implementations are available in both TensorFlow[6] and PyTorch[7]. 
私たちの実装は、TensorFlow[6]とPyTorch[7]の両方で利用可能です。

#### 3.0.7. 4.2 Performance Comparison with NGCF
#### 3.0.8. 4.2 NGCFとの性能比較

We perform detailed comparison with NGCF, recording the performance at different layers (1 to 4) in Table 4, which also shows the percentage of relative improvement on each metric. 
私たちはNGCFとの詳細な比較を行い、異なる層（1から4）での性能を表4に記録し、各指標の相対改善の割合も示します。

We further plot the training curves of training loss and testing recall in Figure 3 to reveal the advantages of LightGCN and to be clear of the training process. 
さらに、図3においてトレーニング損失とテストリコールのトレーニング曲線をプロットし、LightGCNの利点を明らかにし、トレーニングプロセスを明確にします。

The main observations are as follows: 
主な観察結果は次の通りです：

In all cases, LightGCN outperforms NGCF by a large margin. 
すべてのケースにおいて、LightGCNはNGCFを大きく上回ります。

For example, on Gowalla the highest recall reported in the NGCF paper is 0.1570, while our LightGCN can reach 0.1830 under the 4-layer setting, which is 16.56% higher. 
例えば、Gowallaでは、NGCF論文で報告された最高のリコールは0.1570ですが、私たちのLightGCNは4層設定で0.1830に達し、16.56%高くなります。

On average, the recall improvement on the three datasets is 16.52% and the ndcg improvement is 16.87%, which are rather significant. 
平均して、3つのデータセットでのリコールの改善は16.52%、ndcgの改善は16.87%であり、非常に重要です。

Aligning Table 4 with Table 1 in Section 2, we can see that LightGCN performs better than NGCF-fn, the variant of NGCF that removes feature transformation and nonlinear activation. 
表4をセクション2の表1と照らし合わせると、LightGCNは特徴変換と非線形活性化を削除したNGCFの変種であるNGCF-fnよりも優れた性能を発揮していることがわかります。

As NGCF-fn still contains more operations than LightGCN (e.g., self-connection, the interaction between user embedding and item embedding in graph convolution, and dropout), this suggests that these operations might also be useless for NGCF-fn. 
NGCF-fnはLightGCNよりも多くの操作（例えば、自己接続、グラフ畳み込みにおけるユーザ埋め込みとアイテム埋め込みの相互作用、ドロップアウト）を含んでいるため、これらの操作がNGCF-fnにとっても無駄である可能性があることを示唆しています。

Increasing the number of layers can improve the performance, but the benefits diminish. 
層の数を増やすことで性能が向上しますが、その利点は減少します。

The general observation is that increasing the layer number from 0 (i.e., the matrix factorization model, results see [39]) to 1 leads to the largest performance gain, and using a layer number of 3 leads to satisfactory performance in most cases. 
一般的な観察結果は、層の数を0（すなわち、行列因子分解モデル、結果は[39]を参照）から1に増やすことで最大の性能向上が得られ、層の数を3にすることでほとんどのケースで満足のいく性能が得られるということです。

This observation is consistent with NGCF’s finding. 
この観察結果は、NGCFの発見と一致しています。

Along the training process, LightGCN consistently obtains lower training loss, which indicates that LightGCN fits the training data better than NGCF. 
トレーニングプロセス全体を通じて、LightGCNは一貫して低いトレーニング損失を得ており、これはLightGCNがNGCFよりもトレーニングデータに適合していることを示しています。

Moreover, the lower training loss successfully transfers to better testing accuracy, indicating the strong generalization power of LightGCN. 
さらに、低いトレーニング損失はより良いテスト精度に成功裏に移行し、LightGCNの強力な一般化能力を示しています。

In contrast, the higher training loss and lower testing accuracy of NGCF reflect the practical difficulty to train such a heavy model well. 
対照的に、NGCFの高いトレーニング損失と低いテスト精度は、そのような重いモデルをうまくトレーニングすることの実際の難しさを反映しています。

Note that in the figures we show the training process under the optimal hyper-parameter setting for both methods. 
図において、私たちは両方の手法の最適なハイパーパラメータ設定の下でのトレーニングプロセスを示しています。

Although increasing the learning rate of NGCF can decrease its training loss (even lower than that of LightGCN), the testing recall could not be improved, as lowering training loss in this way only finds trivial solution for NGCF. 
NGCFの学習率を上げることでトレーニング損失を減少させることができますが（LightGCNよりも低くなることもあります）、この方法でトレーニング損失を下げることはNGCFにとって自明な解を見つけるだけであるため、テストリコールは改善されません。

which is better than GRMF and NGCF. 
これはGRMFおよびNGCFよりも優れています。

The performance of GRMF is on a par with NGCF, being better than MF, which admits the utility of enforcing embedding smoothness with Laplacian regularizer. 
GRMFの性能はNGCFと同等であり、MFよりも優れており、ラプラシアン正則化を用いて埋め込みの滑らかさを強制する有用性を認めています。

By adding normalization into the Laplacian regularizer, GRMF-norm betters than GRMF on Gowalla, while brings no benefits on Yelp2018 and Amazon-Book. 
ラプラシアン正則化に正規化を追加することで、GRMF-normはGowallaでGRMFよりも優れていますが、Yelp2018およびAmazon-Bookでは利益をもたらしません。

**Table 4: The comparison of overall performance among LightGCN and competing methods.** 
**表4: LightGCNと競合手法の全体的な性能比較。**

**Dataset** **Gowalla** **Yelp2018** **Amazon-Book** 
**Method** **recall** **ndcg** **recall** **ndcg** **recall** **ndcg** 
NGCF 0.1570 0.1327 0.0579 0.0477 0.0344 0.0263 
Mult-VAE 0.1641 0.1335 0.0584 0.0450 0.0407 0.0315 
GRMF 0.1477 0.1205 0.0571 0.0462 0.0354 0.0270 
GRMF-norm 0.1557 0.1261 0.0561 0.0454 0.0352 0.0269 
LightGCN **0.1830** **0.1554** **0.0649** **0.0530** **0.0411** **0.0315** 

#### 3.0.9. 4.4 Ablation and Effectiveness Analyses
#### 3.0.10. 4.4 アブレーションと有効性分析

|Dataset|Gowalla|Yelp2018|Amazon-Book| 
|---|---|---|---| 
|Method|recall ndcg|recall ndcg|recall ndcg| 
|NGCF|0.1570 0.1327|0.0579 0.0477|0.0344 0.0263| 
|Mult-VAE|0.1641 0.1335|0.0584 0.0450|0.0407 0.0315| 
|GRMF GRMF-norm|0.1477 0.1205 0.1557 0.1261|0.0571 0.0462 0.0561 0.0454|0.0354 0.0270 0.0352 0.0269| 
|LightGCN|0.1830 0.1554|0.0649 0.0530|0.0411 0.0315| 

#### 3.0.11. 4.3 Performance Comparison with State-of-the-Arts
#### 3.0.12. 4.3 最先端技術との性能比較

Table 4 shows the performance comparison with competing methods. 
表4は、競合手法との性能比較を示しています。

We show the best score we can obtain for each method. 
各手法で得られる最高のスコアを示します。

We can see that LightGCN consistently outperforms other methods on all three datasets, demonstrating its high effectiveness with simple yet reasonable designs. 
LightGCNは、すべての3つのデータセットで他の手法を一貫して上回っており、シンプルでありながら合理的な設計による高い効果を示しています。

Note that LightGCN can be further improved by tuning the $\alpha_k$ (see Figure 4 for an evidence), while here we only use a uniform setting of $K=1+1$ [to avoid over-tuning it.] 
LightGCNは$\alpha_k$を調整することでさらに改善できることに注意してください（証拠は図4を参照）、ここでは過剰調整を避けるために$K=1+1$の均一設定のみを使用しています。

Among the baselines, Mult-VAE exhibits the strongest performance,  
ベースラインの中で、Mult-VAEは最も強力な性能を示します。

We perform ablation studies on LightGCN by showing how layer combination and symmetric sqrt normalization affect its performance. 
層の組み合わせと対称平方根正規化がLightGCNの性能にどのように影響するかを示すことで、LightGCNに関するアブレーション研究を行います。

To justify the rationality of LightGCN as analyzed in Section 3.2.3, we further investigate the effect of embedding smoothness — the key reason of LightGCN’s effectiveness. 
セクション3.2.3で分析されたLightGCNの合理性を正当化するために、埋め込みの滑らかさの効果をさらに調査します。これはLightGCNの効果的な理由の鍵です。

_4.4.1_ _Impact of Layer Combination. 
_4.4.1_ 層の組み合わせの影響。

Figure 4 shows the results of LightGCN and its variant LightGCN-single that does not use layer combination (i.e., E[(][K] [)] is used for final prediction for a K-layer LightGCN). 
図4は、層の組み合わせを使用しないLightGCNとその変種LightGCN-singleの結果を示しています（すなわち、K層のLightGCNの最終予測にE[(][K] [)]が使用されます）。

We omit the results on Yelp2018 due to space limitation, which show similar trend with Amazon-Book 
Yelp2018の結果はスペースの制限により省略しますが、Amazon-Bookと同様の傾向を示しています。



We omit the results on Yelp2018 due to space limitation, which show similar trend with Amazon-Book. 
Yelp2018の結果は、スペースの制限により省略しますが、Amazon-Bookと同様の傾向を示しています。

We have three main observations: Focusing on LightGCN-single, we find that its performance first improves and then drops when the layer number increases from 1 to 4. 
私たちは主に3つの観察結果があります：LightGCN-singleに注目すると、層の数が1から4に増加するにつれて、その性能は最初に改善し、その後低下することがわかります。

The peak point is on layer 2 in most cases, while after that it drops quickly to the worst point of layer 4. 
ほとんどの場合、ピークポイントは層2にあり、その後すぐに層4の最悪のポイントに低下します。

This indicates that smoothing a node’s embedding with its first-order and second-order neighbors is very useful for CF, but will suffer from oversmoothing issues when higher-order neighbors are used. 
これは、ノードの埋め込みを一次および二次の隣接ノードで平滑化することがCFにとって非常に有用であることを示していますが、高次の隣接ノードを使用すると過剰平滑化の問題が発生することを示しています。

Focusing on LightGCN, we find that its performance gradually improves with the increasing of layers. 
LightGCNに注目すると、層の増加に伴いその性能が徐々に改善することがわかります。

Even using 4 layers, LightGCN’s performance is not degraded. 
4層を使用しても、LightGCNの性能は低下しません。

This justifies the effectiveness of layer combination for addressing over-smoothing, as we have technically analyzed in Section 3.2.2 (relation with APPNP). 
これは、過剰平滑化に対処するための層の組み合わせの効果を正当化します。これは、セクション3.2.2（APPNPとの関係）で技術的に分析しました。

Comparing the two methods, we find that LightGCN consistently outperforms LightGCN-single on Gowalla, but not on Amazon-Book and Yelp2018 (where the 2-layer LightGCN-single performs the best). 
2つの方法を比較すると、LightGCNはGowallaで一貫してLightGCN-singleを上回りますが、Amazon-BookおよびYelp2018ではそうではありません（2層のLightGCN-singleが最も良い性能を発揮します）。

Regarding this phenomenon, two points need to be noted before we draw conclusion: 
この現象に関して、結論を出す前に2つの点に注意する必要があります：

1) LightGCN-single is special case of LightGCN that sets αK to 1 and other αk to 0; 
1）LightGCN-singleは、αKを1に、他のαkを0に設定したLightGCNの特別なケースです。

2) we do not tune the αk and simply set it as _K1+1_ [uniformly for LightGCN.] 
2）私たちはαkを調整せず、単に_K1+1_として設定しています（LightGCNに対して均一に）。

As such, we can see the potential of further enhancing the performance of LightGCN by tuning αk. 
そのため、αkを調整することでLightGCNの性能をさらに向上させる可能性があることがわかります。

_4.4.2_ _Impact of Symmetric Sqrt Normalization. In LightGCN,_ we employ symmetric sqrt normalization √ |Nu |1[√] |Ni | [on each] neighbor embedding when performing neighborhood aggregation (cf. Equation (3)). 
_4.4.2_ _対称平方根正規化の影響。LightGCNでは、近隣集約を行う際に、各隣接ノードの埋め込みに対して対称平方根正規化√ |Nu |1[√] |Ni |を適用します（参照：式（3））。

To study its rationality, we explore different choices here. 
その合理性を研究するために、ここで異なる選択肢を探ります。

We test the use of normalization only at the left side (i.e., the target node’s coefficient) and the right side (i.e., the neighbor node’s coefficient). 
左側（すなわち、ターゲットノードの係数）および右側（すなわち、隣接ノードの係数）での正規化の使用をテストします。

We also test L1 normalization, i.e., removing the square root. 
また、L1正規化、すなわち平方根を取り除くこともテストします。

Note that if removing normalization, the training becomes numerically unstable and suffers from nota-value (NAN) issues, so we do not show this setting. 
正規化を取り除くと、トレーニングが数値的に不安定になり、NAN（値なし）問題に苦しむため、この設定は示しません。

Table 5 shows the results of the 3-layer LightGCN. 
表5は、3層のLightGCNの結果を示しています。

We have the following observations: 
以下の観察結果があります：

The best setting in general is using sqrt normalization at both sides (i.e., the current design of LightGCN). 
一般的に最良の設定は、両側で平方根正規化を使用することです（すなわち、現在のLightGCNの設計）。

Removing either side will drop the performance largely. 
どちらか一方を取り除くと、性能が大幅に低下します。

The second best setting is using L1 normalization at the left side only (i.e., LightGCN-L1-L). 
2番目に良い設定は、左側のみでL1正規化を使用することです（すなわち、LightGCN-L1-L）。

This is equivalent to normalize the adjacency matrix as a stochastic matrix by the in-degree. 
これは、隣接行列を入次数によって確率行列として正規化することに相当します。

Normalizing symmetrically on two sides is helpful for the sqrt normalization, but will degrade the performance of L1 normalization. 
両側で対称的に正規化することは平方根正規化に役立ちますが、L1正規化の性能を低下させます。

_4.4.3_ _Analysis of Embedding Smoothness. As we have analyzed_ in Section 3.2.3, a 2-layer LightGCN smooths a user’s embedding based on the users that have overlap on her interacted items, and the smoothing strength between two users cv→u is measured in Equation (14). 
_4.4.3_ _埋め込みの滑らかさの分析。セクション3.2.3で分析したように、2層のLightGCNは、ユーザが相互作用したアイテムに重複のあるユーザに基づいてユーザの埋め込みを平滑化し、2人のユーザ間の平滑化強度cv→uは式（14）で測定されます。

We speculate that such smoothing of embeddings is the key reason of LightGCN’s effectiveness. 
このような埋め込みの平滑化がLightGCNの効果の鍵であると推測します。

To verify this, we first define the smoothness of user embeddings as: 
これを検証するために、まずユーザ埋め込みの滑らかさを次のように定義します：

|Dataset|Gowalla|Yelp2018|Amazon-Book| 
|---|---|---|---| 
|Method|recall ndcg|recall ndcg|recall ndcg| 
|LightGCN-L1-L LightGCN-L1-R LightGCN-L1|0.1724 0.1414 0.1578 0.1348 0.159 0.1319|0.0630 0.0511 0.0587 0.0477 0.0573 0.0465|0.0419 0.0320 0.0334 0.0259 0.0361 0.0275| 

|LightGCN-L LightGCN-R|0.1589 0.1317 0.1420 0.1156|0.0619 0.0509 0.0521 0.0401|0.0383 0.0299 0.0252 0.0196| 

|LightGCN|0.1830 0.1554|0.0649 0.0530|0.0411 0.0315|

|Dataset|Gowalla|Yelp2018|Amazon-book| 
|---|---|---|---| 
|Smoothness of User Embeddings||| 
|MF|15449.3|16258.2|38034.2| 
|LightGCN-single|12872.7|10091.7|32191.1| 

|Smoothness of Item Embeddings||| 
|MF|12106.7|16632.1|28307.9| 
|LightGCN-single|5829.0|6459.8|16866.0| 

_M_ � _SU =_
_u=1_  
�M **eu** **ev**
_v=1_ _cv→u_ ( ||eu ||[2][ −] ||ev ||[2][ )][2][,] (17)  
where the L2 norm on embeddings is used to eliminate the impact of the embedding’s scale. 
ここで、埋め込みに対するL2ノルムを使用して、埋め込みのスケールの影響を排除します。

Similarly we can obtained the definition for item embeddings. 
同様に、アイテム埋め込みの定義も得られます。

Table 6 shows the smoothness of two models, matrix factorization (i.e., using the E[(0)] for model prediction) and the 2-layer LightGCN-single (i.e., using the E[(2)] for prediction). 
表6は、2つのモデル、行列分解（すなわち、モデル予測にE[(0)]を使用）と2層のLightGCN-single（すなわち、予測にE[(2)]を使用）の滑らかさを示しています。

Note that the 2-layer LightGCN-single outperforms MF in recommendation accuracy by a large margin. 
2層のLightGCN-singleは、推薦精度においてMFを大きく上回ることに注意してください。

As can be seen, the smoothness loss of LightGCN-single is much lower than that of MF. 
見ての通り、LightGCN-singleの滑らかさの損失はMFよりもはるかに低いです。

This indicates that by conducting light graph convolution, the embeddings become smoother and more suitable for recommendation. 
これは、軽いグラフ畳み込みを行うことで、埋め込みがより滑らかになり、推薦に適したものになることを示しています。

**Figure 5: Performance of 2-layer LightGCN w.r.t. different regularization coefficient λ on Yelp and Amazon-Book.** 
**図5：YelpおよびAmazon-Bookにおける異なる正則化係数λに対する2層LightGCNの性能。**

#### 3.0.13. 4.5 Hyper-parameter Studies
#### 3.0.14. 4.5 ハイパーパラメータの研究

When applying LightGCN to a new dataset, besides the standard hyper-parameter learning rate, the most important hyper-parameter to tune is the L2 regularization coefficient λ. 
LightGCNを新しいデータセットに適用する際、標準のハイパーパラメータである学習率に加えて、最も重要なハイパーパラメータはL2正則化係数λです。

Here we investigate the performance change of LightGCN w.r.t. λ. 
ここでは、λに対するLightGCNの性能変化を調査します。

As shown in Figure 5, LightGCN is relatively insensitive to λ — even when λ sets to 0, LightGCN is better than NGCF, which additionally uses dropout to prevent overfitting[8]. 
図5に示すように、LightGCNはλに対して比較的鈍感です。λが0に設定されていても、LightGCNはドロップアウトを追加して過剰適合を防ぐNGCFよりも優れています[8]。

This shows that LightGCN is less prone to overfitting — since the only trainable parameters in LightGCN are ID embeddings of the 0-th layer, the whole model is easy to train and to regularize. 
これは、LightGCNが過剰適合に対してあまり影響を受けないことを示しています。LightGCNの唯一の学習可能なパラメータは0層のID埋め込みであり、全体のモデルはトレーニングと正則化が容易です。

The optimal value for Yelp2018, Amazon-Book, and Gowalla is 1e[−][3], 1e[−][4], and 1e[−][4], respectively. 
Yelp2018、Amazon-Book、およびGowallaの最適値はそれぞれ1e[−][3]、1e[−][4]、1e[−][4]です。

When λ is larger than 1e[−][3], the performance drops quickly, which indicates that too strong regularization will negatively affect model normal training and is not encouraged. 
λが1e[−][3]より大きくなると、性能が急速に低下します。これは、過度の正則化がモデルの通常のトレーニングに悪影響を及ぼすことを示しており、推奨されません。

#### 3.0.15. 5 RELATED WORK
#### 3.0.16. 5 関連研究

5.1 Collaborative Filtering
5.1 協調フィルタリング

Collaborative Filtering (CF) is a prevalent technique in modern recommender systems [7, 45]. 
協調フィルタリング（CF）は、現代の推薦システムで広く使用されている技術です[7, 45]。

One common paradigm of CF model is to parameterize users and items as embeddings, and learn the embedding parameters by reconstructing historical user-item interactions. 
CFモデルの一般的なパラダイムの1つは、ユーザとアイテムを埋め込みとしてパラメータ化し、歴史的なユーザ-アイテムの相互作用を再構築することによって埋め込みパラメータを学習することです。

For example, earlier CF models like matrix factorization (MF) [26, 32] project the ID of a user (or an item) into an embedding vector. 
例えば、行列分解（MF）[26, 32]のような初期のCFモデルは、ユーザ（またはアイテム）のIDを埋め込みベクトルに投影します。

The recent neural recommender models like NCF [19] and LRML [34] use the same embedding component, while enhance the interaction modeling with neural networks. 
最近のニューラル推薦モデルであるNCF [19]やLRML [34]は、同じ埋め込みコンポーネントを使用し、ニューラルネットワークで相互作用モデリングを強化しています。

Beyond merely using ID information, another type of CF methods considers historical items as the pre-existing features of a user, towards better user representations. 
単にID情報を使用するだけでなく、別のタイプのCF手法は、歴史的アイテムをユーザの既存の特徴と見なし、より良いユーザ表現を目指します。

For example, FISM [21] and SVD++ [25] use the weighted average of the ID embeddings of historical items as the target user’s embedding. 
例えば、FISM [21]やSVD++ [25]は、歴史的アイテムのID埋め込みの加重平均をターゲットユーザの埋め込みとして使用します。

Recently, researchers realize that historical items have different contributions to shape personal interest. 
最近、研究者たちは、歴史的アイテムが個人の興味を形成するために異なる貢献を持つことを認識しました。

Towards this end, attention mechanisms are introduced to capture the varying contributions, such as ACF [3] and NAIS [18], to automatically learn the importance of each historical item. 
この目的のために、ACF [3]やNAIS [18]のように、各歴史的アイテムの重要性を自動的に学習するために、異なる貢献を捉えるための注意メカニズムが導入されました。

When revisiting historical interactions as a user-item bipartite graph, the performance improvements can be attributed to the encoding of local neighborhood — one-hop neighbors — that improves the embedding learning. 
ユーザ-アイテムの二部グラフとして歴史的相互作用を再訪すると、性能の向上は、埋め込み学習を改善する1ホップの隣接ノードのエンコーディングに起因することができます。

8Note that Gowalla shows the same trend with Amazon-Book, so its curves are not shown to better highlight the trend of Yelp2018 and Amazon-Book.  
8GowallaはAmazon-Bookと同様の傾向を示すため、その曲線はYelp2018とAmazon-Bookの傾向をより明確にするために示されていません。

5.2 Graph Methods for Recommendation
5.2 推薦のためのグラフ手法

Another relevant research line is exploiting the user-item graph structure for recommendation. 
もう1つの関連する研究分野は、推薦のためにユーザ-アイテムのグラフ構造を活用することです。

Prior efforts like ItemRank [13], use the label propagation mechanism to directly propagate user preference scores over the graph, i.e., encouraging connected nodes to have similar labels. 
ItemRank [13]のような以前の努力は、ラベル伝播メカニズムを使用して、グラフ上でユーザの好みスコアを直接伝播させ、接続されたノードが類似のラベルを持つように促します。

Recently emerged graph neural networks (GNNs) shine a light on modeling graph structure, especially high-hop neighbors, to guide the embedding learning [14, 23]. 
最近登場したグラフニューラルネットワーク（GNN）は、グラフ構造をモデル化すること、特に高ホップの隣接ノードをモデル化して埋め込み学習を導くことに光を当てています[14, 23]。

Early studies define graph convolution on the spectral domain, such as Laplacian eigen-decomposition [1] and Chebyshev polynomials [8], which are computationally expensive. 
初期の研究では、ラプラシアン固有分解[1]やチェビシェフ多項式[8]のように、スペクトル領域でのグラフ畳み込みを定義していますが、これは計算コストが高いです。

Later on, GraphSage [14] and GCN [23] re-define graph convolution in the spatial domain, i.e., aggregating the embeddings of neighbors to refine the target node’s embedding. 
その後、GraphSage [14]やGCN [23]は、空間領域でのグラフ畳み込みを再定義し、隣接ノードの埋め込みを集約してターゲットノードの埋め込みを洗練します。

Owing to its interpretability and efficiency, it quickly becomes a prevalent formulation of GNNs and is being widely used [11, 29, 47]. 
その解釈可能性と効率性により、すぐにGNNの一般的な定式化となり、広く使用されています[11, 29, 47]。

Motivated by the strength of graph convolution, recent efforts like NGCF [39], GC-MC [35], and PinSage [45] adapt GCN to the user-item interaction graph, capturing CF signals in high-hop neighbors for recommendation. 
グラフ畳み込みの強さに触発されて、最近の努力であるNGCF [39]、GC-MC [35]、およびPinSage [45]は、GCNをユーザ-アイテム相互作用グラフに適応させ、高ホップの隣接ノードにおけるCF信号を捉えて推薦を行います。

It is worth mentioning that several recent efforts provide deep insights into GNNs [24, 27, 40], which inspire us developing LightGCN. 
いくつかの最近の努力がGNNに関する深い洞察を提供していることは注目に値します[24, 27, 40]。これが私たちにLightGCNの開発を促しました。 



. Particularly, Wu et al. [40] argues the unnecessary complexity of GCN, developing a simplified GCN (SGCN) model by removing nonlinearities and collapsing multiple weight matrices into one. 
特に、Wuら[40]はGCNの不必要な複雑さを主張し、非線形性を取り除き、複数の重み行列を1つに統合することによって、簡略化されたGCN（SGCN）モデルを開発しました。

One main difference is that LightGCN and SGCN are developed for different tasks, thus the rationality of model simplification is different. 
主な違いは、LightGCNとSGCNが異なるタスクのために開発されているため、モデル簡略化の合理性が異なることです。

Specifically, SGCN is for node classification, performing simplification for model interpretability and efficiency. 
具体的には、SGCNはノード分類のためのものであり、モデルの解釈性と効率のために簡略化を行います。

In contrast, LightGCN is on collaborative filtering (CF), where each node has an ID feature only. 
対照的に、LightGCNは協調フィルタリング（CF）に関するものであり、各ノードはID特徴のみを持っています。

Thus, we do simplification for a stronger reason: nonlinearity and weight matrices are useless for CF, and even hurt model training. 
したがって、私たちはより強い理由で簡略化を行います：非線形性と重み行列はCFには無用であり、モデルのトレーニングを妨げることさえあります。

For node classification accuracy, SGCN is on par with (sometimes weaker than) GCN. 
ノード分類の精度に関しては、SGCNはGCNと同等（時にはそれよりも劣る）です。

While for CF accuracy, LightGCN outperforms GCN by a large margin (over 15% improvement over NGCF). 
一方、CFの精度に関しては、LightGCNはGCNを大きく上回ります（NGCFに対して15%以上の改善）。

Lastly, another work conducted in the same time [4] also finds that the nonlinearity is unnecessary in NGCF and develops linear GCN model for CF. 
最後に、同時期に行われた別の研究[4]も、NGCFにおいて非線形性が不必要であることを発見し、CFのための線形GCNモデルを開発しました。

In contrast, our LightGCN makes one step further — we remove all redundant parameters and retain only the ID embeddings, making the model as simple as MF. 
対照的に、私たちのLightGCNはさらに一歩進んでいます — すべての冗長なパラメータを削除し、ID埋め込みのみを保持することで、モデルをMFと同じくらいシンプルにします。

#### 3.0.17. 6 CONCLUSION AND FUTURE WORK 結論と今後の研究

In this work, we argued the unnecessarily complicated design of GCNs for collaborative filtering, and performed empirical studies to justify this argument. 
本研究では、協調フィルタリングのためのGCNの不必要に複雑な設計について議論し、この主張を正当化するための実証研究を行いました。

We proposed LightGCN which consists of two essential components — light graph convolution and layer combination. 
私たちは、ライトグラフ畳み込みとレイヤー結合という2つの重要なコンポーネントから成るLightGCNを提案しました。

In light graph convolution, we discard feature transformation and nonlinear activation — two standard operations in GCNs but inevitably increase the training difficulty. 
ライトグラフ畳み込みでは、特徴変換と非線形活性化を捨てます — これはGCNにおける2つの標準的な操作ですが、必然的にトレーニングの難易度を増加させます。

In layer combination, we construct a node’s final embedding as the weighted sum of its embeddings on all layers, which is proved to subsume the effect of self-connections and is helpful to control oversmoothing. 
レイヤー結合では、ノードの最終埋め込みをすべてのレイヤーにおける埋め込みの加重和として構築します。これは自己接続の効果を包含することが証明されており、オーバースムージングの制御に役立ちます。

We conduct experiments to demonstrate the strengths of LightGCN in being simple: easier to be trained, better generalization ability, and more effective.  
私たちは、LightGCNのシンプルさにおける強みを示す実験を行いました：トレーニングが容易で、一般化能力が高く、より効果的です。

We believe the insights of LightGCN are inspirational to future developments of recommender models. 
私たちは、LightGCNの洞察が今後の推薦モデルの開発にインスピレーションを与えると信じています。

With the prevalence of linked graph data in real applications, graph-based models are becoming increasingly important in recommendation; 
実際のアプリケーションにおけるリンクされたグラフデータの普及に伴い、グラフベースのモデルは推薦においてますます重要になっています。

by explicitly exploiting the relations among entities in the predictive model, they are advantageous to traditional supervised learning scheme like factorization machines [17, 33] that model the relations implicitly. 
予測モデルにおけるエンティティ間の関係を明示的に利用することにより、彼らは関係を暗黙的にモデル化する因子分解マシン[17, 33]のような従来の教師あり学習スキームに対して有利です。

For example, a recent trend is to exploit auxiliary information such as item knowledge graph [38], social network [41] and multimedia content [44] for recommendation, where GCNs have set up the new state-of-the-art. 
例えば、最近のトレンドは、アイテム知識グラフ[38]、ソーシャルネットワーク[41]、およびマルチメディアコンテンツ[44]などの補助情報を推薦に利用することであり、ここでGCNは新しい最先端を確立しています。

However, these models may also suffer from the similar issues of NGCF since the user-item interaction graph is also modeled by same neural operations that may be unnecessary. 
しかし、これらのモデルは、ユーザーアイテム相互作用グラフも同じ神経操作によってモデル化されるため、NGCFの類似の問題に悩まされる可能性があります。

We plan to explore the idea of LightGCN in these models. 
私たちは、これらのモデルにおけるLightGCNのアイデアを探求する予定です。

Another future direction is to personalize the layer combination weights αk, so as to enable adaptive-order smoothing for different users (e.g., sparse users may require more signal from higher-order neighbors while active users require less). 
もう一つの将来の方向性は、レイヤー結合の重みαkをパーソナライズし、異なるユーザーのために適応的な順序のスムージングを可能にすることです（例えば、スパースユーザーは高次の隣接者からの信号をより多く必要とするかもしれませんが、アクティブユーザーはそれを少なく必要とします）。

Lastly, we will explore further the strengths of LightGCN’s simplicity, studying whether fast solution exists for non-sampling regression loss [20] and streaming it for online industrial scenarios. 
最後に、私たちはLightGCNのシンプルさの強みをさらに探求し、非サンプリング回帰損失[20]のための迅速な解決策が存在するかどうかを研究し、オンライン産業シナリオでのストリーミングを行います。

**Acknowledgement. The authors thank Bin Wu, Jianbai Ye,** and Yingxin Wu for contributing to the implementation and improvement of LightGCN. 
**謝辞。著者は、LightGCNの実装と改善に貢献したBin Wu、Jianbai Ye、Yingxin Wuに感謝します。**

This work is supported by the National Natural Science Foundation of China (61972372, U19A2079, 61725203). 
この研究は、中国国家自然科学基金（61972372、U19A2079、61725203）によって支援されています。

#### 3.0.18. REFERENCES 参考文献
[1] Joan Bruna, Wojciech Zaremba, Arthur Szlam, and Yann LeCun. 2014. Spectral Networks and Locally Connected Networks on Graphs. In ICLR.  
[2] Chih-Ming Chen, Chuan-Ju Wang, Ming-Feng Tsai, and Yi-Hsuan Yang. 2019. Collaborative Similarity Embedding for Recommender Systems. In WWW. 2637– 2643.  
[3] Jingyuan Chen, Hanwang Zhang, Xiangnan He, Liqiang Nie, Wei Liu, and Tat-Seng Chua. 2017. Attentive Collaborative Filtering: Multimedia Recommendation with Item- and Component-Level Attention. In SIGIR. 335–344.  
[4] Lei Chen, Le Wu, Richang Hong, Kun Zhang, and Meng Wang. 2020. Revisiting Graph based Collaborative Filtering: A Linear Residual Graph Convolutional Network Approach. In AAAI.  
[5] Yihong Chen, Bei Chen, Xiangnan He, Chen Gao, Yong Li, Jian-Guang Lou, and Yue Wang. 2019. λOpt: Learn to Regularize Recommender Models in Finer Levels. In KDD. 978–986.  
[6] Zhiyong Cheng, Ying Ding, Lei Zhu, and Mohan S. Kankanhalli. 2018. Aspect-Aware Latent Factor Model: Rating Prediction with Ratings and Reviews. In _WWW. 639–648._  
[7] Paul Covington, Jay Adams, and Emre Sargin. 2016. Deep Neural Networks for YouTube Recommendations. In RecSys. 191–198.  
[8] Michaël Defferrard, Xavier Bresson, and Pierre Vandergheynst. 2016. Convolutional Neural Networks on Graphs with Fast Localized Spectral Filtering. In NeurIPS. 3837–3845.  
[9] Jingtao Ding, Yuhan Quan, Xiangnan He, Yong Li, and Depeng Jin. 2019. Reinforced Negative Sampling for Recommendation with Exposure Data. In _IJCAI. 2230–2236._  
[10] Travis Ebesu, Bin Shen, and Yi Fang. 2018. Collaborative Memory Network for Recommendation Systems. In SIGIR. 515–524.  
[11] Fuli Feng, Xiangnan He, Xiang Wang, Cheng Luo, Yiqun Liu, and Tat-Seng Chua. 2019. Temporal Relational Ranking for Stock Prediction. TOIS 37, 2 (2019), 27:1–27:30.  
[12] Xavier Glorot and Yoshua Bengio. 2010. Understanding the difficulty of training deep feedforward neural networks. In AISTATS. 249–256.  
[13] Marco Gori and Augusto Pucci. 2007. ItemRank: A Random-Walk Based Scoring Algorithm for Recommender Engines. In IJCAI. 2766–2771.  
[14] William L. Hamilton, Zhitao Ying, and Jure Leskovec. 2017. Inductive Representation Learning on Large Graphs. In NeurIPS. 1025–1035.  
[15] Taher H Haveliwala. 2002. Topic-sensitive pagerank. In WWW. 517–526.  
[16] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. 2016. Deep residual learning for image recognition. In CVPR. 770–778.  
[17] Xiangnan He and Tat-Seng Chua. 2017. Neural Factorization Machines for Sparse Predictive Analytics. In SIGIR. 355–364.  
[18] Xiangnan He, Zhankui He, Jingkuan Song, Zhenguang Liu, Yu-Gang Jiang, and Tat-Seng Chua. 2018. NAIS: Neural Attentive Item Similarity Model for Recommendation. TKDE 30, 12 (2018), 2354–2366.  
[19] Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, and Tat-Seng Chua. 2017. Neural Collaborative Filtering. In WWW. 173–182.  
[20] Xiangnan He, Jinhui Tang, Xiaoyu Du, Richang Hong, Tongwei Ren, and Tat-Seng Chua. 2019. Fast Matrix Factorization with Nonuniform Weights on Missing Data. TNNLS (2019).  
[21] Santosh Kabbur, Xia Ning, and George Karypis. 2013. FISM: factored item similarity models for top-N recommender systems. In KDD. 659–667.  
[22] Diederik P. Kingma and Jimmy Ba. 2015. Adam: A Method for Stochastic Optimization. In ICLR.  
[23] Thomas N. Kipf and Max Welling. 2017. Semi-Supervised Classification with Graph Convolutional Networks. In ICLR.  
[24] Johannes Klicpera, Aleksandar Bojchevski, and Stephan Günnemann. 2019. Predict then propagate: Graph neural networks meet personalized pagerank. In ICLR.  
[25] Yehuda Koren. 2008. Factorization meets the neighborhood: a multifaceted collaborative filtering model. In KDD. 426–434.  
[26] Yehuda Koren, Robert M. Bell, and Chris Volinsky. 2009. Matrix Factorization Techniques for Recommender Systems. IEEE Computer 42, 8 (2009), 30–37.  
[27] Qimai Li, Zhichao Han, and Xiao-Ming Wu. 2018. Deeper Insights Into Graph Convolutional Networks for Semi-Supervised Learning. In AAAI. 3538–3545.  
[28] Dawen Liang, Rahul G. Krishnan, Matthew D. Hoffman, and Tony Jebara. 2018. Variational Autoencoders for Collaborative Filtering. In WWW. 689–698.  
[29] Jiezhong Qiu, Jian Tang, Hao Ma, Yuxiao Dong, Kuansan Wang, and Jie Tang. 2018. DeepInf: Social Influence Prediction with Deep Learning. In KDD. 2110–2119.  
[30] Nikhil Rao, Hsiang-Fu Yu, Pradeep K Ravikumar, and Inderjit S Dhillon. 2015. Collaborative filtering with graph information: Consistency and scalable methods. In NIPS. 2107–2115.  
[31] Steffen Rendle and Christoph Freudenthaler. 2014. Improving pairwise learning for item recommendation from implicit feedback. In WSDM. 273–282.  
[32] Steffen Rendle, Christoph Freudenthaler, Zeno Gantner, and Lars Schmidt-Thieme. 2009. BPR: Bayesian Personalized Ranking from Implicit Feedback. In UAI. 452– 461.  
[33] Steffen Rendle, Zeno Gantner, Christoph Freudenthaler, and Lars Schmidt-Thieme. 2011. Fast context-aware recommendations with factorization machines. In SIGIR. 635–644.  
[34] Yi Tay, Luu Anh Tuan, and Siu Cheung Hui. 2018. Latent relational metric learning via memory-based attention for collaborative ranking. In WWW. 729–739.  
[35] Rianne van den Berg, Thomas N. Kipf, and Max Welling. 2018. Graph Convolutional Matrix Completion. In KDD Workshop on Deep Learning Day.  
[36] Petar Velickovic, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro Liò, and Yoshua Bengio. 2018. Graph Attention Networks. In ICLR.  
[37] Jun Wang, Arjen P. de Vries, and Marcel J. T. Reinders. 2006. Unifying User-based and Item-based Collaborative Filtering Approaches by Similarity Fusion. In SIGIR. 501–508.  
[38] Xiang Wang, Xiangnan He, Yixin Cao, Meng Liu, and Tat-Seng Chua. 2019. KGAT: Knowledge Graph Attention Network for Recommendation. In KDD. 950–958.  
[39] Xiang Wang, Xiangnan He, Meng Wang, Fuli Feng, and Tat-Seng Chua. 2019. Neural Graph Collaborative Filtering. In SIGIR. 165–174.  
[40] Felix Wu, Amauri H. Souza Jr., Tianyi Zhang, Christopher Fifty, Tao Yu, and Kilian Q. Weinberger. 2019. Simplifying Graph Convolutional Networks. In ICML. 6861–6871.  
[41] Le Wu, Peijie Sun, Yanjie Fu, Richang Hong, Xiting Wang, and Meng Wang. 2019. A Neural Influence Diffusion Model for Social Recommendation. In SIGIR. 235–244.  
[42] Keyulu Xu, Weihua Hu, Jure Leskovec, and Stefanie Jegelka. 2018. How powerful are graph neural networks?  



. A Neural Influence Diffusion Model for Social Recommendation. In SIGIR.
A Neural Influence Diffusion Model for Social Recommendation. In SIGIR.

235–244.
235–244.

[42] Keyulu Xu, Weihua Hu, Jure Leskovec, and Stefanie Jegelka. 2018. How powerful are graph neural networks?. In ICLR.
[42] Keyulu Xu, Weihua Hu, Jure Leskovec, および Stefanie Jegelka. 2018. グラフニューラルネットワークはどれほど強力か？ In ICLR.

[43] Jheng-Hong Yang, Chih-Ming Chen, Chuan-Ju Wang, and Ming-Feng Tsai. 2018.
[43] Jheng-Hong Yang, Chih-Ming Chen, Chuan-Ju Wang, および Ming-Feng Tsai. 2018. 
HOP-rec: high-order proximity for implicit recommendation. In RecSys. 140–144.
HOP-rec: 暗黙の推薦のための高次近接。 In RecSys. 140–144.

[44] Yinwei Yin, Xiang Wang, Liqiang Nie, Xiangnan He, Richang Hong, and Tat-Seng Chua. 2019. MMGCN: Multimodal Graph Convolution Network for Personalized Recommendation of Micro-video. In MM.
[44] Yinwei Yin, Xiang Wang, Liqiang Nie, Xiangnan He, Richang Hong, および Tat-Seng Chua. 2019. MMGCN: マルチモーダルグラフ畳み込みネットワークによるマイクロビデオのパーソナライズド推薦。 In MM.

[45] Rex Ying, Ruining He, Kaifeng Chen, Pong Eksombatchai, William L. Hamilton, and Jure Leskovec. 2018. Graph Convolutional Neural Networks for Web-Scale Recommender Systems. In KDD (Data Science track). 974–983.
[45] Rex Ying, Ruining He, Kaifeng Chen, Pong Eksombatchai, William L. Hamilton, および Jure Leskovec. 2018. ウェブ規模の推薦システムのためのグラフ畳み込みニューラルネットワーク。 In KDD (データサイエンストラック). 974–983.

[46] Fajie Yuan, Xiangnan He, Alexandros Karatzoglou, and Liguang Zhang. 2020.
[46] Fajie Yuan, Xiangnan He, Alexandros Karatzoglou, および Liguang Zhang. 2020.
Parameter-Efficient Transfer from Sequential Behaviors for User Modeling and Recommendation. In SIGIR.
ユーザモデリングと推薦のための逐次的行動からのパラメータ効率の良い転送。 In SIGIR.

[47] Cheng Zhao, Chenliang Li, and Cong Fu. 2019. Cross-Domain Recommendation via Preference Propagation GraphNet. In CIKM. 2165–2168.
[47] Cheng Zhao, Chenliang Li, および Cong Fu. 2019. Preference Propagation GraphNetによるクロスドメイン推薦。 In CIKM. 2165–2168.

[48] Hongmin Zhu, Fuli Feng, Xiangnan He, Xiang Wang, Yan Li, Kai Zheng, and Yongdong Zhang. 2020. Bilinear Graph Neural Network with Neighbor Interactions. In IJCAI.
[48] Hongmin Zhu, Fuli Feng, Xiangnan He, Xiang Wang, Yan Li, Kai Zheng, および Yongdong Zhang. 2020. 隣接相互作用を持つ双線形グラフニューラルネットワーク。 In IJCAI.
