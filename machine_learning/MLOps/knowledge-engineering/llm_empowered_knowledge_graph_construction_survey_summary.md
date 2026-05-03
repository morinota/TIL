# LLM-Empowered Knowledge Graph Construction: A Survey — セクション別サマリ

**論文**: Haonan Bian (Xidian University), 2025
**原文**: [llm_empowered_knowledge_graph_construction_survey.md](./llm_empowered_knowledge_graph_construction_survey.md) / https://arxiv.org/pdf/2510.20345
**性質**: LLM × KG 構築 の **包括的サーベイ論文** (arXiv preprint)。3 層パイプライン (オントロジー / 抽出 / 融合) を LLM がどう再構築しているかを整理

優先度の凡例 (タグPJ視点):
- 必読: タグマスタ・コンテンツ理解層・記事マッチングの設計判断に直結
- 推奨: 全体像と進化軸の把握に有用
- 任意: 背景理解用、スキップしても主要論点は失わない

---

## Abstract / 1. INTRODUCTION (L10–101) — **必読**

### 主張: KG 構築は新しいパラダイムへ移行中

ルールベース・統計的パイプライン → 言語駆動・生成型フレームワーク へ。著者は 3 層パイプライン (オントロジー工学 / 知識抽出 / 知識融合) を LLM がどう再構築するかを分析。

### 従来パラダイムの 3 つの永続的課題:
1. **スケーラビリティとデータ希薄性**: ルール / 教師あり手法はドメイン横断の汎化が苦手
2. **専門家依存と硬直性**: スキーマ・オントロジー設計は多大な人的介入が必要
3. **パイプライン断片化**: 段階間で累積的にエラーが伝播

### LLM が解く 3 つのメカニズム:
1. **生成的知識モデリング**: 非構造テキストから直接構造化表現を合成
2. **意味的統合**: 自然言語の基盤を通じて異種知識源を統合
3. **指示駆動オーケストレーション**: プロンプトベースで複雑な KG 構築ワークフローを調整

### 結果: LLM はテキスト処理ツールから **「自然言語と構造化知識をつなぐ認知エンジン」** へ進化。これは **rule-driven, pipeline-based → LLM-driven, unified, adaptive** のパラダイムシフト。

**読みどころ**: 3 つの課題 + 3 つのメカニズム を押さえれば、論文全体の地図が掴める。

---

## 2. PRELIMINARIES (L102–177) — 推奨

LLM 以前の従来手法を 3 段階に整理:

### 2.1 Ontology Engineering (OE) — オントロジー工学

- 主にドメイン専門家が手動で構築 (Protégé, METHONTOLOGY, On-To-Knowledge)
- **強い人的監視 + 限られたスケーラビリティ**
- 半自動 (ontology learning) も登場したが、進化・モジュール再利用・動的適応に苦労

### 2.2 Knowledge Extraction (KE) — 知識抽出

- ルールマッチング → 統計的手法 → BiLSTM-CRF / Transformer
- 教師あり / 弱教師あり / 教師なし関係抽出のパラダイム
- **データ希薄性、弱い汎化、累積エラー伝播** が制約

### 2.3 Knowledge Fusion (KF) — 知識融合

- 中心タスク: **エンティティ整合 (entity alignment)** = 異データセット間で同一の現実世界オブジェクトを判定
- 古典: 語彙的・構造的類似度 → 表現学習による埋め込みベース整合
- **意味的異質性、大規模統合、動的更新** に苦戦

---

## 3. LLM-ENHANCED ONTOLOGY CONSTRUCTION (L178–313) — **必読**

LLM 統合により、OE は 2 つの相補的方向に分岐:

### 3.1 Top-Down: LLMs as Ontology Assistants

セマンティックウェブの伝統を拡張、**事前定義された意味的要件**に基づいて LLM がオントロジー設計を支援。

#### 3.1.1 Competency Question (CQ) ベース
- **Ontogenia** (2025): メタ認知プロンプティングで自己反省・構造的修正
- **CQbyCQ** (2024): CQ / ユーザーストーリー → OWL スキーマへ直接変換
- 結果: クラス・プロパティ・論理公理を自律生成、ジュニア人間モデラーと同等の品質

#### 3.1.2 自然言語ベース
- **LLMs4OL** (2023): GPT-4 が概念識別・関係抽出・パターン誘導
- **NeOn-GPT / LLMs4Life** (2024-25): エンドツーエンド、プロンプト駆動、ライフサイエンス等の複雑ドメイン向け
- **LKD-KGC** (2025): 文書要約から抽出した entity type をクラスタリングしてオープンドメイン KG のスキーマ誘導

→ LLM は **受動的ツールから能動的モデリング協力者** へ移行。

### 3.2 Bottom-Up: KGs for LLMs

**RAG フレームワーク**で重要視されるパラダイム。KG は静的リポジトリではなく、LLM の **動的インフラ・構造化メモリ** として機能。

3 段階の進化:
1. **GraphRAG / OntoRAG** (2024-25): instance-level graph 生成 → クラスタリングで概念抽象化 (data-to-schema)
2. **EDC** (2024): Extract → Define → Canonicalize の 3 段階。誘導されたスキーマを既存と整合 or 新規作成
3. **AdaKGC** (2023): スキーマドリフトに対応、再訓練なしで新しい関係 / entity を取り込む

最近の事例:
- **AutoSchemaKG** (2025): スキーマベース + スキーマフリーを統一アーキテクチャで統合、エンタープライズ規模のリアルタイム生成

→ 焦点が「LLMs for OE」 から **「Ontologies/KGs for LLMs」** へシフト。

---

## 4. LLM-DRIVEN KNOWLEDGE EXTRACTION (L314–468) — **必読**

LLM 駆動の知識抽出は 2 つのパラダイムに沿って進化:

### 4.1 Schema-Based — 構造的ガイダンスあり

#### 4.1.1 静的スキーマ駆動
- **Kommineni** (2024): 完全に事前定義された TBox + ABox 充填。高い一貫性 / 限られた柔軟性
- **KARMA** (2025): マルチエージェントが固定オントロジー境界内でタスクを分担
- **Feng** (2024): 2 段階「オントロジーに基づく抽出」 — テキストから ontology を生成 → RDF triple 抽出のプロンプトに使う
- **ODKE+** (2025): ontology snippet (動的に選択した部分集合) で実行時の局所的適応
- **Bhattarai** (2024): UMLS で動的にプロンプト生成

#### 4.1.2 動的・適応的スキーマベース
- **AutoSchemaKG** (2025): 教師なしクラスタリング + 関係発見でスキーマを誘導、抽出と共に進化
- **AdaKGC** (2023): SPI (Schema-Enriched Prefix Instruction) + SDD (Schema-Constrained Dynamic Decoding) で再訓練なしの適応

→ **「スキーマが抽出を導く」 から 「スキーマが抽出と共進化する」** へ。

### 4.2 Schema-Free — 事前定義なし、LLM が自律的に構造発見

#### 4.2.1 構造化生成抽出
- **Nie** (2024): Chain-of-Thought で entity / relation 識別の段階的推論
- **AutoRE** (2024): RHF (Relation–Head–Facts) パイプライン、文書全体の整合性 / スケーラビリティ向上
- **Papaluca** (2024): Retrieval-Augmented プロンプティングで例を動的注入
- **ChatIE** (2024): マルチターン対話で entity / relation 候補を反復洗練
- **KGGEN** (2025): 抽出を 2 段階 LLM 呼出に分解 (entity 検出 → 関係生成) で認知負荷軽減

#### 4.2.2 Open Information Extraction (OIE)
- **EDC** (2024): few-shot で自然言語 triple を網羅生成 → 後段で正規化
- カバレッジ・発見性を構造的規則性より優先

→ schema 誘導や正規化と組み合わせると、**「schema-free → schema-generative」** の連続体が完成。

---

## 5. LLM-POWERED KNOWLEDGE FUSION (L469–572) — **必読**

知識融合は 2 つのレベルの課題に対応:
- **Schema layer**: 統一・正規化された知識スケルトン構築
- **Instance layer**: 具体的な知識インスタンスの統合・整合

### 5.1 Schema-Level Fusion

3 つのフェーズの進化:
1. **Ontology-driven consistency** (Kommineni 2024): 事前定義 ontology を global constraint として強制
2. **Data-driven unification** (LKD-KGC 2025): 埋め込みベースで等価 entity type をクラスタリング・マージ
3. **LLM-enabled canonicalization** (EDC 2024): LLM がスキーマコンポーネントの自然言語定義を生成 → ベクトル類似度で比較し自己整合 / クロススキーママッピング

→ **ontology-driven → data-driven → LLM-enabled** という進化。

### 5.2 Instance-Level Fusion

- **KGGEN** (2025): 反復 LLM クラスタリングで等価 entity / relation をマージ
- **LLM-Align** (2024): 整合を制約付き選択問題として扱う
- **EntGPT** (2025): 2 段階洗練 (候補生成 → ターゲット推論)
- **Pons** (2025): RAG ベース融合でクラス階層 / entity 説明を活用、ゼロショット曖昧解消
- **COMEM** (2024): 軽量フィルタ + 細粒度推論を多段で連鎖、スケーラビリティと精度の両立

→ LLM は **単純マッチャから、文脈・構造・検索シグナルを統合する適応的推論エージェント** へ。

### 5.3 Comprehensive / Hybrid Frameworks

- **KARMA** (2025): マルチエージェントでスキーマ整合・対立解決・品質評価を協調
- **ODKE+** (2025): ontology-guided ワークフローでスキーマ監視 + instance 確認
- **Graphusion** (2024): 単一の生成サイクルで整合・統合・推論を全部こなす統一プロンプトベース

→ 自律的・自己進化型 KG への重要なステップ。

---

## 6. FUTURE APPLICATIONS (L573–662) — **必読**

4 つの有望な研究方向:

### 6.1 KG-Based Reasoning for LLMs

- 構造化 KG を LLM の推論メカニズムに統合 → 論理的一貫性 / 因果推論 / 解釈可能性を強化
- **「知識構築から知識駆動推論へ」** の概念的移行
- KG_based Random-Walk Reasoning (2024), KG-RAR (2025) など
- **自己改善ループ**: 強化された推論能力が、より堅牢で自動化された KG 構築を支える

### 6.2 Dynamic Knowledge Memory for Agentic Systems

- 有限のコンテキストウィンドウを **持続的・構造化メモリ** で克服
- KG を **「動的メモリ基盤」** として、エージェントの相互作用と共に進化
- **A-MEM** (2025): 文脈メタデータ付きの相互接続「ノート」、継続的な再編成と成長
- **Zep** (2025): 時間的知識グラフ (TKG) で事実の妥当性を管理、time-aware reasoning

### 6.3 Multimodal Knowledge Graph (MMKG) Construction

- テキスト・画像・音声・動画を統合した構造化表現
- **VaLiK** (2025): VLM で視覚特徴 → テキスト → クロスモーダル検証
- **KG-MRI** (2024): 対照学習による多モーダル埋め込み
- 課題: モダリティ異質性 / 整合ノイズ / スケーラビリティ / 欠損モダリティ堅牢性

### 6.4 New Roles for KGs in LLM Applications: Beyond RAG

- KG を **「認知的中間層」** として、生入力と LLM 推論をつなぐ
- 構造化された scaffold をクエリ・計画・意思決定に提供
- **CogER** (2023): 推薦を認知認識 KG 推論として定式化
- **PKG-LLM** (2025): バイオメディカル領域でドメイン KG による知識拡張・予測

→ KG は単なる検索バックボーンを超えて、**「インタラクティブな推論基盤」** に進化する。

---

## 7. CONCLUSION (L663–682) — 推奨

### 著者がまとめる 3 つのトレンド:

1. **静的スキーマ → 動的誘導**
2. **パイプラインのモジュール性 → 生成的統合**
3. **シンボリックな硬直性 → 意味的適応性**

これらにより KG は **「言語理解と構造化推論を融合させた、生きた認知インフラ」** に再定義される。

残る課題: スケーラビリティ / 信頼性 / 継続的適応。
今後の鍵: プロンプト設計 / マルチモーダル統合 / 知識基盤推論。

---

## どこを読むべきか — タグPJ視点での提案

### 第一優先 (= まず読む)

1. **§1 INTRODUCTION** (L32–101): 3 課題 + 3 メカニズムが論文全体の地図
2. **§3 ONTOLOGY CONSTRUCTION** (L178–313): タグマスタの位置づけを top-down/bottom-up で整理する材料。特に 3.2 (KGs for LLMs) は RAG・記事推薦と直結
3. **§4 KNOWLEDGE EXTRACTION** (L314–468): 堀崎タグは schema-based 寄りだが、4.1.2 (動的) と 4.2 (schema-free) は将来の発展経路
4. **§5 KNOWLEDGE FUSION** (L469–572): 記事マッチング / タグ重複解消 / 矛盾管理の参考。特に 5.2 (LLM-Align, EntGPT, COMEM) は実装イメージしやすい
5. **§6 FUTURE APPLICATIONS** (L573–662): 中長期ロードマップの方向性 (推論・エージェントメモリ・MMKG・RAG超え)
6. **§7 CONCLUSION** (L663–682): 3 トレンドはタグPJの「次の一手」 を判断する軸

### 第二優先

- **§2 PRELIMINARIES** (L102–177): 伝統的アプローチの整理 — タグPJの現在地把握用

### スキップ可

- **REFERENCES** (L685–): 個別フレームワーク調査時に参照
