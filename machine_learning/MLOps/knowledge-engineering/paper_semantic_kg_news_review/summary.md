# Semantic Knowledge Graphs for the News: A Review — セクション別サマリ

**論文**: Opdahl et al., ACM Computing Surveys, Vol. 55, No. 7, Article 140 (Dec 2022)
**原文**: [paper_ja.md](./paper_ja.md) / https://dl.acm.org/doi/epdf/10.1145/3543508
**性質**: 過去20年・80本の主要論文を対象とした SLR (Systematic Literature Review)

優先度の凡例 (タグPJ視点での示唆度):
- 必読: KR5/KR6/KR7・タグマスタ・コンテンツ理解層と直結する内容
- 推奨: 設計判断・技術選定・トレンド把握に有用
- 任意: 全体像把握用。スキップしても主要論点は失わない


## Abstract / 1. Introduction (L1–113) — 推奨

ニュース業界向けの ICT プラットフォームは異種データソース統合が必要で、Semantic KG は確立された統合手法。本論文は「ニュースの**制作・配信・消費**で Semantic KG をどう使ったか」を 20 年分レビューする。

**4 つのリサーチクエスチョン (RQ1–RQ4)**:
- RQ1: どの研究問題・アプローチが多く、中心的成果は何か
- RQ2: 注目されていない領域・希少な貢献は何か (= グリーンフィールド)
- RQ3: 研究はどう進化してきたか
- RQ4: 引用関係から見える中心論文・プロジェクトは何か

**読みどころ**: RQ の枠組みが本論文全体の地図になっているので、ここだけは目を通すと効率が良い。


## 2. Method (L115–214) — 任意

5つの検索エンジン (ACM, ScienceDirect, IEEE, Springer, WoS) + Google Scholar から 6,000 件 → 3 段階スクリーニング → **80 本の主要論文**に絞り込み。10個のトップレベルテーマ:

1. Technical result type
2. Empirical result type
3. Intended users
4. Task
5. Input data
6. News life cycle
7. Semantic techniques
8. Other techniques
9. News domain
10. Language and region

メタデータは SPARQL エンドポイントとして公開 (4,238 papers / 9,712 authors / 699 topics)。

**読みどころ**: 手法論なのでスキップ可。ただし、上記 10 テーマが Section 3 の節構成と一致しているので「目次」として把握しておくと良い。


## 3. Review of Main Papers — 本論

### 3.1. Technical Result Types 技術的結果の種類 (L222–425) — 推奨

主要論文が「何を作ったか」の分類。
- **Pipelines / Prototypes** (最多): KIM, NEWS, Hermes など、注釈付け・検索を行うリサーチプロトタイプ
- **Production systems**: AnnoTerra (NASA), VLX-Stories (商用、複数国/3言語で 9,000+ events/月)
- **System architectures**: World News Finder など (GATE/ANNIE/JAPE 構成が代表)
- **Algorithms**: IdentityRank (PageRank系 NED), Ponza et al. (LightGBM ベースの LTR)
- **Neural-network architectures**: HEER (新規エンティティ/関係検出), CAGE (セッション推薦), DTN (フェイクニュース検出, TransD埋め込み)
- **Ontologies**: 半数近くの論文が独自オントロジーを定義 (NEWS Ontology, EEOK など)
- **Knowledge graphs**: K-Pop (エンタメ), CrimeBase (犯罪), ClaimsKG (28K以上のファクトチェック済み主張, 6M トリプル)
- **Formal models**: 信念ベース改訂など少数

**重要トレンド**: 近年はアルゴリズム/アーキテクチャからディープNN への移行が顕著。説明可能性 (explainability) も最近言及されている。

### 3.2. Empirical Result Types 実証結果のタイプ (L426–566) — 任意

評価手法の分類。
- **Experiments**: 多数派。gold-standard データセット + IR 指標 (P/R/A/F1) が定番。KOPRA は MIND・Adressa で評価
- **Performance evaluation**: RDFLiveNews は並列で 1,500 RSS 同時処理可能と報告
- **Ablation, explainability, parameter studies**: DL系で定番化
- **Industrial testing**: VLX-Stories, VRT (ベルギー国営放送), Tamilin et al. (イタリア地方紙10年分), NEWS@EFE
- **Case studies / examples**: MediaLoep (VRT) など
- **Proof-of-concept / use cases**: 定性評価
- **User studies**: Yokoo et al. 日本語ニュース推薦 (関連性・好奇心・偶然性で評価)

**読みどころ**: 評価方法論。特定の論文を深掘りする時に振り返る程度で OK。

### 3.3. Intended Users 対象ユーザー (L567–682) — 任意

- 一般ニュースユーザー (最多)
- ジャーナリスト・ニュースルーム・通信社 (2 番目, NEWS Project, MediaLoep, EEOK, News Angler)
- 知識ベース管理者
- アーキビスト (Neptuno)
- フェイクニュース検出/ファクトチェッカー (近年急増, DTN, ClaimsKG)
- 知識労働者一般 (KIM, AGV)

### 3.4. Tasks タスク (L683–1037) — **必読**

タグPJと最も直結する。研究タスクの分類で、扱う粒度が KR5 (タグマスタ)/KR6 (コンテンツ理解層) と完全に重なる。

- **Semantic annotation**: KIM (KIMO への entity リンク + class 注釈), NEWS (Wikipedia/NASDAQ/CIA Factbook etc. へのリンク + DC/IPTC NewsCodes/NITF/NewsML/PRISM 利用)
- **Enrichment**: LOD で注釈済み記事を強化 (Antonini, AGV, Troncy)。CAGE/KOPRA/NewsLink のようにオープン KG のサブグラフで記事を表現する方式もここに分類
- **Content retrieval (pull)**: 検索系 (KIM, NEWS, Hermes, HGQL, World News Finder, NewsLink)
- **Content provision (push)**: 推薦系 (Joseph & Jiang, Cantador, Hopfgartner & Jose, CAGE, KOPRA)
- **Event detection**: NewsReader (Event-Centric KG), ASRAEL (Wikidata イベント階層, 粗化クラスタリング), Hermes/HNP, EEOK, Kuzey, VLX-Stories
- **Relation extraction**: SemNews (TMR→OWL), BKSport (KIMベース, 共参照解決), Prasojo (従属節までトリプル化), Färber (新規ステートメント検出)
- **Sub-graph extraction**: Joseph & Jiang (Freebase), AnchorKG (k-hop 近傍 + 強化学習), CAGE, KOPRA, NewsLink
- **KG updating**: HEER, PolarisX (多言語 BERT で関係抽出), TAMURE (テンソル分解), Sagi et al. (DBpedia/Google KG にない entity の調査: RSS の 13,456 entities 中 297 が両方にない)
- **Ontology development**: KIM, NEWS, EEOK
- **Fake-news detection / fact checking**: Brașoveanu, Pan, Müller-Budack (text+image multimodal), Groza & Pop (FRED + Racer/HermiT で医療神話検出), KLG-GAT (BERT + GAT)
- **Content generation**: Tweet2News, Pundit (因果関係抽出, 150年分の見出し), Jing (画像キャプション自動生成, Good News/Breaking News)
- **Prediction**: EKGStock (中国企業 KG, GRU で株価予測), DKN (CTR 予測)
- **その他**: 類似性 (Kasper), プロベナンス (De Nies, PROV-O), 可視化 (VRBO), アーカイブ (Neptuno), 相互運用性 (MediaLoep, García, Antonini, SPEED, NewsArticles, AnnoTerra)

**伸びている領域**: フェイクニュース識別、事実ジャーナリズム支援、自動ニュース検出。

### 3.5. Input Data 入力データ (L1038–1133) — 推奨

- **News articles** (最多): デジタルテキスト記事
- **RSS / news feeds**: OPWFP (CC/PP + FOAF + ドメインオントロジー)
- **Social media / Web**: Twitter, Wikinews, Wikipedia, HTML サイト
- **Multimedia news**: Jing (text+image), AGV (RAI ビデオアーカイブ)
- **News metadata**: García et al. (MPEG-7/MPEG-21), MediaLoep
- **Knowledge graphs**: 近年急増。Deep NN がオープン KG からトリプルを注入する用途が多い
- **User histories**: 推薦モデル訓練用

**トレンド**: マルチメディアは初期に流行 → DL 時代に再興。RSS は減少、Twitter 系が増加。KG はワールドナレッジ注入用途として急増中。

### 3.6. News Life Cycle ニュースライフサイクル (L1134–1187) — 推奨

ライフサイクル別に既存研究を整理:
- **Already published (最多)**: Neptuno, MediaLoep, AGV
- **Future news** (予測): Pundit, EEOK
- **Emerging news** (兆候検知): Tweet2News (Twitter 系)
- **Breaking news**: SPEED (経済イベント)
- **Developing news**: EEOK, RDFLiveNews

### 3.7. Semantic Techniques and Tools 意味的技術・ツール (L1188–1411) — **必読**

タグPJの技術選定の参考になる。
- **Exchange formats**: RDF (>50%), OWL (>1/3), SPARQL, RDFS
- **Vocabularies / ontologies**: Dublin Core, FOAF (最頻出), SKOS, SEM, OWL Time, SUMO/MILO/ESO, schema.org, PROV-DM/PROV-O, GRaSP, **rNews** (web ニュースマークアップ用), ITS, GAF, NIF (NLP コンポーネント間交換)。論文の 1/3 以上が独自ドメインオントロジーを提案
- **Information resources**: DBpedia (>1/4), Wikidata (近年急増), Google KG (急増中), Freebase (古いが現役), GeoNames, YAGO/YAGO2, Cyc, ConceptNet, **WordNet** (1/3, ネイティブセマンティックではないが圧倒的に最頻出)
- **Processing**: Entity linking 圧倒的最多 (DBpedia Spotlight, OpenCalais, **TagMe** がよく使われる)。論理推論 (DL/OWL-DL) は 7 論文。Jena (Java) が最頻出 API、RDFlib (Python) は近年限定
- **Storage**: RDF4J (Sesame), OpenLink Virtuoso が双璧。AllegroGraph も。NewsReader の **KnowledgeStore** (HDFS + HBase + Virtuoso) はビッグデータ対応で注目

**最近のトレンド**: Wikidata が DBpedia より人気上昇。

### 3.8. Other Techniques and Tools その他の技術 (L1412–1485) — 推奨

- **News standards**: IPTC ファミリー (Media Topics, NewsCodes, rNews)
- **NLP**: GATE, Lucene, **spaCy**, JAPE, StanfordNER。Entity extraction, NL pre-processing, 共参照解決, 形態素解析, semantic role labelling
- **ML**: TransE, TransR, TransD, word2vec などの embedding が定番
- **DL** (2019〜急増): CNN, GRU, **GCN**, LSTM, **BERT**, attention。PolarisX (多言語 BERT), TAMURE (TensorFlow), DKN (CNN+attention), Pan (B-TransE, フェイクニュース)

**進化の流れ**: ~2014 がニュース標準と LOD 統合 → 2015~ 機械学習 (NLP, embedding) → 2019~ 深層学習 (CNN, LSTM, attention)。

### 3.9. News Domain ニュースドメイン (L1486–1541) — 任意

- 経済/金融が最多 (Lupiani-Ruiz, SPEED)
- 政治, スポーツ (BKSport), 科学, ビジネス, 健康, 株式市場
- エンタメ (K-Pop), 環境 (WebLyzard), 教育/科学技術 (AGV), 医学, 犯罪 (CrimeBase), 地球科学 (AnnoTerra)

**示唆**: ドメイン特異性は低く、技術は他ドメインに転用可能。金融が多いのは経済価値 + リアルタイムデータの両立による。

### 3.10. Language 言語 (L1542–1569) — 任意

- 英語が圧倒 (ただしレビューの inclusion criterion が英語のため)
- イタリア語、スペイン語が次いで多い (各 <10 論文)
- フランス語/ドイツ語は英語と組み合わせのみ
- NewsReader: 英・蘭・伊・西。PolarisX: 中・日・韓
- 多言語/言語非依存ソリューションへの関心が増加中

### 3.11. Important Papers 重要論文 (L1571–1602) — 推奨

文献カウントしたいときに参考。同年補正後の引用上位 5:
1. **DKN** (2018, ニュース推薦)
2. **KIM** (2004, セマンティック注釈)
3. **Pundit** (2012, 因果学習)
4. **NewsReader** (2016, ECKG構築)
5. **Pan et al.** (2018, KGによるフェイクニュース検出)

参照頻度の高い古典: Semantic Web 提案論文, WordNet, TransE, GATE, word2vec, DBpedia, Freebase, TransR, GloVe, YAGO。

**注目点**: KIM 以外は他の主要論文同士の相互引用が少なく、まだこの分野は「成熟した研究領域」になっていない。

### 3.12. Frequent Authors and Projects 頻出著者・プロジェクト (L1603–1628) — 任意

- F. Frasincar (7), F. Hogenboom (5), Deursen/Mannens/Walle (3), García/Sánchez (3)
- 主要プロジェクト: NEWS, Hermes, NewsReader, MediaLoep, Neptuno
- 主要論文同士の相互引用は計 43 件のみ → 分野の未成熟を示唆

### 3.13. Evolution over Time 時代区分 (L1629–1701) — **必読**

研究全体を 4 つの時代に整理:
- **〜2009 Semantic Web 時代**: RDF/RDFS/OWL/SPARQL, 基本 NLP, ドメインオントロジー, IPTC Media Topics 統合, アーカイブ/ブラウジング
- **2010–2014 LOD 時代**: コンテキスト化・エンリッチメント中心。WordNet 最頻出。GATE, OpenCalais, Jena
- **2015–2018 KG 時代**: Google が "Knowledge Graphs" 命名 (2012)。RDF/OWL から独立した KG 概念。embedding 登場。DBpedia と entity linking の本格採用。共参照解決, 依存構文解析, StanfordNER
- **2019〜 DL 時代**: deep NN による text+graph embedding。オープン KG からのトリプル注入。タスクはファクトチェック・フェイクニュース・CTR 予測へ。CNN/LSTM/attention/spaCy/BERT。マルチメディアも復活


## 4. Discussion 議論

### 4.1. Conceptual Framework 概念フレームワーク (L1712–1725) — 任意

10 テーマの分析フレームワーク自体の振り返り。地理的地域は当初テーマだったが、地域特化の論文が少なく削除した。

### 4.2. Implications for Practice 実践への示唆 (L1726–1847) — **必読**

ニュースルーム/事業会社が KG 導入を検討する際の指針。タグPJの企画資料・技術選定の論拠として活用できる:

- **Technical result types**: 商用ツール (VLX-Stories, ViewerPro) も登場し始めたが、多くはまだプロトタイプ。**高便益タスク × 低リスク技術** のパイロットが鍵
- **Empirical**: 産業導入時は技術ロバスト性も業務適合性も未知数。継続評価が前提 → 業界×研究の協働余地
- **Intended users**: 検索/アーカイブ/推薦は成熟。一般ユーザー向けは推薦中心
- **Tasks**: 注釈・検索・推薦は成熟。エンリッチメントは情報過多のリスクあり。**自動ニュース検出と背景情報自動付与**がパイロット候補
- **Input data**: テキスト中心。マルチメディアは音声→テキスト経由が多い。Twitter 衰退に対しオウンドプラットフォームでの社会的インタラクションホスティングが機会
- **News life cycle**: 既公開ニュース活用は低リスク開始点。新興/速報イベント検出は高リスク高リターン
- **Semantic techniques**: クラウド (AWS Neptune 等) で初期投資少なく試せる
- **Other techniques**: KG は **多様な情報源を RDF/SPARQL/OWL で統合するハブ**として位置付ける戦略が有効。ML/DL イニシアチブの一部として導入できる
- **News domain**: ビジネス/金融が最も成熟。ロボットジャーナリズムを KG で拡張するのが速攻策
- **Language**: 非英語ニュースルームは国際ニュースを起点に、英語圏は KG-powered の cross-lingual サービスで小言語リソース活用

### 4.3. Implications for Research 研究への示唆 (L1848–1972) — **必読 (研究側)**

未開拓領域・今後の研究方向:
- **Technical**: 産業グレードのプロトタイプ・プラットフォーム不足。技術ドリブン → ステークホルダーニーズ調査も必要
- **Empirical**: ケーススタディ・アクションリサーチ・インタビュー・調査・民族誌的研究が必要。**augmented/computational/digital journalism との接続が薄い**。gold-standard データセットの収束がなく比較困難
- **Intended users**: 市民ジャーナリズム・地域ジャーナリズム・ニュースルームの社会組織的側面・ロボットジャーナリズムへの言及が皆無
- **Tasks**: 名前付き entity/概念/トピック注釈の先 = イベント検出, 関係抽出, KG 更新, **ダークエンティティ/関係**の同定。データ品質 (privacy, provenance, ownership, terms of use) は研究薄い。マルチメディアをテキスト経由でなくネイティブに扱う研究が少ない
- **Input data**: ソーシャルメディア短文の文脈不足を、音声/画像/動画統合で補う方向。**IoT/センサーデータの活用は希少**。GDELT は未活用リソース (品質と低レベルイベントの集約が課題)
- **News life cycle**: 新興・速報・進行中ニュースの検出/追跡研究が少ない
- **Semantic techniques**: 既存コーパス使用が多く、**ジャーナリスティック KG を時間をかけてキュレートする研究が薄い**。ニュースは Volume/Velocity/Variety が高く、リアルタイム+ビッグデータ KG の test bed になる。NewsReader (KnowledgeStore) と News Angler (News Hunter) が big-data ready の代表
- **Other techniques**: 画像理解・音声認識の最近の進歩は KG 研究にあまり取り込まれていない。Pregel/Giraph などのビッググラフ DB 活用も少ない
- **News domain**: 腐敗/政治的縁故主義、誤情報、危機/社会不安 (GDELT) が未開拓
- **Language**: 多言語 BERT などの活用が少なく、小言語向けの言語モデル活用研究も希少

### 4.4. Research Questions の回答 (L1973–2035) — 推奨

- **RQ1**: 多様で常に変化中。新ツール/技術開発タイプ + プロトタイプ + 実験評価が定型。フェイクニュース検出・ファクトチェックが急増中
- **RQ2**: 産業ケーススタディ少, レビュー少, privacy/ownership/terms of use/provenance 研究少, リアルタイム/ビッグデータ評価少。location/IoT/市民ジャーナリズム/Reuters Tracer 的新規イベント検出/物語生成は green field
- **RQ3**: 4 時代区分 (3.13 と同じ): Semantic Web → LOD → KG+ML → DL+KG
- **RQ4**: 引用最多 = DKN, KIM。中心プロジェクト = Hermes, NewsReader, NEWS, MediaLoep, Neptuno

### 4.5. Limitations 制限 (L2036–2053) — 任意

- スコープを「ニュース目的 × Semantic KG/関連技術」に限定
- 他の知識表現技術や他ドメイン論文は除外
- セマンティックリンクされていない (LOD クラウドに繋がらない) KG 研究も対象外
- 一般テキストを KG として表現する研究は除外


## 5. Conclusion 結論 (L2056–2065) — 任意

6,000+ → 80 主要論文の SLR を実施。RQ に対する答えと 4.3 の研究の方向性を提示。実務者・研究者・computational journalism や Semantic KG に関心ある人向け。


---

## どこを読むべきか — タグPJ視点での提案

### 第一優先 (= まず読む)

1. **3.4 Tasks** (L683–1037): タグPJの「タグ付け・関連記事推薦・イベント検出」と直結。各タスクの代表論文も把握できる。
2. **3.7 Semantic Techniques** (L1188–1411): RDF/OWL/SKOS/SEM/Wikidata/DBpedia など、技術選定の参考。タグマスタ設計の論点と直結。
3. **3.13 Evolution over Time** (L1629–1701): 4 時代区分は短く全体像が掴める。歴史的文脈の即席チートシート。
4. **4.2 Implications for Practice** (L1726–1847): ニュースルーム導入観点。タグPJの企画書・社内説明資料の論拠として使える。

### 第二優先 (= 余裕があれば)

- **3.1 Technical Result Types** (L222–425): どんな成果物 (Pipeline/Algorithm/NN/Ontology/KG) が世にあるかの総覧
- **3.5 Input Data** (L1038–1133): KG をニュース分析へ注入する用途の急増を確認
- **3.6 News Life Cycle** (L1134–1187): 既公開 vs. 速報 vs. 発展中の枠組み
- **3.8 Other Techniques** (L1412–1485): NLP/ML/DL ツールチェーンの定番
- **3.11 Important Papers** (L1571–1602): KIM, DKN, Pundit, NewsReader, Pan を起点に深掘りする時に
- **4.3 Implications for Research** (L1848–1972): 研究的な空白地帯。タグPJの「我々が新規にやる価値ある領域」を見極める材料
- **4.4 Research Questions の回答** (L1973–2035): 4.2/4.3 の要約版

### スキップ可

- **2 Method** (L115–214): SLR の手続き
- **3.2 Empirical Result Types** (L426–566): 評価手法の分類
- **3.3 Intended Users** (L567–682): ユーザー像
- **3.9 News Domain** / **3.10 Language** / **3.12 Frequent Authors** / **4.1 Conceptual Framework** / **4.5 Limitations** / **5 Conclusion**: 補足的内容
