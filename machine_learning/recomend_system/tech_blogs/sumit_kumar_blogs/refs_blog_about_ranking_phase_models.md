refs: https://blog.reachsumit.com/posts/2022/11/feature-interactions-ir/


# Feature-Interactions Based Information Retrieval Models 特徴相互作用に基づく情報検索モデル

Sumit Kumar
スミット・クマール

included in
カテゴリ：情報検索

## Introduction はじめに

Large-scale information retrieval applications, such as recommender systems, search ranking, and text analysis often leverage feature interactions for effective modeling. 
大規模な情報検索アプリケーション、例えばレコメンダーシステム、検索ランキング、テキスト分析は、効果的なモデリングのために**特徴の相互作用を活用**することがよくあります。
These models are commonly deployed at the ranking stage of the cascade-style systems. 
これらのモデルは、カスケードスタイルのシステムのランキング段階で一般的に展開されます。
In this article, I summarize the need for modeling feature interactions and introduce some of the most popular ML architectures designed around this theme. 
この記事では、特徴の相互作用をモデル化する必要性を要約し、このテーマに基づいて設計された最も人気のある機械学習（ML）アーキテクチャのいくつかを紹介します。
This article also highlights the high data sparsity issue, that makes it hard for ML algorithms to model second or higher-order feature interactions. 
この記事では、MLアルゴリズムが二次またはそれ以上の特徴の相互作用をモデル化するのを困難にする高いデータスパース性の問題も強調します。

<!-- ここまで読んだ! -->

### Why Should We Model Feature Interactions? なぜ特徴の相互作用をモデル化する必要があるのか？

As an example, consider an artificial Click-through rate (CTR) dataset shown in the table below, where + and - represent the number of clicked and unclicked impressions respectively.
例として、以下の表に示された人工的なクリック率（CTR）データセットを考えてみましょう。ここで、+はクリックされたインプレッションの数、-はクリックされなかったインプレッションの数を表します。

![]()

We can see that an ad from Gucci has a high CTR on Vogue. 
Gucciの広告はVogueで高いCTRを持っていることがわかります。
It is difficult for linear models to learn this information because they learn the two weights Gucci and Vogue separately. 
**線形モデルはGucciとVogueの2つの重みを別々に学習するため、この情報を学習するのが難しい**です。
To address this problem, a machine learning model will have to learn the effect of their feature interaction. 
この問題に対処するために、機械学習モデルはそれらの特徴の相互作用の効果を学習する必要があります。
Algorithms such as Poly2 (degree-2 polynomial) do this by learning a dedicated weight for each feature conjunction (O(n^2) time complexity).
Poly2（2次多項式）などのアルゴリズムは、各特徴の組み合わせに対して専用の重みを学習することでこれを実現します（O(n^2)の時間計算量）。

<!-- ここまで読んだ! -->

### Order of Interaction 相互作用の順序

An order-2 interaction can be between two features, such as app category and timestamp. 
order-2の相互作用は、アプリのカテゴリとタイムスタンプのように、2つの特徴の間で発生する可能性があります。
For example, people often download Uber apps for food delivery at meal-time. 
**例えば、人々は食事の時間に食料品配達のためにUberアプリをダウンロードすることがよくあります。**
Similarly, an order-3 interaction can be between app category, user gender, and age. 
同様に、order-3の相互作用は、アプリのカテゴリ、ユーザーの性別、および年齢の間で発生する可能性があります。
For example, a report showed that male teenagers like shooting and RPG games. 
例えば、ある報告によると、**男性のティーンエイジャーはシューティングゲームやRPGゲームを好むこと**が示されています。
Some research works argue that considering low- and high-order feature interactions simultaneously brings additional improvement over the cases of considering either alone. 
いくつかの研究では、**低次および高次の特徴相互作用を同時に考慮することが、いずれか一方を考慮する場合よりも追加の改善をもたらす**と主張しています。
For a highly sparse dataset, these feature interactions are often hidden and difficult to identify a priori. 
非常にスパースなデータセットでは、これらの特徴相互作用はしばしば隠れており、事前に特定することが難しいです。

<!-- ここまで読んだ! -->

### Data Sparsity データの希薄性

A variety of information retrieval and data mining tasks, such as recommender systems, targeted advertising, etc. model discrete and categorical variables extensively. 
さまざまな情報検索およびデータマイニングのタスク、例えばレコメンダーシステムやターゲット広告などは、**離散的およびカテゴリカルな変数を広範にモデル化**します。
As an example, these variables could be user demographics such as gender and occupation, or item categories. 
例えば、これらの変数は性別や職業などのユーザの人口統計や、アイテムのカテゴリである可能性があります。
Additionally, these systems also utilize identifiers like user IDs, product IDs, and advertisement IDs. 
さらに、これらのシステムはユーザID、製品ID、広告IDなどの識別子も利用します。
A common technique for using these categorical variables in machine learning algorithms is to convert them to a set of binary vectors via one-hot encoding. 
機械学習アルゴリズムでこれらのカテゴリカル変数を使用する一般的な手法は、one-hot encodingを介してそれらを一連のバイナリベクトルに変換することです。
This means that for a system with a large (millions, or even billions) userbase and item catalog, the resultant feature input is highly sparse as the actual engagement data is comparatively smaller. 
**これは、数百万、あるいは数十億のユーザベースとアイテムカタログを持つシステムにおいて、実際のエンゲージメントデータが比較的小さいため、結果として得られる特徴入力が非常に希薄である**ことを意味します。

This highly sparse data makes it difficult to learn effective feature interactions because often there isn’t any observed data for a lot of combinations of feature values. 
この非常に希薄なデータは、特徴値の多くの組み合わせに対して観測データが存在しないことが多いため、効果的な特徴の相互作用を学習することを困難にします。
For example, there is no training data for the pair (NBC, Gucci) in the table above. 
例えば、上の表においてペア(NBC, Gucci)に対するトレーニングデータは存在しません。

<!-- ここまで読んだ! -->

### Memorization vs Generalization Paradigm メモリゼーションと一般化のパラダイム

One common challenge in building such applications is to achieve both memorization and generalization.
このようなアプリケーションを構築する際の一般的な課題の一つは、メモリゼーションと一般化の両方を達成することです。

- Memorization is about learning the frequent co-occurrence of features and exploiting the correlations observed from the historical data. 
  - メモリゼーションは、特徴の頻繁な共起を学習し、歴史的データから観察された相関関係を利用することです。
    As an example, the Google Play store recommender system might use two features ‘installed_app’ and ‘impression_app’ to calculate the probability of a user installing the ‘impression_app’. 
    例えば、Google Playストアのレコメンダーシステムは、ユーザーが「impression_app」をインストールする確率を計算するために、「installed_app」と「impression_app」という2つの特徴を使用するかもしれません。
    Memorization-based algorithms use cross-product transformation and look at specific features, such as “AND(previously_installed_app=netflix, current_impression_app=spotify)”, whose value is 1, and correlate it with the target label. 
    メモリゼーションベースのアルゴリズムは、クロスプロダクト変換を使用し、「AND(previously_installed_app=netflix, current_impression_app=spotify)」のような特定の特徴を見て、その値が1であるものをターゲットラベルと相関させます。
    While such recommendations are topical and directly relevant based on the user’s previous actions, they can not generalize when cross-feature interaction never happened in the training data, like the (NBC, Gucci) pair in the table above. 
    このような推薦は、ユーザーの以前の行動に基づいてトピックに関連し直接的ですが、トレーニングデータでクロス特徴の相互作用が発生しなかった場合、一般化することはできません。例えば、上の表の(NBC, Gucci)ペアのようにです。
    Creating cross-product transformations may also require a lot of manual feature engineering effort. 
    クロスプロダクト変換を作成するには、多くの手動特徴エンジニアリングの努力が必要になる場合もあります。

- Generalization is based on the transitivity of correlation and exploring new feature combinations that have never or rarely occurred in the past. 
  - 一般化は、相関の推移性に基づき、過去に一度もまたは稀にしか発生しなかった新しい特徴の組み合わせを探求することです。
    To achieve this generalization we use embeddings-based methods, such as factorization machines or deep neural networks by learning a low-dimensional dense embedding vector.  
    **この一般化を達成するために、私たちはファクタリゼーションマシンや深層ニューラルネットワークのような埋め込みベースの手法を使用し、低次元の密な埋め込みベクトルを学習**します。
    While such recommenders tend to improve the diversity of the recommended items, they also suffer from the problem of over-generalizing for cases such as users with specific preferences, or niche items with a narrow appeal. 
    このようなレコメンダーは推薦アイテムの多様性を向上させる傾向がありますが、特定の好みを持つユーザーや狭い魅力を持つニッチアイテムのようなケースに対して過剰一般化の問題に悩まされることもあります。
    Also, dense embedding methods always lead to nonzero predictions and thus make less relevant recommendations at times. 
    また、密な埋め込み手法は常に非ゼロの予測をもたらし、そのため時にはあまり関連性のない推薦を行うことになります。
    Comparatively, it is easier for generalized linear models with cross-product feature transformations to memorize these “exception rules” for unique users and items with much fewer parameters. 
    比較すると、クロスプロダクト特徴変換を持つ一般化線形モデルは、ユニークなユーザーやアイテムのためのこれらの「例外ルール」をはるかに少ないパラメータでメモリゼーションする方が容易です。

<!-- ここまで読んだ! -->

## Model Architectures モデルアーキテクチャ

In this article, I will introduce, implement and compare seven popular model architectures that try to balance both memorization and generalization to some degree. 
この記事では、**記憶と一般化のバランスをある程度取ろうとする7つの人気モデルアーキテクチャ**を紹介し、実装し、比較します。
Each of the model implementations is done in its standalone Jupyter Notebook file and is linked in the corresponding section below. 
各モデルの実装は独立したJupyter Notebookファイルで行われており、以下の該当セクションにリンクされています。
Every notebook contains code for data preprocessing, model definition, training, and evaluation as applicable to the respective model. 
各ノートブックには、データ前処理、モデル定義、トレーニング、およびそれぞれのモデルに適用される評価のためのコードが含まれています。

### 1. Factorization Machine (FM) 

Factorization Machines (FMs) were originally purposed in 2010 as a supervised machine-learning method for collaborative recommendations. 
ファクタリゼーションマシン（FM）は、2010年に協調フィルタリングのための教師あり機械学習手法として提案されました。
FMs allow parameter estimation under very sparse data where its predecessors, like SVMs failed, and unlike Matrix Factorization it isn’t limited to modeling the relation of two entities only. 
FMは、SVMのような先行技術が失敗した非常にスパースなデータの下でパラメータ推定を可能にし、行列分解とは異なり、2つのエンティティの関係をモデル化することに制限されません。
FMs learn second-order feature interactions on top of a linear model by modeling all interactions between each pair of features. 
FMは、各特徴のペア間のすべての相互作用をモデル化することによって、線形モデルの上に二次特徴相互作用を学習します。
They can also be optimized to work in linear time complexity. 
また、FMは線形時間計算量で動作するように最適化することもできます。
While in principle, FM can model high-order feature interaction, in practice usually only order-2 features are considered due to high complexity. 
原理的にはFMは高次の特徴相互作用をモデル化できますが、**実際には高い複雑性のため通常は二次の特徴のみが考慮**されます。

$$
\hat{y}_{FM}(x) = w_0 + \sum_{i=1}^{n} w_i x_i + \sum_{i=1}^{n} \sum_{j=i+1}^{n} \hat{w}^{ij} x_i x_j
$$

(上記のxはアイテムとユーザの両方の特徴を含んだ特徴量ベクトル!:thinking:)
(あ、FMって結局線形回帰モデルみたいな感じか...! じゃあ推論は線形モデルと同じくらい軽そうだな〜:thinking:)

where $w_0$ is the global bias, $w_i$ denotes the weight of the i-th feature, and $\hat{w}^{ij}$ denotes the weight of the cross feature $x_i x_j$, which is factorized as: 
ここで、$w_0$はグローバルバイアス、$w_i$はi番目の特徴の重みを示し、$\hat{w}^{ij}$は交差特徴$x_i x_j$の重みを示し、次のように因子分解されます：

$$
\hat{w}^{ij} = v_i^T v_j
$$

where $v_i \in \mathbb{R}^k$ denotes the embedding vector for feature i, and k denotes the size of the embedding vector. 
ここで、$v_i \in \mathbb{R}^k$ は特徴iの埋め込みベクトルを示し、$k$ は埋め込みベクトルのサイズを示します。

![]()

The example above shows a sparse input feature vector $x$ with corresponding target $y$. 
上記の例は、対応するターゲット $y$ を持つスパース入力特徴ベクトル $x$ を示しています。
We have binary indicator variables for the user, movie, and the last movie rated, along with a normalized rating for other movies and timestamps. 
ユーザー、映画、および最後に評価された映画のためのバイナリインジケータ変数があり、他の映画とタイムスタンプのための正規化された評価も含まれています。
Let’s say we want to estimate the interaction between the user Alice (A) and the movie Star Trek (ST). 
ユーザーのアリス（A）と映画のスタートレック（ST）との相互作用を推定したいとしましょう。
You will notice that we do not have any example in $x$ with an interaction between A and ST. 
$x$の中にAとSTの相互作用を持つ例がないことに気付くでしょう。
FM can still estimate this by using the factorized interaction parameters $\langle v_A, v_{ST} \rangle$ even in this case. 
FMは、この場合でも因子分解された相互作用パラメータ$\langle v_A, v_{ST} \rangle$を使用してこれを推定できます。

<!-- ここまで読んだ! -->

#### Implementation 実装

Suppose we have M training examples, n features and we want to factorize feature interaction with vectors of size k i.e. dimensionality of $v_{i}$. 
M個のトレーニング例、n個の特徴があり、サイズkのベクトルで特徴の相互作用を因数分解したいとします。すなわち、$v_{i}$ の次元です。
Let us denote our trainset as $X \in R^{M \times n}$, and matrix of $v_{i}$ (the ith row is $v_{i}$) as $V \in R^{n \times k}$. 
私たちのトレーニングセットを $X \in R^{M \times n}$ とし、$v_{i}$ の行列（i番目の行は$v_{i}$）を $V \in R^{n \times k}$ と表記します。
Also, let’s denote the feature vector for the jth object as $x_{j}$. 
また、j番目のオブジェクトの特徴ベクトルを$x_{j}$と表記します。

$$
X = \begin{bmatrix}
x_{1}^{(1)} & ... & x_{n}^{(1)} \\
... & ... & ... \\
x_{1}^{(M)} & ... & x_{n}^{(M)} \\
\end{bmatrix},
V = \begin{bmatrix}
v_{1}^{(1)} & ... & v_{1}^{(k)} \\
... & ... & ...  \\
v_{n}^{(1)} & ... & v_{n}^{(k)} \\
\end{bmatrix}
$$

The number in brackets indicates the index of the sample for $x$ and the index of the feature for $v$. 
括弧内の数字は、$x$のサンプルのインデックスと$v$の特徴のインデックスを示します。
Also, the FM equation can be expressed as: 
また、FMの方程式は次のように表現できます：

$$
\sum_{i=1}^{n} \sum_{j=i+1}^{n} (v_{i} \cdot v_{j}) x_{i} x_{j} = \frac{1}{2} \sum_{f=1}^{k} \left( \left( \sum_{i=1}^{n} v_{i}^{(f)} x_{i} \right)^{2} - \sum_{i=1}^{n} (v_{i}^{(f)})^{2} x_{i}^{2} \right)
= \frac{1}{2} \sum_{f=1}^{k} (S_{1,f}^{2} - S_{2,f}) = \frac{1}{2} (S_{1}^{2} - S_{2})
$$

$S_{1}$ is a dot product of feature vector $x_{j}$ and ith column of $V$. 
$S_{1}$は特徴ベクトル$x_{j}$と$V$のi列のドット積です。
If we multiply $X$ and $V$, we get: 
$X$と$V$を掛けると、次のようになります：

$$
XV = \begin{bmatrix}
s_{1}^{(1)} & ... & s_{k}^{(1)} \\
... & ... & ... \\
s_{1}^{(M)} & ... & s_{k}^{(M)} \\
\end{bmatrix}
= \begin{bmatrix}
S_{1,1}^{(1)} & ... & S_{1,k}^{(1)} \\
... & ... & ... \\
S_{1,1}^{(M)} & ... & S_{1,k}^{(M)} \\
\end{bmatrix}
$$

So if square $XV$ element-wise and then find the sum of each row, we obtain a vector of $S_{1}^{2}$ terms for each training sample. 
したがって、$XV$を要素ごとに二乗し、各行の合計を求めると、各トレーニングサンプルに対して$S_{1}^{2}$のベクトルが得られます。
Also, if we first square $X$ and $V$ element-wise, then multiply them, and finally sum by rows, we’ll get $S_{2}$ term for each training object. 
また、最初に$X$と$V$を要素ごとに二乗し、それらを掛け合わせ、最後に行ごとに合計すると、各トレーニングオブジェクトに対して$S_{2}$の項が得られます。
So, conceptually, we can express the final term like this: 
したがって、概念的には、最終的な項を次のように表現できます：

$$
\hat{y}(X) = \frac{1}{2} ( \text{square}(XV) - (\text{square}(X) \cdot \text{square}(V)) ).sum(\text{rowwise})
$$

PyTorch Code PyTorchコード

Refer to this Gist for the complete code for this experiment: https://gist.github.com/reachsumit/2a639276fc781870c4dcd480a3417bf9 
この実験の完全なコードについては、このGistを参照してください：https://gist.github.com/reachsumit/2a639276fc781870c4dcd480a3417bf9

You can read more about FMs in the original paper and the official codebase. 
FMsについては、元の論文や公式コードベースでさらに読むことができます。

<!-- ここまで読んだ! -->

### 2. Field-Aware Factorization Machine (FFM) フィールド対応因子分解機（FFM）

Let’s revisit the artificial dataset example from earlier and add another column Gender to it. 
以前の人工データセットの例を再訪し、もう1つの列「性別」を追加しましょう。
One observation of such a dataset might look like this: 
そのようなデータセットの1つの観測は次のようになります：

![]()

FMs will model the effect of feature conjunction as: 
FMsは特徴の結合の効果を次のようにモデル化します：

$$
w_{ESPN} \cdot w_{Nike} + w_{ESPN} \cdot w_{Male} + w_{Nike} \cdot w_{Male}
$$

Field-aware factorization machines (FFMs) extend FMs by introducing the concept of fields and features. 
**フィールド対応因子分解機（Field-aware factorization machines, FFM）**は、**フィールドと特徴の概念を導入**することでFMsを拡張します。
With the same example, Publisher, Advertiser, and Gender will be called fields, while values like ESPN, Nike, and Male will be called their features. 
同じ例を用いると、Publisher、Advertiser、Genderはフィールドと呼ばれ、ESPN、Nike、Maleのような値はそれらの特徴と呼ばれます。(うんうん。イメージ通り...!:thinking:)
Note that in FMs every feature has only one latent vector to learn the latent effect with any other features. 
FMsでは、各特徴は他の特徴との潜在的な効果を学習するために1つの潜在ベクトルしか持たないことに注意してください。
For example, for ESPN, $w_{ESPN}$ is used to learn the latent effect with Nike ($w_{ESPN} \cdot w_{Nike}$) and Male ($w_{ESPN} \cdot w_{Male}$). 
例えば、ESPNの場合、$w_{ESPN}$はNike（$w_{ESPN} \cdot w_{Nike}$）およびMale（$w_{ESPN} \cdot w_{Male}$）との潜在的な効果を学習するために使用されます。
However, because Nike and Male belong to different fields, the latent effects of (ESPN, Nike) and (ESPN, Male) may be different. 
しかし、NikeとMaleは異なるフィールドに属するため、(ESPN, Nike)と(ESPN, Male)の潜在的な効果は異なる可能性があります。

In FFMs, each feature has several latent vectors. 
**FFMでは、各特徴は複数の潜在ベクトルを持ちます。**
Depending on the field of other features, one of them is used to do the inner product. 
他の特徴のフィールドに応じて、そのうちの1つが内積を計算するために使用されます。
So, for the same example, the feature interaction effect is modeled by FFM as: 
したがって、同じ例において、特徴の相互作用効果はFFMによって次のようにモデル化されます：

$$
w_{ESPN,A} \cdot w_{Nike,P} + w_{ESPN,G} \cdot w_{Male,P} + w_{Nike,G} \cdot w_{Male,A}
$$

To learn the latent effect of (ESPN, NIKE), for example, 
例えば、(ESPN, NIKE)の潜在的な効果を学習するために、
$w_{ESPN,A}$ is used because Nike belongs to the field Advertiser, and $w_{Nike,P}$ is used because ESPN belongs to the field Publisher. 
NikeはAdvertiserフィールドに属するため$w_{ESPN,A}$が使用され、ESPNはPublisherフィールドに属するため$w_{Nike,P}$が使用されます。

If $f$ is the number of fields, then the number of variables of FFMs is $nfk$, and the time complexity is $O(\bar{n}^{2}k)$. 
$f$がフィールドの数である場合、FFMの変数の数は$nfk$であり、時間計算量は$O(\bar{n}^{2}k)$です。
Note that because each latent vector in FFMs only needs to learn the effect with a specific field, usually: 
FFMの各潜在ベクトルは特定のフィールドとの効果を学習する必要があるため、通常は次のようになります：
(次元数kを減らさないといけないってことかな...!!:thinking:)

$$
k_{FFM} \ll k_{FM}
$$

FFM authors empirically show that for large, sparse datasets with many categorical features, FFMs perform better than FMs. 
**FFMの著者は、カテゴリ特徴が多く含まれる大規模でスパースなデータセットに対して、FFMがFMよりも優れている**ことを実証しています。
Whereas for small and dense datasets or numerical datasets, FMs perform better than FFMs. 
一方、小規模で密なデータセットや数値データセットに対しては、FMがFFMよりも優れています。

<!-- ここまで読んだ! -->

#### Implementation 実装

PyTorch Code
PyTorchコード
Refer to this Gist for the complete code for this experiment: https://gist.github.com/reachsumit/c6a8037f4596a8181376313fdba33ffd
このGistを参照して、この実験の完全なコードを確認してください。
You can read more about FFMs in the original paper and the official codebase.
FFMについては、元の論文と公式コードベースでさらに読むことができます。

<!-- ここまで読んだ! -->

### 3. Attentional Factorization Machine (AFM) 注意機構ファクタリゼーションマシン (AFM)

However, despite its effectiveness, FMs model all feature interactions with the same weight, but not all feature interactions are equally useful and predictive. 
しかし、その効果にもかかわらず、FMsはすべての特徴の相互作用を同じ重みでモデル化しますが、すべての特徴の相互作用が同じように有用で予測的であるわけではありません。
For example, the interactions with useless features may even introduce noise leading to degraded model performance. 
**例えば、無駄な特徴との相互作用は、ノイズを引き起こし、モデルの性能を低下させる可能性があります**。
Attentional Factorization Machines (AFMs) fix this by learning the importance of each feature interaction from data via a neural attention network. 
注意機構ファクタリゼーションマシン (AFM) は、ニューラル注意ネットワークを介してデータから各特徴の相互作用の重要性を学習することでこれを修正します。

![]()

AFM starts with sparse input and embedding layer and inspired by FM’s inner product, it expands m vectors to $\frac{m(m−1)}{2}$ interacted vectors, where each interacted vector is the element-wise product of two distinct vectors to encode their interaction. 
AFMは、スパース入力と埋め込み層から始まり、FMの内積に触発されて、$m$ベクトルを$\frac{m(m−1)}{2}$の相互作用ベクトルに拡張します。ここで、各相互作用ベクトルは、2つの異なるベクトルの要素ごとの積であり、その相互作用をエンコードします。
The output of the pair-wise interaction layer is fed into an attention-based pooling layer, the idea here is to allow different parts to contribute differently when compressing them to a single representation. 
ペアワイズ相互作用層の出力は、注意に基づくプーリング層に供給されます。ここでのアイデアは、異なる部分が単一の表現に圧縮する際に異なる貢献をすることを可能にすることです。
An attention mechanism is applied to feature interactions by performing a weighted sum on the interacted vectors. 
注意機構は、相互作用ベクトルに対して重み付き和を行うことによって特徴の相互作用に適用されます。
This weight or attention score can be thought of as the importance of weight $\hat{w}_{ij}$ in predicting the target. 
この重みまたは注意スコアは、ターゲットを予測する際の重み$\hat{w}_{ij}$の重要性と考えることができます。
One shortcoming of AFM architecture is that it models only second-order feature interactions. 
AFMアーキテクチャの1つの欠点は、第二次の特徴相互作用のみをモデル化することです。

#### Implementation 実装

PyTorch Code
PyTorchコード
Refer to this Gist for the complete code for this experiment: https://gist.github.com/reachsumit/85fe046691c66221bec00bc7e59e145b
この実験の完全なコードについては、このGistを参照してください: https://gist.github.com/reachsumit/85fe046691c66221bec00bc7e59e145b
You can read more about AFMs in the original paper and the official codebase.
AFMについての詳細は、元の論文と公式コードベースで読むことができます。

<!-- ここまで読んだ! -->

### 4. Wide & Deep Learning

The Wide & Deep learning framework was proposed by Google to achieve both memorization and generalization in one model, by jointly training a linear model component and a neural network component. 
Wide & Deep学習フレームワークは、**Googleによって提案され、線形モデルコンポーネントとニューラルネットワークコンポーネントを共同で訓練することによって、1つのモデルで記憶と一般化の両方を達成**します。
The wide component is a generalized linear model to which raw input features and transformed features (such as cross-product transformations) are supplied. 
広いコンポーネントは、原始的な入力特徴と変換された特徴（交差積変換など）が供給される一般化線形モデルです。
The deep component is a feed-forward neural network, which consumes sparse categorical features in embedding vector form. 
深いコンポーネントは、埋め込みベクトル形式のスパースカテゴリカル特徴を消費するフィードフォワードニューラルネットワークです。
The wide and deep parts are combined using a weighted sum of their output log odds as the prediction which is then fed to a common loss function for joint training. 
**広い部分と深い部分は、それぞれの出力の対数オッズの加重和を使用して結合され、その予測が共通の損失関数に供給され、共同訓練**が行われます。

The authors claim that wide linear models can effectively memorize sparse feature interactions using cross-product feature transformations, while deep neural networks can generalize to previously unseen feature interactions through low-dimensional embeddings. 
著者たちは、広い線形モデルが交差積特徴変換を使用してスパース特徴の相互作用を効果的に記憶できる一方で、深いニューラルネットワークは低次元の埋め込みを通じて以前に見たことのない特徴の相互作用に一般化できると主張しています。
Note that the wide and deep parts work with two different inputs and the input to the wide part still relies on expertise feature engineering. 
**広い部分と深い部分は2つの異なる入力で動作し、広い部分への入力は依然として専門的な特徴エンジニアリングに依存している**ことに注意してください。
The model also suffers from the same problem as the linear models like Polynomial Regression that feature interactions can not be learned for unobserved cross features. 
このモデルは、ポリノミアル回帰のような線形モデルと同様に、未観測の交差特徴に対して特徴の相互作用を学習できないという同じ問題に悩まされています。

#### Implementation 実装

PyTorch Code
PyTorchコード

Refer to this Gist for the complete code for this experiment: https://gist.github.com/reachsumit/a6ab97ed6bc053aaf3d73320b4b31b97
この実験の完全なコードについては、このGistを参照してください: https://gist.github.com/reachsumit/a6ab97ed6bc053aaf3d73320b4b31b97

You can read more about Wide&Deep in the original paper and the official codebase.
Wide&Deepについては、元の論文と公式コードベースでさらに読むことができます。

<!-- ここまで読んだ! -->

### 5. DeepFM

DeepFM model architecture combines the power of FMs and deep learning to overcome the issues with Wide&Deep networks. 
DeepFMモデルのアーキテクチャは、**FMと深層学習の力を組み合わせて、Wide&Deepネットワークの問題を克服**します。
DeepFM uses a single shared input to its wide and deep parts, with no need for any special feature engineering besides raw features. 
**DeepFMは、広い部分と深い部分に対して単一の共有入力を使用し、生の特徴以外に特別な特徴エンジニアリングを必要としません**。
It models low-order feature interactions like FM and models high-order feature interactions like DNN. 
それは、FMのように低次の特徴相互作用をモデル化し、DNNのように高次の特徴相互作用をモデル化します。

![]()

#### Implementation 実装

PyTorch Code
PyTorchコード
Refer to this Gist for the complete code for this experiment: https://gist.github.com/reachsumit/79237a4de62b4033e2576c55df3dc056
この実験の完全なコードについては、このGistを参照してください: https://gist.github.com/reachsumit/79237a4de62b4033e2576c55df3dc056
You can read more about DeepFM in the original paper.
DeepFMについての詳細は、元の論文を参照してください。

<!-- ここまで読んだ! -->

### 6. Neural Factorization Machine (NFM) ニューラルファクタリゼーションマシン（NFM）

Neural Factorization Machine (NFM) model architecture was also proposed by the authors of the AFM paper with the same goal of overcoming the insufficient linear modeling of feature interactions in FM. 
ニューラルファクタリゼーションマシン（NFM）モデルアーキテクチャは、FMにおける特徴相互作用の不十分な線形モデル化を克服するという同じ目的で、AFM論文の著者によって提案されました。
After the sparse input and embedding layer, this time the authors propose a Bi-Interaction layer that models the second-order feature interactions. 
スパース入力と埋め込み層の後、今回は著者が第二次特徴相互作用をモデル化するBi-Interaction層を提案します。
This layer is a pooling layer that converts a set of the embedding vectors set input to one vector by performing an element-wise product of vectors: 
この層はプーリング層であり、ベクトルの要素ごとの積を実行することによって、埋め込みベクトルのセット入力を1つのベクトルに変換します：

$$
\sum_{i=1}^{n} \sum_{j=i+1}^{n} x_{i}v_{i} \odot  x_{j}v_{j}
$$

and passes it on to another set of fully connected layers. 
そして、それを別の完全結合層のセットに渡します。

![]()

#### Implementation 実装

PyTorch Code
PyTorchコード

Refer to this Gist for the complete code for this experiment: https://gist.github.com/reachsumit/f29d7001b7687785f33636c9bca302c3
このGistを参照して、この実験の完全なコードを確認してください: https://gist.github.com/reachsumit/f29d7001b7687785f33636c9bca302c3

You can read more about NFM in the original paper and the official codebase.
NFMについては、元の論文と公式コードベースでさらに読むことができます。

<!-- ここまで読んだ! -->

### 7. Deep Learning Recommendation Model (DLRM) 

The Deep Learning Recommendation Model (DLRM) was proposed by Facebook in 2019. 
Deep Learning Recommendation Model (DLRM)は、2019年にFacebookによって提案されました。
The DLRM architecture can be thought of as a simplified version of DeepFM architecture. 
**DLRMアーキテクチャは、DeepFMアーキテクチャの簡略版と考えることができます**。
DLRM tries to stay away from high-order interactions by not passing the embedded categorical features through an MLP layer. 
**DLRMは、埋め込まれたカテゴリ特徴をMLP層を通さないことで、高次の相互作用を避けようとします。**
First, it makes the continuous features go through a “bottom” MLP layer such that they have the same length as the embedding vectors. 
まず、連続的な特徴を「ボトム」MLP層を通過させ、埋め込みベクトルと同じ長さにします。
Then, it computes the dot product between all combinations of embedding vectors and the bottom MLP output from the previous step. 
次に、すべての埋め込みベクトルの組み合わせと前のステップのボトムMLP出力との間でドット積を計算します。
The dot product output is then concatenated with the bottom MLP output and is passed to a “top” MLP layer to compute the final output. 
ドット積の出力はボトムMLP出力と連結され、「トップ」MLP層に渡されて最終出力を計算します。
This architecture design is tailored to mimic the way Factorization Machines compute the second-order interactions between the embeddings, and the paper also says: 
このアーキテクチャ設計は、因子分解マシンが埋め込み間の二次相互作用を計算する方法を模倣するように調整されており、論文では次のようにも述べています。
We argue that higher-order interactions beyond second-order found in other networks may not necessarily be worth the additional computational/memory cost. 
**他のネットワークで見られる二次を超える高次の相互作用は、追加の計算/メモリコストに見合うものではないと私たちは主張**します。

<!-- ここまで読んだ! -->

#### Implementation 実装

The paper also notes that DLRM contains far more parameters than common models like CNNs, RNNs, GANs, and transformers, making the training time for this model go up to several weeks. 
この論文はまた、**DLRMがCNN、RNN、GAN、トランスフォーマーのような一般的なモデルよりもはるかに多くのパラメータを含んでいることに言及しており、このモデルのトレーニング時間は数週間に達する**ことがあります。
They also propose a framework to parallelize DLRM operations. 
彼らはまた、DLRMの操作を並列化するためのフレームワークを提案しています。
Due to high compute requirements, I couldn’t train the DLRM model myself. 
高い計算要件のため、私は自分でDLRMモデルをトレーニングすることができませんでした。
DLRM results in this experimentation are with a simplified implementation using a concatenation of bottom MLP output and embedding output, instead of their dot product. 
この実験におけるDLRMの結果は、ドット積の代わりにボトムMLP出力と埋め込み出力の連結を使用した簡略化された実装によるものです。
PyTorch Code
Refer to this Gist for the complete code for this experiment: https://gist.github.com/reachsumit/a02a83fbb3ae5e293fde4b90e3a319d7
PyTorchコード
この実験の完全なコードについては、次のGistを参照してください: https://gist.github.com/reachsumit/a02a83fbb3ae5e293fde4b90e3a319d7

You can read more about DLRM in the original paper and the official codebase. 
DLRMについては、元の論文と公式コードベースでさらに読むことができます。

<!-- ここまで読んだ! -->

## Toy Experiment おもちゃ実験  
### Dataset Preprocessing データセット前処理

For this article, I will be using the MovieLens 100K dataset from Kaggle. 
この記事では、KaggleからのMovieLens 100Kデータセットを使用します。
It contains 100K ratings from 943 users on 1682 movies, along with demographic information for the user. 
このデータセットには、943人のユーザから1682本の映画に対する100Kの評価と、ユーザの人口統計情報が含まれています。
Each user has rated at least 20 movies. 
各ユーザは少なくとも20本の映画を評価しています。
The following transformations were applied to prepare the dataset for experimentation. 
実験のためにデータセットを準備するために、以下の変換が適用されました。

- The dataset was sorted by user_id and timestamp to create time ordering for each user.  
  - データセットはuser_idとtimestampでソートされ、各ユーザの時間順序が作成されました。
- A target column was created which is time-wise the next movie that the user will watch.  
  - ユーザが次に視聴する映画を時間的に示すターゲット列が作成されました。
- New columns such as average movie rating per user, average movie rating per genre per user, number of movies watched per user in each genre normalized by total movies watched by that user, etc. were created.  
  - ユーザごとの平均映画評価、ジャンルごとのユーザの平均映画評価、各ジャンルでそのユーザが視聴した映画の数をそのユーザが視聴した総映画数で正規化したものなどの新しい列が作成されました。
- The gender column was label encoded, and the occupation column was dummy encoded.  
  - 性別列はラベルエンコーディングされ、職業列はダミーエンコーディングされました。
- Continuous features were scaled as appropriate.  
  - 連続的な特徴は適切にスケーリングされました。
- A sparse binary tensor was created indicating movies that the user has watched previously.  
  - ユーザが以前に視聴した映画を示すスパースバイナリテンソルが作成されました。
- The dataset was split into train-test with an 80-20 ratio.  
  - データセットは80-20の比率でトレーニングとテストに分割されました。

The following diagram shows the various features generated through preprocessing. 
以下の図は、前処理を通じて生成されたさまざまな特徴を示しています。
Some or all of these features are used during experimentation depending upon the specific model architecture.  
これらの特徴の一部またはすべては、特定のモデルアーキテクチャに応じて実験中に使用されます。
Refer to the respective notebook for data preprocessing steps specific to each model.  
各モデルに特有のデータ前処理手順については、該当するノートブックを参照してください。



### Comparison Results 比較結果

The mean rank of the test set examples was computed using each model, and the following chart shows their comparison based on the best rank achieved on the test set. 
テストセットの例の平均ランクは各モデルを使用して計算され、以下のチャートはテストセットで達成された最高ランクに基づいてそれらの比較を示しています。 
In short, for this experiment: AFM > FFM » DeepFM > DLRM_simplified > Wide & Deep > NFM > FM.
要するに、この実験では: AFM > FFM » DeepFM > DLRM_simplified > Wide & Deep > NFM > FM です。



## Summary 概要

In this article, we defined the need for modeling feature interactions and then looked at some of the most popular machine-learning algorithms designed to estimate feature interactions under sparse settings. 
この記事では、特徴間の相互作用をモデル化する必要性を定義し、スパースな設定下で特徴間の相互作用を推定するために設計された最も人気のある機械学習アルゴリズムのいくつかを見ました。
We implemented all of the algorithms in Python and compared their results on a toy dataset.
私たちは、すべてのアルゴリズムをPythonで実装し、おもちゃのデータセット上でその結果を比較しました。



## References 参考文献

1. Cheng et al. (2016). Wide & Deep Learning for Recommender Systems. 7-10. 10.1145/2988450.2988454.
1. Cheng et al. (2016). Wide & Deep Learning for Recommender Systems. 7-10. 10.1145/2988450.2988454.
2. https://www.kaggle.com/datasets/prajitdatta/movielens-100k-dataset
2. https://www.kaggle.com/datasets/prajitdatta/movielens-100k-dataset



## Related Content 関連コンテンツ



## Embedding Collapse in Recommender Systems: Causes, Consequences, and Solutions
推薦システムにおける埋め込み崩壊：原因、結果、および解決策



## Incorporating Ads into Large Language Models Outputs 大規模言語モデルの出力への広告の組み込み



## The Evolution of Multi-task Learning Based Video Recommender Systems - Part 2
マルチタスク学習に基づく動画推薦システムの進化 - パート2



## The Evolution of Multi-task Learning Based Video Recommender Systems - Part 1
マルチタスク学習に基づくビデオ推薦システムの進化 - パート1



## An Introduction to Multi-Task Learning based Recommender Systems
マルチタスク学習に基づく推薦システムの紹介



## Be the First to Know 知ることが最初になる

Subscribe to get notified when I write a new post.  
新しい投稿を書くときに通知を受け取るために購読してください。

Subscribe  
購読する

We won't send you spam. Unsubscribe at any time.  
スパムは送信しません。いつでも購読を解除できます。

Did you find this article helpful?  
この記事は役に立ちましたか？

Buy me a coffee  
コーヒーを買ってください

Updated on 2023-06-03  
更新日: 2023年6月3日

Back  
戻る

Home  
ホーム

Gitalking ...  
Gitalking ...

Sumit Kumar  
スミット・クマール

CC BY-NC 4.0  
CC BY-NC 4.0
