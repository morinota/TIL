# The Feature Store Advanced Guide 2025年ver.を読んだメモ

## これは何??

- Feature Storeについて色々ググっていたら、 https://www.featurestore.org/ というサイトを見つけたので、そこに紹介されていたFeature Storeの2025年ver.のガイドを読んでみたメモです。
  - Hopsworksの人が書いたものなのかな? ガイドの内容は Hopsworks Feature Store のみでなく一般的なFeature Storeの話をしてるっぽいですが、若干ポジショントークが含まれる可能性も考慮して読んでみます。
  - refs: [Feature Store: The Definitive Guide](https://www.hopsworks.ai/dictionary/feature-store#training-data)


## そもそも特徴量とは? なんで専用の保存場所が欲しい??

- 特徴量(feature) = エンティティの数値的な属性で、学習/推論の入力として使うやつ!
  - ある対象(entity)の属性(property)を数値化したもので、かつMLに役立つもの。
- 専用の保存場所が必要なモチベーション:
  - その1: 「再利用」や「発見しやすさ」が重要だから(=開発効率up)
    - 特徴量を保存することの利点の一部は、**それらが簡単に発見され、異なるモデルで再利用しやすい状況を作れること**である。
    - それにより、**新しいMLシステムを構築するために必要なコストと時間を削減できることである**。
    - (この観点は、まさにFeature Storeの役割って感じだ...!!:thinking:)
  - その2: リアルタイム推論時に、今来たリクエストだけじゃなく、事前計算したリッチな情報が必要だから (=モデルの精度up)
    - オンラインモデルはlocal stateを持たない傾向があるらしい。
      - (これってどういう意味だろ。local stateを持たない傾向、って部分。perplexityに相談してみた感じ、各ユーザやリクエストの履歴・状態をモデル本体やサーバーのメモリ内に溜め込まず、**「今来たリクエスト」に含まれる情報だけをそのまま使う傾向がある**、みたいな意味合いっぽい...!:thinking:)

## Feature StoreとMLOps、MLシステムとの関連

- MLOpsプラットフォームにおけるFeature Storeは、**異なるMLパイプラインを結びつけて完全なMLシステムを作る接着剤の役割**を持つ (FTI Pipelines Architectureの発想そのものじゃん...!:thinking:)
  - Feature Pipeline: 特徴量を計算し、特徴量およびlabel/targetをFeature Storeに書き込む。
  - Training Pipeline: Feature Storeから特徴量およびlabel/targetを読み込み、MLモデルを学習する(学習されたモデルはmodel registryに書き込まれる)。
  - Inference Pipeline: Feature Storeから特徴量を取得し、MLモデルを使って推論する。
  - (メモ: **上記の内容って、思いっきりFTI Pipelines architectureの思想! Feature Storeを採用すること = FTI Pipelines Architectureを採用すること**、と言って良さそう...!:thinking:)
  - (まあFTI Pipelines Architecture自体がHopsworksの人が提唱してる設計思想なので、ここが整合するのは当然かも...!:thinking:)
  
- MLOpsの主な目標 = モデル試行錯誤のiteractionを短縮し、モデルのパフォーマンスを向上させ、ML資産（特徴、モデル）のガバナンスを確保し、コラボレーションを改善すること。
  - (ちなみに「MLOps処方箋本」のMLOpsの定義は「MLの成果をスケールさせるための取り組み」な訳だけど、上記を改善することがMLの成果のスケールに繋がるから、って解釈できそう...!:thinking:)
  - 特徴量ストアを採用すること(i.e. FTI Pipelines Architectureを採用すること)によって、この目標の達成につながるよ〜みたいな話かな:thinking:

## Feature Store が解決する課題

特徴量ストアが解決する課題として以下の11個が挙げられてた:

1. MLシステムのcollaborativeな開発を促進! (一元管理されてるので「発見」しやすいし、取得方法が統一されてるので「再利用」しやすいよね、って話か...!:thinking:)
2. 特徴量データのincrementalな管理 (本番MLシステムにおける特徴量は、一回作って終わりじゃなくて、incrementalに変化していくものなので...!:thinking:)

3. 特徴量のbackfillingと学習データのbackfilling (これは、特徴量ストアは特徴量をevent_timeと一緒に管理するから実現できるよね、って話かな...?:thinking:)

4. ステートレスなリアルタイム推論モデルにリッチな特徴量を供給 (これは前述してたlocal stateを持たない傾向、みたいな話!)

5. 特徴量の再利用がしやすくなる (これは一元管理してるから:thinking:)
6. 特徴量の様々な計算パターンへの対応 (これも一元管理してるから? オンライン/オフラインストアを持つからか:thinking:)
7. 特徴量データのvalidationやドリフト監視がしやすくなる! (これは、feature pipelineが独立するからかな...!:thinking:)
8. 学習時と推論時の特徴量の計算方法のズレ(data skew)を防げる!
9. point-in-time consistency (時点整合性) を持つ学習データを作りやすくなる! (これは特徴量ストアがevent_timeを元に特徴量を管理するから!:thinking:)

10. リアルタイム推論時に、事前計算した特徴量を低レイテンシー提供 (これはオンラインストアを含む特徴量ストアの話! 非対応のものもある印象...! :thinking:)

11. 埋め込みベクトルを使用したsimilarity search (これは特徴量ストアがベクトル検索をサポートしてる場合! similarity search機能はサポートしてない場合も全然ありそう! :thinking:)

シナリオ別の特徴量ストアの役立ちポイント例: 

- バッチMLシステムの本番稼働シナリオ(2, 3, 7, 8, 9)
- リアルタイムMLシステムの本番稼働シナリオ(上記に加えて、4, 6, 10, 11)
- 大規模なML展開シナリオ(上記に加えて、1, 5)

### 1個目について補足: Feature Storeがcollaborativeな開発をどう支えるか??

- 1点目: チームごと・開発者ごとの役割分担を可能にする。
  - Feature Storeがあることで(i.e. FTI Pipelines Architectureであることで)、**MLシステムの構築・運用をパイプライン単位に分解できるようになる**。
    - ex.)
      - Feature Pipeline: データエンジニア・データサイエンティスト
      - Training Pipeline: データサイエンティスト
      - Inference Pipeline: ソフトウェアエンジニア、MLOpsエンジニア
  - これによって、
    - 各種パイプラインでやるべきことが明確化される
    - Feature Storeをハブにして各パイプラインが独立して開発・運用できる
  - したがって、チーム間・チーム内でスムーズに役割分担・連携しやすくなる!
    - (メモ: **特徴量 x ルールベースによる推論だったら、Inference Pipelineを非MLチームのソフトウェアエンジニアが担当することも全然あり得るよね。**...! 欲しい特徴量の取得方法が統一された方法でわかりやすければ...!:thinking:)
- 2点目: 共通言語が生まれる
  - Feature Storeを中心に据えることで、チーム間で「Feature Pipeline」「Training Pipeline」「Inference Pipeline」っていう共通の言葉・設計思想を持てる！
  - ex.) **チームが構築しているのがバッチMLだろうとリアルタイムMLだろうと、開発者たちが「どうやって特徴量を管理してるか」を共通理解できるようになる! だから、チーム内・チーム間のコミュニケーションコストが下がる!**
    - (hogeパイプラインの入り口or出口は、まあFeature Storeだよね〜みたいな共通認識を持ちやすい、みたいな??::thinking:)
  - ML資産の共有とチーム内およびチーム間のコミュニケーションの改善が可能になる!

#### ちなみに...

Feature Storeの各種データの保存場所について:

- historicalな特徴量データ(i.e. event_timeを持つバージョニングされた特徴量データ??)は、オフラインストア(通常は列指向データストア)に保存される。
- リアルタイム推論で使用される最新バージョン(i.e. event_timeが最新)の特徴量データは、オンラインストア(通常は行指向データストア or key-valueストア)に保存される。
- 個人的気づき: **あ、オンラインストアに全ての特徴量を保存する必要はなくて、リアルタイム推論で使うもの、かつ最新のversionの特徴量レコードのみで良さそう...!! :thinking:**
  - 最初オンラインストアのコストめっちゃ高くなりそうだと思ってた。でもオフラインストアの全てをオンラインに同期する必要はなくて、**リアルタイム推論で使う特徴量、かつ最新のversionの特徴量レコードのみ**で良いんだよな...!:thinking:

ストレージ層におけるデータストアの選択について:

- 一部のFeature Storeサービスは、プラットフォームの一部としてストレージ層を提供し、一部は部分的または完全にpluggableなストレージ層を持つ。
  - 前者の例: Sagemaker Feature Store, Google Cloud Vertex AI Feature Store, Snowflake Feature Storeなどのベンダー提供のマネージドサービス。
    - 例えばSagemaker Feature Storeは、オフラインストアはS3上のParquet、オンラインストアはAWS Aurora(MySQL)で多分固定。
  - 後者の例: FeastやHopsworks Feature StoreなどOSS系。
    - Feastは、オフラインストアとしてBigQueryやSnowflakeやS3など、オンラインストアとしてRedisやDynamoDBなどをpluggableに取り替えできる感じ。

また、**予測ラベル(=もしくは報酬ログ的なもの。MLの出力側のデータ...!)もFeature Storeに保存するといいよ**的なことも書いてあった!(特徴量/モデルの監視とデバッグしやすさの観点で!)

### 2個目について補足: Feature Storeが特徴量のincrementalな管理をどう支えるか??

- feature pipelineは、MLシステムが稼働してる限り、特徴量を追加・更新し続ける (incremental dataset)
- Feature Storeがなければ、複数データストアへの整合性管理が大変になる。
  - **オフライン・オンライン・ベクトルDBが別々に存在してる場合、それぞれ認証・接続方法などが異なり、incremental datasetである特徴量について、それぞれのデータ同期を保つのは大変**。
- Feature Storeはこれらをwrapして、統一的なCRUD(create/read/update/delete)インターフェースを提供してくれるので、**可変な特徴量データセットの管理を容易にする役割**を果たす。
  - 同じfeature groupをストリーム処理クライアント(streaming feature pipeline)を使用して更新することもできる。(同じ特徴量グループを、バッチでもストリームでも更新できるよ、って話か。まあそりゃそうな気がする...!:thinking:)
    - 補足: Feature Storeでは、特徴量の論理グループを「feature group」や「Feature View」などと呼んでセットで管理することが多い。(ex. ユーザに関する特徴量は「user_feature_group」みたいな感じで)

### 3個目について補足: Feature Storeが特徴量のbackfilling(および学習データのbackfilling)をどう支えるか??

(この章を読んで思ったこと: **feature pipelineはbackfillできる必要がある。そのためには無状態 & 冪等性を持つパイプラインを意識すべき**...!! :thinking:)
(**単一の実装をバッチでもストリームでも実行できるようにしておく**のが運用上最強ってことでは..!:thinking:)

- backfillingは、生の履歴データからデータセット(=特徴量や学習データセット...!)を再計算するプロセス。
- これには、**ユーザがbackfillするデータの範囲のためにstart_timeとend_timeを提供する必要がある**。(feature pipelineを作るときは、無状態 & 冪等なデータパイプラインを意識すべき...!:thinking:)
  - 思ったことメモ:
    - 毎回全ユーザ分の特徴量を作る系のfeature pipelineだったら、backfillはあくまで学習用データセットを作るため、という用途になりそう...!:thinking:
    - 特定期間内に追加・更新されたアイテムだけの特徴量を作る系(=streamingっぽい)のfeature pipelineだったら、学習用だけじゃなくて推論用のデータを作る目的でもbackfillしそう。
    - まあすでに既存の特徴量パイプライン達が運用されてる状況だったらbackfillってのはあんまりする必要はなくて、**どちらにせよ、特徴量グループに新しい特徴量を追加したり既存特徴量の作り方を変更した場合などにbackfillすることになるはず**:thinking:
    - **backfill可能なデータパイプラインである為には、やはり無状態 & 冪等性を持つパイプラインを意識**する必要がありそう...!:thinking:

- また、ある特徴量のbackfillに使用されるfeature pipelineは、"live"データも処理できる必要がある
  - そのための方法はシンプルで、単にfeature pipelineを、データソースとデータの範囲を指定できるようにすればOK。(要するに、**わざわざ「backfill用の特別なパイプライン」を別で作るのはやめようね**、って話だと思ってる! backfill時は、対象データ期間を「過去データの範囲に切り替えて」動かすだけ! :thinking:)
- バッチとストリーミングのfeature pipelineの両方が、特徴量をbackfillできる必要がある。
  - (**ストリーミングパイプラインもbackfillできるようにしておこうね**、という話か...!ストリームのreplay設計っていうらしい...!:thinking:) 
  - (でも結局、大量の期間のデータをbackifillする際には、バッチというかバルクで一気に処理できる設計になってた方がいいよな...**単一のbackfill可能な実装をバッチでもストリームでも実行できるようにしておくのが運用上最強ってことでは**...!:thinking:)

- 特に学習データを作るという観点で、特徴量をbackfillできることは重要:
  - 逆に、もし特徴量をbackfillできないと、既存特徴量の定義を変更したり新しい特徴量を追加した場合に、本番システムリリース後に特徴量ログを集め始めて学習データが十分に集まるのを待つ必要が出てきてしまう。

### hogehoge
