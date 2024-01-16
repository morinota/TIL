## link

- https://huyenchip.com/2023/04/11/llm-engineering.html#prompt_engineering_challenges

# Part I. Challenges of productionizing prompt engineering

## The ambiguity of natural languages

For most of the history of computers, engineers have written instructions in programming languages. Programming languages are “mostly” exact. Ambiguity causes frustration and even passionate hatred in developers (think dynamic typing in Python or JavaScript).

In prompt engineering, instructions are written in natural languages, which are a lot more flexible than programming languages. This can make for a great user experience, but can lead to a pretty bad developer experience.

The flexibility comes from two directions: how users define instructions, and how LLMs respond to these instructions.

First, the flexibility in user-defined prompts leads to silent failures. If someone accidentally makes some changes in code, like adding a random character or removing a line, it’ll likely throw an error. However, if someone accidentally changes a prompt, it will still run but give very different outputs.

While the flexibility in user-defined prompts is just an annoyance, the ambiguity in LLMs’ generated responses can be a dealbreaker. It leads to two problems:

- 1. Ambiguous output format: downstream applications on top of LLMs expect outputs in a certain format so that they can parse. We can craft our prompts to be explicit about the output format, but there’s no guarantee that the outputs will always follow this format.
- 2. Inconsistency in user experience: when using an application, users expect certain consistency. Imagine an insurance company giving you a different quote every time you check on their website. LLMs are stochastic – there’s no guarantee that an LLM will give you the same output for the same input every time.

You can force an LLM to give the same response by setting temperature = 0, which is, in general, a good practice. While it mostly solves the consistency problem, it doesn’t inspire trust in the system. Imagine a teacher who gives you consistent scores only if that teacher sits in one particular room. If that teacher sits in different rooms, that teacher’s scores for you will be wild.

### How to solve this ambiguity problem?

This seems to be a problem that OpenAI is actively trying to mitigate. They have a notebook with tips on how to increase their models’ reliability.

A couple of people who’ve worked with LLMs for years told me that they just accepted this ambiguity and built their workflows around that. It’s a different mindset compared to developing deterministic programs, but not something impossible to get used to.

This ambiguity can be mitigated by applying as much engineering rigor as possible. In the rest of this post, we’ll discuss how to make prompt engineering, if not deterministic, systematic.

### Prompt evaluation

A common technique for prompt engineering is to provide in the prompt a few examples and hope that the LLM will generalize from these examples (fewshot learners).

As an example, consider trying to give a text a controversy score – it was a fun project that I did to find the correlation between a tweet’s popularity and its controversialness. Here is the shortened prompt with 4 fewshot examples:

Example: controversy scorer

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

- 1. Whether the LLM understands the examples given in the prompt. One way to evaluate this is to input the same examples and see if the model outputs the expected scores. If the model doesn’t perform well on the same examples given in the prompt, it is likely because the prompt isn’t clear – you might want to rewrite the prompt or break the task into smaller tasks (and combine them together, discussed in detail in Part II of this post).
- 2. Whether the LLM overfits to these fewshot examples. You can evaluate your model on separate examples.

One thing I’ve also found useful is to ask models to give examples for which it would give a certain label. For example, I can ask the model to give me examples of texts for which it’d give a score of 4. Then I’d input these examples into the LLM to see if it’ll indeed output 4.

```python
from llm import OpenAILLM

def eval_prompt(examples_file, eval_file):
    prompt = get_prompt(examples_file)
    model = OpenAILLM(prompt=prompt, temperature=0)
    compute_rmse(model, examples_file)
    compute_rmse(model, eval_file)
eval_prompt("fewshot_examples.txt", "eval_examples.txt")
```

### Prompt versioning

Small changes to a prompt can lead to very different results. It’s essential to version and track the performance of each prompt. You can use git to version each prompt and its performance, but I wouldn’t be surprised if there will be tools like MLflow or Weights & Biases for prompt experiments.

### Prompt optimization

There have been many papers + blog posts written on how to optimize prompts. I agree with Lilian Weng in her helpful blog post that most papers on prompt engineering are tricks that can be explained in a few sentences. OpenAI has a great notebook that explains many tips with examples. Here are some of them:

- Prompt the model to explain or explain step-by-step how it arrives at an answer, a technique known as Chain-of-Thought or COT (Wei et al., 2022). Tradeoff: COT can increase both latency and cost due to the increased number of output tokens [see Cost and latency section]
- Generate many outputs for the same input. Pick the final output by either the majority vote (also known as self-consistency technique by Wang et al., 2023) or you can ask your LLM to pick the best one. In OpenAI API, you can generate multiple responses for the same input by passing in the argument n (not an ideal API design if you ask me).
- Break one big prompt into smaller, simpler prompts.

Many tools promise to auto-optimize your prompts – they are quite expensive and usually just apply these tricks. One nice thing about these tools is that they’re no code, which makes them appealing to non-coders.

## Cost and latency

### Cost

The more explicit detail and examples you put into the prompt, the better the model performance (hopefully), and the more expensive your inference will cost.

OpenAI API charges for both the input and output tokens. Depending on the task, a simple prompt might be anything between 300 - 1000 tokens. If you want to include more context, e.g. adding your own documents or info retrieved from the Internet to the prompt, it can easily go up to 10k tokens for the prompt alone.

The cost with long prompts isn’t in experimentation but in inference.

Experimentation-wise, prompt engineering is a cheap and fast way get something up and running. For example, even if you use GPT-4 with the following setting, your experimentation cost will still be just over $300. The traditional ML cost of collecting data and training models is usually much higher and takes much longer.

- Prompt: 10k tokens ($0.06/1k tokens)
- Output: 200 tokens ($0.12/1k tokens)
- Evaluate on 20 examples
- Experiment with 25 different versions of prompts

The cost of LLMOps is in inference.

- If you use GPT-4 with 10k tokens in input and 200 tokens in output, it’ll be $0.624 / prediction.
- If you use GPT-3.5-turbo with 4k tokens for both input and output, it’ll be $0.004 / prediction or $4 / 1k predictions.
- As a thought exercise, in 2021, DoorDash ML models made 10 billion predictions a day. If each prediction costs $0.004, that’d be $40 million a day!
- By comparison, AWS personalization costs about $0.0417 / 1k predictions and AWS fraud detection costs about $7.5 / 1k predictions [for over 100,000 predictions a month]. AWS services are usually considered prohibitively expensive (and less flexible) for any company of a moderate scale.

### Latency

Input tokens can be processed in parallel, which means that input length shouldn’t affect the latency that much.

However, output length significantly affects latency, which is likely due to output tokens being generated sequentially.

Even for extremely short input (51 tokens) and output (1 token), the latency for gpt-3.5-turbo is around 500ms. If the output token increases to over 20 tokens, the latency is over 1 second.

Here’s an experiment I ran, each setting is run 20 times. All runs happen within 2 minutes. If I do the experiment again, the latency will be very different, but the relationship between the 3 settings should be similar.

This is another challenge of productionizing LLM applications using APIs like OpenAI: APIs are very unreliable, and no commitment yet on when SLAs will be provided.F

It is, unclear, how much of the latency is due to model, networking (which I imagine is huge due to high variance across runs), or some just inefficient engineering overhead. It’s very possible that the latency will reduce significantly in a near future.

While half a second seems high for many use cases, this number is incredibly impressive given how big the model is and the scale at which the API is being used. The number of parameters for gpt-3.5-turbo isn’t public but is guesstimated to be around 150B. As of writing, no open-source model is that big. Google’s T5 is 11B parameters and Facebook’s largest LLaMA model is 65B parameters. People discussed on this GitHub thread what configuration they needed to make LLaMA models work, and it seemed like getting the 30B parameter model to work is hard enough. The most successful one seemed to be randaller who was able to get the 30B parameter model work on 128 GB of RAM, which takes a few seconds just to generate one token.

### The impossibility of cost + latency analysis for LLMs

The LLM application world is moving so fast that any cost + latency analysis is bound to go outdated quickly. Matt Ross, a senior manager of applied research at Scribd, told me that the estimated API cost for his use cases has gone down two orders of magnitude over the last year. Latency has significantly decreased as well. Similarly, many teams have told me they feel like they have to redo the feasibility estimation and buy (using paid APIs) vs. build (using open source models) decision every week.

## Prompting vs. finetuning vs. alternatives

- Prompting: for each sample, explicitly tell your model how it should respond.
- Finetuning: train a model on how to respond, so you don’t have to specify that in your prompt.

There are 3 main factors when considering prompting vs. finetuning: data availability, performance, and cost.

If you have only a few examples, prompting is quick and easy to get started. There’s a limit to how many examples you can include in your prompt due to the maximum input token length.

The number of examples you need to finetune a model to your task, of course, depends on the task and the model. In my experience, however, you can expect a noticeable change in your model performance if you finetune on 100s examples. However, the result might not be much better than prompting.

In How Many Data Points is a Prompt Worth? (2021), ​​Scao and Rush found that a prompt is worth approximately 100 examples (caveat: variance across tasks and models is high – see image below). The general trend is that as you increase the number of examples, finetuning will give better model performance than prompting. There’s no limit to how many examples you can use to finetune a model.

The benefit of finetuning is two folds:

- You can get better model performance: can use more examples, examples becoming part of the model’s internal knowledge.
- You can reduce the cost of prediction. The more instruction you can bake into your model, the less instruction you have to put into your prompt. Say, if you can reduce 1k tokens in your prompt for each prediction, for 1M predictions on gpt-3.5-turbo, you’d save $2000.

### Prompt tuning

A cool idea that is between prompting and finetuning is prompt tuning, introduced by Leister et al. in 2021. Starting with a prompt, instead of changing this prompt, you programmatically change the embedding of this prompt. For prompt tuning to work, you need to be able to input prompts’ embeddings into your LLM model and generate tokens from these embeddings, which currently, can only be done with open-source LLMs and not in OpenAI API. On T5, prompt tuning appears to perform much better than prompt engineering and can catch up with model tuning (see image below).

### Finetuning with distillation

In March 2023, a group of Stanford students released a promising idea: finetune a smaller open-source language model (LLaMA-7B, the 7 billion parameter version of LLaMA) on examples generated by a larger language model (text-davinci-003 – 175 billion parameters). This technique of training a small model to imitate the behavior of a larger model is called distillation. The resulting finetuned model behaves similarly to text-davinci-003, while being a lot smaller and cheaper to run.

For finetuning, they used 52k instructions, which they inputted into text-davinci-003 to obtain outputs, which are then used to finetune LLaMa-7B. This costs under $500 to generate. The training process for finetuning costs under $100. See Stanford Alpaca: An Instruction-following LLaMA Model (Taori et al., 2023).

The appeal of this approach is obvious. After 3 weeks, their GitHub repo got almost 20K stars!! By comparison, HuggingFace’s transformers repo took over a year to achieve a similar number of stars, and TensorFlow repo took 4 months.

## Embeddings + vector databases

One direction that I find very promising is to use LLMs to generate embeddings and then build your ML applications on top of these embeddings, e.g. for search and recsys. As of April 2023, the cost for embeddings using the smaller model text-embedding-ada-002 is $0.0004/1k tokens. If each item averages 250 tokens (187 words), this pricing means $1 for every 10k items or $100 for 1 million items.

While this still costs more than some existing open-source models, this is still very affordable, given that:

- 1. You usually only have to generate the embedding for each item once.
- 2. With OpenAI API, it’s easy to generate embeddings for queries and new items in real-time.

To learn more about using GPT embeddings, check out SGPT (Niklas Muennighoff, 2022) or this analysis on the performance and cost GPT-3 embeddings (Nils Reimers, 2022). Some of the numbers in Nils’ post are already outdated (the field is moving so fast!!), but the method is great!

The main cost of embedding models for real-time use cases is loading these embeddings into a vector database for low-latency retrieval. However, you’ll have this cost regardless of which embeddings you use. It’s exciting to see so many vector databases blossoming – the new ones such as Pinecone, Qdrant, Weaviate, Chroma as well as the incumbents Faiss, Redis, Milvus, ScaNN.

If 2021 was the year of graph databases, 2023 is the year of vector databases.

## Backward and forward compatibility

Foundational models can work out of the box for many tasks without us having to retrain them as much. However, they do need to be retrained or finetuned from time to time as they go outdated. According to Lilian Weng’s Prompt Engineering post:

One observation with SituatedQA dataset for questions grounded in different dates is that despite LM (pretraining cutoff is year 2020) has access to latest information via Google Search, its performance on post-2020 questions are still a lot worse than on pre-2020 questions. This suggests the existence of some discrepencies or conflicting parametric between contextual information and model internal knowledge.

In traditional software, when software gets an update, ideally it should still work with the code written for its older version. However, with prompt engineering, if you want to use a newer model, there’s no way to guarantee that all your prompts will still work as intended with the newer model, so you’ll likely have to rewrite your prompts again. If you expect the models you use to change at all, it’s important to unit-test all your prompts using evaluation examples.

One argument I often hear is that prompt rewriting shouldn’t be a problem because:

- 1. Newer models should only work better than existing models. I’m not convinced about this. Newer models might, overall, be better, but there will be use cases for which newer models are worse.
- 2. Experiments with prompts are fast and cheap, as we discussed in the section Cost. While I agree with this argument, a big challenge I see in MLOps today is that there’s a lack of centralized knowledge for model logic, feature logic, prompts, etc. An application might contain multiple prompts with complex logic (discussed in Part 2. Task composability). If the person who wrote the original prompt leaves, it might be hard to understand the intention behind the original prompt to update it. This can become similar to the situation when someone leaves behind a 700-line SQL query that nobody dares to touch.

Another challenge is that prompt patterns are not robust to changes. For example, many of the published prompts I’ve seen start with “I want you to act as XYZ”. If OpenAI one day decides to print something like: “I’m an AI assistant and I can’t act like XYZ”, all these prompts will need to be updated.
