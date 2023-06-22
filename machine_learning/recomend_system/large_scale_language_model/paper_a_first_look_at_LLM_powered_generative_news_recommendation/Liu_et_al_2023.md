## link

- https://arxiv.org/abs/2305.06566

## title

A First Look at LLM-Powered Generative News Recommendation

## abstract

Personalized news recommendation systems have become essential tools for users to navigate the vast amount of online news content, yet existing news recommenders face significant challenges such as the cold-start problem, user profile modeling, and news content understanding. Previous works have typically followed an inflexible routine to address a particular challenge through model design, but are limited in their ability to understand news content and capture user interests. In this paper, we introduce GENRE, an LLM-powered generative news recommendation framework, which leverages pretrained semantic knowledge from large language models to enrich news data. Our aim is to provide a flexible and unified solution for news recommendation by moving from model design to prompt design. We showcase the use of GENRE for personalized news generation, user profiling, and news summarization. Extensive experiments with various popular recommendation models demonstrate the effectiveness of GENRE. We will publish our code and data for other researchers to reproduce our work.

# Introduction

Online news platforms, such as Google News, play a vital role in disseminating information worldwide. However, the sheer volume of articles available on these platforms can be overwhelming for users. Hence, news recommender systems have become an essential component, guiding users navigate through a vast amount of content and pinpointing articles that align with their interests. Nonetheless, present news recommendation systems face several major challenges. One such challenge is the well-known cold-start problem, a scenario where many long-tail or new users have limited browsing history, making it difficult to accurately model and understand their interests. User profile modeling poses another challenge, since user profiles consist of highly condensed information, such as geographic location or topics of interest, which are frequently withheld from datasets due to privacy concerns. Additionally, there is the unique challenge of news content understanding in the field of news recommendation. Due to limited and unaligned text information in news datasets, it can be challenging for models to capture the deeper semantics of news articles. For instance, in an article (in the MIND [48] dataset) with the title “Here’s Exactly When To Cook Every Dish For Thanksgiving Dinner”, the main idea may be “guidance” or “instructions” rather than the specific terms mentioned in the title. However, accurately identifying key concepts or themes in news articles can be challenging, which in turn affects the ability of news recommender systems to provide personalized recommendations to users. Previous works [19, 41, 45] have proposed various recommendation models to tackle the aforementioned challenges. However, due to the limited data and knowledge available in the training dataset, these models are limited in their ability to understand news content and capture user interests. Although some methods [37] have attempted to incorporate external sources, such as knowledge graphs, their performance is often constrained by the size of the knowledge graphs.

LLM-powered generative news recommendation: a novel perspective. The advancement of large language models (LLMs), such as ChatGPT2 or LLaMA [32], has revolutionized the field of natural language processing. The exceptional language modeling capability of LLMs enables them to understand complex patterns and relationships in language. As powerful few-shot learners, they can quickly learn the distribution of news data and incorporate relevant contextual information to improve their understanding of the data. This makes LLMs a suitable tool for addressing the challenges of news recommendation systems, including the cold-start problem, user profile modeling, and news content understanding. In this work, we introduce a novel perspective for news recommendation by using LLMs to generate informative knowledge and news data such as synthetic news content tailored to cold-start users, user profiles, and refined news titles, which can be utilized to enhance the original dataset and tackle the aforementioned challenges. Figure 1 illustrates our proposed LLM-powered GEnerative News REcommendation (GENRE) framework. The main idea is to utilize the available news data, such as the title, abstract, and category of each news article, to construct prompts or guidelines, which can then be fed into an LLM for producing informative news information. Due to its extensive pretrained semantic knowledge, the LLM can comprehend the underlying distribution of news data, even with very limited information provided in the original dataset, and generate enriched news data and information. These generated news data and information can be integrated back into the original dataset for the next round of knowledge generation in an iterative fashion, or utilized to train downstream news recommendation models. In this study, we explore GENRE for 1) personalized news generation, 2) user profiling, and 3) news summarization, to address the three challenges mentioned above. To validate the effectiveness of our proposed GENRE framework, we perform comprehensive experiments on IM-MIND [50], a multimodal news recommendation dataset derived from MIND [48]. We employ GPT-3.5 as the LLM and collect the generated data through API calls. Our evaluation involves four matching-based news recommendation models and four ranking-based CTR models, all of which are typical and widely used in industrial recommender systems. We observe that GENRE improves the performance of the base models significantly. To summarize, our contributions are listed as follows:

- To our knowledge, this work is the first attempt to exploit LLMs for generative news recommendation.
- We propose GENRE, an LLM-based generative news recommendation framework. Compared to traditional methods that require designing individual models for different tasks, GENRE offers a flexible and unified solution by introducing pretrained semantic knowledge to the training data through prompt design.
- We demonstrate the effectiveness of GENRE through extensive experimentation and evaluation on three tasks: 1) personalized news generation, 2) user profiling, and 3) news summarization.

# Preliminaries

## Notations and Problem Statement

Before delving into the details of our proposed method, we first introduce basic notations and formally define the news recommendation task. Let N be a set of news articles, where each news 𝑛 ∈ N is represented by a multi-modal feature set including the title, category, and cover image. Let U be a set of users, where each user 𝑢 ∈ U has a history of reading news articles ℎ (𝑢) . Let D be a set of click data, where each click 𝑑 ∈ D is a tuple (𝑢, 𝑛, 𝑦) indicating whether user 𝑢 clicked on news article 𝑛 with label 𝑦 ∈ {0, 1}. The task of the news recommendation is to infer the user’s interest in a candidate news article.

## General News Recommendation Model

A news recommendation model generally involves three modules: a news encoder, a user encoder, and an interaction module. The news encoder, as depicted in Figure 2, is designed to encode the multimodal features of each news article into a unified 𝑑-dimension news vector v𝑛. The user encoder, as shown in Figure 3a, is designed on the top of the news encoder, generating a unified 𝑑-dimension user vector v𝑢 from the sequence of browsed news vectors. Finally, the interaction modules in ranking models (such as DCN [39]) and matching models (such as NAML [43]) have some differences. For ranking models, the click-through probability is directly calculated based on the candidate news vector v𝑐 and the user vector v𝑢, which is a regression problem. In contrast, for matching models, the interaction module needs to identify the positive sample that best matches the user vector v𝑢 among multiple candidate news vectors V𝑐 = [v (1) 𝑐 , ..., v (𝑘+1) 𝑐 ] where 𝑘 is the number of negative samples, which is a classification problem.

The design of the news encoder, user encoder, and interaction module varies across different news recommendation models.

# Proprsed Framework: GENRE

## Overview

Figure 1 illustrate the our proposed GENRE framework for LLMpowered generative news recommendation, which consists of the following four steps. 1) Prompting: create prompts or instructions to harness the capability of a LLM for data generation for diverse objectives. 2) Generating: the LLM generates new knowledge and data based on the designed prompts. 3) Updating: use the LLMgenerated data to update the current data for the next round of prompting and generation, which is optional. 4) Training: leverage the LLM-generated data to train news recommendation models. Prompt design forms the foundation of GENRE, and the iterative generation and updating mechanism allows for an expansive and complex design space. In the following, we show examples of prompts designed under GENRE for news summarization, user profile modeling, and personalized news generation.

## LLM as News Summarizer

Large language models are capable of summarizing news content into concise phrases or sentences, due to their training on vast amounts of natural language data and summarization tasks. Moreover, large language models possess remarkable skills in comprehending text, allowing them to identify noun entities like the names of individuals and locations. These entities may have appeared infrequently in the original dataset, making it challenging to learn their representations. However, large language models can associate them more effectively with knowledge learned during pre-training.

Therefore, we design a prompt for news title enhancement, as shown in Figure 4a. By providing the news title, abstract, and category as input, the large language model produces a more informative news title as output. As shown by the provided sample, the enhanced title not only summarizes the news information but also highlights the main topic of the news – “guide”, which is missing from the original title.

During the training of the recommendation model, the enhanced news title will replace the original title and be used as one of the input features, together with other multi-modal features, for the news encoder (Figure 2). The green news vectors in Figure 3b represent the news vectors with the enhanced titles.

## LLM as User Profiler

The user profile generally refers to their preferences and characteristics, such as age, gender, topics of interest, and geographic location. These explicit preferences often serve as important features for click-through rate (CTR) recommendation models. However, these information are usually not provided in the anonymized dataset for training recommendation models, due to privacy policies. Large language models are capable of understanding a user’s reading history through their ability to model long sequences, enabling them to analyze and create an outline of the user’s profile. Hence, we design a prompt for user profiles modeling, as depicted in Figure 4b. Given a user’s reading history, the large language model produces a user profile that includes his/her interested topics and regions. In this example, the LLM infers that the user may be interested in the region of Florida, based on the word “Miami” in the news. Although “Miami” may have a low occurrence in the dataset, “Florida” is more frequently represented and therefore more likely to be connected to other news or users for collaborative filtering. The summarized user profile will be fed into an interest fusion module which produces a interest vector v𝑖 (the pink vector in Figure 3c), defined by

$$
\tag{1}
$$

where POOL is the average pooling operation, Etopics and Eregions are the embedding matrices of the interested topics and regions, and [; ] is the vector concatenation operation. The interest vector v𝑖 will be combined with the user vector v𝑢 (the blue vector in Figure 3c) learned by the user encoder to form the interest-aware user vector v𝑖𝑢 (the purple vector in Figure 3c) as follows:

$$  
\tag{2}
$$

where MLP is a multi-layer perceptron with ReLU activation.

## LLM as Personalized News Generator

The cold-start problem, which is well-known for its difficulties, occurs when new users3 have limited interaction data, making it difficult for the user encoder to capture their characteristics and ultimately weakening its ability to model warm users 4 . Recent studies [7, 33] have shown that LLMs possess exceptional capabilities to learn from few examples. Hence, we propose to use an LLM to model the distribution of user-interested news given very limited user historical data. Specifically, we use it as a personalized news generator to generate synthetic news that may be of interest to new users, enhancing their historical interactions and allowing the user encoder to learn effective user representations. The prompt displayed in Figure 4c serves as a guide for the personalized news generator, allowing the LLM to create synthetic news pieces tailored to the user’s interests. The generated news pieces (indicated by the yellow news vectors in Figure 3d) are incorporated into the user historical sequence, which will be encoded and fed to the user encoder to generate the user vector.

## Chain-based Generation

While we have shown several examples of “one-pass generation” (Figure 4) under our GENRE framework, it is worth noting that the design space of GENRE is vast and of a high-order complexity. As illustrated by the diagram in Figure 1, GENRE enables iterative generation and updating. The data generated by the LLM can be leveraged to enhance the quality of current data, which can subsequently be utilized in the next round of generation and prompting in an iterative fashion. We refer to this type of generation as “chainbased generation”, in contrast to “one-pass generation”. We design a chain-based personalized news generator by combining the one-pass user profiler and personalized news generator. As illustrated in Figure 5, we first use the LLM to generate the interested topics and regions of a user, which are then combined with the user history news list to prompt the LLM to generate synthetic news pieces. The user profile helps the LLM to engage in chain thinking, resulting in synthetic news that better matches the user’s interests than the one-pass generator. The prompt for the chain-based generator is provided in the supplementary materials.

## Downstream Training

Our GENRE framework can be applied with any news recommendation model. Existing news recommendation models mainly include matching-based models such as NAML [43], LSTUR [1], NRMS [45], and PLMNR [46], and ranking-based deep CTR models, such as BST [4], DCN [39], PNN [26], and DIN [55]. Since ranking-based models directly calculate the click-through rate, they place greater emphasis on the design of multiple feature interactions, compared to the relatively straightforward design of the news encoder and user encoder (Table 2). These models are trained with the binary cross-entropy loss defined as:

$$
\tag{3}
$$

where 𝑧 is the batch size, 𝑦𝑖 is the label of the 𝑖-th sample (can be 0 or 1), and 𝑦ˆ𝑖 is the predicted probability of the 𝑖-th sample. In contrast, matching-based models concentrate on capturing semantic information from news features and user interests. Therefore, they prioritize the design of news encoder and user encoder and use a relatively simple interaction module (Table 2). These models are trained using the cross-entropy loss:

$$
\tag{4}
$$

where 𝑘 is the number of negative samples, 𝑦𝑖,𝑗 is the label of the 𝑗-th sample in the 𝑖-th sample group (can be 0 or 1), and 𝑦ˆ𝑖,𝑗 is the predicted probability of the 𝑗-th sample in the 𝑖-th sample group.

# Experiments

## Experimental Setup

### Datasets.

We conduct experiments on a large-scale real-world news recommendation dataset, MIND [48], where each news article contains features including title, abstract, category, subcategory, and cover image. The cover image of a news article is crawled from the URLs provided by IMRec [50]. In Table 1, we present the statistics of both the original dataset and the augmented versions, denoted as MIND-NS, MIND-UP, and MIND-NG, which correspond to dataset enhanced using the news summarizer, user profiler, and personalized news generator, respectively. We use OpenAI package5 to call GPT-3.5 APIs6 for data generation. The cost of constructing MIND-NS, MIND-UP, and MIND-NG was approximately 60 USD, 120 USD, and 40 USD, respectively. For the augmented datasets, only the attributes that are different than the orginal datasets are shown in Table 1.

### Recommendation Models.

We evaluate the effectiveness of our proposed GENRE framework with eight popular news recommendation models, including four matching-based models, namely NAML [43], LSTUR [1], NRMS [45], and PLMNR [46], and four ranking-based deep CTR models, namely BST [4], DCN [39], PNN [26], and DIN [55]. They follow a similar pipeline as described in subsection 2.2 and Figure 3a, but with differences in individual components, as summarized in Table 2.

### Evaluation Metrics.

We follow the common practice [25, 45, 46] to evaluate the effectiveness of news recommendation models with the widely used metrics, i.e., AUC [12], MRR [35] and nDCG [15]. In this work, we use nDCG@5 and nDCG@10 for evaluation, shortly denoted as N@5 and N@10, respectively.

### News Features.

To incorporate image information into textbased news recommendation models, we use a pretrained image encoder [28] to extract image features, which we treat as a newsspecific token. We also treat the category and subcategory as special tokens that do not undergo tokenization. Then, we concatenate these features (i.e., title, image, and category) to form the input sequence for the news encoder. For the NAML model, since its original news encoder already incorporates the category information, we only concatenate the image and title features.

### Implementation Details.

We utilize pretrained “clip-vit-basepatch32” models [28] to extract cover image features and BertTokenizer provided by the transformers package [42] to tokenize textual features of news articles. During training, we employ Adam [17] optimizer with a learning rate of 0.001 and weight decay of 0.01. For all models, the embedding dimension is set to 64. For all matchingbased models, a negative sampling ratio of 4 is specified uniformly. The number of transformer layers is set to 3 for both PLMNR [46] and BST [4]. For PLMNR, we use its best variant, PLMNR-NRMS. We use news title, category, and cover image as input features for the news encoder. Since the image embedding dimension is 512, to ensure that it matches the other features, we employ a learnable projection layer to decrease its dimension from 512 to 64. We tune the hyperparameters of all base models to attain optimal performance. We average the results of five independent runs for each model and observe the p-value smaller than 0.01. All the experiments are conducted on a single NVIDIA GeForce RTX 3090 device.

## LLM as News Summarizer

Table 3 presents a comparison of the performance between the original data and the data enhanced by the news summarizer for eight base models. Based on the results, we can make the following observations. Firstly, the improved news titles offer additional semantic information, thereby aiding the news encoder to capture the essence of news articles more effectively. Secondly, rankingbased models (with simple design of news encoder such as average pooling) and matching-based models (with complex design of news encoder) demonstrate comparable levels of enhancement, which could be attributed to the great importance of text keywords in comprehending news. In the above experiments, we only utilize (enhanced) news title, category, and cover image as inputs to the news encoder. Here, we assess the impact of combining more news features. From Figure 6, the following can be summarized. Firstly, the inclusion of additional news features such as abstract and subcategory does lead to an improved model performance, although they are usually excluded from existing models out of efficiency concerns. Secondly, while MIND* has included all available news features, MIND-NS* still outperform MIND\*, indicating the effectiveness of the news titles generated by GPT-3.57.

## LLM as User Profiler

Table 4 displays a comparison of the performance between the original data and the data enhanced by the user profiler for eight base models. Based on the results, we can conclude the following. Firstly, the highly-summarized user interests provide valuable user knowledge to the interaction module, leading to better recommendations. Secondly and unsurprisingly, ranking-based models that employ a more complex interaction module show greater improvements than matching-based models that use a simple interaction module such as dot product. This is because the integration of the generated user profile (the interest vector in Figure 3c) occurs in the interaction module, and a simple combination scheme may prevent the model from fully learning the user profile features.

## LLM as Personalized News Generator

Table 5 shows a comparison of the performance between the original data and the data augmented by the personalized news generator for eight base models. For each new user, two synthetic news articles are generated by the personalized news generator and appended to the user’s history list. The results suggest that the generated news articles for new users align with their potential interests, leading to more reliable and accurate user representations, and consequently, an enhanced performance. Next, we study how the number of generated news articles affects the recommendation performance. As depicted in Figure 7, we evaluate the effectiveness of utilizing 0, 1, and 2 generated news articles per new user for four base models. It can be seen that for each model, the performance improves as the number of generated news articles increases. Additionally, we investigate the impact of the synthetic news data on two user groups, i.e., new user group and warm user group. From the results in Table 6, it can be seen that the personalized news generator improves the performance of both the new and warm user groups in most cases. This is because the user encoder struggles to capture the interests of new users due to their limited history of news consumption, which also affects its ability to model warm users. With the generated news pieces added to the browsing history of new users, the user encoder can better capture their interests, leading to a performance improvement on both groups.

## Chain-based Generation

Here, we study the impact of chain-based generation on the quality of generated personalized news. Based on the results generated by the user profiler, we first remove users whose results do not contain valid topics of interest and obtain a new dataset (which accounts for 96% of the original dataset in terms of the number of users and 97% in terms of the number of interactions). We refer to the filtered dataset as the “Chain” dataset, in contrast to the “Full” dataset that includes all interaction data. Next, we apply chain-based generation, supplying the personalized news generator with the topics of interest generated by the user profiler, as shown in Figure 5. The performance comparison among the original dataset, the one-pass personalized news generator, and the chain-based personalized news generator (i.e., user profiler (UP) → personalized news generator (NG)) is displayed in Table 7. Based on the results, we can conclude that the knowledge learned by the user profiler improves the quality of the synthetic news produced by the personalized news generator.

## Cost Conversion Rate

Finally, we investigate the cost and cost conversion rate (CCR) of different generative schemes under our GENRE framework, as presented in Table 8. We compute the average improvement in AUC compared with the original dataset for both matching and ranking models based on the results from Table 3, Table 4, and Table 5, as well as the cost conversion rate (ratio of improvement in AUC to cost of employing the GPT-3.5 API). Based on the results, we can conclude the following. Firstly, with the full dataset, the personalized news generator (NG) has the best CCR for matchingbased models, and the news summarizer (NS) has the best CCR for ranking-based models. Secondly, the user profiler (UP) has the worst CCR, since the extensive length of a user’s browsing history results in a high token count per request, leading to increased cost for the user profiler. Thirdly, chain-based generation achieves a higher improvement compared to one-pass generation (with the chain dataset), but its CCR decreases due to the use of the expensive user profiler.

# Related Works

## Generative Models for Recommendation

Over past few years, generative models have achieved great success in various fields such as natural language processing [6] and computer vision [30], and have also been explored for recommendation. Examples include generative adversarial networks [3, 38, 51, 52], variational auto-encoders [9, 21, 23, 52], and diffusion models [22, 36, 40].

The recent advancement of large language models, particularly ChatGPT, has triggered a new wave of interest, resulting in the development of diverse applications across multiple domains [7, 27, 49]. There have been several studies attempting to use ChatGPT for rating prediction and direct recommendation through in-context learning (in contrast of involving LLMs in training as part of the model). [8, 13, 16, 24]. There have also been studies applying LLMs to conversational recommender systems, where users provide natural language instructions to receive recommendation results [53]. In this paper, we make the first attempt to introduce LLMs for generative news recommendation.

## News Recommendation

In the past few years, news recommendation has gained significant attention and has been widely studied in both industry and academia. To better capture textual knowledge and user preferences, several models based on deep neural networks have been proposed [1, 43–45]. These models use various techniques such as convolutional neural networks (CNNs) [18], recurrent neural networks (RNNs) [5, 11], and attention mechanisms [34] as news or user encoders. Despite their effectiveness, these end-to-end models have limited semantic comprehension abilities. Recently, there has been a surge of interest in using pretrained language models (PLMs) such as BERT [10] and GPT [29] in news recommendation systems, owing to the powerful transformer-based architectures and the availability of large-scale pretraining data. These models have shown promising results in news recommendation [25, 46, 47, 54]. The emergence of large language models (LLMs) such as ChatGPT and LLaMa [32] has further opened up the possibility of leveraging rich general knowledge to enhance the efficacy of recommender systems. Very recently, there has been a few attempts to utilize LLMs for personalization [31] and product recommendation [20]. LaMP [31] exploits LLMs to develop a personalized benchmark for NLP tasks. GPT4Rec [20] uses LLMs to generate hypothetical search queries and retrieves items for recommendation by searching for these queries. [24] points out that directly employing LLMs as a recommender system has shown negative results [24]. The use of LLMs for news recommendation remains understudied. Due to the large size of LLMs, it is inefficient to use them as news encoders in both the training and inference stages. In this work, we take the first step towards LLM-powered generative news recommendation by proposing a general framework that leverages the pre-trained knowledge in LLMs to enhance the training data from various aspects and improve the performance of news recommendation models.

# Conclusion

Our work addresses the limitations of news recommendation systems and offers a new approach that leverages LLMs to enhance their performance. Our findings indicate that integrating the general knowledge of LLMs into recommendation systems can lead to substantial improvements, which has important implications for online news platforms. Our framework GENRE can be applied to other domains beyond news recommendation. We hope our work will encourage further research and contribute to the development of more efficient and effective recommendation systems
