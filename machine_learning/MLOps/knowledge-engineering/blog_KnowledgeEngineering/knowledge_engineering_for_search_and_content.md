refs: https://medium.com/@brian-curry-research/knowledge-engineering-for-search-and-content-a-practical-guide-468eb49ce3b1


# Knowledge Engineering for Search and Content: A Practical Guide 知識工学による検索とコンテンツ：実践ガイド  
Brian James Curry  
Apr 11, 2026 2026年4月11日  
How modern content platforms turn messy human language into structured understanding — and the open-source frameworks I’ve built to do it at scale.  
現代のコンテンツプラットフォームが混沌とした人間の言語を構造化された理解に変える方法 — そして、私がそれを大規模に実現するために構築したオープンソースのフレームワーク。

## Why Knowledge Engineering Is Back なぜ知識工学が再び注目されているのか

For twenty years, knowledge engineering was the unglamorous corner of information science. 
20年間、知識工学は情報科学の地味な一角でした。
Taxonomies lived in spreadsheets. 
分類体系はスプレッドシートに存在していました。
Ontologies were academic. 
オントロジーは学術的なものでした。(オントロジーわからん...!:thinking:)
Librarians ran the show, and the work was slow, manual, and easy to ignore when keyword search seemed “good enough.”  
図書館員が主導し、作業は遅く手動で行われ、キーワード検索が「十分良い」と思われるときには無視されやすかったのです。

That era is over.  
その時代は終わりました。

The rise of large language models, AI-generated answers, semantic search, and content recommendation systems has made one thing clear: 
大規模言語モデル、AI生成の回答、セマンティック検索、コンテンツ推薦システムの台頭は、1つのことを明らかにしました。
the teams that win are the ones with the best structured understanding of their content and their users’ intent. 
**勝者となるチームは、自分たちのコンテンツとユーザの意図を最もよく構造化して理解しているチーム**です。
LLMs hallucinate less when grounded in a real knowledge graph. 
LLMは、実際の知識グラフに基づくと、幻覚を起こしにくくなります。
Rankers work better when they understand entities, not just tokens. 
ランカーは、トークンだけでなくエンティティを理解することで、より良く機能します。
Content classification drives every downstream decision — what to show, what to suppress, what to recommend, what to summarize.  
コンテンツ分類は、すべての下流の意思決定を推進します — 何を表示するか、何を抑制するか、何を推薦するか、何を要約するか。
(頑張りてぇ...!:thinking:)

Knowledge engineering is the discipline that makes all of this work.  
**知識工学は、これらすべてを機能させる学問**です。(knowledge engineering初めて聞いた...!:thinking:)
I’ve spent the last several years building knowledge systems for enterprises ranging from $4B to $125B in revenue, 
私は過去数年間、40億ドルから1250億ドルの収益を上げる企業向けに知識システムを構築してきました。
and in the process I’ve released a set of open-source Python frameworks — MeaningFlow, Papilon, and PyCausalSim — that handle the core pieces of a modern knowledge engineering stack. 
その過程で、現代の知識工学スタックのコア部分を扱うオープンソースのPythonフレームワーク — MeaningFlow、Papilon、PyCausalSim — をリリースしました。
This article walks through the discipline itself, how to do it, and where those frameworks fit in a practical pipeline.  
この記事では、知識工学の学問そのもの、実施方法、そしてそれらのフレームワークが実際のパイプラインにどのように適合するかについて説明します。

<!-- ここまで読んだ! -->

## What Knowledge Engineering Actually Means 知識工学が実際に意味すること

Knowledge engineering is the practice of encoding what a system needs to know about the world into a form that machines can reason over.  
**知識工学は、システムが世界について知っておく必要があることを、機械が推論できる形にエンコードする実践**です。
In a content and search context, that means four tightly-coupled artifacts:  
**コンテンツと検索の文脈では、それは4つの密接に結びついたアーティファクト**を意味します：

- A taxonomy — a controlled hierarchy of categories (entertainment → music → hip-hop → southern hip-hop).  
  - タクソノミー — カテゴリの制御された階層（エンターテインメント → 音楽 → ヒップホップ → サザンヒップホップ）。

- An ontology — the types of things in your domain and how they relate (an Artist performs a Song; a Song belongs to an Album; an Album has a release date).  
  - オントロジー — あなたのドメインにおける物の種類とそれらの関係（アーティストは曲を演奏する；曲はアルバムに属する；アルバムにはリリース日がある）。

- A knowledge graph — actual instances populated into that ontology (Kendrick Lamar performed “HUMBLE.” on the album DAMN., released April 14, 2017).  
  - 知識グラフ — そのオントロジーに実際のインスタンスが埋め込まれたもの（ケンドリック・ラマーはアルバム「DAMN.」で「HUMBLE.」を演奏しました。リリース日は2017年4月14日です）。

- A query understanding layer — the mapping from how users actually phrase things to the entities and categories above.  
  - クエリ理解レイヤー — ユーザが実際に物事をどのように表現するかを、上記のエンティティとカテゴリにマッピングすることです。

The mistake most teams make is treating these as separate projects owned by separate teams.  
**ほとんどのチームが犯す間違いは、これらを別々のチームが所有する別々のプロジェクトとして扱うこと**です。
They aren’t. They are four views of the same problem: how does our system represent meaning?  
それらはそうではありません。それらは**同じ問題の4つの視点です：私たちのシステムはどのように意味を表現するのか？**

<!-- ここまで読んだ! -->

## The Five Pillars 五つの柱

I structure every knowledge engineering program around five pillars. 
私はすべての知識工学プログラムを**五つの柱**に基づいて構成します。 
Skip any one and the others collapse. 
どれか一つを省略すると、他の柱が崩れてしまいます。

1. Taxonomy and ontology design — the shape of the world.  
   1. タクソノミーとオントロジーの設計 — 世界の形。

2. Content classification — putting documents into that shape.  
   2. コンテンツ分類 — 文書をその形に配置すること。

3. Entity extraction and linking — recognizing the things inside documents.  
   3. エンティティ抽出とリンク — 文書内の物事を認識すること。

4. Query understanding — mapping user language onto the shape.  
   4. クエリ理解 — ユーザの言語をその形にマッピングすること。

5. Evaluation and causal attribution — proving it works and improving it.  
   5. 評価と因果帰属 — それが機能することを証明し、改善すること。

Let’s walk through each.  
それぞれを詳しく見ていきましょう。

<!-- ここまで読んだ! -->

## Pillar 1: Taxonomy and Ontology Design  柱1: タクソノミーとオントロジーの設計  

### Top-Down vs. Bottom-Up トップダウン vs. ボトムアップ  

Every taxonomy project faces the same tension.  
すべてのタクソノミープロジェクトは同じ緊張に直面します。  
You can design the hierarchy top-down based on editorial judgment and domain expertise, or bottom-up by clustering what your content and queries actually contain.  
階層をトップダウンで設計することも、編集者の判断やドメインの専門知識に基づいて行うことも、ボトムアップでコンテンツやクエリが実際に含むものをクラスタリングすることもできます。  
Pure top-down produces elegant structures that don’t match reality.  
純粋なトップダウンは、現実に合わない優雅な構造を生み出します。  
Pure bottom-up produces messes that no editor can defend.  
純粋なボトムアップは、どの編集者も擁護できない混乱を生み出します。  

The answer is both, in sequence:  
**答えは、両方を順番に行うこと**です。  

- **Step 1 — Seed top-down.**  
ステップ1 — トップダウンでのシード。  
Start with a small, opinionated hierarchy written by subject matter experts.  
専門家によって書かれた小さな意見のある階層から始めます。
Three to five top-level categories, two levels deep.  
3〜5のトップレベルのカテゴリ、2階層の深さです。  
Resist the urge to go deeper.
**これ以上深く掘り下げる衝動を抑えてください。**
You don’t know enough yet.  
まだ十分に理解していません。  

- **Step 2 — Mine bottom-up.**  
ステップ2 — ボトムアップでのマイニング。  
Pull six to twelve months of your query logs and content corpus.  
**6〜12か月のクエリログとコンテンツコーパスを取得**します。
Cluster them. 
それらをクラスタリングします。  
Look at what falls outside your seed taxonomy.  
**シードタクソノミーの外にあるものを見てください。**  
Those gaps are the real shape of your domain.  
**それらのギャップが、あなたのドメインの本当の形です。**  

- **Step 3 — Reconcile.**  
ステップ3 — 調整します。  
Expand the seed taxonomy to cover the gaps, merge branches that nobody actually uses, and split branches that are doing double duty.  
ギャップをカバーするためにシードタクソノミーを拡張し、**実際に誰も使用していないブランチを統合し、二重の役割を果たしているブランチを分割**します。 

<!-- ここまで読んだ! -->

### MeaningFlow: A Framework for Semantic Mining セマンティックマイニングのためのフレームワーク  

The bottom-up mining step is where I’ve spent the most engineering effort, and it’s why I built MeaningFlow, an open-source framework for semantic content analysis.  
ボトムアップのマイニングステップは、私が最も多くのエンジニアリング努力を費やした部分であり、セマンティックコンテンツ分析のためのオープンソースフレームワークであるMeaningFlowを構築した理由です。  
MeaningFlow takes a content corpus or a query log, embeds it using Sentence-BERT, reduces dimensionality with UMAP, clusters with HDBSCAN, and then builds a NetworkX graph over the clusters so you can see how topics relate to each other and where the gaps are.  
MeaningFlowは、コンテンツコーパスまたはクエリログを取り込み、Sentence-BERTを使用して埋め込み、UMAPで次元を削減し、HDBSCANでクラスタリングし、その後クラスタ上にNetworkXグラフを構築して、トピックがどのように関連し、ギャップがどこにあるかを視覚化します。

The core pipeline looks like this:  
コアパイプラインは次のようになります：  

```python
from meaningflow import SemanticGraph
import pandas as pd
# Load queries and existing content
queries = pd.read_parquet("queries_last_180d.parquet")["query"].tolist()
content = pd.read_parquet("content_corpus.parquet")["title"].tolist()
# Build a semantic graph of the demand side (queries)
demand = SemanticGraph(
texts=queries,
embedder="all-MiniLM-L6-v2",
min_cluster_size=50,
)
demand.fit()
# Build a semantic graph of the supply side (content you already have)
supply = SemanticGraph(texts=content, embedder="all-MiniLM-L6-v2")
supply.fit()
# Find coverage gaps: clusters of demand with no nearby supply
gaps = demand.coverage_gaps(
reference=supply,
similarity_threshold=0.55,
)
for g in gaps[:20]:
print(f"Gap cluster (n={g.size}): {g.top_terms[:5]}  demand={g.volume}")
```

What this gives you is a ranked list of topical areas where users are asking questions and your content isn’t answering them.  
これにより、ユーザが質問をしているがあなたのコンテンツが回答していないトピック領域のランク付けされたリストが得られます。
That list is the foundation of a bottom-up taxonomy proposal.  
そのリストは、ボトムアップのタクソノミー提案の基礎です。
Editors review the gap clusters, name them, and decide which ones deserve new branches in the hierarchy.  
**編集者はギャップクラスタをレビューし、それに名前を付け、どのクラスタが階層に新しいブランチを持つに値するかを決定**します。  

Underneath, the same primitives are available if you want to build your own pipeline from scratch:  
その下では、独自のパイプラインをゼロから構築したい場合に利用できる同じプリミティブがあります：  

```python
from sentence_transformers import SentenceTransformer
import hdbscan
import umap
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(queries, batch_size=256, show_progress_bar=True)
reducer = umap.UMAP(n_neighbors=30, n_components=10, metric="cosine", random_state=42)
reduced = reducer.fit_transform(embeddings)
clusterer = hdbscan.HDBSCAN(
min_cluster_size=50,
min_samples=10,
metric="euclidean",
cluster_selection_method="eom",
)
labels = clusterer.fit_predict(reduced)
```  

The -1 bucket is noise — queries too unique to cluster.  
-1バケットはノイズです — クラスタリングするにはあまりにもユニークなクエリです。  
In a healthy search system, noise should be 10–25% of your corpus.  
**健全な検索システムでは、ノイズはコーパスの10〜25％であるべき**です。  
Higher means your embedding model doesn't understand your domain.  
それ以上の場合、あなたの埋め込みモデルはあなたのドメインを理解していないことを意味します。  
Lower often means you're over-clustering and losing the long tail.  
それ以下の場合、過剰にクラスタリングしてロングテールを失っていることが多いです。  

<!-- ここまで読んだ! -->

### Ontology: Types and Relations オントロジー: タイプと関係  

A taxonomy tells you what categories exist.  
タクソノミーは、どのカテゴリが存在するかを教えてくれます。  
An ontology tells you what kinds of things exist and how they relate.  
**オントロジーは、どのような種類のものが存在し、それらがどのように関連しているかを教えてくれます。**  
This matters because classification alone isn’t enough for modern search.  
**これは、分類だけでは現代の検索には不十分だから**です。(わかる、カテゴリだけでは、ユーザをガイドできない...!:thinking:)
If a user searches for “movies directed by the guy who made Parasite,” you need to know that Movie is a type, Director is a type, and directed_by is a relation between them.  
ユーザが「パラサイトを作った人が監督した映画」を検索した場合、Movieはタイプであり、Directorはタイプであり、directed_byはそれらの間の関係であることを知っておく必要があります。

A minimal ontology definition can live in a YAML file:  
最小限のオントロジー定義はYAMLファイルに記述できます：  

```yaml
types:
   Person:
      attributes: [name, birth_date, nationality]
   Movie:
      attributes: [title, release_year, runtime, genre]
   Album:
      attributes: [title, release_date, label]

relations:
   directed_by:
      domain: Movie
      range: Person
   performed_by:
      domain: Song
      range: Person
   belongs_to:
      domain: Song
      range: Album
```  

Keep it small.  An ontology that tries to cover everything covers nothing well.  
**小さく保ってください。すべてをカバーしようとするオントロジーは、何も十分にカバーしません。**  
Start with the entity types that show up in your top 1,000 queries and expand from there.  
あなたのトップ1,000クエリに現れるエンティティタイプから始め、そこから拡張してください。  

<!-- ここまで読んだ! -->

## Pillar 2: Content Classification 柱2: コンテンツ分類

Once the taxonomy exists, every piece of content needs to be placed in it. 
**分類体系が存在するようになったら、すべてのコンテンツをその中に配置する必要があります。**
For a site with ten thousand documents, editors can do this by hand.
1万件の文書を持つサイトでは、編集者が手作業でこれを行うことができます。 
For a site with ten million, you need machine learning, and the question becomes which approach. 
**1千万件の文書を持つサイトでは、機械学習が必要であり、どのアプローチを選ぶかが問題になります。**(ここはまあLLMでだいぶハードル下がったよね...!:thinking:)

There are three practical options, and you should probably run all three in parallel. 
**実用的な選択肢は3つあり、おそらくすべてを並行して実行するべき**です。(ふむふむ...!:thinking:)

- Zero-shot classification with LLMs. 
**その1: LLMを用いたゼロショット分類。** 
Fast to set up, no training data required, surprisingly good out of the box for broad categories. 
設定が簡単で、トレーニングデータは不要で、広範なカテゴリに対して驚くほど良好な結果を出します。 
Use it as your baseline and for cold-start on new taxonomy branches. 
これをベースラインとして使用し、新しい分類体系のブランチのコールドスタートに利用します。 

```python
from openai import OpenAI
import json
client = OpenAI()
TAXONOMY = {
"Music": ["Hip-Hop", "Rock", "Pop", "Electronic", "Classical"],
"Film": ["Drama", "Comedy", "Documentary", "Action", "Horror"],
"Sports": ["Basketball", "Football", "Soccer", "Tennis"],
}
def classify(text: str) -> dict:
taxonomy_str = json.dumps(TAXONOMY, indent=2)
prompt = f"""Classify the following content into exactly one top-level category
and one subcategory from this taxonomy. If nothing fits, return "Other".
Taxonomy:
{taxonomy_str}
Content:
{text}
Respond with only JSON: {{"category": "...", "subcategory": "...", "confidence": 0.0-1.0}}
"""
response = client.chat.completions.create(
model="gpt-4o-mini",
max_tokens=200,
response_format={"type": "json_object"},
messages=[{"role": "user", "content": prompt}],
)
return json.loads(response.choices[0].message.content)
```  

- 2. Fine-tuned encoder classifier. 
**その2: ファインチューニングされたエンコーダ分類器。** 
Once you have a few thousand labeled examples — typically harvested by running the LLM baseline and having editors correct its mistakes — fine-tune a small encoder model like DeBERTa or a distilled BERT variant. 
**数千のラベル付き例が得られたら（通常はLLMのベースラインを実行し、編集者がその誤りを修正することで収集されます）、DeBERTaや蒸留BERTのような小さなエンコーダモデルをファインチューニング**します。 
It will be cheaper, faster, and often more accurate than the zero-shot LLM for your specific taxonomy. 
これにより、**特定の分類体系に対してゼロショットLLMよりも安価で迅速、かつしばしばより正確になります。** 

- 3. Rule-based overrides. 
**その3: ルールベースのオーバーライド。** 
Never remove these. 
**これらを削除してはいけません。** 
For every automated system, there will be edge cases where the business needs a hard guarantee: breaking news must always be classified as News, a specific publisher’s content must always route to a specific vertical, legally sensitive categories need manual review. 
**すべての自動化システムには、ビジネスが厳密な保証を必要とするエッジケースがあります**：速報は常にニュースとして分類される必要があり、特定の出版社のコンテンツは常に特定の縦のカテゴリにルーティングされる必要があり、法的に敏感なカテゴリは手動レビューが必要です。(なるほど、意識したい...!!:thinking:)
Rules are ugly but essential. 
ルールは醜いですが、不可欠です。 

<!-- ここまで読んだ! -->

The architecture pattern is simple: rules first, fine-tuned classifier second, LLM fallback third, human review queue for anything with low confidence across all three. 
**アーキテクチャパターンはシンプルです：ルールが最初、ファインチューニングされた分類器が次、LLMのフォールバックがその次、すべての3つで低い信頼度のものに対する人間のレビューキュー**です。

One integration pattern I’ve used repeatedly: run the classifier output back through the MeaningFlow semantic graph.
私が繰り返し使用してきた統合パターンの1つは、分類器の出力をMeaningFlowセマンティックグラフに戻すことです。 
If a classifier assigns a document to “Hip-Hop” but the document’s embedding sits inside a “Classical” cluster with high density, that’s a signal to route the document to human review. 
もし分類器が文書を「ヒップホップ」に割り当てたが、その文書の埋め込みが高密度の「クラシック」クラスタ内にある場合、それは文書を人間のレビューにルーティングする信号です。 
The graph acts as a sanity check on the classifier, and the classifier acts as a sanity check on the graph. 
**グラフは分類器の健全性チェックとして機能し、分類器はグラフの健全性チェックとして機能**します。(このアイデアは頭に入れておいていいかも...!!:thinking:)
Disagreements between them are exactly the examples most worth having an editor look at. 
それらの間の不一致は、まさに編集者が見る価値のある例です。

<!-- ここまで読んだ! -->

### The Labeling Problem ラベリングの問題

The hardest part of classification is not the model. 
分類の最も難しい部分はモデルではありません。
It is producing enough clean labeled data to train and evaluate it. 
それは、トレーニングと評価のために十分なクリーンなラベル付きデータを生成することです。 
Three techniques worth knowing: 
**知っておくべき3つの技術**： 

- Active learning. 
**その1: アクティブラーニング。** 
Don’t label randomly. 
ランダムにラベルを付けてはいけません。 
Label the examples the current model is most uncertain about. 
現在のモデルが最も不確実な例にラベルを付けます。 
Every labeled example moves the decision boundary more than ten random labels would. 
すべてのラベル付き例は、10のランダムラベルよりも意思決定境界をより多く動かします。 

- Weak supervision. 
**その2: 弱い監視。** 
Write a dozen heuristic labeling functions — regex patterns, keyword lists, existing metadata — and let a framework like Snorkel combine them into probabilistic labels. 
ダースのヒューリスティックラベリング関数（正規表現パターン、キーワードリスト、既存のメタデータなど）を作成し、Snorkelのようなフレームワークにそれらを組み合わせて確率的ラベルにします。 
Imperfect, but gets you to a usable training set in a week instead of a quarter. 
不完全ですが、四半期ではなく1週間で使えるトレーニングセットに到達します。 

- LLM-assisted labeling with human verification. 
**その3: 人間の検証を伴うLLM支援ラベリング。** 
Have an LLM produce first-pass labels at scale, then have editors verify rather than label from scratch. 
LLMにスケールで初回ラベルを生成させ、その後、編集者にゼロからラベルを付けるのではなく、検証させます。 
Verification is typically 3–5x faster than labeling. 
**検証は通常、ラベリングの3〜5倍速い**です。

<!-- ここまで読んだ! -->

## Pillar 3: Entity Extraction and Linking 柱3: エンティティ抽出とリンク

Classification puts a whole document into a category. 
分類は、全体の文書をカテゴリに分類します。
Entity extraction and linking go deeper: they identify the specific things mentioned inside the document and connect them to canonical records in your knowledge graph. 
**エンティティ抽出(entity extraction)とリンク(entity linking)はさらに深く、文書内で言及されている特定の事柄を特定し、それらを知識グラフの標準的なレコードに接続**します。

The pipeline has three stages. 
このパイプラインは**3つの段階**から成ります。

- Stage 1 — Named entity recognition (NER). 
**ステージ1 — 固有表現認識（NER）**。
Find the spans of text that refer to entities. 
エンティティを指すテキストの範囲を見つけます。 
“Kendrick Lamar released DAMN. in 2017” contains three entities: a Person, a Work, and a Date. 
「ケンドリック・ラマーは2017年にDAMN.をリリースした」には、人物、作品、日付の3つのエンティティが含まれています。 
Modern NER uses transformer-based sequence labelers; spaCy, Flair, and HuggingFace all have production-ready options.
現代のNERは、トランスフォーマーベースのシーケンスラベラーを使用します。spaCy、Flair、HuggingFaceはすべて、商用利用可能なオプションを提供しています。

- Stage 2 — Entity disambiguation. 
**ステージ2 — エンティティの曖昧性解消。** 
There are twelve people named Michael Jordan in Wikipedia. 
ウィキペディアには、マイケル・ジョーダンという名前の人が12人います。 
Which one does this mention refer to?
この言及はどの人を指しているのでしょうか？
Use surrounding context — other entities in the document, the domain of the source — to pick the right candidate. 
周囲の文脈（文書内の他のエンティティや情報源のドメイン）を使用して、正しい候補を選びます。 
A common approach is to embed both the mention-in-context and each candidate’s description, then take the cosine nearest. 
一般的なアプローチは、文脈内の言及と各候補の説明を埋め込み、コサイン類似度を計算することです。

- Stage 3 — Linking. 
**ステージ3 — リンキング。** 
Write the disambiguated entity ID back into the document metadata so downstream systems can query by entity rather than by string match. 
**曖昧性を解消したエンティティIDを文書のメタデータに書き戻し**、下流のシステムが文字列マッチではなくエンティティでクエリできるようにします。 
This is what lets “movies starring the guy from Parasite” work — the query planner resolves “the guy from Parasite” to a specific Person ID and then executes a structured lookup. 
**これにより「パラサイトの男が出演する映画」が機能**します。クエリプランナーは「パラサイトの男」を特定の人物IDに解決し、その後構造化されたルックアップを実行します。

Production systems add candidate generation from an approximate nearest neighbor index over millions of entities, a learned ranker instead of raw cosine, and confidence thresholding with a fallback to a “NIL” entity when nothing scores high enough. 
商用システムでは、数百万のエンティティに対する近似最近傍インデックスからの候補生成、生のコサインの代わりに学習されたランカー、そして十分なスコアが得られない場合の「NIL」エンティティへのフォールバックを追加します。

<!-- ここまで読んだ! -->

## Pillar 4: Query Understanding 柱4: クエリ理解

(ここは多分検索前提の話...!:thinking:)

This is where knowledge engineering meets the user. A query understanding layer takes a raw user query and produces a structured representation: intent, entities, filters, and modifiers.  
ここでは、知識工学がユーザと出会います。クエリ理解レイヤーは、生のユーザクエリを受け取り、構造化された表現を生成します：**意図、エンティティ、フィルタ、修飾子**。

![]()

“cheap hotels in tokyo under 200 with a pool” contains:  
「200ドル以下の東京の安いホテル（プール付き）」には以下が含まれます：  

- Intent: commercial, accommodation search  
  - 意図：商業、宿泊検索  
- Entity: Tokyo (Location)  
  - エンティティ：東京（場所）  
- Filters: price < 200, amenities includes “pool”  
  - フィルタ：価格 < 200、アメニティには「プール」が含まれる  
- Modifier: “cheap” (a soft preference, not a hard filter)  
  - 修飾子：「安い」（柔らかい好みであり、厳格なフィルタではない）  

Building this well requires three components.  
これをうまく構築するには、**3つのコンポーネントが必要**です。  

### Component A: Intent Classification コンポーネントA: 意図分類  

A small classifier over a fixed set of intent types. Keep the set small — ten to twenty intents is usually enough. Navigational, informational, transactional, and their domain-specific variants.  
**固定された意図タイプの小さな分類器です。セットは小さく保ちます — 通常、10から20の意図で十分**です。ナビゲーショナル、インフォメーショナル、トランザクショナル、およびそれらのドメイン特有のバリエーション。  

<!-- ここまで読んだ! -->

### Component B: Entity Linking on Queries with Session Memory コンポーネントB: セッションメモリを用いたクエリのエンティティリンク

Same pipeline as document entity linking, but harder because queries are short and context-free. “apple” in a document usually has enough surrounding text to disambiguate. “apple” as a standalone query does not.
ドキュメントエンティティリンクと同じパイプラインですが、クエリが短く、文脈がないため、より難しいです。**ドキュメント内の「apple」には通常、曖昧さを解消するための十分な周囲のテキストがありますが、単独のクエリとしての「apple」にはそれがありません。** (確かに...!:thinking:)

The trick is to use the user’s context: recent query history, current session, geographic location, device type, known interests. A user who just searched for “tim cook keynote” and then searches for “apple” almost certainly means the company. This is where your query understanding layer becomes genuinely personalized.
コツは、ユーザの文脈を使用することです：最近のクエリ履歴、現在のセッション、地理的位置、デバイスタイプ、既知の興味。最近「tim cook keynote」を検索したユーザが次に「apple」を検索すると、ほぼ確実にその会社を指しています。ここで、クエリ理解レイヤーが本当にパーソナライズされます。
(なるほどね...!:thinking:)

The architectural challenge is representing that context in a form the query understanding layer can actually use. This is a research area I’ve been working on under Vector1 Research, where I’ve proposed a cognitive architecture called Memory-Node Encapsulation (MNE) — a data structure for artificial episodic memory designed specifically for session-aware reasoning.  
アーキテクチャの課題は、その文脈をクエリ理解レイヤーが実際に使用できる形式で表現することです。これは、私がVector1 Researchの下で取り組んでいる研究分野であり、セッション対応の推論のために特別に設計された人工エピソード記憶のデータ構造であるMemory-Node Encapsulation（MNE）という認知アーキテクチャを提案しました。  
The idea is that each session becomes a memory node linking the entities, intents, and queries a user has touched, and the query understanding layer consults that node when disambiguating new queries.  
このアイデアは、各セッションがユーザが触れたエンティティ、意図、クエリをリンクするメモリノードとなり、クエリ理解レイヤーが新しいクエリの曖昧さを解消する際にそのノードを参照するというものです。  
It’s the same insight that underpins most successful personalized search systems, just made explicit as a reusable primitive.  
これは、ほとんどの成功したパーソナライズ検索システムの基盤となる同じ洞察であり、再利用可能なプリミティブとして明示化されています。

You don’t need a full MNE implementation to get value from the idea. A simple session store with recent entity IDs and their recency weights gets most of the way there:  
このアイデアから価値を得るために、完全なMNE実装は必要ありません。最近のエンティティIDとその新しさの重みを持つシンプルなセッションストアがほとんどの部分をカバーします：  

```python
from collections import deque
from dataclasses import dataclass, field
from time import time
@dataclass
class SessionMemory:
entities: deque = field(default_factory=lambda: deque(maxlen=20))
def add(self, entity_id: str):
self.entities.append((entity_id, time()))
def context_weights(self, half_life_sec: float = 300.0) -> dict:
now = time()
weights = {}
for eid, ts in self.entities:
decay = 0.5 ** ((now - ts) / half_life_sec)
weights[eid] = weights.get(eid, 0.0) + decay
return weights
```

Pass those weights into your entity disambiguator as a prior. Entities the user has recently engaged with get a bump. Everything else competes on the usual signals.  
これらの重みをエンティティの曖昧さ解消器に事前情報として渡します。ユーザが最近関与したエンティティには加点が与えられます。他のすべては通常のシグナルで競争します。

<!-- ここまで読んだ! -->

### Component C: Synonym and Misspelling Management  
### コンポーネントC: 同義語と誤字の管理  

The unglamorous but essential work. Every search team needs a living lexicon of:  
**地味ですが、不可欠な作業です。すべての検索チームには、以下のような生きた辞書が必要**です: 
(そうなんだな〜情報検索領域の初心者だからこれも知らない...!:thinking:)

- Exact synonyms — “tv” = “television”, “nyc” = “new york city”  
  - 正確な同義語 — 「tv」=「テレビ」、「nyc」=「ニューヨーク市」  
- Directional synonyms — “sneakers” → “shoes” (expand sneakers to include shoes, but not vice versa)  
  - 指向的同義語 — 「スニーカー」→「靴」（スニーカーを靴に含めるが、その逆は含めない）  
- Common misspellings — “restraunt” → “restaurant”  
  - 一般的な誤字 — 「restraunt」→「restaurant」  
- Acronym expansion — “nba” → “national basketball association”  
  - 略語の展開 — 「nba」→「全米バスケットボール協会」  
- Stop word handling — when to preserve “the” (The Who) vs. drop it (the best restaurants)  
  - ストップワードの処理 — 「the」を保持する場合（The Who）と削除する場合（the best restaurants）  

Build this as a versioned data asset, not as code. Editors need to add entries without shipping a deploy. Every entry needs a timestamp, an author, and a rationale. Every entry needs an expiration review date — slang ages fast, and a synonym that was right in 2019 may be wrong in 2026.  
**これをコードではなく、バージョン管理されたデータ資産として構築すべき**です。編集者はデプロイを行わずにエントリを追加する必要があります。すべてのエントリにはタイムスタンプ、著者、および理由が必要です。**すべてのエントリには有効期限のレビュー日が必要です — スラングはすぐに古くなり、2019年に正しかった同義語が2026年には間違っている可能性があります**。(なるほどね...!:thinking:)

A simple schema:  
シンプルなスキーマ：  

```sql
CREATE TABLE synonyms (
   id           BIGSERIAL PRIMARY KEY,
   source_term  TEXT NOT NULL,
   target_term  TEXT NOT NULL,
   relation     TEXT NOT NULL CHECK (relation IN ('exact', 'directional', 'misspelling', 'acronym')),
   locale       TEXT NOT NULL DEFAULT 'en-US',
   confidence   REAL NOT NULL DEFAULT 1.0,
   created_by   TEXT NOT NULL,
   created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
   review_by    DATE,
   rationale    TEXT,
   active       BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX ON synonyms (source_term) WHERE active;
CREATE INDEX ON synonyms (review_by) WHERE active;
```

One high-leverage automation: use the MeaningFlow graph to propose synonym candidates. Any two terms that consistently appear in the same cluster across queries are candidates for an exact or directional synonym. Editors review and approve. This is how you keep a synonym lexicon current without drowning editors in manual work.  
高い効果を持つ自動化の一つ：MeaningFlowグラフを使用して同義語候補を提案します。クエリ全体で同じクラスターに一貫して現れる2つの用語は、正確または指向的同義語の候補です。編集者がレビューして承認します。これにより、編集者を手動作業で圧倒することなく、同義語辞書を最新の状態に保つことができます。

<!-- ここまで読んだ! -->

## Pillar 5: Evaluation and Causal Attribution  柱5: 評価と因果帰属

A knowledge engineering program without evaluation is a hobby.  
**評価のない知識工学プログラムは趣味に過ぎません。**  
Three types of measurement matter.
重要な測定のタイプは3つあります。

Intrinsic quality — Is the taxonomy coherent?
**その1: 内的品質 — 分類体系は一貫していますか？** 
Do classifiers produce the right labels on a held-out test set?  
分類器は保持されたテストセットで正しいラベルを生成しますか？  
Are entity links correct?  
エンティティリンクは正しいですか？
Measure with precision, recall, F1 on a human-labeled gold set of at least a few thousand examples, refreshed quarterly.
少なくとも数千の例からなる人間ラベル付きのゴールドセットで、精度、再現率、F1を測定し、四半期ごとに更新します。  

Extrinsic quality — Does any of this actually improve search and content outcomes?  
**その2: 外的品質 — これらのいずれかが実際に検索やコンテンツの結果を改善しますか？**  
Measure with online A/B tests on downstream metrics: click-through rate, dwell time, task completion, user satisfaction.  
クリック率、滞在時間、タスク完了、ユーザ満足度などの下流指標に対してオンラインA/Bテストで測定します。  
A new classifier that scores 5% better on the gold set but moves no downstream metric is not better.  
ゴールドセットで5%良いスコアを出す新しい分類器が、下流指標に影響を与えない場合、それはより良いとは言えません。  

Drift monitoring — The world changes.  
**その3: ドリフトモニタリング — 世界は変わります。**  
Language changes.  
言語は変わります。
Queries change.  
クエリは変わります。  
A model trained in January is stale by July.  
1月に訓練されたモデルは7月には古くなります。  
Monitor the distribution of classifier confidence, the rate of “Other” or NIL classifications, and the divergence between training and production query distributions.  
分類器の信頼度の分布、「その他」またはNIL分類の割合、訓練と本番のクエリ分布の乖離を監視します。  
When drift exceeds a threshold, retrain.  
ドリフトが閾値を超えた場合、再訓練します。  

A practical drift metric is population stability index (PSI) over the classifier output distribution:  
**実用的なドリフト指標は、分類器出力分布に対する人口安定性指数（PSI）**です：  
(何それ??:thinking:)

```python
import numpy as np
def psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
"""
Population Stability Index. Compare a baseline distribution (expected)
against a current distribution (actual). Values above 0.2 typically
indicate significant drift worth investigating.
"""
breakpoints = np.linspace(0, 1, bins + 1)
exp_counts, _ = np.histogram(expected, bins=breakpoints)
act_counts, _ = np.histogram(actual, bins=breakpoints)
exp_pct = exp_counts / exp_counts.sum()
act_pct = act_counts / act_counts.sum()
exp_pct = np.where(exp_pct == 0, 1e-6, exp_pct)
act_pct = np.where(act_pct == 0, 1e-6, act_pct)
return float(np.sum((act_pct - exp_pct) * np.log(act_pct / exp_pct)))
```  

<!-- ここまで読んだ! -->

### Causal Attribution with Papilon and PyCausalSim  PapilonとPyCausalSimによる因果帰属  

A/B testing tells you whether a change helped.  
A/Bテストは、変更が役立ったかどうかを教えてくれます。  
It does not tell you why, and it does not disentangle the effect of overlapping changes — which is the reality of any real production system where multiple improvements ship in the same window.  
なぜそうなったのかは教えてくれず、重複する変更の効果を分離することもできません — これは、複数の改善が同じウィンドウで出荷される実際のproductionシステムの現実です。  
This is the problem I built Papilon and PyCausalSim to solve.  
これが、私がPapilonとPyCausalSimを構築した理由です。

Papilon is a Python framework for marketing mix modeling, causal discovery, and complex systems simulation.  
Papilonは、マーケティングミックスモデリング、因果発見、複雑なシステムシミュレーションのためのPythonフレームワークです。  
PyCausalSim is a companion library focused specifically on causal discovery through simulation.  
PyCausalSimは、シミュレーションを通じた因果発見に特化した補助ライブラリです。  
For knowledge engineering work, they handle three jobs that standard A/B testing cannot:  
**知識工学の作業において、彼らは標準のA/Bテストでは扱えない3つの仕事を処理**します：  

Attribution across overlapping changes.  
**重複する変更に対する帰属。**  
When you ship a new taxonomy, a new classifier, and a synonym update in the same quarter, Papilon’s causal discovery routines can estimate the independent contribution of each to downstream metrics, rather than crediting the entire quarter’s lift to whichever change happened to launch last.  
新しい分類体系、新しい分類器、同義語の更新を同じ四半期に出荷すると、Papilonの因果発見ルーチンは、最後に出荷された変更に全四半期の向上を帰属させるのではなく、それぞれの下流指標への独立した貢献を推定できます。  

Counterfactual simulation.  
**反事実シミュレーション。**  
PyCausalSim lets you ask: what would conversion look like if we had not expanded the taxonomy into a new branch?  
PyCausalSimを使用すると、次のように尋ねることができます：もし分類体系を新しいブランチに拡張していなかったら、コンバージョンはどのように見えたでしょうか？  
By simulating the counterfactual from the causal graph, you can estimate lift without needing to roll back in production.  
因果グラフから反事実をシミュレーションすることで、実際に戻すことなく向上を推定できます。  

Long-horizon effects.  
**長期的な効果。**  
Many knowledge engineering improvements compound over time — better classification improves the training data for the next model, which improves recommendations, which improves engagement, which improves the training data again.  
多くの知識工学の改善は時間とともに累積します — より良い分類が次のモデルの訓練データを改善し、それが推薦を改善し、エンゲージメントを改善し、再び訓練データを改善します。  
Standard A/B tests measure the immediate snapshot.  
標準のA/Bテストは即時のスナップショットを測定します。  
Papilon’s simulation engine can project these feedback loops forward.  
Papilonのシミュレーションエンジンは、これらのフィードバックループを前方に投影できます。  

A minimal pattern for attributing a content classification change:  
コンテンツ分類変更の帰属に関する最小限のパターン：  

```python
import papilon as pp
# Observational panel: metric time series plus the changes that shipped
df = pp.load_panel("search_metrics_2025.parquet")
# Discover the causal DAG over the changes and outcomes
dag = pp.discover_causal_structure(
df,
treatments=["taxonomy_v2", "classifier_retrain", "synonym_update"],
outcome="engagement_per_session",
confounders=["day_of_week", "traffic_source", "device"],
)
# Estimate the independent effect of the taxonomy change
effect = pp.estimate_effect(
df,
treatment="taxonomy_v2",
outcome="engagement_per_session",
dag=dag,
)
print(f"Taxonomy v2 independent effect: {effect.point:.3f} (95% CI {effect.ci_low:.3f}–{effect.ci_high:.3f})")
```  

This kind of attribution is the difference between “we shipped a bunch of stuff and metrics went up” and “the taxonomy expansion drove a 2.3% lift independent of the classifier retrain, and here’s the confidence interval.”  
この種の帰属は、「私たちはたくさんのものを出荷し、指標が上昇した」と「分類体系の拡張が分類器の再訓練に依存せずに2.3%の向上をもたらし、ここに信頼区間があります」という違いです。  
The second answer is what justifies the next quarter’s investment.  
2番目の回答が、次の四半期の投資を正当化するものです。  

<!-- ここまで読んだ! -->

## Where LLMs Fit LLMの適用範囲

A common question in 2026: do we still need knowledge engineering now that LLMs can do so much out of the box? 
2026年の一般的な質問：**LLMがこれほど多くのことを即座に行えるようになった今、私たちはまだ知識工学を必要としていますか？**
The short answer is yes — more than ever.  
**短い答えは「はい」です — 以前にも増して必要**です。

LLMs are powerful but ungrounded.  
LLMは強力ですが、基盤がありません。
They hallucinate.  
彼らは幻覚を見ます。
They have no stable sense of what your catalog contains, what your editorial standards are, or what is currently trending.  
**彼らは、あなたのカタログに何が含まれているのか、あなたの編集基準が何であるのか、また現在何がトレンドであるのかについての安定した感覚を持っていません。**
Knowledge engineering provides the grounding.  
知識工学が基盤を提供します。
The strongest architectures use LLMs and knowledge graphs together:  
**最も強力なアーキテクチャは、LLMと知識グラフを組み合わせて使用**します：

- LLM for flexible understanding — parse messy user queries, summarize documents, generate natural language explanations.  
  - **柔軟な理解のためのLLM** — 混乱したユーザクエリを解析し、文書を要約し、自然言語の説明を生成します。

- Knowledge graph for factual grounding — resolve entities, enforce editorial rules, serve canonical data.  
  - **事実の基盤のための知識グラフ** — エンティティを解決し、編集ルールを強制し、標準データを提供します。

- Retrieval over the graph — pull the right facts and context into the LLM prompt at inference time.  
  - **グラフ上の情報検索** — 推論時に適切な事実とコンテキストをLLMのプロンプトに引き込む。

The pattern is retrieval-augmented generation, but the quality of the retrieval depends entirely on the quality of the underlying knowledge representation.  
このパターンは情報検索を強化した生成ですが、**情報検索の質は根底にある知識表現の質に完全に依存**します。
Good knowledge engineering makes LLMs smarter.  
**良い知識工学はLLMをより賢くします。**
Bad or absent knowledge engineering makes them dangerous.  
悪い、または存在しない知識工学は彼らを危険にします。

<!-- ここまで読んだ! -->

One underused pattern: use LLMs in the knowledge engineering loop itself.  
**あまり使われていないパターンの一つ：知識工学のループ自体でLLMを使用**します。
An LLM can propose taxonomy expansions from MeaningFlow gap clusters, suggest synonym pairs from co-occurrence patterns, draft ontology relations from document corpora, and flag inconsistencies in existing entity records.  
**LLMは、MeaningFlowのギャップクラスターから分類法の拡張を提案し、共起パターンから同義語ペアを提案し、文書コーパスからオントロジー関係を草案し、既存のエンティティレコードの不整合を指摘することができます。**
Human editors then review and approve.  
その後、人間の編集者がレビューし、承認します。
This compresses months of manual work into weeks.  
これにより、数ヶ月の手作業が数週間に圧縮されます。

<!-- ここまで読んだ! -->

## Organizational Patterns That Work 組織的パターンの効果

A few hard-won lessons about how to actually run a knowledge engineering program.  
知識工学プログラムを実際に運営するための**いくつかの苦労して得た教訓**です。

### 教訓1

Embed editors with engineers. Taxonomists, classifiers, and content strategists should sit on the same team as the engineers building the systems that consume their work.  
**編集者をエンジニアと一緒に配置しろ!** 分類学者、分類者、コンテンツ戦略家は、彼らの作業を利用するシステムを構築するエンジニアと同じチームに座るべきです。 
Throwing a taxonomy spreadsheet over the wall produces taxonomies that nobody implements.  
**分類スプレッドシートを壁越しに投げることは、誰も実装しない分類を生み出します。** (うんうん...!!:thinking:)

### 教訓2: 

Treat the knowledge base as a product. It has users (internal teams and ML systems), a release cycle, versioned releases, deprecation policies, and SLAs.  
**知識ベースをプロダクトとして扱え!** 内部チームやMLシステムなどのユーザー、リリースサイクル、バージョン管理されたリリース、廃止方針、SLAがあります。
Run it like a product, not like a wiki.  
製品のように運営し、ウィキのようには運営しません。

### 教訓3:

Invest in tooling early. Editors will not hand-edit JSON.  
**早期にツールに投資しろ!** 編集者はJSONを手動で編集しません。
Build a proper editorial interface for taxonomy changes, entity edits, and synonym management before you scale the team.  
チームを拡大する前に、分類変更、エンティティ編集、同義語管理のための適切な編集インターフェースを構築します。
Every hour spent on tooling saves ten hours of frustration later.  
**ツールに費やした1時間は、後で10時間のフラストレーションを節約**します。

### 教訓4: 

Measure editor velocity. How fast can an editor add a new category, approve a classification correction, ship a new synonym?  
**編集者の速度を測定しろ!** 編集者は新しいカテゴリを追加するのにどれくらいの速さで、分類の修正を承認し、新しい同義語を出荷できますか？
If the answer is “days,” your tooling is broken. The target is minutes.  
**答えが「日」であれば、あなたのツールは壊れています。目標は「分」です。**

### 教訓5: 

Review cadence. Weekly quality reviews, monthly taxonomy reviews, quarterly gold-set refreshes, annual strategic reviews of the whole knowledge model.  
**レビューのペースを守れ!** 毎週の品質レビュー、毎月の分類レビュー、四半期ごとのゴールドセットの更新、知識モデル全体の年次戦略レビュー。
Put them on the calendar and defend them.  
それらをカレンダーに入れ、守ります。

<!-- ここまで読んだ! -->

## A Starting Blueprint 始めの設計図

If you are setting up a knowledge engineering practice from scratch, here is a sequence that has worked for me more than once.  
**もしあなたがゼロから知識工学の実践を立ち上げるのであれば、私に何度も効果があった手順**があります。

Month 1. Audit existing content and query logs. Run MeaningFlow over both to cluster the top queries and identify initial coverage gaps. Draft a seed taxonomy of 3–5 top-level categories. Assemble a gold evaluation set of 1,000 hand-labeled examples.  
月1. 既存のコンテンツとクエリログを監査します。両方に対してMeaningFlowを実行し、トップクエリをクラスタリングして初期のカバレッジギャップを特定します。3〜5のトップレベルカテゴリのシード分類法を作成します。**1,000の手動ラベル付けされた例からなるゴールド評価セットを組み立て**ます。

Month 2. Stand up the zero-shot LLM classifier baseline. Measure against the gold set. Identify the taxonomy branches where it fails. Expand or reshape the taxonomy accordingly.  
月2. **ゼロショットLLM分類器のベースラインを立ち上げ**ます。ゴールドセットに対して測定します。失敗する分類法の枝を特定します。それに応じて分類法を拡張または再構築します。

Month 3. Build the editorial tooling. Synonym management, classification review queue, taxonomy editor. Train editors on the tools.  
月3. **編集ツールを構築**します。シノニム管理、分類レビューキュー、分類法エディタ。ツールについて編集者を訓練します。

Month 4. Start entity extraction on the top-priority entity types (usually People, Places, Organizations, Works). Build the first version of the knowledge graph. Add session memory to the query understanding layer.  
月4. **最優先のエンティティタイプ（通常は人、場所、組織、作品）に対してエンティティ抽出を開始**します。知識グラフの最初のバージョンを構築します。クエリ理解層にセッションメモリを追加します。

Month 5. Launch query understanding. Intent classification, entity linking on queries, initial synonym coverage.  
月5. クエリ理解を開始します。意図分類、クエリに対するエンティティリンク、初期のシノニムカバレッジ。

Month 6. First extrinsic A/B test and causal attribution run using Papilon. Measure whether the knowledge layer actually moves search and content metrics, and decompose the lift across the changes that shipped. Iterate based on results.  
月6. Papilonを使用した最初の外部A/Bテストと因果帰属の実行。知識層が実際に検索とコンテンツの指標に影響を与えるかどうかを測定し、出荷された変更に対するリフトを分解します。結果に基づいて反復します。

By the end of six months, you have a working knowledge engineering program with measurable impact. By month twelve, it should be one of the highest-leverage capabilities your company has.  
6ヶ月の終わりまでに、測定可能な影響を持つ知識工学プログラムが完成します。12ヶ月目までには、それはあなたの会社が持つ最も高いレバレッジ能力の1つであるべきです。

(まあ半年もかけてられないので、1ヶ月でこれらのプロトタイプを作るけど...!:thinking:)

<!-- ここまで読んだ! -->

## Closing Thought 結論

Knowledge engineering used to feel like a cost center — a necessary but dull part of running a content platform. The rise of LLMs and semantic search has flipped that. 
知識工学は以前はコストセンターのように感じられ、**コンテンツプラットフォームを運営する上で必要だが退屈な部分でした。LLMとセマンティック検索の台頭がそれを逆転させました。**
Structured understanding of your content and your users is now the single biggest differentiator between search and content experiences that feel intelligent and those that feel random. 
**コンテンツとユーザの構造的理解**は、知的に感じられる検索とコンテンツ体験と、ランダムに感じられる体験との間の最大の差別化要因となっています。 

The companies that take this seriously — who invest in taxonomies, ontologies, classification pipelines, entity resolution, query understanding, and causal attribution as core infrastructure — will produce search and content experiences that their competitors cannot match. 
**これを真剣に受け止め、分類法、オントロジー、分類パイプライン、エンティティ解決、クエリ理解、因果帰属にコアインフラとして投資する企業は、競合他社が真似できない検索とコンテンツ体験を生み出すでしょう。** 
The ones that don’t will keep wondering why their LLM-powered features feel shallow. 
そうでない企業は、**自社のLLM駆動の機能がなぜ浅く感じられるのかをずっと疑問に思い続ける**でしょう。 

<!-- ここまで読んだ! -->

The work is detailed, iterative, and unglamorous. 
その作業は詳細で反復的であり、華やかさはありません。 
It is also one of the most important things a modern content platform can invest in. 
しかし、**現代のコンテンツプラットフォームが投資できる最も重要なことの一つ**でもあります。 

If any of the frameworks mentioned here are useful to you, they’re all open source and waiting for contributors. 
ここで言及されたフレームワークのいずれかがあなたにとって有用であれば、それらはすべてオープンソースであり、貢献者を待っています。 
MeaningFlow for semantic modeling, Papilon for causal and complex systems work, PyCausalSim for causal discovery through simulation. 
MeaningFlowはセマンティックモデリング、Papilonは因果および複雑なシステムの作業、PyCausalSimはシミュレーションを通じた因果発見のためのものです。 
The goal is to make the tools for this kind of work accessible to any team willing to do it. 
この種の作業のためのツールを、それを行う意欲のあるチームが利用できるようにすることが目標です。 

<!-- ここまで読んだ! -->

---  
Brian Curry is a Kansas City–based data scientist, AI researcher, and founder of Vector1 Research, an independent lab advancing marketing economics, causal inference, and cognitive AI systems. 
ブライアン・カリーは、カンザスシティを拠点とするデータサイエンティスト、AI研究者であり、マーケティング経済学、因果推論、認知AIシステムを進展させる独立した研究所Vector1 Researchの創設者です。 
He has led data and analytics initiatives at enterprises from $4B to $125B, including Koch Industries, Tractor Supply, Vail Resorts, Hallmark, Garmin, and AT&T. 
彼は、Koch Industries、Tractor Supply、Vail Resorts、Hallmark、Garmin、AT&Tなど、40億ドルから1250億ドルの企業でデータと分析のイニシアチブを主導してきました。 
He is the creator of MeaningFlow (semantic content modeling), Papilon (causal inference and complex systems), PyCausalSim (causal discovery through simulation), and the Memory-Node Encapsulation (MNE) architecture for cognitive AI. 
彼は、MeaningFlow（セマンティックコンテンツモデリング）、Papilon（因果推論と複雑なシステム）、PyCausalSim（シミュレーションを通じた因果発見）、および認知AIのためのMemory-Node Encapsulation（MNE）アーキテクチャの創作者です。

<!-- ここまで読んだ! -->
