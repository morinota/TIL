refs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices


$
/
$
- Developer Guide
- API Reference
- MCP
- Resources
- Release Notes
Search...
⌘K
Intro to Claude
Claudeの紹介
Quickstart
クイックスタート
Models overview
モデルの概要
Choosing a model
モデルの選択
What's new in Claude 4.6
Claude 4.6の新機能
Migration guide
移行ガイド
Model deprecations
モデルの非推奨
Pricing
価格設定
Features overview
機能の概要
Using the Messages API
Messages APIの使用
Handling stop reasons
停止理由の処理
Prompting best practices
プロンプトのベストプラクティス
Context windows
コンテキストウィンドウ
Compaction
圧縮
Context editing
コンテキスト編集
Prompt caching
プロンプトキャッシング
Extended thinking
拡張思考
Adaptive thinking
適応思考
Effort
努力
Streaming Messages
ストリーミングメッセージ
Batch processing
バッチ処理
Citations
引用
Multilingual support
多言語サポート
Token counting
トークンカウント
Embeddings
埋め込み
Vision
ビジョン
PDF support
PDFサポート
Files API
ファイルAPI
Search results
検索結果
Structured outputs
構造化出力
Overview
概要
How to implement tool use
ツールの使用を実装する方法
Fine-grained tool streaming
細粒度ツールストリーミング
Bash tool
Bashツール
Code execution tool
コード実行ツール
Programmatic tool calling
プログラムによるツール呼び出し
Computer use tool
コンピュータ使用ツール
Text editor tool
テキストエディタツール
Web fetch tool
Webフェッチツール
Web search tool
Web検索ツール
Memory tool
メモリツール
Tool search tool
ツール検索ツール
Overview
概要
Quickstart
クイックスタート
Best practices
ベストプラクティス
Skills for enterprise
企業向けスキル
Using Skills with the API
APIを使用したスキル
Overview
概要
Quickstart
クイックスタート
TypeScript SDK
TypeScript SDK
TypeScript V2 (preview)
TypeScript V2（プレビュー）
Python SDK
Python SDK
Migration Guide
移行ガイド
Guides
ガイド
MCP connector
MCPコネクタ
Remote MCP servers
リモートMCPサーバー
Amazon Bedrock
Amazon Bedrock
Microsoft Foundry
Microsoft Foundry
Vertex AI
Vertex AI
Overview
概要
Prompt generator
プロンプトジェネレーター
Use prompt templates
プロンプトテンプレートの使用
Prompt improver
プロンプト改善ツール
Be clear and direct
明確かつ直接的に
Use examples (multishot prompting)
例を使用する（マルチショットプロンプティング）
Let Claude think (CoT)
Claudeに考えさせる（CoT）
Use XML tags
XMLタグの使用
Give Claude a role (system prompts)
Claudeに役割を与える（システムプロンプト）
Chain complex prompts
複雑なプロンプトを連鎖させる
Long context tips
長いコンテキストのヒント
Extended thinking tips
拡張思考のヒント
Define success criteria
成功基準の定義
Develop test cases
テストケースの開発
Using the Evaluation Tool
評価ツールの使用
Reducing latency
レイテンシの削減
Reduce hallucinations
幻覚の削減
Increase output consistency
出力の一貫性を高める
Mitigate jailbreaks
脱獄の軽減
Streaming refusals
ストリーミング拒否
Reduce prompt leak
プロンプト漏れの削減
Keep Claude in character
Claudeをキャラクターに保つ
Admin API overview
管理APIの概要
Data residency
データの居住地
Workspaces
ワークスペース
Usage and Cost API
使用とコストAPI
Claude Code Analytics API
Claudeコード分析API
Zero Data Retention
ゼロデータ保持
Agent Skills
エージェントスキル
Best practices
ベストプラクティス
Agent Skills
エージェントスキル
# Skill authoring best practices
スキル作成のベストプラクティス
Copy page
ページをコピー
Good Skills are concise, well-structured, and tested with real usage. This guide provides practical authoring decisions to help you write Skills that Claude can discover and use effectively.
良いスキルは簡潔で、構造が明確で、実際の使用でテストされています。このガイドは、Claudeが効果的に発見し使用できるスキルを書くための実用的な作成の決定を提供します。
For conceptual background on how Skills work, see the Skills overview.
スキルがどのように機能するかの概念的な背景については、スキルの概要を参照してください。



## Core principles コア原則

### Concise is key 簡潔さが重要

The context window is a public good. 
コンテキストウィンドウは公共財です。

Your Skill shares the context window with everything else Claude needs to know, including:
あなたのスキルは、Claudeが知っておく必要のある他のすべての情報とコンテキストウィンドウを共有します。これには以下が含まれます：
- The system prompt
- システムプロンプト
- Conversation history
- 会話履歴
- Other Skills' metadata
- 他のスキルのメタデータ
- Your actual request
- あなたの実際のリクエスト

Not every token in your Skill has an immediate cost. 
あなたのスキル内のすべてのトークンが即座にコストを持つわけではありません。

At startup, only the metadata (name and description) from all Skills is pre-loaded. 
起動時には、すべてのスキルからのメタデータ（名前と説明）のみが事前にロードされます。

Claude reads SKILL.md only when the Skill becomes relevant, and reads additional files only as needed. 
Claudeは、スキルが関連するようになるときにのみSKILL.mdを読み、必要に応じて追加のファイルを読みます。

However, being concise in SKILL.md still matters: once Claude loads it, every token competes with conversation history and other context. 
しかし、SKILL.mdで簡潔であることは依然として重要です。Claudeがそれをロードすると、すべてのトークンが会話履歴や他のコンテキストと競合します。

Default assumption: Claude is already very smart 
デフォルトの仮定：Claudeはすでに非常に賢いです。

Only add context Claude doesn't already have. 
Claudeがすでに持っていないコンテキストのみを追加してください。

Challenge each piece of information:
各情報を検証してください：
- "Does Claude really need this explanation?"
- 「Claudeは本当にこの説明を必要としていますか？」
- "Can I assume Claude knows this?"
- 「Claudeがこれを知っていると仮定してもよいですか？」
- "Does this paragraph justify its token cost?"
- 「この段落はそのトークンコストを正当化していますか？」

Good example: Concise (approximately 50 tokens):
良い例：簡潔（約50トークン）：
```
## Extract PDF text
Use pdfplumber for text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```  



## Extract PDF text PDFテキストの抽出

Use pdfplumber for text extraction: 
テキスト抽出にはpdfplumberを使用します：

```python
```python
import pdfplumber 
import pdfplumber 
import pdfplumberをインポートします。
with pdfplumber.open("file.pdf") as pdf: 
with pdfplumber.open("file.pdf") as pdf: 
"file.pdf"を開くときにpdfplumberを使用します。
text = pdf.pages[0].extract_text() 
text = pdf.pages[0].extract_text() 
ページ0からテキストを抽出します。
```
```
Bad example: Too verbose(approximately 150 tokens): 
悪い例：冗長すぎる（約150トークン）：

```
## Extract PDF text PDF (Portable Document Format) files are a common file format that contains text, images, and other content. 
## PDFテキストの抽出 PDF（ポータブルドキュメントフォーマット）ファイルは、テキスト、画像、その他のコンテンツを含む一般的なファイル形式です。
To extract text from a PDF, you'll need to use a library. 
PDFからテキストを抽出するには、ライブラリを使用する必要があります。
There are many libraries available for PDF processing, but we recommend pdfplumber because it's easy to use and handles most cases well. 
PDF処理のための多くのライブラリがありますが、使いやすくほとんどのケースにうまく対処できるため、pdfplumberをお勧めします。
First, you'll need to install it using pip. 
まず、pipを使用してインストールする必要があります。
Then you can use the code below... 
その後、以下のコードを使用できます...
The concise version assumes Claude knows what PDFs are and how libraries work. 
簡潔なバージョンは、ClaudeがPDFとは何か、ライブラリがどのように機能するかを知っていると仮定しています。

### Set appropriate degrees of freedom 
### 適切な自由度を設定する
Match the level of specificity to the task's fragility and variability. 
タスクの脆弱性と変動性に応じて特異性のレベルを一致させます。
High freedom (text-based instructions): 
高い自由度（テキストベースの指示）：
Use when: 
使用する場合：
- Multiple approaches are valid 
- 複数のアプローチが有効です
- Decisions depend on context 
- 決定は文脈に依存します
- Heuristics guide the approach 
- ヒューリスティックがアプローチを導きます
Example: 
例：
```
## Code review process 
## コードレビューのプロセス
1. Analyze the code structure and organization 
1. コードの構造と組織を分析します
2. Check for potential bugs or edge cases 
2. 潜在的なバグやエッジケースを確認します
3. Suggest improvements for readability and maintainability 
3. 可読性と保守性の向上を提案します
4. Verify adherence to project conventions 
4. プロジェクトの規約への準拠を確認します
```  



## Code review process コードレビューのプロセス

1. Analyze the code structure and organization  
1. コードの構造と組織を分析する

2. Check for potential bugs or edge cases  
2. 潜在的なバグやエッジケースをチェックする

3. Suggest improvements for readability and maintainability  
3. 可読性と保守性の向上を提案する

4. Verify adherence to project conventions  
4. プロジェクトの規約への遵守を確認する

Medium freedom(pseudocode or scripts with parameters):  
中程度の自由度（パラメータを持つ擬似コードまたはスクリプト）：

Use when:  
使用する場合：

- A preferred pattern exists  
- 好ましいパターンが存在する

- Some variation is acceptable  
- いくつかのバリエーションが許容される

- Configuration affects behavior  
- 設定が動作に影響を与える

Example:  
例：

```
## Generate report  
## レポートを生成する
Use this template and customize as needed:  
このテンプレートを使用し、必要に応じてカスタマイズしてください：

```python
def generate_report(data, format="markdown", include_charts=True):  
    # Process data  
    # データを処理する

    # Generate output in specified format  
    # 指定された形式で出力を生成する

    # Optionally include visualizations  
    # 必要に応じて視覚化を含める
```
```  



## Generate report レポートの生成

Use this template and customize as needed:
このテンプレートを使用し、必要に応じてカスタマイズしてください：
```python
```python
def generate_report(data, format="markdown", include_charts=True):
def generate_report(data, format="markdown", include_charts=True):
# Process data
# データを処理する
# Generate output in specified format
# 指定された形式で出力を生成する
# Optionally include visualizations
# 必要に応じて視覚化を含める
```
```
Low freedom(specific scripts, few or no parameters):
自由度が低い（特定のスクリプト、パラメータが少ないまたはない）：
Use when:
使用する場合：
- Operations are fragile and error-prone
- 操作が脆弱でエラーが発生しやすい
- Consistency is critical
- 一貫性が重要である
- A specific sequence must be followed
- 特定の順序に従う必要がある
Example:
例：
```
## Database migration データベース移行
Run exactly this script:
このスクリプトを正確に実行してください：
```bash
python scripts/migrate.py --verify --backup
```
Do not modify the command or add additional flags.
コマンドを変更したり、追加のフラグを加えたりしないでください。



## Database migration データベース移行

Run exactly this script: 
このスクリプトを正確に実行してください：
```bash
```bash
pythonscripts/migrate.py--verify--backup
python
scripts/migrate.py
--verify
--backup
```
```
Do not modify the command or add additional flags. 
コマンドを変更したり、追加のフラグを加えたりしないでください。

Analogy: Think of Claude as a robot exploring a path: 
例えとして、Claudeを道を探検するロボットと考えてください：
- Narrow bridge with cliffs on both sides: There's only one safe way forward. Provide specific guardrails and exact instructions (low freedom). Example: database migrations that must run in exact sequence. 
- 両側に崖のある狭い橋：進むべき安全な道は一つだけです。具体的なガードレールと正確な指示を提供してください（自由度が低い）。例：正確な順序で実行しなければならないデータベース移行。
- Open field with no hazards: Many paths lead to success. Give general direction and trust Claude to find the best route (high freedom). Example: code reviews where context determines the best approach. 
- 危険のない開けた野原：成功に至る道は多くあります。一般的な方向性を示し、Claudeが最良のルートを見つけることを信頼してください（自由度が高い）。例：文脈が最良のアプローチを決定するコードレビュー。

### Test with all models you plan to use 
### 使用予定のすべてのモデルでテストしてください

Skills act as additions to models, so effectiveness depends on the underlying model. 
スキルはモデルに追加されるものであり、その効果は基盤となるモデルに依存します。テストする際の考慮事項はモデルによって異なります：
- Claude Haiku(fast, economical): Does the Skill provide enough guidance? 
- Claude Haiku（迅速で経済的）：スキルは十分なガイダンスを提供していますか？
- Claude Sonnet(balanced): Is the Skill clear and efficient? 
- Claude Sonnet（バランスの取れた）：スキルは明確で効率的ですか？
- Claude Opus(powerful reasoning): Does the Skill avoid over-explaining? 
- Claude Opus（強力な推論）：スキルは過剰な説明を避けていますか？

What works perfectly for Opus might need more detail for Haiku. 
Opusにとって完璧に機能するものは、Haikuにとってはより詳細が必要かもしれません。If you plan to use your Skill across multiple models, aim for instructions that work well with all of them. 
複数のモデルでスキルを使用する予定がある場合は、すべてのモデルでうまく機能する指示を目指してください。



## Skill structure スキル構造

YAML Frontmatter: The SKILL.md frontmatter requires two fields:
YAML Frontmatter: SKILL.mdのフロントマターには、2つのフィールドが必要です。

name:
name:
- Maximum 64 characters
- 最大64文字
- Must contain only lowercase letters, numbers, and hyphens
- 小文字のアルファベット、数字、ハイフンのみを含む必要があります。
- Cannot contain XML tags
- XMLタグを含むことはできません。
- Cannot contain reserved words: "anthropic", "claude"
- 予約語「anthropic」や「claude」を含むことはできません。

description:
description:
- Must be non-empty
- 空であってはなりません。
- Maximum 1024 characters
- 最大1024文字
- Cannot contain XML tags
- XMLタグを含むことはできません。
- Should describe what the Skill does and when to use it
- スキルが何をするのか、いつ使用するのかを説明する必要があります。

For complete Skill structure details, see the Skills overview.
スキル構造の詳細については、スキルの概要を参照してください。

### Naming conventions 命名規則

Use consistent naming patterns to make Skills easier to reference and discuss.
一貫した命名パターンを使用して、スキルを参照しやすく、議論しやすくします。

We recommend using gerund form (verb + -ing) for Skill names, as this clearly describes the activity or capability the Skill provides.
スキル名には動名詞形（動詞 + -ing）を使用することをお勧めします。これにより、スキルが提供する活動や能力が明確に説明されます。

Remember that the name field must use lowercase letters, numbers, and hyphens only.
nameフィールドは小文字のアルファベット、数字、ハイフンのみを使用する必要があります。

Good naming examples (gerund form):
良い命名の例（動名詞形）：
- processing-pdfs
- analyzing-spreadsheets
- managing-databases
- testing-code
- writing-documentation

Acceptable alternatives:
許容される代替案：
- Noun phrases: pdf-processing, spreadsheet-analysis
- 名詞句: pdf-processing, spreadsheet-analysis
- Action-oriented: process-pdfs, analyze-spreadsheets
- アクション指向: process-pdfs, analyze-spreadsheets

Avoid:
避けるべきもの：
- Vague names: helper, utils, tools
- 曖昧な名前: helper, utils, tools
- Overly generic: documents, data, files
- あまりにも一般的: documents, data, files
- Reserved words: anthropic-helper, claude-tools
- 予約語: anthropic-helper, claude-tools
- Inconsistent patterns within your skill collection
- スキルコレクション内の不一致パターン

Consistent naming makes it easier to:
一貫した命名は、以下を容易にします：
- Reference Skills in documentation and conversations
- ドキュメントや会話でスキルを参照すること
- Understand what a Skill does at a glance
- スキルが何をするのかを一目で理解すること
- Organize and search through multiple Skills
- 複数のスキルを整理し、検索すること
- Maintain a professional, cohesive skill library
- プロフェッショナルで一貫したスキルライブラリを維持すること

### Writing effective descriptions 効果的な説明の作成

The description field enables Skill discovery and should include both what the Skill does and when to use it.
descriptionフィールドはスキルの発見を可能にし、スキルが何をするのか、いつ使用するのかの両方を含む必要があります。

Always write in third person. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems.
常に三人称で書いてください。説明はシステムプロンプトに挿入され、不一致な視点は発見の問題を引き起こす可能性があります。

- Good: "Processes Excel files and generates reports"
- 良い例: "Excelファイルを処理し、レポートを生成します"
- Avoid: "I can help you process Excel files"
- 避けるべき例: "私はあなたがExcelファイルを処理するのを手伝うことができます"
- Avoid: "You can use this to process Excel files"
- 避けるべき例: "これを使ってExcelファイルを処理できます"

Be specific and include key terms. Include both what the Skill does and specific triggers/contexts for when to use it.
具体的であり、重要な用語を含めてください。スキルが何をするのか、いつ使用するのかの特定のトリガーや文脈を含めてください。

Each Skill has exactly one description field. The description is critical for skill selection: Claude uses it to choose the right Skill from potentially 100+ available Skills.
各スキルには正確に1つの説明フィールドがあります。説明はスキル選択にとって重要です。Claudeはこれを使用して、利用可能な100以上のスキルから適切なスキルを選択します。

Your description must provide enough detail for Claude to know when to select this Skill, while the rest of SKILL.md provides the implementation details.
あなたの説明は、Claudeがこのスキルを選択するタイミングを知るために十分な詳細を提供しなければなりません。一方、SKILL.mdの残りの部分は実装の詳細を提供します。

Effective examples:
効果的な例：
PDF Processing skill:
PDF処理スキル：
```
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```
description: PDFファイルからテキストと表を抽出し、フォームに記入し、文書をマージします。PDFファイルを扱うときや、ユーザーがPDF、フォーム、または文書抽出について言及したときに使用します。

Excel Analysis skill:
Excel分析スキル：
```
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```
description: Excelスプレッドシートを分析し、ピボットテーブルを作成し、チャートを生成します。Excelファイル、スプレッドシート、表形式データ、または.xlsxファイルを分析するときに使用します。

Git Commit Helper skill:
Gitコミットヘルパースキル：
```
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```
description: gitの差分を分析して、説明的なコミットメッセージを生成します。ユーザーがコミットメッセージの作成やステージされた変更のレビューを手伝ってほしいときに使用します。

Avoid vague descriptions like these:
以下のような曖昧な説明は避けてください：
```
description: Helps with documents
```
description: 文書を手伝います

```
description: Processes data
```
description: データを処理します

```
description: Does stuff with files
```
description: ファイルに関する作業を行います

### Progressive disclosure patterns プログレッシブ開示パターン

SKILL.md serves as an overview that points Claude to detailed materials as needed, like a table of contents in an onboarding guide.
SKILL.mdは、Claudeが必要に応じて詳細な資料にアクセスできるようにする概要として機能します。これは、オンボーディングガイドの目次のようなものです。

For an explanation of how progressive disclosure works, see How Skills work in the overview.
プログレッシブ開示がどのように機能するかの説明については、概要の「スキルの仕組み」を参照してください。

Practical guidance:
実用的なガイダンス：
- Keep SKILL.md body under 500 lines for optimal performance
- 最適なパフォーマンスのためにSKILL.mdの本文は500行未満に保ってください。
- Split content into separate files when approaching this limit
- この制限に近づいた場合は、コンテンツを別のファイルに分割してください。
- Use the patterns below to organize instructions, code, and resources effectively
- 以下のパターンを使用して、指示、コード、およびリソースを効果的に整理してください。

#### Visual overview: From simple to complex ビジュアル概要：シンプルから複雑へ

A basic Skill starts with just a SKILL.md file containing metadata and instructions:
基本的なスキルは、メタデータと指示を含むSKILL.mdファイルから始まります。

As your Skill grows, you can bundle additional content that Claude loads only when needed:
スキルが成長するにつれて、Claudeが必要なときにのみ読み込む追加のコンテンツをバンドルできます。

The complete Skill directory structure might look like this:
完全なスキルディレクトリ構造は次のようになります：
```
pdf/
├── SKILL.md              # Main instructions (loaded when triggered)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
```

#### Pattern 1: High-level guide with references パターン1：参照を含む高レベルガイド
```
---name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---# PDF Processing
## Quick start
Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
## Advanced features
**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```
---
---
name: pdf-processing
name:
pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
description:
PDFファイルからテキストと表を抽出し、フォームに記入し、文書をマージします。PDFファイルを扱うときや、ユーザーがPDF、フォーム、または文書抽出について言及したときに使用します。
---
---
# PDF Processing
# PDF処理



## Quick start クイックスタート

Extract text with pdfplumber: 
pdfplumberを使用してテキストを抽出します：

```python
```python
import pdfplumber
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
with pdfplumber.open(
"file.pdf"
) as pdf:
text = pdf.pages[0].extract_text()
text = pdf.pages[0].extract_text()
```
```  



## Advanced features 高度な機能

**Form filling**: See [FORMS.md](FORMS.md) for complete guide  
**フォーム入力**: 完全なガイドについては[FORMS.md](FORMS.md)を参照してください。

**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods  
**APIリファレンス**: すべてのメソッドについては[REFERENCE.md](REFERENCE.md)を参照してください。

**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns  
**例**: 一般的なパターンについては[EXAMPLES.md](EXAMPLES.md)を参照してください。

Claude loads FORMS.md, REFERENCE.md, or EXAMPLES.md only when needed.  
Claudeは、必要なときにのみFORMS.md、REFERENCE.md、またはEXAMPLES.mdを読み込みます。

#### Pattern 2: Domain-specific organization  
#### パターン2: ドメイン特化型の組織

For Skills with multiple domains, organize content by domain to avoid loading irrelevant context.  
複数のドメインを持つスキルの場合、無関係なコンテキストを読み込まないように、ドメインごとにコンテンツを整理します。

When a user asks about sales metrics, Claude only needs to read sales-related schemas, not finance or marketing data.  
ユーザーが売上指標について尋ねると、Claudeは財務やマーケティングデータではなく、売上関連のスキーマのみを読む必要があります。

This keeps token usage low and context focused.  
これにより、トークンの使用量が少なく、コンテキストが集中します。

```
bigquery-skill/
├── SKILL.md (overview and navigation)  
├── SKILL.md (概要とナビゲーション)
└── reference/  
└── リファレンス/
    ├── finance.md (revenue, billing metrics)  
    ├── finance.md (収益、請求メトリクス)
    ├── sales.md (opportunities, pipeline)  
    ├── sales.md (機会、パイプライン)
    ├── product.md (API usage, features)  
    ├── product.md (APIの使用、機能)
    └── marketing.md (campaigns, attribution)  
    └── marketing.md (キャンペーン、帰属)
```

```
# BigQuery Data Analysis  
# BigQueryデータ分析

## Available datasets  
## 利用可能なデータセット

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)  
**財務**: 収益、ARR、請求 → [reference/finance.md](reference/finance.md)を参照してください。

**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)  
**営業**: 機会、パイプライン、アカウント → [reference/sales.md](reference/sales.md)を参照してください。

**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)  
**製品**: APIの使用、機能、採用 → [reference/product.md](reference/product.md)を参照してください。

**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)  
**マーケティング**: キャンペーン、帰属、メール → [reference/marketing.md](reference/marketing.md)を参照してください。

## Quick search  
## クイック検索

Find specific metrics using grep:  
grepを使用して特定のメトリクスを見つける:

```bash
grep -i "revenue" reference/finance.md  
grep -i "pipeline" reference/sales.md  
grep -i "api usage" reference/product.md  
```



## Available datasets 利用可能なデータセット

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)  
**Finance**  
: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)  

**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)  
**Sales**  
: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)  

**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)  
**Product**  
: API usage, features, adoption → See [reference/product.md](reference/product.md)  

**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)  
**Marketing**  
: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)  



## Quick search クイック検索

Find specific metrics using grep:  
特定のメトリクスをgrepを使用して見つける：

```bash
```bash
grep -i "revenue" reference/finance.md  
grep -i "revenue" reference/finance.md

grep -i "pipeline" reference/sales.md  
grep -i "pipeline" reference/sales.md

grep -i "api usage" reference/product.md  
grep -i "api usage" reference/product.md
```
```

#### Pattern 3: Conditional details パターン3: 条件付き詳細
Show basic content, link to advanced content:  
基本的なコンテンツを表示し、高度なコンテンツへのリンクを提供します：

```
# DOCX Processing  
# DOCX処理

## Creating documents  
## ドキュメントの作成  
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).  
新しいドキュメントにはdocx-jsを使用します。詳細は[DOCX-JS.md](DOCX-JS.md)を参照してください。

## Editing documents  
## ドキュメントの編集  
For simple edits, modify the XML directly.  
簡単な編集の場合は、XMLを直接修正します。

**For tracked changes**: See [REDLINING.md](REDLINING.md)  
**変更履歴の追跡について**: [REDLINING.md](REDLINING.md)を参照してください。

**For OOXML details**: See [OOXML.md](OOXML.md)  
**OOXMLの詳細について**: [OOXML.md](OOXML.md)を参照してください。



## Creating documents 文書の作成

Use docx-js for new documents. 
新しい文書にはdocx-jsを使用してください。

See [DOCX-JS.md](DOCX-JS.md). 
[DOCX-JS.md](DOCX-JS.md)を参照してください。



## Editing documents 文書の編集

For simple edits, modify the XML directly.  
簡単な編集の場合は、XMLを直接修正してください。

**For tracked changes**: See [REDLINING.md](REDLINING.md)  
**変更履歴について**: [REDLINING.md](REDLINING.md)を参照してください。

**For OOXML details**: See [OOXML.md](OOXML.md)  
**OOXMLの詳細について**: [OOXML.md](OOXML.md)を参照してください。

Claude reads REDLINING.md or OOXML.md only when the user needs those features.  
Claudeは、ユーザーがそれらの機能を必要とする場合にのみ、REDLINING.mdまたはOOXML.mdを読みます。

### Avoid deeply nested references 深くネストされた参照を避ける

Claude may partially read files when they're referenced from other referenced files.  
Claudeは、他の参照ファイルから参照されているファイルを部分的に読むことがあります。

When encountering nested references, Claude might use commands like `head -100` to preview content rather than reading entire files, resulting in incomplete information.  
ネストされた参照に遭遇した場合、Claudeは全体のファイルを読むのではなく、内容をプレビューするために`head -100`のようなコマンドを使用することがあり、その結果、不完全な情報になることがあります。

Keep references one level deep from SKILL.md.  
SKILL.mdからの参照は1レベル深く保ってください。

All reference files should link directly from SKILL.md to ensure Claude reads complete files when needed.  
すべての参照ファイルはSKILL.mdから直接リンクする必要があり、必要なときにClaudeが完全なファイルを読むことを保証します。

Bad example: Too deep:  
悪い例: 深すぎる:

```
# SKILL.mdSee [advanced.md](advanced.md)...# advanced.mdSee [details.md](details.md)...# details.mdHere's the actual information...
```

# SKILL.md  
# SKILL.md  
See [advanced.md](advanced.md)...  
[advanced.md](advanced.md)を参照してください...

# advanced.md  
# advanced.md  
See [details.md](details.md)...  
[details.md](details.md)を参照してください...

# details.md  
# details.md  
Here's the actual information...  
ここに実際の情報があります...

Good example: One level deep:  
良い例: 1レベル深い:

```
# SKILL.md**Basic usage**: [instructions in SKILL.md]**Advanced features**: See [advanced.md](advanced.md)**API reference**: See [reference.md](reference.md)**Examples**: See [examples.md](examples.md)
```

# SKILL.md  
# SKILL.md  
**Basic usage**: [instructions in SKILL.md]  
**基本的な使用法**: [SKILL.mdの指示]  

**Advanced features**: See [advanced.md](advanced.md)  
**高度な機能**: [advanced.md](advanced.md)を参照してください。

**API reference**: See [reference.md](reference.md)  
**APIリファレンス**: [reference.md](reference.md)を参照してください。

**Examples**: See [examples.md](examples.md)  
**例**: [examples.md](examples.md)を参照してください。

### Structure longer reference files with table of contents  
長い参照ファイルには目次を構成する

For reference files longer than 100 lines, include a table of contents at the top.  
100行を超える参照ファイルには、最上部に目次を含めてください。

This ensures Claude can see the full scope of available information even when previewing with partial reads.  
これにより、Claudeは部分的に読み取る際でも、利用可能な情報の全体像を把握できます。

Example:  
例:

```
# API Reference## Contents-Authentication and setup-Core methods (create, read, update, delete)-Advanced features (batch operations, webhooks)-Error handling patterns-Code examples## Authentication and setup...## Core methods...
```

# API Reference  
# API Reference  



## Contents 目次
- Authentication and setup 認証とセットアップ
- Core methods (create, read, update, delete) コアメソッド（作成、読み取り、更新、削除）
- Advanced features (batch operations, webhooks) 高度な機能（バッチ操作、ウェブフック）
- Error handling patterns エラーハンドリングパターン
- Code examples コード例



## Authentication and setup 認証と設定

## Authentication and setup 認証と設定



## Core methods コアメソッド

Claude can then read the complete file or jump to specific sections as needed.
Claudeはその後、完全なファイルを読み取ることも、必要に応じて特定のセクションにジャンプすることもできます。
For details on how this filesystem-based architecture enables progressive disclosure, see the Runtime environment section in the Advanced section below.
このファイルシステムベースのアーキテクチャがどのように漸進的開示を可能にするかの詳細については、以下のAdvancedセクションのRuntime environmentセクションを参照してください。



## Workflows and feedback loops ワークフローとフィードバックループ
### Use workflows for complex tasks 複雑なタスクにはワークフローを使用する
Break complex operations into clear, sequential steps. 
複雑な操作を明確で順序立てたステップに分解します。 
For particularly complex workflows, provide a checklist that Claude can copy into its response and check off as it progresses. 
特に複雑なワークフローの場合、Claudeがその応答にコピーして進行状況をチェックできるチェックリストを提供します。

Example 1: Research synthesis workflow(for Skills without code): 
例1: 研究合成ワークフロー（コードなしのスキル用）:
```
## Research synthesis workflowCopy this checklist and track your progress:```Research Progress:- [ ] Step 1: Read all source documents- [ ] Step 2: Identify key themes- [ ] Step 3: Cross-reference claims- [ ] Step 4: Create structured summary- [ ] Step 5: Verify citations```**Step 1: Read all source documents**Review each document in the`sources/`directory. Note the main arguments and supporting evidence.**Step 2: Identify key themes**Look for patterns across sources. What themes appear repeatedly? Where do sources agree or disagree?**Step 3: Cross-reference claims**For each major claim, verify it appears in the source material. Note which source supports each point.**Step 4: Create structured summary**Organize findings by theme. Include:-Main claim-Supporting evidence from sources-Conflicting viewpoints (if any)**Step 5: Verify citations**Check that every claim references the correct source document. If citations are incomplete, return to Step 3.
```
```
## 研究合成ワークフロー このチェックリストをコピーして進捗を追跡してください:```研究の進捗:- [ ] ステップ1: すべてのソース文書を読む- [ ] ステップ2: 主要なテーマを特定する- [ ] ステップ3: 主張を相互参照する- [ ] ステップ4: 構造化された要約を作成する- [ ] ステップ5: 引用を確認する```**ステップ1: すべてのソース文書を読む**`sources/`ディレクトリ内の各文書をレビューします。主要な主張と支持証拠をメモします。**ステップ2: 主要なテーマを特定する**ソース間のパターンを探します。どのテーマが繰り返し現れますか？ソースはどこで一致または不一致ですか？**ステップ3: 主張を相互参照する**各主要な主張について、それがソース資料に現れることを確認します。各ポイントを支持するソースをメモします。**ステップ4: 構造化された要約を作成する**テーマごとに調査結果を整理します。含めるもの:-主要な主張-ソースからの支持証拠-対立する見解（あれば）**ステップ5: 引用を確認する**すべての主張が正しいソース文書を参照していることを確認します。引用が不完全な場合は、ステップ3に戻ります。



## Research synthesis workflow 研究合成ワークフロー
Copy this checklist and track your progress: 
このチェックリストをコピーして進捗を追跡してください：

```
```
Research Progress: 
研究の進捗：
- [ ] Step 1: Read all source documents 
- [ ] ステップ 1: すべてのソース文書を読む
- [ ] Step 2: Identify key themes 
- [ ] ステップ 2: 主要なテーマを特定する
- [ ] Step 3: Cross-reference claims 
- [ ] ステップ 3: 主張を相互参照する
- [ ] Step 4: Create structured summary 
- [ ] ステップ 4: 構造化された要約を作成する
- [ ] Step 5: Verify citations 
- [ ] ステップ 5: 引用を確認する
```
```
**Step 1: Read all source documents** 
**ステップ 1: すべてのソース文書を読む**
Review each document in the `sources/` directory. Note the main arguments and supporting evidence. 
`sources/` ディレクトリ内の各文書をレビューします。主な主張と支持する証拠をメモしてください。

**Step 2: Identify key themes** 
**ステップ 2: 主要なテーマを特定する**
Look for patterns across sources. What themes appear repeatedly? Where do sources agree or disagree? 
ソース間のパターンを探します。どのテーマが繰り返し現れますか？ソースはどこで一致または不一致ですか？

**Step 3: Cross-reference claims** 
**ステップ 3: 主張を相互参照する**
For each major claim, verify it appears in the source material. Note which source supports each point. 
各主要な主張について、それがソース資料に現れることを確認します。各ポイントを支持するソースをメモしてください。

**Step 4: Create structured summary** 
**ステップ 4: 構造化された要約を作成する**
Organize findings by theme. Include: 
発見をテーマごとに整理します。以下を含めます：
-Main claim 
-主な主張
-Supporting evidence from sources 
-ソースからの支持する証拠
-Conflicting viewpoints (if any) 
-対立する見解（あれば）

**Step 5: Verify citations** 
**ステップ 5: 引用を確認する**
Check that every claim references the correct source document. If citations are incomplete, return to Step 3. 
すべての主張が正しいソース文書を参照していることを確認します。引用が不完全な場合は、ステップ 3 に戻ります。

This example shows how workflows apply to analysis tasks that don't require code. 
この例は、ワークフローがコードを必要としない分析タスクにどのように適用されるかを示しています。

The checklist pattern works for any complex, multi-step process. 
チェックリストのパターンは、あらゆる複雑な多段階プロセスに適しています。

Example 2: PDF form filling workflow(for Skills with code): 
例 2: PDFフォーム記入ワークフロー（コードを使用したスキル用）：
```
## PDF form filling workflow 
## PDFフォーム記入ワークフロー
Copy this checklist and check off items as you complete them: 
このチェックリストをコピーして、完了した項目にチェックを入れてください：

```Task Progress: 
```タスクの進捗：
- [ ] Step 1: Analyze the form (run analyze_form.py) 
- [ ] ステップ 1: フォームを分析する（analyze_form.pyを実行）
- [ ] Step 2: Create field mapping (edit fields.json) 
- [ ] ステップ 2: フィールドマッピングを作成する（fields.jsonを編集）
- [ ] Step 3: Validate mapping (run validate_fields.py) 
- [ ] ステップ 3: マッピングを検証する（validate_fields.pyを実行）
- [ ] Step 4: Fill the form (run fill_form.py) 
- [ ] ステップ 4: フォームに記入する（fill_form.pyを実行）
- [ ] Step 5: Verify output (run verify_output.py) 
- [ ] ステップ 5: 出力を確認する（verify_output.pyを実行）
```
```
**Step 1: Analyze the form** 
**ステップ 1: フォームを分析する**
Run: `python scripts/analyze_form.py input.pdf` 
実行: `python scripts/analyze_form.py input.pdf`
This extracts form fields and their locations, saving to `fields.json`. 
これにより、フォームフィールドとその位置が抽出され、`fields.json`に保存されます。

**Step 2: Create field mapping** 
**ステップ 2: フィールドマッピングを作成する**
Edit `fields.json` to add values for each field. 
`fields.json`を編集して、各フィールドの値を追加します。

**Step 3: Validate mapping** 
**ステップ 3: マッピングを検証する**
Run: `python scripts/validate_fields.py fields.json` 
実行: `python scripts/validate_fields.py fields.json`
Fix any validation errors before continuing. 
続行する前に、検証エラーを修正してください。

**Step 4: Fill the form** 
**ステップ 4: フォームに記入する**
Run: `python scripts/fill_form.py input.pdf fields.json output.pdf` 
実行: `python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output** 
**ステップ 5: 出力を確認する**
Run: `python scripts/verify_output.py output.pdf` 
実行: `python scripts/verify_output.py output.pdf`
If verification fails, return to Step 2. 
検証に失敗した場合は、ステップ 2 に戻ります。



## PDF form filling workflow PDFフォーム記入ワークフロー

Copy this checklist and check off items as you complete them:  
このチェックリストをコピーし、完了した項目にチェックを入れてください：

```
```
Task Progress:  
タスクの進捗：

- [ ] Step 1: Analyze the form (run analyze_form.py)  
- [ ] ステップ1: フォームを分析する（analyze_form.pyを実行）

- [ ] Step 2: Create field mapping (edit fields.json)  
- [ ] ステップ2: フィールドマッピングを作成する（fields.jsonを編集）

- [ ] Step 3: Validate mapping (run validate_fields.py)  
- [ ] ステップ3: マッピングを検証する（validate_fields.pyを実行）

- [ ] Step 4: Fill the form (run fill_form.py)  
- [ ] ステップ4: フォームに記入する（fill_form.pyを実行）

- [ ] Step 5: Verify output (run verify_output.py)  
- [ ] ステップ5: 出力を確認する（verify_output.pyを実行）

```
```
**Step 1: Analyze the form**  
**ステップ1: フォームを分析する**

Run:`python scripts/analyze_form.py input.pdf`  
実行：`python scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to`fields.json`.  
これにより、フォームフィールドとその位置が抽出され、`fields.json`に保存されます。

**Step 2: Create field mapping**  
**ステップ2: フィールドマッピングを作成する**

Edit`fields.json`to add values for each field.  
`fields.json`を編集して、各フィールドの値を追加します。

**Step 3: Validate mapping**  
**ステップ3: マッピングを検証する**

Run:`python scripts/validate_fields.py fields.json`  
実行：`python scripts/validate_fields.py fields.json`

Fix any validation errors before continuing.  
続行する前に、検証エラーを修正してください。

**Step 4: Fill the form**  
**ステップ4: フォームに記入する**

Run:`python scripts/fill_form.py input.pdf fields.json output.pdf`  
実行：`python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output**  
**ステップ5: 出力を確認する**

Run:`python scripts/verify_output.py output.pdf`  
実行：`python scripts/verify_output.py output.pdf`

If verification fails, return to Step 2.  
検証に失敗した場合は、ステップ2に戻ってください。

Clear steps prevent Claude from skipping critical validation. The checklist helps both Claude and you track progress through multi-step workflows.  
明確な手順は、Claudeが重要な検証をスキップするのを防ぎます。このチェックリストは、Claudeとあなたの両方が複数のステップのワークフローを通じて進捗を追跡するのに役立ちます。

### Implement feedback loops  
### フィードバックループの実装

Common pattern: Run validator → fix errors → repeat  
一般的なパターン：バリデーターを実行 → エラーを修正 → 繰り返す

This pattern greatly improves output quality.  
このパターンは出力の質を大幅に向上させます。

Example 1: Style guide compliance(for Skills without code):  
例1: スタイルガイドの準拠（コードなしのスキル用）：

```
## Content review process  
## コンテンツレビューのプロセス

1. Draft your content following the guidelines in STYLE_GUIDE.md  
1. STYLE_GUIDE.mdのガイドラインに従ってコンテンツをドラフトする

2. Review against the checklist:  
2. チェックリストに対してレビューする：

- Check terminology consistency  
- 用語の一貫性を確認する

- Verify examples follow the standard format  
- 例が標準フォーマットに従っていることを確認する

- Confirm all required sections are present  
- 必要なすべてのセクションが存在することを確認する

3. If issues found:  
3. 問題が見つかった場合：

- Note each issue with specific section reference  
- 各問題を特定のセクション参照とともに記録する

- Revise the content  
- コンテンツを修正する

- Review the checklist again  
- チェックリストを再度レビューする

4. Only proceed when all requirements are met  
4. すべての要件が満たされたときのみ進む

5. Finalize and save the document  
5. ドキュメントを最終化し、保存する



## Content review process コンテンツレビューのプロセス

1. Draft your content following the guidelines in STYLE_GUIDE.md  
1. STYLE_GUIDE.mdのガイドラインに従ってコンテンツをドラフトします。

2. Review against the checklist:  
2. チェックリストに対してレビューします：
   - Check terminology consistency  
   - 用語の一貫性を確認します
   - Verify examples follow the standard format  
   - 例が標準フォーマットに従っていることを確認します
   - Confirm all required sections are present  
   - 必要なすべてのセクションが存在することを確認します

3. If issues found:  
3. 問題が見つかった場合：
   - Note each issue with specific section reference  
   - 各問題を特定のセクション参照と共に記録します
   - Revise the content  
   - コンテンツを修正します
   - Review the checklist again  
   - チェックリストを再度レビューします

4. Only proceed when all requirements are met  
4. すべての要件が満たされたときのみ進めます

5. Finalize and save the document  
5. ドキュメントを最終化し、保存します

This shows the validation loop pattern using reference documents instead of scripts.  
これは、スクリプトの代わりに参照文書を使用した検証ループパターンを示しています。The "validator" is STYLE_GUIDE.md, and Claude performs the check by reading and comparing.  
「バリデーター」はSTYLE_GUIDE.mdであり、Claudeは読み取りと比較によってチェックを行います。

Example 2: Document editing process(for Skills with code):  
例2: ドキュメント編集プロセス（コードを含むスキル用）：
```
## Document editing process  
## ドキュメント編集プロセス
1. Make your edits to `word/document.xml`  
1. `word/document.xml`に編集を加えます
2. **Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`  
2. **すぐに検証**: `python ooxml/scripts/validate.py unpacked_dir/`
3. If validation fails:  
3. 検証に失敗した場合：
   - Review the error message carefully  
   - エラーメッセージを注意深く確認します
   - Fix the issues in the XML  
   - XML内の問題を修正します
   - Run validation again  
   - 再度検証を実行します
4. **Only proceed when validation passes**  
4. **検証が通ったときのみ進めます**
5. Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`  
5. 再構築: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document  
6. 出力ドキュメントをテストします



## Document editing process 文書編集プロセス

1. Make your edits to `word/document.xml`  
1. `word/document.xml`に編集を加えます。

2. **Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`  
2. **すぐに検証**: `python ooxml/scripts/validate.py unpacked_dir/`

3. If validation fails:  
3. 検証に失敗した場合:

   - Review the error message carefully  
   - エラーメッセージを注意深く確認します。

   - Fix the issues in the XML  
   - XML内の問題を修正します。

   - Run validation again  
   - 再度検証を実行します。

4. **Only proceed when validation passes**  
4. **検証が通った場合のみ進めます**

5. Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`  
5. 再構築: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`

6. Test the output document  
6. 出力文書をテストします。

The validation loop catches errors early.  
検証ループは早期にエラーをキャッチします。



## Content guidelines コンテンツガイドライン

### Avoid time-sensitive information 時間に敏感な情報を避ける
Don't include information that will become outdated:
古い情報になる可能性のある情報を含めないでください：

Bad example: Time-sensitive(will become wrong):
悪い例：時間に敏感（間違ってしまう可能性がある）：

```
If you're doing this before August 2025, use the old API. 
After August 2025, use the new API.
```
```
もし2025年8月以前にこれを行っている場合は、古いAPIを使用してください。 
2025年8月以降は、新しいAPIを使用してください。

Good example(use "old patterns" section):
良い例（「古いパターン」セクションを使用）：

```
## Current method
Use the v2 API endpoint: `api.example.com/v2/messages`
## Old patterns
<details><summary>Legacy v1 API (deprecated 2025-08)</summary>The v1 API used: `api.example.com/v1/messages` This endpoint is no longer supported.</details>
```
```
## 現在の方法
v2 APIエンドポイントを使用します：`api.example.com/v2/messages`
## 古いパターン
<details><summary>レガシーv1 API（2025年8月に廃止）</summary>v1 APIは次のように使用されました：`api.example.com/v1/messages` このエンドポイントはもはやサポートされていません。</details>



## Current method 現在の方法

Use the v2 API endpoint:`api.example.com/v2/messages`
v2 APIエンドポイントを使用します：`api.example.com/v2/messages`

Use the v2 API endpoint:
`api.example.com/v2/messages`
v2 APIエンドポイントを使用します：`api.example.com/v2/messages`



## Old patterns 古いパターン  
## Old patterns 古いパターン
<details>
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used:`api.example.com/v1/messages`
v1 APIは次のように使用されていました：`api.example.com/v1/messages`
This endpoint is no longer supported.
このエンドポイントはもはやサポートされていません。
</details>
</details>
The old patterns section provides historical context without cluttering the main content.
古いパターンのセクションは、主要な内容を混乱させることなく歴史的な文脈を提供します。
### Use consistent terminology 一貫した用語を使用する
Choose one term and use it throughout the Skill:
1つの用語を選び、スキル全体で使用してください：
Good - Consistent:
良い - 一貫性がある：
- Always "API endpoint"
- 常に「APIエンドポイント」
- Always "field"
- 常に「フィールド」
- Always "extract"
- 常に「抽出」
Bad - Inconsistent:
悪い - 一貫性がない：
- Mix "API endpoint", "URL", "API route", "path"
- 「APIエンドポイント」、「URL」、「APIルート」、「パス」を混在させる
- Mix "field", "box", "element", "control"
- 「フィールド」、「ボックス」、「要素」、「コントロール」を混在させる
- Mix "extract", "pull", "get", "retrieve"
- 「抽出」、「プル」、「取得」、「リトリーブ」を混在させる
Consistency helps Claude understand and follow instructions.
一貫性はClaudeが指示を理解し、従うのに役立ちます。



## Common patterns 共通のパターン
### Template pattern テンプレートパターン
Provide templates for output format. Match the level of strictness to your needs.
出力形式のためのテンプレートを提供します。必要に応じて厳密さのレベルを調整してください。

For strict requirements(like API responses or data formats):
厳密な要件（APIレスポンスやデータ形式など）の場合：

```
## Report structureALWAYS use this exact template structure:
## レポート構造は常にこの正確なテンプレート構造を使用してください：
```markdown
# [Analysis Title] 
## Executive summary 
[One-paragraph overview of key findings] 
## Key findings 
-Finding 1 with supporting data 
-Finding 2 with supporting data 
-Finding 3 with supporting data 
## Recommendations 
1. Specific actionable recommendation 
2. Specific actionable recommendation
```
```  



## Report structure 報告書の構成

ALWAYS use this exact template structure:
常にこの正確なテンプレート構成を使用してください：

```markdown
```markdown
# [Analysis Title]
# [Analysis Title]
```  
```  



## Executive summary エグゼクティブサマリー  
[One-paragraph overview of key findings]  
[重要な発見の概要を1段落で説明します]  
[One-paragraph overview of key findings]  
[重要な発見の概要を1段落で説明します]  



## Key findings 主要な発見

-Finding 1 with supporting data
-発見1とそれを裏付けるデータ

-Finding 1 with supporting data
-発見1とそれを裏付けるデータ

-Finding 2 with supporting data
-発見2とそれを裏付けるデータ

-Finding 2 with supporting data
-発見2とそれを裏付けるデータ

-Finding 3 with supporting data
-発見3とそれを裏付けるデータ

-Finding 3 with supporting data
-発見3とそれを裏付けるデータ



## Recommendations 推奨事項

1. Specific actionable recommendation
1. 特定の実行可能な推奨事項
2. Specific actionable recommendation
2. 特定の実行可能な推奨事項

```
For flexible guidance(when adaptation is useful):
```
柔軟なガイダンスのために（適応が有用な場合）：

## Report structureHere is a sensible default format, but use your best judgment based on the analysis:
## 報告書の構成 ここに合理的なデフォルト形式がありますが、分析に基づいて最良の判断を使用してください：

```markdown
# [Analysis Title]
# [分析タイトル]
## Executive summary
## エグゼクティブサマリー
[Overview]
[概要]
## Key findings
## 主要な発見
[Adapt sections based on what you discover]
[発見に基づいてセクションを調整する]
## Recommendations
## 推奨事項
[Tailor to the specific context]
[特定の文脈に合わせる]
```
Adjust sections as needed for the specific analysis type.
特定の分析タイプに応じてセクションを必要に応じて調整してください。



## Report structure 報告書の構成

Here is a sensible default format, but use your best judgment based on the analysis:
ここに合理的なデフォルト形式がありますが、分析に基づいて最良の判断を使用してください。

```markdown
```markdown
```markdown
```markdown



## Executive summary 経営者向け要約

[Overview] 
[概要]



## Key findings 主要な発見

[Adapt sections based on what you discover] 
[発見に基づいてセクションを適応させてください]

[Adapt sections based on what you discover] 
[発見に基づいてセクションを適応させてください]



## Recommendations 推奨事項

[Tailor to the specific context]
[特定の文脈に合わせて調整してください。]
```
```
Adjust sections as needed for the specific analysis type.
特定の分析タイプに応じてセクションを調整してください。

### Examples pattern 例のパターン
For Skills where output quality depends on seeing examples, provide input/output pairs just like in regular prompting:
出力の質が例を見ることに依存するスキルの場合、通常のプロンプティングと同様に入力/出力ペアを提供してください：

```
## Commit message format コミットメッセージのフォーマット
Generate commit messages following these examples:
以下の例に従ってコミットメッセージを生成してください：

**Example 1:** 
**例 1:** 
Input: Added user authentication with JWT tokens
入力: JWTトークンを使用したユーザー認証を追加しました。
Output:
出力:
``` 
feat(auth): implement JWT-based authentication
feat(auth): JWTベースの認証を実装
Add login endpoint and token validation middleware
ログインエンドポイントとトークン検証ミドルウェアを追加
```

**Example 2:** 
**例 2:** 
Input: Fixed bug where dates displayed incorrectly in reports
入力: レポートで日付が不正に表示されるバグを修正しました。
Output:
出力:
``` 
fix(reports): correct date formatting in timezone conversion
fix(reports): タイムゾーン変換における日付フォーマットを修正
Use UTC timestamps consistently across report generation
レポート生成全体でUTCタイムスタンプを一貫して使用
```

**Example 3:** 
**例 3:** 
Input: Updated dependencies and refactored error handling
入力: 依存関係を更新し、エラーハンドリングをリファクタリングしました。
Output:
出力:
``` 
chore: update dependencies and refactor error handling
chore: 依存関係を更新し、エラーハンドリングをリファクタリング
- Upgrade lodash to 4.17.21
- lodashを4.17.21にアップグレード
- Standardize error response format across endpoints
- エンドポイント全体でエラー応答フォーマットを標準化
```

Follow this style: type(scope): brief description, then detailed explanation.
このスタイルに従ってください：type(scope): 簡潔な説明、その後に詳細な説明。



## Commit message format コミットメッセージのフォーマット

Generate commit messages following these examples:
以下の例に従ってコミットメッセージを生成します：

**Example 1:**
**例 1:**
Input: Added user authentication with JWT tokens  
入力: JWTトークンを使用したユーザー認証を追加しました  
Output:  
出力:  
```
feat(auth): implement JWT-based authentication  
feat(auth): JWTベースの認証を実装  
Add login endpoint and token validation middleware  
ログインエンドポイントとトークン検証ミドルウェアを追加  
```
```

**Example 2:**
**例 2:**
Input: Fixed bug where dates displayed incorrectly in reports  
入力: レポートで日付が不正に表示されるバグを修正しました  
Output:  
出力:  
```
fix(reports): correct date formatting in timezone conversion  
fix(reports): タイムゾーン変換における日付フォーマットを修正  
Use UTC timestamps consistently across report generation  
レポート生成全体でUTCタイムスタンプを一貫して使用  
```
```

**Example 3:**
**例 3:**
Input: Updated dependencies and refactored error handling  
入力: 依存関係を更新し、エラーハンドリングをリファクタリングしました  
Output:  
出力:  
```
chore: update dependencies and refactor error handling  
chore: 依存関係を更新し、エラーハンドリングをリファクタリング  
- Upgrade lodash to 4.17.21  
- lodashを4.17.21にアップグレード  
- Standardize error response format across endpoints  
- エンドポイント全体でエラー応答フォーマットを標準化  
```
```

Follow this style: type(scope): brief description, then detailed explanation.  
このスタイルに従ってください：type(scope): 簡潔な説明、その後に詳細な説明を続けます。  
Examples help Claude understand the desired style and level of detail more clearly than descriptions alone.  
例は、Claudeが望ましいスタイルと詳細レベルを説明だけよりも明確に理解するのに役立ちます。

### Conditional workflow pattern  
### 条件付きワークフローパターン  
Guide Claude through decision points:  
Claudeを意思決定ポイントに導きます：  
```
## Document modification workflow  
## ドキュメント修正ワークフロー  
1. Determine the modification type:  
1. 修正タイプを決定します：  
**Creating new content?** → Follow "Creation workflow" below  
**新しいコンテンツを作成していますか？** → 以下の「作成ワークフロー」に従ってください  
**Editing existing content?** → Follow "Editing workflow" below  
**既存のコンテンツを編集していますか？** → 以下の「編集ワークフロー」に従ってください  
2. Creation workflow:  
2. 作成ワークフロー：  
- Use docx-js library  
- docx-jsライブラリを使用  
- Build document from scratch  
- ドキュメントをゼロから構築  
- Export to .docx format  
- .docx形式にエクスポート  
3. Editing workflow:  
3. 編集ワークフロー：  
- Unpack existing document  
- 既存のドキュメントを展開  
- Modify XML directly  
- XMLを直接修正  
- Validate after each change  
- 各変更後に検証  
- Repack when complete  
- 完了したら再パック  



## Document modification workflow 文書修正ワークフロー

1. Determine the modification type:  
1. 修正タイプを決定する:  
**Creating new content?**→ Follow "Creation workflow" below  
**新しいコンテンツを作成していますか？**→ 以下の「作成ワークフロー」に従ってください  
**Editing existing content?**→ Follow "Editing workflow" below  
**既存のコンテンツを編集していますか？**→ 以下の「編集ワークフロー」に従ってください  

2. Creation workflow:  
2. 作成ワークフロー:  
- Use docx-js library  
- docx-jsライブラリを使用する  
- Build document from scratch  
- 文書をゼロから構築する  
- Export to .docx format  
- .docx形式でエクスポートする  

3. Editing workflow:  
3. 編集ワークフロー:  
- Unpack existing document  
- 既存の文書を展開する  
- Modify XML directly  
- XMLを直接修正する  
- Validate after each change  
- 各変更後に検証する  
- Repack when complete  
- 完了したら再パックする  

If workflows become large or complicated with many steps, consider pushing them into separate files and tell Claude to read the appropriate file based on the task at hand.  
ワークフローが大きくなったり、多くのステップで複雑になった場合は、それらを別のファイルに分け、Claudeにその時のタスクに基づいて適切なファイルを読むように指示することを検討してください。  



## Evaluation and iteration 評価と反復
### Build evaluations first 最初に評価を構築する
Create evaluations BEFORE writing extensive documentation. 
広範な文書を書く前に評価を作成します。 
This ensures your Skill solves real problems rather than documenting imagined ones. 
これにより、あなたのスキルが想像上の問題を文書化するのではなく、実際の問題を解決することが保証されます。

Evaluation-driven development: 
評価主導の開発：
1. Identify gaps: Run Claude on representative tasks without a Skill. Document specific failures or missing context 
1. ギャップを特定する：スキルなしで代表的なタスクでClaudeを実行します。特定の失敗や欠落しているコンテキストを文書化します。
2. Create evaluations: Build three scenarios that test these gaps 
2. 評価を作成する：これらのギャップをテストする3つのシナリオを構築します。
3. Establish baseline: Measure Claude's performance without the Skill 
3. ベースラインを確立する：スキルなしでのClaudeのパフォーマンスを測定します。
4. Write minimal instructions: Create just enough content to address the gaps and pass evaluations 
4. 最小限の指示を書く：ギャップに対処し、評価を通過するのに十分なコンテンツを作成します。
5. Iterate: Execute evaluations, compare against baseline, and refine 
5. 反復する：評価を実行し、ベースラインと比較し、洗練させます。

This approach ensures you're solving actual problems rather than anticipating requirements that may never materialize. 
このアプローチは、実際の問題を解決していることを保証し、決して実現しないかもしれない要件を予測することを避けます。

Evaluation structure: 
評価構造：
```
{"skills": ["pdf-processing"],"query":"Extract all text from this PDF file and save it to output.txt","files": ["test-files/document.pdf"],"expected_behavior": ["Successfully reads the PDF file using an appropriate PDF processing library or command-line tool","Extracts text content from all pages in the document without missing any pages","Saves the extracted text to a file named output.txt in a clear, readable format"]}
```
{
{
"skills": ["pdf-processing"],
"skills"
: [
"pdf-processing"
],
"query":"Extract all text from this PDF file and save it to output.txt",
"query"
:
"Extract all text from this PDF file and save it to output.txt"
,
"files": ["test-files/document.pdf"],
"files"
: [
"test-files/document.pdf"
],
"expected_behavior": [
"expected_behavior"
: [
"Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
"Successfully reads the PDF file using an appropriate PDF processing library or command-line tool"
,
"Extracts text content from all pages in the document without missing any pages",
"Extracts text content from all pages in the document without missing any pages"
,
"Saves the extracted text to a file named output.txt in a clear, readable format"
"Saves the extracted text to a file named output.txt in a clear, readable format"
]
]
}
}
This example demonstrates a data-driven evaluation with a simple testing rubric. 
この例は、シンプルなテスト基準を用いたデータ駆動型評価を示しています。 
We do not currently provide a built-in way to run these evaluations. 
現在、これらの評価を実行するための組み込みの方法は提供していません。 
Users can create their own evaluation system. 
ユーザーは独自の評価システムを作成できます。 
Evaluations are your source of truth for measuring Skill effectiveness. 
評価は、スキルの効果を測定するための真実の源です。

### Develop Skills iteratively with Claude Claudeを使ってスキルを反復的に開発する
The most effective Skill development process involves Claude itself. 
最も効果的なスキル開発プロセスは、Claude自体を含みます。 
Work with one instance of Claude ("Claude A") to create a Skill that will be used by other instances ("Claude B"). 
1つのインスタンスのClaude（「Claude A」）を使用して、他のインスタンス（「Claude B」）で使用されるスキルを作成します。 
Claude A helps you design and refine instructions, while Claude B tests them in real tasks. 
Claude Aは指示を設計し洗練するのを助け、Claude Bはそれらを実際のタスクでテストします。 
This works because Claude models understand both how to write effective agent instructions and what information agents need. 
これは、Claudeモデルが効果的なエージェント指示を書く方法と、エージェントが必要とする情報を理解しているからです。

Creating a new Skill: 
新しいスキルを作成する：
1. Complete a task without a Skill: Work through a problem with Claude A using normal prompting. 
1. スキルなしでタスクを完了する：通常のプロンプトを使用してClaude Aと問題を解決します。 
As you work, you'll naturally provide context, explain preferences, and share procedural knowledge. 
作業を進める中で、自然にコンテキストを提供し、好みを説明し、手続き的知識を共有します。 
Notice what information you repeatedly provide. 
繰り返し提供する情報に注意してください。

2. Identify the reusable pattern: After completing the task, identify what context you provided that would be useful for similar future tasks. 
2. 再利用可能なパターンを特定する：タスクを完了した後、将来の類似タスクに役立つコンテキストを特定します。 
Example: If you worked through a BigQuery analysis, you might have provided table names, field definitions, filtering rules (like "always exclude test accounts"), and common query patterns. 
例：BigQuery分析を行った場合、テーブル名、フィールド定義、フィルタリングルール（「常にテストアカウントを除外する」など）、および一般的なクエリパターンを提供したかもしれません。

3. Ask Claude A to create a Skill: "Create a Skill that captures this BigQuery analysis pattern we just used. 
3. Claude Aにスキルを作成するように依頼します：「私たちが使用したこのBigQuery分析パターンをキャプチャするスキルを作成してください。 
Include the table schemas, naming conventions, and the rule about filtering test accounts." 
テーブルスキーマ、命名規則、およびテストアカウントをフィルタリングするルールを含めてください。」 
Claude models understand the Skill format and structure natively. 
Claudeモデルはスキルの形式と構造をネイティブに理解しています。 
You don't need special system prompts or a "writing skills" skill to get Claude to help create Skills. 
スキルを作成するためにClaudeに助けを求めるために特別なシステムプロンプトや「スキルを書く」スキルは必要ありません。 
Simply ask Claude to create a Skill and it will generate properly structured SKILL.md content with appropriate frontmatter and body content. 
単にClaudeにスキルを作成するように依頼すれば、適切なフロントマターと本文を持つ適切に構造化されたSKILL.mdコンテンツが生成されます。

4. Review for conciseness: Check that Claude A hasn't added unnecessary explanations. 
4. 簡潔さを確認する：Claude Aが不必要な説明を追加していないか確認します。 
Ask: "Remove the explanation about what win rate means - Claude already knows that." 
「勝率が何を意味するかの説明を削除してください - Claudeはすでにそれを知っています。」

5. Improve information architecture: Ask Claude A to organize the content more effectively. 
5. 情報アーキテクチャを改善する：Claude Aにコンテンツをより効果的に整理するように依頼します。 
For example: "Organize this so the table schema is in a separate reference file. 
例えば：「テーブルスキーマを別の参照ファイルに整理してください。 
We might add more tables later." 
後でさらにテーブルを追加するかもしれません。」

6. Test on similar tasks: Use the Skill with Claude B (a fresh instance with the Skill loaded) on related use cases. 
6. 類似タスクでテストする：関連するユースケースでClaude B（スキルがロードされた新しいインスタンス）を使用してスキルをテストします。 
Observe whether Claude B finds the right information, applies rules correctly, and handles the task successfully. 
Claude Bが正しい情報を見つけ、ルールを正しく適用し、タスクを成功裏に処理するかどうかを観察します。

7. Iterate based on observation: If Claude B struggles or misses something, return to Claude A with specifics: 
7. 観察に基づいて反復する：Claude Bが苦労したり何かを見逃した場合は、具体的な内容を持ってClaude Aに戻ります。 
"When Claude used this Skill, it forgot to filter by date for Q4. 
「Claudeがこのスキルを使用したとき、Q4のために日付でフィルタリングするのを忘れました。 
Should we add a section about date filtering patterns?" 
日付フィルタリングパターンに関するセクションを追加すべきですか？」

Iterating on existing Skills: 
既存のスキルの反復：
The same hierarchical pattern continues when improving Skills. 
スキルを改善する際には、同じ階層的パターンが続きます。 
You alternate between: 
あなたは次の間で交互に作業します：
- Working with Claude A(the expert who helps refine the Skill) 
- スキルを洗練するのを助ける専門家Claude Aと作業する
- Testing with Claude B(the agent using the Skill to perform real work) 
- 実際の作業を行うためにスキルを使用しているエージェントClaude Bでテストする
- Observing Claude B's behavior and bringing insights back to Claude A 
- Claude Bの行動を観察し、洞察をClaude Aに持ち帰る

1. Use the Skill in real workflows: Give Claude B (with the Skill loaded) actual tasks, not test scenarios 
1. 実際のワークフローでスキルを使用する：Claude B（スキルがロードされた状態）に実際のタスクを与え、テストシナリオではありません。
2. Observe Claude B's behavior: Note where it struggles, succeeds, or makes unexpected choices 
2. Claude Bの行動を観察する：どこで苦労し、成功し、予期しない選択をするかを記録します。 
Example observation: "When I asked Claude B for a regional sales report, it wrote the query but forgot to filter out test accounts, even though the Skill mentions this rule." 
例の観察：「Claude Bに地域の売上レポートを求めたとき、クエリを書いたが、スキルがこのルールに言及しているにもかかわらず、テストアカウントを除外するのを忘れました。」

3. Return to Claude A for improvements: Share the current SKILL.md and describe what you observed. 
3. 改善のためにClaude Aに戻る：現在のSKILL.mdを共有し、観察したことを説明します。 
Ask: "I noticed Claude B forgot to filter test accounts when I asked for a regional report. 
「地域レポートを求めたとき、Claude Bがテストアカウントをフィルタリングするのを忘れたことに気付きました。 
The Skill mentions filtering, but maybe it's not prominent enough?" 
スキルはフィルタリングに言及していますが、もしかしたらそれが十分に目立っていないかもしれませんか？」

4. Review Claude A's suggestions: Claude A might suggest reorganizing to make rules more prominent, using stronger language like "MUST filter" instead of "always filter", or restructuring the workflow section. 
4. Claude Aの提案を確認する：Claude Aは、ルールをより目立たせるために再編成することや、「常にフィルタリングする」ではなく「MUSTフィルタリングする」といった強い言葉を使用すること、またはワークフローセクションを再構成することを提案するかもしれません。

5. Apply and test changes: Update the Skill with Claude A's refinements, then test again with Claude B on similar requests 
5. 変更を適用してテストする：Claude Aの洗練を反映させてスキルを更新し、同様のリクエストで再度Claude Bでテストします。

6. Repeat based on usage: Continue this observe-refine-test cycle as you encounter new scenarios. 
6. 使用に基づいて繰り返す：新しいシナリオに遭遇するたびに、この観察-洗練-テストサイクルを続けます。 
Each iteration improves the Skill based on real agent behavior, not assumptions. 
各反復は、仮定ではなく実際のエージェントの行動に基づいてスキルを改善します。

Gathering team feedback: 
チームのフィードバックを集める：
1. Share Skills with teammates and observe their usage 
1. スキルをチームメイトと共有し、彼らの使用状況を観察します。
2. Ask: Does the Skill activate when expected? Are instructions clear? What's missing? 
2. 質問する：スキルは期待通りにアクティブになりますか？指示は明確ですか？何が欠けていますか？
3. Incorporate feedback to address blind spots in your own usage patterns 
3. 自分の使用パターンの盲点に対処するためにフィードバックを取り入れます。

Why this approach works: 
このアプローチが機能する理由：
Claude A understands agent needs, you provide domain expertise, Claude B reveals gaps through real usage, and iterative refinement improves Skills based on observed behavior rather than assumptions. 
Claude Aはエージェントのニーズを理解し、あなたはドメインの専門知識を提供し、Claude Bは実際の使用を通じてギャップを明らかにし、反復的な洗練が観察された行動に基づいてスキルを改善します。

### Observe how Claude navigates Skills Claudeがスキルをどのようにナビゲートするかを観察する
As you iterate on Skills, pay attention to how Claude actually uses them in practice 
スキルを反復する際には、Claudeが実際にそれらをどのように使用するかに注意を払ってください。



. Watch for:
- Unexpected exploration paths: Does Claude read files in an order you didn't anticipate? This might indicate your structure isn't as intuitive as you thought
- 意外な探索経路に注意してください：Claudeは予想外の順序でファイルを読みますか？これは、あなたの構造が思ったほど直感的でない可能性を示唆しています。
- Missed connections: Does Claude fail to follow references to important files? Your links might need to be more explicit or prominent
- 重要なファイルへの参照を追わない場合：Claudeは重要なファイルへの参照を追わないですか？あなたのリンクは、より明示的または目立つ必要があるかもしれません。
- Overreliance on certain sections: If Claude repeatedly reads the same file, consider whether that content should be in the main SKILL.md instead
- 特定のセクションへの過度の依存：Claudeが同じファイルを繰り返し読む場合、その内容がメインのSKILL.mdに含まれるべきかどうかを考慮してください。
- Ignored content: If Claude never accesses a bundled file, it might be unnecessary or poorly signaled in the main instructions
- 無視されたコンテンツ：Claudeがバンドルされたファイルにアクセスしない場合、それは不要であるか、メインの指示で適切に示されていない可能性があります。
Iterate based on these observations rather than assumptions. The 'name' and 'description' in your Skill's metadata are particularly critical. Claude uses these when deciding whether to trigger the Skill in response to the current task. Make sure they clearly describe what the Skill does and when it should be used.
これらの観察に基づいて反復してください。あなたのSkillのメタデータにおける「name」と「description」は特に重要です。Claudeは、現在のタスクに応じてSkillをトリガーするかどうかを決定する際にこれらを使用します。これらがSkillの機能と使用すべきタイミングを明確に説明していることを確認してください。



## Anti-patterns to avoid 避けるべきアンチパターン

### Avoid Windows-style paths Windowsスタイルのパスを避ける
Always use forward slashes in file paths, even on Windows:  
ファイルパスでは常にスラッシュ（/）を使用し、Windowsでも同様です：
- ✓Good:scripts/helper.py,reference/guide.md  
- ✓良い例:scripts/helper.py,reference/guide.md
- ✗Avoid:scripts\helper.py,reference\guide.md  
- ✗避けるべき例:scripts\helper.py,reference\guide.md  
Unix-style paths work across all platforms, while Windows-style paths cause errors on Unix systems.  
Unixスタイルのパスはすべてのプラットフォームで機能しますが、WindowsスタイルのパスはUnixシステムでエラーを引き起こします。

### Avoid offering too many options 選択肢を多く提供しない
Don't present multiple approaches unless necessary:  
必要でない限り、複数のアプローチを提示しないでください：
```
**Bad example: Too many choices**(confusing):"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."  
**悪い例: 選択肢が多すぎる**（混乱を招く）："pypdf、pdfplumber、PyMuPDF、pdf2image、または..."を使用できます。
**Good example: Provide a default**(with escape hatch):"Use pdfplumber for text extraction:```pythonimportpdfplumber```For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."  
**良い例: デフォルトを提供する**（逃げ道付き）："テキスト抽出にはpdfplumberを使用してください:```pythonimportpdfplumber```OCRが必要なスキャンPDFには、代わりにpdf2imageとpytesseractを使用してください。"
```
**Bad example: Too many choices**(confusing):  
**悪い例: 選択肢が多すぎる**（混乱を招く）：
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."  
"pypdf、pdfplumber、PyMuPDF、pdf2image、または..."を使用できます。
**Good example: Provide a default**(with escape hatch):  
**良い例: デフォルトを提供する**（逃げ道付き）：
"Use pdfplumber for text extraction:  
"テキスト抽出にはpdfplumberを使用してください：
```python  
import pdfplumber  
```  
For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."  
OCRが必要なスキャンPDFには、代わりにpdf2imageとpytesseractを使用してください。"



## Advanced: Skills with executable code 高度なスキル：実行可能なコードを含むスキル

The sections below focus on Skills that include executable scripts. 
以下のセクションでは、実行可能なスクリプトを含むスキルに焦点を当てます。

If your Skill uses only markdown instructions, skip to Checklist for effective Skills. 
スキルがマークダウンの指示のみを使用する場合は、効果的なスキルのチェックリストに進んでください。

### Solve, don't punt 解決する、逃げない

When writing scripts for Skills, handle error conditions rather than punting to Claude. 
スキルのためにスクリプトを書くときは、Claudeに逃げるのではなく、エラー条件を処理してください。

Good example: Handle errors explicitly: 
良い例：エラーを明示的に処理する：

```
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # Create file with default content instead of failing
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # Provide alternative instead of failing
        print(f"Cannot access {path}, using default")
        return ''
```
```
def process_file(path):
    """ファイルを処理し、存在しない場合は作成します。"""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # 失敗するのではなく、デフォルトの内容でファイルを作成します
        print(f"ファイル {path} が見つかりません、デフォルトを作成します")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # 失敗するのではなく、代替手段を提供します
        print(f"{path} にアクセスできません、デフォルトを使用します")
        return ''
```

Bad example: Punt to Claude: 
悪い例：Claudeに逃げる：

```
def process_file(path):
    # Just fail and let Claude figure it out
    return open(path).read()
```
```
def process_file(path):
    # ただ失敗してClaudeに解決させる
    return open(path).read()
```

Configuration parameters should also be justified and documented to avoid "voodoo constants" (Ousterhout's law). 
設定パラメータは、「呪文の定数」（Ousterhoutの法則）を避けるために正当化され、文書化されるべきです。

If you don't know the right value, how will Claude determine it? 
正しい値がわからない場合、Claudeはそれをどのように決定しますか？

Good example: Self-documenting: 
良い例：自己文書化：

```
# HTTP requests typically complete within 30 seconds
# Longer timeout accounts for slow connections
REQUEST_TIMEOUT = 30
# Three retries balances reliability vs speed
# Most intermittent failures resolve by the second retry
MAX_RETRIES = 3
```
```
# HTTPリクエストは通常30秒以内に完了します
# 長いタイムアウトは遅い接続に対応します
REQUEST_TIMEOUT = 30
# 3回のリトライは信頼性と速度のバランスを取ります
# ほとんどの一時的な失敗は2回目のリトライで解決します
MAX_RETRIES = 3
```

Bad example: Magic numbers: 
悪い例：マジックナンバー：

```
TIMEOUT = 47  # Why 47?
RETRIES = 5    # Why 5?
```
```
TIMEOUT = 47  # なぜ47？
RETRIES = 5    # なぜ5？
```

### Provide utility scripts ユーティリティスクリプトを提供する

Even if Claude could write a script, pre-made scripts offer advantages: 
たとえClaudeがスクリプトを書くことができたとしても、事前に作成されたスクリプトには利点があります：

Benefits of utility scripts: 
ユーティリティスクリプトの利点：

- More reliable than generated code 
- 生成されたコードよりも信頼性が高い
- Save tokens (no need to include code in context) 
- トークンを節約する（コンテキストにコードを含める必要がない）
- Save time (no code generation required) 
- 時間を節約する（コード生成は不要）
- Ensure consistency across uses 
- 使用間での一貫性を確保する

The diagram above shows how executable scripts work alongside instruction files. 
上の図は、実行可能なスクリプトが指示ファイルとどのように連携して機能するかを示しています。

The instruction file (forms.md) references the script, and Claude can execute it without loading its contents into context. 
指示ファイル（forms.md）はスクリプトを参照し、Claudeはその内容をコンテキストに読み込むことなく実行できます。

Important distinction: Make clear in your instructions whether Claude should: 
重要な区別：指示の中でClaudeが以下のどちらを行うべきかを明確にしてください：

- Execute the script (most common): "Run analyze_form.py to extract fields" 
- スクリプトを実行する（最も一般的）： "analyze_form.pyを実行してフィールドを抽出する"
- Read it as reference (for complex logic): "See analyze_form.py for the field extraction algorithm" 
- 参照として読む（複雑なロジックの場合）： "フィールド抽出アルゴリズムについてはanalyze_form.pyを参照してください"

For most utility scripts, execution is preferred because it's more reliable and efficient. 
ほとんどのユーティリティスクリプトでは、実行が好まれます。なぜなら、それがより信頼性が高く効率的だからです。

See the Runtime environment section below for details on how script execution works. 
スクリプト実行がどのように機能するかの詳細については、以下のランタイム環境セクションを参照してください。

Example: 
例：

```
## Utility scripts
**analyze_form.py**: Extract all form fields from PDF
```bash
python scripts/analyze_form.py input.pdf > fields.json
```
Output format:
```json
{"field_name": {"type":"text","x":100,"y":200},"signature": {"type":"sig","x":150,"y":500}}
```
**validate_boxes.py**: Check for overlapping bounding boxes
```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```
**fill_form.py**: Apply field values to PDF
```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
```
## ユーティリティスクリプト
**analyze_form.py**: PDFからすべてのフォームフィールドを抽出します
```bash
python scripts/analyze_form.py input.pdf > fields.json
```
出力形式：
```json
{"field_name": {"type":"text","x":100,"y":200},"signature": {"type":"sig","x":150,"y":500}}
```
**validate_boxes.py**: 重複するバウンディングボックスをチェックします
```bash
python scripts/validate_boxes.py fields.json
# 戻り値: "OK" または衝突のリスト
```
**fill_form.py**: フィールド値をPDFに適用します
```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```



## Utility scripts ユーティリティスクリプト

**analyze_form.py**: Extract all form fields from PDF  
**analyze_form.py**: PDFからすべてのフォームフィールドを抽出します。

```bash
pythonscripts/analyze_form.py input.pdf > fields.json
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:  
出力形式:

```json
{
  "field_name": {"type":"text","x":100,"y":200},
  "signature": {"type":"sig","x":150,"y":500}
}
```

**validate_boxes.py**: Check for overlapping bounding boxes  
**validate_boxes.py**: 重複するバウンディングボックスをチェックします。

```bash
pythonscripts/validate_boxes.py fields.json
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts  
# 戻り値: "OK" または衝突のリスト
```

**fill_form.py**: Apply field values to PDF  
**fill_form.py**: フィールド値をPDFに適用します。

```bash
pythonscripts/fill_form.py input.pdf fields.json output.pdf
python scripts/fill_form.py input.pdf fields.json output.pdf
```

### Use visual analysis  
視覚分析を使用する

When inputs can be rendered as images, have Claude analyze them:  
入力が画像としてレンダリングできる場合、Claudeに分析させます:

1. Convert PDF to images:  
   1. PDFを画像に変換します:  
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. Analyze each page image to identify form fields  
   2. 各ページの画像を分析してフォームフィールドを特定します。

3. Claude can see field locations and types visually  
   3. Claudeはフィールドの位置とタイプを視覚的に確認できます。



## Form layout analysis フォームレイアウト分析

1.Convert PDF to images:  
1. PDFを画像に変換します：

```bash
```bash
python scripts/pdf_to_images.py form.pdf  
python scripts/pdf_to_images.py form.pdf  
```
```

2.Analyze each page image to identify form fields  
2. 各ページの画像を分析してフォームフィールドを特定します。

3.Claude can see field locations and types visually  
3. Claudeはフィールドの位置とタイプを視覚的に確認できます。

In this example, you'd need to write the pdf_to_images.py script.  
この例では、pdf_to_images.pyスクリプトを書く必要があります。  
Claude's vision capabilities help understand layouts and structures.  
Claudeの視覚能力は、レイアウトや構造を理解するのに役立ちます。

### Create verifiable intermediate outputs  
### 検証可能な中間出力を作成する

When Claude performs complex, open-ended tasks, it can make mistakes.  
Claudeが複雑でオープンエンドなタスクを実行する際、間違いを犯すことがあります。  
The "plan-validate-execute" pattern catches errors early by having Claude first create a plan in a structured format, then validate that plan with a script before executing it.  
「計画-検証-実行」パターンは、Claudeが最初に構造化された形式で計画を作成し、その後スクリプトでその計画を検証してから実行することで、早期にエラーをキャッチします。

Example: Imagine asking Claude to update 50 form fields in a PDF based on a spreadsheet.  
例：スプレッドシートに基づいてClaudeにPDF内の50のフォームフィールドを更新するように依頼することを想像してください。  
Without validation, Claude might reference non-existent fields, create conflicting values, miss required fields, or apply updates incorrectly.  
検証なしでは、Claudeは存在しないフィールドを参照したり、矛盾する値を作成したり、必須フィールドを見逃したり、更新を誤って適用したりする可能性があります。

Solution: Use the workflow pattern shown above (PDF form filling), but add an intermediate changes.json file that gets validated before applying changes.  
解決策：上記のワークフローパターン（PDFフォームの記入）を使用しますが、変更を適用する前に検証される中間のchanges.jsonファイルを追加します。  
The workflow becomes: analyze → create plan file → validate plan → execute → verify.  
ワークフローは次のようになります：分析 → 計画ファイルの作成 → 計画の検証 → 実行 → 検証。

Why this pattern works:  
このパターンが機能する理由：

- Catches errors early: Validation finds problems before changes are applied  
- エラーを早期にキャッチ：検証は変更が適用される前に問題を見つけます。

- Machine-verifiable: Scripts provide objective verification  
- 機械検証可能：スクリプトは客観的な検証を提供します。

- Reversible planning: Claude can iterate on the plan without touching originals  
- 可逆的な計画：Claudeは元のものに触れることなく計画を反復できます。

- Clear debugging: Error messages point to specific problems  
- 明確なデバッグ：エラーメッセージは特定の問題を指摘します。

When to use: Batch operations, destructive changes, complex validation rules, high-stakes operations.  
使用するタイミング：バッチ操作、破壊的変更、複雑な検証ルール、高リスクの操作。

Implementation tip: Make validation scripts verbose with specific error messages like "Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed" to help Claude fix issues.  
実装のヒント：検証スクリプトを詳細にし、「フィールド 'signature_date' が見つかりません。利用可能なフィールド：customer_name、order_total、signature_date_signed」のような具体的なエラーメッセージを含めて、Claudeが問題を修正できるようにします。

### Package dependencies  
### パッケージ依存関係

Skills run in the code execution environment with platform-specific limitations:  
スキルはプラットフォーム固有の制限を持つコード実行環境で実行されます：

- claude.ai: Can install packages from npm and PyPI and pull from GitHub repositories  
- claude.ai：npmおよびPyPIからパッケージをインストールし、GitHubリポジトリから取得できます。

- Anthropic API: Has no network access and no runtime package installation  
- Anthropic API：ネットワークアクセスがなく、ランタイムパッケージのインストールがありません。

List required packages in your SKILL.md and verify they're available in the code execution tool documentation.  
必要なパッケージをSKILL.mdにリストし、それらがコード実行ツールのドキュメントで利用可能であることを確認してください。

### Runtime environment  
### 実行環境

Skills run in a code execution environment with filesystem access, bash commands, and code execution capabilities.  
スキルはファイルシステムアクセス、bashコマンド、およびコード実行機能を持つコード実行環境で実行されます。  
For the conceptual explanation of this architecture, see The Skills architecture in the overview.  
このアーキテクチャの概念的な説明については、概要の「スキルアーキテクチャ」を参照してください。

How this affects your authoring:  
これが著作にどのように影響するか：

How Claude accesses Skills:  
Claudeがスキルにアクセスする方法：

1. Metadata pre-loaded: At startup, the name and description from all Skills' YAML frontmatter are loaded into the system prompt  
1. メタデータの事前ロード：起動時に、すべてのスキルのYAMLフロントマターから名前と説明がシステムプロンプトにロードされます。

2. Files read on-demand: Claude uses bash Read tools to access SKILL.md and other files from the filesystem when needed  
2. ファイルはオンデマンドで読み取られます：Claudeは必要に応じてbash Readツールを使用してSKILL.mdや他のファイルにアクセスします。

3. Scripts executed efficiently: Utility scripts can be executed via bash without loading their full contents into context.  
3. スクリプトは効率的に実行されます：ユーティリティスクリプトは、コンテキストにその全内容を読み込むことなくbash経由で実行できます。

Only the script's output consumes tokens  
スクリプトの出力のみがトークンを消費します。

4. No context penalty for large files: Reference files, data, or documentation don't consume context tokens until actually read  
4. 大きなファイルに対するコンテキストペナルティなし：参照ファイル、データ、またはドキュメントは、実際に読み取られるまでコンテキストトークンを消費しません。

- File paths matter: Claude navigates your skill directory like a filesystem. Use forward slashes (reference/guide.md), not backslashes  
- ファイルパスは重要です：Claudeはファイルシステムのようにスキルディレクトリをナビゲートします。バックスラッシュではなく、スラッシュを使用してください（reference/guide.md）。

- Name files descriptively: Use names that indicate content: form_validation_rules.md, not doc2.md  
- ファイルに説明的な名前を付ける：内容を示す名前を使用してください：form_validation_rules.mdではなくdoc2.md。

- Organize for discovery: Structure directories by domain or feature  
- 発見のために整理する：ディレクトリをドメインや機能で構造化します。

Good: reference/finance.md, reference/sales.md  
良い例：reference/finance.md、reference/sales.md  
Bad: docs/file1.md, docs/file2.md  
悪い例：docs/file1.md、docs/file2.md  

- Bundle comprehensive resources: Include complete API docs, extensive examples, large datasets; no context penalty until accessed  
- 包括的なリソースをバンドルする：完全なAPIドキュメント、広範な例、大規模なデータセットを含めます。アクセスされるまでコンテキストペナルティはありません。

- Prefer scripts for deterministic operations: Write validate_form.py rather than asking Claude to generate validation code  
- 決定論的操作にはスクリプトを好む：Claudeに検証コードを生成させるのではなく、validate_form.pyを書く。

- Make execution intent clear: "Run analyze_form.py to extract fields" (execute)  
- 実行意図を明確にする：「フィールドを抽出するためにanalyze_form.pyを実行する」（実行）

- "See analyze_form.py for the extraction algorithm" (read as reference)  
- 「抽出アルゴリズムについてはanalyze_form.pyを参照してください」（参照として読む）

Example:  
例：

```
bigquery-skill/  
├── SKILL.md (overview, points to reference files)  
└── reference/  
    ├── finance.md (revenue metrics)  
    ├── sales.md (pipeline data)  
    └── product.md (usage analytics)  
```

When the user asks about revenue, Claude reads SKILL.md, sees the reference to reference/finance.md, and invokes bash to read just that file.  
ユーザーが収益について尋ねると、ClaudeはSKILL.mdを読み、reference/finance.mdへの参照を見て、そのファイルだけを読み取るためにbashを呼び出します。  
The sales.md and product.md files remain on the filesystem, consuming zero context tokens until needed.  
sales.mdおよびproduct.mdファイルはファイルシステムに残り、必要になるまでコンテキストトークンを消費しません。  
This filesystem-based model is what enables progressive disclosure.  
このファイルシステムベースのモデルがプログレッシブディスクロージャーを可能にします。  
Claude can navigate and selectively load exactly what each task requires.  
Claudeはナビゲートし、各タスクに必要なものを正確に選択的にロードできます。

For complete details on the technical architecture, see How Skills work in the Skills overview.  
技術アーキテクチャの完全な詳細については、「スキルの概要におけるスキルの動作」を参照してください。

### MCP tool references  
### MCPツールの参照

If your Skill uses MCP (Model Context Protocol) tools, always use fully qualified tool names to avoid "tool not found" errors.  
スキルがMCP（モデルコンテキストプロトコル）ツールを使用する場合は、常に完全修飾ツール名を使用して「ツールが見つかりません」エラーを回避してください。

Format: ServerName:tool_name  
フォーマット：ServerName:tool_name  

Example:  
例：

```
Use the BigQuery:bigquery_schema tool to retrieve table schemas.  
Use the GitHub:create_issue tool to create issues.  
```

Use the BigQuery:bigquery_schema tool to retrieve table schemas.  
BigQuery:bigquery_schemaツールを使用してテーブルスキーマを取得します。  
Use the GitHub:create_issue tool to create issues.  
GitHub:create_issueツールを使用して問題を作成します。  

Where:  
どこで：

- BigQuery and GitHub are MCP server names  
- BigQueryとGitHubはMCPサーバー名です。

- bigquery_schema and create_issue are the tool names within those servers  
- bigquery_schemaとcreate_issueはそれらのサーバー内のツール名です。

Without the server prefix, Claude may fail to locate the tool, especially when multiple MCP servers are available.  
サーバープリフィックスがないと、Claudeはツールを見つけられない場合があります。特に複数のMCPサーバーが利用可能な場合はそうです。

### Avoid assuming tools are installed  
### ツールがインストールされていると仮定しない

Don't assume packages are available:  
パッケージが利用可能であると仮定しないでください：

```
**Bad example: Assumes installation**: "Use the pdf library to process the file."  
**悪い例：インストールを仮定**：「pdfライブラリを使用してファイルを処理します。」

**Good example: Explicit about dependencies**: "Install required package: `pip install pypdf` Then use it:  
**良い例：依存関係について明示的**：「必要なパッケージをインストールします：`pip install pypdf` その後、次のように使用します：

```python
from pypdf import PdfReader  
reader = PdfReader("file.pdf")  
```  
```  
```python
from pypdf import PdfReader  
reader = PdfReader("file.pdf")  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  
```  



## Technical notes 技術ノート

### YAML frontmatter requirements YAMLフロントマターの要件
The SKILL.md frontmatter requires name and description fields with specific validation rules:  
SKILL.mdのフロントマターは、特定の検証ルールを持つnameおよびdescriptionフィールドを必要とします：
- name: Maximum 64 characters, lowercase letters/numbers/hyphens only, no XML tags, no reserved words  
- name: 最大64文字、小文字のアルファベット/数字/ハイフンのみ、XMLタグなし、予約語なし
- description: Maximum 1024 characters, non-empty, no XML tags  
- description: 最大1024文字、空でない、XMLタグなし
See the Skills overview for complete structure details.  
完全な構造の詳細については、Skills overviewを参照してください。

### Token budgets トークン予算
Keep SKILL.md body under 500 lines for optimal performance.  
SKILL.mdの本文は最適なパフォーマンスのために500行未満に保ってください。 
If your content exceeds this, split it into separate files using the progressive disclosure patterns described earlier.  
コンテンツがこれを超える場合は、前述のプログレッシブディスクロージャーパターンを使用して別のファイルに分割してください。 
For architectural details, see the Skills overview.  
アーキテクチャの詳細については、Skills overviewを参照してください。



## Checklist for effective Skills 効果的なスキルのためのチェックリスト

Before sharing a Skill, verify:
スキルを共有する前に、確認してください：

### Core quality コア品質
- Description is specific and includes key terms
- 説明は具体的で、重要な用語を含んでいます。
- Description includes both what the Skill does and when to use it
- 説明には、スキルが何をするのか、いつ使用するのかが含まれています。
- SKILL.md body is under 500 lines
- SKILL.mdの本文は500行未満です。
- Additional details are in separate files (if needed)
- 追加の詳細は別のファイルにあります（必要に応じて）。
- No time-sensitive information (or in "old patterns" section)
- 時間に敏感な情報は含まれていません（または「古いパターン」セクションに）。
- Consistent terminology throughout
- 一貫した用語が全体で使用されています。
- Examples are concrete, not abstract
- 例は具体的であり、抽象的ではありません。
- File references are one level deep
- ファイル参照は1レベル深いです。
- Progressive disclosure used appropriately
- プログレッシブ・ディスクロージャーが適切に使用されています。
- Workflows have clear steps
- ワークフローには明確なステップがあります。

### Code and scripts コードとスクリプト
- Scripts solve problems rather than punt to Claude
- スクリプトは問題を解決し、Claudeに投げることはありません。
- Error handling is explicit and helpful
- エラーハンドリングは明示的で役立ちます。
- No "voodoo constants" (all values justified)
- 「呪文の定数」はありません（すべての値が正当化されています）。
- Required packages listed in instructions and verified as available
- 必要なパッケージは指示にリストされ、利用可能であることが確認されています。
- Scripts have clear documentation
- スクリプトには明確なドキュメントがあります。
- No Windows-style paths (all forward slashes)
- Windowsスタイルのパスはありません（すべてフォワードスラッシュ）。
- Validation/verification steps for critical operations
- 重要な操作のための検証/確認ステップがあります。
- Feedback loops included for quality-critical tasks
- 品質が重要なタスクのためにフィードバックループが含まれています。

### Testing テスト
- At least three evaluations created
- 少なくとも3つの評価が作成されています。
- Tested with Haiku, Sonnet, and Opus
- Haiku、Sonnet、およびOpusでテストされています。
- Tested with real usage scenarios
- 実際の使用シナリオでテストされています。
- Team feedback incorporated (if applicable)
- チームのフィードバックが組み込まれています（該当する場合）。



## Next steps 次のステップ

Create your first Skill  
最初のSkillを作成します。

Create and manage Skills in Claude Code  
Claude CodeでSkillsを作成および管理します。

Use Skills programmatically in TypeScript and Python  
TypeScriptおよびPythonでプログラム的にSkillsを使用します。

Upload and use Skills programmatically  
Skillsをプログラム的にアップロードして使用します。

Was this page helpful?  
このページは役に立ちましたか？

- Core principles  
- コア原則
- Concise is key  
- 簡潔さが重要
- Set appropriate degrees of freedom  
- 適切な自由度を設定する
- Test with all models you plan to use  
- 使用予定のすべてのモデルでテストする
- Skill structure  
- Skillの構造
- Naming conventions  
- 命名規則
- Writing effective descriptions  
- 効果的な説明を書く
- Progressive disclosure patterns  
- 漸進的開示パターン
- Avoid deeply nested references  
- 深くネストされた参照を避ける
- Structure longer reference files with table of contents  
- 長い参照ファイルは目次で構成する
- Workflows and feedback loops  
- ワークフローとフィードバックループ
- Use workflows for complex tasks  
- 複雑なタスクにはワークフローを使用する
- Implement feedback loops  
- フィードバックループを実装する
- Content guidelines  
- コンテンツガイドライン
- Avoid time-sensitive information  
- 時間に敏感な情報を避ける
- Use consistent terminology  
- 一貫した用語を使用する
- Common patterns  
- 一般的なパターン
- Template pattern  
- テンプレートパターン
- Examples pattern  
- 例パターン
- Conditional workflow pattern  
- 条件付きワークフローパターン
- Evaluation and iteration  
- 評価と反復
- Build evaluations first  
- まず評価を構築する
- Develop Skills iteratively with Claude  
- Claudeと共にSkillsを反復的に開発する
- Observe how Claude navigates Skills  
- ClaudeがSkillsをどのようにナビゲートするかを観察する
- Anti-patterns to avoid  
- 避けるべきアンチパターン
- Avoid Windows-style paths  
- Windowsスタイルのパスを避ける
- Avoid offering too many options  
- あまりにも多くの選択肢を提供することを避ける
- Advanced: Skills with executable code  
- 高度な: 実行可能なコードを持つSkills
- Solve, don't punt  
- 解決する、逃げない
- Provide utility scripts  
- ユーティリティスクリプトを提供する
- Use visual analysis  
- ビジュアル分析を使用する
- Create verifiable intermediate outputs  
- 検証可能な中間出力を作成する
- Package dependencies  
- 依存関係をパッケージ化する
- Runtime environment  
- 実行環境
- MCP tool references  
- MCPツールの参照
- Avoid assuming tools are installed  
- ツールがインストールされていると仮定しない
- Technical notes  
- 技術的ノート
- YAML frontmatter requirements  
- YAMLフロントマターの要件
- Token budgets  
- トークン予算
- Checklist for effective Skills  
- 効果的なSkillsのためのチェックリスト
- Core quality  
- コア品質
- Code and scripts  
- コードとスクリプト
- Testing  
- テスト
- Next steps  
- 次のステップ

### Solutions ソリューション
- AI agents  
- AIエージェント
- Code modernization  
- コードのモダナイゼーション
- Coding  
- コーディング
- Customer support  
- カスタマーサポート
- Education  
- 教育
- Financial services  
- 金融サービス
- Government  
- 政府
- Life sciences  
- 生命科学

### Partners パートナー
- Amazon Bedrock  
- Amazon Bedrock
- Google Cloud's Vertex AI  
- Google CloudのVertex AI

### Learn 学ぶ
- Blog  
- ブログ
- Catalog  
- カタログ
- Courses  
- コース
- Use cases  
- ユースケース
- Connectors  
- コネクタ
- Customer stories  
- カスタマーストーリー
- Engineering at Anthropic  
- Anthropicでのエンジニアリング
- Events  
- イベント
- Powered by Claude  
- Claudeによって提供
- Service partners  
- サービスパートナー
- Startups program  
- スタートアッププログラム

### Company 会社
- Anthropic  
- Anthropic
- Careers  
- キャリア
- Economic Futures  
- 経済の未来
- Research  
- 研究
- News  
- ニュース
- Responsible Scaling Policy  
- 責任あるスケーリングポリシー
- Security and compliance  
- セキュリティとコンプライアンス
- Transparency  
- 透明性

### Learn 学ぶ
- Blog  
- ブログ
- Catalog  
- カタログ
- Courses  
- コース
- Use cases  
- ユースケース
- Connectors  
- コネクタ
- Customer stories  
- カスタマーストーリー
- Engineering at Anthropic  
- Anthropicでのエンジニアリング
- Events  
- イベント
- Powered by Claude  
- Claudeによって提供
- Service partners  
- サービスパートナー
- Startups program  
- スタートアッププログラム

### Help and security ヘルプとセキュリティ
- Availability  
- 利用可能性
- Status  
- ステータス
- Support  
- サポート
- Discord  
- Discord

### Terms and policies 利用規約とポリシー
- Privacy policy  
- プライバシーポリシー
- Responsible disclosure policy  
- 責任ある開示ポリシー
- Terms of service: Commercial  
- サービス利用規約: 商業用
- Terms of service: Consumer  
- サービス利用規約: 消費者
- Usage policy  
- 利用ポリシー
