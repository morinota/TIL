# SimClusters: Community-Based Representations for Heterogeneous Recommendations at Twitter

published date: August 2020,
authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
url(paper): https://www.kdd.org/kdd2020/accepted-papers/view/simclusters-community-based-representations-for-heterogeneous-recommendatio

(勉強会発表者: morinota)

---

## どんなもの?

- twitter の SimClusters (Similarity-based Clusters)というコミュニティ埋め込みベクトルを生成する手法の論文.
- 「K-POP」や「機械学習」といった共通の話題や、「職場が一緒」「高校が一緒」といった社会的関係から構成されるTwitter上のコミュニティ（約 $~10^5$ 件）を発見し、ユーザやコンテンツと各コミュニティの関連を表す埋め込みベクトルを生成する.
- 様々な推薦タスクに活用できる、汎用的な埋め込み表現であるとの事.(論文の後半のオンライン実験にて、活用法を紹介していた.)
- table 1は、Twitterにおける各パーソナライズド・レコメンデーション問題(サービス)の多様性をまとめたもの.
  それぞれ、推薦されるアイテムのカーディナリティ(=unique値の数だっけ?)と計算された推薦のshelf life(賞味期限)が異なっている.
- 本論文の中心的な動機付けとなる問いは、**パーソナライズやレコメンデーションが必要なTwitter製品のすべて、あるいはほとんどの精度を高めるのに役立つ一般的なシステムを構築できるか**という事.
- SimClustersは、DNN [5]やGCN [37]のような**ハイブリッドモデルに供給できるユーザとアイテムの表現(埋め込みベクトル)をスケーラブルに学習するアプローチである**、と本論文は主張している.(特徴量としての使い方)

![](https://camo.qiitausercontent.com/b7c906436ebb895d6e39309eea2985113a40be85/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f62613035656666382d653438612d376130352d353837332d6462306262383939396564622e706e67)

## 先行研究と比べて何がすごい？

本論文で提案するソリューションは、**ユーザ-ユーザグラフから、コミュニティ構造に基づく汎用的な表現を構築できる**という洞察に基づいており、各コミュニティは、そのコミュニティ内の多くの人々がフォローしているインフルエンサーの集合によって特徴づけられる.

**異なる種類のコンテンツ(i.e. 表1の各ターゲット)のそれぞれは、これらのコミュニティの空間におけるベクトルとして表され**、アイテム $j$ に対する $i$ 番目のコミュニティに対応するエントリは、$i$番目のコミュニティがアイテム $j$ にどれだけ興味を持っているかを示している.

本手法のデザインには、2つの特筆すべき点がある：

- 大規模な数値最適化問題を解く必要がある従来の行列分解法を避け、代わりに、スケールアップが容易なSimilarity検索とコミュニティ発見の組み合わせに頼っている. 既存のベースラインと比較して、10倍から100倍高速で、3倍から4倍高精度であり、 $∼10^9$ 個のノードと $∼10^{11}$ 個のエッジを持つグラフに容易に拡張することができる. 「K-POP」や「機械学習」といった共通の話題や、「職場が一緒」「高校が一緒」といった社会的関係から構成されるTwitter上のコミュニティ（約 $∼10^5$ 件）を発見することができる.
- 特定のコンポーネントに最も適したコンピューティングパラダイム(batch-distributed, batch-multicore, streaming-distributed)を使用できるように、全体的にモジュール式(=SimClustersの各stageが疎結合になってる?)で拡張可能な設計となっている

## 技術や手法の肝は？

SimClustersシステム(図1参照)は、2つのステージで構成されている：

![](https://camo.qiitausercontent.com/91062517c63bafedf6953cf10b1e3a74c62de8de/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f32623466333165372d653361632d306639642d656431392d6361316535303763623534332e706e67)

### 段階1: Communityの発見 (User Interest Representationsの取得)

この段階は、Twitterのユーザとユーザのグラフからコミュニティを発見することである. ここで言う"グラフ"とは、ユーザ間のフォロー関係を表す有向グラフ(directed graph)の事.
代表的な既存研究に習って、有向グラフを二部グラフ(bipartite graph)として再定義することが便利であることがわかっている.

#### メモ: bipartite graph(二部グラフ)ってなんだっけ?

> 数学、とくにグラフ理論における2部グラフ(にぶグラフ、英: bipartite graph)とは、**頂点集合を2つに分割**して、各部分の頂点が互いに隣接しないようにできるグラフのこと.
> 一般に**互いに隣接しない頂点からなる集合を独立集合**といい、頂点集合を n 個の独立集合に分割可能なグラフのことを n 部グラフ (n-partite graph) という.
> 完全二部グラフ: 頂点集合を2つの独立集合 V1, V2 に分割したとき、V1 と V2 の任意の頂点が隣接するグラフ.(i.e. 独立集合V_1のある一つの頂点は、もう一つの独立集合V_2内の全ての頂点と隣接している=繋がっている状況...! これは"完全"二部グラフの説明.)

#### 段階1における問題設定を定義:

左パーティション $L$(左の独立集合?) と右パーティション $R$ (=右の独立集合?)を持つbipartite user–user graph(=各頂点がユーザを意味するbi-partite graph)が与えられるとする.
そのグラフから $k$個の (おそらく重複する=独立な集合ではないって事?) bi-partite コミュニティを見つけ、各左ノード(=左の独立集合の各頂点)と右ノード(=右の独立集合の各頂点)にそのメンバーシップの強さ(=k個の各コミュニティに所属する度合いの強さ)を示す重みをつけてコミュニティに割り当てる.

#### 問題設定と sparse non-negative matrix factorizationの関連.

ユーザ->ユーザのフォロー関係を表す有向グラフを、二部グラフとして再定義するもう一つの利点は、ノードの右集合である $R$ をノードの左集合である $L$ と異なるように選択できること.
特に、**典型的なソーシャルネットワークの大部分の辺は少数のユーザに向けられている(=多くの一般ユーザがインフルエンサー的なユーザをフォローしている状況??)ので**、$L$ よりも小さな $R$ を選ぶことは理にかなっていると言える.
Twitterの場合、最もフォローされている上位$10^7$人のユーザを $R$ に含め、残りの全てのユーザを $L$ に含める(約 $10^9$ 個の頂点を左の独立集合に).

また、問題定義では、コミュニティとの関連性の強さを示す非負のスコアを左右(=2つの独立集合R と L?)の各メンバー(=ノード=ユーザ)に割り当てることを求めている.
そこで、左右のメンバーシップ(=2つの独立集合R と L の各頂点の、各コミュニティとの関連度合い)を疎な非負行列 $U_{|L|\times k}$ と $V_{|R|\times k}$ で表現する. ここで、$k$ はコミュニティ数である.
したがって、**bipartite community discoveryの問題(=上述した問題設定=bi-partite user-user graphから、各ユーザとk個の各コミュニティとの関連度合いを定量化する問題)は、sparse non-negative matrix factorization (NMF)の問題と密接な類似性を持っている**のである.

#### SimClustersは問題をどんなアプローチで解く?

SimClustersでは、図2におもちゃの例で示すように、次の**3ステップのアプローチ**を採用している.

![](https://camo.qiitausercontent.com/194f3a26deb259e329da2e62437508f49aad755b/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f65613534653939372d656632322d366463372d626538302d6239333261626561376433632e706e67)

- Step 1. Similarity Graph of Right Nodes: 右の独立集合$R$の類似度グラフを取得する.
- Step 2. Communities of Right Nodes: 右の独立集合$R$の類似度グラフから、k個のコミュニティを計算する(=$R$の各ユーザと各コミュニティとの関連度合いを定量化する).
- Step 3. Communities of Left Nodes: 左の独立集合$L$の各ノード(=頂点=ユーザ)を、Step 2で発見した各コミュニティに割り当てる(=各コミュニティとの関連度合いを定量化する).

行列因数分解の観点から、この3ステップのアプローチは、$A^{T}A$の固有値分解を介した行列$A$のSVDを実行する1つの方法とよく似ている.

#### Step 1: 独立集合$R$のSimilarityグラフを作る

このステップの目的は、右の独立集合$R$のノードを用いて、より小さな uni-partite(一部)の無向グラフ $G$ を構築する事.

$R$ 内の2つのユーザ($u$, $v$)間の重み(=similarityとして表される)を、二部グラフの左側(独立集合 $L$)の"フォロワーのコサイン類似度"に基づいて定義する.
"フォロワーのコサイン類似度"について具体的には、ユーザuとvについての"フォロワーのbinary incidence vectors(入射ベクトル)"をそれぞれ $\vec{x_u}$ と $\vec{x_v}$ とする(=長さは左集合 $L$ の大きさ.もし$L$のユーザiが$u$をフォローしていれば i番目の要素が1, それ以外が0であるようなbinaryベクトル). そのcosine類似度は、以下のように定義される.

$$
similarity(u, v) = \vec{x_u} \cdot \vec{x_v} / \sqrt{|\vec{x_u}||\vec{x_v}|}
$$

この定義によれば、2つのユーザは、二部グラフにおいて一人以上の共通の隣人(フォロワー)を共有するだけで、ゼロではない類似度がある.
すなわち similarityグラフ $G$ にエッジ(=ノード間の接続=辺)を持つことになる.
極端に密な similarityグラフ を生成しないために、similarityスコアがある閾値より低いエッジ(=接続)を破棄し、さらに各ユーザのsimilarityスコアが最も大きい隣人を最大で一定数のみ保持するようにする.

難しいのは、この類似ユーザ問題の解決は、**Twitterのスケールでは非常に困難である**ということ.

最終的に、このステップは、$~10^9$ 個のノードと$∼10^{11}$個のエッジを持つ有向/二部グラフを入力とし、$~10^7$ 個のノード(入力された二部グラフにおける独立集合$R$の要素数)と $~10^9$ 個のエッジを持つ無向のsimilarityグラフを出力する.
つまり、shared-nothing のcluster-computing規模から、shared-memory のマルチコア規模になる、らしい.(=>グラフのスケールが大幅に削減された事で、複数のリソースにまたがる分散処理ではなく、一つのリソース内で共有メモリを使用するようなマルチコア処理で計算可能になった、って事っぽい...!)

#### Step 2: 独立集合$R$のSimilarityグラフから、k個のコミュニティを発見する

前のステップで得られた無向の(おそらくは重み付けされた)Similarityグラフを用いて、このステップでは、密に接続されたノード集合(=右のユーザ集合)のコミュニティを発見することを目的としている.
入力されたSimilarityグラフの構造を正確に保持するためには、**ある1コミュニティ当たりのノード数($k$)が数千、数万ではなく、数百であることが重要**であることが確認されている.
つまり、ノード$∼10^7$個、エッジ$∼10^9$個の入力グラフを処理して、$∼10^5$ 個(=$∼10^7$個で$10^2$で割っている)のコミュニティを見つけることができるアルゴリズムが必要.
しかし、コミュニティ発見アルゴリズムの長い歴史にもかかわらず、これらの規模要件を満たすことができる既存のソリューションを見つけることができなかった.
以下で、今回の要求を満たすために開発した **Neighborhood-aware Metropolis Hastings(以下、Neighborhood-aware MH)**と呼ばれるアルゴリズムについて説明する.

##### Metropolis Hastings sampling approach

本アルゴリズムは、**重複するコミュニティを発見するために[33]で発表されたMetropolis Hastings sampling approach**を拡張したものであり、まず背景として説明する.

$Z_{|R|\times k}$ を疎なbinaryのコミュニティ割り当て行列(**community assignments matrix**)とし、 $Z(u)$ は頂点$u$が割り当てられたコミュニティの集合を表す(言い換えれば、$Z(u)$ は、行列 $Z$ の $u$ 行目から非ゼロの列indicesを出力するfunctionみたいな感じ?)、と仮定する.
式1は、Zに対する目的関数を指定している.(Zが推定すべきパラメータなのか...!)

$$
F(Z) = \alpha \sum_{u, v \in E}  1(|Z(u) \cap Z(v)| > 0)
+ \sum_{u, v \notin E}  1(|Z(u) \cap Z(v)| = 0)
\tag{1}
$$

ここで、

- 1 はindicator function(=特定の条件を満たす場合だけ1を返し、それ以外は0を返すfunction).
- $F(Z)$は2つの項の合計.(それぞれ 割り当てbinary行列$Z$を入力として計算できる.)
- 第一項は、グラフ内のノードの隣接するペアが少なくとも1つのコミュニティを共有する数をカウントする.
- 第二項は、グラフ内のノードの非隣接ペアがコミュニティを共有しない数をカウントする.
- **実際の大規模ネットワークのほとんどは非常にスパースなので、パラメータ$\alpha$ を用いて最初の項の寄与を重み付けすることが有用**. $\alpha$ の値が増加すると、目的関数はよりZの非ゼロ要素に基づいて最適化することになる.

また、上記の目的関数は、**全体の目的関数 $F(Z)$ が個々の頂点に対する関数 $f(u, Z)$ の和として表現できる**意味で、分解可能である. (ここで、$N(u)$ はある頂点 $u$ のneighbors集合を表す.)

$$
f(u, Z) = \alpha \sum_{v \in N(u)} 1(|Z(u) \cap Z(v)| > 0)
+ \sum_{v \notin N(u)} 1(|Z(u) \cap Z(v)| = 0)
\tag{2}
$$

以上の背景を踏まえ、まずアルゴリズム1において、重複するコミュニティを一般的な方法で発見するアプローチを説明する.

![](https://camo.qiitausercontent.com/636b650123d6050e0ad7dd598d84f8e6dab0ff32/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f33613335616133642d316333332d346239652d303463392d3531303532653430303734332e706e67)

- binary割り当て行列 $Z$ を初期化した後、最大で $T$ epoch 回 最適化を実行し、各epoch ではグラフ内のすべての頂点をシャッフルした順序(?)で反復する.
- 各頂点 $u$ について、proposal function(=コードの関数)を用いてコミュニティ割り当ての新しい集合 $Z'(u)$ をサンプリングし、新しく提案された$Z'(u)$ と現在のコミュニティ割り当てのセット $Z(u)$ の間の目的関数の違いを計算する.
- もし $Z'(u)$ の方が良ければ、$Z$を置き換える. もしそうでなくても、アルゴリズム1の6行目で示されるように、ある確率で置き換える.
  - [33]で述べられているように，決定論的な最適化手順ではなく，ランダムな最適化手順を好む理由の1つは，局所最小値にはまるのを避けることが目的.

##### 既存研究[33]の手法: ランダムMH(Metropolis-Hastings)

[33]で行われた`Initialize` function と`Proposal` function の具体的な選択方法は、アルゴリズム2に記載されている.

![](https://camo.qiitausercontent.com/d263bcb74e394587b46a57d75b88a06105c302ec/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f31656530393931352d656334662d346233332d353139652d3733353465613566343034342e706e67)

これらの機能は、純粋にランダムなサンプリングで実装されているため、この手法を"**ランダムMH(Metropolis-Hastings)**"と呼んでいる.
ランダムMHの主な実用上の欠点は、$k$ の値が適度であっても、満足のいく精度の解を得るのに非常に時間がかかるということである.(最適化戦略無しに、ランダムに、より良いパラメータを探索しているから...!)
これは、`Proposal` function が各ステップで完全にランダムなコミュニティ割り当てベクトルを生成し、現在の割り当てベクトルと照らし合わせて評価することを考えれば、驚くべきことではない. $k$ が増加すると、コミュニティ割り当ての空間(=パラメータの選択肢のイメージ)は指数関数的に増加し、`Proposal` function が許容できるtransition (パラメータ更新)を生成できる可能性は非常に低くなる.

##### 提案手法: Neighborhood-aware Metropolis Hastings

既存手法の代わりに、アルゴリズム3で規定される **Neighborhood-aware MH(Metropolis-Hastings)** を提案する.

![](https://camo.qiitausercontent.com/79362c9271640af7550a9c152c52728a49cc6559/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f37313061323631662d363433382d663137382d343864662d3462396362353639373839642e706e67)

Neighborhood-aware MH(Metropolis-Hastings) の proposal functionは、以下の2つの洞察 & 仮定に基づいている:

- 1つ目は、あるノード(=頂点=ユーザ)が、その隣接するノードが現在所属していないコミュニティに所属する可能性は極めて低いということ.
- 2つ目は、**ほとんどの実用的なアプリケーションでは、ノードを少数のコミュニティ以上に所属させる必要はない(?)**ということである.

次のような2段階のproposal function を設計している.

- 最初のステップでは、与えられたノード $u$ について、$u$ のすべてのneigborsを繰り返し、$Z$で彼らのコミュニティ割り当てを検索し、**少なくとも一度は現れるコミュニティ集合**を識別し、それを 部分集合$S$と呼ぶ. 
- 第2ステップでは、第1ステップで得られた $S$ のサイズ $\leq l$ のすべての部分集合について反復処理を行う.
  - ここで、$l$ は、**ある1ノードが割り当てられるコミュニティの数に対する上限値**である.この値はuser-provided(=要するに開発者が指定するハイパーパラメータの意味!).
  - 各サブセット $s$ について、式2より関数 $f(u, s)$を計算し、最後に $e^{f(u,s)}$ に比例する確率でサブセット $s$ をサンプルする. (i.e. ソフトマックスを適用する)
  - (要するに、**近傍コミュニティ集合Sからl個のアイテムをサンプリングしてuの所属コミュニティとする**、って意味? この時、サンプリングはf(u, s)に基づく離散確率質量分布に基づくという事??)
  - $f(u, s)$の計算方法は、$Z(u) = s$とした場合の目的関数f(u, Z)の値、という認識...!

そして、アルゴリズム1の6行目と7行目に規定されているように、サンプリングの結果が受け入れられるか、拒否されるかのどちらかになる.
$Z$の初期化については、各コミュニティにグラフ内のランダムに選ばれたノードのneigbborhoodをシードする.(?)

#### Step 3: 独立集合$L$と、k個の各コミュニティとの関連度を定量化する

前のステップの出力は、右集合に対するコミュニティ割り当て行列 $V_{|R| \times k}$ である. (i.e. $i$ 番目の行が右ノード$i$が割り当てられたコミュニティを指定する行列)
問題設定における残りの問題は、左集合に対するコミュニティ割り当て行列 $U_{|L| \times k}$ を取得する事. (i.e. i番目の行が、左ノードiが割り当てられたコミュニティを指定するような行列)

この割り当てを行う簡単な方法は、左集合の各ノードのneighbors(=全て右集合のノードであるはず!)が割り当てられているコミュニティを見ることによって、左ノードをコミュニティに割り当てること.
より正式には、$A_{|L| \times |R|}$ を**入力二部グラフの隣接行列(adjacency matrix)**(なるほど、二部グラフの入力も行列で表せば良いのか...!)とすると、$U = truncate(A\cdot V)$ とする事である.
ここで、$truncate()$ 関数は、ストレージを節約するために、各行(=左の独立集合の各ノード=各ユーザ)に対してある一定の数までのnon-zero要素だけを保持する.(=任意の1ユーザが所属するコミュニティの数を制限するfunction...!)

ちなみに、この$U$の計算式は、「$V$が正方直交行列(orthonormal matrix)であるケース(i.e. $V^T V = I$であるケース)に、$U = A \cdot V$ は $A = U \cdot V^T$ の解になる.」という事実に動機づけられている.
$V$がorthonormal matrixの場合(これは、**各右ノードを最大1つのコミュニティに割り当てることで実現できる**)(=あ、じゃあ運用する上では基本的に、$V$ は正方直交行列になるのか...!)と、そうでない場合の両方で実験を行い、いずれの場合も、結果として得られる $U$ が左nodesを正確に表現することを発見した.
(あ、じゃあ結局$V$がorthonormal matrixではなくても問題なさそうなのか...!)

上の計算式で得られた $U$を**User Interest Representations** と呼び、以降のステップの主要な入力情報を形成する.(=UがSimClustersの段階2の入力情報になる...? $V$はならない?)
このステップの計算は、Hadoop MapReduce のようなバッチ分散コンピューティングパラダイムで実装することで、プロダクト運用上の要求に合わせて**簡単にスケーリングすることができる**.(処理の並列化に関しては、正直あまりイメージがついていない.)

### 段階2: Item Representations の取得

本節では、**ツイート、ハッシュタグ、ユーザなど、様々な推薦問題の対象となりうるアイテムに対する表現(=embedding)を計算する方法**について説明する.

段階2の**一般的な枠組みは、アイテムに関わったすべてのuser interest表現を集約してアイテムの表現を計算すること**(なるほど...!シンプル!). つまり、アイテム $j$ のSimClusters表現は、

$$
W(j) = aggregate({U(u), \forall u \in N(j)})
\tag{3}
$$

ここで、$N(j)$ は、対応するユーザ-アイテム二部グラフにおいてアイテム$j$に関与したすべてのユーザを示し、$W(j)$ と $U(u)$ はいずれもベクトルとする.
$aggregate$関数は、さまざまなアプリケーションに基づいて選択することができ、特定の教師付きタスクから学習することも可能[13].
この場合、$W(j,c)$ を**コミュニティ$c$の平均的なユーザがこのアイテム$j$に現在抱いている興味のレベル**と解釈できるように、比較的単純で解釈しやすい$aggregate$関数を選択することになる.
本手法では、**aggregate関数として"exponentially time-decayed average(指数関数的時間減衰平均)"を選択**した. これは、アイテムに関わったユーザの貢献度を、そのユーザがアイテムに関わった時間に基づいて指数関数的に減衰させる.
**指数関数的減衰に使用する半減期はアイテムに依存**し、賞味期限(shelf-life って表現されるんだ...!)が長いもの(トピックスなど)には長い半減期を設定し、賞味期限が短いもの(ツイートなど)には短い半減期を設定している。

結果として得られるベクトル$W$は$U$よりもはるかに密度が高く(=>$U$の要素はbinary?で離散的だけど、$W$の場合は連続的な数値だから?)、その非ゼロ値をすべてスケールで保存することは有益ではない.
その代わりに、$W$のview (指標、サブセット、要約統計量的なイメージ?)を2つ追加し、それぞれがトップ$k$ viewを保持する. (値が大きい要素のみを記録する、みたいな?)
first view は$R$で、$R(j)$は**アイテム$j$のトップkコミュニティを追跡する**.
second viewは$C$で、$C(c)$ は**コミュニティ$c$のトップアイテムを追跡する**.
賞味期限が長いものの場合、W、R、Cの計算は、例えば、Hadoop MapReduceを使ってバッチ式で行うのが無難である.

しかし、賞味期限が短いものを扱うとなると、更に興味深い.
この場合、指数関数的に時間的に減衰する平均の大きな利点(例えば時間窓付き平均とは異なる)が実現され、それは$W$のインクリメンタルな更新を容易にすることにつながる.
具体的には、Wの各セルについて、**現在の平均値そのものと、それが更新された最後のタイムスタンプ、という2つの情報のみを保持すればよい**.
アルゴリズム4の4行目から7行目に詳述するように、**新しいユーザとアイテムのエンゲージメントが到着すると、前回の更新からの経過時間に基づいて減衰係数を計算することで、アイテムのWを更新することができる**.(online更新ができるのはいいね...!)

運用上では、2つのtop-k ビュー $R$ と $C$ は、低遅延のkey-valueストアに保存される.
この2つのview(指標?)を用いると、**任意のユーザやアイテムの最近接者を簡単に検索することができる.** ユーザやアイテムと関連度の高い(=興味が近い=active inな) 上位のコミュニティを調べ、そのコミュニティごとに上位のユーザやアイテムを特定するだけでよいのである.
これらの候補は、その完全な表現(=embeddingベクトル)を取得し、queryオブジェクト(ユーザまたはアイテムのいずれか)の表現(=embeddingベクトル)との**類似性を計算することによってランク付け**することができる.
その結果、すべてのユーザやアイテムを総当たりでスキャンする必要も、特別な最近傍インデックスを構築する必要もない.

### 運用方法:

SimClustersは、Twitter社で1年以上前から本番環境に導入されている.
SimClustersシステムから出力されるすべての表現は、**モデルバージョンでキーが設定されており、複数のモデルを並行して運用すること**で、既存の生産に影響を与えずに新しいパラメータやコードの変更を試すことができる.
現在、本番稼働中のメインモデルでは、フォロワー数上位$∼10^7$人のユーザのsimilarityグラフから発見された$∼10^5$のコミュニティが表現されている.
モデルによって発見されたbipartiteコミュニティは、入力されたbipartiteグラフのエッジの70%近くを含んでおり、グラフの構造のほとんどを捉えていることが示唆される.

ステージ1のうち、**ステップ1(類似度計算)は最もコストがかかるステップで、Hadoop MapReduceでエンドツーエンドで実行するのに約2日かかる**が、このジョブはSimClusters以前から運用されていたため、SimClustersによる追加コストではない.
(高い頻度でバッチ実行するような感じではないのかな...。一ヶ月に一度とか? まあこのステップで使用するユーザデータは上位ユーザのみだからすでにデータは十分揃っていて、短期間で傾向がかわる事はないだろうから問題なさそう...!)
ステップ2はSimClustersの起動時に初めて実行された. その後、現在の$V$で初期化した Neighborhood-aware MHの短縮版を実行することにより、ユーザとユーザの類似性グラフの変化を考慮し、$V$行列を更新している.
また、**Step3は、最新版のユーザ-ユーザグラフとStep2の最新$V$を使い、Hadoop MapReduce上でバッチアプリケーションとして定期的に実行される**.
ステップ3の出力($U$行列)(=一般ユーザのcommunity表現ベクトル)を得た後は、$V$行列(=上位ユーザのcommunity表現ベクトル)を直接使用することはない。$V$行列は一般的にスパースすぎて正確なモデリングができない.

Stage2では、"user influence"表現(=ユーザがどのコミュニティで影響を発揮しているかを表すベクトル)と"Topic"表現の**2つのバッチジョブ**と、"ツイート"表現と"トレンド"表現(=これも単に人気度が高いトレンドを全員に見せている訳でなく、各communityと親和性の高いトレンドを探してるのか...!)の**2つのストリーミングジョブ(=online更新的なジョブ.)**の計4つのジョブを現在用意している.
**user influence表現の目的**は、ユーザがどのようなコミュニティに興味を持っているかを表す為のuser interest表現(=ステージ1の出力)とは対照的に、**ユーザがどのようなコミュニティで影響を発揮しているか**を表すことである.
user influence表現は、より多くのユーザをカバーし、またユーザの元のサブセットに対してより密であるため、この目的のために元の$V$行列(=これって上位ユーザのuser interest表現じゃなかったっけ?)よりも優れている.(計算方法は、ステージ2の他のアイテムと同じなのかな...="上位ユーザ"をアイテムとして計算する感じ?)
トピック表現は、どのコミュニティがトピックに最も興味を持っているかを示すもので、これを計算するための入力は、ユーザinterest表現と、ユーザ-トピックの関係グラフの両方である.(アイテム=トピックとしたver.)
ツイート表現とトレンド表現は、リアルタイムで発生するユーザとツイートのエンゲージメントを入力とするストリーミングジョブで計算・更新される.

すべてのSimClusters表現において、ゼロでないものだけを保存し、すべての場合においてゼロに近いエントリーを切り捨てている点が、2種類のveiw $R$と$C$を使用する事のメリット.
user interest表現は約$∼10^9$人のユーザをカバーし、user influence表現は約$∼10^8$人のユーザをカバーしており、どちらの表現も平均10~100個の非ゼロ要素を有している.(user influence表現の方がオーダーが小さいのは、user interest表現を元にaggregate計算する際に、ある一定数以上フォローされている必要があるから?)
ある時点で推薦されるツイートやトレンドの数は少ないが(表1参照)、その表現はより密で、平均して約 $10^2$ の非ゼロ要素を持つ.
なお、以下の4つの表現(user influence、トピック、ツイート、トレンド)については、反転した指標も維持している: あるコミュニティが与えられたとき、そのコミュニティと関連度の高いトップkユーザー/トピック/ツイート/トレンドは何か(セクション4では$C$と表記している).
$C$は、他の表現とのドット積やコサイン類似度が最も大きい表現を持つアイテムを検索するために不可欠.

## どうやって有効だと検証した?

Twitterの各推薦機能にてオンラインテストを行い、いずれもcontrol群と比べてtreatment群の方が高いmetricsスコアを出したとの事.

### ツイート詳細ページでの類似ツイートの推薦:

メールやプッシュ通知でツイートにアクセスしたユーザに対して、Twitterは他のおすすめツイートと返信を並べたモジュールを表示する.
このモジュールは、SimClustersの前に、作者の類似性(ページ上のメインツイートの作者と多くのフォロワーを共有するユーザーが書いたツイート)にのみ基づいてツイートを検索していた.
オンラインA/Bテストでは、SimClusters表現に基づく類似ツイートを追加した. つまり、SimClustersの表現(=どのcommunityと関連度が高いかを表すベクトル)がページ上のメインツイートの表現と高いコサイン類似度を持つツイートを取得した.

その結果、ツイートに対するエンゲージメント率が25％高くなることがわかった.

その後更に、SimClustersに基づくこのproductの第二のソース候補を追加した.
SimClusters表現が、ページ上のメインツイートの著者のuser influence表現(=ユーザがどのコミュニティで影響を発揮しているかを表すベクトル)と高いコサイン類似性を持つツイートを検索する.
このソースを追加することで、カバー率はさらに向上し、全体のエンゲージメント率が7%向上した.

### Home フィードにおけるおすすめツイート

**Twitterのホームフィード**は、直接フォローされているユーザのツイートと、フォローされていないユーザのおすすめツイート（以下「ネットワーク外ツイート」）の両方から構成される.
SimClusters以前は、推薦ツイートの主なアルゴリズムは「ネットワークアクティビティ」と呼ばれるものだった. つまり、GraphJet [31]を使用して、閲覧ユーザのフォロー（つまりネットワーク）がどのツイートに「いいね」を付けているかを特定する. これが推薦アイテムの主なcandidate sourceだった.

**ツイートのSimClusters表現**(ツイートがどのcommunityと関連度が高いか?を表すベクトル)を使って、ネットワークアクティビティツイートを補足する2つのcandidate sources を構築した.
第1のcandidate sources は、リアルタイム表現(=現時点でのツイートのSimClusters表現)が閲覧ユーザのinterest表現とのドット積が最も高いツイートを特定する.
2つ目の候補は、アイテムベースの協調フィルタリングに基づくもので、セクション6.1で説明した「類似ツイート」アプリケーションと同じ基本的な実装を使用して、ユーザが最近「いいね！」を押したツイートと類似するツイートを特定する. (類似度の評価に使用するのは simclustersで作ったtweet表現.=>関連するコミュニティに基づく類似度!)

この2つの新しいcandidate sourceからの推薦アイテム候補を、本番の既存手法による推薦アイテム候補(Homeの特定のポジション)に置き換えて、オンラインでA/Bテストを実施した.
実験では、ネットワークアクティビティで生成されたcandidateと比較して、新しいcandidateのエンゲージメント率が33%高い結果となった.

新しい候補とは別に、user interest表現やツイート表現を利用して、あらゆるソースから来る候補のランキングを改善することもある.
ユーザとアイテムの表現は、エンゲージメント予測モデル(ランキングモデル)の入力において、既存のユーザ特徴、アイテム特徴、およびユーザとアイテムの相互作用特徴のセットを豊かにするために使用される. (=>候補生成後のランキングモデルの特徴量として使用するみたいな感じ)
A/Bテストでは、これらの特徴量で学習させたモデルは、推薦コンテンツのエンゲージメント率を4.7%相対的に高めることができ、成熟したモデルとしては大きなリフトアップ効果があった.

### Personalized Trends のランク付け

トップトレンドのコンテンツ(ハッシュタグ、イベント、ニュース速報など)を表示することは、地域や世界で起こっていることをユーザに知らせる重要な方法.
Trendsの実装は、Trendsの検出とランキングの2段階を踏んでいる.

トレンドのSimClusters表現を使って、user interest表現とリアルタイムのtrend表現のdot product(内積!)を使用することで、与えられたユーザ-トレンドペアをスコア化した.
A/Bテストでは、このスコアを使用することで、Trends自体のユーザエンゲージメントが8％増加し、さらにクリック後のランディングページのエンゲージメントが12％増加することがわかった.

これらの改善は、この推薦機能で行われた他の実験と比較すると、大きなものである.

### Topic Tweetの推薦

「ファッション」や「マーベル映画」など、あらかじめ定義されたトピック(=キーワードみたいな概念?)がある場合、そのトピックに関するコンテンツを表示する機能.
ここでの推薦機能がリリースされる前は、主に人間の専門家がキュレーションしたテキストマッチングルールに依存して、トピックツイートを識別していた(ようするにルールベースの手法だった).
この方法では、多くの誤検出(主にツイートのテキストがトピックのルールと偶然一致することによる)があることがわかったので、今回SimClustersを用いた推薦機能をテストした.
まずSimClusters表現を用いて、対象のtopic表現と高いコサイン類似度を持つツイート表現を特定する.
次にテキストマッチング規則(??既存のアプローチ? 二段階にしたって事?)を適用した.
社内で評価したところ、2番目のアプローチの方がはるかに良い結果が得られたため、このアプローチでproductをlaunchしたとのこと.
この推薦機能は、リリース以来、外部で好評を博し、より多くのユーザからツイートへのエンゲージメントを高めている.

### ユーザフォローの推薦

Who To Followレコメンデーションの候補は、エンゲージメント予測モデルを用いてランク付けされる. このモデルには、**閲覧ユーザと候補ユーザのSimClusters表現**に基づく新しい特徴量が加えられている.(特徴量としての活用.)
A/Bテストでは、これらの新たな特徴量を使用することで、フォロー率が7％向上することが確認された.

## 議論はある？

今後のSimClusters表現の活用として以下の3つが挙げられていた.

### 通知品質フィルター

Twitterプロダクトの重要なタスクとして、罵倒やスパム的なリプライやメンションを受けないようにユーザを保護することがある.
**ユーザとユーザのブロックグラフ（あるユーザーが他のユーザーをブロックした場合）に基づく新しいユーザ表現をSimClustersで開発**し、この表現を特徴として、罵倒やスパムのような返信をフィルタリングするモデルを学習した.
オフラインテストでは、PR-AUC が 4％向上するという素晴らしい結果を示した.

### 特徴量の組み合わせから教師付き埋込を行う

SimClustersの表現は、主に様々なエンゲージメントグラフから情報を取得するが、**ユーザやアイテムに関する他の特徴(例えば、フォロワー数やジオ情報)と組み合わせるアプローチ**も試している.
有望な初期結果を得ているアプローチの1つは、補助的な予測タスク(エンゲージメント予測など)でディープニューラルネットワークを訓練することで、入力特徴としてユーザとアイテムのSimClusters表現と、ユーザとアイテムのために以前に開発した特徴の両方を使用する.
このニューラルネットに適切なアーキテクチャ、例えば2塔式DNNモデル[36]を選択することで、ユーザーとアイテムについて別々に密な埋め込みを学習することができるようになる.(説明変数にユーザやアイテムのsimClusters表現、目的変数にCTR等のengagementスコアで学習させ、中間層を新たなembeddingとして抜き出す、みたいなアプローチ?)

### リアルタイムイベント通知

Twitterでの主な用途は、大きなニュースが起こったときに、興味を持ちそうなユーザに通知することである.(プッシュ通知みたいなことか...!)
イベントのSimClusters表現(これは、そのイベントに関する人間が作成したツイート表現を集約することで得られる)を使って、**そのイベントに興味を持つユーザのコミュニティを特定**し、そのコミュニティに興味を持つユーザをターゲットにすることができる. (新規アイテムの場合はどうしたらいいんだろう... そのアイテムの属性情報と類似したツイート表現や、作成者のUser表現を使ったら、aggregateして新規イベント表現を作れるだろうか...?)

## 次に読むべき論文は？

- neighborhood-basedベースの手法 vs 最新のDNNによるモデルベースの手法の比較の論文 [Are We Really Making Much Progress? A Worrying Analysis of Recent Neural Recommendation Approaches](https://arxiv.org/abs/1907.06902)

## お気持ち実装

### ステージ1のstep1: Similarity graphの算出処理.

テストコード:

```python:test_similarity_graph.py
import numpy as np
from similarity_graph import SimilarityGraph


def test_similarity_graph_build() -> None:
    # 行:左の独立集合L, 列:右の独立集合Rを表す行列
    bi_partite_graph = np.array(
        [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 1],
            [1, 1, 0],
            [1, 1, 1],
        ]
    )  # 各要素:binary.行ユーザが列ユーザをフォローしているか否か
    similarity_graph_expected = np.array(
        [
            [1.0, 0.66666667, 0.408248],
            [0.66666667, 1.0, 0.408248],
            [0.408248, 0.408248, 1.0],
        ]
    )  # (Rの数) * (Rの数)の正方行列. 無向グラフなので、対角線に対して線対称な値.

    similarity_graph_actual = SimilarityGraph.build(bi_partite_graph)
    assert similarity_graph_actual.shape == similarity_graph_expected.shape
    np.testing.assert_array_almost_equal(
        similarity_graph_actual,
        similarity_graph_expected,
        decimal=4,
    )


def test_similarity_calc_cosine_sim() -> None:
    x_u = np.array([0, 1, 0, 1, 1])
    x_v = np.array([1, 0, 0, 1, 1])
    cosine_sim_expected = np.dot(x_u, x_v) / (np.linalg.norm(x_u) * np.linalg.norm(x_v))

    cosine_sim_actual = SimilarityGraph._calc_cosine_sim(x_u, x_v)

    assert np.isclose(cosine_sim_actual, cosine_sim_expected)
```

実装

```python:similarity_graph.py
import abc
import itertools

import numpy as np
from colorama import reinit


class SimilarityGraphInterface(abc.ABC):
    @abc.abstractclassmethod
    def build(cls, bi_partite_graph: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class SimilarityGraph(SimilarityGraphInterface):
    @classmethod
    def build(cls, bi_partite_graph: np.ndarray) -> np.ndarray:
        len_R = bi_partite_graph.shape[1]
        similarity_graph = np.zeros(shape=(len_R, len_R))
        for u, v in itertools.combinations_with_replacement(list(range(len_R)), r=2):
            if u == v:
                similarity_graph[u, u] = 1.0
                continue
            x_u = bi_partite_graph[:, u]
            x_v = bi_partite_graph[:, v]
            cosime_sim = cls._calc_cosine_sim(x_u, x_v)
            similarity_graph[u, v] = cosime_sim
            similarity_graph[v, u] = cosime_sim
        return similarity_graph

    @classmethod
    def _calc_cosine_sim(cls, x_u: np.ndarray, x_v: np.ndarray) -> float:
        dot_product = np.dot(x_u, x_v)
        norm_u = np.linalg.norm(x_u)
        norm_v = np.linalg.norm(x_v)
        return dot_product / (norm_u * norm_v)
```

### ステージ1のstep 2: コミュニティ発見(インフルエンサーのコミュニティ表現 $V$の取得)

#### Metropolis-Hastingsの損失関数のテストと実装

明日追加します!

#### 既存手法 ランダムMH(Metropolis-Hastings) と 提案手法 Neighborhood-aware MH(Metropolis-Hastings)

明日追加します!

### ステージ2 : ステージ1で算出したUser Interest 表現を用いて、他のSimClusters表現を生成する

近日中に追加します!
