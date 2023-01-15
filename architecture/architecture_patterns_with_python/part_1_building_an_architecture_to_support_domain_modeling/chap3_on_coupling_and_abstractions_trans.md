# Chapter 3. A Brief Interlude: On Coupling and Abstractions 第3章 束の間の間奏曲 カップリングと抽象化について

Allow us a brief digression on the subject of abstractions, dear reader.
読者の皆さん、「抽象化」というテーマについて、少し余談をさせてください。
We’ve talked about abstractions quite a lot.
私たちは抽象化について何度も話してきました。
The Repository pattern is an abstraction over permanent storage, for example.
例えばRepositoryパターンは永続的なストレージを抽象化したものです。
But what makes a good abstraction?
しかし、良い抽象化とは何でしょうか？
What do we want from abstractions?
私たちは抽象化に何を求めているのだろうか？
And how do they relate to testing?
そしてそれらはどのようにテストと関係するのだろうか？

- TIP ヒント

The code for this chapter is in the chapter_03_abstractions branch on GitHub:
この章のコードは、GitHubのchapter_03_abstractionsブランチにあります。

A key theme in this book, hidden among the fancy patterns, is that we can use simple abstractions to hide messy details.
本書の主要テーマは、派手なパターンに隠れていますが、単純な抽象化を使って厄介な細部を隠せるということです。
When we’re writing code for fun, or in a kata,1 we get to play with ideas freely, hammering things out and refactoring aggressively.
遊びでコードを書いているときや、型にはまったコードを書いているときは、自由にアイデアを出し合い、積極的にリファクタリングしていくことができます。
In a large-scale system, though, we become constrained by the decisions made elsewhere in the system.
しかし、大規模なシステムでは、システム内の他の場所で行われた決定によって制約を受けることになります。

When we’re unable to change component A for fear of breaking component B, we say that the components have become coupled.
コンポーネントBが壊れるのを恐れて、コンポーネントAを変更できなくなったとき、そのコンポーネントは結合していると言います。
Locally, coupling is a good thing: it’s a sign that our code is working together, each component supporting the others, all of them fitting in place like the gears of a watch.
局所的には、結合は良いことです。それは、コードが協調して動作し、各コンポーネントが他のコンポーネントをサポートし、すべてのコンポーネントが時計の歯車のように所定の位置に収まっていることの証しです。
In jargon, we say this works when there is high cohesion between the coupled elements.
専門用語では、結合された要素の間に高い結合力がある場合に、このような動作になると言います。

Globally, coupling is a nuisance: it increases the risk and the cost of changing our code, sometimes to the point where we feel unable to make any changes at all.
グローバルに見ると、カップリングは厄介なものです。コードを変更するリスクとコストが増加し、時にはまったく変更できなくなることもあります。
This is the problem with the Ball of Mud pattern: as the application grows, if we’re unable to prevent coupling between elements that have no cohesion, that coupling increases superlinearly until we are no longer able to effectively change our systems.
これはBall of Mudパターンの問題点である。アプリケーションが成長するにつれて、結合力のない要素間の結合を防ぐことができなければ、結合は超線形に増加し、もはやシステムを効果的に変更することができなくなるのである。

We can reduce the degree of coupling within a system (Figure 3-1) by abstracting away the details (Figure 3-2).
詳細を抽象化することで、システム内の結合の度合い（図3-1）を減らすことができる（図3-2）。

![Figure 3-1. Lots of coupling](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0301.png)

![Figure 3-2. Less coupling](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0302.png)

In both diagrams, we have a pair of subsystems, with one dependent on the other.
どちらの図でも、一組のサブシステムがあり、一方が他方に依存している。
In Figure 3-1, there is a high degree of coupling between the two; the number of arrows indicates lots of kinds of dependencies between the two.
図3-1では、両者の間に高度な結合がある。矢印の数は、両者の間に多くの種類の依存関係があることを示している。
If we need to change system B, there’s a good chance that the change will ripple through to system A.
システムBを変更する必要がある場合、その変更がシステムAに波及する可能性が高い。

In Figure 3-2, though, we have reduced the degree of coupling by inserting a new, simpler abstraction.
しかし、図3-2では、より単純な新しい抽象化を挿入することで、結合の度合いを減らしている。
Because it is simpler, system A has fewer kinds of dependencies on the abstraction.
より単純であるため、システムAは抽象化されたものへの依存度が低くなっています。
The abstraction serves to protect us from change by hiding away the complex details of whatever system B does—we can change the arrows on the right without changing the ones on the left.
抽象化は、システムBが何をするにしても、その複雑な詳細を隠蔽することで、私たちを変化から守る役割を果たします。

## Abstracting State Aids Testability ステートの抽象化がテスト容易性を向上させる

Let’s see an example.
例を見てみましょう。
Imagine we want to write code for synchronizing two file directories, which we’ll call the source and the destination:
2つのファイル・ディレクトリ（ここではソースとデスティネーションと呼ぶ）を同期させるコードを書きたいとします。

- If a file exists in the source but not in the destination, copy the file over. 

- If a file exists in the source, but it has a different name than in the destination, rename the destination file to match. ソースにファイルが存在し、それがデスティネーションと異なる名前である場合、デスティネーションファイルの名前を一致するように変更します。

- If a file exists in the destination but not in the source, remove it. デスティネーションに存在し、ソースに存在しないファイルがある場合、それを削除します。

Our first and third requirements are simple enough: we can just compare two lists of paths.
1番目と3番目の条件は簡単で、2つのパスのリストを比較すればよいのです。
Our second is trickier, though.
しかし、2番目の要件はより厄介です。
To detect renames, we’ll have to inspect the content of files.
リネームを検出するためには、ファイルの内容を検査する必要があります。
For this, we can use a hashing function like MD5 or SHA-1.
これには、MD5やSHA-1などのハッシュ関数を使用します。
The code to generate a SHA-1 hash from a file is simple enough:
ファイルからSHA-1ハッシュを生成するコードはとてもシンプルです。

Hashing a file (sync.py)
ファイルのハッシュ化(sync.py)

```python
BLOCKSIZE = 65536
def hash_file(path):
hasher = hashlib.sha1()
with path.open("rb") as file:
buf = file.read(BLOCKSIZE)
while buf:
hasher.update(buf)
buf = file.read(BLOCKSIZE)
return hasher.hexdigest()
```

Now we need to write the bit that makes decisions about what to do—the business logic, if you will.
あとは、何をすべきかを判断するビジネスロジックを書けばいい。

When we have to tackle a problem from first principles, we usually try to write a simple implementation and then refactor toward better design.
ある問題に第一原理から取り組まなければならないとき、私たちは通常、単純な実装を書き、より良い設計に向けてリファクタリングすることを試みます。
We’ll use this approach throughout the book, because it’s how we write code in the real world: start with a solution to the smallest part of the problem, and then iteratively make the solution richer and better designed.
本書では、実世界でのコードの書き方として、この方法を用います。問題の最小限の部分に対する解決策から始めて、その解決策を繰り返しより豊かに、より良く設計するのです。

Our first hackish approach looks something like this:
最初のハック的なアプローチは、次のようなものです。

Basic sync algorithm (sync.py)
基本的な同期アルゴリズム(sync.py)

```python
import hashlib
import os
import shutil
from pathlib import Path
def sync(source, dest):
# Walk the source folder and build a dict of filenames and their hashes
source_hashes = {}
for folder, _, files in os.walk(source):
for fn in files:
source_hashes[hash_file(Path(folder) / fn)] = fn
seen = set()  # Keep track of the files we've found in the target
# Walk the target folder and get the filenames and hashes
for folder, _, files in os.walk(dest):
for fn in files:
dest_path = Path(folder) / fn
dest_hash = hash_file(dest_path)
seen.add(dest_hash)
# if there's a file in target that's not in source, delete it
if dest_hash not in source_hashes:
dest_path.remove()
# if there's a file in target that has a different path in source,
# move it to the correct path
elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])
# for every file that appears in source but not target, copy the file to
# the target
for src_hash, fn in source_hashes.items():
if src_hash not in seen:
shutil.copy(Path(source) / fn, Path(dest) / fn)
```

Fantastic!
ファンタスティック
We have some code and it looks OK, but before we run it on our hard drive, maybe we should test it.
でも、ハードディスクで実行する前に、テストしたほうがいいかもしれませんね。
How do we go about testing this sort of thing?
この種のテストはどのように行うのでしょうか？

Some end-to-end tests (test_sync.py)
いくつかのエンドツーエンドのテスト(test_sync.py)

```python
def test_when_a_file_exists_in_the_source_but_not_the_destination():
try:
source = tempfile.mkdtemp()
dest = tempfile.mkdtemp()
content = "I am a very useful file"
(Path(source) / 'my-file').write_text(content)
sync(source, dest)
expected_path = Path(dest) /  'my-file'
assert expected_path.exists()
assert expected_path.read_text() == content
finally:
shutil.rmtree(source)
shutil.rmtree(dest)
def test_when_a_file_has_been_renamed_in_the_source():
try:
source = tempfile.mkdtemp()
dest = tempfile.mkdtemp()
content = "I am a file that was renamed"
source_path = Path(source) / 'source-filename'
old_dest_path = Path(dest) / 'dest-filename'
expected_dest_path = Path(dest) / 'source-filename'
source_path.write_text(content)
old_dest_path.write_text(content)
sync(source, dest)
assert old_dest_path.exists() is False
assert expected_dest_path.read_text() == content
finally:
shutil.rmtree(source)
shutil.rmtree(dest)
```

Wowsers, that’s a lot of setup for two simple cases!
うわー、2つの単純なケースのために、たくさんのセットアップが必要ですね。
The problem is that our domain logic, “figure out the difference between two directories,” is tightly coupled to the I
問題は、「2つのディレクトリの違いを調べる」というドメインロジックが、Intel(R)モジュールと緊密に結合していることです。

And the trouble is, even with our current requirements, we haven’t written enough tests: the current implementation has several bugs (the `shutil.move()` is wrong, for example).
困ったことに、現在の要件でさえも十分なテストが書かれていません。現在の実装にはいくつかのバグがあります (たとえば `shutil.move()` は間違っています)。
Getting decent coverage and revealing these bugs means writing more tests, but if they’re all as unwieldy as the preceding ones, that’s going to get real painful real quickly.
現在の実装にはいくつかのバグがあります (たとえば `shutil.move() ` は間違っています)。きちんとしたカバレッジを確保してこれらのバグを明らかにするには、さらにテストを書く必要があります。

On top of that, our code isn’t very extensible.
その上、私たちのコードはあまり拡張性がありません。
Imagine trying to implement a `--dry-run` flag that gets our code to just print out what it’s going to do, rather than actually do it.
例えば、`--dry-run`フラグを実装して、実際に実行するのではなく、実行しようとしていることを出力するだけのコードにしようとすることを想像してみてください。
Or what if we wanted to sync to a remote server, or to cloud storage?
あるいは、リモート・サーバーやクラウド・ストレージに同期させたいとしたらどうだろう？

Our high-level code is coupled to low-level details, and it’s making life hard.
高水準のコードが低水準の詳細と結合し、生活を困難にしています。
As the scenarios we consider get more complex, our tests will get more unwieldy.
考慮するシナリオがより複雑になればなるほど、テストはより扱いにくくなります。
We can definitely refactor these tests (some of the cleanup could go into pytest fixtures, for example) but as long as we’re doing filesystem operations, they’re going to stay slow and be hard to read and write.
これらのテストをリファクタリングすることは可能ですが (たとえば pytest のフィクスチャにクリーンナップすることもできます)、 ファイルシステム操作を行う限り、テストは遅く、読み書きが困難なままです。

## Choosing the Right Abstraction(s) 正しい抽象化の選択

What could we do to rewrite our code to make it more testable?
もっとテストしやすいコードに書き換えるには、どうしたらいいのだろう？

First, we need to think about what our code needs from the filesystem.
まず、私たちのコードがファイルシステムから何を必要としているかを考える必要があります。
Reading through the code, we can see that three distinct things are happening.
このコードを読むと、3つの異なることが起こっていることがわかります。
We can think of these as three distinct responsibilities that the code has:
これらは、コードが持つ3つの異なる責任と考えることができます。

1. We interrogate the filesystem by using os.walk and determine hashes for a series of paths. This is similar in both the source and the destination cases. os.walkを使ってファイルシステムを照会し、一連のパスのハッシュを決定する。 これは送信元、送信先のいずれの場合も同様である。

2. We decide whether a file is new, renamed, or redundant. ファイルが新規か、リネームか、冗長かを判断します。

3. We copy, move, or delete files to match the source. ソースに合わせて、ファイルをコピー、移動、削除しています。

Remember that we want to find simplifying abstractions for each of these responsibilities.
私たちは、このような各責任を簡略化したものを見つけたいと考えていることを忘れないでください。
That will let us hide the messy details so we can focus on the interesting logic.2
そうすることで、面倒な細部を隠して、興味深い論理に集中することができます2。

- NOTE 注

- In this chapter, we’re refactoring some gnarly code into a more testable structure by identifying the separate tasks that need to be done and giving each task to a clearly defined actor, along similar lines to the `duckduckgo` example. この章では、`duckduckgo`の例と同様に、実行する必要のある個別のタスクを特定し、各タスクを明確に定義されたアクターに与えることによって、いくつかの厄介なコードをよりテストしやすい構造にリファクタリングしています。

For steps 1 and 2, we’ve already intuitively started using an abstraction, a dictionary of hashes to paths.
ステップ1と2では、すでに直感的に、パスに対するハッシュの辞書という抽象的なものを使い始めています。
You may already have been thinking, “Why not build up a dictionary for the destination folder as well as the source, and then we just compare two dicts?”
すでに、"コピー元と同様にコピー先のフォルダについても辞書を構築して、2つの辞書を比較すればいいのでは？"と考えている人もいるかもしれません。
That seems like a nice way to abstract the current state of the filesystem:
それは、ファイルシステムの現在の状態を抽象化する良い方法のように思えます。

```python
source_files = {'hash1': 'path1', 'hash2': 'path2'}
dest_files = {'hash1': 'path1', 'hash2': 'pathX'}
```

What about moving from step 2 to step 3?
ステップ2からステップ3への移動はどうするか？
How can we abstract out the actual move
実際の引越しをどのように抽象化するか

We’ll apply a trick here that we’ll employ on a grand scale later in the book.
ここでは、この本の後半で大々的に採用することになるトリックを適用します。
We’re going to separate what we want to do from how to do it.
やりたいことと、それをやる方法を分離するのです。
We’re going to make our program output a list of commands that look like this:
このプログラムでは、次のようなコマンドのリストを出力するようにします。

```python
("COPY", "sourcepath", "destpath"),
("MOVE", "old", "new"),
```

Now we could write tests that just use two filesystem dicts as inputs, and we would expect lists of tuples of strings representing actions as outputs.
これで、2つのファイルシステムディクショナを入力とするテストを書くことができ、アクションを表す文字列のタプルのリストが出力として期待できます。

Instead of saying, “Given this actual filesystem, when I run my function, check what actions have happened,” we say, “Given this abstraction of a filesystem, what abstraction of filesystem actions will happen?”
"この実際のファイルシステムが与えられたとき、私の関数を実行したら、どんなアクションが起こったかをチェックする "のではなく、"このファイルシステムの抽象化が与えられたとき、どんなファイルシステムのアクションの抽象化が起こるか "と言うのです。

Simplified inputs and outputs in our tests (test_sync.py)
テストにおける入出力の簡略化 (test_sync.py)

```python
def test_when_a_file_exists_in_the_source_but_not_the_destination():
src_hashes = {'hash1': 'fn1'}
dst_hashes = {}
expected_actions = [('COPY', '/src/fn1', '/dst/fn1')]
...
def test_when_a_file_has_been_renamed_in_the_source():
src_hashes = {'hash1': 'fn1'}
dst_hashes = {'hash1': 'fn2'}
expected_actions == [('MOVE', '/dst/fn2', '/dst/fn1')]
...
```

## Implementing Our Chosen Abstractions 選んだ抽象概念を実装する

That’s all very well, but how do we actually write those new tests, and how do we change our implementation to make it all work?
しかし、実際にどのように新しいテストを書き、どのように実装を変更すれば、すべてがうまくいくのでしょうか。

Our goal is to isolate the clever part of our system, and to be able to test it thoroughly without needing to set up a real filesystem.
私たちの目標は、システムの賢い部分を分離し、実際のファイルシステムをセットアップする必要なく、徹底的にテストできるようにすることです。
We’ll create a “core” of code that has no dependencies on external state and then see how it responds when we give it input from the outside world (this kind of approach was characterized by Gary Bernhardt as Functional Core, Imperative Shell, or FCIS).
外部の状態に依存しないコードの「コア」を作り、外部からの入力を与えたときにどう反応するかを見るのです（この種のアプローチは、Gary BernhardtによってFunctional Core, Imperative ShellまたはFCISとして特徴づけられました）。

Let’s start off by splitting the code to separate the stateful parts from the logic.
まずは、ステートフルな部分とロジックを分離するために、コードを分割してみましょう。

And our top-level function will contain almost no logic at all; it’s just an imperative series of steps: gather inputs, call our logic, apply outputs:
そして、トップレベルの関数にはほとんどロジックがありません。入力を集め、ロジックを呼び出し、出力を適用するという一連の命令的なステップに過ぎません。

Split our code into three (sync.py)
コードを3つに分割する (sync.py)

```python
def sync(source, dest):
# imperative shell step 1, gather inputs
source_hashes = read_paths_and_hashes(source)  1
dest_hashes = read_paths_and_hashes(dest)  1
# step 2: call functional core
actions = determine_actions(source_hashes, dest_hashes, source, dest)  2
# imperative shell step 3, apply outputs
for action, *paths in actions:
if action == 'copy':
shutil.copyfile(*paths)
if action == 'move':
shutil.move(*paths)
if action == 'delete':
os.remove(paths[0])
```

1. Here’s the first function we factor out, `read_paths_and_hashes()`, which isolates the I/O part of our application. ここで、最初に因数分解した関数 `read_paths_and_hashes()` は、I.S.S.S.S.S.を分離しています。

2. Here is where carve out the functional core, the business logic. ここでは、機能的なコアとなるビジネスロジックを切り出します。

The code to build up the dictionary of paths and hashes is now trivially easy to write:
パスとハッシュの辞書を構築するコードは、今では些細なことで簡単に書けるようになった。

A function that just does I
I を行うだけの関数

```python
def read_paths_and_hashes(root):
hashes = {}
for folder, _, files in os.walk(root):
for fn in files:
hashes[hash_file(Path(folder) / fn)] = fn
return hashes
```

The `determine_actions()` function will be the core of our business logic, which says, “Given these two sets of hashes and filenames, what should we copy
determine_actions()`関数はビジネスロジックの核となるもので、「これら二つのハッシュとファイル名のセットが与えられたら、何をコピーするべきか」というものです。

A function that just does business logic (sync.py)
ビジネスロジックを行うだけの関数(sync.py)

```python
def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
for sha, filename in src_hashes.items():
if sha not in dst_hashes:
sourcepath = Path(src_folder) / filename
destpath = Path(dst_folder) / filename
yield 'copy', sourcepath, destpath
elif dst_hashes[sha] != filename:
olddestpath = Path(dst_folder) / dst_hashes[sha]
newdestpath = Path(dst_folder) / filename
yield 'move', olddestpath, newdestpath
for sha, filename in dst_hashes.items():
if sha not in src_hashes:
yield 'delete', dst_folder / filename
```

Our tests now act directly on the `determine_actions()` function:
これで、テストは `determine_actions()` 関数に直接作用するようになりました。

Nicer-looking tests (test_sync.py)
より洗練されたテスト (test_sync.py)

```python
def test_when_a_file_exists_in_the_source_but_not_the_destination():
src_hashes = {'hash1': 'fn1'}
dst_hashes = {}
actions = determine_actions(src_hashes, dst_hashes, Path('/src'), Path('/dst'))
assert list(actions) == [('copy', Path('/src/fn1'), Path('/dst/fn1'))]
...
def test_when_a_file_has_been_renamed_in_the_source():
src_hashes = {'hash1': 'fn1'}
dst_hashes = {'hash1': 'fn2'}
actions = determine_actions(src_hashes, dst_hashes, Path('/src'), Path('/dst'))
assert list(actions) == [('move', Path('/dst/fn2'), Path('/dst/fn1'))]
```

Because we’ve disentangled the logic of our program—the code for identifying changes—from the low-level details of I
プログラムのロジック（変更を識別するコード）を、低レベルの詳細から切り離したので、I.

With this approach, we’ve switched from testing our main entrypoint function, `sync()`, to testing a lower-level function, `determine_actions()`.
このアプローチでは、メインのエントリポイント関数である `sync()` のテストから、より低レベルの関数である `determine_actions()` のテストに切り替わりました。
You might decide that’s fine because `sync()` is now so simple.
あなたは、`sync()`がとてもシンプルになったので、それでいいと思うかもしれません。
Or you might decide to keep some integration
あるいは、いくつかの統合を維持することにするかもしれません。

### Testing Edge to Edge with Fakes and Dependency Injection フェイクと依存性注入を用いたエッジ・トゥ・エッジのテスト

When we start writing a new system, we often focus on the core logic first, driving it with direct unit tests.
新しいシステムを書き始めるとき、私たちはしばしば最初にコアロジックに焦点を当て、それを直接ユニットテストで駆動させます。
At some point, though, we want to test bigger chunks of the system together.
しかし、ある時点で、システムのより大きな塊を一緒にテストしたくなることがあります。

We could return to our end-to-end tests, but those are still as tricky to write and maintain as before.
エンドツーエンドのテストに戻ることもできますが、それは以前と同じように書くのも維持するのも厄介です。
Instead, we often write tests that invoke a whole system together but fake the I
その代わりに、システム全体を呼び出すようなテストを書くことが多いのですが、その場合は I

Explicit dependencies (sync.py)
明示的な依存関係(sync.py)

```python
def sync(reader, filesystem, source_root, dest_root): 1
source_hashes = reader(source_root) 2
dest_hashes = reader(dest_root)
for sha, filename in src_hashes.items():
if sha not in dest_hashes:
sourcepath = source_root / filename
destpath = dest_root / filename
filesystem.copy(destpath, sourcepath) 3
elif dest_hashes[sha] != filename:
olddestpath = dest_root / dest_hashes[sha]
newdestpath = dest_root / filename
filesystem.move(olddestpath, newdestpath)
for sha, filename in dst_hashes.items():
if sha not in source_hashes:
filesystem.delete(dest_root/filename)
```

1. Our top-level function now exposes two new dependencies, a `reader` and a `filesystem`. トップレベルの関数は、2つの新しい依存関係、 `reader` と `filesystem` を公開するようになりました。

2. We invoke the `reader` to produce our files dict. 私たちは `reader` を呼び出して、ファイルの dict を生成します。

3. We invoke the `filesystem` to apply the changes we detect. 検出した変更を適用するために `filesystem` を呼び出します。

- TIP ヒント

- Although we’re using dependency injection, there is no need to define an abstract base class or any kind of explicit interface. In this book, we often show ABCs because we hope they help you understand what the abstraction is, but they’re not necessary. Python’s dynamic nature means we can always rely on duck typing. 依存性注入を使っていますが、抽象的な基底クラスや何らかの明示的なインターフェイスを定義する必要はありません。 この本では、ABCをよく示しますが、それは抽象化が何であるかを理解するのに役立つことを期待しているからですが、それは必要ありません。 Pythonの動的な性質は、私たちが常にダックタイピングに頼ることができることを意味します。

Tests using DI
DIを用いたテスト

```python
class FakeFileSystem(list): 1
def copy(self, src, dest): 2
self.append(('COPY', src, dest))
def move(self, src, dest):
self.append(('MOVE', src, dest))
def delete(self, dest):
self.append(('DELETE', src, dest))
def test_when_a_file_exists_in_the_source_but_not_the_destination():
source = {"sha1": "my-file" }
dest = {}
filesystem = FakeFileSystem()
reader = {"/source": source, "/dest": dest}
synchronise_dirs(reader.pop, filesystem, "/source", "/dest")
assert filesystem == [("COPY", "/source/my-file", "/dest/my-file")]
def test_when_a_file_has_been_renamed_in_the_source():
source = {"sha1": "renamed-file" }
dest = {"sha1": "original-file" }
filesystem = FakeFileSystem()
reader = {"/source": source, "/dest": dest}
synchronise_dirs(reader.pop, filesystem, "/source", "/dest")
assert filesystem == [("MOVE", "/dest/original-file", "/dest/renamed-file")]
```

1. Bob loves using lists to build simple test doubles, even though his coworkers get mad. It means we can write tests like `assert foo not in database`. Bob は同僚に怒られながらも、リストを使って簡単なテストダブルズを作るのが大好きです。 つまり、`assert foo not in database` のようなテストが書けるようになる。

2. Each method in our `FakeFileSystem` just appends something to the list so we can inspect it later. This is an example of a spy object. FakeFileSystem` の各メソッドはリストに何かを追加するだけなので、後で検査することができます。 これは、スパイオブジェクトの例です。

The advantage of this approach is that our tests act on the exact same function that’s used by our production code.
この方法の利点は、実運用コードで使われているのとまったく同じ関数でテストが動作することです。
The disadvantage is that we have to make our stateful components explicit and pass them around.
一方、デメリットは、ステートフルなコンポーネントを明示的に作成し、それを受け渡さなければならないことです。
David Heinemeier Hansson, the creator of Ruby on Rails, famously described this as “test-induced design damage.”
Ruby on Rails の開発者である David Heinemeier Hansson は、このことを "test-induced design damage" と表現して有名になりました。

In either case, we can now work on fixing all the bugs in our implementation; enumerating tests for all the edge cases is now much easier.
いずれにせよ、これで実装のバグをすべて修正することができます。すべてのエッジケースに対するテストを列挙することが、はるかに容易になりました。

### Why Not Just Patch It Out? なぜパッチで補修しないのか？

At this point you may be scratching your head and thinking, “Why don’t you just use `mock.patch` and save yourself the effort?
この時点で、あなたは頭をかきむしり、「なぜ `mock.patch` を使って手間を省かないのか」と考えているかもしれません。
"”
""

We avoid using mocks in this book and in our production code too.
この本ではモックを使わないようにしていますし、私たちのプロダクションコードでもモックを使っています。
We’re not going to enter into a Holy War, but our instinct is that mocking frameworks, particularly monkeypatching, are a code smell.
聖戦に突入するつもりはありませんが、私たちの直感では、モッキングフレームワーク、特にモンキーパッチはコードの臭いの元だと思います。

Instead, we like to clearly identify the responsibilities in our codebase, and to separate those responsibilities into small, focused objects that are easy to replace with a test double.
その代わりに、私たちは、コードベースの責任を明確に識別し、それらの責任を、テストダブルで簡単に置き換えられる、小さく焦点を絞ったオブジェクトに分離することを好みます。

- NOTE 注

- You can see an example in Chapter 8, where we `mock.patch()` out an email-sending module, but eventually we replace that with an explicit bit of dependency injection in Chapter 13. 第8章では、電子メール送信モジュールを `mock.patch()` で出力する例を見ることができますが、最終的には第13章で明示的な依存性注入に置き換えます。

We have three closely related reasons for our preference:
私たちが好む理由は、密接に関連する3つの理由です。

- Patching out the dependency you’re using makes it possible to unit test the code, but it does nothing to improve the design. Using `mock.patch` won’t let your code work with a `--dry-run` flag, nor will it help you run against an FTP server. For that, you’ll need to introduce abstractions. 使用している依存関係をパッチすることで、コードのユニットテストは可能になりますが、設計を改善するためには何もしません。 mock.patch`を使用しても、あなたのコードが `--dry-run` フラグで動作するようにはなりませんし、FTPサーバーに対して実行するのにも役に立ちません。 そのためには、抽象化したものを導入する必要があります。

- Tests that use mocks tend to be more coupled to the implementation details of the codebase. That’s because mock tests verify the interactions between things: did we call `shutil.copy` with the right arguments? This coupling between code and test tends to make tests more brittle, in our experience. モックを使用したテストは、コードベースの実装の詳細とより密接に関連する傾向があります。 なぜならモックテストは物事の相互作用を検証するものだからです。例えば、 `shutil.copy` を正しい引数でコールしたかどうか？ 私たちの経験では、このようなコードとテストの結合はテストをより脆弱にする傾向があります。

- Overuse of mocks leads to complicated test suites that fail to explain the code. モックの使いすぎは、コードを説明できない複雑なテストスイートにつながる。

- NOTE 注

- Designing for testability really means designing for extensibility. We trade off a little more complexity for a cleaner design that admits novel use cases. テスト容易性のための設計は、実際には拡張性のための設計を意味します。 私たちは、新しいユースケースを許容するすっきりとした設計のために、もう少し複雑さをトレードオフします。

- MOCKS VERSUS FAKES; CLASSIC-STYLE VERSUS LONDON-SCHOOL TDD 模擬と模倣、古典と倫敦のTDD

- Here’s a short and somewhat simplistic definition of the difference between mocks and fakes: ここでは、モックとフェイクの違いについて、簡単かつやや単純に定義しています。

- Mocks are used to verify how something gets used; they have methods like assert_called_once_with(). They’re associated with London-school TDD. モックは、何かがどのように使われるかを検証するために使われます。モックには assert_called_once_with() のようなメソッドがあります。 ロンドン流のTDDに関連しています。

- Fakes are working implementations of the thing they’re replacing, but they’re designed for use only in tests. They wouldn’t work “in real life”; our in-memory repository is a good example. But you can use them to make assertions about the end state of a system rather than the behaviors along the way, so they’re associated with classic-style TDD. 偽物は、置き換えようとしているものの実装が動作するものですが、テストにのみ使用するように設計されています。 インメモリリポジトリが良い例です。 しかし、システムの最終的な状態について、途中の動作ではなく、アサーションを行うために使用することができるので、古典的なスタイルのTDDに関連付けられます。

- We’re slightly conflating mocks with spies and fakes with stubs here, and you can read the long, correct answer in Martin Fowler’s classic essay on the subject called “Mocks Aren’t Stubs”. ここでは、モックとスパイ、フェイクとスタブを若干混同しています。正解は、Martin Fowlerの「Mocks Aren't Stubs」という古典的なエッセイに長々と書かれていますよ。

- It also probably doesn’t help that the MagicMock objects provided by unittest.mock aren’t, strictly speaking, mocks; they’re spies, if anything. But they’re also often used as stubs or dummies. There, we promise we’re done with the test double terminology nitpicks now. また、unittest.mock が提供する MagicMock オブジェクトは厳密にはモックではなく、どちらかというとスパイであることも、おそらく問題にはならないでしょう。 しかし、これらはスタブやダミーとして使われることもよくあります。 さて、これでテストダブルの用語の小ネタはおしまいです。

- What about London-school versus classic-style TDD? You can read more about those two in Martin Fowler’s article that we just cited, as well as on the Software Engineering Stack Exchange site, but in this book we’re pretty firmly in the classicist camp. We like to build our tests around state both in setup and in assertions, and we like to work at the highest level of abstraction possible rather than doing checks on the behavior of intermediary collaborators.3 ロンドン流のTDDと古典的なスタイルのTDDはどうでしょうか？ この二つについては、先ほど引用したMartin Fowlerの記事や、Software Engineering Stack Exchangeのサイトに詳しく書かれていますが、この本では、かなりしっかりと古典派の陣営に属しています。 私たちは、セットアップとアサーションの両方において、ステートを中心にテストを構築することを好みます。また、中間的な協力者の振る舞いをチェックするのではなく、できるだけ抽象度の高いレベルで作業することを好みます3。

- Read more on this in “On Deciding What Kind of Tests to Write”. これについては、「どのようなテストを書くかを決めるにあたって」で詳しく説明しています。

We view TDD as a design practice first and a testing practice second.
私たちはTDDを、第一に設計の実践、第二にテストの実践ととらえています。
The tests act as a record of our design choices and serve to explain the system to us when we return to the code after a long absence.
テストは設計上の選択の記録として機能し、久しぶりにコードに戻ったときにシステムを説明する役割を果たします。

Tests that use too many mocks get overwhelmed with setup code that hides the story we care about.
モックを多用するテストは、セットアップのコードで溢れかえり、肝心のストーリーが見えなくなってしまいます。

Steve Freeman has a great example of overmocked tests in his talk “Test-Driven Development”.
Steve Freemanは彼のトーク "Test-Driven Development" でオーバーモックテストの素晴らしい例を紹介しています。
You should also check out this PyCon talk, “Mocking and Patching Pitfalls”, by our esteemed tech reviewer, Ed Jung, which also addresses mocking and its alternatives.
また、我々の尊敬する技術評論家 Ed Jung による PyCon の講演 "Mocking and Patching Pitfalls" もチェックしてみてください、モッキングとその代替品について述べています。
And while we’re recommending talks, don’t miss Brandon Rhodes talking about “Hoisting Your I
そして、私たちが講演を推薦している間、Brandon Rhodesによる「Hoisting Your I」についての講演もお見逃しなく。

- TIP ヒント

- In this chapter, we’ve spent a lot of time replacing end-to-end tests with unit tests. That doesn’t mean we think you should never use E2E tests! In this book we’re showing techniques to get you to a decent test pyramid with as many unit tests as possible, and with the minimum number of E2E tests you need to feel confident. Read on to “Recap: Rules of Thumb for Different Types of Test” for more details. この章では、エンドツーエンドテストをユニットテストに置き換えることに多くの時間を費やしてきました。 だからといって、E2E テストを決して使ってはいけないというわけではありません。 この本では、できるだけ多くのユニットテストと、自信を持つために必要な最小限の E2E テストで、適切なテストピラミッドを作るためのテクニックを紹介しています。 続きを読む "まとめ" へ 詳細は、「さまざまな種類のテストに関する経験則」をご覧ください。

- SO WHICH DO WE USE IN THIS BOOK? FUNCTIONAL OR OBJECT-ORIENTED COMPOSITION? この本では、どちらを使うのでしょうか？ 関数型構成かオブジェクト指向構成か？

- Both. Our domain model is entirely free of dependencies and side effects, so that’s our functional core. The service layer that we build around it (in Chapter 4) allows us to drive the system edge to edge, and we use dependency injection to provide those services with stateful components, so we can still unit test them. 両方です。 ドメインモデルは依存関係や副作用が全くないもので、これが機能的なコアとなります。 その周りに構築するサービス層（第4章参照）により、システムをエッジからエッジまで動かすことができます。また、依存性注入を使用して、これらのサービスにステートフルなコンポーネントを提供するので、ユニットテストを行うことができます。

- See Chapter 13 for more exploration of making our dependency injection more explicit and centralized. 依存性注入をより明示的かつ集中的に行う方法については、第13章を参照してください。

## Wrap-Up まとめ

We’ll see this idea come up again and again in the book: we can make our systems easier to test and maintain by simplifying the interface between our business logic and messy I
この本の中で何度も出てくるアイデアですが、ビジネスロジックと面倒なIBMの間のインターフェースを単純化することで、システムをより簡単にテスト・保守することができます。

- Can I choose a familiar Python data structure to represent the state of the messy system and then try to imagine a single function that can return that state? 面倒なシステムの状態を表すために、使い慣れたPythonのデータ構造を選び、その状態を返すことができる一つの関数を想像してみてはどうでしょうか。

- Where can I draw a line between my systems, where can I carve out a seam to stick that abstraction in? 自分のシステムのどこに線を引けばいいのか、どこに継ぎ目を刻めばその抽象的なものを突き刺すことができるのか。

- What is a sensible way of dividing things into components with different responsibilities? What implicit concepts can I make explicit? 物事を異なる責任を持つ構成要素に分割する賢明な方法とは？ どのような暗黙の概念を明示することができますか？

- What are the dependencies, and what is the core business logic? 依存関係はどうなっているのか、コアとなるビジネスロジックは何なのか。

Practice makes less imperfect!
練習すれば不完全なものはなくなる!
And now back to our regular programming…
では、いつもの番組に戻りましょう...

1. A code kata is a small, contained programming challenge often used to practice TDD. See “Kata—The Only Way to Learn TDD” by Peter Provost. コードの型とは、TDDの練習によく使われる、小さくて内容の濃いプログラミングの課題のことです。 Peter Provost著「Kata-The Only Way to Learn TDD」を参照してください。

2. If you’re used to thinking in terms of interfaces, that’s what we’re trying to define here. もし、あなたがインターフェースという言葉で考えることに慣れているなら、ここで定義しようとしているのはそのことです。

3. Which is not to say that we think the London school people are wrong. Some insanely smart people work that way. It’s just not what we’re used to. とはいえ、ロンドン校の人たちが間違っていると考えているわけではありません。 めちゃくちゃ頭のいい人は、そういう働き方をする人もいます。 ただ、私たちの常識とは違うのです。