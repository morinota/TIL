## link

- https://huyenchip.com/2023/04/11/llm-engineering.html#part_3_promising_use_cases

# Part 3. Promising use cases

The Internet has been flooded with cool demos of applications built with LLMs. Here are some of the most common and promising applications that I’ve seen. I’m sure that I’m missing a ton.

For more ideas, check out the projects from two hackathons I’ve seen:

- GPT-4 Hackathon Code Results [Mar 25, 2023]
- Langchain / Gen Mo Hackathon [Feb 25, 2023]

## AI assistant

This is hands down the most popular consumer use case. There are AI assistants built for different tasks for different groups of users – AI assistants for scheduling, making notes, pair programming, responding to emails, helping with parents, making reservations, booking flights, shopping, etc. – but, of course, the ultimate goal is an assistant that can assist you in everything.

This is also the holy grail that all big companies are working towards for years: Google with Google Assistant and Bard, Facebook with M and Blender, OpenAI (and by extension, Microsoft) with ChatGPT. Quora, which has a very high risk of being replaced by AIs, released their own app Poe that lets you chat with multiple LLMs. I’m surprised Apple and Amazon haven’t joined the race yet.

## Chatbot

Chatbots are similar to AI assistants in terms of APIs. If AI assistants’ goal is to fulfill tasks given by users, whereas chatbots’ goal is to be more of a companion. For example, you can have chatbots that talk like celebrities, game/movie/book characters, businesspeople, authors, etc.

Michelle Huang used her childhood journal entries as part of the prompt to GPT-3 to talk to the inner child.

The most interesting company in the consuming-chatbot space is probably Character.ai. It’s a platform for people to create and share chatbots. The most popular types of chatbots on the platform, as writing, are anime and game characters, but you can also talk to a psychologist, a pair programming partner, or a language practice partner. You can talk, act, draw pictures, play text-based games (like AI Dungeon), and even enable voices for characters. I tried a few popular chatbots – none of them seem to be able to hold a conversation yet, but we’re just at the beginning. Things can get even more interesting if there’s a revenue-sharing model so that chatbot creators can get paid.

## Programming and gaming

This is another popular category of LLM applications, as LLMs turn out to be incredibly good at writing and debugging code. GitHub Copilot is a pioneer (whose VSCode extension has had 5 million downloads as of writing). There have been pretty cool demos of using LLMs to write code:

- 1. Create web apps from natural languages
- 2. Find security threats: Socket AI examines npm and PyPI packages in your codebase for security threats. When a potential issue is detected, they use ChatGPT to summarize findings.
- 3. Gaming
  - 3.1 Create games: e.g. Wyatt Cheng has an awesome video showing how he used ChatGPT to clone Flappy Bird.
  - 3.2 Generate game characters.
  - 3.3 Let you have more realistic conversations with game characters: check out this awesome demo by Convai!

## Learning

Whenever ChatGPT was down, OpenAI discord is flooded with students complaining about not being to complete their homework. Some responded by banning the use of ChatGPT in school altogether. Some have a much better idea: how to incorporate ChatGPT to help students learn even faster. All EdTech companies I know are going full-speed on ChatGPT exploration.

Some use cases:

- Summarize books
- Automatically generate quizzes to make sure students understand a book or a lecture. Not only ChatGPT can generate questions, but it can also evaluate whether a student’s input answers are correct.
- I tried and ChatGPT seemed pretty good at generating quizzes for Designing Machine Learning Systems. Will publish the quizzes generated soon!
- Grade / give feedback on essays
- Walk through math solutions
- Be a debate partner: ChatGPT is really good at taking different sides of the same debate topic.

With the rise of homeschooling, I expect to see a lot of applications of ChatGPT to help parents homeschool.

## Talk-to-your-data

This is, in my observation, the most popular enterprise application (so far). Many, many startups are building tools to let enterprise users query their internal data and policies in natural languages or in the Q&A fashion. Some focus on verticals such as legal contracts, resumes, financial data, or customer support. Given a company’s all documentations, policies, and FAQs, you can build a chatbot that can respond your customer support requests.

The main way to do this application usually involves these 4 steps:

- 1. Organize your internal data into a database (SQL database, graph database, embedding/vector database, or just text database)
- 2. Given an input in natural language, convert it into the query language of the internal database. For example, if it’s a SQL or graph database, this process can return a SQL query. If it’s embedding database, it’s might be an ANN (approximate nearest neighbor) retrieval query. If it’s just purely text, this process can extract a search query.
- 3. Execute the query in the database to obtain the query result.
- 4. Translate this query result into natural language.

While this makes for really cool demos, I’m not sure how defensible this category is. I’ve seen startups building applications to let users query on top of databases like Google Drive or Notion, and it feels like that’s a feature Google Drive or Notion can implement in a week.

OpenAI has a pretty good tutorial on how to talk to your vector database.

### Can LLMs do data analysis for me?

I tried inputting some data into gpt-3.5-turbo, and it seems to be able to detect some patterns. However, this only works for small data that can fit into the input prompt. Most production data is larger than that.

## Search and recommendation

Search and recommendation has always been the bread and butter of enterprise use cases. It’s going through a renaissance with LLMs. Search has been mostly keyword-based: you need a tent, you search for a tent. But what if you don’t know what you need yet? For example, if you’re going camping in the woods in Oregon in November, you might end up doing something like this:

- 1. Search to read about other people’s experiences.
- 2. Read those blog posts and manually extract a list of items you need.
- 3. Search for each of these items, either on Google or other websites.

If you search for “things you need for camping in oregon in november” directly on Amazon or any e-commerce website, you’ll get something like this:

But what if searching for “things you need for camping in oregon in november” on Amazon actually returns you a list of things you need for your camping trip?

It’s possible today with LLMs. For example, the application can be broken into the following steps:

- Task 1: convert the user query into a list of product names [LLM]
- Task 2: for each product name in the list, retrieve relevant products from your product catalog.

If this works, I wonder if we’ll have LLM SEO: techniques to get your products recommended by LLMs.

## Sales

The most obvious way to use LLMs for sales is to write sales emails. But nobody really wants more or better sales emails. However, several companies in my network are using LLMs to synthesize information about a company to see what they need.

## SEO

SEO is about to get very weird. Many companies today rely on creating a lot of content hoping to rank high on Google. However, given that LLMs are REALLY good at generating content, and I already know a few startups whose service is to create unlimited SEO-optimized content for any given keyword, search engines will be flooded. SEO might become even more of a cat-and-mouse game: search engines come up with new algorithms to detect AI-generated content, and companies get better at bypassing these algorithms. People might also rely less on search, and more on brands (e.g. trust only the content created by certain people or companies).

And we haven’t even touched on SEO for LLMs yet: how to inject your content into LLMs’ responses!!

# Conclusion

We’re still in the early days of LLMs applications – everything is evolving so fast. I recently read a book proposal on LLMs, and my first thought was: most of this will be outdated in a month. APIs are changing day to day. New applications are being discovered. Infrastructure is being aggressively optimized. Cost and latency analysis needs to be done on a weekly basis. New terminologies are being introduced.

Not all of these changes will matter. For example, many prompt engineering papers remind me of the early days of deep learning when there were thousands of papers describing different ways to initialize weights. I imagine that tricks to tweak your prompts like: "Answer truthfully", "I want you to act like …", writing "question: " instead of "q:" wouldn’t matter in the long run.

Given that LLMs seem to be pretty good at writing prompts for themselves – see Large Language Models Are Human-Level Prompt Engineers (Zhou et al., 2022) – who knows that we’ll need humans to tune prompts?

However, given so much happening, it’s hard to know which will matter, and which won’t.

I recently asked on LinkedIn how people keep up to date with the field. The strategy ranges from ignoring the hype to trying out all the tools.

## Ignore (most of) the hype

Vicki Boykis (Senior ML engineer @ Duo Security): I do the same thing as with any new frameworks in engineering or the data landscape: I skim the daily news, ignore most of it, and wait six months to see what sticks. Anything important will still be around, and there will be more survey papers and vetted implementations that help contextualize what’s happening.

## Read only the summaries

Shashank Chaurasia (Engineering @ Microsoft): I use the Creative mode of BingChat to give me a quick summary of new articles, blogs and research papers related to Gen AI! I often chat with the research papers and github repos to understand the details.

## Try to keep up to date with the latest tools

Chris Alexiuk (Founding ML engineer @ Ox): I just try and build with each of the tools as they come out - that way, when the next step comes out, I’m only looking at the delta.

What’s your strategy?
