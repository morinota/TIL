## link リンク

- <https://huyenchip.com/2023/04/11/llm-engineering.html#prompt_engineering_challenges> <https://huyenchip.com/2023/04/11/llm-engineering.html#prompt_engineering_challenges>

# Part I. Challenges of productionizing prompt engineering パート1 プロンプトエンジニアリングのプロダクション化の課題

## The ambiguity of natural languages 自然言語の曖昧さ

For most of the history of computers, engineers have written instructions in programming languages.
コンピュータの歴史の大半は、技術者がプログラミング言語で命令を書いてきた。
Programming languages are “mostly” exact.
プログラミング言語は「ほとんど」正確です。
Ambiguity causes frustration and even passionate hatred in developers (think dynamic typing in Python or JavaScript).
曖昧さは、開発者のフラストレーションや熱狂的な憎悪を引き起こす（PythonやJavaScriptの動的型付けを思い出してください）。

In prompt engineering, instructions are written in natural languages, which are a lot more flexible than programming languages.
プロンプトエンジニアリングでは、プログラミング言語よりもはるかに柔軟性の高い自然言語で命令が書かれます。
This can make for a great user experience, but can lead to a pretty bad developer experience.
これは素晴らしいユーザーエクスペリエンスになり得ますが、開発者にとってはかなり悪いエクスペリエンスにつながる可能性があります。

The flexibility comes from two directions: how users define instructions, and how LLMs respond to these instructions.
その柔軟性は、ユーザーが指示を定義する方法と、LLMがその指示に対応する方法の2方向からもたらされます。

First, the flexibility in user-defined prompts leads to silent failures.
まず、ユーザー定義のプロンプトの自由度が高いため、サイレント失敗につながる。
If someone accidentally makes some changes in code, like adding a random character or removing a line, it’ll likely throw an error.
誰かが誤ってコードに何らかの変更を加えた場合、例えばランダムな文字を追加したり、行を削除したりすると、エラーが発生する可能性があります。
However, if someone accidentally changes a prompt, it will still run but give very different outputs.
しかし、誰かが誤ってプロンプトを変更してしまった場合、実行はされるものの、出力は大きく異なります。

While the flexibility in user-defined prompts is just an annoyance, the ambiguity in LLMs’ generated responses can be a dealbreaker.
ユーザー定義のプロンプトの柔軟性は煩わしさに過ぎませんが、LLMが生成する回答の曖昧さは、破格のものです。
It leads to two problems:
それは、2つの問題につながります：

- 1. Ambiguous output format: downstream applications on top of LLMs expect outputs in a certain format so that they can parse. We can craft our prompts to be explicit about the output format, but there’s no guarantee that the outputs will always follow this format. 1. 曖昧な出力形式：LLMの上にある下流のアプリケーションは、解析できるように特定の形式の出力を期待します。 出力形式を明示するようにプロンプトを作成することはできますが、出力が常にこの形式に従っているという保証はありません。

- 2. Inconsistency in user experience: when using an application, users expect certain consistency. Imagine an insurance company giving you a different quote every time you check on their website. LLMs are stochastic – there’s no guarantee that an LLM will give you the same output for the same input every time. 2. ユーザーエクスペリエンスの不整合：アプリケーションを使用する際、ユーザーは一定の一貫性を求めます。 保険会社が、ホームページで確認するたびに違う見積もりを出していると想像してください。 LLMは確率的なもので、同じ入力に対して毎回同じ出力が得られるという保証はない。

You can force an LLM to give the same response by setting temperature = 0, which is, in general, a good practice.
温度=0とすることで、LLMに同じ応答をさせることができますが、これは一般的に良い習慣です。
While it mostly solves the consistency problem, it doesn’t inspire trust in the system.
整合性の問題はほぼ解決されますが、システムに対する信頼は得られません。
Imagine a teacher who gives you consistent scores only if that teacher sits in one particular room.
その先生がある特定の部屋に座ったときだけ、安定した点数を出す先生を想像してみてください。
If that teacher sits in different rooms, that teacher’s scores for you will be wild.
その先生が違う部屋に座ると、その先生のあなたに対する点数が乱高下します。

### How to solve this ambiguity problem? この曖昧さの問題を解決するには？

This seems to be a problem that OpenAI is actively trying to mitigate.
これは、OpenAIが積極的に軽減しようとしている問題のようです。
They have a notebook with tips on how to increase their models’ reliability.
モデルの信頼性を高めるためのヒントが書かれたノートがあるそうです。

A couple of people who’ve worked with LLMs for years told me that they just accepted this ambiguity and built their workflows around that.
LLMと何年も一緒に仕事をしている人たちから、彼らはこの曖昧さを受け入れて、その上でワークフローを構築しているのだと言われました。
It’s a different mindset compared to developing deterministic programs, but not something impossible to get used to.
決定論的なプログラムを開発するのとは考え方が違いますが、慣れることができないわけではありません。

This ambiguity can be mitigated by applying as much engineering rigor as possible.
この曖昧さは、可能な限り工学的な厳密さを適用することで緩和することができます。
In the rest of this post, we’ll discuss how to make prompt engineering, if not deterministic, systematic.
この記事の続きでは、プロンプトエンジニアリングを、決定論的ではないにせよ、システム化する方法について説明します。

### Prompt evaluation 迅速な評価

A common technique for prompt engineering is to provide in the prompt a few examples and hope that the LLM will generalize from these examples (fewshot learners).
プロンプトエンジニアリングの一般的な手法は、プロンプトにいくつかの例を示し、LLMがこれらの例から一般化することを期待するものである（fewshot learners）。

As an example, consider trying to give a text a controversy score – it was a fun project that I did to find the correlation between a tweet’s popularity and its controversialness.
例えば、あるツイートの人気度と論争度の相関を調べるという楽しいプロジェクトがありました。
Here is the shortened prompt with 4 fewshot examples:
ここでは、短縮されたプロンプトと、4つの少数撮影の例を紹介します：

Example: controversy scorer
例：物議を醸すスコアラー

```
Given a text, give it a controversy score from 0 to 10.

Examples:

1 + 1 = 2
Controversy score: 0

Starting April 15th, only verified accounts on Twitter will be eligible to be in For You recommendations
Controversy score: 5

Everyone has the right to own and use guns
Controversy score: 9

Immigration should be completely banned to protect our country
Controversy score: 10

The response should follow the format:

Controversy score: { score }
Reason: { reason }

Here is the text.
```

When doing fewshot learning, two questions to keep in mind:
fewshot learningを行う場合、2つの質問に注意する必要があります：

- 1. Whether the LLM understands the examples given in the prompt. One way to evaluate this is to input the same examples and see if the model outputs the expected scores. If the model doesn’t perform well on the same examples given in the prompt, it is likely because the prompt isn’t clear – you might want to rewrite the prompt or break the task into smaller tasks (and combine them together, discussed in detail in Part II of this post). 1. LLMがプロンプトで示された例を理解しているかどうか。 評価方法としては、同じ例を入力し、モデルが期待通りのスコアを出力するかどうかを確認することです。 プロンプトで与えられた同じ例でモデルがうまく動作しない場合、プロンプトが明確でないことが考えられます。プロンプトを書き直すか、タスクを小さなタスクに分割して（この記事のパートIIで詳しく説明しますが、それらを結合して）ください。

- 2. Whether the LLM overfits to these fewshot examples. You can evaluate your model on separate examples. 2. LLMがこれらの数少ない例にオーバーフィットしているかどうか。 別の例でモデルを評価することができます。

One thing I’ve also found useful is to ask models to give examples for which it would give a certain label.
また、あるラベルを付けるとしたら、どのような例を挙げるか、モデルに聞いてみることも有効だと思います。
For example, I can ask the model to give me examples of texts for which it’d give a score of 4.
例えば、「4点をつけるような文章の例を教えてください」とモデルに頼むことができます。
Then I’d input these examples into the LLM to see if it’ll indeed output 4.
そして、これらの例をLLMに入力し、確かに4が出力されるかどうかを確認するのです。

```python
from llm import OpenAILLM

def eval_prompt(examples_file, eval_file):
    prompt = get_prompt(examples_file)
    model = OpenAILLM(prompt=prompt, temperature=0)
    compute_rmse(model, examples_file)
    compute_rmse(model, eval_file)
eval_prompt("fewshot_examples.txt", "eval_examples.txt")
```

### Prompt versioning プロンプト・バージョニング

Small changes to a prompt can lead to very different results.
プロンプトを少し変えるだけで、結果が大きく変わる。
It’s essential to version and track the performance of each prompt.
各プロンプトのパフォーマンスをバージョンアップして追跡することが不可欠です。
You can use git to version each prompt and its performance, but I wouldn’t be surprised if there will be tools like MLflow or Weights & Biases for prompt experiments.
各プロンプトとその性能はgitでバージョン管理できますが、MLflowやWeights & Biasesのようなプロンプト実験用のツールが登場しても不思議ではありませんね。

### Prompt optimization プロンプトの最適化

There have been many papers + blog posts written on how to optimize prompts.
プロンプトを最適化する方法については、これまで多くの論文＋ブログ記事が書かれてきました。
I agree with Lilian Weng in her helpful blog post that most papers on prompt engineering are tricks that can be explained in a few sentences.
プロンプトエンジニアリングの論文の多くは、数センテンスで説明できるようなトリックであるという、Lilian Wengさんの参考になるブログ記事に同意するものです。
OpenAI has a great notebook that explains many tips with examples.
OpenAIには、多くのTipsを実例で解説した素晴らしいノートブックがあります。
Here are some of them:
その一部をご紹介します：

- Prompt the model to explain or explain step-by-step how it arrives at an answer, a technique known as Chain-of-Thought or COT (Wei et al., 2022). Tradeoff: COT can increase both latency and cost due to the increased number of output tokens [see Cost and latency section] 思考連鎖（Chain-of-Thought）またはCOT（Wei et al, 2022）として知られる手法で、モデルが答えにたどり着く方法を段階的に説明または解説するように促します（※）。 トレードオフ：COTは、出力トークンの数が増えるため、レイテンシーとコストの両方が増加する可能性があります[コストとレイテンシーの項を参照]。

- Generate many outputs for the same input. Pick the final output by either the majority vote (also known as self-consistency technique by Wang et al., 2023) or you can ask your LLM to pick the best one. In OpenAI API, you can generate multiple responses for the same input by passing in the argument n (not an ideal API design if you ask me). 同じ入力に対して、多くの出力を生成する。 多数決（Wang et al., 2023による自己無撞着技法としても知られる）で最終出力を選ぶか、LLMに最適なものを選んでもらうか。 OpenAI APIでは、引数nを渡すことで、同じ入力に対して複数のレスポンスを生成することができます（私に言わせれば、理想のAPI設計ではありません）。

- Break one big prompt into smaller, simpler prompts. 一つの大きなプロンプトを、より小さな、よりシンプルなプロンプトに分割する。

Many tools promise to auto-optimize your prompts – they are quite expensive and usually just apply these tricks.
多くのツールがプロンプトの自動最適化を約束してくれますが、それらはかなり高価で、通常はこれらのトリックを適用するだけです。
One nice thing about these tools is that they’re no code, which makes them appealing to non-coders.
これらのツールの良いところは、コードがないことで、ノンコーダーの方にも魅力的なところです。

## Cost and latency コストとレイテンシー

### Cost コスト

The more explicit detail and examples you put into the prompt, the better the model performance (hopefully), and the more expensive your inference will cost.
プロンプトに明示的な詳細や例を入れれば入れるほど、モデルの性能は（うまくいけば）良くなり、推論にかかるコストは高くなります。

OpenAI API charges for both the input and output tokens.
OpenAI APIは、入力トークンと出力トークンの両方に課金されます。
Depending on the task, a simple prompt might be anything between 300 - 1000 tokens.
タスクにもよりますが、簡単なプロンプトであれば、300～1000トークン程度で済むかもしれません。
If you want to include more context, e.g.adding your own documents or info retrieved from the Internet to the prompt, it can easily go up to 10k tokens for the prompt alone.
さらに、プロンプトに自分の文書やインターネットから取得した情報を加えるなど、より多くのコンテキストを含めると、プロンプトだけで10kトークンに達することもあります。

The cost with long prompts isn’t in experimentation but in inference.
長いプロンプトでかかるコストは、実験ではなく、推論にあるのです。

Experimentation-wise, prompt engineering is a cheap and fast way get something up and running.
実験的には、プロンプトエンジニアリングは安価で素早く何かを立ち上げることができる方法です。
For example, even if you use GPT-4 with the following setting, your experimentation cost will still be just over $300.
例えば、GPT-4を以下のような設定で使用したとしても、実験費用は300円強になります。
The traditional ML cost of collecting data and training models is usually much higher and takes much longer.
従来のMLでは、データの収集やモデルのトレーニングにかかるコストは、通常、はるかに高く、時間もかかる。

- Prompt: 10k tokens ($0.06/1k tokens) プロンプト 10kトークン（0.06ドル/1kトークン)

- Output: 200 tokens ($0.12/1k tokens) 出力する： 200トークン（0.12ドル/1kトークン）

- Evaluate on 20 examples 20の例で評価する

- Experiment with 25 different versions of prompts プロンプトの25種類のバージョンで実験

The cost of LLMOps is in inference.
LLMOpsのコストは推論にある。

- If you use GPT-4 with 10k tokens in input and 200 tokens in output, it’ll be $0.624 / prediction. GPT-4を入力10kトークン、出力200トークンで使用した場合、$0.624/予測になります。

- If you use GPT-3.5-turbo with 4k tokens for both input and output, it’ll be $0.004 / prediction or $4 / 1k predictions. GPT-3.5-turboで入力・出力ともに4kトークンを使った場合、0.004ドル/予測、4ドル/1k予測になるそうです。

- As a thought exercise, in 2021, DoorDash ML models made 10 billion predictions a day. If each prediction costs $0.004, that’d be $40 million a day! 思考訓練として、2021年、DoorDashのMLモデルは1日に100億回の予測を行った。 1回の予測に0.004ドルかかるとすると、1日4,000万ドル！

- By comparison, AWS personalization costs about $0.0417 / 1k predictions and AWS fraud detection costs about $7.5 / 1k predictions [for over 100,000 predictions a month]. AWS services are usually considered prohibitively expensive (and less flexible) for any company of a moderate scale. これに対し、AWSのパーソナライゼーションは約0.0417ドル/1k予測、AWSの不正検知は約7.5ドル/1k予測［月10万予測以上の場合］のコストがかかります。 AWSのサービスは、通常、中程度の規模の企業であれば、法外に高価（かつ柔軟性に欠ける）だと考えられています。

### Latency レイテンシー

Input tokens can be processed in parallel, which means that input length shouldn’t affect the latency that much.
入力トークンは並列処理できるので、入力の長さはそれほどレイテンシーに影響しないはずです。

However, output length significantly affects latency, which is likely due to output tokens being generated sequentially.
しかし、出力長がレイテンシーに大きく影響しており、これは出力トークンが順次生成されることに起因していると考えられる。

Even for extremely short input (51 tokens) and output (1 token), the latency for gpt-3.5-turbo is around 500ms.
極端に短い入力（51トークン）と出力（1トークン）でも、gpt-3.5-turboのレイテンシーは500ms程度です。
If the output token increases to over 20 tokens, the latency is over 1 second.
出力されるトークンが20個以上に増えると、レイテンシは1秒以上になります。

Here’s an experiment I ran, each setting is run 20 times.
これは私が行った実験で、各設定を20回実行したものです。
All runs happen within 2 minutes.
すべての走行は2分以内に行われます。
If I do the experiment again, the latency will be very different, but the relationship between the 3 settings should be similar.
もう一度実験をすれば、レイテンシーは大きく変わるでしょうが、3つの設定の関係は似ているはずです。

This is another challenge of productionizing LLM applications using APIs like OpenAI: APIs are very unreliable, and no commitment yet on when SLAs will be provided.F
これは、OpenAIのようなAPIを使ったLLMアプリケーションのプロダクション化のもう一つの課題です。APIは非常に信頼性が低く、SLAがいつ提供されるのか、まだ約束されていません。

It is, unclear, how much of the latency is due to model, networking (which I imagine is huge due to high variance across runs), or some just inefficient engineering overhead.
遅延のうち、モデルやネットワーク（実行時のばらつきが大きいため、膨大な量になると思われる）、あるいは単に非効率なエンジニアリングのオーバーヘッドによるものがどの程度あるのかは不明です。
It’s very possible that the latency will reduce significantly in a near future.
近い将来、レイテンシーが大幅に短縮される可能性は大いにありますね。

While half a second seems high for many use cases, this number is incredibly impressive given how big the model is and the scale at which the API is being used.
多くのユースケースで0.5秒は高いと思われますが、モデルの大きさやAPIの使用規模を考えると、この数字は信じられないほど印象的です。
The number of parameters for gpt-3.5-turbo isn’t public but is guesstimated to be around 150B.
gpt-3.5-turboのパラメータ数は公開されていませんが、150B程度と推測されます。
As of writing, no open-source model is that big.
執筆時点では、オープンソースのモデルでそこまで大きなものはありません。
Google’s T5 is 11B parameters and Facebook’s largest LLaMA model is 65B parameters.
GoogleのT5は11Bパラメータ、Facebookの最大LLaMAモデルは65Bパラメータです。
People discussed on this GitHub thread what configuration they needed to make LLaMA models work, and it seemed like getting the 30B parameter model to work is hard enough.
このGitHubのスレッドで、LLaMAモデルを動作させるために必要な構成が議論されましたが、30Bパラメータモデルを動作させるのは難しいようでした。
The most successful one seemed to be randaller who was able to get the 30B parameter model work on 128 GB of RAM, which takes a few seconds just to generate one token.
最も成功したのはrandallerで、128GBのRAMで30Bのパラメータモデルを動作させることができたようですが、1つのトークンを生成するのに数秒かかっています。

### The impossibility of cost + latency analysis for LLMs LLMのコスト＋レイテンシ解析の不可能性

The LLM application world is moving so fast that any cost + latency analysis is bound to go outdated quickly.
LLMアプリケーションの世界はとても速く動いているので、コスト＋レイテンシーの分析はすぐに時代遅れになるに違いない。
Matt Ross, a senior manager of applied research at Scribd, told me that the estimated API cost for his use cases has gone down two orders of magnitude over the last year.
Scribdの応用研究担当シニアマネージャーであるマット・ロス氏は、彼のユースケースにおけるAPIコストの見積もりは、この1年で2桁下がったと教えてくれた。
Latency has significantly decreased as well.
レイテンシーも大幅に減少しています。
Similarly, many teams have told me they feel like they have to redo the feasibility estimation and buy (using paid APIs) vs.
同様に、多くのチームから、フィージビリティの見積もりをやり直し、（有料APIを使った）購入と比較する必要があるように感じると言われました。
build (using open source models) decision every week.
ビルド（オープンソースモデルを使用）の決定を毎週行います。

## Prompting vs. finetuning vs. alternatives プロンプティング vs. finetuning vs. 選択肢

- Prompting: for each sample, explicitly tell your model how it should respond. プロンプティング：各サンプルに対して、モデルがどう反応すべきかを明示的に指示する。

- Finetuning: train a model on how to respond, so you don’t have to specify that in your prompt. Finetuning：対応方法をモデルで訓練しておけば、プロンプトでそれを指定する必要はない。

There are 3 main factors when considering prompting vs.
プロンプトvsプロンプトを考える場合、大きく3つの要素があります。
finetuning: data availability, performance, and cost.
微調整：データの可用性、パフォーマンス、コスト。

If you have only a few examples, prompting is quick and easy to get started.
事例が少ない場合は、プロンプトが手っ取り早く、簡単に始められます。
There’s a limit to how many examples you can include in your prompt due to the maximum input token length.
入力トークンの長さの上限があるため、プロンプトに含めることができる例文には限りがあります。

The number of examples you need to finetune a model to your task, of course, depends on the task and the model.
モデルをタスクに合わせて微調整するために必要な例の数は、もちろんタスクとモデルによって異なります。
In my experience, however, you can expect a noticeable change in your model performance if you finetune on 100s examples.
しかし、私の経験では、100個の例で微調整を行えば、モデルの性能に顕著な変化が期待できます。
However, the result might not be much better than prompting.
しかし、結果はプロンプトとあまり変わらないかもしれません。

In How Many Data Points is a Prompt Worth? (2021), ​​Scao and Rush found that a prompt is worth approximately 100 examples (caveat: variance across tasks and models is high – see image below).
How Many Data Points is a Prompt Worth? (2021)で、ScaoとRushは、プロンプトは約100例の価値があることを明らかにしました（注意点：タスクやモデルによる分散は大きい - 下の画像を参照）。
The general trend is that as you increase the number of examples, finetuning will give better model performance than prompting.
一般的な傾向として、例数を増やすと、プロンプトよりもファインチューニングの方がモデル性能が向上することがわかります。
There’s no limit to how many examples you can use to finetune a model.
モデルの微調整に使う例は無限にあります。

The benefit of finetuning is two folds:
ファインチューニングのメリットは2つあります：

- You can get better model performance: can use more examples, examples becoming part of the model’s internal knowledge. より良いモデル性能を得ることができる：より多くの例を使用することができ、例はモデルの内部知識の一部となる。

- You can reduce the cost of prediction. The more instruction you can bake into your model, the less instruction you have to put into your prompt. Say, if you can reduce 1k tokens in your prompt for each prediction, for 1M predictions on gpt-3.5-turbo, you’d save $2000. 予測コストを下げることができます。 モデルにインストラクションを焼き付けることができれば、プロンプトに入れるインストラクションは少なくなります。 例えば、gpt-3.5-turboで1Mの予測をする場合、予測ごとにプロンプトのトークンを1k減らすことができれば、2000ドルの節約になりますね。

### Prompt tuning プロンプトチューニング

A cool idea that is between prompting and finetuning is prompt tuning, introduced by Leister et al.in 2021.
プロンプトとファインチューニングの中間に位置するクールなアイデアとして、2021年にLeisterらによって紹介されたプロンプトチューニングがあります。
Starting with a prompt, instead of changing this prompt, you programmatically change the embedding of this prompt.
プロンプトを起点に、このプロンプトを変更するのではなく、このプロンプトの埋め込みをプログラム的に変更する。
For prompt tuning to work, you need to be able to input prompts’ embeddings into your LLM model and generate tokens from these embeddings, which currently, can only be done with open-source LLMs and not in OpenAI API.
プロンプトチューニングを行うには、プロンプトの埋め込みをLLMモデルに入力し、その埋め込みからトークンを生成する必要がありますが、現状ではオープンソースのLLMでしか行えず、OpenAI APIでは行えないようになっています。
On T5, prompt tuning appears to perform much better than prompt engineering and can catch up with model tuning (see image below).
T5では、プロンプトチューニングはプロンプトエンジニアリングよりもはるかに性能が良く、モデルチューニングに追いつくことができるようです（下の画像参照）。

### Finetuning with distillation 蒸留による微調整

In March 2023, a group of Stanford students released a promising idea: finetune a smaller open-source language model (LLaMA-7B, the 7 billion parameter version of LLaMA) on examples generated by a larger language model (text-davinci-003 – 175 billion parameters).
2023年3月、スタンフォード大学の学生グループが、より大きな言語モデル（text-davinci-003 - 1750億パラメータ）が生成した例に対して、より小さなオープンソースの言語モデル（LLaMA-7B、LLaMAの70億パラメータ版）を微調整するという有望なアイデアを発表しました。
This technique of training a small model to imitate the behavior of a larger model is called distillation.
このように、小さなモデルを訓練して大きなモデルの挙動を模倣させる手法を「ディスティレーション」と呼びます。
The resulting finetuned model behaves similarly to text-davinci-003, while being a lot smaller and cheaper to run.
その結果、text-davinci-003と同様の挙動を示しながら、より小さく、より安く動作するようになりました。

For finetuning, they used 52k instructions, which they inputted into text-davinci-003 to obtain outputs, which are then used to finetune LLaMa-7B.
ファインチューニングには52k命令を使用し、text-davinci-003に入力して出力を得て、LLaMa-7Bのファインチューニングに使用しました。
This costs under $500 to generate.
これは生成するのに500円以下のコストです。
The training process for finetuning costs under $100.
ファインチューニングのためのトレーニング工程は100ドル以下です。
See Stanford Alpaca: An Instruction-following LLaMA Model (Taori et al., 2023).
スタンフォード・アルパカを参照してください： An Instruction-following LLaMA Model (Taori et al., 2023)を参照のこと。

The appeal of this approach is obvious.
このアプローチの魅力は明白です。
After 3 weeks, their GitHub repo got almost 20K stars!! By comparison, HuggingFace’s transformers repo took over a year to achieve a similar number of stars, and TensorFlow repo took 4 months.
3週間後、彼らのGitHubレポはほぼ20Kのスターを獲得しました！これに対して、HuggingFaceのtransformersレポは同様のスター数を達成するのに1年以上かかり、TensorFlowレポは4ヶ月かかっています。

## Embeddings + vector databases エンベッディング＋ベクターデータベース

One direction that I find very promising is to use LLMs to generate embeddings and then build your ML applications on top of these embeddings, e.g.for search and recsys.
LLMを使って埋め込みを生成し、その上にMLアプリケーションを構築するというのが、私が非常に有望だと思う方向性の一つです。
As of April 2023, the cost for embeddings using the smaller model text-embedding-ada-002 is $0.0004/1k tokens.
2023年4月現在、より小さなモデルtext-embedding-ada-002を使用した埋め込みのコストは、0.0004ドル/1kトークンです。
If each item averages 250 tokens (187 words), this pricing means $1 for every 10k items or $100 for 1 million items.
1つのアイテムが平均250トークン（187ワード）だとすると、この価格設定は10kアイテムごとに1ドル、100万アイテムで100ドルということになります。

While this still costs more than some existing open-source models, this is still very affordable, given that:
それでも既存のオープンソースモデルに比べればコストはかかりますが、それを考えれば非常に手頃な価格と言えます：

- 1. You usually only have to generate the embedding for each item once. 1. 通常、各アイテムのエンベッディングを生成するのは1回で済みます。

- 2. With OpenAI API, it’s easy to generate embeddings for queries and new items in real-time. 2. OpenAI APIを使えば、クエリや新規項目に対する埋め込みをリアルタイムで簡単に生成できます。

To learn more about using GPT embeddings, check out SGPT (Niklas Muennighoff, 2022) or this analysis on the performance and cost GPT-3 embeddings (Nils Reimers, 2022).
GPTエンベッディングの使用については、SGPT（Niklas Muennighoff、2022年）または性能とコストに関するこの分析GPT-3エンベッディング（Nils Reimers、2022年）をご覧ください。
Some of the numbers in Nils’ post are already outdated (the field is moving so fast!!), but the method is great!
ニルスさんの投稿の中には、すでに古くなっている数字もありますが（現場の動きは早い！！）、その手法は素晴らしいです！

The main cost of embedding models for real-time use cases is loading these embeddings into a vector database for low-latency retrieval.
リアルタイムユースケースのための埋め込みモデルの主なコストは、これらの埋め込みを低遅延で検索するためにベクトルデータベースにロードすることです。
However, you’ll have this cost regardless of which embeddings you use.
ただし、どのエンベッディングを使っても、この費用は発生します。
It’s exciting to see so many vector databases blossoming – the new ones such as Pinecone, Qdrant, Weaviate, Chroma as well as the incumbents Faiss, Redis, Milvus, ScaNN.
Pinecone、Qdrant、Weaviate、Chromaといった新しいものから、Faiss、Redis、Milvus、ScaNNといった既存のものまで、多くのベクターデータベースが開花しているのを見ると、わくわくしますね。

If 2021 was the year of graph databases, 2023 is the year of vector databases.
2021年がグラフデータベースの年だとしたら、2023年はベクトルデータベースの年です。

## Backward and forward compatibility 後方互換性と前方互換性

Foundational models can work out of the box for many tasks without us having to retrain them as much.
基礎的なモデルは、私たちが再教育することなく、多くのタスクですぐに機能することができます。
However, they do need to be retrained or finetuned from time to time as they go outdated.
しかし、時代とともに再教育や微調整が必要になることもあります。
According to Lilian Weng’s Prompt Engineering post:
Lilian WengのPrompt Engineeringの投稿によると：

One observation with SituatedQA dataset for questions grounded in different dates is that despite LM (pretraining cutoff is year 2020) has access to latest information via Google Search, its performance on post-2020 questions are still a lot worse than on pre-2020 questions.
SituatedQAデータセットで、異なる日付に根拠を持つ質問について観察したところ、LM（学習前のカットオフは2020年）はGoogle検索で最新の情報にアクセスできるにもかかわらず、2020年以降の質問に対するパフォーマンスは2020年以前の質問よりずっと悪いことがわかりました。
This suggests the existence of some discrepencies or conflicting parametric between contextual information and model internal knowledge.
このことは、文脈情報とモデル内部知識の間に、何らかの矛盾や相反するパラメトリックが存在することを示唆しています。

In traditional software, when software gets an update, ideally it should still work with the code written for its older version.
従来のソフトウェアでは、ソフトウェアがアップデートされたとき、理想的にはその古いバージョンのために書かれたコードでまだ動作するはずです。
However, with prompt engineering, if you want to use a newer model, there’s no way to guarantee that all your prompts will still work as intended with the newer model, so you’ll likely have to rewrite your prompts again.
しかし、プロンプトエンジニアリングでは、新しい機種を使いたい場合、すべてのプロンプトが新しい機種でも意図したとおりに動作することを保証する方法はないので、プロンプトをもう一度書き直すことになる可能性があります。
If you expect the models you use to change at all, it’s important to unit-test all your prompts using evaluation examples.
もし、使用するモデルが全く変わらないことを期待するのであれば、評価例を用いてすべてのプロンプトをユニットテストすることが重要です。

One argument I often hear is that prompt rewriting shouldn’t be a problem because:
よく聞く意見として、「プロンプトのリライトは問題ないはずだから」というものがあります：

- 1. Newer models should only work better than existing models. I’m not convinced about this. Newer models might, overall, be better, but there will be use cases for which newer models are worse. 1. 新しいモデルは、既存のモデルよりも優れた機能を備えていればいいのです。 これについては納得がいかない。 全体的には新型の方が良いかもしれませんが、新型の方が悪いというユースケースもあるはずです。

- 2. Experiments with prompts are fast and cheap, as we discussed in the section Cost. While I agree with this argument, a big challenge I see in MLOps today is that there’s a lack of centralized knowledge for model logic, feature logic, prompts, etc. An application might contain multiple prompts with complex logic (discussed in Part 2. Task composability). If the person who wrote the original prompt leaves, it might be hard to understand the intention behind the original prompt to update it. This can become similar to the situation when someone leaves behind a 700-line SQL query that nobody dares to touch. 2. プロンプトを使った実験は、「コスト」の項で説明したように、早く、安くできます。 この議論には賛成ですが、現在のMLOpsに見られる大きな課題は、モデルロジック、機能ロジック、プロンプトなどの知識が一元化されていないことです。 アプリケーションには、複雑なロジックを持つ複数のプロンプトが含まれる場合があります（第2回で説明します）。 タスク・コンポーザビリティ）。 元のプロンプトを書いた人が辞めてしまうと、元のプロンプトに込められた意図を理解して更新することが難しくなるかもしれません。 これは、誰かが700行のSQLクエリを残して、誰も触れないのと同じ状況になりかねません。

Another challenge is that prompt patterns are not robust to changes.
また、プロンプトパターンが変化に対してロバストでないことも課題です。
For example, many of the published prompts I’ve seen start with “I want you to act as XYZ”.
例えば、私が見てきた公開プロンプトの多くは、「XYZとして行動してほしい」というところから始まります。
If OpenAI one day decides to print something like: “I’m an AI assistant and I can’t act like XYZ”, all these prompts will need to be updated.
もしOpenAIがある日、次のようなことを印刷することに決めたら： 「私はAIアシスタントですが、XYZのように振る舞うことはできません」と印刷するようになったら、これらのプロンプトはすべて更新する必要があります。
