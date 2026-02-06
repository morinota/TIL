refs: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills

タイトル: How to create custom Skills カスタムスキルの作成方法

Updated this week 今週更新

---
(注釈)
Skills are available for users on Pro, Max, Team, and Enterprise plans. 
スキルは、Pro、Max、Team、およびEnterpriseプランのユーザーが利用できます。
This feature requires code execution to be enabled. 
この機能を使用するには、コード実行が有効である必要があります。
Skills are also available in beta for Claude Code users and for all API users using the code execution tool. 
スキルは、Claude Codeユーザーおよびコード実行ツールを使用するすべてのAPIユーザーにベータ版としても利用可能です。
---

Custom Skills let you enhance Claude with specialized knowledge and workflows specific to your organization or personal work style. 
**カスタムスキルを使用すると、組織や個人の作業スタイルに特化した専門知識やワークフローでClaudeを強化できます。**
This article explains how to create, structure, and test your own Skills. 
この記事では、自分自身のスキルを作成、構造化、およびテストする方法を説明します。
Skills can be as simple as a few lines of instructions or as complex as multi-file packages with executable code. 
スキルは、数行の指示から、実行可能なコードを含む複数ファイルのパッケージまで、シンプルなものから複雑なものまでさまざまです。
The best Skills: 
最良のスキルは次の通りです：

- Solve a specific, repeatable task 
  - 特定の繰り返し可能なタスクを解決します。
- Have clear instructions that Claude can follow 
  - Claudeが従うことができる明確な指示を持っています。
- Include examples when helpful 
  - 役立つ場合は例を含めます。
- Define when they should be used 
  - いつ使用すべきかを定義します。
- Are focused on one workflow rather than trying to do everything 
  - すべてを行おうとするのではなく、1つのワークフローに焦点を当てています。

## 1. Creating a Skill.md File Skill.mdファイルの作成

Every Skill consists of a directory containing at minimum a Skill.md file, which is the core of the Skill. 
すべてのSkillは、SkillのコアであるSkill.mdファイルを含むディレクトリで構成されています。このファイルは、YAMLフロントマターで始まる必要があり、名前と説明のフィールドを保持します。これらは必須のメタデータです。

### 1.1. Required metadata fields 必須メタデータフィールド

`name`: A human-friendly name for your Skill (64 characters maximum)  
name: Skillの人間に優しい名前（最大64文字）

- Example: Brand Guidelines  
  - 例: ブランドガイドライン  

`description`: A clear description of what the Skill does and when to use it.  
description: Skillが何をするのか、いつ使用するのかの明確な説明。 

- This is critical—Claude uses this to determine when to invoke your Skill (200 characters maximum).  
  - これは重要です—Claudeはこれを使用してSkillを呼び出すタイミングを判断します（最大200文字）。
- Example: Apply Acme Corp brand guidelines to presentations and documents, including official colors, fonts, and logo usage.  
  - 例: Acme Corpのブランドガイドラインをプレゼンテーションや文書に適用し、公式の色、フォント、ロゴの使用を含みます。  

### 1.2. Optional Metadata Fields 任意のメタデータフィールド

`dependencies`: Software packages required by your Skill.  
dependencies: Skillに必要なソフトウェアパッケージ。

- Example: python>=3.8, pandas>=1.5.0
  - 例: python>=3.8, pandas>=1.5.0  

The metadata in the Skill.md file serves as the first level of a progressive disclosure system, providing just enough information for Claude to know when the Skill should be used without having to load all of the content.  
Skill.mdファイルのメタデータは、プログレッシブディスクリプションシステムの最初のレベルとして機能し、ClaudeがSkillを使用すべきタイミングを知るために必要な情報を提供します。すべてのコンテンツを読み込む必要はありません。

<!-- ここまで読んだ! -->

### 1.3. Markdown Body マークダウンボディ

The Markdown body is the second level of detail after the metadata, so Claude will access this if needed after reading the metadata.  
マークダウンボディは、メタデータの後の詳細の第二レベルであり、**Claudeはメタデータを読んだ後に必要に応じてこれにアクセス**します。  
Depending on your task, Claude can access the Skill.md file and use the Skill.  
タスクに応じて、ClaudeはSkill.mdファイルにアクセスし、Skillを使用できます。

### 1.4. Example Skill.md 例 Skill.md

Brand Guidelines Skill ブランドガイドラインSkill  

```md
## Metadataname: Brand Guidelinesdescription: Apply Acme Corp brand guidelines to all presentations and documents## OverviewThis Skill provides Acme Corp's official brand guidelines for creating consistent, professional materials. When creating presentations, documents, or marketing materials, apply these standards to ensure all outputs match Acme's visual identity. Claude should reference these guidelines whenever creating external-facing materials or documents that represent Acme Corp.## Brand ColorsOur official brand colors are:- Primary: #FF6B35 (Coral)- Secondary: #004E89 (Navy Blue)- Accent: #F7B801 (Gold)- Neutral: #2E2E2E (Charcoal)## TypographyHeaders: Montserrat BoldBody text: Open Sans RegularSize guidelines:- H1: 32pt- H2: 24pt- Body: 11pt## Logo UsageAlways use the full-color logo on light backgrounds. Use the white logo on dark backgrounds. Maintain minimum spacing of 0.5 inches around the logo.## When to ApplyApply these guidelines whenever creating:- PowerPoint presentations- Word documents for external sharing- Marketing materials- Reports for clients## ResourcesSee the resources folder for logo files and font downloads.
```

<!-- ここまで読んだ! -->

## 2. Adding Resources リソースの追加

If you have too much information to add to a singleSkill.mdfile (e.g., sections that only apply to specific scenarios), you can add more content by adding files within your Skill directory. 
もし、**単一のSkill.mdファイルに追加する情報が多すぎる場合（例えば、特定のシナリオにのみ適用されるセクションなど）**、Skillディレクトリ内にファイルを追加することで、より多くのコンテンツを追加できます。
For example, add a REFERENCE.md file containing supplemental and reference information to your Skill directory. 
例えば、補足情報や参考情報を含むREFERENCE.mdファイルをSkillディレクトリに追加します。
Referencing it inSkill.mdwill help Claude decide if it needs to access that resource when executing the Skill. 
Skill.md内でそれを参照することで、ClaudeがSkillを実行する際にそのリソースにアクセスする必要があるかどうかを判断するのに役立ちます。

<!-- ここまで読んだ! -->

## 3. Adding Scripts スクリプトの追加

For more advanced Skills, attach executable code files to Skill.md, allowing Claude to run code. 
より高度なスキルのために、**実行可能なコードファイルをSkill.mdに添付**し、Claudeがコードを実行できるようにします。
For example, our document skills use the following programming languages and packages:
例えば、私たちのドキュメントスキルは以下のプログラミング言語とパッケージを使用します：

- Python (pandas, numpy, matplotlib)
- JavaScript/Node.js
- Packages to help with file editing
- visualization tools
- Python（pandas、numpy、matplotlib）
- JavaScript/Node.js
- ファイル編集を支援するパッケージ
- 可視化ツール

Note: Claude and Claude Code can install packages from standard repositories (Python PyPI, JavaScript npm) when loading Skills. 
注意：ClaudeとClaude Codeは、スキルを読み込む際に標準リポジトリ（Python PyPI、JavaScript npm）からパッケージをインストールできます。
It’s not possible to install additional packages at runtime with API Skills—all dependencies must be pre-installed in the container.
APIスキルでは、ランタイムで追加のパッケージをインストールすることはできません。すべての依存関係はコンテナ内に事前にインストールされている必要があります。

<!-- ここまで読んだ! -->

## 4. Packaging Your Skill スキルのパッケージング

Once your Skill folder is complete:
スキルフォルダが完成したら：

1. Ensure the folder name matches your Skill's name.
   1. フォルダ名がスキルの名前と一致していることを確認してください。
2. Create a ZIP file of the folder.
   1. フォルダのZIPファイルを作成します。
3. The ZIP should contain the Skill folder as its root (not a subfolder).
   1. ZIPには、スキルフォルダがルートとして含まれている必要があります（サブフォルダではありません）。

Correct structure:
正しい構造：

```bash
my-Skill.zip
└── my-Skill/
    ├── Skill.md
    └── resources/
```

Incorrect structure:
誤った構造：

```bash
my-Skill.zip
└── (files directly in ZIP root)
```  

<!-- ここまで読んだ! -->

## 5. Testing Your Skill スキルのテスト

### 5.1. Before Uploading アップロード前に

1. Review your Skill.md for clarity
   1. Skill.mdを明確さのためにレビューしてください。
2. Check that the description accurately reflects when Claude should use the Skill
   2. **説明がClaudeがスキルを使用すべきタイミングを正確に反映していること**を確認してください。
3. Verify all referenced files exist in the correct locations
   3. 参照されているすべてのファイルが正しい場所に存在することを確認してください。
4. Test with example prompts to ensure Claude invokes it appropriately
   4. 例のプロンプトを使用してテストし、Claudeが適切にそれを呼び出すことを確認してください。

### 5.2. After Uploading to Claude Claudeへのアップロード後に

1. Enable the Skill in Settings > Capabilities.
   1. 設定 > 機能 でスキルを有効にしてください。
2. Try several different prompts that should trigger it
   2. それをトリガーするはずのいくつかの異なるプロンプトを試してください。
3. Review Claude's thinking to confirm it's loading the Skill
   3. Claudeの思考をレビューして、スキルが読み込まれていることを確認してください。
4. Iterate on the description if Claude isn't using it when expected
   4. Claudeが期待通りに使用していない場合は、説明を繰り返し修正してください。

Note for Team and Enterprise plans: To make a skill available to all users in your organization, see Provisioning and managing Skills for your organization.
チームおよびエンタープライズプランに関する注意: スキルを組織内のすべてのユーザーが利用できるようにするには、組織のスキルのプロビジョニングと管理を参照してください。

<!-- ここまで読んだ! -->

## 6. Best Practices ベストプラクティス

- Keep it focused:Create separate Skills for different workflows. Multiple focused Skills compose better than one large Skill.
焦点を絞る:異なるワークフローのために別々のスキルを作成します。複数の焦点を絞ったスキルは、大きなスキルよりも優れた構成を持ちます。

- Write clear descriptions:Claude uses descriptions to decide when to invoke your Skill. Be specific about when it applies.
明確な説明を書く:Claudeは説明を使用して、スキルを呼び出すタイミングを決定します。適用されるタイミングについて具体的に記述してください。

- Start simple:Begin with basic instructions in Markdown before adding complex scripts. You can always expand on the Skill later.
**シンプルに始める:複雑なスクリプトを追加する前に、基本的な指示をMarkdownで始めます**。後でスキルを拡張することは常に可能です。

- Use examples:Include example inputs and outputs in your Skill.md file to help Claude understand what success looks like.
例を使用する:スキルの.mdファイルに例の入力と出力を含めて、Claudeが成功の姿を理解できるようにします。

- Test incrementally:Test after each significant change rather than building a complex Skill all at once.
段階的にテストする:複雑なスキルを一度に構築するのではなく、重要な変更の後にテストを行います。

- Skills can build on each other:While Skills can't explicitly reference other Skills, Claude can use multiple Skills together automatically. This composability is one of the most powerful parts of the Skills feature.
スキルは相互に構築できます:スキルは他のスキルを明示的に参照することはできませんが、**Claudeは複数のスキルを自動的に組み合わせて使用できます**。この組み合わせ可能性は、スキル機能の最も強力な部分の一つです。

- Review the open Agent Skills specification:Follow the guidelines at agentskills.io, so skills you create can work across platforms that adopt the standard.
オープンエージェントスキル仕様を確認する:agentskills.ioのガイドラインに従って、作成したスキルが標準を採用するプラットフォームで機能するようにします。

For a more in-depth guide to skill creation, refer to Skill authoring best practices in our Claude Docs.
スキル作成に関するより詳細なガイドについては、Claude Docsのスキル著作のベストプラクティスを参照してください。

<!-- ここまで読んだ! -->

## 7. Security Considerations セキュリティに関する考慮事項

- Exercise caution when adding scripts to your Skill.md file.
  - Skill.mdファイルにスクリプトを追加する際は注意してください。
- Don't hardcode sensitive information (API keys, passwords).
  - **機密情報（APIキー、パスワード）をハードコーディングしないでください。**
- Review any Skills you download before enabling them.
  - 有効にする前に、ダウンロードしたスキルを確認してください。
- Use appropriate MCP connections for external service access.
  - 外部サービスへのアクセスには適切なMCP接続を使用してください。

<!-- ここまで読んだ! -->

## 8. Example Skills to Reference 参照するための例スキル

Visit our repository on GitHub for example Skills you can use as templates: https://github.com/anthropics/skills/tree/main/skills.
GitHubのリポジトリを訪れて、テンプレートとして使用できる例スキルを確認してください: https://github.com/anthropics/skills/tree/main/skills。

<!-- ここまで読んだ! -->
