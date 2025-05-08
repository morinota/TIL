## これは何?

- これは、GitHub Copilot Agent Modeに関するメモです。

## 用語の整理

- GitHub Copilot:
  - GitHub が提供する AI 機能全体を指す総称。
- GitHub Copilot の VScode 拡張:
  - Copilot と呼ぶとこの機能を指すことが多い。
- GitHub Copilot Edits:
  - AI によるコード生成、コード修正の機能、指定した範囲やファイルを読み込み、指示することでコードを生成する。リポジトリについて質問したり。
- GitHub Copilot Edits Agent mode:
  - Edits の機能に加えて、コンソールでのコマンド実行やその結果を自己解釈して半自動でコードを継続的に生成する。
  - 現在はVSCode insiderのみで提供されてる。

## Custom instructions (カスタム指示)　機能

- Copilot がコード生成やその他のタスクを行う際に、特定のコーディング規約やプロジェクトの要件に合わせた応答を得るために使用できる機能。
- VS Code では、コード生成、テスト生成、コードレビュー、コミットメッセージ生成、プルリクエストのタイトルと説明生成など、**いくつかの種類の custom instructions がサポートされてる**。
- custom instructions の設定方法2パターン:
  - その1: ワークスペースの `.github/copilot-instructions.md` ファイルを使用する。
    - github.copilot.chat.codeGeneration.useInstructionFiles 設定を true にする必要がある。
  - その2: VS Code の設定 (`settings.json`) に直接記述する。
- 

## reusable prompt files　機能についてメモ

refs: https://code.visualstudio.com/docs/copilot/copilot-customization#_reusable-prompt-files-experimental

- **完全なチャットプロンプトをmarkdown形式で記述しておき、チャット内で参照できる機能**。
  - Custom instructionsが既存のプロンプトを補足するのに対し、**プロンプトファイルはスタンドアロンのプロンプト**であり、ワークスペース内に保存して他のユーザーと共有できる。
- 主な特徴:
  - プロンプトのテンプレート化
  - ファイル参照機能
  - 階層化構造
  - 共有容易性
- プロンプトファイルは2種類:
  - ワークスペースプロンプトファイル
    - ワークスペースの `.github/prompts/` フォルダに直接`hoge.prompt.md`ファイルを作成するか、`Chat: Create Prompt`コマンドを使うこともできる。
    - chat.promptFilesLocations 設定で追加のプロンプトファイル場所を指定することも可能。
  - ユーザープロンプトファイル
    - 複数のワークスペースで利用可能。
    - `Chat: Create User Prompt`コマンドで作成できる。
    - ユーザプロンプトファイルは、Settings Sync を使用して、他のデバイスと同期できる。
  - どちらの種類のプロンプトファイルでも、他の`.prompt.md`ファイルを参照して階層構造を作成できる。
    - (この階層構造を使って、ワークフローを作れるのかな...? 各stepを定義した`.prompt.md`と、orchestrator的な役割の`.prompt.md`を作成して、呼び出し時にはorchestratorのプロンプトファイルを選択する、みたいな...!:thinking:)

- 一般的なユースケース
  - コード生成
  - ドメイン知識の共有
  - チームコラボレーション
  - オンボーディング

- 使い方は大きく2通り:
  - その1: Chatビューから「Add Context」ボタンをクリックして、「Prompts」から対象のプロンプトファイルを選択する。
  - その2: 「Chat: Use Prompt」コマンドを使用する。
  - 注目:
    - プロンプトファイルは、ask, edit, agentモードのいずれでも使用できる。
    - 必要に応じて、追加のコンテキストファイルを添付したり、チャットプロンプトに更に指示を含めたりできる。
    - **追加のコンテキスト不要で、そのままプロンプトファイルを使用する場合は、追加の指示なしで送信すれば良い**。
