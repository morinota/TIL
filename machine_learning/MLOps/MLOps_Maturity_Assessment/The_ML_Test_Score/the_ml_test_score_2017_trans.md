refs: https://storage.googleapis.com/gweb-research2023-media/pubtools/4156.pdf


# The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction  
# MLテストスコア：MLの生産準備と技術的負債削減のためのルブリック  

Eric Breck, Shanqing Cai, Eric Nielsen, Michael Salib, D. Sculley Google, Inc. ebreck, cais, nielsene, msalib, dsculley@google.com  

## Abstract 要約

Creating reliable, production-level machine learning systems brings on a host of concerns not found in small toy examples or even large offline research experiments. Testing and monitoring are key considerations for ensuring the production-readiness of an ML system, and for reducing technical debt of ML systems. But it can be difficult to formulate specific tests, given that the actual prediction behavior of any given model is difficult to specify a priori. In this paper, we present 28 specific tests and monitoring needs, drawn from experience with a wide range of production ML systems to help quantify these issues and present an easy to follow road-map to improve production readiness and pay down ML technical debt. 
信頼性の高い生産レベルの機械学習システムを作成することは、小さなトイ例や大規模なオフライン研究実験では見られない多くの懸念をもたらします。**テストと監視は、MLシステムの生産準備性を確保し、MLシステムの技術的負債を削減するための重要な考慮事項**です。しかし、特定のモデルの実際の予測動作を事前に特定することが難しいため、具体的なテストを策定することは困難です。この論文では、幅広い生産MLシステムでの経験から引き出された28の具体的なテストと監視ニーズを提示し、これらの問題を定量化し、生産準備性を改善し、ML技術的負債を返済するための簡単に従うことができるロードマップを提示します。

<!-- ここまで読んだ -->

**_Keywords-Machine Learning, Testing, Monitoring, Reliabil-_**  
**_キーワード-機械学習、テスト、監視、信頼性、_**  
**_ity, Best Practices, Technical Debt_**  
**_ベストプラクティス、技術的負債_**  

## I. INTRODUCTION  I. はじめに  

![]()
figure 1. 

As machine learning (ML) systems continue to take on ever more central roles in real-world production settings, the issue of ML reliability has become increasingly critical.  
機械学習（ML）システムが実世界の生産環境でますます中心的な役割を果たすようになるにつれて、MLの信頼性の問題はますます重要になっています。  
ML reliability involves a host of issues not found in small toy examples or even large offline experiments, which can lead to surprisingly large amounts of technical debt [1].  
MLの信頼性は、小さなトイ例や大規模なオフライン実験では見られない多くの問題を含んでおり、驚くほど大きな技術的負債を引き起こす可能性があります[1]。  
Testing and monitoring are important strategies for improving reliability, reducing technical debt, and lowering longterm maintenance cost.  
**テストと監視は、信頼性を向上させ、技術的負債を削減し、長期的なメンテナンスコストを低下させるための重要な戦略**です。  
However, as suggested by Figure 1, ML system testing is also more complex a challenge than testing manually coded systems, due to the fact that ML system behavior depends strongly on data and models that cannot be strongly specified a priori.  
しかし、図1が示すように、MLシステムのテストは、手動でコーディングされたシステムのテストよりも複雑な課題です。これは、**MLシステムの動作が、事前に強く特定できないデータやモデルに強く依存しているため**です。  
One way to see this is to consider ML training as analogous to compilation, where the source is both code and training data.  
これを理解する一つの方法は、**MLトレーニングをコンパイルに類似したものと考えることです。ここで、ソースはコードとトレーニングデータの両方**です。  
By that analogy, training data needs testing like code, and a trained ML model needs production practices like a binary does, such as debuggability, rollbacks and monitoring.  
この類推により、トレーニングデータはコードのようにテストが必要であり、トレーニングされたMLモデルは、バイナリと同様に、デバッグ可能性、ロールバック、監視などの生産プラクティスが必要です。  

So, what should be tested and how much is enough?  
では、何をテストすべきで、どれだけの量が十分なのでしょうか？  
In this paper, we try to answer this question with a test _rubric, which is based on engineering decades of production-_  
この論文では、数十年にわたる生産レベルのエンジニアリングに基づいたテストルブリックでこの質問に答えようとします。_  
level ML systems at Google, in systems such as ad click prediction [2] and the Sibyl ML platform [3].  
グーグルの広告クリック予測[2]やSibyl MLプラットフォーム[3]などのシステムにおけるMLシステムです。  

We present a rubric as a set of 28 actionable tests, and offer a scoring system to measure how ready for production a given machine learning system is.
**私たちは、28の実行可能なテストのセットとしてルブリックを提示し、特定の機械学習システムがどれだけ生産準備が整っているかを測定するためのスコアリングシステムを提供**します。  
This rubric is intended to cover a range from a team just starting out with machine learning up through tests that even a well-established team may find difficult.  
このルブリックは、機械学習を始めたばかりのチームから、確立されたチームでも難しいと感じるテストまでの範囲をカバーすることを目的としています。  
Note that this rubric focuses on issues specific to ML systems, and so does not include generic software engineering best practices such as ensuring good unit test coverage and a well-defined binary release process.  
**このルブリックはMLシステムに特有の問題に焦点を当てているため、良好なユニットテストカバレッジや明確に定義されたバイナリリリースプロセスを確保するなどの一般的なソフトウェアエンジニアリングのベストプラクティスは含まれていません。**  
Such strategies remain necessary as well.  
そのような戦略も依然として必要です。  
We do call out a few specific areas for unit or integration tests that have unique ML-related behavior.  
私たちは、ユニットまたは統合テストのためのいくつかの特定の領域を指摘します。これらは独自のML関連の動作を持っています。  

_How to read the tests: Each test is written as an_  
_テストの読み方：各テストは_  
