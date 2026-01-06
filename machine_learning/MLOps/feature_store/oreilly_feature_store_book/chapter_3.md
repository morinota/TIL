## CHAPTER 3: Your Friendly Neighborhood Air Quality Forecasting Service
## 第3章: あなたの親しみやすい近隣の空気質予測サービス

The first ML project we will build is an air quality forecasting service for a neighborhood you care about. 
私たちが構築する最初のMLプロジェクトは、あなたが気にかけている近隣の空気質予測サービスです。

We will follow the MVPS process from Chapter 2—divide et _impera (divide and conquer). 
私たちは、第2章のMVPSプロセスに従い、分割して征服します（divide et impera）。

Your work will be a public service built to survive, so please put some time and care into it and your community will love you for it. 
あなたの仕事は、持続可能な公共サービスとなるため、時間と労力をかけてください。そうすれば、あなたのコミュニティはあなたを愛してくれるでしょう。

I have a personal interest in this project as I have two boys with cystic fibrosis, a genetic disorder that primarily affects the lungs. 
私はこのプロジェクトに個人的な関心を持っています。なぜなら、私は肺に主に影響を与える遺伝性疾患である嚢胞性線維症を持つ2人の息子がいるからです。

They were born on the same day, two years apart, and diagnosed the same day. 
彼らは同じ日に生まれ、2年の差があり、同じ日に診断されました。

Anyway, I think I speak for the whole cystic fibrosis community in saying this would be a fantastic service for us and many others! 
とにかく、私は嚢胞性線維症コミュニティ全体を代表して、これは私たちや他の多くの人々にとって素晴らしいサービスになると言いたいです！

The prediction problem our AI system will solve is to predict the air quality for a public air quality sensor close to your home or work, or wherever. 
私たちのAIシステムが解決する予測問題は、あなたの家や職場、またはどこにでも近い公共の空気質センサーの空気質を予測することです。

A worldwide community of Internet of Things (IoT) hobbyists place sensors in their gardens and balconies and publish air quality measurements on the internet. 
世界中のIoT愛好家のコミュニティが、自宅の庭やバルコニーにセンサーを設置し、空気質の測定値をインターネット上に公開しています。

Where I live in Stockholm, there are over 30 public sensors, and in my home city of Dublin, there are over 40. 
私が住んでいるストックホルムには30以上の公共センサーがあり、私の故郷ダブリンには40以上のセンサーがあります。

There is a world air quality index website where you can find a sensor on the map to build your AI system on. 
AIシステムを構築するためのセンサーを地図上で見つけることができる世界の空気質指数のウェブサイトがあります。

Pick one that both (1) has historical data—we will train an ML model on the historical data, so if you have a few years of data, that is great—and (2) produces reliable measurements (some sensors are turned off for periods of time or malfunction). 
(1) 歴史的データがあり—私たちはその歴史的データを使ってMLモデルを訓練しますので、数年分のデータがあれば素晴らしいです—かつ (2) 信頼できる測定値を生成するセンサーを選んでください（いくつかのセンサーは一定期間オフになったり、故障したりします）。

A reliable sensor will enable your AI system to continue to collect measurement data, enabling you to retrain and improve the model as more data becomes available. 
信頼できるセンサーは、AIシステムが測定データを収集し続けることを可能にし、より多くのデータが利用可能になるにつれてモデルを再訓練し、改善することを可能にします。

Even though you will provide a free public service to your community, it won’t cost you a penny—we will run the system on free serverless services (GitHub and Hopsworks). 
あなたがコミュニティに無料の公共サービスを提供するにもかかわらず、あなたに一銭もかかりません—私たちは無料のサーバーレスサービス（GitHubとHopsworks）でシステムを運用します。

Air quality prediction is a pretty straightforward ML problem. 
空気質予測は非常に単純なML問題です。

We will model the prediction problem as a regression problem—we’ll predict the value of PM2.5. 
私たちは予測問題を回帰問題としてモデル化します—PM2.5の値を予測します。

PM2.5 is a fine particulate measure for particles that are 2.5 micrometers or less in diameter, and high levels increase the risk of health problems like low birth weight, heart disease, and lung disease. 
PM2.5は、直径が2.5マイクロメートル以下の微細粒子の測定値であり、高いレベルは低出生体重、心臓病、肺疾患などの健康問題のリスクを高めます。

High levels of PM2.5 also reduce visibility, causing the air to appear hazy. 
PM2.5の高いレベルは視界を悪化させ、空気がかすんで見える原因にもなります。

What are the features we will use to predict the level of PM2.5? 
PM2.5のレベルを予測するために使用する特徴は何ですか？

PM2.5 is correlated with wind speed/direction, temperature, and precipitation, so we will use weather forecast data to predict air quality as measured in PM2.5. 
PM2.5は風速/風向、温度、降水量と相関しているため、私たちは天気予報データを使用してPM2.5で測定された空気質を予測します。

This makes sense because air quality is generally better when the wind blows in a particular direction—if you live beside a busy road, wind direction is crucial. 
これは理にかなっています。なぜなら、空気質は一般的に風が特定の方向に吹くときに良くなるからです—もしあなたが混雑した道路のそばに住んでいるなら、風向きは重要です。

Air quality is often worse in colder weather, as cold air is denser and moves slower than warm air, and in cities where more people may drive than bike when commuting. 
空気質は寒い天候では悪化することが多いです。なぜなら、冷たい空気は密度が高く、暖かい空気よりも遅く動くからです。また、通勤時に自転車よりも車を利用する人が多い都市でも同様です。

Even parts of India that don’t experience cold winter weather have worse air quality in the winter months. 
寒い冬の天候を経験しないインドの一部でも、冬の月には空気質が悪化します。

But wait. 
しかし、待ってください。

You may have read that air quality forecasting is a solved problem. 
あなたは、空気質予測が解決された問題であると読んだかもしれません。

In 2024, Microsoft AI built Aurora, a deep learning model that predicts air pollution for the whole world. 
2024年、Microsoft AIはAuroraを構築しました。これは、世界全体の大気汚染を予測する深層学習モデルです。

Microsoft’s use of AI was championed as a huge step forward compared with the physical models of air quality, which are computed on high-performance computing infrastructure by the European Union’s Copernicus project. 
MicrosoftのAIの使用は、EUのコペルニクスプロジェクトによって高性能コンピューティングインフラで計算される物理モデルと比較して、大きな前進と称賛されました。

However, as of mid-2024, if you examine the performance of Aurora in a city, such as Stockholm, you will see its predictions are not very accurate compared with the actual air quality sensor readings you can find on aqicn.org. 
しかし、2024年中頃の時点で、ストックホルムのような都市でAuroraのパフォーマンスを調べると、aqicn.orgで見つけることができる実際の空気質センサーの読み取り値と比較して、その予測があまり正確でないことがわかります。

Your challenge is therefore to build an AI system that produces better air quality predictions than Aurora for the location of your chosen air quality sensor at a fraction of its cost. 
したがって、あなたの課題は、選択した空気質センサーの位置に対してAuroraよりも優れた空気質予測を生成するAIシステムを、コストの一部で構築することです。

In this project, better-quality data and a decision tree ML model will outperform deep learning. 
このプロジェクトでは、より高品質のデータと決定木MLモデルが深層学習を上回ります。

Finally, every project benefits from a wow factor. 
最後に、すべてのプロジェクトは「ワオ」要素の恩恵を受けます。

We will sprinkle some GenAI dust on the project by making your air quality forecasting service “friendly” by giving it a voice-driven UI powered by an LLM. 
私たちは、LLMによって駆動される音声インターフェースを持たせることで、あなたの空気質予測サービスを「親しみやすく」するために、プロジェクトに少しGenAIの魔法を振りかけます。

###### AI System Overview
###### AIシステムの概要

In my course at KTH, students did project work to build a unique AI system that solved a prediction problem using a dynamic data source. 
私のKTHのコースでは、学生たちが動的データソースを使用して予測問題を解決するユニークなAIシステムを構築するプロジェクト作業を行いました。

But before they started their project, they had to get it approved, and I found that the simplest way to do so was with a prediction service card (see Table 3-1). 
しかし、彼らがプロジェクトを始める前に、承認を得る必要があり、最も簡単な方法は予測サービスカード（表3-1を参照）を使用することだとわかりました。

The card is a slimmed-down version of the kanban board from Figure 2-2, omitting the implementation details. 
このカードは、実装の詳細を省略した図2-2のカンバンボードの簡略版です。

-----
_Table 3-1. AI system card for our air quality forecasting service_
表3-1. 私たちの空気質予測サービスのAIシステムカード

**Dynamic data sources** **Prediction problem** **UI or API** **Monitoring**  
**動的データソース** **予測問題** **UIまたはAPI** **モニタリング**  
Air quality sensor data: _[https://aqicn.org](https://aqicn.org)_ Weather forecasts: _[https://open-meteo.com](https://open-meteo.com)_  
空気質センサーデータ: _[https://aqicn.org](https://aqicn.org)_ 天気予報: _[https://open-meteo.com](https://open-meteo.com)_  
Daily forecast of the level of PM2.5 for the next seven days at the position of an existing air quality sensor  
既存の空気質センサーの位置における次の7日間のPM2.5レベルの毎日の予測  
A web page with graphs and an LLM-powered UI in Python  
グラフとPythonでのLLM駆動のUIを持つウェブページ  
Hindcast graphs show prediction performance of our model  
ヒンドキャストグラフは、私たちのモデルの予測性能を示します  

The AI system card succinctly summarizes the system’s key properties, including the data sources and the prediction problem it solves. 
AIシステムカードは、データソースや解決する予測問題を含むシステムの主要な特性を簡潔に要約しています。

For example, with air quality, there are many possible air quality prediction problems, such as predicting PM10 levels (larger particles that include dust from roads and construction sites), and NO2 (nitrogen dioxide) levels (pollution mostly from internal combustion engine vehicles). 
例えば、空気質に関しては、PM10レベル（道路や建設現場からのほこりを含む大きな粒子）やNO2（窒素二酸化物）レベル（主に内燃機関車両からの汚染）を予測するなど、多くの可能な空気質予測問題があります。

The prediction service card also includes the data sources, which makes it useful as a feasibility test that the data exists and is accessible for your prediction problem. 
予測サービスカードにはデータソースも含まれており、データが存在し、予測問題にアクセス可能であるかどうかの実現可能性テストとして役立ちます。

You should also define how the predictions produced by our AI system will be consumed—by a UI or API. 
また、私たちのAIシステムが生成する予測がどのように消費されるか（UIまたはAPIによって）を定義する必要があります。

A UI is a very powerful tool for communicating the value of your model to stakeholders, and it is now straightforward to build functional UIs in Python. 
UIは、モデルの価値を利害関係者に伝えるための非常に強力なツールであり、Pythonで機能的なUIを構築することは今や簡単です。

In our AI system, we will use LLMs to improve the accessibility of our service—you should be able to ask the air quality forecasting service questions in natural language. 
私たちのAIシステムでは、LLMを使用してサービスのアクセシビリティを向上させます—あなたは空気質予測サービスに自然言語で質問できるようになるべきです。

And, finally, you should outline how you will monitor the performance of your running AI system to ensure it is performing as expected. 
最後に、実行中のAIシステムのパフォーマンスを監視し、期待通りに機能していることを確認する方法を概説する必要があります。

We will use open source and free serverless services to build our AI system—GitHub Actions/Pages and Hopsworks. 
私たちは、オープンソースで無料のサーバーレスサービスを使用してAIシステムを構築します—GitHub Actions/PagesとHopsworksです。

We will write the following Jupyter notebooks in Python: 
私たちは、以下のJupyterノートブックをPythonで作成します：

- Feature groups to store our data and backfill them with historical data  
- データを保存し、歴史的データでバックフィルするための特徴グループ  
- A daily feature pipeline to retrieve new data and store it in the feature store  
- 新しいデータを取得し、特徴ストアに保存するための毎日の特徴パイプライン  
- A training pipeline to train an XGBoost regression model and save it in the model registry  
- XGBoost回帰モデルを訓練し、モデルレジストリに保存するためのトレーニングパイプライン  
- A batch inference pipeline to download the model, make predictions on new feature data, and read from the feature store to produce air quality forecast/hindcast graphs  
- モデルをダウンロードし、新しい特徴データに対して予測を行い、特徴ストアから読み取って空気質予測/ヒンドキャストグラフを生成するためのバッチ推論パイプライン  

We will also use a number of libraries in Python and other technologies to build the system, including: 
私たちはまた、システムを構築するためにPythonや他の技術でいくつかのライブラリを使用します：

- REST APIs to read data from our air quality and weather data sources  
- 空気質および天気データソースからデータを読み取るためのREST API  
- Pandas for processing the data  
- データ処理のためのPandas  
- Hopsworks to store feature data and models  
- 特徴データとモデルを保存するためのHopsworks  
- XGBoost for our ML model as a gradient-boosted decision tree  
- 勾配ブースト決定木としてのMLモデルのためのXGBoost  

-----
- GitHub Actions to schedule our notebooks to run daily  
- 毎日ノートブックを実行するためにGitHub Actionsを使用  
- GitHub Pages as a dashboard web page containing the forecasts/hindcast graphs  
- 予測/ヒンドキャストグラフを含むダッシュボードウェブページとしてのGitHub Pages  

We will also write a Streamlit Python application with a voice and text-powered UI, backed by the open source Whisper transformer model that translates voice to text and an LLM that translates from text to function calls on our AI system. 
私たちはまた、音声とテキスト駆動のUIを持つStreamlit Pythonアプリケーションを作成します。これは、音声をテキストに変換するオープンソースのWhisperトランスフォーマーモデルと、テキストからAIシステムの関数呼び出しに変換するLLMによって支えられています。

That is a lot of technologies for our first project, but don’t be overawed. 
これは私たちの最初のプロジェクトにとって多くの技術ですが、圧倒されないでください。

Just like much great music can be made with three chords, many great AI systems can be made from a feature pipeline, a training pipeline, and an inference pipeline. 
素晴らしい音楽が3つのコードで作られるように、多くの素晴らしいAIシステムは特徴パイプライン、トレーニングパイプライン、推論パイプラインから作られます。

###### Air Quality Data
###### 空気質データ

Thousands of hobbyists around the world have installed air quality sensors and made their measurements publicly and freely available. 
世界中の何千人もの愛好家が空気質センサーを設置し、その測定値を公開かつ無料で利用可能にしています。

You can locate many of these air quality sensors with both historical and live data using the aqicn.org map. 
aqicn.orgの地図を使用して、歴史的データとライブデータの両方を持つ多くの空気質センサーを見つけることができます。

The website is an aggregator of sensor data from many sources, but as a community service, it provides no guarantees on the data quality. 
このウェブサイトは多くのソースからのセンサーデータの集約者ですが、コミュニティサービスとしてデータの品質に対する保証は提供していません。

I have selected a sensor in Stockholm that has both live and historical data available. 
私は、ライブデータと歴史的データの両方が利用可能なストックホルムのセンサーを選びました。

I chose it because it is very close to the Hopsworks office. 
私はそれを選んだ理由は、Hopsworksのオフィスに非常に近いからです。

_Figure 3-1. Export the air quality sensor’s historical data by clicking on the “Download this data (CSV format)” button._  
_図3-1. 「このデータをダウンロード（CSV形式）」ボタンをクリックして空気質センサーの歴史的データをエクスポートします。_

-----
You should pick a sensor either close to you or somewhere special to you. 
あなたは、自分の近くにあるセンサーか、特別な場所にあるセンサーを選ぶべきです。

Scroll down the page and you will find a button to download the historical data for that sensor. 
ページを下にスクロールすると、そのセンサーの歴史的データをダウンロードするためのボタンが見つかります。

If you can’t find the download link for the historical measurements on your sensor’s web page, you can probably find it in the World Air Quality Historical Database. 
センサーのウェブページで歴史的測定値のダウンロードリンクが見つからない場合、世界空気質歴史データベースで見つけることができるかもしれません。

If you still can’t find the download link, pick another sensor. 
それでもダウンロードリンクが見つからない場合は、別のセンサーを選んでください。

Unfortunately, as of mid-2025, there is no API call available to download historical data, so you have to perform this step manually. 
残念ながら、2025年中頃の時点で、歴史的データをダウンロードするためのAPI呼び出しは利用できないため、このステップを手動で実行する必要があります。

You will also need to create an API key on the AQICN website so that your feature pipeline can read the latest air quality values. 
また、あなたの特徴パイプラインが最新の空気質値を読み取れるように、AQICNウェブサイトでAPIキーを作成する必要があります。

Download the CSV file. 
CSVファイルをダウンロードしてください。

I renamed mine _air-quality-data.csv. 
私は自分のファイルを_air-quality-data.csvに名前を変更しました。

For your sensor, you should rename the CSV file you downloaded if it has spaces or unusual characters. 
あなたのセンサーの場合、ダウンロードしたCSVファイルにスペースや異常な文字が含まれている場合は、名前を変更するべきです。

You should open the CSV file in a text editor to check whether its column names are as expected. 
CSVファイルをテキストエディタで開いて、列名が期待通りであるかどうかを確認する必要があります。

Our backfilling Python program will read the CSV file into a Pandas DataFrame and expect that the CSV file has a header line and that two of the columns are named pm25 and date. 
私たちのバックフィリングPythonプログラムは、CSVファイルをPandas DataFrameに読み込み、CSVファイルにヘッダー行があり、2つの列がpm25とdateという名前であることを期待します。

If there are more columns, that is OK, as the program will ignore them. 
他に列があっても問題ありません。プログラムはそれらを無視します。



. If there are more columns, that is OK, as the program will ignore them. 
もし列がもっとあっても問題ありません。プログラムはそれらを無視します。

However, some files do not have a `pm25 column—instead, they have` ``` min/max/median/stdev daily measurements for PM2.5. 
しかし、一部のファイルには`pm25`列がなく、代わりにPM2.5の最小/最大/中央値/標準偏差の毎日の測定値があります。

The easiest way to fix this is to just rename the median column to pm25 in the header in your CSV file. 
これを修正する最も簡単な方法は、CSVファイルのヘッダーで中央値の列名をpm25に変更することです。

You also have to have the date column. 
また、日付列も必要です。

You can now create the GitHub repository for the project by forking the [book’s](https://github.com/featurestorebook/mlfs-book) [GitHub repository to your GitHub account. 
これで、[本の](https://github.com/featurestorebook/mlfs-book) GitHubリポジトリをフォークして、プロジェクトのためのGitHubリポジトリを作成できます。

You should move your CSV file to the](https://github.com/featurestorebook/mlfs-book) _data directory in your forked repository and replace the existing_ _data/air-quality-_ _data.csv file. 
フォークしたリポジトリの_dataディレクトリにCSVファイルを移動し、既存の_data/air-quality-data.csvファイルを置き換える必要があります。

You should also create an .env file from the .env.example template. 
また、.env.exampleテンプレートから.envファイルを作成する必要があります。

You need to update the following values in the .env file with your API key values and the URL, country, city, and street for your chosen sensor: 
次に、.envファイル内の以下の値を、選択したセンサーのAPIキーの値、URL、国、都市、通りで更新する必要があります：

```  
HOPSWORKS_API_KEY=<get your key from Hopsworks>   
AQICN_API_KEY=<get your key from aqicn.org>   
AQICN_URL=https://api.waqi.info/feed/@10009   
AQICN_COUNTRY=sweden   
AQICN_CITY=stockholm   
AQICN_STREET=hornsgatan-108
``` 

The .env file should not be committed to GitHub (it is in the .gitignore file). 
.envファイルはGitHubにコミットしてはいけません（それは.gitignoreファイルに含まれています）。

Commit and push your CSV file to GitHub. 
CSVファイルをGitHubにコミットしてプッシュしてください。

The CSV files are quite small (mine is 58 KB), so there is no problem storing them in GitHub. 
CSVファイルは非常に小さい（私のは58 KBです）ので、GitHubに保存することに問題はありません。

Files of GBs worth of data or larger are not suitable for storage in source-code repositories like GitHub.[2] 
GB単位のデータやそれ以上のファイルは、GitHubのようなソースコードリポジトリに保存するのには適していません。

When you’re working in Python, we strongly recommend that you create a virtual environment for the book, 
Pythonで作業しているときは、本のために仮想環境を作成することを強くお勧めします。

[using a Python dependency management framework such as Conda, Poetry, virtualenv,](https://conda.io) [or pipenv. 
Conda、Poetry、virtualenv、またはpipenvのようなPython依存関係管理フレームワークを使用して。

The dependencies introduced for our project can be installed in your virtual](https://github.com/pypa/pipenv) environment. 
私たちのプロジェクトのために導入された依存関係は、あなたの仮想環境にインストールできます。

2 Large files should be stored in highly available, scalable distributed storage, such as an S3 compatible object store. 
大きなファイルは、高可用性でスケーラブルな分散ストレージ、例えばS3互換のオブジェクトストアに保存するべきです。

These are also currently the cheapest places to store large files.  
これらは現在、大きなファイルを保存するための最も安価な場所でもあります。

environment. 
環境。

See the book’s source code repository for details on setting up a virtual environment and installing your Python dependencies for this project. 
このプロジェクトのための仮想環境の設定とPython依存関係のインストールに関する詳細は、本のソースコードリポジトリを参照してください。

In Chapter 2, we already discussed how to create your Hopsworks account and download an API key. 
第2章では、Hopsworksアカウントの作成方法とAPIキーのダウンロード方法についてすでに説明しました。

###### Exploratory Dataset Analysis
###### 探索的データセット分析

Before we jump in and start building, we should take some time to understand the data we will work with. 
私たちが飛び込んで構築を始める前に、私たちが扱うデータを理解するための時間を取るべきです。

In general, there are six properties or dimensions of any data source that you should understand before using it to solve a prediction problem:  
一般的に、予測問題を解決するためにデータソースを使用する前に理解すべき6つの特性または次元があります：

- Validity
- 有効性
- Accuracy
- 精度
- Consistency  
- 一貫性
- Uniqueness
- 一意性
- Update frequency
- 更新頻度
- Completeness  
- 完全性

Let’s now examine our air quality and weather data sources through this lens. 
それでは、この視点から私たちの空気質と天候データソースを検討してみましょう。

We recommend using Jupyter Notebooks instead of Google Cola‐ boratory (Colab) for this book. 
この本では、Google Colaboratory（Colab）の代わりにJupyter Notebooksを使用することをお勧めします。

The first cell in each notebook adds support for Colab, but you will have to update it to point to your forked repository. 
各ノートブックの最初のセルはColabのサポートを追加しますが、フォークしたリポジトリを指すように更新する必要があります。

Colab currently does not have good support for GitHub, so every notebook has to clone the repository and install all dependencies before it can run. 
Colabは現在、GitHubのサポートが不十分であるため、すべてのノートブックはリポジトリをクローンし、実行する前にすべての依存関係をインストールする必要があります。

There is also no support for sav‐ ing any changes you make to notebooks back to GitHub. 
ノートブックに加えた変更をGitHubに保存するためのサポートもありません。

Colab is still useful, however, if you need a free GPU. 
ただし、無料のGPUが必要な場合、Colabは依然として便利です。

###### Air Quality Data
###### 空気質データ

How does our air quality data source rank on these six properties of dataset quality? 
私たちの空気質データソースは、これらのデータセット品質の6つの特性においてどのように評価されますか？

We will start with data validity, a measure of how accurately the data reflects what it is intended to measure. 
データの有効性、つまりデータが意図された測定をどれだけ正確に反映しているかを測る指標から始めます。

We focus on measuring PM2.5 rather than PM10 or NO2, as, [according to the UN, “PM2.5…poses the greatest health threat,” according to current](https://oreil.ly/s79gI) knowledge. 
私たちは、PM10やNO2ではなくPM2.5の測定に焦点を当てます。なぜなら、[国連によれば、「PM2.5…は最大の健康リスクをもたらす」とのことです](https://oreil.ly/s79gI)。

Next up is data accuracy, which refers to how close the measurements are to the true value. 
次にデータの精度についてです。これは測定値が真の値にどれだけ近いかを指します。

The _[aqicn.org website tells me that my sensor’s data in Stockholm](http://aqicn.org)_ comes from “SLB·analys—Air Quality Management and Operator in the City of Stock‐ holm” and the “European Environment Agency.” 
_[aqicn.orgのウェブサイトによれば、私のセンサーのデータはストックホルムの「SLB·analys—空気質管理および運営者」と「欧州環境庁」から来ています](http://aqicn.org)。

Therefore, I am inclined to trust the data accuracy. 
したがって、私はデータの精度を信頼する傾向があります。

Returning to the stockholm-hornsgatan-108 dataset, we claim that the data is unique. 
ストックホルムのhornsgatan-108データセットに戻ると、私たちはデータが一意であると主張します。

After a web search, I am not aware of any other public air quality sensor on that street. 
ウェブ検索の結果、その通りに他の公共の空気質センサーが存在することは知りません。

Looking at the data from Figure 3-1, I can see that the data is mostly complete, quite _consistent (the colors indicating air quality follow a predictable pattern), and_ timely (it arrives hourly).  
図3-1のデータを見ると、データはほぼ完全であり、かなり_一貫性があり（空気質を示す色は予測可能なパターンに従っています）、_タイムリーです（毎時到着します）。

In general, you should also examine the data in a notebook to check its completeness. 
一般的に、データの完全性を確認するためにノートブックでデータを調べるべきです。

In the following code snippet, we read the CSV file as a Pandas DataFrame and then keep only those columns we need from our air quality dataset (the date and our target, pm25): 
次のコードスニペットでは、CSVファイルをPandas DataFrameとして読み込み、空気質データセットから必要な列（日時とターゲットであるpm25）のみを保持します：

```  
# you may need to rename columns in your CSV file to 'pm25' and 'date'   
# CSVファイル内の列名を「pm25」と「date」に変更する必要があるかもしれません。  
df = pd.read_csv("../../data/stockholm-hornsgatan-108.csv", parse_dates=['date'], skipinitialspace=True)   
df_aq = df[["date", "pm25"]]
``` 

We also read the `country,` `city,` `street, and` `url for the sensor from` _.env using a_ Pydantic settings object and add them as columns to df_aq. 
私たちはまた、_.envからセンサーの`country`、`city`、`street`、および`url`をPydantic設定オブジェクトを使用して読み込み、df_aqに列として追加します。

We will use the city col‐ umn to join our air quality data with the weather features for the same date. 
私たちは、同じ日付の天候特徴と空気質データを結合するために、city列を使用します。

We use the city value to retrieve the longitude and latitude that is required to download the weather data. 
私たちは、天候データをダウンロードするために必要な経度と緯度を取得するためにcityの値を使用します。

The `country,` `city, and` `street columns are` _helper columns that are_ used when we create a dashboard with air quality forecasts. 
`country`、`city`、および`street`列は、空気質予測のダッシュボードを作成する際に使用される_補助列です。

We also store `country,` ``` city, street, url, HOPSWORKS_API_KEY, and AQICN_API_KEY as a secret in Hops‐ works, 
私たちはまた、`country`、`city`、`street`、`url`、`HOPSWORKS_API_KEY`、および`AQICN_API_KEY`をHopsworksの秘密として保存します。

so that later notebooks (daily feature pipeline, training pipeline, and inference pipeline) do not need to read their values from the .env file. 
これにより、後のノートブック（デイリーフィーチャーパイプライン、トレーニングパイプライン、推論パイプライン）は、.envファイルからその値を読み取る必要がなくなります。

The second part of evaluating dataset completeness is to check for missing data. 
データセットの完全性を評価するための2つ目の部分は、欠損データをチェックすることです。

You can call the isna() function on the DataFrame to list any missing values. 
DataFrameに対してisna()関数を呼び出すことで、欠損値をリストアップできます。

However, that may produce a huge number of rows as output, so instead, we will apply a sum() to the result of isna(), summarizing how many values are missing for each column in df: 
ただし、それは大量の行を出力する可能性があるため、代わりにisna()の結果にsum()を適用し、dfの各列に対して欠損している値の数を要約します：

```  
df.isna().sum()
``` 

You can then remove any rows with any missing columns by calling: 
次に、欠損列を持つ行を削除するには、次のように呼び出します：

```  
df.dropna(inplace=True)
``` 

Removing missing observations is reasonable at this point, as there will be no point in collecting data where either the date or the target is missing. 
この時点で欠損観測値を削除することは合理的です。なぜなら、日付またはターゲットが欠損しているデータを収集する意味がないからです。

Often, at this point, we would dive deeper into identifying data sources and candidate features for our model. 
通常、この時点で、私たちはデータソースとモデルの候補特徴を特定するためにさらに深く掘り下げます。

We would try to identify features that have predictive power for the target (PM2.5). 
私たちは、ターゲット（PM2.5）に対して予測力を持つ特徴を特定しようとします。

If there are not enough samples for deep learning models to be performant, we might try to engineer features that capture domain knowledge about our prediction problem. 
深層学習モデルが性能を発揮するためのサンプルが不十分な場合、私たちは予測問題に関するドメイン知識を捉える特徴をエンジニアリングしようとするかもしれません。

However, we will skip those steps in this case, to model it as a simpler prediction problem. 
しかし、今回はそれらのステップをスキップし、より単純な予測問題としてモデル化します。

We will use weather features for our model, as they have good predictive power for PM2.5 levels. 
私たちは、PM2.5レベルに対して良好な予測力を持つため、モデルに天候特徴を使用します。

There will be room for improvement in the model we will train, but right now, our goal is to build an MVPS for our air qual‐ ity forecasting problem. 
私たちがトレーニングするモデルには改善の余地がありますが、今のところ、私たちの目標は空気質予測問題のためのMVPSを構築することです。



###### Weather Data 天気データ

[We will use Open-Meteo to download both historical weather data and weather fore‐](https://open-meteo.com) cast data for the same location as that of your chosen air quality sensor. 
私たちは、選択した空気質センサーと同じ場所の過去の天気データと天気予報データをダウンロードするためにOpen-Meteoを使用します。 
The weather data from Open-Meteo ranks very high on all of our six axes of dataset quality. 
Open-Meteoの天気データは、私たちのデータセット品質の6つの軸すべてで非常に高い評価を得ています。 
OpenMeteo provides two different free APIs: one to download historical weather data and one for weather forecasts. 
OpenMeteoは、過去の天気データをダウンロードするためのAPIと天気予報用のAPIの2つの異なる無料APIを提供しています。 
You do not need an API key. 
APIキーは必要ありません。 
If you are not sure of the best city to use for your weather data, you can search for available weather locations at [Open-Meteo’s Historical Weather API page. In contrast to air quality data, which is](https://oreil.ly/q7LYd) very localized (two neighboring streets could have very different air quality condi‐ tions), weather data at the city or even region level is probably good enough for your model. 
天気データに最適な都市がわからない場合は、[Open-Meteoの過去の天気APIページで利用可能な天気の場所を検索できます。空気質データは非常に局所的であるのに対し（隣接する2つの通りで空気質条件が非常に異なる可能性があります）、都市レベルまたは地域レベルの天気データは、おそらくモデルにとって十分です。 

We will restrict ourselves to those weather conditions that are universally available at weather stations and have the highest predictive power for air quality: precipitation, wind speed, wind direction, and temperature. 
私たちは、気象観測所で普遍的に利用可能で、空気質に対して最も予測力の高い気象条件（降水量、風速、風向、温度）に制限します。 
The Open-Meteo APIs expect longi‐ tude and latitude as parameters for your weather location. 
Open-MeteoのAPIは、天気の場所のパラメータとして経度と緯度を期待します。 
We use the geopy library to resolve the longitude and latitude for a city name that you need to specify (you may need to enter the longitude and latitude manually, if the geopy server blocks your IP). 
私たちは、指定する必要がある都市名の経度と緯度を解決するためにgeopyライブラリを使用します（geopyサーバーがあなたのIPをブロックする場合は、経度と緯度を手動で入力する必要があるかもしれません）。 

In the following code snippet using the historical API, we need to provide the loca‐ tion and time range as longitude, latitude, start_date, and end_date parameters: 
以下のコードスニペットでは、過去のAPIを使用して、経度、緯度、start_date、およびend_dateパラメータとして位置と時間範囲を提供する必要があります： 
```     
     url = "https://archive-api.open-meteo.com/v1/archive"     
     params = {       
       "latitude": latitude,       
       "longitude": longitude,       
       "start_date": start_date,       
       "end_date": end_date,       
       "daily": ["temperature_2m_mean", "precipitation_sum",         
         "wind_speed_10m_max", "wind_direction_10m_dominant"]     
     }     
     responses = openmeteo.weather_api(url, params=params) 
``` 
天気予報データは、同様のREST呼び出しによって取得されます： 
The weather forecast data will be retrieved by a similar REST call: 
```     
     url = "https://api.open-meteo.com/v1/ecmwf"     
     params = {       
       "latitude": latitude,       
       "longitude": longitude,       
       "daily": ["temperature_2m", "precipitation",         
         "wind_speed_10m", "wind_direction_10m"]     
     }     
     responses = openmeteo.weather_api(url, params=params) 
``` 
However, you should note that our forecast API call receives hourly forecasts but our historical API call retrieves aggregate data over a day (i.e., mean temperature, sum of precipitation, and max wind speed). 
ただし、予報API呼び出しは時間ごとの予報を受け取りますが、過去のAPI呼び出しは1日の集計データ（すなわち、平均温度、降水量の合計、最大風速）を取得することに注意してください。 
This is not ideal, but it is good enough for our purposes (we did say the model could be improved!). 
これは理想的ではありませんが、私たちの目的には十分です（モデルは改善できると言いました！）。 

There are two utility functions, get_historical_weather() and get_weather_fore ``` cast(), defined in weather-util.py that return the weather data as Pandas DataFrames:   
2つのユーティリティ関数、get_historical_weather()とget_weather_forecast()がweather-util.pyに定義されており、天気データをPandas DataFrameとして返します：   
   historical_weather_df = util.get_historical_weather("Stockholm", "2019-01-01",     
     "2024-03-01")   
   weather_forecast_df = util.get_weather_forecast("Stockholm") 
``` 
Note that these functions make network calls, so the code may fail if the program does not have internet connectivity. 
これらの関数はネットワーク呼び出しを行うため、プログラムがインターネット接続を持っていない場合、コードが失敗する可能性があります。 
The same holds for the function we will use to retrieve real-time air quality data. 
リアルタイムの空気質データを取得するために使用する関数にも同様のことが当てはまります。 

###### Creating and Backfilling Feature Groups 特徴グループの作成とバックフィリング

We will store our featurized DataFrames in feature groups in the Hopsworks Feature Store. 
私たちは、特徴化されたDataFrameをHopsworks Feature Storeの特徴グループに保存します。 
We will have two feature groups: one for air quality data (containing the obser‐ vations of PM2.5 values, the location, and the timestamps for those observations) and another to store both the historical weather observations and the weather forecast data. 
空気質データ用の1つの特徴グループ（PM2.5値の観測、位置、およびそれらの観測のタイムスタンプを含む）と、過去の天気観測と天気予報データの両方を保存するための別の特徴グループの2つを持ちます。 
Feature groups store the incremental feature data created over time: 
特徴グループは、時間の経過とともに作成された増分特徴データを保存します： 
```   
   air_quality_fg = fs.get_or_create_feature_group(     
     name='air_quality',     
     description='Air Quality observations daily',     
     version=1,     
     primary_key=['country', 'city', 'street'],     
     expectation_suite = aq_expectation_suite,     
     event_time="date",   
   )     
   air_quality_fg.insert(df_aq) 
``` 
We call get_or_create_feature_group(), instead of just create_feature_group(), as we want the notebook to be idempotent (create_feature_group() fails if the fea‐ ture group already exists): 
私たちは、ノートブックが冪等性を持つように、単にcreate_feature_group()の代わりにget_or_create_feature_group()を呼び出します（feature groupがすでに存在する場合、create_feature_group()は失敗します）： 
```   
   weather_fg = fs.get_or_create_feature_group(     
     name='weather',     
     description='Historical daily weather observations and weather forecasts',     
     version=1,     
     primary_key=['city'],     
     event_time="date",     
     expectation_suite = weather_expectation_suite   
   )   
   weather_fg.insert(df_weather) 
``` 
Notice that both feature groups define an expectation_suite parameter. 
両方の特徴グループがexpectation_suiteパラメータを定義していることに注意してください。 
This is a set of data validation rules that we declaratively attach once to the feature group but are applied every time we write a DataFrame to the feature group.i 
これは、私たちが一度特徴グループに宣言的に付加するデータ検証ルールのセットですが、DataFrameを特徴グループに書き込むたびに適用されます。 

We can define data quality tests to validate data retrieved from the air quality and weather data sources. 
空気質データと天気データソースから取得したデータを検証するためのデータ品質テストを定義できます。 
These will help identify faults in the sensor from the moment [they start happening. Great Expectations is a popular open source library for declara‐](https://greatexpectations.io) tively specifying data validation rules. 
これにより、センサーの故障を特定するのに役立ちます。Great Expectationsは、データ検証ルールを宣言的に指定するための人気のオープンソースライブラリです。 
In the following code snippet, we define an expectation in Great Expectations that checks all the values in the pm25 column in our DataFrame, df, to make sure that the scraped values are neither negative nor greater than 500 (a reasonable upper limit for the expected PM2.5 values for my location): 
以下のコードスニペットでは、私たちのDataFrameであるdfのpm25列のすべての値をチェックし、スクレイピングされた値が負でないこと、または500を超えないことを確認するGreat Expectationsでの期待を定義します（私の場所のPM2.5値の期待される上限として合理的な値）： 
```   
   import great_expectations as ge   
   aq_expectation_suite = ge.core.ExpectationSuite(     
     expectation_suite_name="aq_expectation_suite"   
   )   
   aq_expectation_suite.add_expectation(     
     ge.core.ExpectationConfiguration(       
       expectation_type="expect_column_min_to_be_between"       
       kwargs={         
         "column":"pm25",         
         "min_value":0.0,         
         "max_value":500.0,         
         "strict_min":True       
       }     
     )   
   ) 
``` 
In Hopsworks, you can easily add a notification (via Slack or email) if a data valida‐ tion rule fails and set the policy to either ingest the data and warn or fail the inges‐ tion. 
Hopsworksでは、データ検証ルールが失敗した場合に通知（Slackまたはメール経由）を簡単に追加し、データを取り込んで警告するか、取り込みを失敗させるかのポリシーを設定できます。 
In the book’s source code repository, there are also similar expectations defined for the weather data in the temperature_2m and precipitation columns. 
本書のソースコードリポジトリには、temperature_2mおよびprecipitation列の天気データに対しても同様の期待が定義されています。 

###### Feature Pipeline 特徴パイプライン

We just presented the program that creates the feature groups and backfills them with historical data. 
私たちは、特徴グループを作成し、過去のデータでバックフィルするプログラムを提示しました。 
But we also need to process new data daily. 
しかし、毎日新しいデータを処理する必要もあります。 
We could extend our pre‐ vious program and parameterize it to run in either backfill mode or normal mode. 
以前のプログラムを拡張し、バックフィルモードまたは通常モードで実行するようにパラメータ化することもできます。 
But, instead, we will write the daily feature pipeline as a separate program—this sepa‐ rates the concerns of creating the feature groups and backfilling them from daily updates to the feature groups. 
しかし、代わりに、日次の特徴パイプラインを別のプログラムとして記述します。これにより、特徴グループを作成し、バックフィルすることと、特徴グループへの日次更新の懸念が分離されます。 
The common functions used by the backfill and daily feature pipelines are defined in modules in the mlfs/airquality package. 
バックフィルと日次特徴パイプラインで使用される共通の関数は、mlfs/airqualityパッケージのモジュールに定義されています。 
The daily feature pipeline will be scheduled to run once per day, performing the fol‐ lowing tasks: 
日次の特徴パイプラインは、1日1回実行されるようにスケジュールされ、以下のタスクを実行します： 
- Read today’s PM2.5 measurement 
- 今日のPM2.5測定を読み取る 
- Read today’s weather data measurements  
- 今日の天気データ測定を読み取る 
- Read the weather forecast data for the next seven days 
- 次の7日間の天気予報データを読み取る 
- Insert all of this data into the air quality and weather feature groups 
- これらすべてのデータを空気質と天気の特徴グループに挿入する 

There is no feature engineering required in this example. 
この例では特徴エンジニアリングは必要ありません。 
We will read all of the data as numerical feature data and will not encode that data before it is written to feature groups. 
すべてのデータを数値的な特徴データとして読み取り、特徴グループに書き込む前にそのデータをエンコードしません。 
The code shown for downloading the sensor readings and weather forecasts is found in the functions/util.py module: 
センサーの読み取り値と天気予報をダウンロードするためのコードは、functions/util.pyモジュールにあります： 
```   
   url = f"{aqicn_url}/?token={AQI_API_KEY}"   
   data = trigger_request(url)   
   aq_today_df = pd.DataFrame()   
   aq_today_df['pm25'] = [data['data']['iaqi'].get('pm25', {}).get('v', None)]   
   aq_today_df['city'] = city   
   .. 
   aq_today_df['date'] = datetime.date.today()   
   air_quality_fg.insert(df_air_quality)   
   url = "https://api.open-meteo.com/v1/ecmwf"   
   params = {       
       "latitude": latitude,       
       "longitude": longitude,       
       "hourly": ["temperature_2m", "precipitation",   
       "wind_speed_10m", "wind_direction_10m"]   
   }   
   responses = openmeteo.weather_api(url, params=params)   
   hourly_df = # populate with responses data   
   daily_df = hourly_df.between_time('11:59', '12:01')   
   weather_fg.insert(daily_df) 
``` 
Our API calls to aqicn and Open-Meteo return the air quality and weather forecast data, respectively, and we put the returned data into Pandas DataFrames that are then inserted into their respective feature groups. 
aqicnおよびOpen-MeteoへのAPI呼び出しは、それぞれ空気質データと天気予報データを返し、返されたデータをPandas DataFrameに入れ、それをそれぞれの特徴グループに挿入します。 
When you insert the DataFrame into the feature group, its data validation rules will be executed. 
DataFrameを特徴グループに挿入すると、そのデータ検証ルールが実行されます。 
You can see the results of your historical feature pipeline executions in the Hops‐ works UI. 
Hopsworks UIで過去の特徴パイプラインの実行結果を見ることができます。 
Log in to Hopsworks and navigate to “Feature group” → “Recent activity” to see the result of ingestion runs. 
Hopsworksにログインし、「Feature group」→「Recent activity」に移動して、取り込み実行の結果を確認してください。 
You can inspect the content of your feature group in “Feature group” → “Data preview.” 
「Feature group」→「Data preview」で特徴グループの内容を確認できます。 
Have a look at “Feature group” → “Feature sta‐ tistics” to see descriptive statistics computed over the data inserted and the data vali‐ dation results in “Feature group” → “Expectations.” 
「Feature group」→「Feature statistics」で挿入されたデータに対して計算された記述統計と、「Feature group」→「Expectations」でのデータ検証結果を確認してください。 

###### Training Pipeline トレーニングパイプライン

We decided that we would model PM2.5 as a regression problem, and we know we will only have a few hundred or possibly a thousand rows or so. 
私たちは、PM2.5を回帰問題としてモデル化することに決め、数百行またはおそらく千行程度しかないことを知っています。 
This is decidedly in the realm of small data, so we will not use deep learning. 
これは明らかに小さなデータの範疇にあるため、深層学習は使用しません。 
Instead, we will use the [go-to ML framework for small data—XGBoost, an open source gradient-boosted](https://oreil.ly/fbhXp) decision tree framework. 
代わりに、私たちは小さなデータのための定番のMLフレームワークであるXGBoost（オープンソースの勾配ブースト決定木フレームワーク）を使用します。 
XGBoost works well out of the box, and we won’t do any 
XGBoostは、すぐに使える状態でうまく機能し、私たちは何も行いません。



hyperparameter tuning here—we will leave that as an exercise for you to squeeze more performance out of the model.
ここではハイパーパラメータの調整について触れますが、モデルのパフォーマンスをさらに引き出すための演習として残しておきます。

We will start by selecting the features we are going to use in our model. 
私たちは、モデルで使用する特徴量を選択することから始めます。

For this, we will use the feature view in Hopsworks. 
そのために、Hopsworksのフィーチャービューを使用します。

A _feature view defines the schema for a_ model—its input features and output targets (or labels). 
フィーチャービューはモデルのスキーマを定義します—その入力特徴量と出力ターゲット（またはラベル）です。

Hopsworks provides a Pandas-like API for selecting features from different feature groups and then joining the selected features together using a query object. 
Hopsworksは、異なるフィーチャーグループから特徴量を選択し、選択した特徴量をクエリオブジェクトを使用して結合するためのPandasのようなAPIを提供します。

The select() and select_all() methods on a feature group return a `query object that provides a` `join() method` (more details in Chapter 5). 
フィーチャーグループのselect()およびselect_all()メソッドは、`join()メソッドを提供するクエリオブジェクト`を返します（詳細は第5章を参照）。

When you create the feature view, you also specify which of the selected features are the label columns. 
フィーチャービューを作成する際に、選択した特徴量の中でどれがラベル列であるかも指定します。

The code for selecting the features from the feature groups, joining them together using the common `'city' column, and` creating the feature view looks like this: 
フィーチャーグループから特徴量を選択し、共通の'city'列を使用してそれらを結合し、フィーチャービューを作成するためのコードは次のようになります：

```  
selected_features = \  
air_quality_fg.select(['pm25']).join(weather_fg.select_all(on=['city']))  
feature_view = fs.create_feature_view(  
name='air_quality_fv',  
version=version,  
labels=['pm25'],  
query=selected_features  
)
```

With a feature view object, you can now create training data: 
フィーチャービューオブジェクトを使用して、トレーニングデータを作成できます：

```  
X_train, X_test, y_train, y_test = feature_view.train_test_split(test_size=0.2)
```

Here, we read training data as Pandas DataFrames, which are randomly split (80/20) into training set features (X_train), training set labels (y_train), test set features (X_test), and test set labels (y_test). 
ここでは、トレーニングデータをPandas DataFrameとして読み込み、ランダムに分割（80/20）してトレーニングセットの特徴量（X_train）、トレーニングセットのラベル（y_train）、テストセットの特徴量（X_test）、およびテストセットのラベル（y_test）を作成します。

In a single call, `train_test_split reads the` data, joins the air quality and weather data, and then performs a Scikit-Learn random split of the data into features and labels for both training and test sets. 
1回の呼び出しで、`train_test_splitはデータを読み込み、`空気質と天気データを結合し、次にScikit-Learnのランダム分割を行ってトレーニングセットとテストセットの特徴量とラベルに分けます。

The reason I chose a random split over a time-series split is that our chosen features are not time dependent. 
私が時間系列分割よりもランダム分割を選んだ理由は、選択した特徴量が時間に依存しないからです。

A useful exercise would be to improve this air quality model by adding features related to air quality (historical air quality, seasonality factors, and so on) and change to a time-series split. 
有用な演習として、空気質に関連する特徴量（過去の空気質、季節要因など）を追加してこの空気質モデルを改善し、時間系列分割に変更することが考えられます。

We can now train our model using `XGBoostRegressor. 
これで、`XGBoostRegressor`を使用してモデルをトレーニングできます。

We simply fit our model to` our features and labels from the training set, using the default hyperparameters for 
私たちは、トレーニングセットからの特徴量とラベルにモデルを適合させるだけで、デフォルトのハイパーパラメータを使用します。

``` 
XGBoostRegressor:  
clf = XGBRegressor()  
clf.fit(X_train, y_train)
```

Training should only take a few milliseconds. 
トレーニングには数ミリ秒しかかからないはずです。

Then, you can evaluate the trained model, clf, using the features from our test set to produce predictions, y_pred: 
次に、テストセットからの特徴量を使用してトレーニングされたモデルclfを評価し、予測y_predを生成できます：

```  
y_pred = clf.predict(X_test)  
mse = mean_squared_error(y_test, y_pred, squared=False)  
r2 = r2_score(y_test, y_pred)  
plot_importance(clf, max_num_features=4)
```

Because we are modeling PM2.5 prediction as a regression problem, we are using mean squared error (MSE) and R-squared error as metrics to evaluate model performance. 
私たちはPM2.5の予測を回帰問題としてモデル化しているため、モデルのパフォーマンスを評価するための指標として平均二乗誤差（MSE）とR二乗誤差を使用しています。

An alternative to MSE is the mean absolute error (MAE), but MSE punishes a model more if its predictions are wildly off from the outcome compared with MAE. 
MSEの代替として平均絶対誤差（MAE）がありますが、MSEは予測が結果から大きく外れた場合にモデルに対してより厳しいペナルティを与えます。

With the scikit-learn library, it just takes a method call to compute one of many different model performance metrics when you have your outcomes (y_test) and your predictions (y_pred) readily available. 
scikit-learnライブラリを使用すると、結果（y_test）と予測（y_pred）がすぐに利用可能な場合、さまざまなモデルパフォーマンス指標の1つを計算するのにメソッド呼び出しだけで済みます。

We also calculate feature importance, which we later save as a PNG file. 
また、特徴量の重要度も計算し、後でPNGファイルとして保存します。

Now, we need to save the output of this training pipeline, our trained model, clf, to a model registry. 
今、私たちはこのトレーニングパイプラインの出力、トレーニングされたモデルclfをモデルレジストリに保存する必要があります。

We will use the Hopsworks model registry. 
Hopsworksのモデルレジストリを使用します。

This process involves first saving the model to a local directory and then registering the model to the model reg‐ istry, including its name (air_quality_xgboost_model) and description, its evalua‐ tion metrics, and the feature view used to create the training data for the model: 
このプロセスでは、まずモデルをローカルディレクトリに保存し、その後、モデルの名前（air_quality_xgboost_model）や説明、評価指標、モデルのトレーニングデータを作成するために使用されたフィーチャービューを含めてモデルレジストリに登録します：

```  
model_dir = "air_quality_model"  
os.makedirs(model_dir + "/images")  
clf.save_model(model_dir + "/model.json")  
plt.savefig(model_dir + "/images/feature_importance.png")  
mr = project.get_model_registry()  
mr.python.create_model(  
name="air_quality_xgboost_model",  
description="Air Quality (PM2.5) predictor.",  
metrics={ "MSE": mse, "r2": r2 },  
feature_view = feature_view  
)  
mr.save(model_dir)
```

The model registry client extracts the schema and lineage for the model using the feature view object. 
モデルレジストリクライアントは、フィーチャービューオブジェクトを使用してモデルのスキーマと系譜を抽出します。

Any other files in the local directory containing the model will also be uploaded, and any PNG/JPEG files in the _images subdirectory_ (feature_importance.png) will be shown in the “Model evaluation images” section (see Figure 3-2).  
モデルを含むローカルディレクトリ内の他のファイルもアップロードされ、_imagesサブディレクトリ内のPNG/JPEGファイル（feature_importance.png）は「モデル評価画像」セクションに表示されます（図3-2を参照）。

_Figure 3-2. Our XGBoost regression model is stored in the model registry, along with_ _model metrics and two model evaluation images._
図3-2. 私たちのXGBoost回帰モデルは、モデルメトリクスと2つのモデル評価画像とともにモデルレジストリに保存されています。

Notice that every time we register a model, we get a new version of the model. 
モデルを登録するたびに、新しいバージョンのモデルが得られることに注意してください。

Unlike feature groups and feature views, we don’t need to provide the version for the model when creating it—an auto-incrementing version number will be assigned to the newly registered model. 
フィーチャーグループやフィーチャービューとは異なり、モデルを作成する際にバージョンを提供する必要はありません—新しく登録されたモデルには自動インクリメントのバージョン番号が割り当てられます。

With our trained model in the model registry, we can now write our batch inference pipeline that will generate our air quality dashboard. 
モデルレジストリにトレーニングされたモデルがあるので、空気質ダッシュボードを生成するバッチ推論パイプラインを書くことができます。

###### Batch Inference Pipeline
###### バッチ推論パイプライン

The batch inference pipeline is a Python program that downloads the trained model from the model registry, fetches the weather forecast feature data, and uses the model and the weather forecast data to predict air quality for the next seven days. 
バッチ推論パイプラインは、モデルレジストリからトレーニングされたモデルをダウンロードし、天気予報の特徴データを取得し、モデルと天気予報データを使用して次の7日間の空気質を予測するPythonプログラムです。

We will make seven different predictions, one for each of the seven days. 
私たちは7日間それぞれに対して1つの異なる予測を行います。

We will create a [graph of the air quality forecasts using Plotly, save that graph as a PNG file, and push](https://plotly.com) that PNG file to a GitHub repository that contains a public website with GitHub Pages. 
Plotlyを使用して空気質予測のグラフを作成し、そのグラフをPNGファイルとして保存し、そのPNGファイルをGitHub Pagesを含む公開ウェブサイトを持つGitHubリポジトリにプッシュします。

First, we need to download our model from the model registry and load it using the 
まず、モデルレジストリからモデルをダウンロードし、次のようにして`XGBRegressor`オブジェクトを使用してロードする必要があります：

```  
model_ref = mr.get_model(  
name="air_quality_xgboost_model",  
version=1,  
)  
saved_model_dir = model_ref.download()  
retrieved_xgboost_model = XGBRegressor()  
retrieved_xgboost_model.load_model(saved_model_dir + "/model.json")
```

Then, we read a batch of inference data (our weather forecast data for the next seven days) using the weather feature group: 
次に、天気フィーチャーグループを使用して推論データのバッチ（次の7日間の天気予報データ）を読み込みます：

```  
batch_df = weather_fg.filter(weather_fg.date >= today).read()
```

The `batch_df DataFrame now contains the weather forecast features for the next` seven days. 
`batch_df` DataFrameには、次の7日間の天気予報の特徴量が含まれています。

With these features, we can now make the predictions using the model: 
これらの特徴量を使用して、モデルを使って予測を行うことができます：

```  
features = batch_df[['temperature_2m_mean', 'precipitation_sum', \  
'wind_speed_10m_max', 'wind_direction_10m_dominant']]  
batch_df['predicted_pm25'] = model.predict(features)  
batch_df['days_before_forecast_day'] = range(1, len(batch_df)+1)
```

We store the predictions in the pm25_predicted column of batch_df along with the number of days before the forecast. 
予測を`batch_df`の`pm25_predicted`列に保存し、予測までの日数も記録します。

There are seven forecasts, one for each day. 
7つの予測があり、各日ごとに1つずつです。

The first one is seven days beforehand, and the last forecast is one day beforehand. 
最初の予測は7日前のもので、最後の予測は1日前のものです。

This `days_before_forecast_day column will help us evaluate the performance of our` 
この`days_before_forecast_day`列は、私たちのモデルのパフォーマンスを評価するのに役立ちます。

model depending on how many days in advance it is forecasting. 
モデルが何日前に予測しているかに応じて評価します。

We are going to save `batch_df to the feature store, to be used to monitor the features/predictions, as batch_df includes the predictions, feature values, and helper columns: 
`batch_df`をフィーチャーストアに保存し、特徴量/予測を監視するために使用します。`batch_df`には予測、特徴量の値、補助列が含まれています：

```  
monitoring_fg = fs.get_or_create_feature_group(  
name='monitoring_aq',  
description='Monitor Air Quality predictions’,  
version=1,  
primary_key=['city', 'street']  
)  
monitoring_fg.insert(batch_df)
```

We also have to plot our air quality prediction dashboard. 
また、空気質予測ダッシュボードをプロットする必要があります。

We will use the plotly library: 
plotlyライブラリを使用します：

```  
import plotly.express as px  
fig = px.line(batch_df, x = "date", y = "pm25_predicted", title = "..")  
….  
fig.write_image(file="forecast.png", format="png", width=1920, height=1280)
```

We will use a GitHub Action to publish the _forecast.png file on a web page, as_ described in the next section (see Figure 3-3). 
次のセクションで説明するように、GitHub Actionを使用して_webpage上に_forecast.pngファイルを公開します（図3-3を参照）。

_Figure 3-3. The GitHub Pages website contains our air quality forecast as a Plotly chart_ _and the hindcast (shown here) that shows both the predicted PM2.5 and actual PM2.5_ _values._
図3-3. GitHub Pagesウェブサイトには、私たちの空気質予測がPlotlyチャートとして表示され、ここに示されているように、予測されたPM2.5と実際のPM2.5値の両方を示すヒンドキャストが含まれています。

Finally, we create some hindcast PNG files that compare our model’s predictions, from the monitoring feature group data, and the outcomes, from the air quality feature group data. 
最後に、監視フィーチャーグループデータからのモデルの予測と、空気質フィーチャーグループデータからの結果を比較するヒンドキャストPNGファイルを作成します。

See the batch inference pipeline notebook in the book’s source code repository for details. 
詳細については、本のソースコードリポジトリにあるバッチ推論パイプラインノートブックを参照してください。

###### Running the Pipelines
###### パイプラインの実行

To get started, you should run the Jupyter notebooks on your laptop to ensure they work as expected. 
始めるには、Jupyterノートブックをノートパソコンで実行して、期待通りに動作することを確認する必要があります。

Run them from the first cell to the last cell. 
最初のセルから最後のセルまで実行してください。

You should switch to the Hopsworks UI after running each notebook to see the changes made—such as creating a feature group, writing to a feature group, creating a feature view, and saving a trained model to the model registry. 
各ノートブックを実行した後、Hopsworks UIに切り替えて、フィーチャーグループの作成、フィーチャーグループへの書き込み、フィーチャービューの作成、トレーニングされたモデルをモデルレジストリに保存するなどの変更を確認してください。

First, run the feature backfill notebook (1_air_quality_feature_backfill.ipynb). 
まず、フィーチャーバックフィルノートブック（1_air_quality_feature_backfill.ipynb）を実行します。

This will create the air_quality and weather feature groups. 
これにより、air_qualityおよびweatherフィーチャーグループが作成されます。

You should then run the feature pipeline (2_air_quality_feature_pipeline.ipynb) and check the feature groups to see if new rows have been added to them as expected. 
次に、フィーチャーパイプライン（2_air_quality_feature_pipeline.ipynb）を実行し、フィーチャーグループに新しい行が追加されているかどうかを確認します。

Then, you can train your model by running the model training pipeline (3_air_quality_training_pipeline.ipynb); verify that the feature view (air_quality_fv) was created and the trained_
次に、モデルトレーニングパイプライン（3_air_quality_training_pipeline.ipynb）を実行してモデルをトレーニングできます。フィーチャービュー（air_quality_fv）が作成され、トレーニングされた_



model is in the model registry. 
モデルはモデルレジストリにあります。

Finally, test that your batch inference pipeline (4_air_quality_batch_inference.ipynb) works as expected—it should have created an ``` aq_predictions feature group. 
最後に、バッチ推論パイプライン（4_air_quality_batch_inference.ipynb）が期待通りに動作するかテストしてください。これは、``` aq_predictions フィーチャーグループを作成しているはずです。

If you find a bug, please post a GitHub issue. 
バグを見つけた場合は、GitHubのイシューを投稿してください。

If you can improve the code, please file a pull request (PR). 
コードを改善できる場合は、プルリクエスト（PR）を提出してください。

If you need help, please ask questions on the Hopsworks Slack linked in the book’s GitHub repository. 
助けが必要な場合は、本のGitHubリポジトリにリンクされたHopsworks Slackで質問してください。

###### Scheduling the Pipelines as a GitHub Action
###### パイプラインをGitHub Actionとしてスケジュールする

We will use GitHub Actions to schedule the feature and batch inference pipelines and build our dashboard using GitHub Pages. 
私たちは、GitHub Actionsを使用してフィーチャーおよびバッチ推論パイプラインをスケジュールし、GitHub Pagesを使用してダッシュボードを構築します。

As of 2024, GitHub’s free tier gives you 2,000 free minutes of compute every month. 
2024年現在、GitHubの無料プランでは、毎月2,000分の無料コンピュート時間が提供されます。

That is more than enough to run our feature and batch inference pipelines. 
これは、私たちのフィーチャーおよびバッチ推論パイプラインを実行するには十分すぎるほどです。

You can run the training pipeline on a Jupyter notebook on your laptop—we won’t run it on a schedule for now. 
トレーニングパイプラインは、ノートパソコンのJupyterノートブックで実行できますが、今のところスケジュールで実行することはありません。

For our UI, we will use GitHub Pages (which hosts web pages for your GitHub repository); 
私たちのUIには、GitHub Pages（GitHubリポジトリのウェブページをホストする）を使用します。

in GitHub’s free tier, as of 2024, web pages cannot be larger than 1 GB and pages have a soft bandwidth limit of 100 GB per month. 
2024年現在、GitHubの無料プランでは、ウェブページは1GBを超えることができず、ページには月あたり100GBのソフトバンド幅制限があります。

This should be more than enough for this project. 
これは、このプロジェクトには十分すぎるほどです。

There are many different platforms that we can use to schedule our pipelines. 
私たちがパイプラインをスケジュールするために使用できるさまざまなプラットフォームがあります。

In my ID2223 course, students could choose between [Modal and GitHub Actions. 
私のID2223コースでは、学生は[ModalとGitHub Actionsの間で選択できました。

Modal’s free tier is generous and its](http://modal.com) developer experience is great, 
Modalの無料プランは寛大で、その開発者体験は素晴らしいですが、

but Modal requires a credit card for access and can’t schedule notebooks (only Python programs). 
Modalはアクセスにクレジットカードを必要とし、ノートブックをスケジュールすることはできません（Pythonプログラムのみ）。

There are many other serverless compute platforms that offer orchestration capabilities that you could use instead to run the Python programs, 
Pythonプログラムを実行するために使用できるオーケストレーション機能を提供する他のサーバーレスコンピュートプラットフォームも多数あります。

including Google Cloud Run, Azure Logic Apps, AWS Step Functions, [Fly.io, any managed Airflow platform, Dag‐](http://Fly.io) ster, and Mage AI. 
Google Cloud Run、Azure Logic Apps、AWS Step Functions、[Fly.io、任意の管理されたAirflowプラットフォーム、Dagster、Mage AIなどが含まれます。

So what is GitHub Actions? 
では、GitHub Actionsとは何ですか？

It is a continuous integration and continuous deployment (CI/CD) platform that allows you to automate your build, test, and deployment pipelines. 
それは、ビルド、テスト、およびデプロイメントパイプラインを自動化することを可能にする継続的インテグレーションおよび継続的デプロイメント（CI/CD）プラットフォームです。

GitHub Actions is typically used to schedule tests (unit tests or integration tests) and deploy artifacts. 
GitHub Actionsは通常、テスト（単体テストまたは統合テスト）をスケジュールし、アーティファクトをデプロイするために使用されます。

In our case, our feature and batch inference pipelines can be considered deployment pipelines that create features in the feature store and build our dashboard artifacts for GitHub Pages. 
私たちの場合、フィーチャーおよびバッチ推論パイプラインは、フィーチャーストアにフィーチャーを作成し、GitHub Pages用のダッシュボードアーティファクトを構築するデプロイメントパイプラインと見なすことができます。

For your GitHub Action to run successfully, you need to set the HOPSWORKS_API_KEY as a repository secret, 
GitHub Actionを正常に実行するには、HOPSWORKS_API_KEYをリポジトリのシークレットとして設定する必要があります。

so that your pipelines can authenticate with Hopsworks. 
これにより、パイプラインがHopsworksと認証できるようになります。

You can then proceed to define the YAML file containing the GitHub Actions, 
次に、GitHub Actionsを含むYAMLファイルを定義できます。

which is found in the GitHub repository at .github/workflows/air-quality-daily.yml. 
これは、GitHubリポジトリの.github/workflows/air-quality-daily.ymlにあります。

You can run the workflow in the GitHub Actions UI for your repository by clicking on “Run workflow.”  
リポジトリのGitHub Actions UIで「Run workflow」をクリックすることで、ワークフローを実行できます。

The workflow code shows the actions taken by the workflow. 
ワークフローコードは、ワークフローによって実行されるアクションを示しています。

First, you’ll notice that the scheduled execution of this action has been commented out. 
まず、このアクションのスケジュール実行がコメントアウトされていることに気付くでしょう。

When you have successfully run this GitHub Action without errors, 
このGitHub Actionをエラーなしで正常に実行したら、

you can uncomment the `schedule` and - cron lines near the beginning of the file 
ファイルの最初の方にある`schedule`と-cronの行のコメントを外すことができます。

and this GitHub Action will then run daily at 6:11 a.m. 
そうすると、このGitHub Actionは毎日午前6時11分に実行されます。

The steps the workflow will take are as follows. 
ワークフローが実行するステップは次のとおりです。

First, the workflow will run the steps on a container that uses the latest version of Ubuntu. 
まず、ワークフローは最新のUbuntuバージョンを使用するコンテナでステップを実行します。

Second, it will check out the code in this GitHub repository to a local directory in the container 
次に、コンテナ内のローカルディレクトリにこのGitHubリポジトリのコードをチェックアウトします。

and change the current working directory to the root directory of the repository. 
そして、現在の作業ディレクトリをリポジトリのルートディレクトリに変更します。

Third, it will install Python. 
次に、Pythonをインストールします。

Fourth, it will install all the Python dependencies in the requirements.txt file using pip (after upgrading pip to the latest version). 
第四に、requirements.txtファイル内のすべてのPython依存関係をpipを使用してインストールします（pipを最新バージョンにアップグレードした後）。

Finally, it will run the feature pipeline followed by the batch inference pipeline, 
最後に、フィーチャーパイプラインを実行し、その後にバッチ推論パイプラインを実行します。

after it sets the HOPSWORKS_API_KEY as an environment variable. 
その後、HOPSWORKS_API_KEYを環境変数として設定します。

Our GitHub Actions execute our feature pipeline and batch inference notebooks 
私たちのGitHub Actionsは、フィーチャーパイプラインとバッチ推論ノートブックを実行します。

with the help of the nbconvert utility that first transforms the notebook into a Python program 
これは、最初にノートブックをPythonプログラムに変換するnbconvertユーティリティの助けを借りて行われます。

and then runs the program from the first cell to the last cell. 
その後、プログラムは最初のセルから最後のセルまで実行されます。

The HOPSWORKS_API_KEY environment variable is set so that these pipelines can authenticate with Hopsworks: 
HOPSWORKS_API_KEY環境変数は、これらのパイプラインがHopsworksと認証できるように設定されています：

```   
on:    
workflow_dispatch:    
#schedule:    
# - cron: '11 6 * * *'   
jobs:    
test_schedule:     
runs-on: ubuntu-latest     
steps:      
- name: checkout repo content       
uses: actions/checkout@v4      
- name: setup python       
uses: actions/setup-python@v4       
with:        
python-version: '3.10.13'      
- name: install python packages       
run: |        
python -m pip install --upgrade pip        
pip install -r requirements.txt      
- name: execute pipelines       
env:        
HOPSWORKS_API_KEY: ${{ secrets.HOPSWORKS_API_KEY }}       
run: |        
cd notebooks/ch03   
jupyter nbconvert --to notebook --execute 2_air_quality_feature_pipeline.ipynb   
jupyter nbconvert --to notebook --execute 4_air_quality_batch_inference.ipynb
```

###### Building the Dashboard as a GitHub Page
###### GitHub Pageとしてダッシュボードを構築する

Our GitHub Action also includes steps to commit and push the PNG files created by the batch inference pipeline to our GitHub repository 
私たちのGitHub Actionには、バッチ推論パイプラインによって作成されたPNGファイルをGitHubリポジトリにコミットしてプッシュするステップも含まれています。

and then to build and publish a GitHub Page containing the Air Quality Forecasting Dashboard (with our PNG charts). 
その後、空気質予測ダッシュボード（PNGチャートを含む）を含むGitHub Pageを構築して公開します。

The GitHub Action YAML file contains a step called `git-auto-commit-` 
GitHub ActionのYAMLファイルには、`git-auto-commit-`というステップが含まれています。

``` action that pushes the new PNG files to our GitHub repository and rebuilds the Git‐ 
``` これは、新しいPNGファイルをGitHubリポジトリにプッシュし、GitHub Pagesを再構築します。

You shouldn’t need to change this code: 
このコードを変更する必要はありません：

```      
- name: publish GitHub Pages       
uses: stefanzweifel/git-auto-commit-action@v4       
[ … ]
``` 

Note that every time the action runs, in your GitHub history, it will be shown as a commit by you to the repository. 
アクションが実行されるたびに、GitHubの履歴には、リポジトリへのコミットとしてあなたが表示されることに注意してください。

For the `git-auto-commit-action step to run successfully, 
`git-auto-commit-action`ステップが正常に実行されるためには、

you first have to enable GitHub Pages in your repository. 
まず、リポジトリでGitHub Pagesを有効にする必要があります。

Go to Settings → Pages → Branch (main → /docs) and click on Save. 
設定 → ページ → ブランチ（main → /docs）に移動し、保存をクリックします。

This will create the GitHub Page for your repository. 
これにより、リポジトリのGitHub Pageが作成されます。

And that’s it. 
これで完了です。

Once you have the GitHub Page enabled and your GitHub Action runs your workflow every day, 
GitHub Pageが有効になり、GitHub Actionが毎日ワークフローを実行するようになると、

your dashboard will be updated daily with the latest air quality forecasts! 
ダッシュボードは最新の空気質予測で毎日更新されます！

###### Function Calling with LLMs
###### LLMを用いた関数呼び出し

You now should have a working air quality forecasting system powered by ML. 
これで、MLによって動かされる空気質予測システムが機能しているはずです。

But we want to make it even more accessible by adding a voice-activated UI. 
しかし、音声操作のUIを追加することで、さらにアクセスしやすくしたいと考えています。

For this, we are going to use two different open source transformer models 
これには、2つの異なるオープンソースのトランスフォーマーモデルを使用します。

(see Figure 3-4 and the notebook 5_function_calling.ipynb in the repository): 
（図3-4およびリポジトリ内のノートブック5_function_calling.ipynbを参照）：

1. Whisper transcribes audio into text—users speak and ask a question to our application, and the model outputs what the user said as text. 
1. Whisperは音声をテキストに書き起こします。ユーザーはアプリケーションに質問をし、モデルはユーザーが言ったことをテキストとして出力します。

2. The transcribed text will then be fed into a fine-tuned Llama 3 8B LLM that will return one function (from a set of four available functions), including the parameter values to that function. 
2. 書き起こされたテキストは、微調整されたLlama 3 8B LLMに入力され、4つの利用可能な関数のセットから1つの関数（その関数へのパラメータ値を含む）を返します。

3. The chosen function will be executed, returning either historical air quality measurements or a forecast for air quality, 
3. 選択された関数が実行され、過去の空気質測定値または空気質の予測のいずれかを返します。

and that output will be fed back into the LLM as part of the prompt along with your original voice-issued question to the same Llama 3 8B LLM. 
その出力は、元の音声で発行された質問とともに同じLlama 3 8B LLMへのプロンプトの一部としてLLMにフィードバックされます。

4. The LLM will return a human-understandable answer about the air quality (whether it’s safe or healthy) that is not just about the PM2.5 levels. 
4. LLMは、PM2.5レベルだけでなく、空気質についての人間が理解できる回答（安全か健康か）を返します。

_Figure 3-4. Our voice-activated UI uses Whisper to transcribe a user query that triggers_ 
_Figure 3-4. 私たちの音声操作UIは、Whisperを使用してユーザーのクエリを転写し、トリガーします_

_a function to be executed that will return either historical air quality measurements_ 
_実行される関数が、過去の空気質測定値を返すか、_

_from the feature group or forecasts from the model. Those results will be passed again to_ 
_フィーチャーグループまたはモデルからの予測を返します。これらの結果は再び_

_the LLM that answers the original question, but the prompt will also include the exter‐_ 
_元の質問に答えるLLMに渡されますが、プロンプトには外部の_

_nal context information provided by our air quality AI system. This is RAG without a_ 
_私たちの空気質AIシステムによって提供されるコンテキスト情報も含まれます。これは、ベクトルデータベースなしのRAGです。_

We are building our voice-activated UI using the paradigm of RAG using function calling with LLMs. 
私たちは、LLMを用いた関数呼び出しのパラダイムを使用して、音声操作UIを構築しています。

With LLMs, the user enters some text, called the prompt, and the LLM returns with a response. 
LLMを使用すると、ユーザーはプロンプトと呼ばれるテキストを入力し、LLMは応答を返します。

For chat-based LLMs, like OpenAI’s ChatGPT, the response is usually a conversational-style response. 
OpenAIのChatGPTのようなチャットベースのLLMでは、応答は通常、会話スタイルの応答です。

Function calling with LLMs involves the user entering a prompt, 
LLMを用いた関数呼び出しでは、ユーザーがプロンプトを入力しますが、

but now, the LLM will respond with a JSON object containing the function to execute 
今度は、LLMが実行する関数を含むJSONオブジェクトで応答します。

(from a set of available functions) along with the parameters to pass to that function. 
（利用可能な関数のセットから）およびその関数に渡すパラメータとともに。

We will use an LLM that is fine-tuned to return JSON objects describing the functions. 
私たちは、関数を説明するJSONオブジェクトを返すように微調整されたLLMを使用します。

We can then parse the JSON object and use it to execute one of our predefined functions: 
その後、JSONオブジェクトを解析し、私たちの事前定義された関数の1つを実行するために使用できます：

- get_future_data_for_date
- get_future_data_in_date_range
- get_historical_air_quality_for_date
- get_historical_data_in_date_range

That is, users will not be able to get answers to arbitrary questions about air quality— 
つまり、ユーザーは空気質に関する任意の質問に対する回答を得ることはできません—

only historical readings and air quality forecasts. 
過去の測定値と空気質の予測のみです。

You can ask questions like “What was the air quality like last month?” or “What will the air quality be like on Tuesday?” 
「先月の空気質はどうでしたか？」や「火曜日の空気質はどうなりますか？」のような質問をすることができます。

After you pass the list of function declarations in a query to the function-calling LLM, 
関数呼び出しLLMにクエリ内で関数宣言のリストを渡すと、

it tries to answer the user query with one of the provided functions. 
それは、提供された関数の1つでユーザーのクエリに答えようとします。

The LLM understands the purpose of a function by analyzing its function declaration. 
LLMは、関数宣言を分析することで関数の目的を理解します。

The model doesn’t actually call the function. 
モデルは実際には関数を呼び出しません。

Instead, you parse the response to call the function that the model returns. 
代わりに、モデルが返す関数を呼び出すために応答を解析します。

Here are the two forecast functions that we provide in the prompt. 
ここに、プロンプトで提供する2つの予測関数があります。

The other two historical functions are not shown here, as they have similar definitions. 
他の2つの履歴関数は、定義が似ているためここでは示されていません。

Notice that they are quite verbose, with human-understandable parameter names, 
それらは非常に冗長であり、人間が理解できるパラメータ名を持っていることに注意してください。

a description, and descriptions of all arguments and return values: 
説明とすべての引数および戻り値の説明があります：



def get_future_data_for_date \ 
(date: str, city_name: str, feature_view, model) -> pd.DataFrame: 
""" 
Predicts PM2.5 data for a date and city, given feature view and model.
Args: 
date (str): The target future date in the format 'YYYY-MM-DD'.
city_name (str): The name of the city for which the prediction is made.
feature_view: The feature view used to retrieve batch data.
model: The machine learning model used for prediction.
Returns: 
pd.DataFrame: predicted PM2.5 values for each day from target date.
""" 
def get_future_data_in_date_range(date_start: str, date_end: str, \ 
city_name: str, feature_view, model) -> pd.DataFrame: 
""" 
Retrieve data for a specific date range and city from a feature view.
Args: 
date_start (str): The start date in the format "%Y-%m-%d".
date_end (str): The end date in the format "%Y-%m-%d".
city_name (str): The name of the city to retrieve data for.
feature_view: The feature view object.
model: The machine learning model used for prediction.
Returns: 
pd.DataFrame: data for the specified date range and city.
"""
```
```md
def get_future_data_for_date \ 
(date: str, city_name: str, feature_view, model) -> pd.DataFrame: 
""" 
特定の日付と都市のPM2.5データを予測します。フィーチャービューとモデルを考慮します。
引数: 
date (str): 目標となる未来の日付（形式は 'YYYY-MM-DD'）。
city_name (str): 予測を行う都市の名前。
feature_view: バッチデータを取得するために使用されるフィーチャービュー。
model: 予測に使用される機械学習モデル。
戻り値: 
pd.DataFrame: 目標日からの各日の予測PM2.5値。
""" 
def get_future_data_in_date_range(date_start: str, date_end: str, \ 
city_name: str, feature_view, model) -> pd.DataFrame: 
""" 
特定の日付範囲と都市のデータをフィーチャービューから取得します。
引数: 
date_start (str): 開始日（形式は "%Y-%m-%d"）。
date_end (str): 終了日（形式は "%Y-%m-%d"）。
city_name (str): データを取得する都市の名前。
feature_view: フィーチャービューオブジェクト。
model: 予測に使用される機械学習モデル。
戻り値: 
pd.DataFrame: 指定された日付範囲と都市のデータ。
"""
```
```md
We designed the following prompt template for the function-calling query to our LLM as follows. 
First, we defined the available functions, and then we included the JSON representation of those functions, including their parameters, types, and descriptions. 
The fine-tuned LLM should also receive hints about which function to choose and be told not to return a function unless it is confident one of them matches the user query: 
```
```md
次のように、関数呼び出しクエリのためのプロンプトテンプレートを設計しました。 
まず、利用可能な関数を定義し、その後、関数のパラメータ、型、および説明を含むJSON表現を追加しました。 
微調整されたLLMは、どの関数を選択するかについてのヒントを受け取り、ユーザークエリに一致する関数があると確信しない限り、関数を返さないように指示されるべきです: 
```
```md
prompt = f"""<|im_start|>system 
You are a helpful assistant with access to the following functions: 
get_future_data_for_date 
get_future_data_in_date_range 
get_historical_air_quality_for_date 
get_historical_data_in_date_range 
{serialize_function_to_json(get_future_data_for_date)} 
{serialize_function_to_json(get_future_data_in_date_range)} 
{serialize_function_to_json(get_historical_air_quality_for_date)} 
{serialize_function_to_json(get_historical_data_in_date_range)}
```
```md
prompt = f"""<|im_start|>system 
あなたは、次の関数にアクセスできる有用なアシスタントです: 
get_future_data_for_date 
get_future_data_in_date_range 
get_historical_air_quality_for_date 
get_historical_data_in_date_range 
{serialize_function_to_json(get_future_data_for_date)} 
{serialize_function_to_json(get_future_data_in_date_range)} 
{serialize_function_to_json(get_historical_air_quality_for_date)} 
{serialize_function_to_json(get_historical_data_in_date_range)}
```
```md
You need to choose what function to use and retrieve parameters for this function from the user input. 
Today is {datetime.date.today().strftime("%A")}, {datetime.date.today()}.
IMPORTANT: If the user query contains 'will', it is very likely that you will need to use the get_future_data function. 
NOTE: Ignore the Feature View and Model parameters. 
NOTE: Dates should be provided in the format YYYY-MM-DD. 
To use these functions respond with: 
<multiplefunctions> 
<functioncall> {fn} </functioncall> 
<functioncall> {fn} </functioncall> 
...
</multiplefunctions> 
Edge cases you must handle: 
- If there are no functions that match the user request, you will respond politely that you cannot help.<|im_end|> 
```
```md
どの関数を使用するかを選択し、ユーザー入力からこの関数のパラメータを取得する必要があります。 
今日は {datetime.date.today().strftime("%A")}, {datetime.date.today()} です。
重要: ユーザークエリに 'will' が含まれている場合、get_future_data 関数を使用する必要がある可能性が非常に高いです。 
注意: フィーチャービューとモデルのパラメータは無視してください。 
注意: 日付は YYYY-MM-DD 形式で提供する必要があります。 
これらの関数を使用するには、次のように応答してください: 
<multiplefunctions> 
<functioncall> {fn} </functioncall> 
<functioncall> {fn} </functioncall> 
...
</multiplefunctions> 
処理しなければならないエッジケース: 
- ユーザーのリクエストに一致する関数がない場合は、丁寧に助けられないことを伝えます。<|im_end|> 
```
```md
The prompt for the second LLM query can be found in the source code repository. 
It is not shown here as it is straightforward—it includes the results of the function call, the original user query, some domain knowledge about air quality questions, and today’s date. 
```
```md
2回目のLLMクエリのためのプロンプトは、ソースコードリポジトリにあります。 
ここでは表示されていませんが、簡単なもので、関数呼び出しの結果、元のユーザークエリ、空気質に関するドメイン知識、そして今日の日付が含まれています。 
```
```md
The 5_function_calling.ipynb notebook needs a GPU to run efficiently. 
It also has its own set of Python requirements that you need to install: 
```
```md
5_function_calling.ipynb ノートブックは、効率的に実行するためにGPUが必要です。 
また、インストールする必要がある独自のPython要件があります: 
```
```md
pip install -r requirements-llm.txt
```
```md
``` 
pip install -r requirements-llm.txt
```
```md
If you do not have one on your laptop, you can use Google Colab with a T4 GPU at no cost (you will need a Google account, though). 
You need to uncomment and run the first two cells in the notebook to install the LLM Python requirements and download some Python modules. 
```
```md
ノートパソコンにGPUがない場合は、Googleアカウントが必要ですが、無料でT4 GPUを使用できるGoogle Colabを利用できます。 
ノートブックの最初の2つのセルのコメントを外して実行し、LLMのPython要件をインストールし、いくつかのPythonモジュールをダウンロードする必要があります。 
```
```md
The notebook quantizes the weights in the Llama 3 8B to 4 bits, reducing its size in memory so that the LLM will run on a T4 GPU (which has 16 GB of RAM). 
Weight quantization does not appear to negatively affect LLM performance for our system. 
```
```md
ノートブックは、Llama 3 8Bの重みを4ビットに量子化し、メモリ内のサイズを削減して、LLMがT4 GPU（16 GBのRAMを搭載）で実行できるようにします。 
重みの量子化は、私たちのシステムにおけるLLMのパフォーマンスに悪影響を与えないようです。 
```
```md
There is also a Streamlit program (streamlit_app.py) that wraps the same LLM program in a UI. 
Streamlit is a framework for building a UI as an imperative program [written in Python. 
You can host it in a free serverless service such as streamlit.io or](http://streamlit.io) _[huggingface.co.](http://huggingface.co)_  
```
```md
同じLLMプログラムをUIでラップするStreamlitプログラム（streamlit_app.py）もあります。 
Streamlitは、命令型プログラムとしてUIを構築するためのフレームワークです[Pythonで記述されています。 
それをstreamlit.ioや](http://streamlit.io) _[huggingface.co.](http://huggingface.co)_ のような無料のサーバーレスサービスでホストできます。 
```
```md
###### Summary and Exercises
In this chapter, we built our first AI system together—an air quality forecasting service. 
We decomposed the problem into five Python programs in total—a program to create and backfill feature groups, an operational feature pipeline that downloads air quality readings and weather forecasts, a model training pipeline that we run on demand, a batch-inference pipeline that outputs an air quality forecast chart and a hindcast as PNG files, and an LLM-powered program with a voice-driven UI for our service. 
We also defined a GitHub Action workflow as a YAML file to schedule the feature pipeline and batch inference pipeline to run daily. 
That was a good chunk of work, but now you have an AI system that you and your community can be proud of. 
```
```md
###### 要約と演習
この章では、私たちが共同で最初のAIシステム—空気質予測サービスを構築しました。 
問題を合計5つのPythonプログラムに分解しました—フィーチャーグループを作成しバックフィルするプログラム、空気質の読み取り値と天気予報をダウンロードする運用フィーチャーパイプライン、オンデマンドで実行するモデルトレーニングパイプライン、空気質予測チャートとPNGファイルとしてのヒンドキャストを出力するバッチ推論パイプライン、そして私たちのサービスのための音声駆動UIを持つLLM駆動プログラムです。 
また、フィーチャーパイプラインとバッチ推論パイプラインを毎日実行するようにスケジュールするためのYAMLファイルとしてGitHub Actionワークフローを定義しました。 
これは大きな作業でしたが、今ではあなたとあなたのコミュニティが誇りに思えるAIシステムを持っています。 
```
```md
The following exercises will help you learn how to iteratively improve your air quality prediction system:
- Add a lagged PM2.5 feature to your air quality prediction model. 
Start by adding yesterday’s PM2.5 value and then see if two days or three days help improve model accuracy.
- Determine what risks there are in adding historical PM2.5 values to predict future PM2.5 values.  
```
```md
次の演習は、空気質予測システムを反復的に改善する方法を学ぶのに役立ちます:
- 空気質予測モデルに遅延PM2.5フィーチャーを追加します。 
まず、昨日のPM2.5値を追加し、その後、2日または3日がモデルの精度を向上させるかどうかを確認します。
- 将来のPM2.5値を予測するために過去のPM2.5値を追加することにどのようなリスクがあるかを特定します。  
```
```md
###### PART II #### Feature Stores  
```
```md
###### PART II #### フィーチャーストア  



