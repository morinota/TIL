## Link

- https://dl.acm.org/doi/10.1145/3604915.3608868

## title

MCM: A Multi-task Pre-trained Customer Model for Personalization

## abstract

Personalization plays a critical role in helping customers discover the products and contents they prefer for e-commerce stores.Personalized recommendations differ in contents, target customers, and UI. However, they require a common core capability - the ability to deeply understand customers’ preferences and shopping intents. In this paper, we introduce the MCM (Multi-task pre-trained Customer Model), a large pre-trained BERT-based multi-task customer model with 10 million trainable parameters for e-commerce stores. This model aims to empower all personalization projects by providing commonly used preference scores for recommendations, customer embeddings for transfer learning, and a pre-trained model for fine-tuning. In this work, we improve the SOTA BERT4Rec framework to handle heterogeneous customer signals and multi-task training as well as innovate new data augmentation method that is suitable for recommendation task. Experimental results show that MCM outperforms the original BERT4Rec by 17% on on NDCG@10 of next action prediction tasks. Additionally, we demonstrate that the model can be easily fine-tuned to assist a specific recommendation task. For instance, after fine-tuning MCM for an incentive based recommendation project, performance improves by 60% on the conversion prediction task and 25% on the click-through prediction task compared to a baseline tree-based GBDT model.

# Introduction

In a personalized recommendation system, it is critical to understand each customer’s preference and shopping intent holistically based on customers’ profile as well as comprehensive historical behaviors like browsing, searching and purchasing signals. Ecommerce stores usually have tens of billions of customer historical behavior data. These signals, if learned with a large capacity model, can help to provide the grounding of customers understanding and be utilized by thousands of downstream use cases. Bert-based pretrained model like GPT has been successful in NLP and CV [4, 5, 8], Researchers in recommendation field explore Bert-based model on specific task like session-based recommendation [9], under the setting of sequential recommendation [2, 3, 6, 7]. However, large-scale pre-training with Bert is still largely under-explored in the field of recommender systems. In this paper, we propose Multi-task pre-trained Customer Model (MCM) model: a large-capacity Bert-based multi-task model with 10 million trainable parameters, pre-trained on a vast amount of behavior data from a large e-commence service. We make architectural improvements for better pre-training, which will be explained in more detail in the model section. Offline results show that MCM outperform the original Bert4rec on multi-tasks by average 17% on NDCG@10 of next action prediction. In order to evaluate the ability to support new personalization tasks, we fine-tune the model for an incentive offer recommendation task, the performance improves by 60% on conversion rate and 25% on click-through rate, compared to the baseline GBDT model.

# Methodology

## Model Framework

MCM consists of three modules: embedding module, sequential encoding module and readout module1. We inherited the sequential encoding module from Bert4rec, while make algorithm improvements on the other two modules, which we will introduce in more detail in the following sessions.

### Heterogeneous Embedding Module.

In this module, we convert the raw inputs into distributed representations through embedding lookup, as is typically done in bert-based models. The original input is a heterogeneous interaction sequence including purchase actions and non-purchase actions. Non-purchase actions are actions that are High Value Actions (HVAs) customers have with the e-commerce stores, e.g. member sign-up, mobile camera search, click records of products etc. Instead of feeding the raw inputs into the embedding module, we choose to represent each interaction 𝑖 with a set of features 𝑓 𝑗 𝑖 , 𝑗 ∈ 1, 2, ..., |𝐽 |, where |𝐽 | denotes the total number of features for each interaction. Now the inputs of each customer𝑐 are |𝐽 | sequences, with the 𝑗-th sequence in the form of 𝐹 𝑗 = [𝑓 (𝑗) 1 , 𝑓 (𝑗) 2 , ..., 𝑓 (𝑗) 𝑛𝑖 ]. Currently, the features include the hierarchical structures of the product: product line, category, subcategory as well as brand. Additionally, we design a feature called token type to handle heterogeneous input, making it easier for the model to differentiate different types of interactions. Each distinct feature value is assigned a unique embedding vector. After the embedding look-up, the inputs are converted to |𝐽 | sequences of embeddings, we perform average pooling to these sequences, producing a single embedding sequence 𝑬 = [𝒆1, 𝒆2, ..., 𝒆𝒏𝒊 ]. The bert model requires position embedding to capture the order of sequences, we adopt learnable position embeddings 𝑃 for better performance, which is randomly initialized learnable parameters. The output of the embedding module is then

$$
\tag{1}
$$

### Task-Aware Attentional Readout Module.

The output of the sequential encoding module is a sequence of hidden vectors, with the same length as the input sequence. Previous work[9] computes the inner product between the last hidden vector and the item embedding to produce the score for the corresponding item. This can be sub-optimal since the last hidden vector is a fixed representation of the whole behavior sequence, which is not aware of the specific item or task to predict. Different tasks may be related to different behaviors within the whole behavior sequence. We propose a novel task-aware attentional readout module, which allows different items (labels in each task) and different tasks to attend to different subsequences of the hidden sequence with attention mechanism , in order to produce a task-specific representation. Specifically, let 𝒉𝒊 denote the 𝑖-th embedding of the output of the sequential encoding module, and let 𝒆𝒘 denote the embedding for a particular item 𝑤 in a certain task, the attentional readout operation can be described as:

$$
\tag{2}
$$

where 𝒓𝑤 is the representation of the input sequence, specific to item 𝑤. The predicted score for item 𝑤 is:

$$
\tag{3}
$$

Softmax operation is performed on the scores to produce the final distribution.

## Model Learning with prefix-augmentation

Previous work[9] on sequential recommendation adopt a popular augmentation method in NLP called masked language model, which randomly masks out some tokens in the input sequence and asks the model to predict them based on all other tokens. Such augmentation is suitable for language modeling, but we believe it can be problematic for recommendation tasks since it leaks future information. We propose a new augmentation method called random prefix augmentation, which randomly samples a prefix from the whole input sequence, and ask the model to predict the last item. In this case, the input will only include the items before the last item, so that our augmentation avoids leaking future information. For example, suppose the original input sequence is [𝑖1,𝑖2,𝑖3], valid prefixes include [𝑖1] and [𝑖1,𝑖2]. The augmentation is performed at batch time rather than during data pre-processing, in order to save memory. The loss function for each prefix is defined as the negative loglikelihood of the label item (the last item):

$$
\tag{4}
$$

where 𝑖𝑔𝑡 denotes the ground truth item, S denotes the input sequence, which contains all items but the last one. For multi-task
training, the loss of all tasks are summed together.

# Experiment

## Experiment Setup

### Datasets and Evaluation Details.

To train our models, we use data from a large e-commerce service. We use customer behaviour data sampled from 6 years customer history. The dataset consists of 40M customers and 10B interactions. The behavior sequence includes three types of interactions: item purchases, item clicks and customer valuable actions. For each purchase and click interaction, we use products’ hierarchical features including product line (PL), category, subcategory as well as brands. To note, these features are also the tasks we train the model to predict on customer’s next preferences. As suggested in [1], we split the dataset into training, validation and testing dataset by time to avoid leaking future information. We adopt ranking metrics for evaluation, the primary metric is NDCG (Normalized Discounted Cumulative Gain), as well as recall and precision. The Bert encoder consists of three transfomer layers, the head number is four. The maximum sequence length is truncated to 300.

## Quality of Preference Scores

We first compare the performance between our model and a SOTA sequential recommendation model Bert4rec. As illustrated in Table.1, MCM_final significantly outperforms bert4rec by about 11%. We also conduct ablation experiments with variants of MCM model MCM_Single and MCM_MTL. Compared to Bert4rec, MCM_Single utilizs heterogeneous interaction sequence and contextual features to train each single task, and MCM_MTL utilizs attentional readout and MTL. MCM-Final utilizes heterogeneous data, attentional readout and pre-fix data augmentation. The results show that richer input signals contribute to the incrementality the most, while MTL and prefix augmentation are also helpful.

## Extensibility of MCM

To demonstrate the flexibility and extensibility of MCM, we give a detailed example showing how to modify and fine-tune the model on a next action recommendation use case. This task aims to encourage customers to complete one action task by providing incentives (e.g. cash backs). There are in total 28 tasks, including purchasing from a new product line (i.e., the product line that the customer never bought before) and trying new services like camera search or prime video streaming service. The multi-task prediction scores from MCM model have covered the tasks and can be directly utilized, however it may not reflect customers’ behaviors with incentives. So we add a new head on top of the sequential encoder to predict the incentive effect and fine-tune the model with customer behavior data under incentives: 30K action clicks and completion(conversion) records. From the results, MCM significantly outperforms a tree-based GBDT task prediction model by 25% on conversion NDCG, and fine-tuned model (MCM_finetuned) outperforms the MCM model without fine-tuning by 35% on conversion NDCG, which in total drives over 60% improvement on conversion rate as compared to tree-based GBDT model.

# Conclusion

In this paper, we introduce MCM, a large pre-trained customer model that serves as a sequential multi-task recommendation model to support diverse personalization projects. Through experiments, we demonstrate the model’s ability to provide highly accurate preference predictions, which surpass the performance of other baseline models. We also showcase a detailed use case on a recommendation project, demonstrating how MCM can be extended to new tasks and deliver significant performance improvements.

# Speaker bio

Rui Luo and Tianxin Wang are applied scientists in Amazon, they work on recommender systems to improve customer shopping experience.
