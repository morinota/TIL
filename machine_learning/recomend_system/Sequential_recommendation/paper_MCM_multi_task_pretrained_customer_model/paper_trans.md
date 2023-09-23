## Link リンク

- https://dl.acm.org/doi/10.1145/3604915.3608868 https://dl.acm.org/doi/10.1145/3604915.3608868

## title タイトル

MCM: A Multi-task Pre-trained Customer Model for Personalization
MCM： 
パーソナライゼーションのためのマルチタスク事前学習済み顧客モデル

## abstract 抄録

Personalization plays a critical role in helping customers discover the products and contents they prefer for e-commerce stores.Personalized recommendations differ in contents, target customers, and UI.
パーソナライズされたレコメンデーションは、コンテンツ、ターゲット顧客、UIが異なります。
However, they require a common core capability - the ability to deeply understand customers’ preferences and shopping intents.
しかし、これらには共通のコア能力、つまり顧客の嗜好や購買意図を深く理解する能力が必要である。
In this paper, we introduce the MCM (Multi-task pre-trained Customer Model), a large pre-trained BERT-based multi-task customer model with 10 million trainable parameters for e-commerce stores.
本論文では、1,000万個の学習可能なパラメータを持つ、BERTベースの大規模な事前学習済みマルチタスク顧客モデルであるMCM（Multi-task pre-trained Customer Model）を紹介する。
This model aims to empower all personalization projects by providing commonly used preference scores for recommendations, customer embeddings for transfer learning, and a pre-trained model for fine-tuning.
このモデルは、レコメンデーションによく使われるプリファレンス・スコア、転移学習のための顧客エンベッディング、微調整のための事前学習済みモデルを提供することで、あらゆるパーソナライゼーション・プロジェクトに力を与えることを目的としている。
In this work, we improve the SOTA BERT4Rec framework to handle heterogeneous customer signals and multi-task training as well as innovate new data augmentation method that is suitable for recommendation task.
本研究では、SOTA BERT4Recフレームワークを改良し、異種顧客信号やマルチタスク学習を扱えるようにするとともに、推薦タスクに適した新たなデータ補強法を考案した。
Experimental results show that MCM outperforms the original BERT4Rec by 17% on on NDCG@10 of next action prediction tasks.
実験の結果、次の行動予測タスクのNDCG@10において、MCMはオリジナルのBERT4Recを17%上回った。
Additionally, we demonstrate that the model can be easily fine-tuned to assist a specific recommendation task.
さらに、このモデルは特定の推薦タスクを支援するために容易に微調整できることを実証する。
For instance, after fine-tuning MCM for an incentive based recommendation project, performance improves by 60% on the conversion prediction task and 25% on the click-through prediction task compared to a baseline tree-based GBDT model.
例えば、インセンティブベースの推薦プロジェクト用にMCMを微調整した結果、ベースラインのツリーベースのGBDTモデルと比較して、コンバージョン予測タスクで60%、クリックスルー予測タスクで25%パフォーマンスが向上した。

# Introduction はじめに

In a personalized recommendation system, it is critical to understand each customer’s preference and shopping intent holistically based on customers’ profile as well as comprehensive historical behaviors like browsing, searching and purchasing signals.
パーソナライズド・レコメンデーション・システムでは、顧客のプロフィールだけでなく、ブラウジング、検索、購買シグナルなどの包括的な過去の行動に基づいて、各顧客の嗜好とショッピングの意図を総合的に理解することが重要である。
Ecommerce stores usually have tens of billions of customer historical behavior data.
Eコマースストアは通常、何百億という顧客の過去の行動データを持っている。
These signals, if learned with a large capacity model, can help to provide the grounding of customers understanding and be utilized by thousands of downstream use cases.
これらの信号は、大容量モデルで学習すれば、顧客の理解の基礎となり、何千もの下流のユースケースで活用される。
Bert-based pretrained model like GPT has been successful in NLP and CV [4, 5, 8], Researchers in recommendation field explore Bert-based model on specific task like session-based recommendation [9], under the setting of sequential recommendation [2, 3, 6, 7].
GPTのようなBertベースの事前学習済みモデルは、NLPやCV[4, 5, 8]で成功しており、推薦分野の研究者は、逐次推薦[2, 3, 6, 7]の設定下で、セッションベースの推薦[9]のような特定のタスクでBertベースのモデルを研究している。
However, large-scale pre-training with Bert is still largely under-explored in the field of recommender systems.
しかし、Bertを使った大規模な事前学習は、推薦システムの分野ではまだほとんど研究されていない。
In this paper, we propose Multi-task pre-trained Customer Model (MCM) model: a large-capacity Bert-based multi-task model with 10 million trainable parameters, pre-trained on a vast amount of behavior data from a large e-commence service.
本稿では、マルチタスク事前学習済み顧客モデル(MCM)を提案する： 
これは、大規模なeコマースサービスの膨大な行動データを用いて事前学習された、1,000万個の学習可能なパラメータを持つ大容量のBertベースのマルチタスクモデルである。
We make architectural improvements for better pre-training, which will be explained in more detail in the model section.
より良い事前学習のためにアーキテクチャを改良しているが、これについてはモデルのセクションで詳しく説明する。
Offline results show that MCM outperform the original Bert4rec on multi-tasks by average 17% on NDCG@10 of next action prediction.
オフラインの結果、MCMはマルチタスクにおいて、次の行動予測のNDCG@10において、オリジナルのBert4recを平均17%上回った。
In order to evaluate the ability to support new personalization tasks, we fine-tune the model for an incentive offer recommendation task, the performance improves by 60% on conversion rate and 25% on click-through rate, compared to the baseline GBDT model.
新しいパーソナライゼーションタスクをサポートする能力を評価するために、インセンティブオファーの推薦タスク用にモデルを微調整したところ、ベースラインのGBDTモデルと比較して、コンバージョン率で60%、クリックスルー率で25%パフォーマンスが向上しました。

# Methodology 方法論

## Model Framework モデルフレームワーク

MCM consists of three modules: embedding module, sequential encoding module and readout module1.
MCMは3つのモジュールで構成されている： 
エンベデッドモジュール、シーケンシャルエンコーディングモジュール、リードアウトモジュール1。
We inherited the sequential encoding module from Bert4rec, while make algorithm improvements on the other two modules, which we will introduce in more detail in the following sessions.
Bert4recの逐次エンコードモジュールを継承しつつ、他の2つのモジュールにアルゴリズムの改良を加えた。

### Heterogeneous Embedding Module. ヘテロジニアス・エンベッディング・モジュール。

In this module, we convert the raw inputs into distributed representations through embedding lookup, as is typically done in bert-based models.
このモジュールでは、バートベースのモデルで一般的に行われるように、埋め込みルックアップを通して生の入力を分散表現に変換する。
The original input is a heterogeneous interaction sequence including purchase actions and non-purchase actions.
元の入力は、購入行動と非購入行動を含む異種交流シーケンスである。
Non-purchase actions are actions that are High Value Actions (HVAs) customers have with the e-commerce stores, e.g.member sign-up, mobile camera search, click records of products etc.
非購買アクションとは、会員登録、携帯カメラ検索、商品のクリック記録など、顧客がEC店舗で行うHVA（High Value Action）となるアクションのこと。
Instead of feeding the raw inputs into the embedding module, we choose to represent each interaction 𝑖 with a set of features 𝑓 𝑗 𝑖 , 𝑗 ∈ 1, 2, ..., |𝐽 |, where |𝐽 | denotes the total number of features for each interaction.
𝐽
Now the inputs of each customer𝑐 are |𝐽 | sequences, with the 𝑗-th sequence in the form of 𝐹 𝑗 = [𝑓 (𝑗) 1 , 𝑓 (𝑗) 2 , ..., 𝑓 (𝑗) 𝑛𝑖 ].
𝐽
Currently, the features include the hierarchical structures of the product: product line, category, subcategory as well as brand.
現在、この機能には商品の階層構造が含まれている： 
製品ライン、カテゴリー、サブカテゴリー、ブランド。
Additionally, we design a feature called token type to handle heterogeneous input, making it easier for the model to differentiate different types of interactions.
さらに、トークン・タイプと呼ばれる機能を設計し、異種入力を扱うことで、モデルが異なるタイプの相互作用を区別しやすくしている。
Each distinct feature value is assigned a unique embedding vector.
各特徴値には固有の埋め込みベクトルが割り当てられる。
After the embedding look-up, the inputs are converted to |𝐽 | sequences of embeddings, we perform average pooling to these sequences, producing a single embedding sequence 𝑬 = [𝒆1, 𝒆2, ..., 𝒆𝒏𝒊 ].
𝐽
The bert model requires position embedding to capture the order of sequences, we adopt learnable position embeddings 𝑃 for better performance, which is randomly initialized learnable parameters.
bertモデルは、シーケンスの順序をキャプチャするために位置埋め込みを必要とするため、より良いパフォーマンスを得るために学習可能な位置埋め込みᵄを採用し、これはランダムに初期化された学習可能なパラメータである。
The output of the embedding module is then
埋め込みモジュールの出力は次のようになる。

$$
\tag{1}
$$

### Task-Aware Attentional Readout Module. タスクを意識した注意読み出しモジュール。

The output of the sequential encoding module is a sequence of hidden vectors, with the same length as the input sequence.
逐次符号化モジュールの出力は、入力シーケンスと同じ長さの隠れベクトルのシーケンスである。
Previous work[9] computes the inner product between the last hidden vector and the item embedding to produce the score for the corresponding item.
先行研究[9]は、最後の隠れベクトルと項目埋め込みとの内積を計算し、対応する項目のスコアを生成する。
This can be sub-optimal since the last hidden vector is a fixed representation of the whole behavior sequence, which is not aware of the specific item or task to predict.
最後の隠れベクトルは行動シーケンス全体の固定表現であり、予測する特定のアイテムやタスクを意識していないため、これは最適とは言えない可能性がある。
Different tasks may be related to different behaviors within the whole behavior sequence.
異なるタスクは、行動シーケンス全体の中で異なる行動に関連しているかもしれない。
We propose a novel task-aware attentional readout module, which allows different items (labels in each task) and different tasks to attend to different subsequences of the hidden sequence with attention mechanism , in order to produce a task-specific representation.
我々は、タスクを意識した新しい注意読み出しモジュールを提案する。このモジュールは、タスクに特化した表現を生成するために、異なるアイテム（各タスクのラベル）と異なるタスクが、注意メカニズムによって、隠れシーケンスの異なる部分シーケンスに注目することを可能にする。
Specifically, let 𝒉𝒊 denote the 𝑖-th embedding of the output of the sequential encoding module, and let 𝒆𝒘 denote the embedding for a particular item 𝑤 in a certain task, the attentional readout operation can be described as:
具体的には、逐次符号化モジュールの出力の𝑖番目の埋め込みをǔ↪Ll_1D48A とし、あるタスクの特定の項目𝑤に対する埋め込みを𝒘とすると、注意読み出し操作は次のように記述できる：

$$
\tag{2}
$$

where 𝒓𝑤 is the representation of the input sequence, specific to item 𝑤.
ここで、↪L_1D493↩𝑤はアイテム𝑤に固有の入力シーケンスの表現である。
The predicted score for item 𝑤 is:
項目𝑤の予測スコアは次のようになる：

$$
\tag{3}
$$

Softmax operation is performed on the scores to produce the final distribution.
最終的な分布を生成するために、スコアに対してソフトマックス演算が実行される。

## Model Learning with prefix-augmentation プレフィックス拡張によるモデル学習

Previous work[9] on sequential recommendation adopt a popular augmentation method in NLP called masked language model, which randomly masks out some tokens in the input sequence and asks the model to predict them based on all other tokens.
逐次推薦に関する先行研究[9]では、マスキング言語モデルと呼ばれる、自然言語処理でよく使われる補強手法を採用している。これは、入力シーケンスの中のいくつかのトークンをランダムにマスクし、他のすべてのトークンを基に予測するようモデルに求めるものである。
Such augmentation is suitable for language modeling, but we believe it can be problematic for recommendation tasks since it leaks future information.
このような補強は言語モデリングには適しているが、推薦タスクでは将来の情報が漏れてしまうため、問題があると我々は考えている。
We propose a new augmentation method called random prefix augmentation, which randomly samples a prefix from the whole input sequence, and ask the model to predict the last item.
我々は、ランダム接頭辞補強と呼ばれる新しい補強方法を提案する。これは、入力シーケンス全体からランダムに接頭辞をサンプリングし、モデルに最後の項目を予測させるものである。
In this case, the input will only include the items before the last item, so that our augmentation avoids leaking future information.
この場合、入力には最後の項目より前の項目しか含まれないので、我々の補強は将来の情報が漏れるのを避けることができる。
For example, suppose the original input sequence is [𝑖1,𝑖2,𝑖3], valid prefixes include [𝑖1] and [𝑖1,𝑖2].
例えば、元の入力シーケンスが[𝑖1,𝑖2,𝑖3]だとすると、有効な接頭辞は[𝑖1]と[𝑖1,𝑖2]である。
The augmentation is performed at batch time rather than during data pre-processing, in order to save memory.
メモリを節約するため、増強はデータの前処理中ではなく、バッチ時に実行される。
The loss function for each prefix is defined as the negative loglikelihood of the label item (the last item):
各前頭辞の損失関数は、ラベル項目（最後の項目）の負の対数尤度として定義される：

$$
\tag{4}
$$

where 𝑖𝑔𝑡 denotes the ground truth item, S denotes the input sequence, which contains all items but the last one.
ここで、𝑖𝑔𝑡は基底真理項目を表し、Sは最後の項目以外のすべての項目を含む入力シーケンスを表す。
For multi-task
マルチタスク用

training, the loss of all tasks are summed together.
トレーニングでは、すべてのタスクの損失が合計される。

# Experiment 実験

## Experiment Setup 実験セットアップ

### Datasets and Evaluation Details. データセットと評価の詳細

To train our models, we use data from a large e-commerce service.
私たちのモデルを訓練するために、大規模な電子商取引サービスのデータを使用します。
We use customer behaviour data sampled from 6 years customer history.
6年間の顧客履歴からサンプリングした顧客行動データを使用しています。
The dataset consists of 40M customers and 10B interactions.
データセットは40Mの顧客と10Bのインタラクションで構成されている。
The behavior sequence includes three types of interactions: item purchases, item clicks and customer valuable actions.
行動シーケンスには3種類のインタラクションが含まれる： 
アイテムの購入、アイテムのクリック、顧客の価値あるアクションです。
For each purchase and click interaction, we use products’ hierarchical features including product line (PL), category, subcategory as well as brands.
各購買とクリックのインタラクションには、プロダクトライン（PL）、カテゴリー、サブカテゴリー、ブランドを含む商品の階層的特徴を使用する。
To note, these features are also the tasks we train the model to predict on customer’s next preferences.
これらの特徴は、顧客の次の嗜好を予測するためにモデルを訓練するタスクでもある。
As suggested in [1], we split the dataset into training, validation and testing dataset by time to avoid leaking future information.
1]で提案されているように、将来の情報漏えいを避けるために、データセットを時間ごとにトレーニング、検証、テストデータセットに分割する。
We adopt ranking metrics for evaluation, the primary metric is NDCG (Normalized Discounted Cumulative Gain), as well as recall and precision.
評価にはランキングメトリクスを採用し、主なメトリクスはNDCG（正規化割引累積利得）、およびリコールと精度である。
The Bert encoder consists of three transfomer layers, the head number is four.
バートエンコーダーは3つのトランスフォーマー層で構成され、ヘッド数は4である。
The maximum sequence length is truncated to 300.
最大配列長は300に切り詰められる。

## Quality of Preference Scores 

We first compare the performance between our model and a SOTA sequential recommendation model Bert4rec.
まず、我々のモデルとSOTA逐次推薦モデルBert4recの性能を比較する。
As illustrated in Table.1, MCM_final significantly outperforms bert4rec by about 11%.
表.1に示すように、MCM_finalはbert4recを約11%大幅に上回る。
We also conduct ablation experiments with variants of MCM model MCM_Single and MCM_MTL.
また、MCMモデルMCM_SingleとMCM_MTLの変異体を用いたアブレーション実験も行った。
Compared to Bert4rec, MCM_Single utilizs heterogeneous interaction sequence and contextual features to train each single task, and MCM_MTL utilizs attentional readout and MTL.
Bert4recと比較して、MCM_Singleは各単一タスクの訓練に異種相互作用シーケンスと文脈特徴を利用し、MCM_MTLは注意読み出しとMTLを利用する。
MCM-Final utilizes heterogeneous data, attentional readout and pre-fix data augmentation.
MCM-Finalは、ヘテロジニアスデータ、アテンションリードアウト、プレフィックスデータ補強を利用する。
The results show that richer input signals contribute to the incrementality the most, while MTL and prefix augmentation are also helpful.
その結果、豊富な入力信号がインクリメンタリティに最も寄与することが示され、MTLと接頭辞補強も有効であることがわかった。

## Extensibility of MCM MCMの拡張性

To demonstrate the flexibility and extensibility of MCM, we give a detailed example showing how to modify and fine-tune the model on a next action recommendation use case.
MCMの柔軟性と拡張性を実証するために、次のアクションを推奨するユースケースについて、どのようにモデルを修正し、微調整するかを示す詳細な例を示す。
This task aims to encourage customers to complete one action task by providing incentives (e.g.cash backs).
このタスクは、インセンティブ（キャッシュバックなど）を提供することで、顧客に1つのアクションタスクの完了を促すことを目的としている。
There are in total 28 tasks, including purchasing from a new product line (i.e., the product line that the customer never bought before) and trying new services like camera search or prime video streaming service.
タスクは全部で28あり、新しい商品ライン（つまり、顧客がこれまで買ったことのない商品ライン）からの購入や、カメラ検索やプライム・ビデオ・ストリーミング・サービスのような新しいサービスを試すことも含まれる。
The multi-task prediction scores from MCM model have covered the tasks and can be directly utilized, however it may not reflect customers’ behaviors with incentives.
MCMモデルによるマルチタスク予測スコアは、タスクをカバーしており、直接活用することができるが、インセンティブによる顧客の行動を反映していない可能性がある。
So we add a new head on top of the sequential encoder to predict the incentive effect and fine-tune the model with customer behavior data under incentives: 30K action clicks and completion(conversion) records.
そこで、シーケンシャルエンコーダの上に新しいヘッドを追加し、インセンティブ効果を予測し、インセンティブ下の顧客行動データを使ってモデルを微調整する： 
30Kアクションのクリックと完了（コンバージョン）の記録。
From the results, MCM significantly outperforms a tree-based GBDT task prediction model by 25% on conversion NDCG, and fine-tuned model (MCM_finetuned) outperforms the MCM model without fine-tuning by 35% on conversion NDCG, which in total drives over 60% improvement on conversion rate as compared to tree-based GBDT model.
その結果、MCMは木ベースのGBDTタスク予測モデルを変換NDCGで25%大きく上回り、微調整モデル（MCM_finetuned）は微調整なしのMCMモデルを変換NDCGで35%上回り、合計で木ベースのGBDTモデルと比較して変換率を60%以上改善した。

# Conclusion 結論

In this paper, we introduce MCM, a large pre-trained customer model that serves as a sequential multi-task recommendation model to support diverse personalization projects.
本稿では、多様なパーソナライゼーション・プロジェクトを支援する逐次マルチタスク推薦モデルとして機能する、事前に学習された大規模な顧客モデルMCMを紹介する。
Through experiments, we demonstrate the model’s ability to provide highly accurate preference predictions, which surpass the performance of other baseline models.
実験を通じて、このモデルが他のベースラインモデルの性能を凌駕する高精度の嗜好予測を提供できることを実証する。
We also showcase a detailed use case on a recommendation project, demonstrating how MCM can be extended to new tasks and deliver significant performance improvements.
また、レコメンデーション・プロジェクトに関する詳細なユースケースを紹介し、MCMがいかに新しいタスクに拡張され、大幅なパフォーマンス向上を実現できるかを実証する。

# Speaker bio スピーカーの経歴

Rui Luo and Tianxin Wang are applied scientists in Amazon, they work on recommender systems to improve customer shopping experience.
Rui LuoとTianxin Wangはアマゾンの応用科学者で、顧客の買い物体験を向上させるレコメンダー・システムを研究している。