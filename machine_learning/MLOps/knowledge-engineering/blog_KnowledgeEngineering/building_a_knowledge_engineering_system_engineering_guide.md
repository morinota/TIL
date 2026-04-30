refs: https://medium.com/@brian-curry-research/building-a-knowledge-engineering-system-an-engineering-guide-c720f88b9071


Building a Knowledge Engineering System: An Engineering Guide 知識工学システムの構築：エンジニアリングガイド

Brian James Curry — Apr 12, 2026  
ブライアン・ジェームズ・カリー — 2026年4月12日  

Architecture decisions, data pipelines, and production patterns for teams building their first knowledge layer.  
知識レイヤーを初めて構築するチームのためのアーキテクチャの決定、データパイプライン、および生産パターン。

## 1. The Gap Between Theory and Running Code 理論と実行コードのギャップ

Most writing about knowledge engineering describes what the system should do: classify content, extract entities, understand queries, connect facts in a graph. 
知識工学に関するほとんどの文書は、システムが何をすべきかを説明しています：コンテンツを分類し、エンティティを抽出し、クエリを理解し、グラフ内の事実を接続します。 
That's necessary, but it skips the hard part. 
それは必要ですが、難しい部分を省略しています。 
The hard part is the engineering: what runs where, what talks to what, what breaks first, and what you wish you'd done differently six months in. 
難しい部分はエンジニアリングです：何がどこで動作し、何が何と通信し、何が最初に壊れ、6か月後に何を異なって行っておけばよかったかです。

This article is the engineering companion. 
この記事はエンジニアリングの伴侶です。 
It assumes you already know why knowledge engineering matters — taxonomies, ontologies, entity linking, query understanding. 
これは、**あなたがすでに知識工学がなぜ重要であるか（分類法、オントロジー、エンティティリンク、クエリ理解）を知っていると仮定**しています。 
If you need that foundation, start with the conceptual overview. 
その基礎が必要な場合は、概念的な概要から始めてください。 
This piece is about how: the architecture, the data pipelines, the storage decisions, the editorial tooling, and the deployment patterns that make a knowledge engineering system actually work in production. 
この部分は、知識工学システムが実際に運用で機能するためのアーキテクチャ、データパイプライン、ストレージの決定、編集ツール、デプロイメントパターンについてです。

I've built these systems for companies ranging from $4B to $125B in revenue, and I've open-sourced the Python frameworks — MeaningFlow, Papilon, and PyCausalSim — that I use as building blocks. 
私は、40億ドルから1250億ドルの収益を上げる企業のためにこれらのシステムを構築してきました。また、私が構築ブロックとして使用するPythonフレームワーク（MeaningFlow、Papilon、PyCausalSim）をオープンソース化しました。 
This article walks through how those pieces fit together into a real system. 
この記事では、それらの要素がどのように組み合わさって実際のシステムになるかを説明します。

<!-- ここまで読んだ! -->

## 2. System Architecture: The Three Layers システムアーキテクチャ：三層

Every knowledge engineering system I've built decomposes into three layers. 
私が構築したすべての知識工学システムは、**三つの層**に分解されます。 
The boundaries between them are non-negotiable — cross them at your peril. 
それらの境界は交渉の余地がなく、越えると危険です。 

### 2.1. Layer 1: The Knowledge Store 層1：知識ストア

This is the source of truth. 
これは真実の源です。
It holds the taxonomy, the ontology schema, the entity records, the synonym lexicon, and the classification labels for every piece of content. 
それは、**分類法、オントロジースキーマ、エンティティレコード、同義語辞典、およびすべてのコンテンツの分類ラベルを保持**します。 
Everything downstream reads from here. 
**下流のすべてはここから読み取ります。**
Nothing writes to it except the editorial tooling and the batch enrichment pipelines. 
**編集ツールとバッチエンリッチメントパイプライン以外は、何も書き込みません。**

The first architectural decision is storage. 
最初のアーキテクチャの決定はストレージです。 

- **Graph database (Neo4j, Amazon Neptune, TigerGraph)** — Use this when entity relationships are the core of your product. 
- **グラフデータベース（Neo4j、Amazon Neptune、TigerGraph）** — エンティティの関係が製品の核心である場合に使用します。 
If your users search by "show me everything connected to X," traversal speed matters and a graph database earns its operational overhead. 
ユーザーが「Xに接続されているすべてを表示」と検索する場合、トラバーサル速度が重要であり、グラフデータベースはその運用コストを正当化します。 
Neo4j is the pragmatic default: Cypher is readable, the community edition is free, and the tooling ecosystem is mature. 
Neo4jは実用的なデフォルトです：Cypherは読みやすく、コミュニティエディションは無料で、ツールエコシステムは成熟しています。 

- **Relational database (PostgreSQL)** — Use this when the taxonomy and entity catalog are primarily lookup tables consumed by classifiers and search pipelines. 
- **リレーショナルデータベース（PostgreSQL）** — 分類器や検索パイプラインによって主に参照されるルックアップテーブルとして分類法とエンティティカタログを使用する場合に使用します。 
Postgres with JSONB columns handles semi-structured entity attributes cleanly, scales to tens of millions of entities without exotic infrastructure, and your team already knows SQL. 
JSONB列を持つPostgresは、半構造化エンティティ属性をクリーンに処理し、エキゾチックなインフラストラクチャなしで数千万のエンティティにスケールし、あなたのチームはすでにSQLを知っています。 
Most knowledge engineering systems start here and never need to leave. 
ほとんどの知識工学システムはここから始まり、決して離れる必要はありません。 

- **Hybrid** — In practice, many production systems use both. 
- **ハイブリッド** — 実際には、多くの生産システムが両方を使用します。 
Postgres as the canonical store for entities and taxonomy nodes, with a graph database materialized from it for relationship traversal queries. 
エンティティと分類法ノードの標準ストアとしてPostgresを使用し、関係トラバーサルクエリのためにそこからマテリアライズされたグラフデータベースを使用します。 
The graph is a read replica of the relational store, rebuilt nightly or on change events. 
グラフはリレーショナルストアの読み取りレプリカであり、毎晩または変更イベント時に再構築されます。 

My recommendation: start with Postgres. 
私の推奨は：Postgresから始めることです。 
Add Neo4j when (and only when) you have a production query that requires multi-hop traversal and your users are waiting. 
マルチホップトラバーサルを必要とする本番クエリがあり、ユーザーが待っているとき（そしてそのときだけ）にNeo4jを追加します。 

A minimal Postgres schema for the knowledge store: 
知識ストアのための最小限のPostgresスキーマ：

```sql
-- Taxonomy: the category hierarchy (分類体系: カテゴリ階層)
CREATE TABLE taxonomy_nodes (
    id          BIGSERIAL PRIMARY KEY,
    parent_id   BIGINT REFERENCES taxonomy_nodes(id),
    slug        TEXT NOT NULL UNIQUE,
    label       TEXT NOT NULL,
    description TEXT,
    depth       INT NOT NULL DEFAULT 0,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ON taxonomy_nodes (parent_id) WHERE is_active;
CREATE INDEX ON taxonomy_nodes (depth) WHERE is_active;

-- Ontology: entity types and their expected attributes (オントロジー: エンティティタイプとその期待される属性)
CREATE TABLE entity_types (
    id          BIGSERIAL PRIMARY KEY,
    slug        TEXT NOT NULL UNIQUE,
    label       TEXT NOT NULL,
    schema      JSONB NOT NULL DEFAULT '{}',  -- attribute definitions
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Entities: the actual things in the world (エンティティ: 世界の実際のもの, 固有表現)
CREATE TABLE entities (
    id          BIGSERIAL PRIMARY KEY,
    entity_type TEXT NOT NULL REFERENCES entity_types(slug),
    canonical_name TEXT NOT NULL,
    aliases     TEXT[] NOT NULL DEFAULT '{}',
    attributes  JSONB NOT NULL DEFAULT '{}',
    embedding   VECTOR(384),  -- pgvector for similarity search
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ON entities USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX ON entities (entity_type) WHERE is_active;
CREATE INDEX ON entities USING gin (aliases);

-- Entity relationships (エンティティ関係)
CREATE TABLE entity_relations (
    id          BIGSERIAL PRIMARY KEY,
    source_id   BIGINT NOT NULL REFERENCES entities(id),
    target_id   BIGINT NOT NULL REFERENCES entities(id),
    relation    TEXT NOT NULL,
    confidence  REAL NOT NULL DEFAULT 1.0,
    source_doc  TEXT,  -- provenance
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ON entity_relations (source_id, relation);
CREATE INDEX ON entity_relations (target_id, relation);

-- Synonyms: the living lexicon (同義語: 生きた辞書)
CREATE TABLE synonyms (
    id          BIGSERIAL PRIMARY KEY,
    source_term TEXT NOT NULL,
    target_term TEXT NOT NULL,
    relation    TEXT NOT NULL CHECK (relation IN ('exact','directional','misspelling','acronym')),
    locale      TEXT NOT NULL DEFAULT 'en-US',
    confidence  REAL NOT NULL DEFAULT 1.0,
    created_by  TEXT NOT NULL,
    rationale   TEXT,
    review_by   DATE,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ON synonyms (source_term) WHERE is_active;

-- Content classifications (コンテンツ分類)
CREATE TABLE content_classifications (
    id              BIGSERIAL PRIMARY KEY,
    content_id      TEXT NOT NULL,  -- external content identifier
    taxonomy_node   BIGINT NOT NULL REFERENCES taxonomy_nodes(id),
    classifier      TEXT NOT NULL,  -- which system assigned this
    confidence      REAL NOT NULL,
    is_override     BOOLEAN NOT NULL DEFAULT FALSE,  -- editorial override
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ON content_classifications (content_id);
CREATE INDEX ON content_classifications (taxonomy_node);

-- Content-entity links (コンテンツ-エンティティリンク)
CREATE TABLE content_entities (
    id          BIGSERIAL PRIMARY KEY,
    content_id  TEXT NOT NULL,
    entity_id   BIGINT NOT NULL REFERENCES entities(id),
    mention     TEXT NOT NULL,
    start_char  INT,
    end_char    INT,
    confidence  REAL NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX ON content_entities (content_id);
CREATE INDEX ON content_entities (entity_id);
``` 

Notice: pgvector for entity embeddings is built into the same database that holds the structured data. 
注意：エンティティ埋め込みのためのpgvectorは、構造化データを保持するのと同じデータベースに組み込まれています。 
No separate vector store needed for most knowledge engineering workloads. 
**ほとんどの知識工学のワークロードには、別のベクターストアは必要ありません。** (まあこれはposgreだからベクトル検索できるから同じDBに入れればいいよって話ね:thinking:)
One fewer system to maintain, one fewer synchronization problem to debug. 
維持すべきシステムが一つ減り、デバッグすべき同期の問題が一つ減ります。

<!-- ここまで読んだ! -->

### 2.2. Layer 2: The Processing Pipelines 層2：処理パイプライン

These are the batch and streaming jobs that enrich content. 
これらはコンテンツを強化するバッチおよびストリーミングジョブです。 
They read raw content, run classifiers and NER, link entities, and write results back to the knowledge store. 
生のコンテンツを読み取り、分類器とNERを実行し、エンティティをリンクし、結果を知識ストアに書き戻します。 
They never serve user requests directly. 
ユーザーリクエストに直接応答することはありません。 

The pipeline has four stages, always in this order: 
**パイプラインには常にこの順序で4つのステージ**があります：

- **Stage A: Ingest.** Pull raw content from the CMS, the search index, or the content API. 
  - **ステージA：取り込み。** CMS、検索インデックス、またはコンテンツAPIから**生のコンテンツを取得**します。 
    Normalize it: strip HTML, extract plain text, parse metadata. 
    それを正規化します：HTMLを削除し、プレーンテキストを抽出し、メタデータを解析します。 
    Write normalized documents to a staging table or object store. 
    正規化されたドキュメントをステージングテーブルまたはオブジェクトストアに書き込みます。 

- **Stage B: Classify.** Run the content through the classification cascade — rules, fine-tuned classifier, LLM fallback. 
  - **ステージB：分類。** コンテンツを分類カスケードに通します — ルール、微調整された分類器、LLMフォールバック。 
  Write classifications to `content_classifications` with the classifier name and confidence. 
  分類を分類器名と信頼度とともに`content_classifications`に書き込みます。 

- **Stage C: Extract.** Run NER over the content. 
  - **ステージC：抽出。** コンテンツに対してNERを実行します。 
  Disambiguate and link mentions to entities in the knowledge store. 
  言及を明確にし、知識ストア内のエンティティにリンクします。 
  Write to `content_entities`. 
  `content_entities`に書き込みます。 

- **Stage D: Reconcile.** Cross-check classifications against entity extractions. 
  - **ステージD：調整。** 分類をエンティティ抽出と照合します。 
  Flag inconsistencies (a document classified as "Sports" but with no sports entities detected). 
  不整合をフラグ付けします（「スポーツ」と分類されたドキュメントがスポーツエンティティを検出していない）。 
  Route flagged items to the editorial review queue. 
  **不整合フラグ付けされたアイテムを編集レビューキューにルーティング**します。 

The implementation can be as simple as a set of Python scripts orchestrated by cron, or as sophisticated as an Airflow DAG with retry logic and SLAs. 
**実装は、cronによってオーケストレーションされた一連のPythonスクリプトのように単純であったり、リトライロジックとSLAを持つAirflow DAGのように洗練**されていることがあります。
Start with the simplest thing. 
**最も単純なもので始めてください。** (Yes!!俺もそう思う!!:thinking:)
I've seen teams spend months building an elaborate orchestration layer for a pipeline that processes a few thousand documents per day — a cron job with error emails would have shipped in a week. 
数千のドキュメントを処理するパイプラインのために、チームが数ヶ月かけて複雑なオーケストレーションレイヤーを構築するのを見てきました — **エラー通知付きのcronジョブは1週間で出荷できる**でしょう。

A stripped-down pipeline orchestrator: 
簡素化されたパイプラインオーケストレーター：

```python
"""
knowledge_pipeline.py
Run daily: classify, extract, reconcile.
"""
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass

from db import get_session  # your SQLAlchemy or psycopg connection
from classifiers import RuleClassifier, EncoderClassifier, LLMClassifier
from extractors import NERExtractor, EntityLinker
from reconciler import cross_check_and_flag

log = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    lookback_hours: int = 24
    confidence_threshold: float = 0.6
    max_llm_calls: int = 5000  # budget guard


def run_pipeline(config: PipelineConfig):
    session = get_session()
    cutoff = datetime.utcnow() - timedelta(hours=config.lookback_hours)

    # Stage A: fetch new/updated content
    docs = session.execute(
        "SELECT id, body, metadata FROM content WHERE updated_at > :cutoff",
        {"cutoff": cutoff},
    ).fetchall()
    log.info(f"Pipeline processing {len(docs)} documents")

    # Stage B: classify
    rule_clf = RuleClassifier.load("rules_v3.yaml")
    encoder_clf = EncoderClassifier.load("deberta_taxonomy_v2.pt")
    llm_clf = LLMClassifier(budget=config.max_llm_calls)

    classifications = []
    for doc in docs:
        # Cascade: rules → encoder → LLM
        result = rule_clf.classify(doc.body)
        if result and result.confidence >= config.confidence_threshold:
            result.classifier = "rules_v3"
        else:
            result = encoder_clf.classify(doc.body)
            if result.confidence >= config.confidence_threshold:
                result.classifier = "deberta_v2"
            else:
                result = llm_clf.classify(doc.body)
                result.classifier = "llm_fallback"

        classifications.append((doc.id, result))
    bulk_insert_classifications(session, classifications)

    # Stage C: extract entities
    ner = NERExtractor(model="en_core_web_trf")
    linker = EntityLinker(session=session)
    for doc in docs:
        mentions = ner.extract(doc.body)
        linked = linker.link(mentions, context=doc.body)
        bulk_insert_entities(session, doc.id, linked)

    # Stage D: reconcile
    flagged = cross_check_and_flag(session, [d.id for d in docs])
    log.info(f"Flagged {len(flagged)} documents for editorial review")

    session.commit()
    log.info("Pipeline complete")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_pipeline(PipelineConfig())
```

Cost control matters. 
コスト管理は重要です。
The LLM classifier in the cascade is the expensive step. 
**カスケード内のLLM分類器は高コストなステップ**です。
The `max_llm_calls` budget guard prevents a spike in new content from blowing your API bill. 
**`max_llm_calls`の予算ガードは、新しいコンテンツの急増がAPI料金を膨らませるのを防ぎます**。
In practice, a well-tuned encoder classifier should handle 85-95% of documents with high confidence, leaving only the genuinely ambiguous cases for the LLM fallback. 
実際には、**適切に調整されたエンコーダ分類器が85-95%の文書を高い信頼度で処理し、LLMフォールバックのために本当にあいまいなケースだけを残すべき**です。
(あーつまり、安価で高速な内製モデルで大半を処理して、コストのかかるLLM呼び出しは自信ない場合のみに絞るアーキテクチャの話ね...!!:thinking:)

<!-- ここまで読んだ! -->

### 2.3. Layer 3: The Serving Layer

### 2.4. レイヤー3: サービングレイヤー
This is what user-facing systems actually call. 
これは**ユーザー向けシステムが実際に呼び出すもの**です。
It exposes the knowledge store through fast, cacheable APIs. 
それは、**高速でキャッシュ可能なAPIを通じて知識ストアを公開**します。
It never runs classifiers or NER — that's the pipeline layer's job. 
それは分類器やNERを実行することはなく、それはパイプラインレイヤーの仕事です。
It just looks things up. 
単に情報を検索するだけです。

Three APIs cover most use cases: 
**3つのAPIがほとんどのユースケースをカバー**します:
(entityを指定して紐づくコンテンツ一覧を返すAPIも必要そう...!!:thinking:)

- **Classify API** — Given a content ID, return its taxonomy classification. 
  - **Classify API** — コンテンツIDを指定すると、その分類を返します。
    This is a database lookup, not a model inference. 
    **これはデータベースの検索であり、モデル推論ではありません。** (推論はパイプラインレイヤーの仕事だからね!!:thinking:)
    Response time: single-digit milliseconds. 
    応答時間: 1桁ミリ秒。

- **Entity API** — Given a content ID, return the linked entities. 
  - **Entity API** — コンテンツIDを指定すると、リンクされたエンティティを返します。
  Or given an entity ID, return all content linked to it. 
  またはエンティティIDを指定すると、それにリンクされたすべてのコンテンツを返します。
  Again, database lookups with proper indexes. 
  再び、適切なインデックスを持つデータベースの検索です。

- **Query Understanding API** — Given a raw query string, return structured intent, entities, and filters. 
  - **Query Understanding API** — 生のクエリ文字列を指定すると、構造化された意図、エンティティ、およびフィルターを返します。(=これは検索クエリ用のAPIか...!:thinking:)
  This is the only serving-layer endpoint that runs inference (intent classifier + entity linker on queries), but the models are small and fast — a distilled BERT intent classifier runs in under 10ms on a CPU. 
  これは推論を実行する唯一のサービングレイヤーエンドポイント（意図分類器 + クエリのエンティティリンク）ですが、モデルは小さく高速です — 蒸留されたBERT意図分類器はCPU上で10ms未満で動作します。

```python
"""
Minimal FastAPI serving layer.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import get_session
from query_understanding import QueryParser

app = FastAPI(title="Knowledge API")
query_parser = QueryParser.load("query_model_v4")


class QueryResult(BaseModel):
    intent: str
    intent_confidence: float
    entities: list[dict]
    filters: list[dict]
    expanded_terms: list[str]


@app.get("/classify/{content_id}")
async def get_classification(content_id: str):
    session = get_session()
    result = session.execute(
        """SELECT tn.slug, tn.label, cc.confidence, cc.classifier
           FROM content_classifications cc
           JOIN taxonomy_nodes tn ON cc.taxonomy_node = tn.id
           WHERE cc.content_id = :cid
           ORDER BY cc.confidence DESC LIMIT 1""",
        {"cid": content_id},
    ).fetchone()
    if not result:
        raise HTTPException(404, "Content not classified")
    return {
        "content_id": content_id,
        "category": result.slug,
        "label": result.label,
        "confidence": result.confidence,
        "classifier": result.classifier,
    }


@app.get("/entities/{content_id}")
async def get_entities(content_id: str):
    session = get_session()
    rows = session.execute(
        """SELECT e.id, e.canonical_name, e.entity_type, ce.mention, ce.confidence
           FROM content_entities ce
           JOIN entities e ON ce.entity_id = e.id
           WHERE ce.content_id = :cid
           ORDER BY ce.confidence DESC""",
        {"cid": content_id},
    ).fetchall()
    return {"content_id": content_id, "entities": [dict(r._mapping) for r in rows]}


@app.post("/query/parse")
async def parse_query(query: str) -> QueryResult:
    result = query_parser.parse(query)
    return QueryResult(**result)
```

Caching. 
キャッシング。
Content classifications and entity links change only when the pipeline runs. 
**コンテンツの分類とエンティティリンクは、パイプラインが実行されるときのみ変更されます。**
Put a Redis or Memcached layer in front of the classify and entity endpoints. 
RedisまたはMemcachedレイヤーを分類およびエンティティエンドポイントの前に置きます。
Cache TTL = pipeline run interval. 
**キャッシュのTTL = パイプライン実行間隔。**
This handles traffic spikes without touching the database. 
これにより、データベースに触れることなくトラフィックスパイクを処理できます。

<!-- ここまで読んだ! -->

## 3. The Semantic Analysis Layer: MeaningFlow Integration セマンティック分析レイヤー: MeaningFlowの統合

Before any of the classification or entity work begins, you need to understand the shape of your content and your users' demand. 
**分類やエンティティ作業を始める前に、コンテンツの形状とユーザーの需要を理解する必要**があります。 
This is where MeaningFlow fits in the architecture — not as a runtime component, but as an analytical layer that feeds the design of everything else. 
ここでMeaningFlowがアーキテクチャに適合します — 実行時コンポーネントとしてではなく、他のすべての設計に情報を提供する分析レイヤーとしてです。

Run MeaningFlow on two corpora: your content inventory and your query logs. 
**MeaningFlowを2つのコーパスで実行します: あなたのコンテンツインベントリとクエリログ**です。 
The output is a pair of semantic graphs — one representing what you have, one representing what users want. 
**出力は一対のセマンティックグラフです — 一つはあなたが持っているものを表し、もう一つはユーザーが望んでいるものを表します。** 
The gap between them drives three critical design decisions: 
それらの間のギャップは、3つの重要な設計決定を促します:

- **Taxonomy structure.** 
  - **分類構造。** 
  The clusters in the demand graph that have no corresponding supply clusters are the categories your taxonomy is missing. 
  需要グラフの中で対応する供給クラスタがないクラスタは、あなたの分類が欠けているカテゴリです。 
  Don't design taxonomy branches in a conference room. 
  会議室で分類の枝を設計しないでください。 
  Design them from the data. 
  データから設計してください。

- **Entity type priorities.** 
  - **エンティティタイプの優先順位。** 
  The entity types that appear most frequently in high-volume query clusters are the types you should extract first. 
  高ボリュームのクエリクラスタに最も頻繁に現れるエンティティタイプは、最初に抽出すべきタイプです。 
  If "Person" entities dominate your top clusters but "Organization" entities are sparse, build the Person NER pipeline first. 
  「Person」エンティティが上位クラスタを支配しているが「Organization」エンティティがまばらな場合は、まずPerson NERパイプラインを構築してください。

- **Synonym seeds.** 
  - **同義語の種。** 
  Terms that co-occur in the same query cluster but use different surface forms are synonym candidates. 
  同じクエリクラスタに共起するが異なる表面形を使用する用語は同義語候補です。 
  MeaningFlow's graph structure makes these pairs visible without manual analysis. 
  MeaningFlowのグラフ構造は、手動分析なしでこれらのペアを可視化します。 

  The MeaningFlow analysis runs once during system design, then monthly as a monitoring check. 
  MeaningFlow分析はシステム設計中に一度実行され、その後は月次の監視チェックとして実行されます。 
  It's not in the hot path. 
  それはホットパスにはありません。 
  It's in the strategy path. 
  それは戦略パスにあります。

```python
"""
Quarterly semantic health check.
Compare current content coverage against current demand.
"""
from meaningflow import SemanticGraph
import pandas as pd
import json


def semantic_health_check(
    content_path: str,
    queries_path: str,
    previous_report_path: str = None,
) -> dict:
    content = pd.read_parquet(content_path)["title"].tolist()
    queries = pd.read_parquet(queries_path)["query"].tolist()

    supply = SemanticGraph(texts=content, embedder="all-MiniLM-L6-v2", min_cluster_size=30)
    supply.fit()
    demand = SemanticGraph(texts=queries, embedder="all-MiniLM-L6-v2", min_cluster_size=30)
    demand.fit()

    gaps = demand.coverage_gaps(reference=supply, similarity_threshold=0.55)

    report = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "supply_clusters": supply.n_clusters,
        "demand_clusters": demand.n_clusters,
        "gap_clusters": len(gaps),
        "top_gaps": [
            {"terms": g.top_terms[:5], "volume": g.volume, "size": g.size}
            for g in gaps[:20]
        ],
    }

    # Drift detection against previous report
    if previous_report_path:
        with open(previous_report_path) as f:
            prev = json.load(f)
        report["gap_count_change"] = len(gaps) - prev.get("gap_clusters", 0)
        report["demand_cluster_change"] = demand.n_clusters - prev.get("demand_clusters", 0)

    return report
```  

<!-- ここまで読んだ! -->

## 4. Building the Classification Pipeline in Detail 分類パイプラインの詳細構築

The classification cascade — rules, encoder, LLM — deserves a deeper walkthrough because it's the component that breaks most often and costs the most to debug.  
分類カスケード — ルール、エンコーダ、LLM — は、**最も頻繁に壊れ、デバッグに最もコストがかかるコンポーネントであるため、より深く掘り下げる価値があります。**

### 4.1. The Rule Layer ルールレイヤー

Rules are YAML files that editors can update without a deploy:  
ルールは、エディタがデプロイなしで更新できるYAMLファイルです：

```yaml
# classification_rules_v3.yaml
rules:
  - name: "breaking_news_override"
    priority: 1
    conditions:
      - field: "metadata.content_type"
        operator: "equals"
        value: "breaking"
    action:
      category: "news/breaking"
      confidence: 1.0
  - name: "publisher_vertical"
    priority: 2
    conditions:
      - field: "metadata.publisher"
        operator: "in"
        value: ["espn.com", "bleacherreport.com", "theathletic.com"]
    action:
      category: "sports"
      confidence: 0.95
  - name: "keyword_finance"
    priority: 10
    conditions:
      - field: "body"
        operator: "contains_any"
        value: ["stock market", "S&P 500", "Federal Reserve", "interest rate"]
      - field: "body"
        operator: "not_contains_any"
        value: ["fantasy", "betting", "odds"]
    action:
      category: "finance/markets"
      confidence: 0.85
```  
The rule engine evaluates in priority order and returns the first match. Lower priority number = higher precedence. The `not_contains_any` guard in the finance rule prevents sports betting content from being misclassified — a real production bug I've seen at three different companies.  
ルールエンジンは優先順位の順に評価し、最初の一致を返します。優先度の低い番号 = 高い優先度。ファイナンスルールの`not_contains_any`ガードは、スポーツベッティングコンテンツが誤分類されるのを防ぎます — これは私が3つの異なる会社で見た実際のプロダクションバグです。

### 4.2. The Encoder Layer エンコーダレイヤー

A fine-tuned DeBERTa-v3-small classifier trained on your labeled data. The training loop is standard, but two details matter for production:  
ラベル付きデータで訓練された微調整されたDeBERTa-v3-small分類器です。トレーニングループは標準的ですが、プロダクションにおいて重要な2つの詳細があります：

- **Multi-label support.** Content can belong to multiple categories. A movie review is both "entertainment/film" and "culture/criticism." Train with binary cross-entropy per class, not softmax. At inference time, return all classes above a confidence threshold rather than just the argmax.  
- **マルチラベルサポート。** コンテンツは複数のカテゴリに属することができます。映画レビューは「エンターテインメント/映画」と「文化/批評」の両方に該当します。クラスごとにバイナリー交差エントロピーで訓練し、ソフトマックスではありません。推論時には、argmaxだけでなく、信頼度の閾値を超えるすべてのクラスを返します。

- **Calibration.** Neural classifiers are notoriously overconfident. The raw softmax probabilities don't mean what you think they mean. Calibrate with temperature scaling on a held-out set so that a confidence of 0.8 actually means the classifier is right 80% of the time. Without calibration, your confidence thresholds are meaningless.  
- **キャリブレーション。** ニューラル分類器は過信しがちです。生のソフトマックス確率は、あなたが思っている意味とは異なります。保持されたセットで温度スケーリングを使用してキャリブレーションを行い、信頼度0.8が実際に分類器が80%の確率で正しいことを意味するようにします。キャリブレーションがなければ、あなたの信頼度の閾値は無意味です。

```python
"""
Temperature scaling for classifier calibration.
Fit on a held-out validation set after training.
"""
import numpy as np
from scipy.optimize import minimize_scalar
from sklearn.metrics import log_loss


def find_temperature(logits: np.ndarray, labels: np.ndarray) -> float:
    """Find the temperature that minimizes NLL on the validation set."""
    def nll_at_temp(T):
        scaled = logits / T
        probs = np.exp(scaled) / np.exp(scaled).sum(axis=1, keepdims=True)
        return log_loss(labels, probs)

    result = minimize_scalar(nll_at_temp, bounds=(0.1, 10.0), method="bounded")
    return result.x


def calibrated_predict(logits: np.ndarray, temperature: float) -> np.ndarray:
    """Apply temperature scaling to produce calibrated probabilities."""
    scaled = logits / temperature
    return np.exp(scaled) / np.exp(scaled).sum(axis=1, keepdims=True)
```  
### 4.3. The LLM Fallback LLMフォールバック

For the remaining 5–15% of documents where the encoder is uncertain, send the text to an LLM with the taxonomy embedded in the prompt. This is the same pattern I described in the previous article, but with a production-critical addition: caching.  
**エンコーダが不確かな残りの5〜15%のドキュメントについては、テキストをLLMに送信し、プロンプトに組み込まれた分類法を使用**します。これは前回の記事で説明したのと同じパターンですが、**プロダクションにおいて重要な追加点があります：キャッシング。**

Many documents that confuse the encoder are near-duplicates of each other — syndicated content, press releases picked up by multiple outlets, templated product pages. Hash the input text, check the cache before calling the API. A simple content-hash → classification cache cuts LLM costs by 30–50% in most content pipelines.  
**エンコーダ(=LLMの前のステップ)を混乱させる多くのドキュメントは、ほぼ重複している** — シンジケートコンテンツ、複数のメディアに取り上げられたプレスリリース、テンプレート化された製品ページです。入力テキストをハッシュ化し、APIを呼び出す前にキャッシュを確認します。**シンプルなコンテンツハッシュ → 分類キャッシュは、ほとんどのコンテンツパイプラインでLLMコストを30〜50%削減**します。

```python
import hashlib
import json
from functools import lru_cache


class LLMClassifier:
    def __init__(self, budget: int = 5000):
        self.budget = budget
        self.calls_made = 0
        self._cache = {}  # In production, use Redis

    def _content_hash(self, text: str) -> str:
        # Hash first 2000 chars — enough for classification, avoids
        # hashing entire long-form articles
        return hashlib.sha256(text[:2000].encode()).hexdigest()

    def classify(self, text: str) -> dict:
        h = self._content_hash(text)
        if h in self._cache:
            return self._cache[h]
        if self.calls_made >= self.budget:
            return {
                "category": "uncategorized",
                "confidence": 0.0,
                "classifier": "llm_budget_exhausted",
            }
        result = self._call_llm(text)
        self.calls_made += 1
        self._cache[h] = result
        return result

    def _call_llm(self, text: str) -> dict:
        # Your LLM API call here — OpenAI, local model, etc.
        # Returns {"category": "...", "confidence": 0.0-1.0}
        ...
```  

<!-- ここまで読んだ! -->

## 5. Building the Entity Pipeline エンティティパイプラインの構築

Entity extraction and linking is the second major pipeline, and it has its own architectural concerns distinct from classification.  
**エンティティ抽出とリンクは、第二の主要なパイプラインであり、分類とは異なる独自のアーキテクチャ上の懸念**があります。

### 5.1. NER Model Selection NERモデルの選択 (NER=Named Entity Recognition 固有表現抽出)

For most content domains, spaCy's transformer-based models (`en_core_web_trf`) handle the standard entity types — Person, Organization, Location, Date — well enough to start.  
**ほとんどのコンテンツドメインにおいて、spaCyのトランスフォーマーベースのモデル（`en_core_web_trf`）は、標準的なエンティティタイプ（人物、組織、場所、日付）を十分に処理します。**  
Where you'll need custom NER is domain-specific entity types: product names, movie titles, song titles, medical terms, financial instruments.  
カスタムNERが必要となるのは、ドメイン特有のエンティティタイプ（製品名、映画タイトル、曲名、医療用語、金融商品）です。

Two approaches to custom NER:  
カスタムNERには2つのアプローチがあります：

- **Few-shot with an LLM.** Same cost-control patterns as the classification fallback.  
  **LLMを用いたFew-shot。** 分類のフォールバックと同様のコスト管理パターンです。  
  Send a chunk of text with a prompt asking for entities of your custom types.  
  カスタムタイプのエンティティを求めるプロンプトを含むテキストの塊を送信します。  
  Works well for low-volume, high-value content. Not viable for millions of documents per day.  
  低ボリュームで高価値のコンテンツにはうまく機能しますが、1日に数百万の文書には適していません。

- **Fine-tuned span classifier.** Train a small model (SpanBERT, DeBERTa) on a few thousand annotated examples.  
  **ファインチューニングされたスパン分類器。** 数千の注釈付き例で小さなモデル（SpanBERT、DeBERTa）をトレーニングします。  
  This is the long-term answer. The annotation burden is the bottleneck — use the LLM approach to bootstrap the training set, then have editors correct the results.  
  これは長期的な解決策です。注釈の負担がボトルネックとなります。LLMアプローチを使用してトレーニングセットをブートストラップし、その後、編集者が結果を修正します。

<!-- ここまで読んだ! -->

### 5.2. Entity Disambiguation at Scale 大規模なエンティティの曖昧さ解消

The toy version of disambiguation — embed the mention context, embed each candidate, take the nearest — works for a few thousand entities.  
**曖昧さ解消のトイバージョン（言及コンテキストを埋め込み、各候補を埋め込み、最も近いものを取る）は、数千のエンティティに対して機能します。**
At scale (millions of entities in the knowledge store), you need approximate nearest neighbor search.  
スケール（ナレッジストアに数百万のエンティティがある場合）では、近似最近傍検索が必要です。

The architecture: store entity embeddings in pgvector (already in your schema above).  
アーキテクチャ：pgvectorにエンティティの埋め込みを保存します（すでに上記のスキーマにあります）。  
At disambiguation time, embed the mention-in-context, query pgvector for the top-k nearest entity embeddings, then re-rank with a lightweight cross-encoder or heuristic features (entity type match, popularity prior, session context).  
曖昧さ解消の際には、コンテキスト内の言及を埋め込み、pgvectorに対して最も近いk個のエンティティ埋め込みをクエリし、その後、軽量のクロスエンコーダーまたはヒューリスティック特徴（エンティティタイプの一致、人気の事前情報、セッションコンテキスト）で再ランクします。

```python
"""
Scalable entity disambiguation with pgvector + re-ranking.
"""
from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np


class EntityDisambiguator:
    def __init__(self, session, embedder_name="all-MiniLM-L6-v2"):
        self.session = session
        self.embedder = SentenceTransformer(embedder_name)
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def disambiguate(
        self,
        mention: str,
        context: str,
        entity_type: str,
        top_k: int = 10,
    ) -> dict:
        # Embed the mention in context
        query_text = f"{mention}: {context[:300]}"
        query_emb = self.embedder.encode(query_text).tolist()

        # ANN search in pgvector
        candidates = self.session.execute(
            """SELECT id, canonical_name, attributes
               FROM entities
               WHERE entity_type = :etype AND is_active
               ORDER BY embedding <=> :emb::vector
               LIMIT :k""",
            {"etype": entity_type, "emb": str(query_emb), "k": top_k},
        ).fetchall()

        if not candidates:
            return {"entity_id": None, "confidence": 0.0}

        # Re-rank with cross-encoder
        pairs = [(query_text, c.canonical_name) for c in candidates]
        scores = self.reranker.predict(pairs)
        best_idx = int(np.argmax(scores))
        best = candidates[best_idx]

        return {
            "entity_id": best.id,
            "canonical_name": best.canonical_name,
            "confidence": float(scores[best_idx]),
        }
```

<!-- ここまで読んだ! -->

### 5.3. Session-Aware Disambiguation セッション対応の曖昧さ解消

In the previous article, I described a session memory pattern based on my Memory-Node Encapsulation (MNE) research.  
前回の記事では、私のMemory-Node Encapsulation（MNE）研究に基づいたセッションメモリパターンについて説明しました。  
In the system architecture, the session memory lives in Redis with a TTL equal to the session timeout.  
システムアーキテクチャでは、セッションメモリはRedisにあり、TTLはセッションタイムアウトと等しくなっています。  
The query understanding API reads it, and the entity disambiguation step uses it as a prior:  
クエリ理解APIがそれを読み取り、エンティティの曖昧さ解消ステップがそれを事前情報として使用します：

```python
import redis
import json
from time import time


class SessionStore:
    def __init__(self, redis_url: str, ttl_seconds: int = 1800):
        self.r = redis.from_url(redis_url)
        self.ttl = ttl_seconds

    def record_entity(self, session_id: str, entity_id: int):
        key = f"session:{session_id}:entities"
        self.r.zadd(key, {str(entity_id): time()})
        self.r.expire(key, self.ttl)

    def get_recent_entities(self, session_id: str, n: int = 10) -> list[int]:
        key = f"session:{session_id}:entities"
        # Most recent first
        results = self.r.zrevrange(key, 0, n - 1)
        return [int(eid) for eid in results]

    def entity_recency_boost(
        self,
        session_id: str,
        entity_id: int,
        half_life: float = 300.0,
    ) -> float:
        key = f"session:{session_id}:entities"
        ts = self.r.zscore(key, str(entity_id))
        if ts is None:
            return 0.0
        age = time() - ts
        return 0.5 ** (age / half_life)
```

The disambiguation step adds `entity_recency_boost` to the cross-encoder score before picking the best candidate.  
曖昧さ解消のステップでは、最良の候補を選ぶ前に`entity_recency_boost`をクロスエンコーダースコアに追加します。  
Users who just interacted with "Apple Inc." get a disambiguated toward the company on their next query — without any explicit signal from the user.  
「Apple Inc.」と最近やり取りしたユーザーは、次のクエリでその会社に向けた曖昧さ解消を受けます — ユーザーからの明示的な信号なしに。

<!-- ここまで読んだ! -->

## 6. Editorial Tooling: The Most Underinvested Layer 編集ツール: 最も投資が不足している層

In every knowledge engineering system I've seen fail, the failure mode is the same: the ML pipelines work, the knowledge store is correctly designed, but editors can't actually use the system because the tooling is terrible.  
私が見た失敗したすべての知識工学システムでは、**失敗のパターンは同じです: MLパイプラインは機能し、知識ストアは正しく設計されていますが、編集者はツールがひどいために実際にシステムを使用できません。**
They're editing YAML in a text editor, reviewing classifications in a spreadsheet, and managing the synonym lexicon through Jira tickets.  
彼らはテキストエディタでYAMLを編集し、スプレッドシートで分類をレビューし、Jiraチケットを通じて同義語辞典を管理しています。
Build the editorial UI before you scale the pipelines.  
**パイプラインをスケールする前に、編集用UIを構築してください。**
Three screens cover the core workflows:  
3つの画面がコアワークフローをカバーします:

### 6.1. Screen 1: Classification Review Queue 画面1: 分類レビューキュー

A paginated list of documents flagged by the reconciliation step — low-confidence classifications, classifier-graph disagreements, documents in the "uncategorized" bucket.  
調整ステップでフラグが付けられた文書のページネーションされたリスト — 低信頼度の分類、分類器グラフの不一致、「未分類」バケットにある文書。

For each document:  
各文書について:

- The title and first 200 characters of body text.  
  - タイトルと本文の最初の200文字。

- The top three candidate classifications with confidence scores.  
  - 信頼度スコアを持つ上位3つの候補分類。

- One-click buttons to accept a candidate, override with a different category, or skip.  
  - 候補を受け入れる、異なるカテゴリで上書きする、またはスキップするためのワンクリックボタン。

- A "needs new category" flag that routes to the taxonomy editor.  
  - タクソノミーエディタにルーティングされる「新しいカテゴリが必要」フラグ。

The key metric: time per review decision. Measure it.  
**重要な指標: レビュー決定あたりの時間。**測定してください。
If editors are averaging more than 15 seconds per document, the UI is making them work too hard.  
**もし編集者が文書あたり平均15秒以上かかっているなら、UIは彼らに過剰な労力を強いています。**
Common causes: too many clicks, category picker is hard to navigate, no keyboard shortcuts.  
一般的な原因: クリックが多すぎる、カテゴリピッカーがナビゲートしにくい、キーボードショートカットがない。

<!-- ここまで読んだ! -->

### 6.2. Screen 2: Taxonomy Editor 画面2: タクソノミーエディタ

A tree view of the taxonomy with drag-and-drop reordering, inline rename, add child, merge branches, and deprecate (soft delete with a redirect target).  
ドラッグアンドドロップによる並べ替え、インラインリネーム、子の追加、ブランチのマージ、非推奨（リダイレクトターゲットを持つソフト削除）を備えたタクソノミーのツリービュー。
Every change writes an audit log entry.  
すべての変更は監査ログエントリを書き込みます。
Every change triggers a downstream re-classification of affected content — but queued as a batch job, not inline.
すべての変更は影響を受けたコンテンツの下流再分類をトリガーしますが、インラインではなくバッチジョブとしてキューに入れられます。

<!-- ここまで読んだ! -->

### 6.4. Screen 3: Synonym Manager 画面3: 同義語マネージャー

A searchable table of the synonym lexicon.  
同義語辞典の検索可能なテーブル。
Editors can add entries, deactivate entries, and see usage stats (how many queries matched this synonym in the last 30 days).  
編集者はエントリを追加したり、エントリを無効にしたり、使用統計（過去30日間にこの同義語に一致したクエリの数）を確認できます。
An "auto-suggest" tab shows synonym candidates proposed by the MeaningFlow clustering — editors approve or reject with one click.  
「自動提案」タブは、MeaningFlowクラスタリングによって提案された同義語候補を表示します — 編集者はワンクリックで承認または拒否します。

---

Build these as a simple internal web app.  
**これらをシンプルな内部ウェブアプリとして構築してください。**
React + your existing API layer.  
React + 既存のAPIレイヤー。
Do not build them as a Slack bot, a Notion integration, or a Google Sheet.  Those approaches always start "simple" and end in unmaintainable chaos.
**Slackボット、Notion統合、またはGoogleシートとして構築しないでください。これらのアプローチは常に「シンプル」から始まり、維持管理が不可能な混沌に終わります。** (わかる気がする...!!:thinking:)

<!-- ここまで読んだ! -->

## 7. Monitoring and Observability 監視と可観測性

A knowledge engineering system in production needs three monitoring dimensions.  
生産中の知識工学システムには、**3つの監視次元**が必要です。

### 7.1. Pipeline Health パイプラインの健康

Standard data pipeline monitoring: did the pipeline run? How long did each stage take? How many documents were processed? How many failed? Alert on failures and on throughput drops (which often indicate an upstream data issue rather than a pipeline bug).  
標準的なデータパイプラインの監視：パイプラインは実行されましたか？各ステージはどのくらいの時間がかかりましたか？何件のドキュメントが処理されましたか？何件が失敗しましたか？失敗やスループットの低下（これはしばしばパイプラインのバグではなく、上流のデータ問題を示す）にアラートを出します。

### 7.2. Classification Quality 分類の質

Track the distribution of classifier confidence over time. A sudden shift — average confidence dropping from 0.82 to 0.71 — means either the content mix has changed or the model is stale. Either way, investigate.
分類器の信頼度の分布を時間とともに追跡します。突然の変化 — 平均信頼度が0.82から0.71に低下する — は、コンテンツの構成が変わったか、モデルが古くなったことを意味します。いずれにせよ、調査が必要です。

Track the rate of "uncategorized" documents. This is your exhaust valve. A rising uncategorized rate means your taxonomy or your classifier isn't keeping up with the content.  
**「未分類」のドキュメントの割合を追跡**します。これはあなたの排気弁です。未分類の割合が上昇している場合、あなたの分類体系または分類器がコンテンツに追いついていないことを意味します。(これはまさにT-LEAFのカバレッジってやつだ...!!:thinking:)

Track editorial override rate. If editors are overriding more than 10% of machine classifications, the classifier needs retraining. If they're overriding less than 2%, you might be able to reduce the review queue and free up editorial time.  
**編集者のオーバーライド率**を追跡します。編集者が機械による分類の10％以上をオーバーライドしている場合、分類器の再訓練が必要です。2％未満であれば、レビューキューを減らし、編集時間を確保できるかもしれません。
(これはhuman-in-the-loop的な感じのmetricsだ...!! Airbnbの事例でも監視してそう...!:thinking:)

<!-- ここまで読んだ! -->

### 7.3. Drift Detection with Papilon Papilonによるドリフト検出

For deeper attribution — understanding why quality shifted and which changes drove which outcomes — I use Papilon to build causal models over the pipeline's operational data.  
より深い帰属のために — なぜ品質が変化したのか、どの変更がどの結果を引き起こしたのかを理解するために — 私はPapilonを使用してパイプラインの運用データに基づく因果モデルを構築します。

```python
"""
Monthly causal attribution: what drove classification quality changes?
"""
import papilon as pp


def monthly_attribution(metrics_path: str):
    df = pp.load_panel(metrics_path)

    dag = pp.discover_causal_structure(
        df,
        treatments=[
            "taxonomy_version",
            "encoder_version",
            "rule_update_count",
            "content_volume_change",
        ],
        outcome="editorial_override_rate",
        confounders=["month", "content_mix_entropy"],
    )

    for treatment in ["taxonomy_version", "encoder_version", "rule_update_count"]:
        effect = pp.estimate_effect(
            df,
            treatment=treatment,
            outcome="editorial_override_rate",
            dag=dag,
        )
        print(
            f"{treatment}: {effect.point:.4f} "
            f"(95% CI {effect.ci_low:.4f}–{effect.ci_high:.4f})"
        )
```  
This tells you things like: "The taxonomy expansion in March reduced the editorial override rate by 3.2 percentage points, independent of the classifier retrain that shipped the same week." That's the evidence you need to justify continued investment in the knowledge engineering program.  
これは、「3月の分類体系の拡張により、同じ週に出荷された分類器の再訓練とは無関係に、編集者のオーバーライド率が3.2ポイント減少した」といったことを教えてくれます。これは、知識工学プログラムへの継続的な投資を正当化するために必要な証拠です。

<!-- ここまで読んだ! -->

## 8. Deployment Topology 展開トポロジー

For a team of 2–5 engineers supporting a medium-scale content platform (millions of documents, tens of millions of queries per month), the deployment looks like this:  
中規模のコンテンツプラットフォーム（数百万の文書、月間数千万のクエリ）をサポートする2～5人のエンジニアのチームの場合、展開は次のようになります：

- **Knowledge Store:** Single Postgres instance with pgvector extension.  
  - **ナレッジストア:** pgvector拡張を持つ単一のPostgresインスタンス。  
  If you outgrow this, shard by entity type before reaching for a distributed database.  
  これを超える場合は、分散データベースに手を伸ばす前に、エンティティタイプごとにシャーディングしてください。

- **Pipeline:** Python scripts running on a schedule (cron or Airflow).  
  - **パイプライン:** スケジュール（cronまたはAirflow）で実行されるPythonスクリプト。  
  One worker for classification, one for entity extraction.  
  分類用のワーカー1つ、エンティティ抽出用のワーカー1つ。  
  Run on spot instances — pipeline jobs are idempotent and restartable.  
  スポットインスタンスで実行します — **パイプラインジョブは冪等性があり、再起動可能**です。

- **Serving Layer:** FastAPI behind a load balancer, with Redis caching.  
  - **サービングレイヤー:** ロードバランサーの背後にあるFastAPI、Redisキャッシング付き。  
  Two small instances handle most traffic.  
  **2つの小さなインスタンスがほとんどのトラフィックを処理**します。(上のワーカーとは別の常駐インスタンス!:thinking:)
  Scale horizontally if needed — the API is stateless.  
  必要に応じて水平スケーリングします — APIはステートレスです。

- **Editorial UI:** React SPA served from a CDN, talking to the same FastAPI backend.  
  - **エディトリアルUI:** CDNから提供されるReact SPAで、同じFastAPIバックエンドと通信します。  
  Internal-only, behind your VPN or auth provider.  
  内部専用で、VPNまたは認証プロバイダーの背後にあります。

- **MeaningFlow Analysis:** Jupyter notebooks or scheduled Python scripts running monthly.  
  - **MeaningFlow分析:** 月次で実行されるJupyterノートブックまたはスケジュールされたPythonスクリプト。  
  Not a production service — an analytical tool.  
  これは本番サービスではなく、分析ツールです。  
  Results feed into the editorial process, not into the serving layer.  
  結果はサービングレイヤーではなく、エディトリアルプロセスにフィードされます。

- **Papilon Attribution:** Monthly batch job.  
  - **Papilonアトリビューション:** 月次バッチジョブ。  
  Reads operational metrics from the pipeline's log tables, outputs a report.  
  **パイプラインのログテーブルから運用メトリクスを読み取り、レポートを出力**します。  
  Same deployment pattern as MeaningFlow — analytical, not serving.  
  MeaningFlowと同じ展開パターン — 分析用であり、サービング用ではありません。  

Total infrastructure cost for this setup: $500–2,000/month depending on content volume and LLM API usage.  
このセットアップの総インフラコスト：コンテンツのボリュームとLLM APIの使用に応じて、$500–2,000/月。  
The LLM fallback classifier is the variable cost — everything else is fixed and modest.  
LLMフォールバック分類器は変動コストであり、他のすべては固定で控えめです。


<!-- ここまで読んだ! -->


## 9. What Breaks First 何が最初に壊れるのか

In the interest of saving you six months of debugging, here are the failure modes I've seen repeatedly:  
6ヶ月のデバッグを節約するために、私が繰り返し見てきた失敗モードを以下に示します：

- **Taxonomy drift.** The world changes faster than the taxonomy. New categories emerge, old categories become irrelevant, and the classifier keeps assigning content to stale branches.  
  - **分類体系の漂流。** 世界は分類体系よりも早く変化します。新しいカテゴリが出現し、古いカテゴリは無関係になり、分類器は古い枝にコンテンツを割り当て続けます。(わかる...!!:thinking:)  
  Fix: quarterly MeaningFlow health checks with mandatory taxonomy review.  
  修正：**四半期ごとのMeaningFlow健康チェックと必須の分類体系レビュー。**

- **Entity proliferation.** Without deduplication, the entity store fills with near-duplicate records — "Kendrick Lamar," "kendrick lamar," "K. Lamar," "Kendrick Lamar Duckworth." Your entity linker starts splitting mentions across duplicates, degrading every downstream system.  
  - **エンティティの増殖。** **重複排除がないと、エンティティストアはほぼ重複したレコードで埋まります** — "Kendrick Lamar," "kendrick lamar," "K. Lamar," "Kendrick Lamar Duckworth." エンティティリンクは重複間で言及を分割し始め、すべての下流システムを劣化させます。  
  Fix: a deduplication pipeline that runs weekly, using embedding similarity plus edit distance to propose merge candidates for editorial review.  
  修正：週次で実行される重複排除パイプラインを使用し、埋め込みの類似性と編集距離を用いて編集レビューのための**マージ候補を提案**します。

- **Synonym collisions.** An editor adds a synonym that creates an unintended mapping — "apple" → "fruit" breaks searches for Apple Inc.  
  - **同義語の衝突。** 編集者が意図しないマッピングを作成する同義語を追加します — "apple" → "fruit" はApple Inc.の検索を壊します。  
  Fix: every synonym addition triggers an impact assessment showing which existing queries and classifications would be affected. Display this in the editorial UI before the editor clicks "save."  
  修正：すべての同義語の追加は、影響を受ける既存のクエリと分類を示す影響評価を引き起こします。**編集者が「保存」をクリックする前に、これを編集UIに表示**します。

- **LLM cost spikes.** A content migration or a new publisher integration suddenly doubles the volume of documents hitting the LLM fallback. The budget guard catches this eventually, but not before you've burned through a week's API budget in a day.  
  - **LLMコストの急増。** コンテンツ移行や新しい出版社の統合により、LLMフォールバックにヒットする文書の量が突然倍増します。予算の監視は最終的にこれをキャッチしますが、1日のうちに1週間のAPI予算を使い果たす前には気づきません。  
  Fix: rate limiting per-source, with alerts when any single source exceeds its expected volume by more than 2x.  
  修正：ソースごとのレート制限を設け、任意の単一ソースが予想されるボリュームを2倍以上超えた場合にアラートを出します。

- **The cold start problem.** When you launch a new taxonomy branch, you have no training data for it. The encoder classifier can't classify content into a category it's never seen. The LLM fallback works but is expensive at the volume of a new branch.  
  - **コールドスタート問題。** 新しい分類体系のブランチを立ち上げると、そのためのトレーニングデータがありません。エンコーダ分類器は、見たことのないカテゴリにコンテンツを分類できません。LLMフォールバックは機能しますが、新しいブランチのボリュームでは高コストです。  
  Fix: use the LLM to generate the initial labeled dataset (500–1,000 examples), fine-tune the encoder, then shift to the standard cascade. This is a one-time cost per new branch.  
  修正：LLMを使用して初期のラベル付きデータセット（500〜1,000例）を生成し、エンコーダを微調整した後、標準のカスケードに移行します。これは新しいブランチごとの一度限りのコストです。

<!-- ここまで読んだ! -->

## 10. The Build Sequence 構築手順

If I were starting a knowledge engineering system from scratch tomorrow, this is the order I'd build in:  
もし私が明日、ゼロから知識工学システムを始めるとしたら、以下の順序で構築します：

- **Week 1–2:** Postgres schema. Seed taxonomy (3–5 top-level categories from editorial judgment). MeaningFlow analysis to validate and expand the seed.  
  - **第1–2週:** Postgresスキーマ。シード分類（編集判断による3〜5のトップレベルカテゴリ）。シードを検証し拡張するためのMeaningFlow分析。

- **Week 3–4:** Rule classifier (YAML-based). Run it over the full content corpus. Measure coverage — how much content do rules handle alone?  
  - **第3–4週:** ルール分類器（YAMLベース）。全コンテンツコーパスに対して実行します。カバレッジを測定します — ルールが単独で処理するコンテンツはどのくらいですか？

- **Week 5–6:** LLM fallback classifier for everything rules miss. Use the results as training data. Editorial review of a random sample to establish baseline quality.  
  - **第5–6週:** ルールが見逃したすべてのためのLLMフォールバック分類器。結果をトレーニングデータとして使用します。ベースライン品質を確立するためにランダムサンプルの編集レビューを行います。

- **Week 7–8:** Fine-tune encoder classifier on the LLM-generated + editor-corrected labels. Implement the full cascade. Measure the encoder's coverage at your confidence threshold.  
  - **第7–8週:** LLM生成および編集者修正ラベルに基づいてエンコーダ分類器をファインチューニングします。完全なカスケードを実装します。信頼度閾値でのエンコーダのカバレッジを測定します。

- **Week 9–10:** NER pipeline. Entity store. Basic disambiguation using pgvector. Start with the top two entity types by query volume.  
  - **第9–10週:** NERパイプライン。エンティティストア。pgvectorを使用した基本的な曖昧性解消。クエリボリュームによる上位2つのエンティティタイプから始めます。

- **Week 11–12:** Editorial UI — classification review queue and synonym manager. Get editors using the system daily.  
  - **第11–12週:** 編集者UI — 分類レビューキューと同義語管理者。編集者が毎日システムを使用するようにします。

- **Week 13–14:** Serving API. Redis cache. Integration with the search or content platform.  
  - **第13–14週:** サービングAPI。Redisキャッシュ。検索またはコンテンツプラットフォームとの統合。

- **Week 15–16:** Monitoring dashboard. Drift detection. First causal attribution run with Papilon.  
  - **第15–16週:** モニタリングダッシュボード。ドリフト検出。Papilonを使用した最初の因果帰属実行。

Sixteen weeks to a production knowledge engineering system. Not a prototype — a system with editorial tooling, monitoring, and causal attribution. Every subsequent quarter is iterative improvement: more entity types, deeper taxonomy, better classifiers, more synonyms, more coverage.  
生産用の知識工学システムを構築するのに16週間。プロトタイプではなく、編集ツール、モニタリング、因果帰属を備えたシステムです。以降の四半期は反復的な改善です：より多くのエンティティタイプ、より深い分類、より良い分類器、より多くの同義語、より多くのカバレッジ。

<!-- ここまで読んだ! -->

## 11. Closing Thought 結論

The difference between a knowledge engineering project and a knowledge engineering system is infrastructure. 
知識工学プロジェクトと知識工学システムの違いはインフラストラクチャです。
The project produces a taxonomy and a classifier and declares victory. 
プロジェクトは分類法と分類器を生成し、勝利を宣言します。
The system produces a continuously-improving representation of meaning that gets better every week because editors can use it, engineers can monitor it, and leadership can see the causal impact of investing in it. 
**システムは、編集者が使用でき、エンジニアが監視でき、リーダーシップが投資の因果的影響を確認できるため、毎週改善される意味の継続的に改善される表現を生成**します。
Build the system. 
システムを構築してください。
It's more work upfront, but it's the only version that compounds. 
最初はより多くの作業が必要ですが、それが唯一の複利効果を持つバージョンです。



---  
About the Author: Brian Curry is a Kansas City–based data scientist, AI researcher, and founder of Vector1 Research, an independent lab advancing marketing economics, causal inference, and cognitive AI systems. 
著者について：ブライアン・カリーは、カンザスシティを拠点とするデータサイエンティスト、AI研究者であり、マーケティング経済学、因果推論、認知AIシステムを進展させる独立した研究所Vector1 Researchの創設者です。

He has led data and analytics initiatives at enterprises from $4B to $125B, including Koch Industries, Tractor Supply, Vail Resorts, Hallmark, Garmin, and AT&T. 
彼は、コーク・インダストリーズ、トラクター・サプライ、ヴェイル・リゾーツ、ホールマーク、ガーミン、AT&Tなど、40億ドルから1250億ドルの企業でデータと分析のイニシアチブを主導してきました。

He is the creator of MeaningFlow (semantic content modeling), Papilon (causal inference and complex systems), PyCausalSim (causal discovery through simulation), and the Memory-Node Encapsulation (MNE) architecture for cognitive AI. 
彼は、MeaningFlow（意味的コンテンツモデリング）、Papilon（因果推論と複雑系）、PyCausalSim（シミュレーションによる因果発見）、および認知AIのためのMemory-Node Encapsulation（MNE）アーキテクチャの創作者です。

<!-- ここまで読んだ! -->
