## link リンク

https://towardsdatascience.com/topic-modeling-with-bert-779f7db187e6
https://towardsdatascience.com/topic-modeling-with-bert-779f7db187e6

# Topic Modeling with BERT: Leveraging BERT and TF-IDF to create easily interpretable topics. BERT によるトピックモデリング：BERT と TF-IDF を活用して、解釈しやすいトピックを作成する。

Often when I am approached by a product owner to do some NLP-based analyses, I am typically asked the following question:
プロダクト・オーナーからNLPに基づく分析を依頼されると、しばしば次のような質問をされる：

‘Which topic can frequently be found in these documents?’
これらの文書にはどのトピックが頻繁に見られるか？

Void of any categories or labels I am forced to look into unsupervised techniques to extract these topics, namely Topic Modeling.
カテゴリーやラベルがないため、これらのトピックを抽出するために教師なし技術、つまりトピック・モデリングに目を向けざるを得ない。

Although topic models such as LDA and NMF have shown to be good starting points, I always felt it took quite some effort through hyperparameter tuning to create meaningful topics.
LDAやNMFのようなトピックモデルは良い出発点であることが示されているが、意味のあるトピックを作成するためには、ハイパーパラメーターのチューニングを通してかなりの努力が必要だと私はいつも感じていた。

Moreover, I wanted to use transformer-based models such as BERT as they have shown amazing results in various NLP tasks over the last few years.
さらに、BERTのような変換器ベースのモデルは、ここ数年、さまざまな自然言語処理タスクで素晴らしい結果を示しているので、それを使いたかった。
Pre-trained models are especially helpful as they are supposed to contain more accurate representations of words and sentences.
事前に訓練されたモデルは、単語や文章をより正確に表現しているため、特に有用である。

A few weeks ago I saw this great project named Top2Vec\* which leveraged document- and word embeddings to create topics that were easily interpretable.
数週間前、Top2Vec*という素晴らしいプロジェクトを見た。このプロジェクトでは、文書と単語の埋め込みを活用して、解釈しやすいトピックを作成していた。
I started looking at the code to generalize Top2Vec such that it could be used with pre-trained transformer models.
私は、Top2Vecを一般化し、訓練済みの変換モデルで使えるようにするためのコードを調べ始めた。

The great advantage of Doc2Vec is that the resulting document- and word embeddings are jointly embedding in the same space which allows document embeddings to be represented by nearby word embeddings.
Doc2Vecの大きな利点は、結果として得られる文書埋め込みと単語埋め込みが同じ空間に共同で埋め込まれることであり、これにより文書埋め込みを近傍の単語埋め込みで表現できるようになる。
Unfortunately, this proved to be difficult as BERT embeddings are token-based and do not necessarily occupy the same space\*\*.
残念ながら、BERT埋め込みはトークン・ベースであり、必ずしも同じ空間**を占有しないため、これは困難であることが判明した。

Instead, I decided to come up with a different algorithm that could use BERT and 🤗 transformers embeddings.
その代わりに、私はBERTと🤗変換埋め込みを使用できる別のアルゴリズムを考え出すことにした。
The result is BERTopic, an algorithm for generating topics using state-of-the-art embeddings.
その結果がBERTopicであり、最先端の埋め込みを用いてトピックを生成するアルゴリズムである。

The main topic of this article will not be the use of BERTopic but a tutorial on how to use BERT to create your own topic model.
この記事の主なトピックは、BERTopic の使用ではなく、BERT を使用して独自のトピックモデルを作成する方法のチュートリアルである。

PAPER\*: Angelov, D.(2020).
PAPER*： Angelov, D.(2020).
Top2Vec: Distributed Representations of Topics.
Top2Vec： トピックの分散表現
arXiv preprint arXiv:2008.09470.
arXiv preprint arXiv:2008.09470.

NOTE\*\*: Although you could have them occupy the same space, the resulting size of the word embeddings is quite large due to the contextual nature of BERT.
NOTE* 同じ空間を占有させることもできるが、BERTの文脈的性質のため、結果として単語埋め込み のサイズはかなり大きくなる。
Moreover, there is a chance that the resulting sentence- or document embeddings will degrade in quality.
さらに、結果として得られる文埋め込みや文書埋め込みの品質が低下する可能性もある。

## Data & Packages データ＆パッケージ

For this example, we use the famous 20 Newsgroups dataset which contains roughly 18000 newsgroups posts on 20 topics.
この例では、20のトピックに関する約18000のニュースグループの投稿を含む有名な20 Newsgroupsデータセットを使用する。
Using Scikit-Learn, we can quickly download and prepare the data:
Scikit-Learnを使えば、データを素早くダウンロードして準備できる：

If you want to speed up training, you can select the subset train as it will decrease the number of posts you extract.
学習速度を上げたい場合は、サブセット学習を選択すると、抽出する投稿の数が減ります。

NOTE: If you want to apply topic modeling not on the entire document but on the paragraph level, I would suggest splitting your data before creating the embeddings.
注：文書全体ではなく、段落レベルでトピックモデリングを適用したい場合は、埋め込みを作成する前にデータを分割することをお勧めします。

## Embeddings エンベッディング

The very first step we have to do is converting the documents to numerical data.
最初にしなければならないのは、文書を数値データに変換することだ。
We use BERT for this purpose as it extracts different embeddings based on the context of the word.
この目的のために、単語の文脈に基づいて異なる埋め込みを抽出するBERTを使用する。
Not only that, there are many pre-trained models available ready to be used.
それだけでなく、多くの訓練済みモデルが用意されており、すぐに利用できる。

How you generate the BERT embeddings for a document is up to you.
文書の BERT 埋め込みをどのように生成するかは、あなた次第です。
However, I prefer to use the sentence-transformers package as the resulting embeddings have shown to be of high quality and typically work quite well for document-level embeddings.
しかし、私は文変換パッケージを使うことを好む。なぜなら、結果として得られる埋め込みは高品質であることが示されており、一般的に文書レベルの埋め込みでは非常にうまく機能するからである。

Install the package with pip install sentence-transformers before generating the document embeddings.
文書埋め込みを生成する前に、pip install sentence-transformersでパッケージをインストールしてください。
If you run into issues installing this package, then it is worth installing Pytorch first.
このパッケージのインストールで問題が発生した場合は、まずPytorchをインストールする価値がある。

Then, run the following code to transform your documents in 512-dimensional vectors:
次に、以下のコードを実行して、文書を512次元ベクトルに変換する：

We are using Distilbert as it gives a nice balance between speed and performance.
私たちは、スピードとパフォーマンスのバランスが良いDistilbertを使用しています。
The package has several multi-lingual models available for you to use.
このパッケージには、いくつかの多言語モデルが用意されている。

NOTE: Since transformer models have a token limit, you might run into some errors when inputting large documents.
注：トランスフォーマ・モデルにはトークンの制限があるため、大きな文書を入力するとエラーが発生することがあります。
In that case, you could consider splitting documents into paragraphs.
その場合、文書を段落ごとに分割することも考えられる。

## Clustering クラスタリング

We want to make sure that documents with similar topics are clustered together such that we can find the topics within these clusters.
似たようなトピックを持つ文書がクラスター化され、そのクラスター内のトピックを見つけることができるようにしたい。
Before doing so, we first need to lower the dimensionality of the embeddings as many clustering algorithms handle high dimensionality poorly.
その前に、多くのクラスタリング・アルゴリズムが高次元をうまく扱えないため、埋め込みデータの次元を下げる必要がある。

UMAP
UMAP

Out of the few dimensionality reduction algorithms, UMAP is arguably the best performing as it keeps a significant portion of the high-dimensional local structure in lower dimensionality.
数少ない次元削減アルゴリズムの中で、UMAPは、高次元の局所構造のかなりの部分を低次元に保つので、間違いなく最も性能が良い。

Install the package with pip install umap-learn before we lower the dimensionality of the document embeddings.
文書の埋め込み次元を下げる前に、pip install umap-learnでパッケージをインストールする。
We reduce the dimensionality to 5 while keeping the size of the local neighborhood at 15.
局所近傍のサイズを15に保ちながら、次元を5に減らす。
You can play around with these values to optimize for your topic creation.
トピック作成に最適化するために、これらの値を弄ることができる。
Note that a too low dimensionality results in a loss of information while a too high dimensionality results in poorer clustering results.
次元数が低すぎると情報が失われ、次元数が高すぎるとクラスタリング結果が悪くなることに注意。

HDBSAN
HDBSAN

After having reduced the dimensionality of the documents embeddings to 5, we can cluster the documents with HDBSCAN.
埋め込み文書の次元数を5まで減らした後、HDBSCANで文書をクラスタリングすることができる。
HDBSCAN is a density-based algorithm that works quite well with UMAP since UMAP maintains a lot of local structure even in lower-dimensional space.
HDBSCANは密度ベースのアルゴリズムであり、UMAPと非常に相性が良い。UMAPは低次元空間でも多くの局所構造を維持するからだ。
Moreover, HDBSCAN does not force data points to clusters as it considers them outliers.
さらに、HDBSCANはデータ点を外れ値とみなして強制的にクラスタに入れない。

Install the package with pip install hdbscan then create the clusters:
pip install hdbscanでパッケージをインストールし、クラスタを作成します：

Great! We now have clustered similar documents together which should represent the topics that they consist of.
素晴らしい！これで、似たような文書がクラスター化され、それらが構成するトピックを表すようになりました。
To visualize the resulting clusters we can further reduce the dimensionality to 2 and visualize the outliers as grey points:
得られたクラスターを視覚化するために、さらに次元を2に減らし、異常値をグレーの点として視覚化することができる：

It is difficult to visualize the individual clusters due to the number of topics generated (~55).
生成されたトピックの数（～55）が多いため、個々のクラスターを可視化するのは難しい。
However, we can see that even in 2-dimensional space some local structure is kept.
しかし、2次元空間でも局所的な構造が保たれていることがわかる。

NOTE: You could skip the dimensionality reduction step if you use a clustering algorithm that can handle high dimensionality like a cosine-based k-Means.
注意: 余弦ベースのk-Meansのような高次元を扱えるクラスタリングアルゴリズムを使用する場合は、次元削減ステップを省略できます。

## Topic Creation トピック作成

What we want to know from the clusters that we generated, is what makes one cluster, based on their content, different from another?
生成されたクラスターから私たちが知りたいのは、その内容に基づいて、あるクラスターが他のクラスターと何が違うのか、ということだ。

How can we derive topics from clustered documents?
クラスタ化された文書からトピックを導き出すには？

To solve this, I came up with a class-based variant of TF-IDF (c-TF-IDF), that would allow me to extract what makes each set of documents unique compared to the other.
これを解決するために、私はTF-IDFのクラスベースの変形（c-TF-IDF）を考え出した。

The intuition behind the method is as follows.
この方法の背後にある直観は次のようなものだ。
When you apply TF-IDF as usual on a set of documents, what you are basically doing is comparing the importance of words between documents.
文書集合に対してTF-IDFを通常通り適用する場合、基本的に行っていることは、文書間の単語の重要度を比較することである。

What if, we instead treat all documents in a single category (e.g., a cluster) as a single document and then apply TF-IDF? The result would be a very long document per category and the resulting TF-IDF score would demonstrate the important words in a topic.
その代わりに、1つのカテゴリー（クラスターなど）に含まれるすべての文書を1つの文書として扱い、TF-IDFを適用したらどうだろうか。その結果、カテゴリーごとに非常に長い文書ができ、その結果得られるTF-IDFスコアは、トピックにおける重要な単語を示すことになるだろう。

c-TF-IDF
c-TF-IDF

To create this class-based TF-IDF score, we need to first create a single document for each cluster of documents:
このクラス・ベースのTF-IDFスコアを作成するには、まず文書のクラスタごとに1つの文書を作成する必要がある：

Then, we apply the class-based TF-IDF:
次に、クラスベースのTF-IDFを適用する：

Where the frequency of each word t is extracted for each class i and divided by the total number of words w.
ここで、各単語の頻度tは、各クラスiについて抽出され、単語の総数wで割られる。
This action can be seen as a form of regularization of frequent words in the class.
この動作は、クラス内の頻出単語を規則化する一形態と見ることができる。
Next, the total, unjoined, number of documents m is divided by the total frequency of word t across all classes n.
次に、結合されていない総文書数mを、全クラスにわたる単語tの総頻度nで割る。

Now, we have a single importance value for each word in a cluster which can be used to create the topic.
これで、クラスタ内の各単語に対して、トピックを作成するために使用できる単一の重要度値が得られた。
If we take the top 10 most important words in each cluster, then we would get a good representation of a cluster, and thereby a topic.
各クラスターで最も重要な単語の上位10個を取り出せば、クラスター、ひいてはトピックをうまく表現できるだろう。

Topic Representation
トピックの表現

In order to create a topic representation, we take the top 20 words per topic based on their c-TF-IDF scores.
トピック表現を作成するために、c-TF-IDFスコアに基づいてトピックごとに上位20語を抽出する。
The higher the score, the more representative it should be of its topic as the score is a proxy of information density.
スコアが高ければ高いほど、情報密度の代用となるため、そのトピックをより代表していることになる。

We can use topic_sizes to view how frequent certain topics are:
topic_sizesを使えば、特定のトピックがどれくらいの頻度で使われているかを見ることができる：

The topic name-1 refers to all documents that did not have any topics assigned.
トピック名-1は、トピックが割り当てられていないすべての文書を指す。
The great thing about HDBSCAN is that not all documents are forced towards a certain cluster.
HDBSCANの素晴らしいところは、すべての文書が特定のクラスタに強制されるわけではないことだ。
If no cluster could be found, then it is simply an outlier.
クラスターが見つからなかった場合は、単なる外れ値である。

We can see that topics 7, 43, 12, and 41 are the largest clusters that we could create.
トピック7、43、12、41が、作成可能な最大のクラスターであることがわかる。
To view the words belonging to those topics, we can simply use the dictionarytop_n_words to access these topics:
これらのトピックに属する単語を表示するには、単に辞書top_n_wordsを使ってこれらのトピックにアクセスすればよい：

Looking at the largest four topics, I would say that these nicely seem to represent easily interpretable topics!
最大の4つのトピックを見ると、これらはうまく解釈しやすいトピックを表しているように思える！

I can see sports, computers, space, and religion as clear topics that were extracted from the data.
データから抽出された明確なトピックとして、スポーツ、コンピューター、宇宙、宗教を挙げることができる。

Topic Reduction
トピック削減

There is a chance that, depending on the dataset, you will get hundreds of topics that were created! You can tweak the parameters of HDBSCAN such that you will get fewer topics through its min_cluster_size parameter but it does not allow you to specify the exact number of clusters.
データセットによっては、何百ものトピックが作成される可能性があります！HDBSCANのmin_cluster_sizeパラメータでトピックを少なくするようにパラメータを調整することはできますが、正確なクラスタ数を指定することはできません。

A nifty trick that Top2Vec was using is the ability to reduce the number of topics by merging the topic vectors that were most similar to each other.
Top2Vecが使っていた気の利いたトリックは、互いに最も似ているトピックベクトルをマージすることによってトピック数を減らす機能である。

We can use a similar technique by comparing the c-TF-IDF vectors among topics, merge the most similar ones, and finally re-calculate the c-TF-IDF vectors to update the representation of our topics:
トピック間でc-TF-IDFベクトルを比較し、最も類似しているものをマージし、最後にc-TF-IDFベクトルを再計算してトピックの表現を更新することで、同様の手法を使うことができる：

Above, we took the least common topic and merged it with the most similar topic.
上記では、最も一般的でないトピックを取り上げ、最も類似したトピックとマージした。
By repeating this 19 more times we reduced the number of topics from 56 to 36!
これをさらに19回繰り返すことで、トピックの数を56から36に減らした！

NOTE: We can skip the re-calculation part of this pipeline to speed up the topic reduction step.
注：トピック削減ステップを高速化するために、このパイプラインの再計算部分をスキップすることができます。
However, it is more accurate to re-calculate the c-TF-IDF vectors as that would better represent the newly generated content of the topics.
しかし、c-TF-IDFベクトルを再計算する方が、新しく生成されたトピックの内容をより正確に表すことができる。
You can play around with this by, for example, update every n steps to both speed-up the process and still have good topic representations.
例えば、nステップごとに更新することで、処理を高速化し、かつトピックを適切に表現することができる。

TIP: You can use the method described in this article (or simply use BERTopic) to also create sentence-level embeddings.
ヒント：この記事で説明されている方法（または単にBERTopicを使用する）を使用して、文レベルの埋め込みも作成できます。
The main advantage of this is the possibility to view the distribution of topics within a single document.
この主な利点は、1つの文書内のトピックの分布を見ることができることである。

Thank you for reading!
読んでくれてありがとう！

If you are, like me, passionate about AI, Data Science, or Psychology, please feel free to add me on LinkedIn or follow me on Twitter.
私のようにAI、データサイエンス、心理学に情熱を持っている方は、お気軽にLinkedInで私を追加するか、Twitterで私をフォローしてください。

All examples and code in this article can be found here:
この記事のすべての例とコードはここにある：