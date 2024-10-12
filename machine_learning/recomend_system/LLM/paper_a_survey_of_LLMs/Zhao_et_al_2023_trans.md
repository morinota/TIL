## link リンク

- https://ar5iv.labs.arxiv.org/html/2303.18223 https://ar5iv.labs.arxiv.org/html/2303.18223

## title タイトル

A Survey of Large Language Models
大規模言語モデルの調査

## abstract 抄録

Ever since the Turing Test was proposed in the 1950s, humans have explored the mastering of language intelligence by machine.
1950年代にチューリング・テストが提案されて以来、人間は機械による言語知能の習得を探求してきた。
Language is essentially a complex, intricate system of human expressions governed by grammatical rules.
言語とは本来、文法規則に支配された人間の複雑で入り組んだ表現のシステムである。
It poses a significant challenge to develop capable artificial intelligence (AI) algorithms for comprehending and grasping a language.
言語を理解し、把握するための有能な人工知能（AI）アルゴリズムを開発することは重要な課題である。
As a major approach, language modeling has been widely studied for language understanding and generation in the past two decades, evolving from statistical language models to neural language models.
主要なアプローチとして、言語モデリングは過去20年間、言語理解と生成のために広く研究されており、統計的言語モデルからニューラル言語モデルへと発展してきた。
Recently, pre-trained language models (PLMs) have been proposed by pre-training Transformer models over large-scale corpora, showing strong capabilities in solving various natural language processing (NLP) tasks.
近年、大規模なコーパスに対してTransformerモデルを事前学習させた事前学習言語モデル(PLM)が提案されており、様々な自然言語処理(NLP)タスクを解決する上で強力な能力を示している。
Since researchers have found that model scaling can lead to performance improvement, they further study the scaling effect by increasing the model size to an even larger size.
研究者たちは、モデルのスケーリングが性能向上につながることを発見したので、モデルサイズをさらに大きくしてスケーリング効果をさらに研究する。
Interestingly, when the parameter scale exceeds a certain level, these enlarged language models not only achieve a significant performance improvement but also show some special abilities (e.g., in-context learning) that are not present in small-scale language models (e.g., BERT).
興味深いことに、パラメータ・スケールがあるレベルを超えると、これらの拡大言語モデルは大幅な性能向上を達成するだけでなく、小規模言語モデル（BERTなど）にはない特別な能力（文脈内学習など）を示す。
To discriminate the difference in parameter scale, the research community has coined the term large language models (LLM) for the PLMs of significant size (e.g., containing tens or hundreds of billions of parameters).
パラメータ規模の違いを区別するために、研究コミュニティでは、かなりの規模（例えば、数百億から数千億のパラメータを含む）のPLMを大規模言語モデル（LLM）と呼んでいる。
Recently, the research on LLMs has been largely advanced by both academia and industry, and a remarkable progress is the launch of ChatGPT (a powerful AI chatbot developed based on LLMs), which has attracted widespread attention from society.
近年、LLMの研究は産学ともに大きく進展しており、その中でもChatGPT（LLMをベースに開発された強力なAIチャットボット）の登場は、社会的にも広く注目されている。
The technical evolution of LLMs has been making an important impact on the entire AI community, which would revolutionize the way how we develop and use AI algorithms.
LLMの技術的進化は、AIコミュニティ全体に重要なインパクトを与えつつあり、AIアルゴリズムの開発・利用方法に革命をもたらすだろう。
Considering this rapid technical progress, in this survey, we review the recent advances of LLMs by introducing the background, key findings, and mainstream techniques.
このような急速な技術進歩を踏まえ、本サーベイでは、LLMの背景、主要な知見、主要な技術を紹介することにより、LLMの最近の進歩を概観する。
In particular, we focus on four major aspects of LLMs, namely pre-training, adaptation tuning, utilization, and capacity evaluation.
特に、LLMの4つの主要な側面、すなわち事前訓練、適応チューニング、利用、能力評価に焦点を当てる。
Besides, we also summarize the available resources for developing LLMs and discuss the remaining issues for future directions.
さらに、LLMを開発するために利用可能なリソースを要約し、将来の方向性のために残された課題について議論する。
This survey provides an up-to-date review of the literature on LLMs, which can be a useful resource for both researchers and engineers.
この調査は、LLMに関する文献の最新レビューを提供し、研究者と技術者の双方にとって有益なリソースとなる。

# Introduction はじめに

Language is a prominent ability of human beings for expression and communication, which develops in early childhood and evolves over a lifetime [1, 2].
言語は、表現とコミュニケーションのための人間の顕著な能力であり、幼児期に発達し、生涯にわたって発展する[1, 2]。
Whereas for machines, they cannot naturally grasp the abilities of understanding and communicating in the form of human language, unless equipped with powerful artificial intelligence (AI) algorithms.
一方、機械にとっては、強力な人工知能（AI）アルゴリズムを搭載しない限り、人間の言葉を理解し、コミュニケーションするという能力を自然に把握することはできない。
To achieve this goal, it has been a longstanding research challenge that enables machines to read, write, and communicate like humans [3].
この目標を達成するために、機械が人間のように読み、書き、コミュニケーションできるようにすることが長年の研究課題となっている[3]。

Technically, language modeling (LM) is one of the major approaches to advancing language intelligence of machines.
技術的には、言語モデリング（LM）は、機械の言語知能を向上させる主要なアプローチの一つである。
In general, LM aims to model the generative likelihood of word sequences, so as to predict the probabilities of future (or missing) tokens.
一般に、LM は単語列の生成尤度をモデル化し、将来の（あるいは欠落した）トークンの確率を予測することを目的とする。
The research of LM has received extensive research attention in the literature, which can be roughly divided into four major development stages:
LMの研究は、文献上でも広く注目されており、その発展段階は大きく4つに分けられる：

∙
∙

Statistical language models (SLM).
統計的言語モデル（SLM）。
SLMs [4, 5, 6, 7] are developed based on statistical learning methods that rose in the 1990s.
SLM[4、5、6、7]は、1990年代に台頭した統計的学習法に基づいて開発された。
The basic idea is to build the word prediction model based on the Markov assumption, e.g., predicting the next word based on the most recent context.
基本的な考え方は、マルコフ仮定に基づいて単語予測モデルを構築することである。例えば、最新の文脈に基づいて次の単語を予測する。
The SLMs with a fixed context length
コンテクスト長を固定したSLM

�
�

are also called
とも呼ばれる。

�
�

-gram language models, e.g., bigram and trigram language models. -グラム言語モデル、例えばビグラム言語モデルやトリグラム言語モデル。
SLMs have been widely applied to enhance task performance in information retrieval (IR) [8, 9] and natural language processing (NLP) [10, 11, 12].
SLMは、情報検索（IR）[8, 9]や自然言語処理（NLP）[10, 11, 12]において、タスクのパフォーマンスを向上させるために広く応用されている。
However, they often suffer from the curse of dimensionality: it is difficult to accurately estimate high-order language models since an exponential number of transition probabilities need to be estimated.
しかし、それらはしばしば次元の呪いに悩まされる： 指数関数的な数の遷移確率を推定する必要があるためだ。
Thus, specially designed smoothing strategies such as back-off estimation [13] and Good–Turing estimation [14] have been introduced to alleviate the data sparsity problem.
そのため、バックオフ推定[13]やグッドチューリング推定[14]などの特別に設計された平滑化戦略が導入され、データの疎密問題を緩和している。

∙
∙

Neural language models (NLM).
ニューラル言語モデル（NLM）。
NLMs [15, 16, 17] characterize the probability of word sequences by neural networks, e.g., recurrent neural networks (RNNs).
NLM[15,16,17]は、ニューラルネットワーク、例えばリカレントニューラルネットワーク(RNN)によって単語列の確率を特徴付ける。
As a remarkable contribution, the work in [15] introduced the concept of distributed representation of words and modeled the context representation by aggregating the related distributed word vectors.
注目すべき貢献として、[15]の研究は、単語の分散表現の概念を導入し、関連する分散単語ベクトルを集約することによって文脈表現をモデル化した。
By extending the idea of learning effective features for words or sentences, a general neural network approach was developed to build a unified solution for various NLP tasks [18].
単語や文に効果的な特徴を学習するという考え方を拡張することで、さまざまなNLPタスクのための統一されたソリューションを構築する一般的なニューラルネットワークアプローチが開発された[18]。
Further, word2vec [19, 20] was proposed to build a simplified shallow neural network for learning distributed word representations, which were shown to be very effective across a variety of NLP tasks.
さらに、word2vec [19, 20]は、分散した単語表現を学習するための単純化された浅いニューラルネットワークを構築するために提案され、様々なNLPタスクにおいて非常に効果的であることが示された。
These studies initiate the use of language models for representation learning (beyond word sequence modeling), having an important impact on the field of NLP.
これらの研究は、（単語列のモデリングを超えた）表現学習のための言語モデルの使用を開始し、自然言語処理分野に重要な影響を与えた。

∙
∙

Pre-trained language models (PLM).
事前に訓練された言語モデル（PLM）。
As an early attempt, ELMo [21] was proposed to capture context-aware word representations by first pre-training a bidirectional LSTM (biLSTM) network (instead of learning fixed word representations) and fine-tuning the biLSTM network according to specific downstream tasks.
初期の試みとして、ELMo [21]は、まず双方向LSTM（biLSTM）ネットワークを事前学習し（固定的な単語表現を学習する代わりに）、特定の下流タスクに応じてbiLSTMネットワークを微調整することで、文脈を意識した単語表現を捉えることを提案した。
Further, based on the highly parallelizable Transformer architecture [22] with self-attention mechanisms, BERT [23] was proposed by pre-training bidirectional language models with specially designed pre-training tasks on large-scale unlabeled corpora.
さらに、高度に並列化可能なTransformerアーキテクチャ[22]と自己注意メカニズムに基づき、BERT[23]は、大規模なラベル付けされていないコーパス上で特別に設計された事前学習タスクを使用して双方向言語モデルを事前学習することによって提案された。
These pre-trained context-aware word representations are very effective as general-purpose semantic features, which have largely raised the performance bar of NLP tasks.
これらの事前訓練された文脈を考慮した単語表現は、汎用的な意味特徴として非常に効果的であり、自然言語処理タスクのパフォーマンスの水準を大きく引き上げている。
This work has inspired a large number of follow-up work, which sets the “pre-training and fine-tuning” learning paradigm.
この研究は、「事前学習と微調整」という学習パラダイムを設定した多くの後続研究に影響を与えた。
Following this paradigm, a great number of studies on PLMs have been developed, introducing either different architectures [24, 25] (e.g., GPT-2 [26] and BART [24]) or improved pre-training strategies [27, 28, 29].
このパラダイムに従って、異なるアーキテクチャ[24, 25]（GPT-2[26]やBART[24]など）や改良された事前学習戦略[27, 28, 29]を導入したPLMに関する研究が数多く開発されてきた。
In this paradigm, it often requires fine-tuning the PLM for adapting to different downstream tasks.
このパラダイムでは、さまざまな下流タスクに適応するためにPLMを微調整する必要があることが多い。

∙
∙

Large language models (LLM).
大規模言語モデル（LLM）。
Researchers find that scaling PLM (e.g., scaling model size or data size) often leads to an improved model capacity on downstream tasks (i.e., following the scaling law [30]).
研究者たちは、PLMのスケーリング（例えば、モデルサイズやデータサイズのスケーリング）は、多くの場合、下流のタスクにおけるモデル能力の向上につながる（すなわち、スケーリングの法則[30]に従う）ことを発見している。
A number of studies have explored the performance limit by training an ever larger PLM (e.g., the 175B-parameter GPT-3 and the 540B-parameter PaLM).
多くの研究が、より大きなPLM（例えば、175BパラメータのGPT-3や540BパラメータのPaLM）を訓練することによって、性能限界を探ってきた。
Although scaling is mainly conducted in model size (with similar architectures and pre-training tasks), these large-sized PLMs display different behaviors from smaller PLMs (e.g., 330M-parameter BERT and 1.5B-parameter GPT-2) and show surprising abilities (called emergent abilities [31]) in solving a series of complex tasks.
スケーリングは主にモデル・サイズ（同様のアーキテクチャと事前学習タスク）で行われるが、これらの大型PLMは、小型PLM（例えば330MパラメータのBERTや1.5BパラメータのGPT-2）とは異なる挙動を示し、一連の複雑なタスクを解く際に驚くべき能力（創発能力[31]と呼ばれる）を示す。
For example, GPT-3 can solve few-shot tasks through in-context learning, whereas GPT-2 cannot do well.
例えば、GPT-3はコンテクスト内学習によって数ショットのタスクを解くことができるが、GPT-2はうまくできない。
Thus, the research community coins the term “large language models (LLM)”1 for these large-sized PLMs [32, 33, 34, 35].
そのため、研究コミュニティでは、このような大規模なPLMを「大規模言語モデル（LLM）」1という用語で呼んでいる[32, 33, 34, 35]。
A remarkable application of LLMs is ChatGPT2 that adapts the LLMs from the GPT series for dialogue, which presents an amazing conversation ability with humans.
LLMの顕著な応用例として、GPTシリーズのLLMを対話に適応させたChatGPT2があり、人間との驚くべき会話能力を示している。

In the existing literature, PLMs have been widely discussed and surveyed [36, 37, 38, 39], while LLMs are seldom reviewed in a systematic way.
既存の文献では、PLMは広く議論され、調査されている[36, 37, 38, 39]が、LLMは体系的にレビューされることはほとんどない。
To motivate our survey, we first highlight three major differences between LLMs and PLMs.
本調査の動機付けとして、まずLLMとPLMの3つの大きな相違点を強調する。
First, LLMs display some surprising emergent abilities that may not be observed in previous smaller PLMs.
第一に、LLMは、これまでの小型PLMでは見られなかったような、いくつかの驚くべき出現能力を示す。
These abilities are key to the performance of language models on complex tasks, making AI algorithms unprecedently powerful and effective.
これらの能力は、複雑なタスクにおける言語モデルの性能の鍵となり、AIアルゴリズムをかつてないほど強力で効果的なものにしている。
Second, LLMs have revolutionized the way that humans develop and use AI algorithms.
第二に、LLMは人間がAIアルゴリズムを開発し使用する方法に革命をもたらした。
Unlike small PLMs, the major approach to accessing LLMs is through the prompting interface (e.g., GPT-4 API).
小規模なPLMとは異なり、LLMへの主なアクセス方法はプロンプト・インターフェイス（GPT-4 APIなど）を通じて行う。
Humans have to understand how LLMs work and format their tasks in a way that LLMs can follow.
人間は、LLMがどのように働くかを理解し、LLMが従えるようにタスクをフォーマットしなければならない。
Third, the development of LLMs no longer draws a clear distinction between research and engineering.
第三に、LLMの発展は、もはや研究と工学を明確に区別していない。
The training of LLMs requires extensive practical experiences in large-scale data processing and distributed parallel training.
LLMの育成には、大規模データ処理や分散並列トレーニングの豊富な実践経験が必要である。
To develop capable LLMs, researchers have to solve complicated engineering issues, working with engineers or being engineers.
有能なLLMを育成するためには、研究者は複雑な工学的問題を解決し、エンジニアと協力し、あるいはエンジニアになる必要がある。

Nowadays, LLMs are posing a significant impact on the AI community, and the advent of ChatGPT and GPT-4 even leads to the rethinking of the possibilities of artificial general intelligence (AGI).
今日、LLMはAIコミュニティーに大きなインパクトを与えており、ChatGPTやGPT-4の登場は人工知能（AGI）の可能性を再考させるものでさえある。
OpenAI has published a technical article entitled “Planning for AGI and beyond”, which discussed the short-term and long-term plans to approach AGI [40], and a more recent paper has argued that GPT-4 might be considered as an early version of an AGI system [41].
オープンAIは「AGIとその先の計画」と題した技術論文を発表し、AGIに近づくための短期的・長期的な計画について論じている[40]。さらに最近の論文では、GPT-4がAGIシステムの初期バージョンと考えられるかもしれないと論じている[41]。
The research areas of AI have been revolutionized by the rapid progress of LLMs.
AIの研究分野は、LLMの急速な進歩によって革命的な変化を遂げた。
In the field of NLP, LLMs can serve as a general-purpose language task solver (to some extent), and the research paradigm has been shifting towards the use of LLMs.
自然言語処理の分野では、LLMは（ある程度）汎用の言語タスク・ソルバーとして機能することができ、研究のパラダイムはLLMの利用へとシフトしている。
In the field of IR, traditional search engines are challenged by the new information seeking way through AI chatbots (i.e., ChatGPT), and New Bing3 presents an initial attempt that enhances the search results based on LLMs.
IRの分野では、従来の検索エンジンがAIチャットボット（ChatGPT）による新しい情報探索方法に挑戦しており、New Bing3はLLMに基づいて検索結果を強化する最初の試みを提示している。
In the field of CV, the researchers try to develop ChatGPT-like vision-language models that can better serve multimodal dialogues [42, 43, 44, 45], and GPT-4 [46] has supported multimodal input by integrating the visual information.
CVの分野では、研究者はマルチモーダル対話により適したChatGPTのような視覚言語モデルの開発を試みており[42, 43, 44, 45]、GPT-4[46]は視覚情報を統合することでマルチモーダル入力をサポートしている。
This new wave of technology would potentially lead to a prosperous ecosystem of real-world applications based on LLMs.
この新しい技術の波は、LLMに基づく実世界のアプリケーションのエコシステムの繁栄につながる可能性がある。
For instance, Microsoft 365 is being empowered by LLMs (i.e., Copilot) to automate office work, and ChatGPT enables the integration of useful plugins for solving complex tasks.
例えば、マイクロソフト365はLLM（＝Copilot）によってオフィスワークを自動化する力を得ており、ChatGPTは複雑なタスクを解決するための便利なプラグインの統合を可能にしている。

Despite the progress and impact, the underlying principles of LLMs are still not well explored.
その進展と影響にもかかわらず、LLMの根本原理はまだ十分に解明されていない。
Firstly, it is still mysterious why emergent abilities occur in LLMs, instead of smaller PLMs.
第一に、なぜより小さなPLMではなくLLMで創発的な能力が発生するのか、いまだに謎である。
As a more general issue, there still lacks a deep, detailed investigation of the key factors that contribute to the abilities of LLMs.
より一般的な問題として、LLMの能力に寄与する重要な要因に関する深く詳細な調査はまだ行われていない。
It is important to study when and how LLMs obtain such abilities [47].
LLMがいつ、どのようにしてそのような能力を獲得するのかを研究することは重要である[47]。
Although there are some meaningful discussions about this problem [31, 47], more principled investigations are needed to uncover the “secrets“ of LLMs.
この問題については有意義な議論もあるが[31, 47]、LLMの「秘密」を明らかにするためには、より原理的な調査が必要である。
Secondly, it is difficult to train capable LLMs for the research community.
第二に、研究コミュニティーで有能なLLMを育成することが難しい。
Due to the huge cost of model pre-training, it is difficult to carry out repetitive, ablating studies for the research community.
モデルの事前トレーニングに莫大なコストがかかるため、研究者コミュニティのために反復的なアブレーション研究を実施することは難しい。
Indeed, LLMs are mainly trained by industry, where many important training details (e.g., data collection and cleaning) are not revealed to the public.
実際、LLMは主に産業界でトレーニングを受けており、そこでは多くの重要なトレーニングの詳細（データの収集やクリーニングなど）が公開されていない。
Thirdly, it is very challenging to align LLMs with human values or preferences.
第三に、LLMを人間の価値観や嗜好に合わせることは非常に難しい。
Despite the capacities, LLMs are also likely to produce toxic, fictitious, or harmful contents.
LLMは、そのような能力にもかかわらず、有毒な、架空の、あるいは有害なコンテンツを生み出す可能性も高い。
It requires effective and efficient control approaches to eliminating the potential risk of the use of LLMs [46].
LLMの使用による潜在的なリスクを排除するためには、効果的かつ効率的な管理アプローチが必要である[46]。

Faced with both opportunities and challenges, it needs more attention on the research and development of LLMs.
チャンスと課題の両方に直面しているため、LLMの研究開発にもっと注意を払う必要がある。
In order to provide a basic understanding of LLMs, this survey provides a literature review of the recent advances in LLMs from four major aspects, including pre-training (how to pre-train a capable LLM), adaptation tuning (how to effectively tune pre-trained LLMs from the two perspectives of effectiveness and safety), utilization (how to use LLMs for solving various downstream tasks) and capability evaluation (how to evaluate the abilities of LLMs and existing empirical findings).
本サーベイでは、LLMの基本的な理解を提供するために、LLMに関する最近の進歩を、事前訓練（有能なLLMをどのように事前訓練するか）、適応チューニング（事前訓練されたLLMを有効性と安全性の2つの観点からどのように効果的にチューニングするか）、利用（LLMを様々な下流タスクの解決にどのように利用するか）、能力評価（LLMの能力と既存の経験的知見をどのように評価するか）の4つの主要な側面から文献レビューする。
We thoroughly comb the literature and summarize the key findings, techniques, and methods of LLMs.
我々は文献を徹底的に調べ、LLMの主要な発見、技術、方法を要約する。
For this survey, we also create a GitHub project website4 by collecting the supporting resources for LLMs.
今回の調査では、LLMのための支援リソースを集めたGitHubプロジェクトサイト4も作成した。
We are also aware of several related review articles on PLMs or LLMs [38, 39, 48, 36, 49, 50, 32, 51, 52, 43, 53, 54].
また、PLMやLLMに関するいくつかの関連総説[38, 39, 48, 36, 49, 50, 32, 51, 52, 43, 53, 54]も知っている。
These papers either discuss PLMs or some specific (or general) aspects of LLMs.
これらの論文は、PLMまたはLLMの特定の（あるいは一般的な）側面について論じている。
Compared with them, we focus on the techniques and methods to develop and use LLMs and provide a relatively comprehensive reference to important aspects of LLMs.
それらに比べ、我々はLLMを開発し使用するための技術や方法に焦点を当て、LLMの重要な側面について比較的包括的なリファレンスを提供している。

The remainder of the survey is organized as follows: Section 2 introduces the background for the survey article, with the terminology, settings, resources, and organization outline, followed by the summarization of available resources for developing LLMs in Section 3.
調査の残りの部分は以下のように構成されている： セクション2では、用語、設定、リソース、組織の概要など、調査記事の背景を紹介し、セクション3では、LLMを開発するために利用可能なリソースを要約する。
Sections 4, 5, 6, and 7 review and summarize the recent progress from the four aspects of pre-training, adaptation tuning, utilization, and capacity evaluation, respectively.
セクション4、5、6、7では、それぞれ事前トレーニング、適応調整、利用、能力評価の4つの側面から最近の進歩をレビューし、まとめている。
Finally, we conclude this survey in Section 8 by summarizing the major findings and discuss the remaining issues for future work.
最後に、セクション8で主な発見を要約し、今後の課題として残されたものを議論することで、このサーベイを締めくくる。

# Overview 概要

In this section, we introduce the background of LLMs with key terminologies, abilities and techniques.
このセクションでは、LLMの背景を主要な用語、能力、技術とともに紹介する。

Background.
背景
Typically, large language models (LLMs) refer to language models that contain hundreds of billions (or more) of parameters5, which are trained on massive text data [32], such as GPT-3 [55], PaLM [56], Galactica [35], and LLaMA [57].
通常、大規模言語モデル（LLM）とは、数千億（またはそれ以上）のパラメータ5を含む言語モデルを指し、GPT-3[55]、PaLM[56]、Galactica[35]、LLaMA[57]などの膨大なテキストデータ[32]で学習される。
Specifically, LLMs are built upon the Transformer architecture [22], where multi-head attention layers are stacked in a very deep neural network.
具体的には、LLMはTransformerアーキテクチャ[22]に基づいて構築されており、このアーキテクチャでは、非常に深いニューラルネットワークにマルチヘッド注意層が積み重ねられている。
Existing LLMs mainly adopt similar model architectures (i.e., Transformer) and pre-training objectives (i.e., language modeling) as small language models.
既存のLLMは、主に小型言語モデルと同様のモデル・アーキテクチャ（すなわちTransformer）と事前学習目的（すなわち言語モデリング）を採用している。
As the major difference, LLMs largely scale the model size, pre-training data, and total compute (orders of magnification).
大きな違いとして、LLMはモデルサイズ、事前学習データ、総計算量（倍率の桁）を大きくスケールする。
They can better understand the natural language and generate high-quality text based on the given context (i.e., prompts).
自然言語をよりよく理解し、与えられた文脈（すなわちプロンプト）に基づいて高品質のテキストを生成することができる。
Such a capacity improvement can be partially described by the scaling law, where the performance roughly follows a substantial increase with respect to the model size [30].
このような能力向上は、部分的にはスケーリング則によって記述することができ、そこでは、性能はモデルサイズに対して大幅に増加する[30]。
However, some abilities (e.g., in-context learning [55]) are unpredictable according to the scaling law, which can be observed only when the model size exceeds a certain level (as discussed below).
しかし、いくつかの能力（例えば、文脈内学習[55]）は、スケーリング則に従って予測不可能であり、モデルサイズがあるレベルを超えたときにのみ観察できる（後述）。

Emergent Abilities of LLMs.
LLMの新たな能力。
In the literature [31], emergent abilities of LLMs are formally defined as “the abilities that are not present in small models but arise in large models”, which is one of the most distinctive features that distinguish LLMs from previous PLMs.
文献[31]では、LLMの創発能力は「小さなモデルには存在せず、大きなモデルで生じる能力」と正式に定義されており、これはLLMを従来のPLMと区別する最も特徴的な特徴の1つである。
It also introduces a notable characteristic when emergent abilities occur: performance rises significantly above random when the scale reaches a certain level.
また、エマージェンシー・アビリティが発生した場合にも注目すべき特性が導入される： スケールがあるレベルに達すると、パフォーマンスはランダムよりも大幅に上昇する。
By analogy, such an emergent pattern has close connections with the phenomenon of phase transition in physics [31, 58].
類推するに、このような創発パターンは、物理学における相転移現象と密接な関係がある[31, 58]。
In principle, emergent abilities can be also defined in relation to some complex tasks [59, 31], while we are more concerned with general abilities that can be applied to solve multiple tasks.
原理的には、創発的能力はいくつかの複雑なタスクに関連して定義することもできる[59, 31]。
Here, we briefly introduce three representative emergent abilities for LLMs, described as follows.
ここでは、LLMの代表的な3つの能力を簡単に紹介する。

∙
∙

In-context learning.
インコンテクスト学習。
The in-context learning ability is formally introduced by GPT-3 [55]: assuming that the language model has been provided with a natural language instruction and/or several task demonstrations, it can generate the expected output for the test instances by completing the word sequence of input text, without requiring additional training or gradient updates6.
文脈内学習能力はGPT-3 [55]によって正式に導入されている： 言語モデルは、自然言語の命令やいくつかのタスクのデモンストレーションが提供されたと仮定すると、追加の訓練や勾配の更新を必要とせずに、入力テキストの単語シーケンスを完了することにより、テストインスタンスに対して期待される出力を生成することができる6。

∙
∙

Instruction following.
以下の通り。
By fine-tuning with a mixture of multi-task datasets formatted via natural language descriptions (i.e., instructions), LLMs are shown to perform well on unseen tasks that are also described in the form of instructions [61, 62, 28].
自然言語記述（すなわち命令）によってフォーマットされたマルチタスクデータセットを混合して微調整することにより、LLMは、同じく命令形式で記述された未知のタスクでも良好な性能を発揮することが示されている[61, 62, 28]。
With this ability, instruction tuning enables LLMs to perform new tasks by understanding the task instructions without using explicit examples, which can largely improve the generalization ability.
この能力により、LLMは明示的な例を用いることなく、タスクの指示を理解することで新しいタスクを実行できるようになり、汎化能力を大きく向上させることができる。

∙
∙

Step-by-step reasoning.
段階的な推論。
For small language models, it is usually difficult to solve complex tasks that involve multiple reasoning steps, e.g., mathematical word problems.
小さな言語モデルでは、数学の単語問題など、複数の推論ステップを含む複雑なタスクを解くことは通常困難である。
While, with the chain-of-thought reasoning strategy [33], LLMs can solve such tasks by utilizing the prompting mechanism that involves intermediate reasoning steps for deriving the final answer.
一方、思考の連鎖型推論戦略[33]では、LLMは最終的な答えを導き出すための中間推論ステップを含むプロンプトメカニズムを利用することで、このようなタスクを解決することができる。
This ability is speculated to be potentially obtained by training on code [47, 33].
この能力は、コードのトレーニングによって得られる可能性があると推測されている[47, 33]。

Key Techniques for LLMs.
LLMのための主要テクニック
It has been a long way that LLMs evolve into the current state: general and capable learners.
LLMが現在の姿に進化するまでには長い道のりがあった： 一般的で有能な学習者
In the development process, a number of important techniques are proposed, which largely improve the capacity of LLMs.
開発プロセスでは、LLMの能力を大きく向上させる重要な技術が数多く提案されている。
Here, we briefly list several important techniques that (potentially) lead to the success of LLMs, as follows.
ここでは、LLMの成功につながる（可能性のある）いくつかの重要なテクニックを簡単に列挙する。

∙
∙

Scaling.
スケーリング。
Scaling is the key factor to increase the model capacity of LLMs.
スケーリングは、LLMのモデル容量を増やすための重要な要素である。
As the initial attempt, GPT-3 firstly increases the model size to an extremely large scale of 175B parameters.
最初の試みとして、GPT-3はまず、モデルサイズを175Bのパラメータという非常に大きなスケールに拡大した。
Later on, PaLM further raises the parameter scale to a new record of 540B.
その後、PaLMはパラメーター・スケールをさらに引き上げ、540Bという新記録を樹立した。
As discussed before, a large model size is essential to emergent abilities.
前述したように、創発能力には大きなモデルサイズが不可欠である。
While, scaling is not only conducted on model size but also related to data size and total compute [34, 63].
一方、スケーリングはモデル・サイズだけでなく、データ・サイズや総計算量にも関係する[34, 63]。
A recent study [34] has discussed the optimal schedule among the three aspects of model size, data size, and total compute, given a fixed budget.
最近の研究[34]では、固定予算が与えられた場合、モデルサイズ、データサイズ、総計算量の3つの観点から最適なスケジュールを議論している。
Further, the quality of the pre-training data plays a key role in achieving good performance, so that data collection and cleaning strategies are very important to consider when scaling the pre-training corpora.
さらに、事前学習データの質は、良好なパフォーマンスを達成する上で重要な役割を果たすため、事前学習コーパスを拡張する際には、データ収集とクリーニング戦略が非常に重要である。

∙
∙

Training.
トレーニング
Due to the huge model size, it is very challenging to successfully train a capable LLM.
モデルサイズが大きいため、有能なLLMをうまく訓練するのは非常に難しい。
Distributed training algorithms are needed to learn the network parameters of LLMs, in which various parallel strategies are often jointly utilized.
LLMのネットワークパラメータを学習するためには、分散学習アルゴリズムが必要であり、その際、様々な並列戦略が共同で利用されることが多い。
To support distributed training, several optimization frameworks have been released to facilitate the implementation and deployment of parallel algorithms, such as DeepSpeed [64] and Megatron-LM [65].
分散学習をサポートするために、DeepSpeed [64]やMegatron-LM [65]など、並列アルゴリズムの実装と展開を容易にする最適化フレームワークがいくつかリリースされている。
Besides, optimization tricks are also important for training stability and model performance, e.g., restart with training loss spike [56] and mixed precision training [66].
さらに、最適化のトリックも学習の安定性とモデルの性能にとって重要である。例えば、学習損失スパイクによる再スタート[56]や混合精度学習[66]などである。
More recently, GPT-4 [46] proposes to develop special infrastructure and optimization methods that reliably predict the performance of large models with much smaller models.
さらに最近では、GPT-4 [46]が、大規模モデルの性能をはるかに小規模なモデルで確実に予測する特別なインフラと最適化手法の開発を提案している。

∙
∙

Ability eliciting.
能力を引き出す。
After being pre-trained on large-scale corpora, LLMs are endowed with potential abilities as general task solvers.
大規模なコーパスで事前訓練されたLLMは、一般的なタスクソルバとしての潜在的な能力を備えている。
While, these abilities might not be explicitly exhibited when LLMs perform some specific tasks.
しかし、これらの能力は、LLMが特定の仕事をするときには、明示的に発揮されないかもしれない。
As a major approach, it is useful to design suitable task instructions or specific in-context strategies to elicit such abilities.
主要なアプローチとして、そのような能力を引き出すために、適切なタスク指示や特定の文脈内ストラテジーを設計することが有効である。
For instance, chain-of-thought prompting has been shown to be useful to solve complex reasoning tasks by including intermediate reasoning steps.
例えば、思考の連鎖を促すプロンプトは、中間的な推論ステップを含めることで、複雑な推論課題を解決するのに有効であることが示されている。
Besides, we can further perform instruction tuning on LLMs with task descriptions in natural language, for improving the generalizability of LLMs on unseen tasks.
さらに、未知のタスクに対するLLMの汎化性を向上させるために、自然言語によるタスク記述でLLMの命令チューニングを行うことができる。
While, these techniques mainly correspond to the emergent abilities of LLMs, which may not show the same effect on small language models.
一方、これらの技術は主にLLMの創発的な能力に対応するものであり、小さな言語モデルでは同じ効果を示さない可能性がある。

∙
∙

Alignment tuning.
アライメント調整。
Since LLMs are trained to capture the data characteristics of pre-training corpora (including both high-quality and low-quality data), they are likely to generate toxic, biased, or even harmful content for humans.
LLMは（高品質なデータと低品質なデータの両方を含む）事前学習コーパスのデータ特性を捉えるように訓練されているため、人間にとって有害な、偏った、あるいは有害なコンテンツを生成する可能性が高い。
It is necessary to align LLMs with human values, e.g., helpful, honest, and harmless.
LLMを人間の価値観、例えば、役に立つ、正直である、無害であるといった価値観に合わせることが必要である。
For this purpose, InstructGPT [61] designs an effective tuning approach that enables LLMs to follow the expected instructions, which utilizes the technique of reinforcement learning with human feedback [67, 61].
この目的のために、InstructGPT [61]は、LLMが期待される指示に従うことを可能にする効果的なチューニング・アプローチを設計しており、これは人間のフィードバックによる強化学習の技術を利用している[67, 61]。
It incorporates human in the training loop with elaborately designed labeling strategies.
精巧に設計されたラベリング戦略によって、人間をトレーニングループに組み込む。
ChatGPT is indeed developed on a similar technique to InstructGPT, which shows a strong alignment capacity in producing high-quality, harmless responses, e.g., rejecting to answer insulting questions.
ChatGPTは確かにInstructGPTと同様の手法で開発されており、侮辱的な質問には答えないなど、高品質で無害な応答を生成する際に強いアライメント能力を示している。

∙
∙

Tools manipulation.
道具の操作。
In essence, LLMs are trained as text generators over massive plain text corpora, thus performing less well on the tasks that are not best formed or expressed in the text (e.g., numerical computation).
要するに、LLMは膨大なプレーンテキストコーパスのテキストジェネレーターとして訓練されるため、テキストで表現するのが最も適していないタスク（例えば、数値計算）ではあまりうまくいかないのである。
Besides, their capacities are also limited to the pre-training data, e.g., the inability to capture up-to-date information.
その上、その能力もトレーニング前のデータに限られており、例えば、最新の情報を把握することができない。
To tackle these issues, a recently proposed technique is to employ external tools to compensate for the deficiencies of LLMs [68, 69].
これらの問題に取り組むために、最近提案された手法は、LLMの欠陥を補う外部ツールを採用することである[68, 69]。
For example, LLMs can utilize the calculator for accurate computation [69] and employ search engines to retrieve unknown information [70].
例えば、LLMは正確な計算のために電卓を利用し[69]、未知の情報を検索するために検索エンジンを採用することができる[70]。
More recently, ChatGPT has enabled the mechanism of using external plugins (existing or newly created apps)7, which are by analogy with the “eyes and ears” of LLMs.
さらに最近、ChatGPTは外部プラグイン（既存または新たに作成されたアプリ）7を使用するメカニズムを可能にし、これはLLMの「目と耳」に類似している。
Such a mechanism can broadly expand the scope of capacities for LLMs.
このような仕組みは、LLMの能力の幅を広く広げることができる。

Besides, many other factors (e.g., the upgrade of hardware) also contribute to the success of LLMs.
その上、他の多くの要因（例えば、ハードウェアのアップグレード）もLLMの成功に貢献している。
While, we limit our discussion to the technical approaches and key findings for developing LLMs.
一方、ここではLLM開発のための技術的アプローチと主要な発見についての議論に限定する。

# Resources of LLMs LLMのリソース

It is by no means an easy job to develop or reproduce LLMs, considering the challenging technical issues and huge demands of computation resources.
LLMの開発や再現は、困難な技術的問題や計算資源の膨大な要求を考慮すると、決して容易な仕事ではない。
A feasible way is to learn experiences from existing LLMs and reuse publicly available resources for incremental development or experimental study.
実現可能な方法は、既存のLLMから経験を学び、公開されているリソースを再利用して、段階的な開発や実験的研究を行うことである。
In this section, we will mainly summarize the open-source model checkpoints or APIs, available corpora, and useful libraries for LLMs.
このセクションでは、主にオープンソースのモデルチェックポイントやAPI、利用可能なコーパス、LLMのための有用なライブラリについてまとめる。

## Publicly Available Model Checkpoints or APIs 一般に公開されているモデルのチェックポイントまたはAPI

Given the huge cost of model pre-training, well-trained model checkpoints are critical to the study and development of LLMs for the research community.
モデルの事前訓練に莫大なコストがかかることを考えると、よく訓練されたモデルのチェックポイントは、研究コミュニティにとってLLMの研究と開発に不可欠である。
Since the parameter scale is a key factor to consider for using LLMs, we categorize these public models into two scale levels (i.e., tens of billions of parameters or hundreds of billions of parameters), which is useful for users to identify the suitable resources according to their resource budget.
パラメータ規模はLLMを利用する上で考慮すべき重要な要素であるため、我々はこれらの公開モデルを2つの規模レベル（すなわち、数百億パラメータと数千億パラメータ）に分類し、ユーザーがリソース予算に応じて適切なリソースを特定するのに役立つようにした。
Besides, for inference, we can directly employ public APIs to perform our tasks, without running the model locally.
その上、推論に関しては、ローカルでモデルを実行することなく、パブリックAPIを直接利用してタスクを実行することができる。
In this section, we briefly summarize the publicly available checkpoints and APIs for LLMs.
このセクションでは、公開されているLLMのチェックポイントとAPIを簡単に要約する。

Models with Tens of Billions of Parameters.
数百億のパラメータを持つモデル。
Most open-source models of this category have a parameter scale ranging from 10B to 20B, except LLaMA [57] (containing 65B parameters in the largest version).
このカテゴリのほとんどのオープンソースモデルは、LLaMA [57]（最大バージョンで65Bのパラメータを含む）を除いて、10Bから20Bのパラメータスケールを持っている。
Other models within this range include mT5 [72], T0 [28], GPT-NeoX-20B [75], CodeGen [76], UL2 [78], Flan-T5 [81], mT0 [82], and PanGu-
この範囲内の他のモデルには、mT5 [72]、T0 [28]、GPT-NeoX-20B [75]、CodeGen [76]、UL2 [78]、Flan-T5 [81]、mT0 [82]、PanGu-などがある。

�
�

[73].
[73].
Among them, Flan-T5 (11B version) can serve as a premier model for research on instruction tuning, since it explores the instruction tuning from three aspects [81]: increasing the number of tasks, scaling the model size, and fine-tuning with chain-of-thought prompting data.
その中でも、Flan-T5 (11B版)は、3つの側面から命令チューニングを研究しているため、命令チューニング研究の最重要モデルとなり得る[81]： タスク数の増加、モデルサイズの拡大、思考連鎖プロンプトデータによる微調整。
Besides, CodeGen (11B version), as an autoregressive language model designed for generating code, can be considered as a good open-source candidate for exploring the code generation ability.
また、コード生成のために設計された自己回帰言語モデルであるCodeGen（11Bバージョン）は、コード生成能力を探求するための良いオープンソース候補と考えることができる。
It also introduces a new benchmark MTPB [76] specially for multi-turn program synthesis, which is composed by 115 expert-generated problems.
また、多回転プログラム合成に特化した新しいベンチマークMTPB [76]を導入しており、これは115の専門家が生成した問題によって構成されている。
To solve these problems, it requires LLMs to acquire sufficient programming knowledge (e.g., math, array operations, and algorithms).
これらの問題を解決するためには、LLMは十分なプログラミング知識（数学、配列操作、アルゴリズムなど）を身につける必要がある。
As for multilingual tasks, mT0 (13B version) might be a good candidate model, which has been fine-tuned on multilingual tasks with multilingual prompts.
多言語タスクに関しては、多言語プロンプトを含む多言語タスクで微調整されたmT0（13Bバージョン）が良い候補モデルかもしれない。
Furthermore, PanGu-
さらに、パングー

�
�

[73] shows good performance in Chinese downstream tasks in zero-shot or few-shot settings, which is developed based on the deep learning framework MindSpore [99].
[73]は、ディープラーニングのフレームワークであるMindSpore [99]をベースに開発されたもので、ゼロショットまたは数ショットの設定において、中国語の下流タスクで良好なパフォーマンスを示している。
Note that PanGu-
なお、PanGu

�
�

[73] holds multiple versions of models (up to 200B parameters), while the largest public version has 13B parameters.
[73]は複数のバージョンのモデル（最大200Bのパラメータ）を保持しているが、最大の公開バージョンは13Bのパラメータを持つ。
As a more recent release, LLaMA (65B version) [57], which contains approximately five times as many parameters as other models, has exhibited superior performance in tasks related to instruction following.
より最近のリリースとして、LLaMA（65Bバージョン）[57]は、他のモデルの約5倍のパラメータを含み、インストラクション・フォローに関連するタスクで優れたパフォーマンスを示している。
Typically, pre-training models at this scale require hundreds or even thousands of GPUs or TPUs.
通常、この規模のモデルを事前学習するには、数百から数千のGPUやTPUが必要になる。
For instance, GPT-NeoX-20B uses 12 supermicro servers, each equipped with 8 NVIDIA A100-SXM4-40GB GPUs, while LLaMA utilizes 2,048 A100-80G GPUs as reported in their original publications.
例えば、GPT-NeoX-20Bは12台のスーパーマイクロ・サーバーを使用しており、各サーバーには8個のNVIDIA A100-SXM4-40GB GPUが搭載されています。
To accurately estimate the computation resources needed, it is suggested to use the metrics measuring the number of involved computations such as FLOPS (i.e., FLoating point number Operations Per Second) [30].
必要な計算リソースを正確に見積もるには、FLOPS（すなわち、FLoating point number Operations Per Second）[30]のような、関係する計算の数を測定する指標を使用することが推奨される。

Models with Hundreds of Billions of Parameters.
何千億ものパラメータを持つモデル。
For models in this category, only a handful of models have been publicly released.
このカテゴリーのモデルについては、公表されているのはほんの一握りである。
For example, OPT [79], OPT-IML [83], BLOOM [66], and BLOOMZ [82] have nearly the same number of parameters as GPT-3 (175B version), while GLM [80] and Galactica [35] have 130B and 120B parameters, respectively.
例えば、OPT [79]、OPT-IML [83]、BLOOM [66]、BLOOMZ [82]は、GPT-3（175Bバージョン）とほぼ同じ数のパラメータを持ち、GLM [80]とGalactica [35]は、それぞれ130Bと120Bのパラメータを持つ。
Among them, OPT (175B version) has been specially motivated for open-source sharing, which aims to enable researchers to carry out reproducible research at scale.
その中でも、OPT（175B版）は、研究者が再現可能な研究を大規模に実施できるようにすることを目的とした、オープンソース共有のための特別な動機付けがなされている。
For research in cross-lingual generalization, BLOOM (176B version) and BLOOMZ (176B version) can be used as base models, due to the competence in multilingual language modeling tasks.
クロスリンガル汎化の研究では、BLOOM（176Bバージョン）とBLOOMZ（176Bバージョン）は、多言語言語モデリングタスクに適しているため、ベースモデルとして使用することができる。
Among these models, Galactica, GLM, and OPT-IML have been tuned with instructions, which might be good candidates for studying the effect of instruction tuning.
これらのモデルのうち、Galactica、GLM、OPT-IMLは命令でチューニングされており、命令チューニングの効果を研究するための良い候補となるかもしれない。
Models of this scale typically require thousands of GPUs or TPUs to train.
この規模のモデルは通常、訓練に数千のGPUやTPUを必要とする。
For instance, OPT (175B version) requires 992 A100-80GB GPUs, while GLM (130B version) uses a cluster of 96 NVIDIA DGX-A100 (8x40G) GPU nodes.
例えば、OPT（175Bバージョン）は992個のA100-80GB GPUを必要とし、GLM（130Bバージョン）は96個のNVIDIA DGX-A100（8x40G）GPUノードのクラスタを使用します。

Public API of LLMs.
LLMの公開API。
Instead of directly using the model copies, APIs provide a more convenient way for common users to use LLMs, without the need of running the model locally.
モデルのコピーを直接使用する代わりに、APIは、ローカルでモデルを実行する必要なく、一般的なユーザーがLLMを使用するための、より便利な方法を提供します。
As a representative interface for using LLMs, the APIs for the GPT-series models [55, 87, 61, 46] have been widely used for both academia and industry8.
LLMを利用するための代表的なインターフェースとして、GPTシリーズモデルのAPI[55, 87, 61, 46]が学界と産業界の両方で広く利用されている8。
OpenAI has provided seven major interfaces to the models in GPT-3 series: ada, babbage, curie, davinci (the most powerful version in GPT-3 series), text-ada-001, text-babbage-001, and text-curie-001.
OpenAIはGPT-3シリーズのモデルに対して7つの主要なインタフェースを提供しています： ADA、Babbage、Curie、Davinci（GPT-3シリーズで最も強力なバージョン）、text-ada-001、text-babbage-001、text-curie-001です。
Among them, the first four interfaces can be further fine-tuned on the host server of OpenAI.
このうち、最初の4つのインターフェースは、OpenAIのホストサーバー上でさらに微調整することができる。
In particular, babbage, curie, and davinci correspond to the GPT-3 (1B), GPT-3 (6.7B), and GPT-3 (175B) models, respectively [55].
特に、バベッジ、キュリー、ダヴィンチは、それぞれGPT-3 (1B)、GPT-3 (6.7B)、GPT-3 (175B)モデルに対応する[55]。
Besides, there are also two APIs related to Codex [87], called code-cushman-001 (a powerful and multilingual version of the Codex (12B) [87]) and code-davinci-002.
また、Codex [87]に関連するAPIとして、code-cushman-001（Codex (12B) [87]の強力な多言語バージョン）とcode-davinci-002がある。
Further, GPT-3.5 series include one base model code-davinci-002 and three enhanced versions, namely text-davinci-002, text-davinci-003, and gpt-3.5-turbo-0301.
さらに、GPT-3.5シリーズには、1つの基本モデルコード-davinci-002と3つの拡張バージョン、すなわちtext-davinci-002、text-davinci-003、およびgpt-3.5-turbo-0301がある。
It is worth noting that gpt-3.5-turbo-0301 is the interface to invoke ChatGPT.
注目すべきは、gpt-3.5-turbo-0301がChatGPTを呼び出すインターフェースであるということです。
More recently, OpenAI has also released the corresponding APIs for GPT-4, including gpt-4, gpt-4-0314, gpt-4-32k, and gpt-4-32k-0314.
さらに最近、OpenAIはGPT-4に対応するAPI（gpt-4、gpt-4-0314、gpt-4-32k、gpt-4-32k-0314）もリリースした。
Overall, the choice of API interfaces depends on the specific application scenarios and response requirements.
全体として、APIインターフェースの選択は、特定のアプリケーションシナリオと応答要件に依存する。
The detailed usage can be found on their project websites9.
詳しい使い方は、それぞれのプロジェクトのウェブサイト9で見ることができる。

## COmmnly User Corpora 唯一のユーザーコーパス

In contrast to earlier PLMs, LLMs which consist of a significantly larger number of parameters require a higher volume of training data that covers a broad range of content.
以前のPLMとは対照的に、LLMは非常に多くのパラメータから構成されているため、幅広い内容をカバーする大量の学習データを必要とする。
For this need, there are increasingly more accessible training datasets that have been released for research.
このようなニーズに応えるため、研究用に公開されたトレーニングデータセットがますます利用しやすくなっている。
In this section, we will briefly summarize several widely used corpora for training LLMs.
このセクションでは、LLMの学習に広く使われているいくつかのコーパスを簡単に要約する。
Based on their content types, we categorize these corpora into six groups: Books, CommonCrawl, Reddit links, Wikipedia, Code, and others.
コンテンツの種類に基づいて、これらのコーパスを6つのグループに分類した： 書籍、CommonCrawl、Redditリンク、ウィキペディア、コード、その他である。

Books.
本だ。
BookCorpus [100] is a commonly used dataset in previous small-scale models (e.g., GPT [110] and GPT-2 [26]), consisting of over 11,000 books covering a wide range of topics and genres (e.g., novels and biographies).
BookCorpus[100]は、これまでの小規模モデル（GPT[110]やGPT-2[26]など）でよく使われているデータセットで、幅広いトピックやジャンル（小説や伝記など）をカバーする11,000冊以上の書籍から構成されている。
Another large-scale book corpus is Project Gutenberg [101], consisting of over 70,000 literary books including novels, essays, poetry, drama, history, science, philosophy, and other types of works in the public domain.
もう一つの大規模な書籍コーパスはプロジェクト・グーテンベルク[101]で、小説、エッセイ、詩、戯曲、歴史、科学、哲学、その他パブリックドメインの作品を含む7万冊以上の文学書から構成されている。
It is currently one of the largest open-source book collections, which is used in training of MT-NLG [90] and LLaMA [57].
現在、オープンソースの書籍コレクションとしては最大級のもので、MT-NLG [90]やLLaMA [57]の学習に使用されている。
As for Books1 [55] and Books2 [55] used in GPT-3 [55], they are much larger than BookCorpus but have been not publicly released so far.
GPT-3[55]で使用されているBooks1[55]とBooks2[55]については、BookCorpusよりもはるかに大規模であるが、今のところ公開されていない。

CommonCrawl.
コモンクロール
CommonCrawl [111] is one of the largest open-source web crawling databases, containing a petabyte-scale data volume, which has been widely used as training data for existing LLMs.
CommonCrawl [111]は、ペタバイト規模のデータを含む、オープンソースの最大級のウェブクローリングデータベースであり、既存のLLMの学習データとして広く利用されている。
As the whole dataset is very large, existing studies mainly extract subsets of web pages from it within a specific period.
データセット全体が非常に大きいため、既存の研究では主に特定の期間内のウェブページの部分集合を抽出している。
However, due to the widespread existence of noisy and low-quality information in web data, it is necessary to perform data preprocessing before usage.
しかし、ウェブデータにはノイジーで低品質な情報が広く存在するため、利用前にデータの前処理を行う必要がある。
Based on CommonCrawl, there are four filtered datasets that are commonly used in existing work: C4 [71], CC-Stories [102], CC-News [27], and RealNews [103].
CommonCrawlに基づいて、既存の研究で一般的に使用されている4つのフィルタリングされたデータセットがある： C4 [71]、CC-Stories [102]、CC-News [27]、RealNews [103]である。
The Colossal Clean Crawled Corpus (C4) includes five variants10, namely en (806G), en.noclean (6T), realnewslike (36G), webtextlike (17G), and multilingual (38T).
Colossal Clean Crawled Corpus（C4）には、en（806G）、en.noclean（6T）、realnewslike（36G）、webtextlike（17G）、多言語（38T）の5種類がある10。
The en version has been utilized for pre-training T5 [71], LaMDA [85], Gopher [59], and UL2 [78].
enバージョンは、T5 [71]、LaMDA [85]、Gopher [59]、UL2 [78]の事前学習に利用されている。
The multilingual C4, also called mC4, has been used in mT5 [72].
mC4とも呼ばれる多言語C4は、mT5で使用されている[72]。
CC-Stories (31G) is composed of a subset of CommonCrawl data, in which the contents are made in a story-like way.
CC-Stories(31G)は、CommonCrawlデータのサブセットで構成され、その内容はストーリー風に作られている。
While, the original source of CC-Stories is not available now, so a reproduction version, CC-Stories-R [112], has been included in Table II.
一方、CC-Storiesの原典は現在入手できないため、複製版であるCC-Stories-R [112]が表IIに含まれている。
Moreover, two news corpora extracted from CommonCrawl, i.e., REALNEWS (120G) and CC-News (76G), are also commonly used as the pre-training data.
さらに、CommonCrawlから抽出された2つのニュース・コーパス、すなわちREALNEWS（120G）とCC-News（76G）も事前学習データとしてよく使われる。

Reddit Links.
レディットのリンク
Reddit is a social media platform that enables users to submit links and text posts, which can be voted on by others through “upvotes” or “downvotes”.
Redditはソーシャルメディア・プラットフォームで、ユーザーがリンクやテキスト投稿を投稿し、「アップヴォート」や「ダウンヴォート」によって他のユーザーが投票することができる。
Highly upvoted posts are often considered useful, and can be utilized to create high-quality datasets.
アップボートの多い投稿は有用とみなされることが多く、質の高いデータセットを作成するために活用できる。
WebText [26] is a well-known corpus composed of highly upvoted links from Reddit, but it is not publicly available.
WebText[26]は、Redditから高度にupvotedされたリンクで構成された有名なコーパスであるが、一般には公開されていない。
As a surrogate, there is a readily accessible open-source alternative called OpenWebText [104].
その代用として、OpenWebText [104]という容易にアクセスできるオープンソースの代替手段がある。
Another corpus extracted from Reddit is PushShift.io [105], a real-time updated dataset that consists of historical data from Reddit since its creation day.
Redditから抽出された別のコーパスは、PushShift.io [105]である。PushShift.ioは、Redditの作成日からの履歴データから構成されるリアルタイム更新のデータセットである。
Pushshift provides not only monthly data dumps but also useful utility tools to support users in searching, summarizing, and conducting preliminary investigations on the entire dataset.
Pushshiftは、毎月のデータダンプだけでなく、データセット全体の検索、要約、予備調査の実施をサポートする便利なユーティリティツールも提供している。
This makes it easy for users to collect and process Reddit data.
これにより、ユーザーは簡単にレディットのデータを収集し、処理することができる。

Wikipedia.
ウィキペディア
Wikipedia [106] is an online encyclopedia containing a large volume of high-quality articles on diverse topics.
ウィキペディア[106]は、多様なトピックに関する質の高い記事を大量に含むオンライン百科事典である。
Most of these articles are composed in an expository style of writing (with supporting references), covering a wide range of languages and fields.
これらの記事のほとんどは、幅広い言語と分野をカバーする説明的な文体（参考文献付き）で構成されている。
Typically, the English-only filtered versions of Wikipedia are widely used in most LLMs (e.g., GPT-3 [55], LaMDA [85], and LLaMA [57]).
一般的に、ウィキペディアの英語のみでフィルタリングされたバージョンは、ほとんどのLLMで広く使用されている（例えば、GPT-3 [55]、LaMDA [85]、LLaMA [57]）。
Wikipedia is available in multiple languages, so it can be used in multilingual settings.
ウィキペディアは多言語で提供されているので、多言語環境でも利用できる。

Code.
コード
To collect code data, existing work mainly crawls open-source licensed codes from the Internet.
コードデータを収集するために、既存の研究は主にインターネットからオープンソースライセンスコードをクロールしている。
Two major sources are public code repositories under open-source licenses (e.g., GitHub) and code-related question-answering platforms (e.g., StackOverflow).
2つの主要な情報源は、オープンソースライセンスの公開コードリポジトリ（例：GitHub）とコード関連の質問回答プラットフォーム（例：StackOverflow）である。
Google has publicly released the BigQuery dataset [107], which includes a substantial number of open-source licensed code snippets in various programming languages, serving as a representative code dataset.
GoogleはBigQueryデータセット[107]を公開しており、このデータセットには様々なプログラミング言語のオープンソースライセンスされたコードスニペットが相当数含まれており、代表的なコードデータセットとして機能している。
CodeGen has utilized BIGQUERY [76], a subset of the BigQuery dataset, for training the multilingual version of CodeGen (CodeGen-Multi).
CodeGenは、多言語版CodeGen（CodeGen-Multi）の学習に、BigQueryデータセットのサブセットであるBIGQUERY[76]を利用している。

Others.
その他
The Pile [108] is a large-scale, diverse, and open-source text dataset consisting of over 800GB of data from multiple sources, including books, websites, codes, scientific papers, and social media platforms.
Pile [108]は、書籍、ウェブサイト、コード、科学論文、ソーシャルメディアプラットフォームなど、複数のソースから800GBを超えるデータで構成される、大規模で多様なオープンソースのテキストデータセットである。
It is constructed from 22 diverse high-quality subsets.
22の多様で高品質なサブセットから構成されている。
The Pile dataset is widely used in models with different parameter scales, such as GPT-J (6B) [113], CodeGen (16B) [76], and Megatron-Turing NLG (530B) [65].
Pileデータセットは、GPT-J(6B) [113]、CodeGen(16B) [76]、メガトロンチューリングNLG(530B) [65]など、パラメータスケールの異なるモデルで広く使用されている。
Besides, ROOTS [109] is composed of various smaller datasets (totally 1.61 TB of text) and covers 59 different languages (containing natural languages and programming languages), which have been used for training BLOOM [66].
さらに、ROOTS [109]は、さまざまな小さなデータセット（合計1.61 TBのテキスト）から構成され、59の異なる言語（自然言語とプログラミング言語を含む）をカバーしており、BLOOM [66]の学習に使用されている。

As we can see from Figure 2, LLMs no longer rely on a single corpus, but instead utilize multiple data sources for pre-training.
図2からわかるように、LLMはもはや単一のコーパスに頼るのではなく、複数のデータソースを事前学習に利用している。
Therefore, existing studies commonly mix several ready-made datasets (e.g., C4, OpenWebText, and the Pile), and then perform further processing to obtain the pre-training corpus.
そのため、既存の研究では、いくつかの既成のデータセット（C4、OpenWebText、Pileなど）を混ぜ合わせ、さらに処理をして事前学習コーパスを得るのが一般的である。
Besides, to train the LLMs that are adaptive to specific applications, it is also important to extract data from relevant sources (e.g., Wikipedia and BigQuery) for enriching the corresponding information in pre-training data.
さらに、特定のアプリケーションに適応したLLMを学習するためには、事前学習データの対応する情報を充実させるために、関連するソース（例えば、WikipediaやBigQuery）からデータを抽出することも重要である。
To have a quick reference of the data sources used in existing LLMs, we present the pre-training corpora of three representative LLMs:
既存のLLMで使用されているデータソースを簡単に参照できるように、代表的な3つのLLMの事前学習コーパスを紹介する：

∙
∙

GPT-3 (175B) [55] was trained on a mixed dataset of 300B tokens, including CommonCrawl [111], WebText2 [55], Books1 [55], Books2 [55], and Wikipedia [106].
GPT-3(175B)[55]は、CommonCrawl[111]、WebText2[55]、Books1[55]、Books2[55]、Wikipedia[106]を含む300Bトークンの混合データセットで学習された。

∙
∙

PaLM (540B) [56] uses a pre-training dataset of 780B tokens, which is sourced from social media conversations, filtered webpages, books, Github, multilingual Wikipedia, and news.
PaLM(540B)[56]は、780Bトークンの事前学習データセットを使用する。このデータセットは、ソーシャルメディア上の会話、フィルタリングされたウェブページ、書籍、Github、多言語ウィキペディア、ニュースから取得される。

∙
∙

LLaMA [57] extracts training data from various sources, including CommonCrawl, C4 [71], Github, Wikipedia, books, ArXiv, and StackExchange.
LLaMA [57]は、CommonCrawl、C4 [71]、Github、Wikipedia、書籍、ArXiv、StackExchangeを含む様々なソースから学習データを抽出する。
The training data size for LLaMA (6B) and LLaMA (13B) is 1.0T tokens, while 1.4T tokens are used for LLaMA (32B) and LLaMA (65B).
LLaMA（6B）とLLaMA（13B）の学習データサイズは1.0Tトークンで、LLaMA（32B）とLLaMA（65B）では1.4Tトークンが使用されている。

## Library Resource

In this part, we briefly introduce a series of available libraries for developing LLMs.
このパートでは、LLMを開発するために利用可能な一連のライブラリを簡単に紹介する。

∙
∙

Transformers [114] is an open-source Python library for building models using the Transformer architecture, which is developed and maintained by Hugging Face.
Transformers [114]は、Transformerアーキテクチャを使ってモデルを構築するためのオープンソースのPythonライブラリで、Hugging Faceによって開発・保守されている。
It has a simple and user-friendly API, making it easy to use and customize various pre-trained models, as well as tools for dataset processing and evaluation.
シンプルでユーザーフレンドリーなAPIを備えており、様々な事前学習済みモデルの使用やカスタマイズが容易で、データセットの処理や評価のためのツールも用意されている。
It is a powerful library with a large and active community of users and developers who regularly update and improve the models and algorithms.
ユーザーや開発者の大規模で活発なコミュニティがあり、モデルやアルゴリズムを定期的に更新・改良している強力なライブラリである。

∙
∙

DeepSpeed [64] is a PyTorch-based deep learning optimization library developed by Microsoft, which has been used to train a number of LLMs, such as GPT-Neo [115] and BLOOM [66].
DeepSpeed [64]は、Microsoftが開発したPyTorchベースの深層学習最適化ライブラリで、GPT-Neo [115]やBLOOM [66]など、多くのLLMの学習に使用されている。
It provides various optimization techniques for distributed training, such as memory optimization (ZeRO technique), gradient checkpointing, and pipeline parallelism.
メモリ最適化（ZeRO技術）、勾配チェックポイント、パイプライン並列など、分散トレーニングのためのさまざまな最適化技術を提供する。
Additionally, it provides the API for fine-tuning and evaluating these models.
さらに、これらのモデルを微調整し、評価するためのAPIも提供する。

∙
∙

Megatron-LM [116] is a PyTorch-based deep learning library developed by NVIDIA for training large-scale language models.
Megatron-LM [116]は、大規模な言語モデルを学習するためにNVIDIAによって開発されたPyTorchベースのディープラーニングライブラリである。
It also provides rich optimization techniques for distributed training, including model and data parallelism, mixed-precision training, FlashAttention, and gradient checkpointing.
また、モデルとデータの並列処理、混合精度トレーニング、FlashAttention、勾配チェックポイントなど、分散トレーニングのための豊富な最適化技術も提供する。
These optimization techniques can significantly improve the training efficiency and speed, enabling efficient distributed training across GPUs and machines.
これらの最適化技術により、トレーニングの効率と速度を大幅に向上させることができ、GPUやマシン間での効率的な分散トレーニングが可能になります。

∙
∙

JAX [117] is a Python library for high-performance machine learning developed by Google Brain, allowing users to easily perform computations on arrays with hardware acceleration (GPU or TPU) support.
JAX [117]は、Google Brainによって開発された高性能機械学習のためのPythonライブラリで、ハードウェアアクセラレーション（GPUまたはTPU）をサポートする配列上でユーザーが簡単に計算を実行できるようにする。
It supports computation on various devices and also provides several convenient functions, such as just-in-time compilation acceleration and automatic batching.
さまざまなデバイスでの計算をサポートし、ジャストインタイム・コンパイルの高速化や自動バッチ処理など、便利な機能も備えている。

∙
∙

Colossal-AI [118] is a deep learning library developed by EleutherAI for training large-scale language models.
Colossal-AI [118]は、EleutherAIによって開発された、大規模な言語モデルを学習するためのディープラーニング・ライブラリである。
It is built on top of JAX and supports optimization strategies for training such as mixed-precision training and parallelism.
JAXの上に構築され、混合精度のトレーニングや並列処理など、トレーニングの最適化戦略をサポートしている。
Recently, a ChatGPT-like model called ColossalChat [119] has been publicly released with two versions (7B and 13B), which are developed using Colossal-AI based on LLaMA [57].
最近、ColossalChat [119]と呼ばれるChatGPTのようなモデルが、LLaMA [57]に基づくColossal-AIを使用して開発された2つのバージョン（7Bと13B）で公開された。

∙
∙

BMTrain [120] is an efficient library developed by OpenBMB for training models with large-scale parameters in a distributed manner, which emphasizes code simplicity, low resource, and high availability.
BMTrain [120]は、OpenBMBによって開発された、大規模なパラメータを持つモデルを分散して学習するための効率的なライブラリであり、コードのシンプルさ、低リソース、高可用性を重視している。
BMTrain has already incorporated several common LLMs (e.g., Flan-T5 [81] and GLM [80]) into its ModelCenter, where developers can use these models directly.
BMTrainは、すでにいくつかの一般的なLLM（Flan-T5 [81]やGLM [80]など）をModelCenterに組み込んでおり、開発者はこれらのモデルを直接使用することができる。

∙
∙

FastMoE [121] is a specialized training library for MoE (i.e., mixture-of-experts) models.
FastMoE [121]は、MoE（＝mixture-of-experts）モデルに特化した学習ライブラリである。
It is developed on top of PyTorch, prioritizing both efficiency and user-friendliness in its design.
PyTorch上で開発されており、効率性と使いやすさの両方を優先して設計されています。
FastMoE simplifies the process of transferring Transformer models to MoE models and supports both data parallelism and model parallelism during training.
FastMoEは、TransformerモデルをMoEモデルに転送するプロセスを簡素化し、トレーニング中のデータ並列性とモデル並列性の両方をサポートします。

Besides the above libraries, existing deep learning frameworks (e.g., PyTorch [122], TensorFlow [123], MXNet [124], PaddlePaddle [125], MindSpore [99], and OneFlow [126]) have also provided support for parallelism algorithms, which are commonly used for training large-scale models.
上記のライブラリ以外にも、既存の深層学習フレームワーク（PyTorch [122]、TensorFlow [123]、MXNet [124]、PaddlePaddle [125]、MindSpore [99]、OneFlow [126]など）も、大規模モデルの学習によく使われる並列化アルゴリズムのサポートを提供している。

# Pre-training 事前トレーニング

Pre-training establishes the basis of the abilities of LLMs.
事前研修は、LLMの能力の基礎を確立する。
By pre-training on large-scale corpora, LLMs can acquire essential language understanding and generation skills [55, 56].
大規模なコーパスで事前学習することで、LLMは本質的な言語理解と生成スキルを習得することができる[55, 56]。
In this process, the scale and quality of the pre-training corpus are critical for LLMs to attain powerful capabilities.
このプロセスにおいて、LLMが強力な能力を獲得するためには、事前学習コーパスの規模と質が重要である。
Besides, to effectively pre-train LLMs, model architectures, acceleration methods, and optimization techniques need to be well designed.
さらに、LLMを効果的にプリ・トレーニングするためには、モデル・アーキテクチャ、アクセラレーション手法、最適化手法をうまく設計する必要がある。
In what follows, we first discuss the data collection and processing in Section 4.1, then introduce the commonly used model architectures in Section 4.2, and finally present the training techniques to stably and efficiently optimize LLMs in Section 4.3.
以下では、まずセクション4.1でデータの収集と処理について説明し、セクション4.2で一般的に使用されているモデル・アーキテクチャを紹介し、最後にセクション4.3でLLMを安定的かつ効率的に最適化するための学習技術を紹介する。

## Data Collection データ収集

Compared with small-scale language models, LLMs have a stronger demand for high-quality data for model pre-training, and their model capacities largely rely on the pre-training corpus and how it has been preprocessed.
小規模な言語モデルに比べ、LLMはモデルの事前学習に高品質なデータをより強く要求され、そのモデルの能力は事前学習コーパスとその前処理に大きく依存する。
In this part, we discuss the collection and processing of pre-training data, including data sources, preprocessing methods, and important analysis of how pre-training data affects the performance of LLMs.
このパートでは、データソース、前処理方法、および事前学習データがLLMの性能にどのような影響を与えるかについての重要な分析を含む、事前学習データの収集と処理について説明する。

### Data Source データソース

To develop a capable LLM, it is key to collect a large amount of natural language corpus from various data sources.
有能なLLMを開発するためには、様々なデータソースから大量の自然言語コーパスを収集することが鍵となる。
Existing LLMs mainly leverage a mixture of diverse public textual datasets as the pre-training corpus.
既存のLLMは、主に事前学習コーパスとして、多様な公開テキストデータセットの混合を活用している。
Figure 2 shows the distribution of the sources of pre-training data for several existing LLMs.
図2は、いくつかの既存のLLMの事前学習データのソースの分布を示す。

The source of pre-training corpus can be broadly categorized into two types: general data and specialized data.
プリ・トレーニング・コーパスのソースは大きく2種類に分類できる： 一般的なデータと特殊なデータである。
General data, such as webpages, books, and conversational text, is utilized by most LLMs [56, 55, 79] due to its large, diverse, and accessible nature, which can enhance the language modeling and generalization abilities of LLMs.
ウェブページ、書籍、会話テキストなどの一般的なデータは、その大規模で多様、かつアクセスしやすい性質から、ほとんどのLLM [56, 55, 79]で利用されており、LLMの言語モデリング能力と汎化能力を高めることができる。
In light of the impressive generalization capabilities exhibited by LLMs, there are also studies that extend their pre-training corpus to more specialized datasets, such as multilingual data, scientific data, and code, endowing LLMs with specific task-solving capabilities [56, 35, 76].
LLMが示す印象的な汎化能力を考慮して、LLMの事前学習コーパスを多言語データ、科学データ、コードなどのより専門的なデータセットに拡張し、LLMに特定のタスク解決能力を与える研究もある[56, 35, 76]。
In what follows, we describe these two types of pre-training data sources and their effects on LLMs.
以下では、これら2種類の事前学習データソースと、それらがLLMに与える影響について説明する。
For a detailed introduction to the commonly used corpus, one can refer to Section 3.2.
よく使われるコーパスの詳しい紹介は、セクション3.2を参照されたい。

General Data.
一般データ。
As we can see in Figure 2, the vast majority of LLMs adopt general-purpose pre-training data, such as webpages, books, and conversational text, which provides rich text sources on a variety of topics.
図2を見ればわかるように、LLMの大半は、ウェブページ、書籍、会話文などの汎用的な事前学習データを採用しており、さまざまなトピックに関する豊富なテキストソースを提供している。
Next, we briefly summarize three important kinds of general data.
次に、3種類の重要な一般データを簡単にまとめる。

∙
∙

Webpages.
ウェブページ
Owing to the proliferation of the Internet, various types of data have been created, which enables LLMs to gain diverse linguistic knowledge and enhance their generalization capabilities [26, 71].
インターネットの普及により、さまざまな種類のデータが作成され、LLMは多様な言語知識を得て、汎化能力を高めることができる[26, 71]。
For convenient use of these data resources, a large amount of data is crawled from the web in previous work, such as CommonCrawl [111].
これらのデータ資源を便利に利用するために、CommonCrawl [111]のような先行研究では、大量のデータがウェブからクロールされている。
However, the crawled web data tends to contain both high-quality text, such as Wikipedia and low-quality text, like spam mail, thus it is important to filter and process webpages for improving the data quality.
しかし、クロールされたウェブデータには、ウィキペディアのような高品質のテキストと、スパムメールのような低品質のテキストの両方が含まれる傾向があるため、データの品質を向上させるためにウェブページをフィルタリングして処理することが重要である。

∙
∙

Conversation text.
会話文。
Conversation data can enhance the conversational competence of LLMs [79] and potentially improve their performance on a range of question-answering tasks [56].
会話データは、LLMの会話能力を高め[79]、様々な質問応答タスクのパフォーマンスを向上させる可能性がある[56]。
Researchers can utilize subsets of public conversation corpus (e.g., PushShift.io Reddit corpus) [127, 105] or collect conversation data from online social media.
研究者は、公開会話コーパスのサブセット（例：PushShift.io Redditコーパス）[127, 105]を利用したり、オンラインソーシャルメディアから会話データを収集したりすることができる。
Since online conversational data often involves discussions among multiple participants, an effective processing way is to transform a conversation into a tree structure, where the utterance is linked to the one it responds to.
オンライン上の会話データは、複数の参加者の間で議論されることが多いので、効果的な処理方法は、会話をツリー構造に変換することである。
In this way, the multi-party conversation tree can be divided into multiple sub-conversations, which can be collected in the pre-training corpus.
このようにして、複数パーティの会話ツリーを複数のサブ会話に分割し、事前学習コーパスに収集することができる。
Furthermore, a potential risk is that the excessive integration of dialogue data into LLMs may result in a side effect [79]: declarative instructions and direct interrogatives are erroneously perceived as the beginning of conversations, thus leading to a decline in the efficacy of the instructions.
さらに、潜在的なリスクとして、対話データをLLMに過度に統合することで、副作用が生じる可能性がある [79]： 宣言的な指示や直接的な疑問詞は、会話の始まりと誤って認識され、その結果、指示の有効性が低下する。

∙
∙

Books.
本だ。
Compared to other corpus, books provide an important source of formal long texts, which are potentially beneficial for LLMs to learn linguistic knowledge, model long-term dependency, and generate narrative and coherent texts.
他のコーパスに比べ、書籍は正式な長文の重要な情報源であり、LLMが言語知識を学び、長期的な依存関係をモデル化し、物語的で首尾一貫したテキストを生成するのに役立つ可能性がある。
To obtain open-source book data, existing studies usually adopt the Books3 and Bookcorpus2 datasets, which are available in the Pile dataset [108].
オープンソースの書籍データを入手するために、既存の研究では通常、Pileデータセット[108]で利用可能なBooks3とBookcorpus2データセットを採用している。

Specialized Data.
専門的なデータ。
Specialized datasets are useful to improve the specific capabilities of LLMs on downstream tasks.
専門的なデータセットは、下流タスクにおけるLLMの特定の能力を向上させるのに有効である。
Next, we introduce three kinds of specialized data.
次に、3種類の特殊データを紹介する。

∙
∙

Multilingual text.
多言語テキスト。
Besides the text in the target language, integrating a multilingual corpus can enhance the multilingual abilities of language understanding and generation.
ターゲット言語のテキストだけでなく、多言語コーパスを統合することで、言語理解と生成の多言語能力を高めることができる。
For example, BLOOM [66] and PaLM [56] have curated multilingual data covering 46 and 122 languages, respectively, within their pre-training corpora.
例えば、BLOOM [66]とPaLM [56]は、事前学習コーパスに、それぞれ46言語と122言語をカバーする多言語データをキュレーションしている。
These models demonstrate impressive performance in multilingual tasks, such as translation, multilingual summarization, and multilingual question answering, and achieve comparable or superior performance to the state-of-the-art models that are fine-tuned on the corpus in the target language(s).
これらのモデルは、翻訳、多言語要約、多言語質問応答などの多言語タスクにおいて目覚ましい性能を発揮し、対象言語のコーパス上で微調整された最先端のモデルに匹敵するか、それ以上の性能を達成している。

∙
∙

Scientific text.
科学的な文章。
The exploration of science by humans has been witnessed by the increasing growth of scientific publications.
人類による科学の探求は、科学出版物の増加によって証明されている。
In order to enhance the understanding of scientific knowledge for LLMs [35, 128], it is useful to incorporate a scientific corpus for model pre-training [35, 128].
LLM[35,128]の科学的知識の理解を深めるためには、モデルの事前学習に科学コーパスを取り入れることが有効である[35,128]。
By pre-training on a vast amount of scientific text, LLMs can achieve impressive performance in scientific and reasoning tasks [129].
膨大な量の科学的テキストで事前学習することで、LLMは科学的タスクや推論タスクにおいて素晴らしいパフォーマンスを達成することができる[129]。
To construct the scientific corpus, existing efforts mainly collect arXiv papers, scientific textbooks, math webpages, and other related scientific resources.
科学コーパスを構築するために、既存の取り組みでは主にarXiv論文、科学教科書、数学ウェブページ、その他の関連科学リソースを収集している。
Due to the complex nature of data in scientific fields, such as mathematical symbols and protein sequences, specific tokenization and preprocessing techniques are usually required to transform these different formats of data into a unified form that can be processed by language models.
数学記号やタンパク質配列など、科学分野のデータは複雑な性質を持っているため、これらの異なる形式のデータを言語モデルで処理可能な統一された形式に変換するには、通常、特定のトークン化と前処理技術が必要となる。

∙
∙

Code.
コード
Program synthesis has been widely studied in the research community [130, 131, 132, 87, 133], especially the use of PLMs trained on code [115, 113].
プログラム合成は研究コミュニティで広く研究されており[130, 131, 132, 87, 133]、特にコードに学習させたPLMの利用が注目されている[115, 113]。
However, it remains challenging for these PLMs (e.g., GPT-J [113]) to generate high-quality and accurate programs.
しかし、これらのPLM（例えばGPT-J [113]）が高品質で正確なプログラムを生成することは依然として困難である。
Recent studies [87, 133] have found that training LLMs on a vast code corpus can lead to a substantial improvement in the quality of the synthesized programs.
最近の研究[87, 133]では、膨大なコード・コーパスを用いてLLMを訓練することで、合成されたプログラムの品質が大幅に向上することがわかっている。
The generated programs can successfully pass expert-designed unit-test cases [87] or solve competitive programming questions [94].
生成されたプログラムは、専門家が設計した単体テストケース[87]に合格したり、競争的なプログラミング問題[94]を解いたりすることができる。
In general, two types of code corpora are commonly used for pre-training LLMs.
一般に、LLMの事前学習には2種類のコード・コーパスが使用される。
The first source is from programming question answering communities like Stack Exchange [134, 135].
最初のソースは、Stack Exchange [134, 135]のようなプログラミングの質問回答コミュニティである。
The second source is from public software repositories such as GitHub [87, 133, 76], where code data (including comments and docstrings) are collected for utilization.
2つ目のソースは、GitHub [87, 133, 76]のような公開ソフトウェアリポジトリで、コードデータ（コメントやdocstringsを含む）が収集され、活用されている。
Compared to natural language text, code is in the format of a programming language, corresponding to long-range dependencies and accurate execution logic [136].
自然言語のテキストと比較して、コードはプログラミング言語の形式であり、長距離の依存関係と正確な実行ロジックに対応している[136]。
A recent study [47] also speculates that training on code might be a source of complex reasoning abilities (e.g., chain-of-thought ability [33]).
最近の研究[47]では、コードに関する訓練が複雑な推論能力（例えば、思考連鎖能力[33]）の源になるかもしれないとも推測している。
Besides, it has been shown that formatting reasoning tasks into code can help LLMs generate more accurate results [136, 137].
さらに、推論タスクをコードにフォーマットすることで、LLMがより正確な結果を生成できることが示されている[136, 137]。

### Data Preprocessing データの前処理

After collecting a large amount of text data, it is essential to preprocess it for constructing the pre-training corpus, especially removing noisy, redundant, irrelevant, and potentially toxic data [59, 56], which may largely affect the capacity and performance of LLMs.
大量のテキストデータを収集した後は、事前学習コーパスを構築するための前処理が不可欠であり、特に、LLMの能力と性能に大きな影響を与える可能性のある、ノイズの多い、冗長な、無関係な、潜在的に有害なデータを除去する [59, 56]。
In this part, we review the detailed data preprocessing strategies to improve the quality of the collected data [59, 93, 66].
このパートでは、収集したデータの質を向上させるための詳細なデータ前処理戦略をレビューする[59, 93, 66]。
A typical pipeline of preprocessing the pre-training data for LLMs has been illustrated in Figure 3.
LLMの事前学習データの典型的な前処理パイプラインを図3に示す。

Quality Filtering.
クオリティ・フィルタリング。
To remove low-quality data from the collected corpus, existing work generally adopts two approaches: (1) classifier-based, and (2) heuristic-based.
収集されたコーパスから低品質なデータを除去するために、既存の研究では一般的に2つのアプローチが採用されている： (1)分類器ベース、(2)ヒューリスティックベース。
The former approach trains a selection classifier based on high-quality texts and leverages it to identify and filter out low-quality data.
前者のアプローチでは、高品質のテキストに基づいて選択分類器を訓練し、それを活用して低品質のデータを識別してフィルタリングする。
Typically, these methods [55, 93, 56] train a binary classifier with well-curated data (e.g., Wikipedia pages) as positive instances and sample candidate data as negative instances, and predict the score that measures the quality of each data example.
一般的に、これらの手法[55, 93, 56]は、十分にキュレーションされたデータ（例えばウィキペディアのページ）を正インスタンス、サンプル候補データを負インスタンスとして二値分類器を学習し、各データ例の品質を測定するスコアを予測する。
However, several studies [93, 59] also find that a classifier-based approach may result in the unintentional removal of high-quality texts in dialectal, colloquial, and sociolectal languages, which potentially leads to bias in the pre-training corpus and diminishes the corpus diversity.
しかし、いくつかの研究[93, 59]では、分類器ベースのアプローチでは、方言、口語、社会方言の言語における質の高いテキストが意図せず削除される可能性があり、これが事前学習コーパスに偏りをもたらし、コーパスの多様性を低下させる可能性があるとしています。
As the second approach, several studies, such as BLOOM [66] and Gopher [59], employ heuristic-based approaches to eliminate low-quality texts through a set of well-designed rules, which can be summarized as follows:
2番目のアプローチとして、BLOOM [66]やGopher [59]などのいくつかの研究では、よく設計されたルールのセットを通じて低品質のテキストを排除するために、ヒューリスティックに基づくアプローチを採用しています：

• Language filtering.

- 言語フィルタリング。
  If a LLM would be mainly used in the tasks of certain languages, the text in other languages can be filtered.
  LLMが主に特定の言語のタスクで使用される場合、他の言語のテキストをフィルタリングすることができます。

• Metric filtering.

- メトリックフィルタリング。
  Evaluation metrics about the generated texts, e.g., perplexity, can be employed to detect and remove unnatural sentences.
  生成されたテキストに関する評価指標（例えば、perplexity）は、不自然な文章を検出して削除するために採用することができる。

• Statistic filtering.

- 統計フィルタリング。
  Statistical features of a corpus, e.g., the punctuation distribution, symbol-to-word ratio, and sentence length, can be utilized to measure the text quality and filter the low-quality data.
  コーパスの統計的特徴、例えば句読点の分布、記号と単語の比率、文の長さなどを利用して、テキストの品質を測定し、低品質なデータをフィルタリングすることができる。

• Keyword filtering.

- キーワードフィルタリング。
  Based on specific keyword set, the noisy or unuseful elements in the text, such as HTML tags, hyperlinks, boilerplates, and offensive words, can be identified and removed.
  特定のキーワードセットに基づいて、HTMLタグ、ハイパーリンク、定型文、不快な言葉など、テキスト内のノイズや不用な要素を特定し、削除することができる。

De-duplication.
重複排除。
Existing work [138] has found that duplicate data in a corpus would reduce the diversity of language models, which may cause the training process unstable and thus affect the model performance.
既存の研究[138]では、コーパス内の重複データが言語モデルの多様性を低下させ、学習プロセスが不安定になり、モデルの性能に影響を与える可能性があることが分かっている。
Therefore, it is necessary to de-duplicate the pre-training corpus.
したがって、事前学習コーパスの重複を取り除く必要がある。
Specially, de-duplication can be performed at different granularities, including sentence-level, document-level, and dataset-level de-duplication.
特に重複排除は、文レベル、文書レベル、データセットレベルなど異なる粒度で実行できる。
First, low-quality sentences that contain repeated words and phrases should be removed, as they may introduce repetitive patterns in language modeling [139].
まず、繰り返される単語やフレーズを含む低品質な文章は、言語モデリングに繰り返しパターンを導入する可能性があるため、削除する必要がある[139]。
At the document level, existing studies mostly rely on the overlap ratio of surface features (e.g., words and
文書レベルでは、既存の研究のほとんどは、表層的特徴（例えば、単語と

�
�

-grams overlap) between documents to detect and remove duplicate documents containing similar contents [59, 57, 66, 140].
-gramの重複）を検出し、類似した内容を含む重複文書を削除する[59, 57, 66, 140]。
Furthermore, to avoid the dataset contamination problem, it is also crucial to prevent the overlap between the training and evaluation sets [56], by removing the possible duplicate texts from the training set.
さらに、データセット汚染の問題を回避するためには、訓練セットから重複する可能性のあるテキストを削除することで、訓練セットと評価セットの重複を防ぐことも重要である[56]。
It has been shown that the three levels of de-duplication are useful to improve the training of LLMs [141, 56], which should be jointly used in practice.
重複排除の3つのレベルは、LLMのトレーニングを改善するのに有効であることが示されており[141, 56]、これらは実際に共同で使用されるべきである。

Privacy Redaction.
プライバシーの再編集。
The majority of pre-training text data is obtained from web sources, including user-generated content involving sensitive or personal information, which may increase the risk of privacy breaches [142].
学習前テキストデータの大部分は、機密情報や個人情報を含むユーザー生成コンテンツを含むウェブソースから取得されるため、プライバシー侵害のリスクが高まる可能性がある[142]。
Thus, it is necessary to remove the personally identifiable information (PII) from the pre-training corpus.
したがって、学習前のコーパスから個人を特定できる情報（PII）を取り除く必要がある。
One direct and effective approach is to employ rule-based methods, such as keyword spotting, to detect and remove PII such as names, addresses, and phone numbers [109].
直接的で効果的なアプローチの1つは、キーワードスポッティングのようなルールベースの方法を採用して、名前、住所、電話番号などのPIIを検出して除去することである[109]。
Furthermore, researchers also find that the vulnerability of LLMs under privacy attacks can be attributed to the presence of duplicate PII data in the pre-training corpus [143].
さらに研究者は、プライバシー攻撃におけるLLMの脆弱性は、事前学習コーパスに重複したPIIデータが存在することに起因することも発見している[143]。
Therefore, de-duplication can also reduce privacy risks to some extent.
したがって、重複排除はプライバシーリスクをある程度軽減することもできる。

Tokenization.
トークン化。
Tokenization is also a crucial step for data preprocessing.
トークン化もデータ前処理の重要なステップである。
It aims to segment raw text into sequences of individual tokens, which are subsequently used as the inputs of LLMs.
これは生テキストを個々のトークンのシーケンスに分割することを目的とし、その後LLMの入力として使用される。
Although it is expedient to leverage an existing tokenizer (e.g., OPT [79] and GPT-3 [55] utilize the tokenizer of GPT-2 [26]), using a tokenizer specially designed for the pre-training corpus can be highly beneficial [66], especially for the corpus that consists of diverse domains, languages, and formats.
既存のトークナイザを利用するのが便利ですが（例えば、OPT [79]やGPT-3 [55]はGPT-2 [26]のトークナイザを利用しています）、事前学習コーパスのために特別に設計されたトークナイザを使用することは、特に多様なドメイン、言語、フォーマットからなるコーパスの場合、非常に有益です[66]。
Therefore, several recent LLMs train the customized tokenizers specially for the pre-training corpus with SentencePiece [144].
そのため、最近のLLMのいくつかは、SentencePiece [144]を使って、事前学習コーパスに特化してカスタマイズされたトークナイザを学習している。
The byte-level Byte Pair Encoding (BPE) algorithm [145] is utilized to ensure that the information after tokenization is lossless [56, 59].
バイトレベルのバイトペアエンコーディング（BPE）アルゴリズム[145]は、トークン化後の情報がロスレスであることを保証するために利用される[56, 59]。
Notably, normalization techniques in BPE, such as NFKC [146], may even degrade the tokenization performance [34, 59, 66].
特に、NFKC [146]のようなBPEにおける正規化技術は、トークン化のパフォーマンスを低下させる可能性さえある[34, 59, 66]。

### Effect of Pre-training Data on LLMs LLMに対する事前学習データの効果

Unlike small-scale PLMs, it is usually infeasible to iterate the pre-training of LLMs multiple times, due to the huge demand for computational resources.
小規模なPLMとは異なり、LLMの事前学習を何度も繰り返すことは、計算資源が膨大になるため、通常は不可能である。
Thus, it is particularly important to construct a well-prepared pre-training corpus before training a LLM.
したがって、LLMを訓練する前に、十分に準備された事前訓練コーパスを構築することが特に重要である。
In this part, we discuss how the quality and distribution of the pre-training corpus potentially influence the performance of LLMs.
このパートでは、事前学習コーパスの質と分布がLLMの性能にどのような影響を与える可能性があるかについて議論する。

Mixture of Sources.
ソースの混合。
As discussed before, pre-training data from different domains or scenarios has distinct linguistic characteristics or semantic knowledge.
前述したように、異なるドメインやシナリオからの事前学習データは、明確な言語的特徴や意味的知識を持っている。
By pre-training on a mixture of text data from diverse sources, LLMs can acquire a broad scope of knowledge and may exhibit a strong generalization capacity.
多様なソースからのテキストデータを混合して事前学習することで、LLMは幅広い知識を獲得し、強力な汎化能力を示すことができる。
When mixing different sources, one needs to carefully set the distribution of pre-training data, since it is also likely to affect the performance of LLMs on downstream tasks [59].
異なるソースを混合する場合、下流タスクにおけるLLMのパフォーマンスにも影響する可能性が高いため、事前学習データの分布を慎重に設定する必要がある[59]。
Gopher [59] conducts the ablation experiment on data distribution to examine the impact of mixed sources on downstream tasks.
Gopher [59]は、混合ソースが下流タスクに与える影響を調べるために、データ分布に関するアブレーション実験を実施している。
Experimental results on the LAMBADA dataset [147] show that increasing the proportion of books data can improve the capacity of the model in capturing long-term dependencies from text, and increasing the proportion of the C4 dataset [71] leads to performance improvement on the C4 validation dataset [59].
LAMBADAデータセット[147]での実験結果によると、書籍データの割合を増やすことで、テキストから長期的な依存関係を捉えるモデルの能力が向上し、C4データセット[71]の割合を増やすことで、C4検証データセット[59]での性能が向上する。
While, as a side effect, training on excessive data about a certain domain would affect the generalization capability of LLMs on other domains [35, 59].
一方、副次的な効果として、特定のドメインに関する過剰なデータで学習すると、他のドメインにおけるLLMの汎化能力に影響を与える[35, 59]。
Therefore, it is suggested that researchers should carefully determine the proportion of data from different domains in the pre-training corpus, in order to develop LLMs that better meet their specific needs.
従って、研究者は、特定のニーズをよりよく満たすLLMを開発するために、事前訓練コーパスに含まれる異なるドメインからのデータの割合を注意深く決定すべきであることが示唆される。
The readers can refer to Figure 2 for a comparison of the data sources for different LLMs.
異なるLLMのデータソースの比較については、図2を参照されたい。

Amount of Pre-training Data.
プレトレーニングデータの量。
For pre-training an effective LLM, it is important to collect sufficient high-quality data that satisfies the data quantity demand of the LLM.
効果的なLLMを事前に訓練するためには、LLMのデータ量の要求を満たす十分な高品質のデータを収集することが重要である。
Existing studies have found that with the increasing parameter scale in the LLM, more data is also required to train the model [57, 34]: a similar scaling law as model size is also observed in data size, with respect to model performance.
既存の研究では、LLMのパラメータ・スケールが大きくなるにつれて、モデルの訓練に必要なデータ量も多くなることがわかっている[57, 34]： モデル・サイズと同様のスケーリング則が、モデルの性能に関するデータ・サイズでも観察される。
Chinchilla [34] demonstrates that a number of existing LLMs suffer from sub-optimal training due to inadequate pre-training data.
Chinchilla [34]は、既存のLLMの多くが、事前学習データが不十分なために最適な学習が行われていないことを実証している。
By conducting extensive experiments, it further shows that it is necessary to adopt equal scales of the model parameters and training tokens for a given compute budget.
広範な実験を行うことで、与えられた計算予算に対して、モデルパラメータとトレーニングトークンのスケールを等しくする必要があることが示された。
More recently, LLaMA [57] shows that with more data and longer training, smaller models can also achieve good performance.
より最近では、LLaMA [57]が、より多くのデータと長時間の学習により、より小さなモデルでも良好な性能を達成できることを示している。
Therefore, it is suggested that researchers should pay more attention to the amount of high-quality data for adequately training the model, especially when scaling the model parameters.
したがって、研究者はモデルを適切に訓練するために、特にモデルのパラメータをスケーリングする際に、高品質なデータの量にもっと注意を払うべきであることが示唆される。

Quality of Pre-training Data.
事前トレーニングデータの質。
Existing work has shown that pre-training on the low-quality corpus, such as noisy, toxic, and duplicate data, may hurt the performance of models [59, 140, 143, 138].
既存の研究では、ノイズの多いデータや有害なデータ、重複したデータなど、質の低いコーパスで事前学習を行うと、モデルの性能が低下する可能性があることが示されている[59, 140, 143, 138]。
For developing a well-performing LLM, it is crucial to consider not only the quantity but also the quality of the collected training data.
高性能なLLMを開発するためには、収集した訓練データの量だけでなく質も考慮することが極めて重要である。
Recent studies, such as T5 [71], GLaM [93], and Gopher [59], have investigated the influence of data quality on the performance of downstream tasks.
T5 [71]、GLaM [93]、Gopher [59]などの最近の研究では、データ品質が下流タスクのパフォーマンスに与える影響を調査している。
By comparing the performances of models trained on the filtered and unfiltered corpus, they reach the same conclusion that pre-training LMs on cleaned data can improve the model performance.
フィルタリングされたコーパスとフィルタリングされていないコーパスで学習したモデルの性能を比較することで、LMを清浄化されたデータで事前学習することで、モデルの性能を向上させることができるという同じ結論に達した。
More specifically, the duplication of data may result in the “double descent” (referring to the phenomenon of performance initially deteriorating and subsequently improving) [138, 148], or even overwhelm the training process [138].
より具体的には、データの重複は、「二重降下」（最初はパフォーマンスが悪化し、その後改善される現象を指す）[138, 148]を引き起こす可能性があり、あるいは学習プロセスを圧迫する可能性さえある[138]。
Besides, it has been shown that duplicate data degrades the ability of LLMs to copy from the context, which might further affect the generalization capacity of LLMs using in-context learning [138].
その上、重複データがLLMの文脈からのコピー能力を低下させることが示されており、これは文脈内学習を用いたLLMの汎化能力にさらに影響を与える可能性がある[138]。
Therefore, as suggested in existing work [59, 66, 56], it is essential to incorporate preprocessing methods on the pre-training corpus carefully (as illustrated in Section 4.1.2), to improve stability of the training process and avoid affecting the model performance.
したがって、既存の研究[59, 66, 56]で示唆されているように、（セクション4.1.2で説明されているように）学習前のコーパスに慎重に前処理法を組み込むことが、学習プロセスの安定性を向上させ、モデルの性能に影響を与えないために不可欠である。

## Architecture

In this section, we review the architecture design of LLMs, i.e., mainstream architecture, pre-training objective, and detailed configuration.
このセクションでは、LLMのアーキテクチャ設計、すなわち主流アーキテクチャ、事前学習目的、および詳細設定についてレビューする。
Table III presents the model cards of several representative LLMs with public details.
表IIIは、いくつかの代表的なLLMのモデルカードを、公開されている詳細とともに示している。

### Mainstream Architectures 主流アーキテクチャ

Due to the excellent parallelizability and capacity, the Transformer architecture [22] has become the de facto backbone to develop various LLMs, making it possible to scale language models to hundreds or thousands of billions of parameters.
優れた並列性とキャパシティにより、Transformerアーキテクチャ[22]は、様々なLLMを開発するための事実上のバックボーンとなっており、言語モデルを数百から数千の数十億パラメータにまで拡張することを可能にしている。
In general, the mainstream architectures of existing LLMs can be roughly categorized into three major types, namely encoder-decoder, casual decoder, and prefix decoder.
一般に、既存のLLMの主流アーキテクチャは、エンコーダーデコーダー、カジュアルデコーダー、プレフィックスデコーダーの3種類に大別できる。

Encoder-decoder Architecture.
エンコーダー・デコーダーのアーキテクチャ。
The vanilla Transformer model is built on the encoder-decoder architecture [22], which consists of two stacks of Transformer blocks as the encoder and decoder, respectively.
バニラTransformerモデルは、エンコーダーデコーダーアーキテクチャ[22]に基づいて構築されており、それぞれエンコーダーとデコーダーとしてTransformerブロックの2つのスタックで構成されている。
The encoder adopts stacked multi-head self-attention layers to encode the input sequence for generating its latent representations, while the decoder performs cross-attention on these representations and autoregressively generates the target sequence.
エンコーダは、潜在的な表現を生成するために、入力シーケンスを符号化するためのスタック型マルチヘッド自己注意層を採用し、デコーダは、これらの表現に対して交差注意を実行し、自己回帰的にターゲットシーケンスを生成する。
Encoder-decoder PLMs (e.g., T5 [71] and BART [24]) have shown effectiveness on a variety of NLP tasks.
エンコーダー・デコーダーPLM（T5 [71]やBART [24]など）は、さまざまな自然言語処理タスクで有効性を示してきた。
So far, there are only a small number of LLMs that are built based on the encoder-decoder architecture, e.g., Flan-T5 [81].
これまでのところ、エンコーダー・デコーダー・アーキテクチャーに基づいて構築されたLLMは、Flan-T5 [81]など少数しかない。
We leave a detailed discussion about the architecture selection in Section 4.2.4.
アーキテクチャの選択に関する詳細な議論はセクション4.2.4に譲る。

Casual Decoder Architecture.
カジュアル・デコーダー・アーキテクチャ。
The casual decoder architecture incorporates the uni-directional attention mask, to guarantee that each input token can only attend to the past tokens and itself.
カジュアル・デコーダーのアーキテクチャは、各入力トークンが過去のトークンとそれ自身にしかアテンションできないことを保証するために、単一方向のアテンション・マスクを組み込んでいる。
The input and output tokens are processed in the same fashion through the decoder.
入力トークンと出力トークンは、デコーダーを通して同じように処理される。
As representative language models of this architecture, the GPT-series models [110, 26, 55] are developed based on the casual-decoder architecture.
このアーキテクチャの代表的な言語モデルとして、カジュアル・デコーダ・アーキテクチャをベースに開発されたGPTシリーズ[110, 26, 55]がある。
In particular, GPT-3 [55] has successfully demonstrated the effectiveness of this architecture, also showing an amazing in-context learning capability of LLMs.
特にGPT-3 [55]は、このアーキテクチャの有効性を見事に実証し、LLMの驚くべき文脈内学習能力も示している。
Interestingly, GPT-1 [110] and GPT-2 [26] do not exhibit such superior abilities as those in GPT-3, and it seems that scaling plays an important role in increasing the model capacity of this model architecture.
興味深いことに、GPT-1 [110]とGPT-2 [26]はGPT-3のような優れた能力を示しておらず、スケーリングがこのモデル・アーキテクチャのモデル能力を高める上で重要な役割を果たしているようだ。
So far, the casual decoders have been widely adopted as the architecture of LLMs by various existing LLMs, such as OPT [79], BLOOM [66], and Gopher [59].
これまでのところ、カジュアル・デコーダは、OPT [79]、BLOOM [66]、Gopher [59]など、さまざまな既存のLLMでLLMのアーキテクチャとして広く採用されている。
Note that both the casual decoder and prefix decoder discussed next belong to decoder-only architectures.
次に説明するカジュアルデコーダとプレフィックスデコーダは、どちらもデコーダのみのアーキテクチャに属することに注意されたい。
While, when mentioning “decoder-only architecture”, it mainly refers to the casual decoder architecture in existing literature, unless specified.
一方、「デコーダのみのアーキテクチャ」という場合は、特に断りがない限り、主に既存の文献にあるカジュアルなデコーダ・アーキテクチャを指す。

Prefix Decoder Architecture.
プレフィックス・デコーダーのアーキテクチャ。
The prefix decoder architecture (a.k.a., non-casual decoder [149]) revises the masking mechanism of casual decoders, to enable performing bidirectional attention over the prefix tokens [150] and unidirectional attention only on generated tokens.
接頭辞デコーダアーキテクチャ（別名、非カジュアルデコーダ[149]）は、カジュアルデコーダのマスキングメカニズムを修正し、接頭辞トークンに対する双方向の注意[150]と、生成されたトークンに対する一方向の注意のみを実行できるようにしたものである。
In this way, like the encoder-decoder architecture, the prefix decoders can bidirectionally encode the prefix sequence and autoregressively predict the output tokens one by one, where the same parameters are shared during encoding and decoding.
このように、エンコーダ・デコーダのアーキテクチャと同様に、プレフィックスデコーダはプレフィックス列を双方向にエンコードし、出力トークンを1つずつ自己回帰的に予測することができる。
Instead of pre-training from scratch, a practical suggestion is to continually train casual decoders and then convert them into prefix decoders for accelerating convergence [29], e.g., U-PaLM [97] is derived from PaLM [56].
例えば、U-PaLM [97]はPaLM [56]から派生している。
Existing representative LLMs based on prefix decoders include GLM-130B [80] and U-PaLM [97].
プレフィックスデコーダーに基づく既存の代表的なLLMには、GLM-130B [80]とU-PaLM [97]がある。

For the three types of architectures, we can also consider extending them via the mixture-of-experts (MoE) scaling, in which a subset of neural network weights for each input are sparsely activated, e.g., Switch Transformer [25] and GLaM [93].
この3種類のアーキテクチャについては、MoE（mixture-of-experts）スケーリングによって拡張することも検討できる。
It has been shown that substantial performance improvement can be observed by increasing either the number of experts or the total parameter size [151].
エキスパートの数を増やすか、パラメー タのサイズを大きくすることで、大幅な性能向上が見られることが示されている [151]。

### Detailed Configuration 詳細設定

Since the launch of Transformer [22], various improvements have been proposed to enhance its training stability, performance, and computational efficiency.
Transformer[22]が発表されて以来、そのトレーニングの安定性、パフォーマンス、計算効率を高めるために様々な改良が提案されてきた。
In this part, we will discuss the corresponding configurations for four major parts of the Transformer, including normalization, position embeddings, activation functions, attention, and bias.
このパートでは、正規化、位置埋め込み、活性化関数、注意、バイアスなど、Transformerの4つの主要な部分に対応する構成について説明する。

Normalization.
ノーマライゼーション。
Training instability is a challenging issue for pre-training LLMs.
トレーニングの不安定さは、トレーニング前のLLMにとって難しい問題である。
To alleviate this problem, layer normalization (Layer Norm, LN) [152] is widely employed in Transformer architectures.
この問題を軽減するために、レイヤー正規化（Layer Norm、LN）[152]がTransformerアーキテクチャで広く採用されている。
The position of LN is vital to the performance of LLMs.
LNのポジションはLLMのパフォーマンスにとって極めて重要である。
While the initial Transformer [22] uses post-LN, most LLMs employ pre-LN for more stable training in spite of decreasing performance [153].
初期Transformer[22]はpost-LNを使用しているが、ほとんどのLLMは、性能は低下するものの、より安定した学習のためにpre-LNを採用している[153]。
Based on pre-LN, Sandwich-LN [154] adds extra LN before the residual connections to avoid value explosion.
pre-LNに基づき、Sandwich-LN [154]は、値の爆発を避けるために、残余接続の前に余分なLNを追加する。
However, it has been found that Sandwich-LN sometimes fails to stabilize the training of LLMs and may lead to the collapse of training [80].
しかし、Sandwich-LNはLLMの学習を安定させることができず、学習が破綻することがあることが分かっている[80]。
Recently, several advanced normalization techniques have been proposed as alternatives to LN.
近年、LNに代わる高度な正規化技術がいくつか提案されている。
In Gopher [59] and Chinchilla [34], RMS Norm [155] is employed due to its superiority in training speed and performance [156].
Gopher[59]とChinchilla[34]では、RMS Norm[155]がトレーニングのスピードとパフォーマンスに優れているため採用されている[156]。
Compared with LN, DeepNorm [157] has shown a better capability to ensure the stability in training, which has been adopted by GLM-130B with post normalization.
LNと比較して、DeepNorm[157]は学習時の安定性を確保する優れた能力を示しており、これはGLM-130Bにポスト正規化で採用されている。
In addition, adding an extra LN after the embedding layer can also stabilize the training of LLMs.
さらに、埋め込み層の後にLNを追加することで、LLMの学習を安定させることもできる。
However, it tends to incur a significant performance drop [158], which has been removed in several recent LLMs [66].
しかし、この方法では性能が著しく低下する傾向があり [158]、最近のいくつかのLLM [66]では除去されている。

Activation Functions.
活性化機能。
To obtain good performance, activation functions also need to be properly set in feed-forward networks.
良好なパフォーマンスを得るためには、フィードフォワードネットワークでも活性化関数を適切に設定する必要がある。
In existing LLMs, GeLU activations [159] are widely used.
既存のLLMでは、GeLUアクティベーション[159]が広く使われている。
Besides, in the latest LLMs (e.g., PaLM and LaMDA), variants of GLU activation [160, 161] have also been utilized, especially the SwiGLU and GeGLU variants, which often achieve better performance in practice [156].
さらに、最新のLLM（PaLMやLaMDAなど）では、GLU活性化の変種[160, 161]も利用されており、特にSwiGLUとGeGLUの変種は、しばしば実際により良い性能を達成している[156]。
However, compared with GeLU, they require extra parameters (about 50%) in the feed-forward networks [158].
しかし、GeLUと比較すると、フィード・フォワード・ネットワークに余分なパラメータ（約50％）を必要とする[158]。

Position Embeddings.
ポジションの埋め込み。
Since the self-attention modules in Transformer are permutation equivariant, position embeddings are employed to inject absolute or relative position information for modeling sequences.
Transformerの自己アテンションモジュールは順列等変であるため、シーケンスのモデリングのために絶対位置または相対位置情報を注入するために位置埋め込みが採用される。
There are two variants of absolute position embeddings in the vanilla Transformer [22], i.e., sinusoids and learned position embeddings, where the latter is commonly employed in LLMs.
バニラトランスフォーマー[22]における絶対位置埋め込みには、正弦波と学習位置埋め込みの2種類があり、後者はLLMで一般的に採用されている。
Unlike absolute position embeddings, relative positional encodings generate embeddings according to the offsets between keys and queries [71], so it can perform well on sequences longer than those it has seen during training, i.e., extrapolation [162].
絶対位置埋め込みとは異なり、相対位置埋め込みは、キーとクエリ間のオフセットに従って埋め込みを生成する[71]。
ALiBi [162] biases attention scores using a penalty based on the distance between keys and queries.
ALiBi[162]は、キーとクエリ間の距離に基づくペナルティを使用して、アテンションスコアに偏りを持たせている。
Empirical results have shown that it has better zero-shot generalization with a stronger extrapolation capacity than other position embeddings [29].
経験的な結果は、他の位置埋め込みよりも強力な外挿能力を持つ優れたゼロショット汎化であることを示している[29]。
Besides, by setting specific rotatory matrices based on the absolute position, the scores between keys and queries in RoPE [163] can be computed with relative position information, which is useful to model long sequences.
さらに、絶対位置に基づいて特定の回転行列を設定することで、RoPE [163]におけるキーとクエリ間のスコアを相対位置情報で計算することができ、これは長いシーケンスをモデル化するのに有用である。
As a result, RoPE has been widely adopted in several latest LLMs [56, 57, 80]
その結果、RoPEはいくつかの最新のLLMで広く採用されている[56, 57, 80]。

Attention and Bias.
注意とバイアス。
Beyond the full self-attention in the original Transformer [22], sparse attention with lower computation complexity is employed in GPT-3 (i.e., Factorized Attention [164, 55]).
オリジナルのTransformer[22]における完全な自己注意を超えて、GPT-3では、より計算複雑度の低い疎な注意（すなわち、因子化された注意[164, 55]）が採用されている。
In order to effectively and efficiently model longer sequences, more attempts have been made by either introducing special attention patterns [165, 166] or considering GPU memory access (i.e., FlashAttention [167]).
より長いシーケンスを効果的かつ効率的にモデル化するために、特別なアテンションパターン[165, 166]を導入するか、GPUメモリアクセス（すなわち、FlashAttention[167]）を考慮することで、より多くの試みがなされている。
Besides, following the original Transformer, most LLMs keep the biases in each dense kernel and Layer Norm.
さらに、オリジナルのTransformerに従って、ほとんどのLLMは、各密カーネルとレイヤー・ノームのバイアスを保持する。
However, in PaLM [56] and Galactica [35], biases are removed.
しかし、PaLM [56]とGalactica [35]では、バイアスが取り除かれている。
It demonstrates that no biases can enhance training stability for LLMs [56].
これは、バイアスをかけないことでLLMのトレーニングの安定性を高めることができることを示している[56]。

To put all these discussions together, we summarize the suggestions from existing literature for detailed configuration.
これらの議論をまとめるために、詳細なコンフィギュレーションに関する既存文献からの提案を要約する。
For stronger generalization and training stability, it is suggested to choose the pre RMS Norm for layer normalization, and SwiGLU or GeGLU as the activation function.
より強力な汎化と学習の安定性を得るためには、層の正規化にpre RMS Normを、活性化関数にSwiGLUまたはGeGLUを選択することが推奨される。
While, Layer Norm may not be used immediately after embedding layers, which is likely to incur performance degradation.
一方、レイヤー・ノームは、レイヤーを埋め込んだ直後には使用されない可能性があり、パフォーマンスの低下を招く可能性が高い。
Besides, as for position embeddings, RoPE or ALiBi is a better choice since it performs better on long sequences.
また、位置埋め込みに関しては、RoPEやALiBiの方が、長いシーケンスに対してより良いパフォーマンスを発揮するので、より良い選択である。

### Pre-training Tasks トレーニング前の課題

Pre-training plays a key role that encodes general knowledge from large-scale corpus into the massive model parameters.
事前学習は、大規模なコーパスからの一般的な知識を大規模なモデルパラメータに符号化する重要な役割を果たす。
For training LLMs, there are two commonly used pre-training tasks, namely language modeling and denoising autoencoding.
LLMの学習には、言語モデリングとノイズ除去自動エンコーディングという2つの一般的な事前学習タスクがある。
Language Modeling.
言語モデリング。
The language modeling task (LM) is the most commonly used objective to pre-train decoder-only LLMs, e.g., GPT3 [55] and PaLM [56].
言語モデリングタスク(LM)は、GPT3[55]やPaLM[56]などのデコーダのみのLLMの事前学習に最もよく使われる目的である。
Given a sequence of tokens 𝐱 = { � 1 , … , � � } , the LM task aims to autoregressively predict the target tokens � � based on the preceding tokens � < � in a sequence.
トークン列 � = { � 1 , ... , � � } が与えられたとき、LM タスクはトークン列の先行トークン � < � に基づいて、ターゲットのトークン � を自己回帰的に予測することを目的とする。LM タスクの目的は、先行するトークン � < � に基づいて、ターゲットのトークン � � を自己回帰的に予測することである。
A general training objective is to maximize the following likelihood:
一般的なトレーニングの目的は、以下の尤度を最大化することである：

$$
\tag{1}
$$

Since most language tasks can be cast as the prediction problem based on the input, these decoder-only LLMs might be potentially advantageous to implicitly learn how to accomplish these tasks in a unified LM way.
ほとんどの言語タスクは、入力に基づく予測問題として扱うことができるため、デコーダのみのLLMは、統一されたLMの方法でこれらのタスクを達成する方法を暗黙的に学習するのに有利な可能性がある。
Some studies have also revealed that decoder-only LLMs can be naturally transferred to certain tasks by autoregressively predicting the next tokens [26, 55], without fine-tuning.
また、デコーダのみのLLMは、微調整を行わなくても、次のトークンを自己回帰的に予測することで、特定のタスクに自然に移行できることを明らかにした研究もある[26, 55]。
An important variant of LM is the prefix language modeling task, which is designed for pre-training models with the prefix decoder architecture.
LMの重要なバリエーションとして、接頭辞言語モデリングタスクがある。これは、接頭辞デコーダアーキテクチャを持つモデルの事前学習用に設計されている。
The tokens within a randomly selected prefix would be not used in computing the loss of prefix language modeling.
ランダムに選択された接頭辞内のトークンは、接頭辞言語モデリングの損失を計算する際には使用されない。
With the same amount of tokens seen during pre-training, prefix language modeling performs slightly worse than language modeling, since fewer tokens in the sequence are involved for model pre-training [29].
事前学習で見たトークンの量が同じ場合、モデルの事前学習に関わるシーケンスのトークンの数が少ないため、前置詞言語モデリングは言語モデリングよりも若干性能が悪くなる[29]。
Denoising Autoencoding.
デノイジング オートエンコーディング
Besides conventional LM, the denoising autoencoding task (DAE) has also been widely used to pre-train language models [24, 71].
従来のLMの他に、ノイズ除去自動符号化タスク（DAE）も言語モデルの事前学習に広く使われている[24, 71]。
The inputs 𝐱 \ 𝐱 ~ for DAE task are corrupted text with randomly replaced spans.
DAEタスクの入力↪L_1D431↩~は、スパンがランダムに置換された破損テキストである。
Then, the language models are trained to recover the replaced tokens 𝐱 ~ .
次に、置換されたトークン𝐱 ～を復元するために言語モデルを学習する。
Formally, the training objective of DAE is denoted as follows:
正式には、DAEの訓練目的は以下のように示される：

$$
\tag{2}
$$

However, the DAE task seems to be more complicated in implementation than LM task.
しかし、DAEタスクはLMタスクよりも実装が複雑なようだ。
As a result, it has not been widely used to pre-train large language models.
そのため、大規模な言語モデルの事前学習にはあまり使われてこなかった。
Existing LLMs that take DAE as pre-training objectives include T5 [71] and GLM-130B [80].
DAEを事前学習目標とする既存のLLMには、T5 [71]とGLM-130B [80]がある。
These models are mainly trained to recover the replaced spans in an autoregressive way.
これらのモデルは主に自己回帰的に置き換えられたスパンを回復するように訓練される。

### Summary and Discussion まとめと考察

The choice of architecture and pre-training tasks may incur different inductive biases for LLMs, which would lead to different model capacities.
アーキテクチャと事前学習タスクの選択によって、LLMの誘導バイアスが異なり、モデルの能力が異なる可能性がある。
In this part, we summarize some important findings or discussions in the existing literature on this issue.
このパートでは、この問題に関する既存の文献におけるいくつかの重要な発見や議論を要約する。

∙
∙

By pre-training with the LM objective, it seems that casual decoder architecture can achieve a superior zero-shot and few-shot generalization capacity.
LM目的語を用いた事前学習により、カジュアルなデコーダ・アーキテクチャは、優れたゼロショット汎化能力と少数ショット汎化能力を達成できるようだ。
Existing research has shown that without multi-task fine-tuning, the casual decoder has better zero-shot performance than other architectures [29].
既存の研究では、マルチタスクの微調整をしなくても、カジュアルデコーダは他のアーキテ クチャよりも優れたゼロショット性能を持つことが示されている[29]。
The success of GPT-3 [55] has demonstrated that the large casual decoder model can be a good few-shot learner.
GPT-3[55]の成功は、大規模なカジュアルデコーダモデルが優れた少数ショット学習器になり得ることを実証した。
In addition, instruction tuning and alignment tuning discussed in Section 5 have been proven to further enhance the capability of large causal decoder models [62, 61, 81].
さらに、セクション5で説明した命令チューニングとアライメントチューニングは、大規模な因果デコーダモデルの能力をさらに高めることが証明されている[62, 61, 81]。

∙
∙

Scaling law has been widely observed in casual decoders.
スケーリング則は、カジュアルデコーダーで広く観察されている。
By scaling the model size, the dataset size, and the total computation, the performance of casual decoders can be substantially improved [30, 55].
モデルサイズ、データセットサイズ、および総計算量をスケーリングすることで、カジュアルデコーダの性能を大幅に向上させることができる[30, 55]。
Thus, it has become an important strategy to increase the model capacity of the casual decoder via scaling.
したがって、スケーリングによってカジュアルデコーダーのモデル容量を増やすことは重要な戦略となっている。
However, more detailed investigation on encoder-decoder models is still lacking, and more efforts are needed to investigate the performance of encoder-decoder models at a large scale.
しかし、エンコーダー・デコーダー・モデルに関するより詳細な調査はまだ不十分であり、大規模なエンコーダー・デコーダー・モデルの性能を調査するためには、さらなる努力が必要である。

More research efforts about the discussions on architectures and pre-training objectives are in need to analyze how the choices of the architecture and pre-training tasks affect the capacity of LLMs, especially for encoder-decoder architectures.
LLM、特にエンコーダ・デコーダ・アーキテクチャの場合、アーキテクチャと事前学習タスクの選択がLLMの能力にどのような影響を与えるかを分析するためには、アーキテクチャと事前学習目的に関する議論についてさらなる研究努力が必要である。
Besides the major architecture, the detailed configuration of LLM is also worth attention, which has been discussed in Section 4.2.2.
主要なアーキテクチャーに加えて、LLMの詳細な構成も注目に値するが、これについてはセクション4.2.2で説明した。

## Model Training モデルトレーニング
