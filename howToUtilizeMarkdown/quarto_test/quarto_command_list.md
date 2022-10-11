# はじめに

本記事は、Power Pointが苦手な一人の大学院生がquartoと出会い、Document・発表スライド作りの楽しさを取り戻していく物語です。(本当は単に、公式Documentを読みながら、quartoに関するTipsや文法を備忘録を兼ねてまとめていく記事です。)

## Markdownで発表スライドを作りたい...

僕は大学での講義や研究活動における発表機会の際、Power Pointを使用して発表資料を作成していました。これは特にこだわりがあるのではなく、周りの人が全員Power Pointを使っており、それが当たり前だったからです。

最初のうちは何も気にせずPower Pointでスライドを作成していたのですが、研究活動でスクリプトをたくさん書くようになると、だんだんPower PointのGUIによる資料作成が非常に退屈で苦痛に感じてきました。
ただこのことはほぼ間違いなく個人個人の好みの問題でして、Power Pointによるスライド作成を否定しているわけではないんです：）Power Pointは誰もが直感的に操作しやすい、凄く素敵なツールだと思います...!
僕自身の場合はプログラミングが好きで楽しく感じており、かつ凝り性・心配性ゆえにPower Pointのピクセル単位でのオブジェクト調整に必要以上に時間を浪費していたので、もう嫌気が差していたんです。

脱Power Pointを志して以降、Markdown記法でのスライド作成方法をちょくちょく探していました([Marp](https://marp.app/)とか[Slidev](https://sli.dev/)とか！)。そして最近、「markdownによるDocument作成で最近イチオシなのはQuartoらしいよ！」というレコメンドをいただいたのが、僕とquartoとの出会い、そして本記事のきっかけになります！

## quartoとは？

quarto(クオルト?)とは、

> Quarto® is an open-source scientific and technical publishing system built on Pandoc
> らしいです。([公式](https://quarto.org/)より)

まあ僕は今のところ、ざっくり「Markdown記法を使ってDocumentを作り、それを.pdfだったり.htmlだったり.pptx等のスライド形式でも吐き出せるツール」の一つだと認識しています。

[公式のDocument](https://quarto.org/)が非常に丁寧で充実していると感じたので、英語の資料を読むことが苦でない方はぜひそちらを読んでみてください...!

コレ以降のSectionでは、QuartoでDocumentやスライドを作る上でのTipsや気づいた事をまとめていきます。

# Quartoの導入方法

ここに関しては、公式Documentの[Get Started](https://quarto.org/docs/get-started/)を参照。
もしくは、[@Nobukuni-Hyakutake様の記事](https://qiita.com/Nobukuni-Hyakutake/items/112a7bd5b34abd446395)でも丁寧にまとめられています。感謝...!

# QuartoのPreview( Internal or External)

デフォルトでは、.qmdファイルのプレビューはInternal、すなわちVSCode上に表示されます。外部ブラウザを使用してPreviewを表示させたい場合は、設定から`Quarto › Render: Preview Type`オプションを指定する事で実現できます。

# QuartoによるPresentationスライド作成

## スライドのフォーマット

`.qmd`ファイルの先頭のyaml部分で、`format`オプションを以下の3つのうちどれかに指定すると、出力されるプレビューがスライド形式になるようです。

- `revealjs` — reveal.js (HTML)
- `pptx` — PowerPoint (MS Office)
- `beamer` — Beamer (LaTeX/PDF)

例えばこんな感じで。

```qmd
---
title: "demo presentation material"
author: "morinota"
format: revealjs
---
```

公式Documentが推奨するのは`revealjs`みたい。

## 各スライドの区切り方

Header を使う方法と、水平方向の罫線(`---`)を使う方法の2種類。

Header(見出し)を使ってスライドを区切る場合、lebel 1 heading(`#`)とlevel 2 heading(`##`)でスライドが区切られるみたい。

```md
---
title: "demo presentation material"
author: "morinota"
format: revealjs
---

# In the morning

## Getting up

- Turn off alarm
- Get out of bed

## Breakfast

- Eat eggs
- Drink coffee

# In the evening

## Dinner

- Eat spaghetti
- Drink wine

## Going to sleep

- Get in bed
- Count sheep
```

こんな感じで区切られる。
![](../images/2022-09-03-16-52-28.png)

上の例では、各Section毎のTitleスライドとしてlevel 1 header(`#`)を、非Titleスライドとしてlevel 2 header(`##`)として使用している。
この設定はどうやら、slide-levelオプションを使ってカスタマイズできるみたい。

また、水平方向の罫線`---`を使う場合はこんな感じ。

```md
---
title: "Habits"
author: "John Doe"
format: revealjs
---

- Turn off alarm
- Get out of bed

---

- Get in bed
- Count sheepF
```

## Incremental Lists:

この機能は、何と言えばいいのか、「箇条書きの箇所が、ページ遷移時に一斉に表示されない。一つずつ表示させる。」ような機能といえば伝わるでしょうか。フェードインのアニメーションみたいな。
先頭のYAML部分で`incremental`オプションを`true`にすると、全ての箇条書きの箇所がIncremental(＝ページ遷移時に一斉に表示されない・一つずつ)になる。

```md
---
title: "demo presentation material"
author: "morinota"
format:
  revealjs:
    incremental: true
---
```

上の例だと全てのページの箇条書きがIncrementalになるが、該当する箇所の箇条書きのみを明示的にIncremental/Non-Incrementalと指定したい場合には、markdown記法の該当する箇条書きの箇所を、明示的にIncrementalクラス/Non-Incrementalクラスで囲む。

例えば以下のように。この場合、`## Getting up`ページの箇条書き箇所はIncrementalで、`## Breakfast`の箇条書き箇所はNon-Incrementalで表示される。

```md
## Getting up

::: {.incremental}

- Turn off alarm
- Get out of bed

:::

## Breakfast

::: {.nonincremental}

- Eat eggs
- Drink coffee

:::
```

## Multiple Columns

一つのスライド内でオブジェクトを横に並べて配置するには、`.columns`クラスを使ってdivコンテナを作り、その中に2つ以上の`.column`クラスを含める事で実現できます。

そして、`.column`クラスを定義する際には、`width`属性を記述しなければならないようです。
試しに`.columns`クラスで定義したコンテナ内の2つの`.column`クラスのうち、1つで`width`属性を記述しなかったところ、このMultiple Columns機能は反映されずに一列で表示される状態でした。

```md
## Multiple Columns Page

:::: {.columns}

::: {.column width="40%"}
contents...

- hoge
- hogehoge

:::

::: {.column width="60%"}
contents...

- piyo
- piyopiyo

:::

::::
```

作成されるスライドはこんな感じ

![](../images/2022-09-03-17-25-06.png)

## Reveal JS formatの扱い

### themeについて

参考 [quarto Reveal Themes](https://quarto.org/docs/presentations/revealjs/themes.html)

以下のような感じで、YAML部分の`revealjs:`以下の階層に`theme:`オプションを指定します。

```yml
---
title: "Presentation"
format:
  revealjs:
    theme: dark
---
```

デフォルトで利用可能なbuild-in themeは、現状以下の11個のようです。

- `beige`
- `blood`
- `dark`
- `default`
- `league`
- `moon`
- `night`
- `serif`
- `simple`
- `sky`
- `solarized`

### Customizing Themeについて

また、ユーザ自身でカスタマイズされたthemeも使用する事ができるようです。
その際には、独自に`Sass`テーマファイルを作成する必要があります。

#### Sassとは??

参考

- [Black Lives Matter](https://sass-lang.com/)
- [これからはcssはSassで書こう。](https://qiita.com/m0nch1/items/b01c966dd2273e3f6abe)

Sass(Syntactically Awesome StyleSheet)は、CSSを拡張したメタ言語(=ある言語について何らかの記述をするための言語)らしいです。CSSをより効率的にコーディングできるようにした言語、みたいな感じみたいです...!
(そもそも私はCSSをほとんど書いたことがないので、あまりイメージつきませんが...!)

`.sass`記法(インデントで依存関係を表す。Pythonっぽい?)と`.scss`記法(`{}`で依存関係を表す。CSSの書き方)の２種類があるらしく、今回は後者の`.scss`記法を使用してみます。

```css:custom.scss
/*-- scss:defaults --*/

$body-bg: #191919;
// $body-color: #fff;
$body-color: #42affa;
$link-color: #fff;

/*-- scss:rules --*/

.reveal .slide blockquote {
  border-left: 3px solid $text-muted;
  padding-left: 0.5em;
}
```

- `.scss`ファイルのコードの意味：
  - `/*-- scss:defaults --*/` は、フォント、色、ボーダーなどに影響する変数を定義するために使用します
    - 変数は `$` で書き始める。
    - [カスタマイズ可能な変数の一覧](https://quarto.org/docs/presentations/revealjs/themes.html#sass-variables)
  - `/*-- scss:rules --*/` は、CSSルールを作成するために使用します。 - Reveal コンテンツを対象とする CSS 規則は、一般にテーマのデフォルトスタイルをうまく上書きするために `.reveal .slide`という接頭辞を使用する必要があるらしい...! -

作成した`custom.scss`を`.qmd`ファイルと同じ階層に保存し、`.qmd`側での`theme`オプションを以下のように指定します。

```yaml
---
format:
  revealjs:
    incremental: false
    theme: [default, custom.scss]
---
```

### footerとLogoについて

`footer`オプションと`logo`オプションを使用すると、各スライドの下部にフッターテキストとロゴを含めることができます。

## PowerPoint formatの扱い

### Speaker Notes

### PowerPoint Templatesの使用

デフォルトのPowerPointの出力では、かなりプレーンな見た目のTemplateが使用されます。
YAMLパートで`reference-doc`オプションを指定する事で任意のTemplateを適用できます。

```md
---
title: "Presentation"
format:
  pptx:
    reference-doc: template.pptx
---
```

# QuartoのFigureの扱い

## 基本的な記法

画像の表示は、基本的には通常のMarkdown記法ですね。

```md
![Elephant](elephant.png)
```

これでCaptionが"Elephant"と付いて、`elephant.png`が表示されます。

## リンクを紐づけたFigure

```md
[![Elephant](elephant.png)](https://en.wikipedia.org/wiki/Elephant)
```

## 代替テキストの追加

Figureに代替テキストを追加するには、画像に`fig-alt`属性を追加すればいいみたい。

```md
![](elephant.png){fig-alt="A drawing of an elephant."}
```

上の記述によって、ファイル変換時に以下のようなHTMLが生成されるようです。

```html
<img src="elephant.png" alt="A drawing of an elephant." />
```

ここで、図のCaption、Title、代替テキストは、すべて異なるものにすることができることに注意。例えば、以下のようなコード...

```md
![Elephant](elephant.png "Title: An elephant"){fig-alt="A drawing of an elephant."}
```

この場合、変換されるHTMLは以下。

```html
<img
  src="elephant.png"
  title="Title: An elephant"
  alt="A drawing of an elephant."
/>
```

# おわりに

今後もQuarto公式Documentを読みながら、自分の資料作成に使いつつ、適宜追加していきたいです。
数日触ってみた感想ですが、「Marpよりも複雑なDocumentを作成可能」かつ「Slidevより記法が理解しやすい」気がしており、個人的には好感触です...!
興味を持っていただきありがとうございました：）

難しくも楽しい研究者or技術者ライフを～！
