refs: https://bytebytego.com/courses/machine-learning-system-design-interview/visual-search-system

# Visual Search System ビジュアル検索システム

A system helps users discover images that are visually similar to a selected image. 
ユーザーが選択した画像に視覚的に類似した画像を発見するのを助けるシステムです。
In this chapter, we design a visual search system similar to Pinterest’s [1] [2]. 
この章では、Pinterestに似たビジュアル検索システムを設計します。

### Clarifying Requirements 要件の明確化

Here’s a typical interaction between a candidate and an interviewer.
ここでは、候補者と面接官の典型的なやり取りを示します。

Candidate: Should we rank the results from most similar to least similar?
候補者: 結果を最も類似しているものから最も類似していないものへとランク付けすべきでしょうか？
Interviewer: Images that appear first in the list should be more similar to the query image.
面接官: リストの最初に表示される画像は、クエリ画像により類似しているべきです。

Candidate: Should the system support videos, too?
候補者: **システムは動画もサポートすべきでしょうか？**
Interviewer: Let’s focus only on images.
面接官: 画像のみに焦点を当てましょう。

Candidate: A platform like Pinterest allows users to select an image crop and retrieve similar images. Should we support that functionality?
候補者: Pinterestのようなプラットフォームでは、ユーザーが画像の切り抜きを選択し、類似の画像を取得できます。その機能をサポートすべきでしょうか？
Interviewer: Yes.
面接官: はい。

Candidate: Are the displayed images personalized to the user?
候補者: 表示される画像はユーザーにパーソナライズされていますか？
Interviewer: For simplicity, let’s not focus on personalization. A query image yields the same results, regardless of who searches for it.
面接官: **簡単のために、パーソナライズには焦点を当てないことにしましょう。クエリ画像は、誰が検索しても同じ結果をもたらします。**

Candidate: Can the model use the metadata of the query image, such as image tags?
候補者: モデルは、画像タグなどのクエリ画像のメタデータを使用できますか？
Interviewer: In practice, the model uses image metadata. But for simplicity, let’s assume we don’t rely on the metadata, but only on the image pixels.
面接官: **実際には、モデルは画像のメタデータを使用します。しかし、簡単のために、メタデータには依存せず、画像のピクセルのみに基づくと仮定**しましょう。

Candidate: Can users perform other actions such as save, share, or like? These actions can help label training data.
候補者: **ユーザーは保存、共有、または「いいね」をするなどの他のアクションを実行できますか？これらのアクションは、トレーニングデータのラベル付けに役立ちます**。
Interviewer: Great point. For simplicity, let’s assume the only supported action is image clicks.
面接官: いい指摘です。簡単のために、サポートされるアクションは画像のクリックのみと仮定しましょう。

Candidate: Should we moderate the images?
候補者: 画像をモデレートすべきでしょうか？ (=不適切画像のフィルタリングなど??:thinking:)
Interviewer: It’s important to keep the platform safe, but content moderation is out of scope.
面接官: プラットフォームを安全に保つことは重要ですが、コンテンツのモデレーションは範囲外です。

Candidate: We can construct training data online and label them based on user interactions. Is this the expected way to construct training data?
候補者: **オンラインでトレーニングデータを構築し、ユーザーのインタラクションに基づいてラベル付けできます。これはトレーニングデータを構築するための期待される方法ですか？**
Interviewer: Yes, that sounds reasonable.
面接官: はい、それは合理的に聞こえます。
(オンライン学習前提ってことか...?:thinking:)

Candidate: How fast should the search be? Assuming we have 100-200 billion images on the platform, the system should be able to retrieve similar images quickly. Is that a reasonable assumption?
候補者: 検索はどれくらい速くあるべきでしょうか？**プラットフォームに1000億から2000億の画像があると仮定**すると、システムは類似の画像を迅速に取得できるべきです。それは合理的な仮定ですか？
Interviewer: Yes, that is a reasonable assumption.
面接官: はい、それは合理的な仮定です。

Let’s summarize the problem statement.
問題の声明を要約しましょう。
We are asked to design a visual search system.
私たちは、視覚検索システムを設計するよう求められています。
The system retrieves images similar to the query image provided by the user, ranks them based on their similarities to the query image, and then displays them to the user.
システムは、ユーザーが提供したクエリ画像に類似した画像を取得し、それらをクエリ画像との類似性に基づいてランク付けし、ユーザーに表示します。
The platform only supports images, with no video or text queries allowed.
プラットフォームは画像のみをサポートし、動画やテキストのクエリは許可されていません。
For simplicity, no personalization is required.
簡単のために、パーソナライズは必要ありません。

<!-- ここまで読んだ! -->

### Frame the Problem as an ML Task 機械学習タスクとして問題を定義する

In this section, we choose a well-defined ML objective and frame the visual search problem as an ML task.
このセクションでは、明確に定義された機械学習の目的を選択し、視覚検索問題を機械学習タスクとして定義します。

#### Defining the ML objective MLの目的の定義

In order to solve this problem using an ML model, we need to create a well-defined ML objective. 
**この問題をMLモデルを使用して解決するためには、明確に定義されたMLの目的を作成する必要があります**。
A potential ML objective is to accurately retrieve images that are visually similar to the image the user is searching for.
潜在的なMLの目的は、ユーザが検索している画像に視覚的に類似した画像を正確に取得することです。

#### Specifying the system’s input and output システムの入力と出力の指定

The input of a visual search system is a query image provided by the user. 
視覚検索システムの入力は、ユーザによって提供されたクエリ画像です。
The system outputs images that are visually similar to the query image, and the output images are ranked by similarities. 
システムは、クエリ画像に視覚的に類似した画像を出力し、出力画像は類似性によってランク付けされます。
Figure 2.2 shows the input and output of a visual search system. 
図2.2は、視覚検索システムの入力と出力を示しています。

![]()

#### Choosing the right ML category 適切なMLカテゴリの選択

The output of the model is a set of ranked images that are similar to the query image. 
モデルの出力は、クエリ画像に類似したランク付けされた画像のセットです。
As a result, visual search systems can be framed as a ranking problem. 
その結果、**視覚検索システムはランキング問題として定義できます。**
In general, the goal of ranking problems is to rank a collection of items, such as images, websites, products, etc., based on their relevance to a query, so that more relevant items appear higher in the search results. 
一般的に、ランキング問題の目標は、画像、ウェブサイト、製品などの**アイテムのコレクションをクエリに対する関連性に基づいてランク付けし、より関連性の高いアイテムが検索結果の上位に表示されるようにすること**です。
Many ML applications, such as recommendation systems, search engines, document retrieval, and online advertising, can be framed as ranking problems. 
推薦システム、検索エンジン、文書検索、オンライン広告など、**多くのMLアプリケーションはランキング問題として定義できます**。
In this chapter, we will use a widely-used approach called representation learning. 
この章では、**表現学習と呼ばれる広く使用されているアプローチを使用**します。
Let’s examine this in more detail. 
これについて詳しく見ていきましょう。

##### Representation learning. 表現学習。

In representation learning [3], a model is trained to transform input data, such as images, into representations called embeddings. 
表現学習では、**モデルが画像などの入力データを埋め込みと呼ばれる表現に変換するように訓練されます**。
Another way of describing this is that the model maps input images to points in an N-dimensional space called embedding space. 
別の言い方をすると、**モデルは入力画像を埋め込み空間と呼ばれるN次元空間の点にマッピング**します。(わかりやすい...!:thinking:)
These embeddings are learned so that similar images have embeddings that are in close proximity to each other, in the space. 
**これらの埋め込みは、類似した画像が空間内で互いに近接した埋め込みを持つように学習**されます。(いい説明...!:thinking:)
Figure 2.3 illustrates how two similar images are mapped onto two points in close proximity within the embedding space. 
図2.3は、2つの類似した画像が埋め込み空間内の近接した2つの点にマッピングされる様子を示しています。
(そっか、two-towerモデルは表現学習とみなすこともできるのか...!:thinking:)
To demonstrate, we visualize image embeddings (denoted by ‘xxx’) in a222-dimensional space. 
例を示すために、a222次元空間における画像埋め込み（‘xxx’で示される）を視覚化します。
In reality, this space is NNN-dimensional, where NNN is the size of the embedding vector. 
実際には、この空間はN次元であり、Nは埋め込みベクトルのサイズです。

![]()

##### How to rank images using representation learning? 表現学習を使用して画像をランク付けする方法？

First, the input images are transformed into embedding vectors. 
まず、入力画像は埋め込みベクトルに変換されます。
Next, we calculate the similarity scores between the query image and other images on the platform by measuring their distances in the embedding space. 
次に、**埋め込み空間での距離を測定**することによって、クエリ画像とプラットフォーム上の他の画像との間の類似度スコアを計算します。
The images are ranked by similarity scores, as shown in Figure 2.4. 
画像は、図2.4に示されているように、類似度スコアによってランク付けされます。

![]()

At this point, you may have many questions, including how to ensure similar images are placed close to each other in the embedding space, how to define the similarity, and how to train such a model. 
この時点で、埋め込み空間内で類似した画像が互いに近接して配置されるようにする方法、類似性を定義する方法、そしてそのようなモデルを訓練する方法など、多くの質問があるかもしれません。
We will talk more about these in the model development section. 
これらについては、モデル開発セクションでさらに詳しく説明します。

<!-- ここまで読んだ! -->

### Data Preparation データ準備

#### Data engineering データエンジニアリング

Aside from generic data engineering fundamentals, it’s important to understand what data is available.  
一般的なデータエンジニアリングの基本に加えて、どのデータが利用可能であるかを理解することが重要です。
As a visual search system mainly focuses on users and images, we have the following data available:  
視覚検索システムは主にユーザと画像に焦点を当てているため、以下のデータが利用可能です：  

- Images 画像  
- Users ユーザ  
- User-image interactions ユーザ-画像インタラクション  

<!-- ここまで読んだ! -->

##### Images 画像

Creators upload images, and the system stores the images and their metadata, such as owner id, contextual information (e.g., upload time), tags, etc. 
クリエイターは画像をアップロードし、システムは画像とそのメタデータ（所有者ID、コンテキスト情報（例：アップロード時間）、タグなど）を保存します。
Table 2.1 shows a simplified example of image metadata. 
表2.1は、画像メタデータの簡略化された例を示しています。

![]()

Table 2.1: Image metadata 
表2.1: 画像メタデータ

##### Users ユーザ

User data contains demographic attributes associated with users, such as age, gender, etc.
ユーザデータには、年齢、性別などのユーザに関連する人口統計属性が含まれています。
Table 2.2 shows an example of user data. 
表2.2はユーザデータの例を示しています。
Table 2.2: User data
表2.2: ユーザデータ

##### User-image interactions ユーザー-画像インタラクション

Interaction data contains different types of user interactions. 
インタラクションデータには、さまざまなタイプのユーザーインタラクションが含まれています。
Based on the requirements gathered, the primary types of interactions are impressions and clicks. 
**収集した要件に基づいて、主なインタラクションのタイプはインプレッションとクリック**です。
Table 2.3 shows an overview of interaction data. 
表2.3はインタラクションデータの概要を示しています。

![]()

Table 2.3: User-image interaction data 
表2.3: ユーザー-画像インタラクションデータ

<!-- ここまで読んだ! -->

#### Feature engineering 特徴量エンジニアリング

In this section, you are expected to talk about engineering great features and preparing them as model inputs. 
このセクションでは、**優れた特徴量をエンジニアリングし、それらをモデルの入力として準備すること**について説明します。
This usually depends on how we framed the task and what the model’s inputs are.
**これは通常、タスクをどのように定義し、モデルの入力が何であるかに依存します。** 
In the earlier “Framing the problem as an ML task” section, we framed the visual search system as a ranking problem and used representation learning to solve it.
前の「問題をMLタスクとして定義する」セクションでは、視覚検索システムをランキング問題として定義し、それを解決するために表現学習を使用しました。
In particular, we employed a model which expects an image as input. 
特に、画像を入力として期待するモデルを採用しました。 
The image needs to be preprocessed before being passed to the model. 
画像はモデルに渡す前に前処理する必要があります。 
Let’s take a look at common image preprocessing operations: 
一般的な画像前処理操作を見てみましょう：

- Resizing: Models usually require fixed image sizes (e.g., 224×224) 
  - リサイズ：モデルは通常、固定された画像サイズ（例：224×224）を必要とします。
- Scaling: Scale pixel values of the image to the range of 0 and 1 
  - スケーリング：画像のピクセル値を0から1の範囲にスケーリングします。
- Z-score normalization: Scale pixel values to have a mean of 0 and variance of 1 
  - Zスコア正規化：ピクセル値を平均0、分散1になるようにスケーリングします。
- Consistent: Ensuring images have a consistent color mode (e.g., RGB or CMYK) 
  - 一貫性：画像が一貫したカラーモード（例：RGBまたはCMYK）を持つことを確認します。

### Model Development モデル開発

#### Model selection モデル選択

We choose neural networks because:
私たちはニューラルネットワークを選択します。理由は以下の通りです：

- Neural networks are good at handling unstructured data, such as images and text  
  - ニューラルネットワークは、画像やテキストなどの非構造化データを扱うのが得意です。
- Unlike many traditional machine learning models, neural networks are able to produce the embeddings we need for representation learning  
  - 多くの従来の機械学習モデルとは異なり、ニューラルネットワークは表現学習に必要な埋め込みを生成することができます。
  - (そうか、表現学習したいならモデル選択ってかなり限られてくるよな...!:thinking:)

What types of neural network architectures should we use?  
どのような種類のニューラルネットワークアーキテクチャを使用すべきでしょうか？
It is essential that the architecture works with images.  
アーキテクチャが画像に対応することが不可欠です。
CNN-based architectures such as ResNet [4] or more recent Transformer-based architectures [5] such as ViT [6] perform well with image inputs.  
ResNet [4]のようなCNNベースのアーキテクチャや、ViT [6]のような最近のTransformerベースのアーキテクチャは、画像入力に対して良好な性能を発揮します。
Figure 2.5 shows a simplified model architecture that transforms the input image into an embedding vector.  
図2.5は、入力画像を埋め込みベクトルに変換する簡略化されたモデルアーキテクチャを示しています。
The number of convolution layers, the number of neurons in fully connected layers, and the size of the embedding vector are hyperparameters typically chosen via experimentation.  
畳み込み層の数、全結合層のニューロンの数、および埋め込みベクトルのサイズは、通常、実験を通じて選択されるハイパーパラメータです。

![Figure 2.5: A simplified model architecture]()

<!-- ここまで読んだ! -->

#### Model training モデルの訓練

In order to retrieve visually similar images, a model must learn representations (embeddings) during training. 
視覚的に類似した画像を取得するためには、モデルが訓練中に表現（埋め込み）を学習する必要があります。
In this section, we discuss how to train a model to learn image representations. 
このセクションでは、画像表現を学習するためにモデルを訓練する方法について説明します。

A common technique for learning image representations is contrastive training [7]. 
**画像表現を学習するための一般的な手法は、コントラスト訓練(=つまり対照学習ね!:thinking:)です**[7]。
With this technique, we train the model to distinguish similar and dissimilar images. 
この手法を用いて、**モデルは類似した画像と異なる画像を区別するように**訓練されます。
As Figure 2.6 shows, we provide the model with a query image (left), one similar image to the query image (highlighted dog image on the right), and a few dissimilar images (also right.) 
図2.6に示すように、モデルにはクエリ画像（左）、クエリ画像に類似した画像（右のハイライトされた犬の画像）、およびいくつかの異なる画像（右側にも）を提供します。
During training, the model learns to produce representations in which the similar image more closely resembles the query image, than do other images on the right side of Figure 2.6. 
**訓練中、モデルは類似画像がクエリ画像により近い表現を生成することを学習します。**これは図2.6の右側にある他の画像よりもです。

![]()

To train the model using the contrastive training technique, we first need to construct training data. 
コントラスト訓練手法を使用してモデルを訓練するためには、まず訓練データを構築する必要があります。

<!-- ここまで読んだ! -->

#### Constructing the dataset データセットの構築

(nクラス分類問題としてlossを作る的なやつかな...?:thinking:)

As described earlier, each data point used for training contains a query image, a positive image that’s similar to the query image, andn−1{n-1}n−1negative images that are dissimilar to the query image. 
前述のように、トレーニングに使用される各データポイントには、クエリ画像、クエリ画像に類似した正の画像、およびクエリ画像に類似しないn−1の負の画像が含まれています。 
The ground truth label of the data point is the index of the positive image. 
データポイントの真のラベルは、正の画像のインデックスです。 
As Figure 2.7 shows, along with the query image (q), we havennnother images, of which one is similar to the q (image of the dog), and the othern−1{n-1}n−1images are dissimilar. 
図2.7に示すように、クエリ画像（q）とともに、nnnの他の画像があり、そのうちの1つはqに類似しており（犬の画像）、他のn−1{n-1}n−1の画像は類似していません。 
The ground truth label for this data point is the index of the positive image, which is222(the second image among thennnimages in Figure 2.7. 
このデータポイントの真のラベルは、正の画像のインデックスであり、222（図2.7のnnn画像の中の2番目の画像）です。 

![]()

To construct a training data point, we randomly choose a query image andn−1{n-1}n−1images as negative images. 
トレーニングデータポイントを構築するために、クエリ画像とn−1{n-1}n−1の画像を負の画像としてランダムに選択します。 
To select a positive image, we have the following three options: 
**正の画像を選択するために、次の3つのオプション**があります：

- Use human judgment 
  - 人間の判断を使用する
- Use interactions such as user clicks as a proxy for similarity 
  - ユーザーのクリックなどのインタラクションを類似性の代理として使用する
- Artificially create a similar image from the query image, known as self-supervision 
  - クエリ画像から類似画像を人工的に作成する（自己教師ありとして知られています）

Let’s evaluate each option. 
それぞれのオプションを評価してみましょう。 

##### Use human judgment 人間の判断を使用する

This approach relies on human contractors manually finding similar images. 
このアプローチは、人間の契約者が手動で類似画像を見つけることに依存しています。 
Human involvement produces accurate training data, but using human annotators is expensive and time-consuming. 
人間の関与は正確なトレーニングデータを生成しますが、人間のアノテーターを使用することは高価で時間がかかります。 

##### Use interactions such as user clicks as a proxy for similarity ユーザーのクリックなどのインタラクションを類似性の代理として使用する

In this approach, we measure similarity based on interaction data. 
このアプローチでは、インタラクションデータに基づいて類似性を測定します。 
As an example, when a user clicks on an image, the clicked image is considered to be similar to the query image q. 
例えば、ユーザーが画像をクリックすると、クリックされた画像はクエリ画像qに類似していると見なされます。 
This approach does not require manual work and can generate training data automatically. 
このアプローチは手動作業を必要とせず、トレーニングデータを自動的に生成できます。 
However, the click signal is usually very noisy. 
しかし、クリック信号は通常非常にノイズが多いです。 
Users sometimes click on images even when the image is not similar to the query image. 
ユーザーは、画像がクエリ画像に類似していない場合でも、画像をクリックすることがあります。 
Additionally, this data is very sparse, and we may not have click data available for lots of the images. 
さらに、このデータは非常にスパースであり、多くの画像に対してクリックデータが利用できない場合があります。 
The use of noisy and sparse training data leads to poor performance. 
ノイズの多いスパースなトレーニングデータの使用は、パフォーマンスの低下を引き起こします。 

##### Artificially create a similar image from the query image, known as self-supervision クエリ画像から類似画像を人工的に作成する（自己教師ありとして知られています）

(これは結構画像タスク固有の方法だな...!:thinking:)

In this approach, we artificially create a similar image from the query image. 
このアプローチでは、クエリ画像から類似画像を人工的に作成します。 
For example, we can augment the query image by rotating it and using the newly generated image as a similar image. 
例えば、クエリ画像を回転させて新たに生成された画像を類似画像として使用することで、クエリ画像を拡張できます。 
Recently developed frameworks such as SimCLR [7] and MoCo [8] use the same approach. 
最近開発されたSimCLR [7]やMoCo [8]などのフレームワークも同様のアプローチを使用しています。 
An advantage of this method is that no manual work is required. 
この方法の利点は、手動作業が不要であることです。 

We can implement simple data augmentation logic to create similar images. 
類似画像を作成するために、シンプルなデータ拡張ロジックを実装できます。 
In addition, the constructed training data is not noisy, since augmenting an image always results in a similar image. 
さらに、画像を拡張することで常に類似画像が得られるため、構築されたトレーニングデータはノイズがありません。 
The major drawback of this approach is that the constructed training data differs from the real data. 
このアプローチの主な欠点は、構築されたトレーニングデータが実データと異なることです。 
In practice, similar images are not augmented versions of the query image; they are visually and semantically similar, but are distinct. 
実際には、類似画像はクエリ画像の拡張版ではなく、視覚的および意味的に類似していますが、異なります。 

<!-- ここまで読んだ! -->

##### Which approach works best in our case? 私たちの場合、どのアプローチが最適ですか？

In an interview setting, it’s critical you propose various options and discuss their tradeoffs. 
**インタビューの場では、さまざまなオプションを提案し、それらのトレードオフについて議論することが重要**です。 
There is usually not a single best solution that always works. 
通常、常に機能する単一の最良の解決策はありません。 
Here, we use the self-supervision option for two reasons. 
ここでは、自己教師ありオプションを2つの理由で使用します。 

Firstly, there is no upfront cost associated with it, since the process can be automated. 
第一に、このプロセスは自動化できるため、前払いのコストはありません。 
Secondly, various frameworks such as SimCLR [7] have shown promising results when trained on a large dataset. 
第二に、SimCLR [7]などのさまざまなフレームワークは、大規模データセットでトレーニングされたときに有望な結果を示しています。
Since we have access to billions of images on the platform, this approach might be a good fit. 
プラットフォーム上で数十億の画像にアクセスできるため、このアプローチは適しているかもしれません。 

We can always switch to other labeling methods if the experiment results are unsatisfactory. 
**実験結果が満足できない場合は、他のラベリング方法に切り替えることができます**。 
For example, we can start with the self-supervision option and later use click data for labeling. 
例えば、自己監視オプションから始めて、後でクリックデータをラベリングに使用することができます。 
We can also combine the options. 
オプションを組み合わせることもできます。 
For example, we may use clicks to build our initial training data and rely on human annotators to identify and remove noisy data points. 
例えば、クリックを使用して初期トレーニングデータを構築し、人間のアノテーターにノイズの多いデータポイントを特定して削除させることができます。 
Discussing different options and trade-offs with the interviewer is critical to make good design decisions. 
**インタビュアーとさまざまなオプションやトレードオフについて議論することは、良い設計決定を下すために重要です**。 
Once we construct the dataset, it’s time to train the model using a proper loss function. 
データセットを構築したら、適切な損失関数を使用してモデルをトレーニングする時です。 

<!-- ここまで読んだ! -->

#### Choosing the loss function 損失関数の選択

As Figure 2.9 shows, the model takes images as input and produces an embedding for each input image. 
図2.9が示すように、モデルは画像を入力として受け取り、各入力画像の埋め込みを生成します。Ex{E_x}Ex denotes the embedding of the image xxx. 
Ex{E_x}Exは画像xxxの埋め込みを示します。

![]()

The goal of the training is to optimize the model parameters so that similar images have embeddings close to each other in the embedding space. 
トレーニングの目標は、類似の画像が埋め込み空間で互いに近い埋め込みを持つようにモデルのパラメータを最適化することです。As Figure 2.10 shows, the positive image and the query image should become closer during training. 
図2.10が示すように、ポジティブ画像とクエリ画像はトレーニング中に近づくべきです。

![Figure 2.10: Input images mapped into the embedding space]()

To achieve this goal, we need to use a loss function to measure the quality of the produced embeddings.
この目標を達成するためには、**生成された埋め込みの質を測定するために損失関数を使用する必要があります。**Different loss functions are designed for contrastive training, and interviewers don’t usually expect you to hold an in-depth discussion. 
異なる損失関数は対照学習のために設計されており、**面接官は通常、詳細な議論を期待していません。**しかし、対比損失関数がどのように機能するかについての高レベルの理解を持つことは重要です。

We are going to briefly discuss how a simplified contrastive loss operates. 
ここでは、簡略化されたcontrastive lossがどのように機能するかを簡単に説明します。If you are interested in learning more about contrastive losses, refer to [9]. 
contrastive lossについてさらに学びたい場合は、[9]を参照してください。

![]()

As Figure 2.11 shows, we compute the contrastive loss in three steps. 
図2.11が示すように、対比損失は3つのステップで計算します。



###### Compute similarities. 

First, we compute the similarities between the query image and the embeddings of other images. 
類似性の計算。まず、クエリ画像と他の画像の埋め込みとの類似性を計算します。Dot product [10] and cosine similarity [11] are widely used to measure the similarity between points in the embedding space. 
ドット積[10]とコサイン類似度[11]は、埋め込み空間内の点間の類似性を測定するために広く使用されています。Euclidean distance [12] can also measure the similarity. 
ユークリッド距離[12]も類似性を測定できます。しかし, Euclidean distance usually performs poorly in high dimensions because of the curse of dimensionality [13]. 
しかし、ユークリッド距離は次元の呪い[13]のために高次元では通常、パフォーマンスが悪くなります。To learn more about the curse of dimensionality issues, read [14]. 
次元の呪いの問題について詳しく学ぶには、[14]を読んでください。

###### Softmax. 

A softmax function is applied over the computed distances. 
ソフトマックス。計算された距離に対してソフトマックス関数が適用されます。This ensures the values sum up to one, which allows the values to be interpreted as probabilities. 
これにより、値の合計が1になることが保証され、値を確率として解釈できるようになります。

###### Cross-entropy.

Cross-entropy [15] measures how close the predicted probabilities are to the ground truth labels. 
クロスエントロピー。クロスエントロピー[15]は、予測された確率が真のラベルにどれだけ近いかを測定します。When the predicted probabilities are close to the ground truth, it shows that the embeddings are good enough to distinguish the positive image from the negative ones. 
予測された確率が真のラベルに近いとき、埋め込みがポジティブ画像とネガティブ画像を区別するのに十分良いことを示しています。

<!-- ここまで読んだ! -->

In the interview, you can also discuss the possibility of using a pre-trained model. 
**面接では、事前にトレーニングされたモデルを使用する可能性についても議論できます**。For example, we could leverage a pre-trained contrastive model and fine-tune it using the training data. 
例えば、事前にトレーニングされた対比モデルを活用し、トレーニングデータを使用して微調整することができます。These pre-trained models have already been trained on large datasets, and therefore they have learned good image representations. 
これらの事前トレーニングされたモデルはすでに大規模なデータセットでトレーニングされているため、良好な画像表現を学習しています。This significantly reduces the training time compared to training a model from scratch. 
これにより、ゼロからモデルをトレーニングするのに比べてトレーニング時間が大幅に短縮されます。

<!-- ここまで読んだ! -->

### Evaluation 評価

After we develop the model, we can discuss the evaluation. 
モデルを開発した後、評価について議論することができます。
In this section, we cover important metrics for offline and online evaluations.
このセクションでは、オフラインおよびオンライン評価のための重要な指標について説明します。

#### Offline metrics オフラインメトリクス

Based on the given requirements, an evaluation dataset is available for offline evaluation. 
与えられた要件に基づいて、オフライン評価のための評価データセットが利用可能です。
Let’s assume each data point has a query image, a few candidate images, and a similarity score for each candidate image and the query image pair. 
各データポイントには、クエリ画像、いくつかの候補画像、および各候補画像とクエリ画像のペアに対する類似度スコアがあると仮定しましょう。
A similarity score is an integer number between 000 to 555, where 000 indicates no similarity and 555 indicates two images are visually and semantically very similar. 
類似度スコアは、0から5の間の整数であり、0は類似性がないことを示し、5は2つの画像が視覚的および意味的に非常に類似していることを示します。
For each data point in the evaluation dataset, we compare the ranking produced by the model with the ideal ranking, based on the ground truth scores. 
**評価データセット内の各データポイントについて、私たちはモデルによって生成されたランキングを、真のスコアに基づいて理想的なランキングと比較します。**

![Figure 2.12: A data point from the evaluation dataset]()

Now, let’s examine offline metrics that are commonly used in search systems. 
さて、検索システムで一般的に使用されるオフラインメトリクスを見てみましょう。
Note that search, information retrieval, and recommendation systems usually share the same offline metrics. 
**検索、情報検索、および推薦システムは通常、同じオフラインメトリクスを共有することに注意**してください。

- Mean reciprocal rank (MRR) 
  - 平均逆順位（MRR）
- Recall@k 
  - リコール@k
- Precision@k 
  - 精度@k
- Mean average precision (mAP) 
  - 平均平均精度（mAP）
- Normalized discounted cumulative gain (nDCG) 
  - 正規化割引累積ゲイン（nDCG）

##### MRR. 

This metric measures the quality of the model by considering the rank of the first relevant item in each output list produced by the model, and then averaging them. 
MRR。このメトリクスは、モデルによって生成された各出力リストにおける最初の関連アイテムの順位を考慮し、それを平均化することによってモデルの品質を測定します。

The formula is: 
その式は次のとおりです:

$$
MRR = \frac{1}{m} \sum_{i=1}^m \frac{1}{rank_i}
$$

Where $m$ is the total number of output lists and $rank_i$ refers to the rank of the first relevant item in the $i$th output list. 
ここで、$m$は出力リストの総数であり、$rank_i$は$i$番目の**出力リストにおける最初の関連アイテムの順位**を指します。

Figure 2.13 illustrates how this works. 
図2.13は、これがどのように機能するかを示しています。
For each of the 4 ranked lists, we compute the reciprocal rank (RR) and then calculate the average value of the RRs to get the MRR. 
4つのランク付けされたリストのそれぞれについて、逆順位（RR）を計算し、次にRRの平均値を計算してMRRを得ます。

![Figure 2.13: MRR calculation example]()

Let’s examine the shortcoming of this metric. 
このメトリクスの欠点を見てみましょう。
Since MRR considers only the first relevant item and ignores other relevant items in the list, it does not measure the precision and ranking quality of a ranked list. 
**MRRは最初の関連アイテムのみを考慮**し、リスト内の他の関連アイテムを無視するため、ランク付けされたリストの精度とランキングの質を測定しません。
For example, Figure 2.14 shows the outputs of two different models. 
例えば、図2.14は2つの異なるモデルの出力を示しています。
The output of model 1 has 3 relevant items, while the output of model 2 has 1 relevant item. 
モデル1の出力には3つの関連アイテムがあり、モデル2の出力には1つの関連アイテムがあります。
However, the reciprocal rank of both models is 0.5. 
しかし、両方のモデルの逆順位は0.5です。
Given this shortcoming, we will not use this metric. 
この欠点を考慮して、私たちはこのメトリクスを使用しません。

![Figure 2.14: MRR of two different models]()

##### Recall@k. 

This metric measures the ratio between the number of relevant items in the output list and the total number of relevant items available in the entire dataset. 
Recall@k。このメトリクスは、出力リスト内の関連アイテムの数と、全データセットで利用可能な関連アイテムの総数との比率を測定します。

The formula is: 
その式は次のとおりです：

$$
\text{recall@k} = \frac{\text{number of relevant items among the top } k \text{ items in the output list}}{\text{total relevant items}}
$$

Even though recall@k measures how many relevant items the model failed to include in the output list, this isn’t always a good metric. 
**Recall@kは、モデルが出力リストに含められなかった関連アイテムの数を測定**しますが、これは必ずしも良いメトリクスではありません。
Let’s understand why not. 
なぜそうでないのかを理解しましょう。
In some systems, such as search engines, the total number of relevant items can be very high. 
**検索エンジンなどの一部のシステムでは、関連アイテムの総数が非常に多くなる可能性があります**。
This negatively affects the recall as the denominator is very large. 
これは、分母が非常に大きいため、リコールに悪影響を及ぼします。
For example, when the query image is an image of a dog, the database may contain millions of dog images. 
例えば、クエリ画像が犬の画像である場合、データベースには数百万の犬の画像が含まれている可能性があります。
The goal is not to return every dog image but to retrieve a handful of the most similar dog images. 
目標はすべての犬の画像を返すことではなく、最も類似した犬の画像をいくつか取得することです。

Given recall@k doesn’t measure the ranking quality of the model, we will not use it. 
Recall@kはモデルのランキングの質を測定しないため、私たちはそれを使用しません。

<!-- ここまで読んだ! -->

##### Precision@k. 

This metric measures the proportion of relevant items among the top k items in the output list. 
Precision@k。このメトリクスは、出力リストの上位kアイテムの中の関連アイテムの割合を測定します。
The formula is: 
その式は次のとおりです：

$$
\text{precision@k} = \frac{\text{number of relevant items among the top } k \text{ items in the output list}}{k}
$$

This metric measures how precise the output lists are, but it doesn’t consider the ranking quality. 
**このメトリクスは出力リストの精度を測定しますが、ランキングの質は考慮しません**。(順序を考慮しない、って話ね!:thinking:)
For example, in Figure 2.15, if we rank more relevant items higher in the list, the precision won’t change. 
例えば、図2.15では、より関連性の高いアイテムをリストの上位にランク付けしても、精度は変わりません。
This metric is not ideal for our use case, since we need to measure both the precision and ranking quality of the results. 
このメトリクスは、結果の精度とランキングの質の両方を測定する必要があるため、私たちの使用ケースには理想的ではありません。

![Figure 2.15: Precision@5 of two different models]()

##### mAP.

This metric first computes the average precision (AP) for each output list, and then averages AP values. 
mAP。このメトリクスは、最初に各出力リストの平均精度（AP）を計算し、次にAP値を平均化します。

Let’s first understand what AP is. 
まず、APが何であるかを理解しましょう。
It takes a list of k items, such as images, and averages the precision@k at different values of k. 
それは、画像などのkアイテムのリストを取り、異なるkの値でprecision@kを平均化します。
AP is high if more relevant items are located at the top of the list. 
**APは、より多くの関連アイテムがリストの上部に位置する場合に高くなります**。
For a list of size k, the AP formula is: 
サイズkのリストの場合、APの式は次のとおりです：

$$
AP = \frac{\sum_{i=1}^k \text{Precision@}i \text{ if } i\text{'th item is relevant to the user}}{\text{total relevant items}}
$$

Let’s look at an example to better understand the metric. 
このメトリクスをよりよく理解するために、例を見てみましょう。
Figure 2.16 shows AP calculations for each of the 4 output lists produced by the model. 
図2.16は、モデルによって生成された4つの出力リストそれぞれのAP計算を示しています。

![Figure 2.16: mAP calculations]()

Since we average precisions, the overall ranking quality of the list is considered. 
私たちは精度を平均化するため、リストの全体的なランキングの質が考慮されます。
However, mAP is designed for binary relevances; in other words, it works well when each item is either relevant or irrelevant. 
**しかし、mAPはバイナリの関連性のために設計されています。言い換えれば、各アイテムが関連しているか無関係である場合にうまく機能します。**
For continuous relevance scores, nDCG is a better choice. 
**連続的な関連スコアの場合、nDCGがより良い選択です。**
(あ、mAPとnDCGの使い分けってこの観点でいいのか...!:thinking:)

##### nDCG. 

This metric measures the ranking quality of an output list and shows how good the ranking is, compared to the ideal ranking. 
nDCG。このメトリクスは**出力リストのランキングの質を測定し、理想的なランキングと比較してランキングがどれほど良いかを示します。**
First, let’s explain DCG and then discuss nDCG. 
まず、DCGを説明し、その後nDCGについて説明します。

###### What is DCG? DCGとは何ですか？

DCG calculates the cumulative gain of items in a list by summing up the relevance score of each item. 
DCGは、リスト内のアイテムの累積ゲインを計算し、各アイテムの関連スコアを合計します。
Then the score is accumulated from the top of the output list to the bottom, with the score of each result discounted at lower ranks. 
次に、スコアは出力リストの上部から下部に向かって累積され、各結果のスコアは低い順位で割引されます。
The formula is: 
その式は次のとおりです：

$$
DCG_p = \sum_{i=1}^p \frac{rel_i}{\log_2(i+1)}
$$

Where $rel_i$ is the ground truth relevance score of the image ranked at location $i$. 
ここで、$rel_i$ は位置 $i$ にランク付けされた画像の**真の関連スコア**です。(ここが連続値でもOKってことか。mAPと異なり...!:thinking:)

###### What is nDCG? nDCGとは何ですか？

Because DCG sums up the relevance scores of items and discounts their positions, the result of DCG could be any value. 
DCGはアイテムの関連スコアを合計し、その位置を割引するため、**DCGの結果は任意の値になる可能性**があります。(定義されたrelevance scoreのスケールに依存する、ってことか...!:thinking:)
In order to get a more meaningful score, we need to normalize DCG. 
**より意味のあるスコアを得るために、DCGを正規化**する必要があります。
For this, nDCG divides the DCG by the DCG of an ideal ranking. 
これには、nDCGが**理想的なランキングのDCGでDCGを割る**ことが必要です。
The formula is: 
その式は次のとおりです：

$$
nDCG_p = \frac{DCG_p}{IDCG_p}
$$

Where $IDCG_p$ is the DCG of the ideal ranking (a ranking ordered by the relevance scores of items). 
ここで、$IDCG_p$は理想的なランキングのDCG（アイテムの関連スコアによって順序付けられたランキング）です。
Note that in a perfect ranking system, the DCG is equal to IDCG. 
**完璧なランキングシステムでは、DCGはIDCGに等しい**ことに注意してください。

Let’s use an example to better understand nDCG. 
nDCGをよりよく理解するために、例を使いましょう。
In Figure 2.17, we can see a list of output images and their associated ground truth relevance scores produced by a search system. 
図2.17では、検索システムによって生成された出力画像のリストとそれに関連する真の関連スコアを見ることができます。

![Figure 2.17: A ranked list produced by a search system]()
(**各アイテムについて、関連度スコアが非binaryで与えられてる**状況...!:thinking:)

We can compute nDCG in 3 steps: 
nDCGは3つのステップで計算できます:

1. Compute DCG 
   1. DCGを計算する

2. Compute IDCG 
   1. IDCGを計算する

3. Divide DCG by IDCG 
   1. DCGをIDCGで割る

Compute DCG: The DCG for the current ranking produced by the model is: 
DCGを計算する：モデルによって生成された現在のランキングのDCGは次のとおりです：

$$
DCG_p = \sum_{i=1}^p \frac{rel_i}{\log_2(i+1)} = \frac{0}{\log_2(2)} + \frac{5}{\log_2(3)} + \frac{1}{\log_2(4)} + \frac{4}{\log_2(5)} + \frac{2}{\log_2(6)} = 6.151
$$

Compute IDCG: The ideal ranking calculation is the same as the DCG calculation, except that it recommends the most relevant items first (Figure 2.18). 
IDCGを計算する：理想的なランキングの計算はDCGの計算と同じですが、最も関連性の高いアイテムを最初に推奨します（図2.18）。

![Figure 2.18: Ideal ranking list]()

The IDCG for the ideal ranking is: 
理想的なランキングのIDCGは次のとおりです：

$$
IDCG_p = \sum_{i=1}^{\nu} \frac{rel_i}{\log_2(i+1)} = \frac{5}{\log_2(2)} + \frac{4}{\log_2(3)} + \frac{2}{\log_2(4)} + \frac{1}{\log_2(5)} + \frac{0}{\log_2(6)} = 8.9543
$$

Divide DCG by IDCG: 
DCGをIDCGで割る：

$$
nDCG_p = \frac{DCG_p}{IDCG_p} = \frac{6.151}{8.9543} = 0.6869
$$

nDCG works well most times. 
**nDCGはほとんどの場合うまく機能します。**
Its primary shortcoming is that deriving ground truth relevance scores is not always possible. 
**その主な欠点は、真の関連スコアを導出することが常に可能であるとは限らないこと**です。(じゃあ基本的にnDCG、関連スコアor報酬がbinaryだったらmAPでもいい、みたいなことかな...!:thinking:)
In our case, since the evaluation dataset contains similarity scores, we can use nDCG to measure the performance of the model during the offline evaluation. 
私たちのケースでは、評価データセットに類似度スコアが含まれているため、オフライン評価中にモデルのパフォーマンスを測定するためにnDCGを使用できます。

<!-- ここまで読んだ! -->

#### Online metrics オンライン指標

In this section, we explore a few commonly used online metrics for measuring how quickly users can discover images they like.
このセクションでは、ユーザーが好む画像をどれだけ早く発見できるかを測定するために一般的に使用されるいくつかのオンライン指標を探ります。

##### Click-through rate (CTR). 

This metric shows how often users click on the displayed items. 
クリック率（CTR）。この指標は、ユーザーが表示されたアイテムをどれだけ頻繁にクリックするかを示します。
CTR can be calculated using the following formula:
CTRは次の式を使用して計算できます：

$$
\mathrm{CTR}= \frac{\text { Number of clicked images }}{\text { Total number of suggested images }}
$$

A high CTR indicates that users click on the displayed items often. 
高いCTRは、ユーザーが表示されたアイテムを頻繁にクリックすることを示します。
CTR is commonly used as an online metric in search and recommendation systems, as we will see in later chapters.
**CTRは、検索および推薦システムにおけるオンライン指標として一般的に使用されており、後の章で詳しく見ていきます**。

##### Average daily, weekly, and monthly time spent on the suggested images.  提案された画像に費やされる平均日次、週次、月次の時間。

This metric shows how engaged users are with the suggested images. 
この指標は、ユーザーが提案された画像にどれだけ関与しているかを示します。
When the search system is accurate, we expect this metric to increase.
検索システムが正確である場合、この指標が増加することを期待します。

<!-- ここまで読んだ! -->

### Serving サービング

At serving time, the system returns a ranked list of similar images based on a query image. 
サービング時に、システムはクエリ画像に基づいて類似画像のランク付けされたリストを返します。
Figure 2.19 shows the prediction pipeline and an indexing pipeline. 
図2.19は、予測パイプライン(=基本リアルタイム?) とインデックスパイプライン(=基本バッチ or ストリーミング??)を示しています。
Let’s look closer at each pipeline. 
それぞれのパイプラインを詳しく見てみましょう。

![Figure 2.19: Prediction and indexing pipeline]()

#### Prediction pipeline 予測パイプライン

##### Embedding generation service 埋め込み生成サービス  

This service computes the embedding of the input query image.  
このサービスは、入力クエリ画像の埋め込みを計算します。  
As Figure 2.20 shows, it preprocesses the image and uses the trained model to determine the embedding.  
図2.20に示すように、画像を前処理し、訓練されたモデルを使用して埋め込みを決定します。

![Figure 2.20: Embedding generation service]()

##### Nearest neighbor service 最近傍サービス

Once we get the embedding of the query image, we need to retrieve similar images from the embedding space.
クエリ画像の埋め込みを取得したら、埋め込み空間から類似の画像を取得する必要があります。 
The nearest neighbor service does this.
最近傍サービスはこれを行います。

Let’s define the nearest neighbor search more formally. 
最近傍検索をより正式に定義しましょう。 
Given a query point “q” and a set of other points S, it finds the closest points to “q” in set S. 
クエリポイント「q」と他のポイントの集合Sが与えられたとき、集合S内の「q」に最も近いポイントを見つけます。 
Note that an image embedding is a point in $N$-dimensional space, where $N$ is the size of the embedding vector. 
画像の埋め込みは、埋め込みベクトルのサイズである$N$次元空間の点であることに注意してください。 
Figure 2.21 shows the top 3 nearest neighbors of image q. 
図2.21は、画像qの上位3つの最近傍を示しています。 
We denote the query image as q, and other images as $x_1, x_2, \ldots, x_k$. 
クエリ画像をqとし、他の画像を$x_1, x_2, \ldots, x_k$と表します。

![Figure 2.21: Top 3 nearest neighbors to image q in the embedding space]()

##### Re-ranking service 再ランキングサービス

This service incorporates business-level logic and policies. 
**このサービスは、ビジネスレベルのロジックとポリシーを組み込んでいます。**
For example, it filters inappropriate results, ensures we don’t include private images, removes duplicates or near-duplicate results, and enforces other similar logic before displaying the final results to the user.
例えば、不適切な結果をフィルタリングし、プライベートな画像を含まないようにし、重複やほぼ重複する結果を削除し、最終結果をユーザに表示する前に他の類似のロジックを適用します。

<!-- ここまで読んだ! -->

#### Indexing pipeline インデクシングパイプライン  
##### Indexing service インデクシングサービス

All images on the platform are indexed by this service to improve search performance.  
プラットフォーム上のすべての画像は、このサービスによってインデックスされ、検索性能が向上します。

Another responsibility of the indexing service is to keep the index table updated.  
**インデクシングサービスのもう一つの責任は、インデックステーブルを最新の状態に保つこと**です。
For example, when a creator adds a new image to the platform, the service indexes the embedding of the new image to make it discoverable by the nearest neighbor search.  
例えば、クリエイターがプラットフォームに新しい画像を追加すると、サービスは新しい画像の埋め込みをインデックスし、最近傍探索によって発見可能にします。

Indexing increases memory usage because we store the embeddings of the entire images in an index table.  
インデクシングは、インデックステーブルに全画像の埋め込みを保存するため、メモリ使用量が増加します。
Various optimizations are available to reduce memory usages, such as vector quantization [16] and product quantization [17].  
メモリ使用量を削減するためのさまざまな最適化手法が利用可能であり、例えばベクトル量子化 [16] やプロダクト量子化 [17] があります。
(埋め込み表現を軽くするって話か.!:thinking:)

<!-- ここまで読んだ! -->

#### Performance of nearest neighbor (NN) algorithms 最近傍法（NN）アルゴリズムの性能

Nearest neighbor search is a core component of information retrieval, search, and recommendation systems. 
最近傍検索は、情報検索、検索、および推薦システムのコアコンポーネントです。
A slight improvement in its efficiency leads to significant overall performance improvement. 
**その効率のわずかな改善は、全体的な性能の大幅な向上につながります。**(レイテンシーの話??:thinking:)
Given how critical this component is, the interviewer may want you to deep dive into this topic. 
このコンポーネントがいかに重要であるかを考えると、面接官はこのトピックについて深く掘り下げることを望むかもしれません。

NN algorithms can be divided into two categories: exact and approximate. 
**NNアルゴリズムは、正確なものと近似的なものの2つのカテゴリに分けることができます。**
Let’s examine each in more detail. 
それぞれをより詳しく見ていきましょう。

##### Exact nearest neighbor 正確な最近傍

Exact nearest neighbor, also called linear search, is the simplest form of NN. 
正確な最近傍（Exact nearest neighbor）、または線形探索（linear search）とも呼ばれるものは、NNの最も単純な形です。
It works by searching the entire index table, calculating the distance of each point with the query point q, and retrieving the k nearest points. 
これは、全てのインデックステーブルを検索し、各点とクエリ点$q$との距離を計算し、$k$最近傍点を取得することによって機能します。
The time complexity is $O(N \times D)$, where $N$ is the total number of points and $D$ is the point dimension. 
時間計算量は$O(N \times D)$であり、ここで$N$は点の総数、$D$は点の次元です。

In a large-scale system in which $N$ may easily run into the billions, the linear time complexity is too slow. 
**$N$が数十億に達する可能性のある大規模システムでは、線形時間計算量は遅すぎます**。

<!-- ここまで読んだ! -->

##### Approximate nearest neighbor (ANN) 近似最近傍（ANN）

In many applications, showing users similar enough items is sufficient, and there is no need to perform an exact nearest neighbor search. 
**多くのアプリケーションでは、ユーザに十分に似たアイテムを示すことができれば十分であり、正確な最近傍検索を行う必要はありません。** (確かにANNでいい気がしてきたなぁ...:thinking:)

In ANN algorithms, a particular data structure is used to reduce the time complexity of NN search to sublinear (e.g., $O(D \times \log N)$). 
ANNアルゴリズムでは、NN検索の時間計算量をサブリニア（例えば、$O(D \times \log N)$）に削減するために特定のデータ構造が使用されます。
They usually require up-front preprocessing or additional space. 
通常、これらは事前の前処理や追加のスペースを必要とします。

ANN algorithms can be divided into the following three categories: 
**ANNアルゴリズムは以下の3つのカテゴリ**に分けることができます：

- Tree-based ANN 
  - TreeベースのANN
- Locality-sensitive hashing (LSH)-based ANN 
  - ローカリティ感度ハッシング（LSH）ベースのANN
- Clustering-based ANN 
  - クラスタリングベースのANN

There are various algorithms within each category, and interviewers typically do not expect you to know every detail. 
**各カテゴリ内にはさまざまなアルゴリズムがあり、面接官は通常、すべての詳細を知っていることを期待していません。**
It’s adequate to have a high-level understanding of them. 
**それらについて高レベルの(=抽象度高めの!:thinking:)理解を持っていることが十分**です。
So, let’s briefly cover each category. 
それでは、各カテゴリを簡単に説明しましょう。

<!-- ここまで読んだ! -->

##### Tree-based ANN

Tree-based algorithms form a tree by splitting the space into multiple partitions. 
ツリーベースのアルゴリズムは、**空間を複数のパーティションに分割することによってツリーを形成**します。
Then, they leverage the characteristics of the tree to perform a faster search. 
次に、ツリーの特性を利用して、より高速な検索を行います。

We form the tree by iteratively adding new criteria to each node. 
私たちは、各ノードに新しい基準を反復的に追加することによってツリーを形成します。
For instance, one criterion for the root node can be: gender===male. 
例えば、ルートノードの基準の一つは、gender===male（性別が男性である）です。
This means any point with a female attribute belongs to the left sub-tree. 
これは、女性属性を持つ任意の点が左のサブツリーに属することを意味します。

![]()

In the tree, non-leaf nodes split the space into two partitions given the criterion. 
ツリー内では、非葉ノードが**基準に基づいて空間を2つのパーティションに分割**します。
Leaf nodes indicate a particular region in space. 
葉ノードは、空間内の特定の領域を示します。
Figure 2.23 shows an example of the space divided into 7 regions. 
図2.23は、空間が7つの領域に分割された例を示しています。

The algorithm only searches the partition that the query point belongs to. 
**アルゴリズムは、クエリポイントが属するパーティションのみを検索**します。

![Figure 2.23: Partitioned space by the tree]()

Typical tree-based methods are R-trees [18], Kd-trees [19], and Annoy (Approximate Nearest Neighbor Oh Yeah) [20]. 
典型的なツリーベースの手法には、Rツリー[18]、Kdツリー[19]、およびAnnoy（Approximate Nearest Neighbor Oh Yeah）[20]があります。

<!-- ここまで読んだ! -->

##### Locality sensitive hashing (LSH): 

LSH uses particular hash functions to reduce the dimensions of points and group them into buckets. 
**LSHは特定のハッシュ関数を使用して、ポイントの次元を削減し、それらをバケットにグループ化**します。
These hash functions map points in close proximity to each other into the same bucket. 
これらのハッシュ関数は、近接するポイントを同じバケットにマッピングします。
LSH searches only those points belonging to the same bucket as the query point q. 
LSHは、**クエリポイントqと同じバケットに属するポイントのみを検索**します。
You can learn more about LSH by reading [21]. 
LSHについての詳細は[21]を読むことで学ぶことができます。

##### Clustering-based ANN

These algorithms form clusters by grouping the points based on similarities. 
これらのアルゴリズムは、**類似性に基づいてポイントをグループ化することによってクラスタを形成**します。
Once the clusters are formed, the algorithms search only the subset of points in the cluster to which the query point belongs. 
クラスタが形成されると、**アルゴリズムはクエリポイントが属するクラスタ内のポイントのサブセットのみを検索**します。

<!-- ここまで読んだ! -->

##### Which algorithm should we use? どのアルゴリズムを使用すべきか？

Results from the exact nearest neighbor method are guaranteed to be accurate. 
正確な最近傍法からの結果は、正確であることが保証されています。 
This makes it a good option when we have limited data points, or if it’s required to have the exact nearest neighbors. 
これは、**データポイントが限られている場合や、正確な最近傍が必要な場合に良い選択肢**となります。 (正確な最近傍が必要なケースってのがあんまりないかもなぁ...! 理論的に正確なOPEやOPLがしたい場合??:thinking:)
However, when there are a large number of points, it’s impractical to run the algorithm efficiently. 
しかし、多くのポイントがある場合、アルゴリズムを効率的に実行することは非現実的です。 
In this case, ANN methods are commonly used. 
この場合、ANN（Approximate Nearest Neighbor）法が一般的に使用されます。 
While they may not return the exact points, they are more efficient in finding the nearest points. 
正確なポイントを返さないかもしれませんが、最近傍のポイントを見つけるのにより効率的です。

Given the amount of data available in today’s systems, the ANN method is a more pragmatic solution. 
**今日のシステムで利用可能なデータの量を考えると、ANN法はより実用的な解決策**です。 
In our visual search system, we use ANN to find similar image embeddings. 
私たちの視覚検索システムでは、ANNを使用して類似の画像埋め込みを見つけます。

For an applied ML role, the interviewer may ask you to implement ANN. 
応用機械学習(=MLOpsエンジニア?)の役割では、**面接官がANNを実装するように求めることがあります**。 
Two widely used libraries are Faiss [22] (developed by Meta) and ScaNN [23] (developed by Google). 
広く使用されている2つのライブラリは、Faiss [22]（Metaによって開発）とScaNN [23]（Googleによって開発）です。 
Each supports the majority of methods we have described in this chapter. 
それぞれは、この章で説明したほとんどのメソッドをサポートしています。 
You are encouraged to familiarize yourself with at least one of these libraries to better understand the concepts and to gain the confidence with which to implement the nearest neighbor search in an ML coding interview. 
**これらのライブラリの少なくとも1つに慣れることをお勧めします。そうすることで、概念をよりよく理解し、機械学習のコーディング面接で最近傍検索を実装する自信を得ることができます。**(なるほどね...!:thinking:)

<!-- ここまで読んだ! -->

### Other Talking Points その他の話題

If there is extra time at the end of the interview, you might be asked follow-up questions or challenged to discuss advanced topics, depending on various factors such as the interviewer’s preference, the candidate’s expertise, role requirements, etc. 
インタビューの最後に余裕がある場合、面接官の好み、候補者の専門知識、役割の要件などのさまざまな要因に応じて、フォローアップの質問をされたり、進んだトピックについて議論を求められたりすることがあります。
Some topics to prepare for, especially for senior roles, are listed below. 
特にシニア職のために準備すべきトピックは以下の通りです。

- Moderate content in the system by identifying and blocking inappropriate images [24]. 
  - 不適切な画像を特定してブロックすることによって、システム内のコンテンツを適切に管理します[24]。
- Different biases present in the system, such as positional bias [25][26]. 
  - システム内に存在するさまざまなバイアス、例えば位置バイアスについて[25][26]。
  - (パッと簡単な方法として思いつくのは、カスケードモデルをユーザ行動に仮定して学習したりするとかかなぁ...:thinking:)
- How to use image metadata such as tags to improve search results. This is covered in Chapter 3 Google Street View Blurring System. 
  - タグなどの画像メタデータを使用して検索結果を改善する方法について。これは第3章のGoogle Street View Blurring Systemで説明されています。

- Smart crop using object detection [27]. 
  - オブジェクト検出を使用したスマートクロップについて[27]。

- How to use graph neural networks to learn better representations [28]. 
  - グラフニューラルネットワークを使用してより良い表現を学習する方法について[28]。

- Support the ability to search images by a textual query. We examine this in Chapter 4. 
  - テキストクエリによる画像検索のサポートについて。これについては第4章で検討します。

- How to use active learning [29] or human-in-the-loop [30] ML to annotate data more efficiently. 
  - アクティブラーニング[29]やヒューマン・イン・ザ・ループ[30]の機械学習を使用してデータをより効率的に注釈付け(アノテーション)する方法について。

<!-- ここまで読んだ! -->

### References 参考文献

1. Visual search at pinterest.https://arxiv.org/pdf/1505.07647.pdf.
   Visual search at pinterest. https://arxiv.org/pdf/1505.07647.pdf.
2. Visual embeddings for search at Pinterest.https://medium.com/pinterest-engineering/unifying-visual-embeddings-for-visual-search-at-pinterest-74ea7ea103f0.
   Pinterestにおける検索のための視覚埋め込み。 https://medium.com/pinterest-engineering/unifying-visual-embeddings-for-visual-search-at-pinterest-74ea7ea103f0.
3. Representation learning.https://en.wikipedia.org/wiki/Feature_learning.
   表現学習。 https://en.wikipedia.org/wiki/Feature_learning.
4. ResNet paper.https://arxiv.org/pdf/1512.03385.pdf.
   ResNet論文。 https://arxiv.org/pdf/1512.03385.pdf.
5. Transformer paper.https://arxiv.org/pdf/1706.03762.pdf.
   Transformer論文。 https://arxiv.org/pdf/1706.03762.pdf.
6. Vision Transformer paper.https://arxiv.org/pdf/2010.11929.pdf.
   Vision Transformer論文。 https://arxiv.org/pdf/2010.11929.pdf.
7. SimCLR paper.https://arxiv.org/pdf/2002.05709.pdf.
   SimCLR論文。 https://arxiv.org/pdf/2002.05709.pdf.
8. MoCo paper.
   MoCo論文。
9. Contrastive representation learning methods.https://lilianweng.github.io/posts/2019-11-10-self-supervised/.
   対照的表現学習手法。 https://lilianweng.github.io/posts/2019-11-10-self-supervised/.
10. Dot product.https://en.wikipedia.org/wiki/Dot_product.
    内積。 https://en.wikipedia.org/wiki/Dot_product.
11. Cosine similarity.https://en.wikipedia.org/wiki/Cosine_similarity.
    コサイン類似度。 https://en.wikipedia.org/wiki/Cosine_similarity.
12. Euclidean distance.https://en.wikipedia.org/wiki/Euclidean_distance.
    ユークリッド距離。 https://en.wikipedia.org/wiki/Euclidean_distance.
13. Curse of dimensionality.https://en.wikipedia.org/wiki/Curse_of_dimensionality.
    次元の呪い。 https://en.wikipedia.org/wiki/Curse_of_dimensionality.
14. Curse of dimensionality issues in ML.https://www.mygreatlearning.com/blog/understanding-curse-of-dimensionality/.
    MLにおける次元の呪いの問題。 https://www.mygreatlearning.com/blog/understanding-curse-of-dimensionality/.
15. Cross-entropy loss.https://en.wikipedia.org/wiki/Cross_entropy.
    クロスエントロピー損失。 https://en.wikipedia.org/wiki/Cross_entropy.
16. Vector quantization.http://ws.binghamton.edu/fowler/fowler%20personal%20page/EE523_files/Ch_10_1%20VQ%20Description%20(PPT).pdf.
    ベクトル量子化。 http://ws.binghamton.edu/fowler/fowler%20personal%20page/EE523_files/Ch_10_1%20VQ%20Description%20(PPT).pdf.
17. Product quantization.https://towardsdatascience.com/product-quantization-for-similarity-search-2f1f67c5fddd.
    製品量子化。 https://towardsdatascience.com/product-quantization-for-similarity-search-2f1f67c5fddd.
18. R-Trees.https://en.wikipedia.org/wiki/R-tree.
    Rツリー。 https://en.wikipedia.org/wiki/R-tree.
19. KD-Tree.https://kanoki.org/2020/08/05/find-nearest-neighbor-using-kd-tree/.
    KDツリー。 https://kanoki.org/2020/08/05/find-nearest-neighbor-using-kd-tree/.
20. Annoy.https://towardsdatascience.com/comprehensive-guide-to-approximate-nearest-neighbors-algorithms-8b94f057d6b6.
    Annoy。 https://towardsdatascience.com/comprehensive-guide-to-approximate-nearest-neighbors-algorithms-8b94f057d6b6.
21. Locality-sensitive hashing.https://web.stanford.edu/class/cs246/slides/03-lsh.pdf.
    ローカリティ感度ハッシュ。 https://web.stanford.edu/class/cs246/slides/03-lsh.pdf.
22. Faiss library.https://github.com/facebookresearch/faiss/wiki.
    Faissライブラリ。 https://github.com/facebookresearch/faiss/wiki.
23. ScaNN library.https://github.com/google-research/google-research/tree/master/scann.
    ScaNNライブラリ。 https://github.com/google-research/google-research/tree/master/scann.
24. Content moderation with ML.https://appen.com/blog/content-moderation/.
    MLによるコンテンツモデレーション。 https://appen.com/blog/content-moderation/.
25. Bias in AI and recommendation systems.https://www.searchenginejournal.com/biases-search-recommender-systems/339319/#close.
    AIと推薦システムにおけるバイアス。 https://www.searchenginejournal.com/biases-search-recommender-systems/339319/#close.
26. Positional bias.https://eugeneyan.com/writing/position-bias/.
    位置バイアス。 https://eugeneyan.com/writing/position-bias/.
27. Smart crop.https://blog.twitter.com/engineering/en_us/topics/infrastructure/2018/Smart-Auto-Cropping-of-Images.
    スマートクロップ。 https://blog.twitter.com/engineering/en_us/topics/infrastructure/2018/Smart-Auto-Cropping-of-Images.
28. Better search with gnns.https://arxiv.org/pdf/2010.01666.pdf.
    GNNを用いたより良い検索。 https://arxiv.org/pdf/2010.01666.pdf.
29. Active learning.https://en.wikipedia.org/wiki/Active_learning_(machine_learning).
    アクティブラーニング。 https://en.wikipedia.org/wiki/Active_learning_(machine_learning).
30. Human-in-the-loop ML.https://arxiv.org/pdf/2108.00941.pdf.
    ヒューマン・イン・ザ・ループML。 https://arxiv.org/pdf/2108.00941.pdf.


