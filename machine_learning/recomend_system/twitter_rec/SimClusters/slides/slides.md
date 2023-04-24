---
format:
  revealjs:
    # incremental: false
    # theme: [default, custom_lab.scss]
    theme: [default, custom_lab.scss]
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: twitterの様々な推薦機能で活用されてるらしい、ユーザ-ユーザのフォローネットワークからコミュニティ埋め込み表現を生成するSimClustersの論文を読んだ
subtitle: n週連続 推薦システム関連の論文読んだシリーズ13週目(毎週水曜更新)
date: 2023/04/24
author: NewsPicks Data/Algorithm unit インターン 森田大登
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## この論文を選んだ経緯

- 2023/04/01頃に、twitterの推薦アルゴリズムの一部(“For Youフィード” -ツイート推薦の機能)が、ソースコード + techブログによる解説という形で公開されました。
- その中で今回は、twitterの様々な推薦機能で共通基盤として活用されているらしい **SimClusters** という手法によるユーザ + 各種コンテンツの埋め込みベクトルの生成手法に注目しました。
- SimClutersは、**ユーザ-ユーザのフォローネットワークからコミュニティを発見**して、コミュニティ埋め込みベクトル(SimCluters表現)を作ります。(SNS特有の手法...? :thinking:)
- NewsPicksは経済ニュースサービスの性質に加えてSNSの側面もあるので、ユーザやキーワードフォローの情報の活用可能性もあるのでは...? :thinking:
- また、現在NewsPicksでは関連記事やプッシュ通知パーソナライズ等、複数の推薦機能が稼働中or予定なので、"共通基盤"という言葉に惹かれました。

## 参考:

- [SimClustersの論文](https://www.kdd.org/kdd2020/accepted-papers/view/simclusters-community-based-representations-for-heterogeneous-recommendatio)
- [公開されたtechブログ](https://blog.twitter.com/engineering/en_us/topics/open-source/2023/twitter-recommendation-algorithm)
- [公開されたgithub リポジトリ](https://github.com/twitter/the-algorithm)

## SimClusters論文の基本情報

- title: SimClusters: Community-Based Representations for Heterogeneous Recommendations at Twitter.
- ("for Heterogeneous Recommendations" 性質の異なる複数の推薦機能達の為の...:thinking:)
- published date: August 2020,
- authors: Wondo Rhee, Sung Min Cho, Bongwon Suh
- url(paper): https://www.kdd.org/kdd2020/accepted-papers/view/simclusters-community-based-representations-for-heterogeneous-recommendatio

## どんなもの?

- twitter の **SimClusters (Similarity-based Clusters)**というコミュニティ埋め込みベクトルを生成する手法の論文.
- 「K-POP」や「機械学習」といった共通の話題や、「職場が一緒」「高校が一緒」といった社会的関係から構成されるTwitter上のコミュニティ（約 10^5件）を発見し、ユーザやコンテンツと各コミュニティの関連を表す埋め込みベクトルを生成する.
- 様々な推薦タスクに活用できる、汎用的な埋め込み表現であるとの事.(論文の後半のオンライン実験にて、活用法を紹介していた.)

## SimClustersのモチベーション

- Twitterでは多種のアイテムに対して推薦機能がリリースされている:Tweet, Event, Topic(NPにおけるキーワード的な位置づけらしい), ハッシュタグ, ユーザ
- 推薦アイテム達はそれぞれ異質(Heterogeneous)である：Item Cardinality(=計算のスケーラビリティに影響を与える)とShelf Life(推薦生成のlatencyに制約を与える. 賞味期限的なもの)が異なる(table 1参照)
- これまでTwitterは、**これらの異なる推薦問題に個別に対応するシステムを構築しており、再利用や共通化はほとんど行われていなかった**。

![](https://camo.qiitausercontent.com/b7c906436ebb895d6e39309eea2985113a40be85/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f62613035656666382d653438612d376130352d353837332d6462306262383939396564622e706e67)

## Shelf Life が異なるケースって例えばなんだっけ

- フォロワーグラフ(フォロー関係のネットワーク)は比較的ゆっくりと変化するため、ユーザフォローの推薦は数週間にわたってユーザ嗜好との関連性を保つことができる(したがって、**バッチ処理で計算することができる**)
- 一方で、ツイート推薦は陳腐化するのが早い(i.e. lifespanが短い:thinking:)為**オンラインシステムでリアルタイムに近い形で生成する必要があり**、この場合、バッチ計算では要件を満たせない.
- NPの例で言えば、通常の経済ニュースはShelf Lifeは短め。(ツイートよりは長そうだが、shelf lifeは2~3日?:thinking:)
- NPオリジナル記事やオリジナル動画、トピックス(=専門家による記事)等は、もっとShelf life長い気がする:thinking:
- ユーザやキーワードは更にshelf lifeが長いはず:thinking:

## SimClustersのモチベーション

#### 目的:

- 異質(Heterogeneous)な全て or ほとんどの推薦機能の性能を高めるのに役立つ共通基盤的なシステムを構築したい...!

#### 解法

- **ユーザ-ユーザグラフからコミュニティ埋め込みベクトル**を作る。
- 各コミュニティは、そのコミュニティ内の多くのユーザがフォローしているインフルエンサー集合によって特徴づけられる。
- 異質(Heterogeneous)な推薦コンテンツ(i.e. table 1のターゲット)のそれぞれは、**コミュニティ空間におけるベクトル**として表され、アイテム $j$ に対する $i$ 番目のコミュニティに対応する要素は、$i$番目のコミュニティがアイテム $j$ にどれだけ興味を持っているかを示している。
- 最終的には、**異質な推薦対象を、同じ空間のスパースで解釈可能なベクトルとして表現でき**、様々な推薦やパーソナライゼーションタスクに活用可能。

# 技術や手法の肝は?

SimClustersシステム(図1参照)は、2つのstageで構成されている：

![](https://camo.qiitausercontent.com/91062517c63bafedf6953cf10b1e3a74c62de8de/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f32623466333165372d653361632d306639642d656431392d6361316535303763623534332e706e67)

- stage 1: Communityの発見 (User Interest Representationsの取得)
- stage 2: 各種 Item Representationsの取得

## stage 1: Communityの発見 (User Interest Representationsの取得)

- stage 1 は、Twitterのユーザとユーザのグラフからコミュニティを発見する
- ここで言う"グラフ"とは、**ユーザ間のフォロー関係を表す有向グラフ**(directed graph)の事。
- 代表的な既存研究に習って、有向グラフを**二部グラフ(bi-partite graph)として再定義**して扱う

## 二部グラフ(bi-partite graph)ってなんだっけ?

> 数学、とくにグラフ理論における2部グラフ(にぶグラフ、英: bipartite graph)とは、**頂点集合を2つに分割**して、**各部分の頂点が互いに隣接しない**ようにできるグラフのこと. 互いに隣接しない頂点からなる集合を**独立集合**といい、頂点集合を n 個の独立集合に分割可能なグラフのことを n 部グラフ (n-partite graph) という. (wikipediaより)

![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Simple-bipartite-graph.svg/330px-Simple-bipartite-graph.svg.png)

## stage 1 における問題設定を定義:

- 左の独立集合$L$と右の独立集合$R$を持つ**user–user二部グラフ**(=各頂点がユーザを意味する二部グラフ)が与えられるとする.
- そのグラフから**$k$個のコミュニティを発見**し、各左ノード(=$L$の各頂点)と右ノード(=$R$の各頂点)にそのメンバーシップの強さ(=k個の各コミュニティに所属する度合いの強さ)を示す重みをつけてコミュニティに割り当てる。

## ユーザフォローの有向グラフを二部グラフとして再定義する利点

- ユーザ->ユーザのフォロー関係を表す有向グラフを、二部グラフとして再定義する一つの利点は、 $R$ を $L$ と異なるように選択できること。(i.e. 全ユーザ集合を２つに集合に分けられる事?:thinking:)
- 特に、典型的なソーシャルネットワークの**大部分の辺は少数のユーザに向けられている**(=多くの一般ユーザがインフルエンサー的なユーザをフォローしている状況:thinking:)ので\*\*、$L$ よりも小さな $R$ を選ぶことは理にかなっている(グラフからコミュニティを発見する上で:thinking:).
- Twitterの場合、最もフォローされている上位$10^7$人のユーザ(=インフルエンサー)を $R$ に含め、残りの全てのユーザを $L$ に含める.
- (文脈から判断すると"有向グラフ→二部グラフに再定義"というのは、まずフォロー関係の有向グラフから$R$と$L$の2つのユーザ集合を定義する。次に$R$内 & $L$内のノード間のエッジ=辺を切り、二部グラフとして再定義させる、という方法っぽい:thinking:)

## 定義したstage1の問題をどんなアプローチで解く?

次の**3 step** のアプローチを採用している。

- Step 1. Similarity Graph of Right Nodes: 右の独立集合$R$について、**類似度グラフ(Similarity Graph)**を取得する.
- Step 2. Communities of Right Nodes: $R$の類似度グラフから、k個のコミュニティを発見する(=$R$のユーザ達をk個のコミュニティに割り当てる).
- Step 3. Communities of Left Nodes: 左の独立集合$L$の各ノード(=頂点=ユーザ)を、Step 2で発見した各コミュニティに割り当てる(=各コミュニティとの関連度合いを埋め込む).

![](https://camo.qiitausercontent.com/194f3a26deb259e329da2e62437508f49aad755b/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f313639373237392f65613534653939372d656632322d366463372d626538302d6239333261626561376433632e706e67)

## stage1-step1: 右の独立集合$R$のSimilarityグラフを作る ①作り方

- このステップの目的は、右の独立集合$R$のノードを用いて、より小さな uni-partite(一部)の無向グラフ $G$ を構築する事.
- $R$ 内の2つのユーザ($u$, $v$)間の重み(=similarityとして表される)を、二部グラフの左側(独立集合 $L$)の"フォロワーのコサイン類似度"に基づいて定義する.

$$
similarity(u, v) = \vec{x_u} \cdot \vec{x_v} / \sqrt{|\vec{x_u}||\vec{x_v}|}
$$

- "フォロワーのコサイン類似度"について具体的には、ユーザuとvについての"フォロワーのbinary incidence vectors(入射ベクトル)"をそれぞれ $\vec{x_u}$ と $\vec{x_v}$ とする(=長さは左集合 $L$ の大きさ.もし$L$のユーザiが$u$をフォローしていれば i番目の要素が1, それ以外が0であるようなbinaryベクトル).

## stage1-step1: 右の独立集合$R$のSimilarityグラフを作る ②dense過ぎるsimilarityグラフを生成しない工夫

- 定義によれば、2つのユーザは、二部グラフにおいて一人以上の共通の隣人($L$内のフォロワー)を共有するだけで、非ゼロの類似度がある.(=similarityグラフを行列で表した時の非ゼロ要素!)
  - i.e. similarityグラフ $G$ にエッジ(=ノード間の接続=辺)を持つことになる.
- 極端に密な similarityグラフ を生成しないために、similarityスコアがある閾値より低いエッジ(=接続)を破棄する。
- さらに、各ノードのsimilarityスコアが最も大きいノードを最大で一定数のみ保持するようにする。

## stage1-step1: 右の独立集合$R$のSimilarityグラフを作る ③このステップの利点

- twitterでの運用においてstep1は、$~10^9$ 個のノードと$∼10^{11}$個のエッジを持つ有向/二部グラフを入力とし、$~10^7$ 個のノード(=独立集合$R$の要素数)と $~10^9$ 個のエッジを持つ無向のsimilarityグラフを出力する。
- つまり、**shared-nothing のcluster-computingスケール**から、**shared-memory のmulti-coreスケール**に変換する事ができた。
- (=>step1によりグラフのスケールが大幅に削減された事で、複数のリソースにまたがる分散処理ではなく、一つのリソース内で共有メモリを使用するようなマルチコア処理で計算可能になった、って事か:thinking:)

## stage1-step2: $R$のSimilarityグラフから、k個のコミュニティを発見する

- step1で得られた無向のSimilarityグラフを用いて、step2では、**密に接続されたノード集合のコミュニティを発見する**ことを目的としている.
- コミュニティ発見アルゴリズムの長い歴史にもかかわらず、twitterのスケーラビリティ要件を満たすことができる既存のソリューションを見つけることができなかった.
- 今回の要求を満たすために、**Neighborhood-aware Metropolis Hastings(以下、Neighborhood-aware MH)**というアルゴリズムを開発し、similarityグラフからk個のコミュニティを発見し各$R$ノードを割り当てる。
- (ココを話すと時間が足りないので今回は割愛します...!気になった方は[このqiita記事](https://qiita.com/morinota/items/d36421df083df9394bad)に、pythonによるテストコードと実装を載せています)
- (ベイジアンアプローチの文脈で聞いたことある"Metropolis-Hastings"なので、サンプリング的な事を行って目的関数を元に最適なk個のコミュニティを探索する...!みたいなアプローチ:thinking:)

## stage1-step3: 左の独立集合$L$の各ノード(=頂点=ユーザ)を、Step 2で発見した各コミュニティに割り当てる①

- step2の出力は、右集合$R$(i.e. インフルエンサー達)に対するコミュニティ割り当て行列 $V_{|R| \times k}$ である. ($i$ 行目の行ベクトルは、右ノード$i$に割り当てられたコミュニティを示すbinary要素のベクトル.)
- stage1の問題設定において残りの問題は、左集合$L$に対するコミュニティ割り当て行列 $U_{|L| \times k}$ を取得する事.

## stage1-step3: 左の独立集合$L$の各ノード(=頂点=ユーザ)を、Step 2で発見した各コミュニティに割り当てる②方法

- シンプルに、$L$の各ノードの**neighbors(=全て右集合$R$のノードのはず!)が割り当てられているコミュニティを集約**する事によって、各左ノード(=一般ユーザ)をコミュニティに割り当てる:

$$
U = truncate(A\cdot V)
$$

ここで、$A_{|L| \times |R|}$ を**入力二部グラフの隣接行列(adjacency matrix)**(要素=1だと隣接してる事を示すbinary行列.)とする. $truncate()$ 関数は、**任意の1ユーザが所属するコミュニティの数を制限するfunction**(ストレージを節約するため).

得られた$U_{|L| \times k}$を **User Interest Representations** と呼び、$U$を入力としてstage2にて、各種アイテムのSimClusters表現を取得する。

## stage 2: 各種 Item Representationsの取得

- stage2では、ツイート、ハッシュタグ、ユーザなど、**様々な推薦問題の対象となりうるアイテムに対するSimCluters表現**を計算する。
- 段階2の一般的な枠組みは、**アイテムに関わったすべてのuser interest Representationsを集約**してアイテムの表現を計算すること(なるほど...!シンプル!). つまり、アイテム $j$ のSimClusters表現は、以下.

$$
W(j) = aggregate({U(u), \forall u \in N(j)})
\tag{3}
$$

ここで、$N(j)$ は、対応するユーザ-アイテム二部グラフにおいてアイテム$j$に関与したすべてのユーザを示し、$W(j)$ と $U(u)$ はいずれもベクトルである。

## twitterにおける活用例 ①ツイート詳細ページでの類似ツイートの推薦

## twitterにおける活用例 ②Home フィードにおけるツイート推薦

## twitterにおける活用例 ③Personalized Trends のランク付け

## twitterにおける活用例 ④Topic Tweetの推薦

## twitterにおける活用例 ⑤ユーザフォローの推薦

## twitterにおける今後の活用 ①通知品質フィルター

## twitterにおける今後の活用 ②リアルタイムイベント通知

## 感想. NewsPicks推薦機能への適用可能性:thinking:

# 参考:

- [SimClustersの論文](https://www.kdd.org/kdd2020/accepted-papers/view/simclusters-community-based-representations-for-heterogeneous-recommendatio)
- [公開されたtechブログ](https://blog.twitter.com/engineering/en_us/topics/open-source/2023/twitter-recommendation-algorithm)
- [公開されたgithub リポジトリ](https://github.com/twitter/the-algorithm)
- n週連続 推薦システム関連の論文読んだシリーズ13週目(毎週水曜更新):[twitterの様々な推薦機能で活用されてるらしい、ユーザ-ユーザのフォローネットワークからコミュニティ埋め込み表現を生成するSimClustersの論文を読んだ](https://qiita.com/morinota/items/d36421df083df9394bad)
