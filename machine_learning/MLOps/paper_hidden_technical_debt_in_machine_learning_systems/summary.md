---
format:
  html:
    toc: true # 目次(Table of Contents = toc)を自動生成するかどうか
    toc-depth: 3 # tocで表示するsection levelの深さ
    theme: cosmo # theme候補: cerulean, cosmo, flatly, journal, lumen, paper, readable, sandstone, simplex, spacelab, united, yeti
from: markdown+emoji
fig-cap-location: bottom
# title: より持続可能性の高いMLシステムってどう作ればいいんだろうと悩み、有名なMLシステムの隠れた技術的負債の論文を読んだ
title: Hidden Technical Debt in Machine Learning Systems を読んで持続可能性の高いMLシステムに思いをはせた
subtitle: y-tech-ai ワクワク勉強会
date: 2024/05/14
author: モーリタ
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 1. はじめに

### 1.1. この図で有名な論文!

![論文中のFigure 1より引用](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502ad4eb9b805fbe60281f4_figure%203_lightbox.png)

「MLアルゴリズムは、実世界のMLシステムにおいてあくまでも要素の1つだよ!他にも重要な要素はたくさんあるよ!」みたいな意図でよく引用されてるやつ...!:thinking:

### 1.2. なんでこの論文を選んだの??

-
- 業務の中で、漠然と「より良いMLシステムってどう作ればいいんだろう」と思って色々調べ始めた。
  - 「良いMLシステム」ってどういうことだろう?
    - → **持続可能性が高いMLシステム**?:thinking:
    - i.e. 短期的にも長期的にも改善し続ける事ができたり、プロダクトに価値提供し続けることができるようなMLシステム、みたいな...!:thinking:
- 上述の図で有名な論文だけど、前回(約1ヶ月前)喋った際に皆さん意外と読んでない人が多かった!(図は知ってるけど...!)
  - → 概要と感想を共有することで共通認識を得たり議論できればと思いました:smile:
- ちなみに、前回資料は以下です!
  - [より持続可能性の高いMLシステムってどう作ればいいんだろうと悩み、有名なMLの技術的負債の論文を読んでFTI Pipelines architectureに思いを馳せた話](https://morinota.quarto.pub/y-tech-ai-wakuwaku-20240326/)

### 参考文献:

- 2015年の技術的負債の論文: [Hidden Technical Debt in Machine Learning Systems]()
- 上の論文の重箱をつつくブログ: [Nitpicking Machine Learning Technical Debt](https://matthewmcateer.me/blog/machine-learning-technical-debt/)
- 上のブログの日本語訳: [【翻訳】機械学習の技術的負債の重箱の隅をつつく (前編)](https://blog.hoxo-m.com/entry/2020/06/21/190056)

## 2. 導入: MLシステムと技術的負債

### 2.1. 技術的負債ってなんだっけ?

- **技術的負債(technical debt)**とは??
  - 1992年にWard Cunningham(ウォード・カニンガム)が提唱した**比喩表現**(metaphor)。
  - ソフトウェア開発において、**短期的な利益を優先することで、長期的に追加のコストが発生する**ような設計や実装のこと?
    - この概念は、金融の負債に例えられ、将来的にその借金を返済する必要があるとされ、返済しないと利子がついていくというもの。
- 返済の目的は、将来の改良を可能にし(=Easier To Changeだ!:thinking:)、エラーを減らし、運用・保守性を向上させること
  - -> (つまり、**ソフトウェアシステムの持続可能性を高めること**だ...!!:thinking:)
- 一般に技術的負債は、以下のアプローチ等によって返済できる:
  - refatoring code (リファクタリング)
  - improving unit tests (単体テストの改善)
  - deleting dead code (不要なコードの削除)
  - reduce dependencies (依存関係の削減)
  - tightening APIs (APIの設計改善)
  - improving documentation (ドキュメントの改善)

### 2.2. MLシステム特有の技術的負債があるっぽい話

- 本論文では、MLシステムには、従来のソフトウェア開発の技術的負債に加え、以下のような**MLシステム特有の技術的負債**が存在すると主張している。
  - 1. Complex Models Erode Boundaries
  - 2. Data Dependencies Cost More than Code Dependencies
  - 3. Feedback Loops
  - 4. ML-Systems Anti-Patterns
  - 5. Configuration Debt
  - 6. Dealing with Changes in the External World
- これらの技術的負債は、code levelではなくsystem levelに存在するため、検出が難しい可能性がある。

### 2.3. 本論文の目的

- 本論文は新しいMLアルゴリズムを提供するものではない。
- **実践的に長期的に考慮すべき、MLシステムのトレードオフについてコミュニティの意識を高めること**を目的としている。

## 3. MLシステム特有の技術的負債1: Complex Models Erode Boundaries

- 伝統的なソフトウェアエンジニアリングのpracticeでは、カプセル化とmodular設計を使った強力な**abstraction boundary**が、持続可能なコードを作る上で有効。
- でも残念ながらMLシステムの場合は、厳密なabstraction boundaryを規定する事は難しい。
  - (もちろんモジュラー性を高めたり、関心を分離させる事はMLシステムでも変わらず重要だろうけど、どうしても通常のシステムよりも結合が強くなっちゃう、みたいな...!:thinking:)
  - (MLシステムは、外部データに依存したロジックだから?)
- 論文では、**erosion of boundaries(境界の侵食)**が、MLシステムにおける技術的負債を著しく増加させ得ると主張している。
- erosion of boundaries(境界の侵食)の**3つの例**:

  - 1. Entanglement(絡み合い):
  - 2. Correction Cascades(修正の連鎖)
  - 3. Undeclared Consumers(未宣言の消費者)

### 3.1. 例1: Entanglement(絡み合い)

- MLシステムは、複数の入力情報(i.e. 特徴量)を混ぜ合わせ、絡み合い、改善の為の分離を難しくしてしまう。
- ex. 特徴量 $x_1, ...x_n$ を使用するMLモデルをシステム内で使用する場合
  - $x_1$の分布の変化が、残りの $n-1$ 個の特徴量のモデル内での使われ方(パラメータ, feature importance)に影響を与える可能性がある。
  - これは、MLモデルをbatch方式で再学習する場合でも、オンライン方式で適応させる場合でも同様の問題が発生する。
  - また、新しい特徴量 $x_{n+1}$ を追加する場合も、あるいは特徴量 $x_{j}$を削除する場合も、同様の問題が発生する可能性がある。
- 各入力が本当に独立している事はない。
- 論文ではこれを「**CACEの原則**」と呼んでいる：
  - =**Changing Anything Changes Everything(何かを変えればすべてが変わる)**
  - CACEの原則は、入力特徴量だけでなく、ハイパーパラメータやサンプリング方法等の基本的に全ての調整要素にも適用される。
- 緩和策:
  - 1. モデルを分離して、アンサンブルにする事。
    - マルチラベル分類のように、sub問題に自然に分解できるような状況で有用。
  - 2. 推論結果の変化が発生したときに、その変化を検出することに焦点を当てる事。
    - (異常検知、みたいな??:thinking:)

### 3.2. 例2: Correction Cascades(修正の連鎖)

- 問題Aに対するモデル $m_a$ が存在するが、わずかに異なる問題A′の解決策が必要な場合がしばしばある。
- この場合、問題を素早く解く方法として、$m_a$ を入力として受け取り、小さな補正を学習するモデル $m′_a$ を採用したくなるかもしれない...!
- **しかし、この補正モデルは、$m_a$ に新しいシステム依存関係を追加し、将来そのモデルの改善を分析するコストが大幅に増加する**。(モデルの使いまわしへの警鐘...??:thinking:)
- このような補正モデルが連鎖していくと、更にコストが増加していく:
  - 問題A′′のモデルが $m′_a$ の上に学習されたり...!
  - いくつかのわずかに異なるテスト分布に対してまた別の修正モデルを学習させたり...! (ex. 複数のdomainに対する推薦とか?)
  - (複数のタスクで共通のマルチタスクモデルを使ったり、共通の基盤モデルを用意して後は各タスクにfine-tuningするみたいなアプローチに憧れてたけど、これはEasier To Changeの観点からは有効じゃないのかもなぁ...!:thinking:)
- 一度デプロイされた補正モデルの連鎖は、個々のcomponentの精度向上の為の変更が、依存する他のcomponentに悪影響を与える可能性があり、**改善のdeadlock**を引き起こし得る。
  - (MLの各usecaseが密結合になってしまって、あるusecaseの為の変更の影響範囲が大きくなる...??)
- 緩和策:
  - 1. 各usecaseを区別する為の特徴量を追加して、単一のモデル $m_a$ の中で、補正を学習するようにすること。
  - 2. **各usecase $A, A′, A′′$ に対して、別々のモデルを作成するコストを受け入れること**。(こっちの方法が無難な気がするな...!:thinking:)
    - (この話を踏まえると、全usecase共通の基盤モデル、みたいな考え方って結構危ないのかな...??:thinking:)

### 3.3. 例3: Undeclared Consumers(未宣言の消費者)

- 多くの場合、機械学習モデル $m_a$ からの予測結果は、実行時に広くアクセス可能になるか、後で他のシステムによって消費される可能性のあるファイルやログに書き込まれる。
- **アクセス制御を行わなければ、これらのconsumerの中には未宣言のものがいて、特定のモデルの出力を別のシステムの入力として無言で使用しているかもしれない**。
  - (ex. ユーザの埋め込みベクトルを、気づいたらプロダクト内のいろんな機能が使っちゃってた、みたいな??:thinking:)
  - より古典的なソフトウェア工学では、これらの問題は**visibility debt(可視性負債)**と呼ばれる。
- Undeclared consumerは、最悪の場合には危険であり、最高の場合でも高価である。
  - -> なぜなら、**MLモデル $m_a$ とシステムの他のcomponentsとの間にhidden tight coupling(隠れた強い結合)を作り出すから**...!
  - このhidden tight couplingは、MLモデルの変更のコストと難しさを根本的に増加させる可能性がある。
  - (booking.comのsemantic model的なMLの使用って、まさにundeclared consumersだらけだと思うんだけど、この点どうなんだろう...?? まあトレードオフだと思うけど...!:thinking:)
  - (ちゃんとdeclareしたconsumerだとしても、それが多くなっちゃうと、変更のコストは大きくなるよなぁ...!:thinking:)
- **undeclared consumer は、特に対策しない限り簡単に発生し、検出も困難になる**。
  - 障壁がない場合、開発者は、手元にある最も便利な信号を自然に使用するだろう、特に締め切りのプレッシャーに対処するときに...!

## 4. MLシステム特有の技術的負債2: Data Dependencies Cost More than Code Dependencies

- 既存文献では、古典的なソフトウェアエンジニアリングにおいて、「**depencency debt(依存性負債)がコードの複雑さと技術的負債の主要な要因である**」と指摘している。
- 本論文では、MLシステムにおいて、data dependenciesが同様の負債を持ち、かつそれを検出するのがより困難かもしれない、ということを主張している。
  - code dependenciesは、コンパイラやlint tool等の静的解析ツールで検出できる。
  - data depencenciesに対する同様のツールが存在しなければ、大規模やdata depencency chainが簡単に発生し得る。

### 4.1. Unstable data dependencies(不安定なデータ依存関係):

- 素早く開発を進めるために、他のシステムによって作られた信号を入力特徴量として使うことがしばしば便利。
- 入力信号の「改善」でさえ、消費するシステムに任意の悪影響をもたらす可能性がある。

### 4.2. Underutilized data dependencies(十分に活用されていないデータ依存関係):

## 5. MLシステム特有の技術的負債3: Feedback Loops

## 6. MLシステム特有の技術的負債4: ML-Systems Anti-Patterns

## 7. MLシステム特有の技術的負債5: Configuration Debt

## 8. MLシステム特有の技術的負債6: Dealing with Changes in the External World

## 9. その他のMLシステム特有の技術的負債

## 10. 結論

- 技術的負債は有用なメタファー(隠喩)だが、残念ながら、長期にわたって追跡できる厳密な指標を提供するものではない。(定量評価できないから??:thinking:)
  - **システムの技術的負債をどのように測定し、この負債の全体的なコストを評価するのか?**
    - チームがまだ素早く動くことができるということだけが、低い負債や良い実践の証拠となるわけではない。
    - なぜなら、負債の全体的なコストは時間の経過とともに明らかになるから...!
      - (今素早く開発できiるから負債はない、とは言えないって事か...!:thinking:)
- 技術的負債を考える上で有用な質問たち:

  - 1. **全く新しいアルゴリズムのアプローチを、どの程度簡単にfull scalseでテストできるか?** (test at full scaleってE2Eテストのことかな...?:thinking:)
  - 2. 全てのdata dependenciesの接続状況を把握できているか??
    - (メモ) transitive closure(推移閉包) = グラフ理論における、要素間の全ての直接的及び間接的な接続のこと。
    - よって、技術的負債の文脈でのこの質問は、**システム内の全てのデータ依存関係の直接的及び間接的な接続をちゃんと理解できているか否か、ちゃんと答えられる程度にデータ依存関係が少ない事が重要**だよ、みたいな意図???
  - 3. システムに対する新たな変更の影響を、どの程度正確に測定できるか??
    - (ちゃんと監視できる状態にあるかってことか...!)
  - 4. あるモデルやsignal (=モデルによる成果物など!) を改善すると、他のモデルやsignalが劣化するのか??
    - (機能間の独立性とか、data dependencyがシンプルじゃないとこの質問に答えられない...?:thinking:)
  - 5. チームの新しいメンバーを、いかに早くスピードアップさせることができるか??
    - (システム全体の複雑性を管理できていたら、新メンバーのオンボーディングもスムーズにできるってことか...!:thinking:)

- 最も重要な洞察:「**技術的負債は、エンジニアと研究者の両方が認識している必要がある...!**」
  - **システムの複雑さを大幅に増大させる代償として、小さな精度の利益を得る研究ソリューションは、賢明なpracticeであることはほとんど無い**。(うんうん...!:thinking:)
- ML関連の技術的負債を返済する為には、特定のcommitmentが必要。
  - -> チーム文化が重要。
  - **負債を回避するor返済する為の努力を認識し、優先し、報酬を与える事は、成功するMLチームの長期的な健康にとって重要**...!!
