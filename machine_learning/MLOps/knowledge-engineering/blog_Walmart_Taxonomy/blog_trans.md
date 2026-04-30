refs: https://medium.com/walmartglobaltech/transforming-text-classification-with-semantic-search-techniques-faiss-c413f133d0e2


Sign up
サインアップ

Sign up
サインアップ

Sign in
サインイン

Sign in
サインイン

Get app
アプリを入手

Write
書く

Search
検索

Sign up
サインアップ

Sign up
サインアップ

Sign in
サインイン

Sign in
サインイン



## Walmart Global Tech Blog

## Walmart Global Tech Blog

·  
·  
Follow publication  
フォローする出版物  
We’re powering the next great retail disruption. Learn more about us—https://www.linkedin.com/company/walmartglobaltech/  
私たちは次の大きな小売の変革を推進しています。私たちについてもっと知るには、こちらをご覧ください—https://www.linkedin.com/company/walmartglobaltech/  
Follow publication  
フォローする出版物  

# Transforming Text Classification with Semantic Search Techniques — Faiss  
# セマンティック検索技術によるテキスト分類の変革 — Faiss  

Harika SamalaFollow  
Harika Samala  
Follow  
フォロー  

8 min read·Mar 13, 2024  
8分で読めます·2024年3月13日  

Classification models serve as supervised tools for organising documents into specific categories.  
分類モデルは、文書を特定のカテゴリに整理するための教師ありツールとして機能します。  
Semantic search emerges as a practical solution for managing new categories and scaling up seamlessly to huge data.  
セマンティック検索は、新しいカテゴリを管理し、大規模なデータにシームレスにスケールアップするための実用的なソリューションとして登場します。  
Its capability to integrate additional information without extensive retraining adds to its straightforward and reliable nature.  
広範な再トレーニングなしで追加情報を統合する能力は、そのシンプルで信頼性の高い性質を高めます。  
Utilizing a nearest neighbors approach, semantic search robustly tackles imbalances in data distribution, ensuring resilient classification across diverse datasets.  
最近傍法を利用することで、セマンティック検索はデータ分布の不均衡に強力に対処し、多様なデータセットにわたる堅牢な分類を保証します。  
This adaptability, paired with Faiss library’s advanced capabilities, underscores the transformative potential of semantic search in reshaping the classification landscape.  
この適応性は、Faissライブラリの高度な機能と相まって、分類の風景を再構築するセマンティック検索の変革的な可能性を強調します。  
Further, its flexibility strikes a balance between computational efficiency and the evolving nature of datasets.  
さらに、その柔軟性は、計算効率とデータセットの進化する性質とのバランスを取ります。  

Implementation of classification models involves two primary approaches: utilizing pre-trained models or training models from scratch/fine-tuning existing ones.  
分類モデルの実装には、主に2つのアプローチがあります：事前にトレーニングされたモデルを利用するか、ゼロからモデルをトレーニングする/既存のモデルをファインチューニングすることです。  
Pre-trained models have been trained on a large dataset for a general task which can be fine-tuned for a specific application / task or used directly by loading the model.  
事前にトレーニングされたモデルは、一般的なタスクのために大規模なデータセットでトレーニングされており、特定のアプリケーション/タスクにファインチューニングするか、モデルを直接ロードして使用できます。  
In contrast, training a model from scratch involves building and training an artificial intelligence model without relying on pre-existing weights or knowledge.  
対照的に、ゼロからモデルをトレーニングすることは、既存の重みや知識に依存せずに人工知能モデルを構築し、トレーニングすることを含みます。  
Each method comes with its own set of limitations.  
各方法にはそれぞれの制限があります。  
While pre-trained models offer convenience, they may not always be optimal as the training data might differ from our specific dataset.  
事前にトレーニングされたモデルは便利ですが、トレーニングデータが私たちの特定のデータセットと異なる可能性があるため、常に最適とは限りません。  
On the other hand, training models from scratch or fine-tuning requires a substantial amount of data and resources to generate meaningful results.  
一方、ゼロからモデルをトレーニングするかファインチューニングするには、意味のある結果を生成するためにかなりの量のデータとリソースが必要です。  
Additionally, both models need re-training if new categories emerge.  
さらに、新しいカテゴリが出現した場合、両方のモデルは再トレーニングが必要です。  

In this blog post, we will begin by highlighting the advantages of adopting a semantic search approach.  
このブログ記事では、セマンティック検索アプローチを採用する利点を強調することから始めます。  
We will then delve into an exploration of Faiss, elucidating its different index types.  
次に、Faissの探求に入り、その異なるインデックスタイプを明らかにします。  
To illustrate the practical application of this approach, we will walk through a use case involving a news dataset.  
このアプローチの実際の適用を示すために、ニュースデータセットを含むユースケースを通じて説明します。  

Utilizing a semantic approach to tackle classification problems offers several notable advantages:  
分類問題に取り組むためにセマンティックアプローチを利用することは、いくつかの顕著な利点を提供します：  

1. Efficient Handling of New Categories or Data:  
1. 新しいカテゴリやデータの効率的な処理：  
- Eliminates Full Retraining: There is no need to train or fine-tune a new model from scratch.  
- フル再トレーニングを排除：ゼロから新しいモデルをトレーニングまたはファインチューニングする必要はありません。  
Simply generate embeddings (convert text to vectors) for the new data and incorporate it into the existing index.  
新しいデータのために埋め込み（テキストをベクトルに変換）を生成し、それを既存のインデックスに組み込みます。  
This approach eliminates the need for extensive hardware resources that would otherwise be required for training a new model.  
このアプローチは、新しいモデルをトレーニングするために必要な広範なハードウェアリソースを排除します。  

2. Scalability:  
2. スケーラビリティ：  
- Flexible Data Addition: Scaling becomes hassle-free as new data (embeddings) can be seamlessly added to the existing index.  
- 柔軟なデータ追加：新しいデータ（埋め込み）を既存のインデックスにシームレスに追加できるため、スケーリングが簡単になります。  
This flexibility ensures smooth integration of additional information without the need for extensive model retraining.  
この柔軟性は、広範なモデル再トレーニングなしで追加情報のスムーズな統合を保証します。  
We utilise Faiss as it can scale from millions to billions of rows of data.  
私たちは、Faissを利用しています。これは、数百万から数十億のデータ行にスケールできます。  

3. Handling Data Imbalance:  
3. データの不均衡の処理：  
- Mitigating Imbalance: The approach leverages a nearest neighbours approach, mitigating concerns related to imbalances in the data.  
- 不均衡の軽減：このアプローチは最近傍法を活用し、データの不均衡に関連する懸念を軽減します。  
This ensures that classification is not significantly affected by variations in the distribution of data across various categories.  
これにより、分類はさまざまなカテゴリにわたるデータの分布の変動によって大きく影響を受けることはありません。  
Hence this approach doesn’t need a lot of pre-processing for imbalance in the dataset.  
したがって、このアプローチはデータセットの不均衡に対して多くの前処理を必要としません。  

For classification we utilised the news dataset and chose seven distinct categories like space, hardware, medicine, religion, hockey, crypto, graphics.  
分類のために、私たちはニュースデータセットを利用し、宇宙、ハードウェア、医学、宗教、ホッケー、暗号、グラフィックスの7つの異なるカテゴリを選びました。  
We have taken random samples from each class total of 4064 records.  
各クラスからランダムサンプルを取り、合計4064レコードを取得しました。  
All classes do not have the same number of samples necessitating the imbalance to be handled with this approach.  
すべてのクラスが同じ数のサンプルを持っているわけではなく、このアプローチで不均衡を処理する必要があります。  
Before we dive into our strategy, let's discuss briefly about Faiss library and its functionalities.  
私たちの戦略に入る前に、Faissライブラリとその機能について簡単に説明しましょう。  

Brief Introduction to Faiss:  
Faissの簡単な紹介：  
Faiss library allows comparison of vectors with high efficiency.  
Faissライブラリは、高効率でベクトルの比較を可能にします。  
Traditional vector comparison by using for loops are terribly slow especially on huge data.  
従来のベクトル比較は、forループを使用すると非常に遅く、特に大規模データでは顕著です。  
In this scenario Faiss comes handy as it can scale up from hundreds, thousands, millions to billions, especially efficient for sentence similarity.  
このシナリオでは、Faissが役立ちます。これは、数百、数千、数百万から数十億にスケールアップでき、特に文の類似性に対して効率的です。  
It works with the concept of index creation and search.  
インデックスの作成と検索の概念で機能します。  

The CPU version of Faiss excels by leveraging CPU core capabilities with BLAS (a library for efficient matrix computations), followed by SIMD (single instruction, multiple data) integrated with instruction-level parallelism.  
FaissのCPUバージョンは、BLAS（効率的な行列計算のためのライブラリ）を使用してCPUコアの能力を活用し、次に命令レベルの並列性と統合されたSIMD（単一命令、複数データ）によって優れています。  
Additionally, Faiss seamlessly supports GPU implementation through an efficient built-in algorithm.  
さらに、Faissは効率的な組み込みアルゴリズムを通じてGPU実装をシームレスにサポートします。  

Types of Indexes in Faiss:  
Faissのインデックスの種類：  
Different type of indexes which vary by Accuracy and Speed  
精度と速度によって異なるインデックスの種類  

1. Index Flat L2 (Faiss.IndexFlatl2) –  
1. インデックスフラットL2 (Faiss.IndexFlatl2) –  
Flat Index is a type of index that operates by maintaining flat vectors (embeddings).  
フラットインデックスは、フラットベクトル（埋め込み）を維持することによって機能するインデックスの一種です。  
It calculates the distance between vectors using the L2 (Euclidean) distance metric.  
L2（ユークリッド）距離メトリックを使用してベクトル間の距離を計算します。  
Pros: Don’t need any training we just utilise embeddings.  
利点：トレーニングは必要なく、埋め込みを利用するだけです。  
Training is needed only for clustering purpose.  
トレーニングはクラスタリング目的のためにのみ必要です。  
Cons: Since we need to compare all the vectors against one, it is comparatively slow but much better than for loop comparison.  
欠点：すべてのベクトルを1つに対して比較する必要があるため、比較的遅いですが、forループ比較よりははるかに優れています。  

2. Partitioning Index (faiss.IndexIVFFlat) –  
2. パーティショニングインデックス (faiss.IndexIVFFlat) –  
Partition Index uses Voronoi cells to partition vectors.  
パーティションインデックスは、ベクトルをパーティションするためにボロノイセルを使用します。  
It checks the distance between the query vector and each cell’s centroid, limiting the search to vectors within the nearest centroid cell.  
クエリベクトルと各セルの重心との距離をチェックし、最も近い重心セル内のベクトルに検索を制限します。  
The number of centroids for the final search can be chosen using the option index. Probe.  
最終検索のための重心の数は、オプションインデックスを使用して選択できます。Probe。  

From observation on different use cases, we noticed that with a larger number of centroids, the search is faster, but less accurate compared to an exhaustive (Flat L2) search.  
さまざまなユースケースの観察から、より多くの重心があると検索が速くなりますが、徹底的（フラットL2）検索と比較して精度が低くなることに気付きました。  
Pros: Redundant search against all vectors is removed since we have limited the scope to the nearest centroid.  
利点：最も近い重心に範囲を制限したため、すべてのベクトルに対する冗長な検索が排除されます。  
Cons: There might be closest point in another Voronoi cell this is the factor which we compensate for speed.  
欠点：別のボロノイセルに最も近い点が存在する可能性があり、これは速度を補う要因です。  

3. Product Quantization (faiss.IndexIVFPQ) –  
3. プロダクト量子化 (faiss.IndexIVFPQ) –  
In product quantization, the vector dimension is reduced to chunks and clustering is performed to obtain a centroid id which acts as a look up book for vectors.  
プロダクト量子化では、ベクトルの次元がチャンクに削減され、クラスタリングが行われて重心IDが取得され、これはベクトルのルックアップブックとして機能します。  
Finally, when query-vector comes it is divided into sub-vector and a lookup book is used to identify the distance of each sub-vector with all the cluster centroids.  
最後に、クエリベクトルが来ると、それはサブベクトルに分割され、ルックアップブックが使用されて各サブベクトルとすべてのクラスタ重心との距離を特定します。  

Pros: It is a great way to compress a dataset.  
利点：データセットを圧縮するための素晴らしい方法です。  
It is 18 to 20 times faster than other indexes.  
他のインデックスよりも18倍から20倍速いです。  
Cons: Results vary from both partitioning index and flat index.  
欠点：結果はパーティショニングインデックスとフラットインデックスの両方で異なります。  
If speed is the major concern, then PQ is considered.  
速度が主要な懸念である場合、PQが考慮されます。  

We notice that to obtain most accurate results its preferable to use Exhaustive Search (Index Flat L2).  
最も正確な結果を得るためには、徹底的検索（インデックスフラットL2）を使用することが望ましいことに気付きます。  
Faiss allows merging of different indexes using index factory, offering flexibility and enhanced memory efficiency in combining various approaches.  
Faissは、インデックスファクトリーを使用して異なるインデックスを統合することを可能にし、さまざまなアプローチを組み合わせる際の柔軟性とメモリ効率の向上を提供します。  



## index = faiss.index_factory(128, “IVF10000_HNSW32, PQ16”)
# combining HNSW with PQ (it is 15 times more memory efficient than HNSW alone as per experiments).
## index = faiss.index_factory(128, “IVF10000_HNSW32, PQ16”)
# HNSWとPQを組み合わせる（実験によると、HNSW単体と比べて15倍のメモリ効率が良い）。



## Get Harika Samala’s stories in your inbox Harika Samalaのストーリーを受信トレイに取得

Join Medium for free to get updates from this writer. 
この作家からの更新を受け取るために、Mediumに無料で参加してください。

Remember me for faster sign in 
迅速なサインインのために私を覚えておいてください。

Now that we have gained insights into these Faiss indexes, let us further explore their practical applications using real-world data and analyse the observations derived from their implementation. 
これらのFaissインデックスについての洞察を得たので、実世界のデータを使用してその実用的な応用をさらに探求し、実装から得られた観察結果を分析しましょう。



## Implementing the Semantic Search Approach for Classification: 分類のためのセマンティック検索アプローチの実装

1. Data Cleaning:  
   1. データクリーニング:  
   - Start by cleaning the data through essential pre-processing steps, including tokenization, punctuation removal, lowercase conversion, and elimination of stop words.  
   - トークン化、句読点の除去、小文字への変換、ストップワードの排除など、基本的な前処理ステップを通じてデータをクリーニングします。

2. Embedding Generation:  
   2. 埋め込み生成:  
   - Obtain embeddings for the text data using any approach, such as TF-IDF, Glove, or sentence transformer embeddings (we utilized MiniLM-l6-V2).  
   - TF-IDF、GloVe、または文の変換器埋め込み（私たちはMiniLM-l6-V2を使用しました）など、任意のアプローチを使用してテキストデータの埋め込みを取得します。

3. Integration with Faiss Library:  
   3. Faissライブラリとの統合:  
   - Transfer these embeddings to the Faiss library after selecting the appropriate index type (flat index, partitioning index, or product quantization).  
   - 適切なインデックスタイプ（フラットインデックス、パーティショニングインデックス、またはプロダクト量子化）を選択した後、これらの埋め込みをFaissライブラリに転送します。

4. Query Embedding Retrieval:  
   4. クエリ埋め込みの取得:  
   - Retrieve the embedding for a given input test query using the same model chosen in step 2.  
   - ステップ2で選択したのと同じモデルを使用して、指定された入力テストクエリの埋め込みを取得します。

5. Faiss Index Search:  
   5. Faissインデックス検索:  
   - Utilize Faiss index to search for similar sentences. This process returns the top N similar sentences for the input query along with their scores.  
   - Faissインデックスを利用して類似の文を検索します。このプロセスは、入力クエリに対して上位Nの類似文とそのスコアを返します。

6. Category Retrieval:  
   6. カテゴリの取得:  
   - Obtain the categories of the returned top N similar sentences using a mapping dictionary that correlates sentences to categories.  
   - 文とカテゴリを関連付けるマッピング辞書を使用して、返された上位Nの類似文のカテゴリを取得します。

7. Classification Decision:  
   7. 分類決定:  
   - Determine the final output class by either selecting the maximum category count from the top N or applying other statistical ranking methods for the given input.  
   - 上位Nから最大のカテゴリ数を選択するか、指定された入力に対して他の統計的ランキング手法を適用することによって、最終的な出力クラスを決定します。

Original Data:  
元データ:  
Press enter or click to view image in full size  
画像をフルサイズで表示するには、Enterキーを押すかクリックしてください。  
dataset  
データセット  
1. Basic cleaning steps has been followed as mentioned in the step1 after removing redundant data.  
1. 冗長なデータを削除した後、ステップ1で述べた基本的なクリーニング手順が実行されました。

```python
def clean(text):
    text = text.lower()
    url_removed = re.sub(r'https\S+', '', text, flags=re.MULTILINE)
    text = re.sub("[^a-zA-Z]", " ", url_removed)
    text = re.sub("\.+", " ", text)
    text = [word for word in text if word not in string.punctuation]
    text = "".join(text).strip()
    text = re.sub("\s\s+", " ", text)
    return "".join(text).strip()

selected["cleaned_data"] = selected["text"].apply(lambda x: clean(x) if x != None else x)
```
```python
def clean(text):
    text = text.lower()
    url_removed = re.sub(r'https\S+', '', text, flags=re.MULTILINE)
    text = re.sub("[^a-zA-Z]", " ", url_removed)
    text = re.sub("\.+", " ", text)
    text = [word for word in text if word not in string.punctuation]
    text = "".join(text).strip()
    text = re.sub("\s\s+", " ", text)
    return "".join(text).strip()

selected["cleaned_data"] = selected["text"].apply(lambda x: clean(x) if x != None else x)
```
Choosing embeddings is the main key point for obtaining good results. Utilising all-minilm-l6-v2 for this usecase  
埋め込みを選択することは、良い結果を得るための主なポイントです。このユースケースではall-minilm-l6-v2を利用しています。

```python
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
```
```python
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
```
model  
モデル  
'sentence-transformers/all-MiniLM-L6-v2'  
'sentence-transformers/all-MiniLM-L6-v2'  

```python
def get_embeddings(model, sentences: List[str], parallel: bool = True):
    start = time.time()
    if parallel:
        # Start the multi-process pool on all cores
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        pool = model.start_multi_process_pool(target_devices=["cpu"] * 5)
        embeddings = model.encode_multi_process(sentences, pool, batch_size=16)
        model.stop_multi_process_pool(pool)
    else:
        os.environ["TOKENIZERS_PARALLELISM"] = "true"
        embeddings = model.encode(sentences, batch_size=32, show_progress_bar=True, convert_to_tensor=True,)
    print(f"Time taken to encode {len(sentences)} items: {round(time.time() - start, 2)}")
    return embeddings.detach().numpy()
```
```python
def get_embeddings(model, sentences: List[str], parallel: bool = True):
    start = time.time()
    if parallel:
        # Start the multi-process pool on all cores
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        pool = model.start_multi_process_pool(target_devices=["cpu"] * 5)
        embeddings = model.encode_multi_process(sentences, pool, batch_size=16)
        model.stop_multi_process_pool(pool)
    else:
        os.environ["TOKENIZERS_PARALLELISM"] = "true"
        embeddings = model.encode(sentences, batch_size=32, show_progress_bar=True, convert_to_tensor=True,)
    print(f"Time taken to encode {len(sentences)} items: {round(time.time() - start, 2)}")
    return embeddings.detach().numpy()
```
Choosing the index type followed by creating and saving is next step  
インデックスタイプを選択し、作成して保存することが次のステップです。

```python
# we have used flat Index and with Inner product here but another experiment in repo has partition index
def create_index(mappings, samples):
    index = faiss.IndexIDMap(faiss.IndexFlatIP(samples.shape[1]))
    faiss.normalize_L2(samples)  # normalise the embedding
    # index.train(samples)
    index.add_with_ids(samples, np.array(list(mappings.keys())))
    save_index(index)

create_index(mappings=mappings, samples=samples)
```
```python
# we have used flat Index and with Inner product here but another experiment in repo has partition index
def create_index(mappings, samples):
    index = faiss.IndexIDMap(faiss.IndexFlatIP(samples.shape[1]))
    faiss.normalize_L2(samples)  # normalise the embedding
    # index.train(samples)
    index.add_with_ids(samples, np.array(list(mappings.keys())))
    save_index(index)

create_index(mappings=mappings, samples=samples)
```
create_index  
create_index  
IndexIDMap  
IndexIDMap  
IndexFlatIP  
IndexFlatIP  
1  
1  
normalize_L2  
normalize_L2  
train  
train  
add_with_ids  
add_with_ids  
array  
array  
list  
list  
keys  
keys  
save_index  
save_index  
create_index  
create_index  

Last step is to read the index, search the query inside the index and obtain top N results and predicting for user query given mapping of categories  
最後のステップは、インデックスを読み込み、インデックス内でクエリを検索し、上位Nの結果を取得し、カテゴリのマッピングを考慮してユーザークエリを予測することです。

```python
# read the index
index = faiss.read_index("./data/news_train_index")
```
```python
# read the index
index = faiss.read_index("./data/news_train_index")
```
# read the index  
# インデックスを読み込む  
index  
インデックス  
"./data/news_train_index"  
"./data/news_train_index"  

```python
# embeddings for query
def predict_embeddings(query):
    query_embedding = model.encode(query)
    query_embedding = np.asarray([query_embedding], dtype="float32")
    return query_embedding
```
```python
# embeddings for query
def predict_embeddings(query):
    query_embedding = model.encode(query)
    query_embedding = np.asarray([query_embedding], dtype="float32")
    return query_embedding
```
# predict for given query  
# 指定されたクエリの予測  
```python
def predict(query, mappings):
    cleaned_query = clean(query)
    query_embedding = predict_embeddings(cleaned_query)
    faiss.normalize_L2(query_embedding)
    D, I = index.search(query_embedding, 10)  # d is the distance and I is the index number
    D = [np.unique(D)]
    I = [np.unique(I)]
    res_df = []
    for values in I:
        for val in D:
            details = {
                'cleaned_text': list(train.iloc[values]["cleaned_data"]),
                'category': list(train.iloc[values]["title"]),
                'score': list(val)
            }
            res_df.append(details)
    return res_df
```
```python
def predict(query, mappings):
    cleaned_query = clean(query)
    query_embedding = predict_embeddings(cleaned_query)
    faiss.normalize_L2(query_embedding)
    D, I = index.search(query_embedding, 10)  # d is the distance and I is the index number
    D = [np.unique(D)]
    I = [np.unique(I)]
    res_df = []
    for values in I:
        for val in D:
            details = {
                'cleaned_text': list(train.iloc[values]["cleaned_data"]),
                'category': list(train.iloc[values]["title"]),
                'score': list(val)
            }
            res_df.append(details)
    return res_df
```
# predict for given query  
# 指定されたクエリの予測  
def  
def  
predict  
predict  
query, mappings  
query, mappings  
10  
10  
# d is the distance and I is the index number  
# dは距離で、Iはインデックス番号です  
for  
for  
in  
in  
I:  
I:  
for  
for  
in  
D:  
D:  
'cleaned_text'  
'cleaned_text'  
: list  
: list  
"cleaned_data"  
"cleaned_data"  
'category'  
'category'  
: list  
: list  
"title"  
"title"  
'score'  
'score'  
: list  
: list  
return  
return  

Example 1:  
例1:  
```python
res = predict("glycemic index", mappings=mappings)  # score is actually distance so lower is better
```
```python
res = predict("glycemic index", mappings=mappings)  # score is actually distance so lower is better
```
res  
res  
"glycemic index"  
"glycemic index"  
# score is actually distance so lower is better  
# スコアは実際には距離であり、低い方が良い  

```python
def most_frequent(result):
    top2 = Counter(result)
    return top2.most_common(1)
```
```python
def most_frequent(result):
    top2 = Counter(result)
    return top2.most_common(1)
```
most_frequent  
most_frequent  
Counter  
Counter  
most_common  
most_common  
1  
1  
Results of top 5 similar sentences belong to the category sci.med and from above function the most common is sci.med. Hence the final class we considered is sci.med.  
上位5つの類似文の結果はカテゴリsci.medに属し、上記の関数から最も一般的なのはsci.medです。したがって、私たちが考慮した最終クラスはsci.medです。

Example 2  
例2  
```python
res = predict("cad tools utilises graphics card the quality of image depends on the quality of graphics card.", mappings=mappings)
```
```python
res = predict("cad tools utilises graphics card the quality of image depends on the quality of graphics card.", mappings=mappings)
```
res  
res  
"cad tools utilises graphics card the quality of image depends on the quality of graphics card."  
"cad tools utilises graphics card the quality of image depends on the quality of graphics card."  
Press enter or click to view image in full size  
画像をフルサイズで表示するには、Enterキーを押すかクリックしてください。  
The above example returns top 5 from two categories but most common is graphics class. Hence final class for the query is graphics.  
上記の例は2つのカテゴリから上位5を返しますが、最も一般的なのはグラフィックスクラスです。したがって、クエリの最終クラスはグラフィックスです。

Comparison of results with flat index and ivfflat index:  
フラットインデックスとivfflatインデックスの結果の比較:  
Press enter or click to view image in full size  
画像をフルサイズで表示するには、Enterキーを押すかクリックしてください。  
More details about entire logic for different indexes mentioned above are available in the GitHub repository — refer to readme for installation steps.  
上記で言及された異なるインデックスの全体的なロジックに関する詳細は、GitHubリポジトリにあります — インストール手順についてはreadmeを参照してください。

Conclusion:  
結論:  
Faiss is known for its user-friendly nature, making installation and usage hassle-free. The library is compatible with both GPU and CPU, adding to its versatility. It boasts exceptional speed, excelling in both index creation and searching. It is important to be aware that adding new data to an existing index is not currently supported. Instead, creating a new index is required, but the process is quick, so there is no need for significant concern about time consumption.  
Faissはそのユーザーフレンドリーな性質で知られており、インストールと使用が簡単です。このライブラリはGPUとCPUの両方に対応しており、その汎用性を高めています。インデックス作成と検索の両方で優れた速度を誇ります。既存のインデックスに新しいデータを追加することは現在サポートされていないことに注意することが重要です。代わりに、新しいインデックスを作成する必要がありますが、そのプロセスは迅速であるため、時間消費について大きな懸念を抱く必要はありません。

References:  
参考文献:  
https://github.com/Harika-3196/classification-using-faiss-semantic-search-index  
https://www.pinecone.io/learn/faiss-tutorial/  
https://github.com/facebookresearch/faiss/wiki/Getting-started  
Faiss indexes  
Faissインデックス  

Tags:  
タグ:  
Semantic Search Classification Faiss Scaling  
セマンティック検索 分類 Faiss スケーリング  



## Published in Walmart Global Tech Blog

Published in Walmart Global Tech Blog
Walmart Global Tech Blogに掲載されました。

19.1K followers
19.1Kフォロワー

·
·
Apr 7, 2026
2026年4月7日

We’re powering the next great retail disruption. 
私たちは次の大きな小売の変革を推進しています。

Learn more about us—https://www.linkedin.com/company/walmartglobaltech/
私たちについてもっと知る—https://www.linkedin.com/company/walmartglobaltech/

Follow
フォロー

Follow
フォロー

Follow
フォロー

Follow
フォロー



## Written by Harika Samala 著者情報

Written by Harika Samala
ハリカ・サマラによって書かれました
47 followers
フォロワー 47人
·
·
Data Scientist @Walmart
Walmartのデータサイエンティスト
Follow
フォロー



## Responses (1) 返信 (1)

Write a response 返信を書く  
What are your thoughts? あなたの考えは何ですか？  
What are your thoughts? あなたの考えは何ですか？  
Yogesh Gurjar  
Apr 10, 2024  
2024年4月10日  

```
Hi Harika,Have you tried using binary quantized embedding it can save a lot of space and search using GPUs it can make your index and search time more efficient.  
こんにちは、Harika。バイナリ量子化埋め込みを使用してみましたか？これにより、多くのスペースを節約でき、GPUを使用して検索することで、インデックスと検索時間をより効率的にすることができます。
```
Reply 返信



## More from Harika Samala and Walmart Global Tech Blog ハリカ・サマラとウォルマートグローバルテックブログのさらなる情報

In
Walmart Global Tech Blog
by
Harika Samala
ウォルマートグローバルテックブログにおいて
ハリカ・サマラによる



## Evaluation of RAG Metrics using RAGA RAGメトリクスのRAGAを用いた評価

### In the AI domain, Large Language Models (LLMs) are hogging the limelight. 
AI分野では、大規模言語モデル（LLMs）が注目を集めています。 
These innovative marvels serve as the intelligence core for…
これらの革新的な驚異は、…の知能の中核として機能します。

Jul 5, 2024
2024年7月5日

Jul 5, 2024
2024年7月5日

Jul 5, 2024
2024年7月5日

In
Walmart Global Tech Blog
にて

by
Alok Mishra
著者：Alok Mishra



## From Single Instance to Split-Brain: A Database Scaling Journey 単一インスタンスからスプリットブレインへ：データベーススケーリングの旅

### I used to think adding a ‘Read Replica’ was a magic button for scaling applications. 
私は、‘Read Replica’を追加することがアプリケーションのスケーリングのための魔法のボタンだと思っていました。

### I was wrong. 
私は間違っていました。

### While splitting read and write traffic is…
読み取りと書き込みのトラフィックを分割することは…



## Understanding the Jest Coverage Report: A Complete Guide Jestのカバレッジレポートの理解：完全ガイド

### Introduction はじめに
Apr 3, 2025A response icon2
2025年4月3日A response icon2
Apr 3, 2025
2025年4月3日
Apr 3, 2025
2025年4月3日
2
Harika Samala
ハリカ・サマラ



## Meta-Learning Approach for Subjective Sentiment Analysis in Chatbots
### Chatbots have surged in popularity across diverse sectors like e-commerce, healthcare, travel, banking, and food services. 
チャットボットは、eコマース、ヘルスケア、旅行、銀行、食品サービスなどの多様な分野で人気が急上昇しています。
While they…
しかし、彼らは…
Apr 27, 2024
2024年4月27日
Apr 27, 2024
2024年4月27日
Apr 27, 2024
2024年4月27日



## Recommended from Medium おすすめ記事

In
Level Up Coding
by
Vivedha Elango
において



## How to build a Multi-Modal RAG system that finally understands images, tables, and text? 
### Your ultimate guide to building a multimodal RAG system 
画像、表、テキストを最終的に理解するマルチモーダルRAGシステムの構築方法
あなたのマルチモーダルRAGシステム構築のための究極のガイド

Nov 26, 2025A response icon1
2025年11月26日
Nov 26, 2025
2025年11月26日
1
Vishal Mysore
ヴィシャール・マイソール



## What Is PageIndex? How to Build a Vectorless RAG System (No Embeddings, No Vector DB) PageIndexとは何か？ベクトルなしのRAGシステムを構築する方法（埋め込みなし、ベクトルDBなし）

### PageIndex is a vectorless, reasoning-based Retrieval-Augmented Generation (RAG) approach that retrieves answers from long documents without… 
PageIndexは、長い文書から回答を取得するベクトルなしの推論ベースのRetrieval-Augmented Generation（RAG）アプローチです…



## The Past and Present of Stream Processing (Part 23): Python-Native Ultra-Fast Streaming with Quix…
ストリーム処理の過去と現在（第23部）：QuixによるPythonネイティブの超高速ストリーミング…

### Quix Streams is a Python library designed as a Kafka stream processing tool for data engineers and data scientists. 
Quix Streamsは、データエンジニアとデータサイエンティストのために設計されたKafkaストリーム処理ツールとしてのPythonライブラリです。 
It provides a…
それは…を提供します。

Oct 21, 2025
2025年10月21日

Oct 21, 2025
2025年10月21日

Oct 21, 2025
2025年10月21日

In
に

Towards AI
AIに向けて

by
著者

Prem Vishnoi(cloudvala)
Prem Vishnoi（cloudvala）



## Embeddings Made Easy: How to Teach Machines to Understand Images, Videos, and Audio
## 埋め込みを簡単に: 機械に画像、動画、音声を理解させる方法

### Embeddings are how machines understand meaning not just words, but everything they see, hear, and watch
### 埋め込みは、機械が言葉だけでなく、彼らが見る、聞く、そして見るすべての意味を理解する方法です

Nov 8, 2025A response icon1
2025年11月8日 反応アイコン1

Nov 8, 2025
2025年11月8日

Nov 8, 2025
2025年11月8日

1
1

In
Rebooted Minds
に掲載

by
Shreyas Naphad
著者: Shreyas Naphad



## LoRA & QLoRA: The Beginner-Friendly Guide to LLM Fine-Tuning
## LoRA & QLoRA: LLMファインチューニングの初心者向けガイド

### The fine-tuning cheat code nobody told you about
### 誰も教えてくれなかったファインチューニングの裏技
Dec 8, 2025A response icon1
2025年12月8日A response icon1
Dec 8, 2025
2025年12月8日
Dec 8, 2025
2025年12月8日
1
Divyansh Pandey
1
ディヴヤンシュ・パンデイ



## Building a Real-Time Fraud Detection System: Model Serving (Part 4/6) リアルタイム詐欺検出システムの構築：モデル提供（パート4/6）

### Serving XGBoost predictions in 5ms using FastAPI and Pydantic. FastAPIとPydanticを使用して5msでXGBoost予測を提供する。

Jan 15 1月15日
Jan 15 1月15日
Jan 15 1月15日
Help ヘルプ
Status ステータス
About 概要
Careers キャリア
Press プレス
Blog ブログ
Privacy プライバシー
Rules ルール
Terms 利用規約
Text to speech テキスト読み上げ
