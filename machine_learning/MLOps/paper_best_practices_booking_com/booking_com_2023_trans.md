## link リンク

- <https://arxiv.org/pdf/2306.13662> <https://arxiv.org/pdf/2306.13662>

# Best Practices for Machine Learning Systems: An Industrial Framework for Analysis and Optimization 機械学習システムのベストプラクティス 分析と最適化のための産業用フレームワーク

## abstract 抄録

In the last few years, the Machine Learning (ML) and Artificial Intelligence community has developed an increasing interest in Software Engineering (SE) for ML Systems leading to a proliferation of best practices, rules, and guidelines aiming at improving the quality of the software of ML Systems.
ここ数年、機械学習（ML）と人工知能のコミュニティでは、MLシステムのソフトウェアエンジニアリング（SE）への関心が高まっており、MLシステムのソフトウェアの品質向上を目的としたベストプラクティス、ルール、ガイドラインの普及につながっている。
However, understanding their impact on the overall quality has received less attention.
しかし、全体的な品質に与える影響を理解することは、あまり注目されてこなかった。
Practices are usually presented in a prescriptive manner, without an explicit connection to their overall contribution to software quality.
プラクティスは、通常、ソフトウェア品質への全体的な貢献との明確な関連性がないまま、規定的な方法で提示される。
Based on the observation that different practices influence different aspects of software-quality and that one single quality aspect might be addressed by several practices we propose a framework to analyse sets of best practices with focus on quality impact and prioritization of their implementation.
異なるプラクティスがソフトウェア品質の異なる側面に影響を与え、1つの品質側面が複数のプラクティスによって対処される可能性があるという観察に基づき、品質への影響と実装の優先順位付けに焦点を当てたベストプラクティス群を分析するフレームワークを提案する。
We first introduce a hierarchical Software Quality Model (SQM) specifically tailored for ML Systems.
まず、MLシステムに特化した階層的ソフトウェア品質モデル（SQM）を紹介する。
Relying on expert knowledge, the connection between individual practices and software quality aspects is explicitly elicited for a large set of well-established practices.
専門家の知識に基づき、確立されたプラクティスの大規模なセットについて、個々のプラクティスとソフトウェア品質の側面との関連を明示的に引き出す。
Applying set-function optimization techniques we can answer questions such as what is the set of practices that maximizes SQM coverage, what are the most important ones, which practices should be implemented in order to improve specific quality aspects, among others.
集合関数最適化技術を応用することで、SQMカバレッジを最大化するプラクティスの集合は何か、最も重要なプラクティスは何か、特定の品質側面を改善するためにはどのプラクティスを実施すべきか、などの質問に答えることができる。
We illustrate the usage of our framework by analyzing well-known sets of practices.
よく知られたプラクティスのセットを分析することで、私たちのフレームワークの使い方を説明する。

## Introduction

In Software Engineering, Software Quality Models (SQM) are central when it comes to achieving high quality software, as highlighted for example by [10]: "A quality model provides the framework towards a definition of quality".
ソフトウェア工学において、ソフトウェア品質モデル（SQM）は、例えば[10]で強調されているように、高品質なソフトウェアを達成するための中心的存在である： 「品質モデルは、品質の定義に向けたフレームワークを提供する」。
A Software Quality Model is the set of characteristics and the relationships between them that provides the basis for specifying quality requirements and evaluation [19].
ソフトウェア品質モデルとは、品質要件と評価を規定するための基礎となる、特性の集合とそれらの間の関係のことである[19]。
In practice, a SQM is a structured set of attributes describing the aspects that are believed contribute to the overall quality.
実際には、SQMとは、全体的な品質に寄与すると考えられる側面を記述した、構造化された属性の集合である。
Machine Learning (ML) systems have unique properties like data dependencies and hidden feedback loops which make quality attributes such as diversity, fairness, human agency and oversight more relevant than in traditional software systems [29].
機械学習(ML)システムは、データの依存関係や隠れたフィードバックループのようなユニークな特性を持っており、多様性、公平性、人間の主体性、監視のような品質属性が、従来のソフトウェアシステムよりも重要になる[29]。
This makes traditional　quality models not directly applicable for ML applications.
このため、従来の品質モデルはMLアプリケーションには直接適用できない。
Moreover in recent years there has been a rise in the publication of best practices tailored for ML systems [26], [2], [34], [35], [27], however understanding their impact on overall quality and the systematic prioritization for their adoption has not received enough interest.
さらに近年、MLシステム用に調整されたベストプラクティスの発表が増加している[26], [2], [34], [35], [27]が、全体的な品質への影響や、採用のための体系的な優先順位付けを理解することは、十分な関心を集めていない。
Improving the quality of ML systems, especially in an industrial setting where multiple ML systems are in production, does not only require a set of practices, but also a deep understanding of their contribution to specific aspects of the quality of the system, as well as criteria to prioritize their implementation due to their large number and high implementation costs.
MLシステムの品質を向上させるためには、特に複数のMLシステムが生産されている産業環境では、一連のプラクティスだけでなく、システムの品質の特定の側面への貢献についての深い理解と、その数の多さと高い実装コストのために、それらの実装を優先するための基準が必要である。
Without a systematic prioritization based on their contribution to each individual aspect of software quality, it is challenging for practitioners to choose the optimal practices to adopt based on their needs which might lead to limited adoption, undesired biases, inefficient development processes and inconsistent quality.
ソフトウェア品質の各側面への貢献度に基づく体系的な優先順位付けがなければ、実務担当者がニーズに基づいて最適なプラクティスを選択することは困難であり、採用が制限され、望ましくないバイアス、非効率な開発プロセス、一貫性のない品質につながる可能性がある。
The challenge lies on the fact that some best-practices have a narrow impact, strongly affecting a few specific quality aspects while others have wider impact affecting many aspects, which might lead to redundancy or gaps in the coverage of the all the relevant quality aspects.
ベストプラクティスの中には、少数の特定の品質側面に強く影響する狭い影響力を持つものもあれば、多くの側面に影響する広い影響力を持つものもあるという事実に課題がある。
Another challenge is that the importance of each quality aspect depends on the specific ML application, hence there is no single set of best-practices that satisfies the quality requirements of all ML applications.
それゆえ、すべてのMLアプリケーションの品質要件を満たすベストプラクティスは存在しない。
To address these challenges we introduce a reusable framework to analyse the contribution of a set of best practices to the quality of the system according to the specific needs of the particular application.
これらの課題に対処するために、特定のアプリケーションの特定のニーズに従って、システムの品質に対する一連のベストプラクティスの寄与を分析するための再利用可能なフレームワークを紹介する。
The framework consists of a general-purpose Software Quality Model for ML Systems, expert-based representations of a large set of well established best-practices, and a criterion to assess a set of best practices w.r.t.
このフレームワークは、MLシステムのための汎用的なソフトウェア品質モデル、確立されたベストプラクティスの大規模なセットの専門家ベースの表現、およびベストプラクティスのセットを評価するための基準から構成される。
our SQM: the SQM Coverage Criterion, which quantifies how many of the attributes receive enough attention from a given set of best practices.
のSQMである： SQMカバレッジ基準は、与えられたベストプラクティスのセットから、どれだけの属性が十分に注目されているかを定量化するものである。
Applying set optimization techniques we can answer questions such as what are the practices that maximize the coverage, which practices can be implemented to address specific quality aspects and which aspects lack coverage, among others.
集合最適化技術を適用することで、カバレッジを最大化するプラクティスは何か、特定の品質面に対処するためにどのプラクティスを実施できるか、どの面がカバレッジに欠けているか、などの質問に答えることができる。
Concretely, our contributions are the following: 1) A generalpurpose software quality model tailored for ML systems.2) A framework to analyse and prioritize software engineering best practices based on their influence on quality, with the flexibility to be adaptable according to the needs of each organization.3) We apply the proposed framework to analyze existing sets of best practices for ML systems and identify their strengths and potential gaps.
具体的には、以下のような貢献がある： 1)MLシステム向けに調整された汎用ソフトウェア品質モデル。2)各組織のニーズに応じて適応可能な柔軟性を備えた、品質への影響に基づくソフトウェアエンジニアリングのベストプラクティスを分析し、優先順位を付けるためのフレームワーク。3)提案されたフレームワークを適用して、MLシステム向けの既存のベストプラクティスセットを分析し、その強みと潜在的なギャップを特定する。

The rest of the paper is organized as follows.
本稿の残りの部分は以下のように構成されている。
Section 2 discusses related work with emphasis on Software Quality Models and software best-practices for ML systems, section 3 introduces our Software Quality Model and describes its construction process.
セクション2では、ソフトウェア品質モデルとMLシステムのためのソフトウェアのベストプラクティスに重点を置いた関連研究を議論し、セクション3では、我々のソフトウェア品質モデルを紹介し、その構築プロセスを説明する。
Section 4 introduces our best-practices analysis framework with details about its construction process and relevant algorithms.
セクション4では、ベストプラクティス分析のフレームワークを、その構築プロセスと関連アルゴリズムの詳細とともに紹介する。
In section 5 various best-practices sets are analysed using our framework, we present our findings and insights.
セクション5では、我々のフレームワークを用いて様々なベストプラクティスを分析し、その結果と洞察を示す。
Finally, section 6 summarizes our work and discuses limitations and future work.
最後に、セクション6で我々の研究を要約し、限界と今後の課題について述べる。
Appendices include all the details, such as proofs, extensive results, and computer code to facilitate reusability and repeatability of our framework.
付録には、私たちのフレームワークの再利用性と再現性を促進するための証明、広範な結果、コンピューター・コードなど、すべての詳細が含まれている。

## Related Work 関連作品

### Software Quality Models for ML Systems MLシステムのためのソフトウェア品質モデル

Defining and measuring software quality is a fundamental problem and one of the first solutions came through the means of a software quality model in 1978 [8].
ソフトウェア品質の定義と測定は基本的な問題であり、1978年にソフトウェア品質モデルによって最初の解決策の1つがもたらされた[8]。
Such models include general software characteristics which are further refined into sub-characteristics, which are decomposed into measurable software attributes whose values are computed by a metric [6].
このようなモデルには、一般的なソフトウェア特性が含まれ、その特性はさらに細分化されて、測定可能なソフトウェア属性に分解され、その値はメトリックによって計算される[6]。
Software quality models developed until 2001 [5], [15], [11], [19] are characterized as basic since they make global assessments of a software product.
2001年までに開発されたソフトウェア品質モデル[5]、[15]、[11]、[19]は、ソフトウェア製品のグローバルな評価を行うため、基本的なものである。
Models developed afterwards, such as [4], [1], [18] are built on top of basic models and are specific to certain domains or specialized applications, hence are called tailored quality models [22].
その後開発された[4]、[1]、[18]などのモデルは、基本モデルの上に構築され、特定のドメインや特殊なアプリケーションに特化しているため、テーラード品質モデル[22]と呼ばれている。
Such a quality model tailored for data products has been presented in [18].
このようなデータ製品のための品質モデルは、[18]で紹介されている。
Software for ML Systems exhibits differences when compared to traditional software such as the fact that minor changes in the input may lead to large discrepancies in the output [20].
MLシステムのためのソフトウェアは、入力の些細な変更が出力の大きな不一致につながるという事実のような、従来のソフトウェアと比較した場合の違いを示す[20]。
Moreover due to the dependencies on data, ML systems accumulate technical debt which is harder to recognize than code dependencies, which are identified via static analysis by compilers and linkers, tooling that is not widely available for data dependencies.
さらに、データ依存性のために、MLシステムは技術的負債を蓄積する。この負債を認識するのは、コンパイラやリンカによる静的解析で特定されるコード依存性よりも難しい。
Other peculiarities of ML systems include direct and hidden feedback loops where two systems influence each other indirectly [26].
MLシステムの他の特殊性には、2つのシステムが間接的に影響し合う直接的なフィードバック・ループと隠れたフィードバック・ループがある[26]。
Additionally, software quality aspects such as fairness and explainability as well as legal and regulatory aspects which are relevant to ML software are not covered by existing software quality models [32].
さらに、MLソフトウェアに関連する法律や規制の側面だけでなく、公正さや説明可能性といったソフトウェア品質の側面は、既存のソフトウェア品質モデルではカバーされていない[32]。
Furthermore, existing quality attributes such as maintainability and testability need to be rethought in the context of ML software [16].
さらに、保守性やテスト容易性といった既存の品質属性は、MLソフトウェアの文脈で再考される必要がある[16]。
All these peculiarities make existing software quality models only partially applicable to ML software.
これらの特殊性により、既存のソフトウェア品質モデルはMLソフトウェアに部分的にしか適用できない。
In [29] the authors present the systematic construction of quality models for ML systems based on a specific industrial use case.
29]では、特定の産業ユースケースに基づいたMLシステムの品質モデルの体系的な構築について述べている。
The authors focus on the process of constructing a quality meta model, identifying ML quality requirements based on the use case and instantiating a quality model that is tailored to the business application.
著者らは、品質メタモデルの構築、ユースケースに基づくMLの品質要件の特定、ビジネスアプリケーションに合わせた品質モデルのインスタンス化のプロセスに焦点を当てている。
In our work however, we introduce a general software quality model for ML systems that can be directly applied on a large set of industrial applications, without the need to go through a construction process.
しかし、我々の研究では、MLシステムのための一般的なソフトウェア品質モデルを導入し、構築プロセスを経ることなく、大規模な産業アプリケーションに直接適用することができる。
The key difference between our work and [29], is that their main contribution a development process for quality models, while one of our main contributions is the quality model itself, which can be used with no or minimum modifications for a broad range of ML systems.
我々の仕事と[29]の主な違いは、彼らの主な貢献が品質モデルの開発プロセスであるのに対して、我々の主な貢献の一つは、幅広いMLシステムに対して全く、あるいは最小限の修正で使用できる品質モデルそのものである。
This allows the usage of the same quality model for multiple use cases within an organization which reduces the effort of its adoption and allows to create a common communication language regarding the quality of the ML systems in the organization.
これにより、組織内の複数のユースケースに同じ品質モデルを使用することができ、採用の労力を削減し、組織内のMLシステムの品質に関する共通のコミュニケーション言語を作成することができます。
In [23] the authors conclude that the majority of the studies on software quality for ML either adopt or extend the ISO 25010 Quality Model for software product quality [17].
23]では、MLのソフトウェア品質に関する研究の大半は、ソフトウェア製品の品質に関するISO 25010品質モデル[17]を採用するか、拡張していると結論付けている。
They find though that there is no consensus on whether ISO 25010 is appropriate to use for AI-based software or which characteristics of AI-based software may be mapped to attributes of traditional quality models.
しかし、ISO 25010がAIベースのソフトウェアに使用するのが適切かどうか、あるいはAIベースのソフトウェアのどの特性が従来の品質モデルの属性に対応付けられるかについては、コンセンサスが得られていない。
Unlike other studies, we did not adopt or extend ISO 25010 but rather followed a systematic approach to build our quality model from scratch by adding quality sub-characteristics based on their relevance to ML systems.
他の研究とは異なり、我々はISO 25010を採用したり拡張したりするのではなく、MLシステムとの関連性に基づいて品質サブ特性を追加し、ゼロから品質モデルを構築する体系的なアプローチをとった。

### Software Best Practices for ML Systems MLシステムのためのソフトウェアのベストプラクティス

Best practices for increasing the quality of ML systems are presented in [7], [2] and [34] however a systematic way to link the influence of the recommended practices to the software quality attributes of ML systems is not included.
MLシステムの品質を向上させるためのベストプラクティスは、[7]、[2]、[34]に示されているが、推奨されるプラクティスの影響をMLシステムのソフトウェア品質属性に結びつける体系的な方法は含まれていない。
This makes it particularly challenging for ML practitioners to prioritize the adoption (or even understand the impact) of the large set of best practices based on the specific needs of their organizations.
このため、MLの実務者にとっては、組織の具体的なニーズに基づいて、膨大なベストプラクティスの中から優先順位をつけて採用する（あるいはその影響を理解する）ことは、特に難しいことである。
In [35] the authors present published ML practices targeting several testing properties (relevance, robustness, correctness, efficiency, security, privacy, fairness and interpretability) however their influence on quality aspects is not being studied.
35]では、いくつかのテスト特性（妥当性、頑健性、正しさ、効率性、セキュリティ、プライバシー、公平性、解釈可能性）をターゲットとしたMLプラクティスが発表されているが、品質面への影響は研究されていない。
The authors in [27] conducted a survey of ML practitioners from multiple companies and present the effect of various published ML practices on four categories (Agility, Software Quality, Team Effectiveness and Traceability).
27]の著者らは、複数の企業のML実践者を対象に調査を実施し、4つのカテゴリー（アジリティ、ソフトウェア品質、チームの有効性、トレーサビリティ）に対する様々なML実践の効果を発表している。
They present the importance of each practice for each of the categories, as perceived by the surveyed practitioners.
各カテゴリーにおける各練習の重要性を、調査対象となった練習生が認識しているものとして示している。
However, these categories are generic, and in fact only two of them are directly related to software quality (Software Quality and Traceability), in contrast, we study the influence of each best practice on a full-blown general purpose Software Quality Model specifically built for ML system with fine-grained aspects such as testability and deployability.
しかし、これらのカテゴリーは汎用的であり、実際にソフトウェア品質に直接関係するのは2つだけである（ソフトウェア品質とトレーサビリティ）。対照的に、我々は、テスト可能性やデプロイ可能性などのきめ細かい側面を持つMLシステムのために特別に構築された、本格的な汎用ソフトウェア品質モデルに対する各ベストプラクティスの影響を研究する。
Furthermore, we study the influence on each quality aspect of the quality model when a set of practices is applied, which is key to understand and prioritize best-practices since the overall impact is different depending on which other practices are also implemented.
さらに、あるプラクティスが適用された場合に、品質モデルの各品質面に与える影響を調査している。これは、他のプラクティスがどのように適用されるかによって全体的な影響が異なるため、ベスト・プラクティスを理解し、優先順位をつけるための鍵となる。
In [21] the authors extracted challenges and solutions for large scale ML systems synthesized into four quality attributes: adaptability, scalability, safety and privacy.
21]では、大規模MLシステムの課題と解決策を4つの品質属性に集約している： 適応性、拡張性、安全性、プライバシー。
They categorized software practices based on the step on the ML lifecycle and the addressed quality attribute.
彼らは、MLライフサイクルのステップと対応する品質属性に基づいて、ソフトウェアプラクティスを分類した。
A difference of this work with ours, is that in [21] each practice targets a single quality attribute while its effect on multiple attributes is not explicitly studied.
この研究が我々の研究と異なる点は、[21]では各練習が単一の品質属性を対象としているのに対し、複数の属性に対する効果は明示的に研究されていない点である。
Even though there is work that studies the effect of practices on software quality [29], [21], [27] to the best of our knowledge, no study has been published about the interrelationship of software best-practices for ML Systems with multiple fine-grained quality attributes, nor about their prioritization in order to balance Software Quality and implementation costs.
我々の知る限り、ソフトウェア品質に対するプラクティスの効果を研究した研究はあるが[29], [21], [27]、複数のきめ細かな品質属性を持つMLシステムのソフトウェアベストプラクティスの相互関係や、ソフトウェア品質と実装コストのバランスをとるための優先順位付けに関する研究は発表されていない。

## A Software Quality Model for ML Systems MLシステムのためのソフトウェア品質モデル

### The model モデル

A quality model determines which quality aspects are considered when evaluating the properties of a software product [17].
品質モデルは、ソフトウェア製品の特性を評価する際に、どの品質側面を考慮するかを決定する[17]。
Our software quality model for ML systems comprises 7 quality characteristics further divided into sub-characteristics.
MLシステムのための我々のソフトウェア品質モデルは、7つの品質特性からなり、さらにサブ特性に分かれている。
Quality characteristics are general properties of quality that comprise the fundamental factors, which cannot be measured directly.
品質特性とは、直接測定することができない基本的な要素からなる、品質の一般的な特性である。
Each characteristic consists of sub-characteristics, which are concrete quality aspects that can be directly influenced and measured.
各特性は、直接影響を与えたり測定したりできる具体的な品質側面であるサブ特性から構成されている。
A graphical illustration of our software quality model for ML systems is presented in treestructure in Figure 1.
図1は、MLシステムのためのソフトウェア品質モデルの図解である。
We define quality characteristics as follows: Utility — The degree to which a machine learning system provides functions that meet stated and implied needs when used under specified conditions.
品質特性を以下のように定義する： 実用性 - 機械学習システムが、指定された条件下で使用されたときに、明示されたニーズと暗示されたニーズを満たす機能を提供する度合い。
Economy — The level of performance relative to the amount of resources used under stated conditions.
経済性 - 指定された条件下で使用されるリソースの量に対するパフォーマンスのレベル。
Robustness — The tolerance to degradation by the machine learning system under consideration when exposed to dynamic or adverse events.
ロバストネス（頑健性） - ダイナミックな事象や不利な事象にさらされたときの、機械学習システムの劣化に対する耐性。
Modifiability — The degree of effectiveness and efficiency with which a machine learning system can be modified to improve it, correct it or adapt it to changes in environment and in requirements.
修正可能性 - 機械学習システムを改善、修正、または環境や要件の変化に適応させるために修正できる有効性と効率の度合い。
Productionizability — The ease of performing the actions required for a machine learning system to run successfully in production.
生産性（Productionizability） - 機械学習システムを本番稼動させるために必要なアクションの実行の容易さ。
Comprehensibility — The degree to which users and contributors understand the relevant aspects of a machine learning system.
理解しやすさ - ユーザーや貢献者が機械学習システムの関連する側面を理解する度合い。
Responsibility — The level of trustworthiness of a machine learning system.
責任 - 機械学習システムの信頼度。
The definitions of all sub-characteristics can be found in Appendix B.
すべてのサブ特性の定義は付録Bにある。
Notice that there are no data quality attributes in the quality model, as these are defined in well established software quality models tailored for data [18].
品質モデルにはデータ品質属性がないことに注意。データ品質属性は、データ用に調整された確立されたソフトウェア品質モデルで定義されているからである[18]。
This existing data quality model can be used in addition to our software quality model, to analyze the quality of data which are used as input to an ML system.
この既存のデータ品質モデルは、我々のソフトウェア品質モデルに加えて、MLシステムへの入力として使用されるデータの品質を分析するために使用することができる。

### The development process 開発プロセス

We started by creating a list of the quality sub-characteristics to be included in our model.
私たちはまず、モデルに含めるべき品質サブ特性のリストを作成することから始めた。
To achieve this, we went through the list of all the known system quality attributes in [33] and all software quality models in [22] from which we shortlisted and adapted the ones we judged applicable to machine learning systems.
これを達成するために、我々は[33]にある既知のシステム品質属性のリストと[22]にあるソフトウェア品質モデルのリストを調べ、そこから機械学習システムに適用できると判断したものを選別し、適応させた。
The shortlisting was done based on the relevance of each quality attribute to any stages of the ML development lifecycle defined in [3] and taking into account the various types of ML use cases e-commerce platforms like Booking.com has.
Booking.comのようなeコマースプラットフォームが持つ様々なタイプのMLユースケースを考慮し、[3]で定義されたML開発ライフサイクルの各段階における各品質属性の関連性に基づいてリストアップを行った。
Next, we added attributes related to machine learning that were not part of the initial list, such as fairness and explainability (as defined in Appendix B).
次に、公平性や説明可能性（付録Bで定義）など、当初のリストにはなかった機械学習に関連する属性を追加した。
With the final list of attributes, we created clusters of factors (characteristics) comprising related sub-factors (sub-characteristics), following the standard nomenclature for quality models [22].
最終的な属性のリストを用いて、品質モデルの標準的な命名法[22]に従って、関連するサブファクター（サブ特性）からなるファクター（特性）のクラスターを作成した。

We validated the completeness of our quality model using published sets of machine learning practices [26], [7], [2], [27], [28].
私たちは、公表されている機械学習の実践例 [26], [7], [2], [27], [28] を用いて、品質モデルの完全性を検証した。
Concretely, we checked if we can relate these practices to at least one of the quality sub-characteristics in our quality model.
具体的には、これらのプラクティスを、品質モデルの品質サブ特性の少なくとも1つと関連付けることができるかどうかをチェックした。
We iterated on this procedure a few times before we concluded on an first version, which was further refined using feedback from 10 internal senior ML engineers and scientists working in the industry and building ML systems for a minimum of 5 years.
私たちはこの手順を数回繰り返し、最初のバージョンを完成させた。このバージョンは、ML業界で最低5年間MLシステムを構築している社内のシニアMLエンジニアや科学者10人からのフィードバックをもとにさらに改良された。
Given the speed with which the field is evolving, it is important to remark that the software quality model for machine learning is a live artifact constantly reviewed and updated in order to keep its relevance to the current machine learning needs.
この分野の進化のスピードを考えると、機械学習のためのソフトウェア品質モデルは、現在の機械学習のニーズとの関連性を保つために、常に見直され更新される生きた成果物であることを指摘することが重要である。
Another development process for a quality model for machine learning has been presented in [29], in which the authors explain the implementation process of quality models for particular machine learning related use cases.
機械学習のための品質モデルの別の開発プロセスが[29]に示されており、著者らは、特定の機械学習関連のユースケースのための品質モデルの実装プロセスを説明している。
Our development process aimed at creating a general-purpose quality model which is relevant for a wide range of machine learning applications.
私たちの開発プロセスは、幅広い機械学習アプリケーションに関連する汎用的な品質モデルを作成することを目的としています。
Different applications and organizations will put different emphasis onto different sub-characteristics (for example external facing systems should be invulnerable even at the cost of accuracy) something that can be achieved by using importance weights per quality sub-characteristic.
用途や組織によって、重視するサブ特性は異なる（例えば、対外的なシステムは、精度を犠牲にしてでも不死身であるべきだ）。
Having a common quality model for all the machine learning systems allows its usage as a common language for quality related initiatives and for identification of gaps on quality attributes both at the system and organizational level.
すべての機械学習システムに共通の品質モデルを持つことで、品質関連のイニシアティブのための共通言語として使用することができ、システムと組織の両方のレベルで品質属性に関するギャップを特定することができる。

## A Framework to Prioritize Software Practices ソフトウェア・プラクティスの優先順位を決めるフレームワーク

Choosing practices in order to improve ML quality is a challenging task mainly due to their large number, varying implementation costs, and overlapping effects.
MLの質を向上させるためにプラクティスを選択することは、その数の多さ、導入コストの違い、効果の重複などから、難しい課題である。
To tackle this, we propose a framework to analyze and prioritize software practices.
この課題に取り組むため、ソフトウェア・プラクティスを分析し、優先順位をつけるためのフレームワークを提案する。
Given a Software Quality Model represented by a set of sub-characteristics 𝐶, and a set of software best practices 𝑃 we want to choose a subset of practices maximizing the coverage of a given set of sub-characteristics, under a constraint of implementing at most 𝐵 practices 1 .
ソフトウェア品質モデルが部分特性↪L_1D436 の集合で表され、ソフトウェア・ベストプラクティス↪Lu_1D443 の集合が与えられている場合、最大↪Lu_1D435 個のプラクティス1を実装するという制約の下で、与えられた部分特性の集合を最大限にカバーするプラクティスのサブセットを選択したい。
Having an influence 𝑢(𝑝, 𝑐) for a practice 𝑝 on a sub-characteristic 𝑐 we can define coverage as a minimum threshold 𝑘 of influence.
あるサブ特性𝑝に対する影響力𝑢(𝑝)があれば、影響力の最小閾値𝑘としてカバレッジを定義することができる。
Formally we have: (1) A Software Quality Model, represented by its set of subcharacteristics 𝐶 (2) A set of software practices 𝑃 (3) For each practice 𝑝 ∈ 𝑃 and each quality sub-characteristic 𝑐 ∈ 𝐶, the influence defined by a function 𝑢 : 𝑃 × 𝐶 → R + (4) A sub-characteristic importance vector 𝑤 ∈ [0, 1] |𝐶| representing the relevance of each sub-characteristic 𝑐 ∈ 𝐶 (5) An effort budget in the form of number of practices to be adopted 𝐵 ∈ N (6) An integer 𝑘 representing the minimum influence necessary to consider any sub-characteristic covered We define the coverage function as a set function that given a set of sub-characteristics 𝐶 with importance weights 𝑤 and a coverage threshold 𝑘 maps a set of practices 𝑋 ∈ 2 𝑃 to a real number, formally:
形式的には以下のようになる： (1) 副特性 ↪Lu_1D436 の集合で表現されるソフトウェア品質モデル (2) ソフトウェア実践 ᵄ の集合 (3) 各実践 ᵄ と各品質副特性 𝐶 について、関数 𝑢 で定義される影響力： 𝑃 × 𝐶 → R + (4) サブ特性の重要度ベクトル𝑤∈ [0, 1].

The objective is to choose a subset of practices that maximizes the coverage of the quality model weighted by its importance under the budget constraint:
その目的は、予算制約の下で、重要度によって重み付けされた品質モデルの適用範囲を最大化する診療のサブセットを選択することである：

### Eliciting the relationship between best practices and quality sub-characteristics ベストプラクティスと品質サブ特性の関係を引き出す

In order to apply the framework in practice, we first needed a set of practices 𝑃.
フレームワークを実際に適用するために、私たちはまず実践のセット𝑃を必要とした。
To achieve this, we conducted a survey with our internal ML practitioners at Booking.com where we asked them which 3 best practices for ML systems, from the ones they apply in their day to day work, they find the most useful.
これを実現するために、Booking.com社内のML担当者にアンケートを実施し、彼らが日々の業務で適用しているMLシステムのベストプラクティスの中から、最も有用だと思うものを3つ選んでもらいました。
In total we received 25 responses from ML engineers and scientists with a minimum of 3 years of industrial experience building production ML systems.
合計で25人のMLエンジニアと科学者から回答を得た。最低3年の産業用MLシステムの構築経験がある。
Based on the responses we created a list of 41 practices, which can be found in Appendix D.1.Then, we obtained the values of the function 𝑢(𝑝, 𝑐) to be used as inputs in the framework by going through the following procedure.
そして、以下の手順で、フレームワークのインプットとなる関数𝑭(↪Ll_1D45D, 𝑐)の値を求めた。
We conducted a workshop with 13 internal ML practitioners (ML engineers and scientists with a minimum of 3 years of industrial experience building ML systems) who were given a lecture on the proposed Software Quality Model and had interactive exercises to ensure a deep understanding of all the quality sub-characteristics and their nuances.
私たちは、13名のML実務者（MLシステムを構築した3年以上の経験を持つMLエンジニアや科学者）を対象にワークショップを実施し、提案するソフトウェア品質モデルに関する講義と、すべての品質サブ特性とそのニュアンスを深く理解するための対話型演習を行いました。
In the end of the workshop, the practitioners were given a quiz to assess their understanding.
ワークショップの最後には、実践者たちにクイズが出題され、理解度をチェックした。
After the quiz, the practitioners were asked to score the set of 41 practices against each quality sub-characteristic (𝐶) on a 0-4 scale indicating their influence: irrelevant (0), weakly contributes (1), contributes (2), strongly contributes (3) and addresses (4) 2 .
小テストの後、実践者は41の実践を、各品質の下位特性（ǔ）に対して、その影響力を示す0～4の尺度で採点するよう求められた： 無関係(0)、弱く貢献(1)、貢献(2)、強く貢献(3)、貢献(4) 2 。
Finally by taking the median of the scores of all the practitioners we obtain the influence of each practice 𝑝 on each quality sub-characteristic 𝑐, 𝑢(𝑝, 𝑐).
最後に、すべての実践者のスコアの中央値を取ることで、各品質サブ特性𝑐に対する各実践𝑅の影響度𝑭(𝑐)が得られる。
To make this more concrete, we provide some examples of scores 𝑢(𝑝, 𝑐) for several pairs of quality sub-characteristic and practices in Table 1.
これをより具体的にするために、表1に品質サブ特性とプラクティスのいくつかのペアに対するスコア𝑢(𝑝, 𝑐)の例を示す。
Influence scores for each sub-characteristic can be found in Appendix F.
各サブ特性の影響力スコアは付録Fにある。
Given the influence per practice and sub-characteristic 𝑢(𝑝, 𝑐) and a coverage threshold 𝑘, we can determine when a sub-characteristic is considered covered.
練習とサブ特性ごとの影響度𝑢(𝑢, ᵅ)とカバー率閾値ᵅが与えられれば、あるサブ特性がいつカバーされているとみなされるかを決定できる。
For example, given that we want to cover Understandability, if 𝑘 = 10 then the practices documentation, peer code review and error analysis with influence scores 𝑢(𝑝, 𝑐) of 4,3 and 3 respectively, do cover it.
例えば、「理解しやすさ」をカバーしたい場合、 ᵅ = 10とすると、影響スコアᵅ(ᵅ)がそれぞれ4,3,3である文書化、ピア・コード・レ ビュー、エラー分析は、「理解しやすさ」をカバーします。
However the practices logging of metadata and artifacts, data versioning and alerting, with influence scores of 2,1 and 0 respectively, do not cover Understandability.
しかし、メタデータと成果物のロギング、データのバージョニング、アラートというプラクティスは、それぞれ2,1,0という影響力を持ち、理解可能性（Understandability）をカバーしていない。

### Scaling of Influence Scores 影響力スコアのスケーリング

Based on ML practitioners’ evaluation, four practices scored with an influence of weakly contributes = 1 should not be treated equally as a practice scored with addresses = 4, hence to penalize weak contributions we re-scale the scores.
ML実践者の評価によれば、「貢献度が弱い＝1」と採点された4つの実践は、「貢献度が高い＝4」と採点された実践と同等に扱われるべきではない。
To achieve this we chose a piecewise linear function where we define the addresses influence score = 4*strongly contributes, strongly contributes = 3* contributes, contributes = 2 *weakly contributes.
これを達成するために、我々はアドレスの影響力スコア＝4*強く貢献、強く貢献＝3*貢献、貢献＝2*弱く貢献と定義する区分線形関数を選んだ。
For continuous values, after averaging multiple ML practitioners scores, we apply a piecewise linear function between these values which we depict in Figure 2.
連続値については、複数のML実践者のスコアを平均化した後、これらの値の間に区分線形関数を適用する。
We defined coverage in Equation 1 as the minimum threshold of influence 𝑘.
式1でカバレッジを影響力の最小閾値↪Ll458↩と定義した。
We chose one addresses influence to cover a subcharacteristic, and after applying our re-scaling function we get 𝑘 = 24.
サブ特性をカバーするために1つのアドレスの影響力を選び、リスケーリング関数を適用した結果、ᵅ = 24となった。
In general, the parameter 𝑘 defines the coverage threshold, and the re-scaling allows to parameterize the relationship of the influence scores while keeping the scoring of the sub-characteristic and practice pairs on a small linear scale of [0; 4] ∈ Z 0+ .
一般的に、パラメータ↪Ll_1D458 は適用範囲の閾値を定義し、再スケーリングは、サブ特性と実践のペアのスコアリングを[0; 4] ∈ Z 0+ の小さな線形スケール上に維持しながら、影響スコアの関係をパラメータ化することを可能にする。
The choice of 𝑘 and of the re-scaling function depend on the application where the ML System is deployed and on the risk of wrongly treating a sub-characteristic as covered.
の選択とリスケーリング関数は、MLシステムが導入されるアプリケーションと、サブ特性を誤ってカバーするものとして扱うリスクに依存します。

### Inter-annotator Agreement 注釈者間協定

Assessing the influence of a practice in a quality sub-characteristic is a subjective task and therefore subject to annotator disagreement.
品質サブ特性における練習の影響を評価することは主観的な作業であるため、アノテーターの意見の相違に左右される。
We used two tests for agreement - whether two scores are identical (referred as plain agreement) and whether two scores differ by more than one level (referred as practical agreement).
2つの得点が同じかどうか（平易な一致と呼ばれる）と、2つの得点が1レベル以上異なるかどうか（実際的な一致と呼ばれる）という2つの一致のテストを使用した。
The practical test is more aligned with the complexity of the task and the variance coming from the practitioners experience and knowledge.
実技テストは、タスクの複雑さと、プラクティショナーの経験や知識から来るばらつきに沿ったものである。
We found an average agreement rate (between a pair of annotators) of 73.56% (plain) and 86.38% (practical).
平均一致率は73.56%（平文）、86.38%（実用文）であった。
We used Cohen’s Kappa to check the agreement rate while neutralizing the probability of agreement happening by chance, and reached 0.4 (plain) and 0.69 (practical).
偶然に一致する確率を中和しながら一致率をチェックするためにコーエンのカッパを用いたところ、0.4（平明）、0.69（実用）に達した。
These scores represent an agreement rate which is between fair (plain) and substantial (practical) according to [31].
これらのスコアは、[31]によれば、公正（平易）から実質的（実用的）の間の一致率を表している。
The observed consistency suggests that we can have new best practices sets (or new quality sub-characteristics), scored by substantially fewer practitioners, which we consider an important insight when it comes to adopting new practices in an industrial setting.
観察された一貫性は、新しいベストプラクティスセット（または新しい品質サブ特性）を、実質的に少数の実践者によって採点することができることを示唆している。
For example, considering the case of only two annotators, we estimate the sampling distribution for both the agreement-rate and Kappa statistic by computing the metric for every possible pair of annotators among the 13.
例えば、2人の注釈者しかいない場合を考えると、13人の注釈者の中から可能性のあるすべての注釈者ペアについて指標を計算することで、一致率とカッパ統計量のサンプリング分布を推定する。
For the agreement rates, the standard deviation is 1.38% (plain) and 1.68% (practical), and for the Kappa statistic the standard deviation is 0.043 (plain) and 0.05 (practical).
一致率の標準偏差は1.38%（平地）、1.68%（実用）であり、カッパ統計量の標準偏差は0.043（平地）、0.05（実用）である。
Both figures are low enough which enables us to substitute a large group of annotators with only a pair and still get reliable scores.
どちらの数字も十分に低いので、大勢のアノテーター・グループを1組だけで代用しても、信頼できるスコアを得ることができる。

### Algorithms アルゴリズム

The maximization problem we want to solve is similar to the Generalized Maximum Coverage (GMC) problem [9], with a clear difference: in GMC if a set 𝑋 covers an element 𝑎, then at least one subset 𝑌 ⊂ 𝑋 covers 𝑎.
我々が解きたい最大化問題は、一般化最大カバレッジ（GMC）問題 [9]に似ているが、明確な違いがある： GMCでは、集合𝑋が要素ᵄをカバーする場合、少なくとも1つの部分集合𝑋 ⊂ 𝑎が𝑎をカバーする。
In our case, if a set of practices 𝑄 ⊆ 𝑃 covers a sub-characteristic 𝑐 ∈ 𝐶, it might be the case that no subset of 𝑄 covers 𝑐.
私たちの場合、練習の集合𝑄が部分特性⊆𝑃をカバーする場合、𝑐の部分集合が𝑐をカバーすることはないかもしれない。
Consider two practices 𝑝1, 𝑝2 and sub-characteristic 𝑐 with 𝑢(𝑝1, 𝑐) = 𝑢(𝑝2, 𝑐) = 𝑘/2.
2つの練習方法ᵅ1, ᵅ2と、ᵅ(ᵅ1, 𝑐) = 𝑢(ᵅ2, 𝑐) = 𝑢/2 のサブ特性ᵅを考える。
In this case the set 𝑄 = {𝑝1, 𝑝2} covers 𝑐 since 𝑓 (𝑄; {𝑐}, 1, 𝑘)) = 𝑘 but no subset of 𝑄 does since 𝑓 ({𝑝1}; {𝑐}, 1, 𝑘)) = 𝑓 ({𝑝2}; {𝑐}, 1, 𝑘)) = 𝑘/2 and 𝑓 (∅; {𝑐}, 1, 𝑘)) = 0.
[empty]
Because of this, a specific analysis is required.
このため、具体的な分析が必要となる。
The budget expressed as the maximum number of practices to be applied leads to a combinatorial explosion of the search space.
適用するプラクティスの最大数で表される予算は、探索空間の組み合わせ論的爆発につながる。
To illustrate, the set of 41 practices we collected and a budget of 3 practices yields a search space of size 41 3  = 10660, whereas a budget of 10 practices yields a search space of 1.12e+9 options to explore.
例えるなら、我々が収集した41のプラクティスのセットと3プラクティスの予算は、サイズ41 3 = 10660の探索空間をもたらすが、10プラクティスの予算は1.12e+9の探索空間をもたらす。
To tackle this computational problem we propose a greedy solution based on the observation that 𝑓 is positive monotone submodular (proof in Appendix A).
この計算問題に対処するために、我々は、𝑓が正の単調劣モジュラであるという観測に基づく貪欲な解を提案する（付録Aに証明）。
Maximizing a monotone submodular function is known to be NP-Hard [14], [13], however a simple greedy approach yields a (1 − 1 𝑒 )-approximation [25] even for one general knapsack constrain [30], and it is the best polynomial time solution, unless 𝑃 = 𝑁 𝑃 [24], [12].
単調劣モジュラ関数の最大化は、NP-Hard [14], [13]であることが知られているが、単純な貪欲なアプローチは、1つの一般的なナップザック制約に対しても、(1 - 1 ↪Ll_1D452 )- 近似 [25]をもたらし[30]、𝑃 = 𝑃 [24], [12]でない限り、最良の多項式時間解である。
We propose two solutions: brute force and greedy, in Algorithm 1 and 2 respectively.
我々は2つの解決策を提案する： それぞれアルゴリズム1と2で、ブルートフォースと貪欲の2つの解決策を提案する。
In practice we found that the greedy approach rarely yields sub-optimal results for this case.
実際には、貪欲なアプローチがこのケースで最適でない結果をもたらすことはほとんどないことがわかった。

## Applying the Framework フレームワークの適用

In this section we illustrate the usage of our framework by analyzing our own best-practices set and three well-known ML best-practices sets [7], [2], [27] and [28] (we combine the last two as they intersect) including 28, 7, and 45 best practices respectively.
このセクションでは、我々のベストプラクティスセットと、3つのよく知られたMLのベストプラクティスセット[7]、[2]、[27]、[28]（最後の2つは交差しているので組み合わせる）を分析することで、我々のフレームワークの使い方を説明する。
In each case we compute the coverage function, optimal practices sets for different budgets, and highlight gaps as well as general trends.
それぞれのケースで、カバレッジ関数、異なる予算に対する最適な練習セットを計算し、ギャップと一般的な傾向を浮き彫りにする。
We also provide a global analysis combining all sets of best practices.
また、すべてのベストプラクティスを組み合わせたグローバルな分析も提供している。

### Analyzing sets of best practices ベストプラクティスの分析

#### Internal Set 内部セット

Using the influence vectors of the internal set of 41 practices applied at Booking.com, we can visualize the total contribution of the set to all the quality sub-characteristics and assess its completeness.
Booking.comで適用されている41のプラクティスの内部セットの影響ベクトルを使用すると、すべての品質サブ特性に対するセットの総貢献度を視覚化し、その完全性を評価することができます。
We plot the contributions of the internal set in Figure 3, where we mark the threshold 𝑘 = 24 contribution points indicating coverage of a quality sub-characteristic.
図3は、内部セットの寄与をプロットしたもので、品質サブ特性のカバレッジを示す閾値Ņ = 24寄与ポイントを示している。
We observe that 22 out of 29 sub-characteristics are being covered indicating a coverage rate of 75%.
29項目中22項目がカバーされており、カバー率は75%である。
The sub-characteristics with the largest influences are mostly associated with traditional software systems, such as effectiveness and monitoring, while the ones with the least influences are more specific to ML systems, such as explainability and discoverability.
影響が大きい下位特性は、有効性やモニタリングのような伝統的なソフトウェアシステムに関連するものが多く、影響が小さい下位特性は、説明可能性や発見可能性のようなMLシステムにより特有なものである。
This is due to the fact that historically, engineering best practices are more closely related to traditional software systems and only in the recent years ML specific best practices started becoming popular.
これは、歴史的にエンジニアリングのベストプラクティスは伝統的なソフトウェアシステムとより密接に関係しており、近年になってようやくML特有のベストプラクティスが普及し始めたという事実によるものだ。
Based on this analysis we were able to identify the areas for which practices are lacking and work towards their coverage, by creating new ones.
この分析に基づき、私たちは練習が不足している分野を特定し、新しい練習を作ることによって、そのカバーに取り組むことができた。
Concretely, to address the gaps in Vulnerability, Responsiveness and Discoverability we created the following practices: "Request an ML system security inspection", "Latency and Throughput are measured and requirements are defined", "Register the ML system in an accessible registry", which increase the coverage for each of the sub-characteristics respectively (see Appendix D.1 for their descriptions).
具体的には、「脆弱性」、「応答性」、「発見可能性」のギャップに対処するために、以下のような対策を実施しました： 「MLシステムのセキュリティ検査を依頼する」、「遅延とスループットを測定し、要件を定義する」、「アクセス可能なレジストリにMLシステムを登録する」。
To gain further insight, we use the Greedy algorithm to find the top 3 influential practices on all quality sub-characteristics, considering them all equally important.
さらなる洞察を得るために、すべての品質サブ特性について影響力のある上位3つのプラクティスを見つけるために、Greedyアルゴリズムを使用する。
The algorithm outputs a set of the following top 3 practices: "Write documentation about the ML system", "Write modular and reusable code", and "Automate the ML lifecycle".
このアルゴリズムは、以下のトップ3のプラクティスを出力する： 「MLシステムに関するドキュメントを書く「、」モジュール化された再利用可能なコードを書く「、」MLのライフサイクルを自動化する"。
This result has been used to guide the ML practitioners at Booking.com on the prioritization of practice adoption in their daily work, by highlighting the value of these practices on the overall ML quality.
この結果は、Booking.comのML担当者が日常業務でプラクティスを採用する際の優先順位を決める際の指針となり、ML全体の品質に対するプラクティスの価値を浮き彫りにした。
The actual prioritization of their adoption depends on the team, since different teams and departments use different priorities for the quality sub-characteristics.
チームや部門によって品質サブ特性に対する優先順位が異なるため、実際に採用する優先順位はチームによって異なる。

#### External Sets 外部セット

We analyze three ML best practices sets of 80 practices in total.
合計80のプラクティスからなる3つのMLベストプラクティスセットを分析する。
Since it is impractical to have the same 13 ML practitioners scoring the 80 practices, we limit the number of annotators to 2, based on the high agreement rate for a pair of annotators observed in Section 4.3.After the scoring, we compute the plain agreement rate for the 2 annotators to be 63.5% and the practical agreement rate 94.5%.
同じ13人のML実践者が80の実践を採点するのは非現実的なので、4.3節で観察された2人の注釈者のペアの高い一致率に基づいて、注釈者の数を2人に制限する。採点後、2人の注釈者の平明な一致率を63.5%、実用的な一致率を94.5%と計算する。
With these vectors, we can visualize the total contribution of the whole set of practices to each of the quality sub-characteristics and based on that assess which of them are being covered.
これらのベクトルによって、各品質サブ特性に対するプラクティス全体の総貢献度を可視化し、それに基づいてどのサブ特性がカバーされているかを評価することができる。
In Figure 4a we see that applying all the practices presented in [27] 25 sub-characteristics are covered.
図4aを見ると、[27]で紹介されているすべての練習方法を適用することで、25のサブ特性がカバーされていることがわかる。
In this set of practices the strongest emphasis is on sub-characteristics related to cost-effectiveness, responsibility and modifiability.
この一連のプラクティスでは、費用対効果、責任、修正可能性に関連するサブ特性が最も強調されている。
On the other hand, sub-characteristics such asscalability, discoverability, operability and responsiveness, remain uncovered even when applying all the 45 practices from this set.
その一方で、アスカラビリティー、ディスカバビリティー、操作性、レスポンシビリティーといったサブキャラクターは、この45のプラクティスをすべて適用しても、まだ発見されていない。
Figure 4b illustrates the contributions by applying all the 28 practices mentioned in [7] and we observe that this set covers 17 sub-characteristics: we observe the top contributions to be on non-ML specific quality sub-characteristics, although ML specific ones such as accuracy and fairness are also covered.
図4bは、[7]で言及された28のプラクティスをすべて適用した場合の貢献度を示しており、このセットが17のサブ特性をカバーしていることがわかる： このセットは17のサブ特性をカバーしていることがわかります。精度や公平性といったML特有のものもカバーしていますが、ML特有の品質サブ特性以外の貢献が上位を占めていることがわかります。
The least covered are related to collaboration such as ownership, discoverability and readability.
最もカバーされていないのは、所有権、発見しやすさ、読みやすさといったコラボレーションに関するものだ。
Lastly, the contributions of [2] to the software quality are depicted in Figure 4c.
最後に、[2]のソフトウェア品質への貢献を図4cに示す。
This set of 7 practices manages to cover 9 quality sub-characteristics with a focus on those related to economy and modifiability.
この7つのプラクティスは、経済性と修正可能性に関連するものを中心に、9つの品質サブ特性をカバーしている。
The least contributions are achieved on aspects related to the comprehensibility of ML systems.
MLシステムの理解可能性に関連する側面では、最も貢献が少ない。
In general we find that all practice sets focus on different quality attributes and have gaps on different areas of our SQM.
一般的に、どの練習セットも異なる品質属性に焦点を当てており、SQMの異なる領域でギャップがあることがわかる。
This indicates that the sets complement each other, which motivates our next analysis.
このことは、両セットが互いに補完し合っていることを示しており、これが次の分析の動機となる。
In Figure 4d we look into the quality coverage in the scenario where we apply all the practices combined.
図4dでは、すべてのプラクティスを複合的に適用したシナリオにおける品質カバー率を見ている。
After removing overlapping practices (see Appendix D.2), this set includes 76 practices.
重複する練習を取り除いた後（付録D.2参照）、このセットには76の練習が含まれている。
We observe that when we apply the full set of 76 practices, 28 sub-characteristics are covered which verifies that the practices complement each other.
76のプラクティスのフルセットを適用した場合、28のサブ特性がカバーされていることが確認され、プラクティスが互いに補完し合っていることが検証された。
An example that shows this is scalability, which is not covered by any set in isolation, but only when the practices are combined.
これを示す例がスケーラビリティであり、これは単独ではどのセットでもカバーできないが、プラクティスを組み合わせて初めてカバーできる。
We also see that even when applying all the 76 practices, discoverability remains uncovered.
また、76のプラクティスをすべて適用しても、ディスカバビリティ（発見しやすさ）はまだ発見されていない。
This shows that there is lack of practices addressing this quality sub-characteristic, something that was also observed in the analysis of the internal practice set.
このことは、この品質サブ特性に対応する練習が不足していることを示しており、これは内部練習セットの分析でも観察されたことである。
Moreover, the low scores for sub-characteristics like scalability, operability, usability and responsiveness indicate that they receive less attention compared to the rest.
さらに、スケーラビリティ、操作性、使いやすさ、応答性といった下位特性のスコアが低いのは、他の項目と比べて注目度が低いことを示している。
On the other hand, it is encouraging to see large scores for sub-characteristics related to trustworthiness such as fairness and explainability.
一方、「公平性」や「説明のしやすさ」など、信頼性に関連する下位特性のスコアが高いのは心強い。

### Score and coverage threshold sensitivity スコアとカバー率の閾値感度

To further assess the sensitivity of the results to the scores assigned by the ML practitioners, we perturb the scores by adding a random integer in the range [−1; 1] and [−2; 2].
ML実践者によって割り当てられたスコアに対する結果の感度をさらに評価するために、[-1; 1]と[-2; 2]の範囲内のランダムな整数を追加することによってスコアを摂動させる。
We then take the original scores and perturbed ones, and compute the scores of each subcharacteristic as if all practices were applied and rank them by the sum of scores.
次に、元のスコアと摂動されたスコアを取り、すべての練習が適用されたかのように各サブ特性のスコアを計算し、スコアの合計で順位をつける。
Then we measure the Pearson correlation coefficient of the original ranking and the ranking after the scores were perturbed.
次に、元のランキングとスコアを摂動させた後のランキングのピアソン相関係数を測定する。
After 1000 perturbation iterations we obtain a mean correlation coefficient of 0.94 with a variance of 0.0002 for perturbing by [−1; 1], and a mean of 0.91 with a variance of 0.0006 for perturbing by [−2; 2] respectively.
1000回の摂動反復後、[-1; 1]による摂動では平均相関係数0.94、分散0.0002、[-2; 2]による摂動では平均相関係数0.91、分散0.0006を得た。
A random integer in the range [−3; 3] yields a mean of 0.86 and a variance of 0.0016.
範囲[-3; 3]のランダムな整数は、0.86の平均と0.0016の分散をもたらします。
This shows that our results are robust to scoring variance.
このことは、我々の結果が得点分散に対して頑健であることを示している。
Regarding the coverage threshold 𝑘 we remark that 24 points is rather low since one single practice with addresses score would cover the sub-characteristic, at the same time, in Figures 3 and 4 we can see that small changes in 𝑘 do not lead to big changes in which quality sub-characteristics are covered, more importantly, the general observations hold even for moderate changes in 𝑘.
同時に、図3と図4では、ᑘの小さな変化は、どの品質サブ特性がカバーされるかに大きな変化をもたらさないことがわかります。

### How many practices are enough? 何回練習すれば十分か？

To evaluate how many practices are enough to maximize quality, we analyze the internal and open source sets combined (after removing overlapping practices the combined set has 101 practices, see Appendix D.2 for details).
品質を最大化するのに十分なプラクティスがいくつあるかを評価するために、内部プラクティスとオープンソース・セットを組み合わせて分析する（重複するプラクティスを削除した後、組み合わせたセットには101のプラクティスがある、詳細は付録D.2を参照）。
Using our prioritization framework we find the minimum number of practices which cover the same number of quality sub-characteristics as the full set of those 101 practices.
優先順位付けのフレームワークを用いて、101のプラクティスのフルセットと同じ数の品質サブ特性をカバーするプラクティスの最小数を見つける。
To achieve that, we find the top 𝑁 practices from the combined set of practices using our greedy algorithm (brute force takes too long), for 𝑁 ∈ [1, 101] and we evaluate what percentage of the quality sub-characteristics is being covered with each set of practices.
そのために、[1, 101]の貪欲なアルゴリズム（ブルートフォースでは時間がかかりすぎる）を用いて、組み合わせられたプラクティスのセットから上位ǔのプラクティスを見つけ、各プラクティスのセットで品質のサブ特性の何パーセントがカバーされているかを評価する。
Figure 5 illustrates the coverage percentage for all the values of 𝑁.
図5は、↪Lu_1D441 のすべての値に対するカバー率を示している。
We see that applying 5 practices covers almost 40%, 10 cover 70%, and to reach 96%, 24 are needed.
5つのプラクティスを適用することでほぼ40％をカバーし、10で70％をカバーし、96％に達するには24のプラクティスが必要であることがわかる。
The coverage does not increase further with the practices.
練習を積んでも補償額は増えない。
This result shows that using a relatively small number of practices can achieve similar results in terms of quality coverage to the full set of 101 practices.
この結果は、比較的少数の診療所を使用することで、101診療所のフルセットと質のカバー率という点で同様の結果が得られることを示している。
This means that when applying the right set of practices, a significant reduction in the effort of adoption can be achieved, which is especially relevant in an industrial setting.
これは、適切な一連の慣行を適用すれば、採用の労力を大幅に削減できることを意味する。

### Which are the best practices? ベストプラクティスは？

To gain further insights as to which are the 24 practices which maximize coverage, we provide the optimal set in Table 2, along with the source of each practice (some practices have been renamed for better clarity, see Appendix D.3 for details).
カバレッジを最大化する24のプラクティスがどれであるかについて、さらなる洞察を得るために、表2に各プラクティスの出典とともに最適なセットを示す（いくつかのプラクティスは、より明確にするために名称を変更している、詳細は付録D.3を参照）。
It is important to note that here we assume equal importance for each quality subcharacteristic, something that needs to be taken into account from ML practitioners wanting to use this set as guidance.
ここで重要なのは、各品質のサブ特性の重要性が同等であると仮定していることである。
In case a different importance weighting is desired, one needs to re-create this set after applying importance weights to each sub-characteristic.
異なる重要度重み付けが必要な場合は、各サブ特性に重要度重み付けを適用した後、このセットを再作成する必要がある。
Prioritization within the final set, can be achieved by taking into account the specific needs of an organization (for example if safety is top priority, practices focusing on robustness should be prioritized) or the cost of adoption per practice.
最終セット内での優先順位付けは、組織の特定のニーズ（例えば、安全性が最優先事項であれば、堅牢性に焦点を当てたプラクティスを優先すべきである）や、プラクティスごとの採用コストを考慮することによって達成することができる。

### Futher applications of the framework フレームワークの今後の応用

The proposed SQM is currently being used to construct a quality assessment framework for ML systems.
提案されたSQMは現在、MLシステムの品質評価フレームワークの構築に使用されている。
Concretely, the framework assesses the coverage of each quality sub-characteristic on an ML system level, to pinpoint improvement areas.
具体的には、このフレームワークは、MLシステム・レベルで各品質サブ特性のカバー率を評価し、改善点を特定する。
Implementing an ML quality assessment framework without an SQM for ML systems, would lead to an incomplete picture of ML quality.
MLシステムのSQMなしにML品質評価フレームワークを導入することは、MLの品質に関する不完全な把握につながる。
Moreover, the prioritization framework is being used alongside the quality assessment framework: After the quality of an ML system is assessed, by assigning a quality score per quality sub-characteristic, the sub-characteristics with low scores are provided as input in the prioritization framework in order to recommend the best 3 practices to apply in order to cover them.
さらに、優先順位付けフレームワークは、品質評価フレームワークと並行して使用される： MLシステムの品質が評価された後、品質サブ特性ごとに品質スコアが割り当てられ、スコアが低いサブ特性は、それらをカバーするために適用すべきベスト3のプラクティスを推奨するために、優先順位付けフレームワークの入力として提供される。
This has been very helpful for ML practitioners as it allows them to prioritize the improvements to be made efficiently, by focusing on practices that have the largest influence in the quality attributes that are considered the most important for the use case at hand.
これはMLの実務家にとって非常に有益である。というのも、目の前のユースケースにとって最も重要と考えられる品質属性に最も大きな影響を与えるプラクティスに焦点を当てることで、効率的に行うべき改善の優先順位をつけることができるからである。

Additionally, the SQM has created a common language for ML practitioners to discuss ML quality topics and quality related initiatives are easier to be justified.
さらに、SQMはML実務者がMLの品質トピックについて議論するための共通言語を作り出し、品質関連のイニシアチブは正当化されやすくなった。
For example, it is more straightforward to argue about the value of an initiative targeting to increase the adoption of unit-testing for ML systems, since the benefit of it, e.g.improvement in modifiability of the system, is clear.
例えば、MLシステムの単体テストの採用を増やすことを目標にしたイニシアチブの価値について議論することは、より簡単である。なぜなら、単体テストの利点、例えばシステムの修正可能性の向上は明らかだからである。
An advantage of our framework is that it is flexible enough to be adapted to other organizations.
私たちのフレームワークの利点は、他の組織にも適応できる柔軟性があることだ。
For completeness, we describe how this can happen.
念のため、どのようにしてこのようなことが起こりうるかを説明する。
The organization needs to determine which quality sub-characteristics are the most crucial, by specifying the importance weights 𝑊 for each sub-characteristic.
組織は、各サブ特性の重要度重み↪L_1D44A↩を指定することによって、どの品質サブ特性が最も重要であるかを決定する必要がある。
The provided software practices can be used as is or new ones can be added and scored by ML practitioners within the organization.
提供されたソフトウェア・プラクティスはそのまま使用することもできるし、組織内のML実務者が新しいものを追加して採点することもできる。
Lastly, a coverage threshold 𝑘 should be chosen based on how strict an organization wants to be for solving a given quality sub-characteristic.
最後に、網羅率閾値(coverage threshold)ᑘは、与えられた品質サブ特性を解決するために、組織がどの程度厳格でありたいかに基づいて選択されるべきである。
To deal with disagreements in the scores 𝑢(𝑝, 𝑐) or the coverage threshold 𝑘, the mean or median can be taken.
スコア𝑢(ᵅ)またはカバレッジ閾値𝑘の不一致に対処するために、平均値または中央値を取ることができる。
Then, all an ML practitioner needs to do is to run the prioritization algorithm using as inputs the quality sub-characteristics 𝐶 to be improved, the set of practices 𝑃 to be considered, the allowed budget 𝐵, the importance vectors𝑊 and the coverage threshold 𝑘, and then adopt the optimal practices which are recommended by the framework.
そして、ML実務者がすべきことは、改善すべき品質サブ特性ǔ、考慮すべきプラクティスの集合ᵄ、許容予算ᵄ、重要度ベクトル𝑊、カバレッジ閾値ᑘを入力として、優先順位付けアルゴリズムを実行し、フレームワークが推奨する最適なプラクティスを採用することである。

## Conclusions and Discussions 結論と考察

Conclusion.
結論
In this work we presented a framework to analyse the relationship between software engineering best practices for ML Systems and their quality with the primary purpose of prioritizing their implementation in an industrial setting.
この研究では、MLシステムのためのソフトウェア工学のベストプラクティスとその品質との関係を分析するためのフレームワークを提示し、産業環境での実装の優先順位を決めることを主な目的とした。
We addressed the challenge of defining quality by introducing a novel Software Quality Model specifically tailored for ML Systems.
我々は、MLシステムに特化した新しいソフトウェア品質モデルを導入することで、品質を定義するという課題に取り組んだ。
The relationship between best practices and the various aspects of quality was elicited by means of expert opinion and represented by vectors over the sub-characteristics of the Software Quality Model.
ベストプラクティスと品質の様々な側面との関係は、専門家の意見によって引き出され、ソフトウェア品質モデルのサブ特性上のベクトルで表された。
With these vectors we applied Set Optimization techniques to find the subset of best practices that maximize the coverage of the SQM.
これらのベクトルを用いて、SQMのカバレッジを最大化するベストプラクティスのサブセットを見つけるために、集合最適化技術を適用した。
We applied our framework to analyse 1 large industrial set of best practices as implemented at Booking.com and 3 public sets.
私たちは、Booking.comで実施されたベストプラクティスの大規模な産業セット1つと、公開されているセット3つを分析するために、私たちのフレームワークを適用した。
Our main findings are: (1) Different best-practices sets focus on different aspects of quality, reflecting the priorities and biases of the authors.(2) Combining the different best-practices sets, high coverage is achieved, remarkably, aspects that no single best-practices set covers on its own are covered by integrating different practices proposed by different authors.(3) Even though there is a proliferation of best practices for ML Systems, when chosen carefully, only a few are needed to achieve high coverage of all quality aspects.(4) Even though the influence of best-practices on quality aspects is a subjective concept we found surprisingly high consistency among experts.
我々の主な発見は以下の通りである： (1)異なるベストプラクティスセットは、著者の優先順位と偏見を反映し、品質の異なる側面に焦点を当てている。(2)異なるベストプラクティスセットを組み合わせることで、高いカバレッジが達成される。驚くべきことに、単一のベストプラクティスセットだけではカバーできない側面が、異なる著者によって提案された異なるプラクティスを統合することでカバーされる。 (3)MLシステムに関するベストプラクティスは数多く存在するが、慎重に選択すれば、すべての品質側面を高いレベルでカバーするために必要なものはわずかである。(4)品質側面に対するベストプラクティスの影響は主観的な概念であるが、専門家の間では驚くほど高い一貫性が見られた。
Our framework was useful to spot gaps in our practices leading to the creation of new ones to increase the coverage of specific quality aspects.
私たちのフレームワークは、私たちが実践していることのギャップを発見し、特定の品質面のカバー率を高めるための新たな実践を生み出すのに役立った。

Limitations.
制限。
A limitation of this work is that in order to add a new quality sub-characteristic or a new practice to the framework, one needs to score the influence vectors which is a time consuming procedure.
この作業の限界は、新しい品質サブ特性や新しいプラクティスをフレームワークに追加するためには、影響ベクトルをスコアリングする必要があり、これは時間のかかる手順である。
On the other hand, the addition or removal of an existing practice or quality sub-characteristic does not influence the existing scores.
一方、既存の慣習や品質サブ特性の追加や削除は、既存のスコアに影響を与えない。
Another caveat regards the subjectivity of the influence vectors based on the individuals who conduct the scoring.
もう一つの注意点は、採点を行う個人による影響ベクトルの主観性である。
However, our sensitivity analysis described in Section 5.2 indicates that our results are robust to scoring variance, which mitigates the subjectivity concerns.
しかし、セクション5.2で説明する感度分析によれば、我々の結果は得点のばらつきに対してロバストであり、主観性に関する懸念は軽減されている。

Future Work.
今後の課題。
Future work will focus on a comparison of our framework with baseline prioritization approaches (such as prioritizing the most popular practices first or the ones requiring the least effort) and on assessing the coverage of sub-characteristics in existing ML Systems.
今後の課題は、私たちのフレームワークとベースラインの優先順位付けアプローチ（最も人気のあるプラクティスを最初に優先する、あるいは最も労力を必要としないプラクティスを優先するなど）との比較、および既存のMLシステムにおけるサブ特性のカバレッジの評価に焦点を当てる。
We will also keep evolving the assessment framework mentioned in Section 5.5 since this can provide visibility on quality gaps of ML systems, and along with the prioritization framework can provide guidance to ML practitioners on the optimal actions to take to improve them.
また、5.5節で述べた評価フレームワークも進化させ続けます。なぜなら、評価フレームワークは、MLシステムの品質ギャップを可視化し、優先順位付けフレームワークとともに、MLシステムの改善のために取るべき最適な行動について、ML実務者に指針を与えることができるからです。
Furthermore, exploring more realistic practice implementation cost functions can lead to a better cost and quality trade-off.
さらに、より現実的な練習実施コスト関数を探ることで、コストと品質のトレードオフを改善することができる。
Lastly, even though we aim at producing a complete software quality model, further validation is necessary especially by the external ML community.
最後に、我々が完全なソフトウェア品質モデルの作成を目指しているとしても、特に外部のMLコミュニティによる更なる検証が必要である。
