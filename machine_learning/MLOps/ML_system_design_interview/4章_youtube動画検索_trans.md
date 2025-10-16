refs: https://bytebytego.com/courses/machine-learning-system-design-interview/youtube-video-search


Unlock Full Access with 50% off
50%オフでフルアクセスを解除

Login
ログイン



## Machine Learning System Design Interview 機械学習システム設計インタビュー
- 01Introduction and Overview 01はじめにと概要
- 02Visual Search System 02視覚検索システム
- 03Google Street View Blurring System 03Googleストリートビューぼかしシステム
- 04YouTube Video Search 04YouTube動画検索
- 05Harmful Content Detection 05有害コンテンツ検出
- 06Video Recommendation System 06動画推薦システム
- 07Event Recommendation System 07イベント推薦システム
- 08Ad Click Prediction on Social Platforms 08ソーシャルプラットフォームにおける広告クリック予測
- 09Similar Listings on Vacation Rental Platforms 09バケーションレンタルプラットフォームにおける類似リスティング
- 10Personalized News Feed 10パーソナライズされたニュースフィード
- 11People You May Know 11あなたが知っているかもしれない人々
01Introduction and Overview 01はじめにと概要
01Introduction and Overview 01はじめにと概要
02Visual Search System 02視覚検索システム
02Visual Search System 02視覚検索システム
03Google Street View Blurring System 03Googleストリートビューぼかしシステム
03Google Street View Blurring System 03Googleストリートビューぼかしシステム
04YouTube Video Search 04YouTube動画検索
04YouTube Video Search 04YouTube動画検索
05Harmful Content Detection 05有害コンテンツ検出
05Harmful Content Detection 05有害コンテンツ検出
06Video Recommendation System 06動画推薦システム
06Video Recommendation System 06動画推薦システム
07Event Recommendation System 07イベント推薦システム
07Event Recommendation System 07イベント推薦システム
08Ad Click Prediction on Social Platforms 08ソーシャルプラットフォームにおける広告クリック予測
08Ad Click Prediction on Social Platforms 08ソーシャルプラットフォームにおける広告クリック予測
09Similar Listings on Vacation Rental Platforms 09バケーションレンタルプラットフォームにおける類似リスティング
09Similar Listings on Vacation Rental Platforms 09バケーションレンタルプラットフォームにおける類似リスティング
10Personalized News Feed 10パーソナライズされたニュースフィード
10Personalized News Feed 10パーソナライズされたニュースフィード
11People You May Know 11あなたが知っているかもしれない人々
11People You May Know 11あなたが知っているかもしれない人々
Unlock Full Access with 50% off 50%オフでフルアクセスを解除
Login ログイン



# YouTube Video Search YouTube動画検索

On video-sharing platforms such as YouTube, the number of videos can quickly grow into the billions. 
YouTubeのような動画共有プラットフォームでは、動画の数は急速に数十億に達する可能性があります。

In this chapter, we design a video search system that can efficiently handle this volume of content. 
この章では、この膨大なコンテンツ量を効率的に処理できる動画検索システムを設計します。

As shown in Figure 4.1, the user enters text into the search box, and the system displays the most relevant videos for the given text. 
図4.1に示すように、ユーザは検索ボックスにテキストを入力し、システムは指定されたテキストに最も関連性の高い動画を表示します。



### Clarifying Requirements 要件の明確化

Here is a typical interaction between a candidate and an interviewer.
ここでは、候補者と面接官の典型的なやり取りを示します。

Candidate:Is the input query text-only, or can users search with an image or video?
候補者:入力クエリはテキストのみですか、それともユーザーは画像や動画で検索できますか？

Interviewer:Text queries only.
面接官:テキストクエリのみです。

Candidate:Is the content on the platform only in video form? How about images or audio files?
候補者:プラットフォーム上のコンテンツは動画形式のみですか？画像や音声ファイルはどうですか？

Interviewer:The platform only serves videos.
面接官:プラットフォームは動画のみを提供しています。

Candidate:The YouTube search system is very complex. Can I assume the relevancy of a video is determined solely by its visual content and the textual data associated with the video, such as the title and description?
候補者:YouTubeの検索システムは非常に複雑です。動画の関連性は、その視覚的コンテンツと、タイトルや説明などの動画に関連するテキストデータのみによって決まると仮定してもよいですか？

Interviewer:Yes, that's a fair assumption.
面接官:はい、それは妥当な仮定です。

Candidate:Is there any training data available?
候補者:トレーニングデータは利用可能ですか？

Interviewer:Yes, let's assume we have ten million pairs of⟨\langle⟨video, text query⟩\rangle⟩.
面接官:はい、1000万対の⟨\langle⟨動画、テキストクエリ⟩\rangle⟩があると仮定しましょう。

Candidate:Do we need to support other languages in the search system?
候補者:検索システムで他の言語をサポートする必要がありますか？

Interviewer:For simplicity, let's assume only English is supported.
面接官:簡単のために、英語のみがサポートされていると仮定しましょう。

Candidate:How many videos are available on the platform?
候補者:プラットフォーム上には何本の動画がありますか？

Interviewer:One billion videos.
面接官:10億本の動画があります。

Candidate:Do we need to personalize the results? Should we rank the results differently for different users, based on their past interactions?
候補者:結果をパーソナライズする必要がありますか？過去のインタラクションに基づいて、異なるユーザーに対して結果を異なる順位付けをするべきですか？

Interviewer:As opposed to recommendation systems where personalization is essential, we do not necessarily have to personalize results in search systems. 
面接官:パーソナライズが重要な推薦システムとは異なり、検索システムでは必ずしも結果をパーソナライズする必要はありません。

To simplify the problem, let's assume no personalization is required.
問題を簡素化するために、パーソナライズは必要ないと仮定しましょう。

Let's summarize the problem statement. 
問題の定義を要約しましょう。

We are asked to design a search system for videos. 
私たちは、動画の検索システムを設計するよう求められています。

The input is a text query, and the output is a list of videos that are relevant to the text query. 
入力はテキストクエリで、出力はそのテキストクエリに関連する動画のリストです。

To search for relevant videos, we leverage both the videos' visual content and textual data. 
関連する動画を検索するために、動画の視覚的コンテンツとテキストデータの両方を活用します。

We are given a dataset of ten million⟨\langle⟨video, text query⟩\rangle⟩pairs for model training.
モデルのトレーニングのために、1000万対の⟨\langle⟨動画、テキストクエリ⟩\rangle⟩のデータセットが与えられています。



### Frame the Problem as an ML Task 機械学習タスクとして問題を定義する  
#### Defining the ML objective 機械学習の目的を定義する
Users expect search systems to provide relevant and useful results. 
ユーザは検索システムが関連性のある有用な結果を提供することを期待しています。 
One way to translate this into an ML objective is to rank videos based on their relevance to the text query.
これを機械学習の目的に変換する一つの方法は、テキストクエリに対する関連性に基づいて動画をランク付けすることです。



#### Specifying the system's input and output システムの入力と出力の指定

As shown in Figure 4.2, the search system takes a text query as input and outputs a ranked list of videos sorted by their relevance to the text query.
図4.2に示すように、検索システムはテキストクエリを入力として受け取り、そのテキストクエリに対する関連性に基づいてソートされた動画のランキングリストを出力します。



#### Choosing the right ML category 適切なMLカテゴリの選択

In order to determine the relevance between a video and a text query, we utilize both visual content and the video’s textual data. 
ビデオとテキストクエリの関連性を判断するために、視覚コンテンツとビデオのテキストデータの両方を利用します。
An overview of the design can be seen in Figure 4.3. 
デザインの概要は図4.3に示されています。
Let's briefly discuss each component. 
各コンポーネントについて簡単に説明しましょう。



##### Visual search ビジュアル検索

This component takes a text query as input and outputs a list of videos. 
このコンポーネントは、テキストクエリを入力として受け取り、動画のリストを出力します。

The videos are ranked based on the similarity between the text query and the videos' visual content. 
動画は、テキストクエリと動画の視覚コンテンツとの類似性に基づいてランク付けされます。

Representation learning is a commonly used approach to search for videos by processing their visual content. 
表現学習は、動画の視覚コンテンツを処理することによって動画を検索するために一般的に使用されるアプローチです。

In this approach, text query and video are encoded separately using two encoders. 
このアプローチでは、テキストクエリと動画は2つのエンコーダを使用して別々にエンコードされます。

As shown in Figure 4.4, the ML model contains a video encoder that generates an embedding vector from the video, and a text encoder that generates an embedding vector from the text. 
図4.4に示すように、MLモデルは動画から埋め込みベクトルを生成する動画エンコーダと、テキストから埋め込みベクトルを生成するテキストエンコーダを含んでいます。

The similarity score between the video and the text is calculated using the dot product of their representations. 
動画とテキストの類似度スコアは、それらの表現のドット積を使用して計算されます。

In order to rank videos that are visually and semantically similar to the text query, we compute the dot product between the text and each video in the embedding space, then rank the videos based on their similarity scores. 
テキストクエリに視覚的および意味的に類似した動画をランク付けするために、埋め込み空間内でテキストと各動画とのドット積を計算し、その後、類似度スコアに基づいて動画をランク付けします。



##### Text search テキスト検索

Figure 4.5 shows how text search works when a user types in a text query: "dogs playing indoor". 
図4.5は、ユーザがテキストクエリ「室内で遊ぶ犬」と入力したときのテキスト検索の動作を示しています。 
Videos with the most similar titles, descriptions, or tags to the text query are shown as the output. 
テキストクエリに最も類似したタイトル、説明、またはタグを持つ動画が出力として表示されます。

The inverted index is a common technique for creating the text-based search component, allowing efficient full-text search in databases. 
逆インデックスは、テキストベースの検索コンポーネントを作成するための一般的な手法であり、データベース内で効率的な全文検索を可能にします。 
Since inverted indexes aren't based on machine learning, there is no training cost. 
逆インデックスは機械学習に基づいていないため、トレーニングコストは発生しません。 
A popular search engine companies often use is Elasticsearch, which is a scalable search engine and document store. 
多くの企業が使用する人気の検索エンジンはElasticsearchであり、これはスケーラブルな検索エンジンおよびドキュメントストアです。 
For more details and a deeper understanding of Elasticsearch, refer to [1]. 
Elasticsearchの詳細やより深い理解については、[1]を参照してください。



### Data Preparation データ準備  
#### Data engineering データエンジニアリング
Since we are given an annotated dataset to train and evaluate the model, it's not necessary to perform any data engineering. 
モデルを訓練し評価するために注釈付きデータセットが与えられているため、データエンジニアリングを行う必要はありません。
Table 4.1 shows what the annotated dataset might look like. 
表4.1は、注釈付きデータセットがどのようなものかを示しています。
Table 4.1: Annotated dataset 
表4.1: 注釈付きデータセット



#### Feature engineering 特徴量エンジニアリング

Almost all ML algorithms accept only numeric input values. 
ほとんどすべての機械学習アルゴリズムは、数値入力値のみを受け入れます。
Unstructured data such as texts and videos need to be converted into a numerical representation during this step. 
テキストや動画などの非構造化データは、このステップで数値表現に変換する必要があります。
Let's take a look at how to prepare the text and video data for the model. 
モデルのためにテキストと動画データをどのように準備するか見てみましょう。



##### Preparing text data テキストデータの準備

As shown in Figure4.64.64.6, text is typically represented as a numerical vector using three steps: text normalization, tokenization, and tokens to IDs [2].  
図4.64.64.6に示すように、テキストは通常、テキストの正規化、トークン化、トークンをIDに変換するという3つのステップを使用して数値ベクトルとして表現されます[2]。

Let's take a look at each step in more detail.  
各ステップをもう少し詳しく見てみましょう。

Text normalization - also known as text cleanup - ensures words and sentences are consistent.  
テキストの正規化（テキストのクリーンアップとも呼ばれる）は、単語や文が一貫性を持つことを保証します。

For example, the same word may be spelled slightly differently; as in "dog", "dogs", and "DOG!" all refer to the same thing but are spelled in different ways.  
例えば、同じ単語がわずかに異なるスペルで表記されることがあります。「dog」、「dogs」、「DOG！」はすべて同じものを指しますが、異なる方法で綴られています。

The same is true for sentences.  
文についても同様です。

Take these two sentences, for example:  
例えば、次の2つの文を見てみましょう：

- "A person walking with his dog in Montréal !"  
- "a person walks with his dog, in Montreal."  

Both sentences mean the same, but have differing punctuation and verb forms.  
両方の文は同じ意味ですが、句読点や動詞の形が異なります。

Here are some typical methods for text normalization:  
テキストの正規化のための一般的な方法は以下の通りです：

- Lowercasing: make all letters lowercase, as this does not change the meaning of words or sentences  
- 小文字化：すべての文字を小文字にします。これは単語や文の意味を変えません。

- Punctuation removal: remove punctuation from the text. Common punctuation marks are the period, comma, question mark, exclamation point, etc.  
- 句読点の削除：テキストから句読点を削除します。一般的な句読点には、ピリオド、カンマ、疑問符、感嘆符などがあります。

- Trim whitespaces: trim leading, trailing, and multiple whitespaces  
- 空白のトリミング：先頭、末尾、および複数の空白をトリミングします。

- Normalization Form KD (NFKD) [3]: decompose combined graphemes into a combination of simple ones  
- 正規化形式KD（NFKD）[3]：結合されたグラフェムを単純なものの組み合わせに分解します。

- Strip accents: remove accent marks from words. For example: Màlaga→\rightarrow→Malaga, Noël→\rightarrow→Noel  
- アクセントの除去：単語からアクセント記号を削除します。例えば：Màlaga→\rightarrow→Malaga、Noël→\rightarrow→Noel

- Lemmatization and stemming: identify a canonical representative for a set of related word forms. For example: walking, walks, walked→\rightarrow→walk  
- レンマ化とステミング：関連する単語形のセットに対して標準的な代表を特定します。例えば：walking、walks、walked→\rightarrow→walk

Tokenization is the process of breaking down a piece of text into smaller units called tokens.  
トークン化は、テキストの一部をトークンと呼ばれる小さな単位に分解するプロセスです。

Generally, there are three types of tokenization:  
一般的に、トークン化には3つのタイプがあります：

- Word tokenization: split the text into individual words based on specific delimiters. For example, a phrase like "I have an interview tomorrow" becomes [ "I", "have", "an", "interview", "tomorrow"]  
- 単語トークン化：特定の区切り文字に基づいてテキストを個々の単語に分割します。例えば、「I have an interview tomorrow」というフレーズは、[ "I", "have", "an", "interview", "tomorrow"]になります。

- Subword tokenization: split text into subwords (or n-gram characters)  
- サブワードトークン化：テキストをサブワード（またはn-グラム文字）に分割します。

- Character tokenization: split text into a set of characters  
- 文字トークン化：テキストを文字のセットに分割します。

The details of different tokenization algorithms are not usually a strong focus in ML system design interviews.  
異なるトークン化アルゴリズムの詳細は、MLシステム設計のインタビューでは通常強い焦点にはなりません。

If you are interested to learn more, refer to [4].  
もっと学びたい場合は、[4]を参照してください。

Once we have the tokens, we need to convert them to numerical values (IDs).  
トークンが得られたら、それらを数値（ID）に変換する必要があります。

The representation of tokens with numerical values can be done in two ways:  
トークンを数値で表現する方法は2つあります：

- Lookup table  
- ルックアップテーブル

- Hashing  
- ハッシング

Lookup table. In this method, each unique token is mapped to an ID.  
ルックアップテーブル。この方法では、各ユニークなトークンがIDにマッピングされます。

Next, a lookup table is created to store these mappings.  
次に、これらのマッピングを保存するためのルックアップテーブルが作成されます。

Figure4.74.74.7 shows what the mapping table might look like.  
図4.74.74.7は、マッピングテーブルがどのように見えるかを示しています。

Hashing. Hashing, also called "feature hashing" or "hashing trick," is a memory-efficient method that uses a hash function to obtain IDs, without keeping a lookup table.  
ハッシング。ハッシング（「フィーチャーハッシング」または「ハッシングトリック」とも呼ばれる）は、ルックアップテーブルを保持せずに、ハッシュ関数を使用してIDを取得するメモリ効率の良い方法です。

Figure4.84.84.8 shows how a hash function is used to convert words to IDs.  
図4.84.84.8は、ハッシュ関数が単語をIDに変換する方法を示しています。

Let's compare the lookup table with the hashing method.  
ルックアップテーブルとハッシング方法を比較してみましょう。

✘ The table is stored in memory. A large number of tokens will result in an increase in memory required  
✘ テーブルはメモリに保存されます。大量のトークンは必要なメモリの増加をもたらします。

✓ The hash function is sufficient to convert any token to its ID  
✓ ハッシュ関数は、任意のトークンをそのIDに変換するのに十分です。

✓ Easily handles new or unseen words by applying the hash function to any word  
✓ ハッシュ関数を任意の単語に適用することで、新しいまたは未見の単語を簡単に処理します。

Table 4.2: Lookup table vs. feature hashing  
表4.2：ルックアップテーブルとフィーチャーハッシング



##### Preparing video data 動画データの準備

Figure 4.9 shows a typical workflow for preprocessing a raw video.
図4.9は、生の動画を前処理するための典型的なワークフローを示しています。



### Model Development モデル開発  
#### Model selection モデル選択
As discussed in the "Framing the problem as an ML task" section, text queries are converted into embeddings by a text encoder, and videos are converted into embeddings by a video encoder.  
「問題をMLタスクとしてフレーミングする」セクションで述べたように、テキストクエリはテキストエンコーダによって埋め込みに変換され、ビデオはビデオエンコーダによって埋め込みに変換されます。  
In this section, we examine possible model architectures for each encoder.  
このセクションでは、各エンコーダのための可能なモデルアーキテクチャを検討します。  



A typical text encoder’s input and output are shown in Figure 4.10.
典型的なテキストエンコーダの入力と出力は、図4.10に示されています。

The text encoder converts text into a vector representation [6]. 
テキストエンコーダは、テキストをベクトル表現に変換します[6]。

For example, if two sentences have similar meanings, their embeddings are more similar. 
例えば、2つの文が似た意味を持つ場合、それらの埋め込みはより似ています。

To build the text encoder, two broad categories are available: statistical methods and ML-based methods. 
テキストエンコーダを構築するためには、統計的手法と機械学習（ML）ベースの手法の2つの大きなカテゴリがあります。

Let's examine each. 
それぞれを見てみましょう。

Those methods rely on statistics to convert a sentence into a feature vector. 
これらの手法は、統計に基づいて文を特徴ベクトルに変換します。

Two popular statistical methods are:
2つの一般的な統計手法は次のとおりです。

- Bag of Words (BoW)
- Term Frequency Inverse Document Frequency (TF-IDF)

BoW. This method converts a sentence into a fixed-length vector. 
BoW。この手法は、文を固定長のベクトルに変換します。

It models sentence-word occurrences by creating a matrix with rows representing sentences, and columns representing word indices. 
文の単語の出現をモデル化するために、行が文を表し、列が単語のインデックスを表す行列を作成します。

An example of BoW is shown in Figure 4.11. 
BoWの例は図4.11に示されています。

Figure 4.11: BoW representations of different sentences
図4.11: 異なる文のBoW表現

BoW is a simple method that computes sentence representations fast, but has the following limitations: 
BoWは文の表現を迅速に計算するシンプルな手法ですが、以下の制限があります。

- It does not consider the order of words in a sentence. 
- 文中の単語の順序を考慮しません。

For example, "let's watch TV after work" and "let's work after watch TV" would have the same BoW representation. 
例えば、「仕事の後にテレビを見よう」と「テレビを見た後に仕事をしよう」は同じBoW表現になります。

- The obtained representation does not capture the semantic and contextual meaning of the sentence. 
- 得られた表現は文の意味的および文脈的な意味を捉えません。

For example, two sentences with the same meaning but different words have a totally different representation. 
例えば、同じ意味を持つが異なる単語の2つの文は、まったく異なる表現を持ちます。

- The representation vector is sparse. 
- 表現ベクトルはスパースです。

The size of the representation vector is equal to the total number of unique tokens we have. 
表現ベクトルのサイズは、私たちが持っているユニークなトークンの総数に等しいです。

This number is usually very large, so each sentence representation is mostly filled with zeros. 
この数は通常非常に大きいため、各文の表現は主にゼロで埋められています。

TF-IDF. This is a numerical statistic intended to reflect how important a word is to a document in a collection or corpus. 
TF-IDF。これは、コレクションまたはコーパス内の文書に対して単語がどれほど重要であるかを反映することを目的とした数値統計です。

TF-IDF creates the same sentence-word matrix as in BoW, but it normalizes the matrix based on the frequency of words. 
TF-IDFはBoWと同じ文-単語行列を作成しますが、単語の頻度に基づいて行列を正規化します。

To learn more about the mathematics behind this, refer to [7]. 
この背後にある数学について詳しく知りたい場合は、[7]を参照してください。

Since TF-IDF gives less weight to frequent words, its representations are usually better than BoW. 
TF-IDFは頻繁に出現する単語に対して重みを少なくするため、その表現は通常BoWよりも優れています。

However, it has the following limitations: 
しかし、以下の制限があります。

- A normalization step is needed to recompute term frequencies when a new sentence is added. 
- 新しい文が追加されるときに、用語頻度を再計算するための正規化ステップが必要です。

- It does not consider the order of words in a sentence. 
- 文中の単語の順序を考慮しません。

- The obtained representation does not capture the semantic meaning of the sentence. 
- 得られた表現は文の意味を捉えません。

- The representations are sparse. 
- 表現はスパースです。

In summary, statistical methods are usually fast. 
要約すると、統計的手法は通常迅速です。

However, they do not capture the contextual meaning of sentences, and the representations are sparse. 
しかし、文の文脈的な意味を捉えず、表現はスパースです。

ML-based methods address those issues. 
MLベースの手法はこれらの問題に対処します。

In these methods, an ML model converts sentences into meaningful word embeddings so that the distance between two embeddings reflects the semantic similarity of the corresponding words. 
これらの手法では、MLモデルが文を意味のある単語の埋め込みに変換し、2つの埋め込み間の距離が対応する単語の意味的類似性を反映します。

For example, if two words, such as "rich" and "wealth" are semantically similar, their embeddings are close in the embedding space. 
例えば、「rich」と「wealth」のように、2つの単語が意味的に類似している場合、それらの埋め込みは埋め込み空間で近くにあります。

Figure 4.12 shows a simple visualization of word embeddings in the 2D embedding space. 
図4.12は、2D埋め込み空間における単語の埋め込みの簡単な視覚化を示しています。

As you can see, similar words are grouped together. 
ご覧のように、類似した単語は一緒にグループ化されています。

There are three common ML-based approaches for transforming texts into embeddings: 
テキストを埋め込みに変換するための一般的なMLベースのアプローチは3つあります。

- Embedding (lookup) layer
- Word2vec
- Transformer-based architectures

Embedding (lookup) layer. In this approach, an embedding layer is employed to map each ID to an embedding vector. 
Embedding (lookup) layer。このアプローチでは、埋め込み層を使用して各IDを埋め込みベクトルにマッピングします。

Figure 4.13 shows an example. 
図4.13はその例を示しています。

Employing an embedding layer is a simple and effective solution to convert sparse features, such as IDs, into a fixed-size embedding. 
埋め込み層を使用することは、IDのようなスパースな特徴を固定サイズの埋め込みに変換するためのシンプルで効果的な解決策です。

We will see more examples of its usage in later chapters. 
後の章でその使用例をさらに見ていきます。

Word2vec. Word2vec [8] is a family of related models used to produce word embeddings. 
Word2vec。Word2vec [8]は、単語の埋め込みを生成するために使用される関連モデルのファミリーです。

These models use a shallow neural network architecture and utilize the co-occurrences of words in a local context to learn word embeddings. 
これらのモデルは、浅いニューラルネットワークアーキテクチャを使用し、局所的な文脈における単語の共起を利用して単語の埋め込みを学習します。

In particular, the model learns to predict a center word from its surrounding words during the training phase. 
特に、モデルはトレーニングフェーズ中に周囲の単語から中心の単語を予測することを学習します。

After the training phase, the model is capable of converting words into meaningful embeddings. 
トレーニングフェーズの後、モデルは単語を意味のある埋め込みに変換することができます。

There are two main models based on word2vec: Continuous Bag of Words (CBOW) [9] and Skip-gram [10]. 
Word2vecに基づく主なモデルは2つあります: Continuous Bag of Words (CBOW) [9] と Skip-gram [10]。

Figure 4.14 shows how CBOW works at a high level. 
図4.14は、CBOWが高レベルでどのように機能するかを示しています。

If you are interested to learn about these models, refer to [8]. 
これらのモデルについて学びたい場合は、[8]を参照してください。

Even though word2vec and embedding layers are simple and effective, recent architectures based upon Transformers have shown promising results. 
Word2vecと埋め込み層はシンプルで効果的ですが、最近のTransformerに基づくアーキテクチャは有望な結果を示しています。

Transformer-based models. These models consider the context of the words in a sentence when converting them into embeddings. 
Transformerベースのモデル。これらのモデルは、文を埋め込みに変換する際に文中の単語の文脈を考慮します。

As opposed to word2vec models, they produce different embeddings for the same word depending on the context. 
Word2vecモデルとは異なり、文脈に応じて同じ単語に対して異なる埋め込みを生成します。

Figure 4.15 shows a Transformer-based model which takes a sentence - a set of words as input, and produces an embedding for each word. 
図4.15は、文（単語のセット）を入力として受け取り、各単語の埋め込みを生成するTransformerベースのモデルを示しています。

Transformers are very powerful at understanding the context and producing meaningful embeddings. 
Transformerは文脈を理解し、意味のある埋め込みを生成するのに非常に強力です。

Several models, such as BERT [11], GPT3 [12], and BLOOM [13], have demonstrated Transformers' potential to perform a wide variety of Natural Language Processing (NLP) tasks. 
BERT [11]、GPT3 [12]、BLOOM [13]などのいくつかのモデルは、Transformerがさまざまな自然言語処理（NLP）タスクを実行する可能性を示しています。

In our case, we choose a Transformer-based architecture such as BERT as our text encoder. 
私たちの場合、BERTのようなTransformerベースのアーキテクチャをテキストエンコーダとして選択します。

In some interviews, the interviewer may want you to dive deeper into the details of the Transformer-based model. 
いくつかのインタビューでは、面接官がTransformerベースのモデルの詳細に深く掘り下げることを求めるかもしれません。

To learn more, refer to [14]. 
詳細を知りたい場合は、[14]を参照してください。



##### Video encoder ビデオエンコーダ

We have two architectural options for encoding videos:  
ビデオをエンコードするための2つのアーキテクチャオプションがあります：

- Video-level models  
- ビデオレベルモデル

- Frame-level models  
- フレームレベルモデル

Video-level models process a whole video to create an embedding, as shown in Figure 4.16.  
ビデオレベルモデルは、図4.16に示すように、全体のビデオを処理して埋め込みを作成します。  
The model architecture is usually based on 3D convolutions [15] or Transformers.  
モデルアーキテクチャは通常、3D畳み込み[15]またはTransformersに基づいています。  
Since the model processes the whole video, it is computationally expensive.  
モデルが全体のビデオを処理するため、計算コストが高くなります。

Frame-level models work differently.  
フレームレベルモデルは異なる方法で動作します。  
It is possible to extract the embedding from a video using a frame-level model by breaking it down into three steps:  
フレームレベルモデルを使用してビデオから埋め込みを抽出することは、次の3つのステップに分解することで可能です：

- Preprocess a video and sample frames.  
- ビデオを前処理し、フレームをサンプリングします。

- Run the model on the sampled frames to create frame embeddings.  
- サンプリングしたフレームにモデルを実行してフレーム埋め込みを作成します。

- Aggregate (e.g., average) frame embeddings to generate the video embedding.  
- フレーム埋め込みを集約（例：平均）してビデオ埋め込みを生成します。

Since this model works at the frame level, it is often faster and computationally less expensive.  
このモデルはフレームレベルで動作するため、通常はより速く、計算コストも低くなります。  
However, frame-level models are usually not able to understand the temporal aspects of the video, such as actions and motions.  
しかし、フレームレベルモデルは通常、アクションや動きなどのビデオの時間的側面を理解することができません。  
In practice, frame-level models are preferred in many cases where a temporal understanding of the video is not crucial.  
実際には、ビデオの時間的理解が重要でない多くのケースでフレームレベルモデルが好まれます。  
Here, we employ a frame-level model such as ViT [16] for two reasons:  
ここでは、次の2つの理由からViT [16]のようなフレームレベルモデルを採用します：

- Improve the training and serving speed  
- トレーニングとサービングの速度を向上させる

- Reduce the number of computations  
- 計算の数を減らす



#### Model training モデルのトレーニング

To train the text encoder and video encoder, we use a contrastive learning approach. 
テキストエンコーダとビデオエンコーダをトレーニングするために、コントラスト学習アプローチを使用します。
If you are interested in learning more about this, see the "Model training" section in Chapter 2, Visual Search System.
これについて詳しく知りたい場合は、第2章「ビジュアル検索システム」の「モデルのトレーニング」セクションを参照してください。
An explanation of how to compute the loss during model training is shown in Figure 4.18.
モデルのトレーニング中に損失を計算する方法の説明は、図4.18に示されています。



### Evaluation 評価  
#### Offline metrics オフライン指標  
Here are some offline metrics that are typically used in search systems. Let's examine which are the most relevant.  
ここでは、検索システムで一般的に使用されるいくつかのオフライン指標を示します。どれが最も関連性が高いかを検討しましょう。  

**Precision@k and mAP**  
**Precision@kとmAP**  
$$
\text{precision@k} = \frac{\text{number of relevant items among the top } k \text{ items in the ranked list}}{k}
$$  
$$
\text{precision@k} = \frac{\text{ranked listの上位} k \text{項目の中の関連項目の数}}{k}
$$  

In the evaluation dataset, a given text query is associated with only one video. That means the numerator of the precision@k formula is at most 1. This leads to low precision@k values.  
評価データセットでは、特定のテキストクエリは1つのビデオにのみ関連付けられています。つまり、precision@kの式の分子は最大でも1です。これにより、precision@kの値が低くなります。  
For example, for a given text query, even if we rank its associated video at the top of the list, the precision@10 is only 0.1.  
例えば、特定のテキストクエリに対して、その関連ビデオをリストの最上位にランク付けしても、precision@10はわずか0.1です。  
Due to this limitation, precision metrics, such as precision@k and mAP, are not very helpful.  
この制限のため、precision@kやmAPなどの精度指標はあまり役に立ちません。  

**Recall@k.** This measures the ratio between the number of relevant videos in the search results and the total number of relevant videos.  
**Recall@k.** これは、検索結果における関連ビデオの数と、関連ビデオの総数との比率を測定します。  
$$
\text{recall@k} = \frac{\text{Number of relevant videos among the top } k \text{ videos}}{\text{Total number of relevant videos}}
$$  
$$
\text{recall@k} = \frac{\text{上位} k \text{ビデオの中の関連ビデオの数}}{\text{関連ビデオの総数}}
$$  

As described earlier, the "total number of relevant videos" is always 1. With that, we can translate the recall@k formula to the following:  
前述のように、「関連ビデオの総数」は常に1です。それを考慮すると、recall@kの式は次のように表すことができます。  
$$
\text{recall@k} = 
\begin{cases} 
1 & \text{if the relevant video is among the top } k \text{ videos} \\ 
0 & \text{otherwise} 
\end{cases}
$$  
$$
\text{recall@k} = 
\begin{cases} 
1 & \text{関連ビデオが上位} k \text{ビデオの中にある場合} \\ 
0 & \text{それ以外の場合} 
\end{cases}
$$  

What are the pros and cons of this metric?  
この指標の利点と欠点は何ですか？  
**Pros**  
**利点**  
- It effectively measures a model's ability to find the associated video for a given text query.  
- 特定のテキストクエリに対して関連ビデオを見つけるモデルの能力を効果的に測定します。  

**Cons**  
**欠点**  
- It depends on $k$. Choosing the right $k$ could be challenging.  
- $k$に依存します。適切な$k$を選ぶことは難しい場合があります。  
- When the relevant video is not among the $k$ videos in the output list, recall@k is always 0.  
- 関連ビデオが出力リストの$k$ビデオの中にない場合、recall@kは常に0です。  
For example, consider the case where model A ranks a relevant video at place 15, and model B ranks the same video at place 50.  
例えば、モデルAが関連ビデオを15位にランク付けし、モデルBが同じビデオを50位にランク付けする場合を考えてみましょう。  
If we use recall@10 to measure the quality of these two models, both would have recall@10=0, even though model A is better than model B.  
これら2つのモデルの品質をrecall@10で測定すると、どちらもrecall@10=0になりますが、モデルAの方がモデルBよりも優れています。  

**Mean Reciprocal Rank (MRR).** This metric measures the quality of the model by averaging the rank of the first relevant item in each search result. The formula is:  
**平均逆順位（MRR）**。この指標は、各検索結果における最初の関連項目の順位を平均することによってモデルの品質を測定します。式は次の通りです。  
$$
\text{MRR} = \frac{1}{m} \sum_{i=1}^{m} \frac{1}{\text{rank}_i}
$$  
$$
\text{MRR} = \frac{1}{m} \sum_{i=1}^{m} \frac{1}{\text{rank}_i}
$$  

This metric addresses the shortcomings of recall@k and can be used as our offline metric.  
この指標はrecall@kの欠点を解決し、私たちのオフライン指標として使用できます。  



#### Online metrics オンライン指標

As part of online evaluation, companies track a wide variety of metrics. 
オンライン評価の一環として、企業はさまざまな指標を追跡します。 
Let's take a look at some of the most important ones: 
重要な指標のいくつかを見てみましょう：

- Click-through rate (CTR) 
- クリック率 (CTR)
- Video completion rate 
- 動画完了率
- Total watch time of search results 
- 検索結果の総視聴時間

CTR. This metric shows how often users click on retrieved videos. 
CTR。この指標は、ユーザーが取得した動画をどれだけクリックするかを示します。 
The main problem with CTR is that it does not track whether the clicked videos are relevant to the user. 
CTRの主な問題は、クリックされた動画がユーザーにとって関連性があるかどうかを追跡しないことです。 
In spite of this issue, CTR is still a good metric to track because it shows how many people clicked on search results. 
この問題にもかかわらず、CTRは検索結果をクリックした人数を示すため、追跡する価値のある良い指標です。

Video completion rate. A metric measuring how many videos appear in search results and are watched by users until the end. 
動画完了率。検索結果に表示され、ユーザーによって最後まで視聴される動画の数を測定する指標です。 
The problem with this metric is that a user may watch a video only partially, but still find it relevant. 
この指標の問題は、ユーザーが動画を部分的にしか視聴しない場合でも、それが関連性があると感じることです。 
The video completion rate alone cannot reflect the relevance of search results. 
動画完了率だけでは、検索結果の関連性を反映することはできません。

Total watch time of search results. This metric tracks the total time users spent watching the videos returned by the search results. 
検索結果の総視聴時間。この指標は、ユーザーが検索結果によって返された動画を視聴した合計時間を追跡します。 
Users tend to spend more time watching if the search results are relevant. 
ユーザーは、検索結果が関連性がある場合、より多くの時間を視聴する傾向があります。 
This metric is a good indication of how relevant the search results are. 
この指標は、検索結果の関連性を示す良い指標です。



### Serving サービング

At serving time, the system displays a ranked list of videos relevant to a given text query. 
サービング時に、システムは与えられたテキストクエリに関連する動画のランキングリストを表示します。

Figure4.194.194.19shows a simplified ML system design. 
図4.194.194.19は、簡略化されたMLシステムの設計を示しています。

Let's discuss each pipeline in more detail. 
それぞれのパイプラインについて、より詳細に説明しましょう。



#### Prediction pipeline 予測パイプライン

This pipeline consists of:
このパイプラインは以下で構成されています：
- Visual search
- Text search
- Fusing layer
- Re-ranking service

Visual search. This component encodes the text query and uses the nearest neighbor service to find the most similar video embeddings to the text embedding. 
視覚検索。このコンポーネントはテキストクエリをエンコードし、最近傍サービスを使用してテキスト埋め込みに最も類似したビデオ埋め込みを見つけます。

To accelerate the NN search, we use approximate nearest neighbor (ANN) algorithms, as described in Chapter 2, Visual Search System.
NN検索を加速するために、私たちはChapter 2, Visual Search Systemで説明されている近似最近傍（ANN）アルゴリズムを使用します。

Text search. Using Elasticsearch, this component finds videos with titles and tags that overlap the text query.
テキスト検索。Elasticsearchを使用して、このコンポーネントはテキストクエリと重複するタイトルやタグを持つビデオを見つけます。

Fusing layer. This component takes two different lists of relevant videos from the previous step, and combines them into a new list of videos.
融合層。このコンポーネントは前のステップからの2つの異なる関連ビデオのリストを取り、それらを新しいビデオのリストに結合します。

The fusing layer can be implemented in two ways, the easiest of which is to re-rank videos based on the weighted sum of their predicted relevance scores. 
融合層は2つの方法で実装でき、その中で最も簡単なのは、予測された関連スコアの加重和に基づいてビデオを再ランキングすることです。

A more complex approach is to adopt an additional model to re-rank the videos, which is more expensive because it requires model training. 
より複雑なアプローチは、ビデオを再ランキングするために追加のモデルを採用することであり、これはモデルのトレーニングを必要とするため、より高価です。

Additionally, it's slower at serving. As a result, we use the former approach.
さらに、提供速度が遅くなります。その結果、私たちは前者のアプローチを使用します。

Re-ranking service. This service modifies the ranked list of videos by incorporating business-level logic and policies.
再ランキングサービス。このサービスは、ビジネスレベルのロジックとポリシーを組み込むことによって、ビデオのランキングリストを修正します。



#### Video indexing pipeline ビデオインデックス作成パイプライン

A trained video encoder is used to compute video embeddings, which are then indexed. 
訓練されたビデオエンコーダーを使用してビデオ埋め込みを計算し、それをインデックス化します。
These indexed video embeddings are used by the nearest neighbor service.
これらのインデックス化されたビデオ埋め込みは、最近傍サービスによって使用されます。



#### Text indexing pipeline テキストインデックスパイプライン

This uses Elasticsearch for indexing titles, manual tags, and auto-generated tags. 
これは、タイトル、手動タグ、および自動生成されたタグのインデックス作成にElasticsearchを使用します。

Usually, when a user uploads a video, they provide tags to help better identify the video. 
通常、ユーザーがビデオをアップロードするとき、彼らはビデオをよりよく特定するためのタグを提供します。

But what if they do not manually enter tags? 
しかし、彼らが手動でタグを入力しない場合はどうでしょうか？

One option is to use a standalone model to generate tags. 
1つの選択肢は、スタンドアロンモデルを使用してタグを生成することです。

We name this component the auto-tagger and it is especially valuable in cases where a video has no manual tags. 
このコンポーネントをオートタグ付けツールと呼び、特にビデオに手動タグがない場合に価値があります。

These tags may be noisier than manual tags, but they are still valuable. 
これらのタグは手動タグよりもノイズが多いかもしれませんが、それでも価値があります。



### Other Talking Points その他の話題

Before concluding this chapter, it's important to note we have simplified the system design of the video search system. 
この章を締めくくる前に、私たちがビデオ検索システムのシステム設計を簡略化したことに注意することが重要です。 
In practice, it is much more complex. 
実際には、はるかに複雑です。 
Some improvements may include: 
いくつかの改善点には以下が含まれます：

- Use a multi-stage design (candidate generation + ranking). 
- マルチステージ設計（候補生成 + ランキング）を使用すること。
- Use more video features such as video length, video popularity, etc. 
- ビデオの長さ、ビデオの人気など、より多くのビデオ特徴を使用すること。
- Instead of relying on annotated data, use interactions (e.g., clicks, likes, etc.) to construct and label data. 
- 注釈付きデータに依存するのではなく、インタラクション（例：クリック、いいねなど）を使用してデータを構築し、ラベル付けすること。
- This allows us to continuously train the model. 
- これにより、モデルを継続的にトレーニングすることができます。
- Use an ML model to find titles and tags which are semantically similar to the text query. 
- テキストクエリに意味的に類似したタイトルやタグを見つけるためにMLモデルを使用すること。
- This model can be combined with Elasticsearch to improve search quality. 
- このモデルはElasticsearchと組み合わせて検索品質を向上させることができます。

If there's time left at the end of the interview, here are some additional talking points: 
インタビューの最後に時間が残っている場合、以下の追加の話題があります：

- An important topic in search systems is query understanding, such as spelling correction, query category identification, and entity recognition. 
- 検索システムにおける重要なトピックは、スペル修正、クエリカテゴリの特定、エンティティ認識などのクエリ理解です。
- How to build a query understanding component? [17]. 
- クエリ理解コンポーネントをどのように構築するか？[17]。
- How to build a multi-modal system that processes speech and audio to improve search results [18]. 
- 音声とオーディオを処理して検索結果を改善するマルチモーダルシステムをどのように構築するか？[18]。
- How to extend this work to support other languages [19]. 
- この作業を他の言語をサポートするように拡張するにはどうすればよいか？[19]。
- Near-duplicate videos in the final output may negatively impact user experience. 
- 最終出力における近似重複ビデオはユーザー体験に悪影響を及ぼす可能性があります。
- How to detect near-duplicate videos so we can remove them before displaying the results [20][20][20]? 
- 結果を表示する前に近似重複ビデオを検出して削除するにはどうすればよいか？[20][20][20]？
- Text queries can be divided into head, torso, and tail queries. 
- テキストクエリは、ヘッド、トルソー、テールクエリに分けることができます。
- What are the different approaches commonly used in each case [21]? 
- 各ケースで一般的に使用される異なるアプローチは何ですか？[21]？
- How to consider popularity and freshness when producing the output list [22]? 
- 出力リストを生成する際に人気と新鮮さをどのように考慮するか？[22]？
- How real-world search systems work [23][24][25]. 
- 実世界の検索システムはどのように機能するか？[23][24][25]。



### References 参考文献
1. Elasticsearch. https://www.tutorialspoint.com/elasticsearch/elasticsearch_query_dsl.htm.
2. Preprocessing text data. https://huggingface.co/docs/transformers/v4.42.0/preprocessing.
3. NFKD normalization. https://unicode.org/reports/tr15/.
4. What is Tokenization summary. https://huggingface.co/docs/transformers/tokenizer_summary.
5. Hash collision. https://en.wikipedia.org/wiki/Hash_collision.
6. Deep learning for NLP. http://cs224d.stanford.edu/lecture_notes/notes1.pdf.
7. TF-IDF. https://en.wikipedia.org/wiki/Tf%E2%80%93idf.
8. Word2Vec models. https://www.tensorflow.org/tutorials/text/word2vec.
9. Continuous bag of words. https://www.kdnuggets.com/2018/04/implementing-deep-learning-methods-feature-engineering-text-data-cbow.html.
10. Skip-gram model. http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/.
11. BERT model. https://arxiv.org/pdf/1810.04805.pdf.
12. GPT3 model. https://arxiv.org/pdf/2005.14165.pdf.
13. BLOOM model. https://bigscience.huggingface.co/blog/bloom.
14. Transformer implementation from scratch. https://peterbloem.nl/blog/transformers.
15. 3D convolutions. https://www.kaggle.com/code/shivamb/3d-convolutions-understanding-use-case/notebook.
16. Vision Transformer. https://arxiv.org/pdf/2010.11929.pdf.
17. Query understanding for search engines. https://www.linkedin.com/pulse/ai-query-understanding-daniel-tunkelang/.
18. Multimodal video representation learning. https://arxiv.org/pdf/2012.04124.pdf.
19. Multilingual language models. https://arxiv.org/pdf/2107.00676.pdf.
20. Near-duplicate video detection. https://arxiv.org/pdf/2005.07356.pdf.
21. Generalizable search relevance. https://livebook.manning.com/book/ai-powered-search/chapter-10/v-10/20.
22. Freshness in search and recommendation systems. https://developers.google.com/machine-learning/recommendation/dnn/re-ranking.
23. Semantic product search by Amazon. https://arxiv.org/pdf/1907.00937.pdf.
24. Ranking relevance in Yahoo search. https://www.kdd.org/kdd2016/papers/files/adf0361-yinA.pdf.
25. Semantic product search in E-Commerce. https://arxiv.org/pdf/2008.08180.pdf.



### Partner With Us 私たちと提携しましょう



### Company & Legal 会社と法務



### Support サポート



### Careers キャリア

Copyright ©2025 ByteByteGo Inc. All rights reserved.
著作権 ©2025 ByteByteGo Inc. 無断転載を禁じます。
