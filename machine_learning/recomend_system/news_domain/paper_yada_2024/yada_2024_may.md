## refs

<https://arxiv.org/html/2405.13007v1>

## title

News Recommendation with Category Description by a Large Language Model

## abstract

Personalized news recommendations are essential for online news platforms to assist users in discovering news articles that match their interests from a vast amount of online content. Appropriately encoded content features, such as text, categories, and images, are essential for recommendations. Among these features, news categories, such as tv-golden-globe, finance-real-estate, and news-politics, play an important role in understanding news content, inspiring us to enhance the categories’ descriptions. In this paper, we propose a novel method that automatically generates informative category descriptions using a large language model (LLM) without manual effort or domain-specific knowledge and incorporates them into recommendation models as additional information. In our comprehensive experimental evaluations using the MIND dataset, our method successfully achieved 5.8% improvement at most in AUC compared with baseline approaches without the LLM’s generated category descriptions for the state-of-the-art content-based recommendation models including NAML, NRMS, and NPA. These results validate the effectiveness of our approach. The code is available at <https://github.com/yamanalab/gpt-augmented-news-recommendation>.

# Introduction

In recent years, online news platforms have gained widespread popularity, making it commonplace for users to consume news articles on their mobile devices. These platforms deliver a large amount of news content to users daily, leading to an information overload problem, making it challenging to discover articles that align with user’s interests. Therefore, personalized news recommendations have become essential for online news platforms.

Many proposed news recommendation models use deep neural networks, which achieve high performance (lstur; nrecsurvey2023; naml; npa; nrms; nrecsurvey2021). As shown in Figure 1, most neural news recommendation models adopt a common approach that consists of three core modules:

(1) News encoder: it generates a news vector that captures the semantic information from the news content.
(2) User encoder: it generates a user vector that captures the user preferences based on browsing history.
(3) Similarity calculator: it computes the similarity score between the news vector and the user vector, estimating that news items with higher similarity scores are more likely to match the user’s interests.

Previous studies have focused on investigating which neural network structures to apply in the user and news encoder modules, resulting in various proposed architectures for news recommendation models. Recent methods incorporate pre-trained language models (PLMs) into the news encoder to learn news representations. These PLM-based approaches have achieved high performance (once; nrecsurvey2023; reduceCross; nrecsurvey2021; plmnr).

Simultaneously, a crucial source for understanding news content is the news category. For example, the MIND (mind) dataset, a well-known dataset in the news recommendation field, contains news categories such as tv-golden-globes. The naïve way to use categories in recommendation models is to adopt predefined templates (e.g., The news category is {category}) followed by combining them with original news recommendation models. However, these templates are too generic to be applied to all news categories, resulting in insufficient information. Constructing detailed descriptions for each news category and using them as input can be beneficial for enabling recommendation models to recognize news content accurately.

However, manually constructing detailed descriptions for each news category is costly. To address this issue, we propose automatically generating descriptive text for news categories using large language models (LLMs). Since LLMs are pre-trained on vast amounts of text data and have extensive knowledge across diverse topics, the LLM-generated detailed descriptions are expected to enhance the recommendation performance. The contributions of this paper are as follows:

(1) We first propose the adoptation of LLM-generated news category descriptions to enhance news recommendations.
(2) Comprehensive experimental evaluations on the MIND dataset confirmed that our proposed method consistently outperforms baseline approaches across multiple recommendation models, achieving up to 5.8% improvement in AUC compared to methods without category descriptions.
The rest of this paper is organized as follows. In Section 2, we reviews state-of-the-art news recommendations and use of LLM-generated text. We propose a new recommendation method enhanced by an LLM in Section 3, followed by evaluations in Section 4. In Section 5, we discuss the limitations of the proposed method. Finally, In Section 6, we conclude this paper.

# Related Work

2.Related Work
In this section, we review related work on news recommendations and the use of LLM-generated text.

2.1.News Recommendations
News recommendations have been extensively studied through various models (nrecsurvey2023; nrecsurvey2021). Neural network-based models have achieved state-of-the-art performance by encoding news content and user preferences to capture the complex interactions between users and news items (lstur; mccm; naml; npa; nrms). For instance, NRMS (nrms) employs multi-head attention to acquire news and user vectors, while LSTUR (lstur) adopts GRU for to obtain user vectors. Other models, such as MCCM (mccm), NAML (naml), and NPA (npa), leverage CNN and attention mechanisms to generate user and news vectors.

Particularly, the models adopting PLMs, such as BERT (bert) and RoBERTa (roberta), to obtain news vectors have achieved notably high performance (once; nrecsurvey2023; reduceCross; nrecsurvey2021; plmnr; mmrec). For instance, Wu et al. (plmnr) proposed a framework incorporating PLMs into news recommendations, demonstrating 2.63% improvement in the pageview rate through online experiments. In the ONCE (once), proposed by Liu et al., showed that using large-scale language models such as LLaMa (llama) can improve news recommendation performance.

Several neural recommendation models use different architectures from the model shown in Figure 1. For instance, Zhang et al. introduced UNBERT (unbert), which feeds a candidate news article and a list of previously viewed news articles into a single language model to predict click-through rates. Another notable work by Zhang et al. (prompt4nr) is Prompt4NR, a news recommendation approach using prompt learning with PLMs.

In summary, various methods with neural network-based models have been proposed for news recommendation. The use of PLMs shows particularly high performance; however, PLMs lack sufficient knowledge to interpret category names. Thus, a space exists to enhance the performance of news recommendations by adding detailed category information, which inspires us to adopt LLM-generated category descriptions as additional features.

2.2.Use of LLM-Generated Texts
The use of text generated by LLMs, which have acquired extensive knowledge on a wide range of topics through pre-training, has improved the performance in various natural language processing tasks, such as text classification and question answering (qagen; cupl; gpt3mix).

Yoo et al. (gpt3mix) proposed GPT3Mix, which applies GPT-3-based (gpt3) data augmentation to text classification tasks by generating additional training examples. For question answering tasks, Liu et al. (qagen) used knowledge expansion using GPT-3 to augment the context and improve the performance of the question answering model. Pratt et al. (cupl) introduced CuPL, a method that leverages image captions generated by LLMs for zero-shot image classification using CLIP (clip). They automatically generated image captions using LLMs and used them as text inputs for CLIP.

These studies demonstrated the effectiveness of utilizing texts generated by LLMs in various tasks. Inspired by this, we aims to improve news recommendation performance by generating news category descriptions using LLMs.

# Proposed Method

Figure 2 shows our proposed novel news recommendation method enhanced by LLM-generated category descriptions, consisting of two steps: 1) automatic generation of news category descriptions, and 2) integration of the generated category descriptions with the recommendation model as additional input features.

## Generation of Category Descriptions

In this step, we generate the descriptions for news categories using an LLM without any manual effort. We employ GPT-4 (gpt4) as the LLM for generating category descriptions, as it has demonstrated high performance across various domains and tasks (sparkGpt4).

Figure 3 shows the prompts for the LLM to generate descriptions for news categories. Although the prompts need to be prepared manually, they do not require any manual effort once they have been prepared.

Figure 4 shows a specific example of the generated news category descriptions for the tv-golden-globes category, one of the categories that appeared in the MIND dataset (mind). The average word count of the generated category descriptions is 57.7 for all 270 news categories within the MIND dataset used in our experiment.

## Integration of Category Descriptions into News Recommendation Models

After generating the category descriptions, we train the news recommendation model by leveraging the generated descriptions. Let D t ⁢ i ⁢ t ⁢ l ⁢ e denote the news title text and D d ⁢ e ⁢ s ⁢ c represent the generated category description. During the inference phase of the recommendation model, we concatenate D t ⁢ i ⁢ t ⁢ l ⁢ e and D d ⁢ e ⁢ s ⁢ c using the special SEP token from BERT (bert), and feed the resulting text into the news encoder

# Experiments and Results

In this section, we describe our experiments. First, we present the dataset, evaluation metrics, baselines, and hyperparameters used in our experiments. Second, we present the results and then discuss the effectiveness of the proposed method.

## Experimental Setting

We used the MIND (mind) dataset, a widely used dataset for the news recommendation field. The MIND dataset, whose statistics are shown in Table 1, was constructed from the news click records of the Microsoft News1 service between October 12, 2019 and November 22, 2019.

To evaluate the effectiveness of our proposed method, we adopted three state-of-the-art content-based recommendation models: NAML (naml), NRMS (nrms), and NPA (npa). We used the pre-trained models DistilBERT-base (distilbert-base-uncased) (distilbert) and BERT-base (bert-base-uncased) (bert) for the news encoder component. AdamW (adamw) was used as the optimization function with a learning rate of 1e-4, a batch size of 128, and 3 epochs. Following the previous studies (mccm; npa; plmnr; prompt4nr), the maximum number of recently viewed articles, which was used to capture user preference information, was set to 50. We set the number of negative samples in the training phase to 4. All experiments are conducted on a Tesla V100 GPU. For implementation, we used PyTorch v2.1.0 (pytorch) and Transformers v4.35.0 (transformers) libraries. As performance metrics, we used the average AUC, MRR, nDCG@5, and nDCG@10 for all impressions.

## Results

Table 2 summarizes the comparison of our proposed recommendation method with the baselines. The proposed method, title+generated-description, demonstrates the highest performance compared with the baselines across all recommendation models and achieved up to 5.6% and 5.8% improvements in AUC compared with the title only and title+template-based baselines, respectively.

Furthermore, title + template-based shows insignificant improvement in performance compared with the title only in most cases. This result suggests that simply fitting the category name into a predefined template is ineffective for representing the category information. The results also indicate that for relatively small-scale language models like BERT, using only the category names as input does not provide sufficient information for the recommendation models to properly interpret the category information.

# Limitations

To explore the limitations, we performed a manual inspection of the category descriptions. Although GPT-4 generally produces high-quality descriptions, it occasionally fails to generate accurate descriptions.

Figure 5 shows an example in which the generated description for the tunedin category focuses on entertainment, music, and television. However, the actual article titles in Table 3 reflect a wider range of to"pics, including technology and trends. A more accurate description would be that the tunedin category casually provides news on various topics such as entertainment, technology, and business, keeping readers updated on the latest trends. This discrepancy highlights the model’s inability to accurately capture the category’s broad scope.

This example, along with other similar instances, suggests that the model may struggle to generate accurate category descriptions when the input lacks sufficient background knowledge or context.

# Conclusion

In this study, we proposed a method to automatically generate news category descriptions using LLMs and incorporate them into news recommendation models. The experiments on the MIND dataset demonstrated that our method outperformed the baselines across all metrics for multiple models. Our main contribution is a novel approach to enhance news recommendation models’ understanding of category information using LLMs. Our future work will include enhancing the recommendation performance by improving the generated descriptions.
