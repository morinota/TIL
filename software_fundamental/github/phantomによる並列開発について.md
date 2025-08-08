refs: https://github.com/aku11i/phantom

## Phantomによる並列開発について

- Phantomって?
  - Gitのworktreeを超絶カンタン＆直感的に管理できるCLIツール。
    - → 複数の開発作業も同時進行でサクサク進められるようになる...!:thinking:
  - Gitのworktreeって？
    - Gitの単一リポジトリを複数の作業ツリーで同時に操作できる機能。
- 基本的な使い方:
  - (以下のコマンドは全て、並列作業したいリポジトリ内で行うイメージ!)
  - その1: `phantom create <branch-name>`: 新しいworktreeを作成し、指定したブランチに切り替える。
    - ポイント: ブランチ名=worktree名でシンプルに管理できる! 直接 git worktree add するよりも、ブランチ名を意識して管理できるのが良い...!:thinking:
    
  - その2: `phantom list: 現在のworktreeの一覧を表示する。
  - その3: `phantom shell <branch-name>`: 作ったworktreeにシェルで入る
    
  - その4: `phantom exec <ブランチ名> <コマンド>`: 指定したブランチのworktreeで、任意のコマンドを実行する。ex. `phantom exec feature-x npm run build`
  - その5: `phantom delete <branch-name>`: 使い終わったらworktreeを削除する。

- 便利な機能:
  - VS CodeやCursor連携で、worktreeごとにエディタをすぐ開けるらしい。
    - ex. `phantom create feature-x --exec "code ."`
    - 既存のworktreeを開く場合は、`phantom exec <branch-name> code .`で開ける。
  - **fzf連携により、worktreeの選択も楽にできる**らしい!
    -  ex. `phantom shell --fzf`
