## refs

https://www.activeloop.ai/resources/use-llama-index-to-build-an-ai-shopping-assistant-with-rag-and-agents/

# Use LlamaIndex to Build an AI Shopping Assistant with RAG and Agents

Build an AI Shopping Assistant to Personalize and Maximize Online E-commerce Sales with GPT-4V, LlamaIndex, and Deep Lake. Budget, Weather & Look Optimization.

In the ever-expanding landscape of artificial intelligence, vector databases stand as the unsung heroes, forming the foundation upon which many AI applications are built. These powerful databases provide the capacity to store and retrieve complex, high-dimensional data, enabling functionalities like Retrieval Augmented Generation (RAG) and sophisticated recommendation systems, covered in depth in our Advanced Retrieval Augmented Generation course, which this article is a part of.

Alongside vector databases, Large Language Model (LLM) frameworks such as LlamaIndex and LangChain have emerged as key players in accelerating AI development. By simplifying the prototyping process and reducing development overheads associated with API interactions and data formatting, these frameworks allow creators to focus on innovation rather than the intricacies of implementation.

For readers acquainted with the basic tenets of LLMs and vector databases, this blog post will serve as a refresher and a window into their practical deployment. We aim to walk you through constructing a complex and interactive shopping assistant. This assistant exemplifies how intelligent systems can be built from fundamental components like DeepLake and LlamaIndex to create a dynamic tool that responds to user input with tailored outfit suggestions.

Our journey will shed light on the nuances of integrating these technologies. By highlighting this project’s development, we hope to spark your imagination about the possibilities at the intersection of AI technologies and to encourage you to envision new, innovative applications of your own.

## Project Overview
Our project is an AI-powered shopping assistant (follow the GitHub repo here) designed to leverage image processing and LLM agents for outfit recommendations. Imagine uploading a picture of a dress and receiving suggestions for accessories and shoes tailored to occasions like a business meeting or a themed party. This assistant does more than suggest outfits; it understands context and style, providing a personalized shopping experience.

DeepLake forms the backbone of our inventory management, storing detailed item descriptions as vectors for efficient similarity searches. In practice, this means students will interact with DeepLake to query and retrieve the best-matching items based on the properties defined by our AI models.

LlamaIndex is the framework for constructing and utilizing Large Language Model (LLM) agents. These agents interpret item descriptions and user criteria, crafting coherent and stylish outfit recommendations. Through this project, you’ll learn to build and integrate these technologies into a functional application.

The assistant is designed to deliver not only outfit suggestions but actionable shopping options, providing real product IDs (that can be converted into URLs to retailers) along with price comparisons. Throughout the course, you will learn how to extend the AI’s capabilities to facilitate an end-to-end shopping experience.

The user interface of this application is designed with functionality and educational value in mind. It’s intuitive, making the AI’s decision-making process transparent and understandable. You’ll interact with various application elements, gaining insight into the inner workings of vector databases and the practical use of LLMs.

## Architecture design
Our application is designed around the Agent framework: we use an LLM as a reasoning agent, and then we provide the agent with tools, i.e., programs that the LLM can execute by generating the appropriate response in plain text (at this point, the agent framework takes over, executes the desired function, and returns the result for further processing). In this context, accessing a vector database is done through a tool, generating an outfit is performed through a tool. Even getting the today’s date is performed through a tool.

The interaction between system components follows a linear yet dynamic flow. Upon receiving an image upload, ChatGPT-vision generates descriptions for the accompanying outfit pieces. These descriptions guide the subsequent searches in DeepLake’s vector database, where the most relevant items are retrieved for each piece. The LLM then takes the helm, sifting through the results to select and present the best cohesive outfit options to the user.

The system is designed to replicate the personalized experience of working with a fashion stylist. When a user uploads a garment image, our AI stylist gets to work. It discerns the style, consults our extensive inventory, and selects pieces that complement the user’s choice. It’s a streamlined end-to-end process that delivers personalized recommendations with ease and efficiency.

## Dataset Collection and Vector Database Population
Our data journey begins with Apify, a versatile web scraping tool we used to collect product information from Walmart’s online catalog. We targeted three specific starting points: men’s clothing, women’s clothing, and shoe categories. With Apify’s no-code solution, we could quickly collect product data during a free trial period. However, this initial foray returned only the text data—separate processes were needed to download the associated images.


We went with the web-hosted version of Apify, but the low-code version would also work well.

We aimed to construct a representative dataset of men’s and women’s clothing, including various tops, bottoms, and accessories. By scraping from predetermined URLs, we ensured our dataset spanned a broad spectrum of clothing items relevant to our target user base.

The collected data is fairly rich and contains a wide variety of attributes. For the purpose of this project, we kept the attributes used to a minimum. We selected the product ID, category, price, name, and image. The image was included as a URL, so we had to download them separately once the scraper had finished. Overall, we collected 1344 items.

We used pandas to read the scraped JSONs and clean the collected data. In particular, we used the product categories to create a new attribute gender.

To obtain a description that is as detailed as possible, we opted to ignore the scraped description attribute and use gpt-4-vision-preview to generate a new description for each product. For this, we considered imposing a strict taxonomy: color, style, size, age, etc. Ultimately, without a traditional search functionality, we decided that the taxonomy wasn’t needed, and we allowed the LLM to generate arbitrary descriptions.

The following is an example image of the dataset: PRODUCT_ID=0REDJ7M0U7DV, and the generated description by GPT-Vision.

Embedding these descriptions into DeepLake’s vector database was our next step. This process involved encoding the text into vectors while retaining core attributes as metadata.

Initially, we only included the description generated by gpt-4-vision-preview verbatim. However, we later realized that the metadata (price, product_id, name) the agent needed for the final response was not readily available (we could see it as part of the document being retrieved, but we found no way to have the agent generate a response from those attributes).

The solution was to append the product ID, name, and price into the description text, thereby incorporating the critical metadata directly into the vector database.

Finally, to accommodate the separation of text and image data, we established two vector databases within DeepLake. The first housed the textual descriptions and their appended metadata, while the second was dedicated exclusively to image vectors.

## Development of core tools
When using an Agent-based framework, tools are the bread and butter of the system.

For this application, the core functionality can be achieved with two tools: the query retriever and the outfit generator, both of which play integral roles in the application’s ability to deliver tailored fashion recommendations.

# Inventory query engine
The inventory query retriever is a text-based wrapper around DeepLake’s API. It translates the user’s clothing descriptions into queries that probe DeepLake’s vector database for the most similar items. The only exciting modification to the vanilla query_engine is adding a pydantic model to the output. By doing this, we force the AG part of the RAG system to return the relevant information for each item: the product ID, the name, and the price.

Notice the description on each BaseModel? Those are mandatory when using pydantic with the query engine. We learned this the hard way after finding several strange “missing description errors.”
Our outfit generator is engineered around gpt-4-vision-preview, which intakes the user’s image and articulates descriptions of complementary clothing items. The critical feature here is programming the tool to omit searching for items in the same category as the uploaded image. This logical restraint is crucial to ensure the AI focuses on assembling a complete outfit rather than suggesting similar items to the one provided.

When working with agents, debugging and fixing errors is particularly difficult because of their dynamic nature. For example, when using `gpt-4` and providing the images of jeans shown before, `gpt-4-vision-preview` can often realize that the image belongs to an image. However, sometimes the agent forgets to ask the `user's` gender and assumes it's a male. When that happens, `gpt-4-vision-preview` fails because it realizes a mismatch between the prompted gender, `male`, and the gender inferred from the image, `female`. Here we can see some of the biases of large language models at play and how they can suddenly break an application
Adding user preferences like occasion or style into the prompts is done with a straightforward approach. These inputs nudge the AI to consider user-specific details when generating recommendations, aligning the outcomes with the user’s initial inquiry.

The system functionality unfolds with the LLM agent at the helm. It begins by engaging the outfit generator with the user’s uploaded image, receiving detailed descriptions of potential outfit components. The agent then utilizes the query retriever to fetch products that match these descriptions.

## System integration and initial testing
The successful integration of various AI components into a seamless shopping assistant experience required a straightforward approach: encapsulating each function into a tool and crafting an agent to orchestrate these tools.

# LlamaIndex Agent creation and integration process
Tool wrapping: Each functional element of our application, from image processing to querying the vector database, was wrapped as an isolated, callable Tool.
Agent establishment: An LLM agent was created, capable of leveraging these tools to process user inputs and deliver recommendations.

# Initial testing challenges
Our testing phase provided valuable insights, particularly with our initial use of ChatGPT 3.5. We noted that the model tended to respond with descriptions from the outfit recommender, bypassing the vital step of querying the inventory. This was promptly addressed by switching to ChatGPT 4, which utilized all available tools appropriately, thus ensuring the assistant performed the item search as designed.

💡 Using `gpt-3.5-turbo` resulted in the agent not using all the tools. To achieve the expected results, we had to use `gpt-4`.

# Demo: Step-by-step commands and interactions
Below is a demonstration of the system in action, detailing the commands issued to the agent and their corresponding answers at each stage of the process:

Image upload and description generation

Currently, the process of uploading the image is separate. For this version to work, an image needs to exist in the local folder .image_input/. When working later with the UI, the users can click a button to upload a different image.

The image can be uploaded at any point before the agent internally calls the outfit generation tool, which often happens after asking for gender.

### Outfit generation

In this section, we can see how the agent internally uses the tool to generate an outfit from the user description, image, and gender.

### Querying the inventory

At this stage, the agent obtains a description for the two pieces of clothing that it needs to retrieve and uses the query engine to retrieve the best matches from the vector database.

We can observe that the agent gets the two best potential matches and returns both to the agent.

### Final recommendation presentation

After analyzing the options, the agent presents the user with the best matching pairs, complete with item details such as price and purchase links (the product ID could be converted to a URL later). In this case, we can observe how the agent, instead of selecting the best pair, presents both options to the user.

💡 Remember that our dataset is fairly small, and the option suggested by the outfit recommender might not be available in our dataset. To understand if the returned answer is the best in the dataset, even if it's not a perfect fit, or if it was an error with the retriever, having access to an evaluation framework is important.
Having proved that the initial idea for the agent was feasible, it was time to add a bit more complexity. In particular, we wanted to add information about the weather when the outfit would be used.

## Expanding functionality
The natural progression of our shopping assistant entails augmenting its capacity to factor in external elements such as weather conditions. This adds a layer of complexity but also a layer of depth and personalization to the recommendations. These enhancements came with their own sets of technical challenges.

# Adapting to the weather
Weather awareness: Initial considerations center on incorporating simple yet vital weather aspects. By determining whether it will be rainy or sunny and how warm or cold it is, the assistant can suggest fashionable and functional attire.
API Integration: Llama Hub (a repository for tools compatible with LlamaIndex) had a tool to get the weather in a particular location. Unfortunately, the tool required a paid https://openweathermap.org/ plan. To circumvent this problem, we modified the tool to use a similar but free service of the same provider (running this code requires a free OPEN_WEATHER_MAP_API).

# User interaction and data handling
Location input: For accurate weather data, the shopping assistant often queries the user for their location. We contemplate UI changes to facilitate this new interaction—possibly automated but always respectful of user privacy and consent.

# Synchronizing with time
Temporal challenges: Addressing the aspect that LLMs aren’t inherently time-aware, we introduced a new tool that provides the current date. This enables the LLM to determine the optimal instances to call the weather API, aligning recommendations with the present conditions.

It took us a little bit to remember that we needed this. At first, the LLM was consistently returning the wrong weather information. It was only after we closely inspected the calls to the weather API that we realized that it was using the wrong date!

## User Interface (UI) development
In developing the user interface for our AI-powered shopping assistant, we wanted the platform to reflect the conversational nature of the agent’s interactions. We will use Gradio which offers the ability to rapidly prototype and deploy a chat-like interface that users find familiar and engaging.

# Embracing chat interface with Gradio
Chat interface principles: The decision to adopt a chat interface was rooted in the desire for simplicity and intuitiveness. We aimed to provide a natural communication flow where users can interact with the AI in a manner akin to messaging a friend for fashion advice. Furthermore, one of the reasons to use LLM agents is to provide flexibility, in contrast to a traditional declarative programming approach. In that vein, we felt that the UI had to showcase that flexibility as much as possible.

Gradio advantages: Gradio’s flexibility facilitated the integration of our agent into a UI that is not only conversational but also customizable. Its ease of use and active community support made it a practical choice for an educational project focused on demonstrating the capabilities of LLM agents. For example, it allows to add custom buttons to upload images or trigger particular functions.

# Overcoming technical hurdles
Inline image display: One of the initial technical challenges was presenting images seamlessly in the chat interface. Given the visual nature of fashion, it was crucial that users could see the clothing items recommended by the assistant without breaking the flow of conversation.
Activeloop integration: To resolve this, we leveraged Activeloop’s integration with Gradio. This allowed us to filter through the image vector database directly within the UI, presenting users with visual recommendations that are interactive and integrated within the chat context.
It was not trivial to get Activeloop’s extension working for our project. Our solution consisted of having an HTML component in Gradio with an IFrame pointed to the image vector dataset. We could update the URL every time the chatbot answered, but we needed a way to get the product IDS from its answer. Ultimately, since all the product IDs have the same pattern, we decided to go for a “hacky” approach. Search the agent’s response for the product IDs regex, and if there were more than 2 matches, update the iframe URL parameters. Otherwise, do nothing.

## Conclusion
As we’ve journeyed through the intricate process of developing an AI-powered shopping assistant, the roles of DeepLake and LlamaIndex have proven pivotal. From the versatile data handling in DeepLake’s database for AI to the adaptive LLM agents orchestrated by LlamaIndex, these technologies have showcased their robust capabilities and the potential for innovation in the AI space.

DeepLake has demonstrated its capacity to seamlessly manage and retrieve complex structures, enabling efficient and precise item matchings. Its architecture has been the backbone of the shopping assistant, proving that even complex data interactions can be handled with elegance and speed. In addition, it allowed for seamless visualization the data for the RAG application.

LlamaIndex, on the other hand, has been instrumental in empowering the shopping assistant with natural language processing and decision-making abilities. Its framework has enabled the LLM agents to interpret, engage, and personalize the shopping experience, charting new courses in user-AI interaction.

Looking beyond the shopping assistant itself, the potential uses for these technologies span myriad domains. The flexibility and power of DeepLake and LlamaIndex could drive innovation in fields ranging from healthcare to finance and from educational tools to creative industries.

Your insights and feedback are crucial as we continue to navigate and expand the frontiers of artificial intelligence. We are particularly eager to hear your views on the innovative applications of vector databases and LLM frameworks. Additionally, your suggestions for topics you’d like us to delve into in future segments are highly appreciated. If you’re interested in partnering with Tryolabs to build similar projects with Deep Lake & LlamaIndex, feel free to reach out to us.
