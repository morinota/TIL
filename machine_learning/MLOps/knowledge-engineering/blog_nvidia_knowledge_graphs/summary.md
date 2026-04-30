# Summary: Insights, Techniques, and Evaluation for LLM-Driven Knowledge Graphs

- 出典: https://developer.nvidia.com/blog/insights-techniques-and-evaluation-for-llm-driven-knowledge-graphs/
- 発行: NVIDIA Developer Blog

## TL;DR

LLMで非構造テキストから知識グラフ(KG)を自動構築し、それをRAGのretrieverとして接続する一連のパイプラインを提示する記事。大モデルで教師データ生成→小モデルをFTする蒸留的アプローチでコストと精度を両立。3手法比較ではGraphRAGが正確性で最優秀、HybridRAGが規制ドメイン向けにバランス良好と結論。NVIDIA NeMo / NIM / cuGraph の宣伝も兼ねる。

## 背景と課題

- 従来のベクトルRAGは単純QAに強いが、複数ソース横断・多段推論が必要な複雑質問でハルシネーションが出やすい
- マルチクエリRAGやクエリ拡張でも、中間推論ステップやデータ型横断の関係把握は困難
- KGで非構造データを「エンティティ + 関係」として構造化すると、推論精度が上がり幻覚が減る

## 知識グラフの作り方 (本記事の中心)

### 1. データ準備
- arXiv論文 (メタデータ/著者/画像) をソースにテキストをチャンク分割

### 2. スキーマ先行設計
- エンティティのクラス/カテゴリ/関係/プロパティを事前定義
- エンティティ一貫性を担保 (例: America / USA / US / United States → 同一ノード)

### 3. トリプレット抽出
- プロンプト設計済みの **Llama-3 70B NIM** にチャンクを投入し `(entity1, relation, entity2)` を出力
- 初期精度が不十分 → 小型化 + FT へ

### 4. ファインチューニング (蒸留的アプローチ)
- 教師データ生成: **Mixtral-8x7B** で合成トリプレットを作成
- 学習: **Llama-3 8B** を **NeMo Framework + LoRA** でFT
- 効果: 精度向上・レイテンシ減・推論コスト減・出力フォーマット安定化

### 5. 構造化出力の強制
- JSONモード / function calling
- ネイティブ未対応ならFTでJSON出力を学習させる
- 崩れた出力はre-promptで修正 (括弧抜け・句読点)

### 6. グラフDB投入
- トリプレットを Python list/dict にパース → グラフDBへインデックス

### 7. 推論スケール
- NeMo重みを **TensorRT-LLM** checkpointへ変換
- GPU加速推論で数千チャンクを高スループット処理

## cuGraph (GPU加速グラフ分析)

- NVIDIA RAPIDS が提供するGPU加速グラフフレームワーク
- NetworkX / cuDF / cuML とシームレス統合、コード変更ほぼなしで加速
- 最短経路・PageRank・コミュニティ検出などで関連ノード/エッジを高速ランキング
- 数十億ノード規模にマルチGPUでスケール、マルチホップ検索を効率化

## 3手法の比較評価

- 評価モデル: **nemotron-340b reward model**
- 指標: Helpfulness / Correctness / Coherence / Complexity / Verbosity (0〜4)
- データ: arXiv論文。GT QAペアは nemotron-340b 合成データ生成で作成

### 結果
- **GraphRAG**: 正確性・総合性能で最優秀。関係コンテキストを使った深い検索が強み
- **VectorRAG**: ベースライン。単純な意味検索
- **HybridRAG**: Vector + Graphの良いとこ取り。ほぼ全指標でVectorRAGを上回る可能性。一貫性に若干のトレードオフ

### 示唆
- 金融/医療など根拠の強さが重要な規制ドメイン → HybridRAGが好適
- 高精度・深い文脈理解が必須 → GraphRAG

## 残課題と今後

- **動的更新**: リアルタイムデータの組み込み、大規模更新時の関連性維持
- **スケーラビリティ**: 数十億ノード/エッジ規模の効率維持
- **トリプレット抽出の精緻化**: 抽出エラー・不整合の低減
- **システム評価**: ドメイン特化のメトリクス/ベンチマーク整備
- **今後の方向性**: 動的KG、エキスパートエージェント連携、グラフ埋め込みの意味的表現

## 所感 / 自分の業務への示唆

- 「大モデルで教師生成 → 小モデルFT」は堀崎タグ等のタグ付けワーカーでも再利用可能なパターン
- JSONモード + FT + re-prompt の三段構えは構造化出力の安定化テンプレとして流用できる
- GraphRAG採用には「スキーマ設計」「エンティティ正規化」というドメイン知識コストがかかる点に注意
- タクソノミー運用の観点では、LLM抽出後の **エンティティ正規化** (同義語/別表記の統合) が品質の肝
