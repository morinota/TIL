## refs:

- [【Git】cherry-pickで解決](https://qiita.com/okmtz/items/62aa5a25f75b1754a861)
- [git cherry-pickを使用し、Pull Requestを分割する](https://zenn.dev/yussak/articles/cb2009247e89f6)
- [PRを小さく保つための、commit管理3TIPS](https://rabspice.hatenablog.com/entry/2022/01/31/224357)

# Git cherry-pickとは?

- cherry-pick = 気に入ったものだけをつまみ食いする, えり好みして選ぶ、の意味。
- `git cherry-pick` は、あるブランチの特定のコミットを現在のブランチに取り込むことができる

ex. ブランチaにブランチbのコミットX, Yのみを取り込みたいとする。

まずブランチaに移動。
(**注意: 分割先のブランチaは、分割元であるブランチbから派生させてしまうとその差分が全て入ってしまうので、それが入っていないmainブランチなどから派生させる...!**)
(例えば `git checkout origin/main -b a`で、origin/mainを起点としてブランチ作成するなど.)

```bash
$ git checkout a
```

下記のようにmergeしてしまうと、ブランチbの全てのコミットを取り込んでしまう。

```bash
git checkout a
git merge b
```

一方で、下記のようにcherry-pickすると、ブランチbのコミットX, Yのみを取り込むことができる。

```bash
git cherry-pick XのコミットID YのコミットID
```

## conflictが発生した場合

- 当然だが、cherry-pickコマンドもconflictが発生する場合もある。(mergeやrebaseと同様)
  - 現在のブランチのcodebaseと、cherry-pickしたコミットの変更が競合する場合に起こる。
    - そりゃそうだ...! **でもまあ肥大したPR分割の用途で使う場合、基本`origin/main`ブランチから差分のない状態でfcheckoutするので、conflictが発生することはあまりないかも**...?:thinking:
  - gitはどちらの変更を優先すべきか判断がつかないため、手動で解決する必要がある。

## conventional commit と cherry-pickの関連

- 「なんとなくでも良いので、convetional commit の仕様に従ってcommitを作ると良さそう...!」という話:
  - conventional commit の仕様を意識すると、commit メッセージが分かりやすくなるだけでなく、commitに含まれる差分が整理され、**各commit の内容自体が疎結合になっていく**。
  - 「タイトルが綺麗につけられる = commit 内容の意図がはっきりしている」なので、1つのcommitに複数の意図を持つ差分を含めることができなくなる。
  - そして、convetional commit に従ってcommitを分割していくと、単独で切り出してcherry-pickで別ブランチに移すことが容易になる...!
  - -> 意図せず差分が大きくなった時に、PRを分割するのが簡単になる...!
  - conventional commit自体は、レビュワーや将来commitを見る人がcommitの内容を理解しやすくすることが1番のモチベーションのようだが、**これを意識することでcommit自体を綺麗に整理するクセを自然と身につけられるのが素晴らしい...!**

```bash
 <type>[optional scope]: <description>
# ex.
 feat(api): メッセージ取得APIの実装
 fix(app): コメント数がおかしかったのを修正
 test(web): 爆発テストを作成
 docs: コンポーネントについてのコード規約を作成
```
