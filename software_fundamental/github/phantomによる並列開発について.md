refs: https://github.com/aku11i/phantom

## 1. Phantomによる並列開発について

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

## 2. tmux連携による複数作業ディレクトリの分割画面の表示!

- tmux連携を使うことで「複数作業ディレクトリ（ワークツリー）を一気に分割画面で表示＆操作」できる。
  - つまり、AブランチもBブランチもCブランチも、1画面でそれぞれ別ウィンドウで表示できる...!:thinking:

### 2.1. そもそも「tmux」って?

- 正式には「**Terminal Multiplexer**」の略。**1つのターミナルから複数の「擬似ターミナル」を作成できる**。
  - 1つのターミナルで、複数の作業スペースやウィンドウを切り替えたり分割表示できる!
- Tmuxに登場する概念:
  - 1. **セッション**:
    - `tmux`を起動すると生成されるもの。
    - セッションごとに状態を維持できる。
  - 2. **ウィンドウ**:
    - **1つのセッションには、複数のウィンドウを持つことができる**。(MacBookでいう`cmd+T`を押すような感覚。複数のタブを持てるイメージ)
  - **ペイン**:
    - 「枠」「区画」を意味する。
    - 1つのウィンドウには、複数のペインを持つことができる。
    - 画面分割のようなもの。

#### 2.1.1. Tmuxの基本的な操作:

- `tmux`コマンドでセッションを開始。
- tmuxセッション内で各種コマンドを入力するには、最初にprefix keyを入力する必要がある。
  - デフォルトでは`Ctrl + b`がprefix key。
- 代表的なキー(コマンド):
  - `{ウィンドウ番号}`: 指定したウィンドウに切り替え。
    - 現在どのウィンドウにいるかは、画面下部に表示される。`*`がついてる番号が現在のウィンドウ。
  - `c`: 新しいウィンドウを作成。
  - `s`: セッションの一覧を表示
  - `w`: ウィンドウの一覧を表示
  - `d`: セッションをデタッチ(一時的に離れる)
  - `&`: ウィンドウの破棄。
  - `fg`: tmuxに復帰。
  - `x`: ペインの破棄。
  - `ctrl + z`: tmuxのセッションを一時停止。
  - ペインの分割
    - `"`: 上下にペイン分割。
    - `%`: 左右にペイン分割。
    - `o`: ペインを順番に移動。
    - `;`: 以前のペインへ移動。
    - `exit`: ペインを終了。

### 2.2. phantomのtmux連携の使い方:

ワークツリーを新規作成してtmuxで開く:

```shell
tmux
# ワークツリーを新規作成して、新しいtmuxウィンドウでfeature-xブランチの作業ディレクトリが開く。
phantom create <branch-name> --tmux
# ワークツリーを新規作成して、既存tmuxウィンドウの新しい縦分割ペインでfeature-xブランチの作業ディレクトリが開く。
phantom create <branch-name> --tmux-vertical
# ワークツリーを新規作成して、既存tmuxウィンドウの新しい横分割ペインでfeature-xブランチの作業ディレクトリが開く。
phantom create <branch-name> --tmux-horizontal 
```

既存ワークツリーをtmuxで開く:

```shell
# 既存のワークツリーを新しいtmuxウィンドウで開く。
phantom shell <branch-name> --tmux
# 既存のワークツリーを既存のtmuxウィンドウの新しい縦分割ペインで開く。
phantom shell <branch-name> --tmux-vertical
# 既存のワークツリーを既存のtmuxウィンドウの新しい横分割ペインで開く。
phantom shell <branch-name> --tmux-horizontal
```
