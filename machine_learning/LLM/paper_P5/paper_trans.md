## link リンク

https://arxiv.org/pdf/2203.13366.pdf
https://arxiv.org/pdf/2203.13366.pdf

## title タイトル

Recommendation as Language Processing (RLP): A Unified Pretrain, Personalized Prompt & Predict Paradigm (P5)
言語処理としてのレコメンデーション（RLP）： 統一された事前訓練、パーソナライズされたプロンプトと予測パラダイム（P5）

## abstract 抄録

For a long time, different recommendation tasks typically require designing task-specific architectures and training objectives.
長い間、**様々な推薦タスクは通常、タスク固有のアーキテクチャとトレーニング目標を設計する必要があった**。
As a result, it is hard to transfer the learned knowledge and representations from one task to another, thus restricting the generalization ability of existing recommendation approaches, e.g., a sequential recommendation model can hardly be applied or transferred to a review generation method.
その結果、学習した知識や表現をあるタスクから別のタスクに移行することが難しく、既存の推薦アプローチの汎化能力が制限される。例えば、逐次推薦モデルをレビュー生成手法に適用したり移行したりすることは難しい。
To deal with such issues, considering that language can describe almost anything and language grounding is a powerful medium to represent various problems or tasks, we present a flexible and unified text-to-text paradigm called “Pretrain, Personalized Prompt, and Predict Paradigm” (P5) for recommendation, which unifies various recommendation tasks in a shared framework.
このような問題に対処するために、言語がほとんどのものを記述することができ、言語接地が様々な問題やタスクを表現するための強力な媒体であることを考慮し、我々は、**様々な推薦タスクを共有フレームワークで統一する**、柔軟で統一された推薦のための **"Pretrain, Personalized Prompt, and Predict Paradigm"（P5）**と呼ばれる**text-to-textパラダイム**を提案する。(paradigmはざっくり方法論、みたいなイメージ?)
In P5, all data such as user-item interactions, user descriptions, item metadata, and user reviews are converted to a common format — natural language sequences.
P5では、ユーザとアイテムのインタラクション、ユーザの説明、アイテムのメタデータ、ユーザのレビューなどの**すべてのデータが、共通のフォーマットである自然言語シーケンスに変換**される。
Then, P5 learns to generate personalized recommendations by predicting the next tokens in the sequences.
The rich information from natural language assists P5 to capture deeper semantics for personalization and recommendation.
自然言語からの豊富な情報は、P5がパーソナライゼーションと推薦のためのより深い意味を捉えるのを支援する。
Specifically, P5 learns different tasks with the same language modeling objective during pretraining.
具体的には、P5は事前学習中に同じ言語モデリング目的で異なるタスクを学習する。
Thus, it serves as the foundation model for various downstream recommendation tasks, allows easy integration with other modalities, and enables instruction-based recommendation based on prompts.
そのため、**P5は、さまざまな下流の推薦タスクの基礎モデルとして機能し**、他のmodalitiesとの簡単な統合を可能にし、プロンプトに基づいた指示に基づく推薦を実現する。(ここでmodalityは、他のdomainとかの意味だろうか...??:thinking:)
P5 advances recommender systems from shallow model to deep model to large model, and will revolutionize the technical form of recommender systems towards universal recommendation engine.
P5は、推薦システムを浅いモデルから深いモデル、大規模モデルに進化させ、普遍的な推薦エンジンに向けて推薦システムの技術形態を革命的に変えるだろう。
With adaptive personalized prompt for different users, P5 is able to make predictions in a zero-shot or few-shot manner and largely reduces the necessity for extensive fine-tuning.
さまざまなユーザーに適応的にパーソナライズされたプロンプトにより、P5はゼロショットまたは数ショットで予測を行うことができ、大規模な微調整の必要性を大幅に減らすことができる。
On several recommendation benchmarks, we conduct experiments to show the effectiveness of P5.
いくつかの推薦ベンチマークにおいて、P5の有効性を示す実験を行った。
To help advance future research on Recommendation as Language Processing (RLP), Personalized Foundation Models (PFM), and Universal Recommendation Engine (URE), we release the source code, dataset, prompts, and pretrained P5 model at https://github.com/jeykigung/P5.
Recommendation as Language Processing(RLP, 言語処理としてのレコメンデーション)、Personalized Foundation Models(PFM, パーソナライズされた基礎モデル)、Universal Recommendation Engine(URE, 普遍的な推薦エンジン)に関する将来の研究を進めるために、ソースコード、データセット、プロンプト、事前学習済みP5モデルを公開している。

<!-- ここまで読んだ! -->

# Introduction はじめに

For the past decades, recommender systems have witnessed significant advancements and played an essential role in people’s daily life, helping their micro decisions and fulfilling their demands with outstanding accuracy.
過去数十年にわたり、レコメンダーシステムは著しい進歩を遂げ、人々の日常生活において重要な役割を果たしてきた。優れた精度で人々のマイクロ意思決定を支援し、要求を満たしてきた。
In retrospect, we can summarize the development trend of modern recommender systems – towards a more comprehensive system that accommodates diverse features and a wide spectrum of application scenarios.
振り返ってみると、現代のレコメンダーシステムの発展傾向を要約すると、**多様な特徴と幅広いアプリケーションシナリオに対応する包括的なシステムに向かっている。**(色んなusecaseに対応するgeneralなシステムってこと??)

On one hand, feature engineering and learning in recommender systems has evolved greatly from simple to complex.
一方では、推薦システムにおけるfeature engineeringと学習は、単純から複雑へと大きく進化してきた。
In early ages, recommender systems typically adopt logistic regression or collaborative filtering [25, 35, 50, 52] which utilize user-item interaction records to model users’ behavioral patterns.
初期のレコメンダーシステムでは、**ユーザとアイテムの相互作用レコードを利用してユーザの行動パターンをモデル化する**ロジスティック回帰や協調フィルタリング[25, 35, 50, 52]が一般的であった。(うんうん...!)
Later on, the contextual features such as user profile and item metadata are further integrated into the system through more sophisticated models such as factorization machines [48] and GBDT [20].
その後、因数分解マシン[48]やGBDT[20]のような、**より洗練されたモデルを通じて、ユーザプロファイルやアイテムのメタデータのようなcontextual featuresがシステムにさらに統合された**。(うんうん...!)
Recently, deep neural network models [3, 5, 19, 74] facilitate crossing and combination among even more diverse and sophisticated features.
最近では、ディープニューラルネットワークモデル[3, 5, 19, 74]が、**さらに多様で洗練された特徴量間のcrossingやcombinationを容易にしている**。(うんうん...!) (sequential recommender的な、相互作用レコードの捉え方の洗練の話もあるよね...:thinking:)
As a result, these models gain better representation ability compared with traditional feature engineering based approaches.
その結果、これらのモデルは、従来のfeature engineeringに基づくアプローチと比較して、より優れた表現能力を獲得している。

On the other hand, more recommendation tasks have emerged.
その一方で、より多くの推薦タスクが出現している。
Except for classical rating prediction and direct user-item matchingbased recommendation tasks, recent works are broadening the spectrum to new tasks and scenarios such as sequential recommendation [21, 60, 63, 80], conversational recommendation [8, 61, 76], explainable recommendation [17, 31, 62, 70, 75, 77] and so on.
古典的な評価予測や直接的なユーザアイテムマッチングに基づく推薦タスクに加えて、最近の研究は、**sequential recommendation(逐次推薦)[21, 60, 63, 80]、conversational recommendation(会話型推薦)[8, 61, 76]、explainable recommendation(説明可能な推薦)[17, 31, 62, 70, 75, 77]** などの新しいタスクやシナリオにスペクトルを広げている。
While the approaches to the aforementioned recommendation tasks are often proposed separately, there is an evident trend of utilizing multiple recommendation tasks to jointly learn the transferable representations [31, 56, 57, 72].
前述の推薦タスクへのアプローチは、通常別々に提案されるが、**転送可能な表現を共同で学習するために複数の推薦タスクを利用する傾向が明らかになっている**。(なるほど? これが最初に主張してた「多様な特徴と幅広いアプリケーションシナリオに対応する包括的なシステムに向かっている」という話か...!)
Although existing recommender systems achieved great success, there is still a considerable gap between current solutions and the foreseeable intersection of the aforementioned trends – a comprehensive recommender system that can accommodate diverse features and different types of tasks.
既存の推薦システムは大きな成功を収めているが、現在のソリューションと前述のトレンドの予想される交差点との間には、多様な特徴とさまざまなタイプのタスクに対応できる包括的な推薦システムとの間には、かなりのギャップがある。
Since recommendation tasks usually share a common user–item pool and have overlapping contextual features, we believe it is promising to merge even more recommendation tasks into a unified framework so that they can implicitly transfer knowledge to benefit each other and enable generalization to other unseen tasks.
推薦タスクは通常、共通のユーザ-アイテムプールを共有し、重複するコンテキスト特徴量を持っているため、**さらに多くの推薦タスクを統一されたフレームワークに統合し、それらが互いに利益をもたらすために知識を暗黙的に転送し、他の未見のタスクに汎化することができる**と考えている。(generalizeできるはず、という主張なんだ...!:thinking:)

Inspired by the recent progress in multitask prompt-based training [1, 51, 67], in this work, we propose a unified “Pretrain, Personalized Prompt & Predict Paradigm” (denoted as P5).
マルチタスクプロンプトベーストレーニング[1, 51, 67]の最近の進歩に触発され、本研究では、**統一された「Pretrain, Personalized Prompt & Predict Paradigm」（P5）**を提案する。
We show that P5 is possible to learn multiple recommendation related tasks together through a unified sequence-to-sequence framework by formulating these problems as prompt-based natural language tasks, where user–item information and corresponding features are integrated with personalized prompt templates as model inputs.
P5は、ユーザ-アイテム情報と対応する特徴量が、モデル入力としてパーソナライズされたプロンプトテンプレートと統合された、プロンプトベースの自然言語タスクとしてこれらの問題を定式化することで、統一されたシーケンス-シーケンスフレームワークを通じて複数の推薦関連タスクを一緒に学習することが可能であることを示す。
P5 sheds light on a promising technical route for unified and instruction-based recommendation.
P5は、統一された指導に基づく推薦のための有望な技術的ルートに光を当てる。
It has three main advantages: 1) P5 deeply immerses recommendation models into a full language environment, where all recommendation tasks are reformulated to NLP tasks with the help of personalized prompts.
P5には3つの利点がある： 1)P5は推薦モデルを完全な言語環境に深く浸し、すべての推薦タスクはパーソナライズされたプロンプトの助けを借りてNLPタスクに再定式化される。
Since language grounding is sufficiently flexible and powerful to express various kinds of features in text templates, so there is no need to design feature-specific encoders.
言語接地は、テキストテンプレートで様々な種類の特徴を表現するのに十分柔軟で強力であるため、特徴に特化したエンコーダを設計する必要はない。
As a result, P5 can exploit the abundant semantics and knowledge inside the training corpora; 2) P5 integrates multiple recommendation tasks into a shared textto-text encoder-decoder architecture and trains them with the same language modeling loss rather than designing task-specific architectures and objective functions.
その結果、P5は学習コーパス内の豊富なセマンティクスと知識を利用することができる。2) P5は、タスク固有のアーキテクチャや目的関数を設計するのではなく、複数の推薦タスクを共有のテキスト-テキストエンコーダ-デコーダアーキテクチャに統合し、同じ言語モデリングロスで学習する。
In other words, P5 treats all personalized tasks as a conditional text generation problem; 3) Trained with instruction-based prompts, P5 attains sufficient zero-shot performance when generalizing to novel personalized prompts or unseen items in other domains.
言い換えれば、P5はすべてのパーソナライズされたタスクを条件付きテキスト生成問題として扱う。3) 指示ベースのプロンプトで訓練されたP5は、新規のパーソナライズされたプロンプトや他のドメインの未見のアイテムに汎化する際に、十分なゼロショット性能を達成する。
In our experiments, we study how P5 performs compared with task-specific approaches on all five task families as well as evaluating P5’s zero-shot generalization ability.
実験では、P5のゼロショット汎化能力を評価するだけでなく、5つのタスクファミリーすべてについて、タスク固有のアプローチと比較してP5がどのように機能するかを研究した。
We also conduct several ablation studies to justify the design details of P5 framework.
また、P5フレームワークの設計の詳細を正当化するために、いくつかのアブレーション研究も行っている。
Overall, our main contributions can be outlined as follows: • To the best of our knowledge, this is the first work to propose a unified “Pretrain, Personalized Prompt & Predict Paradigm” which integrates various recommendation related tasks into a shared conditional language generation framework.
全体として、我々の主な貢献は以下のように概説できる： - 我々の知る限り、これは様々な推薦関連タスクを共有条件言語生成フレームワークに統合する、統一された「Pretrain, Personalized Prompt & Predict Paradigm」を提案する最初の研究である。
• We create a collection of personalized prompts that cover five different recommendation task families.

- 私たちは、5つの異なる推薦タスクファミリーをカバーするパーソナライズされたプロンプトのコレクションを作成します。
  • According to the experimental results, P5 achieves promising performances on the five task families when taking seen prompt templates as model inputs.
- 実験結果によると、プロンプトテンプレートをモデル入力とした場合、P5は5つのタスクファミリーで有望な性能を達成した。
  • P5 shows sufficient zero-shot generalization ability for novel personalized prompts and new items in unseen domains.
- P5は、新規のパーソナライズされたプロンプトや、未知の領域における新しいアイテムに対して、十分なゼロショット汎化能力を示す。

# Related Work 関連作品

Unified Frameworks.
統一されたフレームワーク。
Many prior works have pursued to solve various tasks in a unified model.
多くの先行研究が、統一されたモデルで様々なタスクを解決することを追求してきた。
As early pioneers, T5 [47] and GPT3 [2] unifies NLP downstream tasks through text-to-text encoder– decoder framework and autoregressive language modeling, respectively.
初期のパイオニアとして、T5 [47]とGPT3 [2]は、それぞれテキスト-テキストエンコーダー-デコーダーのフレームワークと自己回帰言語モデリングによって、NLPの下流タスクを統合している。
They both allow effective knowledge sharing among different tasks based on a common pretrained language model.
どちらも、共通の事前学習済み言語モデルに基づいて、異なるタスク間で効果的に知識を共有することができる。
Following this trend, recent advances started to focus on unifying large-scale language tasks [1, 51, 67] or cross-modality applications [6, 66, 71] through a shared sequence-to-sequence framework, where different types of tasks and modalities are all expressed in the format of natural language.
この傾向を受け、最近の進歩は、異なるタイプのタスクやモダリティがすべて自然言語のフォーマットで表現される、共有されたシーケンス間のフレームワークを通じて、大規模な言語タスク[1, 51, 67]やクロスモダリティアプリケーション[6, 66, 71]を統一することに焦点を当て始めた。
However, aforementioned methods never consider personalization in their sequence-to-sequence models.
しかし、前述の方法では、配列間モデルにおいてパーソナライゼーションが考慮されることはない。
Recently, a line of work [56, 57, 72] attempt to learn universal user representations which are easily transferrable to downstream tasks.
最近、下流のタスクに容易に移行できる普遍的なユーザー表現を学習しようとする一連の研究 [56, 57, 72] が行われている。
One limitation of these methods is that they still require additional finetuning on downstream datasets.
これらの方法の限界のひとつは、下流のデータセットでさらに微調整が必要なことである。
In contrast, our P5 first takes personalization into an encoder-decoder Transformer model that can generalize to a wide spectrum of recommendation related application scenarios – tasks that naturally require personalization.
対照的に、我々のP5は、まずパーソナライゼーションをエンコーダ・デコーダのトランスフォーマーモデルに取り込み、推薦に関連する幅広いアプリケーションシナリオ（当然パーソナライゼーションを必要とするタスク）に一般化することができる。
Moreover, with the help of prompt-based pretraining, P5 acquires zero-shot generalization ability when transferring to unseen prompts and items.
さらに、プロンプトに基づく事前訓練により、P5は未見のプロンプトやアイテムに移行する際にゼロショット汎化能力を獲得する。

Prompt Learning.
学習を促す。
The success of GPT series especially GPT-3 [2] marked the beginning of prompt’s popularization on NLP tasks.
GPTシリーズ、特にGPT-3 [2]の成功は、NLPタスクにおけるプロンプトの普及の始まりとなった。
Trained with huge language data from the Web, GPT-3 exhibited the capability of solving NLP tasks when provided a number of inputoutput examples as exemplar prompts.
ウェブ上の膨大な言語データを用いて学習したGPT-3は、多くの入出力例を模範的なプロンプトとして提供することで、自然言語処理タスクを解く能力を示した。
Besides exemplar prompts, many prompt design methods have proliferated following the “pretrain, prompt, and predict” paradigm [37].
模範的なプロンプト以外にも、「事前訓練、プロンプト、予測」パラダイム [37]に従って、多くのプロンプト設計手法が普及している。
One type of the methods [16, 23, 36, 40, 58] explored prompt search for proper discrete prompts.
プロンプト探索手法の一種 [16, 23, 36, 40, 58] は、適切な離散プロンプトを探索するものである。
Meanwhile, another line of work [18, 28, 33, 38, 45, 81] exploited continuous vector embeddings as prompts.
一方、別の研究 [18, 28, 33, 38, 45, 81]では、プロンプトとして連続ベクトル埋め込みを利用している。
Compared with the aforementioned prompt types, instruction-based prompts contain detailed task descriptions and adhere more to the natural language format.
前述のプロンプトタイプと比較して、インストラクションベースのプロンプトは、詳細なタスクの説明を含み、より自然言語形式に忠実である。
Since instruction-based prompts are flexible and close to how humans communicate with each other, several pioneer works [11, 68] claim that learning from crowd-sourced NLP datasets is a promising route for general purpose NLP systems.
指示ベースのプロンプトは柔軟性があり、人間同士のコミュニケーション方法に近いため、いくつかの先駆的な研究[11, 68]では、クラウドソーシングされたNLPデータセットからの学習は、汎用NLPシステムの有望なルートであると主張している。
Recent works such as FLAN [67] and T0 [51] finetuned pretrained language models on large-scale NLP datasets verbalized via humanreadable prompts.
FLAN [67]やT0 [51]のような最近の研究は、人間が読むことのできるプロンプトを介して言語化された大規模なNLPデータセット上で事前に訓練された言語モデルを微調整している。
As a result, such multitask prompt-based tuning brings powerful models that exhibit strong zero-shot ability on unseen tasks.
その結果、このようなマルチタスク・プロンプトに基づくチューニングは、未見のタスクに対して強力なゼロショット能力を発揮する強力なモデルをもたらす。
Inspired by the success of these approaches, we create a collection of personalized prompts and then train a sequenceto-sequence model on a variety of recommendation related tasks verbalized according to the constructed personalized prompts.
これらのアプローチの成功に触発され、我々はパーソナライズされたプロンプトのコレクションを作成し、構築されたパーソナライズされたプロンプトに従って言語化された推薦に関連する様々なタスクでシーケンス-シーケンスモデルを訓練する。

NLP for Recommendation.
推薦のためのNLP。
Recommendation has been interacting with NLP techniques for a long time.
レコメンデーションは長い間、NLPテクニックと相互作用してきた。
The main work mostly address four lines of research: 1) explainable recommendation [4, 10, 30–32, 75, 77] where NLP models help generating text explanations for a given recommendation; 2) sequential recommendation as language modeling [9, 60, 80] which considers user interaction histories as word token sequences; 3) text feature extraction [69, 74, 79] which aims to extract informative text encodings that can improve the performance of recommendation; and 4) conversational recommendation [8, 12–14, 22, 61, 76] that reasons the intent of users and gives recommendation in an interactive dialog format.
主な研究テーマは以下の4つである： 1) 説明可能な推薦 [4, 10, 30-32, 75, 77]: NLP モデルが、与えられた推薦に対するテキスト説明を生成するのに役立つ。2) 言語モデリングとしての逐次推薦 [9, 60, 80]: ユーザーとの対話履歴を単語トークン列として考慮する。
In our work, we explicitly covers the tasks of sequential recommendation and explanation generation, and additionally offers insights on how to formulate a unified NLP framework for other recommendation problems including rating prediction, top-k recommendation, and review summarization.
私たちの研究では、逐次推薦と説明生成のタスクを明示的にカバーし、さらに、評価予測、トップk推薦、レビュー要約を含む他の推薦問題のための統一的なNLPフレームワークを策定する方法についての洞察を提供する。
Furthermore, pretrained with instructionbased prompts that share similarity with conversational recommendation, our P5 benefits from the natural language environment and improves the performance on a series of recommendation tasks.
さらに、会話による推薦と類似性を持つ指示ベースのプロンプトで事前に訓練することで、我々のP5は自然言語環境の恩恵を受け、一連の推薦タスクのパフォーマンスを向上させる。
Zero-shot and Cold Start Recommendation.
ゼロ・ショットとコールド・スタートの推奨。
Recommender systems’ performances heavily rely on the available training data, but there are always zero-shot cases where the history records are limited.
レコメンダーシステムの性能は、利用可能な学習データに大きく依存するが、履歴記録が限られているゼロショットのケースは常に存在する。
The evidences of performing well on such startup cases signal a good generalization ability of recommendation models.
このようなスタートアップのケースで良好なパフォーマンスを示したことは、推薦モデルの汎化能力の高さを示している。
One widely studied problem under this setting is the cold-start recommendation where users [26] or items [53] are new to the system with no previous interaction records.
この設定の下で広く研究されている問題の1つは、ユーザー[26]やアイテム[53]が、過去にインタラクションの記録がなく、システムにとって新しいものである場合のコールドスタート推薦である。
Solutions to this problem either learn to model content features [15, 29, 44, 55] so that inference can be made without interaction records or learn to transfer representations from auxiliary domains [42, 56, 59, 72, 82].
この問題に対する解決策は、相互作用の記録がなくても推論ができるように、コンテンツの特徴をモデル化することを学習するか[15, 29, 44, 55]、補助的なドメインから表現を転送することを学習する[42, 56, 59, 72, 82]。
Another line of work for zero-shot or few-shot recommendation discusses the quick adaptation to the new domain instead of providing recommendation for cold-start cases only.
ゼロショットまたは数ショットの推薦のための別の作業ラインは、コールドスタートのケースのみに推薦を提供するのではなく、新しいドメインへの迅速な適応について議論している。
Solutions typically follow the meta learning [27, 64] or causal learning [34] frameworks that make the model robust to domain adaptations.
解決策は通常、メタ学習[27, 64]または因果学習[34]のフレームワークに従う。
In our work, we ask P5 model pretrained on an auxiliary domain to solve tasks on target domains, where the users are known to P5 but the items have never been seen by the model before.
我々の研究では、補助ドメインで事前学習されたP5モデルに、P5にとってユーザは既知であるがアイテムは見たことがないターゲットドメインのタスクを解決するよう依頼する。

# Personalized Prompt Collection パーソナライズされたプロンプト・コレクション

To facilitate the multitask prompt-based pretraining for recommendation, we create a collection of personalized prompt templates.
推薦のためのマルチタスク・プロンプトベースの事前学習を容易にするために、パーソナライズされたプロンプト・テンプレートのコレクションを作成する。
The collection covers five different task families – rating, sequential recommendation, explanation, review, and direct recommendation.
このコレクションは、格付け、逐次推薦、説明、レビュー、直接推薦という5つの異なるタスクファミリーをカバーしている。
Each of these task families contains multiple personalized prompts to help P5 discover various aspects about users and items.
これらのタスクファミリーはそれぞれ、P5がユーザーやアイテムに関するさまざまな側面を発見できるよう、パーソナライズされた複数のプロンプトを含んでいる。
As mentioned in [51], a prompt is considered as consisting of an input template and a target template, along with a collection of associated metadata.
51]で述べたように、プロンプトは入力テンプレートとターゲットテンプレート、 および関連するメタデータのコレクションから構成されると考えられる。
In this work, we further define a personalized prompt as a prompt that includes personalized fields for different users and items.
この研究では、さらにパーソナライズされたプロンプトを、さまざまなユーザーやアイテムにパーソナライズされたフィールドを含むプロンプトと定義する。
For example, a user’s preference can be indicated through either an ID number or a description of the user such as name, gender, age, etc.
例えば、ユーザーの嗜好は、ID番号か、名前、性別、年齢などのユーザーの説明のどちらかによって示すことができる。
Moreover, the expected model output of a given personalized prompt should also vary according to its item field.
さらに、与えられたパーソナライズされたプロンプトの期待されるモデル出力も、その項目フィールドによって異なるはずである。
This implies the change of user’s preferences towards different items.
これは、異なるアイテムに対するユーザーの嗜好の変化を意味する。
Such item fields can be represented by either item ID numbers or item metadata that contains detailed descriptions.
このような項目フィールドは、項目ID番号または詳細な説明を含む項目メタデータのいずれかで表すことができる。
We designed basic P5 personalized prompt collection for each task family.
私たちは、各タスクファミリーのために、基本的なP5パーソナライズされたプロンプト集をデザインしました。
For rating prediction task family, we divide the prompts into three categories: 1) Given the information about a user and an item, directly predict the rating score ranging from 1 to 5; 2) Predict whether a user will rate an item a given score.
評価予測タスクファミリーでは、プロンプトを3つのカテゴリに分類する： 1) ユーザーとアイテムに関する情報が与えられたとき、1から5までの評価スコアを直接予測する。
The expected output is yes or no; 3) Predict if a user likes or dislikes an item.
期待される出力は「はい」か「いいえ」である。3) ユーザーが商品を好きか嫌いかを予測する。
Here we consider a star rating equal to or greater than 4 to be a like preference of the user, whereas lower scores indicate a dislike preference.
ここでは、★の評価が4以上であれば、ユーザーの好みが「好き」であるとみなし、それ以下であれば「嫌い」であるとみなす。
For sequential recommendation task family, we create three types of prompts: 1) Directly predict the next item based on user interaction history; 2) Given user interaction history, choose the possible next item from a candidate list, where only one item is positive; 3) Based on user interaction history, predict whether a given item will be interacted next by the user.
逐次推薦タスクファミリーでは、3種類のプロンプトを作成する： 1) ユーザとのインタラクション履歴に基づいて、次のアイテムを直接予測する。2) ユーザとのインタラクション履歴に基づいて、候補リストから次のアイテムを選択する。
For explanation task family, we ask P5 model to generate a textual explanation to justify a user’s preference towards a given item.
説明タスク・ファミリーでは、P5モデルに、与えられたアイテムに対するユーザーの好みを正当化するためのテキスト説明を生成するよう依頼する。
There are two prompt categories in this task family: 1) Directly generate an explanation sentence with user/item information; 2) Generate explanation based on a feature word as hint [31].
このタスクファミリーには2つのプロンプトカテゴリがある： 1)ユーザ/アイテム情報を用いて直接説明文を生成する、2)特徴語をヒントに説明文を生成する[31]。
For each category, there could be other auxiliary information included such as the review headline and the star rating.
各カテゴリーには、レビューの見出しや星の評価など、その他の補助的な情報が含まれることもある。
For review related task family, we create two types of prompts: 1) Summarize review comment to a shorter review title; 2) Predict the corresponding rating score based on the given review comment.
レビューに関連するタスクファミリーでは、2種類のプロンプトを作成する： 1)レビューコメントを短いレビュータイトルに要約する、2)与えられたレビューコメントに基づいて対応する評価スコアを予測する。
For direct recommendation, we also create two types of prompts: 1) Predict whether to recommend an item to a user, the answer should be yes or no; 2) Select the most suitable item from a list of candidate items to recommend to the user.
直接推薦のために、2種類のプロンプトも作成する： 1) あるアイテムをユーザーに推薦するかどうかを予測し、その答えが「はい」か「いいえ」であること。2) ユーザーに推薦するアイテムの候補リストから最適なアイテムを選択すること。
We provide some example prompts in Figure 2, and the complete collection of personalized prompts are provided in the Appendix.
図 2 にプロンプトの例をいくつか示し、パーソナライズされたプロンプトの全集は付録で提供する。
With the prompts, we can directly build input–target pairs from raw data.
プロンプトを使えば、生データから入力とターゲットのペアを直接作ることができる。
As illustrated in Figure 2, we can simply substitute the fields in braces with the corresponding information in the raw data and thus create training input–target pairs or zero-shot testing personalized prompts.
図2に示すように、中括弧内のフィールドを生データの対応する情報に置き換えるだけで、トレーニング入力とターゲットのペア、またはゼロショットテスト用のパーソナライズされたプロンプトを作成することができる。
The training data and pre-training tasks will distill the rich semantics from diverse modalities into the user and item tokens for preference understanding and personalization.
学習データと事前学習タスクは、多様なモダリティから豊富なセマンティクスを抽出し、嗜好の理解とパーソナライゼーションのために、ユーザーとアイテムのトークンに変換する。
Note that we divide the raw data into three parts—rating/review/explanation share the same raw data, while sequential and direct recommendation differ in terms of whether to use interaction history as input information.
生データを3つに分けている。評価／レビュー／説明は同じ生データを共有しているが、逐次レコメンドと直接レコメンドは、交流履歴を入力情報として使うかどうかという点で異なる。
During pretraining, we mix the input–target pairs from different task families together to serve as the training data.
事前訓練では、異なるタスクファミリーの入力とターゲットのペアを混ぜて訓練データとする。
To enhance P5’s robustness and zero-shot generalization, for each raw datum, we only sample a portion of rather than all of the personalized prompts in each task family.
P5のロバスト性とゼロショット汎化を高めるため、各生データムについて、各タスクファミリーのパーソナライズされたプロンプトのすべてではなく、一部のみをサンプリングする。
In sequential and direct recommendation task families, we also randomly select a group of negative items for those prompts that require a candidate list.
逐次推薦と直接推薦のタスクファミリーでは、候補リストが必要なプロンプトに対して、ネガティブ項目のグループもランダムに選択する。

# The P5 Paradigm and Model P5のパラダイムとモデル

## The P5 Architecture P5アーキテクチャ

The collection of personalized prompts introduced in the previous section makes it convenient to create a large amount of available pretraining data that covers a wide range of recommendation related tasks.
前節で紹介したパーソナライズされたプロンプトのコレクションは、推薦に関連する幅広いタスクをカバーする大量の利用可能な事前学習データを作成するのに便利である。
Thanks to the prompt templates, all pretraining data shares a unified format of input–target token sequences, which breaks the boundaries among different tasks.
プロンプト・テンプレートのおかげで、すべてのプレトレーニング・データは入力-ターゲット・トークンのシーケンスの統一されたフォーマットを共有し、異なるタスク間の境界をなくすことができる。
We claim that pretraining multiple recommendation tasks under a unified framework of conditional generation can facilitate all involving tasks together.
我々は、条件生成という統一的な枠組みのもとで複数の推薦タスクを事前学習することで、すべての推薦タスクをまとめて促進することができると主張する。
By immersing P5 in the full language environment throughout the pretraining stage, we also expect its zero-shot generalization capability of understanding unseen personalized prompts with detailed item descriptions.
プレトレーニングの段階からP5を完全な言語環境に浸すことで、詳細な項目説明のある未見のパーソナライズされたプロンプトを理解するゼロショット汎化能力も期待できる。
That is the reason why P5 is called a unified “Pretrain, Personalized Prompt, and Predict Paradigm”.
これが、P5が "Pretrain, Personalized Prompt, and Predict Paradigm "と呼ばれる所以である。
In terms of the model architecture, our P5 is established upon a basic encoder–decoder framework.
モデル・アーキテクチャに関しては、我々のP5は基本的なエンコーダー・デコーダーのフレームワークの上に確立されている。
We employ Transformer [65] blocks to build both the encoder and decoder.
エンコーダーとデコーダーの両方を構築するために、Transformer [65]ブロックを採用している。
Suppose the embeddings of an input token sequence is x = [𝑥1, · · · , 𝑥𝑛].
入力トークン列の埋め込みをx = [𝑥1, - - , 𝑥𝑛]とする。
As depicted in Figure 3, before feeding the embedding sequence into the bidirectional text encoder E (·), we add positional encodings P to the raw embeddings to capture their position information in the sequence.
図3に示すように、埋め込みシーケンスを双方向テキストエンコーダE (-)に入力する前に、シーケンス内の位置情報をキャプチャするために、生の埋め込みに位置エンコーディングPを追加する。
Furthermore, to make P5 aware of the personalized information contained in the input sequence, we also apply whole-word embeddings W to indicate whether consecutive sub-word tokens are from the same original word.
さらに、入力シーケンスに含まれるパーソナライズされた情報をP5に認識させるため、連続するサブワード・トークンが同じ元の単語からのものであるかどうかを示すホールワード埋め込みWも適用する。
For instance, if we directly represent the item with ID number 7391 as “item*7391”, then the word will be split into 4 separate tokens (i.e., “item”, “*”, “73”, “91”) by SentencePiece tokenizer [54].
例えば、ID番号7391のアイテムを "item*7391 "と直接表現する場合、この単語はSentencePieceトークナイザー[54]によって4つのトークン（すなわち、"item"、"*"、"73"、"91"）に分割される。
With the assistance of the shared whole-word embedding “⟨w10⟩” (e.g., in Figure 3), P5 can better recognize the important field with personalized information.
共有された全単語埋め込み"⟨w10⟩"（例えば図3）の支援により、P27はパーソナライズされた情報を持つ重要なフィールドをよりよく認識することができる。
Another alternative is to represent each user/item by an independent extra token (e.g., “⟨item_7391⟩”).
別の方法として、各ユーザー/アイテムを独立した追加トークン（例えば"⟨item_7391⟩"）で表すこともできる。
However, this may incur huge amounts of additional tokens when there is a large pool of users and items.
しかし、ユーザーとアイテムのプールが大きい場合、トークンの追加コストが膨大になる可能性がある。
Hence, in this paper, we adopt multiple sub-word units to represent a user or item.
そこで本稿では、ユーザーやアイテムを表現するために複数のサブワード単位を採用する。
Afterwards, the text encoder takes the sum of the aforementioned three embeddings e = [𝑒1, · · · , 𝑒𝑛] and outputs their contextualized representations t = [𝑡1, · · · , 𝑡𝑛] = E (e).
その後、テキストエンコーダは、前述の3つの埋め込みe = [↪Ll_1D452, - - , 𝑒𝑛]の合計を取り、それらの文脈化表現t = [↪Ll_1D461, - - , 𝑡𝑛] = E (e)を出力します。
The decoder D (·) then attends to both the previously generated tokens y<𝑗 and the encoder output t and predicts the probability distribution of future tokens: 𝑃𝜃 y𝑗 | y<𝑗 , x  = D (y<𝑗 , t).
デコーダ D (-) は、以前に生成されたトークン y<\_1D457 とエンコーダの出力 t の両方に注目し、将来のトークンの確率分布を予測する： 𝑃 | y𝑗 , x = D (y<𝑗 , t)。
During the pretraining stage, P5 learns the model parameters 𝜃 by minimizing the negative log-likelihood of label tokens y conditioned on input text x in an
事前学習段階では、P5は入力テキストxを条件とするラベルトークンyの負の対数尤度を最小化することで、モデルパラメータŰを学習する。

end-to-end manne:
エンド・ツー・エンドのマンネ

$$
\tag{1}
$$

This same objective function is shared by all recommendation tasks under P5.
この同じ目的関数は、P5のすべての推薦タスクで共有される。
As a result, we unify recommendation tasks with one model, one loss, and one data format
その結果、推薦タスクは1つのモデル、1つの損失、1つのデータ形式で統一される。

## Recommendation with Pretrained P5 事前訓練されたP5による推薦

After pretraining, P5 can directly perform different tasks with either seen or unseen personalized prompts.
事前学習後、P5は、目に見える、または目に見えないパーソナライズされたプロンプトを使用して、さまざまなタスクを直接実行することができます。
For rating, explanation, and review tasks, we simply use greedy decoding to generate answers.
評価、説明、レビューのタスクでは、単に貪欲な解読を使って答えを生成する。
In contrast, sequential and direct recommendation tasks usual require an item list as target output.
対照的に、逐次推薦タスクや直接推薦タスクは、通常、ターゲット出力としてアイテムリストを必要とする。
In view of this, for sequential recommendation, we apply beam search to generate a list of potential next items and evaluate it under the all-item setting.
そこで、逐次推薦では、ビームサーチを適用して次の候補リストを生成し、全項目設定の下で評価する。
For direct recommendation, we predict the recommended items from a candidate set S = {𝑆1, · · · , 𝑆𝑚}, where only one of the 𝑚 candidates is positive.
直接推薦では、候補集合S = {↪Lu_1D446, - - , ↪Lu_1D445A} から推薦項目を予測する。
Here, we also use beam search to decode a list of potential target items with the highest scores and then conduct evaluations.
ここでもビームサーチを使って、スコアの高いターゲット候補のリストを解読し、評価を行う。
Both of the above decoding processes can be written as:
上記のデコード処理は、どちらも次のように書くことができる：

$$
\tag{2}
$$

where 𝐵 denotes the beam size and C is the output item list.
ここで、↪L_1D435 はビームサイズを表し、C は出力項目リストを表す。

# Experiments 実験

In this section, we evaluate the performance of the proposed P5 approach on real-world data and compare it with various representative methods targeting at different task families.
このセクションでは、提案するP5アプローチの性能を実世界のデータで評価し、異なるタスクファミリーを対象とした様々な代表的手法と比較する。
Through the performance comparison and ablation studies, we aim to answer the following research questions regarding our unified “Pretrain, Personalized Prompt, and Predict Pargadigm” (P5): • RQ1: How does our unified P5 framework perform compared with task-specific methods on all five task families? • RQ2: Does P5 have enough zero-shot generalization ability when transferring to unseen personalized prompts for either existing or new items? • RQ3: How do scaling factors such as model size, number of task families, and number of prompts affect the performance of P5? • RQ4: Which is a better way to implement personalization in P5: adopting an independent extra token for each user or item (e.g., “⟨user*23⟩”) or the default setting, i.e., tokenizing each user or item into multiple sub-word units (e.g., “user”, “*”, “23”)? • RQ5: How long does it take for P5 to conduct pretraining? Is it efficient to make inference with the pretrained P5 model? We provide statistics on training and inference time in the Appendix.
性能比較とアブレーション研究を通じて、我々の統一的な「Pretrain, Personalized Prompt, and Predict Pargadigm」(P5)に関する以下の研究質問に答えることを目的とする： - RQ1： RQ1：我々の統一されたP5フレームワークは、5つのタスクファミリー全てにおいて、タスク固有の手法と比較してどのようなパフォーマンスを示すか？- RQ2： P5は、既存または新規アイテムの未知のパーソナライズドプロンプトに移行する際に、十分なゼロショット汎化能力を持つか？- RQ3： モデルサイズ、タスクファミリー数、プロンプト数などのスケーリング要因はP5のパフォーマンスにどのような影響を与えるか？- RQ4： P5におけるパーソナライゼーションの実装方法として、どちらが優れているか： 例："⟨user*23⟩"）と、デフォルトの設定（例："user", "*", "23"）では、各ユーザーやアイテムは複数のサブワード単位にトークン化される。- RQ5： P5が事前学習を行うのにかかる時間は？事前学習されたP5モデルを用いた推論は効率的か？学習と推論にかかる時間の統計を付録で提供します。

## Experimental Setup 実験セットアップ

Datasets.
データセット
We conduct extensive experiments over four real-world datasets.
我々は、4つの実世界のデータセットに対して広範な実験を行った。
The Amazon1 datasets are collected from Amazon.com platform with user ratings and reviews on 29 categories of products.
Amazon1データセットは、Amazon.comプラットフォームから収集されたもので、29カテゴリーの商品に関するユーザーの評価とレビューが含まれている。
In this paper, we adopt three of them to evaluate our method, namely Sports & Outdoors, Beauty, as well as Toys & Games.
本稿では、スポーツ＆アウトドア、ビューティー、トイ＆ゲームの3つを採用し、本手法を評価する。
Besides, Yelp2 dataset contains a large number of user ratings and reviews for business recommendation.
さらに、Yelp2データセットには、ビジネス推薦のための多数のユーザー評価とレビューが含まれている。
We follow [80] and use transaction records between January 1, 2019 to December 31, 2019.
80]に従い、2019年1月1日から2019年12月31日までの取引記録を使用する。
Due to space limit and that the results on Yelp show similar trends with other datasets, we put the experimental results on Yelp dataset in the Appendix.
紙面の都合上、またYelpの結果は他のデータセットと同様の傾向を示しているため、Yelpデータセットの実験結果は付録として掲載する。
The detailed statistics of these datasets are presented in Table 1.
これらのデータセットの詳細な統計は表1に示されている。

Task splits.
タスクの分割。
For rating, explanation, and review task families, we randomly split each dataset into training (80%), validation (10%) and testing (10%) sets, and ensure that there is at least one instance included in the training set for each user and item.
評価、説明、レビューのタスクファミリーについては、各データセットをトレーニングセット（80％）、検証セット（10％）、テストセット（10％）にランダムに分割し、各ユーザーとアイテムについて、トレーニングセットに少なくとも1つのインスタンスが含まれるようにする。
To obtain the ground-truth explanations, following the natural language explanation works [30, 31], we first extract item feature words from the reviews with the help of the Sentires toolkit3 [77, 78], and then extract the sentences from reviews that comment on one or more item feature words as users’ explanation about their preference.
グランド・トゥルースの説明を得るために、自然言語説明の研究[30, 31]に従って、まず、Sentires toolkit3 [77, 78]の助けを借りてレビューから項目特徴語を抽出し、次に、1つ以上の項目特徴語にコメントするレビューの文章を、ユーザーの好みに関する説明として抽出する。
In terms of sequential recommendation task family, for each user interaction sequence, the last item is used as the test data, the item before the last one is used as the validation data, and the remaining data is used for training.
逐次推薦タスクファミリーの場合、各ユーザインタラクションシーケンスに対して、最後のアイテムがテストデータとして使用され、最後のアイテムの前のアイテムが検証データとして使用され、残りのデータがトレーニングに使用される。
To avoid data leakage during pretraining, we follow the training split of sequential recommendation to build the training set for direct recommendation task family.
事前学習中のデータ漏洩を避けるため、逐次推薦の学習分割に従って、直接推薦タスクファミリーの学習セットを構築する。
Implementation Details.
実施内容
Our P5 model utilizes the pretrained T5 checkpoints [47] as backbone.
我々のP5モデルは、事前に訓練されたT5チェックポイント[47]をバックボーンとして利用している。
According to the size of T5 backbone, we create two versions of P5, namely P5-small (P5-S) and P5-base (P5-B).
T5バックボーンのサイズに応じて、P5-small（P5-S）とP5-base（P5-B）の2種類のP5を作成する。
For P5-small, there are 6 layers for both encoder and decoder, the model dimensionality is 512 with 8-headed attention, and the number of parameters is 60.75 million.
P5-smallの場合、エンコーダとデコーダともに6層で、モデルの次元数は512、注目度は8ヘッド、パラメータ数は6075万である。
For P5-base, encoder and decoder both have 12 Transformer blocks.
P5ベースの場合、エンコーダーとデコーダーの両方に12個のトランスフォーマーブロックがある。
The model has an embedding dimensionality of 768 and a 12-headed attention, and the number of parameters is 223.28 million.
このモデルの埋め込み次元は768、注目度は12ヘッド、パラメータ数は2億2,328万である。
For tokenization, we use the SentencePiece [54] tokenizer with a vocabulary size of 32,128 for parsing sub-word units.
トークン化には、32,128の語彙サイズを持つSentencePiece [54]トークナイザーを使用し、サブワード単位を構文解析する。
We pretrain P5 for 10 epochs with AdamW optimization [39] on four NVIDIA RTX A5000 GPUs.
4つのNVIDIA RTX A5000 GPUで、AdamW最適化[39]を用いてP5を10エポック事前訓練した。
The batch size is set to 16 for P5-base and 32 for P5-small.
バッチサイズはP5-baseが16、P5-smallが32に設定されている。
We choose 1 × 10−3 as the peak learning rate and set the maximum length of input tokens to 512.
ピーク学習率として1×10-3を選び、入力トークンの最大長を512に設定した。
The warmup strategy is used to adjust the learning rate during training, the warmup stage is set to be the first 5% of all iterations.
ウォームアップ戦略は訓練中の学習率を調整するために使用され、ウォームアップ段階は全反復の最初の5％に設定される。
When negative sampling is needed for training, we use 1:1 positive vs.
トレーニングにネガティブサンプリングが必要な場合は、1:1のポジティブ対ネガティブを使用する。
negative sampling for both P5 and baselines.
P5とベースラインの両方でネガティブサンプリング。
Our default pretrain–predict combination adopts the last prompt in each task family for zero-shot evaluation while all remaining prompts are utilized for multitask prompted pretraining.
私たちのデフォルトのプリトレーニングと予測の組み合わせは、各タスクファミリーの最後のプロンプトをゼロショット評価に採用し、残りのすべてのプロンプトはマルチタスクプロンプトプリトレーニングに利用されます。
For rating prediction, we use Gaussian sampling to convert the original integer scores to float numbers rounded to 1 decimal place.
評価予測には、ガウシアンサンプリングを使用して、元の整数スコアを小数点以下1桁に丸めた浮動小数点数に変換する。
In this way, we can avoid overfitting the limited score types.
こうすることで、限られたスコアタイプへのオーバーフィッティングを避けることができる。
After this change, we increase the number of score classes from 5 to 41.
この変更後、得点クラスの数は5から41に増える。
For sequential recommendation, we set the beam size 𝐵 to 20.
逐次推薦では、ビームサイズ↪L_1D435↩を20に設定した。
For direct recommendation, the beam size is also 20 and the candidate pool contains 100 items, which consist of one ground-truth item and 99 sampled negative ones that the user has not interacted with.
直接推薦の場合も、ビームサイズは20であり、候補プールは100項目から構成され、1つの真実項目と99のサンプリングされた負の項目から構成される。
Metrics.
指標
For rating prediction, we adopt Root Mean Square Error (RMSE) and Mean Absolute Error (MAE).
視聴率予測には、二乗平均平方根誤差（RMSE）と平均絶対誤差（MAE）を採用する。
For sequential recommendation and direct recommendation tasks, we employ top-𝑘 Hit Ratio (HR@𝑘) and Normalized Discounted Cumulative Gain (NDCG@𝑘) to evaluate the performance and report HR@1, 5, 10 and NGCG@5, 10.
逐次推薦タスクと直接推薦タスクについては、性能評価としてトップṞヒット率(HR@𞗥)と正規化割引累積利得(NDCGṞ)を採用し、HR@1, 5, 10とNGCG@5, 10を報告する。
For explanation generation and review summarization, we evaluate different methods with BLEU-4, as well as ROUGE-1, ROUGE-2, and ROUGE-L.
説明生成とレビュー要約のために、BLEU-4、ROUGE-1、ROUGE-2、ROUGE-Lで異なる方法を評価した。
RMSE and MAE are “the lower, the better”, while all other metrics are “the higher, the better”.
RMSEとMAEは "低ければ低いほど良い"、その他の指標は "高ければ高いほど良い"。
For all tables in the following, bold numbers refer to the best performance, while underlined numbers indicate the second best performance.
以下のすべての表において、太字の数字はベストパフォーマンスを示し、下線の数字はセカンドベストパフォーマンスを示している。

## Baselines for Multiple Tasks 複数のタスクのベースライン

To demonstrate P5’s competence on a wide range of recommendation related tasks, we gather a collection of representative approaches for difference task families.
P5が推薦に関連する幅広いタスクで能力を発揮できることを実証するため、異なるタスク群に対する代表的なアプローチを集めた。
Rating Prediction and Direct Recommendation.
格付け予測と直接推薦。
These tasks take the user–item rating/interaction data, but no content or side information is provided.
これらのタスクは、ユーザーアイテムの評価／インタラクションデータを受け取るが、コンテンツやサイド情報は提供されない。
We aim to justify whether the models are able to provide accurate rating prediction or recommendation lists that align with the user preferences.
我々は、モデルが正確な評価予測やユーザーの嗜好に沿った推薦リストを提供できるかどうかを正当化することを目的としている。
We use MF [25] and MLP [5] under mean square root loss as rating prediction baselines.
評価予測のベースラインとして、MF [25]とMLP [5]を平均平方根損失下で使用する。
For direct recommendation, we use BPR-MF [49], BPR-MLP [5], and a state-of-the-art contrastive learning-based collaborative filtering model SimpleX [43] as baselines.
直接推薦には、BPR-MF[49]、BPR-MLP[5]、そして最新の対照学習ベースの協調フィルタリングモデルSimpleX[43]をベースラインとして使用する。
Sequential Recommendation.
順当な推薦。
We adopt several representative sequential recommendation approaches as our baselines.
我々は、いくつかの代表的な逐次推薦アプローチをベースラインとして採用する。
Caser [63] treats sequential recommendation as a Markov Chain and employs convolutional neural networks to model user interests.
Caser [63]は、逐次的な推薦をマルコフ連鎖として扱い、ユーザーの興味をモデル化するために畳み込みニューラルネットワークを採用している。
HGN [41] adopts a hierarchical gating networks to learn user behaviors from the perspectives of both long and short terms.
HGN[41]は、階層的なゲーティング・ネットワークを採用し、長期と短期の両方の観点からユーザーの行動を学習する。
GRU4Rec [21] is originally proposed for session-based recommendation.
GRU4Rec [21]はもともとセッションベースの推薦のために提案された。
It utilizes GRU [7] to model the user click history sequence.
GRU [7]を利用して、ユーザーのクリック履歴シーケンスをモデル化する。
BERT4Rec [60] mimics the BERT-style masked language modeling and learns a bidirectional representation for sequential recommendation.
BERT4Rec [60]は、BERTスタイルのマスク言語モデリングを模倣し、逐次推薦のための双方向表現を学習する。
FDSA [73] focuses on the feature transition patterns by modeling feature sequence with a self-attention module.
FDSA[73]は、特徴列を自己注目モジュールでモデル化することで、特徴遷移パターンに着目している。
SASRec [24] adopts selfattention mechanism in a sequential recommendation model, which reconciles the properties of Markov Chains and RNN-based approaches.
SASRec [24]は、マルコフ連鎖とRNNベースのアプローチの特性を調和させた逐次推薦モデルにおいて、自己注意メカニズムを採用している。
S 3 -Rec [80] leverages self-supervised objectives to help sequential recommendation model better discover the correlations among different items and their attributes.
S 3 -Rec [80]は、逐次推薦モデルが異なる項目とその属性間の相関関係をより良く発見できるように、自己教師付き目標を活用している。
We use the implementation of S3 -Rec and its baselines for comparison4 .
比較には、S3 -Recの実装とそのベースラインを使用する4 。
Explanation Generation.
説明世代。
For performance comparison, we consider several baselines with regard to the task of explanation generation.
性能比較のために、説明生成のタスクに関していくつかのベースラインを検討した。
Attn2Seq [10] learns to encode attributes into vectors, and then invokes an attention mechanism to generate reviews conditioned on the attribute vector.
Attn2Seq [10]は、属性をベクトルにエンコードすることを学習し、次に属性ベクトルを条件とするレビューを生成するためにアテンションメカニズムを呼び出す。
NRT [32] utilizes GRU [7] to generate explanations based on user and item IDs.
NRT[32]は、GRU[7]を利用して、ユーザーIDとアイテムIDに基づいて説明を生成する。
PETER [31] is a simple and effective framework that attempts to utilize user and item IDs to generate explanations.
PETER [31]は、ユーザーIDとアイテムIDを利用して説明を生成しようとするシンプルで効果的なフレームワークである。
It is built upon a modified attention mask of the Transformer architecture.
トランスフォーマーアーキテクチャーのアテンションマスクを改良して作られている。
There is also a variant PETER+, which takes a hint feature word to assist the explanation generation.
また、PETER+というバリエーションもあり、これはヒントとなる特徴語を受け取り、説明の生成を補助する。
Review Related.
レビュー関連
For review summarization, we adopt pretrained T0 [51] and GPT-2 [46] checkpoints hosted by Hugging Face5 as baselines.
レビュー要約には、Hugging Face5がホストする事前学習済みのT0 [51]とGPT-2 [46]のチェックポイントをベースラインとして採用した。
For review preference prediction, we only use T0 to make comparisons because GPT-2 cannot perform this task.
レビュー嗜好予測では、GPT-2はこのタスクを実行できないため、T0のみを使用して比較を行う。

## Performance Comparison on Different Task Families (RQ1) 異なるタスクファミリーのパフォーマンス比較（RQ1）

In this section, we pretrain P5 with prompts from all five task families to verify its multitask learning ability.
本節では、P5のマルチタスク学習能力を検証するため、5つのタスクファミリーのプロンプトを用いてP5の事前学習を行う。
According to the default pretrain–predict task combination, we leave Prompt 1-10, Prompt 2-13, Prompt 3-12, Prompt 4-4, and Prompt 5-8 for zeroshot evaluation and pretrain P5 with the remaining personalized prompts.
デフォルトの事前訓練と予測タスクの組み合わせに従い、プロンプト1-10、プロンプト2-13、プロンプト3-12、プロンプト4-4、プロンプト5-8をゼロショット評価用に残し、残りのパーソナライズされたプロンプトでP5を事前訓練する。
The performances of P5 and relevant baselines on the five task families are presented in Table 2 to Table 7.
5つのタスク・ファミリーにおけるP5と関連するベースラインの性能を表2から表7に示す。
For each task family, we choose one or more seen prompts as supplement to the aforementioned zero-shot unseen prompts to perform evaluations.5.3.1 Rating Prediction.
各タスクファミリーについて、前述のゼロショットの未見プロンプトの補足とし て、1つまたは複数の見たプロンプトを選択して評価を実施する。
Prompt 1-6 and Prompt 1-10 are used for evaluating P5’s performance on rating prediction.
プロンプト1-6とプロンプト1-10は、レーティング予測に関するP5のパフォーマンスを評価するために使用される。
The performance comparison is presented in Table 2.
性能比較を表2に示す。
We can see that when testing with seen Prompt 1-6, P5-B gets better MAE and slightly higher RMSE on all three datasets compared with MF.
プロンプト1～6でテストした場合、P5-BはMFと比較して、3つのデータセットすべてでMAEが良く、RMSEがわずかに高いことがわかる。
When testing with unseen Prompt 1-10, P5-B can achieve similar performance as Prompt 1-6.
未見のプロンプト1～10でテストした場合、P5-Bはプロンプト1～6と同様のパフォーマンスを達成できる。
Moreover, P5-S usually has better MAE but higher RMSE.
さらに、P5-Sは通常、MAEは良いがRMSEは高い。
It seems that P5 is overfitting these data since the task complexity of rating prediction is relatively lower than other recommendation tasks.
格付け予測のタスクの複雑さは他の推薦タスクに比べて比較的低いため、P5はこれらのデータにオーバーフィットしているようだ。
Overall, these results show that it is feasible to perform rating prediction on a conditional text generation framework.5.3.2 Sequential Recommendation.
5.3.2逐次レコメンデーション 全体として、これらの結果は、条件付きテキスト生成フレームワーク上でレーティング予測を実行することが可能であることを示している。
As illustrated in Table 3, Prompt 2-3 and Prompt 2-13 are employed for the evaluation of sequential recommendation under all-item setting, i.e., using all items as candidates rather than sampling 100 or 1,000 items for ranking.
表3に示すように、プロンプト2-3およびプロンプト2-13は、全項目設定、すなわち、ランキングのために100項目または1,000項目をサンプリングするのではなく、すべての項目を候補として使用する場合の逐次推薦の評価に採用される。
From the table, we can see that P5-B surpasses all competitive baselines with a relatively large gap on both seen (Prompt 2-3) and unseen (Prompt 2-13) prompts.
表から、P5-Bは、見たプロンプト（プロンプト2-3）と見なかったプロンプト（プロンプト2-13）の両方で比較的大きな差をつけ、すべての競合ベースラインを上回っていることがわかる。
On Toys, P5-S can get even better performance than P5-B.
Toysでは、P5-SはP5-Bよりさらに良いパフォーマンスを得ることができる。
While on Beauty and Sports, P5-B achieves the advantage over P5-S.
美容とスポーツでは、P5-BがP5-Sより優位に立っている。
The results show that the P5 architecture is effective in modeling the user interaction history and conducting next item prediction with the help of beam search.5.3.3 Explanation Generation.
5.3.3説明の生成 P5アーキテクチャは、ユーザーとのインタラクションの履歴をモデル化し、ビームサーチの助けを借りて次のアイテムの予測を行うのに効果的であることが示された。
In Table 4, Prompt 3-9 and Prompt 3-12 are used to evaluate P5’s performance on explanation generation under feature-based setup, while Prompt 3-3 is used for direct explanation generation without providing a hint word.
表4では、プロンプト3-9とプロンプト3-12は、特徴ベースの設定におけるP5の説明生成性能を評価するために使用され、プロンプト3-3は、ヒント単語を提供しない直接説明生成に使用される。
We can see that for Prompt 3-3, P5 achieves the best performances against all baselines.
プロンプト3-3では、P5がすべてのベースラインに対して最高のパフォーマンスを達成していることがわかる。
For feature-based prompts (Prompts 3-9 & 3-12), P5 can outperform PETER+ on most cases, especially for Beauty and Toys.5.3.4 Review Related.
機能ベースのプロンプト（プロンプト3-9および3-12）では、P5はほとんどのケースでPETER+を上回ることができ、特に美容と玩具ではPETER+を上回ることができる。
We take Prompts 4-2 and 4-4 to compare P5’s performance with T0 on review preference prediction, as shown in Table 5.
表5に示すように、プロンプト4-2と4-4を取り上げ、レビュー嗜好予測におけるP5のパフォーマンスをT0と比較する。
We can see that P5-S achieves better RMSE and MAE on Beauty and Toys, while P5-B shows better performance on Sports.
P5-Sは美容と玩具でより良いRMSEとMAEを達成し、P5-Bはスポーツでより良いパフォーマンスを示していることがわかる。
Additionally, we take Prompt 4-1 to evaluate P5’s ability on review summarization, as shown in Table 6.
さらに、表6に示すように、プロンプト4-1を用いてP5のレビュー要約能力を評価した。
For this task, P5-S clearly outperforms T0 and GPT-2 on both Beauty and Toys datasets.
このタスクでは、P5-SはBeautyとToysの両データセットでT0とGPT-2を明らかに上回った。
It is worth noting that GPT-2 and T0 has 1.5B and 11B parameters, respectively.
注目すべきは、GPT-2とT0のパラメーターがそれぞれ1.5Bと11Bであることだ。
This shows that P5 can achieve better performances than these competitive baselines with a much smaller model size.5.3.5 Direct Recommendation.
5.3.5直接レコメンデーション これは、P5が、はるかに小さなモデルサイズで、これらの競合ベースラインよりも優れたパフォーマ ンスを達成できることを示している。
Finally, Prompts 5-1, 5-4, 5-5 and 5-8 are applied to evaluate the direct recommendation task under the 1-out-of-100 evaluation setting.
最後に、プロンプト5-1、5-4、5-5、5-8を適用して、100点満点中1点という評価設定で直接推薦タスクを評価する。
For binary question prompts (5-1 & 5-4), which are discriminative prompts, we use the softmax generation probability of “yes” to rank the candidate items.
識別プロンプトである2値質問プロンプト（5-1および5-4）については、「はい」のソフトマックス生成確率を使用して、候補項目のランク付けを行う。
For open question prompts (5-5 & 5-8), which are generative prompts, we use beam-search (Eq.(2)) to generate the top-𝑘 list.
生成プロンプトであるオープンクエスチョンプロンプト（5-5 & 5-8）については、ビームサーチ（式(2)）を使用してトップ\_1リストを生成する。
The results are presented in Table 7.
結果を表7に示す。
From the table, we can see that P5-B and P5-S have great advantages over BPR-MF and BPR-MLP on all three datasets.
表から、3つのデータセットすべてにおいて、P5-BとP5-SがBPR-MFとBPR-MLPに対して大きな優位性を持っていることがわかる。
Comparing with SimpleX, we can see that P5 works especially well on top-1 item ranking, which is more than two times better than SimpleX on HR@1.
SimpleXと比較すると、P5はトップ1アイテムランキングで特に効果を発揮し、HR@1ではSimpleXの2倍以上優れていることがわかる。
Besides, P5 also achieves the best result on most of the other metrics.
その上、P5は他のほとんどの指標でも最高の結果を出している。
The success of P5 on direct recommendation shows the competence of the sequence-to-sequence generation framework in recommendation domain.
直接推薦におけるP5の成功は、推薦領域における配列間生成フレームワークの能力を示している。

## Zero-shot Generalization to Unseen Prompts and Items in New Domain (RQ2) 新しい領域における未見のプロンプトとアイテムへのゼロショット汎化（RQ2）

5.4.1 Transfer to Unseen Personalized Prompts.
5.4.1 見えないパーソナライズされたプロンプトへの移行。
In this section, we transfer the pretrained P5 models to the previously heldout prompts during pretraining.
本節では、事前学習で保持されたプロンプトに対して、事前学習済みのP5モデルを転送する。
These unseen prompts are from the same task families, and the testing items have been seen by P5 during pretraining at least once.
これらの未閲覧のプロンプトは同じタスクファミリーのものであり、テスト項目はP5がプレトレーニング中に少なくとも一度は見たことがあるものである。
The experimental results are also reported in Table 2 to Table 7.
実験結果を表2から表7に示す。
As previously discussed in Section 5.3, P5 achieves surprisingly good performances on various task families when being challenged by unseen prompts.
セクション5.3で前述したように、P5は、未知のプロンプトに挑戦されたとき、様々なタスクファミリーで驚くほど優れたパフォーマンスを達成した。
On some specific datasets, the performances of P5 on unseen prompts even surpass seen prompts, e.g., P5-B gets the best performance under Prompt 2-13 on Sports.
例えば、スポーツのプロンプト2-13では、P5-Bが最高のパフォーマンスを示した。
These results show that multitask prompted pretraining empowers P5 enough robustness to understand unseen prompts with wording variations.5.4.2 Transfer to Items in New Domain.
5.4.2新領域の項目への移行。これらの結果は、マルチタスク・プロンプト事前訓練が、文言のバリエーションがある未知のプロンプトを理解するのに十分な頑健性をP5に与えることを示している。
Next, we increase the difficulty level of zero-shot transfer.
次に、ゼロシュート移籍の難易度を上げる。
We collect a group of 741 users that exist in all the three domains with their interaction and review histories in other domains.
3つのドメインすべてに存在する741人のユーザーと、他のドメインでのインタラクションやレビューの履歴を収集する。
The detailed statistics of these domain transfer evaluation sets are illustrated in Table 8.
これらのドメイン移転評価セットの詳細な統計は表8に示されている。
We then challenge P5-B pretrained on one domain with unseen prompts from the Task Family Z, whose item fields are filled with the information from a new product domain.
次に、1つのドメインで事前学習したP5-Bに、タスクファミリーZの未見のプロンプトで挑戦する。
For example, we ask the P5 model pretrained on the Toys domain about an existing user’s preference towards an item in the Beauty domain.
例えば、Toysドメインで事前学習されたP5モデルに、Beautyドメインのアイテムに対する既存ユーザーの嗜好を尋ねます。
The full results on all six directions are reported in Table 9.
全6方向に関する全結果を表9に報告する。
From the table, we notice P5 still maintains sufficient performances for rating prediction (Prompts Z-2 & Z-3), like/dislike prediction (Prompts Z-1 & Z4), as well as explanation generation with feature word (Prompt Z-6).
表から、評価予測（プロンプトZ-2、Z-3）、好き嫌い予測（プロンプトZ-1、Z4）、特徴語による説明生成（プロンプトZ-6）において、P5は依然として十分なパフォーマンスを維持していることがわかる。
In contrast, direct explanation generation without feature word (Prompts Z-5 & Z-7) is very difficult for P5 because it lacks awareness of relevant knowledge in the new domain.
一方、特徴語を用いない直接的な説明生成（プロンプトZ-5とZ-7）は、P5にとって非常に困難である。
In Figure 4, we provide some example explanations generated by P5-B under the setup of zero-shot domain transfer (Prompt Z-6).
図4では、ゼロショット領域移譲（プロンプトZ-6）の設定下でP5-Bが生成した説明の例を示している。
We can see that P5 is able to catch different users’ rating preferences and hint feature words, then integrate them with the knowledge learned from previous domain to generate plausible explanations.
P5は、さまざまなユーザーの評価嗜好とヒントとなる特徴語をキャッチし、それらを前のドメインから学習した知識と統合して、もっともらしい説明を生成することができることがわかる。

## Ablation on Model Size (RQ3) モデルサイズに関するアブレーション（RQ3）

In this section, we will discuss the influence of model size on the performance of P5 on different recommendation tasks.
このセクションでは、異なる推薦タスクにおけるP5のパフォーマンスに対するモデルサイズの影響について議論する。
Here, we train two size variants of P5, namely P5-small and P5-base.
ここでは、P5の2つのサイズバリエーション、すなわちP5-smallとP5-baseをトレーニングする。
The parameter numbers of these two P5 models are 60.75M and 223.28M, respectively.
これら2つのP5モデルのパラメータ数は、それぞれ60.75Mと223.28Mである。
From Table 2 to Table 7, we can see that although P5-S is only 1/4 of the size of P5-B, P5-S can beats P5-B on a series of tasks and datasets.
表2から表7から、P5-SはP5-Bの1/4のサイズしかないが、P5-Sは一連のタスクとデータセットでP5-Bに勝ることがわかる。
For example, P5-S achieves better sequential recommendation, review preference prediction, and direct recommendation (Prompts 5-5 & 5-8) performances than P5-B on Toys.
例えば、P5-SはP5-Bに比べ、逐次レコメンデーション、レビュー嗜好予測、直接レコメンデーション（プロンプト5-5と5-8）において優れたパフォーマンスを達成している。
In contrast, P5-B shows advantages on sequential recommendation and review preference prediction tasks for Sports.
対照的に、P5-Bはスポーツの逐次推薦とレビュー嗜好予測タスクで優位性を示した。
Since Sports contains more users, items and reviews and has a lower sparsity, it requires a model with higher capacity to discover latent correlation among different personalized factors.
スポーツには、より多くのユーザー、アイテム、レビューが含まれ、スパース性が低いため、さまざまなパーソナライズされた要素間の潜在的な相関関係を発見する能力が高いモデルが必要です。
The findings indicate that larger P5 models may be needed when the dataset is large, while for smaller datasets, smaller P5 models could be enough.
この結果は、データセットが大きい場合には、より大きなP5モデルが必要であり、データセットが小さい場合には、より小さなP5モデルで十分であることを示している。
As a result, we should decide an appropriate model size that matches the scale of the training data.
その結果、学習データの規模に合わせて適切なモデルサイズを決める必要がある。

## Ablation on Task Scaling (RQ3) 課題スケーリングに関するアブレーション（RQ3）

Moreover, we explore whether multitask prompted pretraining is superior than pretraining on each task family alone.
さらに、マルチタスクに促した事前トレーニングが、各タスクファミリー単独での事前トレーニングよりも優れているかどうかを調査する。
We pretrain P5-small on Beauty dataset with prompts from every single task family, resulting in five models – P5-S1, P5-S2, P5-S3, P5-S4, and P5-S5.
P5-smallをすべてのタスクファミリーのプロンプトを含むBeautyデータセットで事前学習し、P5-S1、P5-S2、P5-S3、P5-S4、P5-S5の5つのモデルを作成した。
We then compare P5-S on various recommendation tasks with the corresponding single task P5 model.
次に、様々な推薦タスクにおけるP5-Sを、対応する単一タスクのP5モデルと比較する。
The performance comparison between P5-S and P5-SN (𝑁 ∈ [1, 2, 3, 4, 5]) is illustrated in Figure 5.
P5-SとP5-SN（↪Lu_1∈[1,2,3,4,5]）の性能比較を図5に示す。
As shown in the figure, P5-S achieves comparable or better performance than P5-SN on rating prediction, sequential recommendation and direct recommendation tasks, while on text generation tasks such as explanation generation (Prompts 3-9 & 3-12) and review summarization (Prompt 4-1), P5-SN is better than P5-S.
図に示すように、評価予測、逐次推薦、直接推薦のタスクでは、P5-SはP5-SNと同等以上の性能を達成し、説明生成（プロンプト3-9、3-12）やレビュー要約（プロンプト4-1）のようなテキスト生成タスクでは、P5-SNはP5-Sより優れている。
This indicates that multitask modeling (P5-S) seeks a good balance among tasks and improves recommendation performance by leveraging the power of language understanding.
これは、マルチタスク・モデリング（P5-S）がタスク間のバランスを追求し、言語理解の力を活用することで推薦パフォーマンスを向上させることを示している。
Besides, both P5-S and P5-SN perform better than or comparable with state-ofthe-art baselines on all tasks, as shown in Table 2 through Table 7, which demonstrates the power of P5 for recommendation.
さらに、表2から表7に示すように、P5-SとP5-SNは、すべてのタスクにおいて、最新のベースラインよりも優れているか、同等である。

## Ablation on Prompt Scaling (RQ3) プロンプト・スケーリングにおけるアブレーション（RQ3）

As mentioned in implementation details, our default pretrain–predict task combination follows the leave-one-out strategy.
実装の詳細で述べたように、我々のデフォルトの事前訓練と予測タスクの組み合わせは、リーブワンアウト戦略に従っている。
However, do we need so many prompts during pretraining to enable P5’s zeroshot generalization ability? In this section, we explore to reduce the number of pretraining prompts and then make comparisons with the P5 model pretrained under default setup.
しかし、P5のゼロショット汎化能力を発揮させるために、事前学習時に多くのプロンプトが必要なのだろうか？この節では、事前学習のプロンプトの数を減らすことを検討し、デフォルトの設定で事前学習したP5モデルとの比較を行う。
To this end, we choose a collection of pretraining prompts that has the minimum number of prompts to cover all important personalized fields.
このため、すべての重要なパーソナライズされたフィールドをカバーする最小限のプロンプトの数を持つプレトレーニングプロンプトのコレクションを選択します。
Specifically, this combination contains the following 18 personalized prompts: {1-5, 1-6, 1-8, 1-9, 2-1, 2-3, 2-8, 2-11, 3-2, 3-3, 3-6, 3-9, 4-1, 4-2, 4-3, 5-2, 5-5, 5-7}.
具体的には、この組み合わせには以下の18のパーソナライズされたプロンプトが含まれる： {1-5, 1-6, 1-8, 1-9, 2-1, 2-3, 2-8, 2-11, 3-2, 3-3, 3-6, 3-9, 4-1, 4-2, 4-3, 5-2, 5-5, 5-7}.
Similar to the default pretrain–predict combination, the last prompt in each task family is for zero-shot evaluation.
デフォルトのpretrain-predictの組み合わせと同様に、各タスクファミリーの最後のプロンプトは、ゼロショット評価のためのものです。
We name this prompt scaling variant of P5-small as P5-PS and then pretrain P5-PS on Beauty dataset.
このP5-smallのプロンプト・スケーリング・バリアントをP5-PSと名付け、BeautyデータセットでP5-PSを事前訓練する。
The performance comparison between P5-S and P5-PS is also presented in Figure 5.
P5-SとP5-PSの性能比較も図5に示す。
From the figure, we can observe that P5-S beats P5-PS on most tasks except for some generation tasks (i.e., Prompts 3-3, 3-9 & 4-1).
図から、P5-SがP5-PSに勝っていることがわかる。ただし、いくつかの生成タスク（プロンプト3-3、3-9、4-1）は例外である。
Interestingly, P5-S outperforms P5-PS on Prompt 3-12 – a zero-shot explanation generation task.
興味深いことに、P5-Sはプロンプト3-12（ゼロショット説明生成タスク）においてP5-PSを上回っている。
In fact, P5-S also shows its superiority on other zero-shot tasks such as Prompts 1-10, 2-13, and 5-8.
実際、P5-Sは、プロンプト1-10、2-13、5-8といった他のゼロ・ショット・タスクでも優位性を示している。
Overall, we can find that larger number of high quality personalized prompts can generally help P5 achieve better performances on various recommendation tasks especially zero-shot tasks with unseen prompts.
全体として、質の高いパーソナライズされたプロンプトの数が多ければ多いほど、P5が様々な推薦タスク、特に未見のプロンプトを含むゼロショットタスクでより良いパフォーマンスを達成するのに役立つことがわかる。

## How to Implement Personalization (RQ4) パーソナライゼーションの導入方法（RQ4）

In this section, we discuss different strategies to implement personalization in P5.
このセクションでは、P5でパーソナライゼーションを実装するためのさまざまな戦略について説明する。
The default practice is using SentencePiece tokenizer to split personalized fields into multiple sub-word units and meanwhile using whole-word embedding to preserve the field information (Figure 3).
デフォルトでは、SentencePieceトークナイザーを使って、パーソナライズされたフィールドを複数のサブワード単位に分割し、一方、全単語埋め込みを使ってフィールド情報を保持する（図3）。
A straightforward alternative is creating an independent extra token for each user and item.
簡単な代替案は、ユーザーとアイテムごとに独立した追加トークンを作成することである。
Here we name this P5-small variant as P5-I and also pretrain it on Beauty dataset.
ここでは、このP5-small variantをP5-Iと名付け、Beautyデータセットで事前学習する。
While the former utilizes collaborative learning to implicitly optimize the latent correlations among different sub-word tokens, the latter learns a unique personalized representation for every extra token.
前者が異なるサブ単語トークン間の潜在的な相関関係を暗黙のうちに最適化するために協調学習を利用するのに対し、後者は余分なトークンごとにユニークなパーソナライズされた表現を学習する。
The performance comparison between P5-S and P5-I is shown in Figure 6.
P5-SとP5-Iの性能比較を図6に示す。
We can see that P5-I achieves similar performances as P5-S on regression tasks (Prompts 1-6 & 1-10 for rating prediction, Prompts 4-2 & 4-4 for review-based rating regression) and review summarization tasks (Prompt 4-1).
P5-Iは、回帰タスク（評価予測のためのプロンプト1-6と1-10、レビューベースの評価回帰のためのプロンプト4-2と4-4）およびレビュー要約タスク（プロンプト4-1）において、P5-Sと同様のパフォーマンスを達成していることがわかる。
Also, P5-I is slightly better than P5-S on explanation generation tasks (Prompts 3-3, 3-9 & 3-12).
また、説明生成タスク（プロンプト3-3、3-9、3-12）では、P5-IはP5-Sよりわずかに優れている。
However, P5-I significantly underperforms P5-S by a large margin on both sequential and direct recommendation tasks (all prompts in Figure 6 (c) & (d)).
しかし、P5-Iは、逐次推薦タスクと直接推薦タスクの両方で、P5-Sを大きく下回っている（図6 (c)と(d)のすべてのプロンプト）。
The reason behind P5-I’s lower performance lies in that the newly introduced huge number of extra tokens and embeddings cannot be well trained compared with the original sub-word units initialized from T5.
P5-Iの性能が低い理由は、新たに導入された膨大な数の余分なトークンと埋め込みが、T5から初期化された元のサブワード単位に比べてうまく学習できないことにある。
This shows that our default setting can achieve better recommendation and overall performances with the help of collaborative learning while keeping a small and constant amount of learnable tokens.
これは、学習可能なトークンの量を少なく一定に保ちながら、我々のデフォルト設定が協調学習の助けを借りて、より良い推薦と全体的なパフォーマンスを達成できることを示している。

# Conclusion and Future Work 結論と今後の課題

In this paper, we present P5 which unifies different recommendation tasks into a shared language modeling and natural language generation framework.
本稿では、異なる推薦タスクを言語モデリングと自然言語生成の共有フレームワークに統合したP5を紹介する。
By designing a collection of personalized prompts covering five recommendation task families, we transfer all raw data such as the user-item interactions, user descriptions, item metadata, and user reviews to the same format – input-target text pairs.
5つの推薦タスクファミリーをカバーするパーソナライズされたプロンプトのコレクションを設計することにより、ユーザとアイテムのインタラクション、ユーザの説明、アイテムのメタデータ、およびユーザレビューなどのすべての生データを同じフォーマット（入力とターゲットのテキストペア）に転送する。
We then pretrain P5 in a full language environment to help it discover deeper semantics for various recommendation tasks.
次に、P5が様々な推薦タスクに対してより深いセマンティクスを発見できるように、完全な言語環境でP5を事前訓練する。
According to our experiments, P5 can beat or achieve similar performance with several representative approaches on all five task families.
我々の実験によると、P5は5つのタスクファミリーすべてにおいて、いくつかの代表的なアプローチに勝つか、同等の性能を達成することができる。
Moreover, P5 shows the generalization ability on performing zeroshot transfer to new items, new domains, and new personalized prompts.
さらに、P5は、新しいアイテム、新しいドメイン、新しいパーソナライズされたプロンプトへのゼロショットトランスファーに関する汎化能力を示している。
In the future, we will continue exploring to further enlarge the model size of P5 and employ more powerful base models such as GPT-3, OPT, and BLOOM.
将来的には、P5のモデルサイズをさらに拡大し、GPT-3、OPT、BLOOMなど、より強力なベースモデルを採用するための探求を続けていく。
Besides, P5 is a very flexible paradigm and it is promising to further extend P5 to diverse modalities and more tasks such as conversational recommendation, comparative recommendation, cross-platform recommendation, or even various search tasks by incorporating user queries into P5.
さらに、P5は非常に柔軟なパラダイムであり、P5にユーザークエリを組み込むことによって、会話型推薦、比較型推薦、クロスプラットフォーム推薦、あるいは様々な検索タスクなど、多様なモダリティやより多くのタスクにP5をさらに拡張することが期待される。
Finally, in this work, we designed explicit prompts since they are intuitive, flexible, and close to the natural way of how humans communicate with each other, which enables instruction-based recommendation, while in the future, we will also investigate prompt search and/or latent prompt techniques to achieve instruction prompts or leverage retrieval-enhanced generation to further boost P5’s performance on downstream tasks.
最後に、本研究では、明示的なプロンプトは直感的で柔軟性があり、人間同士の自然なコミュニケーションに近いため、指示に基づく推薦が可能であるとして、明示的なプロンプトを設計したが、今後は、プロンプト検索や潜在的なプロンプトの技術も研究し、指示に基づくプロンプトを実現したり、検索を活用した生成を行うことで、下流タスクにおけるP5の性能をさらに向上させる予定である。
