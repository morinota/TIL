refs: https://arxiv.org/pdf/2209.09000.pdf

Reweighting Clicks with Dwell Time in Recommendation   推奨における滞在時間によるクリックの再重み付け

Ruobing Xie[∗]  
WeChat, Tencent Beijing, China ruobingxie@tencent.com  
Lin Ma[∗]  
WeChat, Tencent Beijing, China carrotma@tencent.com  
Shaoliang Zhang  
WeChat, Tencent Beijing, China modriczhang@tencent.com  
Feng Xia  
WeChat, Tencent Beijing, China xiafengxia@tencent.com  
Leyu Lin  
WeChat, Tencent Beijing, China goshawklin@tencent.com  

- 全体像メモ:
  - 本論文の基礎となる主張:
    - 「すべての click を同じ positive label として扱うのはよくないよね」って話。
    - なぜなら、clickには以下のようなノイズがあるから:
      - タイトル釣りでclickされた。
      - タイトルと中身がズレてた(期待と違う)。
      - とりあえず開いたけどすぐ閉じた。
      - いずれもユーザ満足度は低いのに「1 click」として同じ扱いにしてしまう。
    - よって、click後のユーザ満足度をより良く表す定量シグナルとしてdwell time (滞在時間)を用いて、clickをdwell timeで"再重み付け"する。
  - 本論文の２つの新規性:
    - その1: valid read を定義すること
      - 「これは質の高いclickだよね」っていうclickを選別してる。
    - その2: clickの再重み付けとしてdwell timeをそのままは使わない! 正規化関数を設計!
      - 生の dwell time をそのまま報酬とか重みに設定すると、長文記事・長尺動画・元々読むのが遅いユーザ・ヘビーユーザを重視して過剰評価してしまう可能性あり。
      - **dwell time を正規化した関数に通して、短すぎる滞在はしっかり罰しつつ、長すぎる滞在は飽和させる**
  - 本論文が解こうとしてる問題:
    - 論文内ではdwell time modelingの問いを2つに分けている.
    - 問い1: 良い推薦システムって何??
      - 著者たちの答えは「**ユーザを長く拘束することではなく、有益な情報を効率よく読ませること**」
      - ただ単にdwell timeを伸ばすだけだと、以下のような問題が発生する
        - 長い記事ばっかり出す
        - ユーザを沼らせる
        - "効率よく満足した"ことを評価できない
    - 問い2: dwell timeで満足度をどう定量化する??
      - ex. 1秒→15秒の改善と601秒→615秒の改善では、同じ+14秒でも意味が全然異なる。
      - 前者は「誤クリックじゃなくてちゃんと読み始めた」に近い。
      - **なので、dwell time は単調増加ならなんでもいいわけじゃなく、“初期で効いて、後半は飽和する形”がよい** と考えられる!
        - ->あ、だから 報酬関数や sample weightingの時はlogに通すのか...!!:thinking:
  - 本論文の新規性1: valid readの設計
    - 以下の**3種類のルール**でvalid readを作っている。
    - ルール1: 共通閾値を超えたclickはvalid readとみなす!
      - まず全体のdwell time分布を見ると、log(dwell time)は大体正規分布っぽいとみなせる。
      - その上で、 $\mu$ を log(dwell time)の平均、 $\sigma$ を標準偏差として、下限閾値 $x_1 = \exp(\mu - \sigma)$ をvalid readの基準とする。
      - **ちなみにWeChatの実データではこれが約15秒**。
        - i.e. 15秒以上読まれたclickは、まずは"ちゃんと読まれたclick"とみなす!
    - ルール2: ライトユーザのclickはvalid readとみなす!
      - でも、ルール1だけで全員に同じ閾値を適用するだけだと、もともとサクサク読む人、そもそもクリック数が少ない人などの情報が落ちやすい。
      - そこでライトユーザ救済として、直近1週間でクリック数が7未満のlight userは、全てのclickをsupervised signalとしてvalid read扱いにする。
    - ルール3: 各アイテムについて相対的に長いdwell timeのclickはvalid readとみなす!
      - **更に、短いニュースや短尺コンテンツはそもそもdwell timeが短くなりがち。**
      - アイテム間の公平性を保つために、そのアイテムの過去clickの中で相対的に十分長いdwell timeならvalid readとみなす。
        - 本論文内の具体的なhowとしては、各アイテムの過去clickのdwell time分布に対して、上側90%値を超えるclickは全てvalid readとみなしていた。
    - (ルール4: **ノイズ除去として、dwell timeが5秒未満のクリックは全部除外**してる!)
    - valid readの意味:
      - 要するにvalid readは、**長く読まれたclickをそのまま意味するのではなく、ユーザ特性とアイテム特性を多少考慮した高品質clickラベル**、ってイメージ...!
      - (i.e. clickをそのまま全てpositiveにせずに精錬ステップをかましているイメージ...!!)
  - 本論文の新規性2: dwell time正規化関数を用いたclickの再重みづけ!
    - 本論文では、valid readを選定した後で、その中でも更にdwell timeに応じて重み付けしてる。
    - ただし、**生のdwell timeやlog(dwell time)をそのまま使わず、sigmoid関数で変換**してる。
      - 狙いは2つ:
        - 1: valid readの共通閾値近辺で勾配を大きくしたいから!
          - valid / invalid の境界、つまり 15秒付近で重みが敏感に変わるようにしたい。これで ちょい読み/ちゃんと読んだ の差を学習しやすくする。
        - 2: 長すぎるdwell timeでは飽和させる! 過剰評価させない!
          - 逆に長すぎる滞在は重みをほぼ増やしたくない。
          - これにより、 **長尺記事/長尺動画/ヘビーユーザがlossを支配**するのを防ぐ!
      - なぜsigmoid関数を採用した?
        - 性質:
          - 短時間帯では変化が大きい
          - ある程度から飽和する
          - 単調増加
          - 実装も簡単
        - 雑にいうと“**15秒を超えるかどうかはすごく重要。でも200秒と250秒の差はそこまで重要じゃない**”を関数で表現しやすいから。
        - log(dwell time)との違いは?? 何がダメだからsigmoidにしてる?? :thinking:
          - log関数もsigmoid関数の採用理由の一部は満たしてるはず...!
            - ex. log関数も単調増加だし、実装も簡単。短時間帯ほど変化が大きい、も表現できる。
          - 一方で、以下が差分:
            - **log関数は飽和しない。**長すぎるdwell timeに対しても重みが増え続けてしまう。そのまま返す恒等関数よりはだいぶマシ。しかしまだ、長いコンテンツ、ヘビーユーザがまだ過剰評価される可能性がある。
            - **「どこが重要か」「どこで一番区別したいか」を指定・表現できない。**logは単に滑らかに増加するだけなので、valid readの境界(ex. 15秒付近)でここが一番大事! みたいな情報を表現できない!!
          - 要するに、**valid read の境界を一番重視して学習させたい!** なのでlog関数ではなくsigmoid関数を採用してる...!:thinking:
            - logは数学的にいい感じではあるが、sigmoidの方がプロダクト的に意味を持った変換ができる!
              - ex. 閾値付近 -> 超重要!, それ以下 ->　ノイズ, それ以上 -> 飽和!
              - 15秒付近を重要視させたい場合の関数の例 = sigmoid((x - 15) / tau) みたいな感じで簡単に表現できる!
                - ここでtauは、どれくらい急に重みを変化させるかを調整するハイパーパラメータ。小さいほど急になる。大きいほど緩やかな変化になる。


$$
T_{N} = \frac{A}{1 + \exp(-\frac{T - offset}{tau})} - B
\\
= A \cdot sigmoid(\frac{T - offset}{tau}) - B
\tag{1}
$$

- 実際の正規化関数の式は上記。
  - 各ハイパラの意味は以下。
    - その1: offset(どこを重視するか)
      - 例えば15秒を重視したいなら、offset=15にする。
    - その2: tau(勾配の急さ)
      - 例えば、offset付近をすごく重視したいなら、tauを小さくする。
      - 逆に、offset付近もある程度重視しつつ、もう少し広い範囲で重みを変化させたいなら、tauを大きくする。
    - その3: A, B(スケーリングとシフト)
      - これで出力レンジを調整する。
        - なぜ必要? -> 他のbinary報酬と組み合わせて合成報酬関数を作る際に、スケールを揃えるためなど。
      - 例えば、出力を0~1にしたいなら、A=1, B=0にする。
      - (ただまあA, Bは本質ではない! sigmoidの方が本質!)
- 学習の仕方:
  - 論文のメインは正規化関数(dwell time)によるsample reweightingだけど、おまけっぽいが**NNの出力側をmulti-head(2つ)にしてマルチタスク学習をしてるっぽい**。
    - head1: valid read を予測するhead
    - head2: dwell timeでreweightingした上で valid read を予測するhead
    - 学習時はこの2つのlossを足して学習し、推論時は両ヘッドのscoreの和でランキングしてるとのこと。
  - multi-headにしてるモチベーション:
    - hoge
- 実験結果:
  - オフライン実験:
    - アブレーションスタディとして、以下の4つのvariantを比較:
      - single CTR
      - CTR + logDT
      - VR + logDT
      - VR + NDT (本論文の提案手法)
    - 一番AUCがよかったのがVR + NDTで、次いでVR + logDT。CTR単体は一番悪かった。
  - オンライン実験:
    - (ACN = average click number, DT = dwell time, AIN = average impression number)
    - +valid read
      - CTR +1.9%, ACN +2.478%, DT -1.7%, AIN +0.6%
    - +valid read + NDT reweighting
      - CTR +2.6%, ACN +4.1%, DT -3.5%, AIN +1.5%
    - その1: なぜ CTR と ACN が上がるの？という解釈
      - >using high-quality valid reads as training objectives can even improve CTR (高品質なvalid readをトレーニングの目的として使用することで、CTRさえも改善できる) 
      - 解釈:
        - before: 
          - clickベースの目的関数 -> 釣りタイトル強い -> クリックはするけどすぐに離脱。
        - after:
          - valid readベースの目的関数 -> 「ちゃんと読まれる記事」を学習
          - 無駄クリックが減る -> "あたり記事"が増える -> ユーザが次も読む。よってCTRもACNも上がってる。
    - その2: なぜDTが下がるの？という解釈
      - >inevitably sacrificing the performance of dwell time (滞在時間のパフォーマンスを犠牲にすることは避けられない)
      - **このモデルは長く読ませることを目的にしていない。**
      - 長すぎる記事（長尺コンテンツ）を過大評価しない。sigmoidで飽和させてるので。
      - 結果として、ダラダラ長く読む行動が減る。"適切な長さで満足"が増える。
    - その3: DT migraition (DT分布の変化)が観測された。
      - 分析の軸:
        - x軸 -> dwell timeの分位(P10~P90)
        - y軸 -> ユーザのアクティブ度(クリック数で定義)
        - z軸 -> dwell timeの改善率
      - 観察1: short dwell time behaviors (P10/P20) have improvements(短時間だった行動が長くなっている!)
        - 解釈: 誤クリックが減ってる!
          - before: クリック -> 2秒で閉じる
          - after : クリック -> 10秒読む
        - つまり valid readが増えてる!
      - 観察2: >too-long readings decrease (長すぎる読みが減っている!)
        - duration biasが減ってる?
      - 観察3: light users benefits(ライトユーザが特に改善!)
        - もともとあまり読まないユーザのクリックもvalid readとして扱うルールが効いてる!
        - before: ライトユーザのクリック -> 5秒で閉じる
        - after : ライトユーザのクリック -> 20秒読む
      - 結論としてvalid readが増えた!
        - **本論文で実現したこと「長く読ませる」から「ちゃんと読ませる」への転換!**

## ABSTRACT

The click behavior is the most widely-used user positive feedback in recommendation.
クリック行動は、推奨において最も広く使用されるユーザーのポジティブフィードバックです。
However, simply considering each click equally in training may suffer from clickbaits and title-content mismatching, and thus fail to precisely capture users’ real satisfaction on items.
しかし、**トレーニングで各クリックを平等に考慮するだけでは、クリックベイトやタイトルとコンテンツの不一致に悩まされ、ユーザーのアイテムに対する本当の満足度を正確に捉えることができません。**
Dwell time could be viewed as a high-quality quantitative indicator of user preferences on each click, while existing recommendation models do not fully explore the modeling of dwell time.
滞在時間は、各クリックに対するユーザーの好みの高品質な定量的指標と見なすことができる一方で、既存の推奨モデルは滞在時間のモデリングを十分に探求していません。
In this work, we focus on reweighting clicks with dwell time in recommendation.
**本研究では、推奨における滞在時間を用いたクリックの再重み付けに焦点**を当てます。
Precisely, we first define a new behavior named valid read, which helps to select high-quality click instances for different users and items via dwell time.
具体的には、まず「**valid read」という新しい行動**を定義し、これにより滞在時間を通じて異なるユーザとアイテムの高品質なクリックインスタンスを選択するのに役立ちます。
Next, we propose a normalized dwell time function to reweight click signals in training for recommendation.
次に、推奨のためのトレーニングにおいて**クリック信号を再重み付けするための正規化された滞在時間関数**を提案します。
The Click reweighting model achieves significant improvements on both offline and online evaluations in real-world systems.
クリック再重み付けモデルは、実世界のシステムにおけるオフラインおよびオンライン評価の両方で大幅な改善を達成します。

**KEYWORDS**: recommendation, valid read, dwell time, click reweighting

<!-- ここまで読んだ! -->

## 1 INTRODUCTION

Real-world personalized recommendation attempts to provide appropriate items based on user preferences.
実世界のパーソナライズされた推奨は、ユーザーの好みに基づいて適切なアイテムを提供しようとします。
User feedback on items is natural and essential information to discover user interests.
アイテムに対するユーザーフィードバックは、ユーザーの興味を発見するための自然で重要な情報です。
Click, which is a high-quality and widely-existed implicit feedback, is the dominating user behavior used in recommendation. Click-through rate (CTR) prediction is also the central objective [4, 19, 26].
クリックは、高品質で広く存在する暗黙のフィードバックであり、推奨に使用される支配的なユーザー行動です。クリック率（CTR）予測も中心的な目的です [4, 19, 26]。

Despite the ubiquitous usage of clicks, simply relying on clicks as the only supervised training signals may not accurately and comprehensively capture users’ real satisfaction, since the implicit click feedback often struggles with clickbaits or title-content mismatching in practice [17].
クリックの普遍的な使用にもかかわらず、クリックを唯一の監視されたトレーニング信号として単純に依存することは、ユーザーの本当の満足度を正確かつ包括的に捉えることができないかもしれません。なぜなら、暗黙のクリックフィードバックは、実際にはクリックベイトやタイトルとコンテンツの不一致に悩まされることが多いからです [17]。
Moreover, most existing recommendation models intuitively regard all clicks equally as training labels [4, 8, 14], failing to dig out the different intensities of user preferences in each click.
さらに、ほとんどの既存の推奨モデルは、すべてのクリックを直感的にトレーニングラベルとして平等に扱い [4, 8, 14]、各クリックにおけるユーザーの好みの異なる強度を掘り下げることに失敗しています。
To address these issues, an intuitive idea is to enhance the binary clicks with more quantified weights.
これらの問題に対処するための直感的なアイデアは、バイナリクリックにより定量化された重みを追加することです。
Dwell time (DT), which indicates the duration of a user on a clicked item (after clicking and before exiting), is easy-to-collect in real-world systems and perfectly suitable to quantify clicks and discover users’ preferences [7, 24].
滞在時間（DT）は、クリックされたアイテムに対するユーザーの滞在時間を示すものであり（クリック後、退出前）、実世界のシステムで簡単に収集でき、クリックを定量化し、ユーザーの好みを発見するのに最適です [7, 24]。
More dwell time indicates that users are more willing to pay time costs on items, reflecting higher user interests beyond clicks.
より多くの滞在時間は、ユーザーがアイテムに対して時間コストを支払う意欲が高いことを示し、クリックを超えたユーザーの関心の高さを反映しています。
Dwell time is also a widely-used online metric to measure users’ real satisfaction in practical systems [21, 23].
滞在時間は、実際のシステムにおけるユーザーの本当の満足度を測定するための広く使用されているオンライン指標でもあります [21, 23]。

> **Figure 1: Dwell time as the natural weights of clicks.**
> 図1: クリックの自然な重みとしての滞在時間。
> - Click: low-cost, binary, may have noises caused by clickbaits (クリック: 低コスト、バイナリ、クリックベイトによるノイズの可能性)
> - Dwell time: high-cost, quantified, could better reflect user real satisfaction (滞在時間: 高コスト、定量化、ユーザーの本当の満足度をよりよく反映)

There are a few works that jointly consider clicks and dwell time as objectives or features in practical recommendation [2, 18, 22, 27].
クリックと滞在時間を実際の推奨における目的や特徴として共同で考慮した研究は少数あります [2, 18, 22, 27]。
However, most of them simply use the original/log dwell time as another training label besides clicks, ignoring further explorations on quantifying relations between dwell time and user satisfaction.
しかし、ほとんどはクリックの他に元の/ログ滞在時間を別のトレーニングラベルとして単純に使用し、滞在時間とユーザー満足度の関係を定量化するさらなる探求を無視しています。

Two questions need to be answered in dwell time modeling:

**(1) What a good recommender system should be?** We believe that a good recommender system should help users to get useful information more efficiently (rather than pursuing more clicks or dwell time).
**(1) 良いレコメンダーシステムとは何か？** 良いレコメンダーシステムは、ユーザーがより効率的に有用な情報を得るのを助けるべきであると考えています（より多くのクリックや滞在時間を追求するのではなく）。
The central goal is to provide more valid readings for users.
中心的な目標は、ユーザーにより多くの有効な読み取りを提供することです。
Dwell time is intuitively used to define valid reading, while different users and items have different sensitivities on dwell time.
滞在時間は直感的に有効な読み取りを定義するために使用されますが、異なるユーザーとアイテムは滞在時間に対して異なる感受性を持っています。
For example, some users tend to spend less time reading (i.e., light users).
例えば、あるユーザーは読むのにあまり時間をかけない傾向があります（すなわち、ライトユーザー）。
An item’s dwell time is also related to its type and total length (e.g., short news V.S. long videos).
アイテムの滞在時間は、そのタイプや総長（例: 短いニュース対長い動画）にも関連しています。
Valid readings better reflect users’ real satisfaction compared to CTR [2, 25, 27].
有効な読み取りはCTRと比較してユーザーの本当の満足度をより反映します [2, 25, 27]。
How different users and items should be fairly considered in training.
異なるユーザーとアイテムがトレーニングでどのように公平に考慮されるべきか。

**(2) How to accurately quantify user satisfaction with dwell time?** Longer dwell time does imply higher satisfaction, while directly optimizing raw dwell time will inevitably guide the model to over-emphasize items with long total durations, making heavy users and long items dominate the model training [16, 22].
**(2) 滞在時間でユーザーの満足度を正確に定量化するには？** より長い滞在時間はより高い満足度を意味しますが、生の滞在時間を直接最適化すると、モデルが長い総滞在時間を持つアイテムを過度に強調し、重いユーザーと長いアイテムがモデルのトレーニングを支配します [16, 22]。
The same dwell time improvement does not always indicate the same user satisfaction improvement.
同じ滞在時間の改善が必ずしも同じユーザー満足度の改善を示すわけではありません。
For example, the positive impact of a dwell time improvement from 1s to 15s is much larger than that from 601s to 615s.
例えば、滞在時間の改善が1秒から15秒に向かうことのポジティブな影響は、601秒から615秒に向かうことの影響よりもはるかに大きいです。
Intuitively, we hope users to have fewer invalid clicks with too-short dwell time, while we should also avoid over-emphasizing clicks with too-long dwell time, since the information gain will get lower and the seesaw effect may harm the learning of long-tail light users and short items.
直感的には、ユーザーがあまりにも短い滞在時間で無効なクリックを減らすことを望んでいますが、あまりにも長い滞在時間のクリックを過度に強調することも避けるべきです。なぜなら、情報の獲得が低下し、シーソー効果がロングテールのライトユーザーや短いアイテムの学習を損なう可能性があるからです。
How to design a dwell time function to properly reweight clicks remains to be explored.
クリックを適切に再重み付けするための滞在時間関数をどのように設計するかは、今後の探求課題です。

In this work, we aim to reweight clicks with dwell time to build a good recommender system, where users should have more high-quality and efficient readings.
本研究では、滞在時間を用いてクリックを再重み付けし、ユーザーがより高品質で効率的な読み取りを持つべき良いレコメンダーシステムを構築することを目指します。
Precisely, we propose a simple, effective, and model-agnostic Click reweighting framework to improve the training objectives.
具体的には、トレーニングの目的を改善するためのシンプルで効果的、かつモデルに依存しないクリック再重み付けフレームワークを提案します。

The contributions of this work are as follows:
本研究の貢献は以下のとおりです：

- We highlight the significance of valid read, rethink the quantification of user satisfaction with dwell time modeling, and propose our Click reweighting framework. To the best of our knowledge, we are the first to adopt the valid read behavior with dwell time based click reweighting in real-world recommender systems.
  - 私たちは有効な読み取りの重要性を強調し、滞在時間モデリングによるユーザー満足度の定量化を再考し、クリック再重み付けフレームワークを提案します。私たちの知る限り、実世界のレコメンダーシステムにおいて滞在時間ベースのクリック再重み付けと有効な読み取り行動を採用した最初の研究です。
- We define the valid read to collect high-quality clicks considering
  the demands of different users and items. We also design a simple yet effective normalized dwell time function to model the intrinsic relationships between dwell time and user satisfaction.
  - 異なるユーザーとアイテムの要求を考慮して高品質のクリックを収集するために有効な読み取りを定義します。また、滞在時間とユーザー満足度の内在的な関係をモデル化するためのシンプルかつ効果的な正規化滞在時間関数を設計します。
- We evaluate our Click reweighting framework on both offline and online evaluations in a real-world recommender system, achieving significant improvements on various metrics. Currently, the proposed Click reweighting has been deployed on WeChat Top Stories for more than 4 months, affecting millions of users.
  - 実世界のレコメンダーシステムでオフラインとオンラインの両方でクリック再重み付けフレームワークを評価し、さまざまな指標で重要な改善を達成しました。現在、提案されたクリック再重み付けはWeChat Top Storiesに4ヶ月以上展開され、数百万のユーザーに影響を与えています。

<!-- ここまで読んだ! -->

## 2 MODEL DESIGNS AND ANALYSES

### 2.1 Discussions on Dwell Time Modeling

Researchers have devoted themselves to exploring the core problem of recommendation: what kind of recommendation do users really need.
研究者たちは、推薦のコア問題の探求に専念してきました：ユーザーは本当にどのような推薦を必要としているのか。
Recent efforts have shown the advantages of valid readings in reflecting users’ real satisfaction compared to CTR [2, 25, 27].
最近の取り組みは、CTRと比較してユーザーの本当の満足度を反映する有効な読み取りの利点を示しています [2, 25, 27]。

For a deeper understanding of dwell time, we draw the trends of click numbers with different log dwell time. From Fig. 2 (left) we find that:
滞在時間のより深い理解のために、異なるログ滞在時間に基づくクリック数のトレンドを描きます。図2（左）から次のことがわかります：

(1) In general, we could roughly assume that the log dwell time has an approximate Gaussian distribution, i.e., $\ln T = \mu + \sigma \epsilon$, where $T$ is a random dwell time and $\epsilon \sim \mathcal{N}(0, 1)$.
（1）一般的に、ログ滞在時間が近似的なガウス分布を持つと大まかに仮定できます。すなわち $\ln T = \mu + \sigma \epsilon$ であり、$T$ はランダムな滞在時間、$\epsilon \sim \mathcal{N}(0, 1)$ です。

We regard $[\mu - \sigma, \mu + \sigma]$ as the mainstream dwell time range. Nearly 19% click behaviors have shorter than 15s dwell time, and nearly 15% click behaviors have longer than 200s dwell time.
$[\mu - \sigma, \mu + \sigma]$ を主流の滞在時間範囲と見なします。19％のクリック行動は15秒未満の滞在時間を持ち、ほぼ15％のクリック行動は200秒以上の滞在時間を持っています。

We discover two characteristics that a good normalized DT function should have:
良い正規化DT関数が持つべき2つの特性を発見します：

(A2) Users need minimum dwell time to get information from items.
（A2）ユーザーはアイテムから情報を得るために最小限の滞在時間が必要です。

(A3) When dwell time is long enough, the information gain diminishes.
（A3）滞在時間が十分長い場合、情報利得は漸減します。

i.e., a good normalized DT function should guide users to have more valid reads without much negative impact caused by behaviors having too-long dwell time.
すなわち、良い正規化DT関数は、長すぎる滞在時間の行動による悪影響をあまり受けずに、より多くの有効な読み取りを持つようにユーザーを導くべきです。

> **Figure 2: The trend of log dwell time in our system (left) and the trend of our proposed normalized dwell time (right).**
> 図2：私たちのシステムにおけるログ滞在時間のトレンド（左）と提案する正規化された滞在時間のトレンド（右）。
> - 左図: log dwell time の分布は近似的にガウス分布。$\mu - \sigma$ 以下（≈15秒未満）が19%、$\mu + \sigma$ 以上（≈200秒以上）が15%。
> - 右図: $offset = \exp(\mu - \sigma)$ 付近で $T_N$ は最大の勾配を持ち、$\exp(\mu + \sigma)$ 以上では飽和する。

<!-- ここまで読んだ! -->

### 2.2 Valid Read Selection

First, we define a new behavior named **valid read** as a dwell time enhanced high-quality click behavior.
まず、「**valid read**」という新しい行動を、滞在時間を強化した高品質なクリック行動として定義します。
The valid read selects three types of good clicks as the training signals, considering different demands of (a) the common-sense dwell time threshold learned from the global DT distribution, (b) light users, and (c) short items.
有効な読み取りは、トレーニング信号として3種類の良いクリックを選択します。(a) グローバルDT分布から学習した常識的な滞在時間の閾値、(b) ライトユーザー、(c) 短いアイテムの異なる要求を考慮しています。
Valid reads are high-quality click behaviors that could better reflect users’ real preferences, which are naturally selected via dwell time in this work.
有効な読み取りは、ユーザーの本当の好みをよりよく反映できる高品質なクリック行動であり、本研究では滞在時間を通じて自然に選択されます。

It is straightforward to roughly set a shared dwell time threshold to collect valid reads. However, simply relying on the threshold to define valid reads will inevitably ignore the significant behavioral information of light users and short items. Hence, we define three types of valid reads:
共有の滞在時間しきい値を大まかに設定して有効な読み取りを収集するのは簡単です。しかし、しきい値に単純に依存することは、ライトユーザーと短いアイテムの重要な行動情報を無視することになります。したがって、3種類の有効な読み取りを定義します：

- **T1**: the dwell time is longer than $x_l$ seconds.
  - T1：滞在時間が $x_l$ 秒より長い。
- **T2**: the user has clicked less than 7 items in the recent week.
  - T2：ユーザーは直近1週間で7アイテム未満をクリックした（ライトユーザー）。
- **T3**: the dwell time is longer than 10% of this item’s historical dwell time distribution.
  - T3：滞在時間がこのアイテムの過去の滞在時間分布の上位10%より長い。

(1) The first type builds the fundamental rule of valid read according to a common-sense threshold $x_l$. We regard $x_l = \exp(\mu - \sigma)$ of $\ln T$ as the shared dwell time threshold of valid read, which is adaptive to different recommender systems. In our system, $\exp(\mu - \sigma)$ is nearly 15s. 19% click behaviors are filtered by T1.
（1）最初のタイプは、一般的なしきい値 $x_l$ に基づいて有効な読み取りの基本ルールを構築します。$x_l = \exp(\mu - \sigma)$ を有効な読み取りの共有滞在時間しきい値とし、異なるレコメンダーシステムに適応します。私たちのシステムでは $\exp(\mu - \sigma)$ はほぼ15秒です。19%のクリック行動がT1によってフィルタリングされます。

For simplicity, we directly adopt a shared DT threshold for all users and items in respect of the absolute value of time costs, while it is also convenient to set customized dwell time thresholds for different user or item groups.
簡単のために、時間コストの絶対値に関してすべてのユーザーとアイテムに対して共有のDTしきい値を直接採用しますが、異なるユーザーまたはアイテムグループのためにカスタマイズされたしきい値を設定することも便利です。

(2) The second type puts a patch on light users, considering all light users’ click behaviors as supervised signals in training, for their behaviors are rare. We want to avoid critical information loss of long-tail light users that prefer scanning rather than deep reading.
（2）2番目のタイプは、ライトユーザーにパッチを当てます。行動がまれであるため、すべてのライトユーザーのクリック行動をトレーニングの監視信号として考慮します。深く読むのではなくスキャンを好むロングテールのライトユーザーの重要な情報損失を避けたいと考えています。

(3) The third type considers the relative dwell time on a specific item, retrieving clicks that have a relatively qualified dwell time (top 90%) among all historical clicks on the same item. By this, our valid read shows respect to items with naturally short lengths and less dwell time (e.g., news or short videos).
（3）3番目のタイプは、特定のアイテムに対する相対的な滞在時間を考慮し、同じアイテムのすべての履歴クリックの中で比較的適格な滞在時間（上位90%）を持つクリックを取得します。これにより、自然に短い長さと少ない滞在時間を持つアイテム（例：ニュースや短い動画）に敬意を表します。

To avoid noises, we further wipe out all clicks having less than 5s dwell time to ensure the minimum availability of valid reads.
ノイズを避けるために、5秒未満の滞在時間を持つすべてのクリックを削除して、有効な読み取りの最小の可用性を確保します。

In our practical system, the T1, T2, T3 types account for 89.9%, 2.9%, 7.2% of the overall valid reads.
私たちの実際のシステムでは、T1、T2、T3タイプは全体の有効な読み取りの89.9%、2.9%、7.2%を占めています。

Only valid reads are used as supervised signals in training.
有効な読み取りのみがトレーニングの監視信号として使用されます。

<!-- ここまで読んだ! -->

### 2.3 Normalized Dwell Time Function

The valid read selection works as a pre-filter. However, we still face the challenge of precisely defining the goodness of different dwell time values in click reweighting.
有効な読み取りの選択は前フィルターとして機能します。しかし、クリック再重み付けにおける異なる滞在時間値の良さを正確に定義するという課題に直面しています。

It is intuitive that the same dwell time improvement has a larger contribution to the quality of a click when the current dwell time is shorter (e.g., [1s → 15s] is larger than [601s → 615s]). Too long dwell time may bring in fatigue that harms user experience [20].
同じ滞在時間の改善が、現在の滞在時間が短いときにクリックの質に対してより大きな貢献を持つことは直感的です（例：[1秒→15秒]は[601秒→615秒]より大きい）。長すぎる滞在時間は、ユーザー体験を損なう疲労をもたらす可能性があります [20]。

Hence, lots of works adopt MSE with log dwell time as training losses for dwell time prediction [2, 16, 27]. Different from conventional models, we define the valid reads as our high-quality supervised labels and hope to improve the numbers and proportion of valid reads in online systems.
したがって、多くの研究が滞在時間予測のためのトレーニング損失としてログ滞在時間を用いたMSEを採用しています [2, 16, 27]。従来のモデルとは異なり、有効な読み取りを高品質の監視ラベルとして定義し、オンラインシステムにおける有効な読み取りの数と割合を改善することを望みます。

Therefore, our dwell time function should possess the following two characteristics C1 and C2 with respect to the above assumptions A2 and A3 in Sec. 2.1:
したがって、滞在時間関数は、セクション2.1の仮定A2およびA3に関して、次の2つの特性C1およびC2を持つべきです：

- **C1**: the designed dwell time function curve should be steep with large gradients in the early stage (especially near the valid read threshold $\exp(\mu - \sigma)$), guiding models to efficiently distinguish valid reads from invalid clicks.
  - C1：設計された滞在時間関数の曲線は、初期段階（特に有効な読み取りしきい値 $\exp(\mu - \sigma)$ の近く）で大きな勾配を持ち急であるべきです。モデルが有効な読み取りを無効なクリックから効率的に区別できるように導きます。
- **C2**: the dwell time function curve should be flat when the dwell time is too long, avoiding too many rewards over long-duration items that harms light users and short items.
  - C2：滞在時間が長すぎるときに曲線は平坦であるべきです。長時間アイテムに対する過剰な報酬を避け、ライトユーザーや短いアイテムへの害を防ぎます。

Following these rules, we design our normalized dwell time $T_N$ based on the original dwell time $T$ with a sigmoid function as:
これらのルールに従って、元の滞在時間 $T$ に基づいてシグモイド関数を用いて正規化された滞在時間 $T_N$ を設計します：

$$
T_N = \frac{A}{1 + \exp\left(-\frac{T - offset}{\tau}\right)} - B
\tag{1}
$$

Fig. 2 (right) shows the trends of $T_N$. $T_N$ is monotonically increasing with designed rates compared to log dwell time, where $offset$ and $\tau$ are essential parameters to satisfy C1 and C2.
図2（右）は $T_N$ のトレンドを示しています。$T_N$ はログ滞在時間と比較して設計された速度で単調増加し、$offset$ と $\tau$ はC1およびC2を満たすための重要なパラメータです。

- $offset$ determines the dwell time point with the largest gradient. For C1, we set $offset = \exp(\mu - \sigma)$ to make the normalized dwell time have the largest gradient on the borderline of valid/invalid reads, which cooperates well with the valid read based supervised training.
  - $offset$ は最大の勾配を持つ滞在時間ポイントを決定します。C1のために $offset = \exp(\mu - \sigma)$ を設定し、有効/無効の境界で最大の勾配を持たせます。
- $\tau$ defines the sharpness of the dwell time curve. For C2, we define an upper threshold $x_h$ as $\exp(\mu + \sigma)$, assuming that the dwell time $T$ larger than $x_h$ has no contribution on $T_N$ (i.e., the $T_N$ improvement of $x_h \to T$ is smaller than the minimum precision, e.g., $1e-5$ in our system). $\tau$ is set to fit the above assumption of $x_h$.
  - $\tau$ は滞在時間曲線の鋭さを定義します。C2のために上限しきい値 $x_h = \exp(\mu + \sigma)$ を定義し、$T > x_h$ の場合 $T_N$ への寄与はないと仮定します。$\tau$ は $x_h$ の仮定に合わせて設定されます。
- $A$ and $B$ are hyper-parameters that scale $T_N$ to $[0, T_{max}]$, where $T_{max}$ is the maximum dwell time value of our current online dwell time models. We remain the normalized dwell time range unchanged to reduce possible mismatching issues cooperating with other modules in online.
  - $A$ と $B$ は $T_N$ を $[0, T_{max}]$ にスケールするハイパーパラメータです。オンラインの他のモジュールとの不一致を減らすために正規化された滞在時間範囲を変更しません。

Finally, based on the above discussions, we set $offset = 15, \tau = 20, A = 2.319, B = 0.744$ to satisfy C1 and C2. We have also conducted a grid search on these parameters, and find that the current setting does achieve the best online performance.
最後に、上記の議論に基づいて $offset = 15, \tau = 20, A = 2.319, B = 0.744$ を設定してC1およびC2を満たします。グリッドサーチも実施し、現在の設定が最良のオンラインパフォーマンスを達成することを確認しました。

<!-- ここまで読んだ! -->

### 2.4 Click Reweighting

The valid read and normalized dwell time settings are designed to filter noises and quantify the qualities of clicks for better user preference learning.
有効な読み取りと正規化された滞在時間の設定は、ノイズをフィルタリングし、クリックの質を定量化して、より良いユーザーの好み学習を行うために設計されています。

In Click reweighting, we adopt a multi-task learning (MTL) framework for both valid read prediction and weighted valid read prediction tasks. Specifically, we conduct a shared bottom to share raw user/item features across two tasks.
クリック再重み付けでは、有効な読み取り予測と重み付けされた有効な読み取り予測タスクの両方に対してマルチタスク学習（MTL）フレームワークを採用します。具体的には、2つのタスク間で生のユーザー/アイテムの特徴を共有するために共有ボトムを使用します。

For the valid read tower, without losing generality, we adopt a 3-layer MLP, which takes raw user/item features $f_u, f_{d_i}$ as inputs, and outputs the predicted click probability $P_{u,d_i}$ of user $u$ on item $d_i$. Next, the valid read loss $L_v$ is defined as:
有効な読み取りタワーでは、一般性を失うことなく3層のMLPを採用し、生のユーザー/アイテムの特徴 $f_u, f_{d_i}$ を入力として受け取り、ユーザー $u$ のアイテム $d_i$ に対する予測クリック確率 $P_{u,d_i}$ を出力します。有効な読み取り損失 $L_v$ は次のように定義されます：

$$
L_v = - \sum_{(u,d_i) \in S_p} \log P_{u,d_i} + \sum_{(u,d_j) \in S_n} \log(1 - P_{u,d_j})
\tag{2}
$$

$S_p$ and $S_n$ indicate the positive (i.e., valid read) set and negative (i.e., invalid click and unclick) set, respectively.
$S_p$ と $S_n$ は、それぞれ正（有効な読み取り）セットと負（無効なクリックおよび未クリック）セットを示します。

Similarly, for the weighted valid read tower, we directly use the normalized dwell time $T_N^{u,d_i}$ as the weight of each $(u, d_i)$. Another 3-layer MLP is adopted to output the predicted click probability $P’_{u,d_i}$. The weighted valid read tower is then trained under the loss $L_w$ as follows:
同様に、重み付き有効読取タワーでは、正規化された滞在時間 $T_N^{u,d_i}$ を各 $(u, d_i)$ の重みとして直接使用します。別の3層MLPが予測クリック確率 $P’_{u,d_i}$ を出力します。重み付き有効読取タワーは損失 $L_w$ の下で次のように訓練されます：

$$
L_w = \sum_{(u,d_j) \in S_n} T_N^{u,d_j} \log(1 - P’_{u,d_j}) - \sum_{(u,d_i) \in S_p} T_N^{u,d_i} \log P’_{u,d_i}
\tag{3}
$$

$L_v$ and $L_w$ are linearly combined as the final loss $L = L_v + L_w$.
$L_v$ と $L_w$ は線形に結合され、最終的な損失 $L = L_v + L_w$ となります。

In online deployment, the sum of two towers’ predicted scores is used for online ranking in our system.
オンライン展開では、2つのタワーの予測スコアの合計がオンラインランキングに使用されます。

Jointly considering the original and DT weighted valid read prediction tasks via MTL is beneficial for the overall online performance. Moreover, we have explored enhanced neural networks and MTL methods such as MMoE [10] and PLE [15], while the online improvement is not significant. It may be because the dwell time is highly correlated with clicks. For simplicity, we directly use MLP with shared bottom in our model.
元のタスクとDT重み付き有効読取予測タスクをMTLを通じて共同で考慮することは、全体的なオンラインパフォーマンスにとって有益です。MMoE [10] や PLE [15] のような強化されたMTL手法も探求しましたが、オンラインの改善はそれほど顕著ではありません。これは滞在時間がクリックと高い相関関係にあるためかもしれません。簡潔さのために、共有ボトムを持つMLPを直接使用します。

<!-- ここまで読んだ! -->

## 3 EXPERIMENTS

### 3.1 Dataset and Settings

We conduct both offline and online evaluations on an article recommender system of WeChat Top Stories.
WeChat Top Storiesの記事推薦システムでオフラインおよびオンライン評価を実施します。

The offline dataset contains nearly 29.7M users, 5.3M items, and 751M instances (including 104M clicks and 89.6M valid reads). All instances are chronologically split into the train set and the test set (571M/180M instances). All data are pre-processed via data masking to protect user privacy.
オフラインデータセットには、約29.7Mのユーザー、5.3Mのアイテム、および751Mのインスタンス（104Mのクリックと89.6Mの有効読取を含む）が含まれています。すべてのインスタンスは時系列に基づいてトレーニングセットとテストセット（571M/180Mのインスタンス）に分割されます。すべてのデータはユーザーのプライバシーを保護するためにデータマスキングで前処理されます。

### 3.2 Offline Evaluation and Ablation Study

We build four models with different objectives for offline evaluation and ablation study: 
私たちは、オフライン評価とアブレーション研究のために異なる目的を持つ4つのモデルを構築します：

(a) Single CTR, which only uses CTR as the training objective. 
  (a) 単一CTR、これはCTRのみをトレーニング目的として使用します。

(b) CTR+logDT, which is an MTL model with both CTR and log dwell time as objectives following classical CTR+DT optimization [2, 16]. 
  (b) CTR+logDT、これは古典的なCTR+DT最適化 [2, 16] に従い、CTRとログ滞在時間の両方を目的とするMTLモデルです。

(c) VR+logDT, an MTL model with valid read (VR) and logDT objectives. 
  (c) VR+logDT、有効読取（VR）とログDTの目的を持つMTLモデルです。

(d) VR+NDT (i.e., the final Click reweighting model), which further replaces logDT with our normalized dwell time (NDT). 
  (d) VR+NDT（すなわち、最終的なクリック再重み付けモデル）、これはさらにログDTを私たちの正規化された滞在時間（NDT）に置き換えます。

We evaluate them on the valid read prediction task with AUC and RelaImpr as metrics following [4, 13]. 
私たちは、[4, 13] に従って、AUCとRelaImprを指標として有効読取予測タスクでそれらを評価します。
All baselines share the same neural network for single/MTL towers, with the same raw features and settings for fair comparisons. 
すべてのベースラインは、**単一/MTLタワーのために同じニューラルネットワークを共有し、公平な比較のために同じ生の特徴と設定を持っています。**

**Table 1: Offline evaluation on valid read prediction.**
**表1: 有効読取予測に関するオフライン評価。**

| Model | single CTR | CTR+logDT | VR+logDT | **VR+NDT** |
|---|---|---|---|---|
| AUC | 0.7810 | 0.7849 | 0.7932 | **0.7968** |
| RelaImpr | 0.00% | 1.39% | 4.34% | **5.62%** |

Table 1 shows the results, from which we find that:
表1は結果を示しており、次のことを発見しました：

(1) the final Click reweighting model achieves the best performance on valid read prediction. 
(1) 最終的なクリック再重み付けモデルは、有効読取予測において最良のパフォーマンスを達成します。

The improvements are significant (22.57 < 0.01 with paired t-test) and the deviations of all models are less than ±0.0003. 
改善は有意であり（対になったt検定で22.57 < 0.01）、すべてのモデルの偏差は±0.0003未満です。

It indicates that our Click reweighting can recommend more high-quality items users love to click and read. 
これは、私たちのクリック再重み付けが、ユーザーがクリックして読みたい高品質なアイテムをより多く推薦できることを示しています。

(2) Comparing models with/without VR and NDT, we find that both valid read filtering and normalized DT reweighting are essential for improving users’ valid reads. 
(2) VRとNDTの有無でモデルを比較すると、有効読取フィルタリングと正規化されたDT再重み付けの両方が、ユーザーの有効読取を改善するために不可欠であることがわかります。

(3) Single CTR merely focuses on CTR, and thus performs worse than MTL models with dwell time modeling. 
(3) 単一CTRはCTRにのみ焦点を当てているため、滞在時間モデリングを持つMTLモデルよりもパフォーマンスが劣ります。

(4) We have also evaluated these models on the original CTR prediction, where single CTR achieves the best offline AUC for it is naturally designed for this task. 
(4) 私たちは、これらのモデルを元のCTR予測でも評価しましたが、単一CTRはこのタスクに自然に設計されているため、最良のオフラインAUCを達成します。

However, the Click reweighting model surprisingly achieves the best CTR in the online A/B test (which we care more about). 
しかし、クリック再重み付けモデルは、オンラインA/Bテストで驚くべきことに最良のCTRを達成します（私たちがより重視するものです）。

The click reweighting gives top priority to recommending high-quality items which users may have informative reads on, rather than items users are likely to click guided by CTR-oriented training, bringing in long-term benefits via better user experience. 
クリック再重み付けは、CTR指向のトレーニングに導かれてユーザーがクリックする可能性のあるアイテムではなく、ユーザーが情報を得られる高品質なアイテムを推薦することを最優先します。これにより、より良いユーザー体験を通じて長期的な利益をもたらします。

<!-- ここまで読んだ! -->

### 3.3 Online Evaluation

To verify the online power of Click reweighting, we further conduct an online A/B test on WeChat Top Stories. We focus on four online metrics: (a) CTR, (b) average click number per capita (ACN), (c) dwell time (DT), and (d) average impression number per capita (AIN). We conduct the A/B test for 7 days on nearly 5 million users.
クリック再重み付けのオンラインパワーを検証するために、WeChat Top StoriesでオンラインA/Bテストを実施します。4つのオンライン指標に焦点を当てます：(a) CTR、(b) 一人当たり平均クリック数（ACN）、(c) 滞在時間（DT）、(d) 一人当たり平均インプレッション数（AIN）。約500万人のユーザーに対して7日間A/Bテストを実施します。

**Table 2: Online A/B tests on WeChat Top Stories.**
**表2: WeChat Top StoriesにおけるオンラインA/Bテスト。**

| Model | CTR | ACN | DT | AIN |
|---|---|---|---|---|
| +valid read | +1.910% | +2.478% | -1.698% | +0.558% |
| +valid read+NDT | +2.577% | +4.139% | -3.554% | +1.545% |

From Table 2 we find that: 
表2から私たちは次のことを発見しました：

(1) Both CTR and ACN have significant improvements (𝑝 _< 0.05) armed with valid read. 
(1) CTRとACNの両方が、valid readを用いることで有意な改善を示しています（𝑝 _< 0.05）。
It is impressive that using high-quality valid reads as training objectives can even improve the online click-related metrics. 
高品質なvalid readをトレーニング目的として使用することで、オンラインのクリック関連指標が改善されるのは印象的です。
The improvements are further strengthened by adding normalized dwell time, which reconfirms the effectiveness of NDT on user experience. 
改善は、正規化された滞在時間を追加することでさらに強化され、ユーザー体験に対するNDTの効果を再確認します。

(2) The original dwell time modeling over-emphasizes long dwell time behaviors. 
(2) 元の滞在時間モデリングは、長い滞在時間の行動を過度に強調しています。
Our Click reweighting aims to improve valid reads for all users, thus inevitably sacrificing the performance of dwell time. 
私たちのクリック再重み付けは、すべてのユーザーのvalid readを改善することを目指しているため、滞在時間のパフォーマンスを犠牲にせざるを得ません。

(3) The improvements in ACN and AIN further imply that users are more willing to use our system, which is the core driving force of growth. 
(3) ACNとAINの改善は、ユーザーが私たちのシステムをより利用したいと考えていることを示唆しており、これは成長の核心的な原動力です。

<!-- ここまで読んだ! -->

### 3.4 Online Dwell Time Migration

> **Figure 3: Dwell time migration on different dwell time quantiles and different user activeness in an online system.**
> 図3: オンラインシステムにおける異なる滞在時間の分位数と異なるユーザーの活動性に関する滞在時間の移行。
> - x軸: dwell timeの分位数（P10は最短10%の滞在時間）(あ、滞在時間の値そのものではなく分位数を用いて比較するのわかりやすそうだな...!!一旦はユーザセグメントごとに分けないバージョンで出してみよう。:thinking:)
> - y軸: ユーザーの活動レベル（level7が最も活動的）
> - z軸: ベースラインからクリック再重み付けへの滞在時間の変化率
> - 短い滞在時間（P10/P20）では改善（+5%〜+20%）、長い滞在時間（P80/P90）では減少（-5%〜-15%）

In Fig. 3, we discover an interesting dwell time migration trend of users with different activeness. We find that:
図3では、異なる活動性を持つユーザーの滞在時間移行の興味深い傾向を発見しました：
(1) Both light and heavy users have more dwell time on their short dwell time behaviors (especially for less active users). It implies that users tend to have more valid reads.
(1) ライトユーザーとヘビーユーザーの両方が、短い滞在時間の行動においてより多くの滞在時間を持っています（特に活動が少ないユーザー）。ユーザーがより多くの有効読取を持つ傾向があることを示唆しています。
(2) The dwell time of too-long readings inevitably decreases, since too-long items are not over-emphasized due to the normalized dwell time. In contrast, our model pays more attention to the behaviors of light users on short items.
(2) 長すぎる読書の滞在時間は必然的に減少します。正規化された滞在時間のために長すぎるアイテムは過度に強調されないからです。対照的に、モデルは短いアイテムに対するライトユーザーの行動により多くの注意を払います。
(3) The DT migration matches our purpose to provide more informative and efficient recommendations. We hope users get a better reading experience rather than be stuck in our system.
(3) DTの移行は、**より情報豊かで効率的な推薦を提供**するという目的に合致しています。ユーザーがシステムに閉じ込められるのではなく、より良い読書体験を得ることを望んでいます。

<!-- ここまで読んだ! -->

## 4 RELATED WORKS

There are some efforts attempt to discover clickbaits and purify clicks [1, 3, 6, 11, 12]. In real-world scenarios, the dwell time of clicked items is natural and powerful user feedback that can quantify clicks [5, 7, 9, 20, 24]. The content features are often carefully encoded for dwell time prediction [16, 18]. Recently, some works adopt MTL or multi-optimization objectives to jointly consider CTR and dwell time predictions [2, 22, 27]. However, they do not fully address the over-emphasizing issue of too-long items. Zheng et al. [25] designs a watch time gain to measure the relative dwell time on an item, while it loses the essential information of the specific dwell time value in different items. In this work, we propose a novel behavior valid read with a normalized DT to better fit our purpose of enabling more efficient and informative readings.
クリックベイトを発見しクリックを浄化する研究がいくつかあります [1, 3, 6, 11, 12]。実世界ではクリックされたアイテムの滞在時間は自然で強力なフィードバックです [5, 7, 9, 20, 24]。コンテンツ特徴は滞在時間予測のために慎重にエンコードされます [16, 18]。最近ではMTLやマルチ最適化目的でCTRと滞在時間の予測を共同で考慮する研究もあります [2, 22, 27]。しかし長すぎるアイテムの過度な強調の問題には完全に対処していません。Zheng et al. [25] は視聴時間利得を設計しましたが、異なるアイテム間の具体的な滞在時間値の情報を失います。本研究では、より効率的で情報豊かな読書を可能にするために正規化DTを持つvalid readを提案します。

## 5 CONCLUSION AND FUTURE WORK

In this work, we propose a simple yet effective way to reweight clicks via valid read based filtering with normalized dwell time based reweighting. The click reweighting framework has been deployed on a real-world recommender system in WeChat.
本研究では、正規化された滞在時間に基づく再重み付けを用いた有効読取ベースのフィルタリングにより、クリックを再重み付けするシンプルかつ効果的な方法を提案しました。クリック再重み付けフレームワークはWeChatの実世界の推薦システムに展開されています。

In the future, we will explore more sophisticated valid read modeling, and theoretically and experimentally investigate the pros and cons of our purposes of click reweighting via long-term online metrics.
今後、より洗練された有効読書モデルを探求し、長期的なオンラインメトリクスを通じてクリック再重み付けの目的の利点と欠点を理論的・実験的に調査します。

<!-- ここまで読んだ! -->

## REFERENCES
[1] Amol Agrawal. 2016. Clickbait detection using deep learning. In Proceedings of _NGCT._  
[1] Amol Agrawal. 2016. 深層学習を用いたクリックベイト検出。_NGCT_の論文集にて。

[2] Jingwu Chen, Fuzhen Zhuang, Tianxin Wang, Leyu Lin, Feng Xia, Lihuan Du, and Qing He. 2019. Follow the Title Then Read the Article: Click-Guide Network for Dwell Time Prediction. TKDE (2019).  
[2] Jingwu Chen, Fuzhen Zhuang, Tianxin Wang, Leyu Lin, Feng Xia, Lihuan Du、およびQing He. 2019. タイトルに従って記事を読む：滞在時間予測のためのクリックガイドネットワーク。TKDE（2019）。

[3] Yimin Chen, Niall J Conroy, and Victoria L Rubin. 2015. Misleading online content: recognizing clickbait as" false news". In Proceedings of the 2015 ACM on _workshop on multimodal deception detection._  
[3] Yimin Chen, Niall J Conroy、およびVictoria L Rubin. 2015. 誤解を招くオンラインコンテンツ：クリックベイトを「偽ニュース」として認識する。2015年ACMの_マルチモーダル欺瞞検出ワークショップ_の論文集にて。

[4] Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, and Xiuqiang He. 2017. DeepFM: a factorization-machine based neural network for CTR prediction. In _Proceedings of IJCAI._  
[4] Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li、およびXiuqiang He. 2017. DeepFM：CTR予測のための因子分解機械に基づくニューラルネットワーク。_IJCAI_の論文集にて。

[5] Ahmed Hassan. 2012. A semi-supervised approach to modeling web search satisfaction. In Proceedings of SIGIR.  
[5] Ahmed Hassan. 2012. ウェブ検索満足度のモデル化に関する半教師ありアプローチ。SIGIRの論文集にて。

[6] Sawinder Kaur, Parteek Kumar, and Ponnurangam Kumaraguru. 2020. Detecting clickbaits using two-phase hybrid CNN-LSTM biterm model. Expert Systems with _Applications (2020)._  
[6] Sawinder Kaur, Parteek Kumar、およびPonnurangam Kumaraguru. 2020. 二相ハイブリッドCNN-LSTMビタームモデルを使用したクリックベイトの検出。_Expert Systems with Applications (2020)_。

[7] Youngho Kim, Ahmed Hassan, Ryen W White, and Imed Zitouni. 2014. Modeling dwell time to predict click-level satisfaction. In Proceedings of WSDM.  
[7] Youngho Kim, Ahmed Hassan, Ryen W White、およびImed Zitouni. 2014. 滞在時間をモデル化してクリックレベルの満足度を予測する。WSDMの論文集にて。

[8] Bin Liu, Chenxu Zhu, Guilin Li, Weinan Zhang, Jincai Lai, Ruiming Tang, Xiuqiang He, Zhenguo Li, and Yong Yu. 2020. AutoFIS: Automatic Feature Interaction Selection in Factorization Models for Click-Through Rate Prediction. (2020).  
[8] Bin Liu, Chenxu Zhu, Guilin Li, Weinan Zhang, Jincai Lai, Ruiming Tang, Xiuqiang He, Zhenguo Li、およびYong Yu. 2020. AutoFIS：クリック率予測のための因子分解モデルにおける自動特徴相互作用選択。(2020)。

[9] Yiqun Liu, Xiaohui Xie, Chao Wang, Jian-Yun Nie, Min Zhang, and Shaoping Ma. 2016. Time-aware click model. TOIS (2016).  
[9] Yiqun Liu, Xiaohui Xie, Chao Wang, Jian-Yun Nie, Min Zhang、およびShaoping Ma. 2016. 時間認識型クリックモデル。TOIS（2016）。

[10] Jiaqi Ma, Zhe Zhao, Xinyang Yi, Jilin Chen, Lichan Hong, and Ed H Chi. 2018. Modeling task relationships in multi-task learning with multi-gate mixture-of-experts. In Proceedings of KDD.  
[10] Jiaqi Ma, Zhe Zhao, Xinyang Yi, Jilin Chen, Lichan Hong、およびEd H Chi. 2018. マルチゲート混合専門家を用いたマルチタスク学習におけるタスク関係のモデル化。KDDの論文集にて。

[11] Martin Potthast, Sebastian Köpsel, Benno Stein, and Matthias Hagen. 2016. Clickbait detection. In Proceedings of ECIR.  
[11] Martin Potthast, Sebastian Köpsel, Benno Stein、およびMatthias Hagen. 2016. クリックベイト検出。ECIRの論文集にて。

[12] Lanyu Shang, Daniel Yue Zhang, Michael Wang, Shuyue Lai, and Dong Wang. 2019. Towards reliable online clickbait video detection: A content-agnostic approach. Knowledge-Based Systems (2019).  
[12] Lanyu Shang, Daniel Yue Zhang, Michael Wang, Shuyue Lai、およびDong Wang. 2019. 信頼できるオンラインクリックベイト動画検出に向けて：コンテンツ非依存のアプローチ。Knowledge-Based Systems (2019)。

[13] Weiping Song, Chence Shi, Zhiping Xiao, Zhijian Duan, Yewen Xu, Ming Zhang, and Jian Tang. 2019. Autoint: Automatic feature interaction learning via self-attentive neural networks. In Proceedings of CIKM.  
[13] Weiping Song, Chence Shi, Zhiping Xiao, Zhijian Duan, Yewen Xu, Ming Zhang、およびJian Tang. 2019. Autoint：自己注意型ニューラルネットワークを介した自動特徴相互作用学習。CIKMの論文集にて。

[14] Fei Sun, Jun Liu, Jian Wu, Changhua Pei, Xiao Lin, Wenwu Ou, and Peng Jiang. 2019. BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformer. In Proceedings of CIKM.  
[14] Fei Sun, Jun Liu, Jian Wu, Changhua Pei, Xiao Lin, Wenwu Ou、およびPeng Jiang. 2019. BERT4Rec：トランスフォーマーからの双方向エンコーダ表現を用いた逐次推薦。CIKMの論文集にて。

[15] Hongyan Tang, Junning Liu, Ming Zhao, and Xudong Gong. 2020. Progressive layered extraction (ple): A novel multi-task learning (mtl) model for personalized recommendations. In Proceedings of RecSys.  
[15] Hongyan Tang, Junning Liu, Ming Zhao、およびXudong Gong. 2020. プログレッシブレイヤー抽出（ple）：パーソナライズされた推薦のための新しいマルチタスク学習（mtl）モデル。RecSysの論文集にて。

[16] Tianxin Wang, Jingwu Chen, Fuzhen Zhuang, Leyu Lin, Feng Xia, Lihuan Du, and Qing He. 2020. Capturing Attraction Distribution: Sequential Attentive Network for Dwell Time Prediction. In Proceedings of 2020.  
[16] Tianxin Wang, Jingwu Chen, Fuzhen Zhuang, Leyu Lin, Feng Xia, Lihuan Du、およびQing He. 2020. 魅力分布のキャプチャ：滞在時間予測のための逐次注意ネットワーク。2020年の論文集にて。

[17] Wenjie Wang, Fuli Feng, Xiangnan He, Hanwang Zhang, and Tat-Seng Chua. 2021. Clicks can be cheating: Counterfactual recommendation for mitigating clickbait issue. In Proceedings of SIGIR.  
[17] Wenjie Wang, Fuli Feng, Xiangnan He, Hanwang Zhang、およびTat-Seng Chua. 2021. クリックは欺瞞である可能性がある：クリックベイト問題を軽減するための反事実的推薦。SIGIRの論文集にて。

[18] Chuhan Wu, Fangzhao Wu, Tao Qi, and Yongfeng Huang. 2020. User Modeling with Click Preference and Reading Satisfaction for News Recommendation.. In _Proceedings of IJCAI._  
[18] Chuhan Wu, Fangzhao Wu, Tao Qi、およびYongfeng Huang. 2020. ニュース推薦のためのクリックの好みと読書満足度を用いたユーザーモデリング。_IJCAI_の論文集にて。

[19] Ruobing Xie, Cheng Ling, Yalong Wang, Rui Wang, Feng Xia, and Leyu Lin. 2020. Deep feedback network for recommendation. In Proceedings of IJCAI.  
[19] Ruobing Xie, Cheng Ling, Yalong Wang, Rui Wang, Feng Xia、およびLeyu Lin. 2020. 推薦のための深層フィードバックネットワーク。IJCAIの論文集にて。

[20] Ruobing Xie, Cheng Ling, Shaoliang Zhang, Feng Xia, and Leyu Lin. 2022. Multigranularity Fatigue in Recommendation. In Proceedings of CIKM.  
[20] Ruobing Xie, Cheng Ling, Shaoliang Zhang, Feng Xia、およびLeyu Lin. 2022. 推薦におけるマルチグラニュラリティ疲労。CIKMの論文集にて。

[21] Ruobing Xie, Qi Liu, Liangdong Wang, Shukai Liu, Bo Zhang, and Leyu Lin. 2022. Contrastive cross-domain recommendation in matching. In Proceedings of KDD.  
[21] Ruobing Xie, Qi Liu, Liangdong Wang, Shukai Liu, Bo Zhang、およびLeyu Lin. 2022. マッチングにおける対照的なクロスドメイン推薦。KDDの論文集にて。

[22] Ruobing Xie, Yanlei Liu, Shaoliang Zhang, Rui Wang, Feng Xia, and Leyu Lin. 2021. Personalized approximate pareto-efficient recommendation. In Proceedings _of WWW._  
[22] Ruobing Xie, Yanlei Liu, Shaoliang Zhang, Rui Wang, Feng Xia、およびLeyu Lin. 2021. パーソナライズされた近似パレート効率的推薦。_WWW_の論文集にて。

[23] Ruobing Xie, Yalong Wang, Rui Wang, Yuanfu Lu, Yuanhang Zou, Feng Xia, and Leyu Lin. 2022. Long short-term temporal meta-learning in online recommendation. In Proceedings of WSDM.  
[23] Ruobing Xie, Yalong Wang, Rui Wang, Yuanfu Lu, Yuanhang Zou, Feng Xia、およびLeyu Lin. 2022. オンライン推薦における長短期的時間メタ学習。WSDMの論文集にて。

[24] Xing Yi, Liangjie Hong, Erheng Zhong, Nanthan Nan Liu, and Suju Rajan. 2014. Beyond clicks: dwell time for personalization. In Proceedings of RecSys.  
[24] Xing Yi, Liangjie Hong, Erheng Zhong, Nanthan Nan Liu、およびSuju Rajan. 2014. クリックを超えて：パーソナライズのための滞在時間。RecSysの論文集にて。

[25] Yu Zheng, Chen Gao, Jingtao Ding, Lingling Yi, Depeng Jin, Yong Li, and Meng Wang. 2022. DVR: Micro-Video Recommendation Optimizing Watch-Time-Gain under Duration Bias. In MM.  
[25] Yu Zheng, Chen Gao, Jingtao Ding, Lingling Yi, Depeng Jin, Yong Li、およびMeng Wang. 2022. DVR：持続時間バイアスの下での視聴時間利益を最適化するマイクロビデオ推薦。MMにて。

[26] Guorui Zhou, Xiaoqiang Zhu, Chenru Song, Ying Fan, Han Zhu, Xiao Ma, Yanghui Yan, Junqi Jin, Han Li, and Kun Gai. 2018. Deep interest network for click-through rate prediction. In Proceedings of KDD.  
[26] Guorui Zhou, Xiaoqiang Zhu, Chenru Song, Ying Fan, Han Zhu, Xiao Ma, Yanghui Yan, Junqi Jin, Han Li、およびKun Gai. 2018. クリック率予測のための深層興味ネットワーク。KDDの論文集にて。

[27] Tengfei Zhou, Hui Qian, Zebang Shen, Chao Zhang, Chengwei Wang, Shichen Liu, and Wenwu Ou. 2018. Jump: A joint predictor for user click and dwell time. In Proceedings of IJCAI.  
[27] Tengfei Zhou, Hui Qian, Zebang Shen, Chao Zhang, Chengwei Wang, Shichen Liu、およびWenwu Ou. 2018. Jump：ユーザーのクリックと滞在時間のための共同予測器。IJCAIの論文集にて。  
