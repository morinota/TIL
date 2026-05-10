refs: https://arxiv.org/pdf/1506.01094


## Traversing Knowledge Graphs in Vector Space 知識グラフをベクトル空間で探索する

### Kelvin Guu Stanford University ``` kguu@stanford.edu
### John Miller Stanford University ``` millerjp@stanford.edu
### Percy Liang Stanford University ``` pliang@cs.stanford.edu

Abstract 要約

Path queries on a knowledge graph can be used to answer compositional questions such as “What languages are spoken _by people living in Lisbon?”._ 
知識グラフにおけるパスクエリは、「リスボンに住む人々が話す言語は何ですか？」のような構成的な質問に答えるために使用できます。
However, knowledge graphs often have missing facts (edges) which disrupts path queries. 
しかし、知識グラフにはしばしば欠落した事実（エッジ）があり、これがパスクエリを妨げます。
Recent models for knowledge base completion impute missing facts by embedding knowledge graphs in vector spaces. 
最近の知識ベース補完モデルは、知識グラフをベクトル空間に埋め込むことで欠落した事実を補完します。
We show that these models can be recursively applied to answer path queries, but that they suffer from cascading errors. 
私たちは、これらのモデルがパスクエリに答えるために再帰的に適用できることを示しますが、連鎖的なエラーに悩まされることも示します。
This motivates a new “compositional” training objective, which dramatically improves all models’ ability to answer path queries, in some cases more than doubling accuracy. 
これにより、新しい「構成的」トレーニング目的が生まれ、すべてのモデルのパスクエリに答える能力が劇的に向上し、場合によっては精度が2倍以上になることもあります。
On a standard knowledge base completion task, we also demonstrate that compositional training acts as a novel form of structural regularization, reliably improving performance across all base models (reducing errors by up to 43%) and achieving new state-of-the-art results. 
標準的な知識ベース補完タスクにおいて、構成的トレーニングが新しい形の構造的正則化として機能し、すべての基本モデルのパフォーマンスを信頼性高く向上させ（エラーを最大43%削減）、新しい最先端の結果を達成することも示します。

### 1 Introduction はじめに

Broad-coverage knowledge bases such as Freebase (Bollacker et al., 2008) support a rich array of reasoning and question answering applications, but they are known to suffer from incomplete coverage (Min et al., 2013). 
Freebase（Bollacker et al., 2008）などの広範な知識ベースは、豊富な推論および質問応答アプリケーションをサポートしますが、不完全なカバレッジに悩まされることが知られています（Min et al., 2013）。
For example, as of May 2015, Freebase has an entity Tad Lincoln (Abraham Lincoln’s son), but does not have his ethnicity. 
例えば、2015年5月時点で、Freebaseにはタッド・リンカーン（エイブラハム・リンカーンの息子）というエンティティがありますが、彼の民族性はありません。
An elegant solution to incompleteness is using vector space representations: Controlling the dimensionality of the vector space forces generalization to new facts (Nickel et al., 2011; Nickel et al., 2012; Socher et al., 2013; Riedel et al., 2013; Neelakantan et al., 2015). 
不完全性に対する優れた解決策は、ベクトル空間表現を使用することです：ベクトル空間の次元を制御することで、新しい事実への一般化が強制されます（Nickel et al., 2011; Nickel et al., 2012; Socher et al., 2013; Riedel et al., 2013; Neelakantan et al., 2015）。
In the example, we would hope to infer Tad’s ethnicity from the ethnicity of his parents. 
この例では、タッドの民族性を彼の両親の民族性から推測できることを期待します。

Figure 1: We propose performing path queries such as `tad lincoln/parents/location (“Where` _are Tad Lincoln’s parents located?”) in a parallel_ low-dimensional vector space. 
図1：私たちは、`tad lincoln/parents/location（「タッド・リンカーンの両親はどこに住んでいますか？」）のようなパスクエリを並行した低次元ベクトル空間で実行することを提案します。
Here, entity sets (boxed) are represented as real vectors, and edge traversal is driven by vector-to-vector transformations (e.g., matrix multiplication). 
ここでは、エンティティセット（ボックスで囲まれた部分）は実ベクトルとして表現され、エッジのトラバースはベクトル間の変換（例えば、行列の乗算）によって駆動されます。
However, what is missing from these vector space models is the original strength of knowledge bases: the ability to support compositional queries (Ullman, 1985). 
しかし、これらのベクトル空間モデルに欠けているのは、知識ベースの本来の強みです：構成的クエリをサポートする能力（Ullman, 1985）。
For example, we might ask what the ethnicity of Abraham Lincoln’s daughter would be. 
例えば、エイブラハム・リンカーンの娘の民族性は何かと尋ねることができます。
This can be formulated as a path query on the knowledge graph, and we would like a method that can answer this efficiently, while generalizing over missing facts and even missing or hypothetical entities (Abraham Lincoln did not in fact have a daughter). 
これは知識グラフ上のパスクエリとして定式化でき、欠落した事実や欠落または仮想のエンティティ（エイブラハム・リンカーンには実際には娘がいなかった）を一般化しながら、これに効率的に答える方法を望みます。
In this paper, we present a scheme to answer path queries on knowledge bases by “compositionalizing” a broad class of vector space models that have been used for knowledge base completion (see Figure 1). 
本論文では、知識ベースにおけるパスクエリに答えるためのスキームを、知識ベース補完に使用されてきた広範なクラスのベクトル空間モデルを「構成化」することによって提示します（図1を参照）。
At a high level, we interpret the base vector space model as implementing a soft edge traversal operator. 
高いレベルでは、基本的なベクトル空間モデルをソフトエッジトラバースオペレーターを実装していると解釈します。
This operator can then be recursively applied to predict paths. 
このオペレーターは、パスを予測するために再帰的に適用できます。
Our interpretation suggests a new compositional training objective that encourages better modeling of paths. 
私たちの解釈は、パスのより良いモデリングを促進する新しい構成的トレーニング目的を示唆します。
Our technique is applicable to a broad class of composable models that includes the bilinear model (Nickel et al., 2011) and TransE (Bordes et al., 2013). 
私たちの手法は、バイリニアモデル（Nickel et al., 2011）やTransE（Bordes et al., 2013）を含む、構成可能なモデルの広範なクラスに適用可能です。
We have two key empirical findings: 
私たちは2つの重要な実証的発見があります：
First, we show that compositional training enables us to answer path queries up to at least length 5 by substantially reducing cascading errors present in the base vector space model. 
まず、構成的トレーニングにより、基本的なベクトル空間モデルに存在する連鎖的エラーを大幅に削減することで、少なくとも長さ5までのパスクエリに答えることができることを示します。
Second, we find that somewhat surprisingly, compositional training also improves upon state-of-the-art performance for knowledge base completion, which is a special case of answering unit length path queries. 
第二に、驚くべきことに、構成的トレーニングは、単位長のパスクエリに答える特別なケースである知識ベース補完の最先端のパフォーマンスをも向上させることがわかりました。
Therefore, compositional training can also be seen as a new form of structural regularization for existing models. 
したがって、構成的トレーニングは既存のモデルに対する新しい形の構造的正則化とも見なすことができます。

### 2 Task タスク

We now give a formal definition of the task of answering path queries on a knowledge base. 
ここでは、知識ベースにおけるパスクエリに答えるタスクの正式な定義を示します。
Let be a set of entities and be a set of binary _E_ _R_ relations. 
エンティティの集合をE、二項関係の集合をRとします。
A knowledge graph is defined as a _G_ set of triples of the form (s, r, t) where s, t _∈E_ and r _∈R_. 
知識グラフは、s, t _∈E_ および r _∈R_ の形の三重項 (s, r, t) の集合 _G_ として定義されます。
An example of a triple in Freebase is _∈R_ (tad lincoln, parents, abraham lincoln). 
Freebaseの三重項の例は、_∈R_ (tad lincoln, parents, abraham lincoln) です。
A path query q consists of an initial anchor entity, s, followed by a sequence of relations to be traversed, p = (r1, . . ., rk). 
パスクエリ q は、初期のアンカーエンティティ s と、トラバースされる関係のシーケンス p = (r1, . . ., rk) から構成されます。
The answer or denotation of the query, _q_, is the set of all entities that can be reached from s by traversing p. 
クエリ _q_ の答えまたは指示は、s から p をトラバースすることで到達可能なすべてのエンティティの集合です。
Formally, this can be defined recursively: 
形式的には、これは再帰的に定義できます：

$$
_s_ = _s_ _,_ (1) 
$$

$$
_q/r_ = _t :_ _s_ _q_ _, (s, r, t)_ _._ (2) 
$$

For example, tad lincoln/parents/location is a query q that asks: “Where did Tad Lincoln’s parents live?”._ 
例えば、tad lincoln/parents/location は、タッド・リンカーンの両親はどこに住んでいたのかを尋ねるクエリ q です。
For evaluation (see Section 5 for details), we define the set of candidate answers to a query (q) _C_ as the set of all entities that “type match”, namely those that participate in the final relation of q at least once; and let (q) be the incorrect answers: _N_ 
評価のために（詳細はセクション5を参照）、クエリ (q) に対する候補回答の集合 _C_ を「タイプマッチ」するすべてのエンティティの集合、すなわち、q の最終関係に少なくとも1回参加するエンティティの集合として定義し、(q) を不正解の回答とします：_N_

$$
_C (s/r1/ · · · /rk)_ [def]= {t | ∃e, (e, rk, t) ∈G} (3) 
$$

$$
(q) [def]= (q) _q_ _._ (4) _N_ _C_ _\�_ � 
$$

**Knowledge base completion.** Knowledge base completion (KBC) is the task of predicting whether a given edge (s, r, t) belongs in the graph or not. 
**知識ベース補完。** 知識ベース補完（KBC）は、与えられたエッジ (s, r, t) がグラフに属するかどうかを予測するタスクです。
This can be formulated as a path query _q = s/r with candidate answer t._ 
これは、候補回答 t を持つパスクエリ _q = s/r_ として定式化できます。

### 3 Compositionalization 構成化

In this section, we show how to compositionalize existing KBC models to answer path queries. 
このセクションでは、既存のKBCモデルを構成化してパスクエリに答える方法を示します。
We start with a motivating example in Section 3.1, then present the general technique in Section 3.2. 
セクション3.1で動機付けの例を示し、次にセクション3.2で一般的な手法を提示します。
This suggests a new compositional training objective, described in Section 3.3. 
これにより、セクション3.3で説明する新しい構成的トレーニング目的が示唆されます。
Finally, we illustrate the technique for several more models in Section 3.4, which we use in our experiments. 
最後に、セクション3.4でいくつかのモデルに対する手法を示し、これを実験に使用します。

**3.1** **Example 例**

A common vector space model for knowledge base completion is the bilinear model (Nickel et al., 2011). 
知識ベース補完の一般的なベクトル空間モデルは、バイリニアモデル（Nickel et al., 2011）です。
In this model, we learn a vector $x_e \in R^{[d]}$ for each entity $e \in E$ and a matrix $W_r \in R^{[d] \times [d]}$ for each relation $r$. 
このモデルでは、各エンティティ $e \in E$ に対してベクトル $x_e \in R^{[d]}$ を学習し、各関係 $r$ に対して行列 $W_r \in R^{[d] \times [d]}$ を学習します。
Given a query $s/r$ (asking for the set of entities connected to $s$ via relation $r$), the bilinear model scores how likely $t \in \mathcal{E}$ holds using 
クエリ $s/r$（関係 $r$ を介して $s$ に接続されているエンティティの集合を尋ねる）を与えると、バイリニアモデルは $t \in \mathcal{E}$ が成り立つ可能性を次のようにスコアリングします：

$$
\text{score}(s/r, t) = x_s^{\top} W_r x_t. 
$$ (5)

To motivate our compositionalization technique, take $d = |E|$ and suppose $W_r$ is the adjacency matrix for relation $r$ and entity vector $x_e$ is the indicator vector with a 1 in the entry corresponding to entity $e$. 
私たちの構成化手法を動機付けるために、$d = |E|$ とし、$W_r$ が関係 $r$ の隣接行列であり、エンティティベクトル $x_e$ がエンティティ $e$ に対応するエントリに1を持つインジケータベクトルであると仮定します。
Then, to answer a path query $q = s/r_1/ . . . /r_k$, we would then compute 
次に、パスクエリ $q = s/r_1/ . . . /r_k$ に答えるために、次のように計算します：

$$
\text{score}(q, t) = x_s^{\top} W_{r_1} \cdots W_{r_k} x_t. 
$$ (6)

It is easy to verify that the score counts the number of unique paths between $s$ and $t$ following relations $r_1/ . . . /r_k$. 
このスコアは、関係 $r_1/ . . . /r_k$ に従って $s$ と $t$ の間のユニークなパスの数をカウントすることが簡単に確認できます。
Hence, any $t$ with positive score is a correct answer ($q = t : \text{score}(q, t) > 0$). 
したがって、正のスコアを持つ任意の $t$ は正しい回答です（$q = t : \text{score}(q, t) > 0$）。
Let us interpret (6) recursively. 
式 (6) を再帰的に解釈してみましょう。
The model begins with an entity vector $x_s$, and sequentially applies traversal operators $T_{r_i}(v) = v^{\top} W_{r_i}$ for each $r_i$. 
モデルはエンティティベクトル $x_s$ から始まり、各 $r_i$ に対してトラバースオペレーター $T_{r_i}(v) = v^{\top} W_{r_i}$ を順次適用します。
Each traversal operation results in a new “set vector” representing the entities reached at that point in traversal (corresponding to the nonzero entries of the set vector). 
各トラバース操作は、その時点で到達したエンティティを表す新しい「集合ベクトル」を生成します（集合ベクトルの非ゼロエントリに対応します）。
Finally, it applies the membership operator $M(v, x_t) = v^{\top} x_t$ to check if $t \in \{s/r_1/ . . . /r_k\}$. 
最後に、メンバーシップオペレーター $M(v, x_t) = v^{\top} x_t$ を適用して、$t \in \{s/r_1/ . . . /r_k\}$ であるかどうかを確認します。
Writing graph traversal in this way immediately suggests a useful generalization: take $d$ much smaller than $|E|$ and learn the parameters $W_r$ and $x_e$. 
このようにグラフトラバースを記述することで、役立つ一般化がすぐに示唆されます：$d$ を $|E|$ よりもはるかに小さくし、パラメータ $W_r$ と $x_e$ を学習します。

**3.2** **General technique 一般的な手法**

The strategy used to extend the bilinear model of (5) to the compositional model in (6) can be applied to any composable model: namely, one that 
式 (5) のバイリニアモデルを式 (6) の構成モデルに拡張するために使用される戦略は、任意の構成可能なモデルに適用できます：すなわち、

$$
\text{score}(s/r, t) = M(T_r(x_s), x_t) 
$$ (7)

for some choice of membership operator $M : R^{[d]} \times R^{[d]} \to R$ and traversal operator $T_r : R^{[d]} \to R^{[d]}$. 
メンバーシップオペレーター $M : R^{[d]} \times R^{[d]} \to R$ とトラバースオペレーター $T_r : R^{[d]} \to R^{[d]}$ のいずれかの選択に対して。
We can now define the vector denotation of a query $\hat{q}^V$ analogous to the definition of $q$ in (1) and (2): 
ここで、クエリのベクトル表記 $\hat{q}^V$ を、式 (1) と (2) の $q$ の定義に類似して定義できます：

$$
\hat{s}^V = x_s, 
$$ (8)

$$
\hat{q/r}^V = T_r(\hat{q}^V). 
$$ (9)

The score function for a compositionalized model is then 
構成化されたモデルのスコア関数は次のようになります：

$$
\text{score}(q, t) = M(\hat{q}^V, \hat{t}^V). 
$$ (10)

We would like $\hat{q}^V$ to approximately represent the set $q$ in the sense that for every $e \in q$, $M(\hat{q}^V, \hat{e}^V)$ is larger than the values for $e \notin q$. 
私たちは、$\hat{q}^V$ が $q$ の集合を近似的に表現することを望みます。すなわち、$e \in q$ のすべてに対して、$M(\hat{q}^V, \hat{e}^V)$ が $e \notin q$ の値よりも大きくなるようにします。
Of course it is not possible to represent all $\hat{q}$ sets perfectly, but in the next section, we present a training objective that explicitly optimizes $T$ and $M$ to preserve path information. 
もちろん、すべての $\hat{q}$ の集合を完璧に表現することは不可能ですが、次のセクションでは、パス情報を保持するために $T$ と $M$ を明示的に最適化するトレーニング目的を提示します。

**3.3** **Compositional training 構成的トレーニング**

The score function in (10) naturally suggests a new compositional training objective. 
式 (10) のスコア関数は、新しい構成的トレーニング目的を自然に示唆します。
Let $\{(q_i, t_i)\}_{i=1}^N$ denote a set of path query training examples with path lengths ranging from 1 to $L$. 
$\{(q_i, t_i)\}_{i=1}^N$ を、パスの長さが1から $L$ までの範囲のパスクエリのトレーニング例の集合とします。
We minimize the following max-margin objective: 
次の最大マージン目的を最小化します：

$$
\sum_{t' \in N(q_i)} \max(0, 1 - \text{margin}(q_i, t_i, t')) 
$$

$$
\text{margin}(q, t, t') = \text{score}(q, t) - \text{score}(q, t'), 
$$

where the parameters are the membership operator, the traversal operators, and the entity vectors: 
ここで、パラメータはメンバーシップオペレーター、トラバースオペレーター、およびエンティティベクトルです：

$$
\Theta = \{M\} \cup \{T_r : r \in R\} \cup \{x_e \in R^{[d]} : e \in E\}. 
$$

This objective encourages the construction of “set vectors”: because there are path queries of different lengths and types, the model must learn to produce an accurate set vector $\hat{q}^V$ after any sequence of traversals. 
この目的は「集合ベクトル」の構築を促進します：異なる長さとタイプのパスクエリがあるため、モデルは任意のトラバースのシーケンスの後に正確な集合ベクトル $\hat{q}^V$ を生成することを学ばなければなりません。
Another perspective is that each traversal operator is trained such that its transformation preserves information in the set vector which might be needed in subsequent traversal steps. 
別の視点として、各トラバースオペレーターは、その変換が次のトラバースステップで必要となる可能性のある集合ベクトル内の情報を保持するように訓練されます。
In contrast, previously proposed training objectives for knowledge base completion only train on 
対照的に、以前に提案された知識ベース補完のトレーニング目的は、のみ訓練します。



queries of path length 1. We will refer to this special case as single-edge training.
パスの長さが1のクエリ。私たちはこの特別なケースをシングルエッジトレーニングと呼びます。
In Section 5, we show that compositional training leads to substantially better results for both path query answering and knowledge base completion. 
第5節では、構成トレーニングがパスクエリ応答と知識ベースの補完の両方において、実質的により良い結果をもたらすことを示します。
In Section 6, we provide insight into why.
第6節では、その理由についての洞察を提供します。

**3.4** **Other composable models**
**3.4** **他の合成可能なモデル**
There are many possible candidates for T and M.
TとMの候補は多くあります。
For example, T could be one’s favorite neural network mapping from R[d] to R[d]. 
例えば、TはR[d]からR[d]へのお気に入りのニューラルネットワークマッピングである可能性があります。
Here, we focus on two composable models that were both recently shown to achieve state-of-the-art performance on knowledge base completion.
ここでは、知識ベースの補完において最先端の性能を達成することが最近示された2つの合成可能なモデルに焦点を当てます。

**TransE.** The TransE model of Bordes et al. (2013) uses the scoring function
**TransE.** Bordesら（2013）のTransEモデルは、スコアリング関数を使用します。
$$
score(s/r, t) = -\|x_s + w_r - \tilde{x_t}\|^2_2
$$
ここで、$x_s$, $w_r$、および$x_t$はすべてd次元ベクトルです。
In this case, the model can be expressed using membership operator
この場合、モデルはメンバーシップ演算子を使用して表現できます。
$$
M(v, \tilde{x_t}) = -\|v - \tilde{x_t}\|^2_2
$$
and traversal operator $Tr(x_s) = \tilde{x_s} + w_r.$ 
およびトラバーサル演算子 $Tr(x_s) = \tilde{x_s} + w_r.$ 
Hence, TransE can handle a path query $q = \tilde{s}/r_1/r_2/ \cdots /r_k$ using
したがって、TransEはパスクエリ $q = \tilde{s}/r_1/r_2/ \cdots /r_k$ を次のように処理できます。
$$
score(q, t) = -\|x_s + w_{r_1} + \cdots + w_{r_k} - \tilde{x_t}\|^2_2
$$
We visualize the compositional TransE model in Figure 2.
私たちは、図2に構成TransEモデルを視覚化します。

**Bilinear-Diag.** The Bilinear-Diag model of Yang et al. (2015) is a special case of the bilinear model with the relation matrices constrained to be diagonal. 
**Bilinear-Diag.** Yangら（2015）のBilinear-Diagモデルは、関係行列が対角に制約されたバイリニアモデルの特別なケースです。
Alternatively, the model can be viewed as a variant of TransE with multiplicative interactions between entity and relation vectors.
あるいは、このモデルはエンティティと関係ベクトル間の乗法的相互作用を持つTransEの変種として見ることができます。

**Not all models can be compositionalized.** 
**すべてのモデルが合成可能であるわけではありません。**
It is important to point out that some models are not naturally composable—for example, the latent feature model of Riedel et al. (2013) and the neural tensor network of Socher et al. (2013). 
いくつかのモデルは自然に合成可能ではないことを指摘することが重要です。例えば、Riedelら（2013）の潜在特徴モデルやSocherら（2013）のニューラルテンソルネットワークです。
These approaches have scoring functions which combine $s$, $r$ and $t$ in a way that does not involve an intermediate vector representing $s/r$ alone without $t$, so they do not decompose according to (7).
これらのアプローチは、$s$, $r$、および$t$を中間ベクトルを介さずに組み合わせるスコアリング関数を持っているため、（7）に従って分解されません。

-----
Table 1: WordNet and Freebase statistics for base and path query datasets.
表1: 基本およびパスクエリデータセットのWordNetおよびFreebaseの統計。

**3.5** **Implementation**
**3.5** **実装**
We use AdaGrad (Duchi et al., 2010) to optimize $J(\Theta)$, which is in general non-convex.
私たちは、一般に非凸である$J(\Theta)$を最適化するためにAdaGrad（Duchiら、2010）を使用します。
Initialization scale, mini-batch size and step size were cross-validated for all models. 
初期化スケール、ミニバッチサイズ、およびステップサイズはすべてのモデルでクロスバリデーションされました。
We initialize all parameters with i.i.d. Gaussians of variance 0.1 in every entry, use a mini-batch size of 300 examples, and a step size in [0.001, 0.1] (chosen via crossvalidation) for all of the models. 
すべてのパラメータを各エントリで分散0.1のi.i.d.ガウス分布で初期化し、ミニバッチサイズを300例、すべてのモデルに対してクロスバリデーションで選択された[0.001, 0.1]の範囲のステップサイズを使用します。
For each example $q$, we sample 10 negative entities $t^{\prime}(q) \in N$.
各例$q$について、10の負のエンティティ$t^{\prime}(q) \in N$をサンプリングします。
During training, all of the entity vectors are constrained to lie on the unit ball, and we clipped the gradients to the median of the observed gradients if the update exceeded 3 times the median.
トレーニング中、すべてのエンティティベクトルは単位球に制約され、更新が中央値の3倍を超えた場合は、観測された勾配の中央値に勾配をクリップしました。
We first train on path queries of length 1 until convergence and then train on all path queries until convergence. 
まず、収束するまで長さ1のパスクエリでトレーニングし、その後、すべてのパスクエリで収束するまでトレーニングします。
This guarantees that the model masters basic edges before composing them to form paths. 
これにより、モデルはパスを形成するためにそれらを合成する前に基本的なエッジを習得することが保証されます。
When training on path queries, we explicitly parameterize inverse relations. 
パスクエリのトレーニング時には、逆関係を明示的にパラメータ化します。
For the bilinear model, we initialize $W_{r^{-1}}$ with $W_{r^{\top}}$. 
バイリニアモデルでは、$W_{r^{-1}}$を$W_{r^{\top}}$で初期化します。
For TransE, we initialize $w_{r^{-1}}$ with $-w_r$. 
TransEの場合、$w_{r^{-1}}$を$-w_r$で初期化します。
For Bilinear-Diag, we found initializing $w_{r^{-1}}$ with the exact inverse $1/w_r$ is numerically unstable, so we instead randomly initialize $w_{r^{-1}}$ with i.i.d Gaussians of variance 0.1 in every entry. 
Bilinear-Diagの場合、$w_{r^{-1}}$を正確な逆数$1/w_r$で初期化すると数値的に不安定であることがわかったため、代わりに各エントリで分散0.1のi.i.d.ガウス分布で$w_{r^{-1}}$をランダムに初期化します。
Additionally, for the bilinear model, we replaced the sum over $N(q_i)$ in the objective with a max since it yielded slightly higher accuracy. 
さらに、バイリニアモデルでは、目的関数の$N(q_i)$の合計を最大値に置き換えました。これにより、わずかに精度が向上しました。
Our models are implemented using Theano (Bastien et al., 2012; Bergstra et al., 2010).
私たちのモデルはTheano（Bastienら、2012; Bergstraら、2010）を使用して実装されています。

### 4 Datasets
### 4 データセット
In Section 4.1, we describe two standard knowledge base completion datasets. 
第4.1節では、2つの標準的な知識ベース補完データセットについて説明します。
These consist of single-edge queries, so we call them base datasets.
これらはシングルエッジクエリで構成されているため、基本データセットと呼びます。
In Section 4.2, we generate path query datasets from these base datasets.
第4.2節では、これらの基本データセットからパスクエリデータセットを生成します。

**4.1** **Base datasets**
**4.1** **基本データセット**
Our experiments are conducted using the subsets of WordNet and Freebase from Socher et al. (2013). 
私たちの実験は、Socherら（2013）からのWordNetとFreebaseのサブセットを使用して行われます。
The statistics of these datasets and their splits are given in Table 1.
これらのデータセットの統計とその分割は表1に示されています。
The WordNet and Freebase subsets exhibit substantial differences that can influence model performance. 
WordNetとFreebaseのサブセットは、モデルの性能に影響を与える可能性のある実質的な違いを示しています。
The Freebase subset is almost bipartite with most of the edges taking the form $(s, r, t)$ for some person $s$, relation $r$ and property $t$. 
Freebaseのサブセットはほぼ二部グラフであり、ほとんどのエッジはある人物$s$、関係$r$、およびプロパティ$t$の形を取ります。
In WordNet, both the source and target entities are arbitrary words.
WordNetでは、ソースエンティティとターゲットエンティティの両方が任意の単語です。
Both the raw WordNet and Freebase contain many relations that are almost perfectly correlated with an inverse relation. 
生のWordNetとFreebaseの両方には、逆関係とほぼ完全に相関する多くの関係が含まれています。
For example, WordNet contains both has part and part of, and Freebase contains both parents and children. 
例えば、WordNetには「has part」と「part of」の両方が含まれ、Freebaseには「parents」と「children」の両方が含まれています。
At test time, a query on an edge $(s, r, t)$ is easy to answer if the inverse triple $(t, r^{-1}, s)$ was observed in the training set. 
テスト時に、エッジ$(s, r, t)$に対するクエリは、逆三重項$(t, r^{-1}, s)$がトレーニングセットで観察されていれば簡単に回答できます。
Following Socher et al. (2013), we account for this by excluding such “trivial” queries from the test set.
Socherら（2013）に従い、私たちはこのような「自明な」クエリをテストセットから除外することによって考慮します。

**4.2** **Path query datasets**
**4.2** **パスクエリデータセット**
Given a base knowledge graph, we generate path queries by performing random walks on the graph.
基本的な知識グラフが与えられた場合、グラフ上でランダムウォークを行うことによってパスクエリを生成します。
If we view compositional training as a form of regularization, this approach allows us to generate extremely large amounts of auxiliary training data.
構成トレーニングを正則化の一形態と見なすと、このアプローチは非常に大量の補助トレーニングデータを生成することを可能にします。
The procedure is given below.
手順は以下の通りです。
Let $G_{train}$ be the training graph, which consists only of the edges in the training set of the base dataset. 
$G_{train}$をトレーニンググラフとし、これは基本データセットのトレーニングセットのエッジのみで構成されます。
We then repeatedly generate training examples with the following procedure:
次に、以下の手順でトレーニング例を繰り返し生成します。
1. Uniformly sample a path length $L \in \{1, \ldots, L_{max}\}$, and uniformly sample a starting entity $s \in E$.
1. パスの長さ$L \in \{1, \ldots, L_{max}\}$を一様にサンプリングし、開始エンティティ$s \in E$を一様にサンプリングします。
2. Perform a random walk beginning at entity $s$ and continuing $L$ steps.
2. エンティティ$s$から始めてランダムウォークを行い、$L$ステップ続けます。
(a) At step $i$ of the walk, choose a relation $r_i$ uniformly from the set of relations incident on the current entity $e$.
(a) ウォークのステップ$i$で、現在のエンティティ$e$に接続された関係のセットから関係$r_i$を一様に選択します。
(b) Choose the next entity uniformly from the set of entities reachable via $r_i$.
(b) $r_i$を介して到達可能なエンティティのセットから次のエンティティを一様に選択します。
3. Output a query-answer pair, $(q, t)$, where $q = \tilde{s}/r_1/ \cdots /r_L$ and $t$ is the final entity of the random walk.
3. クエリ-回答ペア$(q, t)$を出力します。ここで、$q = \tilde{s}/r_1/ \cdots /r_L$であり、$t$はランダムウォークの最終エンティティです。

-----
In practice, we do not sample paths of length 1 and instead directly add all of the edges from $G_{train}$ to the path query dataset.
実際には、長さ1のパスをサンプリングせず、$G_{train}$からのすべてのエッジをパスクエリデータセットに直接追加します。
To generate a path query test set, we repeat the above procedure except using the graph $G_{full}$, which is $G_{train}$ plus all of the test edges from the base dataset. 
パスクエリテストセットを生成するために、上記の手順を繰り返しますが、グラフ$G_{full}$を使用します。これは$G_{train}$に基本データセットからのすべてのテストエッジを加えたものです。
Then we remove any queries from the test set that also appeared in the training set.
次に、トレーニングセットにも出現したクエリをテストセットから削除します。
The statistics for the path query datasets are presented in Table 1.
パスクエリデータセットの統計は表1に示されています。

### 5 Main results
### 5 主な結果
We evaluate the models derived in Section 3 on two tasks: path query answering and knowledge base completion. 
第3節で導出されたモデルを2つのタスク、すなわちパスクエリ応答と知識ベースの補完で評価します。
On both tasks, we show that the compositional training strategy proposed in Section 3.3 leads to substantial performance gains over standard single-edge training. 
両方のタスクにおいて、私たちは第3.3節で提案された構成トレーニング戦略が標準的なシングルエッジトレーニングに対して実質的な性能向上をもたらすことを示します。
We also compare directly against the KBC results of Socher et al. (2013), demonstrating that previously inferior models now match or outperform state-of-the-art models after compositional training.
また、Socherら（2013）のKBC結果と直接比較し、以前は劣っていたモデルが構成トレーニング後に最先端のモデルと同等またはそれを上回ることを示します。

**Evaluation metric.** 
**評価指標。**
Numerous metrics have been used to evaluate knowledge base queries, including hits at 10 (percentage of correct answers ranked in the top 10) and mean rank. 
知識ベースクエリを評価するために、ヒット数（上位10位にランク付けされた正しい回答の割合）や平均ランクなど、さまざまな指標が使用されています。
We evaluate on hits at 10, as well as a normalized version of mean rank, mean quantile, which better accounts for the total number of candidates. 
私たちは、ヒット数10で評価し、候補の総数をよりよく考慮する平均ランクの正規化バージョンである平均分位数でも評価します。
For a query $q$, the quantile of a correct answer $t$ is the fraction of incorrect answers ranked after $t$:
クエリ$q$に対して、正しい回答$t$の分位数は、$t$の後にランク付けされた不正解の回答の割合です。
$$
t^{\prime}(q) : score(q, t^{\prime}) < score(q, t) \bigg| \{ t^{\prime} \in N \} \bigg| 
$$
$$
\frac{|N(q)|}{|N|} 
$$
The quantile ranges from 0 to 1, with 1 being optimal. 
分位数は0から1の範囲で、1が最適です。
Mean quantile is then defined to be the average quantile score over all examples in the dataset.
平均分位数は、データセット内のすべての例に対する平均分位数スコアとして定義されます。
To illustrate why normalization is important, consider a set of queries on the relation gender. 
正規化が重要である理由を示すために、性別に関する一連のクエリを考えてみましょう。
A model that predicts the incorrect gender on every query would receive a mean rank of 2 (since there are only 2 candidate answers), which is fairly good in absolute terms, whereas the mean quantile would be 0, rightfully penalizing the model.
すべてのクエリで不正確な性別を予測するモデルは、平均ランクが2（候補回答が2つしかないため）となり、絶対的にはかなり良いですが、平均分位数は0となり、モデルに対して正当にペナルティを与えます。
As a final note, several of the queries in the Freebase path dataset are “type-match trivial” in the sense that all of the type matching candidates $(q)$ are correct answers to the query. 
最後に、Freebaseパスデータセットのいくつかのクエリは、「タイプマッチ自明」であり、すべてのタイプマッチ候補$(q)$がクエリに対する正しい回答であるという意味です。
In this case, mean quantile is undefined and we exclude such queries from evaluation.
この場合、平均分位数は未定義であり、そのようなクエリは評価から除外します。



**Overview.** 
**概要。** 

The upper half of Table 2 shows that compositional training improves path querying performance across all models and metrics on both datasets, reducing error by up to 76.2%. 
表2の上半分は、構成的トレーニングが両方のデータセットにおいてすべてのモデルと指標でパスクエリのパフォーマンスを向上させ、エラーを最大76.2%削減することを示しています。

The lower half of Table 2 shows that surprisingly, compositional training also improves performance on knowledge base completion across almost all models, metrics and datasets. 
表2の下半分は、驚くべきことに、構成的トレーニングがほぼすべてのモデル、指標、データセットにおいて知識ベースの補完のパフォーマンスも向上させることを示しています。

On WordNet, TransE benefits the most, with a 43.3% reduction in error. 
WordNetでは、TransEが最も恩恵を受け、エラーが43.3%削減されます。

On Freebase, Bilinear benefits the most, with a 38.8% reduction in error. 
Freebaseでは、Bilinearが最も恩恵を受け、エラーが38.8%削減されます。

In terms of mean quantile, the best overall model is TransE (COMP). 
平均分位数の観点から、全体で最も優れたモデルはTransE (COMP)です。

In terms of hits at 10, the best model on WordNet is Bilinear (COMP), while the best model on Freebase is TransE (COMP). 
ヒット数10の観点から、WordNetでの最良モデルはBilinear (COMP)であり、Freebaseでの最良モデルはTransE (COMP)です。

**Deduction and Induction.** 
**推論と帰納。** 

Table 3 takes a deeper look at performance on path query answering. 
表3は、パスクエリ応答のパフォーマンスをより深く見ています。

We divided path queries into two subsets: deduction and induction. 
私たちはパスクエリを推論と帰納の2つのサブセットに分けました。

The deduction subset consists of queries q = s/p where the source and target entities _q_ are connected via relations p in the training graph Gtrain, but the specific query q was never seen during training. 
推論サブセットは、ソースとターゲットエンティティ_q_がトレーニンググラフGtrain内の関係pを介して接続されているクエリq = s/pで構成されますが、特定のクエリqはトレーニング中に一度も見られませんでした。

Such queries can be answered by performing explicit traversal on the training graph, so this subset tests a model’s ability to approximate the underlying training graph and predict the existence of a path from a collection of single edges. 
このようなクエリはトレーニンググラフ上で明示的なトラバーサルを行うことで回答できるため、このサブセットはモデルが基盤となるトレーニンググラフを近似し、単一のエッジの集合からパスの存在を予測する能力をテストします。

The induction subset consists of all other queries. 
帰納サブセットは他のすべてのクエリで構成されています。

This means that at least one edge was missing on all paths following p from source to target in the training graph. 
これは、トレーニンググラフ内のソースからターゲットへのすべてのパスにおいて、少なくとも1つのエッジが欠落していることを意味します。

Hence, this subset tests a model’s generalization ability and its robustness to missing edges. 
したがって、このサブセットはモデルの一般化能力と欠落したエッジに対する堅牢性をテストします。

Performance on the deduction subset of the dataset is disappointingly low for models trained with single-edge training: they struggle to answer path queries even when all edges in the path query have been seen at training time. 
データセットの推論サブセットにおけるパフォーマンスは、単一エッジトレーニングで訓練されたモデルにとって残念ながら低いです：彼らはパスクエリに回答するのに苦労し、パスクエリ内のすべてのエッジがトレーニング時に見られた場合でもそうです。

Compositional training dramatically reduces these errors, sometimes doubling mean quantile. 
構成的トレーニングはこれらのエラーを劇的に削減し、時には平均分位数を倍増させます。

In Section 6, we analyze how this might be possible. 
セクション6では、これがどのように可能であるかを分析します。

After compositional training, performance on the harder induction subset is also much stronger. 
構成的トレーニングの後、より難しい帰納サブセットにおけるパフォーマンスもはるかに強力です。

Even when edges are missing along a path, the models are able to infer them. 
パスに沿ってエッジが欠落している場合でも、モデルはそれらを推測することができます。

**Interpretable queries.** 
**解釈可能なクエリ。** 

Although our path datasets consists of random queries, both datasets contain a large number of useful, interpretable queries. 
私たちのパスデータセットはランダムなクエリで構成されていますが、両方のデータセットには多くの有用で解釈可能なクエリが含まれています。

Results on a few illustrative examples are shown in Table 4. 
いくつかの例を示した結果は表4に示されています。

-----
**Bilinear** **Bilinear-Diag** **TransE** 
**Bilinear** **Bilinear-Diag** **TransE** 

**Path query task** SINGLE COMP (%red) SINGLE COMP (%red) SINGLE COMP (%red) 
**パスクエリタスク** SINGLE COMP (%red) SINGLE COMP (%red) SINGLE COMP (%red) 

MQ 84.7 89.4 **30.7** 59.7 90.4 **76.2** 83.7 93.3 **58.9** 
MQ 84.7 89.4 **30.7** 59.7 90.4 **76.2** 83.7 93.3 **58.9** 

WordNet H@10 43.6 54.3 **19.0** 7.9 31.1 **25.4** 13.8 43.5 **34.5** 
WordNet H@10 43.6 54.3 **19.0** 7.9 31.1 **25.4** 13.8 43.5 **34.5** 

MQ 58.0 83.5 **60.7** 57.9 84.8 **63.9** 86.2 88 **13.0** 
MQ 58.0 83.5 **60.7** 57.9 84.8 **63.9** 86.2 88 **13.0** 

Freebase H@10 25.9 42.1 **21.9** 23.1 38.6 **20.2** 45.4 50.5 **9.3** 
Freebase H@10 25.9 42.1 **21.9** 23.1 38.6 **20.2** 45.4 50.5 **9.3** 

**KBC task** SINGLE COMP (%red) SINGLE COMP (%red) SINGLE COMP (%red) 
**KBCタスク** SINGLE COMP (%red) SINGLE COMP (%red) SINGLE COMP (%red) 

MQ 76.1 82.0 **24.7** 76.5 84.3 **33.2** 75.5 86.1 **43.3** 
MQ 76.1 82.0 **24.7** 76.5 84.3 **33.2** 75.5 86.1 **43.3** 

WordNet H@10 19.2 27.3 **10.0** 12.9 14.4 **1.72** 4.6 16.5 **12.5** 
WordNet H@10 19.2 27.3 **10.0** 12.9 14.4 **1.72** 4.6 16.5 **12.5** 

MQ 85.3 91.0 **38.8** 84.6 89.1 **29.2** 92.7 92.8 **1.37** 
MQ 85.3 91.0 **38.8** 84.6 89.1 **29.2** 92.7 92.8 **1.37** 

Freebase H@10 70.2 76.4 **20.8** 63.2 67.0 **10.3** 78.8 78.6 -0.9 
Freebase H@10 70.2 76.4 **20.8** 63.2 67.0 **10.3** 78.8 78.6 -0.9 

Table 2: Path query answering and knowledge base completion. 
表2: パスクエリ応答と知識ベースの補完。 

We compare the performance of single-edge training (SINGLE) vs compositional training (COMP). 
単一エッジトレーニング（SINGLE）と構成的トレーニング（COMP）のパフォーマンスを比較します。 

MQ: mean quantile, H@10: hits at 10, %red: percentage reduction in error. 
MQ: 平均分位数、H@10: ヒット数10、%red: エラーの削減率。 

**Interpretable Queries** 
**解釈可能なクエリ** 

Bilinear SINGLE Bilinear COMP 
Bilinear SINGLE Bilinear COMP 

`X/institution/institution[−][1]/profession` 50.0 **93.6** 
`X/institution/institution[−][1]/profession` 50.0 **93.6** 

`X/parents/religion` 81.9 **97.1** 
`X/parents/religion` 81.9 **97.1** 

`X/nationality/nationality[−][1]/ethnicity[−][1]` 68.0 **87.0** 
`X/nationality/nationality[−][1]/ethnicity[−][1]` 68.0 **87.0** 

`X/has part/has instance[−][1]` 92.6 **95.1** 
`X/has part/has instance[−][1]` 92.6 **95.1** 

`X/type of/type of/type of` 72.8 **79.4** 
`X/type of/type of/type of` 72.8 **79.4** 

Table 4: Path query performance (mean quantile) on a selection of interpretable queries. 
表4: 解釈可能なクエリの選択におけるパスクエリパフォーマンス（平均分位数）。 

We compare Bilinear SINGLE and Bilinear COMP. 
Bilinear SINGLEとBilinear COMPを比較します。 

Meanings of each query (descending): “What professions are there at X’s institution?”; “What is the religion of X’s parents?”; “What are the ethnicities of people from the same country as X?”; “What types of parts does X have?”; and the transitive “What is X a type of?”. 
各クエリの意味（降順）: 「Xの機関にはどのような職業がありますか？」; 「Xの両親の宗教は何ですか？」; 「Xと同じ国の人々の民族は何ですか？」; 「Xにはどのような部品がありますか？」; そして推移的な「Xは何のタイプですか？」。 

(Note that a relation r and its inverse r[−][1] do not necessarily cancel out if r is not a one-to-one mapping. 
（関係rとその逆r[−][1]は、rが一対一のマッピングでない場合、必ずしも相殺されるわけではありません。 

For example, X/institution/institution[−][1] denotes the set of all people who work at the institution X works at, which is not just X.) 
例えば、X/institution/institution[−][1]は、Xが働いている機関で働いているすべての人々の集合を示し、Xだけではありません。） 

|Bilinear|Bilinear-Diag| 
|---|---| 
|SINGLE COMP (%red)|SINGLE COMP (%red)| 
|84.7 89.4 30.7 43.6 54.3 19.0 58.0 83.5 60.7 25.9 42.1 21.9|59.7 90.4 76.2 7.9 31.1 25.4 57.9 84.8 63.9 23.1 38.6 20.2| 
|SINGLE COMP (%red)|SINGLE COMP (%red)| 

Table 3: Deduction and induction. 
表3: 推論と帰納。 

We compare mean quantile performance of single-edge training (SINGLE) vs compositional training (COMP). 
単一エッジトレーニング（SINGLE）と構成的トレーニング（COMP）の平均分位数パフォーマンスを比較します。 

Length 1 queries are excluded. 
長さ1のクエリは除外されています。 

**Comparison with Socher et al. (2013).** 
**Socher et al. (2013)との比較。** 

Here, we measure performance on the KBC task in terms of the accuracy metric of Socher et al. (2013). 
ここでは、Socher et al. (2013)の精度指標に基づいてKBCタスクのパフォーマンスを測定します。 

This evaluation involves sampled negatives, and is hence noisier than mean quantile, but makes our results directly comparable to Socher et al. (2013). 
この評価はサンプリングされたネガティブを含み、したがって平均分位数よりもノイズが多いですが、私たちの結果をSocher et al. (2013)と直接比較可能にします。 

Our results show that previously inferior models such as the bilinear model can outperform state-of-the-art models after compositional training. 
私たちの結果は、以前は劣っていたモデル（例えば、バイリニアモデル）が構成的トレーニングの後に最先端のモデルを上回ることができることを示しています。 

Socher et al. (2013) proposed parametrizing each entity vector as the average of vectors of words in the entity (wtad lincoln = 12 [(][w][tad][ +] _wlincoln), and pretraining these word vectors using the method of Turian et al. (2010). 
Socher et al. (2013)は、各エンティティベクトルをエンティティ内の単語のベクトルの平均としてパラメータ化し（wtad lincoln = 12 [(][w][tad][ +] _wlincoln）、Turian et al. (2010)の方法を使用してこれらの単語ベクトルを事前トレーニングすることを提案しました。 

Table 5 reports results when using this approach in conjunction with compositional training. 
表5は、このアプローチを構成的トレーニングと組み合わせて使用した場合の結果を報告します。 

We initialized all models with word vectors from Pennington et al. (2014). 
私たちはすべてのモデルをPennington et al. (2014)の単語ベクトルで初期化しました。 

We found that compositionally trained models outperform the neural tensor network (NTN) on WordNet, while being only slightly behind on Freebase. 
構成的にトレーニングされたモデルはWordNetでニューラルテンソルネットワーク（NTN）を上回り、Freebaseではわずかに劣っていることがわかりました。 

(We did not use word vectors in any of our other experiments.) 
（私たちは他の実験では単語ベクトルを使用しませんでした。） 

When the strategy of averaging word vectors to form entity vectors is not applied, our compositional models are significantly better on WordNet and slightly better on Freebase. 
単語ベクトルを平均化してエンティティベクトルを形成する戦略が適用されない場合、私たちの構成モデルはWordNetで著しく優れており、Freebaseでもわずかに優れています。 

It is worth noting that in many domains, entity names are not lexically meaningful, so word vector averaging is not always meaningful. 
多くのドメインでは、エンティティ名が語彙的に意味を持たないため、単語ベクトルの平均化が常に意味を持つわけではないことに注意する価値があります。 

### 6 Analysis 
### 6 分析 

In this section, we try to understand why compositional training is effective. 
このセクションでは、なぜ構成的トレーニングが効果的であるかを理解しようとします。 

For concreteness, everything is described in terms of the bilinear model. 
具体的には、すべてはバイリニアモデルの観点から説明されます。 

We will refer to the compositionally trained model as COMP, and the model trained with single-edge training as SINGLE. 
構成的にトレーニングされたモデルをCOMPと呼び、単一エッジトレーニングでトレーニングされたモデルをSINGLEと呼びます。 

**6.1 Why does compositional training improve path query answering?** 
**6.1 なぜ構成的トレーニングはパスクエリ応答を改善するのか？** 

It is tempting to think that if SINGLE has accurately modeled individual edges in a graph, it should accurately model the paths that result from those edges. 
SINGLEがグラフ内の個々のエッジを正確にモデル化している場合、それに基づくパスを正確にモデル化すべきだと考えるのは魅力的です。 

This intuition turns out to be incorrect, as revealed by SINGLE’s relatively weak performance on the path query dataset. 
この直感は間違っていることが判明し、SINGLEのパスクエリデータセットにおける比較的弱いパフォーマンスによって明らかになりました。 

We hypothesize that this is due to cascading errors along the path. 
私たちは、これはパスに沿ったカスケードエラーによるものであると仮定します。 

For a given edge (s, r, t) on the path, single-edge training encourages xt to be closer to x[⊤]s _[W][r]_ [than any] other incorrect xt′. 
パス上の特定のエッジ(s, r, t)に対して、単一エッジトレーニングはxtが他の不正確なxt′よりもx[⊤]s _[W][r]_ に近くなるように促します。 

However, once this is achieved by a margin of 1, it does not push xt any closer to _x[⊤]s_ _[W][r][. 
しかし、これが1のマージンで達成されると、xtを_x[⊤]s_ _[W][r][にさらに近づけることはありません。 

The remaining discrepancy is noise which gets added at each step of path traversal. 
残りの不一致は、パスのトラバーサルの各ステップで追加されるノイズです。 

This is illustrated schematically in Figure 2. 
これは図2に概念的に示されています。 

To observe this phenomenon empirically, we examine how well a model handles each intermediate step of a path query. 
この現象を実証的に観察するために、モデルがパスクエリの各中間ステップをどれだけうまく処理できるかを調べます。 

We can do this by measuring the reconstruction quality (RQ) of the set vector produced after each traversal operation. 
これは、各トラバーサル操作の後に生成されるセットベクトルの再構成品質（RQ）を測定することで行えます。 

Since each intermediate stage is itself a valid path query, we define RQ to be the average quantile over all entities that belong in _q_: 
各中間段階はそれ自体が有効なパスクエリであるため、RQを_q_に属するすべてのエンティティの平均分位数として定義します: 

1 RQ (q) = 
_q_ _|�_ �| 
�
quantile (q, t) (14) _t∈�q�_ 

Figure 2: **Cascading errors visualized for TransE.** 
図2: **TransEのカスケードエラーの視覚化。** 

Each node represents the position of an entity in vector space. 
各ノードはベクトル空間内のエンティティの位置を表します。 

The relation parent is ideally a simple horizontal translation, but each traversal introduces noise. 
関係parentは理想的には単純な水平移動ですが、各トラバーサルはノイズを導入します。 

The red circle is where we expect Tad’s parent to be. 
赤い円は、私たちがTadの親がいると期待する場所です。 

The red square is where we expect Tad’s grandparent to be. 
赤い四角は、私たちがTadの祖父母がいると期待する場所です。 

Dotted red lines show that error grows larger as we traverse farther away from Tad. 
点線の赤い線は、Tadから遠くに移動するにつれてエラーが大きくなることを示しています。 

Compositional training pulls the entity vectors closer to the ideal arrangement. 
構成的トレーニングはエンティティベクトルを理想的な配置に近づけます。 

Given the nature of cascading errors, it might seem reasonable to address the problem by adding a term to our objective which explicitly encourages x[⊤]s _[W][r]_ [to be as close as possible to][ x][t][. 
カスケードエラーの性質を考えると、x[⊤]s _[W][r]_ [をできるだけ][ x][t][に近づけるように明示的に促す項を目的に追加することで問題に対処するのは合理的に思えるかもしれません。 

With this motivation, we tried adding λ∥x[⊤]s _[W][r]_ _[−]_ _[x][t][∥]2[2]_ term to the objective of the bilinear model and a _λ∥xs + wr −_ _xt∥2[2]_ [term to the objective of TransE.] 
この動機を持って、私たちはバイリニアモデルの目的にλ∥x[⊤]s _[W][r]_ _[−]_ _[x][t][∥]2[2]_項を追加し、TransEの目的に_λ∥xs + wr −_ _xt∥2[2]_項を追加することを試みました。 

We experimented with different settings of λ over the range [0.001, 100]. 
私たちはλの異なる設定を[0.001, 100]の範囲で実験しました。 

In no case did this additional ℓ2 term improve SINGLE’s performance on the path query or single edge dataset. 
この追加のℓ2項がSINGLEのパスクエリまたは単一エッジデータセットにおけるパフォーマンスを改善することはありませんでした。 

These results suggest that compositional training is a more effective way to combat cascading errors. 
これらの結果は、構成的トレーニングがカスケードエラーに対抗するより効果的な方法であることを示唆しています。 

**6.2 Why does compositional training improve knowledge base completion?** 
**6.2 なぜ構成的トレーニングは知識ベースの補完を改善するのか？** 

Table 2 reveals that COMP also performs better on the single-edge task of knowledge base completion. 
表2は、COMPが知識ベースの補完の単一エッジタスクでもより良いパフォーマンスを発揮することを明らかにしています。 

This is somewhat surprising, since SINGLE is trained on a training set which distributionally matches the test set, whereas COMP is not. 
これはやや驚くべきことで、SINGLEはテストセットと分布的に一致するトレーニングセットで訓練されているのに対し、COMPはそうではありません。 

However, COMP’s better performance on path queries suggests that there must be another factor at play. 
しかし、COMPのパスクエリにおけるより良いパフォーマンスは、他に何らかの要因が働いていることを示唆しています。 

At a high level, training on paths must be providing some form of structural regularization which reduces cascading errors. 
高いレベルでは、パスでのトレーニングはカスケードエラーを減少させる何らかの形の構造的正則化を提供しているに違いありません。 

Indeed, paths in a knowledge graph have proven to be important features for predicting the existence of single edges (Lao et al., 2011; Neelakantan et al., 2015). 
実際、知識グラフ内のパスは単一エッジの存在を予測するための重要な特徴であることが証明されています（Lao et al., 2011; Neelakantan et al., 2015）。 

For example, consider the following Horn clause: 
例えば、次のHorn節を考えてみましょう: 

parents (x, y) location (y, z) place of birth (x, z), _∧_ _⇒_ 
parents (x, y) location (y, z) place of birth (x, z), _∧_ _⇒_ 

When all entities in _q_ are ranked above all in the correct entities, RQ is 1. 
_q_内のすべてのエンティティが正しいエンティティ内のすべてのエンティティよりも上位にランク付けされると、RQは1になります。 

In Figure 3, we illustrate how RQ changes over the course of a query. 
図3では、クエリの過程でRQがどのように変化するかを示します。



When all entities in _q_ are ranked above all in the correct entities, RQ is 1. 
クエリ内のすべてのエンティティが正しいエンティティのすべての上にランク付けされると、RQは1になります。

In Figure 3, we illustrate how RQ changes over the course of a query. 
図3では、クエリの過程でRQがどのように変化するかを示します。

$$
\text{Figure 3: Reconstruction quality (RQ) at each step of the query tad lincoln/parents/place of birth/ profession.}
$$
COMP experiences significantly less degradation in RQ as path length increases. 
COMPは、パスの長さが増加するにつれてRQの劣化が著しく少ないです。

Correspondingly, the set of 5 highest scoring entities computed at each step using COMP (green) is significantly more accurate than the set given by SINGLE (blue). 
それに応じて、COMP（緑）を使用して各ステップで計算された5つの最高得点エンティティのセットは、SINGLE（青）によって与えられたセットよりも著しく正確です。

Correct entities are bolded. 
正しいエンティティは太字で示されています。

which states that if x has a parent with location _z, then x has place of birth z. 
これは、xが場所_zを持つ親を持つ場合、xの出生地はzであることを示しています。

The body of the Horn clause expresses a path from x to z. 
Horn節の本体は、xからzへのパスを表現します。

If COMP models the path better, then it should be better able to use that knowledge to infer the head of the Horn clause. 
もしCOMPがパスをより良くモデル化できれば、その知識を利用してHorn節のヘッドを推測する能力が向上するはずです。

More generally, consider Horn clauses of the form p ⇒ _r, where p = r1/ . . . /rk is a path type and r is the relation being predicted. 
より一般的には、p ⇒ _rの形のHorn節を考えます。ここで、p = r1/ . . . /rkはパスタイプで、rは予測される関係です。

Let us focus on Horn clauses with high precision as defined by: 
高精度のHorn節に焦点を当てましょう。これは次のように定義されます：

$$
\text{prec}(p) = \frac{|p \cap r|}{|p|} 
$$
where _p_ is the set of entity pairs connected by p, and similarly for _r_. 
ここで、_p_はpによって接続されたエンティティペアのセットであり、_r_についても同様です。

Intuitively, one way for the model to implicitly learn and exploit such a Horn clause would be to satisfy the following two criteria: 
直感的に、モデルがそのようなHorn節を暗黙的に学習し活用する方法の1つは、次の2つの基準を満たすことです：

1. The model should ensure a consistent spatial relationship between entity pairs that are related by the path type p; that is, keeping _x[⊤]s_ _[W][r]1_ _[. . . W][r]k_ [close to][ x][t] [for][ all][ valid][ (][s, t][)] pairs. 
1. モデルは、パスタイプpによって関連付けられたエンティティペア間の一貫した空間関係を確保する必要があります。つまり、すべての有効な(s, t)ペアについて、_x[⊤]s_ _[W][r]1_ _[. . . W][r]k_を[x][t]の近くに保つことです。

2. The model’s representation of the path type p and relation r should capture that spatial relationship; that is, x[⊤]s _[W][r]1_ _[. . . W][r]k_ _[≈]_ _[x][t]_ [im-] plies x[⊤]s _[W][r]_ _[≈]_ _[x][t][, or simply][ W][r]1_ _[. . . W][r]k_ _[≈]_ _Wr._ 
2. モデルのパスタイプpと関係rの表現は、その空間関係を捉える必要があります。つまり、x[⊤]s _[W][r]1_ _[. . . W][r]k_ _[≈]_ _[x][t]_はx[⊤]s _[W][r]_ _[≈]_ _[x][t]を意味し、単に[ W][r]1_ _[. . . W][r]k_ _[≈]_ _Wr._です。

We have already seen empirically that SINGLE does not meet criterion 1, because cascading errors cause it to put incorrect entity vectors xt′ closer to x[⊤]s _[W][r]1_ _[. . . W][r]k_ [than the correct entity.] 
私たちはすでに経験的に、SINGLEが基準1を満たさないことを見てきました。なぜなら、カスケードエラーが不正確なエンティティベクトルxt′を正しいエンティティよりもx[⊤]s _[W][r]1_ _[. . . W][r]k_に近づけるからです。

COMP mitigates these errors. 
COMPはこれらのエラーを軽減します。

To empirically verify that COMP also does a better job of meeting criterion 2, we perform the following: 
COMPが基準2を満たすのにより良い仕事をしていることを経験的に確認するために、次のことを行います：

for a path type p and relation r, define dist(p, r) to be the angle between their corresponding matrices (treated as vectors in R[d][2]). 
パスタイプpと関係rについて、dist(p, r)をそれらの対応する行列間の角度（R[d][2]のベクトルとして扱う）と定義します。

This is a natural measure because x[⊤]s _[W][r][x][t]_ [computes] the matrix inner product between Wr and xsx[⊤]t [.] 
これは自然な測定基準です。なぜなら、x[⊤]s _[W][r][x][t]_はWrとxsx[⊤]tの間の行列内積を計算するからです。

Hence, any matrix with small distance from Wr will produce nearly the same scores as Wr for the same entity pairs. 
したがって、Wrからの距離が小さい任意の行列は、同じエンティティペアに対してWrとほぼ同じスコアを生成します。

If COMP is better at capturing the correlation between p and r, then we would expect that when prec(p) is high, compositional training should shrink dist(p, r) more. 
もしCOMPがpとrの相関を捉えるのが得意であれば、prec(p)が高いときに、構成的トレーニングがdist(p, r)をより縮小することを期待します。

To confirm this hypothesis, we enumerated over all 676 possible paths of length 2 (including inverted relations), and examined the proportional reduction in dist(p, r) caused by compositional training, 
この仮説を確認するために、長さ2のすべての676の可能なパス（逆関係を含む）を列挙し、構成的トレーニングによって引き起こされるdist(p, r)の比例的な減少を調べました。

$$
\Delta dist(p, r) = \frac{dist_{COMP}(p, r) - dist_{SINGLE}(p, r)}{dist_{SINGLE}(p, r)} 
$$
Figure 4 shows that higher precision paths indeed correspond to larger reductions in dist(p, r). 
図4は、高精度のパスが実際にdist(p, r)の大きな減少に対応することを示しています。

### 7 Related work 関連研究
**Knowledge base completion with vector space models.** 
**ベクトル空間モデルによる知識ベースの補完。**

Many models have been proposed for knowledge base completion, including those reviewed in Section 3.4 (Nickel et al., 2011; Bordes et al., 2013; Yang et al., 2015; Socher et al., 2013). 
知識ベースの補完のために多くのモデルが提案されており、セクション3.4でレビューされたものも含まれています（Nickel et al., 2011; Bordes et al., 2013; Yang et al., 2015; Socher et al., 2013）。

Dong et al. (2014) demonstrated that KBC models can improve the quality of relation extraction by serving as graph-based priors. 
Dong et al.（2014）は、KBCモデルがグラフベースの事前情報として機能することで関係抽出の質を向上させることができることを示しました。

Riedel et al. (2013) showed that such models can be also be directly used for open-domain relation extraction. 
Riedel et al.（2013）は、そのようなモデルがオープンドメインの関係抽出にも直接使用できることを示しました。

Our compositional training technique is an orthogonal improvement that could help any composable model. 
私たちの構成的トレーニング技術は、任意の構成可能なモデルを助けることができる直交的な改善です。

**Distributional compositional semantics.** 
**分布的構成意味論。**

Previous works have explored compositional vector space representations in the context of logic and sentence interpretation. 
以前の研究では、論理や文の解釈の文脈で構成的ベクトル空間表現が探求されてきました。

In Socher et al. (2012), a matrix is associated with each word of a sentence, and can be used to recursively modify the meaning of nearby constituents. 
Socher et al.（2012）では、文の各単語に行列が関連付けられ、近くの構成要素の意味を再帰的に修正するために使用できます。

Grefenstette (2013) explored the ability of tensors to simulate logical calculi. 
Grefenstette（2013）は、テンソルが論理計算をシミュレートする能力を探求しました。

Bowman et al. (2014) showed that recursive neural networks can learn to distinguish important semantic relations. 
Bowman et al.（2014）は、再帰的ニューラルネットワークが重要な意味的関係を区別することを学習できることを示しました。

Socher et al. (2014) found that compositional models were powerful enough to describe and retrieve images. 
Socher et al.（2014）は、構成モデルが画像を記述し取得するのに十分な力を持っていることを発見しました。

We demonstrate that compositional representations are also useful in the context of knowledge base querying and completion. 
私たちは、構成的表現が知識ベースのクエリと補完の文脈でも有用であることを示します。

In the aforementioned work, compositional models produce vectors which represent truth values, sentiment or image features. 
前述の研究では、構成モデルが真理値、感情、または画像の特徴を表すベクトルを生成します。

In our approach, vectors represent sets of entities constituting the denotation of a knowledge base query. 
私たちのアプローチでは、ベクトルは知識ベースのクエリの指示を構成するエンティティのセットを表します。

**Path modeling.** 
**パスモデリング。**

Numerous methods have been proposed to leverage path information for knowledge base completion and question answering. 
知識ベースの補完と質問応答のためにパス情報を活用するために、多くの方法が提案されています。

Nickel et al. (2014) proposed combining low-rank models with sparse path features. 
Nickel et al.（2014）は、低ランクモデルとスパースパス特徴を組み合わせることを提案しました。

Lao and Cohen (2010) used random walks as features and Gardner et al. (2014) extended this approach by using vector space similarity to govern random walk probabilities. 
LaoとCohen（2010）は、特徴としてランダムウォークを使用し、Gardner et al.（2014）は、ベクトル空間の類似性を使用してランダムウォークの確率を制御することでこのアプローチを拡張しました。

Neelakantan et al. (2015) addressed the problem of path sparsity by embedding paths using a recurrent neural network. 
Neelakantan et al.（2015）は、再帰的ニューラルネットワークを使用してパスを埋め込むことでパスのスパース性の問題に対処しました。

Perozzi et al. 
Perozzi et al. 



(2014) sampled random walks on social networks as training examples, with a different goal to classify nodes in the network. 
(2014年)は、ネットワーク内のノードを分類するという異なる目的で、ソーシャルネットワーク上のランダムウォークをトレーニング例としてサンプリングしました。

Bordes et al. (2014) embed paths as a sum of relation vectors for question answering. 
Bordesら（2014）は、質問応答のためにパスを関係ベクトルの和として埋め込みます。

Our approach is unique in modeling the denotation of each intermediate step of a path query, and using this information to regularize the spatial arrangement of entity vectors. 
私たちのアプローチは、パスクエリの各中間ステップの指示をモデル化し、この情報を使用してエンティティベクトルの空間配置を正則化する点で独自です。

### 8 Discussion 議論

We introduced the task of answering path queries on an incomplete knowledge base, and presented a general technique for compositionalizing a broad class of vector space models. 
私たちは、不完全な知識ベースにおけるパスクエリに答えるタスクを導入し、広範なベクトル空間モデルの合成化のための一般的な技術を提示しました。

Our experiments show that compositional training leads to state-of-the-art performance on both path query answering and knowledge base completion. 
私たちの実験は、合成トレーニングがパスクエリ応答と知識ベースの補完の両方で最先端のパフォーマンスをもたらすことを示しています。

There are several key ideas from this paper: regularization by augmenting the dataset with paths, representing sets as low-dimensional vectors in a context-sensitive way, and performing function composition using vectors. 
この論文からのいくつかの重要なアイデアがあります：パスでデータセットを拡張することによる正則化、文脈に敏感な方法で集合を低次元ベクトルとして表現すること、そしてベクトルを使用して関数合成を行うことです。

We believe these three could all have greater applicability in the development of vector space models for knowledge representation and inference. 
私たちは、これらの3つが知識表現と推論のためのベクトル空間モデルの開発において、より大きな適用可能性を持つと信じています。

**Reproducibility 再現性** 

Our code, data, and experiments are available on the CodaLab platform at `https://www.codalab.org/worksheets/` ``` 0xfcace41fdeec45f3bc6ddf31107b829f. 
私たちのコード、データ、および実験は、CodaLabプラットフォームの`https://www.codalab.org/worksheets/` ``` 0xfcace41fdeec45f3bc6ddf31107b829fで入手可能です。

**Acknowledgments 謝辞** 

We would like to thank Gabor Angeli for fruitful discussions and the anonymous reviewers for their valuable feedback. 
Gabor Angeliに有意義な議論をしていただき、匿名のレビュアーに貴重なフィードバックをいただいたことに感謝します。

We gratefully acknowledge the support of the Google Natural Language Understanding Focused Program and the National Science Foundation Graduate Research Fellowship under Grant No. DGE114747. 
私たちは、Google自然言語理解フォーカスプログラムと、助成金番号DGE114747の下での国立科学財団大学院研究フェローシップの支援に感謝します。

### References 参考文献

F. Bastien, P. Lamblin, R. Pascanu, J. Bergstra, I. J. Goodfellow, A. Bergeron, N. Bouchard, and Y. Bengio. 2012. Theano: new features and speed improvements. Deep Learning and Unsupervised Feature Learning NIPS 2012 Workshop. 
F. Bastien, P. Lamblin, R. Pascanu, J. Bergstra, I. J. Goodfellow, A. Bergeron, N. Bouchard, および Y. Bengio. 2012. Theano: 新機能と速度の改善。深層学習と教師なし特徴学習 NIPS 2012 ワークショップ。

J. Bergstra, O. Breuleux, F. Bastien, P. Lamblin, R. Pascanu, G. Desjardins, J. Turian, D. Warde-Farley, and Y. Bengio. 2010. Theano: a CPU and GPU math expression compiler. In Proceedings of the Python _for Scientific Computing Conference (SciPy)._ 
J. Bergstra, O. Breuleux, F. Bastien, P. Lamblin, R. Pascanu, G. Desjardins, J. Turian, D. Warde-Farley, および Y. Bengio. 2010. Theano: CPUおよびGPUの数学式コンパイラ。Python _for Scientific Computing Conference (SciPy)_ の議事録において。

K. Bollacker, C. Evans, P. Paritosh, T. Sturge, and J. Taylor. 2008. Freebase: a collaboratively created graph database for structuring human knowledge. In _International Conference on Management of Data_ _(SIGMOD), pages 1247–1250._ 
K. Bollacker, C. Evans, P. Paritosh, T. Sturge, および J. Taylor. 2008. Freebase: 人間の知識を構造化するために共同で作成されたグラフデータベース。_International Conference on Management of Data_ _(SIGMOD)、ページ1247–1250_ において。

A. Bordes, N. Usunier, A. Garcia-Duran, J. Weston, and O. Yakhnenko. 2013. Translating embeddings for modeling multi-relational data. In Advances _in Neural Information Processing Systems (NIPS),_ pages 2787–2795. 
A. Bordes, N. Usunier, A. Garcia-Duran, J. Weston, および O. Yakhnenko. 2013. 多関係データのモデル化のための埋め込みの翻訳。_Advances in Neural Information Processing Systems (NIPS)_ において、ページ2787–2795。

A. Bordes, S. Chopra, and J. Weston. 2014. Question answering with subgraph embeddings. In Em_pirical Methods in Natural Language Processing_ _(EMNLP)._ 
A. Bordes, S. Chopra, および J. Weston. 2014. サブグラフ埋め込みを用いた質問応答。_Empirical Methods in Natural Language Processing_ _(EMNLP)_ において。

S. R. Bowman, C. Potts, and C. D. Manning. 2014. Can recursive neural tensor networks learn logical reasoning? In International Conference on Learn_ing Representations (ICLR)._ 
S. R. Bowman, C. Potts, および C. D. Manning. 2014. 再帰的ニューラルテンソルネットワークは論理的推論を学習できるか？_International Conference on Learning Representations (ICLR)_ において。

X. Dong, E. Gabrilovich, G. Heitz, W. Horn, N. Lao, K. Murphy, T. Strohmann, S. Sun, and W. Zhang. 2014. Knowledge vault: A web-scale approach to probabilistic knowledge fusion. In International _Conference on Knowledge Discovery and Data Min-_ _ing (KDD), pages 601–610._ 
X. Dong, E. Gabrilovich, G. Heitz, W. Horn, N. Lao, K. Murphy, T. Strohmann, S. Sun, および W. Zhang. 2014. Knowledge vault: 確率的知識融合へのウェブスケールアプローチ。_International Conference on Knowledge Discovery and Data Mining (KDD)_ において、ページ601–610。

J. Duchi, E. Hazan, and Y. Singer. 2010. Adaptive subgradient methods for online learning and stochastic optimization. In Conference on Learning Theory _(COLT)._ 
J. Duchi, E. Hazan, および Y. Singer. 2010. オンライン学習と確率的最適化のための適応的サブグラディエント法。_Conference on Learning Theory_ _(COLT)_ において。

M. Gardner, P. Talukdar, J. Krishnamurthy, and T. Mitchell. 2014. Incorporating vector space similarity in random walk inference over knowledge bases. In Empirical Methods in Natural Language _Processing (EMNLP)._ 
M. Gardner, P. Talukdar, J. Krishnamurthy, および T. Mitchell. 2014. 知識ベースにおけるランダムウォーク推論にベクトル空間の類似性を組み込む。_Empirical Methods in Natural Language Processing (EMNLP)_ において。

E. Grefenstette. 2013. Towards a formal distributional semantics: Simulating logical calculi with tensors. _arXiv preprint arXiv:1304.5823._ 
E. Grefenstette. 2013. 形式的分布意味論に向けて：テンソルを用いた論理計算のシミュレーション。_arXivプレプリント arXiv:1304.5823_。

N. Lao and W. W. Cohen. 2010. Relational retrieval using a combination of path-constrained random walks. Machine learning, 81(1):53–67. 
N. Lao および W. W. Cohen. 2010. パス制約ランダムウォークの組み合わせを使用した関係的検索。機械学習、81(1):53–67。

N. Lao, T. Mitchell, and W. W. Cohen. 2011. Random walk inference and learning in a large scale knowledge base. In Empirical Methods in Natural Lan_guage Processing (EMNLP), pages 529–539._ 
N. Lao, T. Mitchell, および W. W. Cohen. 2011. 大規模知識ベースにおけるランダムウォーク推論と学習。_Empirical Methods in Natural Language Processing (EMNLP)_ において、ページ529–539。

B. Min, R. Grishman, L. Wan, C. Wang, and D. Gondek. 2013. Distant supervision for relation extraction with an incomplete knowledge base. In _North American Association for Computational Lin-_ _guistics (NAACL), pages 777–782._ 
B. Min, R. Grishman, L. Wan, C. Wang, および D. Gondek. 2013. 不完全な知識ベースを用いた関係抽出のための遠隔監視。_North American Association for Computational Linguistics (NAACL)_ において、ページ777–782。

A. Neelakantan, B. Roth, and A. McCallum. 2015. Compositional vector space models for knowledge base completion. In Association for Computational _Linguistics (ACL)._  
A. Neelakantan, B. Roth, および A. McCallum. 2015. 知識ベースの補完のための合成ベクトル空間モデル。_Association for Computational Linguistics (ACL)_ において。

M. Nickel, V. Tresp, and H. Kriegel. 2011. A three-way model for collective learning on multirelational data. In International Conference on Ma_chine Learning (ICML), pages 809–816._ 
M. Nickel, V. Tresp, および H. Kriegel. 2011. 多関係データにおける集合学習のための三方向モデル。_International Conference on Machine Learning (ICML)_ において、ページ809–816。

M. Nickel, V. Tresp, and H. Kriegel. 2012. Factorizing YAGO. In World Wide Web (WWW). 
M. Nickel, V. Tresp, および H. Kriegel. 2012. YAGOの因子分解。_World Wide Web (WWW)_ において。

M. Nickel, X. Jiang, and V. Tresp. 2014. Reducing the rank in relational factorization models by including observable patterns. In Advances in Neural Informa_tion Processing Systems (NIPS), pages 1179–1187._ 
M. Nickel, X. Jiang, および V. Tresp. 2014. 観測可能なパターンを含めることによって関係因子分解モデルのランクを削減する。_Advances in Neural Information Processing Systems (NIPS)_ において、ページ1179–1187。

J. Pennington, R. Socher, and C. D. Manning. 2014. Glove: Global vectors for word representation. In _Empirical Methods in Natural Language Processing_ _(EMNLP)._ 
J. Pennington, R. Socher, および C. D. Manning. 2014. Glove: 単語表現のためのグローバルベクトル。_Empirical Methods in Natural Language Processing_ _(EMNLP)_ において。

B. Perozzi, R. Al-Rfou, and S. Skiena. 2014. Deepwalk: Online learning of social representations. In _International Conference on Knowledge Discovery_ _and Data Mining (KDD), pages 701–710._ 
B. Perozzi, R. Al-Rfou, および S. Skiena. 2014. Deepwalk: ソーシャル表現のオンライン学習。_International Conference on Knowledge Discovery and Data Mining (KDD)_ において、ページ701–710。

S. Riedel, L. Yao, and A. McCallum. 2013. Relation extraction with matrix factorization and universal schemas. In North American Association for _Computational Linguistics (NAACL)._ 
S. Riedel, L. Yao, および A. McCallum. 2013. 行列因子分解とユニバーサルスキーマを用いた関係抽出。_North American Association for Computational Linguistics (NAACL)_ において。

R. Socher, B. Huval, C. D. Manning, and A. Y. Ng. 2012. Semantic compositionality through recursive matrix-vector spaces. In Empirical Methods in Nat_ural Language Processing and Computational Nat-_ _ural Language Learning (EMNLP/CoNLL), pages_ 1201–1211. 
R. Socher, B. Huval, C. D. Manning, および A. Y. Ng. 2012. 再帰的行列-ベクトル空間を通じた意味的合成性。_Empirical Methods in Natural Language Processing and Computational Natural Language Learning (EMNLP/CoNLL)_ において、ページ1201–1211。

R. Socher, D. Chen, C. D. Manning, and A. Ng. 2013. Reasoning with neural tensor networks for knowledge base completion. In Advances in Neural Infor_mation Processing Systems (NIPS), pages 926–934._ 
R. Socher, D. Chen, C. D. Manning, および A. Ng. 2013. 知識ベースの補完のためのニューラルテンソルネットワークによる推論。_Advances in Neural Information Processing Systems (NIPS)_ において、ページ926–934。

R. Socher, A. Karpathy, Q. V. Le, C. D. Manning, and A. Y. Ng. 2014. Grounded compositional semantics for finding and describing images with sentences. _Transactions of the Association for Computational_ _Linguistics (TACL), 2:207–218._ 
R. Socher, A. Karpathy, Q. V. Le, C. D. Manning, および A. Y. Ng. 2014. 文を用いて画像を見つけて説明するための基盤となる合成意味論。_Transactions of the Association for Computational Linguistics (TACL), 2:207–218_。

J. Turian, L. Ratinov, and Y. Bengio. 2010. Word representations: a simple and general method for semisupervised learning. In Proceedings of the 48th an_nual meeting of the association for computational_ _linguistics, pages 384–394._ 
J. Turian, L. Ratinov, および Y. Bengio. 2010. 単語表現：半教師あり学習のためのシンプルで一般的な方法。計算言語学会の第48回年次会議の議事録において、ページ384–394。

J. D. Ullman. 1985. Implementation of logical query languages for databases. _ACM Transactions on_ _Database Systems (TODS), 10(3):289–321._ 
J. D. Ullman. 1985. データベースのための論理クエリ言語の実装。_ACM Transactions on Database Systems (TODS), 10(3):289–321_。

B. Yang, W. Yih, X. He, J. Gao, and L. Deng. 2015. Embedding entities and relations for learning and inference in knowledge bases. arXiv preprint _arXiv:1412.6575._  
B. Yang, W. Yih, X. He, J. Gao, および L. Deng. 2015. 知識ベースにおける学習と推論のためのエンティティと関係の埋め込み。arXivプレプリント _arXiv:1412.6575_。
