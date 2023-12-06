<!-- (番外編)FTI Pipelines Architectureってなんだ? MLOps勉強会で推薦システム関連の発表を聞いて知らない用語を調べた!: -->

# From MLOps to ML Systems with Feature/Training/Inference Pipelines

published date: 13 September 2023,
authors: Jim Dowling
url(paper): https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines
(勉強会発表者: morinota)

---

(論文じゃないですが、いつもと同じフォーマットっぽく書いてみます。)

## どんなもの?

- 2023/10のMLOps勉強会の[発表](https://speakerdeck.com/masatakashiwagi/di-35hui-mlops-mian-qiang-hui-komiyuniteipuratutohuomunobatutirekomendowozhi-eruji-jie-xue-xi-ji-pan)にて FTI Pipelinesが引用されており気になったので、MLOps周りのcatch upとして読んでみました...! そのパート2です! [前回はMLOps Maturity Assessment](https://qiita.com/morinota/items/726103584287d8ec1795)
- MLシステムのアーキテクチャとして、Feature(特徴量作成) pipelines, Training(学習) pipelines, Inference(推論) pipelinesの、**3種の独立したpipelinesを用いるFTI pipelines architectureが良いよ**！って話。
- FTI pipelines architecture を単なるアーキテクチャパターンとしてのみでなく、MLシステムをプロダクト化する為に指針とすべきメンタルマップとしてもおすすめしてた。

## 先行研究と比べて何がすごい？

### まず2種類のMLシステムがあるよねという話(batch MLシステムと online MLシステム)

- batch MLシステムの例: 「Spotify weekly」
  - 週に一度、各ユーザにどんな曲を推薦するかの予測結果を作成する。
  - 予測結果はkey-valueストアに保存され、Spotifyにログインした際に結果をclient側が取得しユーザに表示される。
- online MLシステムの例: 「TikTok」
  - ユーザがclickやswipeをするたびに、ユーザ履歴とcontext(ex. 最近のトレンド)について、ほぼリアルタイムで特徴量を計算する。

### MLシステムの既存のアーキテクチャの話

MLシステムの第一世代では、batch及びonlineのMLシステムの為の多くの異なるアーキテクチャパターンが提案された。

![fig4](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502ad7d387cfe977467717b_figure%204_lightbox.png)

図4はbatch MLシステムのアーキテクチャ:

- 特徴:
  - 特徴量作成と学習と推論を同じプログラムに含めている、monolithicなシステム。
  - TRAINモード/INFERENCEモードのどちらで実行するかを決めるboolean flagを指定してプログラムを実行する。
- 長所:
  - 学習と推論で、一貫した特徴量を使用している事を保証できる
- 短所:
  - ここで作った特徴量を他のモデルで再利用しづらい。
  - モジュラー性が低い。
    - ex. 特徴量作成処理の入力データ量が増えて、Pythonプログラムで処理しづらくなった場合に、簡単にPySparkに切り替えられない。

![fig5](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502adc6d9992658b4fa84b7_figure%205_lightbox.png)

図5はonline MLシステムのアーキテクチャ:

- 特徴:
  - オフラインでの特徴量作成・学習と、オンラインでの推論のpipelineを分割している。
  - 推論pipeline側において、リクエストにて提供されるデータから特徴量が計算される。(ex. LLMチャットボット)
- 長所:
  - client側からのAPIリクエストを受け、リアルタイムで予測結果を返せる。
- 短所:
  - 図4のbatch MLシステムとは全く異なるアーキテクチャ -> batch MLシステムからonline MLシステムへの移行が難しい。
  - 学習と推論で、一貫した特徴量を保証することができない。
    - (これも原因は、特徴量作成と学習を一緒のpipelineに含めてしまってるからかな...!:thiniking:)

![fig6](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502adf3ca2eceb7be5b949e_figure%206_lightbox.png)

対して本稿では、**3つの独立したML Pipelines = = Feature pipelines, Training pipelines, Inference pipelines = FTI Pipelines**を持つアーキテクチャを提示する。
図6も図5と同様に、online MLシステムのアーキテクチャ。(これがFTI Pipelinesアーキテクチャ)

- 特徴:
  - 特徴量作成・学習・online推論が、3つの独立したpipelinesになっている。
  - 多くのonline MLシステムでは**ユーザ履歴やcontextも使用するが、feature storeはそれらを事前に計算された特徴量の1つとして保存**し、学習pipeline, 推論pipelineに提供する。
- 長所:
  - 推論時に特徴量を作成する必要がない -> 低レイテンシー。
  - 学習と推論で、一貫した特徴量を保証できる。
  - モジュラー性が高い。
- 短所:
  - ?

### メンタルマップの話

- 2020年頃、MLシステムをプロダクト化する為に使用すべき一連のパターンとプロセスとして、MLOpsという用語が出てきた。
  - MLOpsはDevOpsに触発されたもの。
  - しかしMLシステムは、**システムのコードだけでなく、学習・推論に使われるデータも管理しなければならない**という点で、非MLのソフトウェアプロダクトよりも複雑...
  - -> MLOpsコミュニティは、開発組織のベストプラクティス&プロセスに関する**指針を強く必要としていた**...!
- 従来のMLOpsマップの欠陥:
  - GoogleやDatabricksは、MLシステムを開発する為のMLOpsマップを公開した。
  - しかしこれらのMLOpsマップには、メルカトル図法みたいな欠陥がある。->MLシステム開発の現実を反映していないようなMLシステムの見方を投影している。
  - 参入障壁が高すぎる。従来のMLOpsマップを指針として使いこなせるのは、ごく少数のソフトウェアエンジニアリング・オペレーション・データサイエンスの知識に精通した人間だけ。
- 一方で本稿では、**FTI PipelinesをMLシステムのもっと簡単なメンタルマップ(=「何をすべきか」という明確な指針?:thinking:)として提示する**。
  - 各pipelineが生成・消費する成果物(ex. 特徴量、学習済みモデル)は、共通の永続化ストレージレイヤーを介して共有される。
  - 既存のMLOpsアーキテクチャと比較して、FTI pipelinesアーキテクチャは、自動テスト、versioning, モニタリングのベストプラクティスに従いながら、iterativeに改善できる最小限の実用的なMLシステムに高速に到達するのに役立つ。

## 技術や手法の肝は？

![](https://assets-global.website-files.com/618399cd49d125734c8dec95/6501bf916e9d382ecda67424_figure%201_lightbox.png)

FTI Pipelinesアーキテクチャは、**独立に開発・運用される以下の3つのpipelines**から構成される:

- Feature(特徴量) pipeline:
  - rawデータを入力として受け取り継続的に特徴量(や教師ラベル)を作成する。成果物をDataFrameとしてFeature Storeに保存する。
  - batch処理でもonline (streaming)処理でも良い。
- Training(学習) pipeline:
  - Feature Storeから学習データ(=特徴量や教師ラベル)を読み込み、モデルを学習する。成果物として学習済みモデルをモデルレジストリに保存する。
- Inference(推論) pipeline:
  - batch推論またはonline推論の為のpipeline。
  - モデルレジストリから学習済みモデルを読み込み、最新の特徴量データをfeature storeから取得し(もしくはAPIのリクエストから取得)、プロダクト上で消費される予測結果をストレージレイヤーに保存する。(online推論の場合はレスポンスとして返す)

利点:

- 各pipelineの責任(i.e. 役割?責務?関心?)が明確である点
  - いろんな責任を持つ単一のML pipelineが存在しない。
  - -> pipelineが何をするのかについての混乱がなくなる。
  - (ex. 特徴量エンジニアリングと学習なのか。推論もするのか。もしくは学習と推論のどちらか一方だけなのか。)
- オープンアーキテクチャである点:
  - 特にFeature pipelineにおいて、状況(i.e. データサイズ、特徴量の鮮度要件)に応じてPythonやSQLやSpark等を使い分ける事ができる。
  - (Training pipelineはモデルの学習が通常Pythonで行われるので、ほぼPythonが採用される。)
- モジュラー性が高い点:
  - 各pipelineは独立して操作可能。
  - monolithicなML pipelineと比較して、異なるチームが異なるpipelineの開発・運用を担当できる。(開発チーム間のカップリングの度合いを低くしやすい:thinking:)

### Feature Pipelineについて検討すべきこと

- Pipelineはbatch処理か、streaming処理か?
- 特徴量のfeature storeへのingestionは、incrementalか(i.e. 差分更新みたいな?:thinking:)、full-loadか(i.e. 全更新、洗い替えみたいな?:thinking:)?
- Pipelineの実装には、どのようなフレームワーク/言語を採用するか?
- feature storeへのingestionの前に、特徴量データに対してdata validationが行われているか?
  - (これは特徴量の分布が変化していないか、とかの話??:thinking:)
- pipelineのスケジューリングには、どのorchestratorツールを用いる?
  - digdagとか:thinking:
- 上流のシステム(ex. data warehouse)で既に計算済みの特徴量がある場合、どのようにデータの重複を防ぎ、学習データや推論用データを作成する際にそれらの特徴量のみをreadできるようにする??
  - (そのままfeature storeに同期させちゃだめなのかな。その重複がまさによろしくないって話なのかな:thinking:)

### Training Pipelineについて検討すべきこと

- Pipelineの実装には、どのようなフレームワーク/言語を採用するか?
- どのような実験追跡プラットフォームを使用するか?
- Training Pipelineは定期実行される?(その場合どの様なorchestratorツールを使用する?) もしくはon-demandで実行される??(その場合、どのような状況で実行すべき??)
- 学習にGPUは必要? 必要な場合、Pipelineにどのように割り当てる??
- どの特徴量に対して、どのようにencoding/scalingが行われる?
  - 通常、特徴量データはencodeされていない状態でfeature storeに保存される。
  - encoding/scalingは、学習と推論のpipelinesにおいて、一貫した方法で実行される必要がある。
- モデルの評価(evaluation)・検証(validation)はどのように行う?
- 学習済みモデルの保存には、どのようなモデルレジストリを使用する?
  - 例えばS3? :thinking:

### Inference Pipelineについて検討すべきこと

- 予測結果を消費する対象は何?(ダッシュボード?, onlineアプリケーション??)そして、それらはどのように予測結果を消費する??
- Pipelineはbatch処理か、online処理か?
- どの特徴量に対して、どのようにencoding/scalingが行われる?(学習と同様)
- batch推論Pipelineの場合、どのようなフレームワーク/言語を採用するか? それをスケジュールで実行する為に、どのorchestatorが採用される? 作られた予測結果を消費するために、どのようなsinkが使われる??
- online推論Pipelineの場合、デプロイされたモデルをホストする為にどのようなmodel serving serverを使用する? どのようなフレームワーク/言語で実装される? 推論にGPUは必要? 推論用のAPIに関するSLA(service-level agreements)はある??

## 次に読むべき論文は？

- 同じく2023/10のMLOps勉強会の発表にて引用されていた、[RecSysOps](https://netflixtechblog.medium.com/recsysops-best-practices-for-operating-a-large-scale-recommender-system-95bbe195a841)のブログとか?
