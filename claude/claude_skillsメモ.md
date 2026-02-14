## これは何??

- Claude Skillsを作成して活用する際のtipsなどを調査したメモ。

## 参考

- [必要な情報を段階的に渡す。Claude Skillsを使った"複雑な業務"の効率化](https://note.com/higu_engineer/n/n5c29b6077afb)
- [Equipping agents for the real world with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [How to create custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## ざっくりClaude Skillsとは??

- 2025年10月にリリースされた機能。
  - Claude Pro, Max, Team, Enterpriseプランのユーザが利用できる機能。
  - ざっくり「**タスク実行のためのリッチなプロンプトテンプレートを、フォルダ構造として整理しておける仕組み**」!

- 従来のスラッシュコマンドやgpts等との違い:
  - テンプレートという意味ではスラッシュコマンド等も同様。
  - しかしこれらの手法の欠点:
    - タスクが複雑になるほどプロンプトが肥大化。
    - -> コンテキストウィンドウを圧迫。
    - -> 結果としてハルシネーションしたり、必要な情報を渡しきれなかったりした。
  - Claude Skillsはこの問題を解決するために...
    - "プロンプトに全部書く"代わりに、業務の前提やワークフロー、注意点、コード例などを**ファイルシステム上でフォルダとして整理し、それぞれを独立したファイルとして保存できる仕組み**になってる。

- Claude Skillsの便利ポイント: 
  - 1. Skillsは**Progressive Disclosure(段階的な情報開示)**の仕組みで動く。
    - Progressive Disclosureって?
      - 人がマニュアルを読むときに「まず目次だけを見て、必要になったら該当箇所を読み、もっと必要なら付録を見る」というプロセスに近い動き。
      - Claude Skillsも同様に、「まずSkillの**メタデータ(name/description)だけを見て**、そのSkillが必要になった瞬間だけSKILL.mdの全文を読み込み、更に必要な場合にのみ追加ファイルやスクリプトを参照する」みたいな動きになる。
    - この仕組みにより、**コンテキストウィンドウを「本当に必要なタイミングで、本当に必要な量」だけ使える**ようになる!
  - 2. チーム内で共有しやすい!
    - Skillsは単なるファイル群としてフォルダに格納されてるので、**チーム内での共有やバージョン管理も簡単。**
    - Claudeの各プロダクト(Claude Code, Claude App, API, Agent SDK)から利用できるので、用途に応じて統一的に活用できる。
