# 1. chapter 3 :A Brief Interlude: On Coupling and Abstractions カップリングと抽象化について

抽象化というテーマについて少し余談.

例えばRepositoryパターンはpermanent storage(永続的なストレージ)を抽象化したもの.
しかし、良い抽象化とは何だろうか?
私たちは抽象化に何を求めているのだろうか？
そしてそれらはどのようにテストと関係するのだろうか？

本書の主要テーマは、**単純な抽象化を使って厄介な細部を隠せる**ということである(派手なパターンに隠れているが...).
遊びでコードを書いているときや、型にはまったコードを書いているときは、自由にアイデアを出し合い、積極的にリファクタリングしていくことができる.
しかし、大規模なシステムでは、システム内の他の場所で行われた決定によって制約を受けることになる.

コンポーネントBが壊れるのを恐れて、コンポーネントAを変更できなくなったとき、「**それらのコンポーネントはcoupling(結合)**している」と言う.
局所的には、結合は良いこと.それは、コードが協調して動作し、各コンポーネントが他のコンポーネントをサポートし、すべてのコンポーネントが時計の歯車のように所定の位置に収まっていることの証しである.

グローバルに見ると、Couplingは厄介なもの. コードを変更するリスクとコストが増加し、時にはまったく変更できなくなる事もある. アプリケーションが成長するにつれて、不要な要素間の結合を防ぐ事ができなければ、couplingは非線形に増加し、システムを効果的に変更できなくなってしまう...

詳細を抽象化することで、システム内の結合の度合い（図3-1）を減らすことができる（図3-2）

![Figure 3-1. Lots of coupling](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0301.png)

![Figure 3-2. Less coupling](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781492052197/files/assets/apwp_0302.png)

どちらの図でも、一組のサブシステムがあり、一方が他方に依存している.
図3-1では、両者の間に高度な結合がある。矢印の数は、両者の間に多くの種類の依存関係があることを示している. なのでシステムBを変更する必要がある場合、その変更がシステムAに波及する可能性は高い.

しかし、図3-2では、より単純な新しい抽象化を挿入することで、結合の度合いを減らしている. より単純であるため、システムAは抽象化されたものへの依存度が低くなっている. 抽象化は、システムBが何をするにしても、その複雑な詳細を隠蔽することで、システムAを変化から守る役割を果たす.

## 1.1. Abstracting State Aids Testability ステートの抽象化がテスト容易性を向上させる

例を見てみる.
2つのファイル・ディレクトリ（ここではソースとデスティネーションと呼ぶ）を同期させるコードを、以下の仕様に基づいて書きたいとする.

- コピー元に存在し、コピー先に存在しないファイルがある場合、そのファイルをコピーする.
- ソースにファイルが存在し、それがデスティネーションと異なる名前である場合、デスティネーションファイルの名前を一致するように変更する.
- デスティネーションに存在し、ソースに存在しないファイルがある場合、それを削除する.

1番目と3番目の条件は簡単で、2つのパスのリストを比較すればよい.
しかし2番目の要件は厄介で, リネームを検出するためには、ファイルの内容を検査する必要がある. これには、MD5やSHA-1などのハッシュ関数を使用し、ファイルから生成したハッシュを比較する.

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

あとは、何をすべきかを判断するビジネスロジックを書けばいい.
本書では、実世界でのコードの書き方として、「簡単な実装を書いてから、より良い設計に向けてリファクタリングする」方法を用いる. 問題の最小限の部分に対する解決策から始めて、その解決策をより豊かに、より良く設計することを繰り返していく.

```python
def sync(source: Path, dest: Path):
    """sourceとdestinationを同期する."""
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

            # if there's a file in target that's not in source, delete it (仕様3)
            if dest_hash not in source_hashes:
                dest_path.remove()

            # if there's a file in target that has a different path in source,
            # move it to the correct path(仕様2)
            elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])

    # for every file that appears in source but not target, copy the file to
    # the target(仕様1)
    for src_hash, fn in source_hashes.items():
        if src_hash not in seen:
            shutil.copy(Path(source) / fn, Path(dest) / fn)
```

ハードディスクで実行する前に、テストしたほうがいい.
いくつかのエンドツーエンドのテスト(test_sync.py)

```python
def test_when_a_file_exists_in_the_source_but_not_the_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "I am a very useful file"
        (Path(source) / "my-file").write_text(content)

        sync(source, dest)

        expected_path = Path(dest) / "my-file"
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
        source_path = Path(source) / "source-filename"
        old_dest_path = Path(dest) / "dest-filename"
        expected_dest_path = Path(dest) / "source-filename"
        source_path.write_text(content)
        old_dest_path.write_text(content)

        sync(source, dest)

        assert old_dest_path.exists() is False
        assert expected_dest_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
```

2つの単純なケースのために、たくさんのセットアップが必要...。
問題は、「2つのディレクトリの差を求める」というドメインロジックが、I/Oコードと緊密に結合していること...!!
`pathlib`, `shutil`, `hashlib` モジュールを呼び出さなければ、`sync`アルゴリズムを実行することができない事である!

**high-levelのコードがlow-levelの詳細と連動しており、変更(拡張)やテストを困難にしている**.

これらのテストをリファクタリングすることは可能だが(ex. pytest のフィクスチャにクリーンナップ)、ファイルシステム操作を行う限り、テストは遅く、読み書きは困難なまま.

## 1.2. Choosing the Right Abstraction(s) 正しい抽象化の選択

もっとテストしやすいコードに書き換えるには、どうしたらいいのか.

まず、私たちのコードがファイルシステムから何を必要としているかを考える必要がある.
このコードを読むと、**3つの異なることが起こっている**ことがわかる.
言い換えるとこれらは、コードが"**3つの異なる責任(responsibility)を持っている**"と考えることができる.

1. `os.walk`を使ってファイルシステムを照会し、一連のパスのハッシュを生成. これは送信元、送信先のいずれの場合も同様.
2. ファイルが新規か、リネームか、冗長かを判断.
3. ソースに合わせて、ファイルをコピー、移動、削除.

(重要)我々は、このような各responsibilityを簡略化したものを見つけたいと考えている...!!
そうすることで、面倒な細部を隠して、興味深い論理に集中できる.

- Note:
- この章では、**実行する必要のある個別のタスクを特定**し、**各タスクを明確に定義されたアクター(クラスや関数)に与える**ことによって、いくつかの厄介なコードをよりテストしやすい構造にリファクタリングしている.

ステップ1と2の移動では、{ハッシュ:パス}の辞書を使えば良い. (上のコードでも使い始めている)

```python
source_files = {'hash1': 'path1', 'hash2': 'path2'}
dest_files = {'hash1': 'path1', 'hash2': 'pathX'}
```

ステップ2からステップ3への移動はどうすべきか? ここでは、この本の後半で大々的に採用することになるトリックを適用する. "**やりたいことと、それをやる方法を分離**"するのである.
このプログラムでは、次のようなコマンドのリストを出力するようにする.

```python
("COPY", "sourcepath", "destpath"),
("MOVE", "old", "new"),
```

これで、2つのファイルシステムを表すdictを入力とするテストを書くことができ、アクションを表す文字列のタプルのリストが出力として期待できる.
"**実際のファイルシステム**が与えられたとき、私の関数を実行したら、**どんなアクションが起こったか**をチェックする "のではなく、"**ファイルシステムの抽象化されたモノが入力**された時、どんな**ファイルシステムのアクションの抽象化されたモノが出力**されるのか"と言い換える事ができる...!!

上の考え方を用いて、テストにおける入出力を以下の様に簡略化できる. (test_sync.py)

```python
    def test_when_a_file_exists_in_the_source_but_not_the_destination():
        src_hashes = {'hash1': 'fn1'}
        dst_hashes = {}
        expected_actions = [('COPY', '/src/fn1', '/dst/fn1')]
        ...

    def test_when_a_file_has_been_renamed_in_the_source():
        src_hashes = {'hash1': 'fn1'}
        dst_hashes = {'hash1': 'fn2'}
        expected_actions = [('MOVE', '/dst/fn2', '/dst/fn1')]
        ...
```

## 1.3. Implementing Our Chosen Abstractions 選んだ抽象概念を実装する

しかし、実際にどのように新しいテストを書き、どのように実装を変更すれば、すべてがうまくいくだろうか.

私たちの目標は、システムの賢い部分を分離し、**実際のファイルシステムをセットアップする必要なく**、徹底的にテストできるようにする事.
**外部の状態に依存しないコードの「コア」**を作り、外部からの入力を与えたときにどう反応するかを見る(?下のコード例を見るとわかりやすい！)のである（この種のアプローチは、Gary Bernhardtによって**Functional Core**, Imperative Shell、またはFCISと呼ばれている).

まずは、ステートフルな部分とロジックを分離するために、コードを分割してみよう.

コードを3つに分割する (sync.py)

```python
def sync(source:str, dest:str)->None:
    # imperative shell step 1, gather inputs
    source_hashes = read_paths_and_hashes(source) # 1. step 1の関数で I/O partを分離している.
    dest_hashes = read_paths_and_hashes(dest)  1

    # step 2: call functional core
    actions = determine_actions(source_hashes, dest_hashes, source, dest) # 2. ここで、functional core となるビジネスロジックを切り出す.

    # imperative shell step 3, apply outputs
    for action, *paths in actions:
        if action == 'copy':
            shutil.copyfile(*paths)
        if action == 'move':
            shutil.move(*paths)
        if action == 'delete':
            os.remove(paths[0])
```

A function that just does I/O (sync.py) I/O操作を行うだけの関数.

```python
def read_paths_and_hashes(root:str)->Dict[str, str]:
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes
```

`determine_actions()`関数はビジネスロジックを行うだけの関数 = functional core.

```python
def determine_actions(src_hashes:Dict[str, str], dst_hashes:Dict[str,str], src_folder:str, dst_folder:str)->Iterator[Tuple[str, str, str]]:
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

これで、テストは `determine_actions()` 関数に直接適用できるようになった.

より読みやすく拡張しやすいテスト(test_sync.py)

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

プログラムのロジック（変更を識別するコード）と, low-levelのI/Oの詳細を切り離したので、コードのコア(**functional core**)を簡単にテストできるようになった...!!

このアプローチでは、メインのエントリポイント関数( = high-level関数?)である `sync()` のテストから、よりlow-levelの関数である `determine_actions()` のテストに切り替えた.

### 1.3.1. Testing Edge to Edge with Fakes and Dependency Injection フェイクと依存性注入を用いたエッジ・トゥ・エッジのテスト

新しいシステムを書き始めるとき、私たちはしばしば最初にコアロジック(functional core)に焦点を当て、それを直接ユニットテストで駆動させる.
しかし、ある時点で、システムの大きな塊を一緒にテストしたいと思うようになる.

end-to-endのテストに戻ることもできるが、それは以前と同じように書くのも維持するのも厄介.
その代わりに、システム全体を一緒に呼び出すテストを書くことが多いが、**I/O操作を偽って、edge-to-edgeのテスト**を書く. (end-to-end テスト: I/O操作も含めたシステム全体のテスト. egde-to-egde テスト: 両サイドのI/O操作を除いたシステム全体のテスト)

以下では、**dependency injection(DI, 依存関係の注入)**を使って、Explicit dependencies 明示的な依存関係を示している(sync.py)

```python
def sync(reader, filesystem, source_root, dest_root): # 1. トップレベル(highest-level)の関数は、2つの新しい依存関係`reader` と `filesystem` を公開するようにした.

    source_hashes = reader(source_root) # 2. `reader` を呼び出して、ファイルの dict を生成する.
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
            filesystem.delete(dest_root/filename) # 3. 検出した変更を適用するために `filesystem` を呼び出す.
```

dependency injection(DI, 依存関係の注入)を使ったテスト.

```python
class FakeFileSystem(list): # 1. 筆者の好みだが, listを使う事で`assert foo not in database` のようなテストが書ける.

    def copy(self, src, dest): # 2. FakeFileSystem` の各メソッドはリストに何かを追加するだけ. 後でlist内の要素を確認できる.
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

(上での`FakeFileSystem`は、たぶんRepository pattern(永続的ストレージの抽象化)??)

この方法の利点は、実運用コードで使われているのとまったく同じ関数でテストが動作する事.
一方、デメリットは、**ステートフルなコンポーネントを明示的に渡す必要がある**事.(...??)
Ruby on Rails の開発者である David Heinemeier Hansson は、このことを "**test-induced design damage**" と表現して有名になった.

いずれにせよ、これで実装のバグをすべて修正することができる.
すべてのエッジケースに対するテストを列挙することが、はるかに容易になった.

### 1.3.2. Why Not Just Patch It Out? なぜパッチを当てないのか？

この時点で、あなたは頭をかきむしり、「なぜ `mock.patch` を使って手間を省かないのか」と考えているかもしれない. (mockを使えばI/O操作を含んでいてもテストが書けるだろうって意味！)

この本ではモックを使わないようにしているし、プロダクトコードでも同様.
賛否あるが、著者達の直感では、モッキングフレームワーク、特に monkeypatching (?)はコードを読みづらくさせる.

その代わり、我々はコードベースの responsibility を明確に特定し、それらの responsibility を、テストダブル(?)で簡単に置き換えられる(=Fake Repositoryみたいな?)、小さく集中したオブジェクトに分離することを好む. 

その理由は、以下の、相互に関連する3つの理由から:

1. mockを使って、依存関係をpatchする事でユニットテストは可能になる. しかし、設計を改善する事には貢献しない. なので抽象化したものを導入する必要がある.
2. mockを使用したテストは、コードベースの実装の詳細とより密接に関連する傾向がある. 例えば、 `shutil.copy` を正しい引数でコールしたかどうか？ 私たちの経験では、このようなコードとテストの結合はテストをより脆弱にする傾向がある.
3. mockの使いすぎは、コードの挙動を説明できない、複雑なテストコードにつながる.

- Note:
  - **テストしやすい設計**は、実際には**拡張しやすい設計**を意味する...!

- Mock vs Fakes;  LONDON-SCHOOL TDD vs Clasic stype TDD
  - ここでは、モックとフェイクの違いについて、簡単かつやや単純に定義している.
  - mock: 何かがどのように使われるかを検証するため
  - fakes: 置き換えようとしているものの実装が動作するものですが、テストにのみ使用するように設計されている. (ex. Fake Repository)

私たちはTDD(test driven dev)を、第一に設計の実践、第二にテストの実践と捉える.
**テストは設計上の選択の記録**として機能し、**久しぶりにコードに戻ったときにシステムを説明する役割**を果たす.

mockを多用するテストは、セットアップのコードで溢れかえり、肝心のストーリーが見えなくなってしまう.


### 1.3.3. TIP

この章では、エンドツーエンドテストをユニットテストに置き換えることに多くの時間を費やしてきた.
だからといって、E2E テストを決して使ってはいけないというわけではない.
この本では、できるだけ多くのユニットテストと、自信を持つために必要な最小限の E2E テストで、適切なテストピラミッドを作るためのテクニックを紹介している.

### 1.3.4. SO WHICH DO WE USE IN THIS BOOK? FUNCTIONAL OR OBJECT-ORIENTED COMPOSITION? この本では、どちらを使うのでしょうか？ 関数型構成かオブジェクト指向構成か？

両方. 
ドメインモデルは依存関係や副作用が全くないもので、これがfunctional core となる.
その**周りに構築するサービス層(service layer)(第4章参照)**により、システムをエッジからエッジまで動かすことができる.
また、 dependency injection を使用して、これらのサービスにステートフルなコンポーネントを提供するので、ユニットテストを行うことも可能. 

dependency injection をより明示的かつ集中的に行う方法については、第13章を参照せよ.

## 1.4. Wrap-Up まとめ

ビジネスロジック( functional core )と面倒なI/Oの間のインターフェイスを単純化することで、システムのテストと保守を容易にできる.
適切な抽象化を見つけるのは難しいが、ここではいくつかの発見と自問自答を紹介する.

- 面倒なシステムの状態を表すために、身近なPythonのデータ構造を選び、そのstate を返すことができる一つの関数を想像してみるのはどう?
- 自分のシステムのどこに線を引けばいいのか、どこに継ぎ目を刻めばその抽象的なものを突き刺すことができるのか。
- 物事を異なる responsibility を持つ構成要素に分割する賢明な方法とは？ どのような暗黙の概念を明示することができるか?
- dependency はどうなっているのか、コアとなるビジネスロジック(= functional core)は何なのか.

Practice makes less imperfect...!
