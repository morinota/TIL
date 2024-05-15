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

## 0.1. はじめに

### 0.1.1. この図で有名な論文!

![論文中のFigure 1より引用](https://assets-global.website-files.com/618399cd49d125734c8dec95/6502ad4eb9b805fbe60281f4_figure%203_lightbox.png)

「MLアルゴリズムは、実世界のMLシステムにおいてあくまでも要素の1つだよ!他にも重要な要素はたくさんあるよ!」みたいな意図でよく引用されてるやつ...!:thinking:

### 0.1.2. なんでこの論文を選んだの??

-
- 業務の中で、漠然と「より良いMLシステムってどう作ればいいんだろう」と思って色々調べ始めた。
  - 「良いMLシステム」ってどういうことだろう?
    - → **持続可能性が高いMLシステム**?:thinking:
    - i.e. 短期的にも長期的にも改善し続ける事ができたり、プロダクトに価値提供し続けることができるようなMLシステム、みたいな...!:thinking:
- 上述の図で有名な論文だけど、前回(約1ヶ月前)喋った際に皆さん意外と読んでない人が多かった!(図は知ってるけど...!)
  - → 概要と感想を共有することで共通認識を得たり議論できればと思いました:smile:
- ちなみに、前回資料は以下です!
  - [より持続可能性の高いMLシステムってどう作ればいいんだろうと悩み、有名なMLの技術的負債の論文を読んでFTI Pipelines architectureに思いを馳せた話](https://morinota.quarto.pub/y-tech-ai-wakuwaku-20240326/)

### 0.1.3. 参考文献:

- 2015年の技術的負債論文: [Hidden Technical Debt in Machine Learning Systems]()
- 技術的負債論文の日本語の解説スライド: [Hidden technical debt in machine learning systems（日本語資料）](https://www.slideshare.net/Gushi/hidden-technical-debt-in-machine-learning-systems)
- 2020年くらいの技術的負債論文の重箱をつつくブログ: [Nitpicking Machine Learning Technical Debt](https://matthewmcateer.me/blog/machine-learning-technical-debt/)
- 上のブログの日本語訳: [【翻訳】機械学習の技術的負債の重箱の隅をつつく (前編)](https://blog.hoxo-m.com/entry/2020/06/21/190056)

## 0.2. 導入: MLシステムと技術的負債

### 0.2.1. 技術的負債ってなんだっけ?

- **技術的負債(technical debt)**とは??
  - 1992年にWard Cunningham(ウォード・カニンガム)が提唱した**比喩表現**(metaphor)。
  - ソフトウェア開発において、**短期的な利益を優先することで、長期的に追加のコストが発生する**ような設計や実装のこと。
    - 将来的にその借金を返済する必要があって、返済しないと利子がついていく、みたいな...!:thinking:
- 返済の目的は、将来の改良を可能にし(=Easier To Changeだ!:thinking:)、エラーを減らし、運用・保守性を向上させること
  - -> (つまり、**ソフトウェアシステムの持続可能性を高めること**だ...!!:thinking:)
- 一般に技術的負債は、以下のアプローチ等によって返済できる:
  - refatoring code (リファクタリング)
  - improving unit tests (単体テストの改善)
  - deleting dead code (不要なコードの削除)
  - reduce dependencies (依存関係の削減)
  - tightening APIs (APIの設計改善)
  - improving documentation (ドキュメントの改善)

### 0.2.2. MLシステム特有の技術的負債があるっぽい話

- 本論文では、MLシステムには、従来のソフトウェア開発の技術的負債に加え、**MLシステム特有の技術的負債**が存在すると主張してる。
  - 各セクションで、ざっくり以下のような分類の技術的負債が紹介されてました:
    - 1. Complex Models Erode Boundaries (抽象化境界の話)
    - 2. Data Dependencies Cost More than Code Dependencies (データ依存関係が難しい話)
    - 3. Feedback Loops
    - 4. ML-Systems Anti-Patterns (pipeline-jungleとかの話!)
    - 5. Configuration Debt 
    - 6. Dealing with Changes in the External World 
    - 7. その他
- 本論文の目的: 
  - 本論文は新しいMLアルゴリズムを提供するものではない。
  - **実践的に長期的に考慮すべき、MLシステムのトレードオフについてコミュニティの意識を高めること**である!
  - 

# 1. MLシステム特有の技術的負債1: Complex Models Erode Boundaries

要するに、**MLシステムは変更の影響範囲を管理するのが難しい**よね、という話...!:thinking:

- 一般に、modulerな設計や関心の分離を意識しながらコンポーネントを抽象化できていれば、変更の影響範囲を小さくすることができる。
-  でもMLシステムでは、厳密なabstract boundaryを維持するのが難しい -> 変更の難易度が上がりがちなんだ、という話でした...!
-  3つの例を紹介してました:
  - 1. **Entanglement(絡み合い)**: 
    - 複数の特徴量を使うMLモデルの場合、モデルが複雑であるほど特徴量間の相互作用とかを使ったりしてる。
      - (モデルの中で特徴量たちが絡まり合って...!:thinking:)
    - ある特徴量を変更/削除すると、他の特徴量のモデル内での使われ方や、モデルの性能に影響を与える可能性がある。
    - 何かを変えればすべてが変わる、という**CACE原則(Changing Anything Changes Everything)**が主張されてた。
  - 2. **Correction Cascades(補正の連鎖)**:
    - あるMLを適用したいusecaseがあった場合、類似したusecaseのMLモデル $m_a$ が既に存在していたら、そのモデルを補正(fine-tuning的な?:thinking:)して新しいモデル $m_a'$ を作成したくなりがち。(特に開発のスケジュールがきつい時は...!)
    - このような補正モデルが連鎖していくと、元のモデル $m_a$ に新しいシステム依存関係が追加され、**将来そのモデルを変更するコストが大幅に増加する**。
    - 改善のデッドロック状態になり得る。
  - 3. **Undeclared Consumers(未宣言の消費者)**:
    - (ex. ユーザの特徴を表す埋め込みベクトルを、気づいたら勝手にプロダクト内のいろんな機能が使っちゃってた。埋め込みの作り方を変えたら、プロダクト内の予期せぬ機能の品質低下が発生した、みたいな??:thinking:)
    - 推論APIのアクセス制限とかしてないと、検出するのは難しい。
    - 「障壁がない場合、開発者は、手元にある最も便利な信号を自然に使用するだろう、特に締め切りのプレッシャーに対処するときに...!」
      - **複数のusecaseで単一のモデルを使い回すことへの警鐘??** :thinking:

このセクションを読んでの感想:

- MLの複数のusecaseに対して、単一の**マルチタスクなモデル**だったり、共通の基盤モデルを用意して後は各usecaseに応じてfine-tuningするみたいなアプローチに憧れてたけど、**Easier To Changeみたいな観点ではイマイチかも**。
  - 複数のusecase間の依存関係が強くなっちゃって、改善しづくなりそう...? :thinking:
- Booking.comさんのMLの教訓の論文で「特定のusecaseに特化した specialized なモデル」と「**様々なusecaseで活用可能性がある semantic なモデル**」みたいな話を思い出した。
  - semanticモデルの出力の例: 「ユーザが旅行の目的地に対してflexibleである度合い」を出力するMLモデル
  - 「開発に携わる全ての人がsemantic モデルの出力に基づいて、新機能やパーソナライゼーション、説得力のある意思決定などに使用可能性がある。」みたいな話を聞いていいなぁって思ってたんだけど、正にこういう問題に直面したりするんだろうか?? semantic モデルは改善のデッドロック状態になり得るのか...??:thinking:
  - 参考: [宿泊予約サービスbooking.comの150個の機械学習モデルの開発運用で得た6つの教訓をまとめた論文(KDD2019)を読んだ](https://morinota.quarto.pub/journal_club_20231030/#/title-slide)

# 2. MLシステム特有の技術的負債2: Data Dependencies Cost More than Code Dependencies

- 既存文献では、そもそも古典的なソフトウェアエンジニアリングにおいて、「**depencency debt(依存性負債)がコードの複雑さと技術的負債の主要な要因である**」と指摘している。
- 本論文では、MLシステムにおいて、data dependenciesが同様の負債を持ち、かつそれを検出するのがより困難かもしれない、ということを主張している。
  - code dependenciesは、コンパイラやlint tool等の静的解析ツールで検出できる。
  - data depencenciesに対する同様のツールが存在しなければ、**大規模やdata depencency chainが簡単に発生し得る**。

# 3. MLシステム特有の技術的負債3: Feedback Loops

(よく理解できてないです...!:pray:)

- MLシステムのfeedback loopは、**analysis debt(分析負債?)**につながる。
  - リリース前にモデルの振る舞いを予測することが難しくなる。
  - (=要するにレコメンドの文脈でよく出てくる、オフライン評価とオンライン評価が相関しづらい問題のこと...??:thinking:)
- Direct Feedback Loops と Hidden Feedback Loops が存在してるらしい。

# 4. MLシステム特有の技術的負債4: ML-Systems Anti-Patterns

これは、前回の資料に含まれてた話(glue codeとか、pipeline-jungleとか、dead experiment pathの話...!)

- このセクションについて喋りたかった話は前回できたので、もし興味があったら前回資料へ!
  - [より持続可能性の高いMLシステムってどう作ればいいんだろうと悩み、有名なMLの技術的負債の論文を読んでFTI Pipelines architectureに思いを馳せた話](https://morinota.quarto.pub/y-tech-ai-wakuwaku-20240326/)

# 5. MLシステム特有の技術的負債5: Configuration Debt

- MLシステムのconfigurationも、技術的負債の一部になり得るよ、という話。
- 課題:
  - 研究者やエンジニアはconfigを後回しにしがちで、その検証やテストを重要視しないことがある。
  - 成熟したシステムでは、configの行数がモデルのコードの行数を上回ることがある。
  - configの各要素にはミスの可能性があり、その影響は大きい。
- 良いconfigurationの5つの原則を主張してた:
  - (**要するに、configもversion管理と自動テストすべき、みたいな感じっぽい**...?:thinking:)
  - 小さな変更が簡単
  - 手作業ミスが起こりにくい
  - 差異の視覚的な確認が簡単
  - 自動検証
  - 未使用・冗長設定の検出
  - 完全なコードレビュー

# 6. MLシステム特有の技術的負債6: Dealing with Changes in the External World

- MLシステムは、しばしば外界(i.e. 現実世界?)と直接的な相互作用を持つ。
  - 経験上、外界が安定していることはほとんどない。
  - -> **この外界の変化は、MLシステムに継続的なメンテナンスコストを発生させる**。
- 論文では以下の話が紹介されてた:
  - マニュアルで設定するような閾値の話。外界の変化によって適切でなくなることがある。
  - MLシステムが正常に動いてるか否かのモニタリングが難しい話。

# 7. その他のMLシステム特有の技術的負債

- データテストの負債
  - (コードもデータも重要なんだったら、コードもデータも退行をテストすべきだよね...!みたいな話??:thinking:)
- 再現性の負債
- プロセス管理の負債
  - 成熟したシステムでは、数十から数百のモデルが同時に実行される可能性がある、みたいな話。
- 文化的な負債
  - MLの研究とエンジニアリングの間に存在し得る、協力よりも対立を生じさせがちな文化的な境界、みたいな話:thinking:

# 8. 結論

- 技術的負債は有用なメタファー(隠喩)だが、残念ながら、長期にわたって追跡できる厳密な指標を提供するものではない。(定量評価できないから??:thinking:)
  - **システムの技術的負債をどのように測定し、この負債の全体的なコストを評価するのか?**
    - チームがまだ素早く動くことができるということだけが、低い負債や良い実践の証拠となるわけではない。
    - なぜなら、負債の全体的なコストは時間の経過とともに明らかになるから...!
      - (今素早く開発できiるから負債はない、とは言えないって事か...!:thinking:)

## 8.1. 技術的負債を考える上で有用な質問たち:

  - 1. **全く新しいアルゴリズムのアプローチを、どの程度簡単にfull scaleでテストできるか?** (full scale = 本番環境ってこと?)
  - 2. **全てのdata dependenciesのtransitive closureを把握できているか??**
    - (メモ) transitive closure(推移閉包) = グラフ理論における、要素間の全ての直接的及び間接的な接続のこと、らしい...!
    - なので、技術的負債の文脈でのこの質問は、「**システム内の全てのデータ依存関係の直接的及び間接的な接続をちゃんと把握できているか否か**、もしくは、**ちゃんと把握できる程度にデータ依存関係がシンプルか?**」みたいな意図?? :thinking:
  - 3. **システムに対する新たな変更の影響を、どの程度正確に測定できるか??**
    - (上述の技術的負債1に関する内容っぽい)
  - 4. あるモデルやsignal (=モデルによる成果物など!) を改善すると、他のモデルやsignalが劣化するのか??
    - (各usecaseでのMLモデルの独立性とか、データ依存関係がシンプルだと答えられru質問)
  - 5. チームの新しいメンバーを、いかに早くスピードアップさせることができるか??
    - (システム全体の複雑性を管理できてたら、新メンバーのオンボーディングもスムーズにできるよね...!:thinking:)

## 8.2. 最も重要な洞察:

「**技術的負債は、エンジニアと研究者の両方が認識している必要がある...!**」

- **システムの複雑さを大幅に増大させる代償として、小さな精度の利益を得る研究ソリューションは、賢明なpracticeであることはほとんど無い**。
  - (ここは金銭的なコストの面も言えるよね...!:thinking:)
- ML関連の技術的負債を返済する為には、特定のcommitmentが必要。
  - -> チーム文化が重要。
  - **負債を回避するor返済する為の努力を認識し、優先し、報酬を与える事は、成功するMLチームの長期的な健康にとって重要**...!!
