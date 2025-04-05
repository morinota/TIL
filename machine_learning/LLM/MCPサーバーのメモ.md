## これは何?

- MCPサーバーがよくわからなかったので調べたメモです。

## refs

- https://zenn.dev/tomo0108/articles/6b472b4c9cacfa
- [MCP サーバーを自作して GitHub Copilot の Agent に可読性の低いクラス名を作ってもらう](https://zenn.dev/microsoft/articles/semantickernel-mcp4)

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
