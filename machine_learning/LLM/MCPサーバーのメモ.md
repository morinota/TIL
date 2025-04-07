## これは何?

- MCPサーバーがよくわからなかったので調べたメモです。

## refs

- https://zenn.dev/tomo0108/articles/6b472b4c9cacfa
- [MCP サーバーを自作して GitHub Copilot の Agent に可読性の低いクラス名を作ってもらう](https://zenn.dev/microsoft/articles/semantickernel-mcp4)
- [VS Code の設定から MCPサーバーを追加して GitHub Copilot agent mode で利用してみる（安定版でも利用可能に）](https://qiita.com/youtoy/items/adfeedeedf1309f194ce)

# メモ

- 何それ??
  - MCPはModel Context Protocolの略。
    - Anthropic社が提唱したオープンソースのプロトコル。
      - 注意: 「プロトコル」って、"規則"や"約束事"みたいな意味で合ってる? 特定のInterfaceを定義する約束事、みたいなイメージ??:thinking:
        - 特に技術文脈では、プロトコル = 異なるシステム間でやり取りするための決まり事。ex. HTTPはWeb通信のためのプロトコル(決まり事)の1つ。
      - なので**Hogehoge Protocolサーバーは、特定のプロトコルに従った(i.e. 特定の規則に従うInterfaceを持つ)サーバー、みたいな感じかな**...!:thinking:
    - MCPの目的は、「**modelに与える文脈(context)を、外部から柔軟かつ標準化された形で制御する**」こと。
      - あ、context constructionを行うInterfaceを揃えよう〜みたいなモチベーションなのかな...!!:thinking:
    - MCPはUSBタイプCのポートのようなもの! このポートによって、デバイスと周辺機器を**標準化された方法でつなぐ**ことができる。
- github copilotなどの多くのAIホストがMCPに対応し始めてる。
  - MCPという共通のプロトコルを使うことで、プラグに近い感覚でAIホストに機能追加することができる。
    - あるMCPサービスをAIホストに接続すると、AgenticなAIがそのサービスを利用可能なツールの1つとして認識してくれる、みたいな感じか...!:thinking:
  - MCPサーバーは例えばクラウド上にホストすることも、使う時だけローカルでホストする、みたいなことも選択肢としてあるっぽい。

## MCP Python SDKについてメモ

- refs: https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#quickstart

### 主要な概念たち

#### Server

- FastMCPサーバーは、MCPプロトコルを実装したインターフェース。
- 接続管理、プロトコルの遵守、メッセージのルーティングを行う。

```python
# Add lifespan support for startup/shutdown with strong typing
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from fake_database import Database  # Replace with your actual DB type

from mcp.server.fastmcp import Context, FastMCP

# Create a named server
mcp = FastMCP("My App")

# Specify dependencies for deployment and development
mcp = FastMCP("My App", dependencies=["pandas", "numpy"])


@dataclass
class AppContext:
    db: Database


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        # Cleanup on shutdown
        await db.disconnect()


# Pass lifespan to server
mcp = FastMCP("My App", lifespan=app_lifespan)


# Access type-safe lifespan context in tools
@mcp.tool()
def query_db(ctx: Context) -> str:
    """Tool that uses initialized resources"""
    db = ctx.request_context.lifespan_context["db"]
    return db.query()
```


#### Resources

- リソースは、LLMにデータを公開する方法。
- **REST APIにおけるGETエンドポイントに似てる!**
- データを提供するが、重要な計算を実行したり副作用があったりしてはいけない。
  - GETエンドポイントの位置付けなら、RAGのretrievalはこれでいいのかも。

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

@mcp.resource("config://app")
def get_config() -> str:
    return "App configuration here"

@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    return f"Profile data for user {user_id}"
```

#### Tools

- ツールは、LLMがサーバーを通してアクションを起こせるようにする。
  - (read-onlyアクションではなく、writeアクション、みたいなイメージ??:thinking:)
- リソースとは異なり、ツールは計算を実行し、副作用を持つことが期待されてる。
  - たとえば、ユーザ質問の意図分類器などは、GETっていうよりはこっちで実装すべきなのかな:thinking:

```python
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")


@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


# 天気の取得は、リソースじゃなくてツールなのか...:thinking:
@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.text
```

#### Prompts

- プロンプトは再利用可能なテンプレート。
  - (あ、プロンプトテンプレートはローカルのymlファイルじゃなくて、MCPサーバーから提供してもらう時代なのか...!:thinking:)

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("My App")


@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]
```

#### Imagesクラス

- (Imagesという概念は、前述の3つのHTTPメソッド的な概念とは異なるっぽい!)
- MCPサーバー上で画像データを扱うためのクラス!

```python
from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage

mcp = FastMCP("My App")


@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")
```

#### Context

- Contextクラスは、ツールやリソースがMCP capability(何それ?)にアクセスするためのもの。
  - chatGPTによると...Contextクラスは、MCPサーバ内で動作するツールやリソースが**リクエストごとの情報やサーバーの状態にアクセスするための役割**。
    - ex. リクエスト関連情報へのアクセス, サーバリソースへのアクセス、ログの記録など。

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context

# FastMCPサーバーのインスタンスを作成
mcp = FastMCP("MyApp")

# ツールの定義
@mcp.tool()
async def example_tool(ctx: Context, param: str) -> str:
    # リクエストのメタデータにアクセス
    request_info = ctx.request_context

    # サーバーのリソースにアクセス（例：データベース接続）
    db_connection = ctx.lifespan_context["db"]

    # ログの記録
    await ctx.info(f"Received parameter: {param}")

    # 進捗の報告
    await ctx.report_progress(1, 3)

    # 何らかの処理
    result = f"Processed {param}"

    # 進捗の報告
    await ctx.report_progress(2, 3)

    # 処理結果を返す
    return result
```

### MCPサーバーの起動

- 開発中は、以下のコマンドでMCPサーバーを起動してデバッグできる。

```bash
mcp dev server.py

# Add dependencies
mcp dev server.py --with pandas --with numpy

# Mount local code
mcp dev server.py --with-editable .
```
