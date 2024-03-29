## 0.1. link 0.1.リンク

- https://dl.acm.org/doi/abs/10.1145/3523227.3546788 https://dl.acm.org/doi/abs/10.1145/3523227.3546788

- https://arxiv.org/pdf/2212.04120.pdf https://arxiv.org/pdf/2212.04120.pdf

## 0.2. title # 0.2.title

Denoising Self-Attentive Sequential Recommendation
デノイジング自己注意的逐次推薦

## 0.3. abstract # 0.3.abstract

Transformer-based sequential recommenders are very powerful for capturing both short-term and long-term sequential item dependencies.
トランスフォーマーに基づく逐次レコメンダーは、短期的および長期的な逐次アイテムの依存関係を捉えるのに非常に強力である。
This is mainly attributed to their unique self-attention networks to exploit pairwise item-item interactions within the sequence.
これは主に、シーケンス内のアイテムとアイテムの対の相互作用を利用する独自の自己注意ネットワークに起因する。
However, real-world item sequences are often noisy, which is particularly true for implicit feedback.
しかし、実世界の項目列はしばしばノイズが多く、特に暗黙的フィードバックに当てはまる。
For example, a large portion of clicks do not align well with user preferences, and many products end up with negative reviews or being returned.
例えば、クリックの大部分はユーザーの嗜好に合っておらず、多くの商品が否定的なレビューを受けたり、返品されたりしている。
As such, the current user action only depends on a subset of items, not on the entire sequences.
そのため、現在のユーザーアクションは、シーケンス全体ではなく、アイテムのサブセットにのみ依存する。
Many existing Transformer-based models use full attention distributions, which inevitably assign certain credits to irrelevant items.
既存のTransformerベースのモデルの多くは、完全な注意分布を使用しており、必然的に無関係な項目に一定のクレジットを割り当てる。
This may lead to sub-optimal performance if Transformers are not regularized properly.
これは、トランスフォーマーが適切に正則化されていない場合、最適なパフォーマンスを発揮できない可能性がある。

Here we propose the Rec-denoiser model for better training of self-attentive recommender systems.
ここでは、自己アテンション型推薦システムのより良い学習のために、Rec-denoiserモデルを提案する。
In Rec-denoiser, we aim to adaptively prune noisy items that are unrelated to the next item prediction.
Rec-denoiserでは、次のアイテムの予測に無関係なノイズの多いアイテムを適応的に除去することを目指している。
To achieve this, we simply attach each self-attention layer with a trainable binary mask to prune noisy attentions, resulting in sparse and clean attention distributions.
これを実現するために、各自己注意層に訓練可能なバイナリマスクを付けるだけで、ノイズの多い注意を除去し、その結果、まばらできれいな注意分布が得られる。
This largely purifies item-item dependencies and provides better model interpretability.
これにより、項目-項目間の依存関係がほとんどなくなり、モデルの解釈性が向上する。
In addition, the self-attention network is typically not Lipschitz continuous and is vulnerable to small perturbations.
さらに、自己注意ネットワークは一般的にリプシッツ連続ではなく、小さな摂動に弱い。
Jacobian regularization is further applied to the Transformer blocks to improve the robustness of Transformers for noisy sequences.
ヤコビアン正則化はさらに、ノイズの多いシーケンスに対するトランスフォーマーのロバスト性を向上させるために、トランスフォーマーブロックに適用される。
Our Rec-denoiser is a general plugin that is compatible to many Transformers.
私たちのRec-denoiserは、多くのトランスフォーマーと互換性のある一般的なプラグインです。
Quantitative results on real-world datasets show that our Rec-denoiser outperforms the state-of-the-art baselines.
実世界のデータセットにおける定量的な結果は、我々のRec-denoiserが最先端のベースラインを上回ることを示している。

# 1. introduction 1. イントロダクション

Sequential recommendation aims to recommend the next item based on a user’s historical actions [20, 35, 39, 44, 47], e.g., to recommend a bluetooth headphone after a user purchases a smart phone.
逐次レコメンデーションは、ユーザーの過去の行動に基づいて次のアイテムをレコメンドすることを目的としている[20, 35, 39, 44, 47]、例えば、ユーザーがスマートフォンを購入した後にブルートゥースヘッドフォンをレコメンドする。
Learning sequential user behaviors is, however, challenging since a user’s choices on items generally depend on both long-term and short-term preferences.
しかし、一般的にユーザーのアイテム選択は長期的嗜好と短期的嗜好の両方に依存するため、逐次的なユーザー行動の学習は困難である。
Early Markov Chain models [19, 39] have been proposed to capture short-term item transitions by assuming that a user’s next decision is derived from a few preceding actions, while neglecting long-term preferences.
初期のマルコフ連鎖モデル[19, 39]は、長期的な嗜好を無視する一方で、ユーザーの次の決定は先行するいくつかの行動から導き出されると仮定することで、短期的な項目の遷移を捕捉するために提案されてきた。
To alleviate this limitation, many deep neural networks have been proposed to model the entire users’ sequences and achieve great success, including recurrent neural networks [20, 53] and convolutional neural networks [42, 54, 57].
この制限を緩和するために、リカレントニューラルネットワーク[20, 53]や畳み込みニューラルネットワーク[42, 54, 57]など、ユーザーのシーケンス全体をモデル化する多くのディープニューラルネットワークが提案され、大きな成功を収めている。

Recently, Transformers have shown promising results in various tasks, such as machine translation [43].
最近、トランスフォーマーは、機械翻訳[43]などの様々なタスクで有望な結果を示している。
One key component of Transformers is the self-attention network, which is capable of learning long-range dependencies by computing attention weights between each pair of objects in a sequence.
トランスフォーマーの重要なコンポーネントのひとつが自己注意ネットワークであり、これはシーケンス内の各対オブジェクト間の注意重みを計算することによって、長距離依存関係を学習することができる。
Inspired by the success of Transformers, several self-attentive sequential recommenders have been proposed and achieve the state-of-the-art performance [26, 41, 49, 50].
Transformersの成功に触発されて、いくつかの自己注 意型逐次推薦器が提案されており、最先端の性能を達成している[26, 41, 49, 50]。
For example, SASRec [26] is the pioneering framework to adopt self-attention network to learn the importance of items at different positions.
例えば、SASRec [26]は、異なる位置にあるアイテムの重要度を学習するために自己注意ネットワークを採用した先駆的なフレームワークである。
BERT4Rec [41] further models the correlations of items from both left-to-right and right-to-left directions.
BERT4Rec [41]は、さらに左右両方向の項目の相関をモデル化している。
SSE-PT [50] is a personalized Transformer model that provides better interpretability of engagement patterns by introducing user embeddings.
SSE-PT [50]は、パーソナライズされたTransformerモデルであり、ユーザー埋め込みを導入することで、エンゲージメントパターンのより良い解釈可能性を提供する。
LSAN [31] adopts a novel twin-attention sequential framework, which can capture both long-term and short-term user preference signals.
LSAN[31]は、新しいツイン・アテンション・シーケンシャル・フレームワークを採用しており、長期的なユーザー嗜好信号と短期的なユーザー嗜好信号の両方を捉えることができる。
Recently, Transformers4Rec [14] performs an empirical analysis with broad experiments of various Transformer architectures for the task of sequential recommendation.
最近、Transformers4Rec [14]は、逐次推薦のタスクに対して、様々なTransformerアーキテクチャの広範な実験による実証的分析を行っている。

Although encouraging performance has been achieved, the robustness of sequential recommenders is far less studied in the literature.
有望な性能は達成されているが、逐次レコメンダーのロバスト性は文献上あまり研究されていない。
Many real-world item sequences are naturally noisy, containing both true-positive and false-positive interactions [6, 45, 46].
実世界のアイテム・シーケンスの多くは当然ノイズが多く、真陽性と偽陽性の両方の相互作用を含んでいる[6, 45, 46]。
For example, a large portion of clicks do not align well with user preferences, and many products end up with negative reviews or being returned.
例えば、クリックの大部分はユーザーの嗜好に合っておらず、多くの商品が否定的なレビューを受けたり、返品されたりしている。
In addition, there is no any prior knowledge about how a user’s historical actions should be generated in online systems.
さらに、オンラインシステムにおいて、ユーザーの過去の行動がどのように生成されるべきかについての予備知識はない。
Therefore, developing robust algorithms to defend noise is of great significance for sequential recommendation.
したがって、ノイズに強いアルゴリズムを開発することは、逐次推薦にとって大きな意義がある。

Clearly, not every item in a sequence is aligned well with user preferences, especially for implicit feedbacks (e.g., clicks, views, etc.) [8].
特に暗黙的なフィードバック（クリック、ビューなど）については、シーケンス内のすべての項目がユーザーの嗜好にうまく合致しているわけではないことは明らかである[8]。
Unfortunately, the vanilla self-attention network is not Lipschitz continuous1 , and is vulnerable to the quality of input sequences [28].
残念ながら、バニラ自己注意ネットワークはリプシッツ連続ではなく1、入力シーケンスの質に弱い[28]。
Recently, in the tasks of language modeling, people found that a large amount of BERT’s attentions focus on less meaningful tokens, like "[SEP]" and ".", which leads to a misleading explanation [11].
最近、言語モデリングのタスクにおいて、BERT の注意の多くが、"[SEP]"や". "のような、あまり意味のないトー クンに集中し、誤解を招く説明につながることが発見された[11]。
It is thus likely to obtain sub-optimal performance if self-attention networks are not well regularized for noisy sequences.
そのため、自己注意ネットワークがノイズの多いシーケンスに対してうまく正則化されていないと、最適なパフォーマンスが得られない可能性が高い。
We use the following example to further explain above concerns.
以下の例を用いて、上記の懸念をさらに説明する。

Figure 1 illustrates an example of left-to-right sequential recommendation where a user’s sequence contains some noisy or irrelevant items.
図1は左から右への逐次推薦の例を示しており、ユーザーのシーケンスにはノイズの多い項目や無関係な項目が含まれている。
For example, a father may interchangeably purchase (phone, headphone, laptop) for his son, and (bag, pant) for his daughter, resulting in a sequence: (phone, bag, headphone, pant, laptop).
例えば、父親が息子に（電話、ヘッドフォン、ノートパソコン）を、娘に（バッグ、ズボン）を交換購入し、その結果、（電話、バッグ、ヘッドフォン、ズボン、ノートパソコン）という順序になる。
In the setting of sequential recommendation, we intend to infer the next item, e.g., laptop, based on the user’s previous actions, e.g., (phone, bag, headphone, pant).
逐次推薦の設定では、ユーザーの以前の行動、例えば（携帯電話、バッグ、ヘッドフォン、ズボン）に基づき、次のアイテム、例えばノートパソコンを推測することを意図している。
However, the correlations among items are unclear, and intuitively pant and laptop are neither complementary nor compatible to each other, which makes the prediction untrustworthy.
しかし、項目間の相関関係は不明確であり、直感的にはパンとラップトップは互いに補完し合うものでも相容れるものでもないため、予測は信用できない。
A trustworthy model should be able to only capture correlated items while ignoring these irrelevant items within sequences.
信頼できるモデルは、シーケンス内の無関係な項目を無視して、相関のある項目だけを捉えることができるはずだ。
Existing self-attentive sequential models (e.g., SASRec [26] and BERT4Rec [41]) are insufficient to address noisy items within sequences.
既存の自己注意型逐次モデル（例えば、SASRec [26]やBERT4Rec [41]）は、シーケンス内のノイズの多い項目を扱うには不十分である。
The reason is that their full attention distributions are dense and would assign certain credits to all items, including irrelevant items.
というのも、彼らの全注意分布は密度が高く、無関係な項目を含むすべての項目に一定のクレジットを割り当ててしまうからだ。
This causes a lack of focus and makes models less interpretable [10, 58].
そのため焦点が定まらず、モデルの解釈性が低くなる [10, 58]。

To address the above issues, one straightforward strategy is to design sparse Transformer architectures that sparsify the connections in the attention layers, which have been actively investigated in language modeling tasks [10, 58].
上記の問題に対処するために、1つの簡単な戦略は、言語モデリングタスクで活発に研究されている[10, 58]、注意層の接続をスパースにするスパースTransformerアーキテクチャを設計することである。
Several representative models are Star Transformer [18], Sparse Transformer [10], Longformer [2], and BigBird [58].
代表的なモデルとして、Star Transformer [18]、Sparse Transformer [10]、Longformer [2]、BigBird [58]がある。
These sparse attention patterns could mitigate noisy issues and avoid allocating credits to unrelated contents for the query of interest.
このような疎なアテンションパターンは、ノイズの問題を軽減し、関心のあるクエリに無関係なコンテンツにクレジットを割り当てることを避けることができる。
However, these models largely rely on pre-defined attention schemas, which lacks flexibility and adaptability in practice.
しかし、これらのモデルの多くは、あらかじめ定義された注意スキーマに依存しているため、実際には柔軟性や適応性に欠ける。
Unlike end-to-end training approaches, whether these sparse patterns could generalize well to sequential recommendation remains unknown and is still an open research question.
エンド・ツー・エンドの学習アプローチとは異なり、このような疎なパターンが逐次推薦にうまく一般化できるかどうかは未知であり、まだ未解決の研究課題である。

Fig.1.An illustrative example of sequential recommendation where a sequence contains noisy or irrelevant items in left-to-right self-attention networks.
図1.左から右への自己注意ネットワークにおける、ノイズや無関係な項目を含むシーケンシャル推薦の例。

Contributions.
貢献だ。
In this work, we propose to design a denoising strategy, Rec-Denoiser, for better training of selfattentive sequential recommenders.
本研究では、Rec-Denoiserと呼ばれるノイズ除去戦略を提案する。
Our idea stems from the recent findings that not all attentions are necessary and simply pruning redundant attentions could further improve the performance [10, 12, 40, 55, 58].
私たちのアイデアは、すべての注意が必要なわけではなく、冗長な注意を刈り込むだけでパフォーマンスをさらに向上させることができるという最近の知見に由来する[10, 12, 40, 55, 58]。
Rather than randomly dropping out attentions, we introduce differentiable masks to drop task-irrelevant attentions in the self-attention layers, which can yield exactly zero attention scores for noisy items.
ランダムに注意を取り除くのではなく、微分可能なマスクを導入し、タスクに無関係な注意を自己注意層で取り除くことで、ノイズの多いアイテムの注意スコアを正確にゼロにすることができる。
The introduced sparsity in the self-attention layers has several benefits: 1) Irrelevant attentions with parameterized masks can be learned to be dropped in a data-driven way.
自己注意層に導入されたスパース性にはいくつかの利点がある： 1) パラメータ化されたマスクを持つ無関係な注意は、データ駆動型の方法で削除するように学習できる。
Taking Figure 1 as an example, our Rec-denoiser would prune the sequence (phone, bag, headphone) for pant, and (phone, bag, headphone, pant) for laptop in the attention maps.
図1を例にとると、Rec-denoiserはアテンション・マップの中で、(電話、バッグ、ヘッドフォン)をパンツに、(電話、バッグ、ヘッドフォン、パンツ)をラップトップにプルーンする。
Namely, we seek next item prediction explicitly based on a subset of more informative items.2) Our Rec-Denoiser still takes full advantage of Transformers as it does not change their architectures, but only the attention distributions.
2）我々のRec-Denoiserは、Transformerのアーキテクチャを変更せず、注目度分布のみを変更するため、Transformerの利点を最大限に活用している。
As such, Rec-Denoiser is easy to implement and is compatible to any Transformers, making them less complicated as well as improving their interpretability.
このように、Rec-Denoiserは実装が簡単で、どのようなトランスフォーマーとも互換性があるため、複雑さが軽減され、解釈可能性も向上する。

In our proposed Rec-Denoiser, there are two major challenges.
私たちが提案するRec-Denoiserには、2つの大きな課題がある。
First, the discreteness of binary masks (i.e., 0 is dropped while 1 is kept) is, however, intractable in the back-propagation.
第一に、2値マスクの離散性（すなわち、0は削除され、1は維持される）は、しかし、バックプロパゲーションでは実行不可能である。
To remedy this issue, we relax the discrete variables with a continuous approximation through probabilistic reparameterization [25].
この問題を解決するために、確率的再パラメータ化[25]によって離散変数を連続近似で緩和する。
As such, our differentiable masks can be trained jointly with original Transformers in an end-to-end fashion.
このように、我々の微分可能なマスクは、エンド・ツー・エンド方式でオリジナルのトランスフォーマーと共同で学習することができる。
In addition, the scaled dot-product attention is not Lipschitz continuous and is thus vulnerable to input perturbations [28].
さらに、スケーリングされたドットプロダクトアテンションはリプシッツ連続ではないため、入力摂動の影響を受けやすい[28]。
In this work, Jacobian regularization [21, 24] is further applied to the entire Transformer blocks, to improve the robustness of Transformers for noisy sequences.
この研究では、ノイズの多いシーケンスに対するトランスフォーマーのロバスト性を向上させるために、ヤコビアン正則化[21, 24]をトランスフォーマーブロック全体にさらに適用する。
Experimental results on real-world benchmark datasets demonstrate the effectiveness and robustness of the proposed Rec-Denoiser.
実世界のベンチマークデータセットを用いた実験結果は、提案するRec-Denoiserの有効性と頑健性を実証している。
In summary, our contributions are:
まとめると、我々の貢献は以下の通りである：

- We introduce the idea of denoising item sequences for better of training self-attentive sequential recommenders, which greatly reduces the negative impacts of noisy items. 我々は、自己注意的な逐次レコメンダーを学習するために、項目列をノイズ除去するというアイデアを導入し、ノイズの多い項目の悪影響を大幅に軽減する。

- We present a general Rec-Denoiser framework with differentiable masks that can achieve sparse attentions by dynamically pruning irrelevant information, leading to better model performance. 我々は、微分可能なマスクを持つ一般的なRec-Denoiserフレームワークを提示する。このフレームワークは、無関係な情報を動的に刈り込むことによって疎な注意力を実現し、より優れたモデル性能をもたらす。

- We propose an unbiased gradient estimator to optimize the binary masks, and apply Jacobian regularization on the gradients of Transformer blocks to further improve its robustness. 我々は、バイナリマスクを最適化するための不偏勾配推定器を提案し、Transformerブロックの勾配にヤコビアン正則化を適用して、そのロバスト性をさらに向上させる。

- The experimental results demonstrate significant improvements that Rec-Denoiser brings to self-attentive recommenders (5.05% ∼ 19.55% performance gains), as well as its robustness against input perturbations. 実験結果は、Rec-Denoiserが自己注視型レコメンダーにもたらす大幅な改善（5.05%〜19.55%の性能向上）と、入力摂動に対する頑健性を示している。

# 2. Related Work 2. 関連作品

In this section, we briefly review the related work on sequential recommendation and sparse Transformers.
このセクションでは、逐次推薦とスパース変換器に関する関連研究を簡単にレビューする。
We also highlight the differences between the existing efforts and ours.
また、既存の取り組みと我々の取り組みとの違いも強調する。

## 2.1. Sequential Recommendation 

Leveraging sequences of user-item interactions is crucial for sequential recommendation.
ユーザーとアイテムのインタラクションのシーケンスを活用することは、逐次レコメンデーションにとって極めて重要である。
User dynamics can be caught by Markov Chains for inferring the conditional probability of an item based on the previous items [19, 39].
ユーザダイナミクスは、前の項目に基づいて項目の条件付き確率を推論するためのマルコフ連鎖によって捕らえることができる[19, 39]。
More recently, growing efforts have been dedicated to deploying deep neural networks for sequential recommendation such as recurrent neural networks [20, 53], convolutional neural networks [42, 54, 57], memory networks [9, 22], and graph neural networks [4, 7, 51].
最近では、リカレントニューラルネットワーク[20, 53]、畳み込みニューラルネットワーク[42, 54, 57]、メモリネットワーク[9, 22]、グラフニューラルネットワーク[4, 7, 51]など、逐次推薦のためのディープニューラルネットワークの導入に向けた取り組みが活発化している。
For example, GRU4Rec [20] employs a gated recurrent unit to study temporal behaviors of users.
例えば、GRU4Rec [20]は、ゲーテッド・リカレント・ユニットを用いて、ユーザーの時間的行動を研究している。
Caser [42] learns sequential patterns by using convolutional filters on local sequences.
Caser[42]は、局所的なシーケンスに対して畳み込みフィルタを使用することで、シーケンシャルパターンを学習する。
MANN [9] adopts memory-augmented neural networks to model user historical records.
MANN [9]は、ユーザーの履歴記録をモデル化するために、記憶増強ニューラルネットワークを採用している。
SR-GNN [51] converts session sequences into graphs and uses graph neural networks to capture complex item-item transitions.
SR-GNN[51]はセッションシーケンスをグラフに変換し、複雑なアイテム-アイテムの遷移をキャプチャするためにグラフニューラルネットワークを使用する。

Transformer-based models have shown promising potential in sequential recommendation [5, 26, 30, 32, 33, 41, 49, 50], due to their ability of modeling arbitrary dependencies in a sequence.
トランスフォーマーベースのモデルは、シーケンスの任意の依存関係をモデル化できるため、逐次推薦において有望な可能性を示している[5, 26, 30, 32, 33, 41, 49, 50]。
For example, SASRec [26] first adopts self-attention network to learn the importance of items at different positions.
例えば、SASRec [26]は、異なる位置にあるアイテムの重要度を学習するために、まず自己注意ネットワークを採用している。
In the follow-up studies, several Transformer variants have been designed for different scenarios by adding bidirectional attentions [41], time intervals [30], personalization [50], importance sampling [32], and sequence augmentation [33].
フォローアップ研究では、双方向注意[41]、時間間隔[30]、パーソナライゼーション[50]、重要度サンプリング[32]、シーケンス拡張[33]を追加することで、さまざまなシナリオ用にいくつかのTransformerの亜種が設計されている。
However, very few studies pay attention to the robustness of self-attentive recommender models.
しかし、自己注視型レコメンダーモデルの頑健性に注目した研究は非常に少ない。
Typically, users’ sequences contain lots of irrelevant items since they may subsequently purchase a series of products with different purposes [45].
通常、ユーザーのシーケンスには無関係なアイテムが多く含まれる。なぜなら、ユーザーはその後、異なる目的で一連の製品を購入する可能性があるからだ[45]。
As such, the current user action only depends on a subset of items, not on the entire sequences.
そのため、現在のユーザーアクションは、シーケンス全体ではなく、アイテムのサブセットにのみ依存する。
However, the self-attention module is known to be sensitive to noisy sequences [28], which may lead to sub-optimal generalization performance.
しかし、自己注意モジュールはノイズの多いシーケンスに敏感であることが知られており[28]、最適な汎化性能が得られない可能性がある。
In this paper, we aim to reap the benefits of Transformers while denoising the noisy item sequences by using learnable masks in an end-to-end fashion.
本論文では、学習可能なマスクをエンド・ツー・エンドで使用することにより、ノイズの多いアイテム列をノイズ除去しながら、トランスフォーマーの利点を享受することを目指す。

## 2.2. Sparce Transformer 

Recently, many lightweight Transformers seek to achieve sparse attention maps since not all attentions carry important information in the self-attention layers [2, 10, 18, 29, 58].
最近、多くの軽量トランスフォーマーは、すべての注意が自己注意層に重要な情報を持っているわけではないので、疎な注意マップを実現しようとしている[2, 10, 18, 29, 58]。
For instance, Reformer [29] computes attentions based on locality-sensitive hashing, leading to lower memory consumption.
例えば、Reformer [29]は、局所性を考慮したハッシュに基づいて注目度を計算するため、メモリ消費量が少なくて済む。
Star Transformer [18] replaces the fully-connected structure of self-attention with a star-shape topology.
Star Transformer [18]は、自己アテンションの完全連結構造を星形トポロジーに置き換えたものである。
Sparse Transformer [10] and Longformer [2] achieve sparsity by using various sparse patterns, such as diagonal sliding windows, dilated sliding windows, local and global sliding windows.
Sparse Transformer [10]とLongformer [2]は、対角スライディング・ウィンドウ、拡張スライディング・ウィンドウ、ローカル・スライディング・ウィンドウ、グローバル・スライディング・ウィンドウなど、さまざまなスパース・パターンを使用してスパース性を実現する。
BigBird [58] uses random and several fixed patterns to build sparse blocks.
BigBird [58]は、ランダムといくつかの固定パターンを使ってスパースブロックを構築する。
It has been shown that these sparse attentions can obtain the state-of-the-art performance and greatly reduce computational complexity.
このようなスパースアテンションは、最先端の性能を得ることができ、計算量を大幅に削減できることが示されている。
However, many of them rely on fixed attention schemas that lack flexibility and require tremendous engineering efforts.
しかし、その多くは柔軟性に欠け、多大なエンジニアリング努力を必要とする固定的なアテンションスキーマに依存している。

Another line of work is to use learnable attention distributions [12, 36, 38, 40].
もうひとつの研究は、学習可能な注意分布 [12, 36, 38, 40] を使うことである。
Mostly, they calculate attention weights with variants of sparsemax that replaces the softmax normalization in the self-attention networks.
ほとんどの場合、彼らは自己注意ネットワークのソフトマックス正規化に代わるスパースマックスの変種を使って注意の重みを計算している。
This allows to produce both sparse and bounded attentions, yielding a compact and interpretable set of alignments.
これにより、スパースと境界のある注意の両方を生成することができ、コンパクトで解釈可能なアラインメントのセットを得ることができる。
Our Rec-denoiser is related to this line of work.
私たちのRec-denoiserはこの仕事に関連している。
Instead of using sparsemax, we design a trainable binary mask for the self-attention network.
sparsemaxを使う代わりに、自己注意ネットワーク用に訓練可能なバイナリマスクを設計する。
As a result, our proposed Rec-denoiser can automatically determine which self-attention connections should be deleted or kept in a data-driven way.
その結果、我々の提案するRec-denoiserは、データ駆動型の方法で、どの自己アテンション・コネクションを削除すべきか、あるいは残すべきかを自動的に決定することができる。

# 3. Problem and Background 3. 問題と背景

In this section, we first formulate the problem of sequential recommendation, and then revisit several self-attentive models.
このセクションでは、まず逐次推薦の問題を定式化し、次にいくつかの自己注意モデルを再検討する。
We further discuss the limitations of the existing work.
さらに、既存の研究の限界についても述べる。

## 3.1. Problem Setup 

In sequential recommendation, let $U$ be a set of users, $I$ a set of items, and $S = {S^1, S^2,\cdots, S^{|U|}}$ a set of users' actions.
U

We user $S^u = (S^u_1, S^u_2, \cdots, S^u_{|S^u|})$ to denote a sequence of items for user $u \in U$ in a chronological order, where $S^u_t \in I$ is the item that user $u$ has interacted with at time $t$, and $|S^u|$ is the length of sequence.
S^u|})$ to denote a sequence of items for user $u \in U$ in a chronological order, where $S^u_t \in I$ is the item that user $u$ has interacted with at time $t$, and $

Given the interaction history $S^u$, sequential recommendation seeks to predict the next item $S^u_{S^u+1}$ at time step $|S^u+1|$.
S^u+1

During the training process [26, 41], it will be convenient to regard the model’s input as $(S^u_1, S^u_2, \cdots, S^u_{|S^u - 1|})$ and its expected output is a shifted version of the input sequence: $(S^u_2, S^u_3, \cdots, S^u_{|S^u|})$.
S^u - 1

## 3.2. Self-attenvive Recommenders 3.2.自己アテンバイブ・レコメンダー

Owing to the ability of learning long sequences, Transformer architectures [43] have been widely used in sequential recommendation, like **SASRec** [26], BERT4Rec [41], and TiSASRec [30].
Transformerアーキテクチャ[43]は、長いシーケンスを学習することができるため、**SASRec** [26]、BERT4Rec [41]、TiSASRec [30]のように、逐次推薦に広く使用されている。
Here we briefly introduce the design of SASRec and discuss its limitations.
ここでは、SASRecの設計を簡単に紹介し、その限界について述べる。

### 3.2.1. Embedding Layer 3.2.1. 埋め込みレイヤー

Transformer-based recommenders maintain an item embedding table $T \in R^{|I| \times d}$ , where 𝑑 is the size of the embedding.
I
For each sequence $(S^u_1, S^u_2, \cdots, S^u_{|S^u - 1|})$, it can be converted into a fixed-length sequence $(s_1, s_2, \cdots s_n)$, where $n$ is the maximum length (e.g., keeping the most recent 𝑛 items by truncating or padding items).
S^u - 1|})$, it can be converted into a fixed-length sequence $(s_1, s_2, \cdots s_n)$, where $n$ is the maximum length (e.g., keeping the most recent 𝑛 items by truncating or padding items).
The embedding for $(s_1, s_2, \cdots s_n)$ is denoted as $E \in R^{n \times d}$ , which can be retrieved from the table $T$.
(s_1, s_2, ⊖cdots s_n)$ の埋め込みを $E ⊖in R^{n ⊖times d}$ と表し、表 $T$ から取り出すことができる。
To capture the impacts of different positions, one can inject a learnable positional embedding $P \in R^{n \times d}$ into the input embedding as:
異なる位置の影響を捉えるために、学習可能な位置埋め込み $P \in R^{n ౪times d}$ を入力埋め込みに注入することができる：

$$
\hat{E} = E + P \tag{1}
$$

where $\hat{E} \in R^{n\times d}$ is an order-aware embedding, which can be directly fed to any Transformer-based models.
ここで、$hat{E}は \in R^{ntimes d}$ は順序を意識した埋め込みで、Transformerベースのモデルに直接与えることができる。

### 3.2.2. Transformer Block 3.2.2. 変圧器ブロック

A Transformer block consists of a self-attention layer and a point-wise feed-forward layer.
トランスフォーマー・ブロックは、セルフ・アテンション・レイヤーとポイント・ワイズ・フィードフォワード・レイヤーで構成される。

**Self-attention Layer**: The key component of Transformer block is the self-attention layer that is highly efficient to uncover sequential dependencies in a sequence [43].
**自己注意層**： Transformerブロックの重要なコンポーネントは、シーケンスの逐次的な依存関係を明らかにするために非常に効率的である自己注意層である[43]。
The scaled dot-product attention is a popular attention kernel:
スケールド・ドット・プロダクト・アテンションは一般的なアテンション・カーネルである：

$$
\text{Attention}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d}}) V
\tag{2}
$$

where $\text{Attention}(Q, K, V) \in R^{n \times d}$ is the output item representations; $Q = \hat{E}W^Q$, $K =\hat{E}W^K$, and $V = \hat{E}W^V$ are the queries, keys and values, respectively; ${W^Q, W^K, W^V} \in R^{d \times d}$ are three projection matrices; and $\sqrt{d}$ is the scale factor to produce a softer attention distribution.
ここで、$text{Attention}(Q, K, V)  \in R^{n ¶times d}$は出力項目表現であり、$Q = ¶hat{E}W^Q$, $K = ¶hat{E}W^K$, $V = ¶hat{E}W^V$ はそれぞれクエリ、キー、値であり、${W^Q, W^K, W^V}は3つの射影行列である。\in R^{d }$ は3つの射影行列、$sqrt{d}$ はより柔らかい注意分布を生成するためのスケールファクタである。
In sequential recommendation, one can utilize either left-to-right unidirectional attentions (e.g., SASRec [26] and TiSASRec [30]) or bidirectional attentions (e.g., BERT4Rec [41]) to predict the next item.
逐次推薦では、左から右への一方向注意（例えば、SASRec [26]やTiSASRec [30]）または双方向注意（例えば、BERT4Rec [41]）を利用して、次のアイテムを予測することができる。
Moreover, one can apply H attention functions in parallel to enhance expressiveness: $H <- \text{MultiHead}(\hat{E})$ [43].
さらに、H注意関数を並列に適用することで、表現力を高めることができる：$H <- \text{MultiHead}(E})$ [43]。

**Point-wise Feed-forward Layer**: As the self attention layer is built on linear projections, we can endow the nonlinearity by introducing a point-wise feed-forward layers:
**ポイント・ワイズ・フィードフォワード層**： 自己注意層は線形投影で構築されているので、ポイントワイズ・フィードフォワード層を導入することで、非線形性を付与することができる：

$$
F_i = FFN(H_i) = \text{ReLU}(H_i W^{(1)} + b^{(1)})W^{(2)} + b^{(2)}
\tag{3}
$$

where $W^{(*)} \in R^{d \times d}$, $b^{(*)} \in R^d$ are the learnable weights and bias.
ここで、$W^{(*)} \in R^{d }$, $b^{(*)} \in R^d$ は学習可能な重みとバイアスである。

In practice, it is usually beneficial to learn hierarchical item dependencies by stacking more Transformer blocks.
実際には、より多くのTransformerブロックを積み重ねることによって、階層的なアイテムの依存関係を学習することが通常有益である。
Also, one can adopt the tricks of residual connection, dropout, and layer normalization for stabilizing and accelerating the training.
また、残差接続、ドロップアウト、レイヤー正規化などのトリックを採用することで、学習の安定化と高速化を図ることができる。
Here we simply summarize the output of $L$ Transformer blocks as: $F^{(L)} <- \text{Transformer}(\hat{E})$.
ここでは、$L$Transformerブロックの出力を単純に次のようにまとめる： F^{(L)} <- \text{Transformer}(E})$.

### 3.2.3. Learning Objective 3.2.3. 学習目標

After stacked $L$ Transformer blocks, one can predict the next item (given the first $t$ items) based on $F_t^{(L)}$.
L$個のTransformerブロックを積み重ねた後、$F_t^{(L)}$に基づいて（最初の$t$個の項目があれば）次の項目を予測できる。
In this work, we use inner product to predict the relevance of item $i$ as:
この研究では、内積を使って項目$i$の関連性を次のように予測する：

$$
r_{i, t} = <F_{t}^{(L)}, T_i>,
$$

where $T_i \in R^d$ is the embedding of item $i$.
ここで $T_i \in R^d$ は項目 $i$ の埋め込みである。
Recall that the model inputs a sequence $s = (s_1, s_2, \cdots, s_n)$ and its desired output is a shifted version of the same sequence $o = (o_1, o_2, \cdots, o_n)$, we can adopt the binary cross-entropy loss as:
モデルはシーケンス$s = (s_1, s_2, ˶cdots, s_n)$を入力し、その出力は同じシーケンス$o = (o_1, o_2, ˶cdots, o_n)$をシフトしたものである：

$$
L_{BCE} = - \sum_{S^u \in S} \sum_{t=1}^{n}{[\log{\sigma(r_{o_t, t})} + \log{1 - \sigma (r_{o_t', t})}]} + a \cdot ||\theta||^2_F
\tag{4}
$$

where $\theta$ is the mode parameters, $a$ is the reqularizer to prevent over-fitting, $o'_t \notin S^u$ is a negative sample corresponding to $o_t$, and $\sigma(\cdot)$ is the sigmoid function.
ここで、$theta$はモードパラメータ、$a$はオーバーフィットを防ぐためのreqularizer、$o'_t \notin S^u$は$o_t$に対応する負のサンプル、$sigma( \cdot)$はシグモイド関数である。

More details can be found in SASRec [26] and BERT4Rec [41].
詳細は、SASRec[26]およびBERT4Rec[41]に記載されている。

## 3.3. The Noisy Attentions Problem 

Despite the success of SASRec and its variants, we argue that they are insufficient to address the noisy items in sequences.
SASRecとその亜種の成功にもかかわらず、シーケンス中のノイズの多い項目に対処するには不十分であると我々は主張する。
The reason is that the full attention distributions (e.g., Eq.(2)) are dense and would assign certain credits to irrelevant items.
その理由は、完全な注目度分布（例えば式(2)）は密度が高く、無関係な項目に一定のクレジットを割り当ててしまうからである。
This complicates the item-item dependencies, increases the training difficulty, and even degrades the model performance.
これは項目-項目の依存関係を複雑にし、トレーニングの難易度を上げ、さらにはモデルの性能を低下させる。
To address this issue, several attempts have been proposed to manually define sparse attention schemas in language modeling tasks [2, 10, 18, 58].
この問題に対処するため、言語モデリングタスクでスパース注意スキーマを手動で定義する試みがいくつか提案されている[2, 10, 18, 58]。
However, these fixed sparse attentions cannot adapt to the input data [12], leading to sub-optimal performance.
しかし、このような固定的なスパース・アテンションは、入力データに適応することができず[12]、最適なパフォーマンスとは言えない。

On the other hand, several dropout techniques are specifically designed for Transformers to keep only a small portion of attentions, including LayerDrop [17], DropHead [60], and UniDrop [52].
一方、LayerDrop[17]、DropHead[60]、UniDrop[52]など、トランスフォーマーのために特別に設計された、注目のごく一部だけを残すドロップアウト技術がいくつかある。
Nevertheless, these randomly dropout approaches are susceptible to bias: the fact that attentions can be dropped randomly does not mean that the model allows them to be dropped, which may lead to over-aggressive pruning issues.
とはいえ、このようなランダムに脱落させるアプローチは、バイアスの影響を受けやすい。注意がランダムに脱落させられるという事実は、モデルが脱落を許容していることを意味しないので、過度に攻撃的な刈り込みの問題につながる可能性がある。
In contrast, we propose a simple yet effective data-driven method to mask out irrelevant attentions by using differentiable masks.
これに対して我々は、微分可能なマスクを用いて無関係な注意をマスクする、シンプルかつ効果的なデータ駆動法を提案する。

# 4. Rec-Denoiser 4. レク・デノイザー

In this section, we present our Rec-Denoiser that consists of two parts: differentiable masks for self-attention layers and Jacobian regularization for Transformer blocks.
このセクションでは、Rec-Denoiserを紹介する。Rec-Denoiserは、自己注意層のための微分可能なマスクと、Transformerブロックのためのヤコビアン正則化の2つの部分から構成される。

## 4.1. Differentiable Masks 

The self-attention layer is the cornerstone of Transformers to capture long-range dependencies.
セルフ・アテンション・レイヤーは、長距離の依存関係を捉えるトランスフォーマーの要である。
As shown in Eq.(2), the softmax operator assigns a non-zero weight to every item.
式(2)に示すように、ソフトマックス演算子はすべての項目に0でない重みを割り当てる。
However, full attention distributions may not always be advantageous since they may cause irrelevant dependencies, unnecessary computation, and unexpected explanation.
しかし、完全な注目度分布は、無関係な依存関係、不必要な計算、予期せぬ説明を引き起こす可能性があるため、必ずしも有利とは限らない。
We next put forward differentiable masks to address this concern.
次に、この懸念に対処するために、微分可能なマスクを提案する。

### 4.1.1. Learnable Sparse Attentions 4.1.1. 学習可能なスパース・アテンション

Not every item in a sequence is aligned well with user preferences in the same sense that not all attentions are strictly needed in self-attention layers.
セルフ・アテンション・レイヤーにおいて、すべてのアテンションが厳密に必要とされるわけではないのと同じ意味で、シーケンス内のすべてのアイテムがユーザーの嗜好にうまく合致しているわけではない。
Therefore, we attach each self-attention layer with a trainable binary mask to prune noisy or task-irrelevant attentions.
そこで、各自己注意層に学習可能なバイナリ・マスクを付加し、ノイズの多い注意やタスクと無関係な注意を除去する。
Formally, for the 𝑙-th self-attention layer in Eq.(2), we introduce a binary matrix $Z^{(l)} \in {0, 1}^{n\times n}$, where $Z^{(l)}_{u,v}$ denotes whether the connection between query $u$ and key $v$ is present.
ここで、$Z^{(l)}_{u,v}$はクエリ$u$とキー$v$の接続の有無を表す。
As such, the $l$-th self-attention layer becomes:
このように、$l$番目の自己注意層は次のようになる：

$$
A^{(l)} = \text{softmax}(\frac{Q^{(l)} K^{(l)T}}{\sqrt{d}}),
\\
M^{(l)} = A^{(l)} \odot Z^{(l)},
\\
\text{Attention}(Q^{(l)}, K^{(l)}, V^{(l)}) = M^{(l)} V^{(l)},
\tag{5}
$$

where $A^{(l)}$ is the original full attentions, $M^{(l)}$ denotes the sparse attentions, and $\odot$ is the element-wise product.
ここで、$A^{(l)}$は元の完全注目度、$M^{(l)}$は疎注目度、$modot$は要素ごとの積である。
Intuitively, the mask $Z^{(l)}$ (e.g., 1 is kept and 0 is dropped) requires minimal changes to the original self-attention layer.
直感的には、マスク$Z^{(l)}$（例えば、1を残して0を落とす）は、元の自己注意層に最小限の変更を加えるだけで済む。
More importantly, they are capable of yielding exactly zero attention scores for irrelevant dependencies, resulting in better interpretability.
さらに重要なのは、無関係な依存関係に対して注意スコアを正確にゼロにすることができるため、解釈しやすくなるということだ。
The idea of differentiable masks is not new.
微分可能なマスクというアイデアは新しいものではない。
In the language modeling, differentiable masks have been shown to be very powerful to extract short yet sufficient sentences, which achieves better performance [1, 13].
言語モデリングにおいて、微分可能なマスクは、短くても十分なセンテンスを抽出するのに非常に強力であり、より良いパフォーマンスを達成することが示されている[1, 13]。

One way to encourage sparsity of $M^{(l)}$ is to explicitly penalize the number of non-zero entries of $Z^{(l)}$, for $1 \leq l \leq L$, by minimizing:
M^{(l)}$のスパース性を奨励する一つの方法は、$Z^{(l)}$のゼロでないエントリーの数を、$1 ￢l ￢L$に対して、最小化することで明示的にペナルティを課すことである：

$$
R_M = \sum_{l=1}^{L}||Z^{l}||_{0}
= \sum_{l=1}^{L} \sum_{u=1}^{n} \sum_{v=1}^{n} I[Z_{u,v}^{(l)} \neq 0],
\tag{6}
$$

where $I[c]$ is an indicator that is equal to 1 if the condition $c$ holds and 0 otherwise; and $||\cdot||_{0}$ denotes the $L_0$ norm that is able to drive irrelevant attentions to be exact zeros.
|\cdot

However, there are two challenges for optimizing $Z^{(l)}$: non-differentiability and large variance.
しかし、$Z^{(l)}$の最適化には、微分不可能性と分散の大きさという2つの課題がある。
$L_0$ is discontinuous and has zero derivatives almost everywhere.
L_0$は不連続であり、ほとんどどこでもゼロ導関数を持つ。
Additionally, there are $2^{n^2}$ possible states for the binary mask $Z^{(l)}$ with large variance.
さらに、2値マスク$Z^{(l)}$には大きな分散を持つ$2^{n^2}$個の可能な状態がある。
Next, we propose an efficient estimator to solve this stochastic binary optimization problem.
次に、この確率的二元最適化問題を解くための効率的な推定器を提案する。

### 4.1.2. Efficient Gradient Computation 4.1.2. 効率的な勾配計算

Since Z (𝑙) is jointly optimized with the original Transformer-based models, we combine Eq.(4) and Eq.(6) into one unified objective:
Z (↪Ll_1459) はオリジナルのTransformerベースのモデルと共同で最適化されるので、式(4)と式(6)を1つの統一された目的にまとめる：

$$
L(Z, \Theta) = L_{BCE}({A^{(l)} \odot Z^{(l)}}, \Theta) + \beta \cdot \sum_{l=1}^{L} \sum_{u=1}^{n} \sum_{v=1}^{n} I[Z_{u,v}^{(l)} \neq 0]
\tag{7}
$$

where 𝛽 controls the sparsity of masks and we denote Z as Z := {Z (1) , · · · , Z (𝐿) }.
ここで ↪L_1FD はマスクのスパース性を制御し、Z を Z := {Z (1) , - - , Z (↪Lu_1D43F) } とする。
We further consider each Z (𝑙) 𝑢,𝑣 is drawn from a Bernoulli distribution parameterized by Π (𝑙) 𝑢,𝑣 such that Z (𝑙) 𝑢,𝑣 ∼ Bern(Π (𝑙) 𝑢,𝑣 ) [34].
さらに、Z (𝑙) ∼ Bern(Π (𝑙) 𝑢,↪Ll_1D463 ) のようなΠ (𝑙) ∼ Bern(Π (𝑢),↪Ll_1D463 ) でパラメータ化されたBernoulli分布からZ (𝑙) ∼ 𝑢,↪Ll_1D463) が引かれると考える。[34].
As the parameter Π (𝑙) 𝑢,𝑣 is jointly trained with the downstream tasks, a small value of Π (𝑙) 𝑢,𝑣 suggests that the attention A (𝑙) 𝑢,𝑣 is more likely to be irrelevant, and could be removed without side effects.
パラメータΠ (𝑙) 𝑢,𝑣は下流タスクと共同で学習されるため、Π (𝑙) 𝑢,𝑣の値が小さいと、注目A (𝑙) 𝑢,𝑣は無関係である可能性が高く、副作用なく削除できる。
By doing this, Eq.(7) becomes:
こうすることで、式(7)は次のようになる：

$$
\tag{8}
$$

where E(·) is the expectation.
ここでE(-)は期待値である。
The regularization term is now continuous, but the first term L𝐵𝐶𝐸 (Z, Θ) still involves the discrete variables Z (𝑙) .
正則化項は連続になったが、第一項L𝐵𝐸 (Z, Θ)はまだ離散変数Z (↪Ll_1D459) を含んでいる。
One can address this issue by using existing gradient estimators, such as REINFORCE [48] and Straight Through Estimator [3], etc.
REINFORCE [48]やStraight Through Estimator [3]などの既存の勾配推定器を使用することで、この問題に対処することができる。
These approaches, however, suffer from either biased gradients or high variance.
しかし、これらのアプローチは、偏った勾配や高い分散に悩まされている。
Alternatively, we directly optimize discrete variables using the recently proposed augment-REINFORCEmerge (ARM) [15, 16, 56], which is unbiased and has low variance.
あるいは、最近提案されたaugment-REINFORCEmerge（ARM）[15, 16, 56]を使って直接離散変数を最適化する。
In particular, we adopt the reparameterization trick [25], which reparameterizes Π (𝑙) 𝑢,𝑣 ∈ [0, 1] to a deterministic function 𝑔(·) with parameter Φ (𝑙) 𝑢,𝑣 , such that:
特に、Π (𝑙) 𝑢,↪Ll_1D463 ∈ [0, 1]をパラメータΦ (𝑙) ↪Ll_1D463 を持つ決定論的関数𝑔(-)に再パラメータ化する再パラメータ化トリック[25]を採用する：

$$
\tag{9}
$$

since the deterministic function 𝑔(·) should be bounded within [0, 1], we simply choose the standard sigmoid function as our deterministic function: 𝑔(𝑥) = 1/(1 + 𝑒 −𝑥 ).
決定論的関数 ᑔ(-) は[0, 1]内で有界であるべきなので、決定論的関数として標準シグモイド関数を選ぶ： ᑔ = 1/(1 + 𝑒 -↪Ll_1D465 ).
As such, the second term in Eq.(8) becomes differentiable with the continuous function 𝑔(·).
そのため、式(8)の第2項は連続関数ᑔ(-)で微分可能になる。
We next present the ARM estimator for computing the gradients of binary variables in the first term of Eq.(8) [15, 16, 56].
次に、式(8)の第1項のバイナリ変数の勾配を計算するためのARM推定器を示す[15, 16, 56]。
According to Theorem 1 in ARM [56], we can compute the gradients for Eq.(8) as:
ARM [56]の定理1によれば、式(8)の勾配は次のように計算できる：

$$
\tag{10}
$$

where Uni(0, 1) denotes the Uniform distribution within [0, 1], and L𝐵𝐶𝐸 (I[U > 𝑔(−Φ)], Θ) is the cross-entropy loss obtained by setting the binary masks Z (𝑙) to 1 if U (𝑙) > 𝑔(−Φ (𝑙) ) in the forward pass, and 0 otherwise.
ここでUni(0, 1)は[0, 1]内の一様分布を表し、L𝐵𝐸 (I[U > 𝑔(-Φ)])、 Θ) は、フォワードパスにおいて、U (↪Ll_1D459) > Φ (-Φ (↪Ll_1D459) の場合にバイナリマスクZ (↪Ll_1D459) を1に設定し、それ以外の場合に0に設定することで得られるクロスエントロピー損失。
The same strategy is applied to L𝐵𝐶𝐸 (I[U < 𝑔(Φ)], Θ).
同じ戦略をL𝐵𝐸 (I[U < ǔ], Θ)にも適用する。
Moreover, ARM is an unbiased estimator due to the linearity of expectations.
さらに、ARMは期待値の線形性により不偏推定量となる。
Note that we need to evaluate L𝐵𝐶𝐸 (·) twice to compute gradients in Eq.(10).
式(10)の勾配を計算するために、L𝐵𝐸 (-)を2回評価する必要があることに注意。
Given the fact that 𝑢 ∼ Uni(0, 1) implies (1 − 𝑢) ∼ Uni(0, 1), we can replace U with (1 − U) in the indicator function inside L𝐵𝐶𝐸 (I[U > 𝑔(−Φ)], Θ):
↪Ll_1D462 ∼ Uni(0, 1)が(1 - ↪Ll_1D462) ∼ Uni(0, 1)を意味することから、L𝐶𝐸 (I[U > 𝑔(-Φ)], Θ)内の指標関数において、Uを(1 - U)に置き換えることができる：

$$
\tag{}
$$

To this end, we can further reduce the complexity by considering the variants of ARM – Augment-Reinforce (AR) [56]:
このため、ARMの変形であるAugment-Reinforce（AR）[56]を考慮することで、さらに複雑さを軽減することができる：

$$
\tag{11}
$$

where only requires one-forward pass.
ここで必要なのはワンフォワードパスだけだ。
The gradient estimator ∇ 𝐴𝑅 Φ L (Φ, Θ) is still unbiased but may pose higher variance, comparing to ∇ 𝐴𝑅𝑀 Φ L (Φ, Θ).
勾配推定量∇ Φ 𝐴 L (Φ, Θ)は依然として不偏であるが、∇ Φ 𝐴 Φ L (Φ, Θ)に比べて分散が大きくなる可能性がある。
In the experiments, we can trade off the variance of the estimator with complexity.
実験では、推定量の分散と複雑さをトレードオフにすることができる。

In the training stage, we update ∇ΦL (Φ, Θ) (either Eq.(10) or Eq.(11)) and ∇ΘL (Φ, Θ) 3 during the back propagation.
学習段階では、逆伝播中に∇ΦL（Φ，Θ）（式（10）または式（11））と∇ΘL（Φ，Θ）3を更新する。
In the inference stage, we can use the expectation of Z (𝑙) 𝑢,𝑣 ∼ Bern(Π (𝑙) 𝑢,𝑣 ) as the mask in Eq.(5), i.e., E(Z (𝑙) 𝑢,𝑣 ) = Π (𝑙) 𝑢,𝑣 = 𝑔(𝚽 (𝑙) 𝑢,𝑣 ).
推論段階では、Z (𝑙) 𝑢,𝑣 ∼ Bern(Π (𝑢),𝑣 )の期待値を式(5)のマスクとして使うことができる、すなわち、E(Z (𝑙) 𝑢,𝑣 = Π(𝑙) 𝑢,𝑣 = 𝑔(𝑢 (𝑙) 𝑣 )。
Nevertheless, this will not yield a sparse attention M(𝑙) since the sigmoid function is smooth unless the hard sigmoid function is used in Eq.(9).
とはいえ、式(9)でハードシグモイド関数を使わない限り、シグモイド関数は平滑なので、これではスパース注意M(↪Ll459)は得られない。
Here we simply clip those values 𝑔(𝚽 (𝑙) 𝑢,𝑣 ) ≤ 0.5 to zeros such that a sparse attention matrix is guaranteed and the corresponding noisy attentions are eventually eliminated.
ここでは、疎な注意行列が保証され、対応するノイジーな 注意が最終的に排除されるように、単に値𝑔(𝚽) ≤ 0.5 をゼロに切り取る。

## 4.2. Jacobian Regularization 

As recently proved by [28], the standard dot-product self-attention is not Lipschitz continuous and is vulnerable to the quality of input sequences.
最近[28]によって証明されたように、標準的なドット積自己アテンションはリプシッツ連続ではなく、入力シーケンスの品質に弱い。
Let 𝑓 (𝑙) be the 𝑙-th Transformer block (Sec 3.2.2) that contains both a self-attention layer and a point-wise feed-forward layer, and x be the input.
𝑓を𝑙番目のTransformerブロック(第3.2.2節)とし、自己注意層とポイント単位のフィードフォワード層を含むとする。
We can measure the robustness of the Transformer block using the residual error: 𝑓 (𝑙) (x + 𝝐) − 𝑓 (𝑙) (x), where 𝝐 is a small perturbation vector and the norm of 𝝐 is bounded by a small scalar 𝛿, i.e., ∥𝝐 ∥2 ≤ 𝛿.
ここで、𝝐は小さな摂動ベクトルであり、𝝐のノルムは小さなスカラー𝝐で境界付けられている、 ∥𝝐 ∥2 ≤ 𝛿。
Following the Taylor expansion, we have:
テイラー展開に従うと、次のようになる：

$$
\tag{}
$$

Let J (𝑙) (x) represent the Jacobian matrix at x where J (𝑙) 𝑖𝑗 = 𝜕 𝑓 (𝑙) 𝑖 (x) 𝜕𝑥𝑗 .
J (𝑙) (x)はxにおけるヤコビアン行列を表し、J (𝑙) 𝑖 (𝑗) = 𝜕 𝑓 (𝑙) (x) 𝜕とする。
Then, we set J (𝑙) 𝑖 (x) = 𝜕 𝑓 (𝑙) 𝑖 (x) 𝜕x to denote the 𝑖-th row of J (𝑙) (x).
そして、J (↪Ll_1D459) (x) の𝑖番目の行を表すために、J (↪Ll_1D459) (x) = 𝑖 (𝜕) 𝜕x とする。
According to Hölder’s inequality4 , we have:
Hölderの不等式4 によれば、次のようになる：

$$
\tag{}
$$

Above inequality indicates that regularizing the 𝐿2 norm on the Jacobians enforces a Lipschitz constraint at least locally, and the residual error is strictly bounded.
上記の不等式は、ヤコビアンのᵃ2ノルムを正則化することで、少なくとも局所的にはリプシッツ制約が強制され、残差は厳密に有界であることを示している。
Thus, we propose to regularize Jacobians with Frobenius norm for each Transformer block as:
そこで、各トランスフォーマーブロックのヤコビアンをフロベニウスノルムで正則化することを提案する：

$$
\tag{12}
$$

Importantly, ∥J (𝑙) ∥ 2 𝐹 can be approximated via various Monte-Carlo estimators [23, 37].
重要なことは、∥J (↪Ll459) ∥ 2 ǔは様々なモンテカルロ推定量[23, 37]によって近似できることです。
In this work, we adopt the classical Hutchinson estimator [23].
本研究では、古典的なHutchinson推定量[23]を採用する。
For each Jocobian matrix J (𝑙) ∈ R 𝑛×𝑛 , we have:
各ヨコビア行列J (↪Ll_1D459) ∈ R 𝑛×𝑛 に対して、次のようになる：

$$
\tag{}
$$

where 𝜼 ∈ N (0, I𝑛) is the normal distribution vector.
ここで、↪Ll_1∈N (0, I𝑛)は正規分布ベクトルである。
We further make use of random projections to compute the norm of Jacobians R𝐽 and its gradient ∇ΘR𝐽 (Θ) [21], which significantly reduces the running time in practice.
さらに、ヤコビアンのノルムR𝐽とその勾配∇ΘR𝐽 (Θ)[21]を計算するためにランダム射影を利用する。

## 4.3. Optimization 

### 4.3.1. Joint Training 4.3.1. 合同トレーニング

Putting together loss in Eq.(4), Eq.(6), and Eq.(12), the overall objective of Rec-Denoiser is:
式(4)、式(6)、式(12)の損失をまとめると、Rec-Denoiserの全体的な目的は次のようになる：

$$
\tag{13}
$$

where 𝛽 and 𝛾 are regularizers to control the sparsity and robustness of self-attention networks, respectively.
ここで↪Ll_1D6FD と↪L_1D6FE↩は、それぞれ自己注意ネットワークのスパース性とロバスト性を制御する正則化子である。
Algorithm 1 summarizes the overall training of Rec-Denoiser with the AR estimator.
アルゴリズム1は、AR推定器を用いたRec-Denoiserの全体的なトレーニングをまとめたものである。

Lastly, it is worth mentioning that our Rec-Denoiser is compatible to many Transformer-based sequential recommender models since our differentiable masks and gradient regularizations will not change their main architectures.
最後に、我々のRec-Denoiserは、微分可能なマスクと勾配正則化は、それらの主要なアーキテクチャを変更しないので、多くのTransformerベースの逐次推薦モデルと互換性があることを言及する価値がある。
If we simply set all masks Z (𝑙) to be all-ones matrix and 𝛽 = 𝛾 = 0, our model boils down to their original designs.
単純にすべてのマスクZ (↪Ll_1D459) をオール1の行列とし、𝛽 = ↪Ll_1D6FE = 0とすると、モデルは元の設計に帰着する。
If we randomly set subset of masks Z (𝑙) to be zeros, it is equivalent to structured Dropout like LayerDrop [17], DropHead [60].
マスクのサブセットZ (↪Ll45↩)をランダムにゼロに設定すると、LayerDrop [17]やDropHead [60]のような構造化Dropoutと等価になる。
In addition, our Rec-Denoiser can work together with linearized self-attention networks [27, 59] to further reduce the complexity of attentions.
さらに、私たちのRec-Denoiserは、線形化された自己注意ネットワーク[27, 59]と連携することができ、注意の複雑さをさらに軽減することができる。
We leave this extension in the future.
私たちはこの延長を将来に残す。

### 4.3.2. Model Complexity 4.3.2. モデルの複雑さ

The complexity of Rec-Denoiser comes from three parts: a basic Transformer, differentiable masks, and Jacobian regularization.
Rec-Denoiserの複雑さは、基本的な変換器、微分可能なマスク、ヤコビアンの正則化という3つの部分から来ている。
The complexity of basic Transformer keeps the same as SASRec [26] or BERT4Rec [41].
基本的なTransformerの複雑さは、SASRec [26]やBERT4Rec [41]と同じである。
The complexity of differentiable masks requires either one-forward pass (e.g., AR with high variance) or two-forward pass (e.g., ARM with low variance) of the model.
微分可能なマスクの複雑さは、モデルのワン・フォワード・パス（高分散のARなど）またはツー・フォワード・パス（低分散のARMなど）を必要とする。
In sequential recommenders, the number of Transformer blocks is often very small (e.g., 𝐿 = 2 in SASRec [26] and BERT4Rec [41] ).
逐次レコメンダーでは、Transformerブロックの数は非常に少ないことが多い（例えば、SASRec [26]とBERT4Rec [41] では 𝐿 = 2 ）。
It is thus reasonable to use the ARM estimator without heavy computations.
従って、重い計算をせずにARM推定量を使用することは合理的である。
Besides, we compare the performance of AR and ARM estimators in Sec 5.3.Moreover, the random project techniques are surprisingly efficient to compute the norms of Jacobians [21].
さらに、ランダム・プロジェクト技法はヤコビアンのノルムを計算するのに驚くほど効率的である[21]。
As a result, the overall computational complexity remains the same order as the original Transformers during the training.
その結果、全体的な計算量は、トレーニング中のオリジナルのTransformersと同じオーダーのままである。
However, during the inference, our attention maps are very sparse, which enables much faster feed-forward computations.
しかし、推論中の注意マップは非常に疎なため、フィードフォワード計算をより高速に行うことができる。

# 5. Experiments 5. 実験

Here we present our empirical results.
ここでは実証的な結果を紹介する。
Our experiments are designed to answer the following research questions:
我々の実験は、以下の研究課題に答えるためにデザインされた：

- RQ1: How effective is the proposed Rec-Denoiser compared to the state-of-the-art sequential recommenders? RQ1: 提案するRec-Denoiserは、最新の逐次推薦器と比較してどの程度有効か？

- RQ2: How can Rec-Denoiser reduce the negative impacts of noisy items in a sequence? RQ2：Rec-Denoiserは、シーケンス内のノイズの多いアイテムの悪影響をどのように軽減できますか？

- RQ3: How do different components (e.g., differentiable masks and Jacobian regularization) affect the overall performance of Rec-Denoiser? RQ3：異なる構成要素（微分可能マスクやヤコビアン正則化など）は、Rec-Denoiserの全体的な性能にどのような影響を与えるか？

## 5.1. Experimental Setting # 5.1.Experimental Setting

### 5.1.1. Dataset 5.1.1. データ集合

We evaluate our models on five benchmark datasets: Movielens5 , Amazon6 (we choose the three commonly used categories: Beauty, Games, and Movies&TV), and Steam7 [30].
我々は5つのベンチマークデータセットでモデルを評価する： Movielens5、Amazon6（美容、ゲーム、映画＆TVの3つのよく使われるカテゴリーを選択）、Steam7 [30]である。
Their statistics are shown in Table 1.
統計は表1の通りである。
Among different datasets, MovieLens is the most dense one while Beauty has the fewest actions per user.
異なるデータセットの中で、MovieLensは最も密度が高く、Beautyはユーザーあたりのアクション数が最も少ない。
We use the same procedure as [26, 30, 39] to perform preprocessing and split data into train/valid/test sets, i.e., the last item of each user’s sequence for testing, the second-to-last for validation, and the remaining items for training.
26,30,39]と同じ手順で前処理を行い、データをtrain/valid/testセットに分割する。つまり、各ユーザーのシーケンスの最後のアイテムをtestingに、最後から2番目のアイテムをvalidationに、残りのアイテムをtrainingに使用する。

### 5.1.2. Baselines 5.1.2. ベースライン

Here we include two groups of baselines.
ここでは、2つのベースライン・グループが含まれている。
The first group includes general sequential methods (Sec 5.2): 1) FPMC [39]: a mixture of matrix factorization and first-order Markov chains model; 2) GRU4Rec [20]: a RNN-based method that models user action sequences; 3) Caser [42]: a CNN-based framework that captures high-order relationships via convolutional operations; 4) SASRec [26]: a Transformer-based method that uses left-to-right selfattention layers; 5) BERT4Rec [41]: an architecture that is similar to SASRec, but using bidirectional self-attention layers; 6) TiSASRec [30]: a time-aware self-attention model that further considers the relative time intervals between any two items; 7) SSE-PT [50]: a framework that introduces personalization into self-attention layers; 8) Rec-Denoiser: our proposed Rec-Denoiser that can choose any self-attentive models as its backbone.
最初のグループには、一般的な逐次的手法が含まれる（Sec.5.2）： 1) FPMC [39]：行列分解と一次マルコフ連鎖モデルの混合、2) GRU4Rec [20]：ユーザーの行動シーケンスをモデル化するRNNベースの手法、3) Caser [42]：畳み込み演算によって高次の関係を捉えるCNNベースのフレームワーク、4) SASRec [26]：左から右への自己注意層を使用するTransformerベースの手法、5) BERT4Rec [41]： 6) TiSASRec [30]：任意の2つのアイテムの間の相対的な時間間隔をさらに考慮する、時間を考慮した自己注意モデル、7) SSE-PT [50]：自己注意層にパーソナライズを導入するフレームワーク、8) Rec-Denoiser：バックボーンとして任意の自己注意モデルを選択できる、我々の提案するRec-Denoiser。
The second group contains sparse Transformers (Sec 5.3): 1) Sparse Transformer [10]: it uses a fixed attention pattern, where only specific cells summarize previous locations in the attention layers; 2) 𝛼-entmax sparse attention [12]: it simply replaces softmax with 𝛼-entmax to achieve sparsity.
番目のグループにはスパース変換器（Sec.5.3）が含まれる： 2) 𝛼-entmax sparse attention [12]: スパース性を達成するためにソフトマックスを 𝛼-entmax に置き換えたもの。
Note that we do not compare with other popular sparse Transformers like Star Transformer [18], Longformer [2], and BigBird [58].
なお、Star Transformer [18]、Longformer [2]、BigBird [58]のような他の有名なスパース変換器とは比較していない。
These Transformers are specifically designed for thousands of tokens or longer in the language modeling tasks.
これらのトランスフォーマーは、言語モデリングタスクにおける数千以上のトークン用に特別に設計されている。
We leave their explorations for recommendations in the future.
彼らの探求は今後の提言に委ねたい。
We also do not compare with LayerDrop [17] and DropHead [60] since the number of Transformer blocks and heads are often very small (e.g., 𝐿 = 2 in SARRec) in sequential recommendation.
また、LayerDrop[17]やDropHead[60]との比較は行わない。なぜなら、逐次推薦では、Transformerブロックやヘッドの数が非常に少ない（例えば、SARRecでは𝐿 = 2）ことが多いからである。
Other sequential architectures like memory networks [9, 22] and graph neural networks [4, 51] have been outperformed by the above baselines, we simply omit these baselines and focus on Transformer-based models.
メモリ・ネットワーク[9, 22]やグラフ・ニューラル・ネットワーク[4, 51]のような他の逐次アーキテクチャは、上記のベースラインよりも優れている。
The goal of experiments is to see whether the proposed differentiable mask techniques can reduce the negative impacts of noisy items in the self-attention layers.
実験の目的は、提案された微分可能なマスク技術が、自己アテンション層におけるノイズアイテムの悪影響を軽減できるかどうかを確認することである。

### 5.1.3. Evaluation metrics 5.1.3. 評価指標

For easy comparison, we adopt two common Top-N metrics, Hit@𝑁 and NDCG@𝑁 (with default value 𝑁 = 10), to evaluate the performance of sequential models [26, 30, 41].
比較を容易にするために、逐次モデルのパフォーマンスを評価するために、2つの一般的なTop-Nメトリクス、Hit@_141とNDCG@_441（デフォルト値ǔ = 10）を採用する[26, 30, 41]。
Typically, Hit@𝑁 counts the rates of the ground-truth items among top-𝑁 items, while NDCG@𝑁 considers the position and assigns higher weights to higher positions.
一般的に、Hit@_141は、トップ_1アイテムの中でグランドトゥルースアイテムの割合をカウントし、NDCG@_441は位置を考慮し、高い位置に高い重みを割り当てる。
Following the work [26, 30], for each user, we randomly sample 100 negative items, and rank these items with the ground-truth item.
26,30]に従い、各ユーザーについて100個のネガティブアイテムをランダムにサンプリングし、これらのアイテムをグランドトゥルースアイテムと順位付けする。
We calculate Hit@10 and NDCG@10 based on the rankings of these 101 items.
この101項目のランキングをもとにHit@10とNDCG@10を算出した。

### 5.1.4. Parameter settings 5.1.4. パラメータ設定

For all baselines, we initialize the hyper-parameters as the ones suggested by their original work.
すべてのベースラインについて、ハイパーパラメータを彼らのオリジナル研究で提案されたものとして初期化した。
They are then well tuned on the validation set to achieve optimal performance.
そして、最適なパフォーマンスを達成するために、検証セット上で十分に調整される。
The final results are conducted on the test set.
最終的な結果はテストセットで実施される。
We search the dimension size of items within {10, 20, 30, 40, 50}.
項目の次元サイズを{10, 20, 30, 40, 50}の範囲で検索する。
As our Rec-Denoiser is a general plugin, we use the same hyper-parameters as the basic Transformers, e.g., number of Transformer blocks, batch size, learning rate in Adam optimizer, etc.
我々のRec-Denoiserは一般的なプラグインであるため、基本的なTransformerと同じハイパーパラメーターを使用する。例えば、Transformerブロックの数、バッチサイズ、Adamオプティマイザーの学習率などである。
According to Table 1, we set the maximum length of item sequence 𝑛 = 50 for dense datasets MovieLens and Movies&TV, and 𝑛 = 25 for sparse datasets Beauty, Games, and Steam.
表1によると、密なデータセットであるMovieLensとMovies&TVにはアイテム列の最大長𝑛 = 50を、疎なデータセットであるBeauty、Games、Steamには𝑛 = 25を設定した。
In addition, we set the number of Transformer blocks 𝐿 = 2, and the number of heads 𝐻 = 2 for self-attentive models.
さらに、トランスフォーマーブロックの数𝐿 = 2、自己注意モデルのヘッド数𝐻 = 2とした。
For Rec-Denoiser, two extra regularizers 𝛽 and 𝛾 are both searched within {10−1 , 10−2 , .
Rec-Denoiserでは、2つの正則化子ǽと𝛾が{10-1 , 10-2 , .
..
..
, 10−5 }.
, 10-5 }.
We choose ARM estimator due to the shallow structures of self-attentive recommenders.
我々は、自己アテンション型推薦者の浅い構造からARM推定器を選択した。

## 5.2. Overall Performance(RQ1) 5.2.総合成績（RQ1）

Table 2 presents the overall recommendation performance of all methods on the five datasets.
表2は、5つのデータセットにおけるすべての手法の総合的な推薦性能を示している。
Our proposed Recdenoisers consistently obtain the best performance for all datasets.
我々の提案するRecdenoisersは、すべてのデータセットで一貫して最高の性能を得た。
Additionally, we have the following observations:
さらに、次のような見解もある：

- The self-attentive sequential models (e.g., SASRec, BERT4Rec, TiSASRec, and SSE-PT) generally outperform FPMC, GRU4Rec, and Caser with a large margin, verifying that the self-attention networks have good ability of capture long-range item dependencies for the task of sequential recommendation. 自己注意型逐次推薦モデル（SASRec、BERT4Rec、TiSASRec、SSE-PTなど）は、一般にFPMC、GRU4Rec、Caserを大きなマージンをもって上回り、自己注意型ネットワークが逐次推薦のタスクに対して長距離項目依存性を捕捉する優れた能力を持つことが検証された。

- Comparing the original SASRec and its variants BERT4Rec, TiSASRec and SSE-PT, we find that the self-attentive models can gets benefit from incorporating additional information such as bi-directional attentions, time intervals, and user personalization. Such auxiliary information is important to interpret the dynamic behaviors of users. オリジナルのSASRecとその変種であるBERT4Rec、TiSASRec、SSE-PTを比較すると、自己注意モデルは、双方向の注意、時間間隔、ユーザーのパーソナライゼーションなどの追加情報を取り入れることで利益を得ることができることがわかる。 このような補助情報は、ユーザーのダイナミックな行動を解釈するために重要である。

- The relative improvements of Rec-denoisers over their backbones are significant for all cases. For example, SASRec+Denoiser has on average 8.04% improvement with respect to Hit@10 and over 12.42% improvements with respect to NDCG@10. Analogously, BERT4Rec+Denoiser outperforms the vanilla BERT4Rec by average 7.47% in Hit@10 and 11.64% in NDCG@10. We also conduct the significant test between Rec-denoisers and their backbones, where all 𝑝-values< 1𝑒 −6 , showing that the improvements of Rec-denoisers are statistically significant in all cases. Rec-denoisersのバックボーンに対する相対的な向上は、すべてのケースで顕著である。 例えば、SASRec+Denoiserは、Hit@10に対して平均8.04%、NDCG@10に対して平均12.42%以上の改善が見られる。 同様に、BERT4Rec+Denoiserは、Hit@10では平均7.47%、NDCG@10では平均11.64%で、バニラBERT4Recを上回っている。 また、Rec-denoiserとそのバックボーンとの間の有意差検定も行った。ここでは、すべての ↪L_1D45↩値< 1𝑒 -6であり、Rec-denoiserの改善がすべてのケースで統計的に有意であることが示された。

These improvements of our proposed models are mainly attributed to the following reasons: 1) Rec-denoisers inherit full advantages of the self-attention networks as in SASRec, BERT4Rec, TiSASRec, and SSE-PT; 2) Through differentiable masks, irrelevant item-item dependencies are removed, which could largely reduce the negative impacts of noisy data; 3) Jacobian regularization enforces the smoothness of gradients, limiting quick changes of the output against input perturbations.
提案モデルのこれらの改善は主に以下の理由による： 1）Rec-denoisersは、SASRec、BERT4Rec、TiSASRec、SSE-PTのような自己注意ネットワークの利点を完全に受け継いでいる、2）微分可能なマスクを通して、無関係な項目-項目依存性が除去され、ノイズの多いデータの悪影響を大幅に軽減できる、3）ヤコビアの正則化は勾配の滑らかさを強制し、入力摂動に対する出力の素早い変化を制限する。
In general, smoothness improves the generalization of sequential recommendation.
一般的に、滑らかさは逐次推薦の一般性を向上させる。
Overall, the experimental results demonstrate the superiority of our Rec-Denoisers.
全体として、実験結果は我々のRec-Denoisersの優位性を示している。

## 5.3. Robustness to Noises(RQ2) 

As discussed before, the observed item sequences often contain some noisy items that are uncorrelated to each other.
前述したように、観測された項目列には、しばしば互いに無相関なノイズ項目が含まれる。
Generally, the performance of self-attention networks is sensitive to noisy input.
一般に、自己注意ネットワークの性能はノイズの多い入力に敏感である。
Here we analyze how robust our training strategy is for noisy sequences.
ここでは、ノイズの多いシーケンスに対して、我々のトレーニング戦略がどの程度ロバストであるかを分析する。
To achieve this, we follow the strategy [35] that corrupts the training data by randomly replacing a portion of the observed items in the training set with uniformly sampled items that are not in the validation or test set.
これを達成するために、我々は、トレーニングセットで観測された項目の一部を、検証セットやテストセットにはない一様にサンプリングされた項目でランダムに置き換えることによって、トレーニングデータを破損させる戦略[35]に従う。
We range the ratio of the corrupted training data from 0% to 25%.
破損したトレーニングデータの比率は、0%から25%の範囲である。
We only report the results of SASRec and SASRec-Denoiser in terms of Hit@10.
SASRecとSASRec-Denoiserの結果は、Hit@10でのみ報告する。
The performance of other self-attentive models is the same and omitted here due to page limitations.
他の自己アテンションモデルのパフォーマンスも同様で、ここではページの都合上省略した。
In addition, we compare with two recent sparse Transformers: Sparse Transformer [10] and 𝛼-entmax sparse attention [12].
さらに、最近の2つのスパース変換器と比較する： Sparse Transformer [10]と ↪L_1D6FC↩-entmax sparse attention [12]である。
All the simulated experiments are repeated five times and the average results are shown in Figure 2.
すべての模擬実験を5回繰り返し、その平均結果を図2に示す。
Clearly, the performance of all models degrades with the increasing noise ratio.
明らかに、すべてのモデルの性能は、ノイズ比率の増加とともに低下する。
We observe that our Rec-denoiser (use either ARM or AR estimators) consistently outperforms 𝛼-entmax and Sparse Transformer under different ratios of noise on all datasets.
我々は、我々のRec-denoiser（ARMまたはAR推定量を使用）が、全てのデータセットにおいて、異なるノイズ比率の下で一貫して↪L_1D6FC↩-entmaxとSparse Transformerを上回ることを観察した。
𝛼-entmax heavily relies on one trainable parameter 𝛼 to filter out the noise, which may be over tuned during the training, while Sparse Transformer adopts a fixed attention pattern, which may lead to uncertain results, especially for short item sequences like Beauty and Games.
𝛼-entmax は、ノイズをフィルタリングするための1つの訓練可能なパラメータ𝛼に大きく依存しており、訓練中に過剰に調整される可能性があります。一方、Sparse Transformerは固定された注意パターンを採用しており、特にBeautyやGamesのような短いアイテムシーケンスでは、不確実な結果につながる可能性があります。
In contrast, our differentaible masks have much more flexibility to adapt to noisy sequences.
対照的に、我々の異種マスクは、ノイズの多いシーケンスに適応する柔軟性がはるかに高い。
The Jacobian regularization further encourages the smoothness of our gradients, leading to better generalization.
ヤコビアン正則化は、勾配の滑らかさをさらに促進し、より良い汎化をもたらす。
From the results, the AR estimator performs better than 𝛼-entmax but worse than ARM.
その結果、AR推定器は𝛼-entmaxよりは良いが、ARMよりは悪い。
This result is expected since ARM has much low variance.
ARMは分散が少ないので、この結果は予想通りである。
In summary, both ARM and AR estimators are able to reduce the negative impacts of noisy sequences, which could improve the robustness of self-attentive models.
まとめると、ARMとARの両推定器は、ノイズの多いシーケンスの悪影響を軽減することができ、自己注意モデルの頑健性を向上させることができる。

## 5.4. Study of Rec-Denoiser(RQ3) 

We further investigate the parameter sensitivity of Rec-Denoiser.
さらにRec-Denoiserのパラメータ感度を調べた。
For the number of blocks 𝐿 and the number of heads 𝐻, we find that self-attentive models typically benefit from small values (e.g., 𝐻, 𝐿 ≤ 4), which is similar to [31, 41].
ブロック数ᵃとヘッド数ᵃについては、自己注意モデルは一般的に小さな値（例えば、ᵃ≦4）が有効であることがわかり、これは[31, 41]と同様である。
In this section, we mainly study the following hyper-parameters: 1) the maximum length 𝑛, 2) the regularizers 𝛽 and 𝛾 to control the sparsity and smoothness.
本節では、主に以下のハイパーパラメータを研究する： 1)最大長𝑛、2)スパース性と平滑性を制御する正則化子ǽと↪L_1FE↩。
Here we only study the SASRec and SASRec-Denoiser due to page limitations.
ここでは、ページの都合上、SASRecとSASRec-Denoiserについてのみ述べる。

Fig.3.Effect of maximum length 𝑛 on ranking performance (Hit@10).
図3.最大長𝑛がランキング性能に与える影響（Hit@10）。

Fig.4.Effect of regularizers 𝛽 and 𝛾 on ranking performance (Hit@10).
図4.正則化量ǽとǖがランキング性能に与える影響(Hit@10FE6)。

### 5.4.1. Maximum Length $n$ 5.4.1. 最大長 $n$

Figure 3 shows the Hit@10 for maximum length 𝑛 from 20 to 80 while keeping other optimal hyper-parameters unchanged.
図3は、他の最適ハイパーパラメータを変えずに、最大長𝑛を20から80まで変化させた場合のHit@10を示している。
We only test on the densest and sparsest datasets: MovieLeans and Beauty.
最も高密度で疎なデータセットでのみテストする： MovieLeansとBeautyである。
Intuitively, the larger sequence we have, the larger probability that the sequence contains noisy items.
直観的には、シーケンスが大きければ大きいほど、そのシーケンスにノイズのある項目が含まれる確率が高くなる。
FWe observed that our SASRec-Denoiser improves the performance dramatically with longer sequences.
F我々のSASRec-Denoiserは、長いシーケンスで劇的に性能が向上することが確認された。
This demonstrates that our design is more suitable for longer inputs, without worrying about the quality of sequences.
これは、我々の設計がシーケンスの質を気にすることなく、より長い入力に適していることを示している。

### 5.4.2. The regularizers $\beta$ and $\gamma$ 5.4.2. 正則化記号$beta$と$gamma$。

There are two major regularization parameters 𝛽 and 𝛾 for sparsity and gradient smoothness, respectively.
正則化パラメータǽと𝛾は、それぞれスパース性と勾配平滑性を表す。
Figure 4 shows the performance by changing one parameter while fixing the other as 0.01.
図4は、一方のパラメーターを0.01に固定し、もう一方のパラメーターを変更した場合のパフォーマンスを示している。
As can be seen, our performance is relatively stable with respect to different settings.
見てわかるように、我々のパフォーマンスは異なる設定に対して比較的安定している。
In the experiments, the best performance can be achieved at 𝛽 = 0.01 and 𝛾 = 0.001 for the MovieLens dataset.
実験では、MovieLensデータセットに対して、↪Ll_1D6FD = 0.01とǖ = 0.001で最高の性能を達成することができた。

# 6. Conclusion and Fture Work 6. 結論と今後の課題

In this work, we propose Rec-Denoiser to adaptively eliminate the negative impacts of the noisy items for self-attentive recommender systems.
本研究では、Rec-Denoiserを提案し、自己アテンション型レコメンダーシステムにおけるノイズアイテムの悪影響を適応的に除去する。
The proposed Rec-Denoiser employs differentiable masks for the self-attention layers, which can dynamically prune irrelevant information.
提案するRec-Denoiserは、自己注意層に微分可能なマスクを採用し、無関係な情報を動的に除去することができる。
To further tackle the vulnerability of self-attention networks to small perturbations, Jacobian regularization is applied to the Transformer blocks to improve the robustness.
小さな摂動に対する自己アテンション・ネットワークの脆弱性にさらに取り組むため、ロバスト性を向上させるヤコビアン正則化がトランスフォーマー・ブロックに適用される。
Our experimental results on multiple real-world sequential recommendation tasks illustrate the effectiveness of our design.
実世界の複数の逐次推薦タスクに関する実験結果は、我々の設計の有効性を示している。

Our proposed Rec-Denoiser framework (e.g., differentiable masks and Jacobian regularization) can be easily applied to any Transformer-based models in many tasks besides sequential recommendation.
我々の提案するRec-Denoiserフレームワーク（微分可能マスクやヤコビアン正則化など）は、逐次推薦以外の多くのタスクにおいて、あらゆるTransformerベースのモデルに容易に適用できる。
In the future, we will continue to demonstrate the contributions of our design in many real-world applications.
将来的には、多くの実世界のアプリケーションにおいて、我々の設計の貢献を実証していくつもりである。