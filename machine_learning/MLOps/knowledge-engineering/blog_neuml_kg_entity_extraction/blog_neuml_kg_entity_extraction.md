# Build knowledge graphs with LLM-driven entity extraction

- 原文: https://neuml.hashnode.dev/build-knowledge-graphs-with-llm-driven-entity-extraction
- ミラー: https://dev.to/neuml/build-knowledge-graphs-with-llm-driven-entity-extraction-4hlm
- Colab: https://colab.research.google.com/github/neuml/txtai/blob/master/examples/57_Build_knowledge_graphs_with_LLM_driven_entity_extraction.ipynb
- 著者: NeuML (txtaiのメンテナ)

## テーマ

txtai 7.0の新機能を使い、LLMでエンティティ関係を抽出して知識グラフを構築するチュートリアル記事。txtai 7.0以前はセマンティックグラフに自動関係検出しかなかったが、**手動(LLM抽出)で導出した関係をtxtaiデータベースに直接ロードできる** ようになった。

## 全体構成 (コードチュートリアル形式)

### 1. 前提

- txtai はベクトルインデックス (sparse/dense) + グラフ + リレーショナルDB を統合
- SQLでベクトル検索 / トピックモデリング / RAG が可能

```bash
pip install txtai[graph]
```

### 2. Wikipediaデータのロードと類似検索

`neuml/txtai-wikipedia` データセット (2024年1月時点のWikipedia要約) を使用。

```python
from txtai import Embeddings

wikipedia = Embeddings()
wikipedia.load(provider="huggingface-hub", container="neuml/txtai-wikipedia")

query = """
SELECT id, text FROM txtai WHERE similar('Viking raids in France') and percentile >= 0.5
"""
results = wikipedia.search(query, 5)
```

### 3. LLMでエンティティ関係抽出

モデル: `Qwen/Qwen3-4B-Instruct-2507`
プロンプトで `(nodes, edges)` のJSONを出力させる:

- **node**: `label`, `type`
- **edge**: `source`, `target`, `relationship`

```python
from txtai import LLM
import json

llm = LLM("Qwen/Qwen3-4B-Instruct-2507")

data = []
for result in results:
    prompt = f"""<|im_start|>system
    You are a friendly assistant. You answer questions from users.<|im_end|>
    <|im_start|>user
    Extract an entity relationship graph from the following text. Output as JSON

    Nodes must have label and type attributes. Edges must have source, target and relationship attributes.

    text: {result['text']} <|im_end|>
    <|im_start|>assistant
    """
    try:
        data.append(json.loads(llm(prompt, maxlength=4096)))
    except:
        pass
```

### 4. 埋め込みDB + グラフの構築

抽出したJSONを走査してノードを統合し、`Embeddings(graph={...})` にストリーム投入。

```python
def stream():
    nodes = {}
    for row in data.copy():
        for node in row["nodes"]:
            if node["label"] not in nodes:
                node["id"] = len(nodes)
                nodes[node["label"]] = node
        for edge in row["edges"]:
            source = nodes.get(edge["source"])
            target = nodes.get(edge["target"])
            if source and target:
                if "relationships" not in source:
                    source["relationships"] = []
                source["relationships"].append({"id": target["id"], "relationship": edge["relationship"]})
    return nodes.values()

embeddings = Embeddings(
    autoid="uuid5",
    path="intfloat/e5-base",
    instructions={"query": "query: ", "data": "passage: "},
    columns={"text": "label"},
    content=True,
    graph={"approximate": False, "topics": {}},
)
embeddings.index(stream())
```

### 5. ネットワーク可視化

matplotlib + networkx でエンティティタイプ別に色分け描画。

```python
import matplotlib.pyplot as plt
import networkx as nx

def plot(graph):
    labels = {x: f"{graph.attribute(x, 'text')} ({x})" for x in graph.scan()}
    lookup = {
        "Person": "#d32f2f",
        "Location": "#0277bd",
        "Event": "#e64980",
        "Role": "#757575",
    }
    colors = []
    for x in graph.scan():
        value = embeddings.search("select type from txtai where id = :x", parameters={"x": x})[0]["type"]
        colors.append(lookup.get(value, "#7e57c2"))
    # ... (spring_layout で描画)
```

### 6. グラフトラバース (Cypher風クエリ)

txtai 7.0で検索結果を **グラフとして返せる** ようになった。ノード間の関係をそのまま可視化可能。

```python
g = embeddings.graph.search("""
  MATCH P=(A{id: 8})-[R1]->()-[*1..3]->(D{id:5})
  WHERE
    R1.relationship == "has_object"
  RETURN P
""", graph=True)
plot(g)
```

## 結論

- **セマンティック類似で自動導出した関係** と **LLMで明示的に抽出した関係** のハイブリッドが強力
- txtaiだけで「ベクトル検索 + LLMエンティティ抽出 + グラフDB + Cypher風traversal」が完結する

## NVIDIA記事との対比 (メモ)

| 観点 | NVIDIA記事 | 本記事 (neuml/txtai) |
| --- | --- | --- |
| スケール | 大規模・プロダクション (TensorRT-LLM, cuGraph, マルチGPU) | 小規模・Colabで完結 |
| 抽出モデル | Llama-3 8B (NeMo+LoRAでFT) + Mixtral-8x7B で教師生成 | Qwen3-4B-Instruct を素のまま |
| 出力 | トリプレット (entity-relation-entity) | nodes/edges のJSON |
| DB | グラフDB (Neo4j等) | txtai統合DB (ベクトル+グラフ+RDB) |
| 検索 | GraphRAG / HybridRAG 評価 | Cypher風グラフトラバース |
| 読者 | エンタープライズ | 個人開発者 |

**タグプロジェクトへの示唆**: Qwen3-4BクラスでもJSONエンティティ抽出が回るなら、堀崎タグの延長でタグ間の関係グラフ (タグ階層・共起) を軽量に構築できる可能性あり。
