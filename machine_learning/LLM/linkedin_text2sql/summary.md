---

marp: true
theme: default
header: "LinkedIn SQL Bot事例に学ぶText-to-SQLの実践"
style: |
section {
font-size: 28px;
background-repeat: no-repeat;
}

section\:not(.cover) {
background-image: url("slide\_template.svg");
background-position: top left;
background-size: 1280px;
}

section.cover {
background-image: url("cover\_template.svg");
background-position: center center;
background-size: cover;
}

h1 {
font-size: 42px;
}
h2 {
font-size: 36px;
}
img {
max-height: 450px;
display: block;
margin: 0 auto;
}
a {
color: #0066cc;
}
-

<!-- _class: cover -->

# LinkedIn SQL Botの事例に学ぶ

## 実用的Text-to-SQLの展開戦略

2025年5月

---

## 背景と目的

* データ専門家の工数削減
* SQL Botの目的:

  * 自然言語→SQL変換
  * クエリ生成 & 修正 & 実行支援
* DARWINプラットフォームに統合

![bg contain right:40%](sqlbot_overview.png)

---

## 戦略 #1: 高品質なメタデータと検索最適化

* EBR（埋め込みベース検索）を採用
* 不完全メタデータへの対応:

  * 認証済みデータセットの説明収集
  * Slack議論＋AI補完
* ユーザ組織図とICAによるパーソナライズ
* DataHubと連携して更新・廃止の自動管理

---

## 戦略 #2: LLM×知識グラフによる最適化

* 知識グラフ構成:

  * ノード: ユーザ・テーブル群・フィールドなど
  * 属性: 使用頻度, メトリクス分類, 結合履歴など
* LLMを活用:

  * テーブル/フィールド選択の再ランク
  * 計画→段階的クエリ生成 (LangGraph的分業構造)
* EXPLAIN実行+自己修正で最終精度を担保

---

## 戦略 #3: リッチUIによるUX向上

* DARWINに統合 → 採用率5〜10倍増
* Quick replies & guidedモードの導入
* 表示要素:

  * テーブルメタ情報＋DataHubリンク
  * クエリ構文チェック＋修正提案ボタン
* アクセス権の自動判定と接続コード補完

![bg contain right:40%](query_output_ui.png)

---

## 戦略 #4: ユーザによるカスタマイズ性

* カスタマイズ手段:

  1. データセット定義 (ユーザorグループ単位)
  2. カスタム指示の登録 (優先テーブルなど)
  3. サンプルクエリの登録 (certifiedタグ付き)
* UIから直感的に指定可能に

---

## 戦略 #5: 継続的ベンチマーキング

* 評価指標:

  * recall, hallucination率, 構文正当性, 応答レイテンシ
* 人手＋LLM-as-a-judgeによる評価体制
* 回答が複数存在するケースも考慮:

  * 60%以上の質問に複数正答あり
  * 3ヶ月毎に専門家レビューでSOT更新

---

## インパクトと学び

* 社内採用率の高さ: 約95%が「合格以上」評価
* “Fix with AI”の利用率80%以上 → 高ROI機能
* コンテキスト公開・インライン修正など改善余地も明確

![bg contain right:40%](fix_with_ai.png)

---

## まとめ: 学びのエッセンス

* 高品質な検索+LLM分業+UX改善の三位一体が鍵
* LangGraph・DataHubとの統合が本質的
* 評価指標を持つことで継続改善が可能に

### 💡 高ROIなpain pointの特定から始めよう！

---

## 参考リンク & 謝辞

* [Practical Text-to-SQL for Data Analytics](https://www.linkedin.com/blog/engineering/ai/practical-text-to-sql-for-data-analytics)
* Contributorsに深いリスペクト🙏
* トピック: Generative AI / Data Science / RAG / LangChain
