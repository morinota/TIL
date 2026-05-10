refs: https://arxiv.org/pdf/2212.12061


_The peer-reviewed version of this paper is published in Data at https://doi.org/10.3390/data8050074._ 
この論文の査読済み版は、Dataにて公開されています: https://doi.org/10.3390/data8050074。

_This version is typeset by the authors and differs only in pagination and typographical detail._ 
この版は著者によって組版されており、ページ番号と印刷上の詳細のみが異なります。

MN-DS: A Multilabeled News Dataset for 
News Article Hierarchical Classification / MN-DS: ニュース記事の階層分類のためのマルチラベルニュースデータセット

**Alina Petukhova *** **, Nuno Fachada**  
**アリーナ・ペトゥホバ*** **、ヌーノ・ファカダ**  
Lusófona University, COPELABS, Campo Grande 376, 1749-024 Lisbon, Portugal; nuno.fachada@ulusofona.pt  
ルソフォナ大学、COPELABS、カンポ・グランデ376、1749-024リスボン、ポルトガル; nuno.fachada@ulusofona.pt  
*** Correspondence: alina.petukhova@ulusofona.pt**  
*** 連絡先: alina.petukhova@ulusofona.pt**

## Abstract / 要約

This article presents a dataset of 10,917 news articles with hierarchical news categories collected between 1 January 2019 and 31 December 2019.  
本稿では、2019年1月1日から2019年12月31日までに収集された階層的ニュースカテゴリを持つ10,917件のニュース記事のデータセットを提示します。
We manually labeled the articles based on a hierarchical taxonomy with 17 first-level and 109 second-level categories.  
私たちは、17の第一レベルと109の第二レベルのカテゴリを持つ階層的taxonomyに基づいて、記事に手動でラベルを付けました。  
This dataset can be used to train machine learning models for automatically classifying news articles by topic.  
このデータセットは、ニュース記事をトピック別に自動的に分類するための機械学習モデルのトレーニングに使用できます。  
This dataset can be helpful for researchers working on news structuring, classification, and predicting future events based on released news.  
**このデータセットは、ニュースの構造化、分類、公開されたニュースに基づく将来のイベントの予測に取り組む研究者にとって有用**です。  

**Keywords: news dataset; text classification; NLP; media topic taxonomy**  
**キーワード: ニュースデータセット; テキスト分類; NLP; メディアトピックtaxonomy**

<!-- ここまで読んだ! -->

## 1. Background and Summary / 1. 背景と要約

A news dataset is a collection of news articles classified into different categories.  
ニュースデータセットは、異なるカテゴリに分類されたニュース記事のコレクションです。  
In the past decade, there has been a sharp increase in news datasets available for analysis [1].  
過去10年間で、分析可能なニュースデータセットが急増しました[1]。  
These datasets can be used to understand various topics, from politics to the economy.  
これらのデータセットは、**政治から経済までのさまざまなトピックを理解するため**に使用できます。  

A few different types of news datasets are commonly used for analysis.  
分析に一般的に使用されるニュースデータセットには、**いくつかの異なるタイプ**があります。  

The first is raw data, which includes all the data that a news organization collects.  
最初は**生データ(raw data)**で、ニュース組織が収集するすべてのデータを含みます。
This data can be used to understand how a news organization operates, what stories are covered, and how they are covered.
このデータは、ニュース組織がどのように運営されているか、どのようなストーリーが取り上げられているか、そしてどのように取り上げられているかを理解するために使用できます。
The second type of news dataset is processed data.  
ニュースデータセットの2番目のタイプは**処理データ(processed data)**です。  
These data have been through some processing, such as aggregation or cleaned up.  
これらのデータは、集約やクリーンアップなどの処理を経ています。  
Processed data are often easier to work with than raw data and can be used to answer specific questions such as providing additional information for the decision-making process.  
処理データは、生データよりも扱いやすく、意思決定プロセスのための追加情報を提供するなど、特定の質問に答えるために使用できます。  
The third type of news dataset is derived data.  
ニュースデータセットの3番目のタイプは**派生データ(derived data)**です。  
These data are created by combining multiple datasets, often from different sources [2].  
これらのデータは、複数のデータセットを組み合わせて作成され、しばしば異なるソースからのものです[2]。 

<!-- ここまで読んだ! -->

News datasets can be used for various purposes in a machine learning context, for example:  
ニュースデータセットは、機械学習の文脈でさまざまな目的に使用できます。例えば:  

- Predicting future events based on past news articles.  
  - 過去のニュース記事に基づいて将来のイベントを予測すること。  
- Understanding the news cycle.  
  - ニュースサイクルを理解すること。  
- Determining the sentiment of news articles.  
  - ニュース記事の感情を判断すること。  
- Extracting information from news articles (e.g., named entities, location, dates).  
  - ニュース記事から情報を抽出すること（例: 固有名詞、場所、日付）。  
- Classifying news articles into predefined categories.  
  - ニュース記事を事前定義されたカテゴリに分類すること。  

To adequately answer research questions, news datasets should contain sufficient data points and span a significant enough period.  
研究質問に適切に答えるためには、ニュースデータセットは十分なデータポイントを含み、十分な期間をカバーする必要があります。
There are many labeled news datasets available, each with specific limitations.  
多くのラベル付きニュースデータセットが利用可能で、それぞれ特定の制限があります。  
For example, they may only cover a specific period or geographical area or be confined to a particular topic.  
例えば、特定の期間や地理的領域のみをカバーしているか、特定のトピックに限定されている場合があります。  
Additionally, the categories may not be completely accurate, and the datasets may be biased in some way [3,4].  
さらに、カテゴリが完全に正確でない場合や、データセットが何らかの形でバイアスを持っている場合があります[3,4]。  

<!-- ここまで読んだ! -->

Some of the more popular news datasets include the 20 Newsgroups dataset [5], AG’s news topic classification dataset [6], L33-Yahoo News dataset [7,8], News Category dataset [9], and Media Cloud dataset [10].  
より人気のあるニュースデータセットには、20 Newsgroupsデータセット[5]、AGのニューストピック分類データセット[6]、L33-Yahoo Newsデータセット[7,8]、ニュースカテゴリデータセット[9]、およびMedia Cloudデータセット[10]が含まれます。  
Each of these datasets has been used extensively by researchers in the fields of natural language processing and machine learning, and each has its advantages and disadvantages.  
これらのデータセットは、自然言語処理や機械学習の分野で研究者によって広く使用されており、それぞれに利点と欠点があります。 
The 20 Newsgroups dataset was created in 1997 and contains 20 different categories of news, each with a training and test set.  
**20 Newsgroupsデータセット**は1997年に作成され、20の異なるニュースカテゴリを含み、それぞれにトレーニングセットとテストセットがあります。  
The data is already pre-processed and tokenized, which makes it very easy to use.  
データはすでに前処理され、トークン化されているため、非常に使いやすいです。  
However, the dataset is outdated and relatively small, with only about 1000 documents in each category.  
しかし、このデータセットは古く、比較的小さく、各カテゴリに約1000件の文書しかありません。  

<!-- ここまで読んだ! -->

The AG’s news topic classification dataset is a collection of news articles from the academic news search engine “ComeToMyHead” during more than one year of activity.  
**AGのニューストピック分類データセット**は、学術ニュース検索エンジン「ComeToMyHead」からのニュース記事のコレクションで、1年以上の活動期間にわたります。 
Articles were classified into 13 categories: business, entertainment, Europe, health, Italia, music feeds, sci/tech, software & dev., sports, toons, top news, U.S., and world.  
記事は、ビジネス、エンターテインメント、ヨーロッパ、健康、イタリア、音楽フィード、科学/技術、ソフトウェア＆開発、スポーツ、アニメ、トップニュース、米国、世界の13カテゴリに分類されました。  
The dataset contains more than 1 million news articles.  
データセットには100万件以上のニュース記事が含まれています。  
However, there are several limitations to this dataset.  
しかし、このデータセットにはいくつかの制限があります。  
First, it is currently outdated since data were collected in 2005.  
まず、データは2005年に収集されたため、現在は古くなっています。
Second, the taxonomy covers specific countries such as the US and Italy but has general references such as Europe or world, creating overlaps in the classification (e.g., Italy and Europe) as well as potential imbalances (e.g., events in China are likely to be underrepresented and/or under-reported compared to those in the US).  
第二に、taxonomyは米国やイタリアなどの特定の国をカバーしていますが、ヨーロッパや世界などの一般的な参照も含まれており、分類に重複を生じさせています（例: イタリアとヨーロッパ）および潜在的な不均衡（例: 中国のイベントは米国のイベントに比べて過小評価される可能性が高い）。
Finally, the dataset does not include methods for type or category description.  
最後に、このデータセットにはタイプやカテゴリの説明方法が含まれていません。

<!-- ここまで読んだ! -->

The L33-Yahoo News dataset is a collection of news articles from the Yahoo News website provided as part of the Yahoo! Webscope program.  
**L33-Yahoo Newsデータセット**は、Yahoo! Webscopeプログラムの一部として提供されるYahoo Newsウェブサイトからのニュース記事のコレクションです。  
The articles are labeled into 414 categories such as music, movies, crime justice, and others.  
記事は、音楽、映画、犯罪司法などの414のカテゴリにラベル付けされています。  
The dataset includes the random article id followed by possible associated categories.  
データセットには、ランダムな記事IDとそれに関連する可能性のあるカテゴリが含まれています。  
The L33-Yahoo News dataset is available under Yahoo’s data protection standards.  
L33-Yahoo Newsデータセットは、Yahooのデータ保護基準の下で利用可能です。  
It can be used for non-commercial purposes if researchers credit the source and license new creations under identical terms.  
研究者が出典をクレジットし、新しい創作物を同じ条件でライセンスする場合、非商業目的で使用できます。  
The limitations of the L33 dataset are the license terms, restricting companies from using this dataset for commercial purposes, and the amount of data per class, with the category “supreme court decisions” having only five articles, for example.  
**L33データセットの制限は、ライセンス条件であり、企業がこのデータセットを商業目的で使用することを制限していること**、そしてクラスごとのデータ量であり、例えば「最高裁判所の決定」というカテゴリにはわずか5件の記事しかありません。  
In addition, there is some overlap in the categories, which makes it challenging to train a model that can accurately predict multiple categories.  
さらに、カテゴリにいくつかの重複があり、複数のカテゴリを正確に予測できるモデルをトレーニングするのが難しくなっています。  

<!-- ここまで読んだ! -->

The News Category Dataset is a collection of around 210k news articles from the Huffington Post, labeled with their respective categories, which include business, entertainment, politics, science and technology, and sports.  
**ニュースカテゴリデータセットは、ハフィントンポストからの約210,000件のニュース記事のコレクション**で、それぞれのカテゴリ（ビジネス、エンターテインメント、政治、科学技術、スポーツなど）にラベル付けされています。  
However, the dataset has several limitations.  
しかし、このデータセットにはいくつかの制限があります。  
First, the dataset is not comprehensive since it only includes articles from one source.  
まず、このデータセットは1つのソースからの記事のみを含むため、包括的ではありません。  
Second, news categories are not standardized, including broad categories such as “Media” and “Politics” and very narrow ones like “Weddings” and “Latino voices”.  
**第二に、ニュースカテゴリは標準化されておらず、「メディア」や「政治」などの広範なカテゴリや、「結婚式」や「ラティーノの声」などの非常に狭いカテゴリが含まれています。** (そうなるよね〜わかる~ taxonomy設計じゃん!:thinking:)

The Media Cloud Data Set is a collection of over 1.7 billion articles from more than 60 thousand media sources around the world.
**Media Cloudデータセット**は、世界中の60,000以上のメディアソースからの17億件以上の記事のコレクションです。  
The dataset includes articles from both mainstream and alternative news sources, including newspapers, magazines, blogs, and online news outlets.  
データセットには、新聞、雑誌、ブログ、オンラインニュースメディアなど、主流および代替のニュースソースからの記事が含まれています。
Data can be queried by keyword, tag, category, sentiment, and location.  
データは、キーワード、タグ、カテゴリ、感情、場所でクエリできます。  
This dataset is useful for researchers who are interested in studying media coverage of specific topics or trends over time.  
**このデータセットは、特定のトピックやトレンドに対するメディアの報道を時間の経過とともに研究したい研究者にとって有用**です。  
Media Cloud is a large multilingual dataset that has good media coverage but limited use in topic classification models since it does not include a mapping of articles to a specific news taxonomy.  
Media Cloudは、大規模な多言語データセットであり、良好なメディアカバレッジを持っていますが、**特定のニュースtaxonomyへの記事のマッピングが含まれていないため(これってどういう意味だろ??:thinking:)**、トピック分類モデルでの使用は限られています。

<!-- ここまで読んだ! -->

The main motivation for this work is to provide a dataset for building specific topic models.  
この作業の主な動機は、特定のトピックモデルを構築するためのデータセットを提供することです。  
It consists of a categorized subset taken from an existing news dataset.  
これは、既存のニュースデータセットから取得したカテゴリ化されたサブセットで構成されています。  
We show that such a dataset, with up-to-date articles mapped into a standardized news taxonomy, can contribute to the accuracy improvement of news classification models.  
私たちは、このようなデータセットが、最新の記事が標準化されたニュースtaxonomyにマッピングされていることで、ニュース分類モデルの精度向上に寄与できることを示します。  

<!-- ここまで読んだ! -->

## 2. Methods / 2. 方法

In this paper, we present a new dataset based on the NELA-GT-2019 data source [11], classified with IPTC’s[1] NewsCodes Media Topic taxonomy [12].  
本論文では、**NELA-GT-2019データソース[11]に基づいた新しいデータセットを提示**し、IPTCの[1] NewsCodesメディアトピックtaxonomy[12]で分類しました。 
The original NELA-GT-2019 dataset contains 1.12 M news articles from 260 sources collected between 1 January 2019 and 31 December 2019, providing essential content diversity and topic coverage.  
元のNELA-GT-2019データセットには、2019年1月1日から2019年12月31日までに収集された260のソースからの1.12百万件のニュース記事が含まれており、重要なコンテンツの多様性とトピックのカバレッジを提供します。  
Sources include a wide range of mainstream and alternative news outlets.  
ソースには、主流および代替のニュースメディアが幅広く含まれています。  

In turn, the IPTC taxonomies are a set of controlled vocabularies used to describe news stories’ content.  
一方、**IPTC taxonomyは、ニュースストーリーの内容を説明するために使用される制御語彙のセット**です。  
The NewsCodes Media Topic taxonomy has been one of IPTC’s main subject taxonomies for text classification since 2010.  
NewsCodesメディアトピックtaxonomyは、2010年以降、テキスト分類のためのIPTCの主要な主題taxonomyの1つです。  
We used the 2020 version of NewsCodes Media Topic taxonomy [13].  
私たちは、**NewsCodesメディアトピックtaxonomyの2020年版[13]**を使用しました。  
News organizations use it to categorize and index their content, while search engines use it to improve the discoverability of news stories [14].  
**ニュース組織はそれを使用してコンテンツを分類およびインデックス化し、検索エンジンはそれを使用してニュースストーリーの発見可能性を向上**させます[14]。 

<!-- ここまで読んだ! -->

Algorithm of the article selection process:  
記事選択プロセスのアルゴリズム: 

1. Obtain a random article from the NELA dataset;  
   1. NELAデータセットからランダムな記事を取得します;  
2. Classify it for the second-level category of the NewsCodes Media Topic taxonomy by checking the keywords and thorough reading of the article; the news article is assigned to exactly one category;  
   1. キーワードを確認し、記事を徹底的に読み込むことで、NewsCodesメディアトピックtaxonomyの第二レベルカテゴリに分類します; ニュース記事は正確に1つのカテゴリに割り当てられます;  
3. If there are already 100 articles in that category discard it, otherwise assign a second-level category to the article;  
   1. そのカテゴリにすでに100件の記事がある場合は破棄し、そうでない場合は記事に第二レベルカテゴリを割り当てます;  
4. Return to step 1 and repeat until each second-level category has 100 articles assigned.  
   1. ステップ1に戻り、各第二レベルカテゴリに100件の記事が割り当てられるまで繰り返します。  

The described algorithm allows for overcoming the limitation of the NELA-GT datasets where a large proportion of the dataset is fringe, conspiracy-based news due to the discharging of the news if a category already has 100 articles in it.  
**このアルゴリズムは、NELA-GTデータセットの制限を克服**することを可能にします。これは、カテゴリにすでに100件の記事がある場合、ニュースが破棄されるため、データセットの大部分がフリンジ、陰謀論に基づくニュースであることです。

<!-- ここまで読んだ! -->

We observed that the first-level category of the NewsCodes Media Topic taxonomy is not accurate enough to catalogue an article.  
私たちは、**NewsCodesメディアトピックtaxonomyの第一レベルカテゴリが記事をカタログ化するには十分に正確でないことを観察**しました。  
For example, the “sport” category may include different aspects, such as information about specific sports, sports event announcements, and the sports industry in general, which have more specific meanings than the first-level category label is able to convey.  
**例えば、「スポーツ」カテゴリには、特定のスポーツに関する情報、スポーツイベントの発表、スポーツ産業全般など、第一レベルカテゴリラベルが伝えることのできるより具体的な意味を持つさまざまな側面が含まれる**場合があります。
Therefore, we used a second-level category of NewsCodes Media Topic taxonomy to have a more specific article category.
したがって、より具体的な記事カテゴリを持つために、NewsCodesメディアトピックtaxonomyの第二レベルカテゴリを使用しました。
In comparison to the previously published datasets, we included in our dataset unique categories such as “arts and entertainment”, “mass media”, “armed conflict”, “weather statistic”, and “weather warning”.  
以前に公開されたデータセットと比較して、私たちのデータセットには「アートとエンターテインメント」、「マスメディア」、「武力紛争」、「天気統計」、「天気警報」などのユニークなカテゴリを含めました。  
Therefore, we created the proposed Multilabeled News Dataset (MN-DS) by hand-picking and labeling approximately 100 news articles for each second level category[2] of the NewsCodes Media Topic taxonomy.  
したがって、NewsCodesメディアトピックtaxonomyの各第二レベルカテゴリ[2]に対して約100件のニュース記事を手動で選択し、ラベル付けすることによって提案されたマルチラベルニュースデータセット（MN-DS）を作成しました。 

<!-- ここまで読んだ! -->

## 3. Data Records / 3. データレコード

After manually selecting news articles relevant to each category, we obtained 10,917 articles in 17 first-level and 109 second-level categories from 215 media sources.  
各カテゴリに関連するニュース記事を手動で選択した後、215のメディアソースから17の第一レベルと109の第二レベルカテゴリにおいて10,917件の記事を取得しました。  
During the selection process, one article was processed by one coder.  
選択プロセス中、1つの記事は1人のコーダーによって処理されました。  
An overview of the released MN-DS dataset by category is provided in Table 1.  
**リリースされたMN-DSデータセットのカテゴリ別の概要は、表1に**示されています。
All data are available in CSV format at [https://doi.org/10.5281/zenodo.7394850 under a Creative Commons license.](https://doi.org/10.5281/zenodo.7394850) 
すべてのデータは、[https://doi.org/10.5281/zenodo.7394850のCreative Commonsライセンスの下でCSV形式で利用可能です。](https://doi.org/10.5281/zenodo.7394850)

**Table 1. The number of articles under each Level 1 category. / 表1. 各レベル1カテゴリにおける記事の数。**

| Categories / カテゴリ | Count / 数 |
| --- | ---: |
| Arts, culture, entertainment, and media / 芸術、文化、エンターテインメント、メディア | 300 |
| Conflict, war, and peace / 紛争、戦争、平和 | 800 |
| Crime, law, and justice / 犯罪、法律、正義 | 500 |
| Disaster, accidents, and emergency incidents / 災害、事故、緊急事態 | 500 |
| Economy, business and finance / 経済、ビジネス、金融 | 400 |
| Education / 教育 | 607 |
| Environment / 環境 | 600 |
| Health / 健康 | 700 |
| Human interest / 人間の関心 | 600 |
| Labor / 労働 | 703 |
| Lifestyle and leisure / ライフスタイルとレジャー | 300 |
| Politics / 政治 | 900 |
| Religion and belief / 宗教と信念 | 800 |
| Science and technology / 科学と技術 | 800 |
| Society / 社会 | 1100 |
| Sport / スポーツ | 907 |
| Weather / 天気 | 400 |

-----
4 of 9  
MN-DS contains articles published in 2019, the distribution of selected articles over the year is balanced with slightly more articles for the month of January 2019. 
MN-DSには2019年に発表された記事が含まれており、選定された記事の年間分布はバランスが取れており、2019年1月の記事がやや多くなっています。
The majority of the articles were selected from mainstream sources such as ABC News, the BBC, The Sun, TASS, The Guardian, Birmingham Mail, The Independent, Evening Standard, and others. 
記事の大部分は、ABCニュース、BBC、ザ・サン、TASS、ガーディアン、バーミンガム・メール、インデペンデント、イブニング・スタンダードなどの主流の情報源から選ばれました。
The dataset also includes a relatively small percentage of articles from alternative sources such as Sputnik, FREEDOMBUNKER, or Daily Buzz Live. 
データセットには、Sputnik、FREEDOMBUNKER、Daily Buzz Liveなどの代替情報源からの比較的小さな割合の記事も含まれています。

To describe the dataset, we created a word cloud representation of each category, as shown in Figure 1. 
データセットを説明するために、**各カテゴリのワードクラウド表現**を作成しました（図1参照）。
The central concept of a word cloud is to visualize for each category the most popular words with a size corresponding to the degree of popularity. 
**ワードクラウドの中心的な概念は、各カテゴリの最も人気のある単語を視覚化**し、そのサイズが人気の度合いに対応することです。
This representation allows us to quickly assess the quality of the text annotation since it displays the most common words of the category. 
**この表現により、カテゴリの最も一般的な単語を表示するため、テキスト注釈の質を迅速に評価することができます。**
In the bar chart shown in Figure 2, we can observe that the “science and technology” first-level category contains the highest count of topic-specific words, while in more general categories, such as “weather” or “human interest”, there is less variety in the texts, probably because they represent shorter and more similar articles. 
図2に示されている棒グラフでは、「科学と技術」の第一レベルカテゴリがトピック特有の単語の数が最も多いことがわかりますが、「天気」や「人間の関心」などのより一般的なカテゴリでは、テキストのバラエティが少なく、恐らくそれらがより短く、より類似した記事を表しているためです。

![]()

![]()

The purpose of this dataset is to provide labeled data to train and test classifiers to predict the topic of a news article. 
**このデータセットの目的は、ニュース記事のトピックを予測するための分類器を訓練およびテストするためのラベル付きデータを提供すること**です。
Since the MN-DS represent the subset of the NELA-GT dataset, it could be also used to study the veracity of news articles but is not limited to this application. 
MN-DSはNELA-GTデータセットのサブセットを表しているため、ニュース記事の真実性を研究するためにも使用できますが、この用途に限られません。
Due to the nature of the NELA-GT dataset, the style of articles is less formal, and we expect it to be the best fit for the alternative/conspiracy sources or social media article classification. 
NELA-GTデータセットの性質上、記事のスタイルはあまりフォーマルではなく、代替/陰謀情報源やソーシャルメディア記事の分類に最適であると考えています。

Description of Columns in the Data Table / データテーブルの列の説明

| Column | Description / 説明 |
| --- | --- |
| id | Unique identifier of the article. / 記事のユニーク識別子。 |
| date | Date of the article release. / 記事のリリース日。 |
| source | Publisher information of the article. / 記事の出版社情報。 |
| title | Title of the news article. / ニュース記事のタイトル。 |
| content | Text of the news article. / ニュース記事のテキスト。 |
| author | Author of the news article. / ニュース記事の著者。 |
| url | Link to the original article. / 元の記事へのリンク。 |
| published | Date of article publication in local time. / 現地時間での記事の公開日。 |
| published_utc | Date of article publication in utc time. / UTC時間での記事の公開日。 |
| collection_utc | Date of article scraping in utc time. / UTC時間での記事のスクレイピング日。 |
| category_level_1 | First level category of Media Topic NewsCodes’s taxonomy. / メディアトピックニュースコードのtaxonomyの第一レベルカテゴリ。 |
| category_level_2 | Second level category of Media Topic NewsCodes’s taxonomy. / メディアトピックニュースコードのtaxonomyの第二レベルカテゴリ。 |

<!-- ここまで読んだ! -->

-----
5 of 9  
**Figure 1. Word clouds of MN-DS dataset for selected second-level categories.**  
**図1. 選定された第二レベルカテゴリのMN-DSデータセットのワードクラウド。**

**Figure 2. Mean number of non-repeated words in article body for first-level categories. The error bars** represent the 95% confidence interval.  
**図2. 第一レベルカテゴリにおける記事本文の非重複単語の平均数。エラーバーは95%信頼区間を示します。**

<!-- ここまで読んだ! -->

## 4. Usage Example / 4. 使用例

We used the dataset to train the most common text classification models to extend the technical validation of the proposed dataset and establish the benchmark for multiclass classification.  
私たちは、提案されたデータセットの技術的検証を拡張し、多クラス分類のベンチマークを確立するために、最も一般的なテキスト分類モデルを訓練するためにデータセットを使用しました。
The following embeddings were selected:  
以下の埋め込みが選択されました：

- Tf-idf embedding, where Tf-idf stands for term frequency-inverse document frequency [15].  
  - Tf-idf埋め込み、ここでTf-idfは用語頻度-逆文書頻度を表します[15]。
  Tf-idf transforms text into a numerical representation called a tf-idf matrix.  
  Tf-idfはテキストをtf-idf行列と呼ばれる数値表現に変換します。
  The term frequency is the number of times a word appears in a document.  
  用語頻度は、単語が文書に出現する回数です。
  The inverse document frequency measures how common a word is across all documents.  
  逆文書頻度は、単語がすべての文書にどれだけ一般的であるかを測定します。
  Tf-idf is used to weigh words so that important words are given more weight.  
  Tf-idfは、重要な単語により多くの重みを与えるように単語を重み付けするために使用されます。
  The dataset’s news texts and categories were combined and vectorized with TfidfVectorizer [16].  
  データセットのニューステキストとカテゴリは結合され、TfidfVectorizer [16]を使用してベクトル化されました。

- GloVe (Global Vectors for Word Representation) embeddings with an algorithm based on a co-occurrence matrix, which counts how often words appear together in a text corpus.  
  - GloVe（単語表現のためのグローバルベクトル）埋め込みは、テキストコーパス内で単語が一緒に出現する頻度をカウントする共起行列に基づくアルゴリズムを使用しています。
  The resulting vectors are then transformed into a lower-dimensional space using singular value decomposition [17]. 
  得られたベクトルは、特異値分解[17]を使用して低次元空間に変換されます。

- DistilBertTokenizer [18], which is a distilled version of BERT, a popular pre-trained model for natural language processing.  
  - DistilBertTokenizer [18]は、自然言語処理のための人気のある事前学習モデルBERTの蒸留版です。
  DistilBERT is smaller and faster than BERT, making it more suitable for fast training with limited resources.  
  DistilBERTはBERTよりも小さく、速いため、限られたリソースでの迅速な訓練により適しています。
  The trade-off is that DistilBERT’s performance is 3% lower than BERT’s.  
  そのトレードオフは、DistilBERTのパフォーマンスがBERTよりも3%低いことです。
  DistilBERT embeddings are trained on the same data as BERT, so they are equally good at capturing the meaning of words in context.  
  DistilBERTの埋め込みはBERTと同じデータで訓練されているため、文脈における単語の意味を捉えるのに同等に優れています。

<!-- ここまで読んだ! -->

During dataset validation, we combined the selected embeddings with different classifiers.  
データセットの検証中に、選択した埋め込みを異なる分類器と組み合わせました。
We tested multinomial naive Bayes (NB) classifier [19], logistic regression [20], support vector classifier (SVC) [21], and DistilBERT model [22].  
多項ナイーブベイズ（NB）分類器[19]、ロジスティック回帰[20]、サポートベクター分類器（SVC）[21]、およびDistilBERTモデル[22]をテストしました。
Since MN-DS is a multiclass dataset, we used the OneVsRestClassifier strategy for classification models [16].  
MN-DSは多クラスデータセットであるため、分類モデルにはOneVsRestClassifier戦略[16]を使用しました。
OneVsRestClassifier is a classifier that trains multiple binary classifiers, one for each class.  
OneVsRestClassifierは、各クラスごとに1つのバイナリ分類器を訓練する分類器です。
The individual binary classifiers are then combined to create a single multiclass classifier.  
個々のバイナリ分類器は、単一の多クラス分類器を作成するために組み合わされます。
This approach is often used when there are many categories, as it can be more efficient than training a single multiclass classifier from scratch.  
このアプローチは、カテゴリが多い場合によく使用されます。なぜなら、ゼロから単一の多クラス分類器を訓練するよりも効率的である可能性があるからです。
The tested classifiers work as follows:  
テストされた分類器は次のように機能します：

- The multinomial NB is a text classification algorithm that uses Bayesian inference to classify text.  
  - 多項NBは、ベイズ推論を使用してテキストを分類するテキスト分類アルゴリズムです。
  It is a simple and effective technique that can be used for various tasks, such as spam filtering and document classification.  
  これは、スパムフィルタリングや文書分類など、さまざまなタスクに使用できるシンプルで効果的な手法です。
  The algorithm is based on the assumption that the features in a document are independent of each other, which allows it to make predictions about the category of a document based on its individual features.  
  このアルゴリズムは、文書内の特徴が互いに独立であるという仮定に基づいており、これにより文書の個々の特徴に基づいて文書のカテゴリについての予測を行うことができます。

- The logistic regression classifier works by using a sigmoid function to map data points from an input space to an output space, where the categories are assigned based on a linear combination of the features.  
  - ロジスティック回帰分類器は、シグモイド関数を使用してデータポイントを入力空間から出力空間にマッピングし、カテゴリは特徴の線形結合に基づいて割り当てられます。
  The weights of the features are learned through training, and the predictions are made by taking the dot product of the feature vector and the weight vector.  
  特徴の重みは訓練を通じて学習され、予測は特徴ベクトルと重みベクトルの内積を取ることによって行われます。

- The SVC classifier is a powerful machine learning model based on the support vector machines algorithm.  
  - SVC分類器は、サポートベクターマシンアルゴリズムに基づく強力な機械学習モデルです。
  The model is based on finding the optimal decision boundary between categories to maximize the margin of separation between them.  
  このモデルは、カテゴリ間の最適な決定境界を見つけて、それらの間の分離のマージンを最大化することに基づいています。
  The SVC model can be used for linear and non-linear classification tasks and is particularly well-suited for problems with high dimensional data.  
  SVCモデルは、線形および非線形の分類タスクに使用でき、高次元データの問題に特に適しています。
  The classifier is also robust to overfitting and can generalize well to new data.  
  この分類器は過剰適合に対しても頑健であり、新しいデータに対しても良好に一般化できます。

- DistilBERTModel, a light version of the BERT classifier [18], developed and open-sourced by the team at Hugging Face.  
  - DistilBERTModelは、Hugging Faceのチームによって開発され、オープンソース化されたBERT分類器の軽量版です。
  DistilBERTModel can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of NLP tasks with minimal training data.  
  DistilBERTModelは、最小限の訓練データで幅広いNLPタスクの最先端モデルを作成するために、1つの追加出力層で微調整できます。

Classification results for level 1 and level 2 categories are presented in Table 2 and Table 3, respectively.  
レベル1およびレベル2カテゴリの分類結果は、それぞれ表2および表3に示されています。
It is possible to observe that DistilBERTModel achieves better classification results for both category levels.  
DistilBERTModelが両方のカテゴリレベルでより良い分類結果を達成していることが観察できます。
To improve these results in future studies, we suggest applying hierarchical classification methods as described by Silla and Freitas [23], for example.  
今後の研究でこれらの結果を改善するために、SillaとFreitasによって説明された階層分類手法を適用することを提案します[23]。

<!-- ここまで読んだ! -->

**Table 2. Multilabel classification results for level 1 categories. / 表2. レベル1カテゴリのマルチラベル分類結果。**

| Model / モデル | TFIDF Precision / 適合率 | TFIDF Recall / 再現率 | TFIDF F1 | Glove Precision / 適合率 | Glove Recall / 再現率 | Glove F1 | DistilBert Precision / 適合率 | DistilBert Recall / 再現率 | DistilBert F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Multinomial NB / 多項NB | 0.802 | 0.631 | 0.649 | 0.629 | 0.499 | 0.529 | n/a | n/a | n/a |
| Logistic Regression / ロジスティック回帰 | 0.800 | 0.763 | 0.774 | 0.747 | 0.739 | 0.739 | n/a | n/a | n/a |
| SVC Classifier / SVC分類器 | 0.808 | 0.796 | 0.799 | 0.768 | 0.762 | 0.760 | n/a | n/a | n/a |
| DistilBERTModel | n/a | n/a | n/a | n/a | n/a | n/a | 0.849 | 0.842 | 0.844 |

**Table 3. Multilabel classification results for level 2 categories. / 表3. レベル2カテゴリのマルチラベル分類結果。**

| Model / モデル | TFIDF Precision / 適合率 | TFIDF Recall / 再現率 | TFIDF F1 | Glove Precision / 適合率 | Glove Recall / 再現率 | Glove F1 | DistilBert Precision / 適合率 | DistilBert Recall / 再現率 | DistilBert F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Multinomial NB / 多項NB | 0.628 | 0.602 | 0.583 | 0.496 | 0.484 | 0.469 | n/a | n/a | n/a |
| Logistic Regression / ロジスティック回帰 | 0.646 | 0.649 | 0.635 | 0.589 | 0.589 | 0.577 | n/a | n/a | n/a |
| SVC Classifier / SVC分類器 | 0.645 | 0.646 | 0.628 | 0.581 | 0.595 | 0.571 | n/a | n/a | n/a |
| DistilBERTModel | n/a | n/a | n/a | n/a | n/a | n/a | 0.735 | 0.715 | 0.715 |

## Data Availability Statement / データの可用性に関する声明

The data described in this paper is available in CSV format at [https://doi.org/10.5281/zenodo.7394850](https://doi.org/10.5281/zenodo.7394850).  
本論文で説明されているデータは、[https://doi.org/10.5281/zenodo.7394850](https://doi.org/10.5281/zenodo.7394850)でCSV形式で利用可能です。
. Code for the technical validation of the dataset is available at](https://\doi.org/10.5281/zenodo.7394850)
データセットの技術的検証のためのコードは、次のリンクで入手可能です: [https://doi.org/10.5281/zenodo.7394850](https://doi.org/10.5281/zenodo.7394850)

[https://github.com/alinapetukhova/mn-ds-news-classification (accessed on 15 April 2023).](https://github.com/alinapetukhova/mn-ds-news-classification)
[https://github.com/alinapetukhova/mn-ds-news-classification (2023年4月15日アクセス)](https://github.com/alinapetukhova/mn-ds-news-classification)

## Conflicts of Interest / 利益相反

The authors declare no conflicts of interest.  
著者は利益相反がないことを宣言します。

<!-- ここまで読んだ! -->
