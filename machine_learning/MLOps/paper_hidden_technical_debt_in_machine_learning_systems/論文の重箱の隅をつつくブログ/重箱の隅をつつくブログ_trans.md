## refs 審判

https://matthewmcateer.me/blog/machine-learning-technical-debt/
https://matthewmcateer.me/blog/machine-learning-technical-debt/

# Nitpicking Machine Learning Technical Debt Nitpicking 機械学習 技術的負債

Revisiting a resurging NeurIPS 2015 paper (and 25 best practices more relevant than that for 2020)
復活したNeurIPS 2015の論文を再考する（そして2020年に向けて、それよりも関連性の高い25のベストプラクティスを考える）

MAY 10, 2020 | UPDATED JULY 9, 2020
 UPDATED JULY 9, 2020

## Background for this post この投稿の背景

I recently revisited the paper Hidden Technical Debt in Machine Learning Systems (Sculley et al.2015) (which I’ll refer to as the Tech Debt Paper throughout this post for the sake of brevity and clarity).
私は最近、Hidden Technical Debt in Machine Learning Systems (Sculley et al.2015)という論文を読み返した（簡潔でわかりやすくするために、この投稿ではTech Debt Paperと呼ぶことにする）。
This was a paper shown at NeurIPS 2015, but it sort of fell to the background because at the time everyone was swooning over projects based on this new “Generative Adversarial Networks” technique from Ian GoodFellow.
これはNeurIPS 2015で発表された論文だが、当時はイアン・グッドフェローの新しい「生成的逆説的ネットワーク」技術に基づくプロジェクトに皆が熱狂していたため、背景には隠れていたようなものだ。

Now the Tech Debt Paper is making a comeback.
今、テック・デット・ペーパーが復活しつつある。
At the time of writing this, there have been 25 papers citing this in the last 75 days.
この記事を書いている時点で、過去75日間に25本の論文が引用されている。
This is understandable, as machine learning has gotten to the point where we need to worry about technical debt.
機械学習は技術的負債を心配しなければならないところまで来ているのだから、これは理解できる。
However, if a lot of people are going to be citing this paper (if not for more than just citing all the papers that have the phrase “machine learning technical debt” in them), we should at least be aware of which parts have and have not stood the test of time.
しかし、もし多くの人がこの論文を引用するのであれば（「機械学習の技術的負債」というフレーズが含まれる論文をすべて引用する以上の理由がないとしても）、少なくとも、どの部分が時の試練に耐え、どの部分が耐えられなかったかを認識すべきだ。
With that in mind, I figured it would save a lot of time and trouble for everyone involved to write up which parts are outdated, and point out the novel methods that have superseded them.
それを念頭に置いて、どの部分が時代遅れなのかを書き上げ、それに取って代わった斬新な方法を指摘することは、関係者全員の時間と手間を省くことになると考えた。
Having worked at companies ranging from fast-growing startups to large companies like Google (the company of the Tech Debt Paper authors), and seeing the same machine learning technical debt mistakes being made everywhere, I felt qualified to comment on this.
急成長中の新興企業からグーグル（Tech Debt Paperの著者の会社）のような大企業まで、さまざまな会社で働いてきた私は、同じ機械学習の技術的負債ミスがいたるところで行われているのを目の当たりにし、これについてコメントする資格があると感じた。

This post covers some of the relevant points of the Tech Debt Paper, while also giving additional advice on top that’s not 5 years out of date.
この投稿では、Tech Debt Paperの関連ポイントをいくつか取り上げつつ、5年前のものではないトップへの追加アドバイスも紹介する。
Some of this advice is in the form of tools that didn’t exist back then…and then some is in the form of tools/techniques that definitely did exist that the authors missed a huge opportunity by not bringing up.
このアドバイスのいくつかは、当時は存在しなかったツールの形をとっている...そしていくつかは、著者が取り上げなかったことで大きなチャンスを逃してしまった、間違いなく存在していたツール／テクニックの形をとっている。

## Introduction 

Tech debt is an analogy for the long-term buildup of costs when engineers make design choices for speed of deployment over everything else.
技術的負債とは、エンジニアが他のすべてよりも配備のスピードを優先して設計上の選択をした場合に、長期的に積み重なるコストの例えである。
Fixing technical debt can take a lot of work.
技術的負債を修正するには、多くの労力がかかる。
It’s the stuff that turns “Move fast and break things” into “Oh no, we went too fast and gotta clean some of this up”
"速く動いて壊す "を "ああ、ダメだ、急ぎすぎた。

Okay, we know technical debt in software is bad, but the authors of this paper assert that technical debt for ML systems specifically is even worse.
さて、ソフトウェアの技術的負債が悪いことは分かっているが、この論文の著者は、特にMLシステムの技術的負債はさらに悪いと主張している。
The Tech Debt Paper proposes a few types of tech debt in ML, and for some of them a few solutions (like how there are different recycling bins, different types of garbage code need different approaches 🚮).
Tech Debt Paperでは、MLにおける技術的負債をいくつかのタイプに分類し、そのうちのいくつかについて解決策を提示している（リサイクル用のゴミ箱が異なるように、異なるタイプのゴミコードには異なるアプローチが必要だ🚮）。
Given that the Tech Debt Paper was an opinion piece that was originally meant to get people’s attention, it’s important to note several pieces of advice from this work that may no longer be relevant, or may have better solutions in the modern day.
Tech Debt Paperが元々人々の注目を集めることを意図したオピニオン・ピースであったことを考えると、この作品にあるいくつかのアドバイスのうち、もはや適切でないかもしれないもの、あるいは現代においてより良い解決策があるかもしれないものに注目することは重要である。

## Part 1: ML tech debt is worse than you thought その1 ML技術負債は想像以上に深刻

You’re all probably familiar by now with technical debt.
技術的負債については、もう皆さんよくご存知だろう。
The Tech Debt Paper starts with a clarification that by technical debt, we’re not referring to adding new capabilities to existing code.
技術的負債ペーパーは、技術的負債とは、既存のコードに新しい機能を追加することを指しているのではないということを明確にすることから始まる。
This is the less glamorous task of writing unit tests, improving readability, adding documentation, getting rid of unused sections, and other such tasks for the sake of making future development easier.
これは、単体テストを書いたり、可読性を高めたり、ドキュメントを追加したり、未使用のセクションを取り除いたりと、将来の開発を容易にするための、あまり派手ではない仕事である。
Well, since standard software engineering is a subset of the skills needed in machine learning engineering, more familiar software engineering tech debt is just a subset of the space of possible ML tech debt.
標準的なソフトウェアエンジニアリングは、機械学習エンジニアリングで必要とされるスキルのサブセットであるため、より身近なソフトウェアエンジニアリングの技術負債は、ML技術負債の可能性のある空間のサブセットに過ぎない。

## Part 2: The Nebulous Nature of Machine Learning Part 2： 機械学習の曖昧な本質

The Tech Debt Paper section after the intro goes into detail about how the nebulous nature of machine learning models makes dealing with tech debt harder.
イントロの後の「テック・デット・ペーパー」では、機械学習モデルの曖昧な性質が、テック・デットへの対処をいかに難しくしているかについて詳しく述べている。
A big part of avoiding or correcting technical debt is making sure the code is properly organized and segregated.
技術的負債を回避・修正するための大きなポイントは、コードが適切に整理され、分離されていることを確認することだ。
The fact is we often use machine learning in cases where precise rules or needs are super hard to specify in real code.
実際のところ、正確なルールやニーズを実際のコードで指定するのが非常に難しい場合に、機械学習を使うことが多い。
Instead of hardcoding the rules to turn data into outputs, more often than not we’re trying to give an algorithm the data and the outputs (and sometimes not even that) to output the rules.
データをアウトプットに変えるためにルールをハードコーディングするのではなく、多くの場合、アルゴリズムにデータとアウトプットを与えて（時にはそれさえも）ルールを出力させようとしている。
We don’t even know what the rules that need segregation and organizing are.
棲み分けや組織化が必要なルールが何なのかさえわかっていない。

Best Practice #1: Use interpretability/explainability tools.
ベストプラクティスその1： 解釈可能性/説明可能性ツールを使用する。

This is where the problem of entanglement comes in.
そこで絡みの問題が出てくる。
Basically, if you change anything about a model, you risk changing the performance of the whole system.
基本的に、モデルについて何かを変更すれば、システム全体のパフォーマンスが変わるリスクがある。
For example, taking a 100-feature model on health records for individuals and adding a 101st feature (like, you’re suddenly listing whether or not they smoked weed).
例えば、個人の健康記録に関する100の機能モデルを用いて、101番目の機能を追加する（例えば、突然マリファナを吸ったかどうかを列挙する）。
Everything’s connected.
すべてがつながっている。
It’s almost like dealing with a chaotic system (ironically enough, a few mathematicians have tried to describe neural networks as chaotic attractors as though they were double pendulums or weather systems).
まるでカオスシステムを扱っているようだ（皮肉なことに、数人の数学者はニューラルネットワークをカオスアトラクターとして、あたかも二重振り子や気象システムのように表現しようとしている）。

The authors suggest a few possible fixes like ensembling models or high-dimensional visualization tools, but even these fall short if any of the ensembled model outputs are correlated, or if the data is too high-dimensional.
著者らは、モデルのアンサンブルや高次元の可視化ツールなど、いくつかの可能な解決策を提案しているが、アンサンブルされたモデル出力のいずれかに相関がある場合や、データが高次元すぎる場合は、これらも不十分である。
A lot of the recommendations for interpretable ML are a bit vague.
解釈可能なMLに関する提言の多くは、少し曖昧だ。
With that in mind, I recommend checking out Facebook’s high-dimensional visualization tool, as well as reading by far the best resource I’ve seen on interpretable machine learning: “Interpretable Machine Learning” by Christoph Molnar (available online here)
このことを念頭に置いて、フェイスブックの高次元可視化ツールをチェックすることと、解釈可能な機械学習について私が見た中で最高のリソースを読むことをお勧めする： クリストフ・モルナー著「解釈可能な機械学習」（オンライン版はこちら）

Sometimes using more explainable model types, like decision trees, can help with this entanglement problem, but the jury’s still out for best practices for solving this for Neural networks.
決定木のような、より説明しやすいモデルタイプを使うことで、このもつれ問題を解決できることもあるが、ニューラル・ネットワークでこの問題を解決するためのベストプラクティスについては、まだ結論が出ていない。

Best Practice #2: Use explainable model types if possible.
ベストプラクティスその2： 可能であれば、説明可能なモデルタイプを使用する。

Correction Cascades are what happens when some of the inputs to your nebulous machine learning model are themselves nebulous machine learning models.
補正カスケードとは、あなたの漠然とした機械学習モデルへの入力の一部が、それ自体漠然とした機械学習モデルである場合に起こるものである。
It’s just setting up this big domino rally of errors.
ドミノ倒しのような大失敗を招きかねない。
It is extremely tempting to set up sequences of models like this, for example, when applying a pre-existing model to a new domain (or a “startup pivot” as so many insist on calling it).
例えば、既存のモデルを新しいドメインに適用する場合（あるいは、多くの人がそう呼ぶ「スタートアップ・ピボット」）、このように一連のモデルを設定することは非常に魅力的である。
You might have an unsupervised dimensionality reduction step right before your random forest, but changing the t-SNE parameters suddenly tanks the performance of the rest of the model.
ランダムフォレストの直前に教師なし次元削減ステップがあるかもしれないが、t-SNEのパラメータを変更すると、残りのモデルのパフォーマンスが突然低下する。
In the worst case scenario, it’s impossible to improve any of the subcomponents without detracting from the performance of the entire system.
最悪の場合、システム全体のパフォーマンスを損なうことなく、サブコンポーネントのどれかを改善することは不可能だ。
Your machine learning pipeline goes from being positive sum to zero sum (that’s not a term from the Tech Debt Paper, I just felt like not adding it in was a missed opportunity).
あなたの機械学習パイプラインは、プラス・サムからゼロ・サムになる（これはTech Debt Paperの用語ではない。）

As far as preventing this, one of the better techniques is a variant of greedy unsupervised layer-wise pretraining (or GULP).
これを防ぐ方法としては、貪欲な教師なし層別事前トレーニング（GULP）の変形がある。
There’s still some disagreement on the mathematical reasons WHY this works so well, but basically you train the early models or early parts of your ensembles, freeze them, and then work your way up the rest of the sequence (again, not mentioning this in the Tech Debt Paper was another missed opportunity, especially since the technique has existed at least since 2007).
なぜこれがうまく機能するのか、その数学的な理由についてはまだ意見が分かれているが、基本的には、初期のモデルまたはアンサンブルの初期部分をトレーニングし、それを凍結させ、それからシーケンスの残りの部分をトレーニングしていくのだ（繰り返しになるが、技術的負債論文でこのことに触れなかったのは、特にこのテクニックは少なくとも2007年から存在していたため、またとない機会損失だった）。

Best Practice #3: Always re-train downstream models in order.
ベストプラクティスその3： 下流のモデルは常に順番に再トレーニングする。

Another inconvenient feature of machine learning models: more consumers might be relying on the outputs than you realize, beyond just other machine learning models.
機械学習モデルのもう一つの不都合な特徴： 他の機械学習モデルだけでなく、あなたが思っている以上に多くの消費者がその出力に依存しているかもしれない。
This is what the authors refer to as Undeclared Consumers.
これが著者の言う「無申告消費者」である。
The issue here isn’t that the output data is unstructured or not formatted right, it’s that nobody’s taking stock of just how many systems depend on the outputs.
ここで問題なのは、出力データが構造化されていないとか、フォーマットが適切でないとかいうことではなく、その出力にどれだけ多くのシステムが依存しているかを誰も把握していないということだ。
For example, there are plenty of custom datasets on sites like Kaggle, many of which are themselves machine learning model outputs.
例えば、Kaggleのようなサイトにはたくさんのカスタムデータセットがあり、その多くは機械学習モデルの出力そのものである。
A lot of projects and startups will often use datasets like this to build and train their initial machine learning models in lieu of having internal datasets of their own.
多くのプロジェクトや新興企業は、自社でデータセットを持つ代わりに、このようなデータセットを使って最初の機械学習モデルを構築し、訓練することが多い。
Scripts and tasks that are dependent on these can find their data sources changing with little notice.
これらに依存しているスクリプトやタスクは、気づかないうちにデータソースが変わっていることがある。
The problem is compounded for APIs that don’t require any kind of sign-in to access data.
データへのアクセスにサインインを必要としないAPIでは、問題はさらに深刻になる。
Unless you have some kind of barrier to entry for accessing the model outputs, like access keys or service-level agreements, this is a pretty tricky one to handle.
アクセスキーやサービスレベル契約のような、モデル出力にアクセスするための何らかの障壁がない限り、これを扱うのはかなり難しい。
You may be just saving your model outputs to a file, and then someone else on the team may decide to use those outputs for a model of their own because, hey, why not, the data’s in the shared directory.
モデルのアウトプットをファイルに保存しておくだけで、チームの誰かがそのアウトプットを自分のモデルに使おうとするかもしれない。
Even if it’s experimental code, you should be careful about who’s accessing model outputs that aren’t verified yet.
たとえそれが実験的なコードであっても、まだ検証されていないモデル出力に誰がアクセスするかには注意すべきだ。
This tends to be a big problem with toolkits like JupyterLab (if I could go back in time and add any kind of warning to the Tech Debt Paper, it would be a warning about JupyterLab).
これは、JupyterLabのようなツールキットでは大きな問題になりがちだ（過去にさかのぼってTech Debt Paperに何らかの警告を加えることができるとしたら、それはJupyterLabについての警告だろう）。

Basically fixing this type of technical debt involves cooperation between machine learning engineers and security engineers.
基本的に、この種の技術的負債を解決するには、機械学習エンジニアとセキュリティ・エンジニアの協力が必要だ。

Best Practice #4: Set up access keys, directory permissions, and service-level-agreements.
ベストプラクティスその4： アクセスキー、ディレクトリパーミッション、サービスレベルアグリーメントを設定する。

## Section 3: Data Dependencies (on top of regular dependencies) セクション3： データ依存関係 (通常の依存関係の上に)

The third section goes a bit deeper with data dependency issues.
第3節では、データ依存の問題をもう少し深く掘り下げる。
More bad news: in addition to the regular code dependencies of software engineering, machine learning systems will also depend on large data sources that are probably more unstable than the developers realize.
さらに悪いニュースがある： ソフトウェアエンジニアリングにおける通常のコード依存に加え、機械学習システムは、おそらく開発者が思っている以上に不安定な大規模データソースにも依存することになる。

For example, your input data might take the form of a lookup table that’s changing underneath you, or a continuous data stream, or you might be using data from an API you don’t even own.
例えば、入力データはルックアップテーブルのような形かもしれないし、連続的なデータストリームかもしれない。
Imagine if the host of the MolNet dataset decided to update it with more accurate numbers (ignoring for a moment how they would do this for a moment).
もしMolNetデータセットのホストが、より正確な数字で更新することを決めたとしたらどうだろう（彼らがどのようにするのかはちょっと無視して）。
While the data may reflect reality more accurately, countless models have been built against the old data, and many of the makers will suddenly find that their accuracy is tanking when they re-run a notebook that definitely worked just last week.
データは現実をより正確に反映しているかもしれないが、数え切れないほどのモデルが古いデータに基づいて作られており、メーカーの多くは、先週まで間違いなく機能していたノートを再実行すると、突然その精度が落ちていることに気づくだろう。

One of the proposals by the authors is to use data dependency tracking tools like Photon for versioning.
著者の提案のひとつは、バージョン管理のためにPhotonのようなデータ依存性追跡ツールを使うことだ。
That being said in 2020 we also have newer tools like DVC, which literally just stands for “Data Version Control”, that make Photon obsolete for the most part.
とはいえ、2020年にはDVC（文字通り "Data Version Control "の略）のような新しいツールも登場する。
It behaves much the same way as git, and saves a DAG keeping track of the changes in a dataset/database.
gitとほぼ同じように動作し、データセット/データベースの変更を追跡するDAGを保存する。
Two other great tools to be used together for versioning are Streamlit (for keeping track of experiments and prototypes) and Netflix’s Metaflow.
バージョニングのために一緒に使える他の2つの素晴らしいツールは、Streamlit（実験やプロトタイプの追跡用）とNetflixのMetaflowだ。
How much version control you do will come down to a tradeoff between extra memory and avoiding some giant gap in the training process.
バージョン管理をどの程度行うかは、余分なメモリとトレーニング過程における巨大なギャップを避けることのトレードオフに帰着する。
Still, insufficient or inappropriate versioning will lead to enormous survivorship bias (and thus wasted potential) when it comes to model training
それでもなお、不十分あるいは不適切なバージョニングは、モデル・トレーニングの際に膨大なサバイバーシップ・バイアス（つまり潜在能力の浪費）につながる。

Best Practice #5: Use a data versioning tool.
ベストプラクティス#5： データのバージョン管理ツールを使用する。

The data dependency horror show goes on.
データ依存の恐怖のショーは続く。
Compared to the unstable data dependencies, the underutilized ones might not seem as bad, but that’s how they get you! Basically, you need to keep a lookout for data that’s unused, data that was once used but is considered legacy now, and data that’s redundant because it’s heavily correlated with something else.
不安定なデータ依存に比べれば、十分に活用されていないデータはそれほど悪いものには見えないかもしれない！基本的には、使われていないデータ、かつて使われていたが今はレガシーとみなされているデータ、他の何かと大きく相関しているために冗長になっているデータに注意を払う必要がある。
If you’re managing a data pipeline where it turns out entire gigabytes are redundant, that will incur development costs on its own just as well.
ギガバイト全体が冗長であることが判明したデータパイプラインを管理している場合、それだけで開発コストが発生する。

The correlated data is especially tricky, because you need to figure out which variable is the correlated one, and which is the causative one.
相関のあるデータは特にやっかいで、どの変数が相関のあるもので、どの変数が因果のあるものかを見極める必要があるからだ。
This is a big problem in biological data.
これは生物学的データでは大きな問題である。
Tools like ANCOVA are increasingly outdated, and they’re unfortunately being used in scenarios where some of the ANCOVA assumptions definitely don’t apply.
ANCOVAのようなツールはますます時代遅れになってきており、残念なことにANCOVAの仮定が間違いなく当てはまらないようなシナリオで使われている。
A few groups have tried proposing alternatives like ONION and Domain Aware Neural Networks, but many of these are improving upon fairly unimpressive standard approaches.
ONIONやDomain Aware Neural Networkのような代替案を提案しようとするグループもいくつかあるが、これらの多くは、かなり印象の悪い標準的なアプローチを改良したものだ。
Some companies like Microsoft and QuantumBlack have come up with packages for causal disentanglement (DoWhy and CausalNex respectively).
マイクロソフト社やQuantumBlack社のように、因果関係解明のためのパッケージ（それぞれDoWhyとCausalNex）を開発している企業もある。
I’m particularly fond of DeepMind’s work on Bayesian Causal Reasoning.
私はディープマインドのベイズ因果推論に関する研究が特に好きだ。
Most of these were not around at the time of the Tech Debt Paper’s writing, and many of these packages have their own usability debt, but it’s important to make it known that ANCOVA is not a one-size-fits-all solution to this.
これらのほとんどは、Tech Debt Paperが書かれた時点では存在しておらず、これらのパッケージの多くには独自のユーザビリティ負債があるが、ANCOVAがこれに対する万能の解決策ではないことを知らしめることが重要である。

Best Practice #6: Drop unused files, extraneous correlated features, and maybe use a causal inference toolkit.
ベストプラクティスその6： 未使用のファイルや余計な相関フィーチャーを削除し、因果推論ツールキットを使用する。

Anyway, the authors were a bit less pessimistic about the fixes for these.
いずれにせよ、著者はこれらの修正については少し悲観的ではなかった。
They suggested a static analysis of data dependencies, giving the one used by Google in their click-through predictions as an example.
彼らは、グーグルがクリックスルー予測に使用しているものを例に挙げ、データの依存関係を静的に分析することを提案した。
Since the Tech Debt Paper was published the pool of options for addressing this has grown a lot.
Tech Debt Paperが発表されて以来、この問題に対処するための選択肢は大幅に増えた。
For example, there are tools like Snorkel which lets you track which slices of data are being used for which experiments.
例えば、Snorkelのようなツールがあり、どのデータのどのスライスがどの実験に使われているかを追跡することができる。
Cloud Services like AWS and Azure have their own data dependency tracking services for DevOps, and there’s also tools like Red Gate SQL dependency tracker.
AWSやAzureのようなクラウドサービスは、DevOpsのために独自のデータ依存性追跡サービスを持っているし、Red Gate SQL依存性追跡ツールのようなツールもある。
So, yeah, looks like the authors were justified in being optimistic about that one.
だから、著者たちがこの件に関して楽観的であったのは正当だったようだ。

Best Practice #7: Use any of the countless DevOps tools that track data dependencies.
ベストプラクティスその7： データの依存関係を追跡する無数のDevOpsツールのいずれかを使用する。

## Part 4: Frustratingly undefinable feedback loops ＃その4．定義できないフィードバック・ループに苛立つ

Now we had a bit of a hope spot in the previous section, but the bad news doesn’t just stop at data dependencies.
しかし、悪いニュースはデータ依存だけにとどまらない。
Section 4 of the paper goes into how unchecked feedback loops can influence the machine learning development cycle.
本稿のセクション4では、チェックされていないフィードバック・ループが機械学習の開発サイクルにどのような影響を与えるかについて述べる。
This can both refer to direct feedback loops like in semi-supervised learning or reinforcement learning, or indirect loops like engineers basing their design choices off of another machine learning output.
これは、半教師付き学習や強化学習のような直接的なフィードバック・ループを指す場合もあれば、エンジニアが別の機械学習の出力に基づいて設計の選択をするような間接的なループを指す場合もある。
This is one of the least defined issues in the Tech Debt Paper, but countless other organizations are working on this feedback loop problem, including what seems like the entirety of OpenAI (at least that’s what the “Long Term Safety” section of their charter, before all that “Capped Profit” hubbub).
しかし、OpenAIの全組織がこのフィードバックループの問題に取り組んでいるようだ（少なくとも、彼らの憲章の「長期的な安全性」のセクションは、「利益の上限」の騒動の前にそうなっている）。
What I’m trying to say is that if you’re going to be doing research on direct or indirect feedback loops, you’ve got much better and more specific options than this paper.
私が言いたいのは、直接的あるいは間接的なフィードバックループの研究をするのであれば、この論文よりももっと具体的で良い選択肢があるということだ。

This one goes back on track with solutions that seem a bit more hopeless than the last section.
前節より少し絶望的と思える解決策で軌道修正。
They give examples of bandit algorithms as being resistant to the direct feedback loops, but not only do those not scale, technical debt accumulates the most when you’re trying to build systems at scale.
彼らは、直接的なフィードバック・ループに強いとしてバンディット・アルゴリズムの例を挙げているが、それはスケールしないだけでなく、スケールするシステムを構築しようとするときに技術的負債が最も蓄積される。
Useless.
役に立たない。
The indirect feedback fixes aren’t much better.
間接的なフィードバックの修正はあまり良くない。
In fact, the systems in the indirect feedback loop might not even be part of the same organization.
実際、間接的なフィードバック・ループにあるシステムは、同じ組織に属していないかもしれない。
This could be something like trading algorithms from different firms each trying to meta-game each other, but instead causing a flash crash.
これは、異なる会社の取引アルゴリズムが互いにメタゲームを試みているが、その代わりにフラッシュクラッシュを引き起こしているようなものかもしれない。
Or a more relevant example in biotech, suppose you have a model that’s predicting the error likelihood for a variety of pieces of lab equipment.
あるいは、バイオテクノロジーに関連した例として、さまざまな実験器具の誤差の可能性を予測するモデルがあるとする。
As time goes on, the actual error rate could go down because people have become more practiced with it, or possibly up because the scientists are using the equipment more frequently, but the calibrations haven’t increased in frequency to compensate.
時間が経つにつれて、実際の誤差率は、人々がより慣れ親しんだために下がるかもしれないし、科学者がより頻繁に機器を使用するようになったために上がるかもしれないが、校正の頻度はそれを補うほどには増えていない。
Ultimately, fixing this comes down to high-level design decisions, and making sure you check as many assumptions behind your model’s data (especially the independence assumption) as possible.
結局のところ、この問題を解決するには、ハイレベルな設計上の決定と、モデルのデータの背後にある仮定（特に独立性の仮定）をできるだけ多く確認することに尽きる。

This is also an area where many principles and practices from security engineering become very useful (e.g., tracking the flow of data throughout a system, searching for ways the system can be abused before bad actors can make use of them).
これはまた、セキュリティ・エンジニアリングの多くの原則と実践が非常に役立つ分野でもある（例えば、システム全体のデータの流れを追跡し、悪意ある行為者がそれを利用する前に、システムが悪用される可能性のある方法を探索する）。

Best Practice #8: Check independence assumptions behind models (and work closely with security engineers).
ベストプラクティス#8： モデルの背後にある独立性の前提条件をチェックする（セキュリティエンジニアと緊密に連携する）。

By now, especially after the ANCOVA comments, you’re probably sensing a theme about testing assumptions.
さて、特にANCOVAのコメントの後では、仮定をテストするというテーマを感じていることだろう。
I wish this was something the authors devoted at least an entire section to.
せめて一節を割いてほしいものだ。

## Part 5: Common no-no patterns in your ML code パート5： MLコードにありがちなNGパターン

The “Anti-patterns” section of the Tech Debt Paper was a little more actionable than the last one.
Tech Debt Paperの "Anti-patterns "のセクションは、前回のものよりも少し実用的だった。
This part went into higher-level patterns that are much-easier to spot than indirect-feedback loops.
このパートでは、間接的なフィードバックループよりもはるかに見つけやすい、より高度なパターンに踏み込んだ。

(This is actually a table from the Tech Debt Paper, but with hyperlinks to actionable advice on how to fix them.
(この表は、実際には「Tech Debt Paper」に掲載されたものだが、これらの問題を解決するための実用的なアドバイスへのハイパーリンクが付されている。
This table was possibly redundant, as the authors discuss unique code smells and anti-patterns in ML, but these are all regular software engineering anti-patterns you should address in your code first.)
この表は、著者がMLにおけるユニークなコード臭やアンチパターンについて論じているため、もしかしたら冗長かもしれないが、これらはすべて、あなたのコードで最初に対処すべき、通常のソフトウェアエンジニアリングのアンチパターンである)。

The majority of these patterns revolve around the 90% or more of ML code that’s just maintaining the model.
これらのパターンの大半は、モデルを維持するだけのMLコードの90％以上を中心に展開される。
This is the plumbing that most people in a Kaggle competition might think doesn’t exist.
これは、Kaggleのコンペティションに参加するほとんどの人が存在しないと思うかもしれない配管です。
Solving cell segmentation is a lot easier when you’re not spending most of your time digging through the code connecting the Tecan Evo camera to your model input.
Tecan Evoカメラとモデル入力を接続するコードに時間を費やすことがなければ、細胞分割を解くのはずっと簡単になる。

Best Practice #9: Use regular code-reviews (and/or use automatic code-sniffing tools).
ベストプラクティス#9： 定期的なコードレビューの実施（および／または自動コードスニッフィングツールの使用）。

The first ML-anti-pattern introduced is called “glue code”.
最初に紹介したMLアンチパターンは「グルーコード」と呼ばれる。
This is all the code you write when you’re trying to fit data or tools from a general-purpose package into a super-specific model that you have.
これは、汎用パッケージのデータやツールを、あなたが持っている超特殊なモデルに適合させようとするときに書くコードすべてだ。
Anyone that’s ever tried doing something with packages like RDKit knows what I’m talking about.
RDKitのようなパッケージを使って何かをしようとしたことがある人なら、私が何を言っているのかわかるだろう。
Basically, most of the stuff you shove into the utils.py file can count as this (everyone does it).
基本的に、あなたがutils.pyファイルに押し込んだもののほとんどは、これとして数えることができます(誰もがやっています)。
These (hopefully) should be fixable by repackaging these dependencies as more specific API endpoints.
これらは（うまくいけば）、これらの依存関係をより具体的なAPIエンドポイントとして再パッケージ化することで修正できるはずだ。

Best Practice #10: Repackage general-purpose dependencies into specific APIs.
ベストプラクティス#10： 汎用的な依存関係を特定のAPIにリパッケージする。

“Pipeline jungles” are a little bit tricker, as this is where a lot of glue code accumulates.
「パイプライン・ジャングル」は少し厄介で、ここには多くの接着剤コードが溜まっているからだ。
This is where all the transformations that you add for every little new data source piles up into an ugly amalgam.
これは、新しいデータソースを追加するたびに、すべての変換が積み重なり、醜いアマルガムになるところだ。
Unlike with Glue Code, the authors pretty much recommend letting go and redesigning codebases like this from scratch.
Glue Codeとは異なり、著者はこのようなコードベースは手放し、ゼロから再設計することを推奨している。
I want to say this is something that has more options nowadays, but when glue code turns into pipeline jungles even tools like Uber’s Michelangelo can become part of the problem.
しかし、グルーコードがパイプラインのジャングルと化すと、ウーバーのミケランジェロのようなツールでさえも問題の一部となりうる。

Of course, the advantage of the authors’ advice is that you can make this replacement code seem like an exciting new project with a cool name that’s also an obligatory Tolkien reference, like “Balrog” (as yes, ignoring unfortunate implications of your project name isn’t just Palantir’s domain.
もちろん、著者のアドバイスの利点は、この置き換えコードを、"Balrog "のようなトールキンの引用を義務づけたクールな名前を持つ、エキサイティングな新しいプロジェクトのように見せることができることだ（そう、プロジェクト名の不幸な意味合いを無視することは、Palantirだけの領域ではない。
You’re free to do that as well).
それも自由だ）。

Best Practice #11: Get rid of Pipeline jungles with top-down redesign/reimplementation.
ベストプラクティス#11： トップダウンの再設計／再実装でパイプラインのジャングルをなくす。

On the subject of letting go, experimental code.
手放すというテーマでは、実験的なコード。
Yes, you thought you could just save that experimental code for later.
そう、あなたはその実験的なコードを後で保存すればいいと思っていた。
You thought you could just put it in an unused function or unreferenced file and it would be all fine.
未使用の関数や参照されないファイルに入れれば問題ないと思ったのだろう。
Unfortunately, stuff like this is part of why maintaining backwards compatibility can be such a pain in the neck.
残念ながら、このようなことが後方互換性を維持することが首の痛くなる理由の一部なのだ。
Anyone that’s taken a deep dive into the Tensorflow framework can see the remains of frameworks that were only partially absorbed, experimental code, or even incomplete “TODO” code that was left for some other engineer to take care of at a later date.
Tensorflowフレームワークに深く潜ったことのある人なら誰でも、部分的にしか吸収されなかったフレームワーク、実験的なコード、あるいは後日他のエンジニアに任せるために残された不完全な「TODO」コードの残骸を見ることができる。
You probably first came across these while trying to debug your mysteriously failing Tensorflow code.
おそらく、謎の失敗をするTensorflowコードをデバッグしようとしているときに、初めてこのようなものに出会ったことだろう。
This certainly puts all the compatibility hiccups between Tensorflow 1.X and 2.X in a new light.
このことは、Tensorflow 1.Xと2.Xの間の互換性の問題を、新たな視点でとらえることになる。
Do yourself a favor, and don’t put off pruning your codebase for 5 years.
自分のために、コードベースの整理を5年も先延ばしにしないことだ。
Keep doing experiments, but set some criteria for when to quarantine an experiment away from the rest of the code.
実験は続けるが、実験を他のコードから隔離するときの基準を決めておくこと。

Best Practice #12: Set regular checks and criteria for removing code, or put the code in a directory or on a disk far-removed from the business-critical stuff.
ベストプラクティス#12： コードを削除するための定期的なチェックと基準を設定する。または、コードをビジネスクリティカルなものから遠く離れたディレクトリやディスクに置く。

Speaking of old code, you know what software engineering has had for a while now? Really great abstractions! Everything from the concept of relational databases to views in web pages.
古いコードといえば、ソフトウェア工学がここしばらくの間持っていたものをご存知だろうか？本当に素晴らしい抽象化だ！リレーショナル・データベースの概念からウェブページのビューまで、すべてがそうだ。
There are entire branches of applied category theory devoted to figuring out the best ways to organize code like this.
応用カテゴリー理論には、このようにコードを整理する最良の方法を解明することに専念する分野がある。
You know what applied category theory hasn’t quite caught up to yet? That’s right, machine learning code organization.
応用カテゴリー理論がまだ追いついていないものをご存知だろうか？そう、機械学習によるコード整理だ。
Software engineering has had decades of throwing abstraction spaghetti at the wall and seeing what sticks.
ソフトウェア工学は、何十年もの間、抽象化スパゲッティを壁に投げつけ、何がくっつくかを見てきた。
Machine learning? Aside from Map-Reduce (which is like, not as impressive relational databases) or Async Parameter servers (which nobody can agree on how this should be done), or sync allreduce (which just sucks for most use-cases), we don’t have much to show.
機械学習？Map-Reduce（これはリレーショナル・データベースほど印象的ではない）や非同期パラメータ・サーバー（これはどのように行うべきか誰も同意できない）、sync allreduce（これはほとんどのユースケースにとって最悪だ）を除けば、私たちはあまり見せるものがない。

In fact, between groups doing research on random networks and Pytorch advertising how fluid the nodes in their neural networks are, Machine Learning has been throwing the abstraction spaghetti clean out the window! I don’t think the authors realized that this problem was going to get MUCH worse as time went on.
実際、ランダムネットワークの研究をしているグループと、ニューラルネットワークのノードがいかに流動的であるかを宣伝しているPytorchの間で、機械学習は抽象化されたスパゲッティを窓の外に投げ捨てている！著者たちは、この問題が時間が経つにつれて非常に悪化していくことに気づいていなかったと思う。
My recommendation? Read more of the literature on the popular high-level abstractions, and maybe don’t use PyTorch for production code.
私のお勧めは？一般的な高水準抽象化機能に関する文献をもっと読んで、PyTorchをプロダクションコードに使わないこと。

Best Practice #13: Stay up-to-date on abstractions that are becoming more solidified with time.
ベストプラクティス第13号： 時間の経過とともに固まりつつある抽象化について、常に最新の情報を得ること。

I’ve met plenty of senior machine learning engineers who have pet frameworks that they like to use for most problems.
私は、多くの機械学習エンジニアに会ってきたが、彼らはほとんどの問題で使用するお気に入りのフレームワークを持っている。
I’ve also seen many of the same engineers watch their favorite framework fall to pieces when applied to a new context, or get replaced by another framework that’s functionally indistinguishable.
また、同じエンジニアの多くが、お気に入りのフレームワークが新しい文脈に適用されたときに粉々になったり、機能的に見分けがつかない別のフレームワークに取って代わられたりするのを見てきた。
This is especially prevalent on teams doing anything with distributed machine learning.
これは、分散型機械学習を行うチームでは特に顕著だ。
I want to make something absolutely clear:
はっきりさせておきたいことがある：

Aside from MapReduce, you should avoid getting too attached to any single framework.
MapReduceは別として、特定のフレームワークに固執しすぎるのは避けるべきだ。
If your “senior” machine learning engineer believes with all their being that Michelangelo is the bee’s knees and will solve everything, they’re probably not all that senior.
もしあなたの "上級 "機械学習エンジニアが、ミケランジェロこそが蜂の膝であり、すべてを解決してくれると全身全霊で信じているのであれば、そのエンジニアはおそらく上級ではないだろう。
While ML engineering has matured, it’s still relatively new.
MLエンジニアリングは成熟してきたとはいえ、まだ比較的新しい。
An actually “senior” senior ML engineer will probably focus on making workflows that are framework agnostic, since they know most of those frameworks are not long for this world.
実際に "上級 "のMLエンジニアは、フレームワークにとらわれないワークフローを作ることに集中するだろう。
⚰️
⚰️

Now, the previous sections mentioned a bunch of distinct scenarios and qualities of technical debt in ML, but they also provide examples of higher-level anti-patterns for ML development.
さて、ここまでのセクションでは、MLにおける技術的負債のシナリオと性質について述べましたが、同時にML開発におけるより高度なアンチパターンの例も挙げました。

Most of you reading this have probably heard the phrase code-smells going around.
これを読んでいるほとんどの人は、コード臭がするという言葉を耳にしたことがあるだろう。
You’ve probably used tools like good-smell or Pep8-auto-checking (or even the hot new Black auto-formatter that everyone is using on their production python code).
あなたはおそらくgood-smellやPep8-auto-checkingのようなツールを使ったことがあるでしょう（あるいは、誰もが本番のPythonコードで使っているホットな新しいBlack自動整形も）。
Truth be told I don’t like this term “code smell”.
実を言うと、私はこの「コード臭」という言葉が好きではない。
“Smell” always seems to imply something subtle, but the patterns described in the next section are pretty blatant.
「匂い」は常に微妙なものを暗示しているように見えるが、次のセクションで説明するパターンはかなり露骨だ。
Nonetheless, the authors list a few types of code smells that indicate a high level of debt (beyond the usual types of code smells).
それにもかかわらず、著者は（通常のコード・スモークの種類を超えて）高水準の負債を示すコード・スモークの種類をいくつか挙げている。
For some reason, they only started listing the code-smells halfway into the section on code smells.
どういうわけか、彼らはコード臭のセクションの途中からしかコード臭を列挙しなかった。

The “Plain data” smell You may have code that’s dealing with a lot of data in the form of numpy floats.
プレーンなデータ」の匂い numpyの浮動小数点数形式で大量のデータを扱うコードがあるかもしれない。
There may be little information preserved about the nature of the data, such as whether your RNA read counts represent samples from a Bernoulli distribution, or whether your float is a log of a number.
RNAリードカウントがベルヌーイ分布からのサンプルなのか、フロートが数値の対数なのかなど、データの性質に関する情報はほとんど保存されていないかもしれない。
They don’t mention this in the Tech Debt Paper, but this is one area where using typing in python can help out.
Tech Debt Paperでは触れられていないが、これはパイソンでタイピングを使うことで解決できる分野だ。
Avoiding unnecessary use of floats, or floats with too much precision will go a long way.
不必要な浮き輪の使用や、精度の高すぎる浮き輪の使用は避けるべきだろう。
Again, using the built-in Decimal or Typing packages will help a lot (and not just for code navigation but also speedups on CPUs).
繰り返しになるが、組み込みのDecimalパッケージやTypingパッケージを使うことは大いに役立つ（コードのナビゲーションだけでなく、CPUのスピードアップにもつながる）。

Best Practice #14: Use packages like Typing and Decimal, and don’t use ‘float32’ for all data objects.
ベストプラクティスその14： TypingやDecimalのようなパッケージを使用し、すべてのデータオブジェクトに'float32'を使用しないこと。

The “Prototyping” smell Anyone that’s been in a hackathon knows that code slapped together in under 24 hours has a certain look to it.
プロトタイピング」の匂い ハッカソンに参加したことのある人なら誰でも、24時間以内に叩き出されたコードにはある種の見栄えがあることを知っている。
This ties back into the unused experimental code mentioned earlier.
これは、先に述べた未使用の実験的コードと関連している。
Yes, you might be all excited to try out the new PHATE dimensionality reduction tool for biological data, but either clean up your code or throw it out.
生物学的データのための新しい次元削減ツールPHATEを試すことに興奮しているかもしれないが、コードをきれいにするか、それを捨てるかのどちらかだ。

Best Practice #15: Don’t leave all works-in-progress in the same directory.
ベストプラクティス#15： すべての仕掛品を同じディレクトリに置かない。
Clean it up or toss it out.
掃除するか捨てるかだ。

The “Multi-language” smell Speaking of language typing, multi-language-codebases act almost like a multiplier for technical debt and make it pile up much faster.
多言語」臭 言語タイピングについて言えば、多言語コードベースは技術的負債を倍増させるようなもので、負債をより早く積み上げることになる。
Sure, these languages all have their benefits.
確かに、これらの言語にはどれも利点がある。
Python is great for building ideas fast.
Pythonはアイデアを素早く構築するのに適している。
JavaScript is great for interfaces.
JavaScriptはインターフェースに最適だ。
C++ is great for graphics and making computations go fast.
C++はグラフィックスや計算の高速化に適している。
PHP…uhhh…okay maybe not that one.
PHPは......ああ......そうかもしれない。
Golang is useful if you’re working with kubernetes (and you work at Google).
Golangは、あなたがkubernetesを使って仕事をしているなら（そしてあなたがGoogleで働いているなら）役に立つ。
But if you’re making these languages talk to each other there will be a lot of spots for things to go wrong, whether it be broken endpoints or memory leaks.
しかし、これらの言語を互いに会話させるのであれば、エンドポイントの破損やメモリーリークなど、うまくいかない点がたくさん出てくるだろう。
At least in machine learning, there are a few toolkits like Spark and Tensorflow that have similar semantics between languages.
少なくとも機械学習では、SparkやTensorflowのように、言語間で似たようなセマンティクスを持つツールキットがいくつかある。
If you absolutely must use multiple languages, at least we now have that going for us post-2015.
どうしても多言語を使いたいのであれば、少なくとも2015年以降はそれが可能だ。

Best Practice #16: Make sure endpoints are accounted for, and use frameworks that have similar abstractions between languages.
ベストプラクティス#16： エンドポイントが考慮されていることを確認し、言語間で同様の抽象度を持つフレームワークを使用する。

(Calling this a code-smell was a weird choice, as this is a pretty blatant pattern even by the standard of usual code-smells)
(通常のコード臭の基準からしても、これはかなり露骨なパターンなので、これをコード臭と呼ぶのは奇妙な選択だった）。

## Part 6: Configuration Debt (boring but easy to fix) コンフィギュレーション・デット（退屈だが簡単に解決できる）

The “Configuration debt” section of the Tech Debt Paper is probably the least exciting one, but the problem it describes is the easiest to fix.
Tech Debt Paperの "Configuration debt "のセクションは、おそらく最もエキサイティングなものではないが、そこに書かれている問題は最も簡単に解決できるものである。
Basically, this is just the practice of making sure all the tuneable and configurable information about your machine learning pipeline is in one place, and that you don’t have to go searching through multiple directories just to figure out how many units your second LSTM layer had.
基本的に、これは機械学習パイプラインに関するすべての調整可能で設定可能な情報が1つの場所にあることを確認し、2番目のLSTMレイヤーのユニット数を把握するためだけに複数のディレクトリを検索する必要がないようにすることだ。
Even if you’ve gotten into the habit of creating config files, the packages and technologies haven’t all caught up with you.
コンフィグファイルを作成する習慣が身についていたとしても、パッケージやテクノロジーがすべてあなたに追いついているわけではない。
Aside from some general principles, this part of the Tech Debt Paper doesn’t go into too much detail.
いくつかの一般原則を除けば、技術負債報告書のこの部分はあまり詳細には触れていない。
I suspect that the authors of the Tech Debt Paper were more used to packages like Caffe (in which case yes, setting up configs with Caffe protobufs was objectively buggy and terrible).
Tech Debt Paperの著者は、Caffeのようなパッケージに慣れていたのではないかと思う（その場合、Caffeのプロトタイプを使ったコンフィグ設定は、客観的に見てバグが多く、ひどいものだった）。

Personally, I would suggest using a framework like tf.Keras or Chainer if you’re going to be setting up configuration files.
個人的には、設定ファイルをセットアップするのであれば、tf.KerasやChainerのようなフレームワークを使うことをお勧めする。
Most cloud services have some version of configuration management, but outside of that you should at least be prepared to use a config.json file or parameter flags in your code.
ほとんどのクラウド・サービスには、何らかのバージョンのコンフィギュレーション管理があるが、それ以外では、少なくともconfig.jsonファイルやコード内のパラメータ・フラグを使う準備をしておく必要がある。

Best Practice #17: Make it so you can set your file paths, hyperparameters, layer type and layer order, and other settings from one location.
ベストプラクティスその17： ファイルパス、ハイパーパラメータ、レイヤーの種類、レイヤーの順序、その他の設定を1カ所で行えるようにする。

If you’re going to be tuning these settings with a command line, try to use a package like Click instead of Argparse.
これらの設定をコマンドラインで調整するのであれば、Argparseの代わりにClickのようなパッケージを使ってみてほしい。

## Part 7: The real world dashing your dreams of solving this Part 7： 解決への夢を打ち砕く現実の世界

Section 7 acknowledges that a lot of managing tech debt is preparing for the fact that you’re dealing with a constantly changing real world.
第7章では、技術的負債を管理することの多くが、絶えず変化する現実の世界に対処するための準備であることを認めている。
For example, you might have a model where there’s some kind of decision threshold for converting a model output into a classification, or picking a True or False Boolean.
例えば、モデルの出力を分類に変換するための、あるいは真か偽のブール値を選ぶための、ある種の決定しきい値があるモデルがあるかもしれない。
Any group or company that works with biological or health data is familiar with how diagnosis criteria can change rapidly.
生物学的データや健康データを扱う団体や企業であれば、診断基準がいかに急速に変化しうるかを熟知している。
You shouldn’t assume the thresholds you work with will last forever, especially if you’re doing anything with bayesian machine learning.
特にベイジアン機械学習で何かをするのであればなおさらだ。

Best Practice #18: Monitor the models’ real-world performance and decision boundaries constantly.
ベストプラクティスその18： モデルの実世界でのパフォーマンスと意思決定の境界を常に監視する。

The section stresses the importance of real-time monitoring; I can definitely get behind this.
このセクションでは、リアルタイム・モニタリングの重要性を強調している。
As for which things to monitor, the paper’s not a comprehensive guide but they give a few examples.
どのようなことをモニターすべきかについては、この論文は包括的なガイドではないが、いくつかの例を挙げている。
One is to compare the summary statistics for your predicted labels with the summary statistics of the observed labels.
一つは、予測されたラベルの要約統計量と観測されたラベルの要約統計量を比較することである。
It’s not foolproof, but it’s like checking a small animal’s weight.
確実ではないが、小動物の体重をチェックするようなものだ。
If something’s very wrong there, it can alert you to a separate problem very quickly.
そこに何か大きな問題があれば、別の問題を素早く警告することができる。

Best Practice #19: Make sure distribution of predicted labels is similar to distribution of observed labels.
ベストプラクティス#19： 予測されたラベルの分布が、観測されたラベルの分布と類似していることを確認する。

If your system is making any kind of real-world decisions, you probably want to put some kind of rate limiter on it.
もしあなたのシステムが実世界で何らかの決定を下すのであれば、おそらく何らかのレートリミッターをかけたいだろう。
Even if your system is NOT being trusted with millions of dollars for bidding on stocks, even if it’s just to alert you that something’s not right with the cell culture incubators, you will regret not setting some kind of action limit per unit of time.
たとえあなたのシステムが株の入札で何百万ドルも任されていなくても、細胞培養インキュベーターに何か異常があることを警告するためであっても、単位時間あたりの何らかのアクション制限を設定しなかったことを後悔することになるだろう。

Best Practice #20: Put limits on real-world decisions that can be made by machine learning systems.
ベストプラクティス#20： 機械学習システムで行える現実世界の意思決定に制限を設ける。

You also want to be mindful of any changes with upstream producers of the data your ML pipeline is consuming.
また、MLパイプラインが消費するデータの上流生産者の変更にも注意したい。
For example, any company running machine learning on human blood or DNA samples obviously wants to make sure those samples are all collected with a standardized procedure.
例えば、人間の血液やDNAサンプルを使って機械学習を行う企業は、当然ながら、それらのサンプルがすべて標準化された手順で採取されたものであることを確認したい。
If a bunch of samples are all coming from a certain demographic, the company should make sure that won’t skew their analysis.
多くのサンプルがすべて特定の層から得られている場合、企業はそれが分析に歪みを与えないことを確認する必要がある。
If you’re doing some kind of single-cell sequencing on cultured human cells, you want to make sure you’re not confusing cancer cells dying due to a drug working with, say, an intern accidentally letting the cell cultured dehydrate.
培養したヒト細胞のシングルセルシークエンシングを行う場合、例えば、インターンが培養した細胞を誤って脱水させてしまい、薬剤が作用してがん細胞が死滅するのと混同しないようにしたい。
The authors say ideally you want a system that can respond to these changes (e.g., logging, turning itself off, changing decision thresholds, alert a technician or whomever does repairs) even when humans aren’t available.
著者によれば、理想的には、人間が利用できないときでも、このような変化に対応できるシステム（例えば、ログを記録したり、電源を切ったり、判定しきい値を変更したり、技術者や修理担当者に警告を発したり）が望ましいという。

Best Practice #21: Check assumptions behind input data.
ベストプラクティス#21： 入力データの背後にある仮定をチェックする。

## Part 8: The weirdly meta section その8 奇妙なメタセクション

The penultimate section of the Tech Debt Paper goes on to mention other areas.
Tech Debt Paperの最後のセクションは、他の分野についても言及している。
The authors previously mentioned failure of abstraction as a type of technical debt, and apparently that extends to the authors not being able to fit all these technical debt types into the first 7 sections of the paper.
著者は以前、技術的負債の一種として抽象化の失敗を挙げたが、どうやらそれは、これらの技術的負債タイプをすべて論文の最初の7つのセクションに収めることができなかったことにまで及んでいるようだ。

Sanity Checks
正気度チェック

Moving on, it’s critically important to have sanity checks on the data.
次に、データの健全性をチェックすることが決定的に重要だ。
If you’re training a new model, you want to make sure your model is at least capable of overfitting to one type of category in the data.
新しいモデルをトレーニングする場合、モデルが少なくともデータの1種類のカテゴリーにオーバーフィットできることを確認したい。
If it’s not converging on anything, you might want to check that the data isn’t random noise before tuning those hyperparameters.
もし何も収束しないのであれば、ハイパーパラメータを調整する前に、データがランダムノイズでないことを確認したほうがいいかもしれない。
The author’s weren’t that specific, but I figured that was a good test to mention.
著者はそれほど具体的ではなかったが、これは良いテストだと思った。

Best Practice #22: Make sure your data isn’t all noise and no signal by making sure your model is at least capable of overfitting.
ベストプラクティス#22： モデルが少なくともオーバーフィットできることを確認することで、データがノイズばかりでシグナルがないことを確認する。

Reproducibility
再現性

Reproducibility.
再現性。
I’m sure many of you on the research team have had a lot of encounters with this one.
研究チームの皆さんの多くが、この件に関して多くの出会いを経験していることだろう。
You’ve probably seen code without seed numbers, notebooks written out of order, repositories without package versions.
シード番号のないコード、順番通りに書かれていないノートブック、パッケージ・バージョンのないリポジトリなどを見たことがあるだろう。
Since the Tech Debt Paper was written a few have tried making reproducibility checklists.
Tech Debt Paperが書かれて以来、何人かが再現性のチェックリストを作ろうとしている。
Here’s a pretty good one that was featured on hacker news about 4 months ago.
4ヶ月ほど前にハッカー・ニュースで紹介された、なかなか良いものがある。

Best Practice #23: Use reproducibility checklists when releasing research code.
ベストプラクティス#23： 研究コードを公開する際には、再現性チェックリストを使用する。

Process Management
プロセス管理

Most of the types of technical debt discussed so far have referred to single machine learning models, but process management debt is what happens when you’re running tons of models at the same time, and you don’t have any plans for stopping all of them from waiting around for the one laggard to finish.
これまで述べてきた技術的負債のほとんどは、単一の機械学習モデルについて言及してきた。しかし、プロセス管理負債とは、大量のモデルを同時に実行しているときに起こるものであり、1つの遅れているモデルの終了を待つために、すべてのモデルを停止させる計画を持っていない。
It’s important not to ignore the system-level smells, also, this is where checking the runtimes of your models becomes extremely important.
システムレベルの匂いを無視しないことも重要で、モデルのランタイムをチェックすることが非常に重要になる。
Machine learning engineering is at least improving at thinking about high-level system design since the Tech Debt Paper’s writing.
機械学習工学は、少なくともテック・デット・ペーパーの執筆以来、高レベルのシステム設計を考えることができるようになってきている。

Best Practice #24: Make a habit of checking and comparing runtimes for machine learning models.
ベストプラクティス#24： 機械学習モデルのランタイムをチェックし、比較する習慣をつける。

Cultural Debt
文化的負債

Cultural debt is the really tricky type of debt.
文化的債務は、本当に厄介なタイプの債務である。
The authors point out that sometimes there’s a divide between research and engineering, and that it’s easier to encourage debt-correcting behavior in heterogeneous teams.
著者らは、時として研究とエンジニアリングの間に溝があること、異質なチームでは負債を修正する行動を奨励しやすいことを指摘している。

Personally, I’m not exactly a fan of that last part.
個人的には、最後の部分はあまり好きではない。
I’ve witnessed many teams that have individuals that end up reporting to both the engineering directors and the research director.
私は、エンジニアリング・ディレクターとリサーチ・ディレクターの両方に報告することになる個人がいるチームを数多く目撃してきた。
Making a subset of the engineers report to two different branches without the authority to make needed changes is not a solution for technical debt.
必要な変更を行う権限のないエンジニアの一部を2つの異なる支社に報告させることは、技術的負債の解決策にはならない。
It’s a solution insofar as a small subset of engineers take the brunt of the technical debt.
技術的負債の大半を一部のエンジニアが負うという点では、これは解決策だ。
The end result is that such engineers usually end up with No Authority Gauntlet Syndrome (NAGS), burn out, and are fired by whichever manager had the least of their objectives fulfilled by the engineer all while the most sympathetic managers are out at Burning Man.
その結果、そのようなエンジニアは通常、権威なきガントレット症候群（NAGS）に陥り、燃え尽き、最も同情的なマネジャーがバーニングマンに出かけている間に、そのエンジニアによって最も目的を果たせなかったマネジャーに解雇されることになる。
If heterogeneity helps, then it needs to be across the entire team.
もし異質性が役に立つのであれば、それはチーム全体にわたっている必要がある。

Plus, I think the authors make some of the same mistakes many do when talking about team or company culture.
加えて、著者はチームや企業文化について語るとき、多くの人が犯すのと同じ間違いを犯していると思う。
Specifically, confusing culture with values.
具体的には、文化と価値観を混同していることだ。
It’s really easy to list a few aspirational rules for a company or team and call them a culture.
企業やチームのためにいくつかの理想的なルールを列挙し、それを文化と呼ぶのは実に簡単だ。
You don’t need an MBA to do that, but these are more values than actual culture.
そのためにMBAは必要ないが、これは実際の文化というより価値観だ。
Culture is what people end up doing when they’re in situations that demand they choose between two otherwise weighted values.
文化とは、2つの価値観のどちらかを選ばなければならない状況に置かれたとき、人々が最終的にとる行動である。
This was what got Uber in so much trouble.
これがウーバーを大問題に巻き込んだ。
Both competitiveness and honesty were part of their corporate values, but in the end, their culture demanded they emphasized competitiveness over everything else, even if that meant HR violating laws to keep absolute creeps at the company.
競争力と誠実さの両方が企業価値の一部であったが、結局のところ、彼らの企業文化は、たとえ人事が絶対的な不気味な人物を会社に留めておくために法律に違反することになっても、他のすべてよりも競争力を重視することを求めていた。

The issue with tech debt is that it comes up in a similar situation.
技術借金の問題は、同じような状況で出てくるということだ。
Yes, it’s easy to talk about how much you want maintainable code.
そう、保守性の高いコードを求めるのは簡単だ。
But, if everyone’s racing for a deadline, and writing documentation keeps getting shifted down in priority on the JIRA board, that debt is going to pile up despite your best efforts.
しかし、全員が締め切りに追われ、JIRAボード上でドキュメント作成の優先順位がどんどん下がっていくようでは、最善を尽くしても負債が積み重なっていくことになる。

Best Practice #25: Set aside regular, non-negotiable time for dealing with technical debt (whatever form it might take).
ベストプラクティス#25： 技術的負債（それがどのような形であれ）に対処するための、定期的で譲れない時間を確保する。

## Part 9: A technical debt litmus test パート9 技術的負債のリトマス試験紙

It’s important to remember that the ‘debt’ part is just a metaphor.
借金』という部分は単なる比喩であることを忘れてはならない。
As much as the authors try to make this seem like something that has more rigor, that’s all it is.
著者がこれをより厳密なもののように見せかけようとしているが、それだけだ。
Unlike most debts, machine learning technical debt is something that’s hard to measure.
他の負債とは異なり、機械学習の技術的負債は測定が難しいものだ。
How fast your team is moving at any given time is usually a poor indicator of how much you have (despite what many fresh-out-of-college product managers seem to insist).
ある時点でチームがどれくらいのスピードで動いているかは、（多くの大学出たてのプロダクトマネジャーが主張しているようだが）通常、自分がどれだけのものを持っているかの指標にはならない。
Rather than a metric, the authors suggest 5 questions to ask yourself (paraphrased for clarity here):
指標というよりも、著者は自問すべき5つの質問を提案している（ここではわかりやすくするために言い換えた）：

How long would it take to get an algorithm from an arbitrary NeurIPS paper running on your biggest data source?
任意のNeurIPS論文のアルゴリズムを、あなたの最大のデータソース上で実行させるには、どれくらいの時間がかかるだろうか？

Which data dependencies touch the most (or fewest) parts of your code?
コードのどの部分に、どのデータ依存性が最も多く（あるいは最も少なく）触れているか？

How much can you predict the outcome of changing one part of your system?
システムの一部分を変更した場合の結果をどれだけ予測できるか？

Is your ML model improvement system zero-sum or positive sum?
MLモデルの改善システムはゼロサムか、それともプラスサムか？

Do you even have documentation? Is there a lot of hand-holding through the ramping up process for new-people?
文書はあるのか？新人の立ち上げ過程では、手取り足取り教えてくれますか？

Of course, since 2015, other articles and papers have tried coming up with more precise scoring mechanisms (like scoring rubrics).
もちろん、2015年以降、他の論文や記事でも（採点基準など）より正確な採点メカニズムが試みられている。
Some of these have the benefit of being able to create an at-a-glance scoring mechanisms that even if imprecise will help you track technical debt over time.
これらの中には、たとえ不正確であったとしても、技術的負債を長期にわたって追跡するのに役立つ、一目でわかるスコアリングメカニズムを作成できるという利点があるものもある。
Also, there’s been a ton of advancements in the Interpretable ML tools that were extolled as a solution to some types of technical debt.
また、ある種の技術的負債を解決するソリューションとして称賛されたInterpretable MLツールにも大きな進歩があった。
With that in mind, I’m going to recommend “Interpretable Machine Learning” by Christoph Molnar (available online here) again.
それを念頭に置いて、クリストフ・モルナー著『解釈可能な機械学習』（オンライン版はこちら）を再度推薦しておこうと思う。

## The 25 Best Practices in one place 25のベストプラクティスを一挙公開

Here are all the Best Practices I mentioned throughout in one spot.
ここでは、私がこれまで述べてきたベストプラクティスを一箇所にまとめて紹介する。
There are likely many more than this, but tools for fixing technical debt follow the Pareto Principle: 20% of the technical debt remedies can fix 80% of your problems.
これ以外にもたくさんあるだろうが、技術的負債を解決するためのツールはパレートの原則に従っている： 技術的負債の20％を改善すれば、問題の80％を解決できる。

Use interpretability tools like SHAP values
SHAP値のような解釈可能性ツールを使う

Use explainable model types if possible
可能であれば、説明可能なモデルタイプを使用する

Always re-train downstream models
常に下流モデルを再トレーニングする

Set up access keys, directory permissions, and service-level-agreements.
アクセスキー、ディレクトリパーミッション、サービスレベルアグリーメントを設定する。

Use a data versioning tool.
データのバージョン管理ツールを使用する。

Drop unused files, extraneous correlated features, and maybe use a causal inference toolkit.
未使用のファイルや余計な相関特徴を削除し、因果推論ツールキットを使用する。

Use any of the countless DevOps tools that track data dependencies.
データの依存関係を追跡する無数のDevOpsツールのいずれかを使用する。

Check independence assumptions behind models (and work closely with security engineers.
モデルの背後にある独立性の仮定をチェックする（セキュリティ・エンジニアと緊密に連携する）。

Use regular code-reviews (and/or use automatic code-sniffing tools).
定期的にコードレビューを行う（あるいは自動コードスニッフィングツールを使う）。

Repackage general-purpose dependencies into specific APIs.
汎用の依存関係を特定のAPIにリパッケージする。

Get rid of Pipeline jungles with top-down redesign/reimplementation.
トップダウンの再設計／再実装でパイプラインのジャングルをなくす。

Set regular checks and criteria for removing code, or put the code in a directory or on a disk far-removed from the business-critical stuff.
コードを削除するための定期的なチェックと基準を設定するか、ビジネスクリティカルなものから遠く離れたディレクトリやディスクにコードを置く。

Stay up-to-date on abstractions that are becoming more solidified with time
時代とともに固まりつつある抽象化について、常に最新の情報を入手する。

Use packages like Typing and Decimal, and don’t use ‘float32’ for all data objects
TypingやDecimalのようなパッケージを使い、すべてのデータ・オブジェクトに'float32'を使わない。

Don’t leave all works-in-progress in the same directory.
すべての仕掛品を同じディレクトリに置いてはいけない。
Clean it up or toss it out.
掃除するか捨てるかだ。

Make sure endpoints are accounted, and use frameworks that have similar abstractions between languages
エンドポイントが説明されていることを確認し、言語間で同様の抽象化を持つフレームワークを使用する。

Make it so you can set your file paths, hyperparameters, layer type and layer order, and other settings from one location
ファイルパス、ハイパーパラメータ、レイヤーの種類、レイヤーの順序、その他の設定を1カ所で行えるようにします。

Monitor the models’ real-world performance and decision boundaries constantly
モデルの実世界でのパフォーマンスと意思決定の境界を常に監視する。

Make sure distribution of predicted labels is similar to distribution of observed labels
予測されたラベルの分布が、観測されたラベルの分布と類似していることを確認する。

Put limits on real-world decisions that can be made by machine learning systems
機械学習システムによる現実世界の判断に制限を設ける

Check assumptions behind input data
入力データの前提条件をチェックする

Make sure your data isn’t all noise and no signal by making sure your model is at least capable of overfitting
モデルが少なくともオーバーフィットが可能であることを確認することで、データがノイズばかりでシグナルがないことを確認する。

Use reproducibility checklists when releasing research code
研究コードを公開する際には、再現性チェックリストを使用する。

Make a habit of checking and comparing runtimes for machine learning models
機械学習モデルのランタイムをチェックし、比較する習慣をつける。

Set aside regular, non-negotiable time for dealing with technical debt (whatever form it might take)
技術的負債（それがどのような形であれ）に対処するための、定期的で譲れない時間を確保する。