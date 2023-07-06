## 0.1. link 0.1. リンク

- https://dl.acm.org/doi/abs/10.1145/3523227.3546788 httpsを使用しています。

- https://arxiv.org/pdf/2212.04120.pdf httpsを使用しています。

## 0.2. title 0.2. タイトル

Denoising Self-Attentive Sequential Recommendation
デノイジング自己調整型逐次推薦法

## 0.3. abstract 0.3. 抽象的

Transformer-based sequential recommenders are very powerful for capturing both short-term and long-term sequential item dependencies.
トランスフォーマーに基づくsequential推薦器は、短期的および長期的な**sequentialなアイテム間の依存関係**を捉えるのに非常に強力である.
This is mainly attributed to their unique self-attention networks to exploit pairwise item-item interactions within the sequence.
これは主に、sequence内のペアワイズアイテム-アイテム相互作用を利用するための、独自のself-attention ネットワークに起因している.
However, real-world item sequences are often noisy, which is particularly true for implicit feedback.
しかし、**実世界のitem sequencesはしばしばノイズが多く、特に暗黙的なフィードバックにはそれが当てはまる**。
For example, a large portion of clicks do not align well with user preferences, and many products end up with negative reviews or being returned.
例えば、**クリックの大部分はユーザの嗜好に合わないし**、多くの購入した製品は否定的なレビューを受けたり、返品されることになる.
As such, the current user action only depends on a subset of items, not on the entire sequences.
このように、現在のユーザーアクションはシーケンス全体ではなく、アイテムのsubset(部分集合)にのみ依存する。
Many existing Transformer-based models use full attention distributions, which inevitably assign certain credits to irrelevant items.
既存のTransformerベースのモデルの多くは、完全なattention分布を使用しており、必然的に無関係なアイテムに一定のクレジットを割り当てることになる。
This may lead to sub-optimal performance if Transformers are not regularized properly.
これはTransformerが適切に正則化されない場合、最適でない性能につながる可能性がある.

Here we propose the Rec-denoiser model for better training of self-attentive recommender systems.
本論文では、自己調整型推薦システムのより良い学習のために、**Rec-denoiserモデルを提案**する。
In Rec-denoiser, we aim to adaptively prune noisy items that are unrelated to the next item prediction.
Rec-denoiserでは、**next item prediction**に関係のないノイズの多いアイテムを適応的に刈り取ることを目的とする.(そっか、NLPのnext-token predictionみたいな感じ...!)
To achieve this, we simply attach each self-attention layer with a trainable binary mask to prune noisy attentions, resulting in sparse and clean attention distributions.
そのため、**各self-attention層に学習可能なbinary maskを付加**し、ノイズの多いattentionを除去することで、スパースでクリーンなattention分布が得られる。
This largely purifies item-item dependencies and provides better model interpretability.
これにより、item-itemの依存性(の多く??)がほぼ除去され、モデルの解釈可能性が向上する。
In addition, the self-attention network is typically not Lipschitz continuous and is vulnerable to small perturbations.
さらに、self-attentionネットワークは一般的にリプシッツ連続ではなく、小さな摂動に弱い.(このへんよくわからん...!)
Jacobian regularization is further applied to the Transformer blocks to improve the robustness of Transformers for noisy sequences.
**さらにヤコビアン正則化をTransformerブロックに適用し、ノイズの多いシーケンスに対するTransformerの頑健性を向上させる**。
Our Rec-denoiser is a general plugin that is compatible to many Transformers.
**我々のRec-denoiserは多くのTransformerに対応する汎用プラグインである**. (general plugin、素晴らしい...!!)
Quantitative results on real-world datasets show that our Rec-denoiser outperforms the state-of-the-art baselines.
実世界のデータセットにおける定量的な結果は、我々のRec-denoiserが最先端のベースラインを凌駕することを示している.

# 1. introduction 1.はじめに

Sequential recommendation aims to recommend the next item based on a user’s historical actions [20, 35, 39, 44, 47], e.g., to recommend a bluetooth headphone after a user purchases a smart phone.
**Sequential recommendationの目的は，ユーザの過去の行動に基づいて次のアイテムを推薦すること(next-item-prediction)**である[20, 35, 39, 44, 47]．例えば，**ユーザがスマートフォンを購入した後にBluetoothヘッドホンを推薦するような場合**である.
Learning sequential user behaviors is, however, challenging since a user’s choices on items generally depend on both long-term and short-term preferences.
しかし，一般にユーザのアイテム選択は**長期的嗜好(long-term preference)**と**短期的嗜好(short-term preference)**の両方に依存するため，逐次的(sequential)なユーザ行動の学習は困難である.
Early Markov Chain models [19, 39] have been proposed to capture short-term item transitions by assuming that a user’s next decision is derived from a few preceding actions, while neglecting long-term preferences.
初期のマルコフ連鎖モデル[19, 39]は、ユーザの次の決定がいくつかの先行行動から導かれると仮定することによって、短期的なアイテムの遷移を捉えるために提案されたが、長期的な嗜好は無視されたままであった.
To alleviate this limitation, many deep neural networks have been proposed to model the entire users’ sequences and achieve great success, including recurrent neural networks [20, 53] and convolutional neural networks [42, 54, 57].
この限界を緩和するために、リカレントニューラルネットワーク[20, 53]や畳み込みニューラルネットワーク[42, 54, 57]など、**ユーザのsequence全体をモデル化する多くのディープニューラルネットワークが提案され、大きな成功を収めている**.

Recently, Transformers have shown promising results in various tasks, such as machine translation [43].
最近、Transformersは機械翻訳のような様々なタスクで有望な結果を示している[43].
One key component of Transformers is the self-attention network, which is capable of learning long-range dependencies **by computing attention weights between each pair of objects in a sequence**.
Transformersの主要な構成要素の1つはself-attention networkであり、シーケンス中の各object ペアのattention weightを計算することで**長距離依存関係を学習することができる**.
Inspired by the success of Transformers, several self-attentive sequential recommenders have been proposed and achieve the state-of-the-art performance [26, 41, 49, 50].
Transformersの成功に触発され、いくつかのself-attentive sequential recommendersが提案され、最新の性能を達成している[26, 41, 49, 50].
For example, SASRec [26] is the pioneering framework to adopt self-attention network to learn the importance of items at different positions.
例えば、SASRec [26]は、異なる位置にあるitemの重要度を学習するために、self-attention networkを採用した先駆的なフレームワークである.
BERT4Rec [41] further models the correlations of items from both left-to-right and right-to-left directions.
BERT4Rec [41]は、さらに左から右、右から左の両方向のitemの相関をモデル化する.
SSE-PT [50] is a personalized Transformer model that provides better interpretability of engagement patterns by introducing user embeddings.
SSE-PT [50]は、user embeddingsを導入することにより、エンゲージメントパターンの解釈可能性を向上させるパーソナライズドトランスフォーマーモデルである.
LSAN [31] adopts a novel twin-attention sequential framework, which can capture both long-term and short-term user preference signals.
LSAN [31]は新しいtwin-attention sequential frameworkを採用し、長期と短期の両方のユーザ嗜好シグナルを捉えることができる.
Recently, Transformers4Rec [14] performs an empirical analysis with broad experiments of various Transformer architectures for the task of sequential recommendation.
最近、**Transformers4Rec** [14]は、sequential推薦のタスクのために、様々なTransformerアーキテクチャの幅広い実験による実証分析を行っている.

Although encouraging performance has been achieved, the robustness of sequential recommenders is far less studied in the literature.
しかし、**sequential推薦器のrobustnessについてはあまり研究されていない**.
Many real-world item sequences are naturally noisy, containing both true-positive and false-positive interactions [6, 45, 46].
実世界の多くのアイテム列は自然にノイズが多く、真陽性(true-positive)と偽陽性(false-positive. ex. **好きじゃないけどクリックしてしまった. 購入してみたが嫌いだった...??**)の両方の相互作用を含んでいる [6, 45, 46].
For example, a large portion of clicks do not align well with user preferences, and many products end up with negative reviews or being returned.
例えば、クリックの大部分はユーザの嗜好に合わず、多くの製品は否定的なレビューで終わったり、返品されたりする.
In addition, there is no any prior knowledge about how a user’s historical actions should be generated in online systems.
また、オンラインシステムでは、ユーザの過去の行動をどのように生成すべきかという事前知識は存在しない.
Therefore, developing robust algorithms to defend noise is of great significance for sequential recommendation.
そのため、**ノイズに強いアルゴリズムを開発することは、逐次推薦において大きな意義がある**.

Clearly, not every item in a sequence is aligned well with user preferences, especially for implicit feedbacks (e.g., clicks, views, etc.) [8].
特に、暗黙のフィードバック（クリック、ビューなど）の場合、**sequence内のすべてのitemがユーザーの嗜好とうまく整合しているわけではないことは明らか**である [8].
Unfortunately, the vanilla self-attention network is not Lipschitz continuous1 , and is vulnerable to the quality of input sequences [28].
残念ながら、バニラな(デフォルトの) self-attention networkは**Lipschitz連続ではなく(?)**、**入力シーケンスの質に弱いという問題**がある[28]。
Recently, in the tasks of language modeling, people found that a large amount of BERT’s attentions focus on less meaningful tokens, like "[SEP]" and ".", which leads to a misleading explanation [11].
最近、言語モデリングのタスクにおいて、BERT の注意の多くが、"[SEP]" や "."のようなあまり意味のないトークンに集中し、誤解を招く説明になっていることが判明している[11]。
It is thus likely to obtain sub-optimal performance if self-attention networks are not well regularized for noisy sequences.
このように、self-attentionネットワークがノイズの多いsequenceに対してうまく正則化されていない場合、最適とは言えない性能が得られる可能性がある.
We use the following example to further explain above concerns.
以下の例を用いて、上記の懸念についてさらに説明する.

Figure 1 illustrates an example of left-to-right sequential recommendation where a user’s sequence contains some noisy or irrelevant items.
図1は、左から右へのsequential recommendationの一例である.
For example, a father may interchangeably purchase (phone, headphone, laptop) for his son, and (bag, pant) for his daughter, resulting in a sequence: (phone, bag, headphone, pant, laptop).
例えば、ある父親が息子に（携帯電話、ヘッドフォン、ノートパソコン）、娘に（カバン、ズボン）を購入する場合、（携帯電話、カバン、ヘッドフォン、ズボン、ノートパソコン）という順序になる.
In the setting of sequential recommendation, we intend to infer the next item, e.g., laptop, based on the user’s previous actions, e.g., (phone, bag, headphone, pant).
逐次推薦の設定では、**ユーザーの以前の行動、例えば（電話、カバン、ヘッドホン、ズボン）から、次のアイテム、例えばノートパソコンを推論すること**を意図している.
However, the correlations among items are unclear, and intuitively pant and laptop are neither complementary nor compatible to each other, which makes the prediction untrustworthy.
しかし、アイテム間の相関が不明確であり、**直感的にpantとlaptopは補完関係にも相容れない**ため、この予測は信頼できない.
A trustworthy model should be able to only capture correlated items while ignoring these irrelevant items within sequences.
**信頼できるモデルは、シーケンス内のこれらの無関係なアイテムを無視し、相関のあるアイテムのみを捉えることができるはず**である.
Existing self-attentive sequential models (e.g., SASRec [26] and BERT4Rec [41]) are insufficient to address noisy items within sequences.
既存のself-attentive sequential model（例えば、SASRec [26]やBERT4Rec [41]）は、シーケンス内のノイズの多いアイテムに対処するには不十分である.
The reason is that their full attention distributions are dense and would assign certain credits to all items, including irrelevant items.
その理由は、それらのfull attention distributionsが密であり、無関係なitemを含むすべてのitemに一定のcreditを割り当ててしまうからである.
This causes a lack of focus and makes models less interpretable [10, 58].
このため、注目度(focus)が不足し、モデルの解釈性が低下する[10, 58].

To address the above issues, one straightforward strategy is to design sparse Transformer architectures that sparsify the connections in the attention layers, which have been actively investigated in language modeling tasks [10, 58].
上記の問題を解決するために、一つの簡単な戦略は、言語モデリングタスクで活発に研究されている**attention layersの接続をsparseにした**Transformerアーキテクチャを設計することである[10, 58].
Several representative models are Star Transformer [18], Sparse Transformer [10], Longformer [2], and BigBird [58].
いくつかの代表的なモデルはStar Transformer [18], Sparse Transformer [10], Longformer [2], そしてBigBird [58]である.
These sparse attention patterns could mitigate noisy issues and avoid allocating credits to unrelated contents for the query of interest.
これらのsparse attentionパターンは、ノイズの問題を軽減し、関心のあるクエリに無関係なコンテンツにクレジットを割り当てることを回避することができる.
However, these models largely rely on pre-defined attention schemas, which lacks flexibility and adaptability in practice.
しかし、これらのモデルは事前に定義されたattention schemas(??)に大きく依存しており、実際のところ柔軟性や適応性に欠けている.
Unlike end-to-end training approaches, whether these sparse patterns could generalize well to sequential recommendation remains unknown and is still an open research question.
また、エンドツーエンドの学習アプローチとは異なり、言語モデルタスクのsparseパターンがsequential推薦にうまく一般化できるかどうかは不明であり、まだ未解決の研究課題である.

## 1.1. Contributions.

貢献度
In this work, we propose to design a denoising strategy, Rec-Denoiser, for better training of selfattentive sequential recommenders.
本研究では、自己注意型逐次推薦器をより良く学習させるためのノイズ除去戦略、Rec-Denoiserを提案する.
Our idea stems from the recent findings that not all attentions are necessary and simply pruning redundant attentions could further improve the performance [10, 12, 40, 55, 58].
我々のアイデアは、全てのattentionsは必要ではなく、冗長なattentionsを刈り取ることでさらに性能が向上するという最近の知見に由来する[10, 12, 40, 55, 58].
Rather than randomly dropping out attentions, we introduce differentiable masks to drop task-irrelevant attentions in the self-attention layers, which can yield exactly zero attention scores for noisy items.
我々は、ランダムにattentionsを削除するのではなく、**微分可能なマスクを導入し、タスクと無関係なattentionsをself-attention layersで削除する**ことで、ノイズの多いitemに対してattentionスコアを正確にゼロにすることができる.
The introduced sparsity in the self-attention layers has several benefits:
self-attention layersに導入されたスパース性には、いくつかの利点がある.

- 1. Irrelevant attentions with parameterized masks can be learned to be dropped in a data-driven way. パラメータ化されたマスクを持つ無関係なattentionは、データ駆動型の方法で削除されるように学習させることができる.
  - Taking Figure 1 as an example, our Rec-denoiser would prune the sequence (phone, bag, headphone) for pant, and (phone, bag, headphone, pant) for laptop in the attention maps.図1を例にとると、Rec-denoiserは、アテンションマップにおいて、ズボンには(phone, bag, headphone)、ノートパソコンには(phone, bag, headphone, pant)という順序を切り捨てることになる.
  - Namely, we seek next item prediction explicitly based on a subset of more informative items. つまり、より情報量の多いアイテムの部分集合(subset)に基づき、明示的に次のアイテム予測を行うのです.
- 2. Our Rec-Denoiser still takes full advantage of Transformers as it does not change their architectures, but only the attention distributions.我々のRec-DenoiserはTransformerのアーキテクチャを変更せず、**アテンション分布のみを変更する**ため、Transformerを最大限に活用することができる.
  - As such, Rec-Denoiser is easy to implement and is compatible to any Transformers, making them less complicated as well as improving their interpretability. そのため、Rec-Denoiserは実装が容易で、あらゆるTransformerと互換性があり、Transformerの複雑さを軽減し、その解釈可能性を向上させることができる.

In our proposed Rec-Denoiser, there are two major challenges.
我々が提案するRec-Denoiserでは、2つの大きな課題がある.
First, the discreteness of binary masks (i.e., 0 is dropped while 1 is kept) is, however, intractable in the back-propagation.
まず、2値マスクの離散性（すなわち、0は削除され、1は保持される）は、しかし、バックプロパゲーションでは実行不可能である.
To remedy this issue, we relax the discrete variables with a continuous approximation through probabilistic reparameterization [25].
この問題を解決するために、我々は確率的再パラメータ化[25]により、離散変数を連続的な近似値で緩和する.
As such, our differentiable masks can be trained jointly with original Transformers in an end-to-end fashion.
このように、我々の微分可能なマスクは、オリジナルのTransformerとエンドツーエンドで共同して学習することができる.
In addition, the scaled dot-product attention is not Lipschitz continuous and is thus vulnerable to input perturbations [28].
また、scaled dot-product attentionはLipschitz連続(?)ではないため、入力摂動に対して脆弱である[28].
In this work, Jacobian regularization [21, 24] is further applied to the entire Transformer blocks, to improve the robustness of Transformers for noisy sequences.
この研究では、**ノイズの多いシーケンスに対するTransformerのrobustnessを向上させるため**に、Transformerブロック全体にヤコビアン正則化[21, 24]をさらに適用している.
Experimental results on real-world benchmark datasets demonstrate the effectiveness and robustness of the proposed Rec-Denoiser.
実世界のベンチマークデータセットに対する実験結果から、提案するRec-Denoiserの有効性と頑健性を実証する.
In summary, our contributions are:
まとめると、我々の貢献は以下の通りである.

- We introduce the idea of denoising item sequences for better of training self-attentive sequential recommenders, which greatly reduces the negative impacts of noisy items. 本論文では、自己認識型逐次推薦器を学習するために、item列のノイズ除去のアイデアを紹介し、ノイズの多いitemによる悪影響を大幅に軽減する.

- We present a general Rec-Denoiser framework with differentiable masks that can achieve sparse attentions by dynamically pruning irrelevant information, leading to better model performance. 我々は、微分可能なマスクを持つ一般的なRec-Denoiserフレームワークを提示し、無関係な情報を動的に刈り取ることで疎な注意を達成し、より良いモデル性能を導くことが可能である.

- We propose an unbiased gradient estimator to optimize the binary masks, and apply Jacobian regularization on the gradients of Transformer blocks to further improve its robustness. バイナリマスクの最適化のために不偏勾配推定器を提案し、Transformerブロックの勾配にヤコビアン正則化を適用して、さらに頑健性を向上させる.

- The experimental results demonstrate significant improvements that Rec-Denoiser brings to self-attentive recommenders (5.05% ∼ 19.55% performance gains), as well as its robustness against input perturbations. 実験結果は、Rec-Denoiserが自己注意型推薦器にもたらす大きな改善（5.05% ∼ 19.55%の性能向上）と、入力の摂動に対する頑健性を示している.

# 2. Related Work 2. 関連作品

In this section, we briefly review the related work on sequential recommendation and sparse Transformers.
本節では、逐次推薦とスパーストランスフォーマーに関する関連研究を簡単にレビューする。
We also highlight the differences between the existing efforts and ours.
また、既存の取り組みと我々の取り組みとの相違点を強調する。

## 2.1. Sequential Recommendation

Leveraging sequences of user-item interactions is crucial for sequential recommendation.
逐次推薦では、ユーザとアイテムのinteractionのsequenceを活用することが重要である。
User dynamics can be caught by Markov Chains for inferring the conditional probability of an item based on the previous items [19, 39].
ユーザダイナミクスはマルコフ連鎖によって捕捉され、前のアイテムに基づくアイテムの条件付き確率を推論することができる[19, 39].
More recently, growing efforts have been dedicated to deploying deep neural networks for sequential recommendation such as recurrent neural networks [20, 53], convolutional neural networks [42, 54, 57], memory networks [9, 22], and graph neural networks [4, 7, 51].
最近では、リカレントニューラルネットワーク [20, 53]、畳み込みニューラルネットワーク [42, 54, 57]、メモリネットワーク [9, 22]、グラフニューラルネットワーク [4, 7, 51] などの**深いニューラルネットワークを逐次推薦に利用する取り組みが盛んになっている**。
For example, GRU4Rec [20] employs a gated recurrent unit to study temporal behaviors of users.
例えば、GRU4Rec[20]はユーザの時間的行動を研究するためにゲーテッドリカレントユニットを採用している。
Caser [42] learns sequential patterns by using convolutional filters on local sequences.
Caser [42]は局所的な配列に対して畳み込みフィルタを用いて連続的なパターンを学習する。
MANN [9] adopts memory-augmented neural networks to model user historical records.
MANN [9]はユーザの履歴記録をモデル化するためにメモリ補強型ニューラルネットワークを採用する。
SR-GNN [51] converts session sequences into graphs and uses graph neural networks to capture complex item-item transitions.
SR-GNN [51]はセッションシーケンスをグラフに変換し、グラフニューラルネットワークを使用して複雑なアイテム-アイテム遷移を捉える。

Transformer-based models have shown promising potential in sequential recommendation [5, 26, 30, 32, 33, 41, 49, 50], due to their ability of modeling arbitrary dependencies in a sequence.
Transformerに基づくモデルは、sequence中の任意の依存関係をモデル化できるため、逐次推薦において有望な可能性を示している[5, 26, 30, 32, 33, 41, 49, 50]．
For example, SASRec [26] first adopts self-attention network to learn the importance of items at different positions.
例えば、SASRec [26]では、まず、異なる位置にあるアイテムの重要度を学習するために、self-attentionネットワークを採用している.
In the follow-up studies, several Transformer variants have been designed for different scenarios by adding bidirectional attentions [41], time intervals [30], personalization [50], importance sampling [32], and sequence augmentation [33].
その後、bidirectional attentions[41]、time intervals[30]、personalization[50]、importance sampling[32]、sequence augmentation[33]を追加し、異なるシナリオのためにいくつかの変種が設計されてきた.
However, very few studies pay attention to the robustness of self-attentive recommender models.
しかし、self-attention型推薦モデルの頑健性に注目した研究は非常に少ない.
Typically, users’ sequences contain lots of irrelevant items since they may subsequently purchase a series of products with different purposes [45].
一般に、ユーザのシーケンスには無関係なアイテムが多く含まれる.
As such, the current user action only depends on a subset of items, not on the entire sequences.
このような場合、現在のユーザの行動は、シーケンス全体ではなく、アイテムのサブセットにのみ依存する。
However, the self-attention module is known to be sensitive to noisy sequences [28], which may lead to sub-optimal generalization performance.
しかし、**self-attentionモジュールはノイズの多いシーケンスに敏感であることが知られており**[28]、これは最適でない汎化性能につながる可能性がある。
In this paper, we aim to reap the benefits of Transformers while denoising the noisy item sequences by using learnable masks in an end-to-end fashion.
本論文では、学習可能なマスクをend-to-endで用いる(i.e. Transformerの学習と一緒にmaskのパラメータも学習できる)ことにより、ノイズの多いアイテムsequenceをdenoiseしつつ、Transformersの利点を享受することを目指す.

## 2.2. Sparce Transformer

Recently, many lightweight Transformers seek to achieve sparse attention maps since not all attentions carry important information in the self-attention layers [2, 10, 18, 29, 58].
最近、多くの軽量トランスフォーマーが、全てのattentionがself-attention層の重要な情報を持っているわけではないので、sparseなアテンションマップ(=attention分布?)を実現することを追求している[2, 10, 18, 29, 58].
(既存研究において、sparseなattention分布を採用する目的は、noiseへのrobust性の向上というよりも、軽量化やスケーラビリティ向上だったりするんだろうか...??:thinking:)
For instance, Reformer [29] computes attentions based on locality-sensitive hashing, leading to lower memory consumption.
例えば、Reformer [29]は局所性を考慮したハッシュに基づいてアテンションを計算し、メモリ消費の低減につながる.
Star Transformer [18] replaces the fully-connected structure of self-attention with a star-shape topology.
Star Transformer [18]は、self-attentionの完全連結構造を星形のトポロジーに置き換えたものである。
Sparse Transformer [10] and Longformer [2] achieve sparsity by using various sparse patterns, such as diagonal sliding windows, dilated sliding windows, local and global sliding windows.
Sparse Transformer [10] と Longformer [2] は、斜めスライド窓、拡張スライド窓、ローカルスライド窓、グローバルスライド窓など、様々なスパースパターンを用いてスパース性を実現する。
BigBird [58] uses random and several fixed patterns to build sparse blocks.
BigBird [58]では，**ランダムなパターンといくつかの固定パターン**を用いて，疎なブロックを構築している．
It has been shown that these sparse attentions can obtain the state-of-the-art performance and greatly reduce computational complexity.
これらのsparse attentionは、最先端の性能を得ることができ、計算量を大幅に削減できることが示されている。
However, many of them rely on fixed attention schemas that lack flexibility and require tremendous engineering efforts.
しかし、これらの多くは、柔軟性に欠け、膨**大な工学的努力を必要とする固定的なattention schemaに依存**している.

Another line of work is to use learnable attention distributions [12, 36, 38, 40].
また、**学習可能なattention分布**[12, 36, 38, 40]を使用することもある。
Mostly, they calculate attention weights with variants of sparsemax that replaces the softmax normalization in the self-attention networks.
ほとんどの場合、self-attentionネットワークにおけるソフトマックス正規化を置き換える**sparsemax**(最大値のみを残す、みたいなイメージ??:thinking:)の変種を用いてattention weightを計算する.
This allows to produce both sparse and bounded attentions, yielding a compact and interpretable set of alignments.
これにより、疎でboundedな(境界のある?)attentionを生成することができ、コンパクトで解釈可能なアラインメントの集合を得ることができる.
Our Rec-denoiser is related to this line of work.
我々のRec-denoiserは、この研究に関連している.
Instead of using sparsemax, we design a trainable binary mask for the self-attention network.
sparsemax(? 最大値のみを残す、みたいなイメージ??)を用いる代わりに、我々は**self-attentionネットワークに対して学習可能なbinaryマスクを設計**する。
As a result, our proposed Rec-denoiser can automatically determine which self-attention connections should be deleted or kept in a data-driven way.
その結果、我々の提案するRec-denoiserは、データ駆動型の方法で、どのself-attetionの接続を削除すべきか、あるいは保持すべきかを自動的に決定することができる.

# 3. Problem and Background 3. 問題点と背景

In this section, we first formulate the problem of sequential recommendation, and then revisit several self-attentive models.
本節では、まず逐次推薦の問題を定式化し、次にいくつかのself-attetnionモデルを再検討する。
We further discuss the limitations of the existing work.
さらに、既存の研究の限界について議論する。

## 3.1. Problem Setup 3.1. 問題の設定

In sequential recommendation, let $U$ be a set of users, $I$ a set of items, and $S = {S^1, S^2,\cdots, S^{|U|}}$ a set of users' actions.
逐次推薦において、$U$ をユーザの集合、$I$ をアイテムの集合、$S= (S^1,S^2, \cdots, S^{|U|})$ をユーザの行動の集合とする.
We user $S^u = (S^u_1, S^u_2, \cdots, S^u_{|S^u|})$ to denote a sequence of items for user $u \in U$ in a chronological order, where $S^u_t \in I$ is the item that user $u$ has interacted with at time $t$, and $|S^u|$ is the length of sequence.
$S^u = (S^{u}_{1}, S^{u}_{2}, \cdots, S^{u}_{|S^u|})$ は、時系列に並んだユーザ $u \in U$ のitem sequence を表し、$S^{u}_{t} in I$ は時刻(=sequence内の要素の識別子的な意味合い) $t$ にユーザ $u$ がinteractしたアイテム、$|S^u|$ はsequenceの長さを表す.

Given the interaction history $S^u$, sequential recommendation seeks to predict the next item $S^u_{|S^{u}+1|}$ at time step $|S^{u}+1|$
interaction history $S^u$ が与えられると、sequential推薦では time step $|S^{u}+1|$ において next item $S^u_{|S^{u}+1|}$ を予測しようとする.
During the training process [26, 41], it will be convenient to regard the model’s input as $(S^{u}_{1}, S^{u}_{2}, \cdots, S^{u}_{|S^u - 1|})$ and its expected output is a shifted version of the input sequence: $(S^{u}_{2}, S^{u}_{3}, \cdtos, S^{u}_{|S^{u}|})$
モデルの学習プロセス[26, 41]では、モデルの入力を $(S^{u}_{1}, S^{u}_{2}, ˶cdots, S^{u}_{|S^u - 1|})$ とみなし、その expected output(i.e. 教師ラベル!) を入力sequence の シフトバージョン $(S^{u}_{2}, S^{u}_{3}, ˶cdtos, S^{u}_{|S^{u}|})$ とみなすと便利である.

## 3.2. Self-attentive Recommenders

Owing to the ability of learning long sequences, Transformer architectures [43] have been widely used in sequential recommendation, like **SASRec** [26], BERT4Rec [41], and TiSASRec [30].
Transformerアーキテクチャ[43]は長いsequenceを学習することができるため、逐次推薦において**SASRec** [26], BERT4Rec [41], TiSASRec [30] など広く利用されている。
Here we briefly introduce the design of SASRec and discuss its limitations.
ここでは、SASRecの設計を簡単に紹介し、その限界について考察する.

### 3.2.1. Embedding Layer 3.2.1. エンベデッドレイヤー

Transformer-based recommenders maintain an item embedding table $T \in R^{|I| \times d}$ , where 𝑑 is the size of the embedding.
Transformerベースのレコメンダーはアイテムの **embedding table** $T \in R^{|I| \times d}$ を保持する. ここで、$d$ は embeddingのサイズ. (embedding tableは、アイテムid -> embedding vector のmapみたいなイメージ:thinking:).
For each sequence $(S^u_1, S^u_2, \cdots, S^u_{|S^u - 1|})$, it can be converted into a fixed-length sequence $(s_1, s_2, \cdots s_n)$, where $n$ is the maximum length (e.g., keeping the most recent 𝑛 items by truncating or padding items).
各sequence $(S^u_1, S^u_2, \cdots, S^u_{|S^u - 1|})$ に対して、**fixed-length(固定長)のsequence $(s_1, s_2, \cdots s_n)$ に変換**することができる. ここで、$n$は、sequenceの最大長である. (ex. アイテムを truncating したり、padding したりして、最新の$n$個のアイテムを残す)
The embedding for $(s_1, s_2, \cdots s_n)$ is denoted as $E \in R^{n \times d}$ , which can be retrieved from the table $T$.
$(s_1, s_2, \cdots s_n)$ の埋め込みを $E \in R^{n \times d}$ と表し(= $E$ は埋め込みベクトル行列 ...!)、embedding table $T$ から取り出すことができる.
To capture the impacts of different positions, one can inject a learnable positional embedding $P \in R^{n \times d}$ into the input embedding as:
sequence内の異なるpositionの影響(=time step間の距離やsequenceの順序)を捉えるために、学習可能なpositonal embedding $P \in R^{n ౪times d}$ を入力embeddng $E$ にinject(注入)することができる:

(各tokenの特徴量ベクトルに、positonal encoding vectorを追加する式!)

$$
\hat{E} = E + P \tag{1}
$$

where $\hat{E} \in R^{n\times d}$ is an order-aware embedding, which can be directly fed to any Transformer-based models.
ここで、$hat{E} \in R^{n \times d}$ は order-awareな(=sequence内の順序を考慮した) 埋め込みベクトル行列 で、Transformerベースのモデルに直接与えることができる.

### 3.2.2. Transformer Block

A Transformer block consists of a self-attention layer and a point-wise feed-forward layer.
トランスフォーマー・ブロックは、self-attention layer と point-wise feed-forward layer (=全結合層) で構成される.

**Self-attention Layer**: The key component of Transformer block is the self-attention layer that is highly efficient to uncover sequential dependencies in a sequence [43].
**self-attention層**： Transformerブロックの重要なコンポーネントは、シーケンスの逐次的な依存関係を明らかにするために非常に効率的であるself-attention層である[43]。
The scaled dot-product attention is a popular attention kernel:
scaled dot-product attentionは一般的なattention kernel(=かなり一般的なattention関数の一つ、という認識:thinking:)である：

(scaled-dot-product attentionの関数式)

$$
\text{Attention}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d}}) V
\tag{2}
$$

where $\text{Attention}(Q, K, V) \in R^{n \times d}$ is the output item representations; $Q = \hat{E}W^Q$, $K =\hat{E}W^K$, and $V = \hat{E}W^V$ are the queries, keys and values, respectively; ${W^Q, W^K, W^V} \in R^{d \times d}$ are three projection matrices; and $\sqrt{d}$ is the scale factor to produce a softer attention distribution.
ここで、

- $\text{Attention}(Q, K, V) \in R^{n \times d}$ は **output item representations**.
- $Q = \hat{E} W^Q$, $K =\hat{E} W^K$, and $V = \hat{E} W^V$ はそれぞれ Query, Key, Valueである. (QもKもVも、埋め込みベクトル行列Eを元にしてるので、attention関数のself-attention的な使い方...!)
- ${W^Q, W^K, W^V} \in R^{d \times d}$ は3つのprojection行列
- $sqrt{d}$ はより柔らかい(?)attention分布を生成するためのscale-factorである.(正規化的なイメージ!)

In sequential recommendation, one can utilize either left-to-right unidirectional attentions (e.g., SASRec [26] and TiSASRec [30]) or bidirectional attentions (e.g., BERT4Rec [41]) to predict the next item.
逐次推薦では、**left-to-right uni-directional attentions(左から右への一方向のattention)**(ex. SASRec [26]やTiSASRec [30])や、もしくは**bi-directional attention(双方向のattention)** (ex. BERT4Rec [41])を利用して、次のアイテムを予測することができる.
Moreover, one can apply $H$ attention functions in parallel to enhance expressiveness: $H <- \text{MultiHead}(\hat{E})$ [43].
さらに、$H$ 個のattention関数を並列に適用することで、表現力を高めることができる：$\mathbf{H} <- \text{MultiHead}(\hat{E})$ [43].
(元のtransformerでも採用してる、Multi-head attentionね:thinking:)

**Point-wise Feed-forward Layer**: As the self attention layer is built on linear projections, we can endow the nonlinearity by introducing a point-wise feed-forward layers:
**ポイント・ワイズ・フィードフォワード層**： self-attention層はlinear projectionで構築されているので、**Point-wise Feed-forward層を導入することで、非線形性を付与する(モデルの表現力を高める為の非線形変換!)**ことができる(あ、そういうモチベーションなのか...!中間層１つのやつ! :thinking:)：

(補足: "point-wise" -> **要素毎に独立して操作を行う**、という意味. Transformerの場合はSequenceデータを入力に取るが、この層は、sequenceデータの各要素に対して個別に処理が行われる. つまり、sequenceデータの各要素に対して同じ操作が行われる.:thinking:)
(補足: "feed-forward" -> データの入出力の流れが1方向=前方方向にのみ進む事を意味する. 逆に、"feed-forward"ではない層はRNNとか! CNNは"point-wise"ではないが"feed-forward"である気はする:thinking:)

$$
F_i = FFN(H_i) = \text{ReLU}(H_i W^{(1)} + b^{(1)})W^{(2)} + b^{(2)}
\tag{3}
$$

where $W^{(\ast)} \in R^{d \times d}$, $b^{(\ast)} \in R^d$ are the learnable weights and bias.
ここで、$W^{(\ast)} \in R^{d \times d}$, $b^{(\ast)} \in R^d$ は FFN層内の学習可能なparameters(重みとバイアス).

In practice, it is usually beneficial to learn hierarchical item dependencies by stacking more Transformer blocks.
実際には、より多くのTransformerブロックを積み重ねることによって、階層的なアイテムの依存関係を学習することが通常有益である.(元祖Transformerでも、$N$個のブロックを重ねるよね...:thinking:)
Also, one can adopt the tricks of residual connection, dropout, and layer normalization for stabilizing and accelerating the training.
また、**residual connection(残差接続), dropout, layer normalization(レイヤー正則化) などのトリックを採用することで、学習の安定化と高速化を図ることができる**.(そういう目的なんだ...!:thinking:)
Here we simply summarize the output of $L$ Transformer blocks as: $F^{(L)} <- \text{Transformer}(\hat{E})$.
ここでは、$L$ 個のTransformerブロックの出力(=L個のブロックが連結した最終的な出力の意味??)を単純に次のようにまとめる: $F^{(L)} <- \text{Transformer}(\hat{E})$.

### 3.2.3. Learning Objective 3.2.3. 学習目標

After stacked $L$ Transformer blocks, one can predict the next item (given the first $t$ items) based on $F_t^{(L)}$.
$L$ 個のTransformerブロックを積み重ねた後、$F_t^{(L)}$ に基づいて(最初の$t$個のアイテムが与えられれば)次のアイテムを予測できる.
In this work, we use inner product to predict the relevance of item $i$ as:
この研究では、内積を使ってアイテム $i$ の relevance を次のように予測する:

$$
r_{i, t} = <F_{t}^{(L)}, T_i>,
$$

where $T_i \in R^d$ is the embedding of item $i$.
ここで $T_i \in R^d$ は、アイテム $i$ の埋め込みベクトルである.
Recall that the model inputs a sequence $s = (s_1, s_2, \cdots, s_n)$ and its desired output is a shifted version of the same sequence $o = (o_1, o_2, \cdots, o_n)$, we can adopt the binary cross-entropy loss as:
モデルはsequence $s = (s_{1}, s_{2}, \cdots, s_{n})$ を入力し、その出力は同じ sequence をシフトしたもの $o = (o_{1}, o_{2}, \cdots, o_{n})$ である. なので、binary cross-entropy lossを適用できる:

(= $o_2$ は $s = (s_1, s_2)$ が与えられた時のnext-item predictionの正解ラベル、という認識. ~~$r_{i,t}$が最も高いアイテムを$o_2$として採用する、みたいなイメージ??~~ これは推論時ではなく学習時の話なので、$o_2 = s_3$ って事かな.:thinking:)

$$
L_{BCE} = - \sum_{S^{u} \in S} \sum_{t=1}^{n}{[\log{\sigma(r_{o_t, t})} + \log{1 - \sigma (r_{o_t', t})}]} + \alpha \cdot ||\theta||^2_F
\tag{4}
$$

where $\theta$ is the model parameters, $a$ is the reqularizer to prevent over-fitting, $o'_t \notin S^u$ is a negative sample corresponding to $o_t$, and $\sigma(\cdot)$ is the sigmoid function.
ここで、

- $\theta$はmodel parameters
- $\alpha$はオーバーフィットを防ぐためのreqularizer(正則化パラメータ)
- $o_{t}' \notin S^{u}$ は $o_t$ に対応するnegative sample()
- $sigma(\cdot)$ はシグモイド関数である.

More details can be found in SASRec [26] and BERT4Rec [41].
詳細は、SASRec[26]およびBERT4Rec[41]に記載されている.

## 3.3. The Noisy Attentions Problem

Despite the success of SASRec and its variants, we argue that they are insufficient to address the noisy items in sequences.
SASRecとその亜種の成功にもかかわらず、sequence中のノイズの多いアイテムに対処するには不十分であると我々は主張する.
The reason is that the full attention distributions (e.g., Eq.(2)) are dense and would assign certain credits to irrelevant items.
その理由は、**full attetnion分布（例えば式(2)）は密度が高く、無関係な項目に一定のクレジット(=attention weight)を割り当ててしまうから**である.
This complicates the item-item dependencies, increases the training difficulty, and even degrades the model performance.
これはitem-itemの依存関係を複雑にし、トレーニングの難易度を上げ、さらにはモデルの性能を低下させる.
To address this issue, several attempts have been proposed to manually define sparse attention schemas in language modeling tasks [2, 10, 18, 58].
この問題に対処するため、言語モデリングタスクで sparse attention schemas を手動で定義する試みがいくつか提案されている[2, 10, 18, 58]。
However, these fixed sparse attentions cannot adapt to the input data [12], leading to sub-optimal performance.
しかし、このようなfixed(固定的な) sparse attentions は、入力データに適応することができず[12]、最適なパフォーマンスとは言えない.

On the other hand, several dropout techniques are specifically designed for Transformers to keep only a small portion of attentions, including LayerDrop [17], DropHead [60], and UniDrop [52].
一方、LayerDrop[17]、DropHead[60]、UniDrop[52]など、トランスフォーマーのために特別に設計された、**attentionのごく一部だけを残すdropout技術**がいくつかある.
Nevertheless, these randomly dropout approaches are susceptible to bias: the fact that attentions can be dropped randomly does not mean that the model allows them to be dropped, which may lead to over-aggressive pruning issues.
とはいえ、このようなランダムにdropoutさせるアプローチは、バイアスの影響を受けやすい。attentionがランダムにdropoutさせられるという事実は、モデルが脱落を許容していることを意味しないので、**過度に攻撃的な刈り込みの問題**につながる可能性がある。
In contrast, we propose a simple yet effective data-driven method to mask out irrelevant attentions by using differentiable masks.
これに対して我々は、微分可能なマスクを用いて無関係なattentionをマスクする、シンプルかつ効果的なdata-driven method(=確かに、固定的でもランダムでもない:thinking:)を提案する.

# 4. Rec-Denoiser

In this section, we present our Rec-Denoiser that consists of two parts: differentiable masks for self-attention layers and Jacobian regularization for Transformer blocks.
このセクションでは、Rec-Denoiserを紹介する。Rec-Denoiserは、**self-attention層のための微分可能なmask**と、**Transformerブロックのためのヤコビアン正則化**の2つの部分から構成される.

## 4.1. Differentiable Masks

The self-attention layer is the cornerstone of Transformers to capture long-range dependencies.
セルフ・アテンション・レイヤーは、長距離の依存関係を捉えるトランスフォーマーの要である.
As shown in Eq.(2), the softmax operator assigns a non-zero weight to every item.
**式(2)に示すように、softmax演算子はすべてのitemにnon-zeroの重みを割り当てる**. (なるほど. これがfull attention分布か...!:thinking:)
However, full attention distributions may not always be advantageous since they may cause irrelevant dependencies, unnecessary computation, and unexpected explanation.
しかし、full attention分布は、無関係な依存関係、不必要な計算、予期せぬ(解釈困難な)説明を引き起こす可能性があるため、必ずしも有利とは限らない.
We next put forward differentiable masks to address this concern.
次に、この懸念に対処するために、微分可能なマスクを提案する.

### 4.1.1. Learnable Sparse Attentions 4.1.1. 学習可能なスパース・アテンション

Not every item in a sequence is aligned well with user preferences in the same sense that not all attentions are strictly needed in self-attention layers.
**self-attention層において全てのattentionが厳密に必要とされるわけではないのと同じ意味で、sequence内のすべてのアイテムがユーザの嗜好にうまく合致しているわけではない**.
Therefore, we attach each self-attention layer with a trainable binary mask to prune noisy or task-irrelevant attentions.
そこで、各self-attention層に学習可能な binary mask を付加し、ノイズの多い attention やタスクと無関係な attention を除去する.
Formally, for the $l$-th self-attention layer in Eq.(2), we introduce a binary matrix $Z^{(l)} \in {0, 1}^{n \times n}$, where $Z^{(l)}_{u,v}$ denotes whether the connection between query $u$ and key $v$ is present.
形式的には、式(2)の $l$ 番目のself-attention層に対して、$Z^{(l)} \in {0, 1}^{n \times n}$ の**binary行列 $Z^{(l)}$ を導入**する. ここで、$Z^{(l)}_{u,v}$ は query $u$ と key $v$ のconnectionの有無(??:thinking:)を表す.
As such, the $l$ -th self-attention layer becomes:
よって、$l$ 番目のself-attention層は次のように改良される:

$$
A^{(l)} = \text{softmax}(\frac{Q^{(l)} K^{(l)T}}{\sqrt{d}}),
\\
M^{(l)} = A^{(l)} \odot Z^{(l)},
\\
\text{Attention}(Q^{(l)}, K^{(l)}, V^{(l)}) = M^{(l)} V^{(l)},
\tag{5}
$$

where $A^{(l)}$ is the original full attentions, $M^{(l)}$ denotes the sparse attentions, and $\odot$ is the element-wise product.
ここで、$A^{(l)}$は元のfull attention、$M^{(l)}$は sparse attention, $\odot$ は 要素ごとの積.(=確か"アダマール積"だっけ??:thinking:)
Intuitively, the mask $Z^{(l)}$ (e.g., 1 is kept and 0 is dropped) requires minimal changes to the original self-attention layer.
直感的には、mask $Z^{(l)}$ (ex. 1を残して0を落とす)は、元のself-attention層に最小限の変更を加えるだけで済む.
More importantly, they are capable of yielding exactly zero attention scores for irrelevant dependencies, resulting in better interpretability.
さらに重要なのは、**無関係な依存関係に対してattentionスコアを正確にゼロにすることができるため、解釈しやすくなる**ということだ.
The idea of differentiable masks is not new.
微分可能なmaskというアイデアは新しいものではない.(なるほど. LMの世界で既存研究があるんだ...!:thinking:)
In the language modeling, differentiable masks have been shown to be very powerful to extract short yet sufficient sentences, which achieves better performance [1, 13].
言語モデリングにおいて、微分可能なmaskは、短くても十分なsentencesを抽出するのに非常に強力であり、より良いパフォーマンスを達成することが示されている[1, 13].

One way to encourage sparsity of $M^{(l)}$ is to explicitly penalize the number of non-zero entries of $Z^{(l)}$, for $1 \leq l \leq L$, by minimizing:
$M^{(l)}$ のsparsity(sparse性)を奨励する一つの方法は、$Z^{(l)}$ 内のnon-zero entry(=要素)の数に対して明示的にペナルティを課すことである.
そのために、以下の $R_M$ を $1 \leq l \leq L$ の間で最小化する:

$$
R_M = \sum_{l=1}^{L}||Z^{l}||_{0}
= \sum_{l=1}^{L} \sum_{u=1}^{n} \sum_{v=1}^{n} I[Z_{u,v}^{(l)} \neq 0],
\tag{6}
$$

(要は、L個のmask binary行列内の非ゼロ要素の数を最小する項を、学習時の損失関数に組み込むって事...??)

where $I[c]$ is an indicator that is equal to 1 if the condition $c$ holds and 0 otherwise; and $||\cdot||_{0}$ denotes the $L_0$ norm that is able to drive irrelevant attentions to be exact zeros.
ここで、

- $I[c]$ は条件 $c$ が成立すれば1、成立しなければ0に等しい indicator function である.
- $||\cdot||_{0}$ は、無関係な attention を正確な 0 に追い込むことができる $L_0$ ノルムを表す.

However, there are two challenges for optimizing $Z^{(l)}$: non-differentiability and large variance.
しかし、$Z^{(l)}$ の最適化には、**微分不可能性と分散の大きさという2つの課題**がある.
$L_0$ is discontinuous and has zero derivatives almost everywhere.
$L_0$ は不連続(binaryだから?)であり、ほとんどどこでもゼロ導関数を持つ.
Additionally, there are $2^{n^2}$ possible states for the binary mask $Z^{(l)}$ with large variance.
さらに、binary mask行列 $Z^{(l)}$ には大きな分散を持つ $2^{n^2}$ 個の可能な状態がある.
Next, we propose an efficient estimator to solve this stochastic binary optimization problem.
次に、この**確率的binary最適化問題を解くための効率的な推定器**を提案する.

### 4.1.2. Efficient Gradient Computation 4.1.2. 効率的な勾配計算

Since $Z^{(l)}$ is jointly optimized with the original Transformer-based models, we combine Eq.(4) and Eq.(6) into one unified objective:
$Z^{(l)}$ はオリジナルのTransformerベースのモデルと共同で最適化されるので、式(4)と式(6)を1つの統一された目的関数にまとめる:

$$
L(Z, \Theta) = L_{BCE}({A^{(l)} \odot Z^{(l)}}, \Theta) + \beta \cdot \sum_{l=1}^{L} \sum_{u=1}^{n} \sum_{v=1}^{n} I[Z_{u,v}^{(l)} \neq 0]
\tag{7}
$$

where $\beta$ controls the sparsity of masks and we denote $Z$ as $Z := \{Z^{(1)}, \cdots, Z^{(L)}\}$.
ここで $\beta$ はmaskのsparse性を制御し、$Z$ を $Z := \{Z^{(1)}, \cdots, Z^{(L)}\}$ とする.
We further consider each $Z^{(l)}_{u,v}$ is drawn from a Bernoulli distribution parameterized by $\Pi^{(l)}_{u,v}$ such that $Z^{(l)}_{u,v} \sim Bern(\Pi^{(l)}_{u,v})$ [34].
さらに、$Z^{(l)}_{u,v} \sim Bern(\Pi^{(l)}_{u,v})$ のような $\Pi^{(l)}_{u,v}$ でパラメータ化されたBernoulli分布から それぞれの $Z^{(l)}_{u,v}$ が生成される(=サンプリングされる?)と考える[34].
As the parameter $\Pi^{(l)}_{u,v}$ is jointly trained with the downstream tasks, a small value of $\Pi^{(l)}_{u,v}$ suggests that the attention $A^{(l)}_{u,v}$ is more likely to be irrelevant, and could be removed without side effects.
パラメータ $\Pi^{(l)}_{u,v}$ は下流タスクと共同で学習されるため、$\Pi^{(l)}_{u,v}$ の値が小さいと、attention $A^{(l)}_{u,v}$ は無関係である可能性が高く、副作用なく削除できる。
By doing this, Eq.(7) becomes:
こうすることで、式(7)は次のようになる：

$$
L(Z, \Theta) =
E_{Z \in \Pi_{l=1}^{L} Bern(Z^{(l)}; \Pi^{(l)})}[L_{BCE}(Z, \Theta)]
+ \beta \cdot \sum_{l=1}^{L} \sum_{u=1}^{n} \sum_{v=1}^{n} Z_{u,v}^{(l)}
\tag{8}
$$

where $E(\cdot)$ is the expectation.
ここで $E(\cdot)$ は期待値である。
The regularization term is now continuous, but the first term $L_{BCE}(Z, \Theta)$ still involves the discrete variables $Z^{(l)}$.
正則化項は連続になったが、第一項 $L_{BCE}(Z, \Theta)$ はまだ離散変数(i.e. binary parameters) $Z^{(l)}$ を含んでいる.
One can address this issue by using existing gradient estimators, such as REINFORCE [48] and Straight Through Estimator [3], etc.
REINFORCE [48]や Straight Through Estimator [3]などの既存の勾配推定器を使用することで、この問題に対処することができる.
These approaches, however, suffer from either biased gradients or high variance.
しかし、これらのアプローチは、偏った勾配や高い分散に悩まされている.
Alternatively, we directly optimize discrete variables using the recently proposed augment-REINFORCEmerge (ARM) [15, 16, 56], which is unbiased and has low variance.
あるいは、最近提案されたaugment-REINFORCEmerge（ARM）[15, 16, 56]を使って直接離散変数を最適化する.

In particular, we adopt the reparameterization trick [25], which reparameterizes $\Pi_{u,v}^{(l)} \in [0, 1]$ to a deterministic function $g(\cdot)$ with parameter $\Phi_{u,v}^{(l)}$, such that:
特に、$\Pi_{u,v}^{(l)} \in [0, 1]$ をパラメータ $\Phi_{u,v}^{(l)}$ を持つ決定論的関数 $g(\cdot)$ に再パラメータ化する **reparameterization trick**[25]を採用する:

$$
\Pi_{u,v}^{(l)} = g(\Phi_{u,v}^{(l)})
\tag{9}
$$

since the deterministic function $g(\cdot)$ should be bounded within [0, 1], we simply choose the standard sigmoid function as our deterministic function: $g(x) = \frac{1}{(1 + e^{-x})}$.
決定論的関数(=閾値以上であれば陽性、みたいな?) $g(\cdot)$ は[0, 1]内で有界であるべきなので、決定論的関数として標準シグモイド関数を選ぶ： $g(x) = \frac{1}{(1 + e^{-x})}$.
As such, the second term in Eq.(8) becomes differentiable with the continuous function $g(\cdot)$.
そのため、式(8)の第2項は連続関数 $g(\cdot)$ で微分可能になる.
We next present the ARM estimator for computing the gradients of binary variables in the first term of Eq.(8) [15, 16, 56].
次に、式(8)の第1項のbinary変数(= L個のbinary mask行列 $\mathbf{Z}$ の事!)の勾配を計算するためのARM推定器を示す[15, 16, 56].

According to Theorem 1 in ARM [56], we can compute the gradients for Eq.(8) as:
ARM [56]の定理1によれば、式(8)の勾配は次のように計算できる(難しい...!!:thinking:):

$$
\Delta_{\Phi}^{ARM} L(\Phi, \Theta) =
\\
E_{\mathbf{U} \in \Pi_{l=1}^{L} Uni(\mathbf{U}^{(l)}; 0, 1)}
[L_{BCE}(I[\mathbf{U} > g(-\Phi)], \Theta) - L_{BCE}(I[\mathbf{U} < g(\Phi)], \Theta) \cdot (\mathbf{U} - \frac{1}{2})]
\\
+ \beta \Delta_{\Phi} g(\Phi)
\tag{10}
$$

where $Uni(0, 1)$ denotes the Uniform distribution within [0, 1], and $L_{BCE}(I[\mathbf{U} > g(-\Phi)], \Theta)$ is the cross-entropy loss obtained by setting the binary masks $\mathbf{Z}^{(l)}$ to 1 if $\mathbf{U}^{(l)} > g(- \Phi^{(l)})$ in the forward pass, and 0 otherwise.
ここで $Uni(0, 1)$ は[0, 1]内の一様分布を表し、$L_{BCE}(I[\mathbf{U} > g(-\Phi)], \Theta)$ は、フォワードパス(i.e. 推論時の順伝搬の事??)において、$\mathbf{U}^{(l)} > g(- \Phi^{(l)})$ の場合にバイナリマスク $\mathbf{Z}^{(l)}$ を1に設定しそれ以外の場合に0に設定する(=要はindicator functionを使ってるだけね!)ことで得られるクロスエントロピー損失. ($L_{BCE}[hoge, fuga]$ がクロスエントロピー損失関数か...!:thinking:)
The same strategy is applied to L𝐵𝐶𝐸 (I[U < 𝑔(Φ)], Θ).
同じ戦略を $L_{BCE}(I[\mathbf{U} < g(\Phi)], \Theta)$ にも適用している.
Moreover, ARM is an unbiased estimator due to the linearity of expectations.
さらに、ARM は期待値の線形性により不偏推定量となる. (真の導関数の?:thinking:)

Note that we need to evaluate L𝐵𝐶𝐸 $L_{BCE}(\cdot)$ twice to compute gradients in Eq.(10).
式(10)の勾配を計算するために、$L_{BCE}(\cdot)$ を2回評価する必要があることに注意。
Given the fact that $u \sim Uni(0, 1)$ implies $(1 − u) \sim Uni(0, 1)$, we can replace $\mathbf{U}$ with $(1 − \mathbf{U})$ in the indicator function inside $L_{BCE}(I[\mathbf{U} > g(-\Phi)],  \Theta)$:
$u \sim Uni(0, 1)$ が $(1 − u) \sim Uni(0, 1)$ を意味することから、$L_{BCE}(I[\mathbf{U} > g(-\Phi)],  \Theta)$ 内の indicator function において、$\mathbf{U}$ を $(1 − \mathbf{U})$ に置き換えることができる:

$$
I[\mathbf{U} > g(-\Phi)]
\rightleftarrows I[1 - \mathbf{U} > g(-\Phi)]
\\
\rightleftarrows I[\mathbf{U} < 1 - g(-\Phi)]
\\
\rightleftarrows I[\mathbf{U} < g(\Phi)]
$$

To this end, we can further reduce the complexity by considering the variants of ARM – Augment-Reinforce (AR) [56]:
このため、ARMの変形である**Augment-Reinforce(AR)**[56]を考慮することで、さらに複雑さを軽減することができる:

$$
\Delta_{\Theta}^{AR} L(\Phi, \Theta)
\\
= E_{\mathbf{U} \in \Pi_{l=1}^{L} Uni(\mathbf{U}^{(l)}; 0, 1)}
[L_{BCE}(I[\mathbf{U} < g(\Phi)], \Theta) \cdot (1 - 2 \mathbf{U})]
\\
+ \beta \Delta_{\Phi} g(\Phi)
\tag{11}
$$

where only requires one-forward pass.
ここで必要なのは **one-forward pass** だけだ.(なにそれ?:thinking:)
The gradient estimator $\Delta_{\Theta}^{AR} L(\Phi, \Theta)$ is still unbiased but may pose higher variance, comparing to $\Delta_{\Theta}^{ARM} L(\Phi, \Theta)$.
勾配推定量 $\Delta_{\Theta}^{AR} L(\Phi, \Theta)$ は依然として不偏であるが、$\Delta_{\Theta}^{ARM} L(\Phi, \Theta)$ に比べて分散が大きくなる可能性がある。
In the experiments, we can trade off the variance of the estimator with complexity.
実験では、推定量の分散と複雑さをトレードオフにすることができる.(ARM推定量の方が分散が小さい、AR推定量の方が複雑性が低い.)

In the training stage, we update ∇ΦL (Φ, Θ) (either Eq.(10) or Eq.(11)) and ∇ΘL (Φ, Θ) 3 during the back propagation.
学習段階では、逆伝播中に $\Delta_{\Phi} L(\Phi, \Theta)$ (式（10) または式（11））と $\Delta_{\Theta} L(\Phi, \Theta)$ を更新する.($\Phi$ と $\Theta$ をそれぞれ更新する為か...:thinking:)
In the inference stage, we can use the expectation of $Z_{u,v}^{(l)} \sim Bern(\Pi_{u,v}^{(l)})$ as the mask in Eq.(5), i.e., $E(Z_{u,v}^{(l)}) = \Pi_{u,v}^{(l)} = g(\Phi_{u,v}^{(l)})$.
推論段階では、$Z_{u,v}^{(l)} \sim Bern(\Pi_{u,v}^{(l)})$ の期待値を式(5)のマスクとして使うことができる、すなわち、$E(Z_{u,v}^{(l)}) = \Pi_{u,v}^{(l)} = g(\Phi_{u,v}^{(l)})$.
Nevertheless, this will not yield a sparse attention M(𝑙) since the sigmoid function is smooth unless the hard sigmoid function is used in Eq.(9).
とはいえ、式(9)でhard sigmoid関数(hardとは??:thinking:)を使わない限り、シグモイド関数は平滑なので、これではsparse attention $M(l)$ は得られない.(=なめらかなattention weight 分布になってしまう、って意味...!)
Here we simply clip those values $g(\Phi_{u,v}^{(l)}) \leq 0.5$ to zeros such that a sparse attention matrix is guaranteed and the corresponding noisy attentions are eventually eliminated.
ここでは、sparse attetnion行列が保証され、対応するノイジーな attentionが最終的に排除されるように、単に $g(\Phi_{u,v}^{(l)}) \leq 0.5$ をゼロに切り取る.(**閾値で0 or 1を決める**:thinking:)

## 4.2. Jacobian Regularization

As recently proved by [28], the standard dot-product self-attention is not Lipschitz continuous and is vulnerable to the quality of input sequences.
最近[28]によって証明されたように、**標準的なdot-product self-attentionはLipschitz continuous(リプシッツ連続?)ではなく**、入力sequenceの品質に弱い.
Let $f^{(l)}$ be the $l$-th Transformer block (Sec 3.2.2) that contains both a self-attention layer and a point-wise feed-forward layer, and x be the input.
$f^{(l)}$ を $l$ 番目のTransformerブロック(第3.2.2節)とし、self-attention層とpoint-wise フィードフォワード層を含むとする.
We can measure the robustness of the Transformer block using the residual error: $f^{(𝑙)}(x + \epsilon) − f^{(𝑙)}(x)$, where $\epsilon$ is a small perturbation vector and the norm of $\epsilon$ is bounded by a small scalar $\delta$, i.e., $|\epsilon|_{2} \leq \delta$.
$f^{(l)}(x + \epsilon) − f^{(l)}(x)$ (=関数の出力値の差)を使って、Transformerブロックのロバスト性を測ることができる. ここで、$\epsilon$ は小さな摂動ベクトルであり、𝝐のノルム(i.e. 大きさ!)は小さなスカラー $\delta$ で境界付けられている. i.e. $|\epsilon|_{2} \leq \delta$.
Following the Taylor expansion, we have:
テイラー展開に従うと、次のようになる:

$$
f^{(l)}_{i}(x + \epsilon) − f^{(𝑙)}_{i}(x) \eqsim [\frac{\partial f^{(𝑙)}_{i}(x)}{\partial x}]^{T} \epsilon
$$

Let $J^{(𝑙)}(x)$ represent the Jacobian matrix at $x$ where $\frac{\partial f^{(𝑙)}_{i}(x)}{\partial x}$.
$J^{(l)}(x)$ は 入力 $x$ におけるヤコビアン行列を表し、$\frac{\partial f^{(𝑙)}_{i}(x)}{\partial x}$ とする.
Then, we set $J^{(l)}_{i}(x) = \frac{\partial f^{(𝑙)}_{i}(x)}{\partial x}$ to denote the $i$-th row of $J^{(𝑙)}(x)$.
そして、$J^{(𝑙)}(x)$ の$i$番目の行を表すために、$J^{(l)}_{i}(x) = \frac{\partial f^{(𝑙)}_{i}(x)}{\partial x}$ とする.
According to Hölder’s inequality4 , we have:
[Hölderの不等式](https://en.wikipedia.org/wiki/Hölder’s_inequality)によれば、次のようになる:

$$
||f^{(l)}_{i}(x + \epsilon) − f^{(𝑙)}_{i}(x)||_{2}
\eqsim
||f^{(𝑙)}_{i}(x)^T \epsilon||_{2} \leq ||f^{(𝑙)}_{i}(x)^T \epsilon||_{2} \cdot ||\epsilon||_{2}
$$

Above inequality indicates that regularizing the L2 norm on the Jacobians enforces a Lipschitz constraint at least locally, and the residual error is strictly bounded.
上記の不等式は、**ヤコビアンのL2ノルムを正則化することで、少なくとも局所的にはリプシッツ制約が強制され**、残差(=関数の出力値の差)は厳密に有界(=定数 $L$ 以下!)であることを示している.(この場合の正の定数Lって $||f^{(𝑙)}_{i}(x)^T \epsilon||_{2} \cdot ||\epsilon||_{2}$ か...!:thinking:)
Thus, we propose to regularize Jacobians with Frobenius norm for each Transformer block as:
そこで、各Transformerブロックのヤコビアンを **Frobenius norm(?) で正則化**することを提案する: 

$$
R_{J} = \sum_{l=1}^{L} ||J^{(l)}||^{2}_{F}
\tag{12}
$$

Importantly, $|J^{(l)}|^{2}_{F}$ can be approximated via various Monte-Carlo estimators [23, 37].
重要なことは、$|J^{(l)}|^{2}_{F}$ は様々なモンテカルロ推定量[23, 37]によって近似できることです。
In this work, we adopt the classical Hutchinson estimator [23].
本研究では、古典的なHutchinson推定量[23](??)を採用する.
For each Jocobian matrix J (𝑙) ∈ R 𝑛×𝑛 , we have:
各ヤコビアン行列 $J^{(l)} \in \mathbb{R}^{n \times n}$ に対して、次のようになる：

$$
||J^{(l)}||^{2}_{F} = Tr(J^{(l)} J^{(l)}^{T})
= E_{\nu \in N(0, I_{n})} [|| \nu^{T} J^{(l)}||^{2}_{F}]
\tag{}
$$

where $\nu \in N(0, I_{n})$ is the normal distribution vector.
ここで、$\nu \in N(0, I_{n})$ は正規分布ベクトルである.(共分散行列が単位行列なので、各要素は独立...!:thinking:)
We further make use of random projections to compute the norm of Jacobians $R_{j}$ and its gradient $\Delta_{\Theta} R_{j}(\Theta)$ [21], which significantly reduces the running time in practice.
さらに、ヤコビアンのノルム $R_{j}$ とその勾配 $\Delta_{\Theta} R_{j}(\Theta)$ [21]を計算するためにrandom projections(ランダムな重みによるlinear projectionの意味??:thinking:)を利用する.

## 4.3. Optimization

### 4.3.1. Joint Training 4.3.1. 合同トレーニング

Putting together loss in Eq.(4), Eq.(6), and Eq.(12), the overall objective of Rec-Denoiser is:
式(4)、式(6)、式(12)の損失をまとめると、Rec-Denoiserの全体的な目的は次のようになる：

$$
L_{Rec-Denoiser} = L_{BCE} + \beta \cdot R_{M} + \gamma \cdot R_{J}
\tag{13}
$$

where $\beta$ and $\gamma$ are regularizers to control the sparsity and robustness of self-attention networks, respectively.
ここで $\beta$ と $\gamma$ は、**それぞれself-attentionネットワークのスパース性とロバスト性を制御する regularizer(正則化パラメータ) である**.
Algorithm 1 summarizes the overall training of Rec-Denoiser with the AR estimator.
アルゴリズム1は、AR推定器を用いたRec-Denoiserの全体的なトレーニングをまとめたものである。

![]()

Lastly, it is worth mentioning that our Rec-Denoiser is compatible to many Transformer-based sequential recommender models since our differentiable masks and gradient regularizations will not change their main architectures.
最後に、我々のRec-Denoiserは、微分可能なmask と 勾配正則化は、それらの主要なアーキテクチャを変更しないので、**多くのTransformerベースの逐次推薦モデルと互換性がある**ことを言及する価値がある.
If we simply set all masks $Z^{(l)}$ to be all-ones matrix and $\beta = \gamma = 0$, our model boils down to their original designs.
単純にすべてのマスク $Z^{(l)}$ ($\forall l=1, \cdots, L$ :thinking:)をオール1の行列とし、$\beta = \gamma = 0$ とすると、**モデルは元の設計に帰着する**.(分かる分かる...!)
If we randomly set subset of masks Z (𝑙) to be zeros, it is equivalent to structured Dropout like LayerDrop [17], DropHead [60].
マスクのサブセット(i.e. L個のbinary mask matrixのうちのいくつか) $Z^{(l)}$ をランダムにゼロに設定すると、LayerDrop [17]やDropHead [60]のような **structured Dropout と等価**になる.
In addition, our Rec-Denoiser can work together with linearized self-attention networks [27, 59] to further reduce the complexity of attentions.
さらに、私たちのRec-Denoiserは、線形化されたself-attentionネットワーク[27, 59]と連携(よくイメージが湧いてない...?)することができ、attentionの複雑さをさらに軽減することができる。
We leave this extension in the future.
私たちはこの延長を将来に残す.

### 4.3.2. Model Complexity 4.3.2. モデルの複雑さ

The complexity of Rec-Denoiser comes from three parts: a basic Transformer, differentiable masks, and Jacobian regularization.
Rec-Denoiserのcomplexity(計算量?)は、基本的なTransformer、微分可能なmask、Jacobian正則化という3つの部分から来ている。
The complexity of basic Transformer keeps the same as SASRec [26] or BERT4Rec [41].
基本的なTransformerのcomplexity(計算量?)は、SASRec [26]やBERT4Rec [41]と同じである。
The complexity of differentiable masks requires either one-forward pass (e.g., AR with high variance) or two-forward pass (e.g., ARM with low variance) of the model.
微分可能なマスクの計算量は、モデルのone-forward pass(高分散のARなど)またはtwo-forward pass(低分散のARMなど)を必要とする.(n-forward passの意味がわかってない...:thinking:)
In sequential recommenders, the number of Transformer blocks is often very small (e.g., 𝐿 = 2 in SASRec [26] and BERT4Rec [41] ).
**逐次レコメンダーでは、Transformerブロックの数は非常に少ないことが多い**（例えば、SASRec [26]とBERT4Rec [41] では L = 2 ）。
It is thus reasonable to use the ARM estimator without heavy computations.
従って、重い計算をせずにARM推定量を使用することは合理的である。
Besides, we compare the performance of AR and ARM estimators in Sec 5.3.
加えて、5.3章でAR推定量とARM推定量を用いる場合のperformanceを比較した.

Moreover, the random project techniques are surprisingly efficient to compute the norms of Jacobians [21].
さらに、random project技法はヤコビアンのノルムを計算するのに驚くほど効率的である[21].
As a result, the overall computational complexity remains the same order as the original Transformers during the training.
その結果、**全体的な計算量は、トレーニング中のオリジナルのTransformersと同じオーダーのまま**である.
However, during the inference, our attention maps are very sparse, which enables much faster feed-forward computations.
しかし、推論中の attention map は非常に疎なため、フィードフォワード計算をより高速に行うことができる. (推論は元々のTransformerよりも高速ってことね...!)

# 5. Experiments 5. 実験

Here we present our empirical results.
ここでは実証的な結果を紹介する
Our experiments are designed to answer the following research questions:
我々の実験は、以下の研究課題に答えるためにデザインされた：

- RQ1: How effective is the proposed Rec-Denoiser compared to the state-of-the-art sequential recommenders? RQ1: 提案するRec-Denoiserは、**最新の逐次推薦器と比較してどの程度有効**か？
- RQ2: How can Rec-Denoiser reduce the negative impacts of noisy items in a sequence? RQ2：Rec-Denoiserは、**sequence内のノイズの多いアイテムの悪影響をどのように軽減できますか**？

- RQ3: How do different components (e.g., differentiable masks and Jacobian regularization) affect the overall performance of Rec-Denoiser? RQ3：**異なる構成要素(微分可能 mask や Jacobian 正則化など）は、Rec-Denoiserの全体的な性能にどのような影響を与えるか**？

## 5.1. Experimental Setting # 5.1.Experimental Setting

### 5.1.1. Dataset 5.1.1. データ集合

We evaluate our models on five benchmark datasets: Movielens5 , Amazon6 (we choose the three commonly used categories: Beauty, Games, and Movies&TV), and Steam7 [30].
我々は5つのベンチマークデータセットでモデルを評価する： Movielens5、Amazon6（美容、ゲーム、映画＆TVの3つのよく使われるカテゴリーを選択）、Steam7 [30]である。
Their statistics are shown in Table 1.
統計は表1の通りである。
Among different datasets, MovieLens is the most dense one while Beauty has the fewest actions per user.
異なるデータセットの中で、MovieLensは最も密度が高く、Beautyはユーザーあたりのアクション数が最も少ない。
We use the same procedure as [26, 30, 39] to perform preprocessing and split data into train/valid/test sets, i.e., the last item of each user’s sequence for testing, the second-to-last for validation, and the remaining items for training.
26,30,39]と同じ手順で前処理を行い、データをtrain/valid/testセットに分割する。つまり、各ユーザのsequenceの最後のアイテムをtestingに、最後から2番目のアイテムをvalidationに、残りのアイテムをtrainingに使用する。

### 5.1.2. Baselines 5.1.2. ベースライン

Here we include two groups of baselines.
ここでは、2つのベースライン・グループが含まれている。
The first group includes general sequential methods (Sec 5.2): 1) FPMC [39]: a mixture of matrix factorization and first-order Markov chains model; 2) GRU4Rec [20]: a RNN-based method that models user action sequences; 3) Caser [42]: a CNN-based framework that captures high-order relationships via convolutional operations; 4) SASRec [26]: a Transformer-based method that uses left-to-right selfattention layers; 5) BERT4Rec [41]: an architecture that is similar to SASRec, but using bidirectional self-attention layers; 6) TiSASRec [30]: a time-aware self-attention model that further considers the relative time intervals between any two items; 7) SSE-PT [50]: a framework that introduces personalization into self-attention layers; 8) Rec-Denoiser: our proposed Rec-Denoiser that can choose any self-attentive models as its backbone.
最初のグループには、一般的な逐次的手法が含まれる（Sec.5.2）：

- 1. FPMC [39]：行列分解と一次マルコフ連鎖モデルの混合
- 2. GRU4Rec [20]：ユーザーの行動シーケンスをモデル化するRNNベースの手法
- 3. Caser [42]：畳み込み演算によって高次の関係を捉えるCNNベースのフレームワーク、
- 4. SASRec [26]：左から右への自己注意層を使用するTransformerベースの手法、
- 5. BERT4Rec [41]：
- 6. TiSASRec [30]：任意の2つのアイテムの間の相対的な時間間隔をさらに考慮する、時間を考慮した自己注意モデル、
- 7. SSE-PT [50]：self-attention層にパーソナライズを導入するフレームワーク、
- 8. Rec-Denoiser：バックボーンとして任意のself-attentionモデルを選択できる、我々の提案するRec-Denoiser。

The second group contains sparse Transformers (Sec 5.3):
2番目のグループにはスパース変換器（Sec.5.3）が含まれる：

- 1. Sparse Transformer [10]: it uses a fixed attention pattern, where only specific cells summarize previous locations in the attention layers; **固定されたatteniton パターンを使用**し、特定のセルだけがattetnion層の前の位置を要約する；
- 2. 𝛼-entmax sparse attention [12]: it simply replaces softmax with 𝛼-entmax to achieve sparsity. スパース性を達成するためにソフトマックスを 𝛼-entmax に置き換えたもの。

Note that we do not compare with other popular sparse Transformers like Star Transformer [18], Longformer [2], and BigBird [58].
なお、Star Transformer [18]、Longformer [2]、BigBird [58]のような他の有名なスパース変換器とは比較していない。
These Transformers are specifically designed for thousands of tokens or longer in the language modeling tasks.
これらのトランスフォーマーは、言語モデリングタスクにおける数千以上のトークン用に特別に設計されている。(だからね!)
We leave their explorations for recommendations in the future.
彼らの探求は今後の提言に委ねたい。
We also do not compare with LayerDrop [17] and DropHead [60] since the number of Transformer blocks and heads are often very small (e.g., 𝐿 = 2 in SARRec) in sequential recommendation.
また、LayerDrop[17]やDropHead[60]との比較は行わない。なぜなら、逐次推薦では、Transformerブロックやヘッドの数が非常に少ない(例えば、SARRecでは𝐿 = 2)ことが多いからである。
Other sequential architectures like memory networks [9, 22] and graph neural networks [4, 51] have been outperformed by the above baselines, we simply omit these baselines and focus on Transformer-based models.
メモリ・ネットワーク[9, 22]やグラフ・ニューラル・ネットワーク[4, 51]のような他の逐次アーキテクチャは、上記のベースラインよりも優れている.
The goal of experiments is to see whether the proposed differentiable mask techniques can reduce the negative impacts of noisy items in the self-attention layers.
**実験の目的は、提案された微分可能なマスク技術が、self-attention層におけるノイズアイテムの悪影響を軽減できるかどうかを確認すること**である。

### 5.1.3. Evaluation metrics 5.1.3. 評価指標

For easy comparison, we adopt two common Top-N metrics, Hit@𝑁 and NDCG@𝑁 (with default value $N = 10$), to evaluate the performance of sequential models [26, 30, 41].
比較を容易にするために、逐次モデルのパフォーマンスを評価するために、2つの一般的なTop-Nメトリクス、**Hit@N**と**NDCG@N**(デフォルト値ǔ = 10)を採用する[26, 30, 41].
Typically, Hit@𝑁 counts the rates of the ground-truth items among top-𝑁 items, while NDCG@𝑁 considers the position and assigns higher weights to higher positions.
一般的に、Hit@N は、top-Nアイテムの中でグランドトゥルースアイテムの割合をカウントし、NDCG@N は位置(ランキング内)を考慮し、高い位置に高い重みを割り当てる.
Following the work [26, 30], for each user, we randomly sample 100 negative items, and rank these items with the ground-truth item.
[26,30]に従い、各ユーザについて100個のネガティブアイテム(ex. まだ購入してないアイテム)をランダムにサンプリングし、これらのアイテムをground-truthアイテム(=testデータの1 item)と一緒に順位付けする.
We calculate Hit@10 and NDCG@10 based on the rankings of these 101 items.
この**101項目のランキング**をもとにHit@10とNDCG@10を算出した.

### 5.1.4. Parameter settings 5.1.4. パラメータ設定(ハイパーパラメータ設定)

For all baselines, we initialize the hyper-parameters as the ones suggested by their original work.
すべてのベースラインについて、ハイパーパラメータを彼らのオリジナル研究で提案されたものとして初期化した。
They are then well tuned on the validation set to achieve optimal performance.
They are then well tuned on the validation set to achieve optimal performance.
そして、最適なパフォーマンスを達成するために、セット上で十分に調整される。
The final results are conducted on the test set.
最終的な結果はtestセットで実施される.
We search the dimension size of items within {10, 20, 30, 40, 50}.
itemの(embeddingの?)次元サイズを{10, 20, 30, 40, 50}の範囲で検索する。
As our Rec-Denoiser is a general plugin, we use the same hyper-parameters as the basic Transformers, e.g., number of Transformer blocks, batch size, learning rate in Adam optimizer, etc.
我々のRec-Denoiserは一般的なプラグインであるため、基本的なTransformerと同じハイパーパラメータを使用する。例えば、Transformerブロックの数、バッチサイズ、Adamオプティマイザーの学習率などである。
According to Table 1, we set the maximum length of item sequence $n = 50$ for dense datasets MovieLens and Movies&TV, and $n = 25$ for sparse datasets Beauty, Games, and Steam.
表1によると、アイテム列の最大長を、密なデータセットであるMovieLensとMovies&TVには $n = 50$ を、疎なデータセットであるBeauty、Games、Steamには $n = 25$ を設定した.
In addition, we set the number of Transformer blocks 𝐿 = 2, and the number of heads 𝐻 = 2 for self-attentive models.
さらに、トランスフォーマーブロックの数 $L = 2$、self-attentionモデルのヘッド数$H = 2$とした. (LもHもnext-token predictionタスクと比較して少なめなんだな...!:thinking:)
For Rec-Denoiser, two extra regularizers 𝛽 and 𝛾 are both searched within {10−1 , 10−2 , . . . , 10−5 }
Rec-Denoiserでは、2つの正則化子 $\beta$ と $\gamma$ が ${10-1 , 10-2 , ... , 10-5}$ 内で探索される.
We choose ARM estimator due to the shallow structures of self-attentive recommenders.
我々は、self-attention型推薦者の構造が浅いことから、ARM推定器を選択した.

## 5.2. Overall Performance(RQ1) 5.2.総合成績（RQ1）

![table2]()

Table 2 presents the overall recommendation performance of all methods on the five datasets.
表2は、5つのデータセットにおけるすべての手法の総合的な推薦性能を示している。
Our proposed Recdenoisers consistently obtain the best performance for all datasets.
我々の提案する**Recdenoisersは、すべてのデータセットで一貫して最高の性能を得た**。
Additionally, we have the following observations:
さらに、次のような見解もある：

- The self-attentive sequential models (e.g., SASRec, BERT4Rec, TiSASRec, and SSE-PT) generally outperform FPMC, GRU4Rec, and Caser with a large margin, verifying that the self-attention networks have good ability of capture long-range item dependencies for the task of sequential recommendation. self-attention型逐次推薦モデル（SASRec、BERT4Rec、TiSASRec、SSE-PTなど）は、一般にFPMC、GRU4Rec、Caserを大きなマージンをもって上回る結果だった. **self-attention型ネットワークが逐次推薦のタスクに対して長距離項目依存性を捕捉する優れsた能力を持つことが検証された**.

- Comparing the original SASRec and its variants BERT4Rec, TiSASRec and SSE-PT, we find that the self-attentive models can gets benefit from incorporating additional information such as bi-directional attentions, time intervals, and user personalization. Such auxiliary information is important to interpret the dynamic behaviors of users. オリジナルのSASRecとその変種であるBERT4Rec、TiSASRec、SSE-PTを比較すると、**self-attentionsモデルは、bi-directional attentions、time intervals、user personalizationなどの追加情報を取り入れることで利益を得る**ことができることがわかる。 このような補助情報は、ユーザのダイナミックな行動を解釈するために重要である.

- The relative improvements of Rec-denoisers over their backbones are significant for all cases. For example, SASRec+Denoiser has on average 8.04% improvement with respect to Hit@10 and over 12.42% improvements with respect to NDCG@10. Analogously, BERT4Rec+Denoiser outperforms the vanilla BERT4Rec by average 7.47% in Hit@10 and 11.64% in NDCG@10. We also conduct the significant test between Rec-denoisers and their backbones, where all 𝑝-values< 1𝑒 −6 , showing that the improvements of Rec-denoisers are statistically significant in all cases. **Rec-denoisersのバックボーンに対する相対的な向上は、すべてのケースで顕著である**。 例えば、SASRec+Denoiserは、Hit@10に対して平均8.04%、NDCG@10に対して平均12.42%以上の改善が見られる。 同様に、BERT4Rec+Denoiserは、Hit@10では平均7.47%、NDCG@10では平均11.64%で、バニラBERT4Recを上回っている。 また、Rec-denoiserとそのバックボーンとの間の有意差検定も行った。ここでは、すべての p < 1𝑒 -6であり、Rec-denoiserの改善がすべてのケースで統計的に有意であることが示された.

These improvements of our proposed models are mainly attributed to the following reasons: 1) Rec-denoisers inherit full advantages of the self-attention networks as in SASRec, BERT4Rec, TiSASRec, and SSE-PT; 2) Through differentiable masks, irrelevant item-item dependencies are removed, which could largely reduce the negative impacts of noisy data; 3) Jacobian regularization enforces the smoothness of gradients, limiting quick changes of the output against input perturbations.
提案モデルのこれらの改善は主に以下の理由による：

- 1）Rec-denoisersは、SASRec、BERT4Rec、TiSASRec、SSE-PTのような**self-attentionネットワークの利点を完全に受け継いでいる** (だから性能が下がるはずがないか:thinking:)
- 2）微分可能なマスクを通して、無関係なitem-item依存性が除去され、ノイズの多いデータの悪影響を大幅に軽減できる
- 3）Jacobian正則化は勾配の滑らかさを強制し、入力摂動に対する出力の素早い変化を制限する。(Jacobian正則化を導入しないと、勾配が急になるってことだろうか??)In general, smoothness improves the generalization of sequential recommendation.一般的に、滑らかさは逐次推薦の一般性を向上させる。

Overall, the experimental results demonstrate the superiority of our Rec-Denoisers.
全体として、実験結果は我々のRec-Denoisersの優位性を示している。

## 5.3. Robustness to Noises(RQ2)

As discussed before, the observed item sequences often contain some noisy items that are uncorrelated to each other.
前述したように、観測されたitem sequence には、しばしば**互いに無相関なノイズitem**が含まれる.(=絶対的にnoisyなitemというよりは、相対的にnoisyなitemの意味合い:thiking:)
Generally, the performance of self-attention networks is sensitive to noisy input.
一般に、self-attentionネットワークの性能はノイズの多い入力に敏感である。
Here we analyze how robust our training strategy is for noisy sequences.
ここでは、**ノイズの多いsequenceに対して、我々のトレーニング戦略がどの程度ロバストであるか**を分析する。
To achieve this, we follow the strategy [35] that corrupts the training data by randomly replacing a portion of the observed items in the training set with uniformly sampled items that are not in the validation or test set.
これを達成するために、我々は、**トレーニングセットで観測されたitemの一部を、検証セットやテストセットにはない一様にサンプリングされたitemでランダムに置き換える**ことによって、トレーニングデータを破損させる戦略[35]に従う.
We range the ratio of the corrupted training data from 0% to 25%.
**破損したトレーニングデータの比率は、0%から25%の範囲**である.
We only report the results of SASRec and SASRec-Denoiser in terms of Hit@10.
SASRecとSASRec-Denoiserの結果は、Hit@10でのみ報告する。
The performance of other self-attentive models is the same and omitted here due to page limitations.
他のself-attentionモデルのパフォーマンスも同様で、ここではページの都合上省略した。
In addition, we compare with two recent sparse Transformers: Sparse Transformer [10] and 𝛼-entmax sparse attention [12].
さらに、最近の2つのスパース変換器と比較する： Sparse Transformer [10]と ↪L_1D6FC↩-entmax sparse attention [12]である.

![figure2]()

All the simulated experiments are repeated five times and the average results are shown in Figure 2.
すべての模擬実験を5回繰り返し、その平均結果を図2に示す。
Clearly, the performance of all models degrades with the increasing noise ratio.
明らかに、**すべてのモデルの性能は、ノイズ比率の増加とともに低下する**。
We observe that our Rec-denoiser (use either ARM or AR estimators) consistently outperforms 𝛼-entmax and Sparse Transformer under different ratios of noise on all datasets.
我々は、我々の**Rec-denoiser(ARMまたはAR推定量を使用)が、全てのデータセットにおいて、異なるノイズ比率の下で一貫して $\alpha$-entmaxとSparse Transformerを上回ることを観察した**。
𝛼-entmax heavily relies on one trainable parameter 𝛼 to filter out the noise, which may be over tuned during the training, while Sparse Transformer adopts a fixed attention pattern, which may lead to uncertain results, especially for short item sequences like Beauty and Games.
𝛼-entmax は、ノイズをフィルタリングするための1つの訓練可能なパラメータ𝛼に大きく依存しており、訓練中に過剰に調整される可能性があります. 一方、Sparse Transformerは固定されたattenitionパターン(maskパターン)を採用しており、特にBeautyやGamesのような短いアイテムシーケンスでは、不確実な結果につながる可能性があります。
In contrast, our differentaible masks have much more flexibility to adapt to noisy sequences.
対照的に、我々の**微分可能マスクは、ノイズの多いシーケンスに適応する柔軟性がはるかに高い**。
The Jacobian regularization further encourages the smoothness of our gradients, leading to better generalization.
**ヤコビアン正則化は、勾配の滑らかさをさらに促進し**、より良い汎化をもたらす。
From the results, the AR estimator performs better than 𝛼-entmax but worse than ARM.
その結果、AR推定器は𝛼-entmaxよりは良いが、ARMよりは悪い。
This result is expected since ARM has much low variance.
**ARMは分散が少ないので、この結果は予想通り**である。
In summary, both ARM and AR estimators are able to reduce the negative impacts of noisy sequences, which could improve the robustness of self-attentive models.
まとめると、ARMとARの両推定器は、ノイズの多いシーケンスの悪影響を軽減することができ、self-attentionモデルの頑健性を向上させることができる。

## 5.4. Study of Rec-Denoiser(RQ3)

We further investigate the parameter sensitivity of Rec-Denoiser.
さらに**Rec-Denoiserのparameter sensitivity**を調べた.
For the number of blocks $L$ and the number of heads $H$, we find that self-attentive models typically benefit from small values (e.g., $H, L \leq 4$), which is similar to [31, 41].
**ブロック数 $L$ とヘッド数 $H$ については、self-attentionモデルは一般的に小さな値（例えば、$H, L \leq 4$）が有効であることがわかり**、これは[31, 41]と同様である。
In this section, we mainly study the following hyper-parameters: 1) the maximum length 𝑛, 2) the regularizers 𝛽 and 𝛾 to control the sparsity and smoothness.
本節では、主に以下のハイパーパラメータを研究する： 1)sequence最大長$n$、2)スパース性と平滑性を制御する正則化子$\beta$と$\gamma$.
Here we only study the SASRec and SASRec-Denoiser due to page limitations.
ここでは、ページの都合上、SASRecとSASRec-Denoiserについてのみ述べる。

![figure3]()

Fig.3.Effect of maximum length 𝑛 on ranking performance (Hit@10).
図3.最大長𝑛がランキング性能に与える影響（Hit@10）.

![figure4]()

Fig.4.Effect of regularizers 𝛽 and 𝛾 on ranking performance (Hit@10).
図4.正則化量ǽとǖがランキング性能に与える影響(Hit@10FE6)。

### 5.4.1. Maximum Length $n$ 5.4.1. sequence の 最大長 $n$

Figure 3 shows the Hit@10 for maximum length 𝑛 from 20 to 80 while keeping other optimal hyper-parameters unchanged.
図3は、他の最適ハイパーパラメータを変えずに、最大長$n$を20から80まで変化させた場合のHit@10を示している。
We only test on the densest and sparsest datasets: MovieLeans and Beauty.
最も高密度で疎なデータセットでのみテストする： MovieLeansとBeautyである。
Intuitively, the larger sequence we have, the larger probability that the sequence contains noisy items.
直観的には、**シーケンスが大きければ大きいほど、そのシーケンスにノイズのあるitemが含まれる確率が高くなる**。
We observed that our SASRec-Denoiser improves the performance dramatically with longer sequences.
**我々のSASRec-Denoiserは、長いシーケンスで劇的に性能が向上する**ことが確認された。
This demonstrates that our design is more suitable for longer inputs, without worrying about the quality of sequences.
これは、我々の設計がシーケンスの質を気にすることなく、より長い入力に適していることを示している。

### 5.4.2. The regularizers $\beta$ and $\gamma$ 5.4.2. 正則化記号$beta$と$gamma$。

There are two major regularization parameters 𝛽 and 𝛾 for sparsity and gradient smoothness, respectively.
正則化パラメータǽと𝛾は、それぞれスパース性と勾配平滑性を表す。
Figure 4 shows the performance by changing one parameter while fixing the other as 0.01.
図4は、一方のパラメーターを0.01に固定し、もう一方のパラメーターを変更した場合のパフォーマンスを示している
As can be seen, our performance is relatively stable with respect to different settings.
見てわかるように、**我々のパフォーマンスは異なるハイパーパラメータ設定に対して比較的安定している**
In the experiments, the best performance can be achieved at 𝛽 = 0.01 and 𝛾 = 0.001 for the MovieLens dataset.
実験では、MovieLensデータセットに対して、↪Ll_1D6FD = 0.01とǖ = 0.001で最高の性能を達成することができた。

# 6. Conclusion and Fture Work 6. 結論と今後の課題

In this work, we propose Rec-Denoiser to adaptively eliminate the negative impacts of the noisy items for self-attentive recommender systems.
本研究では、Rec-Denoiserを提案し、self-attention型レコメンダーシステムにおけるノイズアイテムの悪影響を適応的に除去する。
The proposed Rec-Denoiser employs differentiable masks for the self-attention layers, which can dynamically prune irrelevant information.
提案するRec-Denoiserは、self-attention層に微分可能なマスクを採用し、無関係な情報を動的に除去することができる。
To further tackle the vulnerability of self-attention networks to small perturbations, Jacobian regularization is applied to the Transformer blocks to improve the robustness.
小さな摂動に対するself-attentionネットワークの脆弱性にさらに取り組むため、ロバスト性を向上させるヤコビアン正則化がトランスフォーマー・ブロックに適用される.
Our experimental results on multiple real-world sequential recommendation tasks illustrate the effectiveness of our design.
実世界の複数の逐次推薦タスクに関する実験結果は、我々の設計の有効性を示している。

Our proposed Rec-Denoiser framework (e.g., differentiable masks and Jacobian regularization) can be easily applied to any Transformer-based models in many tasks besides sequential recommendation.
**我々の提案するRec-Denoiserフレームワーク（微分可能マスクやヤコビアン正則化など）は、逐次推薦以外の多くのタスクにおいて、あらゆるTransformerベースのモデルに容易に適用**できる.(推薦以外にも、Transformerを用いる汎ゆるタスク?? next-token predictionとかにも??:thinking:)
In the future, we will continue to dmonstrate the contributions of our design in many real-world applications.
将来的には、多くの実世界のアプリケーションにおいて、我々の設計の貢献を実証していくつもりである。
