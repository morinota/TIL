## refs

<https://medium.com/google-cloud/embeddings-how-to-select-the-right-one-135032315709>

# Embeddings: How to select the right one?

Notes from my reading in quest to answer questions like:
How do I choose the right embedding model for a task?
Will the same embedding model work for all my tasks?
How can I evaluate an embedding model for a given task?
How do I detect bias in embedding model?
Is the model with higher number of dimensions always the best choice?

## What are Embeddings?

Imagine trying to explain the taste of an apple to someone who’s never had one. You could use words like “sweet,” “crunchy,” and “juicy,” but it’s hard to truly capture the experience. Embeddings are like giving computers a taste of language, helping them understand the meaning and connections between words, even if they don’t “experience” them like we do.

Computers may be intelligent at crunching numbers, but they cannot understand text directly. Words, text and documents need to be converted into numbers for making computers understand them.

Essentially, embeddings turn words and phrases into special codes that computers can understand. Similar words get codes that are close to each other, while different words get codes that are far apart. This allows computers to “see” how words relate, like understanding that “happy” and “joyful” are similar, while “happy” and “sad” are opposites. Embeddings could be created for words, sentences or documents as well.

## Why are embeddings becoming important?

Embeddings are becoming increasingly important because they help computers handle the massive amounts of text we create every day. They’re like super-efficient translators, allowing computers to quickly process and understand language, leading to better search results, more accurate translations, and even smarter chatbots.

Think of it like teaching a computer to read between the lines. Instead of just looking for specific words, embeddings help computers grasp the overall meaning of a sentence or document, leading to more relevant and helpful information.

In short, embeddings are like giving computers a secret decoder ring for human language. They’re helping bridge the gap between how we communicate and how computers understand, making technology more intuitive and useful for everyone.

## Design Considerations for choosing Embeddings

### Dimensionality

Dimensionality refers to the number of features of the text represented by the embeddings. This is the number of numerical values used to represent each word/phrase/document in a vector space. Imagine each word as a point in a multi-dimensional space, where the number of dimensions determines the quality and complexity of this representation.

Quality of Embeddings: Higher dimensionality of embeddings provides more features to capture subtle nuances and relationships between words. This can lead to improved performance in tasks like machine translation, sentiment analysis, and question answering, where context and precision are important. Whereas lower dimensionality might not fully capture the semantic richness of words but can be sufficient for simpler tasks like word similarity or document clustering.
Latency: Higher dimensional embeddings results in larger embedding vectors, requiring more memory and computational resources for storage and processing. This can lead to increased latency, especially in real-time applications or on resource-constrained devices. Lower dimensional embeddings can enable faster processing and reduced latency

There are newer embedding models that can handle long context and variable dimensions

Long Context Embeddings that can encode longer sequences
Variable Dimension Embeddings that can produce a latent representation of an arbitrary number of tokens

### Sparsity

Sparsity refers to the proportion of zero values within the embedding vectors.

Sparse Embeddings contain a large number of zero values, with only a few non-zero elements. They are often associated with high-dimensional representations where many dimensions are irrelevant for the given word. SPLADE v2 model provides highly sparse representations and competitive results. Dense Embeddings have non-zero values in most or all dimensions, capturing a richer and more continuous representation of word meanings

Quality of Embeddings: Sparse embeddings might compromise on the semantic information due to the limited number of non-zero values. Dense embeddings capture more semantic information leading to improved accuracy in tasks like machine translation, sentiment analysis, and natural language inference.
Computational Efficiency: Sparse embeddings allows for optimized storage and computation leading to faster processing. Dense embeddings would require more storage and computational resources that could impact the performance especially in real time applications.
Dimensionality reduction techniques like Principal Component Analysis (PCA) or Autoencoders can be used to transform high-dimensional dense embeddings into a lower dimensional space.

### Embedding Algorithms

Traditional Algorithms: Text embedding models like Word2Vec, Glove create static embeddings where each word or phrase has fixed representation regardless of the context.
Contextual Algorithms: With Transformers, context is included via self-attention making the recent embedding models better at more nuanced understanding of language though increasing computational complexity. Embeddings created using contextual algorithms can handle polysemy (words with multiple meanings) and homonymy (words with same spelling but different meanings) much better

### Interpretability

Implementing interpretability in embeddings involves employing techniques to understand and explain the relationships captured within the embedding space.

#### Visualization of Embeddings

Embedding Projector: A tool that interactively visualizes embeddings in 3D, enabling exploration of nearest neighbors, clusters, and semantic relationships. This tool uses different dimensionality reduction techniques like PCA, T-SNE, UMAP to visualize the embeddings as a 2D or 3D visualization
Custom Code for visualizing the embeddings can also be leveraged

#### Visualizing Attention Mechanisms

Attention in neural networks: Attention mechanisms highlight the most relevant parts of input data when making predictions, providing insights into which words or features are important for a specific task. Visualizing attention mechanisms using tools like BERTViz can reveal the attention patterns, showing which words or regions of the input contribute most to the output.

### Bias and Fairness

Embeddings are often obtained from training on large pre-existing datasets, and are susceptible to biases due to unfair representations in the original datasets. Some of the techniques available Word Embedding Fairness Evaluation (WEFE) is an open source library for measuring and mitigating bias in word embedding models.

WEFE also offers API, Github Repository and documentation to implement the framework.
The framework includes different metrics like Word Embedding Association Test (WEAT), Relative Norm Distance (RND), Mean Average Cosine Similarity (MAC), Embedding Coherence Test (ECT)
WEFE also includes a mitigation framework and Debias APIs to overcome Bias

### Latency

There are different ways of setting up Embedding models — accessing via HuggingFace, Langchain (uses HuggingFace integration) or use the embedding APIs from various providers.

Custom embedding models hosted can also be accessed via an endpoint. Network latency can be reduced in this case, however the infrastructure scaling and updating the embedding models would have to be managed.

Embedding APIs from different providers simplified the task of obtaining word embeddings and allowed developers to focus on building applications. They make it easy for the developers to access state of the art NLP technologies. However, if latency, privacy and security are critical, embedding models can also be hosted privately. Embedding APIs can be accessed directly from the provider like Google Cloud text embeddings API. Another alternative is to use LangChain provided integrations with various model providers that allow you to use embeddings with LangChain.

It is important to understand the rate and quota limitations when using the Embedding APIs in your solution.

Embedding APIs from different providers also could vary in latency. Choice of APIs can be evaluated for latency. The blog by getzep.com provides a comparison of latency across different APIs.

### Cost

Cloud based embedding models offer flexibility and scalability, but can incur ongoing costs. On-premise hosted models require upfront investment in compute but can be more cost-effective in the long run for high volume proprietary models.

Many high quality open source models are available, which might reduce cost. However, due diligence need to be done to assess the fitment to the use case.

For custom models, strategies like quantization and distillation to reduce the model size and batching inference requests can be used to optimize cost

Google Cloud offers different options and cost structures like multimodal embeddings for text, image, video. Pricing for embeddings for text also varies for online and batch requests.

### Ability to Fine Tune

Fine tuning the model on datasets specific to the use case can enhance the performance of the pre-trained model if it is not trained on data relevant to the domain or for the specific needs.

Google Cloud provides options to fine tune the text and multilingual embedding models with user specific data. The tuning is executed using Vertex AI Pipelines

### Selection of Embedding Models for your use case

The constant evolution of models makes it challenging to identify the right embedding model for a given task and the nature of the dataset used for the use case. Massive Text Embedding Benchmark (MTEB) aims to provide clarity on how different models perform on a variety of embedding tasks on different datasets.

MTEB code is available open-source enabling evaluation of any embedding model on different tasks and datasets in less than 10 lines of code.

Python code to use MTEB for a custom model

```
import mteb
# load a model from the hub (or for a custom implementation see https://github.com/embeddings-benchmark/mteb/blob/main/docs/reproducible_workflow.md)
model = mteb.get_model("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
tasks = mteb.get_tasks(…) # get specific tasks
# or
from mteb.benchmarks import MTEB_MAIN_EN
tasks = MTEB_MAIN_EN # or use a specific benchmark
evaluation = mteb.MTEB(tasks=tasks)
evaluation.run(model, output_folder="results")
```

MTEB Leaderboard provides insights for selection of the right embedding model based on:

- Embedding Model performance based on task and task specific metrics relevant for the use case
- Embedding Model performance on different datasets similar to the datasets and languages relevant to the use case

MTEB evaluates models on datasets of varying text lengths which are grouped into three categories:

Sentence to Sentence (S2S) — a sentence is compared to another sentence
Paragraph to Paragraph (P2P) — A paragraph is compared with another paragraph
Sentence to Paragraph (S2P) — a single sentence is input query, but used to retrieve long documents consisting of multiple sentences.
MTEB leaderboard consists of 199 datasets (as displayed on the leaderboard). These include 10 multilingual datasets for some of the tasks. Some of the datasets have similarities with each other.

Performance of the embedding models on custom datasets or datasets similar to the existing datasets can be evaluated based on the metrics for the given task.

## References

Embeddings | Machine Learning | Google for Developers
On the Dimensionality of Embedding
SPLADE v2: Sparse Lexical and Expansion Model for Information Retrieval
Embedding projector
BertVIZ
WEFE: The Word Embeddings Fairness Evaluation Framework
the WEFE documentation!
Mitigation Framework — WEFE 0.4.1 documentation
Text embeddings API | Generative AI on Vertex AI | Google Cloud
Embedding models | 🦜️🔗 LangChain
longembed: extending embedding models for long context retrieval
[2305.09967] Variable Length Embeddings
Get multimodal embeddings | Generative AI on Vertex AI | Google Cloud
Massive Text Embedding Benchmark
A Survey of Embedding Models (and why you should look beyond OpenAI)
Tune text embeddings | Generative AI on Vertex AI | Google Cloud
