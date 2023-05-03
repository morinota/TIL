## link

- https://huyenchip.com/2023/04/11/llm-engineering.html#part_2_task_composability

# Part 2. Task composability

## Applications that consist of multiple tasks

The example controversy scorer above consists of one single task: given an input, output a controversy score. Most applications, however, are more complex. Consider the “talk-to-your-data” use case where we want to connect to a database and query this database in natural language. Imagine a credit card transaction table. You want to ask things like: "How many unique merchants are there in Phoenix and what are their names?" and your database will return: "There are 9 unique merchants in Phoenix and they are …".

One way to do this is to write a program that performs the following sequence of tasks:

- Task 1: convert natural language input from user to SQL query [LLM]
- Task 2: execute SQL query in the SQL database [SQL executor]
- Task 3: convert the SQL result into a natural language response to show user [LLM]

## Agents, tools, and control flows

I did a small survey among people in my network and there doesn’t seem to be any consensus on terminologies, yet.

The word agent is being thrown around a lot to refer to an application that can execute multiple tasks according to a given control flow (see Control flows section). A task can leverage one or more tools. In the example above, SQL executor is an example of a tool.

Note: some people in my network resist using the term agent in this context as it is already overused in other contexts (e.g. agent to refer to a policy in reinforcement learning).

### Tools vs. plugins

Other than SQL executor, here are more examples of tools:

search (e.g. by using Google Search API or Bing API)
web browser (e.g. given a URL, fetch its content)
bash executor
calculator
Tools and plugins are basically the same things. You can think of plugins as tools contributed to the OpenAI plugin store. As of writing, OpenAI plugins aren’t open to the public yet, but anyone can create and use tools.

### Control flows: sequential, parallel, if, for loop

In the example above, sequential is an example of a control flow in which one task is executed after another. There are other types of control flows such as parallel, if statement, for loop.

Sequential: executing task B after task A completes, likely because task B depends on Task A. For example, the SQL query can only be executed after it’s been translated from the user input.
Parallel: executing tasks A and B at the same time.
If statement: executing task A or task B depending on the input.
For loop: repeat executing task A until a certain condition is met. For example, imagine you use browser action to get the content of a webpage and keep on using browser action to get the content of links found in that webpage until the agent feels like it’s got sufficient information to answer the original question.
Note: while parallel can definitely be useful, I haven’t seen a lot of applications using it.

### Control flow with LLM agents

In traditional software engineering, conditions for control flows are exact. With LLM applications (also known as agents), conditions might also be determined by prompting.

For example, if you want your agent to choose between three actions search, SQL executor, and Chat, you might explain how it should choose one of these actions as follows (very approximate), In other words, you can use LLMs to decide the condition of the control flow!

```
You have access to three tools: Search, SQL executor, and Chat.

Search is useful when users want information about current events or products.

SQL executor is useful when users want information that can be queried from a database.

Chat is useful when users want general information.

Provide your response in the following format:

Input: { input }
Thought: { thought }
Action: { action }
Action Input: { action_input }
Observation: { action_output }
Thought: { thought }
```

### Testing an agent

For agents to be reliable, we’d need to be able to build and test each task separately before combining them. There are two major types of failure modes:

One or more tasks fail. Potential causes:
Control flow is wrong: a non-optional action is chosen
One or more tasks produce incorrect results
All tasks produce correct results but the overall solution is incorrect. Press et al. (2022) call this “composability gap”: the fraction of compositional questions that the model answers incorrectly out of all the compositional questions for which the model answers the sub-questions correctly.
Like with software engineering, you can and should unit test each component as well as the control flow. For each component, you can define pairs of (input, expected output) as evaluation examples, which can be used to evaluate your application every time you update your prompts or control flows. You can also do integration tests for the entire application.
