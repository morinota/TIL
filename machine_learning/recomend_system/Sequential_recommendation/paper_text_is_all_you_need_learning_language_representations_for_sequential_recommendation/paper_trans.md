## link リンク

https://arxiv.org/abs/2305.13731
https://arxiv.org/abs/2305.13731

## title タイトル

Text Is All You Need: Learning Language Representations for Sequential Recommendation
テキストがあればいい： 
逐次推薦のための言語表現を学ぶ

## abstract 抄録

Sequential recommendation aims to model dynamic user behavior from historical interactions.
逐次レコメンデーションは、過去のインタラクションからダイナミックなユーザー行動をモデル化することを目的としている。
Existing methods rely on either explicit item IDs or general textual features for sequence modeling to understand user preferences.
既存の方法は、ユーザーの嗜好を理解するためのシーケンスモデリングに、明示的なアイテムIDか一般的なテキスト特徴のどちらかに依存している。
While promising, these approaches still struggle to model cold-start items or transfer knowledge to new datasets.
有望ではあるが、これらのアプローチは、コールドスタート項目のモデル化や、新しいデータセットへの知識の移行にはまだ苦労している。
In this paper, we propose to model user preferences and item features as language representations that can be generalized to new items and datasets.
本論文では、ユーザーの嗜好とアイテムの特徴を、新しいアイテムやデータセットに汎化可能な言語表現としてモデル化することを提案する。
To this end, we present a novel framework, named Recformer, which effectively learns language representations for sequential recommendation.
この目的のために、我々は、逐次推薦のための言語表現を効果的に学習する、Recformerと名付けられた新しいフレームワークを提示する。
Specifically, we propose to formulate an item as a "sentence" (word sequence) by flattening item key-value attributes described by text so that an item sequence for a user becomes a sequence of sentences.
具体的には、テキストで記述されたアイテムのキー・バリュー属性を平坦化することで、ユーザーにとってのアイテム列が文の列になるように、アイテムを「文」（単語列）として定式化することを提案する。
For recommendation, Recformer is trained to understand the "sentence" sequence and retrieve the next "sentence".
推薦のために、Recformerは「文」の並びを理解し、次の「文」を検索するように訓練されている。
To encode item sequences, we design a bi-directional Transformer similar to the model Longformer but with different embedding layers for sequential recommendation.
アイテムのシーケンスをエンコードするために、我々は、モデルLongformerと同様の双方向トランスフォーマーを設計するが、シーケンシャル推薦のために異なるエンベッディングレイヤーを持つ。
For effective representation learning, we propose novel pretraining and finetuning methods which combine language understanding and recommendation tasks.
効果的な表現学習のために、言語理解と推薦タスクを組み合わせた新しい事前学習と微調整方法を提案する。
Therefore, Recformer can effectively recommend the next item based on language representations.
したがって、Recformerは、言語表現に基づいて次の項目を効果的に推薦することができる。
Extensive experiments conducted on six datasets demonstrate the effectiveness of Recformer for sequential recommendation, especially in low-resource and cold-start settings.
6つのデータセットを用いて行われた広範な実験により、Recformerの逐次推薦の有効性が、特に低リソースかつコールドスタートな環境において実証された。

# Introduction はじめに

Sequential recommender systems model historical user interactions as temporally-ordered sequences to recommend potential items that users are interested in.
シーケンシャル・レコメンダー・システムは、過去のユーザーとのやりとりを時間的に順序付けられたシーケンスとしてモデル化し、ユーザーが興味を持っている潜在的なアイテムを推薦する。
Sequential recommenders [11, 14, 25, 27] can capture both short-term and long-term preferences of users and hence are widely used in different recommendation scenarios.
逐次レコメンダー[11, 14, 25, 27]は、ユーザーの短期的嗜好と長期的嗜好の両方を捉えることができるため、様々なレコメンデーションシナリオで広く使われている。
Various methods have been proposed to improve the performance of sequential recommendation, including Markov Chains [9, 25], RNN/CNN models [11, 17, 28, 34] and self-attentive models [14, 19, 27].
逐次推薦のパフォーマンスを向上させるために、マルコフ連鎖[9, 25]、RNN/CNNモデル[11, 17, 28, 34]、自己注意モデル[14, 19, 27]など、様々な手法が提案されている。
Traditional sequential recommendation models convert items into IDs and create item embedding tables for encoding.
従来の逐次推薦モデルは、アイテムをIDに変換し、エンコーディングのためにアイテム埋め込みテーブルを作成する。
Item embeddings are learned from sequences of user interactions.
アイテム埋め込みは、ユーザーとのインタラクションのシーケンスから学習される。
To enrich item features, some approaches [4, 20, 37, 38] incorporate item contexts such as item textual information or categorical features into ID embeddings.
項目の特徴を豊かにするために、いくつかのアプローチ[4, 20, 37, 38]は、項目のテキスト情報やカテゴリ的特徴などの項目のコンテキストをID埋め込みに組み込んでいる。
While ID-based methods are promising, they struggle to understand cold-start items or conduct cross-domain recommendations where models are trained and then applied to different recommendation scenarios.
IDベースの手法は有望ではあるが、コールドスタート項目の理解や、モデルを学習した後に異なる推薦シナリオに適用するクロスドメイン推薦の実施に苦戦している。
Item-specific IDs prevent models from learning transferable knowledge from training data for cold-start items and new datasets.
項目固有のIDは、コールドスタート項目や新しいデータセットのトレーニングデータからモデルが移行可能な知識を学習することを妨げる。
As a result, item IDs limit the performance of sequential recommenders on cold-start items and we have to re-train a sequential recommender for continually added new items.
その結果、アイテムIDはコールドスタートアイテムに対する逐次レコメンダーの性能を制限し、継続的に追加される新しいアイテムに対して逐次レコメンダーを再トレーニングしなければならない。
Therefore, transferable recommenders can benefit both cold-start items and new-domain datasets.
したがって、転送可能なレコメンダーは、コールドスタートの項目と新しいドメインのデータセットの両方に利益をもたらすことができる。
To develop transferable recommender systems, previous studies usually assume shared information such as overlapping users/items [13, 26, 39] and common features [29] is available and then reduce the gap between source and target domains by learning either semantic mappings [39] or transferable components [16].
転送可能な推薦システムを開発するために、先行研究では通常、重複するユーザー／アイテム[13, 26, 39]や共通の特徴[29]などの共有情報が利用可能であると仮定し、意味的マッピング[39]または転送可能なコンポーネント[16]のいずれかを学習することによって、ソースドメインとターゲットドメイン間のギャップを減らす。
Such assumptions are rarely true in real applications because items in different domains (e.g., Laptops and T-shirts) usually contain different features for recommendation.
なぜなら、異なるドメインのアイテム（例えば、ノートパソコンとTシャツ）には、通常、推薦のための異なる特徴が含まれているからである。
Therefore, to have effective cross-domain transfer, recent works [7, 12] leverage the generality of natural language texts (e.g., titles, descriptions of items) for common knowledge in different domains.
したがって、効果的なクロスドメイン転送を行うために、最近の研究[7, 12]では、異なるドメインで共通の知識を得るために、自然言語テキストの一般性（例：タイトル、アイテムの説明）を活用している。
The basic idea is to employ pre-trained language models such as BERT [6] to obtain text representations and then learn the transformation from text representations to item representations.
基本的な考え方は、BERT [6]のような事前に訓練された言語モデルを採用してテキスト表現を取得し、テキスト表現から項目表現への変換を学習することである。
The knowledge of the transformation can be transferred across different domains and shows promising performance.
変換の知識は、異なるドメインにまたがって転送することができ、有望な性能を示している。
However, such frameworks of learning transformation from language to items have several limitations: (1) Pre-trained language models are usually trained on a general language corpus (e.g., Wikipedia) serving natural language tasks that have a different language domain from item texts (e.g., concatenation of item attributes), hence text representations from pretrained language models for items are usually sub-optimal.(2) Text representations from pre-trained language models are not able to learn the importance of different item attributes and only provide coarse-grained (sentence-level) textual features but cannot learn fine-grained (word-level) user preferences for recommendations (e.g., find the same color in recent interactions for clothing recommendations).(3) Due to the independent training of pre-trained language models (by language understanding tasks, e.g., Masked Language Modeling) and transformation models (by recommendation tasks, e.g., next item prediction), the potential ability of models to understand language for recommendations has not been fully developed (by joint training).
しかし、言語から項目への変換を学習するこのような枠組みには、いくつかの限界がある： 
(1)事前に学習された言語モデルは、通常、一般的な言語コーパス（Wikipediaなど）で学習される、 (2)事前訓練された言語モデルからのテキスト表現は、異なるアイテム属性の重要性を学習することができず、粗い粒度（文レベル）のテキスト特徴しか提供しない、 (3)事前に学習された言語モデル(例えば、マスクされた言語モデリングなどの言語理解タスク)と変換モデル(例えば、次のアイテム予測などの推薦タスク)の独立した学習により、推薦のための言語理解モデルの潜在的な能力は(共同学習により)完全には開発されていない。）
With the above limitations in mind, we aim to unify the frameworks of natural language understanding and recommendations in an ID-free sequential recommendation paradigm.
以上のような制約を念頭に置き、我々は自然言語理解とレコメンデーションの枠組みをIDフリーの逐次レコメンデーション・パラダイムに統一することを目指している。
The pre-trained language models [6, 15, 23, 24] benefit various downstream natural language processing tasks due to their transferable knowledge from pre-training.
事前に訓練された言語モデル[6, 15, 23, 24]は、事前訓練から得られる知識の伝達が可能であるため、様々な自然言語処理タスクの下流に恩恵をもたらす。
The basic idea of this paper is to use the generality of language models through joint training of language understanding and sequential recommendations.
本稿の基本的な考え方は、言語理解と逐次推薦の共同学習を通じて、言語モデルの汎用性を利用することである。
To this end, there are three major challenges to be solved.
そのためには、解決すべき3つの大きな課題がある。
First, previous text-based methods [7, 12] usually have their specific item texts (e.g., item descriptions, concatenation of item attributes).
第一に、これまでのテキストベースの手法[7, 12]は、通常、特定の項目テキスト（例：項目の説明、項目属性の連結）を持っている。
Instead of specific data types, we need to find a universal input data format of items for language models that is flexible enough to different kinds of textual item information.
特定のデータ型の代わりに、異なる種類のテキスト項目情報に対して十分に柔軟な、言語モデルのための項目の普遍的な入力データ形式を見つける必要がある。
Second, it is not clear how to model languages and sequential transitions of items in one framework.
第二に、言語とアイテムの逐次遷移を一つのフレームワークでモデル化する方法が明確でない。
Existing language models are not able to incorporate sequential patterns of items and cannot learn the alignment between items and item texts.
既存の言語モデルは、アイテムの連続的なパターンを組み込むことができず、アイテムとアイテムのテキスト間のアラインメントを学習することができない。
Third, a training and inference framework is necessary to bridge the gap between natural languages and recommendations like how to efficiently rank items based on language models without trained item embeddings.
第三に、自然言語とレコメンデーションの間のギャップを埋めるために、学習と推論のフレームワークが必要である。例えば、学習済みのアイテム埋め込みなしで、言語モデルに基づいてアイテムを効率的にランク付けする方法などである。
To address the above problems, we propose Recformer, a framework that can learn language representations for sequential recommendation.
上記の問題点を解決するために、我々は逐次推薦のための言語表現を学習するフレームワークであるRecformerを提案する。
Overall, our approach takes a text sequence of historical items as input and predicts the next item based on language understanding.
全体として、我々のアプローチは、歴史的項目のテキストシーケンスを入力とし、言語理解に基づいて次の項目を予測する。
Specifically, as shown in Figure 1, we first formulate an item as key-value attribute pairs which can include any textual information such as the title, color, brand of an item.
具体的には、図1に示すように、まず、アイテムのタイトル、色、ブランドなどの任意のテキスト情報を含むことができるキーと値の属性ペアとしてアイテムを定式化します。
Different items can include different attributes as item texts.
異なるアイテムは、アイテムのテキストとして異なる属性を含めることができます。
Then, to encode a sequence of key-value attribute pairs, we propose a novel bi-directional Transformer [30] based on Longformer structure [2] but with different embeddings for item texts to learn item sequential patterns.
次に、キーと値の属性ペアのシーケンスをエンコードするために、Longformer構造[2]に基づくが、アイテムのシーケンシャルパターンを学習するために、アイテムのテキストに対して異なるエンベッディングを持つ、新しい双方向トランスフォーマー[30]を提案する。
Finally, to effectively learn language representations for recommendation, we design the learning framework for the model including pre-training, finetuning and inference processes.
最後に、推薦のための言語表現を効果的に学習するために、事前学習、微調整、推論プロセスを含むモデルの学習フレームワークを設計する。
Based on the above methods, Recformer can effectively recommend the next items based on item text representations.
以上の方法に基づいて、Recformerはアイテムのテキスト表現に基づいて次のアイテムを効果的に推薦することができる。
Furthermore, the knowledge learned from training can be transferred to cold-start items or a new recommendation scenario.
さらに、トレーニングから学んだ知識は、コールドスタートの項目や新しい推薦シナリオに移すことができる。

To evaluate Recformer, we conduct extensive experiments on real-world datasets from different domains.
Recformerを評価するために、我々は様々なドメインの実世界のデータセットで広範な実験を行った。
Experimental results show that our method can achieve 15.83% and 39.78% (NDCG@10) performance improvements under fully-supervised and zero-shot sequential recommendation settings respectively.1 Our contributions in this paper can be summarized as follows:
実験結果によれば、我々の手法は、完全教師あり推薦とゼロショット逐次推薦の設定において、それぞれ15.83％と39.78％（NDCG@10）の性能向上を達成できる：

- We formulate items as key-value attribute pairs for the IDfree sequential recommendation and propose a novel bidirectional Transformer structure to encode sequences of key-value pairs. 我々は、IDフリーの逐次推薦のために、項目をキーと値の属性ペアとして定式化し、キーと値のペアのシーケンスを符号化するための新しい双方向トランスフォーマー構造を提案する。

- We design the learning framework that helps the model learn users’ preferences and then recommend items based on language representations and transfer knowledge into different recommendation domains and cold-start items. 我々は、モデルがユーザーの嗜好を学習し、言語表現に基づいてアイテムを推薦し、異なる推薦ドメインやコールドスタートアイテムに知識を転送することを支援する学習フレームワークを設計する。

- Extensive experiments are conducted to show the effectiveness of our method. Results show that Recformer outperforms baselines for sequential recommendation and largely improves knowledge transfer as shown by zero-shot and cold-start settings. 本手法の有効性を示すため、広範な実験を行った。 その結果、Recformerは逐次推薦においてベースラインを上回り、ゼロ・ショットとコールド・スタート設定によって示されるように、知識伝達を大きく改善することが示された。

# Methodology 方法論

In this section, we present Recformer which can learn language representations for sequential recommendation and effectively transfer and generalize to new recommendation scenarios.
本節では、逐次推薦のための言語表現を学習し、新しい推薦シナリオに効果的に移行・汎化できるRecformerを紹介する。

## Problem Setup and Formulation 問題の設定と定式化

In the setting of sequential recommendation, we are given an item set I and a user’s interaction sequence 𝑠 = {𝑖1,𝑖2, .
逐次推薦の設定では、アイテム集合Iとユーザーの対話シーケンス𝑠 = {𝑖1,𝑖2, .
..
..
,𝑖𝑛} in temporal order where 𝑛 is the length of𝑠 and 𝑖 ∈ I.
𝑖𝑛}を時間順に並べたもので、𝑛は𝑠の長さ、𝑖∈Iである。
Based on 𝑠, we seek to predict the next item.
𝑠に基づいて、次の項目を予測する。
In previous sequential recommendation methods, each interacted item𝑖 is associated with a unique item ID.
これまでの逐次推薦法では、各インタラクト項目𝑖は一意の項目IDと関連付けられている。
In this paper, each item 𝑖 has a corresponding attribute dictionary 𝐷𝑖 containing key-value attribute pairs {(𝑘1, 𝑣1), (𝑘2, 𝑣2), .
本稿では、各項目𝑖は、キーと値の属性ペア{(𝑘1, 𝑣2, (𝑘2), ...}を含む対応する属性辞書𝐷𝑖を持つ。
..
..
, (𝑘𝑚, 𝑣𝑚)} where 𝑘 denotes an attribute name (e.g., Color) and 𝑣 is the corresponding value (e.g., Black).
↪Ll_1D45A, (↪Ll_1D458, ↪Ll_1D45A)} ここで、↪Ll_1D458 は属性名（例：Color）、𝑣 は対応する値（例：Black）を表す。
𝑘 and 𝑣 are both described by natural languages and contain words (𝑘, 𝑣) = {𝑤 𝑘 1 , .
𝑘と↪Ll453↩はどちらも自然言語で記述され、単語 (𝑘, 𝑣) = {𝑘 1 , .
..
..
,𝑤𝑘 𝑐 ,𝑤𝑣 1 , .
𝑤𝑐 ,𝑤𝑣 1 , .
..
..
,𝑤𝑣 𝑐 }, where 𝑤 𝑘 and 𝑤 𝑣 are words of 𝑘 and 𝑣 from a shared vocabulary in the language model and 𝑐 denotes the truncated length of text.
ここで、𝑣 と 𝑣 は言語モデルで共有される語彙の𝑤 と 𝑤 の単語、𝑐 と 𝑣 はテキストの切り捨てられた長さを表す。
An attribute dictionary 𝐷𝑖 can include all kinds of item textual information such as titles, descriptions, colors, etc.
属性辞書𝐷𝑖には、タイトル、説明、色など、あらゆる種類のアイテムのテキスト情報を含めることができます。
As shown in Figure 2, to feed the attribute dictionary 𝐷𝑖 into a language model, we flatten key-value attribute pairs into 𝑇𝑖 = {𝑘1, 𝑣1, 𝑘2, 𝑣2, .
図2に示すように、属性辞書𝐷𝑖を言語モデルに入力するために、キーと値の属性ペアを𝑇𝑖 = {𝑘1,𝑣2,𝑣2, .
..
..
, 𝑘𝑚, 𝑣𝑚} to obtain an item “sentence” as the input data.
, 𝑚, ↪Ll_1D45A} を入力データとして、項目「文」を得る。
Unlike previous sequential recommenders [12, 37] using both text and item IDs, in this study, we use only text for the sequential recommendation.
テキストとアイテムIDの両方を使用する以前の逐次推薦器[12, 37]とは異なり、本研究では逐次推薦にテキストのみを使用する。

## Recformer ♪リフォーマー

Figure 3 (a) shows the architecture of Recformer.
図3（a）はRecformerのアーキテクチャを示している。
The model has a similar structure as Longformer [2] which adopts a multi-layer bidirectional Transformer [30] with an attention mechanism that scales linearly with sequence length.
このモデルはLongformer[2]と同様の構造を持ち、多層双方向トランスフォーマー[30]を採用し、配列の長さに応じて線形にスケールするアテンションメカニズムを持つ。
We consider only computing efficiency for using Longformer but our method is open to other bidirectional Transformer structures such as BERT [6] and BigBird [36].
我々は、Longformerを使用する場合の計算効率のみを考慮するが、我々の方法は、BERT [6]やBigBird [36]のような他の双方向トランスフォーマー構造にもオープンである。

### Model Inputs. モデルの入力。

As introduced in Section 2.1, for each item 𝑖 and corresponding attribute dictionary 𝐷𝑖 , we flatten the dictionary into an item “sentence”𝑇𝑖 = {𝑘1, 𝑣1, 𝑘2, 𝑣2, .
セクション2.1で紹介したように、各項目𝑖と対応する属性辞書𝐷𝑖について、辞書を項目「文」𝑇𝑖 = {𝑘1,𝑣2,𝑣2, ...に平坦化する。
..
..
, 𝑘𝑚, 𝑣𝑚} where 𝑘 and 𝑣 are described by words, formally (𝑘, 𝑣) = {𝑤 𝑘 1 , .
𝑘, 𝑚, 𝑣, 𝑓}ここで、𝑘と𝑓は単語で記述され、形式的には (𝑘, 𝑣) = {𝑘 1 , .
..
..
,𝑤𝑘 𝑐 ,𝑤𝑣 1 , .
𝑤𝑐 ,𝑤𝑣 1 , .
..
..
,𝑤𝑣 𝑐 }.
𝑤𝑣 𝑐 }.
To encode a user’s interaction sequence 𝑠 = {𝑖1,𝑖2, .
ユーザーのインタラクションシーケンス𝑠 = {𝑖1,𝑖2, .
..
..
,𝑖𝑛}, we first reverse items in a sequence to {𝑖𝑛,𝑖𝑛−1, .
𝑖𝑛}とすると、まず、{𝑖𝑛,𝑖𝑛-1, .
..
..
,𝑖1} because intuitively recent items (i.e., 𝑖𝑛,𝑖𝑛−1, .
𝑖1}は、直感的に最近の項目（すなわち、𝑖𝑛,𝑖𝑛-1, .
..
..
) are important for the next item prediction and reversed sequences can make sure recent items are included in the input data.
)は次のアイテムの予測に重要であり、順序を逆にすることで最近のアイテムが入力データに含まれていることを確認することができる。
Then, we use the item “sentences” to replace items and add a special token [CLS] at the beginning of sequences.
そして、アイテムの置換にアイテム「センテンス」を使用し、シーケンスの先頭に特別なトークン[CLS]を追加する。
Hence, model inputs are denoted as:
したがって、モデルの入力は次のように表記される：

$$
\tag{1}
$$

where 𝑋 is a sequence of words containing all items and corresponding attributes the user interacted with in the historical interactions.
ここで𝑋は、過去の相互作用の中でユーザーが相互作用したすべての項目と対応する属性を含む単語のシーケンスである。

### Embedding Layer. レイヤーを埋め込む。

The target of Recformer is to understand the model input 𝑋 from both language understanding and sequential patterns in recommendations.
Recformerの目標は、言語理解とレコメンデーションの逐次的パターンの両方からモデル入力𝑋を理解することである。
The key idea in our work is to combine the embedding layers from language models [6, 21] and self-attentive sequential recommenders [14, 27].
我々の研究で重要なアイデアは、言語モデル[6, 21]と自己アテンション型逐次レコメンダー[14, 27]の埋め込みレイヤーを組み合わせることである。
Hence, Recformer contains four embeddings as follows:
したがって、Recformerは以下の4つの埋め込みを含んでいる：

- Token embedding represents the corresponding tokens. We denote the word token embedding by A ∈ R 𝑉𝑤 ×𝑑 , where 𝑉𝑤 is the number of words in our vocabulary and 𝑑 is the embedding dimension. Recformer does not have item embeddings as previous sequential recommenders and hence Recformer understands items in interaction sequences mainly based on these token embeddings. The size of token embeddings is a constant for different recommendation scenarios; hence, our model size is irrelevant to the number of items. トークン埋め込みは、対応するトークンを表す。 ここで、ǔ は語彙の単語数、ǔ は埋め込み次元である。 Recformerはこれまでの逐次推薦器のようなアイテムの埋め込みを持っていないため、Recformerは主にこれらのトークン埋め込みに基づいて相互作用シーケンスのアイテムを理解する。 トークンの埋め込みサイズは、異なる推薦シナリオに対して一定である。したがって、我々のモデルのサイズはアイテム数に関係ない。

- Token position embedding represents the position of tokens in a sequence. A word appearing at the 𝑖-th position in the sequence 𝑋 is represented as B𝑖 ∈ R 𝑑 . Similar to language models, token position embedding is designed to help Transformer understand the sequential patterns of words. トークン位置埋め込みは、シーケンス内のトークンの位置を表す。 配列𝑋の𝑖番目の位置に現れる単語は、B𝑖∈R ↪Ll_1D451 と表される。 言語モデルと同様に、トークン位置埋め込みは、Transformerが単語の連続パターンを理解するのを助けるように設計されている。

- Token type embedding represents where a token comes from. Specifically, the token type embedding totally contains three vectors C[CLS], CKey, CValue ∈ R 𝑑 to represent if a token comes from [CLS], attribute keys, or attribute values respectively. Different types of tokens usually have different importance for the next item prediction. For example, because most items usually have the same attribute keys in a recommendation dataset, models with token type embedding will recognize repeated words from the same attribute keys. トークン型の埋め込みは、トークンがどこから来たかを表す。 具体的には、トークンタイプエンベッディングは、3つのベクトルC[CLS], CKey, CValue∈R ᑑを含み、トークンがそれぞれ[CLS]、属性キー、属性値から来るかどうかを表します。 通常、トークンの種類によって、次のアイテムの予測における重要度が異なる。 例えば、推薦データセットでは、ほとんどの項目が同じ属性キーを持っているので、トークン型の埋め込みを行うモデルは、同じ属性キーから繰り返される単語を認識する。

- Item position embedding represents the position of items in a sequence. A word from attributes of the 𝑘-th item in the sequence 𝑋 is represented as D𝑘 ∈ R 𝑑 and D ∈ R 𝑛×𝑑 where 𝑛 is the maximum length of a user’s interaction sequence 𝑠. Same as previous self-attentive sequential recommenders [14, 27], the item position embedding is a key component for item sequential pattern learning. In Recformer, the item position embedding can also help the model learn the alignment between word tokens and items 項目の位置埋め込みは、シーケンス内の項目の位置を表す。 シーケンス𝑋の𝑘番目の項目の属性からの単語は、D𝑘とD∈R 𝑛×𝑑として表現される（𝑛はユーザーの対話シーケンス𝑠の最大長）。 これまでの自己注意型逐次推薦器[14, 27]と同様に、アイテム位置埋め込みはアイテム逐次パターン学習の重要な要素である。 Recformerでは、アイテムの位置の埋め込みは、単語トークンとアイテムの間のアライメントを学習するのにも役立つ。

Therefore, given a word 𝑤 from the input sequence 𝑋, the input embedding is calculated as the summation of four different embeddings followed by layer normalization [1]:
したがって、入力シーケンス𝑋から単語ǔが与えられると、入力埋め込みは、4つの異なる埋め込みとレイヤーの正規化の和として計算される[1]：

$$
\tag{2}
$$

where E𝑤 ∈ R 𝑑 .
ここで、E𝑤∈ R𝑑 。
The embedding of model inputs 𝑋 is a sequence of E𝑤,
モデル入力𝑋の埋め込みは、E𝑤のシーケンスである、

$$
\tag{3}
$$

where E𝑋 ∈ R (𝑙+1)×𝑑 and 𝑙 is the maximum length of tokens in a user’s interaction sequence.
ここで、E𝑋∈R (𝑙+1)×𝑙はユーザーの対話シーケンスにおけるトークンの最大長である。

### Item or Sequence Representations. アイテムまたはシーケンスの表現。

To encode E𝑋 , we employ the bidirectional Transformer structure Longformer [2] as our encoder.
E𝑋を符号化するために、双方向トランスフォーマー構造Longformer [2]をエンコーダーとして採用する。
Because 𝑋 is usually a long sequence, the local windowed attention in Longformer can help us efficiently encode E𝑋 .
𝑋は通常長いシーケンスなので、Longformerの局所的な窓付きアテンションは、E𝑋を効率的に符号化するのに役立つ。
As the standard settings in Longformer for document understanding, the special token [CLS] has global attention but other tokens use the local windowed attention.
文書理解のためのLongformerの標準設定として、特別なトークン[CLS]はグローバルなアテンションを持つが、他のトークンはローカルなウィンドウアテンションを使う。
Hence, Recformer computes 𝑑-dimensional word representations as follows:
したがって、Recformerは次のように↪L_1D451↩次元の単語表現を計算する：

$$
\tag{4}
$$

where h𝑤 ∈ R 𝑑 .
ここで h_1D464 は R 𝑑 である。
Similar to the language models used for sentence representations, the representation of the first token h[CLS] is used as the sequence representation.
文の表現に使用される言語モデルと同様に、最初のトークンh[CLS]の表現がシーケンス表現として使用される。
In Recformer, we do not maintain an embedding table for items.
Recformerでは、アイテムの埋め込みテーブルを保持しない。
Instead, we view the item as a special case of the interaction sequence with only one item.
その代わりに、アイテムは1つしかない相互作用シーケンスの特別なケースとみなす。
For each item 𝑖, we construct its item “sentence” 𝑇𝑖 and use 𝑋 = {[CLS],𝑇𝑖 } as the model input to get the sequence representation h[CLS] as the item representation h𝑖 .
各項目𝑖について、その項目「文」𝑇𝑖を構成し、𝑋 = {[CLS],𝑇𝑖 }をモデル入力として、配列表現h[CLS]を項目表現h𝑖として得る。

### Prediction. 予想

We predict the next item based on the cosine similarity between a user’s interaction sequence 𝑠 and item 𝑖.
ユーザーの対話シーケンス𝑠とアイテム𝑖の余弦類似度に基づいて次のアイテムを予測する。
Formally, after obtaining the sequence representation h𝑠 and the item representation h𝑖 as introduced in Section 2.2.3, we calculate the scores between 𝑠 and 𝑖 as follows:
形式的には、2.2.3節で紹介したシーケンス表現h_460と項目表現h𝑖を得た後、𝑠と𝑖のスコアを以下のように計算する：

$$
\tag{5}
$$

where 𝑟𝑖,𝑠 ∈ R is the relevance of item 𝑖 being the next item given 𝑠.
ここで、𝑟𝑖,↪Ll_1D460∈R は、𝑠が与えられたとき、項目𝑖が次の項目であることの関連性である。
To predict the next item, we calculate 𝑟𝑖,𝑠 for all items 2 in the item set I and select item with the highest 𝑟𝑖,𝑠 as the next item:
次の項目を予測するために、項目セットIのすべての項目2についてᵅ𝑖,𝑠を計算し、最も高いᵅ𝑖,𝑠を持つ項目を次の項目として選択する：

$$
\tag{6}
$$

where ˆ𝑖𝑠 is the predicted item given user interaction sequence 𝑠.
ここで、ˆ𝑖𝑠はユーザー対話シーケンス𝑠から予測される項目である。

## Learning Framework 学習フレームワーク

To have an effective and efficient language model for the sequential recommendation, we propose our learning framework for Recformer including pre-training and two-stage finetuning.
逐次推薦のための効果的で効率的な言語モデルを持つために、事前学習と2段階の微調整を含むRecformerの学習フレームワークを提案する。

### Pre-training. 事前トレーニング

The target of pre-training is to obtain a highquality parameter initialization for downstream tasks.
事前トレーニングの目的は、下流タスクのための高品質なパラメータ初期化を得ることである。
Different from previous sequential recommendation pre-training methods which consider only recommendations, we need to consider both language understanding and recommendations.
レコメンデーションのみを考慮した従来の逐次レコメンデーション事前学習法とは異なり、言語理解とレコメンデーションの両方を考慮する必要がある。
Hence, to pre-train Recformer, we adopt two tasks: (1) Masked Language Modeling (MLM) and (2) an item-item contrastive task.
そこで、Recformerを事前に学習させるために、2つのタスクを採用した： 
(1)マスク言語モデリング(MLM)と(2)項目-項目対照タスクである。
Masked Language Modeling (MLM) [6] is an effective pre-training method for language understanding and has been widely used for various NLP pre-training tasks such as sentence understanding [8], phrase understanding [18].
マスク言語モデリング（MLM）[6]は、言語理解のための効果的な事前学習手法であり、文の理解[8]、フレーズの理解[18]など、様々なNLPの事前学習タスクに広く利用されている。
Adding MLM as an auxiliary task will prevent language models from forgetting the word semantics when models are jointly trained with other specific tasks.
補助タスクとしてMLMを追加することで、モデルが他の特定のタスクと共同で学習される際に、言語モデルが単語の意味を忘れてしまうことを防ぐことができる。
For recommendation tasks, MLM can also eliminate the language domain gap between a general language corpus and item texts.
推薦タスクの場合、MLMは一般的な言語コーパスとアイテムテキストとの間の言語ドメインギャップをなくすこともできる。
In particular, following BERT [6], the training data generator chooses 15% of the token positions at random for prediction.
特に、BERT [6]に従い、訓練データ生成器はトークン位置の15%を予測用にランダムに選択する。
If the token is selected, we replace the token with (1) the [MASK] with probability 80%; (2) a random token with probability 10%; (3) the unchanged token with probability 10%.
トークンが選択された場合、トークンを(1) 80%の確率で[MASK]、(2) 10%の確率でランダムなトークン、(3) 10%の確率で変更前のトークンに置き換える。
The MLM loss is calculated as:
MLMの損失は次のように計算される：

$$
\tag{7}
$$

$$
\tag{8}
$$

$$
\tag{9}
$$

where Wℎ ∈ R 𝑑×𝑑 , bℎ ∈ R 𝑑 , W0 ∈ R |V |×𝑑 , b0 ∈ R |V | , GELU is the GELU activation function [10] and V is the vocabulary used in the language model.
V

Another pre-training task for Recformer is the item-item contrastive (IIC) task which is widely used in the next item prediction for recommendations.
Recformerのもう一つの事前学習タスクは、レコメンデーションの次のアイテム予測に広く使われているIIC（item-item contrastive）タスクである。
We use the ground-truth next items as positive instances following previous works [12, 14, 27].
我々は、先行研究[12, 14, 27]に従い、グランド・トゥルースの次の項目をポジティブ・インスタンスとして使用する。
However, for negative instances, we adopt in-batch next items as negative instances instead of negative sampling [14] or fully softmax [12, 27].
ただし、負インスタンスについては、負サンプリング[14]や完全ソフトマックス[12, 27]の代わりに、バッチ内次アイテムを負インスタンスとして採用する。
Previous recommenders maintain an item embedding table, hence they can easily retrieve item embeddings for training and update embeddings.
これまでの推薦者は、項目埋め込みテーブルを保持しており、学習や埋め込み更新のために項目埋め込みを簡単に取り出すことができる。
In our case, item embeddings are from Recformer, so it is infeasible to re-encode items (from sampling or full set) per batch for training.
私たちの場合、項目の埋め込みはRecformerによるものであるため、学習のためにバッチごとに（サンプリングまたはフルセットから）項目を再エンコードすることは不可能である。
In-batch negative instances [3] are using ground truth items of other instance sequences in the same batch as negative items.
バッチ内負インスタンス[3]は、負アイテムとして、同じバッチ内の他のインスタンスシーケンスのグランドトゥルースアイテムを使用する。
Although it is possible to provide false negatives, false negatives are less likely in the pre-training dataset with a large size.
偽陰性を提供する可能性はあるが、サイズが大きい事前学習データセットでは偽陰性の可能性は低い。
Furthermore, the target of pre-training is to provide high-quality initialized parameters and we have the finetuning with accurate supervision for downstream tasks.
さらに、事前学習の目標は、高品質の初期化されたパラメータを提供することであり、下流のタスクのために正確な監視による微調整を行う。
Therefore, we claim that inbatch negatives will not hurt the recommendation performance but have much higher training efficiency than accurate supervision.
したがって、インバッチネガティブは推薦性能を損なわず、正確な監視よりもはるかに高い学習効率が得られると主張する。
Formally, the item-item contrastive loss is calculated as:
正式には、項目対比損失は次のように計算される：

$$
\tag{10}
$$

where sim is the similarity introduced in Equation (5); h + 𝑖 is the representation of the ground truth next item; B is the ground truth item set in one batch and 𝜏 is a temperature parameter.
ここで、simは式(5)で導入された類似度であり、h +𝑖 は次の項目の表現であり、Bは1バッチで設定されたグランドトゥルース項目であり、↪L_1D70F↩は温度パラメータである。
At the pre-training stage, we use a multi-task training strategy to jointly optimize Recformer:
事前学習段階では、マルチタスク学習戦略を用いてRecformerを共同最適化する：

$$
\tag{11}
$$

where 𝜆 is a hyper-parameter to control the weight of MLM task loss.
ここで、↪Ll_1 はMLMタスクロスの重みを制御するハイパーパラメータである。
The pre-trained model will be fine-tuned for new scenarios.
事前に訓練されたモデルは、新しいシナリオのために微調整される。

### Two-Stage Finetuning. 2段階の微調整。

Similar to pre-training, we do not maintain an independent item embedding table.
事前学習と同様に、独立したアイテム埋め込みテーブルは保持しない。
Instead, we encode items by Recformer.
その代わりに、Recformerによってアイテムをエンコードする。
However, in-batch negatives cannot provide accurate supervision in a small dataset because it is likely to have false negatives which undermine recommendation performance.
しかし、バッチ内否定は、推薦性能を損なう偽否定が発生する可能性が高いため、小さなデータセットでは正確な監視を提供できない。
To solve this problem, we propose two-stage finetuning as shown in Algorithm 1.
この問題を解決するために、アルゴリズム1に示すような2段階の微調整を提案する。
The key idea is to maintain an item feature matrix I ∈ R | I |×𝑑 .
I
Different from the item embedding table, I is not learnable and all item features are encoded from Recformer.
アイテム埋め込みテーブルとは異なり、Iは学習可能ではなく、すべてのアイテムの特徴はRecformerからエンコードされる。
As shown in Algorithm 1, our proposed finetuning method has two stages.
アルゴリズム1に示すように、我々の提案するファインチューニング法には2つの段階がある。
In stage 1, I is updated (line 4) per epoch,3 whereas, in stage 2 we freeze I and update only parameters in model 𝑀.
ステージ1では、Iはエポックごとに更新される（4行目）3が、ステージ2ではIを凍結し、モデルǔのパラメータのみを更新する。
The basic idea is that although the model is already pre-trained, item representations from the pre-trained model can still be improved by further training on downstream datasets.
基本的な考え方は、モデルはすでに事前訓練されているが、事前訓練されたモデルからの項目表現は、下流のデータセットでさらに訓練することで改善できるということである。
It is expensive to re-encode all items in every batch hence we re-encode all items in every epoch to update I (line 4) and use I as supervision for item-item contrastive learning (line 5).
バッチごとに全項目を再エンコードするのはコストがかかるので、エポックごとに全項目を再エンコードしてIを更新し（4行目）、Iを項目-項目対比学習のスーパービジョンとして使用する（5行目）。
After obtaining the best item representations, we re-initialize the model with the corresponding parameters (line 12) and start stage 2.
最適な項目表現が得られたら、対応するパラメータでモデルを再初期化し（12行目）、ステージ2を開始する。
Since I keeps updating in stage 1, the supervision for finetuning is also changing.
第1ステージでアップデートを繰り返しているので、微調整のための監督も変わってきている。
In this case, the model is hard to be optimized to have the best performance.
この場合、モデルを最適化するのは難しい。
Therefore, we freeze I and continue training the model until achieving the best performance on the validation dataset.
そこで、Iを凍結し、検証データセットで最高の性能を達成するまでモデルの訓練を続ける。
The learning task used in finetuning is item-item contrastive learning which is the same as pre-training but with fully softmax instead of in-batch negatives.
ファインチューニングで使用される学習タスクは項目対比学習であり、これは事前学習と同じであるが、バッチ内否定の代わりに完全なソフトマックスを使用する。
The finetuning loss is calculated as:
微調整ロスは次のように計算される：

$$
\tag{12}
$$

where I𝑖 is the item feature of item 𝑖.
ここで、I𝑖は項目𝑖の項目特徴である。

## Discussion 

In this section, we briefly compare Recformer to other sequential recommendation methods to highlight the novelty of our method.
このセクションでは、Recformerと他の逐次推薦法を簡単に比較し、我々の手法の新規性を強調する。
Traditional sequential recommenders such as GRU4Rec [11], SASRec [14] and BERT4Rec [27] rely on item IDs and corresponding trainable item embeddings to train a sequential model for recommendations.
GRU4Rec [11]、SASRec [14]、BERT4Rec [27]のような従来の逐次レコメンダーは、レコメンデーションのための逐次モデルを学習するために、アイテムIDと対応する学習可能なアイテム埋め込みに依存している。
These item embeddings are learned from sequential patterns of user interactions.
これらのアイテム埋め込みは、ユーザーとのインタラクションの連続パターンから学習される。
However, as mentioned in [20], these approaches suffer from data sparsity and can not perform well with cold-start items.
しかし、[20]で述べられているように、これらのアプローチはデータのスパース性に悩まされ、コールドスタートアイテムではうまく機能しない。
To reduce the dependence on item IDs, some context-aware sequential recommenders such as UniSRec [12], S3 -Rec [38], ZESRec [7] are proposed to incorporate side information (e.g., categories, titles) as prior knowledge for recommendations.
アイテムIDへの依存を減らすために、UniSRec [12]、S3 -Rec [38]、ZESRec [7]のようなコンテキストを考慮した逐次推薦器が提案されている。
All of these approaches rely on a feature extractor such as BERT [6] to obtain item feature vectors and then fuse these vectors into item representations with an independent sequential model.
これらのアプローチはすべて、BERT [6]のような特徴抽出器に依存して、項目特徴ベクトルを取得し、次 にこれらのベクトルを独立逐次モデルで項目表現に融合する。
In this paper, we explore conducting sequential recommendations in a new paradigm that learns language representations for the next item recommendations.
本稿では、次のアイテムを推薦するための言語表現を学習する新しいパラダイムで、逐次推薦を行うことを探求する。
Instead of trainable item embeddings or fixed item features from language models, we bridge the gap between natural language understanding and sequential recommendation to directly learn representations of items and user sequences based on words.
学習可能な項目埋め込みや言語モデルからの固定項目特徴の代わりに、自然言語理解とシーケンシャル・レコメンデーションのギャップを埋め、単語に基づいて項目とユーザーシーケンスの表現を直接学習する。
We expect the generality of natural language can improve the transferability of recommenders in order to benefit new domain adaptation and cold-start item understanding
自然言語の一般性は、新たなドメイン適応やコールドスタートの項目理解のために、レコメンダーの移植性を向上させることができると期待している。

# Experiments 実験

In this section, we empirically show the effectiveness of our proposed model Recformer and learning framework.
このセクションでは、我々の提案するモデルRecformerと学習フレームワークの有効性を実証的に示す。

## Experimental Setup 実験セットアップ

### Datasets. データセット

To evaluate the performance of Recformer, we conduct pre-training and finetuning on different categories of Amazon review datasets [22].
Recformerの性能を評価するために、我々はAmazonレビューデータセットの異なるカテゴリーに対して事前学習と微調整を行った[22]。
The statistics of datasets after preprocessing are shown in Table 1.
前処理後のデータセットの統計を表1に示す。
For pre-training, seven categories are selected as training data including “Automotive”, “Cell Phones and Accessories”, “Clothing Shoes and Jewelry”, “Electronics”, “Grocery and Gourmet Food”, “Home and Kitchen”, “Movies and TV”, and one category “CDs and Vinyl” is left out as validation data.
事前学習では、「自動車」、「携帯電話・アクセサリー」、「衣類・靴・宝飾品」、「電子機器」、「食料品・グルメ食品」、「家庭・台所」、「映画・テレビ」の7カテゴリを学習データとして選択し、検証データとして「CD・レコード」の1カテゴリを除外した。
Datasets from these categories are used as source domain datasets.
これらのカテゴリのデータセットが、ソース・ドメインのデータセットとして使用される。
For finetuning, we select six categories including “Industrial and Scientific”, “Musical Instruments”, “Arts, Crafts and Sewing”, “Office Products”, “Video Games”, “Pet Supplies”, as target domain datasets to evaluate Recformer.
Recformerを評価するために、"Industrial and Scientific"、"Musical Instruments"、"Arts, Crafts and Sewing"、"Office Products"、"Video Games"、"Pet Supplies "の6つのカテゴリーをターゲット・ドメイン・データセットとして選択する。
For pre-training and finetuning, we use the five-core datasets provided by the data source and filter items whose title is missing.
事前学習と微調整には、データソースから提供された5コアのデータセットを使用し、タイトルが欠落しているアイテムをフィルタリングする。
Then we group the interactions by users and sort them by timestamp ascendingly.
次に、ユーザーごとにインタラクションをグループ化し、タイムスタンプの昇順でソートする。
Following previous work [12], we select item attributes title, categories and brand as key-value pairs for items.
先行研究[12]に従い、アイテムのタイトル、カテゴリー、ブランドの属性をアイテムのキーと値のペアとして選択する。

### Baselines. ベースライン

We compare three groups of works as our baselines which include methods with only item IDs; methods using item IDs and treating item text as side information; and methods using only item texts as inputs.
アイテムIDのみを使用する方法、アイテムIDを使用し、アイテムテキストをサイド情報として扱う方法、アイテムテキストのみを入力として使用する方法の3つのグループをベースラインとして比較する。

- (1) ID-Only methods: • GRU4Rec [11] adopts RNNs to model user action sequences for session-based recommendations. We treat each user’s interaction sequence as a session. • SASRec [14] uses a directional self-attentive model to capture item correlations within a sequence. • BERT4Rec [27] employs a bi-directional self-attentive model with the cloze objective for modeling user behavior sequences. • RecGURU [16] proposes to pre-train sequence representations with an autoencoder in an adversarial learning paradigm. We do not consider overlapped users for this method in our setting. (2) ID-Text methods: • FDSA [37] uses a self-attentive model to capture item and feature transition patterns.• S 3 -Rec [38] pre-trains sequential models with mutual information maximization to learn the correlations among attributes, items, subsequences, and sequences. (3) Text-Only methods: • ZESRec [7] encodes item texts with a pre-trained language model as item features. We pre-train this method and finetune the model on six downstream datasets. • UniSRec [12] uses textual item representations from a pretrained language model and adapts to a new domain using an MoE-enhance adaptor. We initialize the model with the pre-trained parameters provided by the authors and finetune the model on target domains. (1)IDのみの手法 
- GRU4Rec [11]は、セッションベースの推薦のために、ユーザーの行動シーケンスをモデル化するためにRNNを採用する。 各ユーザーのインタラクション・シーケンスをセッションとして扱う。 - SASRec [14]は、シーケンス内の項目相関を捕捉するために、方向性自己注視モデルを使用している。 - BERT4Rec [27]は、ユーザーの行動シーケンスをモデル化するために、クロース目的による双方向自己注 意モデルを採用している。 - RecGURU[16]は、敵対的学習パラダイムにおいて、オートエンコーダでシーケンス表現を事前学習することを提案している。 (2)ID-Text法： 
- FDSA[37]は、項目と特徴の遷移パターンを捉えるために、自己学習モデルを用いる。 - S 3 -Rec[38]は、属性、項目、部分列、シーケンス間の相関を学習するために、相互情報最大化で逐次モデルを事前学習する： 
- ZESRec [7]は、事前に学習された言語モデルを用いて、項目のテキストを項目の特徴としてエンコードする。 この方法を事前に訓練し、6つのダウンストリームデータセットでモデルを微調整する。 - UniSRec [12]は、事前に学習された言語モデルからテキスト項目表現を使用し、MoE-enhanceアダプターを使用して新しいドメインに適応する。 我々は、著者から提供された事前訓練されたパラメータでモデルを初期化し、ターゲットドメイン上でモデルを微調整する。

### Evaluation Settings. 評価設定。

To evaluate the performance of sequential recommendation, we adopt three widely used metrics NDCG@N, Recall@N and MRR, where N is set to 10.
逐次推薦の性能を評価するために、NDCG@N、Recall@N、MRRの3つの広く使われている指標を採用する。
For data splitting of finetuning datasets, we apply the leave-one-out strategy [14] for evaluation: the most recent item in an interaction sequence is used for testing, the second most recent item for validation and the remaining data for training.
ファインチューニングデータセットのデータ分割のために、評価のためにリーブワンアウト戦略[14]を適用する： 
相互作用のシーケンスの中で最も新しい項目がテストに、2番目に新しい項目が検証に、そして残りのデータがトレーニングに使用される。
We rank the ground-truth item of each sequence among all items for evaluation and report the average scores of all sequences in the test data.
各シーケンスのグランドトゥルースアイテムを全アイテムの中でランク付けして評価し、テストデータに含まれる全シーケンスの平均スコアを報告する。

### Implementation Details. 実施内容

We build Recformer based on Longformer implemented by Huggingface 4 .
Huggingface4で実装されたLongformerをベースにRecformerを構築する。
For efficient computing, we set the size of the local attention windows in Longformer to 64.
効率的な計算のために、Longformerのローカルアテンションウィンドウのサイズを64に設定した。
The maximum number of tokens is 32 for each attribute and 1,024 for each interaction sequence (i.e., 𝑋 in Equation (1)).
トークンの最大数は、各属性について32個、各相互作用シーケンスについて1,024個である（すなわち、式（1）の𝑋）。
The maximum number of items in a user sequence is 50 for all baselines and Recformer.
ユーザー・シーケンスの最大アイテム数は、すべてのベースラインとRecformerで50である。
The temperature parameter 𝜏 is 0.05 and the weight of MLM loss 𝜆 is 0.1.Other than token type embedding and item position embedding in Recformer, other parameters are initialized with pre-trained parameters of Longformer 5 before pre-training.
温度パラメータᵰは0.05、MLM損失の重み𝜆は0.1である。Recformerのトークン型埋め込みとアイテム位置埋め込み以外のパラメータは、事前学習前にLongformer 5の事前学習済みパラメータで初期化されている。
The batch size is 64 for pre-training and 16 for finetuning.
バッチサイズは、事前学習用に64、微調整用に16である。
We optimize Recformer with Adam optimizer with learning rate 5e-5 and adopt early stop with the patience of 5 epochs to prevent overfitting.
学習率5e-5のアダム・オプティマイザでRecformerを最適化し、オーバーフィッティングを防ぐために5エポックの忍耐で早期停止を採用する。
For baselines, we use the suggested settings introduced in [12].
ベースラインについては、[12]で紹介されている推奨設定を使用する。

## Overall Performance 総合成績

We compare Recformer to baselines on six datasets across different recommendation domains.
Recformerとベースラインとの比較を、異なる推薦領域にわたる6つのデータセットで行う。
Results are shown in Table 2.
結果を表2に示す。
For baselines, ID-Text methods (i.e., FDSA and S3 -Rec) achieve better results compared to ID-Only and Text-Only methods in general.
ベースラインについては、ID-Text法（すなわち、FDSAとS3 -Rec）は、一般的にID-Only法やText-Only法よりも良い結果を達成している。
Because ID-Text methods include item IDs and content features, they can learn both content-based information and sequential patterns from finetuning.
ID-Textメソッドは、アイテムIDとコンテンツ特徴を含むため、コンテンツベースの情報と、微調整によるシーケンシャルパターンの両方を学習することができる。
Comparing Text-Only methods and ID-Only methods, we can find that on the Scientific, Instruments, and Pet datasets, Text-Only methods perform better than ID-Only methods.
テキストのみのメソッドとIDのみのメソッドを比較すると、科学、機器、ペットのデータセットでは、テキストのみのメソッドの方がIDのみのメソッドよりも性能が良いことがわかる。
A possible reason is that the item transitions in these three datasets are highly related to item texts (i.e., title, brand) hence text-only methods can recommend the next item based on content similarity.
考えられる理由としては、これら3つのデータセットにおけるアイテム遷移は、アイテムのテキスト（タイトルやブランドなど）と関連性が高いため、テキストのみの手法では、内容の類似性に基づいて次のアイテムを推薦することができる。
Our proposed method Recformer, achieves the best overall performance on all datasets except the Recall@10 of Instruments.
提案手法Recformerは、InstrumentsのRecall@10を除く全てのデータセットで最高の総合性能を達成した。
Recformer improves the NDCG@10 by 15.83% and MRR by 15.99% on average over the second best results.
RecformerはNDCG@10を15.83%改善し、MRRを15.99%改善した。
Different from baselines, Recformer learns language representations for sequential recommendation without pre-trained language models or item IDs.
ベースラインとは異なり、Recformerは事前に学習した言語モデルやアイテムIDを使わずに、逐次推薦のための言語表現を学習する。
With two-stage finetuning, Recformer can be effectively adapted to downstream domains and transferred knowledge from pre-training can consistently benefit finetuning tasks.
2段階の微調整により、Recformerは下流のドメインに効果的に適応することができ、事前学習から伝達された知識は微調整タスクに一貫して役立つ。
The results illustrate the effectiveness of the proposed Recformer.
この結果は、提案するRecformerの有効性を示している。

## Low-Resource Performance 低リソース・パフォーマンス

### Zero-Shot. ゼロショット。

To show the effectiveness of pre-training, we evaluate the zero-shot recommendation performance of three TextOnly methods (i.e., UniSRec, ZESRec, Recformer) and compare results to the average scores of three ID-Only methods fully trained on downstream datasets.
事前学習の有効性を示すために、3つのTextOnly手法（UniSRec、ZESRec、Recformer）のゼロショット推薦性能を評価し、ダウンストリームデータセットで完全に訓練された3つのID-Only手法の平均スコアと結果を比較する。
The zero-shot recommendation setting requires models to learn knowledge from pre-training datasets and directly test on downstream datasets without further training.
ゼロショット推薦の設定では、モデルが事前学習データセットから知識を学習し、さらに学習することなく下流のデータセットで直接テストする必要がある。
Hence, traditional ID-based methods cannot be evaluated in this setting.
したがって、従来のIDベースの手法は、この設定では評価できない。
We evaluate the knowledge transferability of Text-Only methods in different recommendation scenarios.
様々な推薦シナリオにおいて、テキストのみの手法の知識伝達性を評価する。
All results in six downstream datasets are shown in Figure 4.
6つのダウンストリームデータセットの全結果を図4に示す。
Overall, Recformer improves the zero-shot recommendation performance compared to UniSRec and ZESRec on six datasets.
全体として、Recformerは6つのデータセットにおいてUniSRecやZESRecと比較してゼロショット推薦の性能を向上させた。
On the Scientific dataset, Recformer performs better than the average performance of three ID-Only methods trained with full training sets.
Scientificデータセットでは、Recformerは、完全な訓練セットで訓練された3つのID-Only手法の平均性能よりも優れている。
These results show that (1) natural language is promising as a general item representation across different recommendation scenarios; (2) Recformer can effectively learn knowledge from pre-training and transfer learned knowledge to downstream tasks based on language understanding.
これらの結果は、(1)自然言語が様々な推薦シナリオに渡る一般的な項目表現として有望であること、(2)Recformerは事前学習から知識を効果的に学習し、学習した知識を言語理解に基づいて下流のタスクに転送できることを示している。

### Low-Resource. 低資源。

We conduct experiments with SASRec, UniSRec and Recformer in low-resource settings.
SASRec、UniSRec、Recformerを使った実験を低リソース環境で行った。
In this setting, we train models on downstream datasets with different ratios of training data and results are shown in Figure 5.
この設定で、学習データの比率を変えたダウンストリームデータセットでモデルを学習し、結果を図5に示す。
We can see that methods with item text (i.e., UniSRec and Recformer) outperform ID-only method SASRec especially when less training data is available.
特に学習データが少ない場合、項目テキストを含む方法（すなわちUniSRecとRecformer）がIDのみの方法SASRecを上回ることがわかる。
This indicates UniSRec and Recformer can incorporate prior knowledge and do recommendations based on item texts.
これは、UniSRecとRecformerが事前知識を取り入れ、アイテムのテキストに基づいたレコメンデーションを行えることを示している。
In low-resource settings, most items in the test set are unseen during training for SASRec.
低リソース環境では、SASRecの学習中にテストセットのほとんどの項目が未見となる。
Therefore, the embeddings of unseen items are randomly initialized and cannot provide high-quality representations for recommendations.
そのため、未見のアイテムの埋め込みはランダムに初期化され、レコメンデーションのための高品質な表現を提供することはできない。
After being trained with adequate data, SASRec could rapidly improve its performance.
適切なデータで訓練された後、SASRecは急速に性能を向上させることができた。
Recformer achieves the best performance over different ratios of training data.
Recformerは、学習データの比率を変えても最高の性能を発揮する。
On the Scientific dataset, Recformer outperforms other methods by a large margin with 1% and 5% of training data.
Scientificデータセットでは、Recformerは1%と5%の学習データで他の手法に大きな差をつけた。

## Further Analysis さらなる分析

### Performance w.r.t. Cold-Start Items. パフォーマンス コールドスタート・アイテム

In this section, we simulate this scenario by splitting a dataset into two parts, i.e., an in-set dataset and cold-start dataset.
この節では、データセットを2つの部分、すなわちインセット・データセットとコールドスタート・データセットに分割して、このシナリオをシミュレートする。
Specifically, for the in-set dataset, we make sure all test items appear in the training data and all other test items (never appearing in training data) will be sent to the cold-start dataset.
具体的には、インセット・データセットでは、すべてのテスト項目がトレーニング・データに現れるようにし、それ以外のテスト項目（トレーニング・データに現れることはない）はコールドスタート・データセットに送られるようにする。
We train models on in-set datasets and test on both in-set and cold-start datasets.
インセット・データセットでモデルを学習し、インセット・データセットとコールドスタート・データセットの両方でテストする。
In this case, models never see the cold-start items during training and item embedding tables do not contain cold-start items.
この場合、モデルは学習中にコールドスタートのアイテムを見ることはなく、アイテム埋め込みテーブルにはコールドスタートのアイテムは含まれない。
We compare the ID-only method SASRec and the Text-only method UniSRec to Recformer.
IDのみのSASRecとテキストのみのUniSRecをRecformerと比較する。
For ID-based SASRec, we substitute items appearing only once in the training set with a cold token and after training, we add this cold token embedding to cold-start item embeddings to provide prior knowledge 6 .
IDベースのSASRecでは、学習セットに一度だけ出現するアイテムをコールドトークンで置き換え、学習後、このコールドトークンの埋め込みをコールドスタートのアイテム埋め込みに追加し、事前知識を提供する6 。
For UniSRec, cold-start items are represented by item texts and encoded by BERT which is identical to seen items.
UniSRecでは、コールドスタート項目は項目テキストで表現され、BERTで符号化される。
Recformer directly encode item texts to represent cold-start items.
Recformerは、コールドスタートのアイテムを表現するために、アイテムのテキストを直接エンコードする。
Experimental results are shown in Table 3.
実験結果を表3に示す。
We can see that Text-Only methods significantly outperform SASRec, especially on datasets with a large size (i.e., Arts, Pet).
特にサイズの大きいデータセット（ArtsやPetなど）では、テキストのみの手法がSASRecを大きく上回ることがわかる。
Because of randomly initialized cold-start item representations, the performance of SASRec is largely lower on cold-start items than in-set items.
コールドスタート項目の表現がランダムに初期化されるため、SASRecの性能はインセット項目よりもコールドスタート項目で大きく低下する。
Hence, IDonly methods are not able to handle cold-start items and applying text is a promising direction.
したがって、IDのみの方法ではコールドスタートのアイテムを扱うことができず、テキストを適用することが有望な方向性である。
For Text-only methods, Recformer greatly improves performance on both in-set and cold-start datasets compared to UniSRec which indicates learning language representations is superior to obtaining text features for recommendations.
テキストのみの手法の場合、RecformerはUniSRecと比較して、インセットとコールドスタートの両方のデータセットでパフォーマンスを大幅に向上させる。これは、推薦のためのテキスト特徴を得るよりも、言語表現を学習する方が優れていることを示している。

### Ablation Study. アブレーション研究。

We analyze how our proposed components influence the final sequential recommendation performance.
提案する構成要素が最終的な逐次推薦の性能にどのような影響を与えるかを分析する。
The results are shown in Table 4.
結果を表4に示す。
We introduce the variants and analyze their results respectively.
それぞれの変種を紹介し、その結果を分析する。
We first test the effectiveness of our proposed two-stage finetuning.
まず、我々の提案する2段階のファインチューニングの有効性をテストする。
In variant (1) w/o two-stage finetuning, we do not update item feature matrix I and only conduct finetuning based on I from pre-trained parameters.
2段階の微調整を行わないバリエーション(1)では、項目特徴行列Iの更新は行わず、事前に学習したパラメータからIに基づく微調整のみを行う。
We find that compared to (0) Recformer, (1) has similar results on Scientific but has a large margin on Instruments since the pre-trained model has better pre-trained item representations on Scientific compared to Instruments (shown in Figure 4).
その結果、(0)のRecformerと比較して、(1)はScientificでは同じような結果を示すが、Instrumentsでは大きなマージンを持つことがわかった（図4）。
Hence, our proposed two-stage finetuning can effectively improve the sub-optimal item representations from pre-training and further improve performance on downstream datasets.
従って、我々の提案する2段階のファインチューニングは、事前学習による最適でない項目表現を効果的に改善し、下流のデータセットでの性能をさらに向上させることができる。
Then, we investigate the effects of freezing/trainable word embeddings and item embeddings.
次に、凍結/学習可能な単語埋め込みと項目埋め込みの効果を調べる。
In our default setting (1), we freeze the item feature matrix I and train word embeddings of Recformer.
デフォルトの設定(1)では、項目特徴行列Iを凍結し、Recformerの単語埋め込みを学習する。
In variants (2)(3)(4), we try to train the item feature matrix or freeze word embeddings.
バリエーション(2)(3)(4)では、項目特徴行列または凍結単語埋め込みを学習しようとする。
Overall, on the Scientific dataset, the model with fixed item embeddings performs better than the model with trainable item embeddings, whereas on the Instruments dataset, our model performs well when item embeddings are trainable.
全体として、Scientificデータセットでは、項目埋め込みを固定したモデルの方が、項目埋め込みを学習可能なモデルよりも性能が良いが、Instrumentsデータセットでは、項目埋め込みが学習可能な場合、我々のモデルの方が性能が良い。
The divergence can be eliminated by our two-stage finetuning strategy.
この発散は、2段階の微調整戦略によって解消できる。
Variant (5) w/o pre-training finetunes Recformer from scratch.
バリエーション(5) プリ・トレーニングなし ゼロからリコンストラクターを調整する。
We can see that (0) Recformer significantly outperforms Variant (5) in both datasets because without pre-training, the item feature matrix I is not trained and cannot provide informative supervision during finetuning even if we update I by two-stage finetuning.
これは、事前学習なしでは、項目特徴行列Iが学習されていないため、2段階のファインチューニングによってIを更新しても、ファインチューニング中に有益な監視を提供できないからである。
These results show the effectiveness of pre-training.
これらの結果は、事前トレーニングの有効性を示している。
Finally, we explore the effectiveness of our proposed model structure (i.e., item position embeddings and token type embeddings).
最後に、提案するモデル構造（すなわち、項目位置埋め込みとトークン型埋め込み）の有効性を探る。
Variant (6) removes the two embeddings and results show that the model in (6) causes performance decay on the instruments dataset which indicates the two embeddings are necessary when the gap between pre-training and finetuning is large.
変形(6)は、2つの埋め込みを削除し、結果は、(6)のモデルは、事前学習と微調整の間のギャップが大きい場合に2つの埋め込みが必要であることを示す、計器データセット上で性能減衰を引き起こすことを示している。

### Pre-training Steps vs. Performance. トレーニング前のステップとトレーニング後のステップの比較 パフォーマンス

We investigate the zeroshot sequential recommendation performance on downstream tasks over different pre-training steps and results on four datasets are shown in Figure 6.
ゼロショット逐次レコメンデーションの性能を、異なる事前学習ステップの下流タスクで調査し、4つのデータセットでの結果を図6に示す。
The pre-training of natural language understanding usually requires a large number of training steps to achieve a promising result.
自然言語理解の事前学習は通常、有望な結果を得るために多くの学習ステップを必要とする。
However, we have a different situation in sequential recommendation.
しかし、逐次推薦では事情が異なる。
From Figure 6, we can see that most datasets already achieve their best performance after around 4,000 training steps and further pre-training may hurt the knowledge transferability on downstream tasks.
図6から、ほとんどのデータセットは4,000ステップ程度の学習ですでに最高の性能を達成しており、これ以上の事前学習は下流のタスクでの知識伝達性を損なう可能性があることがわかる。
We think there are two possible reasons: (1) We initialize most parameters from a Longformer model pre-trained by the MLM task.
考えられる理由は2つある： 
(1) MLMタスクによって事前に訓練されたLongformerモデルからほとんどのパラメータを初期化する。
In this case, the model already has some essential knowledge of natural languages.
この場合、モデルはすでに自然言語に関する本質的な知識を持っている。
The domain adaptation from a general language understanding to the item text understanding for recommendations should be fast.(2) Even if we include seven categories in the training data, there is still a language domain difference between pre-training data and downstream data since different item categories have their own specific vocabularies.
一般的な言語理解からレコメンデーションのためのアイテムテキスト理解へのドメイン適応は高速であるべきである。(2) 学習データに7つのカテゴリを含めたとしても、アイテムカテゴリにはそれぞれ固有の語彙があるため、事前学習データと下流データには言語ドメインの違いがある。
For instance, the category Electronics has quite different words in item text compared to the Pets category.
例えば、「エレクトロニクス」カテゴリーと「ペット」カテゴリーでは、アイテムのテキストに含まれる単語がかなり異なっている。

# Related Work 関連作品

## Sequential Recommendation 

Sequential recommendation [11, 14, 27] aims to predict the next item based on historical user interactions.
逐次推薦[11, 14, 27]は、過去のユーザーインタラクションに基づいて次のアイテムを予測することを目的としている。
Proposed methods model user interactions as a sequence ordered by their timestamps.
提案された方法は、ユーザーのインタラクションをタイムスタンプによって並べられたシーケンスとしてモデル化する。
Due to the ability to capture the long-term preferences and short-term dynamics of users, sequential recommendation methods show their effectiveness for personalization and attract a lot of studies.
ユーザーの長期的な嗜好と短期的なダイナミクスを捉えることができるため、逐次レコメンデーション手法はパーソナライゼーションに有効であり、多くの研究が行われている。
Early works [9, 25] apply the Markov Chain to model item-item transition relations based on matrix factorization.
初期の研究[9, 25]では、マルコフ連鎖を応用して、行列分解に基づいて項目-項目の遷移関係をモデル化している。
For deep learning methods, Convolutional Sequence Embedding (Caser) [28] views the embedding matrix of previous items as an “image” and applies convolutional operations to extract transitions.
ディープラーニングの手法としては、Convolutional Sequence Embedding（Caser）[28]が、過去のアイテムの埋め込み行列を「画像」とみなし、畳み込み演算を適用して遷移を抽出する。
GRU4Rec [11] introduces Gated Recurrent Units (GRU) [5] to model user sequential patterns.
GRU4Rec [11]は、Gated Recurrent Units (GRU) [5]を導入し、ユーザーのシーケンシャルパターンをモデル化する。
With the development of the Transformer [30], recent studies [14, 27] widely use self-attention model for sequential recommendation.
Transformer[30]の開発により、最近の研究[14, 27]では、逐次推薦に自己注意モデルが広く使われている。
Although these approaches achieve promising performance, they struggle to learn transferable knowledge or understand cold-start items due to the dependence on IDs and item embeddings which are specific to items and datasets.
これらのアプローチは有望な性能を達成しているが、項目やデータセットに固有のIDや項目埋め込みに依存しているため、転移可能な知識を学習したり、コールドスタート項目を理解したりするのに苦労している。
Recently, researchers attempt to employ textual features as transferable item representations [7, 12].
最近では、転送可能な項目表現としてテキスト特徴を採用する試みがなされている[7, 12]。
These methods first obtain item features by encoding item texts with language models and then learn transferable item representations with an independent sequential model.
これらの方法は、まず言語モデルで項目テキストを符号化することによって項目の特徴を取得し、次に独立した逐次モデルで転送可能な項目表現を学習する。
Independent language understanding and sequential pattern learning still limit the capacity of the model to learn user interactions based on languages.
独立した言語理解と逐次的なパターン学習は、言語に基づいてユーザーのインタラクションを学習するモデルの能力をまだ制限している。
In this paper, we explore unifying the language understanding and sequential recommendations into one Transformer framework.
本稿では、言語理解と逐次レコメンデーションを1つのTransformerフレームワークに統合することを探求する。
We aim to have a sequential recommendation method that can effectively model cold-start items and learn transferable sequential patterns for different recommendation scenarios.
我々は、コールドスタート項目を効果的にモデル化し、様々な推薦シナリオに対して転送可能な順序パターンを学習できる逐次推薦手法を持つことを目指している。

## Transfer Learning for Recommendation 推薦のための転移学習

Data sparsity and cold-start item understanding issues are challenging in recommender systems and recent studies [33, 39, 40] explore transferring knowledge across different domains to improve the recommendation at the target domain.
最近の研究[33, 39, 40]では、ターゲットドメインでの推薦を改善するために、異なるドメイン間で知識を転送することを探求している。
Previous methods for knowledge transfer mainly rely on shared information between the source and target domains including common users [13, 31, 32, 35], items [26, 39] or attributes [29].
これまでの知識移転の方法は、主に共通のユーザー[13, 31, 32, 35]、項目[26, 39]、属性[29]など、ソースとターゲットのドメイン間で共有される情報に依存している。
To learn common item features from different domains, pre-trained language models [6, 21] provide high-quality item features by encoding item texts (e.g., title, brand).
異なるドメインから共通のアイテム特徴を学習するために、事前に学習された言語モデル[6, 21]は、アイテムのテキスト（例：タイトル、ブランド）を符号化することにより、高品質のアイテム特徴を提供する。
Based on pre-trained item features, several methods [7, 12] are proposed to learn universal item representations by applying additional layers.
事前に学習された項目特徴に基づき、追加レイヤーを適用することで普遍的な項目表現を学習する方法[7, 12]がいくつか提案されている。
In this work, we have the same target as previous transfer learning for recommendation (i.e., alleviate data sparsity and cold-start item issues).
本研究では、これまでの推薦のための転移学習と同じ目標を掲げている（すなわち、データのスパース性とコールドスタート項目の問題を緩和する）。
However, instead of relying on common users, items and attributes or encoding items with pre-trained language models, we directly learn language representations for sequential recommendation and hence transfer knowledge based on the generality of natural languages.
しかし、一般的なユーザー、アイテム、属性に依存したり、事前に訓練された言語モデルでアイテムをエンコードしたりするのではなく、逐次推薦のための言語表現を直接学習することで、自然言語の一般性に基づく知識の伝達を行う。

# Conclusion 結論

In this paper, we propose Recformer, a framework that can effectively learn language representations for sequential recommendation.
本稿では、逐次推薦のための言語表現を効果的に学習するフレームワークRecformerを提案する。
To recommend the next item based on languages, we first formulate items as key-value attribute pairs instead of item IDs.
言語に基づいて次のアイテムを推薦するために、まずアイテムをアイテムIDではなく、キーと値の属性ペアとして定式化する。
Then, we propose a novel bi-directional Transformer model for sequence and item representations.
次に、シーケンス表現とアイテム表現のための新しい双方向変換モデルを提案する。
The proposed structure can learn both natural languages and sequential patterns for recommendations.
提案された構造は、推薦のための自然言語と逐次パターンの両方を学習することができる。
Furthermore, we design a learning framework including pretraining and finetuning that helps the model learn to recommend based on languages and transfer knowledge into different recommendation scenarios.
さらに、事前学習と微調整を含む学習フレームワークを設計し、言語に基づいて推薦することを学習し、異なる推薦シナリオに知識を伝達することを支援する。
Finally, extensive experiments are conducted to evaluate the effectiveness of Recformer under full-supervised and low-resource settings.
最後に、Recformerの有効性を評価するために、完全教師ありの設定と低リソース設定の下で広範な実験を行った。
Results show that Recformer largely outperforms existing methods in different settings, especially for the zero-shot and cold-start items recommendation which indicates Recformer can effectively transfer knowledge from training.
その結果、Recformerは様々な設定において既存の手法を大きく上回った。特に、ゼロショットとコールドスタートの推薦項目においては、Recformerが訓練から効果的に知識を伝達できることを示している。
An ablation study is conducted to show the effectiveness of our proposed components.
提案したコンポーネントの有効性を示すため、アブレーション試験を実施した。