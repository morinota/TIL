## link リンク

- <https://huyenchip.com/2023/04/11/llm-engineering.html> <https://huyenchip.com/2023/04/11/llm-engineering.html>

## title タイトル

Building LLM applications for production
production向けLLMアプリケーションの構築

# intro ♪ イントロ

A question that I’ve been asked a lot recently is how large language models (LLMs) will change machine learning workflows.
最近よく聞かれるのが、**大規模言語モデル（LLM）が機械学習のワークフローをどう変えるか**という質問です。
After working with several companies who are working with LLM applications and personally going down a rabbit hole building my applications, I realized two things:
LLMの申請書を作成しているいくつかの会社と仕事をし、個人的には申請書を作成するためにウサギの穴に行った後、私は2つのことに気づきました：

- 1. It’s easy to make something cool with LLMs, but very hard to make something production-ready with them.
**LLMを使って何かを作るのは簡単ですが、それをproduction-readyにするのは非常に難しい**。

- 2. LLM limitations are exacerbated by a lack of engineering rigor in prompt engineering, partially due to the ambiguous nature of natural languages, and partially due to the nascent nature of the field. 2. LLMの限界は、プロンプトエンジニアリングにおける工学的厳密さの欠如、自然言語の曖昧な性質による部分的なもの、そしてこの分野の新しさによる部分的なものによって悪化している。

This post consists of three parts.
この記事は3つのパートで構成されています。

- Part 1 discusses the key challenges of productionizing LLM applications and the solutions that I’ve seen. 第1部では、LLMアプリケーションをプロダクション化する際の主な課題と、その解決策について解説しています。

- Part 2 discusses how to compose multiple tasks with control flows (e.g. if statement, for loop) and incorporate tools (e.g. SQL executor, bash, web browsers, third-party APIs) for more complex and powerful applications. 第2部では、より複雑で強力なアプリケーションのために、複数のタスクを制御フロー（if文、forループなど）で構成し、ツール（SQL executor、bash、Webブラウザ、サードパーティAPIなど）を組み込む方法について説明します。

- Part 3 covers some of the promising use cases that I’ve seen companies building on top of LLMs and how to construct them from smaller tasks. 第3部では、LLMの上に構築される有望なユースケースをいくつか取り上げ、より小さなタスクからどのように構築するかについて説明します。

There has been so much written about LLMs, so feel free to skip any section you’re already familiar with.
LLMについてはあまりにも多くのことが書かれているので、すでに馴染みのあるセクションは自由に読み飛ばしてください。
