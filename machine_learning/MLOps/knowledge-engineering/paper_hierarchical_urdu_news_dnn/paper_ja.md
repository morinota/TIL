refs: https://arxiv.org/pdf/2107.03141


## Hierarchical Text Classification of Urdu News using Deep Neural Network
## ウルドゥー語ニュースの階層的テキスト分類に関する深層ニューラルネットワークの使用

### TAIMOOR AHMED JAVED[∗], National University of Computer and Emerging Sciences, Islamabad, Pakistan 
### WASEEM SHAHZAD, National University of Computer and Emerging Sciences, Islamabad, Pakistan 
### UMAIR ARSHAD, National University of Computer and Emerging Sciences, Islamabad, Pakistan
### TAIMOOR AHMED JAVED[∗], パキスタン、イスラマバードのコンピュータおよび新興科学大学 
### WASEEM SHAHZAD, パキスタン、イスラマバードのコンピュータおよび新興科学大学 
### UMAIR ARSHAD, パキスタン、イスラマバードのコンピュータおよび新興科学大学

Digital text is increasing day by day on the internet. 
デジタルテキストは、インターネット上で日々増加しています。

It is very challenging to classify a large and heterogeneous collection of data, which require improved information processing methods to organize text. 
大規模で異種のデータコレクションを分類することは非常に困難であり、テキストを整理するためには改善された情報処理方法が必要です。

To classify large size of corpus, one common approach is to use hierarchical text classification, which aims to classify textual data in a hierarchical structure. 
大規模なコーパスを分類するための一般的なアプローチの一つは、階層的テキスト分類を使用することであり、これはテキストデータを階層構造で分類することを目的としています。

Several approaches have been proposed to tackle classification of text but most of the research has been done on English language. 
テキストの分類に対処するためにいくつかのアプローチが提案されていますが、ほとんどの研究は英語に関して行われています。

This paper proposes a deep learning model for hierarchical text classification of news in Urdu language - consisting of 51,325 sentences from 8 online news websites belonging to the following genres: Sports; Technology; and Entertainment. 
本論文では、ウルドゥー語のニュースの階層的テキスト分類のための深層学習モデルを提案します - これは、スポーツ、技術、エンターテインメントというジャンルに属する8つのオンラインニュースウェブサイトからの51,325文で構成されています。

The objectives of this paper are twofold: 
本論文の目的は二つあります：

(1) to develop a large human-annotated dataset of news in Urdu language for hierarchical text classification; 
(1) 階層的テキスト分類のためのウルドゥー語ニュースの大規模な人手注釈データセットを開発すること；

and (2) to classify Urdu news hierarchically using our proposed model based on LSTM mechanism named as Hierarchical Multi-layer LSTMs (HMLSTM). 
(2) Hierarchical Multi-layer LSTMs (HMLSTM)と呼ばれるLSTMメカニズムに基づいて、提案したモデルを使用してウルドゥー語ニュースを階層的に分類することです。

Our model consists of two modules: 
私たちのモデルは二つのモジュールで構成されています：

Text Representing Layer, for obtaining text representation in which we use Word2vec embedding to transform the words to vector 
テキスト表現層は、テキスト表現を取得するためのもので、Word2vec埋め込みを使用して単語をベクトルに変換します。

and Urdu Hierarchical LSTM Layer (UHLSTML) an end-to-end fully connected deep LSTMs network to perform automatic feature learning, 
ウルドゥー階層LSTM層（UHLSTML）は、特徴学習を自動的に行うためのエンドツーエンドの完全接続深層LSTMネットワークです。

we train one LSTM layer for each level of the class hierarchy. 
クラス階層の各レベルに対して1つのLSTM層を訓練します。

We have performed extensive experiments on our self created dataset named as Urdu News Dataset for Hierarchical Text Classification (UNDHTC). 
私たちは、ウルドゥー語ニュースの階層的テキスト分類のために作成したデータセット（UNDHTC）で広範な実験を行いました。

The result shows that our proposed method is very effective for hierarchical text classification and it outperforms baseline methods significantly and also achieved good results as compare to deep neural model. 
結果は、私たちの提案した方法が階層的テキスト分類に非常に効果的であり、ベースライン手法を大幅に上回り、深層ニューラルモデルと比較しても良好な結果を達成したことを示しています。

CCS Concepts: 
CCS概念：

• Computing methodologies → **Neural networks; Natural language processing; Super-** **vised learning; 
• 情報システム →** _Clustering and classification._

Additional Key Words and Phrases: 
追加のキーワードとフレーズ：

Hierarchical Urdu Text Classification,Natural language processing, Deep Neural Network, Urdu News Dataset
階層的ウルドゥー語テキスト分類、自然言語処理、深層ニューラルネットワーク、ウルドゥー語ニュースデータセット

**ACM Reference Format:** 
**ACM参照形式：**

Taimoor Ahmed Javed, Waseem Shahzad, and Umair Arshad. 2021. Hierarchical Text Classification of Urdu News using Deep Neural Network. 
Taimoor Ahmed Javed, Waseem Shahzad、およびUmair Arshad. 2021. 深層ニューラルネットワークを使用したウルドゥー語ニュースの階層的テキスト分類。

ACM Trans. Asian Low-Resour. Lang. Inf. Process. 37, 4, Article 111 (August 2021), 22 pages. 
ACM Trans. Asian Low-Resour. Lang. Inf. Process. 37, 4, Article 111 (2021年8月)、22ページ。

https://doi.org/10.1145/1122445.1122456
https://doi.org/10.1145/1122445.1122456



## 1 INTRODUCTION 1. はじめに

Nowadays, electronic information extraction systems are omnipresent, from instant mobile messaging apps to automated archives having millions of data. 
今日、電子情報抽出システムは、インスタントモバイルメッセージングアプリから数百万のデータを持つ自動アーカイブに至るまで、至る所に存在しています。 
Due to large amount of data, it has
大量のデータのため、それは

Authors’ addresses: Taimoor Ahmed Javed, taimurahmed60@gmail.com, National University of Computer and Emerging Sciences, Islamabad, H-11/4, Islamabad, Islamabad Capital Territory, Pakistan, 44000; Waseem Shahzad, National University of Computer and Emerging Sciences, Islamabad, H-11/4, Islamabad, Pakistan, waseem.shahzad@nu.edu.pk; Umair Arshad, National University of Computer and Emerging Sciences, Islamabad, Pakistan.
著者の住所: Taimoor Ahmed Javed, taimurahmed60@gmail.com, ナショナルコンピュータ大学および新興科学、イスラマバード、H-11/4、イスラマバード、イスラマバード首都圏、パキスタン、44000; Waseem Shahzad, ナショナルコンピュータ大学および新興科学、イスラマバード、H-11/4、イスラマバード、パキスタン、waseem.shahzad@nu.edu.pk; Umair Arshad, ナショナルコンピュータ大学および新興科学、イスラマバード、パキスタン。

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. 
この作品のすべてまたは一部のデジタルまたは印刷コピーを個人または教室で使用するために作成する許可は、コピーが利益または商業的利益のために作成または配布されず、コピーにこの通知と最初のページに完全な引用が記載されている限り、無料で付与されます。 
Copyrights for components of this work owned by others than ACM must be honored.
ACM以外の他者が所有するこの作品のコンポーネントの著作権は尊重されなければなりません。 
Abstracting with credit is permitted. 
クレジット付きの要約は許可されています。 
To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. 
それ以外の方法でコピーしたり、再出版したり、サーバーに投稿したり、リストに再配布したりするには、事前の特定の許可および/または料金が必要です。 
Request permissions from permissions@acm.org.
許可はpermissions@acm.orgにリクエストしてください。 
© 2021 Association for Computing Machinery.
© 2021 コンピュータ機械協会。 
2375-4699/2021/8-ART111 $15.00 [https://doi.org/10.1145/1122445.1122456](https://doi.org/10.1145/1122445.1122456)
2375-4699/2021/8-ART111 $15.00 [https://doi.org/10.1145/1122445.1122456](https://doi.org/10.1145/1122445.1122456)



## 111  

111:2 Taimoor and Waseem, et al.  
TaimoorとWaseemらは、多くの課題を生み出します。しかし、ユーザーがデータにアクセスし、解釈し、パターンや知識生成のためにデータを修正しやすくするために、これらのテキストコンテンツの一部を自動的に分類するという取り組みがあります。大量の電子データをカテゴリに整理することは、多くの個人や企業にとって関心のあるトピックになっています。この問題の唯一の解決策はテキスト分類です。テキスト分類は、文書をそのカテゴリに応じて分類するプロセスです。  
It uses a wide variety of areas of expertise which includes AI, NLP and machine learning.  
それは、AI、NLP、機械学習を含むさまざまな専門分野を使用します。  
It uses a supervised learning based approach, in which we train a model by giving a large amount of data.  
それは、モデルを大規模なデータを与えることによって訓練する、教師あり学習に基づくアプローチを使用します。  
Recently, several algorithms have been proposed like SVM, k-Nearest Neighbor, Naive Bayes.  
最近、SVM、k-Nearest Neighbor、Naive Bayesのような複数のアルゴリズムが提案されています。  
Results shows that these approaches are very effective in conventional text classification applications.  
結果は、これらのアプローチが従来のテキスト分類アプリケーションで非常に効果的であることを示しています。  
There are many application of text classification like topic modeling, sentiment analysis, intent detection and spam detection.  
テキスト分類の多くのアプリケーションには、トピックモデリング、感情分析、意図検出、スパム検出などがあります。  
Generally text classification tasks have only few classes.  
一般的に、テキスト分類タスクには少数のクラスしかありません。  
When classification tasks have large number of classes then we will extend text classification problem because they have some specific challenges which require particular solution.  
分類タスクに多数のクラスがある場合、特定の解決策を必要とする特定の課題があるため、テキスト分類の問題を拡張します。  
There are numerous significant issues in classification which consists of similar categories which are organized into hierarchical structure.  
分類には、階層構造に整理された類似のカテゴリからなる多くの重要な問題があります。  
So here hierarchical classification comes into being.  
したがって、ここで階層分類が登場します。  
In hierarchical classification, classes are organized into categories and sub categories or we can say that classes are organized into class hierarchy and when we apply this to textual data it will become hierarchical text classification.  
階層分類では、クラスはカテゴリとサブカテゴリに整理されるか、クラス階層に整理されると言えます。そして、これをテキストデータに適用すると、階層テキスト分類になります。  
In recent years, hierarchical classification seems to be an active topic of research in the field of databases.  
近年、階層分類はデータベース分野で活発な研究テーマのようです。  
Web directories like Yahoo, Wikipedia are example of hierarchical text repositories.  
YahooやWikipediaのようなウェブディレクトリは、階層テキストリポジトリの例です。  
There are different applications nowadays in which documents are organized as hierarchical structure.  
現在、文書が階層構造として整理されるさまざまなアプリケーションがあります。  
If we take a real world example, Hierarchical text classification is like a librarian job, who want to place a book in a shelf.  
実世界の例を挙げると、階層テキスト分類は、本を棚に置きたい図書館員の仕事のようなものです。  
Many organizations like IT companies, law firms and medical companies are taking advantage of automatic classification of documents.  
IT企業、法律事務所、医療会社など、多くの組織が文書の自動分類の利点を享受しています。  
Therefore, it shows that hierarchical classification have a significant impact on many applications and organizations.  
したがって、階層分類は多くのアプリケーションや組織に重要な影響を与えることを示しています。  
The Urdu language has a global reach and it is Pakistan’s national language.  
ウルドゥー語は世界的な広がりを持ち、パキスタンの国語です。  
Urdu language is also being spoke in six states of India as their official language.  
ウルドゥー語は、インドの6つの州でも公用語として話されています。  
There are more than 12 million speakers in Pakistan and over 300 million speakers all across the globe [27].  
パキスタンには1200万人以上の話者がいて、世界中で3億人以上の話者がいます[27]。  
Previously, Urdu was ignored by researchers due to its complex composition, peculiar characteristics and absence of linguistic capital [7].  
以前、ウルドゥー語はその複雑な構成、特異な特徴、言語資本の欠如のために研究者に無視されていました[7]。  
Due to these features, Urdu text classification is much more complex than other languages.  
これらの特徴により、ウルドゥー語のテキスト分類は他の言語よりもはるかに複雑です。  
Moreover, automatic text classification systems which is developed for other languages cannot be used for Urdu language.  
さらに、他の言語のために開発された自動テキスト分類システムは、ウルドゥー語には使用できません。  
Since last 10 years, we saw a rapid growth in Urdu text documents like journals, web databases and online news articles.  
過去10年間、ジャーナル、ウェブデータベース、オンラインニュース記事などのウルドゥー語のテキスト文書が急速に増加しました。  
Because of these considerations, it raise the interest of researchers in the Urdu language.  
これらの考慮事項により、ウルドゥー語に対する研究者の関心が高まっています。  
Mostly research work is done in English language for hierarchical text classification.  
階層テキスト分類に関する研究は主に英語で行われています。  
Recently, many researches shows that this topic is gaining a lot of interest nowadays.  
最近、多くの研究がこのトピックが非常に関心を集めていることを示しています。  
So research work on hierarchical classification has been started in many languages like Chinese, Arabic and Indonesian.  
したがって、階層分類に関する研究は、中国語、アラビア語、インドネシア語など多くの言語で始まっています。  
There is a huge gap for Urdu language.  
ウルドゥー語には大きなギャップがあります。  
Research is done on simple text classification but there is no research work on hierarchical Urdu text classification.  
単純なテキスト分類に関する研究は行われていますが、階層ウルドゥー語テキスト分類に関する研究はありません。  
However, many studies has been found on simple Urdu text classification.  
しかし、単純なウルドゥー語テキスト分類に関する多くの研究が見つかっています。  
For instance, [3] have done research on Urdu text classification by applying SVM on large urdu corpus.  
例えば、[3]は大規模なウルドゥー語コーパスにSVMを適用してウルドゥー語テキスト分類に関する研究を行いました。  
[14] have applied different feature extraction techniques on Urdu language text and Decision Tree algorithm J-48 is used for classification.  
[14]はウルドゥー語テキストに対して異なる特徴抽出技術を適用し、分類には決定木アルゴリズムJ-48を使用しました。  
Most of the previous studies on automated text classification is based on supervised learning techniques such as decision trees, naive Bayes and support vector machines (SVM).  
自動テキスト分類に関するほとんどの以前の研究は、決定木、ナイーブベイズ、サポートベクターマシン（SVM）などの教師あり学習技術に基づいています。  
Nevertheless automated classification has become more and more difficult due to a rising number of corpus sizes and categorizing a document into fields and subfields.  
それにもかかわらず、自動分類はコーパスサイズの増加と文書をフィールドおよびサブフィールドに分類することにより、ますます困難になっています。  
Due to this, these machine learning algorithms tend to have less accuracy.  
このため、これらの機械学習アルゴリズムは精度が低くなる傾向があります。  
In fact mostly studies perform performance on machine learning methods.  
実際、ほとんどの研究は機械学習手法の性能を評価します。  
Since, the proposed approach is based on deep neural network.  
提案されたアプローチは深層ニューラルネットワークに基づいています。  
Neural networks have recently been shown to be efficient in conducting endways learning of hierarchical text classification.  
ニューラルネットワークは最近、階層テキスト分類のエンドウェイ学習を行うのに効率的であることが示されています。  
To fill a gap of hierarchical text classification for Urdu language and overcome the limitations of the above machine learning models and to obtain improved results for the Urdu document classification, we introduce a hierarchical model based on LSTM mechanism named as Hierarchical Multi-layer LSTMs (HMLSTM).  
ウルドゥー語の階層テキスト分類のギャップを埋め、上記の機械学習モデルの制限を克服し、ウルドゥー文書分類の改善された結果を得るために、LSTMメカニズムに基づく階層モデルであるHierarchical Multi-layer LSTMs（HMLSTM）を導入します。  
HMLSTM incorporates deep learning algorithms to facilitate both general and advanced learning at the document hierarchy level.  
HMLSTMは、文書階層レベルで一般的および高度な学習を促進するために深層学習アルゴリズムを組み込んでいます。  
In this study, we implement a supervised HMLSTM model on Urdu news to extract categories and sub categories and their hierarchical relationships.  
この研究では、ウルドゥー語のニュースに対してカテゴリとサブカテゴリおよびその階層関係を抽出するために、教師ありHMLSTMモデルを実装します。  
We first apply Text Representing Layer to achieve text representation in which we use Word2vec embedding to transform the words to vector and prepare words vocabulary.  
最初に、テキスト表現を達成するためにテキスト表現層を適用し、Word2vec埋め込みを使用して単語をベクトルに変換し、単語の語彙を準備します。  
Then we apply Urdu Hierarchical LSTM Layer (UHLSTML) on our self created dataset named as Urdu News Dataset for Hierarchical Text Classification (UNDHTC)[1].  
次に、ウルドゥー語ニュースデータセット（Hierarchical Text Classificationのためのウルドゥー語ニュースデータセット（UNDHTC）[1]）と呼ばれる自己作成データセットにウルドゥー階層LSTM層（UHLSTML）を適用します。  
In our experiments, we select six state of the art machine learning models and one deep neural model to evaluate the effectiveness of HMLSTM.  
私たちの実験では、HMLSTMの効果を評価するために、最先端の機械学習モデル6つと1つの深層ニューラルモデルを選択します。  
The experiments on real world dataset shows the efficiency and predictive capacity of our model.  
実世界のデータセットに対する実験は、私たちのモデルの効率性と予測能力を示しています。  
In particular, our model exhibits improved accuracy over conventional text classification approaches.  
特に、私たちのモデルは従来のテキスト分類アプローチに対して精度が向上しています。  
To summarize, this paper includes the following contributions:  
要約すると、この論文には以下の貢献が含まれています：  
Urdu language has insufficient resources, but it has a complex and complicated morphological script, which makes automated text processing more difficult.  
ウルドゥー語は資源が不十分ですが、複雑で難解な形態素スクリプトを持っており、自動テキスト処理をより困難にしています。  
A big issue for the Urdu language is the lack of availability of large, standardized, accessible and cost-free text dataset.  
ウルドゥー語にとって大きな問題は、大規模で標準化され、アクセス可能で無料のテキストデータセットの不足です。  
So in this study, we develop a large dataset of Urdu news documents and will make this dataset freely accessible for future study.  
したがって、この研究では、ウルドゥー語のニュース文書の大規模データセットを開発し、将来の研究のためにこのデータセットを無料で利用できるようにします。  
This research is conducted because hierarchical text classification method has never been applied to classify Urdu news using deep neural network.  
この研究は、階層テキスト分類手法が深層ニューラルネットワークを使用してウルドゥー語のニュースを分類するために適用されたことがないために行われます。  
So, we have developed the HMLSTM method which can predict the categories of each level while classifying all categories in the whole hierarchical structure accurately.  
したがって、私たちは、全階層構造のすべてのカテゴリを正確に分類しながら、各レベルのカテゴリを予測できるHMLSTMメソッドを開発しました。  
We conduct a thorough evaluation of our proposed method on Urdu News dataset (UNDHTC) from different domains.  
私たちは、さまざまなドメインからのウルドゥー語ニュースデータセット（UNDHTC）に対して提案した方法の徹底的な評価を行います。  
The experiment results show that our method can outperforms various baselines methods and deep neural model.  
実験結果は、私たちの方法がさまざまなベースライン手法や深層ニューラルモデルを上回ることを示しています。  
The rest of this paper is structured as follows.  
この論文の残りの部分は次のように構成されています。  
In the next segment, we will be discussing related work.  
次のセグメントでは、関連研究について議論します。  
In Section 3, we will discuss the background of hierarchical text classification process.  
第3節では、階層テキスト分類プロセスの背景について議論します。  
We will address what form of class structures most widely used, that is either DAG structure or tree structure.  
最も広く使用されているクラス構造の形式、すなわちDAG構造またはツリー構造について説明します。  
We will also discuss the types of hierarchical text classification and analyse which type is better than other.  
階層テキスト分類の種類についても議論し、どのタイプが他のタイプよりも優れているかを分析します。  
In Section 4, we will discuss base line techniques.  
第4節では、ベースライン技術について議論します。  
In Section 5, we will address our proposed methodology and dataset.  
第5節では、提案する方法論とデータセットについて説明します。  
Section 6 presents the experiments and results.  
第6節では、実験と結果を示します。  
Section 7 concludes the paper and also future work is discussed.  
第7節では、論文を締めくくり、今後の研究についても議論します。  



## 2 RELATED WORK 関連研究

This section of the paper discusses recent efforts and contribution on hierarchical text classification and their methods used in similar areas which have an influence in this field. 
このセクションでは、階層的テキスト分類に関する最近の取り組みと貢献、およびこの分野に影響を与える類似の領域で使用される手法について論じます。

A variety of methods have been proposed to enhance the quality of classification results which are discussed below. 
分類結果の質を向上させるために提案されたさまざまな手法について、以下で説明します。

In conventional text classification, feature engineering has been used to get useful quality features which help in improving the model performance. 
従来のテキスト分類では、モデルのパフォーマンスを向上させるために役立つ有用な特徴を得るために特徴エンジニアリングが使用されてきました。

Text classification is a well-proven way to organize a large scale document set. 
テキスト分類は、大規模な文書セットを整理するための確立された方法です。

Many algorithms have been proposed [13] to do text classification, such as SVM, kNN, naïve bayes, decision trees. 
SVM、kNN、ナイーブベイズ、決定木など、テキスト分類を行うために多くのアルゴリズムが提案されています[13]。

Analyses showed that in conventional text classification applications, these algorithms are very efficient. 
分析によると、従来のテキスト分類アプリケーションでは、これらのアルゴリズムは非常に効率的です。

Nowadays, deep learning models are widely use in natural language processing tasks. 
現在、深層学習モデルは自然言語処理タスクで広く使用されています。

Recently, Nabeel et al [4] applied deep learning classification methodologies on Urdu text. 
最近、Nabeelら[4]はウルドゥー語のテキストに深層学習分類手法を適用しました。

For Arabic text classification [8] also applied deep neural models. 
アラビア語のテキスト分類においても[8]、深層ニューラルモデルが適用されました。

Similarly, authors applied attention mechanism for Chinese text classification [30]. 
同様に、著者らは中国語のテキスト分類に注意メカニズムを適用しました[30]。

Nonetheless, text classification has become very challenging these days. 
それにもかかわらず、テキスト分類は最近非常に困難になっています。

It is due to the growth in corpus sizes, categories and subcategories. 
これは、コーパスのサイズ、カテゴリ、およびサブカテゴリの増加によるものです。

With the increasing number of categories and subcategories of a document, it is important to not just label the document by a specialized field but also organized in its overall category and subcategory. 
文書のカテゴリとサブカテゴリの数が増えるにつれて、文書を専門分野でラベル付けするだけでなく、全体のカテゴリとサブカテゴリに整理することが重要です。

So we use hierarchical classification. 
そのため、階層的分類を使用します。

Deep neural models have recently gained popularity in the classification of text by means of their communication capacity and low requirements for features. 
深層ニューラルモデルは、通信能力と特徴の低い要件により、テキストの分類で最近人気を集めています。

But deep neural models based on extensive training data and needs people to provide lots of labelled data and in many cases when we have to label data, we have to find domain expert person to do this task which can be too costly. 
しかし、広範なトレーニングデータに基づく深層ニューラルモデルは、多くのラベル付きデータを提供する必要があり、データにラベルを付ける必要がある場合には、専門家を見つける必要があり、これが非常に高価になることがあります。

Another issue in deep neural models is that in the hierarchical text classifications it cannot determine appropriate levels in the class hierarchy. 
深層ニューラルモデルのもう一つの問題は、階層的テキスト分類においてクラス階層の適切なレベルを決定できないことです。

There is no automatic way to determine best level in class hierarchy. 
クラス階層の最適なレベルを自動的に決定する方法はありません。

So recently Meng et al [23] proposed a weakly supervised neural method for hierarchical text classification which address above issues. 
そこで最近、Mengら[23]は、上記の問題に対処するための階層的テキスト分類のための弱教師ありニューラル手法を提案しました。

This approach is based on deep neural network which requires only small amount of labelled data provided by the users. 
このアプローチは、ユーザーが提供する少量のラベル付きデータのみを必要とする深層ニューラルネットワークに基づいています。

It doesn’t require large amount of training data. 
大量のトレーニングデータは必要ありません。

So they pre train local classifier at each node in hierarchical structure and then ensemble all local classifier into a global classifier using self-training. 
そのため、彼らは階層構造の各ノードでローカル分類器を事前にトレーニングし、次に自己学習を使用してすべてのローカル分類器をグローバル分類器に統合します。

The entire process automatically determine the most appropriate level of each document. 
このプロセス全体は、各文書の最も適切なレベルを自動的に決定します。

They have performed experiments on New York Times news articles. 
彼らはニューヨークタイムズのニュース記事で実験を行いました。

Corpus consists of 5 categories and 25 sub categories. 
コーパスは5つのカテゴリと25のサブカテゴリで構成されています。

The model that have been used is CNN. 
使用されたモデルはCNNです。

They have compared their results with other models and gives satisfactory results. 
彼らは他のモデルと結果を比較し、満足のいく結果を得ました。

There are many existing approaches for document classification but few organize the document into the correct areas. 
文書分類のための既存のアプローチは多数ありますが、文書を正しい領域に整理するものは少ないです。

This paper [18] proposed a new approach for hierarchical classification of text which is named as Hierarchical Deep learning for text classification. 
この論文[18]は、テキストの階層的分類のための新しいアプローチを提案しており、これを「テキスト分類のための階層的深層学習」と名付けています。

This paper employed new methods of deep learning. 
この論文では、深層学習の新しい手法が採用されています。

In neural networks, deep learning is very effective. 
ニューラルネットワークにおいて、深層学習は非常に効果的です。

Deep learning can manage supervised, unsupervised and semi supervised learning. 
深層学習は、教師あり、教師なし、半教師あり学習を管理できます。

In this paper, approaches to the hierarchy of the classification of documents advance the concept of deep neural learning network. 
この論文では、文書の分類の階層に対するアプローチが深層ニューラル学習ネットワークの概念を進展させています。

The authors brought together various approaches to create hierarchical document classifiers. 
著者らは、階層的文書分類器を作成するためにさまざまなアプローチを統合しました。

They have used three neural networks DNN, CNN and RNN. 
彼らは、3つのニューラルネットワークDNN、CNN、RNNを使用しました。

DNN is used for first level of classification of documents. 
DNNは文書の最初のレベルの分類に使用されます。

Lets suppose if the first model output is medical, in next level it will train only all medical science documents. 
最初のモデルの出力が「医療」であると仮定すると、次のレベルではすべての医療科学文書のみをトレーニングします。

So, DNN is trained on first hierarchical level and in next level, each hierarchy of document is trained with specified domain. 
したがって、DNNは最初の階層レベルでトレーニングされ、次のレベルでは、各文書の階層が特定のドメインでトレーニングされます。

They have collected data of articles from Web of science. 
彼らはWeb of Scienceから記事のデータを収集しました。

Results were compared with conventional text classification methods like K-NN, decision tree, Naive Bayes and came to know that RNN outperforms all of them. 
結果は、K-NN、決定木、ナイーブベイズなどの従来のテキスト分類手法と比較され、RNNがすべての手法を上回ることがわかりました。

CNN performs second best. 
CNNは2番目に良い結果を出しました。

The results shows that by using deep learning approaches, we can get good improvement in performance as compared to traditional methods. 
結果は、深層学習アプローチを使用することで、従来の手法と比較してパフォーマンスの向上が得られることを示しています。

The HDLTex approach clearly shows variations of RNN at the top level and CNN or DNN at the lower level produced consistently good results. 
HDLTexアプローチは、最上位レベルでのRNNの変動と、下位レベルでのCNNまたはDNNが一貫して良好な結果を生み出すことを明確に示しています。

A topical text classification is basic issue for many applications like emotion analysis, question answering, auto-tagging customer queries and categorizing articles. 
トピカルテキスト分類は、感情分析、質問応答、自動タグ付け顧客クエリ、記事の分類など、多くのアプリケーションにとって基本的な問題です。

To handle large amount of labels, hierarchical text classification has been used as an effective way to organize text. 
大量のラベルを処理するために、階層的テキスト分類がテキストを整理するための効果的な方法として使用されています。

Authors have proposed a new technique named as Hierarchically Regularized Deep graph Cnn [26], which will solve the problem of document level topical classification and also address issues in topical classification which are long distance word dependency and nonconsecutive phrases. 
著者らは、文書レベルのトピカル分類の問題を解決し、長距離単語依存関係や非連続フレーズに関するトピカル分類の問題に対処する「階層的正則化深層グラフCNN」という新しい手法を提案しました[26]。

First documents are converted into graphs that is centered on the word co-occurrence. 
最初に文書は、単語の共起に基づいてグラフに変換されます。

Every document represents as a graph of vectors. 
各文書はベクトルのグラフとして表されます。

For nodes of graph, pretrained vectors are used as an input. 
グラフのノードには、事前学習されたベクトルが入力として使用されます。

Word2vec is used in this scenario. 
このシナリオではWord2vecが使用されます。

After that they have generated sub graph of words and apply graph preprocessing on them. 
その後、彼らは単語のサブグラフを生成し、それにグラフ前処理を適用しました。

They have used both RNN and CNN models for text classification. 
彼らはテキスト分類のためにRNNとCNNの両方のモデルを使用しました。

They have proposed deep graph CNN approach for classification of text. 
彼らはテキストの分類のために深層グラフCNNアプローチを提案しました。

Dependency between the labels can improve classification results, so that why they have used recursive regularization. 
ラベル間の依存関係は分類結果を改善できるため、彼らは再帰的正則化を使用しました。

They have used two data sets RCV1 and NY Times for experiments. 
彼らは実験のために2つのデータセットRCV1とNY Timesを使用しました。

Authors compared their experimental results with traditional hierarchical text classification models. 
著者らは実験結果を従来の階層的テキスト分類モデルと比較しました。

The results shows that proposed approach have achieved good results than other models. 
結果は、提案されたアプローチが他のモデルよりも良好な結果を達成したことを示しています。

Many applications arrange documents in the form hierarchical structure where classes are divided into categories and subcategories. 
多くのアプリケーションは、クラスがカテゴリとサブカテゴリに分かれた階層構造の形で文書を整理します。

In previous papers flat based methods were proposed. 
以前の論文では、フラットベースの手法が提案されました。

They only predict the categories of last level and ignore the hierarchical structure. 
彼らは最終レベルのカテゴリのみを予測し、階層構造を無視します。

To solve this problem, some work has been done in hierarchical category structure. 
この問題を解決するために、階層的カテゴリ構造に関するいくつかの作業が行われています。

Nevertheless, these literature focuses mainly on certain local areas or global structure as a whole ignoring dependencies between different levels of hierarchy. 
それにもかかわらず、これらの文献は、異なる階層のレベル間の依存関係を無視して、主に特定のローカル領域または全体のグローバル構造に焦点を当てています。

In short, it’s a challenging task in which records are allocated to different categories and every category have its dependencies. 
要するに、これは、レコードが異なるカテゴリに割り当てられ、各カテゴリに依存関係があるという挑戦的なタスクです。

The challenges are, connection among texts and hierarchy must be identified when interpreting the semantics of documents. 
課題は、文書の意味を解釈する際に、テキストと階層間の接続を特定する必要があることです。

Next challenge is that the hierarchical category structure has dependencies among different levels, which is mostly ignored by past research papers. 
次の課題は、階層的カテゴリ構造が異なるレベル間に依存関係を持っていることであり、これは過去の研究論文でほとんど無視されています。

Another challenge is that when we are assigning document to hierarchical categories, we should consider overall structure of hierarchical tree rather than just considering local region. 
もう一つの課題は、文書を階層的カテゴリに割り当てる際に、単にローカル領域を考慮するのではなく、階層ツリーの全体構造を考慮する必要があることです。

This paper [10] have proposed a new approach named as recurrent neural network based on hierarchical attention to solve all above challenges. 
この論文[10]は、上記のすべての課題を解決するために、階層的注意に基づく再帰的ニューラルネットワークという新しいアプローチを提案しました。

This framework automatically compiles a document with the most appropriate level of categories. 
このフレームワークは、自動的に文書を最も適切なカテゴリレベルでコンパイルします。

In this paper, authors have first work on the illustration of documents and hierarchical framework. 
この論文では、著者らは最初に文書と階層フレームワークの説明に取り組みました。

They have applied embedding layer. 
彼らは埋め込み層を適用しました。

This layer is used to computes text and the structure of their hierarchy. 
この層は、テキストとその階層の構造を計算するために使用されます。

Word2vec is used for this task. 
このタスクにはWord2vecが使用されます。

After that, they have applied Bi LSTM to improve semantic text representation. 
その後、彼らは意味的テキスト表現を改善するためにBi LSTMを適用しました。

After enhancing text representation and their structure, attention based recurrent layer is applied to represent the dependency for each category level from top to down. 
テキスト表現とその構造を強化した後、注意に基づく再帰層が適用され、上から下への各カテゴリレベルの依存関係を表現します。

After that hybrid approach is designed for making predictions of the categories for each level. 
その後、各レベルのカテゴリの予測を行うためにハイブリッドアプローチが設計されます。

The experiments were conducted on academic exercises and repository of patent papers. 
実験は学術的な演習と特許文書のリポジトリで行われました。

Educational dataset is categorized into three levels hierarchy while repository of patent papers into four levels hierarchy. 
教育データセットは3レベルの階層に分類され、特許文書のリポジトリは4レベルの階層に分類されます。

Experimental results shows that HARNN approach is effective. 
実験結果は、HARNNアプローチが効果的であることを示しています。

Ivana et al [11] have done hierarchical classification on Indonesian news articles. 
Ivanaら[11]はインドネシアのニュース記事に対して階層的分類を行いました。

This research is conducted to examine whether hierarchical multi label classification could provide desirable results in classifying Indonesian news articles. 
この研究は、階層的マルチラベル分類がインドネシアのニュース記事の分類において望ましい結果を提供できるかどうかを検証するために行われました。

So authors have proposed a hierarchical multi label classification model for Indonesian news articles. 
そのため、著者らはインドネシアのニュース記事のための階層的マルチラベル分類モデルを提案しました。

Three kinds of methods are available, which are global approach, flat approach and top down approach. 
利用可能な手法は3種類あり、グローバルアプローチ、フラットアプローチ、トップダウンアプローチです。

To handle multi label classification, authors have used calibrated label ranking and binary relevance. 
マルチラベル分類を処理するために、著者らはキャリブレーションされたラベルランキングとバイナリ関連性を使用しました。

Dataset is collected from news website and it is organized into two level hierarchy. 
データセットはニュースウェブサイトから収集され、2レベルの階層に整理されています。

The news articles have been split into 10 categories and 4 subcategories. 
ニュース記事は10のカテゴリと4つのサブカテゴリに分割されています。

For classification algorithms that were used are j48, Naïve bayes and SVM. 
使用された分類アルゴリズムはj48、ナイーブベイズ、SVMです。

In this paper [2], the author has present a study on Hierarchical text classification for Arabic language. 
この論文[2]では、著者がアラビア語の階層的テキスト分類に関する研究を発表しています。

Previously no research work is done on Hierarchical Arabic text classification, however many studies shows that work is done on flat Arabic text classification. 
以前には階層的アラビア語テキスト分類に関する研究は行われていませんが、多くの研究がフラットアラビア語テキスト分類に関する作業を行っていることを示しています。

The method used for Hierarchical Arabic text classification is first order Markov chain. 
階層的アラビア語テキスト分類に使用される手法は、一次マルコフ連鎖です。

Transition probability matrix is created for each category when performing text classification task in Markov chain approach then for every document, a scoring procedure is carried out for all training set categories. 
マルコフ連鎖アプローチでテキスト分類タスクを実行する際に、各カテゴリの遷移確率行列が作成され、その後、すべてのトレーニングセットカテゴリに対してスコアリング手順が実行されます。

In this study, data is taken from Alqabas newspaper. 
この研究では、Alqabas新聞からデータが取得されます。

The documents are divided into 3 level hierarchy. 
文書は3レベルの階層に分割されます。

First they preprocess the data. 
最初にデータを前処理します。

These kind of activities helps to get rid of useless data. 
このような活動は、無駄なデータを取り除くのに役立ちます。

TF IDF is used for preprocessing. 
前処理にはTF-IDFが使用されます。

Then they train the data by creating markov chain matrices. 
その後、マルコフ連鎖行列を作成することでデータをトレーニングします。

For each Arabic character a number is assigned. 
各アラビア文字には番号が割り当てられます。

This process is called mapping. 
このプロセスはマッピングと呼ばれます。



. Then they train the data by creating markov chain matrices. 
その後、彼らはマルコフ連鎖行列を作成することによってデータを訓練します。 
For each Arabic character a number is assigned. 
各アラビア文字には番号が割り当てられます。 
This process is called mapping. 
このプロセスはマッピングと呼ばれます。 
Probability matrix is created for each category. 
各カテゴリに対して確率行列が作成されます。 
The writers have compared their proposed solution with LSI. 
著者たちは、提案した解決策をLSIと比較しました。 
Results demonstrate that top level performance is relatively good while it keeps on decreasing in below levels. 
結果は、最上位のパフォーマンスが比較的良好である一方で、下位レベルでは減少し続けることを示しています。 

-----
111:6 Taimoor and Waseem, et al. 
111:6 タイムールとワシームら。 
Deep neural networks are becoming more common task for classifying text because of their strong expressive capacity and less practical technical requirement. 
深層ニューラルネットワークは、その強力な表現能力と実用的な技術要件が少ないため、テキスト分類の一般的なタスクになりつつあります。 
Although it is so attractive, models of neural text recognition suffer from the absence of trained data in many applications. 
非常に魅力的ではありますが、ニューラルテキスト認識のモデルは、多くのアプリケーションで訓練データが不足しているという問題に直面しています。 
In this paper [31], author have proposed a hierarchical attention network for text classification of document. 
この論文では[31]、著者は文書のテキスト分類のための階層的注意ネットワークを提案しました。 
They have evaluated their model on large scale data. 
彼らは大規模データでモデルを評価しました。 
Datasets that they have used are reviews of imdb, yelp and amazon. 
彼らが使用したデータセットは、imdb、yelp、amazonのレビューです。 
They have compared their model with baselines methods like SVM, LSTM and word based CNN. 
彼らは、SVM、LSTM、単語ベースのCNNなどのベースライン手法とモデルを比較しました。 
Their model develops the document vector by combining relevant terms to the sentence vector and then the sentence vector to the document vector. 
彼らのモデルは、関連する用語を文ベクトルに結合し、次に文ベクトルを文書ベクトルに結合することによって文書ベクトルを生成します。 
The experimental results shows that their model perform better than the previous models. 
実験結果は、彼らのモデルが以前のモデルよりも優れていることを示しています。 

Mao et al. suggested a method for hierarchical text classification. 
マオらは、階層的テキスト分類のための方法を提案しました。 
Authors have formulate hierarchical text classification as Markov decision process [22]. 
著者たちは、階層的テキスト分類をマルコフ決定過程として定式化しました[22]。 
In this process, at each phase, the agent examines the current situation and makes decisions. 
このプロセスでは、各段階でエージェントが現在の状況を調査し、決定を下します。 
In this paper, authors suggested a framework in which system learns label assignment policy to decide when to place object and where to interrupt the assignment process. 
この論文では、著者たちは、システムがラベル割り当てポリシーを学習し、オブジェクトを配置するタイミングと割り当てプロセスを中断する場所を決定するフレームワークを提案しました。 
Their label assignment policy place each object to its label in a hierarchical structure. 
彼らのラベル割り当てポリシーは、各オブジェクトを階層構造のラベルに配置します。 
At start policy place an object on the root label. 
最初のポリシーは、オブジェクトをルートラベルに配置します。 
At every point, the policy determines which label object will be put next until stop action has been taken. 
すべてのポイントで、ポリシーは次にどのラベルのオブジェクトを配置するかを決定し、停止アクションが取られるまで続きます。 
Hierarchical label assignment policy examines the hierarchical structure of labels, both through training and analysis, in a precise way, which eliminates identity prejudice frequently seen in previous local and global strategies. 
階層的ラベル割り当てポリシーは、トレーニングと分析の両方を通じてラベルの階層構造を正確に検討し、以前のローカルおよびグローバル戦略でよく見られるアイデンティティの偏見を排除します。 
Hierarchical label assignment policy is more versatile than other approaches in learning when to stop that support leaf node prediction. 
階層的ラベル割り当てポリシーは、葉ノード予測をサポートする停止タイミングを学習する点で、他のアプローチよりも多用途です。 
When exploring the labels hierarchy during training, Hierarchical label assignment policy performs better as compared to flat and local methods. 
トレーニング中にラベルの階層を探索する際、階層的ラベル割り当てポリシーはフラットおよびローカル手法と比較して優れた性能を発揮します。 
Authors have conducted experiments on five publically available datasets. 
著者たちは、5つの公開データセットで実験を行いました。 
Two datasets are related to news category which are RCV1 and NYT and other two are related to protein functional catalogue and gene prediction and last dataset is from Yelp Dataset Challenge. 
2つのデータセットはニュースカテゴリに関連しており、RCV1とNYTであり、他の2つはタンパク質機能カタログと遺伝子予測に関連しており、最後のデータセットはYelp Dataset Challengeからのものです。 
The models that have been used for feature encoding are TextCNNN proposed by Kim et al. [15], Hierarchical Attention Network proposed by Yang et al. [31] and bow-CNN proposed by Johnson et al. [12]. 
特徴エンコーディングに使用されたモデルは、Kimらによって提案されたTextCNNN [15]、Yangらによって提案されたHierarchical Attention Network [31]、およびJohnsonらによって提案されたbow-CNN [12]です。 
They have compared their results with state of art hierarchical text classification methods and neural methods. 
彼らは、最先端の階層的テキスト分類手法およびニューラル手法と結果を比較しました。 
The experiments results shows that their method surpassing traditional hierarchical text classification methods notably. 
実験結果は、彼らの方法が従来の階層的テキスト分類手法を著しく上回っていることを示しています。 

Recently many approaches have been proposed for chinese text classification. 
最近、中国語のテキスト分類のために多くのアプローチが提案されています。 
Chinese text classification is difficult as compared to other language like English, owing to the features of the Chinese text itself. 
中国語のテキスト分類は、英語のような他の言語と比較して難しいのは、中国語のテキスト自体の特徴によるものです。 
To improve quality of chinese text classification, Liu et al. [21] proposed a hierarchical model architecture which can extract rigorous context and information in a sequence manner from Chinese texts named as hierarchical comprehensive context modeling network. 
中国語のテキスト分類の質を向上させるために、Liuらは、階層的包括的コンテキストモデリングネットワークと呼ばれる、中国語テキストから厳密なコンテキストと情報を順序的に抽出できる階層モデルアーキテクチャを提案しました。 
This approach is a combination of LSTM and temporal convolutional networks [5]. 
このアプローチは、LSTMと時間的畳み込みネットワークの組み合わせです[5]。 
LSTM is used for extracting context and sequence features of document. 
LSTMは、文書のコンテキストとシーケンス特徴を抽出するために使用されます。 
In this paper authors have used four datasets for experimentation. 
この論文では、著者たちは実験のために4つのデータセットを使用しました。 
The results conducted on CRTEXT dataset shows that their model achieved the best results as compared to other datasets. 
CRTEXTデータセットでの結果は、彼らのモデルが他のデータセットと比較して最良の結果を達成したことを示しています。 
This paper [9] proposed a new approach for a largescale multi-label text classification. 
この論文[9]は、大規模なマルチラベルテキスト分類のための新しいアプローチを提案しました。 
First text is converted into a graph structure then attention mechanism is used to represent the full functionality of the text. 
最初にテキストはグラフ構造に変換され、その後注意メカニズムがテキストの全機能を表現するために使用されます。 
They have also used convolutional neural networks for feature extraction. 
彼らは特徴抽出のために畳み込みニューラルネットワークも使用しました。 
The proposed method shows good results as compared to state-of-the-art methods. 
提案された方法は、最先端の手法と比較して良好な結果を示しています。 
In this paper [20] authors have proposed a neural network approach which is based on BiLSTM and Hierarchical Attention layer. 
この論文[20]では、著者たちはBiLSTMと階層的注意層に基づくニューラルネットワークアプローチを提案しました。 
They have performed experiments on different news datasets. 
彼らは異なるニュースデータセットで実験を行いました。 
They have compared their model with CNN and BiLSTM attention network and achieved better results. 
彼らはCNNおよびBiLSTM注意ネットワークとモデルを比較し、より良い結果を達成しました。 

-----
Hierarchical Text Classification of Urdu News using Deep Neural Network 111:7 
深層ニューラルネットワークを用いたウルドゥー語ニュースの階層的テキスト分類 111:7



## 3 HIERARCHICAL TEXT CLASSIFICATION BACKGROUND 階層的テキスト分類の背景

Nowadays, text classification techniques are normally focused on a flat model. 
現在、テキスト分類技術は通常、フラットモデルに焦点を当てています。

Currently, some methods for hierarchical text classification have been implemented to resolve the constraints of flat models and their methodology is focused on the classification method and feature selection. 
現在、フラットモデルの制約を解決するために、階層的テキスト分類のいくつかの方法が実装されており、その方法論は分類方法と特徴選択に焦点を当てています。

Mostly supervised learning technique is used which requires a category-based linear classification. 
主に、カテゴリベースの線形分類を必要とする教師あり学習技術が使用されます。

In hierarchical classification, we are provided with different categories which are organized hierarchically. 
階層的分類では、階層的に整理された異なるカテゴリが提供されます。

The corpus consist of training data in which documents are placed in categories and sub categories. 
コーパスは、文書がカテゴリとサブカテゴリに配置されたトレーニングデータで構成されています。

Words or vocabulary are extracted from this corpus which have high frequency in a certain category. 
特定のカテゴリで高頻度の単語や語彙がこのコーパスから抽出されます。

The vocabulary of every node is filtered and words are weighed according to their defined category. 
各ノードの語彙はフィルタリングされ、単語は定義されたカテゴリに応じて重み付けされます。

After this, test documents are evaluated and categories are ranked according to their term weighting. 
その後、テスト文書が評価され、カテゴリはその用語の重みに基づいてランク付けされます。

Term weights are assigned to each level node of hierarchy. 
用語の重みは、階層の各レベルノードに割り当てられます。

These classifications allocate documents to categories on the basis of ranking. 
これらの分類は、ランクに基づいて文書をカテゴリに割り当てます。

For categorizing, feature selection is used to determine categories of document. 
分類のために、特徴選択が文書のカテゴリを決定するために使用されます。

The words which are useless or have low frequency are removed to increase accuracy. 
無駄な単語や低頻度の単語は、精度を向上させるために削除されます。

There are different approaches that used to remove low frequency words. 
低頻度の単語を削除するために使用されるさまざまなアプローチがあります。

For example in “Fig. 1”, news is divided into three category i.e sports, entertainment and technology. 
例えば、「図1」では、ニュースはスポーツ、エンターテインメント、テクノロジーの3つのカテゴリに分けられています。

Fig. 1. Example of Hierarchical Classification. 
図1. 階層的分類の例。

On level 1, we can easily differentiate between all categories, if or not the document refers to sports, entertainment or technology. 
レベル1では、文書がスポーツ、エンターテインメント、またはテクノロジーに言及しているかどうかにかかわらず、すべてのカテゴリを簡単に区別できます。

If text corresponds to sports, then we will further categories into sub categories, either the sports is cricket, football or hockey. 
テキストがスポーツに該当する場合、さらにサブカテゴリに分類します。スポーツはクリケット、サッカー、またはホッケーのいずれかです。

In a hierarchy, each level represents the category of a document. 
階層内では、各レベルが文書のカテゴリを表します。

A classifier is trained for each node in a hierarchical tree. 
階層ツリーの各ノードに対して分類器がトレーニングされます。

When the new document arrives in a classification process, it is assigned to a suitable root node category then it use good category classifier to determine which direction to proceed in a hierarchy. 
新しい文書が分類プロセスに到着すると、それは適切なルートノードカテゴリに割り当てられ、その後、良いカテゴリ分類器を使用して階層内で進むべき方向を決定します。

And it will proceed until a document is assigned to a leaf node. 
そして、文書がリーフノードに割り当てられるまで進行します。

There are two approaches for describing a hierarchical structure, which are tree structure and Direct Acyclic Graph also known as DAG. 
階層構造を説明するための2つのアプローチがあり、ツリー構造と有向非巡回グラフ（DAG）として知られています。

The difference between these two structures is that, in tree structure each node should have one parent while in Direct Acyclic Graph structure single node may have one or more parent. 
これら2つの構造の違いは、ツリー構造では各ノードが1つの親を持つ必要があるのに対し、有向非巡回グラフ構造では単一のノードが1つ以上の親を持つ可能性があることです。

Fig. 2 shows the illustration of both structure. 
図2は、両方の構造の図を示しています。

According to Freitas et al. (2007) and Sun et al. (2001), there are different types of hierarchical classification [28], which are discussed below. 
Freitas et al.（2007）およびSun et al.（2001）によると、さまざまなタイプの階層的分類があり[28]、以下で説明します。

**3.1** **Flat Classification フラット分類** Koller and Sahami (1997) proposed this approach[17]. 
**3.1** **フラット分類** KollerとSahami（1997）はこのアプローチを提案しました[17]。

It is the most simple and straightforward method to handle hierarchical classification and it totally neglects class hierarchy. 
これは階層的分類を扱うための最も単純で直接的な方法であり、クラス階層を完全に無視します。

In flat classification you don’t worry about parent categories, only just classify document to its final leaf node. 
フラット分類では、親カテゴリを気にせず、文書を最終的なリーフノードに分類するだけです。

This method works as a conventional algorithm for classification. 
この方法は、分類のための従来のアルゴリズムとして機能します。

Nonetheless, the problem of hierarchical classification is solved implicitly. 
それでも、階層的分類の問題は暗黙的に解決されます。

If a leaf class is allocated to instance, almost all of its descendant classes are also allocated to it indirectly. 
リーフクラスがインスタンスに割り当てられると、その子孫クラスのほとんどすべても間接的に割り当てられます。

The advantage of this method is its simplicity. 
この方法の利点は、そのシンプルさです。

It is an easy way to execute with an out of-the-box classifier. 
これは、アウトオブボックスの分類器を使用して実行する簡単な方法です。

This approach also have some disadvantages. 
このアプローチにはいくつかの欠点もあります。

The main disadvantage is that this approach doesn’t explore complete information of parent child class relationship which can lose important information and could decrease the efficiency. 
主な欠点は、このアプローチが親子クラス関係の完全な情報を探求しないため、重要な情報を失い、効率が低下する可能性があることです。

“Fig. 3” shows the illustration of flat classification approach. 
「図3」は、フラット分類アプローチの図を示しています。

Fig. 3. Flat classification approach. 
図3. フラット分類アプローチ。

**3.2** **Global (big bang) approach グローバル（ビッグバン）アプローチ** This approach is simple, relatively complicated model, in which the whole class hierarchy takes into account in a single run. 
**3.2** **グローバル（ビッグバン）アプローチ** このアプローチはシンプルで、比較的複雑なモデルであり、全クラス階層を単一の実行で考慮します。

That means it classify data in one run. 
つまり、データを1回の実行で分類します。

Fig. 4 shows the illustration of one global classifier for the entire class hierarchy. 
図4は、全クラス階層のための1つのグローバル分類器の図を示しています。

When used in the test process, the induced model is identified by each test example, which can allocate classes to check example at any hierarchical level. 
テストプロセスで使用されると、誘導されたモデルは各テスト例によって識別され、任意の階層レベルでチェック例にクラスを割り当てることができます。

This approach can go in different direction. 
このアプローチは異なる方向に進むことができます。

Many use clustering approach, some recreate the problem as a multi-label, and others have altered the latest algorithms. 
多くの人がクラスタリングアプローチを使用し、一部は問題をマルチラベルとして再構築し、他の人は最新のアルゴリズムを変更しました。

The advantage of this approach is that this approach have smaller model as compare to other models and the class relationship is determined during model development and it provide fast predictions. 
このアプローチの利点は、他のモデルと比較してモデルが小さく、クラス関係がモデル開発中に決定され、迅速な予測を提供することです。

The drawback of this approach is that due to the high computations, there is higher chance of misclassify unseen data. 
このアプローチの欠点は、高い計算により、見えないデータを誤分類する可能性が高くなることです。

However, due to the high complexity of this approach, it is rarely used. 
しかし、このアプローチの高い複雑性のため、ほとんど使用されません。

Labrou et al. illustrate this approach. 
Labrouらはこのアプローチを示しています。

In their work [19], the program classifies website as subcategory of Yahoo! hierarchical groups. 
彼らの研究[19]では、プログラムはウェブサイトをYahoo!の階層グループのサブカテゴリとして分類します。

This approach is unique to applications for text mining. 
このアプローチはテキストマイニングのアプリケーションに特有です。

A threshold is used for the final classification. 
最終分類にはしきい値が使用されます。

There are some other method of global classifier which is based on multi label classification. 
マルチラベル分類に基づく他のグローバル分類器の方法もあります。

Kiritchenko et al. have done work on multi label classification[16]. 
Kiritchenkoらはマルチラベル分類に関する研究を行っています[16]。

To determine a hierarchical class, the learning process is amended to include all hierarchical classes by increasing the number of nodes having no child with information of predecessor classes. 
階層クラスを決定するために、学習プロセスは、前のクラスの情報を持つ子を持たないノードの数を増やすことによって、すべての階層クラスを含むように修正されます。

Fig. 4. Global approach: one global classifier for the entire class hierarchy. 
図4. グローバルアプローチ：全クラス階層のための1つのグローバル分類器。

**3.3** **Hierarchically-Structured Local Classifiers 階層構造のローカル分類器** The third approach is called as local approach which is also known as top down approach. 
**3.3** **階層構造のローカル分類器** 第三のアプローチはローカルアプローチと呼ばれ、トップダウンアプローチとしても知られています。

This method uses predefined data classification scheme to construct a classification hierarchy. 
この方法は、分類階層を構築するために事前定義されたデータ分類スキームを使用します。

It uses hierarchy to develop classifiers utilizing local information. 
階層を利用してローカル情報を使用して分類器を開発します。

Benefits of this strategy are straightforward, effective and can handle multi-label hierarchical classification and it maintains natural information of data hierarchy. 
この戦略の利点は、簡潔で効果的であり、マルチラベル階層分類を処理でき、データ階層の自然な情報を維持できることです。

One major drawback of this approach is if there is classification mistake in parent node, it will be propagated downwards the hierarchy. 
このアプローチの主な欠点は、親ノードに分類ミスがある場合、それが階層の下に伝播することです。

It can greatly affect the result of classification. 
これは分類結果に大きな影響を与える可能性があります。

There are three methods to implement local classification approach named as local classifier per parent node, local classifier per node and local classifier per level. 
ローカル分類アプローチを実装するための3つの方法があり、親ノードごとのローカル分類器、ノードごとのローカル分類器、レベルごとのローカル分類器と呼ばれています。

_3.3.1_ _Local classifier per parent node. この戦略はトップダウンアプローチとも呼ばれます。_ 
_3.3.1_ _親ノードごとのローカル分類器。この戦略はトップダウンアプローチとも呼ばれます。_

In this approach, we train one multi class classifier for each parent node to differentiate between its child nodes. 
このアプローチでは、各親ノードに対して子ノードを区別するための1つのマルチクラス分類器をトレーニングします。

Now lets take an example of class tree as shown in Figure. 5 and approach that is used is class prediction of hierarchy. 
ここで、図5に示すクラスツリーの例を取り、使用されるアプローチは階層のクラス予測です。

Lets assume document is assigned to class 2 node by initial classifier. 
文書が初期分類器によってクラス2ノードに割り当てられたと仮定します。

Then in level 2 we have second classifier which is class 5 node, is learned with the children of class 2 node. 
次に、レベル2では、クラス5ノードという2番目の分類器があり、クラス2ノードの子とともに学習されます。

Then class 5 node will make its class assignment. 
その後、クラス5ノードがそのクラス割り当てを行います。

This process will continue until classifiers are available. 
このプロセスは、分類器が利用可能になるまで続きます。

In our example, we have one classifier on the first level and one classifier on second level. 
私たちの例では、最初のレベルに1つの分類器があり、2番目のレベルに1つの分類器があります。

To stop incoherence with the prediction of different level, then you can develop a framework in which a document classified by first classifier as node 2, can only be seen by the node 2 classifier at the second level. 
異なるレベルの予測との不整合を防ぐために、最初の分類器によってノード2として分類された文書は、2番目のレベルでノード2分類器によってのみ表示されるフレームワークを開発できます。

_3.3.2_ _Local classifier per node. この方法は多くの研究で使用されている最も人気のある方法です。_ 
_3.3.2_ _ノードごとのローカル分類器。この方法は多くの研究で使用されている最も人気のある方法です。_

This method trains one binary classifier for each node of hierarchical class except root node. 
この方法は、ルートノードを除く階層クラスの各ノードに対して1つのバイナリ分類器をトレーニングします。

Figure. 6 shows that illustration of local classifier per node. 
図6は、ノードごとのローカル分類器の図を示しています。

There are a few issues with this strategy, first one is the hierarchical structure of local training sets is not taken into account. 
この戦略にはいくつかの問題があります。最初の問題は、ローカルトレーニングセットの階層構造が考慮されていないことです。

Secondly, it is restricted to issues where partial depth labeling examples involves. 
第二に、部分的な深さラベリングの例が関与する問題に制限されています。

The benefit of this method is that it is by default multi label that means it can predict several labels per class hierarchy. 
この方法の利点は、デフォルトでマルチラベルであり、クラス階層ごとに複数のラベルを予測できることです。

_3.3.3_ _Local classifier per level. この方法では、クラス階層の各レベルに対して1つのマルチクラス分類器をトレーニングします。_ 
_3.3.3_ _レベルごとのローカル分類器。この方法では、クラス階層の各レベルに対して1つのマルチクラス分類器をトレーニングします。_

This classification method has not been widely used in researches. 
この分類方法は、研究で広く使用されていません。

Figure. 7 shows that illustration of local classifier per level approach. 
図7は、レベルごとのローカル分類器アプローチの図を示しています。

Lets take this example, we have three classifier that will be trained to predict classes. 
この例を考えてみましょう。クラスを予測するためにトレーニングされる3つの分類器があります。

The training data are built in the same manner as the parent node method is applied in the local classifier. 
トレーニングデータは、ローカル分類器における親ノードメソッドが適用されるのと同じ方法で構築されます。

The disadvantage of this approach is the inconsistency problem it presents. 
このアプローチの欠点は、提示される不整合の問題です。

Fig. 7. Local classifier per level (each dashed rectangle represents a multiclass classifier). 
図7. レベルごとのローカル分類器（各破線の長方形はマルチクラス分類器を表します）。

Local classifier approaches are very efficient. 
ローカル分類器アプローチは非常に効率的です。

It uses hierarchical data information while preserving generality and smoothness. 
一般性と滑らかさを保ちながら、階層データ情報を使用します。

Nevertheless, the categorization method that have chosen, you could have a heavy final model in the end. 
それにもかかわらず、選択した分類方法によっては、最終的に重いモデルを持つ可能性があります。

In local classifier approach, there is also an issue of error propagation, which means if an error occur on first level, it will affect all the following ones down the hierarchy. 
ローカル分類器アプローチでは、エラー伝播の問題もあり、最初のレベルでエラーが発生すると、階層の下のすべてのレベルに影響を与えることを意味します。



## 4 提案手法とデータセット

In this section, we will discuss our proposed methodology and self created dataset for hierarchical text classification of urdu news. 
このセクションでは、ウルドゥー語ニュースの階層的テキスト分類のための提案手法と自己作成したデータセットについて説明します。

As shown in figure 8, our approach Hierarchical Multi-Layer LSTMs (HMLSTM) contains two parts that is Text Representing Layer (TRL) and Urdu Hierarchical LSTM Layer (UHLSTML). 
図8に示すように、私たちのアプローチである階層的マルチレイヤーLSTM（HMLSTM）は、テキスト表現層（TRL）とウルドゥー階層LSTM層（UHLSTML）の2つの部分から構成されています。

Mainly, we use the Text Representing Layer to achieve a unified representation of each urdu news text and the hierarchical category structure. 
主に、テキスト表現層を使用して、各ウルドゥー語ニューステキストと階層的カテゴリ構造の統一表現を達成します。

After this, we apply our deep neural model Urdu Hierarchical LSTM Layer (UHLSTML) to predict hierarchical categories and sub categories of urdu news text. 
その後、ウルドゥー階層LSTM層（UHLSTML）という深層ニューラルモデルを適用して、ウルドゥー語ニューステキストの階層的カテゴリとサブカテゴリを予測します。

**4.1** **テキスト表現層**

In first phase of our approach HMLSTM, text representing layer TRL purpose is to make a unified representation of each urdu news text and their hierarchy structure. 
私たちのアプローチHMLSTMの最初のフェーズでは、テキスト表現層TRLの目的は、各ウルドゥー語ニューステキストとその階層構造の統一表現を作成することです。

As we know, it is complicated for machine learning algorithms to use natural language directly. 
ご存知のように、機械学習アルゴリズムが自然言語を直接使用することは複雑です。

So we use embedding for this, which helps to convert words into a numeric representation. 
そのため、単語を数値表現に変換するのに役立つ埋め込みを使用します。

In TRL, an embedding layer is used to encode text. 
TRLでは、テキストをエンコードするために埋め込み層が使用されます。

We first convert urdu news text U into tokens and take hierarchical category labels L as an input. 
まず、ウルドゥー語ニューステキストUをトークンに変換し、階層的カテゴリラベルLを入力として受け取ります。

After this, we apply word2vec [24] embedding, word2vec requires list of tokens of a document then start vector encoding of tokens. 
その後、word2vec [24]埋め込みを適用します。word2vecはドキュメントのトークンのリストを必要とし、トークンのベクトルエンコーディングを開始します。

The fundamental principle of Word2vec is that rather than representing words as one-hot encoding i.e tf-idf vectorizer in high dimensional space, we define words in dense low dimensional space in such a way that identical words get identical word vectors, such that they are projected to adjacent points. 
Word2vecの基本原則は、単語をワンホットエンコーディング、すなわち高次元空間のtf-idfベクトライザーとして表現するのではなく、同一の単語が同一の単語ベクトルを得るように、密な低次元空間で単語を定義することです。その結果、同一の単語は隣接する点に投影されます。

It learns to represent words with similar meanings using similar vectors. 
それは、類似の意味を持つ単語を類似のベクトルを使用して表現することを学習します。

Word2vec accepts text corpus as an input and converts text into numerical data which will later pass it to our model as an input. 
Word2vecはテキストコーパスを入力として受け入れ、テキストを数値データに変換し、後でそれを私たちのモデルの入力として渡します。

We can formulize urdu news text U as a sequence of N words $U = (v_1, v_2, \ldots, v_N)$ where $u_i \in R^h$ is initialized by h-dimensional of the feature vectors with Word2vec. 
ウルドゥー語ニューステキストUをN語のシーケンスとして定式化できます。$U = (v_1, v_2, \ldots, v_N)$ ここで、$u_i \in R^h$はWord2vecによるh次元の特徴ベクトルで初期化されます。

As our approach is supervised learning we have labeled data in the form of categories and sub categories. 
私たちのアプローチは教師あり学習であるため、カテゴリとサブカテゴリの形でラベル付きデータがあります。

Our proposed model UHLSTML take hierarchical category structure labels L as an input. 
私たちの提案したモデルUHLSTMLは、階層的カテゴリ構造ラベルLを入力として受け取ります。

We can formulize labels L as a sequence of 12 classes. $L = (l_1, l_2, \ldots, l_{12})$. 
ラベルLを12クラスのシーケンスとして定式化できます。$L = (l_1, l_2, \ldots, l_{12})$。

So similar to word2vec, we have to convert categorical data into numerical data. 
したがって、word2vecと同様に、カテゴリデータを数値データに変換する必要があります。

There are several methods to transform categorical values to numerical values. 
カテゴリ値を数値値に変換するためのいくつかの方法があります。

Every method has certain effects on the feature set. 
各方法は特徴セットに特定の影響を与えます。

Here we are using label encoding for categories and sub categories labels. 
ここでは、カテゴリとサブカテゴリラベルのためにラベルエンコーディングを使用しています。

As we have 12 classes, 3 categories and 9 sub categories. 
私たちには12クラス、3カテゴリ、9サブカテゴリがあります。

Label encoding convert these labels in machine readable form. 
ラベルエンコーディングは、これらのラベルを機械可読形式に変換します。

So, Label L is an input vector which has integers representing various classes in the data. 
したがって、ラベルLはデータ内のさまざまなクラスを表す整数を持つ入力ベクトルです。

As already discussed, UHLSTML is deep neural model, it works well if we have classes distributed in a binary matrix. 
すでに述べたように、UHLSTMLは深層ニューラルモデルであり、クラスがバイナリ行列に分散している場合にうまく機能します。

So, we convert label class vectors (ordinal numbers) to binary matrix so that our labels are easily understandable by UHLSTML. 
したがって、ラベルクラスベクトル（順序数）をバイナリ行列に変換し、UHLSTMLがラベルを簡単に理解できるようにします。

For this, we have used tensorflow keras [6] to-categorical which converts a class vector (integers) to a matrix of binary values (either ‘1’ or ‘0’). 
これには、クラスベクトル（整数）をバイナリ値の行列（‘1’または‘0’）に変換するtensorflow keras [6]のto-categoricalを使用しました。

After this our text representation layer obtained whole representation of data and achieved a unified representation of each urdu news text and the hierarchical category structured labels, we pass it towards our propose model UHLSTML. 
これにより、私たちのテキスト表現層はデータの全体的な表現を取得し、各ウルドゥー語ニューステキストと階層的カテゴリ構造ラベルの統一表現を達成し、それを提案モデルUHLSTMLに渡します。

**4.2** **ウルドゥー階層LSTM層**

Urdu Hierarchical LSTM layer is based on Hierarchically-Structured Local Classifiers approach in which we have Local classifier per level method. 
ウルドゥー階層LSTM層は、階層構造ローカル分類器アプローチに基づいており、各レベルにローカル分類器を持つ方法です。

In this method we train one LSTM layer for each level of the class hierarchy as shown in figure 9. 
この方法では、図9に示すように、クラス階層の各レベルに対して1つのLSTM層をトレーニングします。

After receiving combined and structured representation of urdu news text and labels, we propose UHLSTML, an end-to-end fully connected deep LSTMs network to perform automatic feature learning. 
ウルドゥー語ニューステキストとラベルの結合された構造化表現を受け取った後、私たちは自動特徴学習を行うためのエンドツーエンドの完全接続深層LSTMネットワークであるUHLSTMLを提案します。

It is based on recurrent neural networks architecture. 
これは再帰神経ネットワークアーキテクチャに基づいています。

Figure 10 shows the architecture of the proposed network, which has two LSTM layers, one LSTM layer for top categories and second LSTM layer for sub categories and a softmax layer that gives the predictions. 
図10は、提案されたネットワークのアーキテクチャを示しており、2つのLSTM層、1つはトップカテゴリ用、もう1つはサブカテゴリ用のLSTM層、予測を提供するソフトマックス層があります。

First layer will also be used as feedforward layer, it learns the features of top level category that is sports, technology and entertainment and forward all these features to second LSTM layer. 
最初の層はフィードフォワード層としても使用され、スポーツ、テクノロジー、エンターテインメントというトップレベルカテゴリの特徴を学習し、これらのすべての特徴を第二のLSTM層に転送します。

The input layer contains text features. 
入力層にはテキスト特徴が含まれています。

We pass input which is urdu news text U to first LSTM layer which learns features of top category and gives output of y. 
ウルドゥー語ニューステキストUを最初のLSTM層に渡し、トップカテゴリの特徴を学習し、出力yを生成します。

First LSTM layer is used for first level of classification. 
最初のLSTM層は、分類の最初のレベルに使用されます。

After this, we pass these features as an input to second LSTM layer. 
その後、これらの特徴を第二のLSTM層への入力として渡します。

The second level classification in the hierarchy consists of a trained top category. 
階層内の第二レベルの分類は、トレーニングされたトップカテゴリで構成されています。

In second LSTM layer, each second level hierarchy is connected to the output of the first level. 
第二のLSTM層では、各第二レベルの階層が第一レベルの出力に接続されています。

Let’s take an example in this case, if the output of our first LSTM is labeled as Sports then the second LSTM is trained only with all sports related news like football, hockey and cricket. 
この場合の例を考えてみましょう。最初のLSTMの出力がスポーツとしてラベル付けされている場合、第二のLSTMはサッカー、ホッケー、クリケットなどのすべてのスポーツ関連ニュースでのみトレーニングされます。

Which means first level LSTM is trained with all news whereas second level LSTM will only trained with the news of specific category. 
つまり、第一レベルのLSTMはすべてのニュースでトレーニングされるのに対し、第二レベルのLSTMは特定のカテゴリのニュースのみでトレーニングされます。

The LSTMs in this research are trained with a standardized back propagation algorithm that uses ReLU as an activation function and a softmax layer that gives the output. 
この研究のLSTMは、ReLUを活性化関数として使用し、出力を提供するソフトマックス層を持つ標準化されたバックプロパゲーションアルゴリズムでトレーニングされています。

Optimizer that we used is Adam having learning rate 0.001. 
私たちが使用したオプティマイザーは、学習率0.001のAdamです。

To calculate loss, categorical crossentropy is used. 
損失を計算するために、カテゴリカルクロスエントロピーが使用されます。

LSTM dropout is applied to the last LSTM layer to reduce over fitting and allow extra efficient learning. 
LSTMドロップアウトは、過学習を減らし、より効率的な学習を可能にするために、最後のLSTM層に適用されます。

**4.3** **提案データセット**

In supervised learning, the performance of the model mainly relies on dataset. 
教師あり学習において、モデルの性能は主にデータセットに依存します。

The learning of a neural network relies on the dataset and if there is less amount of dataset, the learning will be insufficient and it will decrease the accuracy of model. 
ニューラルネットワークの学習はデータセットに依存し、データセットの量が少ない場合、学習は不十分になり、モデルの精度が低下します。

There are alot of publicly available dataset like Reuters-21578, 20 Newsgroups and RCV1 for english news but there is limited amount of large dataset for urdu news. 
Reuters-21578、20 Newsgroups、RCV1などの英語ニュース用の公開データセットは多数ありますが、ウルドゥー語ニュース用の大規模データセットは限られています。

So large datasets are required to perform various natural language tasks and applications. 
したがって、さまざまな自然言語タスクやアプリケーションを実行するには、大規模なデータセットが必要です。

To provide a suitable dataset for model training and evaluation of model results, we created a urdu news corpus which is named as Urdu News Dataset for Hierarchical Text Classification (UNDHTC) which will be publicly available at github [2]. 
モデルのトレーニングとモデル結果の評価のために適切なデータセットを提供するために、ウルドゥー語ニュースコーパスを作成しました。これは「ウルドゥー語ニュースデータセット階層的テキスト分類用（UNDHTC）」と名付けられ、github [2]で公開される予定です。

The main goal of corpus development is to make use of it in comparison and evaluation in hierarchical classification and to help researchers in future to perform NLP tasks. 
コーパス開発の主な目標は、階層的分類における比較と評価に利用し、将来の研究者がNLPタスクを実行するのを助けることです。

UNDHTC is classified into 12 categories that is 3 categories Sports, Technology and Entertainment which is further classified into 9 sub categories cricket, hockey, football, applications, mobile, internet, music, fashion and movies as shown in figure 11. 
UNDHTCは、スポーツ、テクノロジー、エンターテインメントの3つのカテゴリに分類され、さらにクリケット、ホッケー、サッカー、アプリケーション、モバイル、インターネット、音楽、ファッション、映画の9つのサブカテゴリに分類されています（図11参照）。

_4.3.1_ _データセット作成。最も多くのデータは、人気のあるパキスタンのウルドゥー語ニュースウェブサイトから収集されました_ 
_（Daily Pakistan[3]、Urdupoint[4]、Express news[5]、Dawn news[6]、BBC Urdu[7]、ARYnews[8]、BOL news[9]、Hum news[10]）。データの収集を自動化するために、Chromeウェブブラウザ用のChromeドライバーを使用してSeleniumを使用しました。_

_4.3.2_ _注釈。データセットのラベルは12のカテゴリに分かれています。_ 
_私たちは、ウルドゥー語に関する確固たる知識を持つ同僚の支援を受けてデータセットにラベルを付けました。データの注釈のために、適切な指示と例を提供しました。ラベルは文の文脈と主題に応じて割り当てられました。_

_4.3.3_ _データセット統計。約299815件のニュースが_ 
_異なるウェブサイトからスクレイピングツールを使用して抽出されました。57566件のニュースがクリーンアップされ、ラベル付けされ、表1に示すように、カテゴリ内の文書の総数は表2に示されています。次のセクションでは、実験について説明します。_

**表1. データセット統計**
**Dataset Statistics**
Total News 299815 Cleaned 57566 Labeled 51325

**表2**



. In next section, we will discuss experiments that
次のセクションでは、実施した実験について議論します。

Table 1. Dataset Statics
表1. データセットの統計

**Dataset Statistics**
**データセット統計**
Total News 299815 Cleaned 57566 Labeled 51325
総ニュース数 299,815件 クリーンデータ 57,566件 ラベル付けデータ 51,325件

Table 2. Dataset Stats in Detail
表2. データセットの詳細な統計

**Category** **Sub Category** **Number of documents** **Total**
**カテゴリ** **サブカテゴリ** **文書数** **合計**
Cricket 12431 Sports Hockey 2011 20002 Football 5560
クリケット 12,431件 スポーツ ホッケー 2,011件 20,002件 サッカー 5,560件
Internet 1735 Technology Applications 3742 16208 Mobile 10731
インターネット 1,735件 テクノロジー アプリケーション 3,742件 16,208件 モバイル 10,731件
Movies 3902 Entertainment Music 2552 15115 Fashion 8661
映画 3,902件 エンターテインメント 音楽 2,552件 15,115件 ファッション 8,661件

were performed on this dataset and also compare results with baseline methods.
このデータセットで実施され、ベースライン手法との結果を比較します。



## 5 EXPERIMENTS 実験

In this section, we first introduce the dataset and apply preprocessing steps. 
このセクションでは、まずデータセットを紹介し、前処理ステップを適用します。

Then we conduct extensive experiments and compare our proposed approach with state-of-the-art traditional machine learning algorithms and deep neural model. 
次に、広範な実験を行い、提案したアプローチを最先端の従来の機械学習アルゴリズムおよび深層ニューラルモデルと比較します。

In the end we will discuss experimental results. 
最後に、実験結果について議論します。

Figure 12 shows complete flow diagram of our experiment. 
図12は、私たちの実験の完全なフローダイアグラムを示しています。

The total number of 57566 news were used in this experiment. 
この実験では、57566件のニュースが使用されました。

UNDHTC dataset is manually labeled which are divided into total 12 categories which contain 3 top categories and 9 sub categories. 
UNDHTCデータセットは手動でラベル付けされており、合計12のカテゴリに分かれており、3つの主要カテゴリと9つのサブカテゴリが含まれています。

The training/test split for UNDHTC is done by ourselves, which is 80% for training and 20% for test as shown in table 3. 
UNDHTCのトレーニング/テストの分割は私たち自身で行い、トレーニングに80%、テストに20%を使用します（表3に示されています）。

We randomly sample 20% from the training data. 
トレーニングデータからランダムに20%をサンプリングします。

Table 3. The training/test split for UNDHTC 
表3. UNDHTCのトレーニング/テストの分割

**Dataset** **Training** **Testing** **Class/Labels**  
**データセット** **トレーニング** **テスト** **クラス/ラベル**  
51325 41060 10265 12  
-----
111:16 Taimoor and Waseem, et al.  
図12. 実験フローダイアグラム。  

**5.1** **Preprocessing**  
**5.1** **前処理**  

We have applied basic pre-processing methods on our data. 
私たちはデータに基本的な前処理方法を適用しました。

Data pre-processing in every language is an essential step taken before applying any machine learning algorithm or deep neural network. 
すべての言語におけるデータ前処理は、機械学習アルゴリズムや深層ニューラルネットワークを適用する前に行う重要なステップです。

It helps to remove unnecessary data in the corpus. 
これはコーパス内の不要なデータを削除するのに役立ちます。

English characters, special symbols, numeric values, and URLs are omitted such that the text includes only the target Urdu language. 
英語の文字、特殊記号、数値、およびURLは省略され、テキストにはターゲットのウルドゥー語のみが含まれるようにします。

The structured representation of text data is efficiently controlled to improve the experiment’s accuracy and efficiency. 
テキストデータの構造化された表現は、実験の精度と効率を向上させるために効率的に制御されます。

Preprocessing steps that we applied on our dataset are as follows. 
私たちがデータセットに適用した前処理ステップは以下の通りです。

_5.1.1_ _Tokenization. This is the initial step in the processing of any language of the NLP task. It_ transforms the phrases into valuable tokens or a single expression. 
_5.1.1_ _トークン化。これはNLPタスクの任意の言語の処理における初期ステップです。これはフレーズを価値のあるトークンまたは単一の表現に変換します。_

It transforms raw text into a tokens chart, in which every token is a Word. 
生のテキストをトークンチャートに変換し、各トークンが単語になります。

Inaccurate tokenization can affect the results of the experiment. 
不正確なトークン化は実験の結果に影響を与える可能性があります。

Urdu is a less linguistic tool and its signs face different problems as spatial incoherence between terms and sentence limit detection. 
ウルドゥー語は言語的なツールが少なく、その記号は用語間の空間的不整合や文の限界検出などの異なる問題に直面します。

Here is a figure 13 which show urdu text converted into tokens. 
ここに、ウルドゥー語のテキストがトークンに変換された図13があります。

_5.1.2_ _Stop Words Removal. To remove unnecessary words we use stop words. It is used for removing_ words that carry little to no meaning. 
_5.1.2_ _ストップワードの削除。不要な単語を削除するためにストップワードを使用します。これは意味をほとんど持たない単語を削除するために使用されます。_

Natural languages are consist of meaningless words and functional words. 
自然言語は無意味な単語と機能的な単語で構成されています。

In Urdu, we call stopwords as Haroof-e-Jar and in English they are called conjunctions. 
ウルドゥー語ではストップワードをHaroof-e-Jarと呼び、英語では接続詞と呼ばれます。

Stop words are often omitted from the corpus before NLP is done. 
ストップワードはNLPが行われる前にコーパスから省略されることがよくあります。

By removing these words, we can get better results in our research work.  
これらの単語を削除することで、研究作業でより良い結果を得ることができます。  

-----
Hierarchical Text Classification of Urdu News using Deep Neural Network 111:17  
図13. ウルドゥー語のトークン化された文書  

_5.1.3_ _Punctuation Removing. In Urdu, mostly used punctuation are ‘-‘, ’_’, and ‘.’. Such symbols do_ not have much value to be used as a feature for classification tasks. 
_5.1.3_ _句読点の削除。ウルドゥー語で主に使用される句読点は「-」、「_」、および「。」です。これらの記号は_ 分類タスクの特徴として使用するにはあまり価値がありません。_

So we remove these symbols by using regular expressions. 
したがって、正規表現を使用してこれらの記号を削除します。

**5.2** **Experimental Setup**  
**5.2** **実験設定**  

All of our experiments were run on 6 core Intel Core i7 9750 @2.60GHz, with 16 GB RAM and GTX 1660ti GPU. 
私たちのすべての実験は、6コアのIntel Core i7 9750 @2.60GHz、16GB RAM、およびGTX 1660ti GPUで実行されました。

The software that we used is jupyter notebook having Python 3.7.6. 
私たちが使用したソフトウェアは、Python 3.7.6を搭載したJupyter Notebookです。

In our experiments, we used public version of word2vec in which training algorithm CBOW is used to train 100 dimensional word embeddings with minimum count of words 5, filter window size is 5 and other default parameters. 
私たちの実験では、単語の最小カウントが5、フィルタウィンドウサイズが5、その他のデフォルトパラメータを使用して、トレーニングアルゴリズムCBOWを使用して100次元の単語埋め込みをトレーニングするpublic versionのword2vecを使用しました。

For deep learning model, the parameters of training the models were set as batch size 32, drop out 0.5 and other default parameters. 
深層学習モデルでは、モデルのトレーニングパラメータをバッチサイズ32、ドロップアウト0.5、その他のデフォルトパラメータに設定しました。

Data was trained on 80% for training and 20% randomly selected for test as shown in table 3. 
データはトレーニングのために80%でトレーニングされ、テストのためにランダムに選択された20%でトレーニングされました（表3に示されています）。

We have done our hardest to use the best parameters in our experiments. 
私たちは実験で最良のパラメータを使用するために最善を尽くしました。

**5.3** **Baselines and Deep Neural Model Comparison**  
**5.3** **ベースラインと深層ニューラルモデルの比較**  

We compare our proposed approach HMLSTM with several baseline methods, such as Naïve Bayes, Support Vector Machines (SVMs), Decision Tree, Random Forest, K-Nearest Neighbors, Logistic Regression and deep neural model such as convolutional neural network (CNN). 
私たちは提案したアプローチHMLSTMを、Naïve Bayes、サポートベクターマシン（SVM）、決定木、ランダムフォレスト、K近傍法、ロジスティック回帰、深層ニューラルモデル（畳み込みニューラルネットワーク（CNN）など）と比較します。

- Gaussian Naïve Bayes : We have used global approach in this method that builds a single decision tree to classify all categories simultaneously. 
- ガウスナイーブベイズ：この方法では、すべてのカテゴリを同時に分類する単一の決定木を構築するグローバルアプローチを使用しました。

In this method, we first convert urdu news text in the form of words. 
この方法では、まずウルドゥー語のニューステキストを単語の形に変換します。

After this we use one hot encoding to encode those words. 
その後、ワンホットエンコーディングを使用してそれらの単語をエンコードします。

We encode both columns category and sub category having labels by using label encoding. 
ラベルエンコーディングを使用して、カテゴリとサブカテゴリの両方の列をラベル付きでエンコードします。

Then we combine both the labels (category and subcategory) in a single variable. 
次に、両方のラベル（カテゴリとサブカテゴリ）を単一の変数に結合します。

After that, we split the dataset to the train and the test parts. 
その後、データセットをトレーニング部分とテスト部分に分割します。

Then we apply GaussianNB algorithm using binary relevance with default parameters in which variance is 1.0 raise to power -9 and perform predictions. 
次に、分散が$1.0 \times 10^{-9}$であるデフォルトパラメータを使用してバイナリ関連性を用いたGaussianNBアルゴリズムを適用し、予測を行います。

skmultilearn library is used in it [29]. 
これにはskmultilearnライブラリが使用されています[29]。

- Support Vector Machines (SVMs): In this method, we perform standard multi-label classification using one-vs-the-rest (OvR) strategy because we have multiple labels, so we use it. 
- サポートベクターマシン（SVM）：この方法では、複数のラベルがあるため、one-vs-the-rest（OvR）戦略を使用して標準的なマルチラベル分類を行います。

Scikit-learn is a pipeline framework for automating workflows for training. 
Scikit-learnは、トレーニングのワークフローを自動化するためのパイプラインフレームワークです。

In machine learning applications, pipelines are very common because there are many data to manipulate and many transformations to be carried out. 
機械学習アプリケーションでは、操作するデータが多く、実行する変換が多いため、パイプラインは非常に一般的です。

So we used pipeline to train OnevsRest classifier. 
そのため、OnevsRest分類器をトレーニングするためにパイプラインを使用しました。

We use LinearSVC with OneVsRestClassifier and other default parameters. 
LinearSVCをOneVsRestClassifierおよびその他のデフォルトパラメータと共に使用します。

- Decision Tree: In this method, we also used global approach strategy. 
- 決定木：この方法でも、グローバルアプローチ戦略を使用しました。

Data Reading is done using Pandas. 
データの読み取りはPandasを使用して行います。

We first convert urdu news text in the form of tokens. 
まず、ウルドゥー語のニューステキストをトークンの形に変換します。

After this we use word2vec embedding to encode those words. 
その後、word2vec埋め込みを使用してそれらの単語をエンコードします。

For labels, we use label encoding. 
ラベルにはラベルエンコーディングを使用します。

Label encoding convert these labels into vectors. 
ラベルエンコーディングはこれらのラベルをベクトルに変換します。

As, we have multiple labels so we used multilabel classification. 
複数のラベルがあるため、マルチラベル分類を使用しました。

Multilabel classification tasks can be handled using decision trees. 
マルチラベル分類タスクは決定木を使用して処理できます。

In Decision Tree Classifier, we set criterion=’entropy’ and remaining parameters are set as default and perform predictions. 
決定木分類器では、criterionを「entropy」に設定し、残りのパラメータをデフォルトに設定して予測を行います。

sklearn library [25] is used for classification.  
分類にはsklearnライブラリ[25]が使用されます。  

-----
111:18 Taimoor and Waseem, et al.  
- Random Forest: Random forest is also used for multilabel classification task. 
- ランダムフォレスト：ランダムフォレストもマルチラベル分類タスクに使用されます。

So we used this method in hierarchical text classification. 
したがって、階層的テキスト分類にこの方法を使用しました。

Random Forest can inherently deal with multiclass datasets. 
ランダムフォレストは本質的にマルチクラスデータセットを扱うことができます。

As a result, we adopted a one-versus-rest strategy using random forest classifier. 
その結果、ランダムフォレスト分類器を使用してone-versus-rest戦略を採用しました。

Regular Random Forest cannot perform well on multilabel classification [1]. 
通常のランダムフォレストはマルチラベル分類でうまく機能しません[1]。

Experimental results shows better classification performances with one versus all classifier. 
実験結果は、one versus all分類器でより良い分類性能を示しています。

In random forest, we set parameters as default and perform predictions. 
ランダムフォレストでは、パラメータをデフォルトに設定し、予測を行います。

- K-Nearest Neighbors: In this method, we first convert data and labels into vectors by using embedding and label encoding. 
- K近傍法：この方法では、まず埋め込みとラベルエンコーディングを使用してデータとラベルをベクトルに変換します。

After that, we split the dataset to the train and the test parts then apply k-nearest neighbors (KNN) algorithm. 
その後、データセットをトレーニング部分とテスト部分に分割し、k近傍法（KNN）アルゴリズムを適用します。

We set number of neighbors 3 with other default parameters and perform predictions. 
隣接数を3に設定し、その他のデフォルトパラメータで予測を行います。

- Logistic Regression: In this method, we also perform standard multi-label classification using one-vs-the-rest (OvR) strategy. 
- ロジスティック回帰：この方法でも、one-vs-the-rest（OvR）戦略を使用して標準的なマルチラベル分類を行います。

Scikit-learn [25] is a pipeline framework for automating workflows for training. 
Scikit-learn [25]は、トレーニングのワークフローを自動化するためのパイプラインフレームワークです。

Here we also used pipeline to train OnevsRest classifier and apply logistic regression on data. 
ここでも、OnevsRest分類器をトレーニングするためにパイプラインを使用し、データにロジスティック回帰を適用しました。

L2 regularization is applied in logistic regression with other default parameters and perform predictions. 
ロジスティック回帰ではL2正則化が適用され、その他のデフォルトパラメータで予測を行います。

- Convolutional Neural Network: In CNN, we first convert urdu news text in the form of tokens. 
- 畳み込みニューラルネットワーク：CNNでは、まずウルドゥー語のニューステキストをトークンの形に変換します。

After this we use word2vec embedding to encode those words. 
その後、word2vec埋め込みを使用してそれらの単語をエンコードします。

Then we apply CNN on our dataset, we pass the kernel over these embeddings to find convolutions. 
次に、データセットにCNNを適用し、これらの埋め込みにカーネルを通して畳み込みを見つけます。

CNN model is trained with two layers, one is convolution and other is softmax layer. 
CNNモデルは、1つは畳み込み層、もう1つはソフトマックス層の2層でトレーニングされます。

We also applied “relu” activation layer on the output of every neuron. 
また、すべてのニューロンの出力に「relu」活性化層を適用しました。

Drop out layer is also applied to reduce overfitting. 
ドロップアウト層も適用して過学習を減少させます。

**5.4** **Evaluation Metrics**  
**5.4** **評価指標**  

To evaluate the performance of algorithms we have used three common evaluation metrics i.e. 
アルゴリズムの性能を評価するために、私たちは3つの一般的な評価指標を使用しました。すなわち、

Precision, Recall, and F1 score which includes Micro-F1 and Macro-F1. 
精度、再現率、F1スコア（Micro-F1およびMacro-F1を含む）です。

We also used Classification Accuracy, which is also known as term accuracy. 
また、分類精度（用語精度とも呼ばれる）も使用しました。

Let 𝑇𝑃𝑙, 𝐹𝑃𝑙, 𝐹𝑁𝑙 be the number of true positives, false positives and false negatives for the l-th label in the category C respectively. 
$TP_l, FP_l, FN_l$を、カテゴリ$C$における$l$番目のラベルの真陽性、偽陽性、偽陰性の数とします。

Then the equation of Micro-F1 is  
次に、Micro-F1の式は次のようになります。

$$
P = \frac{\sum_{l \in C} TP_l}{\sum_{l \in C} TP_l + FP_l}, \quad R = \frac{\sum_{l \in C} TP_l}{\sum_{l \in C} TP_l + FN_l}, \quad F1_{Micro} = \frac{2P \cdot R}{P + R}
$$

Equation for Macro-F1 is defined as  
Macro-F1の式は次のように定義されます。

$$
P_l = \frac{TP_l}{TP_l + FP_l}, \quad R_l = \frac{TP_l}{TP_l + FN_l}, \quad F1_{Macro} = \frac{1}{|C|} \sum_{l \in C} \frac{2P_l R_l}{P_l + R_l}
$$

**5.5** **Qualitative Analysis**  
**5.5** **定性的分析**  

To measure the performance of algorithms across different examples, we summarizes some of the examples from evaluation set as shown in figure 14. 
アルゴリズムの性能を異なる例で測定するために、評価セットからのいくつかの例を図14に示します。

We can see that HMLSTM works well in most of the cases because LSTM can look back to many time steps which means it retain long term memory when dealing with long sentences. 
HMLSTMはほとんどのケースでうまく機能していることがわかります。なぜなら、LSTMは多くの時間ステップを振り返ることができ、長い文を扱う際に長期記憶を保持するからです。

In first example, we can see that all baseline approaches fails, but HMLSTM and CNN predict correctly. 
最初の例では、すべてのベースラインアプローチが失敗しているのがわかりますが、HMLSTMとCNNは正しく予測しています。

However our model still needs improvement, as we can see in second example our model fails because it didn’t consider context of news due to presence of keywords like actor and drama. 
しかし、私たちのモデルはまだ改善が必要です。2番目の例では、俳優やドラマのようなキーワードの存在により、ニュースの文脈を考慮しなかったため、モデルが失敗しています。

**5.6** **Experimental Results**  
**5.6** **実験結果**  

To demonstrate practical significance of our proposed model, we compare HMLSTM with all the baselines. 
提案したモデルの実用的な重要性を示すために、HMLSTMをすべてのベースラインと比較します。

The experiments perform on urdu news dataset (UNDHTC) shows that our proposed approach Hierarchical Multi-Layer LSTMs (HMLSTM) outperforms the machine learning models. 
ウルドゥー語ニュースデータセット（UNDHTC）での実験は、提案したアプローチである階層型マルチレイヤーLSTM（HMLSTM）が機械学習モデルを上回ることを示しています。

-----
Hierarchical Text Classification of Urdu News using Deep Neural Network 111:19  
図14. HMLSTMの結果と他のベースライン手法の定性的分析  

Table 4. HMLSTM and other model Results on Urdu News Dataset  
表4. HMLSTMおよび他のモデルのウルドゥー語ニュースデータセットにおける結果  

Methods #Classes Accuracy Precision Recall Macro-F1 Micro-F1  
手法 クラス数 精度 精度 再現率 Macro-F1 Micro-F1  
Gaussian Naïve Bayes 12 0.4744 0.4223 0.8693 0.5257 0.6987  
Support Vector Machines 12 0.7711 0.7434 0.7769 0.7590 0.8878  
Decision Tree 12 0.7285 0.6113 0.6092 0.6102 0.7949  
Random Forest 12 0.7959 0.9256 0.6331 0.7391 0.8806  
K-Nearest Neighbors 12 0.5989 0.6300 0.5668 0.5467 0.6940  
Logistic Regression 12 0.7962 0.7875 0.7822 0.7848 0.8980  
CNN 12 0.8740 0.8866 0.8496 0.8632 0.9323  
HMLSTM 12 **0.9402** **0.9259** **0.8812** **0.8927** **0.9683**  

The table 4 shows comprehensive results of all models. 
表4は、すべてのモデルの包括的な結果を示しています。

CNN performed well and gave promising result as compare to state-of-the-art methods. 
CNNは良好なパフォーマンスを発揮し、最先端の手法と比較して有望な結果を示しました。



. CNN performed well and gave promising result as compare to state-of-the-art methods. 
CNNは良好な性能を示し、最先端の手法と比較して有望な結果をもたらしました。

For traditional text classification algorithms, we can see that Logistic Regression using one-vs-the-rest (OvR) strategy and applying regularization, it outperform other models. 
従来のテキスト分類アルゴリズムでは、one-vs-the-rest (OvR) 戦略を使用し、正則化を適用したロジスティック回帰が他のモデルを上回ることがわかります。

Then we have Support Vector Machines after LR, which is performing better than other four algorithms. 
次に、ロジスティック回帰の後にサポートベクターマシン（SVM）があり、これは他の4つのアルゴリズムよりも優れた性能を発揮しています。

SVM is good in performing multi label classification, that is why its better than rest. 
SVMはマルチラベル分類を行うのに優れているため、他の手法よりも優れています。

While K nearest neighbor perform least on urdu news dataset. 
一方、K近傍法はウルドゥー語のニュースデータセットで最も低い性能を示します。

By splitting labels according to their levels, we evaluate causes of performance gains. 
ラベルをそのレベルに応じて分割することにより、性能向上の原因を評価します。

Table 4 indicates Macro-F1 variations between the base models. 
表4は、基本モデル間のMacro-F1の変動を示しています。

HMLSTM achieves the best results in all evaluation metrics, which shows HMLSTM is more competent for doing hierarchical multi label. 
HMLSTMはすべての評価指標で最良の結果を達成しており、HMLSTMが階層的マルチラベル分類においてより優れていることを示しています。

-----
111:20 Taimoor and Waseem, et al. 
-----
Fig. 15. Results showing Accuracy, Macro-F1 and Micro-F1 
図15. 精度、Macro-F1、およびMicro-F1を示す結果

text classification tasks with hierarchical group structure and it deal with hierarchical category adequately and correctly. 
階層的グループ構造を持つテキスト分類タスクであり、階層的カテゴリを適切かつ正確に扱います。

The main reason is that HMLSTM could identify the correlations between the Urdu news texts and labels, while other algorithms can’t. 
主な理由は、HMLSTMがウルドゥー語のニューステキストとラベルの相関関係を特定できるのに対し、他のアルゴリズムはできないことです。

HMLSTM integrate the predictions of every level in the form of hierarchical structure. 
HMLSTMは、階層構造の形で各レベルの予測を統合します。

The bar chart as shown in figure 16 clearly 
図16に示されている棒グラフは明確に

-----
Fig. 16. Hierarchical Multi-Layer LSTMs (HMLSTM) Results  
図16. 階層的マルチレイヤーLSTM（HMLSTM）の結果

-----
Hierarchical Text Classification of Urdu News using Deep Neural Network 111:21 
深層ニューラルネットワークを用いたウルドゥー語ニュースの階層的テキスト分類

demonstrates the effectiveness of our proposed approach for hierarchical text classification. 
私たちの提案したアプローチが階層的テキスト分類において効果的であることを示しています。



## 6 CONCLUSION AND FUTURE WORK 結論と今後の課題

In this paper, we have proposed Hierarchical Multi-Layer LSTMs method built upon deep neural network which is used for hierarchical text classification of urdu news text. 
本論文では、ウルドゥー語のニューステキストの階層的テキスト分類に使用される深層ニューラルネットワークに基づいた階層的マルチレイヤーLSTM手法を提案しました。

We first applied Text Representing Layer for obtaining numeric representation of text and categories by applying embedding. 
まず、埋め込みを適用してテキストとカテゴリの数値表現を取得するために、テキスト表現層を適用しました。

After receiving combined and structured representation of urdu news text and labels, we applied Urdu Hierarchical LSTM Layer, an end-to-end fully connected deep LSTMs network to perform automatic feature learning. 
ウルドゥー語のニューステキストとラベルの結合された構造化表現を受け取った後、エンドツーエンドの完全接続型深層LSTMネットワークであるウルドゥー階層LSTM層を適用して、自動特徴学習を行いました。

Finally, extensive experiments is performed on our self created dataset named as Urdu news dataset for hierarchical text classification. 
最後に、階層的テキスト分類のために「ウルドゥーニュースデータセット」と名付けた自己作成データセットで広範な実験を行いました。

Our experimental results clearly demonstrate that our method outperforms baseline methods significantly and also performed well as compare to neural model CNN. 
私たちの実験結果は、私たちの手法がベースライン手法を大幅に上回り、ニューラルモデルCNNと比較しても良好な性能を示すことを明確に示しています。

In the future, we are interested to concentrate further on improving the network structure in order to further improve the efficiency of our method. 
今後は、私たちの手法の効率をさらに向上させるために、ネットワーク構造の改善にさらに注力したいと考えています。

We will also try to develop Bi-LSTM based approach to to obtain improved hierarchical structure. 
また、改善された階層構造を得るために、Bi-LSTMベースのアプローチを開発しようと考えています。

In future, we will also try to optimize our model because it takes long training time. 
将来的には、トレーニング時間が長いため、モデルの最適化にも取り組む予定です。

**REFERENCES 参考文献**
[1] Md Nasim Adnan and Md Zahidul Islam. 2015. One Vs All Binarization Technique in the Context of Random Forest. In _ESANN 2015 proceedings. i6doc.com publication, Belgium, 385–390._  
[2] Fawaz S Al-Anzi and Dia AbuZeina. 2018. Beyond vector space model for hierarchical Arabic text classification: A Markov chain approach. Information Processing & Management 54, 1 (2018), 105–115.  
[3] Abbas Raza Ali and Maliha Ijaz. 2009. Urdu Text Classification. In Proceedings of the 7th International Conference on _Frontiers of Information Technology. Association for Computing Machinery, New York, NY, USA, 7._  
[4] Muhammad Nabeel Asim, Muhammad Usman Ghani, Muhammad Ali Ibrahim, Waqar Mahmood, Andreas Dengel, and Sheraz Ahmed. 2020. Benchmarking performance of machine and deep learning-based methodologies for Urdu text document classification. arXiv e-prints (2020), arXiv–2003.  
[5] Shaojie Bai, J. Zico Kolter, and Vladlen Koltun. 2018. An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling. CoRR abs/1803.01271 (2018). http://arxiv.org/abs/1803.01271  
[6] François Chollet et al. 2015. Keras. https://keras.io.  
[7] Ali Daud, Wahab Khan, and Dunren Che. 2017. Urdu language processing: a survey. Artificial Intelligence Review 47, 3 (2017), 279–311.  
[8] Ashraf Elnagar, Ridhwan Al-Debsi, and Omar Einea. 2020. Arabic text classification using deep learning models. _Information Processing & Management 57, 1 (2020), 102121._  
[9] J. Gong, Z. Teng, Q. Teng, H. Zhang, L. Du, S. Chen, M. Z. A. Bhuiyan, J. Li, M. Liu, and H. Ma. 2020. Hierarchical Graph Transformer-Based Deep Learning Model for Large-Scale Multi-Label Text Classification. IEEE Access 8 (2020), 30885–30896.  
[10] Wei Huang, Enhong Chen, Qi Liu, Yuying Chen, Zai Huang, Yang Liu, Zhou Zhao, Dan Zhang, and Shijin Wang. 2019. Hierarchical multi-label text classification: An attention-based recurrent network approach. In Proceedings of the 28th _ACM International Conference on Information and Knowledge Management. ACM, New York, NY, USA, 1051–1060._  
[11] Ivana Clairine Irsan and Masayu Leylia Khodra. 2016. Hierarchical multilabel classification for Indonesian news articles. In 2016 International Conference On Advanced Informatics: Concepts, Theory And Application (ICAICTA). IEEE, Penang, Malaysia, 1–6.  
[12] Rie Johnson and Tong Zhang. 2015. Effective Use of Word Order for Text Categorization with Convolutional Neural Networks. In Proceedings of the 2015 Conference of the North American Chapter of the Association for Computational _Linguistics: Human Language Technologies. Association for Computational Linguistics, Denver, Colorado, 103–112._  
[13] Armand Joulin, Edouard Grave, Piotr Bojanowski, and Tomas Mikolov. 2017. Bag of Tricks for Efficient Text Classification. In Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: _Volume 2, Short Papers. Association for Computational Linguistics, Valencia, Spain, 427–431._  
[14] K Khan, R Ullah Khan, Ali Alkhalifah, and N Ahmad. 2015. Urdu text classification using decision trees. In 2015 _12th International Conference on High-capacity Optical Networks and Enabling/Emerging Technologies (HONET). IEEE,_ Islamabad, Pakistan, 1–4.  
[15] Yoon Kim. 2014. Convolutional Neural Networks for Sentence Classification. In Proceedings of the 2014 Conference on _Empirical Methods in Natural Language Processing (EMNLP). Association for Computational Linguistics, Doha, Qatar,_ [1746–1751. https://doi.org/10.3115/v1/D14-1181](https://doi.org/10.3115/v1/D14-1181)  
-----
111:22 Taimoor and Waseem, et al.  
[16] Svetlana Kiritchenko, Stan Matwin, Richard Nock, and A Fazel Famili. 2006. Learning and evaluation in the presence of class hierarchies: Application to text categorization. In Conference of the Canadian Society for Computational Studies _of Intelligence. Springer, Berlin, Heidelberg, 395–406._  
[17] Daphne Koller and Mehran Sahami. 1997. Hierarchically Classifying Documents Using Very Few Words. In Proceedings _of the Fourteenth International Conference on Machine Learning. Morgan Kaufmann Publishers Inc., San Francisco, CA,_ USA, 170–178.  
[18] Kamran Kowsari, Donald E Brown, Mojtaba Heidarysafa, Kiana Jafari Meimandi, Matthew S Gerber, and Laura E Barnes. 2017. Hdltex: Hierarchical deep learning for text classification. In 2017 16th IEEE international conference on _machine learning and applications (ICMLA). IEEE, Cancun, Mexico, 364–371._  
[19] Yannis Labrou and Tim Finin. 1999. Yahoo! as an ontology: using Yahoo! categories to describe documents. In _Proceedings of the eighth international conference on Information and knowledge management. ACM, New York, NY,_ USA, 180–187.  
[20] J. Li, Y. Xu, and H. Shi. 2019. Bidirectional LSTM with Hierarchical Attention for Text Classification. In 2019 IEEE 4th _Advanced Information Technology, Electronic and Automation Control Conference (IAEAC), Vol. 1. IEEE, Chengdu, China,_ 456–459.  
[21] Jingang Liu, Chunhe Xia, Haihua Yan, Zhipu Xie, and Jie Sun. 2019. Hierarchical Comprehensive Context Modeling for Chinese Text Classification. IEEE Access 7 (2019), 154546–154559.  
[22] Yuning Mao, Jingjing Tian, Jiawei Han, and Xiang Ren. 2019. Hierarchical Text Classification with Reinforced Label Assignment. CoRR (Nov. 2019), 445–455.  
[23] Yu Meng, Jiaming Shen, Chao Zhang, and Jiawei Han. 2019. Weakly-Supervised Hierarchical Text Classification. _Proceedings of the AAAI Conference on Artificial Intelligence 33, 01 (Jul. 2019), 6826–6833. https://ojs.aaai.org/index.php/AAAI/article/view/4658_  
[24] Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S Corrado, and Jeff Dean. 2013. Distributed Representations of Words and Phrases and their Compositionality. In Advances in Neural Information Processing Systems, Vol. 26. Curran Associates, Inc., Red Hook, NY, USA, 3111–3119.  
[25] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay. 2011. Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research 12 (2011), 2825–2830.  
[26] Hao Peng, Jianxin Li, Yu He, Yaopeng Liu, Mengjiao Bao, Lihong Wang, Yangqiu Song, and Qiang Yang. 2018. Largescale hierarchical text classification with recursively regularized deep graph-cnn. In Proceedings of the 2018 World Wide _Web Conference. ACM, Republic and Canton of Geneva, CHE, 1063–1072._  
[27] Kashif Riaz. 2008. Baseline for Urdu IR evaluation. In Proceedings of the 2nd ACM workshop on Improving non english _web searching. ACM, New York, NY, USA, 97–100._  
[28] Aixin Sun and Ee-Peng Lim. 2001. Hierarchical text classification and evaluation. In Proceedings 2001 IEEE International _Conference on Data Mining. IEEE, San Jose, CA, USA, 521–528._  
[29] P. Szymański and T. Kajdanowicz. 2017. A scikit-based Python environment for performing multi-label classification. _ArXiv e-prints abs/1702.01460 (2017). arXiv:1702.01460 [cs.LG]_  
[30] Jinbao Xie, Yongjin Hou, Yujing Wang, Qingyan Wang, Baiwei Li, Shiwei Lv, and Yury I Vorotnitsky. 2020. Chinese text classification based on attention mechanism and feature-enhanced fusion neural network. Computing 102, 3 (2020), 683–700.  
[31] Zichao Yang, Diyi Yang, Chris Dyer, Xiaodong He, Alex Smola, and Eduard Hovy. 2016. Hierarchical attention networks for document classification. In Proceedings of the 2016 conference of the North American chapter of the association for _computational linguistics: human language technologies. aclweb, San Diego, California, 1480–1489._  
-----
