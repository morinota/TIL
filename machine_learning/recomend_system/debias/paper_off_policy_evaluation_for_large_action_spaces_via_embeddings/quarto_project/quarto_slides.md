---
format:
  revealjs:
    # incremental: false
    theme: [default, quarto_custom_style_format.scss]
    slide-number: true
    logo: https://s3-ap-northeast-1.amazonaws.com/qiita-image-store/0/1697279/dfa905d1c1e242b4e39be182ae21a2b6ac72c0ad/large.png?1655951919
    footer: ⇒ [https://qiita.com/morinota](https://qiita.com/morinota)
from: markdown+emoji

fig-cap-location: bottom

title: hogehogeな論文を読んだ
subtitle: n週連続推薦システム系論文読んだシリーズ k週目
date: 2023/07/05
author: morinota
title-slide-attributes:
  #   data-background-image: https://i.imgur.com/nTazczH.png
  data-background-size: contain
  data-background-opacity: "0.5"
---

## 論文の基本情報

- title: Off-Policy Evaluation for Large Action Spaces via Embeddings
- published date: 16 June 2022
- authors: Yuta Saito, Thorsten Joachims
- url(paper):　https://arxiv.org/pdf/2202.06317.pdf

## ざっくり論文概要

ｃｖ

# Intro

## Contextual Banditってなんだっけ?

## Off-Policy Evaluationってなんだっけ?

# 人気なOPE推定量IPS推定量について

IPSは、**観測された報酬 $r_{i}$ を以下のように再重み付けする**ことでπの性能を推定する.

$$
\hat{V}_{IPS}(\pi; D)
:= \frac{1}{n} \sum_{i}^{n} \frac{\pi(a_i|x_i)}{\pi_{0}(a_i|x_i)} r_{i}
\\
= \frac{1}{n} \sum_{i}^{n} w(x_i, a_i) r_{i}
$$

## Common Support Assumption

以下のCommon Support Assunptionを満たす場合に、IPS推定量は不偏になる:

$$
\pi(a|x) > 0 → \pi_{0}(a|x) > 0 for all a \in A and x \in X
$$

(なるほど...!この仮定を、決定論的な推薦モデルよりも確率論的な推薦モデルの方が満たしやすいのかな:thinking:)

## 大規模行動空間の場合のIPSのbias

- しかし、IPSは、特にアクション空間が大きい場合、非常に偏ったものになる可能性がある. -> common support assumptionが満たせなくなるから!
- common support assumptionが真でない場合、IPSは以下のようなバイアスを持つ(Sachdeva et al.(2020))

$$
|Bias(\hat{V}_{IPS}(\pi))| = \mathbb{E}_{p(x)}[\sum_{a \in U_{0}(x, \pi_0)} \pi(a|x) q(x,a)]
$$

- ここで、$U_{0}(x, \pi_0) := {a｜in A｜｜pi_{0}(a|x) = 0}$ は、$\pi_0$ の下での context $x$ に対してsupportされない(i.e. 不足する)アクションの集合.
- $U_{0}(x, \pi_0)$ は、特に行動空間 A が大きいときに大きくなりやすい.
- このバイアスは、logged dataset $D$ に、($\pi_0$ に)サポートされていないactionに関する情報が含まれていないことに起因する.

## 大規模行動空間の場合のIPSのvariance

$$
n \mathbb{V}_{D}[\hat{V}_{IPS}(\pi;D)]
= \mathbb{E}_{p(x) \pi_{0}(a|x)}[w(x,a)^2 \sigma^2(x,a)]
\\
+ \mathbb{V}_{p(x)} [\mathbb{E}_{\pi_{0}(a|x)}[w(x,a) q(x,a)]]
\\
+ \mathbb{E}_{p(x)} [\mathbb{V}_{\pi_{0}(a|x)}[w(x,a) q(x,a)]]
\tag{2}
$$

- ここで、$\sigma^2(x, a) := \mathbb{V}[r|x, a]$ (context $x$ に対して action $a$ を選択した場合に得られる報酬の分散)
- 分散は3つの項から構成される:
  - 第1項は報酬のランダム性.
  - 第2項は context のランダム性.
  - 第3項はIPS重み付けの使用から生じるペナルティで、重みと真の期待報酬(の分散??)に比例する.

# 大規模行動空間に対応する為の新しい推定量の提案

- IPSとDRの限界を克服するための我々の重要なアイデアは、事前情報としてアクションの埋め込みの存在を仮定すること.

## action embedding の活用

## action embedding を用いてV()を再定義

アクションの埋め込みを用いて、policy の性能の定義を次のように再定義する:

$$
V(\pi) = \mathbb{E}_{p(x) \pi(a|x) p(e|x, a) p(r|x, a, e)}[r]
$$

- ここで、期待報酬 $q(x, a) = E_{p(e|x,a)}[q(x, a, e)]$ であり、$q(x, a, e) := E[r|x, a, e]$ であるから、上記の改良は式(1)で与えられた元の定義と矛盾しないことに注意.
- logged bandit dataset: $D = {(x_{i}, a_{i}, e_{i}, r_{i})}_{i=1}^{n}$
- $D$ の各tupleはlogging policy $\pi_0$ によって $(x, a, e, r) \sim p(x) \pi_0(a|x) p(e|x, a) p(r|x, a, e)$ として生成される.

# action embedding を特徴づける2つの性質

## 性質1: Common Embedding Support 仮定

以下の条件を満たす時、logging policy $\pi_{0}$ は policy $\pi$ に対して、Common Embedding Support を持つという.

$$
p(e|x, \pi) > 0 → p(e|x, \pi_{0}) > 0, \forall e \in E,  x \in X
$$

- ここで、$p(e|x, \pi) := \sum_{a \in A} p(e|x, a) \pi(a|x)$ は、context $x$ と policy $\pi$ が与えられた場合の行動埋め込み空間上の周辺分布.
- Common Action Support 仮定に類似しているが、この仮定はaction embedding space(行動埋め込み空間)に関する共通サポートのみを必要とし、行動空間よりも実質的にコンパクトになる.
- Common Action Support仮定が真 -> Common Embedding Supoprt仮定も真になる($p(e|x, a)$ は $\pi$ も $\pi_0$ も同じだから...!). 逆は成立しない.

## 性質2: No Direct Effect Assumption

- 以下の条件を満たす時、action $a$ は action embedding $e$ と reward $r$ に対して no direct effect 仮定を満たす.

$$
a \perp r | x, e
$$

- (xとeで条件づけた時に、$r$ と $a$ は独立になる...!:thinking:)
-
