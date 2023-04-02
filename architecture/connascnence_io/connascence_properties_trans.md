## link リンク

- https://connascence.io/strength.html https

# Properties プロパティ

## Strength ストレングスです。

The strength of a form of connascence is determined by the ease with which that type of coupling can be refactored.
**connascenceの形態の strength は、そのタイプの coupling がリファクタリングしやすいかどうかで決まる**.
For example, connascence of name is a weak form of connascence because renaming entities across a codebase is usually reasonably trivial.
例えば、コードベース全体でエンティティの名前を変更することは、通常、合理的に些細なこと(=リファクタリングしやすい!)であるため、connascence of name は weak な形式である.
However, connascence of meaning is considered a stronger form of connascence since semantic meaning is harder to find across an entire codebase..
しかし、connascence of meaning はコードベース全体で見つけるのが難しいため、connascence of meaningはより strongな形式と考えられている.

Static connascences are considered to be weaker than dynamic connascences, since static connascences can be determined simply by examining the source code.
Static connascences は、ソースコードを調べるだけで判断できるため、dynamic connascences よりも弱いと考えられている.
Dynamic connascences require knowledge of run-time behavior, and thus are harder to reason about..
dynamic connascences は、実行時の動作に関する知識を必要とするため、推論が困難である.

Strength and locality should be considered together.
Strength と locality は一緒に考えるべき. (そうすると強いconnascenceを発見しやすい?)
Stronger forms of connascence are often found within the same function, class, or module where their impact can be more easily observed..
より強力な connascence は、同じfunction、class、module内で見られることが多く、その影響をより容易に観察することができる.

## Locality

The locality of an instance of connascence is how close the two entities are to each other.
**connascence のインスタンスの locality とは、2つの entity が互いにどれだけ近いかということ**である.
Code that is close together (in the same module, class, or function) should typically have more, and higher forms of connascence than code that is far apart (in separate modules, or even codebases).
近くにあるコード(ex. 同じモジュール、クラス、関数の中にある)は、遠くにあるコード(別々のモジュール、あるいはコードベースの中で)よりも、一般的に、より多く、より高い(=より強い?)形式の connascence を持つべきである.
Many of the stronger forms of connascence that can be devastating to the readability and maintainability of a codebase when they appear far apart are innocuous when close together.
遠く離れている場合はコードベースの可読性と保守性に壊滅的な打撃を与えるような **強いconnascence形式でも、近くにいると無害なものが多い**.

![]()

Locality matters! Stronger connascences are more acceptible within a module.
Localityは重要である. モジュール内では、より強い connascences が受け入れられやすい.
Weaker connascences should be used between entities that are far apart (in separate modules or even codebases)..
**離れた場所にあるEntity(別のモジュールやコードベース)間では、より弱いconnascencesを使用する必要がある**.

## Degree ディグリー

The degree of a piece of connascence is related to the size of its impact.
connascenceの断片の Degree は、その影響(=影響範囲?)の大きさに関係する.
Does the coupling in question affect 2 entities, or 200?.
ある coupling(=ある connascence)は、**2つのentityに影響を与えるのか、それとも200のentityに影響を与えるのか**.

## The Origins of COnnascence The Origins of COnnascence.

Connascence is a software quality metric that attempts to measure coupling between entities.
**Connascenceは、entity間の coupling (の度合い?) を測定しようとするソフトウェア品質指標**である.
The term was used in a computer science context by Meilir Page-Jones in his article, Comparing techniques by means of encapsulation and connascence, Communications of the ACM volume 35 issue 9 (September 1992)..
この言葉は、Meilir Page-Jonesの論文「Comparing techniques by means of encapsulation and connascence」（Communications of ACM volume 35 issue 9 (September 1992) ）で、コンピュータサイエンスの文脈で使われた.

In 1996, Meilir Page-Jones included a large section on connascence in his book "What every programmer should know about object-oriented design".
1996年、Meilir Page-Jonesは著書「What every programmer should know about object-oriented design」の中で、connascenceに関する大きな章を設けた.
The book can still be found on amazon.com.
この本は、今でもamazon.comで見ることができる.

## Other Resources その他のリソース

Since Meilir Page-Jones published his book, several other people have adapted and expanded on the concept of connascnence..
メイリール・ペイジ・ジョーンズが著書を出版して以来、何人もの人々がconnascnenceの概念を翻案し、拡張してきた.

### Jim Weirich Jim Weirich.

The greatest proponent of connascence is probably the late Jim Weirich.
コナクションの最大の提唱者は、故ジム・ウィーリッチ氏だろう.
Several examples of his contributions to the industry can be found below:.
彼の業界への貢献は、以下のようにいくつか例を挙げることができる.

- Connascence Examined.

  - A one hour long talk from 2012 that goes into considerable detail of the various types of connascence.
  - 2012年に行われた1時間の講演で、様々なタイプのconnascenceについてかなり詳しく説明されている.

- Grand Unified Theory of Software Design.
  A 45 minute talk given at 'Aloha on Rails'..
  Aloha on Rails」で行われた45分の講演です。

- The Grand Unified Theory.
  - An earlier talk from 2009. 2009年の以前の講演の様子。 Note: The audio quality on this talk is questionable at times.. 注：この講演の音声は、時折、音質に問題があることがあります。

Connascence Examined.
Connascence Examined.
Jim Weirich gave an hour long talk at YOW in 2012..
Jim Weirichは2012年にYOWで1時間の講演を行いました。

Ruby Rogues ep.
ルビーローグep. 60. 60.
Ruby Rogues is a weekly podcast about programming.
Ruby Roguesは、プログラミングに関する週刊ポッドキャストです。
This episode features Jim Weirich, and discusses both the SOLID principles and connascence..
このエピソードでは、Jim Weirich氏を迎え、SOLIDの原則とその関連性について議論します。

### Kevin Rutherford ケビン・ラザフォード

Kevin Rutherford has published a series of blog posts about connascence: they have inspired much of the content on this website.
ケビン・ラザフォードは、コナスカンスに関する一連のブログ記事を発表しており、本サイトのコンテンツの多くに影響を与えています。
He also has a recorded talk, Red, Green, ...
また、録音したトーク『Red, Green, ...』もある。
now what?!, where he goes over the usage of connascence during a refactoring kata..
リファクタリングの型に沿ったコナンスの使い方を解説した「neow what?

### Multiple Authors 複数の著者がいる。

In 2013, this google hangout was broadcast that included several luminaries of the software development industry, including Corey Haines, Curtis Cooley, Dale Emery, J.
2013年には、Corey Haines、Curtis Cooley、Dale Emery、J.
B.
B.
Rainsberger, Jim Weirich, Kent Beck, Nat Pryce, and Ron Jeffries..
レインズバーガー、ジム・ウェイリッチ、ケント・ベック、ナット・プライス、ロン・ジェフリーズの各氏。

### Josh Robb ジョシュ・ロブ

In 2015 Josh Robb gave a talk titled Connascence & Coupling at codemania.
2015年、ジョシュ・ロブはcodemaniaで「Connascence & Coupling」と題した講演を行った.
That talk was the inspiration to build this site..
その時の話が、このサイトを作るきっかけになった.

### Thomi Richards トミ・リチャーズ

In 2015 Thomi Richards summarized the contents of this website in a talk at Kiwi PyCon..
2015年、Thomi RichardsはKiwi PyConでの講演で本サイトの内容をまとめました。

### Gregory Brown グレゴリー・ブラウン

In 2016 Gregory Brown wrote "Connascence as a Software Design Metric" for the practicingruby.com blog..
2016年、グレゴリー・ブラウンは、practicingruby.comのブログに「ソフトウェア設計指標としてのConnascence」を書きました。

### Patches Welcome! パッチ歓迎!

The connascence.io website is an open source project hosted on github.
connascence.ioのウェブサイトは、githubでホストされているオープンソースプロジェクトである.
Help us make this website awesome! We're interested in any and all contributions you might have, including:.
このウェブサイトを素晴らしいものにするために、私たちに協力してください.
私たちは、あなたが持っているかもしれないすべての貢献に興味がある：以下を含む。

- Spelling and grammatical fixes.スペルや文法の修正。

- New and better content. 新しく、より良いコンテンツを提供します。

- Links to other resources about connascence. connascenceに関する他の資料へのリンクです。

- Graphical & design changes. グラフィックの変更、デザインの変更

- Translating pages into other languages. **ページを他言語に翻訳する**.

- Translating examples into other programming languages. **他のプログラミング言語に例を翻訳**する.

- ...anything else - give us your good ideas!...その他、何でも構いませんので、皆様の良いアイデアをお聞かせください。
