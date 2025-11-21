# Two Tower Model Architecture: Current State and Promising Extensions
# ツータワーモデルアーキテクチャ：現状と有望な拡張

Sumit Kumar
スミット・クマール

## Introduction はじめに

Two-tower model is widely adopted in industrial-scale retrieval and ranking workflows across a broad range of application domains, such as content recommendations, advertisement systems, and search engines. 
Two-towerモデルは、コンテンツ推薦、広告システム、検索エンジンなど、幅広いアプリケーションドメインにおける産業規模の検索およびランキングワークフローで広く採用されています。
It is also the current go-to state-of-the-art solution for pre-ranking tasks. 
また、これはプレランキングタスクに対する現在の最先端の解決策でもあります。(pre-ranking taskってなんだろ??:thinking:)
This article explores the history and current state of the Two Tower models and also highlights potential improvements proposed in some of the recently published literature. 
この記事では、Two Towerモデルの歴史と現在の状態を探り、最近発表された文献の中で提案された潜在的な改善点も強調します。
The goal here is to help understand what makes the Two Tower model an appropriate choice for a bunch of applications, and how it can be potentially extended from its current state. 
ここでの目的は、**Two Towerモデルが多くのアプリケーションにとって適切な選択である理由を理解し、現在の状態からどのように拡張できるか**を考察することです。

<!-- ここまで読んだ! -->

## Cascade Ranking System カスケードランキングシステム

Large-scale information retrieval and item recommendation services often contain tens of millions of candidate items or documents. 
大規模な情報検索およびアイテム推薦サービスは、しばしば数千万の候補アイテムや文書を含んでいます。
A search query on Google may have matching keywords in millions of documents (web pages), and Instagram may have thousands or even millions of candidate videos for generating a recommended feed for a user. 
Googleでの検索クエリは、数百万の文書（ウェブページ）に一致するキーワードを持つ可能性があり、Instagramはユーザーのために推奨フィードを生成するための数千または数百万の候補動画を持つことがあります。
Designing such systems often has to deal with the additional challenge of strict strict latency constraints. 
**このようなシステムを設計する際には、厳しいレイテンシ制約という追加の課題に対処する必要があります**。
Studies have shown that even a 100ms increase in response time leads to degraded user experience and a measurable impact on revenue. 
研究によると、**応答時間が100ms増加するだけで、ユーザー体験が悪化し、収益に測定可能な影響を与えること**が示されています。
A single, complex ranking algorithm cannot efficiently rank such large sets of candidates. 
**単一の複雑なランキングアルゴリズムでは、そのような大規模な候補セットを効率的にランク付けすることはできません**。
Hence, a multi-stage ranking system is commonly adopted to balance efficiency and effectiveness. 
したがって、効率と効果のバランスを取るために、一般的にマルチステージランキングシステムが採用されます。

![]()

In this system, simpler and faster algorithms that focus on recall metrics are employed at earlier steps (Recall and Pre-Ranking). 
このシステムでは、リコールメトリクスに焦点を当てたよりシンプルで高速なアルゴリズムが、初期のステップ（リコールおよびプレランキング）で使用されます。
(あ、pre-rankingってのは、2-stages推薦でいう1段階目のことっぽい...!:thinking:)
Whereas the large-scale deep neural networks are employed at the later steps (Ranking and Re-Ranking). 
一方、大規模な深層ニューラルネットワークは、後のステップ（ランキングおよび再ランキング）で使用されます。
Keeping latency expectations and accuracy tradeoffs in mind, an appropriate algorithm is used at each step. 
**レイテンシの期待と精度のトレードオフを考慮し、各ステップで適切なアルゴリズムが使用されます**。
Each algorithm calculates some form of relevance or similarity value for every single candidate and passes the most relevant candidate set onto the next step. 
各アルゴリズムは、すべての候補に対して何らかの関連性または類似性の値を計算し、最も関連性の高い候補セットを次のステップに渡します。

In an earlier blog post, I introduced several interaction-focused DNN algorithms that can be used for the ranking stage. 
[以前のブログ記事では、ランキングステージで使用できるいくつかのインタラクションに焦点を当てたDNNアルゴリズムを紹介](https://blog.reachsumit.com/posts/2022/11/feature-interactions-ir/)しました。
I recommend going through that article for developing a good understanding of these algorithms. 
これらのアルゴリズムを理解するために、その記事を読むことをお勧めします。
This current article will mainly talk about the Two Tower model in the context of the pre-ranking stage. 
この現在の記事では、プレランキングステージにおけるTwo Towerモデルについて主に説明します。

<!-- ここまで読んだ! -->

## Two Tower Model

The pre-ranking stage does the initial filtering of the candidates received from the preceding recall or retrieval stage. 
プレランキングステージは、前のリコールまたはリトリーバルステージから受け取った候補の初期フィルタリングを行います。
Compared to the ranking stage, the pre-ranking model has to evaluate a larger number of candidates and therefore a faster approach is preferred here. 
ランキングステージと比較して、プレランキングモデルはより多くの候補を評価する必要があるため、ここではより**迅速なアプローチが好まれ**ます。
The following figure shows the development history of pre-ranking systems from an ads recommendation modeling perspective. 
以下の図は、**広告推薦モデルの観点から見たプレランキングシステムの発展の歴史**を示しています。

![]()

Herexux_{u}xu,xax_{a}xa,xuax_{ua}xuaare the raw user features, ad features, and cross features. 
ここで、$x_{u}$ は生のユーザ特徴、$x_{a}$ は生の広告特徴、$x_{ua}$ は生のクロス特徴を表します。
The first generation calculated the pre-rank score in a non-personalized way by averaging the recent click-through rate of each ad. 
第一世代は、各広告の最近のクリック率を平均することによって、**非個別化の方法でプレランクスコアを計算**しました。
Logistic regression used in the second generation is also a lightweight algorithm that can be deployed in online learning and serving manner. 
第二世代で使用されるロジスティック回帰は、オンライン学習およびリアルタイム推論に展開できる軽量なアルゴリズムでもあります。
The third generation commonly used a Two Tower model which is a vector-produced based DNN. 
第三世代では、ベクトル生成に基づくDNNであるTwo Towerモデルが一般的に使用されました。
In this method, user and ad features pass through embedding and DNN layers to generate a latent vector representation for both the user and the ad. 
この方法では、ユーザと広告の特徴が埋め込み層とDNN層を通過し、ユーザと広告の両方の潜在ベクトル表現を生成します。
Then an inner product of the two vectors is calculated to obtain the pre-ranking score. 
その後、2つのベクトルの内積が計算され、プレランキングスコアが得られます。
This Two Tower structure was originally developed in search systems as a means to map a query to the most relevant documents. 
**このTwo Tower構造は、クエリを最も関連性の高い文書にマッピングする手段として、元々検索システムで開発されました**。

![]()

The reason why the Two Tower model rose to popularity was its accuracy as well as its inference efficiency-focused design. 
**Two Towerモデルが人気を博した理由は、その精度と推論効率に焦点を当てた設計**にあります。
The two towers generate latent representations independently in parallel and interact only at the output layer (referred to as “late interaction”). 
**2つのタワーは、独立して並行に潜在表現を生成し、出力層でのみ相互作用します（これを「遅延相互作用(late interaction)」と呼びます）。**
Often the learned ad or item tower embeddings are also frozen after training and stored in an indexing service for a quicker operation at inference time. 
学習された広告またはアイテムタワーの埋め込みは、トレーニング後に凍結され、**推論時の迅速な操作のためにインデックスサービスに保存されることがよくあります**。

<!-- ここまで読んだ! -->

## Related DNN Paradigms 関連するDNNパラダイム

The information retrieval domain has several other DNN paradigms related to the Two Tower model.
情報検索の分野には、Two Towerモデルに関連する他のいくつかのDNNパラダイムがあります。
The following figure shows some examples in the context of neural matching applications (query to document matching)5. 
以下の図は、ニューラルマッチングアプリケーション（クエリからドキュメントへのマッチング）の文脈におけるいくつかの例を示しています5。

![]()

As you can see, the Two Tower model (Figure a) is a representation-based ranker architecture, which independently computes embeddings for the query and documents and estimates their similarity via interaction between them at the output layer. 
ご覧のように、**Two Towerモデル（図a）は、表現に基づくランカーアーキテクチャ**であり、**クエリとドキュメントの埋め込みを独立して計算し、出力層での相互作用を通じてそれらの類似性を推定**します。(この言語化、わかりやすすぎる...!!ありがたい :pray:)
(そうそう、だからTwo Towerモデルって基本的には表現学習 representation learning の一種とも言えるんだよね...!!:thinking:)
The other paradigms represent more interaction-focused rankers. 
**他のパラダイムは、より相互作用に焦点を当てた**ランカーを表しています。
Models like DRMM, and KNRM (Figure b) model word- and phrase-level relationships across query and document using an interaction matrix and then feed it to a neural network like CNN or MLP. 
DRMMやKNRM（図b）のようなモデルは、クエリとドキュメント間の単語およびフレーズレベルの関係を**相互作用行列**を使用してモデル化し、それをCNNやMLPのようなニューラルネットワークに供給します。(=パラダイムbはなんか行列分解みがある...!!:thinking:)
Similarly, models like BERT (Figure c), also called cross-encoders, are much more powerful as they model interactions between words as well as across the query and documents at the same time. 
同様に、BERT（図c）のようなモデルは、クロスエンコーダーとも呼ばれ、単語間の相互作用とクエリとドキュメント間の相互作用を同時にモデル化するため、はるかに強力です。
On the other hand, models like ColBERT (Contextualized later interactions over BERT) (Figure d) keep interactions within the query and document features while delaying the query-document interaction to the output layer. 
一方、ColBERT（BERT上の文脈化された後の相互作用）のようなモデル（図d）は、クエリとドキュメントの特徴内での相互作用を保持し、クエリとドキュメントの相互作用を出力層に遅延させます。
This allows the model to preserve the “query-document decoupling” (or “user-item decoupling”) architecture paradigm, and the document or item embeddings can be frozen after training and served through an index at the inference time as shown on the left in the figure below. 
これにより、モデルは「クエリ-ドキュメントのデカップリング」（または「ユーザー-アイテムのデカップリング」）アーキテクチャパラダイムを保持でき、**ドキュメントまたはアイテムの埋め込みはトレーニング後に凍結され、以下の図の左側に示されているように推論時にインデックスを介して提供**されます。(ここで凍結、ってのは、事前計算しておいてそのまま使う、っていう意味の認識...!:thinking:)
Inference costs can be further reduced if the application can work with freezing both towers. 
アプリケーションが両方のタワーを凍結して動作できる場合、推論コストはさらに削減できます。
(i.e. ユーザ埋め込みも事前計算しておく場合、もっと早くなるよね！って話。)
For example, as shown on the right in the following figure, Alibaba creates indexes out of the learned embeddings from both towers and retrains the model offline on a daily frequency3. 
例えば、以下の図の右側に示されているように、Alibabaは両方のタワーから学習した埋め込みを使用してインデックスを作成し、**モデルをオフラインで日次頻度で再トレーニング**します3。
(あ、Alibabaは企業名か!:thinking:)

![]()

(図を見るとまさにtwo-towerモデルって感じ!)

<!-- ここまで読んだ! -->

## Comparing Dual Encoder Architectures 二重エンコーダーアーキテクチャの比較

Two tower models, like DSSM, are also called the dual encoder or bi-encoder architecture as they encode the input (such as a query, an image, or a document) into an embedding using the two sub-networks ("towers" or “encoders”). 
DSSMのようなtwo-towerモデルは、入力（クエリ、画像、または文書など）を二つのサブネットワーク（「タワー」または「エンコーダー」）を使用して埋め込みにエンコードするため、**dual encoderまたはbi-encoderアーキテクチャ**とも呼ばれます。
The model is then optimized based on similarity metrics in the embedding space. 
モデルは、その後、**埋め込み空間における類似性メトリックに基づいて最適化**されます。 
Dual encoders have shown excellent performance in a wide range of information retrieval tasks, such as question-answering, entity linking, dense retrieval, etc. 
dual encodersは、質問応答、エンティティリンク、密な検索など、幅広い情報検索タスクで優れたパフォーマンスを示しています。
They are also easy to productionize because the embedding for new or updated documents can be dynamically added to the embedding index, without retraining the encoders. 
**エンコーダーを再訓練することなく、新しいまたは更新された文書の埋め込みを動的に埋め込みインデックスに追加できるため、プロダクション化も容易**です。

<!-- ここまで読んだ! -->

A Siamese encoder model is a type of dual encoder that consists of two identical sub-networks joined at their outputs. 
Siameseエンコーダーモデルは、出力で結合された二つの同一のサブネットワークから構成されるdual encoderの一種です。
Generally, the two sub-networks also share their parameters. 
**一般に、二つのサブネットワークはそのパラメータも共有**します。(あ、なるほど...!これがSiameseエンコーダーの特徴なのかな...!:thinking:)
The Siamese architecture was originally proposed by Bromley et al. for signature verification application. 
Siameseアーキテクチャは、もともとBromleyらによって署名検証アプリケーションのために提案されました。 
It processes two inputs concurrently and maps them onto a single scalar output representing the distance or similarity between the inputs. 
**このアーキテクチャは、二つの入力を同時に処理し、それらの距離または類似性を表す単一のスカラー出力にマッピング**します。 
On the other hand, an asymmetric dual encoder (ADE) refers to a model with two distinctly parameterized encoders. 
一方、**asymetric(非対称) dual encoder (ADE)**は、二つの異なるパラメータ化されたエンコーダーを持つモデルを指します。(多くの推薦タスクで使われるのは、こっちのイメージ...!:thinking:)
In practice, ADEs are used when a certain asymmetry is required in the dual encoders. 
実際には、dual encodersに特定の非対称性が必要な場合にADEが使用されます。
Dong et al. conducted a study to explore the different ways dual encoders can be structured and compared their efficacy on the question-answering retrieval task. 
Dongらは、dual encodersを構造化するさまざまな方法を調査し、質問応答検索タスクにおけるその有効性を比較する研究を行いました。

![]()
Dual encoders architectures. SDE: Siamese Dual Encoder, ADE: Asymmetric Dual Encoder, ADE-STE: ADE with shared token embedder, ADE-FTE: ADE with frozen token embedder, ADE-SPL: ADE with shared projection layer.
dual encodersアーキテクチャ。SDE: Siamese Dual Encoder、ADE: Asymmetric Dual Encoder、ADE-STE: トークンエンベッダーを共有するADE、ADE-FTE: トークンエンベッダーを固定するADE、ADE-SPL: 投影層を共有するADE。

<!-- ここまで読んだ! -->

The study concluded that the Siamese Dual Encoders (SDEs) perform significantly better than Asymmetric Dual Encoders (ADEs) because ADEs tend to embed the two inputs into disjoint embedding spaces, which hurts the retrieval quality. 
この研究は、Siamese Dual Encoders（SDEs）がAsymmetric Dual Encoders（ADEs）よりも著しく優れた性能を発揮することを結論付けました。なぜなら、**ADEは二つの入力を互いに重ならない埋め込み空間に埋め込む傾向があり、これが検索品質を損なうから**です。(これってどういう意味だろ?? 同じ埋め込み空間ではあるけど、その中で両者のmappingが離れがち、ってこと?? これを近づけるために学習するイメージだけど...!:thinking:)
They also found that ADE performance can be enhanced to be on par or even better than SDEs by sharing a projection layer between the two encoders (ADE-SPL). 
また、二つのエンコーダー間で投影層を共有することによって、ADEの性能をSDEと同等またはそれ以上に向上させることができることも発見しました（ADE-SPL）。 
However, sharing the token embedders between the two towers (ADE-STE) or freezing the token embedders during training (ADE-FTE) only brings marginal improvements. 
しかし、二つのタワー間でトークンエンベッダーを共有すること（ADE-STE）や、トレーニング中にトークンエンベッダーを固定すること（ADE-FTE）は、わずかな改善しかもたらしません。

<!-- ここまで読んだ! -->

## Enhancing Two Tower Model 2タワーモデルの強化

In this section, we look at some of the proposals from different researchers for extending the Two Tower model. 
このセクションでは、2タワーモデルを拡張するための異なる研究者からのいくつかの提案を見ていきます。
One common problem with the Two Tower model that this research works focus on is the lack of information interaction between the two towers. 
この研究が焦点を当てている2タワーモデルの一般的な問題の1つは、2つのタワー間の情報の相互作用が欠如していることです。
As we saw earlier, the Two Tower model trains the latent embeddings in both towers independently and without using any enriching information from the other tower. 
前述のように、2タワーモデルは、他のタワーからの強化情報を使用せずに、両方のタワーで潜在埋め込みを独立して訓練します。(一般に、訓練は一緒にやると思うんだけど...!昔の話なのかな??:thinking:)
This limitation hinders the model’s performance. 
この制限は、モデルのパフォーマンスを妨げます。

<!-- ここまで読んだ! -->

### Dual Augmented Two-Tower Model (DAT) デュアル拡張二塔モデル (DAT)

To model feature interactions between two towers, Yu et al.8 proposed augmenting the embedding input of each tower with a vector (aua_{u}au and ava_{v}av in the figure below) that captures historical positive interaction information from the other tower. 
2つのtoworの間の特徴の相互作用をモデル化するために、Yuらは**各towerの埋め込み入力を、他のtowerからの過去のポジティブな相互作用情報をキャプチャするベクトル（図の $a_{u}$ と $a_{v}$）で拡張する**ことを提案しました。
(ユーザタワー側に、過去のアイテムとの相互作用情報を持つベクトルを追加するのは、推薦タスクではイメージしやすい。アイテムタワー側に、過去のユーザとの相互作用情報を持つベクトルを追加するのは、例えば相互作用したユーザのCB/CFベクトルの平均値とかかな!なるほど確かに...!:thinking:)
$a_u$ and $a_{v}$ vectors get updated during the training process and are used to model the information interaction between the two towers by regarding them as the input feature of the two towers. 
$a_{u}$ と $a_{v}$ ベクトルはトレーニングプロセス中に更新され、2つのタワーの入力特徴として扱うことによって、2つのタワー間の情報相互作用をモデル化するために使用されます。
(あれ、ここのベクトルってtwo-towerモデルの出力ってこと?? よくわからなくなった:thinking:)
This paper also proposes a new category alignment loss to handle the imbalance among different categories of items by transferring the knowledge learned from the category with a large amount of data to other categories. 
この論文では、データ量が多いカテゴリから他のカテゴリに学習した知識を転送することによって、異なるアイテムのカテゴリ間の不均衡を処理するための新しいカテゴリアライメント損失も提案しています。
Later research showed that the gains achieved by the DAT model are still limited. 
**その後の研究では、DATモデルによって達成された利得は依然として限られていることが示されました。**

![]()

<!-- ここまで読んだ! -->

### Interaction Enhanced Two Tower Model (IntTower) インタラクション強化二塔モデル (IntTower)

The authors of this research design a two-tower model that emphasizes both information interactions and inference efficiency.  
この研究の著者は、**情報の相互作用と推論の効率の両方を強調する二塔モデル**を設計しています。
Their proposed model consists of three new blocks, as mentioned below.  
彼らの提案したモデルは、以下に述べる**3つの新しいブロックで構成**されています。

#### Light-SE Block ライトSEブロック

This module is used to identify the importance of different features and obtain refined feature representations in each tower.  
このモジュールは、異なる特徴の重要性を特定し、各塔で洗練された特徴表現を取得するために使用されます。
The design of this module is based on the SENET model proposed in the “Squeeze-and-Excitation Networks” paper.  
このモジュールの設計は、「Squeeze-and-Excitation Networks」論文で提案されたSENETモデルに基づいています。
SENET is used in the computer vision domain to explicitly model the interdependencies between the image channels through feature recalibration, i.e. selectively emphasizing informative features and suppressing less useful ones.  
SENETは、コンピュータビジョンの分野で、特徴の再キャリブレーションを通じて画像チャネル間の相互依存性を明示的にモデル化するために使用されます。つまり、情報を提供する特徴を選択的に強調し、あまり役に立たない特徴を抑制します。
The basic structure of the SE building block is shown in the next figure.  
SEビルディングブロックの基本構造は、次の図に示されています。

![]()

First, a squeeze operation aggregates the feature maps across spatial dimensions to produce a channel descriptor.  
まず、スクイーズ操作が空間次元にわたって特徴マップを集約し、チャネル記述子を生成します。
An excitation operation then excites informative features by a self-gating mechanism based on channel dependence (similar to calculating attention weights).  
次に、エキサイテーション操作がチャネル依存性に基づく自己ゲーティングメカニズムによって情報を提供する特徴を活性化します（注意重みを計算するのに似ています）。
The final output of the block is obtained through a scaling step by rescaling the transformation output with the learned activations.  
ブロックの最終出力は、学習した活性化を用いて変換出力を再スケーリングすることで得られます。
The authors of the IntTower paper adopt a more lightweight approach with a single FC layer to obtain the feature importance.  
**IntTower論文の著者は、特徴の重要性を取得するために、単一のFC層を用いたより軽量なアプローチを採用**しています。(これなら実装簡単そう??:thinking:)
The following figure shows the SENET and Light-SE blocks side-by-side.  
次の図は、SENETとLight-SEブロックを並べて示しています。

![]()

<!-- ここまで読んだ! -->

#### FE-Block FEブロック

The purposed FE (Fine-grained and Early Feature Interaction) Block is inspired by the later interaction style of ColBERT.  
提案されたFE（細粒度および早期特徴相互作用）ブロックは、ColBERTの後の相互作用スタイルに触発されています。
It performs fine-grained early feature interaction between multi-layer user representations and the last layer of item representation.  
これは、マルチレイヤーのユーザ表現とアイテム表現の最終層との間で細粒度の早期特徴相互作用を実行します。


![]()


#### CIR Module CIRモジュール

A Contrastive Interaction Regularization (CIR) module was also purposed to shorten the distance between a user and positive items using InfoNCE loss function.  
対照的相互作用正則化（CIR）モジュールも提案されており、InfoNCE損失関数を使用してユーザとポジティブアイテム間の距離を短縮します。
During training, this loss value is combined with the logloss between the model prediction scores and the true labels.  
トレーニング中、この損失値はモデルの予測スコアと真のラベルとの間のログ損失と組み合わされます。

#### IntTower Model Architecture IntTowerモデルアーキテクチャ

![]()

As shown in the figure above, the IntTower model architecture combines the three blocks described earlier.  
上の図に示すように、IntTowerモデルアーキテクチャは前述の3つのブロックを組み合わせています。
Through experimentation, the authors show that the IntTower model outperforms other pre-ranking algorithms (Logistic Regression, Two-Tower, DAT, COLD) and even performs comparably to some ranking algorithms (Wide&Deep, DeepFM, DCN, AutoInt).  
実験を通じて、著者はIntTowerモデルが他のプレランキングアルゴリズム（ロジスティック回帰、二塔、DAT、COLD）を上回り、いくつかのランキングアルゴリズム（Wide&Deep、DeepFM、DCN、AutoInt）と同等の性能を発揮することを示しています。
Compared with the Two Tower model, the increased parameters count and training time of IntTower are negligible and the serving latency is also acceptable.  
**二塔モデルと比較して、IntTowerのパラメータ数の増加とトレーニング時間は無視できるものであり、サービングレイテンシも許容範囲**です。
The authors also investigate the user and item representations generated by Two Tower and IntTower models by projecting them into 2-dimensions using t-SNE.  
著者はまた、**t-SNEを使用して二塔モデルとIntTowerモデルによって生成されたユーザおよびアイテムの表現を2次元に投影することによって調査**しています。
As shown in the next figure, the IntTower representations have the user and positive items in the same cluster while negative items are far away from the user.  
次の図に示すように、**IntTowerの表現はユーザとポジティブアイテムが同じクラスターにあり、ネガティブアイテムはユーザから遠く離れています**。
(この調査方法いいな、作図方法も含めて、真似しやすそう...!:thinking:)

![]()

<!-- ここまで読んだ! -->

## Other Alternatives to Two Tower Model 二塔モデルの他の代替案

Apart from Two Tower models, there has been some research work with single-tower structures to fully model feature interactions and further improve prediction accuracy. 
二塔モデルとは別に、特徴の相互作用を完全にモデル化し、予測精度をさらに向上させるために、**シングルタワー構造に関する研究**がいくつか行われています。
However, due to the lack of a “user-item decoupling architecture” paradigm, these models have to employ several optimization tricks to alleviate efficiency degradations. 
しかし、**"user-item decoupling architecture"パラダイムがないため**、これらのモデルは効率の低下を緩和するためにいくつかの最適化トリックを採用する必要があります。
(そうだよね、デカップリングしてるから事前計算できる。事前計算できるからリアルタイム推論が速いはず。それができないと推論どうしても遅くなりそう...!:thinking:)
For example, the COLD (Computing power cost-aware Online and Lightweight Deep pre-ranking system) model performs offline feature selection experiments to find out a set of important features for the ranking algorithm that are optimal concerning metrics such as QPS (queries per second) and RT (return time). 
例えば、COLD（Computing power cost-aware Online and Lightweight Deep pre-ranking system）モデルは、オフラインの特徴量選択実験を実施し、QPS（クエリ毎秒）やRT（応答時間）などの指標に関して最適なランキングアルゴリズムの重要な特徴量のセットを見つけ出します。
Similarly, FSCD (Feature Selection method based on feature Complexity and variational Dropout) model uses learnable dropout parameters to perform feature-wise regularization such that the pre-ranking model is effectively inherited from that of the ranking model. 
同様に、FSCD（Feature Selection method based on feature Complexity and variational Dropout）モデルは、学習可能なドロップアウトパラメータを使用して特徴ごとの正則化を行い、プレランキングモデルがランキングモデルから効果的に継承されるようにします。
(なるべく高速になるように、特徴量を取捨選択する方法ってこと??:thinking:)

<!-- ここまで読んだ! -->s

## Conclusion 結論

This article introduced the historical evolution of pre-ranking approaches in the context of cascade ranking-based systems. 
この記事では、カスケードランキングベースのシステムにおけるプレランキングアプローチの歴史的進化を紹介しました。
We learned how the balance of efficiency and effectiveness makes Two Tower models an excellent choice for several information retrieval use cases. 
効率性と効果性のバランスが、Two Towerモデルをいくつかの情報検索のユースケースにとって優れた選択肢にしていることを学びました。
We also explored several recent research proposals that combine ideas from related domains to enhance the Two Tower model. 
また、Two Towerモデルを強化するために関連する分野からのアイデアを組み合わせた最近の研究提案をいくつか探りました。
We wrapped up the article with a look at some of the available alternatives to the Two Tower model architecture. 
最後に、Two Towerモデルアーキテクチャの利用可能な代替案のいくつかを見て、記事を締めくくりました。


## References 参考文献

1. Kohavi, R., Deng, A., Frasca, B., Walker, T., Xu, Y., & Pohlmann, N. (2013). Online controlled experiments at large scale. Proceedings of the 19th ACM SIGKDD international conference on Knowledge discovery and data mining.
   Kohavi, R., Deng, A., Frasca, B., Walker, T., Xu, Y., & Pohlmann, N. (2013). 大規模なオンライン制御実験。第19回ACM SIGKDD国際会議の議事録、知識発見とデータマイニング。

2. Sumit Kumar. Recommender Systems for Modeling Feature Interactions under Sparse Settings. https://blog.reachsumit.com/posts/2022/11/sparse-recsys/
   Sumit Kumar. スパース設定における特徴相互作用のモデリングのためのレコメンダーシステム。https://blog.reachsumit.com/posts/2022/11/sparse-recsys/

3. Wang, Zhe & Zhao, Liqin & Jiang, Biye & Zhou, Guorui & Zhu, Xiaoqiang & Gai, Kun. (2020). COLD: Towards the Next Generation of Pre-Ranking System.
   Wang, Zhe & Zhao, Liqin & Jiang, Biye & Zhou, Guorui & Zhu, Xiaoqiang & Gai, Kun. (2020). COLD: 次世代のプレランキングシステムに向けて。

4. Huang, P., He, X., Gao, J., Deng, L., Acero, A., & Heck, L. (2013). Learning deep structured semantic models for web search using clickthrough data. Proceedings of the 22nd ACM international conference on Information & Knowledge Management.
   Huang, P., He, X., Gao, J., Deng, L., Acero, A., & Heck, L. (2013). クリックデータを使用したウェブ検索のための深層構造的意味モデルの学習。第22回ACM国際会議の議事録、情報と知識管理。

5. Khattab, O., & Zaharia, M.A. (2020). ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval.
   Khattab, O., & Zaharia, M.A. (2020). ColBERT: BERT上での文脈化された遅延インタラクションによる効率的かつ効果的なパッセージ検索。第43回国際ACM SIGIR会議の議事録、情報検索の研究と開発。

6. Dong, Z., Ni, J., Bikel, D. M., Alfonseca, E., Wang, Y., Qu, C., & Zitouni, I. (2022). Exploring Dual Encoder Architectures for Question Answering. ArXiv. /abs/2204.07120
   Dong, Z., Ni, J., Bikel, D. M., Alfonseca, E., Wang, Y., Qu, C., & Zitouni, I. (2022). 質問応答のためのデュアルエンコーダアーキテクチャの探求。ArXiv. /abs/2204.07120

7. Bromley, J., Bentz, J.W., Bottou, L., Guyon, I.M., LeCun, Y., Moore, C., Säckinger, E., & Shah, R. (1993). Signature Verification Using A “Siamese” Time Delay Neural Network. Int. J. Pattern Recognit. Artif. Intell., 7, 669-688.
   Bromley, J., Bentz, J.W., Bottou, L., Guyon, I.M., LeCun, Y., Moore, C., Säckinger, E., & Shah, R. (1993). 「シャム」時間遅延ニューラルネットワークを使用した署名検証。パターン認識と人工知能の国際ジャーナル、7、669-688。

8. Yu, Y., Wang, W., Feng, Z., Xue, D., Meituan, & Beijing (2021). A Dual Augmented Two-tower Model for Online Large-scale Recommendation.
   Yu, Y., Wang, W., Feng, Z., Xue, D., Meituan, & Beijing (2021). オンライン大規模推薦のためのデュアル拡張二塔モデル。

9. Li, X., Chen, B., Guo, H., Li, J., Zhu, C., Long, X., Li, S., Wang, Y., Guo, W., Mao, L., Liu, J., Dong, Z., & Tang, R. (2022). IntTower: The Next Generation of Two-Tower Model for Pre-Ranking System. Proceedings of the 31st ACM International Conference on Information & Knowledge Management.
   Li, X., Chen, B., Guo, H., Li, J., Zhu, C., Long, X., Li, S., Wang, Y., Guo, W., Mao, L., Liu, J., Dong, Z., & Tang, R. (2022). IntTower: プレランキングシステムのための次世代二塔モデル。第31回ACM国際会議の議事録、情報と知識管理。

10. Hu, J., Shen, L., Albanie, S., Sun, G., & Wu, E. (2017). Squeeze-and-Excitation Networks. IEEE Transactions on Pattern Analysis and Machine Intelligence, 42, 2011-2023.
    Hu, J., Shen, L., Albanie, S., Sun, G., & Wu, E. (2017). Squeeze-and-Excitation Networks。IEEEパターン分析と機械知能のトランザクション、42、2011-2023。

11. https://lilianweng.github.io/posts/2021-05-31-contrastive/#infonce
    https://lilianweng.github.io/posts/2021-05-31-contrastive/#infonce

12. Ma, X., Wang, P., Zhao, H., Liu, S., Zhao, C., Lin, W., Lee, K., Xu, J., & Zheng, B. (2021). Towards a Better Tradeoff between Effectiveness and Efficiency in Pre-Ranking: A Learnable Feature Selection based Approach. Proceedings of the 44th International ACM SIGIR Conference on Research and Development in Information Retrieval.
    Ma, X., Wang, P., Zhao, H., Liu, S., Zhao, C., Lin, W., Lee, K., Xu, J., & Zheng, B. (2021). プレランキングにおける効果と効率のより良いトレードオフに向けて：学習可能な特徴選択に基づくアプローチ。第44回国際ACM SIGIR会議の議事録、情報検索の研究と開発。

<!-- ここまで読んだ! -->
