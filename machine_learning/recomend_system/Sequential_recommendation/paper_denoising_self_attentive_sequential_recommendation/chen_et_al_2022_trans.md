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
One key component of Transformers is the self-attention network, which is capable of learning long-range dependencies by computing attention weights between each pair of objects in a sequence.
Transformersの主要な構成要素の1つはself-attention networkであり、シーケンス中の各対象間のattention weightを計算することで**長距離依存関係を学習することができる**.
Inspired by the success of Transformers, several self-attentive sequential recommenders have been proposed and achieve the state-of-the-art performance [26, 41, 49, 50].
Transformersの成功に触発され、いくつかのself-attentive sequential recommendersが提案され、最新の性能を達成している[26, 41, 49, 50].
For example, SASRec [26] is the pioneering framework to adopt self-attention network to learn the importance of items at different positions.
例えば、SASRec [26]は、異なる位置にあるitemの重要度を学習するために、self-attention networkを採用した先駆的なフレームワークである.
BERT4Rec [41] further models the correlations of items from both left-to-right and right-to-left directions.
BERT4Rec [41]は、さらに左から右、右から左の両方向のitemの相関をモデル化する.
SSE-PT [50] is a personalized Transformer model that provides better interpretability of engagement patterns by introducing user embeddings.
SSE-PT [50]は、user embeddingsを導入することにより、エンゲージメントパターンの解釈可能性を向上させるパーソナライズドトランスフォーマーモデルである.
LSAN [31] adopts a novel twin-attention sequential framework, which can capture both long-term and short-term user preference signals.
LSAN [31]は新しいtwin-attention sequential frameworkを採用し、長期と短期の両方のユーザー嗜好シグナルを捉えることができる.
Recently, Transformers4Rec [14] performs an empirical analysis with broad experiments of various Transformer architectures for the task of sequential recommendation.
最近、Transformers4Rec [14]は、逐次推薦のタスクのために、様々なTransformerアーキテクチャの幅広い実験による実証分析を行っている.

Although encouraging performance has been achieved, the robustness of sequential recommenders is far less studied in the literature.
しかし、**逐次推薦器のrobustnessについてはあまり研究されていない**.
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
残念ながら、vanilla self-attention networkは**Lipschitz連続ではなく(?)**、**入力シーケンスの質に弱いという問題**がある[28]。
Recently, in the tasks of language modeling, people found that a large amount of BERT’s attentions focus on less meaningful tokens, like "[SEP]" and ".
最近、言語モデリングのタスクにおいて、BERT の注意の多くが、"[SEP]" や "." のようなあまり意味のないトークンに集中することが判明した.
", which leads to a misleading explanation [11].
「のような、あまり意味のないトークンに BERT の注意が集中し、誤解を招く説明になっていることが判明している[11]。
It is thus likely to obtain sub-optimal performance if self-attention networks are not well regularized for noisy sequences.
このように、自己注意ネットワークがノイズの多いシーケンスに対してうまく正則化されていない場合、最適とは言えない性能が得られる可能性がある.
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
また、エンドツーエンドの学習アプローチとは異なり、これらの疎なパターンが逐次推薦にうまく一般化できるかどうかは不明であり、まだ未解決の研究課題である.

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

1. Irrelevant attentions with parameterized masks can be learned to be dropped in a data-driven way.
2. パラメータ化されたマスクを持つ無関係なattentionは、データ駆動型の方法で削除されるように学習させることができる.
   - Taking Figure 1 as an example, our Rec-denoiser would prune the sequence (phone, bag, headphone) for pant, and (phone, bag, headphone, pant) for laptop in the attention maps.図1を例にとると、Rec-denoiserは、アテンションマップにおいて、ズボンには(phone, bag, headphone)、ノートパソコンには(phone, bag, headphone, pant)という順序を切り捨てることになる.
   - Namely, we seek next item prediction explicitly based on a subset of more informative items. つまり、より情報量の多いアイテムの部分集合(subset)に基づき、明示的に次のアイテム予測を行うのです.
3. Our Rec-Denoiser still takes full advantage of Transformers as it does not change their architectures, but only the attention distributions.
4. 我々のRec-DenoiserはTransformerのアーキテクチャを変更せず、**アテンション分布のみを変更する**ため、Transformerを最大限に活用することができる.
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
また、スケールドットプロダクトの注目点はLipschitz連続(?)ではないため、入力摂動に対して脆弱である[28].
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

## 2.1. Sequential Recommendation 2.1. シーケンシャルレコメンデーション

Leveraging sequences of user-item interactions is crucial for sequential recommendation.
逐次推薦では、ユーザーとアイテムの相互作用のシーケンスを活用することが重要である。
User dynamics can be caught by Markov Chains for inferring the conditional probability of an item based on the previous items [19, 39].
ユーザダイナミクスはマルコフ連鎖によって捕捉され、前のアイテムに基づくアイテムの条件付き確率を推論することができる[19, 39]。
More recently, growing efforts have been dedicated to deploying deep neural networks for sequential recommendation such as recurrent neural networks [20, 53], convolutional neural networks [42, 54, 57], memory networks [9, 22], and graph neural networks [4, 7, 51].
最近では、リカレントニューラルネットワーク [20, 53]、畳み込みニューラルネットワーク [42, 54, 57]、メモリネットワーク [9, 22]、グラフニューラルネットワーク [4, 7, 51] などの深いニューラルネットワークを逐次推薦に利用する取り組みが盛んになっている。
For example, GRU4Rec [20] employs a gated recurrent unit to study temporal behaviors of users.
例えば、GRU4Rec[20]はユーザの時間的行動を研究するためにゲーテッドリカレントユニットを採用している。
Caser [42] learns sequential patterns by using convolutional filters on local sequences.
Caser [42]は局所的な配列に対して畳み込みフィルタを用いて連続的なパターンを学習する。
MANN [9] adopts memory-augmented neural networks to model user historical records.
MANN [9]はユーザの履歴記録をモデル化するためにメモリ補強型ニュー ラルネットワークを採用する。
SR-GNN [51] converts session sequences into graphs and uses graph neural networks to capture complex item-item transitions.
SR-GNN [51]はセッションシーケンスをグラフに変換し、グラフニューラルネットワークを使用して複雑なアイテム-アイテム遷移を捉える。

Transformer-based models have shown promising potential in sequential recommendation [5, 26, 30, 32, 33, 41, 49, 50], due to their ability of modeling arbitrary dependencies in a sequence.
トランスフォーマーに基づくモデルは、シーケンス中の任意の依存関係をモデル化できるため、逐次推薦において有望な可能性を示している[5, 26, 30, 32, 33, 41, 49, 50]．
For example, SASRec [26] first adopts self-attention network to learn the importance of items at different positions.
例えば、SASRec [26]では、まず、異なる位置にある項目の重要度を学習するために、自己アテンションネットワークを採用している。
In the follow-up studies, several Transformer variants have been designed for different scenarios by adding bidirectional attentions [41], time intervals [30], personalization [50], importance sampling [32], and sequence augmentation [33].
その後、双方向の注意[41]、時間間隔[30]、個人化[50]、重要度サンプリング[32]、シーケンス拡張[33]を追加し、異なるシナリオのためにいくつかの変種が設計されてきた。
However, very few studies pay attention to the robustness of self-attentive recommender models.
しかし、自己アテンション型推薦モデルの頑健性に注目した研究は非常に少ない。
Typically, users’ sequences contain lots of irrelevant items since they may subsequently purchase a series of products with different purposes [45].
一般に、ユーザのシーケンスには無関係な項目が多く含まれる。
As such, the current user action only depends on a subset of items, not on the entire sequences.
このような場合、現在のユーザの行動は、シーケンス全体ではなく、アイテムのサブセットにのみ依存する。
However, the self-attention module is known to be sensitive to noisy sequences [28], which may lead to sub-optimal generalization performance.
しかし、自己注意モジュールはノイズの多いシーケンスに敏感であることが知られており[28]、これは最適でない汎化性能につながる可能性がある。
In this paper, we aim to reap the benefits of Transformers while denoising the noisy item sequences by using learnable masks in an end-to-end fashion.
本論文では、学習可能なマスクをエンドツーエンドで用いることにより、ノイズの多いアイテム列をノイズ化しつつ、Transformersの利点を享受することを目指す。

## 2.2. Sparce Transformer 2.2. スパース変圧器

Recently, many lightweight Transformers seek to achieve sparse attention maps since not all attentions carry important information in the self-attention layers [2, 10, 18, 29, 58].
最近、多くの軽量トランスフォーマーが、全てのアテンションが自己アテンション層の重要な情報を持っているわけではないので、疎なアテンションマップを実現することを追求している[2, 10, 18, 29, 58]。
For instance, Reformer [29] computes attentions based on locality-sensitive hashing, leading to lower memory consumption.
例えば、Reformer [29]は局所性を考慮したハッシュに基づいてアテンションを計算し、メモリ消費の低減につながる。
Star Transformer [18] replaces the fully-connected structure of self-attention with a star-shape topology.
Star Transformer [18]は、自己アテンションの完全連結構造を星形のトポロジーに置き換えたものである。
Sparse Transformer [10] and Longformer [2] achieve sparsity by using various sparse patterns, such as diagonal sliding windows, dilated sliding windows, local and global sliding windows.
Sparse Transformer [10] と Longformer [2] は、斜めスライド窓、拡張スライド窓、ローカルスライド窓、グローバルスライド窓など、様々なスパースパターンを用いてスパース性を実現する。
BigBird [58] uses random and several fixed patterns to build sparse blocks.
BigBird [58]では，ランダムなパターンといくつかの固定パターンを用いて，疎なブロックを構築している．
It has been shown that these sparse attentions can obtain the state-of-the-art performance and greatly reduce computational complexity.
これらの疎な注意は、最先端の性能を得ることができ、計算量を大幅に削減できることが示されている。
However, many of them rely on fixed attention schemas that lack flexibility and require tremendous engineering efforts.
しかし、これらの多くは、柔軟性に欠け、膨大な工学的努力を必要とする固定的な注意スキーマに依存している。

Another line of work is to use learnable attention distributions [12, 36, 38, 40].
また、学習可能な注意分布[12, 36, 38, 40]を使用することもある。
Mostly, they calculate attention weights with variants of sparsemax that replaces the softmax normalization in the self-attention networks.
ほとんどの場合、自己アテンションネットワークにおけるソフトマックス正規化を置き換えるsparsemaxの変種を用いてアテンション重みを計算する。
This allows to produce both sparse and bounded attentions, yielding a compact and interpretable set of alignments.
これにより、疎で境界のある注意を生成することができ、コンパクトで解釈可能なアラインメントの集合を得ることができる。
Our Rec-denoiser is related to this line of work.
我々のRec-denoiserは、この研究に関連している。
Instead of using sparsemax, we design a trainable binary mask for the self-attention network.
スパースマックスを用いる代わりに、我々は自己注意ネットワークに対して学習可能なバイナリマスクを設計する。
As a result, our proposed Rec-denoiser can automatically determine which self-attention connections should be deleted or kept in a data-driven way.
その結果、我々の提案するRec-denoiserは、データ駆動型の方法で、どの自己注意の接続を削除すべきか、あるいは保持すべきかを自動的に決定することができる。

# 3. Problem and Background 3. 問題点と背景

In this section, we first formulate the problem of sequential recommendation, and then revisit several self-attentive models.
本節では、まず逐次推薦の問題を定式化し、次にいくつかの自己アテンションモデルを再検討する。
We further discuss the limitations of the existing work.
さらに、既存の研究の限界について議論する。

## 3.1. Problem Setup 3.1. 問題の設定

In sequential recommendation, let $U$ be a set of users, $I$ a set of items, and $S = {S^1, S^2,\cdots, S^{
U

We user $S^u = (S^u*1, S^u_2, \cdots, S^u*{
S^u

Given the interaction history $S^u$, sequential recommendation seeks to predict the next item $S^u_{S^u+1}$ at time step $
S^u+1

During the training process [26, 41], it will be convenient to regard the model’s input as $(S^u*1, S^u_2, \cdots, S^u*{
S^u - 1

## 3.2. Self-attenvive Recommenders 3.2. 自己アテンバイブ型レコメンダー

Owing to the ability of learning long sequences, Transformer architectures [43] have been widely used in sequential recommendation, like **SASRec** [26], BERT4Rec [41], and TiSASRec [30].
Transformerアーキテクチャ[43]は長いシーケンスを学習することができるため、逐次推薦において**SASRec** [26], BERT4Rec [41], TiSASRec [30] など広く利用されている。
Here we briefly introduce the design of SASRec and discuss its limitations.
ここでは、SASRecの設計を簡単に紹介し、その限界について考察する。

### 3.2.1. Embedding Layer 3.2.1. エンベデッドレイヤー

Transformer-based recommenders maintain an item embedding table $T \in R^{
I

$$
\hat{E} = E + P \tag{1}
$$

where $\hat{E}
ここで、$hat{E}
\in R^{n\times d}$ is an order-aware embedding, which can be directly fed to any Transformer-based models.
\in R^{n}times d}$ は順序を考慮した埋め込みで、Transformerベースのモデルに直接与えることができる。

### 3.2.2. Transformer Block 3.2.2. 変圧器ブロック

A Transformer block consists of a self-attention layer and a point-wise feed-forward layer.
Transformerブロックは、自己アテンション層とポイントワイズフィードフォワード層で構成されています。

**Self-attention Layer**:
**自己アテンション層**。
The key component of Transformer block is the self-attention layer that is highly efficient to uncover sequential dependencies in a sequence [43].
Transformerブロックのキーコンポーネントは、シーケンス中の順序依存性を発見するために非常に効率的である自己注意層である[43]。
The scaled dot-product attention is a popular attention kernel:
スケールドドットプロダクトアテンションは、一般的なアテンションカーネルである。

$$
\text{Attention}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d}}) V
\tag{2}
$$

where $\text{Attention}(Q, K, V) \in R^{n \times d}$ is the output item representations; $Q = \hat{E}W^Q$, $K =\hat{E}W^K$, and $V = \hat{E}W^V$ are the queries, keys and values, respectively; ${W^Q, W^K, W^V}
ここで、$text{Attention}(Q, K, V) \in R^{n \times d}$は出力項目表現、$Q = \hat{E}W^Q$, $K = \hat{E}W^K$, $V = \hat{E}W^V$ はそれぞれクエリー、キー、値、 ${W^Q, W^K, W^V} , は3つの射影変換行列であり、$θsqrt{time, tpm, tpm}$は注意の分布を柔らかくするスケールファクタである。
\in R^{d \times d}$ are three projection matrices; and $\sqrt{d}$ is the scale factor to produce a softer attention distribution.
\W^Q, W^K, W^V} は3つの射影行列、$sqrt{d}$ はより柔らかい注目分布を生成するためのスケールファクタである。
In sequential recommendation, one can utilize either left-to-right unidirectional attentions (e.g., SASRec [26] and TiSASRec [30]) or bidirectional attentions (e.g., BERT4Rec [41]) to predict the next item.
逐次推薦では、左から右への一方向の注目（例：SASRec [26], TiSASRec [30]）や双方向の注目（例：BERT4Rec [41] ）を用いて次の項目を予測することができる。
Moreover, one can apply H attention functions in parallel to enhance expressiveness: $H <- \text{MultiHead}(\hat{E})$ [43].
さらに、H個の注意関数を並列に適用して表現力を高めることもできます：$H <- \{MultiHead}(\hat{E})$ [43]。

**Point-wise Feed-forward Layer**:
**ポイント・ワイズ・フィードフォワード層**。
As the self attention layer is built on linear projections, we can endow the nonlinearity by introducing a point-wise feed-forward layers:
自己注意層は線形投射で構築されているので、ポイントワイズフィードフォワード層を導入することにより、非線形性を付与することが可能である。

$$
F_i = FFN(H_i) = \text{ReLU}(H_i W^{(1)} + b^{(1)})W^{(2)} + b^{(2)}
\tag{3}
$$

where $W^{(*)} \in R^{d \times d}$, $b^{(*)} \in R^d$ are the learnable weights and bias.
ここで、$W^{(*)} \in R^{d \times d}$, $b^{(*)} \in R^d$は学習可能な重みとバイアスである。

In practice, it is usually beneficial to learn hierarchical item dependencies by stacking more Transformer blocks.
実際には、より多くのTransformerブロックを積み重ねることによって、階層的な項目の依存関係を学習することが通常有益である。
Also, one can adopt the tricks of residual connection, dropout, and layer normalization for stabilizing and accelerating the training.
また、学習の安定化と高速化のために、残差接続、ドロップアウト、層正規化などのトリックを採用することができる。
Here we simply summarize the output of $L$ Transformer blocks as:
ここでは、$L$個のTransformerブロックの出力を単純に以下のようにまとめる。
$F^{(L)} <- \text{Transformer}(\hat{E})$.
F^{(L)} <- \text{Transformer}(\hat{E})$.

### 3.2.3. Learning Objective 3.2.3. 学習目標

After stacked $L$ Transformer blocks, one can predict the next item (given the first $t$ items) based on $F_t^{(L)}$.
L$個のTransformerブロックを積み重ねた後、$F_t^{(L)}$に基づいて、（最初の$t$個のアイテムがあれば）次のアイテムを予測することができる。
In this work, we use inner product to predict the relevance of item $i$ as:
本研究では、アイテム$i$の関連性を予測するために、内積を次のように使用する。

$$
r_{i, t} = <F_{t}^{(L)}, T_i>,
$$

where $T_i \in R^d$ is the embedding of item $i$.
ここで、$T_i \in R^d$ は項目$i$の埋め込みである。
Recall that the model inputs a sequence $s = (s_1, s_2, \cdots, s_n)$ and its desired output is a shifted version of the same sequence $o = (o_1, o_2, \cdots, o_n)$, we can adopt the binary cross-entropy loss as:
モデルは配列$s = (s_1, s_2, \cdots, s_n)$を入力し、その望ましい出力は同じ配列$o = (o_1, o_2, \cdots, o_n)$のシフト版であるとすると、2値クロスエントロピー損失として採用できることを想起してください。

$$
L_{BCE} = - \sum_{S^u \in S} \sum_{t=1}^{n}{[\log{\sigma(r_{o_t, t})} + \log{1 - \sigma (r_{o_t', t})}]} + a \cdot ||\theta||^2_F
\tag{4}
$$

where $\theta$ is the mode parameters, $a$ is the reqularizer to prevent over-fitting, $o'_t \notin S^u$ is a negative sample corresponding to $o_t$, and $\sigma(\cdot)$ is the sigmoid function.
ここで、$theta$はモードパラメータ、$a$はオーバーフィッティングを防ぐためのreqularizer、$o'_t \notin S^u$は$o_t$に対応する負のサンプル、$sigma( \cdot)$ はシグモイド関数である。

More details can be found in SASRec [26] and BERT4Rec [41].
詳細は、SASRec [26]とBERT4Rec [41]に記載されています。

## 3.3. The Noisy Attentions Problem 3.3. ノイジー・アテンション問題

Despite the success of SASRec and its variants, we argue that they are insufficient to address the noisy items in sequences.
SASRecとその変種の成功にもかかわらず、我々はシーケンス中のノイズの多いアイテムに対処するには不十分であると主張する。
The reason is that the full attention distributions (e.g., Eq. (2)) are dense and would assign certain credits to irrelevant items.
その理由は、完全な注目度分布（例えば、式（2））は密であり、無関係なアイテムに一定のクレジットを割り当ててしまうからである。
This complicates the item-item dependencies, increases the training difficulty, and even degrades the model performance.
これは、項目-項目依存関係を複雑にし、学習の難易度を上げ、さらにはモデルの性能を低下させる。
To address this issue, several attempts have been proposed to manually define sparse attention schemas in language modeling tasks [2, 10, 18, 58].
この問題に対処するため、言語モデリングタスクにおいて疎な注意スキーマを手動で定義する試みがいくつか提案されている[2, 10, 18, 58]。
However, these fixed sparse attentions cannot adapt to the input data [12], leading to sub-optimal performance.
しかし、これらの固定的な疎な注意は入力データに適応できず[12]、最適とは言えない性能になる。

On the other hand, several dropout techniques are specifically designed for Transformers to keep only a small portion of attentions, including LayerDrop [17], DropHead [60], and UniDrop [52].
一方、LayerDrop [17], DropHead [60], UniDrop [52]など、いくつかのドロップアウト技術は、Transformersが注目のごく一部だけを保持するように特別に設計されています。
Nevertheless, these randomly dropout approaches are susceptible to bias: the fact that attentions can be dropped randomly does not mean that the model allows them to be dropped, which may lead to over-aggressive pruning issues.
しかしながら、これらのランダムドロップアウトのアプローチはバイアスの影響を受けやすい：注意がランダムにドロップできるという事実は、モデルがそれらをドロップすることを許可していることを意味しないので、過度に攻撃的な刈り込みの問題につながる可能性がある。
In contrast, we propose a simple yet effective data-driven method to mask out irrelevant attentions by using differentiable masks.
これに対し、我々は微分可能なマスクを用いて無関係な注意をマスクする、シンプルかつ効果的なデータ駆動型の方法を提案する。

# 4. Rec-Denoiser 4. レックデノイザー

In this section, we present our Rec-Denoiser that consists of two parts: differentiable masks for self-attention layers and Jacobian regularization for Transformer blocks.
本節では、Rec-Denoiserを紹介する。Rec-Denoiserは、自己認識層に対する微分可能なマスクとTransformerブロックに対するヤコビアン正則化の2つの部分から構成されている。

## 4.1. Differentiable Masks 4.1. 微分可能なマスク

The self-attention layer is the cornerstone of Transformers to capture long-range dependencies.
自己アテンション層は長距離依存関係を捉えるためのTransformersの要である。
As shown in Eq. (2), the softmax operator assigns a non-zero weight to every item.
式(2)に示すように、ソフトマックス演算子は全ての項目に0でない重みを割り当てる。
However, full attention distributions may not always be advantageous since they may cause irrelevant dependencies, unnecessary computation, and unexpected explanation.
しかし、完全な注意分布は、無関係な依存関係、不必要な計算、予期せぬ説明を引き起こす可能性があるため、必ずしも有利とは言えない。
We next put forward differentiable masks to address this concern.
次に、この懸念に対処するため、微分可能なマスクを提唱する。

### 4.1.1. Learnable Sparse Attentions 4.1.1. 学習可能なスパースアテンション

Not every item in a sequence is aligned well with user preferences in the same sense that not all attentions are strictly needed in self-attention layers.
これは、自己アテンション層で全てのアテンションが厳密に必要とされるわけではないのと同じ意味である。
Therefore, we attach each self-attention layer with a trainable binary mask to prune noisy or task-irrelevant attentions.
そこで、各自己認識層に学習可能なバイナリマスクを付加し、ノイズやタスクと無関係な認識を排除する。
Formally, for the 𝑙-th self-attention layer in Eq. (2), we introduce a binary matrix $Z^{(l)} \in {0, 1}^{n\times n}$, where $Z^{(l)}_{u,v}$ denotes whether the connection between query $u$ and key $v$ is present.
ここで、$Z^{(l)}_{u,v}$はクエリ$u$とキー$v$の間の接続が存在するかどうかを表す。
As such, the $l$-th self-attention layer becomes:
このように、$l$番目の自己アテンション層は次のようになる。

$$
A^{(l)} = \text{softmax}(\frac{Q^{(l)} K^{(l)T}}{\sqrt{d}}),
\\
M^{(l)} = A^{(l)} \odot Z^{(l)},
\\
\text{Attention}(Q^{(l)}, K^{(l)}, V^{(l)}) = M^{(l)} V^{(l)},
\tag{5}
$$

where $A^{(l)}$ is the original full attentions, $M^{(l)}$ denotes the sparse attentions, and $\odot$ is the element-wise product.
ここで、$A^{(l)}$は元の完全注意、$M^{(l)}$は疎注意、$Θodot$は要素ワイズ積であることを表している。
Intuitively, the mask $Z^{(l)}$ (e.g., 1 is kept and 0 is dropped) requires minimal changes to the original self-attention layer.
直感的には、マスク$Z^{(l)}$（例えば、1を残し0を落とす）は、元の自己注意層に最小限の変更を加えるだけで済む。
More importantly, they are capable of yielding exactly zero attention scores for irrelevant dependencies, resulting in better interpretability.
さらに重要なことは、無関係な依存関係に対して正確にゼロの注意スコアをもたらすことができ、結果として解釈可能性が向上することである。
The idea of differentiable masks is not new.
微分可能なマスクの考え方は新しいものではない。
In the language modeling, differentiable masks have been shown to be very powerful to extract short yet sufficient sentences, which achieves better performance [1, 13].
言語モデリングにおいて、微分可能なマスクは、短いが十分な文章を抽出するのに非常に強力であることが示されており、より良い性能を達成している[1, 13]。

One way to encourage sparsity of $M^{(l)}$ is to explicitly penalize the number of non-zero entries of $Z^{(l)}$, for $1 \leq l \leq L$, by minimizing:
M^{(l)}$ のスパース性を促す方法の一つとして、$Z^{(l)}$ の0でないエントリーの数を、1 \l L$ に対して、明示的にペナルティとして、最小化する方法があります。

$$
R_M = \sum_{l=1}^{L}||Z^{l}||_{0}
= \sum_{l=1}^{L} \sum_{u=1}^{n} \sum_{v=1}^{n} I[Z_{u,v}^{(l)} \neq 0],
\tag{6}
$$

where $I[c]$ is an indicator that is equal to 1 if the condition $c$ holds and 0 otherwise; and $
|\cdot

However, there are two challenges for optimizing $Z^{(l)}$: non-differentiability and large variance.
しかし、$Z^{(l)}$を最適化するためには、非微分性と大きな分散の2つの課題がある。
$L_0$ is discontinuous and has zero derivatives almost everywhere.
L_0$は不連続であり、ほぼ全域でゼロ微分となる。
Additionally, there are $2^{n^2}$ possible states for the binary mask $Z^{(l)}$ with large variance.
さらに、バイナリマスク$Z^{(l)}$の可能な状態は$2^{n^2}$であり、分散が大きい。
Next, we propose an efficient estimator to solve this stochastic binary optimization problem.
次に、この確率的二値最適化問題を解くための効率的な推定器を提案する。

### 4.1.2. Efficient Gradient Computation 4.1.2. 効率的な勾配計算

$$
L(Z, \Theta) = L_{BCE}({A^{(l)} \odot Z^{(l)}}, \Theta) + \beta \cdot \sum_{l=1}^{L} \sum_{u=1}^{n} \sum_{v=1}^{n} I[Z_{u,v}^{(l)} \neq 0]
\tag{7}
$$

## 4.2. Jacobian Regularization 4.2. ヤコビアの正則化

## 4.3. Optimization 4.3. 最適化

### 4.3.1. Joint Training 4.3.1. 合同訓練

### 4.3.2. Model Complexity 4.3.2. モデルの複雑さ

# 5. Experiments 5. 実験

## 5.1. Experimental Setting 5.1. 実験設定

### 5.1.1. Dataset 5.1.1. データセット

### 5.1.2. Baselines 5.1.2. ベースライン

### 5.1.3. Evaluation metrics 5.1.3. 評価指標

### 5.1.4. Parameter settings 5.1.4. パラメータの設定

## 5.2. Overall Performance(RQ1) 5.2. 総合パフォーマンス(RQ1)

## 5.3. Robustness to Noises(RQ2) 5.3. ノイズに対するロバスト性(RQ2)

## 5.4. Study of Rec-Denoiser(RQ3) 5.4. Rec-Denoiserの研究(RQ3)

We further investigate the parameter sensitivity of Rec-Denoiser.
さらに、Rec-Denoiserのパラメータ感度を調査した。
For the number of blocks 𝐿 and the number of heads 𝐻, we find that self-attentive models typically benefit from small values (e.g., 𝐻, 𝐿 ≤ 4), which is similar to [31, 41].
ブロック数ᵃとヘッド数ᵃについて、自己注意型モデルは典型的に小さな値（例えば、ᵃ≤ 4）から恩恵を受けることがわかり、これは[31, 41]と同様である。
In this section, we mainly study the following hyper-parameters:
本節では、主に以下のハイパーパラメータについて検討する。

1. the maximum length 𝑛, 2) the regularizers 𝛽 and 𝛾 to control the sparsity and smoothness.
1. 最大長 𝑛, 2) 正則化 ǖ と 𝛾 で疎密と平滑性を制御する。
   Here we only study the SASRec and SASRec-Denoiser due to page limitations.
   ここでは、ページの制限からSASRecとSASRec-Denoiserについてのみ検討する。

Fig. 3.
図3.
Effect of maximum length 𝑛 on ranking performance (Hit@10).
最大長𝑛がランキング性能に与える影響（Hit@10）。

Fig. 4.
図 4.
Effect of regularizers 𝛽 and 𝛾 on ranking performance (Hit@10).
正則化 ǖ と ǖ がランキング性能に与える影響(Hit@10)。

### 5.4.1. Maximum Length $n$ 5.4.1. 最大長 $n$

Figure 3 shows the Hit@10 for maximum length 𝑛 from 20 to 80 while keeping other optimal hyper-parameters unchanged.
図3は、他の最適なハイパーパラメータを変更せず、最大長𝑛を20から80にした場合のHit@10を示したものです。
We only test on the densest and sparsest datasets:
最も高密度なデータセットと最も疎なデータセットでのみテストしています。
MovieLeans and Beauty.
MovieLeansとBeautyの2つのデータセットでテストしています。
Intuitively, the larger sequence we have, the larger probability that the sequence contains noisy items.
直感的には、シーケンスが大きければ大きいほど、シーケンスにノイズの多い項目が含まれる確率が高くなる。
FWe observed that our SASRec-Denoiser improves the performance dramatically with longer sequences.
その結果、我々のSASRec-Denoiserは長いシーケンスで劇的に性能が向上することが確認された。
This demonstrates that our design is more suitable for longer inputs, without worrying about the quality of sequences.
これは、我々の設計がシーケンスの品質を気にすることなく、より長い入力に適していることを示している。

### 5.4.2. The regularizers $\beta$ and $\gamma$ 5.4.2. 正則化変数$β$と$Θgamma$。

There are two major regularization parameters 𝛽 and 𝛾 for sparsity and gradient smoothness, respectively.
正則化パラメータには、スパース性と勾配平滑性のために、それぞれǖとᵯの2つがある。
Figure 4 shows the performance by changing one parameter while fixing the other as 0.01.
図4は、一方のパラメータを0.01に固定し、他方のパラメータを変化させた場合の性能を示している。
As can be seen, our performance is relatively stable with respect to different settings.
見てわかるように、我々の性能は異なる設定に対して比較的安定している。
In the experiments, the best performance can be achieved at 𝛽 = 0.01 and 𝛾 = 0.001 for the MovieLens dataset.
実験では，MovieLensデータセットにおいて，ǖ = 0.01 とǖ = 0.001 で最高の性能を達成することができる．

# 6. Conclusion and Fture Work 6. 結論とフューチャーワーク

In this work, we propose Rec-Denoiser to adaptively eliminate the negative impacts of the noisy items for self-attentive recommender systems.
本研究では、自己注視型推薦システムにおいて、ノイズの多いアイテムの悪影響を適応的に除去するRec-Denoiserを提案する。
The proposed Rec-Denoiser employs differentiable masks for the self-attention layers, which can dynamically prune irrelevant information.
提案するRec-Denoiserは、自己注視層に微分可能なマスクを用いることで、無関係な情報を動的に刈り取ることができる。
To further tackle the vulnerability of self-attention networks to small perturbations, Jacobian regularization is applied to the Transformer blocks to improve the robustness.
さらに、小さな摂動に対する自己注視ネットワークの脆弱性に対処するため、Transformerブロックにヤコビアン正則化を適用し、頑健性を向上させる。
Our experimental results on multiple real-world sequential recommendation tasks illustrate the effectiveness of our design.
実世界の複数の逐次推薦タスクに対する実験結果から、我々の設計の有効性が示される。

Our proposed Rec-Denoiser framework (e.g., differentiable masks and Jacobian regularization) can be easily applied to any Transformer-based models in many tasks besides sequential recommendation.
我々の提案するRec-Denoiserフレームワーク（微分可能なマスクやヤコビアン正則化など）は、逐次推薦以外の多くのタスクにおいて、Transformerベースのモデルに容易に適用することが可能である。
In the future, we will continue to demonstrate the contributions of our design in many real-world applications.
今後、多くの実世界のアプリケーションにおいて、我々の設計の貢献度を実証していく予定である。
