---
format:
  revealjs:
    # incremental: false
    # theme: [default, custom_lab.scss]
    theme: [default, custom_lab.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: MNARデータを使った推薦モデルのオフライン評価において、データを重み付けサンプリングしてMARデータに近づける事でbias軽減を試みる論文を読んだ
subtitle: n週連続推薦システム系論文読んだシリーズ 18週目
# date: 2023/06/02
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 論文の基本情報

- title: Debiased offline evaluation of recommender systems: a weighted-sampling approach
- published date: 30 March 2020,
- authors: Diego Carraro, Derek Bridge
- url(paper): [https://dl.acm.org/doi/10.1145/3341105.3375759](https://dl.acm.org/doi/10.1145/3341105.3375759)

## ざっくり論文概要

- MNAR(Missing Not At Random)データをテストデータに使用する場合の推薦モデルのオフライン評価において、テストデータを**重み付けサンプリングしてMARデータに近づける**事でbias軽減を試みる...!という論文.
- MNAR(Missing Not At Random)データの特性を気にせずにnaiveにモデル評価に使用してしまうと、**biasによってモデル性能を誤解してしまい**、本番プロダクトに適用した後に思った通りの効果が出ない可能性があるので......!みたいなモチベーション
- 個人的には、MNARデータに対応する他のアプローチ(ex. 不偏な損失関数を設計)と比較して、学習や評価に使うデータに対する前処理(データを削る)を追加する様なアプローチなので、**既存の学習フローや評価フローをいじる事なく低コストで導入できそうな点**が素敵ポイント...!
- また、先週読んだ論文ではPropensity score(傾向スコア)を用いていたアプローチを提案していたが、この論文でも"交絡因子"という用語が良く使われており、**推薦システムのdebiasの研究分野と因果推論の結びつきを感じた**...!

# Introduction

## 推薦システムのオフライン評価 と 様々な交絡因子

推薦システムのオフライン評価には、ユーザ-アイテム間のinteraction(ex. クリック, 購入, 評価, etc.)の観測データを用いる.しかし様々な**交絡因子(Confounding factor)**によってbias(選択bias)が含まれる. (因果推論の用語だが、推薦の文脈で言えば、"interactionの観測" -> "ユーザのアイテムへの嗜好度合い" の因果関係の観測に影響を与えうる第三の因子.)

- 例1. UI上で目立つ位置に露出されたアイテムは、interactionが発生しやすい.
- 例2. 推薦システム自身が露出したアイテムは、ユーザとinteractionが発生しやすい.(feedback loop)
- 例3. 映画の星1~5の様な明示的評価において、ユーザは自分が好きなアイテムを評価しやすい.

これにより観測データにて欠損したinteractionは**MNAR(Missing Not At Random)**となる. (このような観測データをMNARデータと呼ぶ...!)

## MNARデータが与える影響

- 古典的なオフライン評価は、観測データが**MCAR(Missing Completely At Random)**データまたは**MAR(Missing At Random)**データのいずれかである、という仮定に基づいている.
- MCARやMARであるかのようにMNARデータを評価すると、推薦モデル性能の推定にてbiasが発生する. (ex. 人気アイテムを推薦するモデルや、activeなユーザに過度に特化したモデルを不正に評価する.)
- MNARデータの問題に対応する為に、**3種**のアプローチがある.
  - 1. MNARテストデータの代わりにMARデータを収集する.
  - 2. MNARテストデータのbiasを補正できるように、真のモデル性能の不偏推定量を設計する.
  - 3. MNARテストデータからデータをサンプリングし、**MARに近い性質を持つ介入テストデータ**を作る.

本論文は、**3つ目のアプローチ**に焦点を当てている.

## 本論文の目的 & アプローチの概要

- 本論文の目的: MNARテストデータから MARデータに近い介入テストデータを作る為の、**新しいサンプリング戦略**を調査する事.
- そのために...
  - MNARデータにおけるユーザとアイテムの分布と、unbiasedなMAR分布との間の乖離を考慮して重みを計算する、**重み付けサンプリング戦略**を提案する.
  - オフライン実験を行い、提案したサンプリング手法と既存のサンプリング戦略 SKEW を比較した.

# MNARデータに対処する為の三種のアプローチ

- 1. MNARテストデータの代わりに**MARデータを収集**する.
- 2. MNARテストデータのbiasを補正できるように、**真のモデル性能の不偏推定量を設計**する.
- 3. MNARテストデータからデータをサンプリングし、**MARに近い性質を持つ介入テストデータ**を作る.

本論文では3つ目のアプローチに焦点を当てている.

## (補足) MCARデータとMARデータの定義

MCAR(Missing Completely At Random)とMAR(Missing At Random)は区別される事がある. (ただし本論文ではよりシンプルに、)

- MCAR: ユーザ-アイテムのinteractionが欠損しているか否かは、interaction valueに全く依存しない.
- MAR: ユーザ-アイテムのinteractionが欠損しているか否かは、観測されたinteraction valueに依存し得るが、欠損したinteraction valueには依存しない.

この区別は、**欠損データ分析理論(missing data analysis theory)**に基づいており、最初に[16]によって提案され、後に[18]によって推薦者システムの文献に紹介された.

- MCAR、MAR、MNARは、データの観察パターンを生成するプロセスを記述する為の、異なる**欠損データメカニズム(missing data mechanisms)**を示すために使用される用語.
- 因果推論の文脈では、**割り当てメカニズム(assignment mechanism)**と呼ばれるらしい.

## 方法1. MARデータを収集する.

この方法は通常、**“forced rating approach”(強制評価アプローチ)**と呼ばれる方法によって実施される.

- ユーザとアイテムのペアを一様にランダムサンプリングし、選択された各ユーザ-アイテムのペアに対して、評価を提供することを要求する(強制する).
- この方法で収集したデータは、様々な交絡因子によるbiasを除去できる.
- ただし、この方法で収集されるデータは多くの場合、**MAR-likeなデータ**(MARと比べて少しbiasを含む.) -> 参加に同意するユーザに何らかの傾向がある可能性があるから.
- “forced rating approach”は適用可能 or 適用困難な分野がある.
  - アイテムを提示されたユーザが、**そのアイテムを素早く消費してratingを提供できる**様な分野では可能. (ex. 音楽、衣服ショッピング)
  - アイテム消費にかかる時間が長い場合は困難(ex. 映画.)(映画の予告編を見せる事は可能...!)

## 方法2. biasを補正できるような推定量を設計する.

多くの文献は、MNARテストデータにおける**真の性能に対して不偏な新しい推定量**(i.e. 評価metricや損失関数)を設計することを提案している.

- ex.) [24]にて、データ内の人気バイアスを補正できる様な損失関数の提案.
- ex.2) [22, 28]にて、Inverse-Propensity-Scoring (IPS)を用いて、誤差を重み付ける新たな損失関数を提案. (propensityとは、特定のユーザとアイテムのペアが観察される確率の意味.)

## 方法3. MNARデータから介入データをサンプリングする.

"**intervention approach(介入アプローチ)**"とも呼ばれる.

- **MNARテストセットからサンプリングして、より小さなMARのような介入テストセット(intervened test set)を作成**し、MNARテストセットの代わりに評価で使用する、という方法.
- ex.) Lange et al のSKEW法で、アイテムの人気度に反比例してユーザとアイテムのペアをサンプリングする. -> アイテム間の露出分布がほぼ均一な介在テストセットが生成され、テストセットにおけるアイテムの人気バイアスが軽減される.

# 提案手法の準備: MARデータとMNARデータの特性を紐解く.

MARとMNARのデータセットの特性を分析するための確率的フレームワークを定義する.
このセクションで定義した両データセットの特性を利用して、unbiasedなオフライン評価の為のアプローチを提案する.

## 表記法(notation)の定義

- user-item 空間 : $U \times I$, サイズは$|U| \cdot |I|$
  - user idx: $u \in U = {1, \cdots, |U|}$, item idx: $i \in I = {1, \cdots, |I|}$
- 一般的な観測データセットを $D = {O \in {0, 1}^{U \times I}, Y \in \mathbb{R}^{U \times I}}$ と表記.
  - binary行列$O$には、user-item間にinteractionが観察されたか否か.
  - 行列 $Y$ には、$O$の観測要素に対応するinteraction value が記録：$O_{u,i} = 1 \rightarrow Y_{u,i} \neq 0$ , $O_{u,i} = 0K \rightarrow Y_{u,i} = 0$.
  - "rating"ではなく、"**interaction value(相互作用値)**"という一般的な用語を使用する.($Y$には評価, クリック, 閲覧, 視聴時間などを適用できる.)
- 各user-itemペアが観測されるか否かを表す、binary確率変数 $\mathcal{O}: U \times I → \{0, 1\}$を定義する. 観測確率を$P(\mathcal{O} = 1|u,i) = P(\mathcal{O}|u,i)$ と表す.
- ↑の表記を用いて、同じU×I空間上の2種類のデータセット、**$D_{mnar} = \{O^{mnar},Y^{mna}\}$**と **$D_{mar} = \{O^{mar} ,Y^{mar}\}$** の特性を表現する.

## MARデータセットの特性① 生成過程を整理

$D_{mar}$ の生成過程を述べる.(既存手法のforced ratings approachを想定.)

- ユーザ-アイテムのペアをランダムサンプリングして, $O^{mar}$ を生成.
- $O^{mar}$ の各非ゼロ要素の Interaction value を収集し、$Y^{mar}$ を取得.

生成過程を U×I空間上で定義される確率分布$P_{mar}(\mathcal{O}|u,i)$ を利用して導出する.

## MARデータセットの特性② uとiそれぞれの事後確率を定式化

このような手法で収集されたデータセット $D_{mar}$ を想定すると、**ユーザとアイテムの事後確率**の経験的な推定値は **(ほぼ)一様に分布している** はずである:

$$
P_{mar}(u|\mathcal{O}) = \frac{|O_{u}^{mar}|}{O^{mar}} \approx \frac{1}{|U|}, \forall u \in U
\tag{1}
$$

$$
P_{mar}(i|\mathcal{O}) = \frac{|O_{i}^{mar}|}{O^{mar}} \approx \frac{1}{|I|}, \forall i \in I
\tag{2}
$$

ここで、$O^{mar}_{u}$と$O^{mar}_{i}$はそれぞれ、ユーザuとアイテムiの$O^{mar}$で観測されたInteractionである.

## MARデータセットの特性③ uとiの同時事後確率を定式化

また、観測されるユーザとアイテムは独立のはずなので、(u,i)の事後分布も独立であることがわかり、以下のように書ける：

$$
P_{mar}(u,i|\mathcal{O}) = P_{mar}(u|\mathcal{O}) \cdot P_{mar}(i|\mathcal{O}) \approx \frac{1}{|U||I|}, \forall(u,i) \in U \times I
\tag{3}
$$

ここで、$P_{mar}(u,i|Q)$は、特定のユーザとアイテムのペアの同時事後分布(=事後分布の同時分布、みたいな?)を表す。
よって、MARデータ $D_{mar}$ の特性として、式(3)の性質を満たしているはずである.

## MNARデータセットの特性① 生成過程を整理

同様に、MNARデータセット $D_{mnar} = {O^{mnar},Y^{mnar}}$ の生成過程をモデル化する.

- MARシナリオとは異なりbiasが存在するため，**サンプリング分布 $P_{mnar}$** が、interaction value $Y^{mnar}$(あるいは特定のユーザとアイテム(u,i)を含む他の交絡因子からも)から独立していると仮定できない.
- つまりMNARデータセットでは、一般的に**未知のサンプリング確率 $P_{mnar}(\mathcal{O}|u,i,Y,X)$** によって生成される.
  - ここで $Y⊃Y^{mnar}$は、ユーザとアイテムのinteraction valueの完全なセット(i.e. 答えの様なデータ. ゼロ要素が存在しない真の評価行列).
  - $X$ はサンプリング確率に影響を与える特徴量(共変量、交絡因子)のセット(ex. ユーザのデモグラフィック、アイテムの特徴、アイテムをユーザに公開する方法などのシステム由来の特徴量など).

## MNARデータセットの特性② uとiそれぞれの事後確率を定式化

MNARデータセット $D_{mnar}$ が収集されている場合、MARデータセットで行ったように、 $O^{mnar}$ のユーザとアイテムの事後確率を推定する事ができる. 今度は一般的に、以下の性質があるはず.
(ここでいう事後確率は、O=1のinteractionをランダムに取得した時に、それがユーザuのinteractionである確率、みたいなイメージ...!)

$$
P_{mnar}(u|\mathcal{O}) = \frac{|O^{mnar}_{u}|}{O^{mnar}} \neq  \frac{1}{|U|}, \forall u \in U
\tag{4}
$$

$$
P_{mnar}(i|\mathcal{O}) = \frac{|O^{mnar}_{u}|}{O^{mnar}} \neq  \frac{1}{|U|}, \forall u \in U
\tag{5}
$$

## MNARデータセットの特性③ uとiの同時事後確率を定式化

**一般に、ユーザとアイテムは一様に分布しているわけではない**ので、特定のエントリーが観測された場合、すなわち$\mathcal{O} = 1$の場合、同時事後確率 $P_{mnar}(u,i|\mathcal{O})$ に対してユーザとアイテムの事後独立性は仮定できない. よって...

$$
P_{mnar}(u,i|\mathcal{O}) \neq P_{mnar}(u|\mathcal{O}) \cdot P_{mnar}(i|Q), \forall (u,i) \in U \times I
\tag{6}
$$

本セクションで示した定式化(式(3)と式(6))を使って、次のセクションでdebiasの為のサンプリング戦略を設計する.
(なるほど...?これらの事後確率の定式化をサンプリング戦略で使うのか!)
(このセクションは、**MARデータやMNARデータの性質はかくあるべき**、というような話...!!)

# 提案手法: 重み付けサンプリングによる介入テストセットの作成

**偏ったデータから偏りのない評価を行うため**に、伝統的なランダム hold-out テストセットの代わりに、**介入テストセット(Intervened test set)**を生成して使用する.
本論文では、**WTD** と **WTD_H** の2つのサンプリング戦略を提案している.

## 一般的なサンプリングアプローチの概要

- サンプリングアプローチは、$S$で示されるサンプリング戦略によって、MNARデータ$D^{mnar}$に対してdebias介入を行う事.
- 目的は、介入の結果、データセット$D_S = {O^S \subset O^{mnar},Y^S \subset Y^{mnar}}$となり、**$D_s$が不偏的な性質を持つこと**.(ふむふむ...!)
- 前のセクションのデータ生成過程と同様に、まず$O_S$を生成し、それに応じて$Y_S$を得る.
- **サンプリングを導くbinary確率変数**を$\mathcal{S} : U × I → {0, 1}$とする. (i.e. あるユーザ-アイテムペアがサンプリングされるか否かのbinaryの確率変数=bernouli分布に従うやつ...!) ($\mathcal{O}$と同様に、$P(\mathcal{S}=1)$の代わりに $P(\mathcal{S})$ という略語表記を使う)
- サンプリング戦略 $S$ は、**確率分布関数 $P_S(\mathcal{S}|u,i), \forall(u,i) \in O^{mnar}$** に基づいて実行される. (i.e. u,iを条件づけた時にS=1となる確率が決定される関数のイメージ. つまりこの関数の出力値はbernouli分布のパラメータlambda...!!)

## 提案手法 WTD ① 本戦略のアイデア

- 本アプローチでは、MNARデータ$O^{mnar}$に加えて、MAR的なデータ$O^{mar}$があることを前提に説明する. (え! debiasアプローチ1で取得する様なMAR-likeなデータも必要なの??)
  - ただし後述する実験結果にて、**MARデータがない場合でも、本アプローチを使用できること**を確認した.(良かったー...!)
- 本戦略の主なアイデアは、サンプリング後の $O^S$ の各ユーザ・アイテムペアの事後確率分布、すなわち **$P_S(u，i|\mathcal{S})$ を, $O^{mar}$ のユーザ・アイテム・ペアの観測された事後確率分布、すなわち $P_{mar}(u, i|\mathcal{O})$ とほぼ同じにすること** である. つまり、**$O^S$を$O^{mar}$に後付けで似せたい**...!!

数式で表すと以下:

$$
P_S(u,i|\mathcal{S}) \approx P_{mar}(u,i|\mathcal{O}), \forall(u,i) \in O^S
\tag{7}
$$

## 提案手法 WTD ② 重み付けMNAR事後分布の定義

$$
P_S(u,i|\mathcal{S}) \approx P_{mar}(u,i|\mathcal{O}), \forall(u,i) \in O^S
\tag{7}
$$

この近似を得るために，**ユーザアイテムの重み** $w = (w_{ui})_{u \in U ,i \in I}$ を用いて，サンプリング空間 $O^{mnar}$ の事後分布，すなわち $P_{mnar}(u,i|\mathcal{O})$ を調整する. 調整された**重み付けMNAR事後分布**を $P_{mnar}(u,i|\mathcal{O},w)$ と表記する.
つまり、以下の等式を満たせるような**重みw**を見つけたい:

$$
P_{mnar}(u,i|\mathcal{O},w) = P_{mar}(u,i|\mathcal{O}), \forall(u,i) \in O^{mnar}
\tag{8}
$$

MARデータセットがユーザとアイテムに一様に分布している事から、式(3)の独立性を利用して式(8)の右辺を書き換える:

$$
P_{mnar}(u,i|\mathcal{O},w) = P_{mar}(i|\mathcal{O}) \times P_{mar}(u|\mathcal{O})
\tag{9}
$$

## 提案手法 WTD ② 重み付けMNAR事後分布の定義

ユーザとアイテムのMNAR事後分布を検討した式(6)と同様に、重み付けMNAR事後分布においても **ユーザとアイテムは一般に独立ではない**.
しかし、**ここではユーザとアイテムを独立したものとして扱い**、次のように求める:

$$
P_{mnar}(u,i|\mathcal{O},w)
= P_{mnar}(i|\mathcal{O},w) \times P_{mnar}(u|\mathcal{O},w)
\\
, \forall(u,i) \in O^{mnar}
\tag{10}
$$

**式10は一般的には正しくないが、第6節で経験的に良い結果が得られることを示し、これを正当化する**.(理論的には不当な式変形だけど、経験的に効果あるから採用！って話...!)

## 提案手法 WTD ② 重み付けMNAR事後分布の定義

さて、式(10)を使って、式(9)を次の2つの式に分割することができる:

$$
P_{mnar}(u|\mathcal{O},w) = P_{mar}(u|\mathcal{O})
\tag{11}
$$

$$
P_{mnar}(i|\mathcal{O},w) = P_{mar}(i|\mathcal{O})
\tag{12}
$$

重み付き MNAR 事後分布に関する式(11)と式(12)の結果として、ユーザ-アイテムペアでユニークな重みの代わりに、**ユーザ固有の重み $w = (w_{u})_{u \in U}$** と**アイテム固有の重み $w = (w_i)_{i \in I}$** を定義して計算できる.

(ユーザとアイテムの重みが独立していることは、スケーラビリティの面でも有利. $|U \times I|$の代わりに、$|U| + |I|$の重みだけを計算すればよいから. そして推薦システムの領域では$|U \times I| > |U|+|I|$ となるので...!)

## 提案手法 WTD ③ 重み$w$を導出

本論文では、重み付けMNAR事後分布をモデル化する最も簡単な解決策として, **$P_{mnar}(.|\mathcal{O},w) = w_{.} \cdot P_{mnar}(.|\mathcal{O})$** を提案している (元々の事後確率を重み付けする...!シンプルな作戦!).
これを式(11)及び式(12)に当てはめると、各ユーザ及びアイテムの重み付け分布について、それぞれ**$w_u \cdot P_{mnar}(u|\mathcal{O})＝P_{mar}(u|\mathcal{O})$** と **$w_i \cdot P_{mnar}(i｜\mathcal{O})＝P_{mar}(i｜\mathcal{O})$** が得られる.

この2つの式を逆にすれば、重み$w$の計算式ができあがる:

$$
w_{u} = \frac{P_{mar}(u｜\mathcal{O})}{P_{mnar}(u｜\mathcal{O})}, \forall u \in U
\tag{13}
$$

$$
w_{i} = \frac{P_{mar}(i｜\mathcal{O})}{P_{mnar}(i｜\mathcal{O})}, \forall i \in I
\tag{14}
$$

算出された重みは、**サンプリング空間のMNAR分布と目標のMAR分布との乖離を測る量**と考えることができる.

## 提案手法 WTD ④ 重み$w$を用いてサンプリング確率分布をモデル化

特定の重み$w_u, w_i$が対応するユーザorアイテムのMNAR分布を調整するため、ウェイトを直接使用してサンプリング確率分布をモデル化する. すなわち...

$$
P_S(\mathcal{S}|u,i) = w_u \cdot w_i
$$

サンプリングにおける重みの効果は、**MAR分布に対するMNARサンプリング空間のユーザとアイテムの事後確率がどれだけ乖離しているか**によって、**特定のユーザとアイテムのペアがサンプリングされる確率が増減する**こと.

本サンプリング戦略を**WTD**と呼び、実際には上式の代わりに、**$P_S(\mathcal{S}|u,i) = w_u \cdot (w_i)^2$** を採用する.(アイテムのbias対処により重きを置いた方が経験的に結果が良かったみたい...)

(この変形は、**MNARデータにおいてアイテムの人気が最も影響力のある交絡因子の1つであるとする文献で報告された先行研究**[21, 24]に照らして理にかなっている.)(popularity biasが最も影響のある交絡因子の一つなのか...!)

## 提案手法 WTD_H ① WTDは MARデータが必要だよなぁ...

WTDでは、近似に必要な事後分布(=$P_{mar}(u,i|\mathcal{O})$)を与えるために、**MAR-likeデータを必要としていた**.
しかし“forced rating approach”の説明の際に述べたように、**MARデータは高価であったり、収集不可能だったり**する.
さらに、手元にそれなりの量のMARのようなデータがある場合には、そもそもそのままunbiasedなテストセットとして使用すれば良い.

本論文では、WTDを **MAR-likeデータが無い場合でも適用できる**様に拡張した.

## 提案手法 WTD_H ② 仮説のMAR事後分布を利用

**MARデータの事後確率分布はユーザ & アイテムに対して一様**である(i.e. $P_{mar}(u|\mathcal{O}) = 1/|U|, P_{mar}(i|\mathcal{O}) = 1/|I|$)ことが分かっており、この情報が本サンプリングアプローチに必要なすべてである(うんうん!やっぱり!).
そのため、重み$w_u, w_i$を計算する際にこの**仮説のMAR事後分布**を利用することで、MAR-likeデータセットが不要になる.

このWTDをMARデータ不要ver.に拡張したサンプリング戦略を、**WTD_H（Hは "hypothesized "の略）**と命名する.

# 実験方法 & 結果

**MNARデータから介入テストセットを作成する様々なサンプリング戦略の良し悪し**を評価し、本論文で提案された WTD と WTD_H の活用可能性を探る為に、オフライン実験を行った.

## 実験設定

- **MARデータ部分($D^{mar} = \{O^{mar} ,Y^{mar}\}$)とMNARデータ部分($D^{mar} = \{O^{mnar},Y^{mnar}\}$)**の両方を持つ、公開データセット(2種)を使用した.
- ある推薦モデルのオフライン評価において、**MNARデータから作る介入テストセットによる評価結果**が、**MARな(unbiasedな)テストセットによる評価結果(今回のground-truth!)**とどれだけ**似ているか**という観点から、様々な戦略の良し悪しを評価した.
- シンプルな5種の推薦モデル(AveRating, PosPop, UB_KNN, IB_KNN, MF)に対して、5種のサンプリング戦略(FULL, REG, SKEW, WTD, WTD_H)を適用した.
- 介入テストデータのサイズが、**元のMNARテストデータの50%のサイズ**になる様にサンプリングした.

## (補足)使用するデータセット:

- 2つの公開データセットを使用: CoatShopping(衣服) と Webscope R3(音楽)
- どちらも**MARデータ部分($D^{mar} = \{O^{mar} ,Y^{mar}\}$)とMNARデータ部分($D^{mar} = \{O^{mnar},Y^{mnar}\}$)で構成される**. -> 今回の目的にぴったり...!
- $D^{mar}$ 部分は、いずれもforced ratings approachで収集されているため、ほぼbiasのないMARデータなはず.
- $D^{mnar}$ 部分は、推薦システムの運用中に収集されたもの.

## (補足)サンプリング戦略の良し悪しの評価方法:

- 実験の目的は、**介入テストセットを作成する様々な戦略の良し悪し**を評価すること.
- "良し悪し"の基準は、ある推薦システムのオフライン評価において、介入テストセットによる評価結果が、**unbiasedなテストセットによる評価結果とどれだけ似ているか**.

## (補足)シンプルな5種の推薦モデル

実験において5種の推薦モデルを学習させ、全てのモデルが推薦アイテムのランク付けリストを生成する.

- AvgRating: 非個別化推薦1. 評価値の平均値が高いアイテム順に推薦.
- PosPop: 非個別化推薦2. positive評価値の数が多いアイテム順に推薦.
- UB_KNN: 個別化推薦1. ユーザベースの最近傍アルゴリズム. (評価値傾向が似てるユーザを探す)
- IB_KNN: 個別化推薦2. アイテムベースの最近傍アルゴリズム. (評価値傾向が似てるアイテムを探す)
- MF: 個別化推薦3. 一般的なMatrix Factorizationアルゴリズム.(UB_KNNとIB_KNNのハイブリッド的なイメージ)

## (補足)比較対象の5種のサンプリング戦略

各戦略はサンプリング確率分布 $P_{S}(\mathcal{S}|u,i)$ を定義し、元のMNARテストセット $O^{he}$ (i.e. $Y^{he}$)から介在テストセット $O^{S}$ (i.e. $Y^{S}$)をサンプリングする.

- FULL: サンプリング無しの戦略. $P_S(\mathcal{S}|u,i) = 1$.
- REG: $O^{he}$からの一様ランダムなサンプリング. $P_S(\mathcal{S}|u,i) = 1/|O^{he}|$.
- SKEW: 既存のアイテム人気度に基づくサンプリング戦略. $P_S(\mathcal{S}|u,i) = 1/pop(i)$. $pop(i)$ は$O^{he}$におけるアイテムiのinteractionの観測数.
- **WTD: 提案された戦略1**. $P_S(\mathcal{S}|u,i) = w_{u}(w_{i})^2$. 実際のMARデータ $O^{w}$ からMAR事後分布を推定して $w_u, w_i$ を計算.
- **WTD_H: 提案された戦略1**. $P_S(\mathcal{S}|u,i)$はWTDと同じ. 実際のMARデータ $O^{w}$ を使用せず、仮説のMAR事後分布から $w_{u}, w_{i}$ を計算.

## 実験①: モデル精度指標のground-truth との差

表2は、各推薦モデルに関する**モデル精度指標(Recall@10)のground-truth**(=MARテストセット $Y^gt$ による評価結果)と、各サンプリング戦略による**介在テストセットを使った推定値**のpercentage difference.

![](https://imgur.com/kIAHdl0)

- 一般に提案手法(WTD, WTD_H)は、**ground-truthのモデル性能を最も良く近似**できている.
- **FULL戦略とREG戦略の結果は似ておりground-truthから非常に離れている**.(サンプリング戦略大事!)

## 実験②: オフライン評価による推薦モデル達の順位づけ

- オフライン評価は複数の推薦モデルを順位づけ、**"良さそう"なモデルを絞り込む**. これによりオンライン実験(ex. ABテスト)のコストを節約できる.
- -> モデル性能の推定値がground-truthと近いだけでなく、**複数のモデルの順位付け結果がground-truthとどの程度合致しているか**も重要...!!
- ランキング類似度の評価指標(kendall's tau)を用いて、ground-truthによる順位付けの結果と比較した.

## 実験②: オフライン評価による推薦モデル達の順位づけ

table3は、2種類のデータセットに対する5種のMNARサンプリング戦略によるモデルの順位付け結果の、ground-truthとの類似度の結果.

![](https://imgur.com/WGETlym)

- CoatShoppingデータの場合、いずれもgroud-truthとはかけ離れた順位付け結果.
- $\tau$ 値が低い原因は、MFを最も性能の良いモデルの1つと誤認した結果であり、**ground-truthでは最も悪いモデルだった**. (**学習時も介入データを使ったら**、MFはもっと良いモデルになったりするだろうか...?)

## 実験②: オフライン評価による推薦モデル達の順位づけ

table4は、MFモデルを順位付け対象から除いたver.の結果.F

![](https://imgur.com/0b7IiVw)

- MFモデルを比較対象から外しただけで、$\tau$ の値が大きく異なった.
- モデル順位付けの正解度合い($\tau$)は、比較する推薦モデルの集合によって、大きく変動した.

# まとめ

## 結論

- 本論文では、MNARデータからMAR的な性質を持つ介在テストセットを生成する新しいサンプリング戦略 **WTD**, **WTD_H** を提案した.
- 偏りのないMARテストセットをground-truthとして使用した実験により、サンプリング戦略が、MNARデータがモデルのオフライン性能評価に与えるbiasを軽減できる事を示した.
- 既存のサンプリング戦略 SKEW と比較して、本戦略は**様々な推薦モデルにおいて最も堅牢(robust)**という結果だった.
- WTD戦略ではMARデータが必要だが、**仮説のMAR分布を使うWTD_H**が上手く機能する事わかったので、本戦略の適用においてMARデータは必要ない.

## 提案手法の利点:

提案手法の利点:

- low overhead:
  - 重みの複雑な学習ステップが不要で、シンプルな設計->実装が簡単.
  - 介入によりデータセットのサイズが小さくなる-> 評価(や学習)にかかる**計算コストを削減**できる.
- high generality:
  - データセット中のinteraction valueに依存しない->**explicitデータにもimplicitデータにも**適用可能.
  - 推薦モデルの評価(検証)のみでなく、**学習に拡張**する事も可能.
  - 既存のモデルの学習や、既存のmetricによるオフライン評価に適用可能. (特別なモデルやmetricの設計が不要.)
- サンプリング重みの算出方法に、因果推論的な手法を使うのもありかも...!(それこそpropensity scoreとか?でもlow overheadの利点を失うか...!)