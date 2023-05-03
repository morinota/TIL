## link

- https://huyenchip.com/2023/04/11/llm-engineering.html

## title

Building LLM applications for production

# intro

A question that I’ve been asked a lot recently is how large language models (LLMs) will change machine learning workflows. After working with several companies who are working with LLM applications and personally going down a rabbit hole building my applications, I realized two things:

- 1. It’s easy to make something cool with LLMs, but very hard to make something production-ready with them.
- 2. LLM limitations are exacerbated by a lack of engineering rigor in prompt engineering, partially due to the ambiguous nature of natural languages, and partially due to the nascent nature of the field.

This post consists of three parts.

- Part 1 discusses the key challenges of productionizing LLM applications and the solutions that I’ve seen.
- Part 2 discusses how to compose multiple tasks with control flows (e.g. if statement, for loop) and incorporate tools (e.g. SQL executor, bash, web browsers, third-party APIs) for more complex and powerful applications.
- Part 3 covers some of the promising use cases that I’ve seen companies building on top of LLMs and how to construct them from smaller tasks.

There has been so much written about LLMs, so feel free to skip any section you’re already familiar with.
