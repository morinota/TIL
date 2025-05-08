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

## reusable prompt files　機能についてメモ

refs: https://code.visualstudio.com/docs/copilot/copilot-customization#_reusable-prompt-files-experimental

- GitHub Copilotで使える再利用可能なプロンプトを、markdownで管理する機能。
  - プロジェクトやチームでよく使う指示をテンプレ化して、効率的に使えるようにする。
- 主な特徴:
  - プロンプトのテンプレート化
  - ファイル参照機能
  - 階層化構造
  - 共有容易性
- 設定方法
  - その1: VSCodeの設定で"chat.promptFiles": trueを追加
  - その2: ワークスペースの`.github/prompts/`にプロンプトファイル `hoge.prompt.md`ファイルを作成
  - その3: プロンプト内容をmarkdown形式で記載
- 使い方のコツ:
  - コンテキスト追加：チャット画面で📎アイコン→「Prompt...」から選択
  - 複数ファイル連携: プロンプト内で別の `.prompt.md`ファイルを参照することができる。
  - 変数活用: `#file`や`#folder`を使って、関連ファイルを自動読み込みできる。
