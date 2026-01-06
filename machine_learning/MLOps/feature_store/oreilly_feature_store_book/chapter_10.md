## CHAPTER 10: Training Pipelines 第10章: トレーニングパイプライン

Model training is the broadest and deepest area of data science. 
モデルのトレーニングは、データサイエンスの中で最も広範で深い分野です。

We will cover the most important concepts and scalability challenges involved when training the full gamut of models, from decision trees with XGBoost, to deep learning at scale with Ray, to fine-tuning LLMs with low-rank adaptation (LoRA). 
私たちは、XGBoostを用いた決定木から、Rayを用いた大規模な深層学習、低ランク適応（LoRA）を用いたLLMのファインチューニングまで、さまざまなモデルのトレーニングに関わる最も重要な概念とスケーラビリティの課題を扱います。

There are many resources available to go into further depth on these topics. 
これらのトピックについてさらに深く掘り下げるためのリソースは多数存在します。

What we will focus on is mastering the yin and yang of model training: 
私たちが焦点を当てるのは、モデルトレーニングの陰と陽をマスターすることです：

_Model-centric AI_ The iterative process of improving model performance by experimenting with model architecture and tuning hyperparameters 
_モデル中心のAI_ モデルアーキテクチャを実験し、ハイパーパラメータを調整することによってモデルのパフォーマンスを改善する反復プロセス

_Data-centric AI_ The iterative process of selecting features and data to improve model performance 
_データ中心のAI_ モデルのパフォーマンスを改善するために特徴とデータを選択する反復プロセス

To become a great data scientist, you need to be good at both model-centric and data-centric training. 
優れたデータサイエンティストになるためには、モデル中心のトレーニングとデータ中心のトレーニングの両方に精通している必要があります。

With our yin and yang philosophy, we will cover the most important practical elements of training pipelines: 
私たちの陰と陽の哲学に基づき、トレーニングパイプラインの最も重要な実践的要素を扱います：

choice of learning algorithm, connecting labels to features in a feature store, feature selection, training dataset creation, model architecture, distributed training, and model evaluation. 
学習アルゴリズムの選択、フィーチャーストアにおけるラベルと特徴の接続、特徴選択、トレーニングデータセットの作成、モデルアーキテクチャ、分散トレーニング、モデル評価です。

We will also look at performance challenges for scaling model training on GPUs. 
また、GPU上でのモデルトレーニングのスケーリングに関するパフォーマンスの課題についても見ていきます。

###### Unstructured Data and Labels in Feature Groups
###### 非構造化データとフィーチャーグループにおけるラベル

In the MVPS development methodology from Chapter 2, you start by identifying the prediction problem and the data sources available to solve that problem. 
第2章のMVPS開発手法では、予測問題を特定し、その問題を解決するために利用可能なデータソースを特定することから始めます。

Prediction problems can be divided into three groups: supervised learning that requires explicit labels/targets in datasets, unsupervised learning that does not require labeled data, and self-supervised learning that creates its own labels from data. 
予測問題は、データセットに明示的なラベル/ターゲットを必要とする教師あり学習、ラベル付きデータを必要としない教師なし学習、データから独自のラベルを生成する自己教師あり学習の3つのグループに分けることができます。

Self-supervised and unsupervised learning are traditionally associated with unstructured data, such as image, audio, video, and text files. 
自己教師あり学習と教師なし学習は、伝統的に画像、音声、動画、テキストファイルなどの非構造化データに関連付けられています。

###### Self-Supervised and Unsupervised Learning
###### 自己教師あり学習と教師なし学習

Self-supervised and unsupervised learning models do not require separate labels/targets. 
自己教師あり学習と教師なし学習モデルは、別々のラベル/ターゲットを必要としません。

For example, an LLM predicts the next token in a sequence of text. 
例えば、LLMはテキストのシーケンスにおける次のトークンを予測します。

You don’t need an externally provided label, as the label is simply the next token. 
外部から提供されたラベルは必要なく、ラベルは単に次のトークンです。

Self-supervised learning is where the algorithm generates the labels automatically from the input data. 
自己教師あり学習は、アルゴリズムが入力データから自動的にラベルを生成するプロセスです。

The LLM uses the predicted next token to predict the following token, and it continues predicting tokens using previous token predictions until it predicts a stop token. 
LLMは予測された次のトークンを使用して次のトークンを予測し、停止トークンを予測するまで前のトークンの予測を使用してトークンを予測し続けます。

Models that use previous predictions as inputs are known as autoregressive models. 
前の予測を入力として使用するモデルは、自己回帰モデルとして知られています。

Autoregressive models can be unstable. 
自己回帰モデルは不安定になることがあります。

For example, in our air quality example, if you were to predict air quality seven days in advance using only lagged air quality (e.g., one, two, three days prior) as a feature, you could get error accumulation in forecasts, producing runaway predictions. 
例えば、私たちの空気質の例では、遅延した空気質（例えば、1日前、2日前、3日前）だけを特徴として使用して、7日先の空気質を予測すると、予測における誤差の蓄積が発生し、暴走する予測を生む可能性があります。

The solution is to use weather features to stabilize predictions, which makes lagged air quality a good feature so long as you don’t overfit on the lagged features. 
解決策は、予測を安定させるために気象特徴を使用することであり、遅延した空気質は遅延した特徴に過剰適合しない限り良い特徴となります。

Another self-supervised algorithm for language models is masked language modeling, as popularized with the BERT transformer model. 
言語モデルのための別の自己教師ありアルゴリズムは、BERTトランスフォーマーモデルで普及したマスク付き言語モデリングです。

During training, BERT randomly masks out (hides) target words in input text sequences and trains the language model to predict the missing words. 
トレーニング中、BERTは入力テキストシーケンス内のターゲットワードをランダムにマスク（隠す）し、言語モデルに欠落した単語を予測させるようにトレーニングします。

As BERT doesn’t use previously predicted words, it is not autoregressive. 
BERTは以前に予測された単語を使用しないため、自己回帰的ではありません。

The feature store can manage unstructured data (for unsupervised and self-supervised ML) by indexing information about its files in feature groups, making it easier to process and search for files. 
フィーチャーストアは、フィーチャーグループ内のファイルに関する情報をインデックス化することによって、非構造化データ（教師なしおよび自己教師ありML）を管理でき、ファイルの処理と検索を容易にします。

For each file in your unstructured dataset, you store a row in a feature group with metadata about the file and the path to the file. 
非構造化データセット内の各ファイルについて、ファイルに関するメタデータとファイルへのパスを含む行をフィーチャーグループに保存します。

Table 10-1 shows examples of unsupervised and self-supervised ML models and what data is stored for them in feature groups. 
表10-1は、教師なしおよび自己教師ありMLモデルの例と、それらに対してフィーチャーグループに保存されるデータを示しています。

_Table 10-1. Self-supervised and unsupervised data in feature groups does not include labels_  
**ML model** **Feature group** **Prediction problems**  
Pretrained LLMs Feature groups storing filenames and metadata for files used as training data  
Vector embeddings  
Feature groups storing features and embeddings for image, audio, and text files  
Predicting the next token.  
Self-supervised.  
ANN search. Unsupervised.  
kNN Feature groups storing features for image, audio, and text files Search/clustering. Unsupervised.  
-----
**ML model** **Feature group** **Prediction problems**  
GANs Feature groups storing filenames and metadata for image, audio, and text files  
Stable diffusion Feature groups storing filenames for images, metadata, and text descriptions for images  
Anomaly detection. Unsupervised.  
Generating images from textual descriptions. Partially unsupervised.  
k-nearest neighbor (kNN) is an unsupervised learning algorithm for (a) ANN search and (b) segmenting or clustering a set of unlabeled data points. 
k近傍法（kNN）は、(a) ANN検索および(b) ラベルのないデータポイントのセットをセグメント化またはクラスタリングするための教師なし学習アルゴリズムです。

You can also use kNN as a supervised method for classification/regression. 
kNNは、分類/回帰のための教師あり手法としても使用できます。

If you index your image/video/audio files in feature groups, you need to ensure consistency among the filepaths in your feature group to the files. 
フィーチャーグループに画像/動画/音声ファイルをインデックス化する場合、フィーチャーグループ内のファイルパスとファイルとの一貫性を確保する必要があります。

If you move/delete files, you will break the linkage. 
ファイルを移動または削除すると、リンクが切れてしまいます。

Another unsupervised learning algorithm is the _generative adversarial network_ (GAN). 
別の教師なし学習アルゴリズムは、_生成的敵対ネットワーク_（GAN）です。

GANs consist of two neural networks, a _generator and a_ _discriminator, that_ compete in a feedback loop. 
GANは、フィードバックループで競い合う2つのニューラルネットワーク、_ジェネレーター_と_ディスクリミネーター_で構成されています。

The generator creates new input data samples, while the discriminator tries to distinguish real samples from generated ones. 
ジェネレーターは新しい入力データサンプルを生成し、ディスクリミネーターは実際のサンプルと生成されたサンプルを区別しようとします。

They do not require labeled data, as learning emerges from this adversarial process, pushing the generator to produce outputs that closely resemble the original data distribution. 
彼らはラベル付きデータを必要とせず、この敵対的プロセスから学習が生まれ、ジェネレーターが元のデータ分布に近い出力を生成するように促します。

For example, a GAN trained on nonfraudulent credit card transactions can identify whether new transactions deviate significantly from the nonfraudulent examples. 
例えば、非詐欺的なクレジットカード取引で訓練されたGANは、新しい取引が非詐欺的な例から大きく逸脱しているかどうかを特定できます。

A stable diffusion network is another algorithm that includes unsupervised learning. 
安定拡散ネットワークは、教師なし学習を含む別のアルゴリズムです。

It is used to generate images from text. 
これは、テキストから画像を生成するために使用されます。

The core diffusion step in training is unsupervised learning, where the model learns to predict and remove noise to reconstruct the original input image. 
トレーニングにおけるコアの拡散ステップは教師なし学習であり、モデルはノイズを予測して除去し、元の入力画像を再構築することを学びます。

###### Supervised Learning Requires a Label
###### 教師あり学習はラベルを必要とする

For supervised learning, the starting point for your prediction problem is the labels/targets. 
教師あり学習の場合、予測問題の出発点はラベル/ターゲットです。

How do you find the labels for your prediction problem? 
予測問題のラベルをどのように見つけますか？

If you are lucky, the labels are already available, stored in a table in your data warehouse, an operational database, or files. 
運が良ければ、ラベルはすでに利用可能で、データウェアハウスのテーブル、運用データベース、またはファイルに保存されています。

Sometimes you need to write code to create the labels. 
時には、ラベルを作成するためにコードを書く必要があります。

For example, in our credit card example, we have a table `cc_fraud, which stores transactions` marked as fraud. 
例えば、私たちのクレジットカードの例では、詐欺としてマークされた取引を保存するテーブル`cc_fraud`があります。

To create labels for all transactions, we need to join the rows in `cc_fraud with the nonfraud transactions from credit_card_transactions, as` shown here: 
すべての取引のラベルを作成するために、`cc_fraud`の行を`credit_card_transactions`の非詐欺取引と結合する必要があります。以下のように示されています：

```  
fraud_df = fs.get_feature_group("cc_fraud").read()  
transactions_df = fs.get_feature_group("credit_card_transactions").read()  
transactions_df = transactions_df.merge(fraud_df, on="t_id", how="left")  
transactions_df["fraud"] = transactions_df["fraud"].fillna(0)
``` 
We use a `LEFT JOIN, implemented as a Pandas merge, so that rows in` `transactions_df that do not have a matching row in fraud_df will have a null value for fraud. 
私たちは`LEFT JOIN`を使用し、Pandasのマージとして実装しているので、`fraud_df`に一致する行がない`transactions_df`の行は、fraudに対してnull値を持つことになります。

The matching rows will have a “1” in fraud; we then set the null values to “0,” using fillna(0), for nonmatching rows. 
一致する行はfraudに「1」を持ち、一致しない行のnull値を`fillna(0)`を使用して「0」に設定します。

###### Labels for Unstructured Data
###### 非構造化データのラベル

Sometimes noncoding work is required to create labels, particularly for unstructured data. 
時には、特に非構造化データのラベルを作成するためにコーディング以外の作業が必要です。

For example, in early work on deep learning, most of the labels for image classification datasets were created by humans manually drawing bounding boxes around the parts of the image being classified. 
例えば、深層学習の初期の作業では、画像分類データセットのほとんどのラベルは、人間が手動で分類される画像の部分の周りにバウンディングボックスを描くことによって作成されました。

Manual work to label unstructured data is expensive to scale, so techniques have been developed to accelerate labeling. 
非構造化データにラベルを付けるための手作業はスケールするのが高価であるため、ラベリングを加速するための技術が開発されました。

For example, _weak supervision leverages abundant noisy label data to generate a large_ amount of weakly trusted labels. 
例えば、_弱い監視は豊富なノイズの多いラベルデータを活用して、大量の弱く信頼されたラベルを生成します_。

Sometimes, having lots of reasonable-quality labels is better than having a small number of high-quality labels. 
時には、合理的な品質のラベルがたくさんある方が、少数の高品質のラベルを持つよりも良いことがあります。

Cleanlab is a popular open source library that supports weak supervision. 
Cleanlabは、弱い監視をサポートする人気のオープンソースライブラリです。

Cleanlab can also fix/clean label data, for both unstructured and structured data. 
Cleanlabは、非構造化データと構造化データの両方のラベルデータを修正/クリーンアップすることもできます。

When you use the feature store as the source for labels, you typically start by importing the labels as a feature group. 
フィーチャーストアをラベルのソースとして使用する場合、通常はラベルをフィーチャーグループとしてインポートすることから始めます。

If the labels are an existing table in an external store, you probably can mount that table as an external feature group. 
ラベルが外部ストアにある既存のテーブルである場合、そのテーブルを外部フィーチャーグループとしてマウントできる可能性があります。

Alternatively, you can import a static dataset of labels directly into a feature group. 
あるいは、ラベルの静的データセットをフィーチャーグループに直接インポートすることもできます。

If the label data is non-static, write a batch feature pipeline to ingest the labels into a feature group. 
ラベルデータが非静的である場合、ラベルをフィーチャーグループに取り込むためのバッチフィーチャーパイプラインを書く必要があります。

Table 10-2 shows how labels for different types of ML models can be managed in feature groups. 
表10-2は、異なるタイプのMLモデルのラベルがフィーチャーグループでどのように管理されるかを示しています。

_Table 10-2. Supervised learning requires labels that can be stored in feature groups_  
**ML model** **Label feature group** **Prediction problems**  

Decision trees Feature group with features, label column(s), and (optionally) `event_time.`  
Classification or regression  
Time-series: Prophet and ARIMA  
Time-series predictions  
Classification and segmentation for image, audio, and video  
Machine translation, time-series predictions, image segmentation, etc.  
Convolutional neural networks (CNNs)  
Feature groups storing time-series data as features, including `event_time and primary key, and a measurement as the` label column.  
Feature groups storing filepaths for image, audio, and video files.  
Bounding boxes, segmentation masks, and tags as labels.  

Transformers Feature groups storing tabular data and filepaths for image, audio, and text files as features and the label as a column.  
-----
**ML model** **Label feature group** **Prediction problems**  

Fine-tuned LLMs Feature groups storing instruction datasets as instructions, input columns as features, and output columns as labels.  
Chatbots that can answer questions more effectively  



Fine-tuned LLMs Feature groups storing instruction datasets as instructions, input columns as features, and output columns as labels.
ファインチューニングされたLLMは、指示データセットを指示として、入力列を特徴として、出力列をラベルとして格納する特徴グループを持っています。

Chatbots that can answer questions more effectively
質問により効果的に答えることができるチャットボット

We have covered tabular data in feature groups extensively. 
私たちは、特徴グループにおける表形式データを広範囲にわたって扱ってきました。

Data for both decision trees and time-series models, such as Prophet (by Meta) or autoregressive integrated moving average (ARIMA), are naturally stored in feature groups. 
決定木や時系列モデル（MetaのProphetや自己回帰統合移動平均（ARIMA）など）のデータは、自然に特徴グループに格納されます。

Unstructured data sources can also be stored in feature groups as a filepath/URI plus metadata columns and/or labels about the files. 
非構造化データソースも、ファイルパス/URIとファイルに関するメタデータ列および/またはラベルとして特徴グループに格納できます。

CNNs and transformers are typically trained using unstructured data from files (images, audio, video). 
CNNやトランスフォーマーは、通常、ファイル（画像、音声、動画）からの非構造化データを使用して訓練されます。

Pretrained LLMs use text data for supervised fine-tuning (SFT) and preference tuning, commonly stored in JSON Lines (JSONL) files. 
事前訓練されたLLMは、監視付きファインチューニング（SFT）および好みの調整にテキストデータを使用し、一般的にJSON Lines（JSONL）ファイルに格納されます。

Compared with JSON, JSONL can be appended to without rewriting the entire file and can be read and written in a streaming manner. 
JSONと比較して、JSONLはファイル全体を書き換えることなく追加でき、ストリーミング方式で読み書きできます。

For instruction datasets, which are training data for the supervised finetuning of LLMs, each line contains three columns: 
LLMの監視付きファインチューニングのための訓練データである指示データセットでは、各行に3つの列が含まれています。

- Instruction (the task or directive for the model) 
- Instruction（モデルのタスクまたは指示）

- Input (the context provided for the task) 
- Input（タスクに提供されるコンテキスト）

- Output (the expected result or response for the instruction and input) 
- Output（指示と入力に対する期待される結果または応答）

_Preference datasets extend instruction datasets with additional fields to represent multiple possible responses and either the preferred response or scores for each response._ 
好みデータセットは、複数の可能な応答を表すための追加フィールドを持つ指示データセットを拡張し、好ましい応答または各応答のスコアを持ちます。

They are used to train reward models for reinforcement learning with human feedback (RLHF), a post-training alignment step for LLMs that adapts their behavior to make them safer, more useful, and consistent with ethical principles and societal norms. 
これらは、人間のフィードバック（RLHF）を用いた強化学習のための報酬モデルを訓練するために使用され、LLMの行動を適応させて安全で、より有用で、倫理的原則や社会的規範に一致させるための訓練後の調整ステップです。

Both instruction datasets and preference datasets that follow JSON schemas are easily stored in a feature group, with each JSONL line being a row in the feature group and the instruction, input, output, and responses being columns. 
JSONスキーマに従う指示データセットと好みデータセットは、特徴グループに簡単に格納でき、各JSONL行が特徴グループの行となり、指示、入力、出力、および応答が列となります。

The benefits of feature groups over JSONL files are analogous to using a database over raw files. 
特徴グループの利点は、JSONLファイルよりも生データファイルよりもデータベースを使用することに類似しています。

JSONL files have no indexes or search capabilities. 
JSONLファイルにはインデックスや検索機能がありません。

It is expensive to query data and update/delete rows. 
データをクエリし、行を更新/削除するのは高コストです。

Storing instruction and preference datasets in feature groups also gives you time-travel support, as well as lineage information that tracks which models are trained with those datasets. 
指示データセットと好みデータセットを特徴グループに格納することで、タイムトラベルサポートや、どのモデルがそれらのデータセットで訓練されたかを追跡する系譜情報も得られます。

-----
###### Root and Label Feature Groups
###### ルートおよびラベル特徴グループ

Each feature group column is either an index column or a feature. 
各特徴グループの列は、インデックス列または特徴のいずれかです。

Feature groups do not designate any of their columns as labels. 
特徴グループは、その列のいずれかをラベルとして指定しません。

Feature views can define one or more columns in feature groups as labels. 
特徴ビューは、特徴グループ内の1つ以上の列をラベルとして定義できます。

Within the context of a feature view, the feature group that provides the labels for the feature view is called the label feature group. 
特徴ビューの文脈内で、特徴ビューにラベルを提供する特徴グループは、ラベル特徴グループと呼ばれます。

In the AI systems we have seen thus far, the labels were stored in the root feature group of a feature view (transactions in Figure 10-1). 
これまでに見てきたAIシステムでは、ラベルは特徴ビューのルート特徴グループ（図10-1のトランザクション）に格納されていました。

However, labels can also be stored in a child feature group of the root feature group (fraud labels in Figure 10-1). 
ただし、ラベルはルート特徴グループの子特徴グループ（図10-1の詐欺ラベル）にも格納できます。

If you want to create a feature view without labels, you will still have a root feature group and select features as usual, but there will be no label feature group. 
ラベルなしの特徴ビューを作成したい場合でも、ルート特徴グループを持ち、通常通りに特徴を選択しますが、ラベル特徴グループは存在しません。

_Figure 10-1. The feature view starts from the root feature group. It can include any features and labels that are reachable via the data model’s graph, with feature groups as nodes and foreign keys as edges connecting feature groups._ 
_図10-1. 特徴ビューはルート特徴グループから始まります。データモデルのグラフを介して到達可能な任意の特徴とラベルを含むことができ、特徴グループがノード、外部キーが特徴グループを接続するエッジとなります。_

The root feature group is the starting feature group for your feature view. 
ルート特徴グループは、あなたの特徴ビューの出発点となる特徴グループです。

From the root feature group, you can include any features or labels in the feature view that can be reached by graph traversal. 
ルート特徴グループから、グラフトラバーサルによって到達可能な特徴やラベルを特徴ビューに含めることができます。

By graph traversal, we mean that if feature groups are nodes and edges are foreign keys, there must exist a path from the root feature group to the feature group containing the features or labels. 
グラフトラバーサルとは、特徴グループがノードで、エッジが外部キーである場合、ルート特徴グループから特徴やラベルを含む特徴グループへのパスが存在しなければならないことを意味します。

If there is no path to a feature group, such as Weather in Figure 10-1, you cannot include its features. 
図10-1のWeatherのように、特徴グループへのパスがない場合、その特徴を含めることはできません。

To be able to add `Weather features to a feature view that has` `Transactions as its root feature` group, you would need to pick a reachable feature group from the root. 
`Transactions`をルート特徴グループとする特徴ビューに`Weather`の特徴を追加するには、ルートから到達可能な特徴グループを選択する必要があります。

Then at that feature group, add a foreign key to Weather. 
次に、その特徴グループでWeatherへの外部キーを追加します。

For example, assuming Weather has city as its primary key and date as its event time, through feature engineering, you could add to `Transactions a` `city column, computed by geolocating the transaction’s` `ip_address. 
例えば、Weatherが都市を主キー、日付をイベント時間と仮定すると、特徴エンジニアリングを通じて、`Transactions`に取引の`ip_address`をジオロケーションして計算された`city`列を追加できます。

Then you could include Weather features in the feature view by joining from `Transactions to` `Weather on the` `city column. 
その後、`Transactions`から`Weather`に`city`列で結合することで、特徴ビューにWeatherの特徴を含めることができます。

The join would also ensure point-in-time correct data with the Transactions’ event time ts and Weather’s date column, automatically casting the timestamp to a date. 
この結合は、Transactionsのイベント時間tsとWeatherの日付列に対して、時点正確なデータを保証し、タイムスタンプを自動的に日付にキャストします。

Figure 10-1 is an example of a data mart. 
図10-1はデータマートの例です。

Many data teams who manage data marts would like data scientists to only work with data mart data. 
データマートを管理する多くのデータチームは、データサイエンティストがデータマートのデータのみを扱うことを望んでいます。

But what if you need raw data from other tables to create features for your desired model? 
しかし、望むモデルの特徴を作成するために他のテーブルから生データが必要な場合はどうしますか？

In the canonical three-tier medallion architecture for data warehouses, our data mart is the last layer (known as the gold layer; see Figure 10-2). 
データウェアハウスの標準的な三層メダリオンアーキテクチャでは、私たちのデータマートは最後の層（ゴールド層として知られる；図10-2を参照）です。

_Figure 10-2. Data warehouses often have a medallion architecture, with bronze, silver, and gold layers. Features and labels for ML models may come from all layers, not just the gold layer._ 
_図10-2. データウェアハウスはしばしばメダリオンアーキテクチャを持ち、ブロンズ、シルバー、ゴールドの層があります。MLモデルの特徴とラベルは、ゴールド層だけでなく、すべての層から来る可能性があります。_

Behind this gold layer, there are other tables that could be useful for creating features. 
このゴールド層の背後には、特徴を作成するのに役立つ他のテーブルがあります。

The first layer (the bronze layer) typically stores a copy of the raw data from operational databases and event-streaming platforms. 
最初の層（ブロンズ層）は、通常、運用データベースやイベントストリーミングプラットフォームからの生データのコピーを格納します。

For this, you would need access to the Parquet or lakehouse tables in the bronze layer. 
これには、ブロンズ層のParquetまたはレイクハウステーブルへのアクセスが必要です。

The middle (second) layer is called the silver layer, and it typically stores cleaned and deduplicated data in (lakehouse) tables in third normal form (3NF). 
中間の（第二）層はシルバー層と呼ばれ、通常、（レイクハウス）テーブルにおいてクリーンで重複のないデータを第三正規形（3NF）で格納します。

If you cannot find the source data for your features and labels in the gold layer, you should also look in the silver and bronze layers. 
ゴールド層で特徴やラベルのソースデータが見つからない場合は、シルバー層やブロンズ層も確認する必要があります。

It may be that you need to create a new gold layer for your features or labels— using either the snowflake schema or star schema data model. 
特徴やラベルのために新しいゴールド層を作成する必要があるかもしれません—スノーフレークスキーマまたはスタースキーマデータモデルを使用して。

###### Feature Selection
###### 特徴選択

At this point, you have identified your labels and imported them into feature groups. 
この時点で、ラベルを特定し、それらを特徴グループにインポートしました。

What features should you select for your model? 
モデルのためにどの特徴を選択すべきでしょうか？

Figure 10-3 gives high-level guidance for how to identify useful features for a model. 
図10-3は、モデルにとって有用な特徴を特定する方法についての高レベルのガイダンスを提供します。

A useful feature has predictive power for the label/target that you can check by visualizing the feature with respect to the target and computing quick signal checks (mutual information, monotonic trend, predictive power score).  
有用な特徴は、ターゲット/ラベルに対して予測力を持ち、ターゲットに対して特徴を視覚化し、迅速な信号チェック（相互情報量、単調トレンド、予測力スコア）を計算することで確認できます。

-----
_Figure 10-3. Identify features that have predictive power for your target/label. Avoid including redundant, irrelevant, prohibited, and infeasible features._ 
_図10-3. ターゲット/ラベルに対して予測力を持つ特徴を特定します。冗長、無関係、禁止、実行不可能な特徴を含めることは避けてください。_

When selecting features, you should avoid: 
特徴を選択する際には、次のことを避けるべきです：

_Redundant features_ Identify redundant features by computing a correlation matrix across candidate features to catch linear correlations. 
_冗長な特徴_ 候補特徴間で相関行列を計算して線形相関を捉えることで冗長な特徴を特定します。

If two features are highly correlated, exclude one of them as it adds no new information but adds complexity, storage cost, and processing time. 
もし2つの特徴が高い相関を持つ場合、情報を新たに追加しないため、1つを除外しますが、複雑さ、ストレージコスト、処理時間が増加します。

_Irrelevant features_ Use common sense and don’t just include as many features as you can find. 
_無関係な特徴_ 常識を使い、見つけられるだけ多くの特徴を含めることは避けてください。

Irrelevant features will add cost and make it harder for the model to converge. 
無関係な特徴はコストを追加し、モデルの収束を難しくします。

_Prohibited features_ Ensure your feature groups have tags identifying their usage scope. 
_禁止された特徴_ 特徴グループに使用範囲を特定するタグがあることを確認してください。

For example, if you are training a model that is not allowed to use PII, do not include features from feature groups with a PII tag. 
例えば、PIIを使用することが許可されていないモデルを訓練している場合、PIIタグのある特徴グループからの特徴を含めないでください。

_Infeasible features_ These features are not computable or usable for some reason. 
_実行不可能な特徴_ これらの特徴は、何らかの理由で計算可能または使用可能ではありません。

Leaky features are infeasible as they contain information not available at prediction time. 
リーキー特徴は、予測時に利用できない情報を含むため、実行不可能です。

Another example is if your online model could benefit from a feature but is too computationally expensive and would break a model’s SLO. 
別の例として、オンラインモデルが特徴から利益を得られるが、計算コストが高すぎてモデルのSLOを破る場合があります。

The goal of feature selection is to create a feature view that contains the features (and labels) that will be used for both training and inference with your model (see Figure 10-4). 
特徴選択の目標は、モデルの訓練と推論の両方に使用される特徴（およびラベル）を含む特徴ビューを作成することです（図10-4を参照）。

In Hopsworks, you start by identifying the root feature group. 
Hopsworksでは、ルート特徴グループを特定することから始めます。

This is often the label feature group, but it does not have to be. 
これはしばしばラベル特徴グループですが、そうである必要はありません。

If they are not the same, the label feature group should be able to be joined directly with the root (as a child).  
もしそれらが異なる場合、ラベル特徴グループはルートと直接結合できる必要があります（子として）。

-----
_Figure 10-4. From your data model containing a root feature group, labels, and features, select the features and labels to create the feature view._ 
_図10-4. ルート特徴グループ、ラベル、および特徴を含むデータモデルから、特徴とラベルを選択して特徴ビューを作成します。_

Here, we create the feature view from Figure 10-1, including all features from the feature groups: 
ここでは、図10-1から特徴ビューを作成し、特徴グループからすべての特徴を含めます：

```  
card_subtree = card_details.select_features()   
.join(account.select_features())   
.join(bank.select_features())   
selection = transactions.select_features()   
.join(fraud_labels.select_features())   
.join(card_subtree)   
.join(merchant.select_features())   
fv = fs.create_feature_view(name="trans_fv", version=1,        
query=selection,        
labels=['fraud']   
)
``` 

In the code snippet, we join the selected features from a feature group together without explicitly specifying the join column(s). 
このコードスニペットでは、結合列を明示的に指定することなく、特徴グループから選択した特徴を結合します。

In this case, Hopsworks will identify join columns as the columns in the parent group that match the primary key (and event time) columns of the child feature group. 
この場合、Hopsworksは、親グループの列が子特徴グループの主キー（およびイベント時間）列と一致する結合列を特定します。

In this example, we didn’t do much selection. 
この例では、あまり選択を行いませんでした。

We selected all available features. 
利用可能なすべての特徴を選択しました。

Feature selection, however, should be a process for selecting the feature subset that is predictive for a target or label. 
ただし、特徴選択は、ターゲットまたはラベルに対して予測的な特徴のサブセットを選択するプロセスであるべきです。

It is unlikely that all the features we just selected have predictive power for the fraud label. 
私たちが選択したすべての特徴が詐欺ラベルに対して予測力を持つ可能性は低いです。



But, how do you know which features to include from the feature groups? 
しかし、特徴群からどの特徴を含めるべきかをどのように知るのでしょうか？

There are four traditional categories of feature selection methods for refining the set of selected features: 
選択された特徴のセットを洗練させるための伝統的な特徴選択手法には4つのカテゴリがあります：

_Recursive feature addition/elimination methods_ 
_再帰的特徴追加/削除手法_

These methods are a form of data-centric hyperparameter tuning, where you create many different feature views with different combinations of features and choose the feature view that produces a training dataset that the model performs best with. 
これらの手法は、データ中心のハイパーパラメータチューニングの一形態であり、異なる特徴の組み合わせを持つ多くの異なる特徴ビューを作成し、モデルが最も良いパフォーマンスを発揮するトレーニングデータセットを生成する特徴ビューを選択します。

_Filter methods_ 
_フィルタ手法_

These methods select features by ranking them according to a statistical or information-theoretic criterion (e.g., mutual information) and choosing the top-ranked features, independent of the downstream learning algorithm. 
これらの手法は、統計的または情報理論的基準（例：相互情報量）に従って特徴をランク付けし、下流の学習アルゴリズムに依存せずに上位の特徴を選択します。

_Wrapper methods_ 
_ラッパー手法_

These methods identify a locally optimal feature subset that maximizes the performance of the downstream prediction model using a heuristic search strategy (e.g., recursive feature elimination). 
これらの手法は、ヒューリスティック検索戦略（例：再帰的特徴削除）を使用して、下流の予測モデルのパフォーマンスを最大化する局所的最適特徴サブセットを特定します。

_Embedded methods_ 
_埋め込み手法_

These methods select features as part of the model learning process and are often based on regularization techniques that encourage feature sparsity. 
これらの手法は、モデル学習プロセスの一部として特徴を選択し、特徴のスパース性を促進する正則化技術に基づくことが多いです。

A recent novel method of feature selection is to use LLMs and natural language to select features. 
最近の新しい特徴選択手法は、LLM（大規模言語モデル）と自然言語を使用して特徴を選択することです。

Through RAG or prompt engineering, you add to the LLM prompt the descriptions of available feature groups, their features, and statistical properties of the features. 
RAG（Retrieval-Augmented Generation）やプロンプトエンジニアリングを通じて、利用可能な特徴群の説明、その特徴、および特徴の統計的特性をLLMプロンプトに追加します。

The LLM then uses that information, along with your request (for example, “Select features to predict if a credit card transaction is fraudulent”) and domain knowledge of the prediction problem to propose appropriate features from the feature groups. 
その後、LLMはその情報を使用し、あなたのリクエスト（例えば、「クレジットカード取引が不正であるかを予測するための特徴を選択してください」）と予測問題のドメイン知識を組み合わせて、特徴群から適切な特徴を提案します。

The LLM can also suggest features that are not currently available that you could create from your existing data sources. 
LLMは、現在利用可能でない特徴を提案することもでき、既存のデータソースから作成できるものです。

Jeong et al. showed that “given only input feature names and a description of a prediction task, [LLMs] are capable of selecting the most predictive features, with performance rivaling the standard tools of data science.”[1] 
Jeongらは、「入力特徴名と予測タスクの説明のみを与えられた場合、[LLMs]は最も予測力のある特徴を選択することができ、データサイエンスの標準ツールに匹敵するパフォーマンスを発揮する」と示しました。[1]

But be careful: LLMs may exhibit biases inherited from their pretraining data, potentially leading to poor feature selection. 
しかし注意が必要です：LLMは、事前学習データから引き継いだバイアスを示す可能性があり、結果として不適切な特徴選択につながることがあります。

Despite this, I think it doesn’t hurt to ask the LLM its opinion on the best features for the task. 
それにもかかわらず、タスクに最適な特徴についてLLMに意見を求めることは悪くないと思います。

[1 Daniel P. Jeong et al., “LLM-Select: Feature Selection with Large Language Models”, arXiv preprint, 2024.](https://oreil.ly/V-uGW)

###### Training Data
###### トレーニングデータ

When tabular training data is small enough to fit in memory, you probably should read training data as Pandas DataFrames. 
表形式のトレーニングデータがメモリに収まるほど小さい場合、トレーニングデータをPandas DataFrameとして読み込むべきです。

Compared with the size of the training data in a CSV file, you typically need at least two to three times the file size of RAM for Pandas to operate efficiently, as Pandas creates intermediate copies during operations. 
CSVファイルのトレーニングデータのサイズと比較して、Pandasが効率的に動作するためには、通常、RAMのファイルサイズの少なくとも2〜3倍が必要です。これは、Pandasが操作中に中間コピーを作成するためです。

Neither PySpark nor Polars DataFrames are ideal as in-memory DataFrames for training data. 
PySparkもPolarsも、トレーニングデータのためのインメモリDataFrameとしては理想的ではありません。

PySpark’s DataFrames are distributed, and most training pipelines end up calling df.toPandas(), which copies the Spark DataFrame to a Pandas DataFrame on the driver, risking out-of-memory (OOM) errors. 
PySparkのDataFrameは分散型であり、ほとんどのトレーニングパイプラインはdf.toPandas()を呼び出し、Spark DataFrameをドライバー上のPandas DataFrameにコピーするため、メモリ不足（OOM）エラーのリスクがあります。

Polars does not yet have support in Scikit-Learn (you will need to copy your DataFrame to a Pandas DataFrame or NumPy array) but can be a good choice if you have compute-intensive MDTs in your training pipeline. 
PolarsはまだScikit-Learnでのサポートがありません（DataFrameをPandas DataFrameまたはNumPy配列にコピーする必要があります）が、トレーニングパイプラインに計算集約型のMDTがある場合には良い選択肢となる可能性があります。

Figure 10-5 shows three different ways to create training data from feature groups: 
図10-5は、特徴群からトレーニングデータを作成する3つの異なる方法を示しています：

- In-memory DataFrames, read as Arrow data 
- インメモリDataFrame、Arrowデータとして読み込む

- On-disk (CSV, Parquet) files materialized from feature groups 
- 特徴群からマテリアライズされたディスク上の（CSV、Parquet）ファイル

- Unstructured data as files from an object store, with DataFrames providing file paths and metadata 
- オブジェクトストアからのファイルとしての非構造化データ、DataFrameがファイルパスとメタデータを提供

_Figure 10-5. In Hopsworks, training data can be (1) retrieved as in-memory DataFrames or (2) materialized as files that are then read by the training pipeline. Unstructured data as files use in-memory DataFrames to index the files._ 
_図10-5. Hopsworksでは、トレーニングデータは（1）インメモリDataFrameとして取得されるか、（2）トレーニングパイプラインによって読み込まれるファイルとしてマテリアライズされます。ファイルとしての非構造化データは、インメモリDataFrameを使用してファイルをインデックス化します。_

When training data is materialized to files from feature groups with a feature view, there are many different file formats that can be used as training data in different ML frameworks (see Table 10-3). 
特徴ビューを持つ特徴群からファイルにマテリアライズされたトレーニングデータには、さまざまなMLフレームワークでトレーニングデータとして使用できる多くの異なるファイル形式があります（表10-3を参照）。

_Table 10-3. File formats for training data for ML frameworks_ 
_表10-3. MLフレームワークのトレーニングデータ用ファイル形式_

**Training data** **Format** **ML frameworks** 
**トレーニングデータ** **形式** **MLフレームワーク**

Tabular data as files CSV, Parquet Scikit-Learn, XGBoost, Prophet, PyTorch, TensorFlow 
ファイルとしての表形式データ CSV、Parquet Scikit-Learn、XGBoost、Prophet、PyTorch、TensorFlow

Instruction/preference datasets JSONL Fine-tuning for LLMs 
指示/好みデータセット JSONL LLMのファインチューニング

Tensors: files, preprocessed HDF5, TFRecord, NPY PyTorch, TensorFlow 
テンソル：ファイル、前処理済み HDF5、TFRecord、NPY PyTorch、TensorFlow

Tensors: files, unstructured PNG, MP3, MP4, etc. PyTorch, TensorFlow 
テンソル：ファイル、非構造化 PNG、MP3、MP4など PyTorch、TensorFlow

CSV and Parquet are popular file formats for tabular training data. 
CSVとParquetは、表形式のトレーニングデータに人気のあるファイル形式です。

CSV is a row-oriented file format supported by nearly all ML frameworks. 
CSVは、ほぼすべてのMLフレームワークでサポートされている行指向のファイル形式です。

CSV files are poorly _splittable, as you have to know the row boundary for splitting files. 
CSVファイルは分割が難しく、ファイルを分割するためには行の境界を知っている必要があります。

Parquet is a columnar file format that has better compression support than CSV and is also supported by the main ML frameworks. 
Parquetは、CSVよりも優れた圧縮サポートを持つ列指向のファイル形式であり、主要なMLフレームワークでもサポートされています。

Parquet files can be split into many files and directories, enabling the storage of massive tables (PBs) spread across many smaller files (GBs). 
Parquetファイルは多くのファイルやディレクトリに分割でき、大規模なテーブル（PB）を多くの小さなファイル（GB）に分散して保存することができます。

JSONL files, covered earlier, are used to fine-tune pretrained LLMs. 
前述のJSONLファイルは、事前学習済みのLLMをファインチューニングするために使用されます。

TFRecord is described in Chapter 6 and is a row-oriented, binary, splittable file format that is efficient at sequential input/output (I/O). 
TFRecordは第6章で説明されており、行指向のバイナリで分割可能なファイル形式で、シーケンシャルな入出力（I/O）に効率的です。

Both PyTorch and TensorFlow use tensors as the primary data structure for training and inference, integrating them seamlessly through their Dataset APIs. 
PyTorchとTensorFlowの両方は、トレーニングと推論のための主要なデータ構造としてテンソルを使用し、Dataset APIを通じてシームレスに統合しています。

Hierarchical Data Format 5 (HDF5) is a nonsplittable file format for storing large numerical data arrays (including tensors) and metadata. 
階層データ形式5（HDF5）は、大規模な数値データ配列（テンソルを含む）とメタデータを保存するための分割不可能なファイル形式です。

It can store complex hierarchical data (nested data structures) and supports efficient I/O and random access. 
複雑な階層データ（ネストされたデータ構造）を保存でき、効率的なI/Oとランダムアクセスをサポートします。

However, as it is not splittable, it is not suitable for managing large volumes of data for multihost training. 
しかし、分割不可能であるため、マルチホストトレーニングのための大規模なデータを管理するには適していません。

NPY is also a nonsplittable file format that can only store NumPy arrays. 
NPYもまた、NumPy配列のみを保存できる分割不可能なファイル形式です。

As NumPy arrays are designed to store numerical data, all your feature data needs to first be transformed into a numerical representation. 
NumPy配列は数値データを保存するために設計されているため、すべての特徴データは最初に数値表現に変換する必要があります。

You can also store compressed NumPy arrays as NPZ files. 
圧縮されたNumPy配列をNPZファイルとして保存することもできます。

NPY files work well with Scikit-Learn, but I would still recommend Parquet files for Scikit-Learn, as Parquet files are splittable, compressed, and work well with the feature store and feature engineering frameworks like Spark and Pandas. 
NPYファイルはScikit-Learnとよく連携しますが、Parquetファイルは分割可能で圧縮されており、SparkやPandasのような特徴ストアや特徴エンジニアリングフレームワークともうまく連携するため、Scikit-LearnにはParquetファイルをお勧めします。

In Chapter 5, we looked at materializing training data as files in a dedicated training dataset pipeline. 
第5章では、専用のトレーニングデータセットパイプラインでファイルとしてトレーニングデータをマテリアライズする方法を見ました。

This decomposes model training into two stages: first, run a training dataset pipeline to create training data as files, and then, run the training pipeline to fit the training data to your model. 
これにより、モデルのトレーニングが2つのステージに分解されます：最初に、トレーニングデータセットパイプラインを実行してファイルとしてトレーニングデータを作成し、次に、トレーニングパイプラインを実行してトレーニングデータをモデルに適合させます。

Some reasons to have a separate training dataset pipeline include: 
別のトレーニングデータセットパイプラインを持つ理由には以下が含まれます：

- Your training is CPU-bound, leaving your GPUs underutilized. 
- トレーニングがCPUに依存しているため、GPUが十分に活用されていない。

This can happen because you have a lot of compute-heavy MDTs performed on CPUs. 
これは、CPUで実行される計算集約型のMDTが多いために発生する可能性があります。

- Your training data is larger than available memory in the container(s) training the models, causing an OOM error. 
- トレーニングデータがモデルをトレーニングしているコンテナの利用可能メモリよりも大きく、OOMエラーを引き起こす。

With training data as files, data loaders in ML frameworks, like PyTorch and TensorFlow, can stream training rows (samples) during training, bounding memory usage in training jobs. 
トレーニングデータをファイルとして扱うことで、PyTorchやTensorFlowのようなMLフレームワークのデータローダーは、トレーニング中にトレーニング行（サンプル）をストリーミングでき、トレーニングジョブのメモリ使用量を制限できます。

We now look at subtasks in training data creation: splitting training data and reproducible training data. 
次に、トレーニングデータ作成のサブタスク、すなわちトレーニングデータの分割と再現可能なトレーニングデータについて見ていきます。

###### Splitting Training Data
###### トレーニングデータの分割

In Chapter 3, we split the training data for our air quality prediction system using a random split. 
第3章では、空気質予測システムのトレーニングデータをランダム分割を使用して分割しました。

For AI systems built with time-series data, such as our credit card fraud system, a time-series split is preferable, as we want to see if our model generalizes to find novel fraud patterns it wasn’t trained on. 
クレジットカード不正検知システムのような時系列データを使用して構築されたAIシステムでは、時系列分割が好ましいです。なぜなら、モデルが訓練されていない新しい不正パターンを見つける一般化能力を持つかどうかを確認したいからです。

For example, if you have 48 months of credit card transaction data, train the model on the first 42 months of data and evaluate its performance on the last 6 months of data. 
例えば、48か月のクレジットカード取引データがある場合、最初の42か月のデータでモデルを訓練し、最後の6か月のデータでそのパフォーマンスを評価します。

In Hopsworks, you can create training data as files, with a time-series split into train and test sets, as follows: 
Hopsworksでは、トレーニングデータをファイルとして作成し、時系列分割を行ってトレーニングセットとテストセットを作成できます。以下のように：

```  
feature_view.create_train_test_split(         
train_start="2021-01-01", train_end="2024-06-15",         
test_start="2024-07-01", test_end="2024-12-31",         
storage_connector=s3_bucket,         
…   
)
``` 

The preceding code specifies an s3_bucket as the destination for the files. 
前述のコードは、ファイルの宛先としてs3_bucketを指定しています。

If you don’t specify a storage_connector and you run this program on Hopsworks, files will be stored in the <proj>_Training_Datasets directory in your project. 
storage_connectorを指定せずにこのプログラムをHopsworksで実行すると、ファイルはプロジェクト内の<proj>_Training_Datasetsディレクトリに保存されます。

For time-series problems, like fraud, you often need a gap between `train_end` and `test_start` to avoid overlap when features are based on rolling aggregations. 
不正検知のような時系列問題では、特徴がローリング集計に基づいている場合、`train_end`と`test_start`の間にギャップが必要です。

If you intend to perform hyperparameter tuning when training your model, you should create three splits: the train, validation, and test sets. 
モデルをトレーニングする際にハイパーパラメータチューニングを行う予定がある場合、トレーニングセット、バリデーションセット、テストセットの3つの分割を作成する必要があります。

The train set is used to train the model, the validation set is used to tune hyperparameters and select the best model, and the test set is used to evaluate the final model’s performance on unseen data. 
トレーニングセットはモデルのトレーニングに使用され、バリデーションセットはハイパーパラメータを調整し最良のモデルを選択するために使用され、テストセットは未見のデータに対する最終モデルのパフォーマンスを評価するために使用されます。

A common split ratio is 70%–80% for training, 10%–20% for validation, and 10%–20% for testing, although it depends on the dataset size and problem domain. 
一般的な分割比率は、トレーニングに70%〜80%、バリデーションに10%〜20%、テストに10%〜20%ですが、データセットのサイズや問題のドメインによって異なります。

You can create train/validation/test splits as Pandas DataFrames in Hopsworks as follows: 
HopsworksでPandas DataFrameとしてトレーニング/バリデーション/テストの分割を作成することができます：



X_train, X_val, X_test, y_train, y_val, y_test = feature_view.train_validation_test_split(validation_size=0.1, test_size=0.15)
X_train, X_val, X_test, y_train, y_val, y_test = feature_view.train_validation_test_split(validation_size=0.1, test_size=0.15)

Sometimes, random and time-series splits aren’t enough. 
時には、ランダムおよび時系列の分割だけでは不十分です。

Data is rarely _independent_ _and identically distributed (i.i.d.). 
データはほとんどの場合、_独立_ _かつ同一分布（i.i.d.）ではありません。

For imbalanced classification, such as our credit_ card fraud system with less fraud than nonfraud transactions, _stratified sampling_ ensures that splits preserve the portion of positive fraud rows. 
不均衡な分類、例えば、詐欺取引よりも非詐欺取引が少ないクレジットカード詐欺システムでは、_層化サンプリング_ によって分割が正の詐欺行の割合を保持することが保証されます。

That is, it can maintain class balance across splits. 
つまり、分割間でクラスのバランスを維持できます。

_k-fold cross-validation helps improve robustness. 
_k-fold クロスバリデーションはロバスト性を向上させるのに役立ちます。

For example, in Hopsworks you can_ read features and labels as DataFrames and take one stratified train/validation split using Scikit-Learn’s StratifiedKFold as follows: 
例えば、Hopsworksでは、特徴とラベルをDataFrameとして読み込み、Scikit-LearnのStratifiedKFoldを使用して層化されたトレーニング/検証分割を次のように行うことができます：

```   
from sklearn.model_selection import StratifiedKFold   
X, y = feature_view.training_data()   
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)   
train_idx, val_idx = next(skf.split(X, y.squeeze()))   
X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]   
y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
```

###### Reproducible Training Data
###### 再現可能なトレーニングデータ

``` 
Reproducible training data is important for compliance—if a training dataset has been deleted but the feature data is still in the feature store, you should be able to re-create the training data. 
再現可能なトレーニングデータはコンプライアンスにとって重要です。トレーニングデータセットが削除されても、特徴データがフィーチャーストアに残っている場合、トレーニングデータを再作成できる必要があります。

It is also important if you want to train many models and compare their performance—you need to ensure their training data is identical. 
多くのモデルをトレーニングし、そのパフォーマンスを比較したい場合にも重要です。トレーニングデータが同一であることを確認する必要があります。

For example, if the train-test split is re-created every time a new model is trained, it is likely you will end up with different train/validation/test data splits if you’re not careful. 
例えば、新しいモデルがトレーニングされるたびにトレイン-テスト分割が再作成される場合、注意しないと異なるトレーニング/検証/テストデータの分割が得られる可能性があります。

Rereading training data with a random or time-series split is not guaranteed to return the same training/test sets. 
ランダムまたは時系列の分割でトレーニングデータを再読み込みしても、同じトレーニング/テストセットが返されることは保証されません。

For time-series splits, feature data could have been added/ removed/updated since the previous read request. 
時系列の分割では、前回の読み取り要求以降に特徴データが追加/削除/更新されている可能性があります。

For random splits, a different random number seed could have been used. 
ランダム分割の場合、異なる乱数シードが使用されている可能性があります。

The solution in Hopsworks is to create the training data once and have all models reread the same training data using the training_dataset_version (see Chapter 5). 
Hopsworksの解決策は、トレーニングデータを一度作成し、すべてのモデルがtraining_dataset_versionを使用して同じトレーニングデータを再読み込みすることです（第5章を参照）。

When you create a training dataset, Hopsworks stores metadata, including the random seed for splitting and the commit IDs for the feature groups, to ensure it rereads the training data at the point in time the training_dataset_version was created. 
トレーニングデータセットを作成すると、Hopsworksは分割のための乱数シードや特徴グループのコミットIDを含むメタデータを保存し、training_dataset_versionが作成された時点でトレーニングデータを再読み込みすることを保証します。

There are other sources of randomness when training: weight initialization, data augmentation, Compute Unified Device Architecture (CUDA) kernels, and dropout introduce randomness and shuffle training data across training epochs. 
トレーニング時には他にもランダム性の要因があります：重みの初期化、データ拡張、Compute Unified Device Architecture (CUDA) カーネル、ドロップアウトがランダム性を導入し、トレーニングエポック間でトレーニングデータをシャッフルします。

Shuffling training data across epochs is crucial in deep learning models because it improves generalization and prevents overfitting. 
エポック間でトレーニングデータをシャッフルすることは、深層学習モデルにおいて重要です。なぜなら、それが一般化を改善し、過学習を防ぐからです。

To ensure reproducibility, you should set a random seed when training, so that shuffles are deterministic across training runs. 
再現性を確保するために、トレーニング時に乱数シードを設定するべきです。そうすれば、シャッフルがトレーニング実行間で決定論的になります。

Here is example code in PyTorch for setting a random seed: 
以下は、乱数シードを設定するためのPyTorchのサンプルコードです：

```   
SEED = 42   
os.environ["PYTHONHASHSEED"] = str(SEED)   
# For full CUDA matmul determinism (set before CUDA ops):   
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:2")   
random.seed(SEED)   
np.random.seed(SEED)   
torch.manual_seed(SEED)   
torch.cuda.manual_seed_all(SEED)   
torch.backends.cudnn.benchmark = False   
torch.use_deterministic_algorithms(True) # error if nondeterministic op   
X_df, y_df = feature_view.get_training_data(training_dataset_version=1)   
X = torch.tensor(X_df.values, dtype=torch.float32)   
y = torch.tensor(np.ravel(y_df.values), dtype=torch.long)   
g = torch.Generator()   
g.manual_seed(SEED)   

def seed_worker(worker_id):     
    # Ensures each worker has a deterministic RNG state derived from SEED     
    worker_seed = SEED + worker_id     
    np.random.seed(worker_seed)     
    random.seed(worker_seed)     
    torch.manual_seed(worker_seed)   

dataset = TensorDataset(X, y)   
dataloader = DataLoader(     
    dataset, batch_size=10,     
    shuffle=True,      # uses the generator below     
    generator=g,      # deterministic shuffles across epochs     
    num_workers=0,     # safest for determinism; or >0 with seed_worker     
    worker_init_fn=seed_worker if 0 else None,   
)
```

###### Model Training
###### モデルのトレーニング

``` 
Training a good-enough model that meets your requirements is an iterative, experi‐ mental process. 
要件を満たす十分なモデルをトレーニングすることは、反復的で実験的なプロセスです。

Model-centric approaches to make gains in model performance involve changing the model architecture, tuning the hyperparameters, and increasing the training time. 
モデルのパフォーマンスを向上させるためのモデル中心のアプローチには、モデルアーキテクチャの変更、ハイパーパラメータの調整、トレーニング時間の延長が含まれます。

Data-centric approaches involve adding more training data and adding/removing features. 
データ中心のアプローチには、より多くのトレーニングデータを追加したり、特徴を追加/削除したりすることが含まれます。

The goal is to produce the highest-performing model pos‐ sible while passing your model validation tests (see Figure 10-6). 
目標は、モデル検証テストに合格しながら、可能な限り最高のパフォーマンスを持つモデルを生成することです（図10-6を参照）。

_Figure 10-6. Training an ML model is an iterative process that involves experimentation_ _with data-centric steps (feature selection) and model-centric steps (everything to the_ _right)._
_Figure 10-6. MLモデルのトレーニングは、データ中心のステップ（特徴選択）とモデル中心のステップ（右側のすべて）を含む反復的なプロセスです。_

The core steps in model training are: 
モデルのトレーニングにおける主要なステップは次のとおりです：

1. Select features and create training data. 
1. 特徴を選択し、トレーニングデータを作成します。

2. Create a model architecture. 
2. モデルアーキテクチャを作成します。

3. Perform hyperparameter tuning trials, evaluating each trial’s model on the valida‐ tion set. 
3. ハイパーパラメータ調整の試行を行い、各試行のモデルを検証セットで評価します。

4. Use the best hyperparameters to fit the model to the training data. 
4. 最良のハイパーパラメータを使用して、モデルをトレーニングデータに適合させます。

5. Evaluate the trained model on the test set and evaluation sets (model validation), and if all model validation checks pass, register the model in the model registry. 
5. テストセットおよび評価セット（モデル検証）でトレーニングされたモデルを評価し、すべてのモデル検証チェックが合格した場合、モデルをモデルレジストリに登録します。

Each of these steps can be revisited and updated as part of the iterative development workflow. 
これらの各ステップは、反復的な開発ワークフローの一部として再訪し、更新できます。

Training data is typically not static. 
トレーニングデータは通常静的ではありません。

New data may arrive, and you may include different sets of features. 
新しいデータが到着する可能性があり、異なる特徴セットを含めることがあります。

You may also change the MDTs that are applied when reading the training data. 
トレーニングデータを読み込む際に適用されるMDTを変更することもできます。

We have already looked at data-centric challenges in selecting features and building training datasets. 
私たちはすでに特徴を選択し、トレーニングデータセットを構築する際のデータ中心の課題を見てきました。

In the following sections, we will look at model architecture, training, and hyperparameter tuning of deep learning models in the context of PyTorch and Ray. 
次のセクションでは、PyTorchとRayの文脈における深層学習モデルのモデルアーキテクチャ、トレーニング、およびハイパーパラメータ調整について見ていきます。

Ray is an open source distributed frame‐ work for managing compute and data for ML. 
Rayは、MLの計算とデータを管理するためのオープンソースの分散フレームワークです。

Ray Train supports the training of models in many different ML frameworks, from XGBoost to PyTorch, on GPUs or CPUs, on a single-host or a massive cluster of GPUs. 
Ray Trainは、XGBoostからPyTorchまでのさまざまなMLフレームワークでのモデルのトレーニングをサポートし、GPUまたはCPU、単一ホストまたは大規模なGPUクラスターで実行できます。

Ray Tune supports hyperpara‐ meter tuning across many CPUs or GPUs. 
Ray Tuneは、多くのCPUまたはGPUでのハイパーパラメータ調整をサポートします。

###### Model Architecture
###### モデルアーキテクチャ

A model’s architecture is its layout: what components it has, how they’re connected, and how data flows from input to prediction. 
モデルのアーキテクチャはそのレイアウトです：どのようなコンポーネントがあり、それらがどのように接続され、データが入力から予測にどのように流れるかです。

Here are some of the most common ML families and important parts of their layouts: 
以下は、最も一般的なMLファミリーとそのレイアウトの重要な部分です：

_Decision trees_ Splitting criterion and maximum depth (pruning) 
_決定木_ 分割基準と最大深さ（剪定）

_Feed-forward neural networks_ Layer depth/width, activation functions, normalization/dropout, and output head 
_フィードフォワードニューラルネットワーク_ レイヤーの深さ/幅、活性化関数、正規化/ドロップアウト、および出力ヘッド

_CNNs_ Convolution and pooling blocks with stride/padding 
_CNN_ ストライド/パディングを持つ畳み込みおよびプーリングブロック

_Transformers_ Stacks of self-attention and feed-forward blocks with residuals and layer norm 
_トランスフォーマー_ 残差とレイヤーノルムを持つ自己注意とフィードフォワードブロックのスタック

Each of these model architectures has many concepts, each of which has filled many books. 
これらの各モデルアーキテクチャには多くの概念があり、それぞれが多くの本を埋めています。

Unfortunately, we don’t have space to cover all of these concepts here. 
残念ながら、ここですべての概念をカバーするスペースはありません。

But, at a high level, you should be able to choose the right ML family and its model architec‐ ture by understanding the prediction problem, the appropriate learning algorithm, the type of input data (structured or unstructured), and the scale of training data. 
しかし、高いレベルでは、予測問題、適切な学習アルゴリズム、入力データの種類（構造化データまたは非構造化データ）、およびトレーニングデータのスケールを理解することで、適切なMLファミリーとそのモデルアーキテクチャを選択できるはずです。

For example, some simple rules of thumb for supervised learning with structured data are: 
例えば、構造化データを用いた教師あり学習のためのいくつかの簡単なルールは次のとおりです：

- For datasets with less than 10 million rows, decision tree-based models, especially XGBoost, often outperform neural networks (NNs) due to their ability to handle structured data efficiently with minimal preprocessing. 
- 1000万行未満のデータセットでは、決定木ベースのモデル、特にXGBoostが、最小限の前処理で構造化データを効率的に処理できるため、ニューラルネットワーク（NN）よりも優れたパフォーマンスを発揮することがよくあります。

- For datasets between 10 and 100 million rows, the choice depends on the com‐ plexity of the data and available computational resources; both XGBoost and NNs can perform well. 
- 1000万行から1億行のデータセットでは、選択はデータの複雑さと利用可能な計算リソースに依存します。XGBoostとNNの両方が良好なパフォーマンスを発揮できます。

- For datasets exceeding 100 million rows, NNs tend to outperform XGBoost, as they can better capture complex patterns and scale effectively with large amounts of data. 
- 1億行を超えるデータセットでは、NNがXGBoostよりも優れたパフォーマンスを発揮する傾向があります。なぜなら、NNは複雑なパターンをよりよく捉え、大量のデータで効果的にスケールできるからです。

When using NNs, you can optimize performance by adjusting the num‐ ber of layers/blocks and applying regularization techniques such as dropout. 
NNを使用する際は、レイヤー/ブロックの数を調整し、ドロップアウトなどの正則化手法を適用することでパフォーマンスを最適化できます。



Why do tree-based models still outperform deep learning on typical tabular data? 
なぜツリーベースのモデルは、典型的なタブularデータにおいて依然として深層学習を上回るのでしょうか？

An influential paper at NeurIPS 2022 showed that for small (<10K sample) datasets, tree-based models outperform NNs. 
NeurIPS 2022で発表された影響力のある論文は、小規模（<10Kサンプル）のデータセットにおいて、ツリーベースのモデルがニューラルネットワーク（NN）を上回ることを示しました。

Deep learning is superior when you have raw input data (of high dimensionality) with recurring patterns. 
深層学習は、繰り返しのパターンを持つ高次元の生データがある場合に優れています。

NNs are efficient at automatically creating higher-level features from the raw input data. 
NNは、生データから自動的に高次の特徴を生成するのに効率的です。

Tabular data, in contrast, typically consists of preprocessed, aggregated, or engineered features, which do not always require the hierarchical representation learning power of deep learning. 
対照的に、タブularデータは通常、前処理された、集約された、またはエンジニアリングされた特徴で構成されており、必ずしも深層学習の階層的表現学習の力を必要としません。

Tree-based models are also interpretable, while deep learning models are not, which is important in domains where you need to explain why a model has made a certain decision. 
ツリーベースのモデルは解釈可能ですが、深層学習モデルはそうではなく、モデルが特定の決定を下した理由を説明する必要がある領域では重要です。

For supervised learning on unstructured data (such as images, audio, video, and text), NNs are generally the preferred choice. 
非構造化データ（画像、音声、動画、テキストなど）に対する教師あり学習では、一般的にNNが好まれます。

Depending on the data type and task, you may choose among different model architectures: 
データの種類やタスクに応じて、さまざまなモデルアーキテクチャの中から選択できます：

- CNNs are best suited for 2D and 3D spatial data, such as images and videos, as they exploit local receptive fields and translation equivariance to learn hierarchical patterns. 
- CNNは、画像や動画などの2Dおよび3D空間データに最適であり、局所受容野と変換等変性を利用して階層的パターンを学習します。

- Transformers are effective for sequential and contextual data, particularly in NLP and time-series forecasting. 
- トランスフォーマーは、特に自然言語処理（NLP）や時系列予測において、順序的および文脈的データに効果的です。

- Feed-forward NNs are suitable for tabular input data where no spatial or sequential relationships exist. 
- フィードフォワードNNは、空間的または順序的関係が存在しないタブular入力データに適しています。

- Long short-term memory (LSTM) networks handle sequential data with temporal dependencies (e.g., speech, certain time series). 
- 長短期記憶（LSTM）ネットワークは、時間的依存性を持つ順序データ（例：音声、特定の時系列）を処理します。

Transformers often outperform them at scale due to parallelism and pretraining. 
トランスフォーマーは、並列処理と事前学習により、大規模でしばしばそれらを上回ります。

Here is an example of a feed-forward NN for the Modified National Institute of Standards and Technology (MNIST) dataset (containing 70K grayscale images of handwritten digits from 0 to 9). 
ここに、修正された国立標準技術研究所（MNIST）データセット（0から9までの手書き数字の70Kのグレースケール画像を含む）用のフィードフォワードNNの例があります。

The NN takes as input a batch of black-and-white images of size 28 × 28 pixels (784 pixels in total). 
NNは、28 × 28ピクセルの白黒画像のバッチを入力として受け取ります（合計784ピクセル）。

For training, it outputs logits that are used by loss functions like nn.CrossEntropyLoss: 
トレーニングのために、nn.CrossEntropyLossのような損失関数で使用されるロジットを出力します：

```python
class CustomMnist(nn.Module):
    def __init__(self, layer_sz=128, dropout=0.3):
        super(CustomMnist, self).__init__()
        self.fc1 = nn.Linear(28*28, layer_sz)
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(layer_sz, 10)

    def forward(self, x):
        x = torch.flatten(x, 1) # Flatten (batch_sz, 28, 28) -> (batch_sz, 784)
        x = torch.relu(self.fc1(x)) # Apply ReLU activation
```
```python
        x = self.dropout(x) # Apply dropout after activation
        return self.fc2(x) # Output logits
```

In PyTorch, we define the NN as a custom class that inherits from `nn.Module` and implements an `__init__` and `forward` method to implement the forward pass. 
PyTorchでは、NNを`nn.Module`から継承したカスタムクラスとして定義し、フォワードパスを実装するために`__init__`と`forward`メソッドを実装します。

The forward pass is the process in which an input is passed through the NN from the input layer to the output layer, producing logits for training and predictions for inference. 
フォワードパスは、入力が入力層から出力層へとNNを通過し、トレーニング用のロジットと推論用の予測を生成するプロセスです。

The hyperparameters are the layer size (layer_sz) and dropout rate (dropout). 
ハイパーパラメータは、層のサイズ（layer_sz）とドロップアウト率（dropout）です。

We train this NN using cross-entropy loss and the Adaptive Moment Estimation (Adam) optimizer. 
このNNは、クロスエントロピー損失と適応モーメント推定（Adam）オプティマイザを使用してトレーニングします。

Cross-entropy is a loss function for classification that measures the difference between the true labels and predicted probabilities. 
クロスエントロピーは、真のラベルと予測確率の違いを測定する分類用の損失関数です。

This difference, or loss, is used to compute the gradients via the backpropagation algorithm in the backward pass. 
この違い、または損失は、バックワードパスでバックプロパゲーションアルゴリズムを介して勾配を計算するために使用されます。

The gradient represents the contribution of each parameter to the total loss. 
勾配は、各パラメータが総損失に寄与する度合いを表します。

An optimizer then updates the weights of all the parameters in the NN using the gradient. 
その後、オプティマイザは勾配を使用してNN内のすべてのパラメータの重みを更新します。

Stochastic gradient descent is the most well-known optimizer. 
確率的勾配降下法は、最もよく知られたオプティマイザです。

It updates the weights for a mini-batch of parameters by changing the values of the parameters in the opposite direction of the gradient using a fixed learning rate. 
これは、固定学習率を使用して、勾配の逆方向にパラメータの値を変更することによって、パラメータのミニバッチの重みを更新します。

The learning rate defines the relative size of each update. 
学習率は、各更新の相対的なサイズを定義します。

We create training data for CustomMnist using a custom PyTorch Dataset that uses a feature view to return a DataFrame containing the image_path as a feature and a label (the actual digit in the image). 
CustomMnistのトレーニングデータは、画像パスを特徴として返し、ラベル（画像内の実際の数字）を含むDataFrameを返す特徴ビューを使用したカスタムPyTorchデータセットを使用して作成します。

ImageDataset extracts the path and label for each image from each row in the DataFrame. 
ImageDatasetは、DataFrameの各行から各画像のパスとラベルを抽出します。

In training, we return the images and labels, but in inference (train=False), we only return the images: 
トレーニングでは、画像とラベルを返しますが、推論（train=False）では、画像のみを返します：

```python
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import torchvision.transforms as T

class ImageDataset(Dataset):
    def __init__(self, transform, features, labels=None):
        self.transform = transform
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        img_path = pathlib.Path(self.features.iloc[idx]["image_path"])
        image = Image.open(img_path).convert("L")
        image = self.transform(image)
        if self.labels is not None:
            label = int(self.labels.iloc[idx]["label"])
            return image, torch.tensor(label, dtype=torch.long)
        return image
```
```python
proj = hopsworks.login()
fv = proj.get_feature_store().get_feature_view(name="mnist", version=1)
transform = T.Compose([T.Resize((28, 28)), T.ToTensor()])
features, labels = fv.training_data()
dataset = ImageDataset(transform, features, labels)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
```

You can build on this example to store image metadata as columns that can be used in both training and inference. 
この例を基に、トレーニングと推論の両方で使用できる列として画像メタデータを保存することができます。

For training, you might include data quality scores as a feature. 
トレーニングでは、データ品質スコアを特徴として含めることができます。

For inference, you might include a helper column to identify where to store or how to tag predictions. 
推論では、予測を保存する場所やタグ付け方法を特定するための補助列を含めることができます。

Another advantage of using feature groups over vanilla files as training data is lineage information about what files were used to train a given model. 
バニラファイルよりも特徴グループをトレーニングデータとして使用するもう一つの利点は、特定のモデルをトレーニングするために使用されたファイルに関する系譜情報です。

Lower learning rates have better convergence properties but usually require more steps. 
低い学習率は、より良い収束特性を持ちますが、通常はより多くのステップを必要とします。

Here, we use the Adam optimizer, which automatically adjusts the learning rate for each parameter by estimating the first and second moments of the gradients. 
ここでは、勾配の第一および第二モーメントを推定することによって、各パラメータの学習率を自動的に調整するAdamオプティマイザを使用します。

Typically, this means higher learning rates at the start of training and progressively lower learning rates as the model converges. 
通常、これはトレーニングの開始時に高い学習率を意味し、モデルが収束するにつれて徐々に低い学習率になります。

An alternative would have been AdamW, an Adam variant with decoupled weight decay. 
代替案としては、重み減衰が分離されたAdamの変種であるAdamWが考えられます。

It computes per-parameter adaptive step sizes from the first and second moments of the gradients. 
これは、勾配の第一および第二モーメントからパラメータごとの適応ステップサイズを計算します。

Thanks to their stability and strong general performance, both Adam and AdamW are common choices as optimizers for deep learning: 
その安定性と強力な一般的なパフォーマンスのおかげで、AdamとAdamWの両方は深層学習のオプティマイザとして一般的な選択肢です：

```python
def train_model(config, train_loader):
    model = CustomMnist(layer_sz=config["layer_sz"], dropout=config["dropout"])
    optimizer = optim.Adam(model.parameters(), lr=config["lr"])
    loss_fn = nn.CrossEntropyLoss()
    state = None
    model.train() # sets the model to training mode (enables dropout)
    for epoch in range(config["num_epochs"]):
        correct, total = 0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            logits = model(inputs)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()
            preds = logits.argmax(1)
            total += labels.size(0)
            correct += (preds == labels).sum().item()
        # Uncomment next line to add Ray support
        # ray_train.report({"train_accuracy": correct / max(total, 1)})
    return model

config = {"layer_sz": 128, "dropout": 0.3, "lr": 1e-3, "num_epochs": 10}
model = train_model(config, train_loader)
```
```python
state = {k: v.detach().cpu() for k, v in model.state_dict().items()}
model_registry = proj.get_model_registry()
mr_model = model_registry.python.create_model(
    name="mnist",
    metrics=config, # save hparams for inference
    feature_view=fv
)
with tempfile.TemporaryDirectory() as tmpdir:
    joblib.dump(state, os.path.join(tmpdir, "model.pkl"))
    joblib.dump(transform, os.path.join(tmpdir, "transform.pkl"))
    mr_model.save(tmpdir)
```

The config dictionary contains the hyperparameters that we can tune, like dropout, layer_sz, num_epochs, and lr (learning rate). 
config辞書には、ドロップアウト、layer_sz、num_epochs、lr（学習率）など、調整可能なハイパーパラメータが含まれています。

Loss functions and optimizers are a wide area of research in deep learning, and you can read more about them in Aurélien Géron’s book, Hands-On Machine Learning with Scikit-Learn and PyTorch (O’Reilly, 2025). 
損失関数とオプティマイザは深層学習における広範な研究分野であり、Aurélien Géronの書籍『Hands-On Machine Learning with Scikit-Learn and PyTorch』（O’Reilly、2025年）でさらに詳しく読むことができます。

Note that we need to save the weights of the model, its hyperparameters, and its transformer object so that we download them in inference and avoid skew. 
モデルの重み、ハイパーパラメータ、およびトランスフォーマーオブジェクトを保存する必要があることに注意してください。これにより、推論時にそれらをダウンロードし、偏りを避けることができます。

###### Checkpoints to Recover from Failures
###### 障害から回復するためのチェックポイント

You need hardware accelerators to efficiently train deep learning models. 
深層学習モデルを効率的にトレーニングするには、ハードウェアアクセラレーターが必要です。

GPUs are the most popular accelerators. 
GPUは最も一般的なアクセラレーターです。

Meta trained its Llama 3 model with 405 billion parameters over 54 days on 16,384 NVIDIA H100 80 GB GPUs. 
Metaは、16,384のNVIDIA H100 80 GB GPU上で54日間にわたり、4050億のパラメータを持つLlama 3モデルをトレーニングしました。

They also experienced an average of one failure every three hours (most issues were caused by GPUs or their onboard HBM3 memory). 
彼らはまた、平均して3時間ごとに1回の障害を経験しました（ほとんどの問題はGPUまたはそのオンボードHBM3メモリによって引き起こされました）。

A failure in any of the GPUs (or workers) during training causes the training process to fail. 
トレーニング中にGPU（またはワーカー）のいずれかで障害が発生すると、トレーニングプロセスが失敗します。

To handle such failures, you periodically create training checkpoints so that training can be restarted from a checkpoint after failure. 
そのような障害に対処するために、定期的にトレーニングチェックポイントを作成し、障害後にチェックポイントからトレーニングを再開できるようにします。

This resulted in an effective training time of 90% for Llama 3. 
これにより、Llama 3の効果的なトレーニング時間は90%になりました。

Without checkpoints, this number would have been much lower. 
チェックポイントがなければ、この数値ははるかに低くなっていたでしょう。

The following code snippet shows you how to add storing and recovering from checkpoints in a training pipeline: 
以下のコードスニペットは、トレーニングパイプラインにチェックポイントの保存と回復を追加する方法を示しています：

```python
def train_model(config, train_loader, model, optimizer, checkpoint_path):
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch'] + 1
    for epoch in range(start_epoch, config["num_epochs"]):
        …
        torch.save({ # Save checkpoint after every epoch
            'epoch': epoch,
```
```python
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict()
        }, checkpoint_path)
```

Checkpoints should be stored and loaded from shared distributed storage. 
チェックポイントは、共有分散ストレージから保存および読み込む必要があります。



. The check ``` point_path is a path to a distributed filesystem, such as an S3 bucket or a local direc‐
. チェックポイントパスは、S3バケットやHopsFS Filesystem in Userspace (FUSE)を介したローカルディレクトリなど、分散ファイルシステムへのパスです。

###### Hyperparameter Tuning with Ray Tune
###### Ray Tuneによるハイパーパラメータチューニング

Hyperparameter tuning can be easily integrated into a training pipeline by using an _AutoML library that automates the process of running hyperparameter tuning trials_ [for you. 
ハイパーパラメータチューニングは、ハイパーパラメータチューニング試行を実行するプロセスを自動化するAutoMLライブラリを使用することで、トレーニングパイプラインに簡単に統合できます。

For a single-host AutoML solution, auto-sklearn works well for tabular data.](https://oreil.ly/fMiYl) 
単一ホストのAutoMLソリューションでは、auto-sklearnが表形式データに対してうまく機能します。

For a cluster, [Ray Tune can scale out hyperparameter tuning on CPUs or GPUs for](https://oreil.ly/RNGZ_) deep learning and decision tree models. 
クラスターの場合、Ray Tuneは深層学習および決定木モデルのためにCPUまたはGPUでハイパーパラメータチューニングをスケールアウトできます。

Hyperparameter tuning requires you to define:
ハイパーパラメータチューニングでは、次のことを定義する必要があります：

- A hyperparameter search space (the hyperparameters you want to tune and the range of values you want to evaluate)
- ハイパーパラメータの探索空間（調整したいハイパーパラメータと評価したい値の範囲）

- A search algorithm over that search space (for example, random or grid search, or search using a model built from trials, such as Bayesian optimization)
- その探索空間に対する探索アルゴリズム（例えば、ランダムまたはグリッドサーチ、または試行から構築されたモデルを使用した探索、例えばベイズ最適化など）

- A scheduler to allocate resources to all the trials that will be performed in parallel
- 並行して実行されるすべての試行にリソースを割り当てるスケジューラ

At the end of hyperparameter tuning, you can select the best hyperparameters you’ve found and train your model for more epochs (and more data) with those hyperpara‐ meters. 
ハイパーパラメータチューニングの最後に、見つけた最良のハイパーパラメータを選択し、それらのハイパーパラメータでモデルをさらにエポック（およびより多くのデータ）でトレーニングできます。

AutoML solutions simplify hyperparameter tuning by automatically defining the hyperparameter search space, search algorithm, and scheduling. 
AutoMLソリューションは、ハイパーパラメータ探索空間、探索アルゴリズム、およびスケジューリングを自動的に定義することで、ハイパーパラメータチューニングを簡素化します。

However, you also lose control with AutoML. 
ただし、AutoMLを使用すると、制御を失うことにもなります。

It is not particularly hard to understand these three abstractions, so it is worth your while to learn the basics, so you don’t waste compute resources on unnecessary trials.
これらの3つの抽象概念を理解することは特に難しくないため、基本を学ぶ価値があります。そうすれば、不必要な試行に計算リソースを無駄にすることはありません。

Ray Tune is an orchestrator for hyperparameter tuning. 
Ray Tuneはハイパーパラメータチューニングのオーケストレーターです。

It wraps hyperparameter search optimization libraries, such as [Bayesian optimization and](https://oreil.ly/7mhyO) [Optuna, and exe‐](https://oreil.ly/3_2p4) cutes trials using a configurable scheduler that manages resources, stops unpromising trials early, and allocates more resources to promising configurations. 
それは、リソースを管理し、有望でない試行を早期に停止し、有望な構成により多くのリソースを割り当てる構成可能なスケジューラを使用して、[ベイズ最適化や](https://oreil.ly/7mhyO) [Optunaなどのハイパーパラメータ探索最適化ライブラリをラップします。](https://oreil.ly/3_2p4)

The Asynchro‐ _nous Successive Halving Algorithm (ASHA) scheduler launches many small-budget_ trials in parallel, periodically pruning underperformers and promoting the best to larger budgets (higher “rungs”) according to a reduction factor. 
非同期逐次ハルビングアルゴリズム（ASHA）スケジューラは、多くの小予算の試行を並行して開始し、定期的にパフォーマンスが低いものを剪定し、最良のものをより大きな予算（より高い「段階」）に昇格させます。

Freed resources are given to new or promoted trials, and the process continues until the tuning budget is exhausted.
解放されたリソースは新しい試行または昇格された試行に与えられ、プロセスはチューニング予算が尽きるまで続きます。



This example code shows a hyperparameter tuning workflow using Ray Tune with ASHA and Optuna and our previous MNIST example code: 
この例のコードは、Ray Tuneを使用したハイパーパラメータチューニングのワークフローを、ASHAおよびOptunaと以前のMNISTの例コードを用いて示しています。

```   
   from ray.tune.schedulers import ASHAScheduler   
   from ray.tune.search.optuna import OptunaSearch   
   scheduler = ASHAScheduler(metric="train_accuracy", mode="max", grace_period=3)   
   searcher = OptunaSearch()   
   param_space = {     
     "lr": tune.loguniform(1e-4, 1e-2),     
     "dropout": tune.choice([0.1, 0.3, 0.5]),     
     "layer_sz": tune.choice([64, 128, 256]),     
     "num_epochs": 10, # max epochs per trial; ASHA may stop early   
   }   
   resources_per_trial = {"cpu": 2, "gpu": 0}   
   tuner = tune.Tuner(     
     tune.with_resources(       
       tune.with_parameters(         
         train_model,         
         train_loader=train_loader,         
         proj=proj,         
         fv=fv,         
         transform=transform,       
       ),       
       resources=resources_per_trial,     
     ),     
     param_space=param_space,     
     tune_config=tune.TuneConfig(       
       metric="train_accuracy",       
       mode="max",       
       scheduler=scheduler,       
       search_alg=searcher,       
       num_samples=15,     
     ),     
     run_config=air.RunConfig(name="mnist_asha_optuna_acc"),   
   )   
   results = tuner.fit()   
   best = results.get_best_result(metric="train_accuracy", mode="max")   
   print("Best config:", best.config)   
   print("Best train_accuracy:", best.metrics["train_accuracy"])
``` 
このコードは、Ray Tuneを使用してハイパーパラメータを調整するワークフローを示しています。

Note that we do have to modify `train_model() from earlier to report per-epoch` training metrics to Ray Tune. 
以前の`train_model()`を修正して、エポックごとのトレーニングメトリクスをRay Tuneに報告する必要があります。

This line should be added: 
次の行を追加する必要があります：

```   
   train.report({"mean_accuracy": mean_acc, "epoch": epoch}) 
``` 
```   
   train.report({"mean_accuracy": mean_acc, "epoch": epoch}) 
``` 

_Experiment tracking services are widely used to store hyperparame‐_ 
実験トラッキングサービスは、ハイパーパラメータチューニングの実験結果やトレーニング損失曲線を保存するために広く使用されています。

ter tuning experiment results as well as training loss curves. 
MLflow is a popular open source framework. 
MLflowは人気のあるオープンソースフレームワークです。

SaaS platforms [include neptune.ai, comet.ai, and wandb.ai. 
SaaSプラットフォームには、neptune.ai、comet.ai、wandb.aiが含まれます。

You can also use Hops‐](http://neptune.ai) works model registry to store model performance plots, model cards, and validation results along with the trained model. 
また、Hopsworksモデルレジストリを使用して、モデルのパフォーマンスプロット、モデルカード、および検証結果をトレーニング済みモデルと共に保存することもできます。

###### Distributed Training with Ray
###### Rayによる分散トレーニング

Distributed training is needed when you want to train large deep learning models on large amounts of data. 
大量のデータで大規模な深層学習モデルをトレーニングしたい場合、分散トレーニングが必要です。

For example, training Llama 3.1 405B with 16-bit weights requires roughly 3.24 TB of GPU memory—made up of 810 GB each for the model parameters and gradients and 1.62 TB for the (Adam) optimizer state. 
例えば、16ビットの重みを持つLlama 3.1 405Bをトレーニングするには、約3.24 TBのGPUメモリが必要です。これは、モデルパラメータと勾配それぞれ810 GB、(Adam)オプティマイザの状態に1.62 TBを要します。

The NVIDIA H100 has 80 GB of memory, so without memory optimizations, you need roughly 40 such GPUs just to fit Llama 3.1 in memory. 
NVIDIA H100は80 GBのメモリを持っているため、メモリの最適化なしでは、Llama 3.1をメモリに収めるために約40のGPUが必要です。

With 40 GPUs (assuming no failures and linear scaling), it would take roughly 60 years to train Llama 3.1. 
40のGPUを使用した場合（障害がなく、線形スケーリングを仮定すると）、Llama 3.1をトレーニングするのに約60年かかります。

Distributed training enables you to both speed up training by adding more GPUs and scale up model sizes by partitioning your model state (parameters, gradients, optimizer) over many GPUs. 
分散トレーニングにより、より多くのGPUを追加することでトレーニングを加速し、モデルの状態（パラメータ、勾配、オプティマイザ）を複数のGPUに分割することでモデルサイズを拡大できます。

_Data-parallel training is where you want to reduce the training time by replicating the_ 
データ並列トレーニングは、モデルを複数のGPUに複製することでトレーニング時間を短縮したい場合に使用されます。

model on many different GPUs. 
Ray Train supports data-parallel training that can be scaled out across many hosts using a gradient synchronization algorithm such as ring _all-reduce (described later in this chapter)._ 
Ray Trainは、リング全体の削減（この章の後半で説明）などの勾配同期アルゴリズムを使用して、多くのホストにスケールアウトできるデータ並列トレーニングをサポートしています。

_Tensor parallelism is a technique where large tensors (such as model weights or acti‐_ 
テンソル並列性は、大きなテンソル（モデルの重みや活性化など）を複数のGPUに分割する技術であり、パフォーマンスを向上させます。

vations) are partitioned across multiple GPUs, improving performance. 
これにより、単一の操作（例えば、行列の乗算）の異なる部分を並行して処理でき、計算とメモリの負荷を効率的に分散させることができます。

This allows different parts of a single operation (e.g., matrix multiplication) to be processed in parallel, distributing computation and memory load efficiently. 
NVIDIAのMegatron_LMフレームワークは、テンソル並列性を使用して、個々のレイヤーを複数のGPUに分割し、単一のデバイスに収まらないモデルを可能にします。

NVIDIA’s Megatron_LM framework uses tensor parallelism to split individual layers across multiple GPUs,_ 
NVIDIAのMegatron_LMフレームワークは、テンソル並列性を使用して、個々のレイヤーを複数のGPUに分割します。

enabling models that are too large to fit on a single device. 
これにより、単一のデバイスに収まらないモデルが可能になります。

_Model-parallel training is required when your model does not fit in memory of a sin‐_ 
モデルが単一のGPUのメモリに収まらない場合、モデル並列トレーニングが必要です。

gle GPU. 
Model-parallel training scales best when you can fit the model on a single GPU server (containing up to 8 or 16 GPUs) with a high-performance GPU intercon‐ 
モデル並列トレーニングは、高性能GPUインターコネクトを持つ単一のGPUサーバー（最大8または16のGPUを含む）にモデルを収めることができるときに最も効果的にスケールします。

nect. 
When you need to partition models over hosts across the network, you need a very high-performance network (such as InfiniBand) to prevent training from bottle‐ 
ネットワークを介してホスト間でモデルを分割する必要がある場合、トレーニングがネットワークI/Oでボトルネックにならないようにするために、非常に高性能なネットワーク（InfiniBandなど）が必要です。

necking on network I/O. 
DeepSpeed ZeRO-3 is a framework for model-parallel train‐ 
DeepSpeed ZeRO-3は、深層学習モデルのモデル並列トレーニングのためのフレームワークです。

ing of deep learning models. 
It implements both tensor-level and model-level parallelism, as well as memory (or Zero Redundancy Optimizer [ZeRO]) optimiza‐ 
テンソルレベルとモデルレベルの並列性の両方を実装し、メモリ（またはゼロ冗長オプティマイザ[ZeRO]）の最適化も行います。

tions. 
DeepSpeed is included in Megatron-LM and can be run on top of Ray Train (which handles coordinating and scaling training workloads). 
DeepSpeedはMegatron-LMに含まれており、Ray Trainの上で実行することができます（Ray Trainはトレーニングワークロードの調整とスケーリングを処理します）。

Multihost training with Ray Train requires distributed storage (S3, HopsFS via FUSE) for the training data. 
Ray Trainを使用したマルチホストトレーニングには、トレーニングデータのための分散ストレージ（S3、FUSE経由のHopsFS）が必要です。

Ray Data is a data processing library that supports the parallel reading of training data during training. 
Ray Dataは、トレーニング中にトレーニングデータの並列読み込みをサポートするデータ処理ライブラリです。

That is, training data is read and fetched in 
つまり、トレーニングデータは読み込まれ、取得されます。

chunks in the background by CPUs, enabling GPUs to remain saturated during training. 
CPUによってバックグラウンドでチャンク単位で読み込まれ、GPUがトレーニング中に飽和状態を維持できるようになります。

Ray Data provides dataset tasks as a general-purpose abstraction for tasks such as data loading, MDTs (preprocessing of training data), and data output. 
Ray Dataは、データの読み込み、MDT（トレーニングデータの前処理）、データ出力などのタスクのための汎用抽象としてデータセットタスクを提供します。

Figure 10-7 shows how Ray Data is used by Ray Train and Ray Tune. 
図10-7は、Ray DataがRay TrainとRay Tuneでどのように使用されるかを示しています。

Ray is an actor-based frame‐ 
Rayはアクターベースのフレームワークであり、

work, and both Ray Train and Ray Tune use train actors to perform model training (often on GPUs). 
Ray TrainとRay Tuneの両方は、モデルのトレーニングを実行するためにトレインアクターを使用します（通常はGPU上で）。

There is also a pipeline coordinator actor that helps jobs recover from failures. 
ジョブが障害から回復するのを助けるパイプラインコーディネーターアクターも存在します。

_Figure 10-7. Ray is an actor-based framework, with support for distributed training_ 
_図10-7. Rayはアクターベースのフレームワークであり、分散トレーニングをサポートしています_

_(Ray Train) and distributed hyperparameter tuning (Ray Tune). Ray Data enables dis‐_ 
_(Ray Train)および分散ハイパーパラメータチューニング（Ray Tune）。Ray Dataは、_

_[tributed dataset pipeline tasks to be performed in parallel on separate workers. (Image](https://oreil.ly/Yb0eO)_ 
_[分散データセットパイプラインタスクを別々のワーカーで並行して実行できるようにします。 (画像](https://oreil.ly/Yb0eO)_

_[adapted from Ray Docs.)](https://oreil.ly/Yb0eO)_ 
_[Ray Docsからの適応です。](https://oreil.ly/Yb0eO)_

Ray Data is framework agnostic and portable between different distributed training frameworks, including PyTorch and TensorFlow. 
Ray Dataはフレームワークに依存せず、PyTorchやTensorFlowを含むさまざまな分散トレーニングフレームワーク間で移植可能です。

It has an I/O layer for common file formats. 
一般的なファイル形式のためのI/Oレイヤーを持っています。

Ray Data also supports zero-copy exchange between processes, enabling dis‐ 
Ray Dataはプロセス間のゼロコピー交換もサポートしており、

tributed functionality such as global per-epoch shuffling that is interleaved with 
グローバルなエポックごとのシャッフルなどの分散機能を可能にします。



training. If you use Torch datasets, instead, it does not natively support shuffling across worker shards, and you would have to implement it yourself.
トレーニング。代わりにTorchデータセットを使用する場合、ワーカーシャード間でのシャッフルをネイティブにサポートしておらず、自分で実装する必要があります。

This Ray code snippet creates a distributed data preprocessing pipeline that reads Parquet files, applies preprocessing transformations (MDTs), shuffles the data, and then feeds this processed data to a distributed PyTorch training job.
このRayのコードスニペットは、Parquetファイルを読み込み、前処理変換（MDT）を適用し、データをシャッフルし、その後この処理されたデータを分散PyTorchトレーニングジョブに供給する分散データ前処理パイプラインを作成します。

The data-parallel neural network training job runs in parallel across three GPU workers:
データ並列のニューラルネットワークトレーニングジョブは、3つのGPUワーカーで並行して実行されます：

```  
pipe = ray.data.read_parquet(path)  
pipe = pipe.map_batches(preprocess)  
dataset_pipeline = pipe.random_shuffle()  
def train_model():  
    model = NeuralNetworkModel(...)  
    model = train.torch.prepare_model(model)  
    optimizer = torch.optim.Adam(model.parameters())  
    for batch in train.get_dataset_shard().iter_batches():  
        # Proper training loop here  
trainer = Trainer(num_workers=3, backend="torch", use_gpu=True)  
result = trainer.run(train_model, dataset=dataset_pipeline)  
```

###### Parameter-Efficient Fine-Tuning of LLMs
###### パラメータ効率の良いLLMのファインチューニング

LLMs are transformer models. 
LLMはトランスフォーマーモデルです。

The training of LLMs goes through three different phases (see Figure 10-8):
LLMのトレーニングは、3つの異なるフェーズを経ます（図10-8を参照）。

_Pretraining_ This is self-supervised learning on massive amounts of text that is optimized for _perplexity—a measure of the expectation for the next token (technically, perplexity is the exponentiated average negative log likelihood).
_事前学習_ これは、大量のテキストに対する自己教師あり学習であり、_perplexity（次のトークンの期待値の尺度）_に最適化されています（技術的には、perplexityは指数化された平均負の対数尤度です）。

You can extend a foundation LLM with new knowledge with continued pretraining using text data and self-supervised learning.
テキストデータと自己教師あり学習を使用して、基盤となるLLMを新しい知識で拡張できます。

However, you won’t have access to the optimizer states used at the end of pretraining, and there is a risk of catastrophic forgetting, where a pretrained model loses its previously learned knowledge when trained on new tasks or data.
ただし、事前学習の最後に使用されたオプティマイザの状態にアクセスできず、事前学習済みモデルが新しいタスクやデータでトレーニングされると、以前に学習した知識を失う「壊滅的忘却」のリスクがあります。

For these reasons, continued pretraining is not widely adopted.
これらの理由から、継続的な事前学習は広く採用されていません。

_Supervised fine-tuning (SFT)_ This takes the pretrained LLM and fine-tunes it with labeled training data specific to a target task.
_教師ありファインチューニング（SFT）_ これは、事前学習済みのLLMを取り、特定のターゲットタスクに特化したラベル付きトレーニングデータでファインチューニングします。

Common target tasks are to create a chatbot, a summarizer, and a coding assistant.
一般的なターゲットタスクには、チャットボット、要約作成者、コーディングアシスタントの作成があります。

The SFT training data is an instruction dataset, such as a question-and-answer dataset.
SFTトレーニングデータは、質問応答データセットなどの指示データセットです。

_Preference alignment_ This further fine-tunes the instruction model to align its outputs with human preferences, using techniques like RLHF.
_好みの整合_ これは、RLHFのような技術を使用して、指示モデルをさらにファインチューニングし、その出力を人間の好みに合わせます。

_Figure 10-8. LLM chatbot training undergoes three separate training phases: pretraining,_ _supervised fine-tuning with instruction datasets, and preference alignment with RLHF._
_Figure 10-8. LLMチャットボットのトレーニングは、事前学習、指示データセットを用いた教師ありファインチューニング、RLHFによる好みの整合という3つの異なるトレーニングフェーズを経ます。_

In RLHF, humans first generate preference data by ranking or selecting the best response from a set of model outputs for a given prompt.
RLHFでは、人間が最初に、特定のプロンプトに対するモデル出力のセットから最良の応答をランク付けまたは選択することによって、好みデータを生成します。

A sample row in a preference alignment training dataset might look as follows (a human has labeled Response 1 as “preferred”):
好みの整合トレーニングデータセットのサンプル行は次のようになります（人間が応答1を「好ましい」とラベル付けしています）：

Prompt: “What is the capital of Sweden?”
プロンプト: 「スウェーデンの首都は何ですか？」

Response 1 (preferred): “The capital of Sweden is Stockholm.”
応答1（好ましい）: 「スウェーデンの首都はストックホルムです。」

Response 2 (not preferred): “Sweden is big, and the biggest city is Stockholm.”
応答2（好ましくない）: 「スウェーデンは大きく、最大の都市はストックホルムです。」

By selecting one preferred answer from two to four different possible answers, you create training data.
2つから4つの異なる可能な回答の中から1つの好ましい回答を選択することによって、トレーニングデータを作成します。

This training data is then used to train a reward model, which estimates the quality of a response.
このトレーニングデータは、その後、応答の質を推定する報酬モデルのトレーニングに使用されます。

The _reward model guides a reinforcement learning_ [algorithm (such as Proximal Policy Optimization [PPO]) to adjust the policy model so](https://oreil.ly/y0IGT) that its outputs align more closely with human preferences.
_報酬モデルは強化学習_ [アルゴリズム（近接ポリシー最適化[PPO]など）をガイドし、ポリシーモデルを調整して](https://oreil.ly/y0IGT)、その出力が人間の好みにより密接に一致するようにします。

Different LLMs may give different responses based on how they were aligned.
異なるLLMは、どのように整合されているかに基づいて異なる応答を返す場合があります。

For example, what if you ask an LLM, “What is the status of Taiwan and Palestine?”
例えば、LLMに「台湾とパレスチナの状況はどうですか？」と尋ねた場合、どうなるでしょうか？

The “Chinese” DeepSeek R1 model gives answers that are different from those from the “American” Llama 3.1 model.
「中国」のDeepSeek R1モデルは、「アメリカ」のLlama 3.1モデルとは異なる回答を返します。

Both are open source LLMs, and both were pretrained on roughly the same data (all text documents accessible on the internet).
どちらもオープンソースのLLMであり、どちらもほぼ同じデータ（インターネット上でアクセス可能なすべてのテキストドキュメント）で事前学習されています。

The different answers they produce, however, are due to their different post-training finetuning and preference alignment steps.
しかし、彼らが生成する異なる回答は、異なる事後トレーニングファインチューニングと好みの整合ステップによるものです。

Recently in 2025, large reasoning models (see Chapter 12), like DeepSeek R1, have favored reinforcement learning over SFT for fine-tuning.
最近の2025年には、DeepSeek R1のような大規模推論モデル（第12章を参照）が、ファインチューニングにおいてSFTよりも強化学習を好むようになっています。

The only constant in post-training techniques is that they keep evolving.
事後トレーニング技術における唯一の一定のことは、それらが進化し続けるということです。

Many organizations are interested in fine-tuning foundation LLMs to optimize their performance for a task of interest.
多くの組織は、特定のタスクのパフォーマンスを最適化するために基盤となるLLMのファインチューニングに関心を持っています。

The most accessible method is to use parameter_efficient fine-tuning (PEFT), a technique that requires far fewer GPU resources than does full fine-tuning, as it does not update the weights of the base model.
最もアクセスしやすい方法は、パラメータ効率の良いファインチューニング（PEFT）を使用することであり、これはフルファインチューニングよりもはるかに少ないGPUリソースを必要とする技術です。なぜなら、ベースモデルの重みを更新しないからです。

Instead, PEFT updates the weights of a smaller adapter model.
代わりに、PEFTは小さなアダプタモデルの重みを更新します。

LoRA is the most popular PEFT adapter model (see Figure 10-9).
LoRAは最も人気のあるPEFTアダプタモデルです（図10-9を参照）。

LoRA freezes the original weights of the LLM and adds small, trainable low-rank matrices to selected weight matrices, most commonly the query and value projection layers within the transformer’s attention blocks.
LoRAはLLMの元の重みを固定し、選択された重み行列に小さく、トレーニング可能な低ランク行列を追加します。最も一般的には、トランスフォーマーのアテンションブロック内のクエリと値のプロジェクション層です。

Quantized LoRA (QLoRA) is an optimized version of LoRA that requires even less GPU memory than LoRA, as it uses smaller four-bit weights in the base model (at the cost of slightly worse model performance).
量子化LoRA（QLoRA）は、LoRAの最適化されたバージョンであり、ベースモデル内でより小さな4ビットの重みを使用するため、LoRAよりもさらに少ないGPUメモリを必要とします（モデルのパフォーマンスがわずかに低下する代償として）。

_Figure 10-9. LoRA for parameter-efficient supervised fine-tuning of LLMs._
_Figure 10-9. LLMのパラメータ効率の良い教師ありファインチューニングのためのLoRA。_

LoRA (as well as QLoRA) is based on the insight that foundation models often have a _low intrinsic dimension, meaning that they can often be described with far fewer_ dimensions than what is represented in the original weights.
LoRA（およびQLoRA）は、基盤モデルがしばしば_低い内在次元_を持ち、元の重みで表現されているよりもはるかに少ない次元で説明できることに基づいています。

The implication of this insight is that the updates to the model weights (e.g., parameters) have a low intrinsic rank during model adaptation, meaning you can use smaller matrices, with fewer dimensions, to fine-tune.
この洞察の意味は、モデル適応中にモデルの重み（例えば、パラメータ）の更新が低い内在ランクを持つため、より少ない次元の小さな行列を使用してファインチューニングできるということです。

The final output is obtained by summing the outputs of the base LLM model and the LoRA adapter.
最終的な出力は、ベースLLMモデルとLoRAアダプタの出力を合計することによって得られます。

By reducing the number of trainable parameters, LoRA reduces both the training time required and the amount of GPU memory needed.
トレーニング可能なパラメータの数を減らすことによって、LoRAは必要なトレーニング時間とGPUメモリの量の両方を減少させます。

You can also share the same base model for many LoRA adapters.
また、多くのLoRAアダプタに対して同じベースモデルを共有することもできます。

A sample instruction dataset for LoRA fine-tuning could look as follows:
LoRAファインチューニングのためのサンプル指示データセットは次のようになります：

```  
{  
    "instruction": "Name one famous Swedish company.",  
    "input": "",  
    "output": "IKEA"  
}  
```

For organizations without their own fleet of GPUs, fine-tuning is often preferable to pretraining a new LLM.
自社のGPUのフリートを持たない組織にとって、ファインチューニングは新しいLLMの事前学習よりも好まれることが多いです。

As of mid-2025, open source and open-weight foundation models are close in performance to the best proprietary models.
2025年中頃の時点で、オープンソースおよびオープンウェイトの基盤モデルは、最高のプロプライエタリモデルに近いパフォーマンスを持っています。

You can build your finetuning instruction dataset once and fine-tune many LLMs with it, always staying up-to-date with the latest open source foundation LLM.
ファインチューニング指示データセットを一度構築し、それを使用して多くのLLMをファインチューニングすることができ、常に最新のオープンソース基盤LLMに追いつくことができます。

Fine-tuning is, however, not good at adding new knowledge to or replacing existing knowledge in LLMs.
ただし、ファインチューニングはLLMに新しい知識を追加したり、既存の知識を置き換えたりするのには適していません。

If you need to add new knowledge, you can do it at inference time through either prompt engineering or RAG.
新しい知識を追加する必要がある場合は、プロンプトエンジニアリングまたはRAGを通じて推論時に行うことができます。

###### Credit Card Fraud Model with XGBoost
###### XGBoostによるクレジットカード詐欺モデル

We now take a brief detour from deep learning to examine training our credit card fraud detection model, XGBoost—an ensemble of gradient-boosted decision trees.
ここで、深層学習から少し離れて、クレジットカード詐欺検出モデルであるXGBoost（勾配ブースト決定木のアンサンブル）のトレーニングを検討します。

As stated earlier, in the submillion sample data regime, decision trees outperform deep learning.
前述のように、サブミリオンサンプルデータの領域では、決定木が深層学習を上回ります。

When solving a supervised-learning problem, we will have a big challenge, though: there is a large class imbalance.
ただし、教師あり学習の問題を解決する際には、大きな課題があります。それは、大きなクラスの不均衡が存在することです。

That is, there are many more nonfraud transactions than fraudulent transactions.
つまり、詐欺でない取引が詐欺取引よりもはるかに多いのです。

It is possible to build an unsupervised-learning model based on anomaly detection, [such as a GAN-based anomaly detection model.
異常検出に基づく教師なし学習モデルを構築することは可能ですが、[GANベースの異常検出モデルのように。

However, their latency is too high for](https://oreil.ly/cjvMM) real-time credit card transaction validation.
ただし、リアルタイムのクレジットカード取引検証にはレイテンシが高すぎます。](https://oreil.ly/cjvMM)

As such, we will follow the KISS (keep it simple, stupid) approach and use an XGBoost binary classifier that will provide 1–2 ms latency for inference requests on a multicore server.
そのため、KISS（シンプルに保つ、愚か者）アプローチに従い、マルチコアサーバーでの推論リクエストに対して1〜2msのレイテンシを提供するXGBoostバイナリ分類器を使用します。

We will address the large imbalance between the positive class (fraud) and the negative class (no fraud) by upsampling the positive class and downsampling the negative class.
ポジティブクラス（詐欺）とネガティブクラス（詐欺でない）との間の大きな不均衡に対処するために、ポジティブクラスをアップサンプリングし、ネガティブクラスをダウンサンプリングします。

Some hyperparameter tuning tips for XGBoost with larger training datasets (of 1M rows or so) are:
1M行程度の大きなトレーニングデータセットに対するXGBoostのハイパーパラメータチューニングのヒントは次のとおりです：

- Increase `max_depth and adjust` `n_estimators with early stopping to control` overfitting.
- `max_depth`を増加させ、`n_estimators`を調整し、早期停止を使用して過学習を制御します。

- Decrease `learning_rate and use GPU acceleration (tree_method='gpu_hist')` to speed up training (smaller learning rates increase training time).
- `learning_rate`を減少させ、GPUアクセラレーション（`tree_method='gpu_hist'`）を使用してトレーニングを加速します（小さな学習率はトレーニング時間を増加させます）。

- Increase `lambda,` `alpha, and` `min_child_weight to control overfitting and` generalization.
- 過学習と一般化を制御するために、`lambda`、`alpha`、および`min_child_weight`を増加させます。



Here is a snippet showing hyperparameter tuning using Ray Tune for the preceding hyperparameters: 
ここでは、前述のハイパーパラメータに対するRay Tuneを使用したハイパーパラメータチューニングのスニペットを示します。

```   
def train_xgboost(config):     
    model = xgb.XGBClassifier(       
        objective='binary:logistic',       
        max_depth=config['max_depth'],       
        n_estimators=config['n_estimators'],       
        learning_rate=config['learning_rate'],       
        reg_lambda=config['reg_lambda'],       
        reg_alpha=config['reg_alpha'],       
        min_child_weight=config['min_child_weight'],       
        eval_metric='logloss'     
    )     
    model.fit(X_train, y_train, \       
        eval_set=[(X_val, y_val)], early_stopping_rounds=20)     
    preds = model.predict(X_val)     
    f1 = f1_score(y_val, preds)     
    tune.report({"f1_score": f1})   
search_space = { # Define the hyperparameter search space     
    'max_depth': tune.choice([3, 5, 7, 9, 11]),     
    'n_estimators': tune.choice([50, 100, 200, 300]),     
    'learning_rate': tune.loguniform(0.01, 0.3),     
    'reg_lambda': tune.loguniform(1e-3, 10),     
    'reg_alpha': tune.loguniform(1e-3, 10),     
    'min_child_weight': tune.choice([1, 3, 5, 7])   
}   
analysis = tune.run( # Run hyperparameter tuning     
    train_xgboost,     
    config=search_space,     
    num_samples=50,     
    resources_per_trial={"cpu": 2, "gpu": 0},     
    metric="f1_score",     
    mode="max"   
)   
best_config = analysis.get_best_result("f1_score")   
print(f"Best hyperparameters: {best_config}")
``` 
このコードは、完全なトレーニング実行に使用できる最適なハイパーパラメータのbest_configを生成します。GPUにアクセスできる場合は、XGBoostのGPUアクセラレーションを有効にすることで、``` tree_method='gpu_hist' ```トレーニング時間を大幅に短縮できます。

###### Identifying Bottlenecks in Distributed Training
###### 分散トレーニングにおけるボトルネックの特定

``` 
We saw already that you can use a cluster of GPUs to reduce training time for deep learning models. 
すでに、GPUのクラスターを使用して深層学習モデルのトレーニング時間を短縮できることを見ました。

The GPUs can either be colocated on the same host (in a GPU server, such as NVIDIA’s DGX with up to 16 GPUs) or distributed across many hosts that are connected together via a high-performance network (such as Infiniband).
GPUは、同じホスト上に配置される（NVIDIAのDGXのように最大16のGPUを持つGPUサーバー内）か、高性能ネットワーク（Infinibandなど）を介して接続された多くのホストに分散されることができます。

Distributed training involves workers (each of which manages a single GPU) collaborating to train a model using a distributed training algorithm, such as ring all-reduce.
分散トレーニングは、各ワーカーが単一のGPUを管理し、ring all-reduceのような分散トレーニングアルゴリズムを使用してモデルをトレーニングするために協力することを含みます。

Ring all-reduce is an architecture in which workers are connected logically in a ring, and they use both their upload and download network bandwidth capacity to share gradients (computed locally by each GPU using its own subset of training data) with their neighboring workers.
Ring all-reduceは、ワーカーが論理的にリングに接続され、アップロードおよびダウンロードのネットワーク帯域幅を使用して、隣接するワーカーと勾配（各GPUが自分のトレーニングデータのサブセットを使用してローカルに計算したもの）を共有するアーキテクチャです。

Ring all-reduce works on both the GPU interconnect and across the network. 
Ring all-reduceは、GPUインターコネクトとネットワークの両方で機能します。

A multihost training setup is shown in Figure 10-10, where the workers are spread across multiple GPU servers and each server has eight GPUs.
マルチホストトレーニングセットアップは、図10-10に示されており、ワーカーは複数のGPUサーバーに分散され、各サーバーには8つのGPUがあります。

Training data is stored in a shared object store.
トレーニングデータは、共有オブジェクトストアに保存されます。

_Figure 10-10. Match up hardware and network performance to maximize GPU utilization._
_Figure 10-10. ハードウェアとネットワークのパフォーマンスを一致させてGPUの利用率を最大化します。_

Each GPU server has one or more local (fast) nonvolatile memory express (NVMe) disks to cache a partition of training samples (rows). 
各GPUサーバーには、トレーニングサンプル（行）のパーティションをキャッシュするための1つ以上のローカル（高速）不揮発性メモリエクスプレス（NVMe）ディスクがあります。

This helps prevent training bottlenecking on reading training data from the object store. 
これにより、オブジェクトストアからトレーニングデータを読み取る際のトレーニングボトルネックを防ぐのに役立ちます。

The GPU servers have a GPU interconnect (such as NVIDIA’s NVLink 5.0 that supports up to 1.8 TB/s aggregate bidirectional links between GPUs) connecting all GPUs. 
GPUサーバーには、すべてのGPUを接続するGPUインターコネクト（NVIDIAのNVLink 5.0のように、最大1.8 TB/sの集約双方向リンクをGPU間でサポート）が備わっています。

The GPUs transfer data to/from main memory on the server using the Peripheral Component Interconnect Express (PCIe) 5.0 bus (which has a number of PCI lanes—16 lanes gives you 64 GB/s).
GPUは、Peripheral Component Interconnect Express (PCIe) 5.0バスを使用してサーバーのメインメモリとのデータを転送します（このバスには複数のPCIレーンがあり、16レーンで64 GB/sを提供します）。

The GPU servers are connected together via a dedicated 400 Gb/s (50 GB/s) network. 
GPUサーバーは、専用の400 Gb/s（50 GB/s）ネットワークを介して接続されています。

The network is also used to read training data from object storage and to copy training data from object storage to local NVMe disks if object storage is too slow (which is often the case).
このネットワークは、オブジェクトストレージからトレーニングデータを読み取るためにも使用され、オブジェクトストレージが遅すぎる場合（これはしばしば発生します）、トレーニングデータをオブジェクトストレージからローカルNVMeディスクにコピーするためにも使用されます。

A dedicated network may be used for storage traffic so as not to compete with gradient synchronization traffic during training.
専用のネットワークは、トレーニング中に勾配同期トラフィックと競合しないようにストレージトラフィックに使用される場合があります。

If you experience low GPU utilization during training in this setup, Figure 10-11 presents a process for the root cause analysis of your low GPU utilization.
このセットアップでトレーニング中にGPUの利用率が低い場合、図10-11は低いGPU利用率の根本原因分析のプロセスを示しています。

We assume Linux hosts.
Linuxホストを前提としています。

_Figure 10-11. Analyze throughput and utilization in the storage, networking, and memory hierarchy to find distributed training bottlenecks._
_Figure 10-11. ストレージ、ネットワーキング、およびメモリ階層におけるスループットと利用率を分析して分散トレーニングのボトルネックを見つけます。_

You start your debugging process by observing GPU utilization levels during training with something like a cluster-wide Grafana dashboard or a command-line tool for your server(s), like nvidia-smi: 
トラブルシューティングプロセスは、クラスター全体のGrafanaダッシュボードや、nvidia-smiのようなサーバー用のコマンドラインツールを使用して、トレーニング中のGPU利用率レベルを観察することから始まります。

```   
nvidia-smi -l
``` 
GPUの利用率が望ましいよりも低いと仮定すると、次に階層の1つ下に移動して、GPU間のインターコネクトがボトルネックであるかどうかを確認します。

On each host, you can use the nvlink subcommand to observe network bandwidth utilization between GPUs (assuming you have NVLink connecting your GPUs): 
各ホストで、nvlinkサブコマンドを使用してGPU間のネットワーク帯域幅利用率を観察できます（GPUを接続するNVLinkがあると仮定します）：

```   
nvidia-smi nvlink --status
```
CUDA also comes with a utility program `bandwidthTest that measures the bandwidth between GPUs and from GPUs across the PCIe bus to host memory. 
CUDAには、GPU間およびGPUからホストメモリへのPCIeバスを介した帯域幅を測定するユーティリティプログラム`bandwidthTest`も付属しています。

If memory bus bandwidth is not a bottleneck, you can measure local disk I/O bandwidth utilization—assuming you are caching the training data on local (NVMe) disks. 
メモリバスの帯域幅がボトルネックでない場合、ローカル（NVMe）ディスクにトレーニングデータをキャッシュしていると仮定して、ローカルディスクI/O帯域幅利用率を測定できます。

On Linux hosts, you can use a command-line utility, such as `iostat, to measure local disk I/O: 
Linuxホストでは、`iostat`のようなコマンドラインユーティリティを使用してローカルディスクI/Oを測定できます：

```   
iostat -x 1 <device-name>
``` 
This prints disk read/write rates in MB/s every second and the idle percentage. 
これにより、毎秒MB/s単位でディスクの読み取り/書き込み速度とアイドル率が表示されます。

If disk I/O is not a bottleneck, check network bandwidth utilization using tools like bmon or `iftop. 
ディスクI/Oがボトルネックでない場合、bmonや`iftop`のようなツールを使用してネットワーク帯域幅利用率を確認します。

Compare measured bandwidth with your available capacity. 
測定された帯域幅を利用可能な容量と比較します。

If it’s significantly lower, you may be bottlenecked by reading training data from object storage. 
それが大幅に低い場合、オブジェクトストレージからトレーニングデータを読み取ることによってボトルネックが発生している可能性があります。

One fix is to pre-copy training data from object storage to local NVMe disks. 
1つの解決策は、オブジェクトストレージからローカルNVMeディスクにトレーニングデータを事前にコピーすることです。

Another is to use a tiered storage setup with shared high-performance NVMe between workers and object storage. 
別の解決策は、ワーカーとオブジェクトストレージの間で共有された高性能NVMeを使用した階層ストレージセットアップを使用することです。

If neither is possible, ensure your dataset is split into enough files to be read in parallel to saturate available bandwidth.
どちらも不可能な場合は、データセットが十分なファイルに分割されていることを確認し、利用可能な帯域幅を飽和させるために並行して読み取ることができるようにします。

Together, these steps are a guide for finding hardware-related training bottlenecks and removing them, enabling higher GPU utilization.
これらのステップは、ハードウェア関連のトレーニングボトルネックを見つけて取り除くためのガイドであり、より高いGPU利用率を可能にします。

###### Model Evaluation and Model Validation
###### モデル評価とモデル検証

Now that you have trained your model, you should evaluate it using test data to determine its performance for the intended task. 
モデルをトレーニングしたので、テストデータを使用してそのパフォーマンスを評価する必要があります。

You also need to validate that the model is free from bias—we will use evaluation data to validate the model. 
また、モデルがバイアスがないことを検証する必要があります。評価データを使用してモデルを検証します。

The evaluation data is not just the holdout set to measure model performance but different slices of the holdout set containing entities (such as related groups of users) who are considered to be at risk of bias.
評価データは、モデルのパフォーマンスを測定するためのホールドアウトセットだけでなく、バイアスのリスクがあると見なされるエンティティ（関連するユーザーグループなど）を含むホールドアウトセットの異なるスライスです。

Model evaluation and validation are typically performed in the training pipeline (directly after model training has finished). 
モデル評価と検証は通常、トレーニングパイプライン内で（モデルのトレーニングが終了した直後に）実行されます。

It is also possible to have a separate model validation pipeline that runs after model training completes. 
モデルのトレーニングが完了した後に実行される別のモデル検証パイプラインを持つことも可能です。

The input into a model validation pipeline is a trained model and evaluation data, and the output is a model validation scorecard for your model. 
モデル検証パイプラインへの入力はトレーニング済みモデルと評価データであり、出力はモデルの検証スコアカードです。

Model evaluation and validation results are typically stored with the model in the model registry. 
モデル評価と検証の結果は通常、モデルレジストリ内のモデルと共に保存されます。

Some reasons for having a separate model validation pipeline are:
別のモデル検証パイプラインを持つ理由はいくつかあります：

- Your training pipeline allocates both GPUs and CPUs, and training only uses GPUs, while model validation requires only CPUs. 
- トレーニングパイプラインはGPUとCPUの両方を割り当て、トレーニングはGPUのみを使用しますが、モデル検証はCPUのみを必要とします。

But GPUs are only released when the pipeline completes, causing your pipeline to unnecessarily hold expensive GPUs for longer than necessary.
しかし、GPUはパイプラインが完了するまで解放されないため、パイプラインが不必要に高価なGPUを長時間保持することになります。

- Model validation is managed by a separate team that owns the compliance tests.
- モデル検証は、コンプライアンステストを所有する別のチームによって管理されます。



- Model training produces a huge number of candidate models, and it is easier and/or more cost-effective to validate many models in a batch model validation pipeline.
- モデルのトレーニングは膨大な数の候補モデルを生成し、バッチモデル検証パイプラインで多くのモデルを検証する方が容易であるか、またはコスト効率が良いです。

###### Model Performance for Classification and Regression
###### 分類と回帰のためのモデル性能

Model performance evaluation is tightly coupled with the type of ML model: classification, regression, or other.
モデルの性能評価は、MLモデルの種類（分類、回帰、またはその他）と密接に関連しています。

You should evaluate regression models by using metrics such as mean absolute error (MAE), mean squared error (MSE), and R-squared. 
回帰モデルは、平均絶対誤差（MAE）、平均二乗誤差（MSE）、およびR二乗などの指標を使用して評価する必要があります。

R-squared measures the proportion of variance in the target explained by the model. 
R二乗は、モデルによって説明されるターゲットの分散の割合を測定します。

It is dimensionless and remains the same across different scales of target values. 
これは無次元であり、異なるターゲット値のスケールに関係なく同じです。

You should use it to compare different models on the same dataset to assess relative performance.
異なるモデルの相対的な性能を評価するために、同じデータセット上で異なるモデルを比較するために使用する必要があります。

You should evaluate classification models by using the metrics of accuracy, precision, recall, and F1 score. 
分類モデルは、精度、適合率、再現率、およびF1スコアの指標を使用して評価する必要があります。

For our credit card fraud model, ROC AUC (receiver operating characteristic—area under the curve) measures the ability of a classification model to distinguish between classes by evaluating the trade-off between the true positive rate (sensitivity) and the false positive rate across different threshold values, with higher values indicating better model performance.
私たちのクレジットカード詐欺モデルでは、ROC AUC（受信者動作特性—曲線下面積）が、異なる閾値における真陽性率（感度）と偽陽性率のトレードオフを評価することによって、分類モデルがクラスを区別する能力を測定し、高い値はより良いモデル性能を示します。

In our credit card fraud model, we evaluate the model’s performance on the test set as the accuracy, F1 score, and ROC AUC.
私たちのクレジットカード詐欺モデルでは、テストセットにおけるモデルの性能を精度、F1スコア、およびROC AUCとして評価します。

The confusion matrix shows the counts for predicting correctly (true positive and true negative) and incorrectly (false positive and false negative) on the test set.
混同行列は、テストセットにおける正しく予測した数（真陽性と真陰性）と誤って予測した数（偽陽性と偽陰性）を示します。

Here is code to calculate these evaluation metrics using the model, predictions, and test set: 
以下は、モデル、予測、およびテストセットを使用してこれらの評価指標を計算するためのコードです：

```   
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix   
y_pred = model.predict(X_test)   
y_prob = model.predict_proba(X_test)[:, 1]    

accuracy = accuracy_score(y_test, y_pred)   
f1 = f1_score(y_test, y_pred)   
cm = confusion_matrix(y_test, y_pred)   
roc_auc = roc_auc_score(y_test, y_prob)
```

###### Model Interpretability
###### モデルの解釈可能性

In some domains where compliance is important, like finance, healthcare, and insurance, you need to understand and explain how an ML model makes its predictions, a concept known as model interpretability.
金融、医療、保険など、コンプライアンスが重要な分野では、MLモデルがどのように予測を行うかを理解し説明する必要があります。これはモデルの解釈可能性として知られています。

It adds transparency to the model’s predictions, building stakeholders’ trust and ensuring compliance with regulations.
これはモデルの予測に透明性を加え、利害関係者の信頼を築き、規制への準拠を確保します。

One popular technique for interpreting complex models is using SHAP (SHapley Additive exPlanations) values, which provide a unified measure of feature importance based on game theory:
複雑なモデルを解釈するための一般的な手法の一つは、SHAP（SHapley Additive exPlanations）値を使用することで、これはゲーム理論に基づいた特徴の重要性の統一的な測定を提供します：

```   
import shap   
explainer = shap.Explainer(model, X_test)   
shap_values = explainer(X_test)   
# Summary plot to visualize feature importance   
shap.summary_plot(shap_values, X_test)
```

SHAP values are particularly effective when used in decision trees and ensemble models, but they can also be applied to NNs using specialized explainers such as Deep Explainer.
SHAP値は、決定木やアンサンブルモデルで使用されると特に効果的ですが、Deep Explainerなどの専門的な説明者を使用してNNにも適用できます。

However, NNs’ nonlinear nature makes their interpretation challenging.
しかし、NNの非線形性はその解釈を難しくします。

There is, however, one technique that is widely used to evaluate NNs. 
しかし、NNを評価するために広く使用されている手法があります。

Ablation studies evaluate the contribution of different components or features of an NN by systematically “ablating” (removing or altering) parts of its architecture.
アブレーションスタディは、NNの異なるコンポーネントや特徴の寄与を評価するために、そのアーキテクチャの一部を体系的に「アブレート」（削除または変更）することによって評価します。

By removing a feature, model layer, or regularizer and rerunning performance tests, you can determine how much the removed part contributed to overall model performance.
特徴、モデル層、または正則化項を削除し、性能テストを再実行することによって、削除された部分が全体のモデル性能にどれだけ寄与したかを判断できます。

Note that the inputs into the SHAP explainer, X_test, are the transformed feature values (the inputs into the model after MDTs have been applied).
SHAP説明者への入力であるX_testは、変換された特徴値（MDTが適用された後のモデルへの入力）であることに注意してください。

In feature monitoring (see Chapter 14), we commonly use the untransformed feature values as inputs into feature monitoring algorithms.
特徴モニタリング（第14章を参照）では、通常、未変換の特徴値を特徴モニタリングアルゴリズムへの入力として使用します。

###### Model Bias Tests
###### モデルバイアステスト

Model bias tests should assess and measure potential bias in a model.
モデルバイアステストは、モデルにおける潜在的なバイアスを評価し測定する必要があります。

If a model passes all bias tests, it can be marked as free from known bias and continue to production.
モデルがすべてのバイアステストに合格すれば、既知のバイアスがないとマークされ、製品に進むことができます。

For this, you need to extract different slices of evaluation data from the test dataset.
これには、テストデータセットから異なる評価データのスライスを抽出する必要があります。

For example, you can group users by gender, age, ethnicity, orientation, location, and so on.
たとえば、ユーザーを性別、年齢、民族、オリエンテーション、場所などでグループ化できます。

Model bias tests evaluate the model on these different subsets of users who are considered to be at risk of bias.
モデルバイアステストは、バイアスのリスクがあると考えられるこれらの異なるユーザーのサブセットに対してモデルを評価します。

In Hopsworks, you can use filters and training helper columns in a feature view to help create evaluation data.
Hopsworksでは、フィルターとトレーニングヘルパーカラムを特徴ビューで使用して評価データを作成できます。

For example, a column describing a user could be their gender, and you may want to evaluate the model for gender bias.
たとえば、ユーザーを説明する列は性別であり、性別バイアスについてモデルを評価したい場合があります。

However, you don’t want to train the model using gender as a feature.
ただし、性別を特徴としてモデルをトレーニングしたくはありません。

That would probably introduce gender bias into the model.
それはおそらくモデルに性別バイアスを導入することになります。

Instead, you use the gender as a training helper column in your training data, using it to group rows into evaluation datasets, organized by gender.
代わりに、性別をトレーニングデータのトレーニングヘルパーカラムとして使用し、性別で整理された評価データセットに行をグループ化します。

The training helper columns are dropped before training and not returned when reading inference data, so they are not learned by the model:
トレーニングヘルパーカラムはトレーニングの前に削除され、推論データを読み取るときには返されないため、モデルによって学習されません：

```   
fv = fs.create_feature_view(name="trans_fv", version=1,     
training_helper_columns=["gender"],     
...
)   
X_train, X_test, y_train, y_test = fv.train_test_split(     
test_size=0.2,
```

```     
training_helper_columns=True   
)   
X_train = X_train.drop("gender", axis=1) # Drop helper column before training   
model = xgboost.XGBClassifier().fit(X_train, y_train)   
# Evaluate on female subset   
female_mask = X_test["gender"] == "female"   
X_female_test = X_test[female_mask].drop("gender", axis=1)   
y_female_test = y_test[female_mask]   
y_female_pred = model.predict(X_female_test)   
female_accuracy = accuracy_score(y_female_test, y_female_pred)
```

###### Model File Formats and the Model Registry
###### モデルファイル形式とモデルレジストリ

From a software engineering perspective, training a model is conceptually similar to compiling a program into a binary—you build once and deploy anywhere.
ソフトウェア工学の観点から、モデルをトレーニングすることは、プログラムをバイナリにコンパイルすることに概念的に似ています。つまり、一度構築し、どこにでも展開します。

The model registry plays the same roles as the artifact registry in software engineering—it stores immutable models (as files) that can be later downloaded and used by inference pipelines.
モデルレジストリは、ソフトウェア工学におけるアーティファクトレジストリと同じ役割を果たします。すなわち、後でダウンロードして推論パイプラインで使用できる不変のモデル（ファイルとして）を保存します。

The most common file formats for saved models are:
保存されたモデルの最も一般的なファイル形式は次のとおりです：

_.safetensors_ Interoperable, efficient model format (PyTorch, TensorFlow, etc.) used by most LLMs and transformer models. 
_.safetensors_は、ほとんどのLLMおよびトランスフォーマーモデルで使用される相互運用可能で効率的なモデル形式です。

Models larger than 2 GB are typically stored as sharded files to enable parallel loading of LLMs.
2GBを超えるモデルは、通常、LLMの並列読み込みを可能にするためにシャードファイルとして保存されます。

_.pkl_ Scikit-Learn models. 
_.pkl_は、Scikit-Learnモデルです。

Create a pickled Python object using the joblib library.
joblibライブラリを使用してピクルスされたPythonオブジェクトを作成します。

Make sure you use the same version in training/inference pipelines. 
トレーニング/推論パイプラインで同じバージョンを使用することを確認してください。

Warning: pickle has a major, inherent security risk—it can execute arbitrary code when loading data.
警告：pickleには重大な固有のセキュリティリスクがあります。データを読み込むときに任意のコードを実行する可能性があります。

_.json_ XGBoost/LightGBM models. 
_.json_は、XGBoost/LightGBMモデルです。

You should prefer .json over .pkl.
.jsonを.pklよりも優先するべきです。

_.onnx_ Interoperable model format (PyTorch, TensorFlow, etc.) requires either Open Neural Network Exchange (ONNX) runtime or supported runtime, such as TensorRT.
_.onnx_は、相互運用可能なモデル形式（PyTorch、TensorFlowなど）で、Open Neural Network Exchange（ONNX）ランタイムまたはTensorRTなどのサポートされたランタイムが必要です。

_.pt and .pth_ Generic PyTorch checkpoint file formats that can be used to resume training.
_.ptおよび.pth_は、トレーニングを再開するために使用できる一般的なPyTorchチェックポイントファイル形式です。

_.engine_ TensorRT file format that is optimized for NVIDIA GPUs and requires TensorRT server.
_.engine_は、NVIDIA GPUに最適化されたTensorRTファイル形式で、TensorRTサーバーが必要です。

_.pb and .h5_ TensorFlow model file formats (.pb is protobuf and .h5 is interoperable).
_.pbおよび.h5_は、TensorFlowモデルファイル形式です（.pbはprotobufで、.h5は相互運用可能です）。

_.bin and .ckpt with optimizer states (Lightning Checkpoints)_ These are used if you need optimizer states and full checkpoint information (not just model weights) for continued training or fine-tuning.
_.binおよび.ckpt（オプティマイザーステート付き）（Lightning Checkpoints）は、継続的なトレーニングやファインチューニングのためにオプティマイザーステートと完全なチェックポイント情報（モデルの重みだけでなく）が必要な場合に使用されます。

###### Model Cards
###### モデルカード

_Model cards are one-page overviews of models in the model registry that are increasingly required for governance and compliance._
モデルカードは、モデルレジストリ内のモデルの1ページの概要であり、ガバナンスとコンプライアンスのためにますます必要とされています。

They are useful cheat sheets for sharing model information, particularly in a team where the person who trains the model is not the one who deploys it to production.
これは、モデル情報を共有するための便利なチートシートであり、特にモデルをトレーニングする人がそれを製品に展開する人ではないチームにおいて役立ちます。

A model card includes information about the model, its performance, whether it has passed validation tests, and usage instructions or guidance so that the model can be deployed to production.
モデルカードには、モデルに関する情報、性能、検証テストに合格したかどうか、モデルを製品に展開できるようにするための使用指示やガイダンスが含まれています。

It is common to include the results of the model’s evaluation and bias tests.
モデルの評価結果やバイアステストの結果を含めることは一般的です。

Often, these are PNG files—plots or graphs.
これらはしばしばPNGファイル—プロットやグラフです。

In general, the code in your training pipeline will be able to generate anywhere from 20% to 60% of the information in the following sample model card when you register your model.
一般的に、モデルを登録する際に、トレーニングパイプライン内のコードは、以下のサンプルモデルカードの情報の20%から60%を生成できるでしょう。



. For deployed models, your model card should strive to cover 100% of the categories, and you should have a process to ensure accurate and complete model cards:
展開されたモデルの場合、モデルカードは100%のカテゴリをカバーするよう努めるべきであり、正確で完全なモデルカードを確保するためのプロセスを持つべきです。

**Model Name/Version: [Model Name, Version Number]**
**モデル名/バージョン: [モデル名、バージョン番号]**

**Date: [MM/DD/YYYY]**
**日付: [MM/DD/YYYY]**

**Intended Use:**
**意図された使用:**
- [Describe the primary purpose of the model and intended applications and stake‐ holders]
- [モデルの主な目的と意図されたアプリケーションおよび利害関係者を説明してください]
- [Describe not intended uses, where the model should not be used]
- [意図されていない使用、モデルを使用すべきでない場所を説明してください]

**Model Details:**
**モデルの詳細:**
- Model Architecture: [e.g., Random Forest, CNN, Transformer, etc.]
- モデルアーキテクチャ: [例: ランダムフォレスト、CNN、トランスフォーマーなど]
- Feature View: Input features required by model
— Training Data: Size and feature groups used
- 特徴ビュー: モデルに必要な入力特徴
— トレーニングデータ: 使用されるサイズと特徴グループ
- Model Signature: [Input features and output labels for model]  
- モデルシグネチャ: [モデルの入力特徴と出力ラベル]  

-----
**Performance Evaluation:**
**パフォーマンス評価:**
- Evaluation Metrics: [RMSE, F1 score, ROC AUC, etc.]
- 評価指標: [RMSE、F1スコア、ROC AUCなど]
- Test Dataset: [Describe the test dataset—size, split policy]
- テストデータセット: [テストデータセットを説明—サイズ、分割ポリシー]
- Performance Results: [Provide key performance numbers on test data]
- パフォーマンス結果: [テストデータにおける主要なパフォーマンス数値を提供]
- Comparison with Baselines: [How does it compare with existing methods?]
- ベースラインとの比較: [既存の方法と比較してどうか？]

**Ethical Considerations and Limitations:**
**倫理的考慮事項と制限:**
- Bias: [Evaluation datasets and bias tests performed]
- バイアス: [評価データセットと実施されたバイアステスト]
- Potential Risks and Limitations: [Describe potential harms and limitations of the model]
- 潜在的リスクと制限: [モデルの潜在的な危害と制限を説明]

**Deployment and Maintenance:**
**展開とメンテナンス:**
- Intended Deployment Environment: [Batch, API/Online, Streaming, Edge]
- 意図された展開環境: [バッチ、API/オンライン、ストリーミング、エッジ]
- Model Dependencies: [List libraries or frameworks required]
- モデルの依存関係: [必要なライブラリやフレームワークのリスト]
- Monitoring Strategy: [Describe plans for post-deployment monitoring]
- モニタリング戦略: [展開後のモニタリング計画を説明]
- Retraining Schedule: [Planned model updates and frequency]
- 再トレーニングスケジュール: [計画されたモデルの更新と頻度]

**Explainability and Interpretability:**
**説明可能性と解釈可能性:**
- Feature Importance: [Key features influencing the model’s decisions]
- 特徴の重要性: [モデルの決定に影響を与える主要な特徴]
- Interpretability Techniques Used: [SHAP, LIME, etc.]
- 使用された解釈技術: [SHAP、LIMEなど]

**Responsible AI Considerations:**
**責任あるAIの考慮事項:**
- Compliance: [Regulatory frameworks followed, such as GDPR, EU AI Act]
- コンプライアンス: [GDPR、EU AI法など、遵守される規制フレームワーク]
- Feedback Mechanism: [How users can report issues or provide feedback]
- フィードバックメカニズム: [ユーザーが問題を報告したりフィードバックを提供する方法]
- Cost of Model Training and Deployment: [Electricity consumption]
- モデルのトレーニングと展開のコスト: [電力消費]

**References:**
**参考文献:**
- Code/Papers/Documentation: [Source code, referenced publications, doc links]
- コード/論文/文書: [ソースコード、参照された出版物、文書リンク]
- Contact Information: [Who to contact for questions]  
- 連絡先情報: [質問がある場合の連絡先]  

-----
###### Summary and Exercises
###### 要約と演習
In this chapter, we took a whirlwind tour of the key challenges in developing and operating training pipelines. 
この章では、トレーニングパイプラインの開発と運用における主要な課題を駆け足で紹介しました。

Training pipelines are mostly the realm of data science— identifying the labels and features for your model, hyperparameter tuning, fitting the data to your model, and evaluating the performance and compliance of your model.
トレーニングパイプラインは主にデータサイエンスの領域であり、モデルのラベルと特徴を特定し、ハイパーパラメータの調整を行い、データをモデルに適合させ、モデルのパフォーマンスとコンプライアンスを評価します。

But they also require data engineering skills, such as preparing labels and joining them to features. 
しかし、ラベルを準備し、それを特徴に結合するなどのデータエンジニアリングスキルも必要です。

And they can require the ML engineering skills of managing GPUs, scaling out training, and removing scalability bottlenecks in your training pipeline.
また、GPUの管理、トレーニングのスケーリング、トレーニングパイプラインのスケーラビリティボトルネックを取り除くためのMLエンジニアリングスキルも必要です。

Do the following exercises to help you learn how to do data-centric model training:
データ中心のモデルトレーニングを学ぶために、以下の演習を行ってください。

- You want to build a batch ML system that predicts churn for customers. 
- 顧客の離脱を予測するバッチMLシステムを構築したいと考えています。

Your data mart has a fact table about customer interactions with support and marketing operations. 
あなたのデータマートには、サポートおよびマーケティング業務との顧客インタラクションに関するファクトテーブルがあります。

How could you use this fact table to provide labels/features for a customer churn model?
このファクトテーブルをどのように使用して、顧客離脱モデルのラベル/特徴を提供できますか？

- Select features for a target using mutual information. 
- 相互情報量を使用してターゲットの特徴を選択します。

First, find a public labeled tabular dataset. 
まず、公開されたラベル付きの表形式データセットを見つけます。

Then compute the mutual information between each feature and the target. 
次に、各特徴とターゲットとの相互情報量を計算します。

Finally, select the top N features and explain why you chose them.  
最後に、上位Nの特徴を選択し、なぜそれを選んだのかを説明します。

-----
-----
###### PART V #### Inference and Agents  
###### 第V部 #### 推論とエージェント  
-----
-----  



