## link リンク

- [Principles of chaos engineering](https://principlesofchaos.org/)

## title タイトル

PRINCIPLES OF CHAOS ENGINEERING
カオスエンジニアリングの原理

# Introduction 序章

Chaos Engineering is the discipline of experimenting on a system in order to build confidence in the system’s capability to withstand turbulent conditions in production.
カオスエンジニアリングとは、production環境での乱気流に耐えるシステムの信頼性を高めるために、**production環境のシステムで実験**する学問.

Advances in large-scale, distributed software systems are changing the game for software engineering.
大規模な分散型ソフトウェアシステム(=マイクロサービスアーキテクチャ的な??)の進歩は、ソフトウェア工学のゲームに変化をもたらしている.
As an industry, we are quick to adopt practices that increase flexibility of development and velocity of deployment.
業界として、私たちは開発の柔軟性と展開の速さを向上させるプラクティスをいち早く採用している.
An urgent question follows on the heels of these benefits: How much confidence we can have in the complex systems that we put into production?
このようなメリットの後には、緊急の疑問がつきまとう： production環境に投入する複雑なシステムに対して、私たちはどれだけの信頼を寄せることができるのか.

Even when all of the individual services in a distributed system are functioning properly, the interactions between those services can cause unpredictable outcomes.
分散システムの個々のサービスがすべて正常に機能している場合でも、それらのサービス間の相互作用によって、予測不可能な結果が生じることがある.
Unpredictable outcomes, compounded by rare but disruptive real-world events that affect production environments, make these distributed systems inherently chaotic.
予測不可能な結果は、production環境に影響を及ぼすまれではあるが破壊的な現実世界の出来事と相まって、これらの分散システムを本質的にカオスにする.

We need to identify weaknesses before they manifest in system-wide, aberrant behaviors.
**システム全体の異常なふるまいとして現れる前に、弱点を特定する必要がある**.
Systemic weaknesses could take the form of: improper fallback settings when a service is unavailable; retry storms from improperly tuned timeouts; outages when a downstream dependency receives too much traffic; cascading failures when a single point of failure crashes; etc.
システム的な弱点は、サービスが利用できないときの不適切なフォールバック設定、不適切に調整されたタイムアウトによる再試行ストーム、下流の依存関係がトラフィックを受けすぎたときの停止、単一障害点のクラッシュによるカスケード障害、などの形で現れる.
We must address the most significant weaknesses proactively, before they affect our customers in production.
**最も重要な弱点が、production環境のお客様に影響を与える前に、積極的に対処しなければならない**.
We need a way to manage the chaos inherent in these systems, take advantage of increasing flexibility and velocity, and have confidence in our production deployments despite the complexity that they represent.
このようなシステムに内在するカオスを管理し、柔軟性と速度の向上を利用し、複雑であるにもかかわらず本番環境に自信を持つための方法が必要である.

An empirical, systems-based approach addresses the chaos in distributed systems at scale and builds confidence in the ability of those systems to withstand realistic conditions.
実証的なシステムベースのアプローチは、大規模な分散システムにおけるカオスに対処し、それらのシステムが現実的な条件に耐える能力に対する信頼性を構築するものである.
We learn about the behavior of a distributed system by observing it during a controlled experiment.
分散システムの挙動については、制御された実験中に観察することで学ぶ.
We call this Chaos Engineering.
私たちはこれをカオスエンジニアリングと呼んでいる.

# Chaos in Practice カオスの実践

To specifically address the uncertainty of distributed systems at scale, Chaos Engineering can be thought of as the facilitation of experiments to uncover systemic weaknesses.
カオスエンジニアリングは、**大規模な分散システムの不確実性**に対処するために、**システムの弱点を発見するための実験を促進するもの**と考えることができる.
These experiments follow four steps:
これらの実験は、4つのステップを踏んで行われる：

- 1. Start by defining ‘steady state’ as some measurable output of a system that indicates normal behavior. まず、**‘steady state’(定常状態)**を、**正常な動作を示すシステムの測定可能な出力**(metricだよね...?)と定義することから始める.

- 2. Hypothesize that this steady state will continue in both the control group and the experimental group. コントロールグループと実験グループの両方で、このsteady stateが続くと仮定する.

- 3. Introduce variables that reflect real world events like servers that crash, hard drives that malfunction, network connections that are severed, etc. サーバーのクラッシュ、ハードディスクの故障、ネットワーク接続の切断など、現実世界の事象を反映した変数を導入する.

- 4. Try to disprove the hypothesis by looking for a difference in steady state between the control group and the experimental group. control群とexperimental群のsteady stateの違いを探して、仮説の反証を試みる.

The harder it is to disrupt the steady state, the more confidence we have in the behavior of the system.
steady stateを崩すのが難しいほど、システムの挙動に対する信頼性が高くなる.
If a weakness is uncovered, we now have a target for improvement before that behavior manifests in the system at large.
もし弱点が発見されれば、その動作がシステム全体に現れる前に改善する目標ができたことになる.

# Advanced Principles アドバンスドプリンシプル

The following principles describe an ideal application of Chaos Engineering, applied to the processes of experimentation described above.
カオスエンジニアリングの理想的な応用を、上記の実験プロセスに適用したのが以下の原則である.
The degree to which these principles are pursued strongly correlates to the confidence we can have in a distributed system at scale.
これらの原則がどの程度追求されているかは、スケールの大きな分散システムに対する信頼性に強く関係している.

## Build a Hypothesis around Steady State Behavior 定常的な振る舞いを軸に仮説を立てる

Focus on the measurable output of a system, rather than internal attributes of the system.
システムの内部属性ではなく、システムの測定可能な出力に焦点を当てる.
Measurements of that output over a short period of time constitute a proxy for the system’s steady state.
その出力を短時間で測定することで、システムの steady state を代用することができる.
The overall system’s throughput, error rates, latency percentiles, etc. could all be metrics of interest representing steady state behavior.
システム全体のスループット、エラーレート、レイテンシパーセンタイルなど.は、**いずれも steady state な挙動を表す注目すべきmetrics**となり得る.
By focusing on systemic behavior patterns during experiments, Chaos verifies that the system does work, rather than trying to validate how it works.
カオスは、実験中にシステム的な動作パターンに注目することで、システムがどのように動作するかを検証するのではなく、システムが動作することを検証している.

## Vary Real-world Events Vary 実世界のイベント

Chaos variables reflect real-world events.
**Chaos variables**は現実世界の事象を反映する.
Prioritize events either by potential impact or estimated frequency.
潜在的な影響または推定される頻度によって、事象の優先順位をつける.
Consider events that correspond to hardware failures like servers dying, software failures like malformed responses, and non-failure events like a spike in traffic or a scaling event.
サーバーが死ぬなどのハードウェア障害、不正な応答などのソフトウェア障害、トラフィックの急増やスケーリングイベントなどの非障害に対応するイベントを検討する.
Any event capable of disrupting steady state is a potential variable in a Chaos experiment.
**steady stateを崩し得る事象は、カオス実験における潜在的な変数となる**.

## Run Experiments in Production 実験を本番で実行する

Systems behave differently depending on environment and traffic patterns.
システムは、環境やトラフィックパターンによって異なる挙動を示す.
Since the behavior of utilization can change at any time, sampling real traffic is the only way to reliably capture the request path.
利用率の挙動はいつでも変化する可能性があるため、実際のトラフィックをサンプリングすることが、リクエスト経路を確実に捉える唯一の方法となる.
To guarantee both authenticity of the way in which the system is exercised and relevance to the current deployed system, Chaos strongly prefers to experiment directly on production traffic.
システムの運用方法の信憑性と、現在配備されているシステムとの関連性の両方を保証するために、**カオスは本番トラフィックで直接実験することを強く希望している**.

## Automate Experiments to Run Continuously 実験を自動化し、継続的に実行する

Running experiments manually is labor-intensive and ultimately unsustainable.
手作業で実験を行うのは労力がかかり、結局は持続不可能である.
Automate experiments and run them continuously.
実験を自動化し、継続的に実行すべき.
Chaos Engineering builds automation into the system to drive both orchestration and analysis.
カオスエンジニアリングは、オーケストレーションと分析の両方を推進するために、システムに自動化を構築している.

## Minimize Blast Radius ブラスト半径を最小にする

Experimenting in production has the potential to cause unnecessary customer pain.
**本番で実験することは、お客様に無用な苦痛を与える可能性がある.**
While there must be an allowance for some short-term negative impact, it is the responsibility and obligation of the Chaos Engineer to ensure the fallout from experiments are minimized and contained.
短期的な悪影響はある程度許容しなければなりませんが、実験による影響を最小限に抑え、抑制することはカオスエンジニアの責任であり義務である.

# Finally... 最後に...

Chaos Engineering is a powerful practice that is already changing how software is designed and engineered at some of the largest-scale operations in the world.
カオスエンジニアリングは、世界最大規模の事業所において、ソフトウェアの設計やエンジニアリングの方法をすでに変えている強力な手法である.
Where other practices address velocity and flexibility, Chaos specifically tackles systemic uncertainty in these distributed systems.
他のプラクティスがベロシティやフレキシビリティを扱うのに対し、カオスはこうした分散システムにおけるシステム的な不確実性に特に取り組んでいる.
The Principles of Chaos provide confidence to innovate quickly at massive scales and give customers the high quality experiences they deserve.
カオスの原理は、大規模なスケールで迅速にイノベーションを起こし、顧客が求める高品質な体験を提供するための自信を与えてくれる.

Join the ongoing discussion of the Principles of Chaos and their application in the Chaos Community.
カオスの原理とその応用について、カオス・コミュニティで進行中の議論に参加してください.
